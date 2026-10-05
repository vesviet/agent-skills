# Production vLLM v1 Deployment & High-Throughput Inference Guide

This reference guide provides production-grade architecture patterns, mathematical formulations, Kubernetes resource manifests, and observability configurations for deploying large language models with the vLLM v1 inference engine in enterprise environments.

---

## 1. Architectural Foundations: vLLM v0 vs vLLM v1

The vLLM v1 architecture redesigns the engine core to address the concurrency, latency jitter, and memory fragmentation bottlenecks inherent in Python-bound serving architectures.

```
+-------------------------------------------------------------------------------+
|                       HTTP / gRPC Ingress (FastAPI / Envoy)                  |
+---------------------------------------+---------------------------------------+
                                        | Zero-Copy Deserialization
                                        v
+-------------------------------------------------------------------------------+
|                    vLLM v1 C++ Engine Core (Process Isolated)                 |
|                                                                               |
|   +-----------------------+     Shared Memory      +----------------------+   |
|   |  Request Scheduler    | <====================> |  PagedBlockManager   |   |
|   |  (Chunked Prefill)    |    Lock-Free SPSC      |  (Radix Tree Cache)  |   |
|   +-----------------------+     Ring Buffers       +----------------------+   |
+---------------------------------------+---------------------------------------+
                                        | Asynchronous TMA Descriptors
                                        v
+-------------------------------------------------------------------------------+
|                   NVIDIA Hopper Architecture (H100 / H200 SXM5)               |
|                                                                               |
|   Producer Warps: Async TMA Load (HBM3e -> Shared Memory / Register File)    |
|   Consumer Warps: FP8 Tensor Core Matrix Multiply (Warp Specialization)       |
+-------------------------------------------------------------------------------+
```

### Key Architectural Shifts

1. **Decoupled C++ Engine Core (`VLLM_USE_V1=1`)**: Request scheduling, block allocation, and iteration execution run in a dedicated C++ process completely decoupled from the Python Global Interpreter Lock (GIL). This reduces scheduling step latency from $> 1.8\text{ms}$ in v0 to $< 0.15\text{ms}$ in v1.
2. **Lock-Free SPSC Ring Buffers**: Inter-process communication between HTTP frontend workers and the C++ engine core operates over POSIX shared memory (`/dev/shm`) using lock-free Single-Producer Single-Consumer (SPSC) ring buffers. Synchronous CPU polling loops (`torch.cuda.Event.query()`) are replaced with asynchronous CUDA completion queues.
3. **Hopper Warp Specialization & TMA**: KV cache operations on Hopper GPUs leverage Tensor Memory Accelerator (TMA) hardware for asynchronous, direct memory copies between High Bandwidth Memory (HBM3e) and Shared Memory (SMem), bypassing register files and CPU overhead. Producer warps issue TMA memory descriptors while consumer warps execute FP8 Tensor Core GEMMs concurrently.
4. **MFU Target**: High-throughput serving clusters achieve Model FLOPs Utilization (MFU) of $\ge 50\%$ on NVIDIA H100 SXM5 across large batch sizes ($B_{concurrency} \ge 128$).

---

## 2. Mathematical Modeling of PagedAttention v3 Memory Bounds

PagedAttention partitions the continuous Key-Value (KV) cache of autoregressive models into fixed-size physical memory slabs, analogous to virtual memory paging in operating systems.

### 2.1 Token Block Formulation

Let sequence $i$ have current context length $S_i$ tokens. The number of allocated physical blocks $N_{blocks}(i)$ is defined by:

$$N_{blocks}(i) = \left\lceil \frac{S_i}{B} \right\rceil$$

where $B$ is the block size ($B = 32$ tokens in PagedAttention v3).

### 2.2 Slab Memory Footprint

The memory footprint of a single physical block across all Transformer layers $L$ is given by:

$$\text{BlockSize}_{bytes} = 2 \times L \times H_{KV} \times D_{head} \times B \times \text{sizeof}(\text{dtype})$$

