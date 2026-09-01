---
name: system-design
description: Design, specify, and document complex system architectures covering compute, network, storage, middleware, and AI inference layers. Translate NFRs into measurable infrastructure targets and produce capacity models. Use when designing or reviewing system topology, sizing infrastructure, planning capacity, or specifying AI infrastructure (GPU, inference servers, vector databases).
---

# System Design

Use this skill when designing system topology for a new service or infrastructure layer, translating non-functional requirements into engineering specifications, planning capacity for growth, or architecting AI inference infrastructure.

## When to Use

- a new system, environment, or service needs infrastructure topology specified before implementation
- non-functional requirements (latency, throughput, availability, scalability) need translating into measurable engineering targets
- capacity planning is needed for known or forecast growth
- AI inference infrastructure (GPU allocation, inference server, vector database) needs to be designed or selected
- an existing system needs a performance or capacity review
- infrastructure decisions require documented trade-off analysis

## Core Rules

- every design decision must trace to a measurable NFR or explicit business requirement — "best practice" alone is not a rationale
- do not accept vague NFRs (e.g., "the system should be fast"); return unmeasurable NFRs for clarification before producing a design
- all infrastructure changes must be committed to IaC (Terraform, Ansible, Kubernetes manifests) — manual-only changes are invisible drift
- analyze cross-layer impact for every proposed change; a change at one layer creates second-order effects at adjacent layers
- capacity planning is proactive — produce a capacity model before production, not after the first resource incident
- for AI inference: GPU memory allocation must account for model weights + KV cache + activation memory + batch overhead; never underestimate VRAM headroom
- **GPU-VRAM-FORMULA**: Total VRAM = model weights in target precision + KV cache (2×num_layers×head_dim×seq_len×batch×precision_bytes) + activation memory (~2-5% overhead) + safety headroom (≥15%); running below 10% headroom causes OOM-kill under burst traffic.
- **INFERENCE-SERVER-SELECTION**: vLLM for high-throughput LLM serving with continuous batching; TensorRT-LLM for NVIDIA-optimized lowest-latency serving; Triton for multi-model ensemble pipelines; Ollama for local/development deployments; vLLM v0.6+ Automatic Prefix Caching (APC) — place static system prompts first and dynamic vars last for maximum cache hit rate.
- **LLM-SLOS**: Set measurable LLM SLOs: TTFT p95 < 800ms, TBT (time-between-tokens) p95 < 25ms, throughput > 40 tokens/s per user; define these before sizing GPU infrastructure.
- **VECTOR-DB-TUNING**: Never deploy production vector databases with default index parameters; specify HNSW m (graph connectivity), ef_construction (build quality), and query-time ef (recall-latency trade-off) explicitly.
- **EMBEDDING-CACHE**: Always design a caching layer for embeddings; repeated embedding of the same content is the most common preventable AI cost spike.

## Suggested Process

### Step 1: Collect Inputs

Before designing, gather:

- NFRs from Technical Architect (ADRs) or Product Manager (feature briefs)
- traffic and load projections (current and forecast)
- service topology (what services exist and how they communicate)
- security requirements and data residency constraints
- cost envelope and budget constraints
- AI model specifications if inference infrastructure is in scope: model name/version, parameter count, quantization target, expected QPS, P99 latency target, context window length

### Step 2: Translate NFRs Into Measurable Targets

For each NFR, produce a specific, measurable engineering target:

| NFR (vague) | Engineering target (specific) |
|-------------|-------------------------------|
| "High availability" | 99.9% availability = max 8.7h downtime/year; RTO < 15min; RPO < 5min |
| "Fast response" | P99 API latency < 200ms at 1000 req/s peak load |
| "Handle growth" | Scale to 10x current traffic without design changes; scale to 100x with horizontal sharding |
| "Low cost AI inference" | < $0.005 per LLM request; token budget: 2K input + 500 output average |

Return NFRs to their source if a measurable target cannot be derived from available information.

### Step 3: Design System Topology

Specify each layer of the system:

**Compute layer:**
- instance types and sizing rationale
- replica count and autoscaling policy (scale-out trigger, scale-in threshold)
- placement strategy (availability zones, regions)

**Network layer:**
- VLAN/subnet segmentation
- load balancer type and configuration (L4 vs L7, health check intervals, session persistence)
- DNS strategy (TTL, health-check-aware failover)
- service mesh or direct connection decision

**Storage layer:**
- database type selection and sizing
- storage tier hierarchy (hot/warm/cold)
- replication and backup strategy
- retention policy

**Middleware layer:**
- message queue topology (Kafka partition strategy, consumer group design; or Redis Streams; or cloud-native alternatives)
- cache hierarchy (L1 in-process, L2 Redis/Memcached, L3 CDN)
- API gateway or service mesh configuration

**AI inference layer (when in scope):**
- GPU type, count, and allocation plan
- inference serving stack selection with configuration
- vector database selection and index parameters
- embedding pipeline design

### Step 4: Build Capacity Model

Produce a capacity model for every primary resource:

