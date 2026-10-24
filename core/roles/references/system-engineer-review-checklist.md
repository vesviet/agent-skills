## System Engineer Review Checklist

This reference checklist provides operational systems architecture, kernel performance engineering, hardware virtualization, and capacity planning criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across measurable NFR translation, proactive capacity modeling, Linux kernel sysctl optimization, NUMA-aware compute architecture, GPU VRAM allocation modeling, Infrastructure as Code (IaC) source-of-truth governance, cross-layer cascading impact analysis, and event-driven autoscaling via KEDA.

### 1. Measurable NFR Derivation & Topology Architecture (`DESIGN-FIRST LOCK` / `NFR-MEASURABLE LOCK`)
- **Measurable Non-Functional Requirements**:
  - all system designs begin with explicit, quantifiable NFR targets: P99 latency (ms), peak throughput (req/s), availability (99.9x%), recovery time (RTO), and recovery point (RPO)
  - subjective or unmeasurable requirements (e.g. "high performance", "must be fast") rejected and returned for quantitative clarification
- **Little's Law Concurrent Capacity Formulation**:
  - baseline concurrency capacity modeled according to Little's Law:
    $$N_{\text{concurrent}} = \lambda \cdot W$$
    where $\lambda$ is average request arrival rate (requests/second) and $W$ is mean system residence time (seconds)
  - system architectures sized with $\ge 30\%$ headroom over peak projected concurrency ($N_{\text{provisioned}} \ge 1.3 \times N_{\text{peak}}$)
- **End-to-End System Topology**:
  - infrastructure topologies documented in `contracts/schemas/system-design-spec.json` with explicit compute tiers, network partitions, load balancer routing, storage layers, and message brokers
  - single points of failure (SPOF) identified and mitigated via multi-availability zone or active-active clustering

### 2. Proactive Capacity Modeling & Headroom Planning (`CAPACITY-BEFORE-INCIDENT LOCK`)
- **Multi-Horizon Capacity Projections**:
  - capacity models project resource demand across current baseline, 3-month P95 peak, and 12-month growth targets across CPU, memory, storage IOPS, and network bandwidth
  - minimum 30% headroom maintained across all primary compute and storage tiers; actionable scaling triggers defined for when utilization exceeds 70%
- **Storage IOPS & Queue-Depth Sizing**:
  - NVMe storage volumes provisioned with queue depths aligned to application worker concurrency; burst credit exhaustion alerts configured in monitoring

### 3. Linux Kernel 6.x Sysctl Optimization & OS-Level Hardening
- **Network Stack & High-Concurrency Socket Tuning**:
  - kernel networking parameters configured and persisted in `/etc/sysctl.d/99-performance.conf`:
    ```ini
    # High-concurrency socket backlog and connection reuse
    net.core.somaxconn = 65535
    net.ipv4.tcp_max_syn_backlog = 65535
    net.ipv4.tcp_tw_reuse = 1
    net.ipv4.tcp_fin_timeout = 15
    net.ipv4.tcp_slow_start_after_idle = 0
    net.core.rmem_max = 16777216
    net.core.wmem_max = 16777216
    
    # Virtual memory and file descriptors
    vm.swappiness = 10
    vm.max_map_count = 1048576
    vm.dirty_ratio = 15
    vm.dirty_background_ratio = 5
    fs.file-max = 2097152
    ```
  - `/etc/security/limits.conf` mandates `nofile 1048576` for service accounts
- **Transparent Huge Pages (THP) Tuning**:
  - Transparent Huge Pages (THP) disabled (`echo never > /sys/kernel/mm/transparent_hugepage/enabled`) for latency-critical database engines (Redis, PostgreSQL, OceanBase) to eliminate kernel compaction latency spikes

### 4. Asynchronous I/O, `io_uring` & NUMA Node Binding
- **Kernel-Bypass & High-Performance I/O (`io_uring`)**:
  - high-throughput storage and network workloads utilize `io_uring` with Submission Queue Polling (`IORING_SETUP_SQPOLL`) rather than blocking thread-per-connection architectures, eliminating userspace-to-kernel context switch overhead
  - disk I/O schedulers tuned: `none` or `mq-deadline` for NVMe SSDs; `bfq` for rotational media