where:
- $L$ is the number of hidden transformer layers.
- $H_{KV}$ is the number of Key/Value attention heads (accounting for Grouped-Query Attention, GQA).
- $D_{head}$ is the attention head hidden dimension ($D_{head} = \frac{d_{model}}{H_{Q}}$).
- $\text{sizeof}(\text{dtype}) = 1\text{ byte}$ for FP8 (`fp8_e4m3`), or $2\text{ bytes}$ for FP16/BF16.

For Meta-Llama-3.1-70B-Instruct ($L = 80$, $H_{KV} = 8$, $D_{head} = 128$, $B = 32$):
- **FP16 KV Cache**: $\text{BlockSize}_{bytes} = 2 \times 80 \times 8 \times 128 \times 32 \times 2 = 10,485,760\text{ bytes} \approx 10.0\text{ MiB per block}$ ($327.68\text{ KB/token}$). Across Tensor Parallel size 8 ($TP=8$), this equals $40.96\text{ KB/token/GPU}$.
- **FP8 KV Cache**: $\text{BlockSize}_{bytes} = 2 \times 80 \times 8 \times 128 \times 32 \times 1 = 5,242,880\text{ bytes} \approx 5.0\text{ MiB per block}$ ($163.84\text{ KB/token}$). Across $TP=8$, this equals $20.48\text{ KB/token/GPU}$.

### 2.3 Memory Fragmentation Bounds

- **External Fragmentation**: Bounded to $0.0\%$. PagedAttention allocates non-contiguous physical blocks from a pre-allocated pool, eliminating external fragmentation entirely.
- **Internal Fragmentation**: Only the final block of an active sequence contains unwritten token slots. For sequence $i$, unused tokens in the tail block are:

$$U_i = (N_{blocks}(i) \times B) - S_i, \quad 0 \le U_i < B$$

The fraction of wasted memory $\Phi_i$ for sequence $i$ is strictly bounded by:

$$\Phi_i = \frac{U_i}{N_{blocks}(i) \times B} < \frac{B}{S_i}$$

For $B = 32$ and standard context length $S_i = 4096$:

$$\Phi_i < \frac{32}{4096} = 0.78125\%$$

Across concurrent workloads with mixed sequence lengths, internal fragmentation remains strictly $< 2.4\%$.

---

## 3. Dynamic Chunked Prefill & Iteration Scheduling Mechanics

Monolithic prompt prefill causes severe head-of-line blocking: when a 32,768-token prompt arrives, a monolithic scheduler monopolizes GPU Tensor Cores for $\sim 410\text{ms}$. During this window, all active decode streams stall, causing Time-Per-Output-Token (TPOT) to spike from $11\text{ms}$ to $> 180\text{ms}$ ($16\times$ jitter).

### 3.1 Token Chunk Formulation

Dynamic chunked prefill slices incoming prefill requests into bounded token chunks $c_p$ that interleave with active decode tokens within a global iteration token budget $T_{budget}$:

$$c_p = \min\left(U_p,\, C_{chunk},\, C_{avail}^{(k)}\right)$$

where:
- $U_p$ is remaining uncomputed tokens for prefill request $p$.
- $C_{chunk}$ is the maximum chunk size ($C_{chunk} \in [512, 2048]$, default: $1024$).
- $C_{avail}^{(k)} = T_{budget} - \sum_{d \in \mathcal{D}} 1 - \sum_{j < p} c_j$ is remaining token capacity in iteration $k$.
- $\mathcal{D}$ is the set of active decode requests.
- $T_{budget}$ is the global iteration token budget ($T_{budget} = 2048$).

```
Iteration k:
+-------------------------------------------------------------+
| Decode Tokens (64 reqs = 64 tokens) | Chunked Prefill (1984) |
+-------------------------------------------------------------+
<------------------------ T_budget = 2048 -------------------->
```

### 3.2 Performance Guarantees

