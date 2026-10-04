## DevOps Engineer Review Checklist

This reference checklist provides detailed platform engineering, delivery safety, infrastructure-as-code, and runtime verification criteria for DevOps engineering to meet 2026–2027 SOTA standards. It synthesizes The Great Architectural Convergence across declarative universal control planes, progressive canary delivery, sidecarless service mesh, deep eBPF observability, cloud-native AI/GPU infrastructure, cryptographic supply chain provenance, and Senior Team Lead Kubernetes development debugging standards.

### 1. Declarative GitOps & Universal Control Plane (ArgoCD SSA & Crossplane)
- **Server-Side Apply (SSA) & Closed-Loop Reconciliation**:
  - all Kubernetes workloads deployed via ArgoCD v2.12+ enforcing Server-Side Apply (`syncOptions: [ServerSideApply=true]`) to transfer field management to Kubernetes API Server, completely eliminating 264KB `kubectl.kubernetes.io/last-applied-configuration` annotation limits and race conditions
  - automated drift detection and reconciliation configured with `RespectIgnoreDifferences=true`, `ApplyOutOfSyncOnly=true`, and `PruneLast=true`
  - explicit `ignoreDifferences` rules configured for dynamically mutated fields (e.g. HPA `/spec/replicas`, admission webhook annotations, dynamic token timestamps)
  - explicit `syncWaves` (e.g., Wave -1: namespaces/CRDs, Wave 0: secrets/configmaps, Wave 1: storage/stateful workloads, Wave 2: stateless deployments/rollouts, Wave 3: ingress/monitoring) and lifecycle phase hooks (`PreSync`, `Sync`, `PostSync`, `SyncFail`) governing multi-tier dependencies; zero manual out-of-band `kubectl apply` in production
- **ApplicationSets & Dynamic Fleet Fan-Out**:
  - standardized `ApplicationSet` manifests combining Git directory discovery (`apps/services/*`) and Matrix/List generators (`staging`, `production`) using Go templating (`goTemplate: true`, `goTemplateOptions: ["missingkey=error"]`)
  - progressive sync waves and rolling update strategies configured within ApplicationSets to prevent thundering-herd API server exhaustion during mass fleet synchronizations
- **Crossplane v1.16+ Compositions as Code**:
  - cloud infrastructure managed as Kubernetes custom resources via Composite Resource Definitions (XRDs); platform teams expose high-level schemas, shielding developers from raw cloud provider parameter complexity
  - Crossplane Compositions powered by compiled Go (`function-go-templating`) or KCL (`function-kcl`) functions, replacing fragile YAML patch-and-transform with compile-time type validation, conditionals, and deterministic loops
  - continuous closed-loop reconciliation actively correcting out-of-band cloud drift against desired XRD state
- **Controller Scale & Reconciliation Storm Prevention**:
  - ArgoCD controller deployed with dynamic sharding (`ARGOCD_CONTROLLER_SHARDING_METHOD="consistent-hashing"`) across $\ge 3$ replicas to distribute application workqueues
  - client-go rate limits tuned to `ARGOCD_K8S_CLIENT_QPS="300"` and `ARGOCD_K8S_CLIENT_BURST="600"` to prevent API Priority and Fairness (APF) request shedding
  - `argocd-repo-server` mounted on in-memory `tmpfs` volume with 24-hour commit-SHA caching (`ARGOCD_REPO_CACHE_EXPIRATION="24h"`) and Redis HA with gzip compression to handle fleets $> 5,000$ applications without OOM crashes

### 2. Secret Management & Client-Side State Encryption (Vault, ESO, OpenTofu KMS)
- **External Secrets Operator (ESO v1beta1) Declarative Sync**:
  - zero plaintext, base64-encoded, or encrypted secrets committed to Git repositories; all sensitive credentials synchronized declaratively via `ExternalSecret` manifests referencing namespace-scoped `SecretStore`
  - authentication to upstream secret vaults (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) leverages short-lived Kubernetes ServiceAccount OIDC tokens or AWS IAM Roles for Service Accounts (IRSA); hardcoded static tokens or long-lived IAM keys strictly prohibited
  - wildcard cluster-wide `ClusterSecretStore` prohibited; secret synchronization intervals (`refreshInterval: 1h`) configured with automated secret rotation handling and Prometheus drift alerting
