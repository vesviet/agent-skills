## AI Systems Engineer Review Checklist

This reference checklist provides detailed AI systems engineering, model serving infrastructure, accelerator virtualization, SLM distillation, and gateway governance criteria to meet 2026–2027 SOTA standards. It synthesizes high-throughput vLLM v1 PagedAttention serving, dynamic chunked prefill, Radix Tree prefix caching, NVIDIA MIG and Kubernetes 1.31+ DRA hardware slicing, DeepSeek-R1 SLM distillation, FastMCP tool integration, and LiteLLM spend governance.

### 1. High-Throughput Model Serving Engine (vLLM v1 C++ Core & Lock-Free IPC)
- **Standalone C++ Core Execution Loop**:
  - vLLM serving engine configured using v1 architecture (`VLLM_USE_V1=1`), decoupling request scheduling and batch allocation from Python GIL contention
  - inter-process communication between HTTP/gRPC frontend and engine core utilizes lock-free SPSC ring buffers over POSIX shared memory (`/dev/shm`), restricting scheduling step overhead to $\le 0.15\text{ms}$
  - Model FLOPs Utilization (MFU) on NVIDIA H100 SXM5 verified at $\ge 50\%$ across standard batch serving workloads
  - synchronous `torch.cuda.Event.query()` CPU polling loops eliminated in favor of asynchronous CUDA completion queues

### 2. Memory Virtualization & PagedAttention v3 (Hopper TMA & FP8 Slabs)
- **PagedAttention v3 Memory Bounds & Slab Layout**:
  - Key-Value (KV) cache partitioned into discrete physical blocks of size $B=32$ tokens, completely eliminating external memory fragmentation and restricting internal memory fragmentation to $<2.4\%$ across high-concurrency batches
  - Key-Value tensors quantized to FP8 (`--kv-cache-dtype fp8` / `fp8_e4m3`), halving byte footprint per token from 163.8 KB/tok to 81.9 KB/tok on 70B parameter models
  - Hopper Tensor Memory Accelerator (TMA) asynchronous memory transfers and Warp Specialization active (Producer warps issue TMA descriptors; Consumer warps execute FP8 Tensor Core GEMMs)
- **VRAM Utilization Safety Ceiling**:
  - `--gpu-memory-utilization` strictly capped between `0.88` and `0.90`
  - setting 0.95+ strictly rejected: batch burst activations and NCCL communication buffers cause unrecoverable CUDA OOM crashes

### 3. Dynamic Chunked Prefill & Head-of-Line Blocking Mitigation
- **Token Chunk Slicing & Iteration Budgets**:
  - dynamic chunked prefill enabled (`--enable-chunked-prefill=true`) with max batched tokens configured (`--max-num-batched-tokens 2048`)
  - long incoming prompts decomposed into bounded chunks ($C_{chunk} \in [512, 2048]$ tokens) interleaved with active decode steps
  - global iteration budget ($T_{budget} = 2048$) enforced to bound single-step GPU kernel execution time to $\le 25\text{ms}$
- **Latency SLAs & Jitter Verification**:
  - P99 Time-to-First-Token (TTFT) under concurrent burst prefill verified at $\le 100\text{ms}$
  - Time-Per-Output-Token (TPOT) tail jitter locked within $\pm 2.0\text{ms}$ (eliminating decode stalls caused by monolithic GEMM prefill bursts)

### 4. Hierarchical Prefix Caching & Radix Tree Block Management
- **Radix Tree Cache Traversal**:
  - automatic prefix caching enabled (`--enable-prefix-caching=true`) utilizing a memory-resident Radix Tree block manager rather than fragile all-or-nothing hash tables
  - multi-turn conversation branches and common system instructions share ancestor KV blocks via atomic reference counting
  - warm prompt prefix hit rate verified at $\ge 70\%$ in conversational workflows, reducing TTFT by up to $4.5\times$
- **High-Watermark LRU Pruning**:
  - memory pressure watermark set at 88% HBM utilization; leaf nodes pruned via adaptive LRU while preserving frequently referenced root system prompts