- **TPOT Stability**: Interleaving bounded prefill slices restricts single-step GPU kernel execution time to $\le 25\text{ms}$, locking TPOT tail jitter within $\pm 1.8\text{ms}$.
- **TTFT Target**: Chunked prefill guarantees high scheduling fairness, maintaining P99 Time-to-First-Token (TTFT) $\le 100\text{ms}$ under concurrent burst arrivals.

---

## 4. Hierarchical Radix Tree Prefix Caching

Prefix caching avoids redundant computation by reusing KV cache blocks for prompts sharing common initial sequences (e.g., system prompts, few-shot examples, multi-turn dialogues).

### 4.1 Radix Tree Data Structure

Instead of static, flat hash tables, vLLM v1 uses a memory-resident Radix Tree:
- **Nodes**: Represent token sequences of variable length.
- **Edges**: Labeled by sub-sequences of token IDs.
- **Block Mapping**: Nodes map directly to physical PagedAttention block IDs with reference counters.
- **Branch Sharing**: Multi-turn dialogue branches split from common ancestor nodes without duplicating ancestor KV blocks.

### 4.2 Pruning & Eviction Policy

When GPU memory utilization reaches the high watermark ($88\%$ of physical KV cache capacity):
1. The block manager identifies nodes with reference count $\text{ref\_count} = 0$ (no active request currently generating from this prefix).
2. Eviction runs via Least-Recently-Used (LRU) order from leaf nodes toward root nodes.
3. Root nodes containing frequently referenced enterprise system instructions stay pinned in HBM, maintaining warm prefix cache hit rates $\ge 70\%$.

---

## 5. Multi-Tier Distributed KV Cache Offloading (RoCEv2 RDMA Fabric)

When local GPU HBM3e is saturated during high-concurrency peaks, KV slabs offload across a 4-tier storage hierarchy:

```
+-------------------------------------------------------------------------+
| Tier 0: GPU HBM3e              | 4.8 TB/s Bandwidth | Sub-Microsecond    |
+-------------------------------------------------------------------------+
                                    | PCIe Gen5 x16 (64 GB/s)
                                    v
+-------------------------------------------------------------------------+
| Tier 1: Host NUMA DDR5         | 64 GB/s Bandwidth  | Latency: ~15µs     |
+-------------------------------------------------------------------------+
                                    | GPUDirect Storage / io_uring
                                    v
+-------------------------------------------------------------------------+
| Tier 2: Local NVMe SSD         | 14 GB/s Bandwidth  | Latency: ~80µs     |
+-------------------------------------------------------------------------+
                                    | 400Gbps RoCEv2 (GPUDirect RDMA)
                                    v
+-------------------------------------------------------------------------+
| Tier 3: Remote Node Memory     | 46 GB/s Wire Speed | Latency: 3.4ms     |
+-------------------------------------------------------------------------+
```

### 5.1 Kernel-Bypass GPUDirect RDMA Transfers

1. **One-Sided Operations**: KV tensors are transferred between local GPU HBM and remote GPU memory via one-sided InfiniBand / RoCEv2 RDMA writes (`IBV_WR_RDMA_WRITE`).
2. **Zero Host CPU Involvement**: The host CPU is not interrupted during packet transfers; Mellanox ConnectX-7 NICs interact directly with GPU HBM via PCIe Gen5 switches.
3. **Lossless Fabric**: Priority Flow Control (PFC, IEEE 802.1Qbb) on priority 3 and Data Center Quantized Congestion Notification (DCQCN) eliminate packet drops and head-of-line blocking across the 400Gbps network fabric.

---

## 6. Kubernetes 1.31+ Dynamic Resource Allocation (DRA) & NVIDIA MIG

### 6.1 Kubernetes 1.31+ DRA `ResourceClaimTemplate`

Declare accelerator requirements declaratively using Common Expression Language (CEL) selectors matching GPU topology and memory capacity:

```yaml
apiVersion: resource.k8s.io/v1alpha3
kind: ResourceClaimTemplate
metadata:
  name: vllm-h100-dra-template
  namespace: ai-inference
spec:
  spec:
    devices:
      requests:
        - name: gpu-cluster
          deviceClassName: gpu.nvidia.com
          count: 8
          selectors:
            - cel:
                expression: >-
                  device.attributes['gpu.nvidia.com'].architecture == 'Hopper' &&
                  device.attributes['gpu.nvidia.com'].memory >= 80.GiB &&
                  device.attributes['gpu.nvidia.com'].interconnect == 'NVLink'
```