- **OpenTofu v1.8+ Client-Side State Encryption**:
  - IaC state files (`.tfstate`) and plan files encrypted in-memory client-side using OpenTofu v1.8+ before transmitting bytes to remote S3/GCS/HTTP backends
  - encryption keys managed through AWS KMS (`aws_kms`), GCP KMS, or HashiCorp Vault using authenticated AES-GCM (256-bit); unencrypted state storage in remote S3 buckets blocked via bucket policy and IaC policy-as-code gates
  - key rotation policies enforced at KMS provider level without requiring state re-encryption downtime
- **Pipeline Push Protection & Secret Scanning**:
  - automated pre-commit hooks and CI/CD secret scanning (Gitleaks, TruffleHog) active across all repository branches to catch high-entropy credentials before commit
  - GitHub Advanced Security Secret Scanning Push Protection or GitLab Secret Detection enabled across all repositories to reject secret leaks at push time

### 3. Progressive Delivery & MetricAnalysis Canary Gates (Argo Rollouts & PromQL)
- **Argo Rollouts Canary Traffic Splitting**:
  - deployments configured with Argo Rollouts (`argoproj.io/v1alpha1 Rollout`) replacing static `Deployment` objects; step-based progressive traffic shifting (e.g. 10% → 25% → 50% → 100%) integrated with Cilium L7 or Istio `VirtualService` / Gateway API
  - explicit pause intervals (`pause: {duration: 5m}`) between steps to accumulate statistically significant metric telemetry before advancing
- **Prometheus MetricAnalysis Gates & Verification Criteria**:
  - automated `AnalysisTemplate` checks bound to rollouts evaluating P99 latency (threshold: $< 250\text{ms}$, `result[0] < 0.250`) and HTTP 5xx error rate (threshold: $< 1.0\%$, `result[0] < 1.0`)
  - consecutive failure limits (`failureLimit: 2`) and evaluation intervals (`interval: 30s`, `count: 10`) configured to trigger automated abort and emergency rollback upon metric breach
- **PromQL Zero-Traffic Vector-Drop Coalescing**:
  - metric queries implement empty vector coalescing (`or on() vector(0)`) to guard against false rollbacks during low-traffic maintenance windows when zero requests drop the evaluation vector:
    ```promql
    (
      (
        sum(rate(http_requests_total{job="kubernetes-service-endpoints", service="{{ args.service-name }}", status=~"5.*"}[2m]))
        or vector(0)
      )
      /
      (
        (sum(rate(http_requests_total{job="kubernetes-service-endpoints", service="{{ args.service-name }}"}[2m])) > 0)
        or vector(1)
      )
      * 100
    ) or on() vector(0)
    ```
  - P99 latency queries using `histogram_quantile(0.99, ...)` similarly protected with `or on() vector(0)` to prevent undefined vector evaluation errors

### 4. Sidecarless Service Mesh & Kernel Networking (Cilium eBPF & Istio Ambient)
- **Sidecarless Architecture & Resource Efficiency**:
  - zero intrusive Envoy sidecars injected into application pods; Layer 4 mutual TLS (mTLS) enforced at the node kernel layer via Cilium eBPF socket redirection (`sockops`) or Istio Ambient `ztunnel` over HBONE (HTTP/2 Based Overlay Network Encapsulation, port 15008)
  - pod memory footprint reduced by 60–80% compared to traditional sidecar meshes; application restarts eliminated during mesh control plane upgrades
- **L7 Waypoint Proxies On-Demand**:
  - Layer 7 routing, retries, header manipulation, and JWT authentication isolated to dedicated, per-namespace or per-service-account Waypoint proxies (`istio.io/use-waypoint`), provisioned only where L7 policies are strictly required