### 5. Multi-Tier Distributed KV Cache Offloading (RoCEv2 RDMA Fabric)
- **Four-Tier Storage Hierarchy**:
  - memory fabric configured across Tier 0 (GPU HBM3e, 4.8 TB/s), Tier 1 (Host NUMA DDR5, 64 GB/s via PCIe Gen5), Tier 2 (Local NVMe via io_uring / GPUDirect Storage, 14 GB/s), and Tier 3 (Remote Nodes via 400Gbps RoCEv2)
  - DeepSeek Multi-Head Latent Attention (MLA) compressed KV tensors ($d_c = 512, d_r = 64$) streamed across physical servers in $\le 3.5\text{ms}$ over 400Gbps RoCEv2 links
- **Kernel-Bypass GPUDirect RDMA Transfers**:
  - one-sided RDMA writes (`IBV_WR_RDMA_WRITE`) transfer KV slabs directly between GPU HBM and Mellanox ConnectX-7 NICs without host CPU kernel interruption
  - RoCEv2 Priority Flow Control (PFC) and DCQCN congestion notification enabled to eliminate packet loss

### 6. Hardware Virtualization, GPU Slicing & Kubernetes 1.31+ DRA
- **Hardware-Level Partitioning via NVIDIA MIG**:
  - multi-tenant or multi-workload GPU nodes enforce physical hardware slicing using NVIDIA Multi-Instance GPU (MIG, e.g. `nvidia.com/mig-3g.40gb`), providing isolated compute instances, memory controllers, and fault domains
  - software time-slicing on shared GPUs strictly prohibited in production inference to prevent cross-tenant CUDA OOM cascades
- **Kubernetes 1.31+ Dynamic Resource Allocation (DRA)**:
  - GPU resources claimed via Kubernetes 1.31+ DRA `ResourceClaim` / `ResourceClaimTemplate` objects using Common Expression Language (CEL) device selectors:
    ```yaml
    selector: "device.attributes['gpu.nvidia.com'].memory >= 40.GiB && device.attributes['gpu.nvidia.com'].architecture == 'Hopper'"
    ```
  - opaque integer GPU requests (`nvidia.com/gpu: 1`) without detailed VRAM capacity models rejected

### 7. Small Language Model (SLM) Knowledge Distillation & DeepSeek-R1 CoT
- **Reasoning-Enriched Synthetic Fine-Tuning**:
  - distillation datasets pair input queries with explicit reasoning chains (`<think>` tokens) and finalized answers extracted from DeepSeek-R1
  - fine-tuning executed via QLoRA 4-bit / 8-bit parameter-efficient methods on domain-specific corpora
- **Lossless Quantization & Accuracy Verification**:
  - quantized SLMs (AWQ / GGUF / FP8) must achieve $\ge 98.5\%$ benchmark accuracy relative to unquantized FP16 baselines before production release
  - reasoning consistency score on domain golden sets verified at $\ge 90\%$

### 8. Hybrid Edge/Cloud Inference Routing & Cost Optimization
- **Dynamic Complexity-Aware Router**:
  - inference router evaluates incoming query complexity and confidence scores ($\tau = 0.85$)
  - high-confidence, routine domain tasks routed to local/edge 7B SLMs ($0.08 / 1\text{M}$ tokens); ambiguous or high-complexity queries escalated to cloud frontier models
  - hybrid routing architecture verified to reduce aggregate token inference expenditures by $\ge 65\%$ while maintaining overall task accuracy

### 9. FastMCP Server Architecture & Streaming Tool Sandboxing
- **Model Context Protocol (MCP) Stream Transport**:
  - FastMCP servers implement JSON-RPC 2.0 streaming transport over Server-Sent Events (SSE) or stdio
  - tool definitions declare explicit JSON Schema input contracts and comprehensive parameter descriptions for LLM function calling