- **NUMA Node Alignment & Core Pinning**:
  - multi-socket bare-metal and virtualized hosts bind CPU worker threads and memory allocations to the same NUMA node:
    ```bash
    # Execute high-throughput worker on NUMA node 0
    numactl --cpunodebind=0 --membind=0 /usr/local/bin/worker-service
    ```
  - NIC IRQ affinities pinned to CPU cores sharing the local PCIe root complex

### 5. Cgroup v2 Resource Controller Isolation
- **Hierarchical Resource Limits**:
  - production services enforce cgroup v2 controller boundaries:
    - `cpu.weight` set to prioritize latency-critical API paths over background jobs
    - `memory.high` configured as throttle watermark; `memory.max` as hard OOM boundary
    - `io.weight` configured to prevent disk-heavy batch tasks from starving database IOPS

### 6. AI Inference Infrastructure & GPU VRAM Accounting (`AI-INFRA-FIRST-CLASS LOCK` / `GPU-VRAM-ACCOUNTING LOCK`)
- **Formulaic VRAM Allocation Modeling**:
  - GPU allocation for LLM inference workloads must document the explicit formulaic calculation:
    $$\text{VRAM}_{\text{total}} = \text{Model Weights} + \text{KV Cache Slab} + \text{Activation Memory} + \text{Runtime Overhead}$$
  - minimum 15% VRAM headroom reserved to prevent CUDA out-of-memory (OOM) crashes during concurrent batch bursts
- **Hardware Slicing & Storage Topology**:
  - multi-tenant GPU nodes utilize NVIDIA Multi-Instance GPU (MIG) for physical compute and memory isolation
  - model weight distribution uses local NVMe caches or GPUDirect Storage to achieve model cold-start load times $\le 45\text{s}$

### 7. Cross-Layer Impact Analysis & Destructive Action Controls (`CROSS-LAYER-IMPACT LOCK` / `IRREVERSIBLE-INFRA LOCK`)
- **Second-Order Dependency Assessment**:
  - changes to network MTU, TCP buffer sizes, or kernel parameters evaluated against downstream database connection pools and RPC runtimes
  - OS-level upgrades verified against container engine and kernel module compatibility matrices
- **Irreversible Infrastructure Protection**:
  - destructive infrastructure operations (terminating production compute, dropping persistent volumes, re-partitioning disks) mandate explicit human sign-off and validated snapshot backups

### 8. Observability & Event-Driven Autoscaling via KEDA (`KEDA-NOT-HPA LOCK`)
- **KEDA Queue-Depth Driven Autoscaling**:
  - asynchronous message workers and inference fleets scale via KEDA ScaledObjects evaluating queue backlog and consumer lag rather than lagging CPU metrics:
    ```yaml
    apiVersion: keda.sh/v1alpha1
    kind: ScaledObject
    metadata:
      name: queue-worker-scaler
    spec:
      scaleTargetRef:
        name: queue-worker
      minReplicaCount: 2
      maxReplicaCount: 50
      triggers:
      - type: rabbitmq
        metadata:
          queueName: tasks
          mode: QueueLength
          value: "20"
    ```

### 9. Operational Telemetry & Health Invariants
- **PromQL System Health Invariants**:
  ```promql
  # Socket listen backlog drop detection
  rate(node_netstat_TcpExt_ListenDrops[5m]) > 0
  
  # NVMe I/O queue wait latency
  rate(node_disk_io_time_weighted_seconds_total[5m]) / rate(node_disk_reads_completed_total[5m] + node_disk_writes_completed_total[5m]) > 0.020
  ```

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Sysctl Conformance** | `somaxconn == 65535` | `sysctl net.core.somaxconn` | Returns 65535 |
| **VRAM Headroom** | Headroom $\ge 15\%$ | `nvidia-smi --query-gpu=memory.free` | Free VRAM $\ge 15\%$ total |
| **NUMA Locality** | Cross-node misses $\approx 0$ | `numastat -c worker-service` | Local node hits $\ge 98\%$ |
| **THP Disabled** | THP == never | `cat /sys/kernel/mm/transparent_hugepage/enabled` | `[never]` active |
| **cgroup v2 Controller**| Hierarchy valid | `cat /sys/fs/cgroup/cgroup.controllers` | `cpu memory io pids` active |
| **Listen Drop Rate**   | Drops == 0 | Prometheus `ListenDrops` | 0 drops across all sockets |
| **System Spec Schema** | Valid `system-design-spec.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