### 6.2 Multi-Instance GPU (MIG) Slicing

For smaller models (e.g. 7B–14B SLMs) or multi-tenant workloads, physical hardware partitioning via NVIDIA Multi-Instance GPU (MIG) enforces hardware-level fault isolation:

- **Profile**: `nvidia.com/mig-3g.40gb` (3 GPU Compute Instances, 40GB dedicated HBM3e, 4 memory controllers).
- **Isolation**: Each slice possesses dedicated streaming multiprocessors (SMs), memory controllers, crossbar paths, and DMA engines. Software time-slicing is strictly prohibited in production inference to eliminate noisy-neighbor latency cascades and cross-tenant CUDA OOMs.

---

## 7. Complete Production Kubernetes StatefulSet Manifest

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vllm-llama3-70b-v1
  namespace: ai-inference
  labels:
    app.kubernetes.io/name: vllm-inference
    app.kubernetes.io/part-of: ai-platform
    model: meta-llama-3.1-70b-instruct
spec:
  serviceName: vllm-llama3-70b-headless
  replicas: 2
  podManagementPolicy: Parallel
  selector:
    matchLabels:
      app.kubernetes.io/name: vllm-inference
  template:
    metadata:
      labels:
        app.kubernetes.io/name: vllm-inference
        model: meta-llama-3.1-70b-instruct
        team-id: enterprise-ai
        service-name: llm-serving
        budget-tier: production-high
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
        k8s.v1.cni.cncf.io/networks: '[{"name": "rocev2-net", "interface": "net1"}]'
    spec:
      priorityClassName: system-cluster-critical
      terminationGracePeriodSeconds: 120
      containers:
        - name: vllm-engine
          image: vllm/vllm-openai:v0.7.2
          imagePullPolicy: IfNotPresent
          env:
            - name: VLLM_USE_V1
              value: "1"
            - name: NCCL_DEBUG
              value: "WARN"
            - name: NCCL_IB_DISABLE
              value: "0"
            - name: NCCL_IB_HCA
              value: "mlx5_0,mlx5_1"
            - name: NCCL_IB_GID_INDEX
              value: "3"
            - name: NCCL_NET_GDR_LEVEL
              value: "5"
            - name: HF_HUB_ENABLE_HF_TRANSFER
              value: "1"
            - name: MODEL_NAME
              value: "meta-llama/Meta-Llama-3.1-70B-Instruct"
          args:
            - "--model=$(MODEL_NAME)"
            - "--tensor-parallel-size=8"
            - "--kv-cache-dtype=fp8"
            - "--block-size=32"
            - "--max-num-batched-tokens=2048"
            - "--max-num-seqs=256"
            - "--enable-chunked-prefill=true"
            - "--enable-prefix-caching=true"
            - "--gpu-memory-utilization=0.90"
            - "--swap-space=16"
            - "--disable-log-requests"
            - "--port=8000"
          resources:
            claims:
              - name: gpu-cluster
            requests:
              cpu: "32"
              memory: "256Gi"
              hugepages-2Mi: "32Gi"
            limits:
              cpu: "64"
              memory: "384Gi"
              hugepages-2Mi: "32Gi"
          securityContext:
            capabilities:
              add:
                - IPC_LOCK
                - SYS_RAWIO
                - NET_RAW
            readOnlyRootFilesystem: false
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          volumeMounts:
            - name: dshm
              mountPath: /dev/shm
            - name: hugepages
              mountPath: /dev/hugepages
            - name: model-cache
              mountPath: /root/.cache/huggingface
          startupProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 10
            failureThreshold: 30
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            periodSeconds: 15
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2
      volumes:
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: 64Gi
        - name: hugepages
          emptyDir:
            medium: HugePages
        - name: model-cache
          persistentVolumeClaim:
            claimName: model-cache-pvc
      resourceClaims:
        - name: gpu-cluster
          resourceClaimTemplateName: vllm-h100-dra-template