- **Progressive Component Streaming & Isolation**:
  - long-running tools emit intermediate progress fragments before LLM token generation concludes
  - client-side UI widgets rendered via Shadow DOM with strict Content Security Policy (CSP) nonces, preventing dynamic widgets from accessing host session storage or global DOM

### 10. Centralized AI Gateway Orchestration & LiteLLM Spend Governance
- **Centralized Gateway Choke Point**:
  - 100% of application and agent LLM calls route through centralized proxy gateways (LiteLLM, Portkey); direct provider calls using hardcoded API keys are a strict policy violation
  - gateway enforces automated multi-provider fallback chains (e.g. Anthropic Claude 3.5 Sonnet $\rightarrow$ OpenAI GPT-4o $\rightarrow$ local self-hosted vLLM) with exponential backoff
- **Token Budget Ceilings & FinOps Metadata**:
  - all requests carry mandatory cost-attribution headers (`x-team-id`, `x-service-name`, `x-budget-tier`)
  - autonomous agentic sessions bound to circuit breakers capping per-session token spend to $\le 10\%$ of the daily allocated budget to terminate circular execution loops

### 11. Structured Outputs & Constrained Decoding
- **Grammar-Based Constrained Decoding**:
  - machine-consumed model outputs enforce context-free grammar (CFG) constrained decoding (Outlines, XGrammar) at the engine level
  - regex post-processing and retry-on-parse-failure loops strictly prohibited for structured backend integration
  - JSON Schema contracts compiled and validated before token generation begins

### 12. Continuous Empirical Evaluation (CI/CD Evals)
- **Quantifiable Quality & Hallucination Gates**:
  - CI/CD release pipelines run automated evaluation suites (DeepEval, Ragas, promptfoo) against versioned golden benchmark datasets
  - release criteria enforced: hallucination rate $< 1.0\%$, factual grounding score $\ge 0.85$, semantic drift $< 0.05$
- **Adversarial Robustness & Jailbreak Testing**:
  - automated prompt injection and jailbreak stress test pass rate $\ge 98\%$ (OWASP LLM Top 10 & OWASP ASI01–ASI10)

### 13. GPU FinOps, DCGM Observability & Queue-Depth Autoscaling
- **Queue-Depth Driven HPA Autoscaling**:
  - Kubernetes Horizontal Pod Autoscaler (`autoscaling/v2`) scales on request queue depth custom metrics (`vllm:num_requests_waiting`, target: 5 requests per pod) and KV cache usage factor (`vllm:gpu_cache_usage_factor`, target: 0.80) via Prometheus Adapter
  - autoscaling based solely on GPU compute utilization (`DCGM_FI_DEV_GPU_UTIL`) strictly rejected: memory-bound autoregressive decoding leaves compute at 30–40% while queues saturate
- **OpenCost DCGM Metric Attribution**:
  - NVIDIA DCGM Prometheus exporters collect `DCGM_FI_DEV_GPU_UTIL` and `DCGM_FI_DEV_FB_USED`; OpenCost attributes hourly GPU costs per namespace and service
- **Shared Memory Volume Sizing**:
  - inference pods mount high-speed in-memory tmpfs on `/dev/shm` (minimum 16GiB: `emptyDir: { medium: Memory, sizeLimit: 16Gi }`), preventing PyTorch NCCL collective bus timeouts

### 14. Production Kubernetes AI Serving Deployment & StatefulSets
- **StatefulSet & System Capabilities**:
  - inference engine deployed via Kubernetes `StatefulSet` with dedicated headless service
  - container security context grants `IPC_LOCK`, `SYS_RAWIO`, and `NET_RAW` capabilities for RoCEv2 RDMA memory pinning and kernel bypass
- **HugePages & Storage Mounts**:
  - worker pods allocate $\ge 32\text{GiB}$ HugePages (`hugepages-2Mi: 32Gi`) for low-overhead RDMA memory registration
  - health check endpoints (`/health`) configured for liveness and readiness probes with initial delays accounting for model weight loading and warmup
