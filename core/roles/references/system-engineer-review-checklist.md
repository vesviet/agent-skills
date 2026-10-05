## System Engineer Review Checklist

This reference checklist provides operational systems architecture, kernel performance engineering, hardware virtualization, and capacity planning criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across measurable NFR translation, proactive capacity modeling, Linux kernel sysctl optimization, NUMA-aware compute architecture, GPU VRAM allocation modeling, Infrastructure as Code (IaC) source-of-truth governance, cross-layer cascading impact analysis, and event-driven autoscaling via KEDA.

### 1. Measurable NFR Derivation & Topology Architecture (`DESIGN-FIRST LOCK` / `NFR-MEASURABLE LOCK`)
- **Measurable Non-Functional Requirements**:
  - all system designs begin with explicit, quantifiable NFR targets: P99 latency (ms), peak throughput (req/s), availability (99.9x%), recovery time (RTO), and recovery point (RPO)
  - subjective or unmeasurable requirements (e.g. "high performance", "must be fast") rejected and returned for quantitative clarification
- **End-to-End System Topology**:
  - infrastructure topologies documented in `contracts/schemas/system-design-spec.json` with explicit compute tiers, network partitions, load balancer routing, storage layers, and message brokers
  - single points of failure (SPOF) identified and mitigated via multi-availability zone or active-active clustering

### 2. Proactive Capacity Modeling & Headroom Planning (`CAPACITY-BEFORE-INCIDENT LOCK`)
- **Multi-Horizon Capacity Projections**:
  - capacity models project resource demand across current baseline, 3-month P95 peak, and 12-month growth targets across CPU, memory, storage IOPS, and network bandwidth
  - minimum 30% headroom maintained across all primary compute and storage tiers; actionable scaling triggers defined for when utilization exceeds 70%
- **Database & Storage Scaling Limits**:
  - storage volume growth rates modeled with explicit alerts when free disk space falls below 20% or IOPS burst credits exhaust

### 3. Linux Kernel Sysctl Optimization & OS-Level Hardening
- **Network Stack & Socket Tuning**:
  - high-concurrency connection parameters configured and persisted in `/etc/sysctl.d/99-network.conf`:
    - `net.core.somaxconn = 65535`
    - `net.ipv4.tcp_max_syn_backlog = 65535`
    - `net.ipv4.tcp_tw_reuse = 1`
    - `net.ipv4.tcp_fin_timeout = 15`
  - system file descriptor limits tuned: `fs.file-max = 2097152` and `/etc/security/limits.conf` set to `nofile 1048576`
- **Memory Subsystem & Hugepages Configuration**:
  - virtual memory swappiness configured appropriately (`vm.swappiness = 10` for general services, `vm.swappiness = 1` for database engines)
  - Transparent Huge Pages (THP) disabled for latency-critical database workloads (Redis, PostgreSQL, MongoDB) to eliminate memory allocation stalls

### 4. Asynchronous I/O, Event Loops & NUMA Optimization
- **Kernel-Bypass & High-Performance I/O**:
  - high-throughput storage and network workloads utilize `io_uring` or `epoll` asynchronous event loops rather than blocking thread-per-connection architectures
  - disk I/O schedulers tuned: `none` or `mq-deadline` for NVMe/SSD storage volumes; `bfq` for traditional rotational disks
- **NUMA Node Alignment & CPU Core Pinning**:
  - multi-socket servers bind CPU threads and memory allocations to the same NUMA node (`numactl --cpunodebind=0 --membind=0`) to eliminate cross-QPI/UPI memory access latency penalties
  - network interface card (NIC) IRQ affinities pinned to CPU cores sharing the local PCIe root complex

### 5. AI Inference Infrastructure & GPU VRAM Accounting (`AI-INFRA-FIRST-CLASS LOCK` / `GPU-VRAM-ACCOUNTING LOCK`)
- **Formulaic VRAM Allocation Modeling**:
  - GPU allocation for LLM inference workloads must document the explicit formulaic calculation:
    $$\text{VRAM}_{\text{total}} = \text{Model Weights} + \text{KV Cache Slab} + \text{Activation Memory} + \text{Runtime Overhead}$$
  - minimum 15% VRAM headroom reserved to prevent CUDA out-of-memory (OOM) crashes during concurrent batch bursts
- **Hardware Slicing & Storage Topology**:
  - multi-tenant GPU nodes utilize NVIDIA Multi-Instance GPU (MIG) for physical compute and memory isolation
  - model weight distribution uses local NVMe caches or GPUDirect Storage to achieve model cold-start load times $\le 45\text{s}$

### 6. Infrastructure as Code (IaC) & Source of Truth (`IaC-SOURCE-OF-TRUTH LOCK`)
- **Zero Manual Configuration Drift**:
  - all operating system configurations, sysctl parameters, firewall rules, and container runtimes declared in version-controlled IaC (OpenTofu, Ansible, Crossplane)
  - manual hot-patching of production servers prohibited; changes applied via declarative pipelines
- **Automated Validation & Linting**:
  - IaC configurations validated via automated linters, syntax checkers, and security scans (TFLint, Trivy, Ansible-Lint) prior to pull request merge

### 7. Cross-Layer Impact Analysis & Destructive Action Controls (`CROSS-LAYER-IMPACT LOCK` / `IRREVERSIBLE-INFRA LOCK`)
- **Second-Order Dependency Assessment**:
  - changes to network MTU, TCP buffer sizes, or kernel parameters evaluated against downstream database connection pools and RPC runtimes
  - OS-level upgrades verified against container engine and kernel module compatibility matrices
- **Irreversible Infrastructure Protection**:
  - destructive infrastructure operations (terminating production compute, dropping persistent volumes, re-partitioning disks) mandate explicit human sign-off and validated snapshot backups

### 8. Observability & Event-Driven Autoscaling via KEDA (`OTEL-GENAI-REQUIRED LOCK` / `KEDA-NOT-HPA LOCK`)
- **OpenTelemetry Instrumentation**:
  - system nodes emit standard host and runtime metrics (node_exporter, OpenTelemetry Collector)
  - AI workloads emit standardized `gen_ai.*` OpenTelemetry spans including token usage and latency metrics
- **KEDA Event-Driven Scaling**:
  - inference and background queue workers scale via KEDA based on queue depth, request backlog, and KV cache utilization rather than deceptive CPU/memory metrics