- **Path MTU & Redirection Loop Prevention**:
  - Geneve/VXLAN overlay networks explicitly configured with clamped MTU (1,450 bytes on standard 1,500-byte physical networks) and TCP MSS clamping (`bpf.clamp-mss: true`) to prevent MTU black-hole packet drops with `DF` (Don't Fragment) flag set
  - ambient redirection rules explicitly exclude HBONE port 15008 and 15021 (`ISTIO_INBOUND_PORTS: "*,!15008,!15021"`) to prevent kernel packet encapsulation loops
  - dynamic BPF connection tracking maps sized to $\ge 524,288$ entries (`bpf-ct-global-any-max: 524288`) to avoid `-ENOSPC` map exhaustion under high connection churn

### 5. Deep Observability & OTel Collector Pipeline Architecture
- **OpenTelemetry Collector Contrib Processor Pipeline Order**:
  - `memory_limiter` processor declared as the absolute **first processor** in every trace, log, and metric pipeline to guarantee load shedding before buffer allocation:
    ```yaml
    processors: [memory_limiter, k8sattributes, tail_sampling, batch]
    ```
  - declaring `memory_limiter` after `tail_sampling` is an anti-pattern that buffers spans until cgroup OOM kills the collector pod (exit code 137)
  - memory limiter configured with `check_interval: 1s`, `limit_percentage: 75`, and `spike_limit_percentage: 15` relative to container memory limits
- **Tail-Based Sampling Configuration**:
  - sampling decisions deferred until full trace completion; 100% of errors (`status_code: ERROR`, HTTP 5xx, gRPC error codes) and high-latency traces (`threshold_ms: 500`) retained, while healthy traces probabilistically downsampled (e.g. 5.0%)
  - `decision_wait` capped at 5s–10s to prevent collector memory exhaustion; upstream routing tier deploys `loadbalancingexporter` hashing on `trace_id` so all spans for a trace arrive at the same collector pod
- **W3C Trace Propagation & GenAI Semantic Conventions**:
  - unbroken propagation of W3C `traceparent` and `tracestate` headers across HTTP, gRPC, and asynchronous message queues (Kafka, RabbitMQ)
  - AI and LLM inference workloads instrumented using stable OpenTelemetry GenAI semantic conventions (v1.28+, `OTEL_SEMCONV_STABILITY_OPT_IN=genai`) tracking `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, and `gen_ai.usage.output_tokens`

### 6. Kernel-Level Runtime Security & Forensics (Cilium Tetragon & Hubble)
- **In-Kernel Synchronous Enforcement (Tetragon)**:
  - Tetragon `TracingPolicy` hooks attached to kernel system calls (`sys_execve`) and LSM hooks (`security_bprm_check`); synchronous in-kernel termination (`Sigkill`) triggered immediately upon detection of unauthorized interactive shells (`/bin/sh`, `/bin/bash`, `/bin/ash`, `/bin/zsh`), scripting runtimes (`/usr/bin/python`, `/usr/bin/perl`), or network utilities (`/usr/bin/nc`, `/usr/bin/netcat`) in production namespaces before execution returns to userspace
  - scoped filtering enforced via `matchBinaryNames` and namespace filters; generic unscoped kprobes on high-volume IO calls (`sys_enter_read`, `sys_enter_write`, `sys_enter_close`) strictly prohibited to avoid ring buffer saturation
- **Kernel Platform Prerequisites**:
  - worker nodes enforce Linux kernel $\ge 5.15$ LTS with BPF Type Format (BTF) enabled to prevent instruction ceiling limit verifier rejections (4,096 instruction ceiling on kernel $< 5.15$ vs 1,000,000 on 5.15+)
  - Tetragon Helm values allocate $\ge 32\text{MB}$ BPF ring buffer (`bpf.mapSizes.ringBuffer: 33554432`)
- **Hubble L7 Protocol Flow Observability**:
  - Hubble L7 protocol parsing enabled for HTTP, gRPC, DNS, and Kafka flows without sidecar proxies; flow records exported via Hubble Relay gRPC server to OpenTelemetry Collector and Grafana
  - egress `CiliumNetworkPolicy` rules enforce DNS domain regex filtering (FQDN policies) to prevent unauthorized command-and-control communication and data exfiltration

### 7. Internal Developer Platforms & Self-Service Golden Paths (Backstage & Score)
- **Platform-as-a-Product & Golden Path Blueprints**:
  - infrastructure provisioning exposed via self-service Golden Paths; ad-hoc individual team provisioning tickets rejected
  - Golden Path templates encode security, observability (OTel), and GitOps by default; time-to-provision for new microservices targeted at $< 30$ minutes
- **Declarative Workload Intent via Score YAML**:
  - workload intent declared using environment-agnostic `score.yaml` specifications describing service containers, ports, dependencies (`type: postgres`, `type: redis`), and resource requests
  - Score CLI and providers translate workload intent into Compose for local development (`score-compose`) and Helm/ArgoCD manifests for Kubernetes (`score-k8s`) without developer manifest duplication
- **Backstage v1.30+ Dynamic Plugins & Catalog Ingestion**:
  - service catalog maintains ownership, repository references, API contracts, and health scorecards; dynamic plugins loaded at runtime without rebuilding Backstage frontend container images
  - event-driven catalog ingestion via Git push webhooks (`/api/catalog/refresh`) replaces periodic full-org polling to prevent database lock contention on PostgreSQL entities tables
- **Kratix Promises & Radius Recipes**:
  - cloud capabilities packaged as Kratix Promises bundling CRDs, containerized request/configure pipelines, and GitOps state store placements
  - Radius Universal Control Plane (UCP) decouples infrastructure recipes (Bicep/Terraform) from application topology, enabling self-service database/cache provisioning without cloud provider lock-in

### 8. Cloud-Native AI Model Serving & Distributed Orchestration (KubeRay & vLLM)
- **High-Throughput Model Serving (vLLM on RayService)**:
  - distributed LLM inference clusters orchestrated via KubeRay `RayService` running vLLM; worker pods deploy high-throughput PagedAttention engines
  - `--gpu-memory-utilization` capped at `0.88` to `0.90` to reserve dedicated VRAM headroom for dynamic PyTorch runtime activations, CUDA context overhead, and NCCL buffers; setting 0.95+ triggers CUDA OOM under batch spikes
- **PagedAttention & Prefix Caching Optimization**:
  - `--enable-chunked-prefill` and `--enable-prefix-caching` enabled to eliminate redundant prompt processing on repeated system instructions and multi-turn conversations
  - block size tuning (`--block-size 16` or `32`) aligned with workload prompt length distribution to minimize internal KV-cache fragmentation
- **High-Speed Shared Memory (`/dev/shm`)**:
  - high-speed in-memory `tmpfs` volume mounted on `/dev/shm` (minimum 16GiB: `emptyDir: { medium: Memory, sizeLimit: 16Gi }`) across all inference worker pods; default Docker 64MB `/dev/shm` causes immediate NCCL bus deadlocks during inter-process tensor transfers

### 9. Hardware Virtualization, GPU Slicing & Queue-Depth Autoscaling (MIG, DRA, HPA)
- **Hardware-Level GPU Partitioning (NVIDIA MIG)**:
  - multi-tenant or multi-workload GPU nodes enforce physical hardware slicing using NVIDIA Multi-Instance GPU (MIG, e.g. `nvidia.com/mig-3g.40gb`), providing isolated compute instances, memory controllers, and fault domains; unpartitioned time-sharing on production inference strictly prohibited to avoid noisy-neighbor CUDA OOM cascades
- **Dynamic Resource Allocation (DRA K8s 1.31+)**:
  - GPU resources claimed via Kubernetes 1.31+ DRA `ResourceClaim` objects using Common Expression Language (CEL) device selectors (`device.attributes['gpu.nvidia.com'].memory >= 40.GiB`), matching specific hardware architectures, memory tiers, and topology-aware NVLink interconnects
- **Queue-Depth Driven HPA Autoscaling**:
  - Horizontal Pod Autoscalers (`autoscaling/v2`) driven by PrometheusAdapter custom metrics tracking request queue depth (`vllm:num_requests_waiting` target: 5) and KV cache saturation (`vllm:gpu_cache_usage_factor` target: 0.80)
  - autoscaling based solely on raw GPU compute utilization (`DCGM_FI_DEV_GPU_UTIL`) strictly rejected: transformer memory-bandwidth decoding stalls leave Tensor Cores at 30–40% utilization while request queues are completely saturated

### 10. AI FinOps, Cost Attribution & LLM Gateway Choke Point (OpenCost & LiteLLM)
- **Centralized LLM Gateway Choke Point**:
  - 100% of application LLM calls route through centralized proxy gateways (LiteLLM, Portkey); direct calls to model provider endpoints using hardcoded API keys are a strict policy violation
  - gateway enforces per-tenant token rate limits, automated multi-provider failover fallbacks (primary → secondary → tertiary model), and provider credential vaulting
- **Shift-Left FinOps & Metadata Tagging**:
  - CI/CD pipelines block deployments lacking mandatory cost attribution headers (`x-team-id`, `x-service-name`, `x-budget-tier`) on LLM requests
  - agentic circuit breakers configured to cap per-session token expenditure ($\le 10\%$ of daily budget) to terminate autonomous agent infinite loops
- **OpenCost DCGM GPU Cost Allocation**:
  - OpenCost deployed with NVIDIA DCGM Prometheus exporter metrics (`DCGM_FI_DEV_GPU_UTIL`, `DCGM_FI_DEV_FB_USED`); all GPU workloads labeled with mandatory `cost-center` and `team` tags for namespace-level billing attribution and Value-Per-Token scorecard generation

### 11. Cryptographic Supply Chain Security & Provenance (SLSA, Syft SBOM, Cosign Keyless)
- **SLSA Level 3+ Build Provenance**:
  - container images built inside isolated, ephemeral CI/CD environments generating cryptographic SLSA Level 3+ build provenance attestations (`https://slsa.dev/provenance/v0.2`)
  - third-party GitHub Actions and build tools pinned to immutable 40-character commit SHAs, never mutable branch or tag names (`uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`)
- **Software Bill of Materials (SBOM) Generation**:
  - comprehensive Syft SPDX 2.3 (`spdx-json=sbom.spdx.json`) or CycloneDX 1.6 SBOM generated for every build artifact at compile time; SBOM attached as signed in-toto OCI attestation via Cosign (`cosign attest --type spdxjson --predicate sbom.spdx.json`)
  - MCP servers and external agent skills audited for supply-chain provenance and included in SBOM with SCA scrutiny
- **Keyless Signing via Sigstore Cosign**:
  - container images and SBOM attestations signed keylessly using Cosign via Fulcio OpenID Connect (OIDC) identity tokens and recorded in Rekor transparency logs (`https://rekor.sigstore.dev`)
  - short-lived OIDC tokens ($\le 10$ min TTL) requested immediately prior to signing; unsigned or unverified container images treated as completely undeployable

### 12. Policy-as-Code & Fail-Closed Admission Enforcement (Kyverno Strict)
- **Fail-Closed Admission Controller Architecture**:
  - Kyverno admission controllers deployed across failure zones with $\ge 3$ replicas, `PodDisruptionBudget` (`minAvailable: 2`), and `priorityClassName: system-cluster-critical`
  - all production image validation policies enforce `failurePolicy: Fail` and `validationFailureAction: Enforce`; `failurePolicy: Ignore` strictly prohibited on security policies to prevent unverified containers from bypassing admission during controller restarts
- **Image Signature & Digest Verification**:
  - Kyverno `ClusterPolicy` verifies Cosign keyless signatures against Rekor transparency logs before admitting pods; unsigned images blocked unconditionally
  - automated tag-to-digest mutation (`mutateDigest: true`) enforced to convert mutable tags (`:latest`, `:hotfix`) into immutable cryptographic SHA256 digests
- **Minimal Distroless Attack Surface**:
  - all containerized microservices utilize Wolfi or Chainguard distroless base images; package managers (`apk`, `apt`), interactive shells (`/bin/sh`, `/bin/bash`), and non-essential system utilities completely stripped from runtime images, reducing CVE attack surface to near-zero

### 13. Senior Fullstack / Team Lead Kubernetes Dev Debugging Standards
- **Kubernetes Dev Context & Namespace Isolation**:
  - active kubectl context strictly verified and pinned to development clusters and namespaces (`kubectl config set-context --current --namespace=dev`); running commands against unverified or production contexts prohibited
- **Collision-Resistant Port-Forwarding Lifecycle**:
  - multi-service port-forwarding scripts implement local port availability detection via `lsof -Pi :<port> -sTCP:LISTEN -t`, background PID file tracking (`/tmp/k8s-pf-*.pid`), and signal cleanup traps:
    ```bash
    trap 'kill $(cat /tmp/k8s-pf-*.pid 2>/dev/null) 2>/dev/null' EXIT INT TERM
    ```
  - zombie listener processes eliminated; automated netcat health probing (`nc -z 127.0.0.1 <port>`) verifies port readiness for PostgreSQL (5432), Redis (6379), Dapr HTTP (3500), Kratos HTTP (8000), gRPC (9000), and pprof (6060)
- **Structured JSON Logging with Trace Correlation**:
  - application logs in dev pods emit structured JSON containing `ts`, `level`, `caller`, `msg`, `trace_id`, and `span_id` (Go Kratos `SlogLogger` adapter); streamable triage via `jq` verified:
    ```bash
    kubectl logs -f -n dev -l app=payment-service --tail=200 | \
      jq -R 'fromjson? | select(.level == "ERROR" or .level == "WARN") | {ts: .ts, level: .level, trace_id: .trace_id, caller: .caller, msg: .msg, err: .error}'
    ```
- **Non-Invasive Ephemeral Debug Containers**:
  - distroless container diagnosis executed via `kubectl debug` attaching `nicolaka/netshoot:v0.13` with shared process namespaces (`--share-processes`), enabling live socket (`ss -tulpn`), packet (`tcpdump`), and process inspection without altering base images
- **Diagnostic In-Pod Profiling (`net/http/pprof`)**:
  - Go microservices expose diagnostic HTTP endpoints on `:6060` with mutex profiling (`runtime.SetMutexProfileFraction(5)`); CPU (`/debug/pprof/profile?seconds=30`), heap (`/debug/pprof/heap`), goroutine (`/debug/pprof/goroutine`), and mutex contention profiles captured and analyzed via `go tool pprof` and SVG callgraph generation. Profile capture duration strictly capped at 30 seconds to prevent thread starvation.