```
| Resource     | Current  | P95 (3mo) | P95 (12mo) | Headroom | Action trigger |
|--------------|----------|-----------|------------|----------|----------------|
| CPU (avg)    | 35%      | 52%       | 78%        | 22%      | Scale at 70%   |
| Memory       | 12 GB    | 18 GB     | 28 GB      | 4 GB     | Scale at 80%   |
| Storage      | 500 GB   | 750 GB    | 1.2 TB     | 300 GB   | Expand at 80%  |
| GPU VRAM     | 18 GB    | 22 GB     | 30 GB      | 10 GB    | Upgrade at 85% |
| Network egr. | 50 GB/d  | 75 GB/d   | 120 GB/d   | —        | Review at 2x   |
```

Derive forecasts from: current usage × growth rate (from traffic projections or business targets).

### Step 5: Document Trade-offs

For every significant design decision, record:

- what was chosen and why
- what alternatives were considered and rejected
- what trade-off was accepted (e.g., higher cost for lower latency; lower availability for simpler design)

### Step 6: Analyze Cross-Layer Impact

Before finalizing:

- trace each infrastructure decision to its second-order effects: "changing connection pool max from 50 to 200 enables higher concurrency but increases database memory pressure by ~4 GB"
- identify changes that affect multiple layers simultaneously
- flag any changes that require coordination with adjacent roles (DevOps for pipeline, SRE for SLO alignment, Security Engineer for security review)

### Step 7: Produce IaC and Deliverable

- author or update Terraform modules, Ansible playbooks, or Kubernetes manifests for all infrastructure changes
- produce `contracts/schemas/system-design-spec.json` for machine-readable handoff when downstream roles need to consume the design
- produce a human-readable System Design Brief using the Output Template in `system-engineer.md`

## Checklist

- [ ] all NFRs have specific, measurable targets with measurement methods
- [ ] system topology covers all in-scope layers with rationale for each major decision
- [ ] capacity model produced for all primary resources (compute, memory, network, storage, GPU if applicable)
- [ ] 3-month and 12-month capacity forecasts present
- [ ] action triggers defined (when to scale, when to upgrade)
- [ ] cost vs. performance trade-off surfaced to stakeholders
- [ ] cross-layer impact analysis complete
- [ ] all infrastructure changes represented in IaC — no manual-only configuration
- [ ] trade-offs documented: what was chosen, what was rejected, and why
- [ ] AI infrastructure specified (when in scope): GPU allocation, inference server config, vector DB, embedding pipeline
- [ ] system-design-spec.json produced when structured downstream handoff required
- [ ] open questions, accepted risks, and escalation items documented

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- `contracts/schemas/system-design-spec.json` — Required fields: topology, nfr_targets, capacity_model, rollback_plan, and trade_offs. Set produced_by_role to System Engineer or Technical Architect.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Vague NFR accepted**: a design proceeds with "the system should be fast". Mitigation: return unmeasurable NFRs to the source for clarification before producing a design.
- **VRAM under-provisioned**: GPU memory is sized without accounting for KV cache, activation, or safety headroom. Mitigation: enforce the GPU-VRAM formula; require ≥ 15% headroom.
- **Default vector index deployed**: a vector database ships with default HNSW parameters. Mitigation: explicitly set `m`, `ef_construction`, and query-time `ef`; document the recall-latency trade-off.
- **Embedding re-computed**: the same content is re-embedded on every request, driving unnecessary GPU cost. Mitigation: design an embedding cache layer; verify cache hit rate in production.
- **LLM SLO missing**: GPU infrastructure is sized without TTFT, TBT, or throughput targets. Mitigation: define measurable SLOs (TTFT p95 < 800ms, TBT p95 < 25ms) before sizing.
- **Capacity model stale**: the capacity model was produced once and never updated. Mitigation: re-validate the capacity model quarterly or after every 2x growth event.
- **Cross-layer impact missed**: a connection pool change breaks an adjacent layer. Mitigation: trace second-order effects for every change; flag coordination requirements with adjacent roles.
- **Manual-only config**: infrastructure is set up via console without IaC. Mitigation: require all changes to be in Terraform/Ansible/Kubernetes manifests; surface drift as a CI failure.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: every infrastructure component must declare its auth surface; reject "internal-only" claims without a network policy or service-mesh boundary.
- **ASI04 Supply Chain**: AI model versions, vector database versions, and inference server versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct IaC modules, capacity formulas, or routing configs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the system design spec is consumed by multiple downstream roles; treat it as a public contract and review all changes before deploy.
- **ASI09 Human-Agent Trust Exploitation**: do not present a design as "secure" without a security review; surface remaining risks and accepted trade-offs honestly.

## Related Skills

- **performance-profiling**: Benchmark and investigate performance bottlenecks after the design is implemented
- **debug-runtime-platform**: Debug system-level issues at OS, network, and runtime layers
- **plan-technical-delivery**: Coordinate system design phases with the delivery timeline
- **add-telemetry-instrumentation**: Define observability requirements for the system being designed
- **conduct-research**: Technology selection research when infrastructure decisions require vendor evaluation
- **security-audit**: Security review of the infrastructure design before production apply
- **database-maintenance**: Database-level investigation when storage design choices are being validated
