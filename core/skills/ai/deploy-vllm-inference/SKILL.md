---
name: deploy-vllm-inference
description: Deploy, configure, scale, and optimize high-throughput LLM inference workloads using vLLM v1 PagedAttention. Use when serving self-hosted open models (DeepSeek-R1, Qwen2.5, Llama 3.3) on Kubernetes with Dynamic Resource Allocation (DRA), NVIDIA MIG slicing, dynamic chunked prefill, prefix caching, and multi-tier KV cache offloading.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Deploy vLLM Inference

Use this skill when deploying, configuring, scaling, and benchmarking production LLM serving workloads with the vLLM v1 engine on Kubernetes.

## When to Use

- deploying self-hosted open models (DeepSeek-R1, Qwen2.5, Llama 3.3) with vLLM v1
- configuring PagedAttention v3 with FP8 KV cache memory bounds (<2.4% fragmentation)
- configuring dynamic chunked prefill to eliminate decode latency jitter (TPOT)
- enabling hierarchical Radix Tree prefix caching for multi-turn conversations
- allocating GPU accelerators via Kubernetes 1.31+ Dynamic Resource Allocation (DRA) or NVIDIA MIG hardware slicing
- setting up queue-depth driven Horizontal Pod Autoscaling (HPA) via Prometheus metrics
- configuring high-speed `/dev/shm` tmpfs mounts and HugePages for RDMA RoCEv2 transfers

## Core Rules

- **Enforce vLLM v1 Architecture**: set `VLLM_USE_V1=1` to utilize the standalone C++ engine core and lock-free SPSC ring buffers over `/dev/shm`.
- **Dynamic Chunked Prefill**: enable chunked prefill (`--enable-chunked-prefill=true`, `--max-num-batched-tokens 2048`) to interleave prompt prefill chunks (512–2048 tokens) with decode steps, locking TPOT jitter within ±2.0ms.
- **Prefix Caching with Radix Trees**: enable `--enable-prefix-caching=true` with block size 32 (`--block-size 32`) to achieve $\ge 70\%$ cache hits on repeated prompts.
- **VRAM Utilization Safety Ceiling**: cap `--gpu-memory-utilization` between `0.88` and `0.90` to preserve headroom for PyTorch runtime activations and NCCL buffers.
- **Hardware Isolation**: multi-tenant inference must use NVIDIA MIG (`3g.40gb`) or Kubernetes 1.31+ DRA with CEL device selectors; software time-slicing on production inference is prohibited.
- **Queue-Depth Autoscaling**: autoscale pods on request queue depth (`vllm:num_requests_waiting`, target: 5), never solely on GPU compute utilization.
- **Mandatory tmpfs `/dev/shm`**: mount an in-memory `tmpfs` volume of at least 16GiB on `/dev/shm` to prevent NCCL bus deadlocks.
- refer to `references/vllm-production-guide.md` for production StatefulSet manifests, DRA ResourceClaims, and Prometheus HPA configs.

## Suggested Process

### 1. Calculate VRAM Capacity & Sizing Model
Model GPU memory requirements:
$$\text{VRAM}_{\text{total}} = \text{Weights}_{\text{FP8/FP16}} + \text{KV-Cache}_{\text{FP8}} + \text{Activation-Workspace} + \text{Safety-Headroom (12\%)}$$
For Llama-3.1-70B FP8 on 8x H100 (640GB total VRAM), allocate 70GB weights + 480GB KV cache + 90GB activation headroom.

### 2. Claim GPU via Kubernetes 1.31+ DRA or NVIDIA MIG
Declare a `ResourceClaim` requesting GPUs via CEL selectors:
```yaml
apiVersion: resource.k8s.io/v1alpha3
kind: ResourceClaim
metadata:
  name: vllm-h100-claim
spec:
  devices:
    requests:
      - name: gpu
        deviceClassName: gpu.nvidia.com
        selectors:
          - cel:
              expression: "device.attributes['gpu.nvidia.com'].memory >= 80.GiB"
```

### 3. Configure vLLM v1 Engine Parameters
Define CLI flags in container arguments:
```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3.1-70B-Instruct \
  --tensor-parallel-size 8 \
  --kv-cache-dtype fp8 \
  --block-size 32 \
  --max-num-batched-tokens 2048 \
  --enable-chunked-prefill true \
  --enable-prefix-caching true \
  --gpu-memory-utilization 0.90 \
  --port 8000
```

### 4. Deploy Kubernetes StatefulSet Manifest
Mount tmpfs `/dev/shm` (64GiB), HugePages (32GiB), and assign security capabilities (`IPC_LOCK`):
```yaml
volumeMounts:
  - name: dshm
    mountPath: /dev/shm
  - name: hugepages
    mountPath: /dev/hugepages
volumes:
  - name: dshm
    emptyDir:
      medium: Memory
      sizeLimit: 64Gi
  - name: hugepages
    emptyDir:
      medium: HugePages
```

### 5. Configure Queue-Depth Driven HPA Autoscaler
Bind HPA to custom queue depth metrics from Prometheus Adapter:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-inference-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: vllm-v1-h100-cluster
  minReplicas: 2
  maxReplicas: 8
  metrics:
    - type: Pods
      pods:
        metric:
          name: vllm_num_requests_waiting_per_pod
        target:
          type: AverageValue
          averageValue: "5"
```

### 6. Verify Engine Health, Throughput & Cache Telemetry
Verify endpoints via HTTP probes:
```bash
curl -f http://localhost:8000/health
curl -s http://localhost:8000/metrics | grep -E "vllm:num_requests_waiting|vllm:gpu_cache_usage_factor"
```

## Checklist

- [ ] Confirm vLLM v1 engine is enabled (`VLLM_USE_V1=1`) with C++ standalone core
- [ ] Verify `--enable-chunked-prefill=true` and `--max-num-batched-tokens 2048` are set
- [ ] Confirm `--enable-prefix-caching=true` is enabled with `--block-size 32`
- [ ] Validate `--gpu-memory-utilization` is capped between 0.88 and 0.90
- [ ] Verify container mounts tmpfs on `/dev/shm` with minimum 16GiB capacity
- [ ] Ensure multi-tenant GPU allocation uses NVIDIA MIG or K8s 1.31+ DRA CEL selectors
- [ ] Confirm HPA scales on request queue depth (`vllm_num_requests_waiting_per_pod`)

## Related Skills

- **setup-gpu-finops**: GPU capacity modeling, DCGM telemetry, and OpenCost attribution
- **setup-llm-gateway**: Centralized LiteLLM proxy routing, failover, and rate limiting
- **deploy-aws-eks-workloads**: Kubernetes deployment, Karpenter node provisioning, and Pod Identity
- **debug-runtime-platform**: Diagnosing pod crash loops, NCCL deadlocks, and container networking
- **add-telemetry-instrumentation**: OpenTelemetry Collector pipelines and GenAI semantic conventions