```

---

## 8. Prometheus Custom Metric HorizontalPodAutoscaler (HPA)

Autoregressive LLM generation is fundamentally memory-bandwidth bound. Scaling purely on GPU compute utilization (`DCGM_FI_DEV_GPU_UTIL`) fails because compute utilization hovers around 30%–45% during decode iterations even as incoming requests accumulate in queues.

Inference autoscaling must scale on **queue depth** and **KV cache utilization**.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-queue-hpa
  namespace: ai-inference
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: vllm-llama3-70b-v1
  minReplicas: 2
  maxReplicas: 12
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60
      selectPolicy: Min
  metrics:
    - type: Pods
      pods:
        metric:
          name: vllm_num_requests_waiting_per_pod
        target:
          type: AverageValue
          averageValue: "5"
    - type: Pods
      pods:
        metric:
          name: vllm_gpu_cache_usage_factor_per_pod
        target:
          type: AverageValue
          averageValue: "800m"
```

---

## 9. NVIDIA DCGM Prometheus Metric Queries & Grafana Alerting Rules

### 9.1 Essential PromQL Queries

1. **Queue Saturation (Waiting Requests per Pod)**:
   ```promql
   sum by (pod) (vllm:num_requests_waiting{namespace="ai-inference"})
   ```

2. **KV Cache Memory Utilization Factor**:
   ```promql
   avg by (pod) (vllm:gpu_cache_usage_factor{namespace="ai-inference"}) * 100
   ```

3. **Prefix Cache Hit Rate Percentage**:
   ```promql
   (
     sum by (pod) (rate(vllm:prefix_cache_hits_total[5m]))
     /
     sum by (pod) (rate(vllm:prefix_cache_queries_total[5m]))
   ) * 100
   ```

4. **Normalized Token Generation Throughput (Tokens/sec)**:
   ```promql
   sum by (model) (rate(vllm:generation_tokens_total[2m]))
   ```

5. **P99 Time-to-First-Token (TTFT)**:
   ```promql
   histogram_quantile(0.99, sum by (le, model) (rate(vllm:time_to_first_token_seconds_bucket[5m])))
   ```

6. **P99 Time-Per-Output-Token (TPOT)**:
   ```promql
   histogram_quantile(0.99, sum by (le, model) (rate(vllm:time_per_output_token_seconds_bucket[5m])))
   ```

7. **DCGM GPU High-Bandwidth Memory (HBM) Utilization**:
   ```promql
   (
     DCGM_FI_DEV_FB_USED{model="meta-llama-3.1-70b-instruct"}
     /
     (DCGM_FI_DEV_FB_USED{model="meta-llama-3.1-70b-instruct"} + DCGM_FI_DEV_FB_FREE{model="meta-llama-3.1-70b-instruct"})
   ) * 100
   ```

### 9.2 Grafana Alerting Rules

- **Alert: `InferenceQueueSaturationCritical`**
  - **Condition**: `sum(vllm:num_requests_waiting) > 25 for 1m`
  - **Severity**: `critical`
  - **Mitigation**: Trigger immediate HPA burst scale-out; enable LiteLLM fallback to cloud provider.
- **Alert: `KVCacheExhaustionImminent`**
  - **Condition**: `avg(vllm:gpu_cache_usage_factor) > 0.95 for 30s`
  - **Severity**: `page`
  - **Mitigation**: Shed batch prefill load; prune unpinned prefix cache blocks; shed lowest priority tenants.
- **Alert: `TPOTLatencyJitterBreach`**
  - **Condition**: `histogram_quantile(0.99, sum by (le)(rate(vllm:time_per_output_token_seconds_bucket[5m]))) > 0.035 for 2m`
  - **Severity**: `warning`
  - **Mitigation**: Audit dynamic chunked prefill settings; verify `--max-num-batched-tokens` is not exceeded.
