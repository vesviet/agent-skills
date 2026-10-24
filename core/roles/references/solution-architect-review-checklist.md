## Solution Architect Review Checklist

This reference checklist provides detailed evaluation criteria for solution architectures designed to meet 2027 Agentic SWE standards.

### 1. Architecture-as-Code (AaC) & Executable Modeling
- **C4 Model Precision**: Architecture is modeled across System Context, Containers, Components, and Deployment Topology using Structurizr DSL (`workspace.dsl`) or LikeC4 DSL (`workspace.c4`).
- **Source Control Synchronization**: Architecture models reside in Git alongside application source code; automated CI syntax validation prevents drift.
- **Dynamic Viewpoint Rendering**: System views (context, container, component, deployment) are generated deterministically from code, eliminating static whiteboard diagrams.
- **Relationship Typing**: All container and component relationships declare explicit protocol, latency, and serialization types (e.g., `gRPC/Protobuf`, `JSON/HTTPS`, `Dapr/CloudEvents`).

### 2. Spec-Driven Architecture (SDA) & Contract Governance
- **Immutable Spec Prerequisite**: Solution design establishes machine-readable contract schemas (`contracts/schemas/`) as the single source of truth before engineering work begins.
- **Centralized Schema Registry**: Protobuf BSR (`buf`) and OpenAPI 3.1 / AsyncAPI 3.0 schemas are validated with automated Spectral rulesets (`.spectral.yaml`).
- **Contract Boundary Freezing**: Schema contracts are frozen and version-controlled; breaking changes require SemVer major bumps and sunset windows.
- **Spec Drift Prevention**: CI quality gates block PRs if code or implementation artifacts diverge from frozen contract definitions.
- **Deterministic Validation**: Downstream engineering teams are provided with machine-verifiable contract artifacts (`solution-brief.json`, `api-contract-spec.json`) to drive slice generation.

### 3. Cell-Based Architecture & Failure Domain Isolation (FDI)
- **Cellular Boundaries**: Platforms targeting $\ge 99.95\%$ availability are partitioned into shared-nothing cells with zero synchronous cross-cell dependencies.
- **Shuffle Sharding Routing**: Envoy Gateway implements Highest Random Weight (HRW) rendezvous hashing rings ($P(\text{Collision}) = 1/\binom{N}{K} \le 0.005\%$) to isolate noisy neighbors.
- **Epoch Fencing Tokens**: Cell routers and stateful partitions carry monotonic epoch fencing tokens validated against etcd distributed consensus to prevent split-brain dual-master writes.
- **Little's Law Bulkheads**: Concurrency quotas for thread pools, memory limits, and database connection pools are dimensioned via Little's Law ($L = \lambda \times W$).
- **Asynchronous Decoupling**: Cross-domain data flow utilizes Transactional Outbox (`SELECT ... FOR UPDATE SKIP LOCKED`) and Dapr Pub/Sub event brokers.
- **Deterministic Degradation**: System defines 4-tier graceful degradation behaviors (L1 in-memory cache, L2 Redis stale read, L3 deterministic rule engine fallback, L4 circuit trip).
- **Single-Canary Circuit Breaker**: Circuit breakers enforce an atomic single-canary probe lock in `HALF-OPEN` state to prevent thundering herd crashes upon upstream recovery.

### 4. Mathematical Capacity Sizing & GPU VRAM Allocation
- **Microservice Concurrency Quotas**: Peak ingress/egress bandwidth, Little's Law worker goroutines, and PostgreSQL connection pool sizing with PgBouncer transaction pooling.
- **Exact GPU Memory Sizing**: LLM GPU allocation adheres to the 4-component equation:
  $$VRAM_{total} = VRAM_{weights} + VRAM_{KV} + VRAM_{activation} + VRAM_{overhead}$$
  reserving $\ge 15\%$ safety headroom to prevent CUDA OOM panics under concurrent prompt bursts.
- **PagedAttention Dimensioning**: KV-cache memory pools are dimensioned based on model parameter count, context lengths ($L_{prompt}$, $L_{gen}$), and batch concurrency ($B_{max}$).
- **Inference Latency Dynamics**: Time-To-First-Token ($TTFT \le 800\text{ms}$ via MFU) and Time-Between-Tokens ($TBT \le 25\text{ms}$ via MBU) are documented before sizing GPU clusters.
- **Token Economics & VPT**: Cost-Per-Token ($CPT$) is computed and Value-Per-Token ($VPT$) business viability thresholds are validated.

### 5. Clean Architecture & Saga Orchestration (Go 1.25+ Kratos & Dapr)
- **Layer Separation**: Kratos 4-layer architecture strictly separates Transport (`api`), Adapter (`service`), Domain (`biz`), and Persistence (`data`).
- **Zero ORM Leakage**: Database driver instances (`gorm.DB`) are prohibited from leaking into the `internal/biz` domain package.
- **Compile-Time Wire DI**: Dependency injection is wired via `google/wire` AST code generation; untracked global singletons are rejected.
- **Asynchronous Saga State Machine**: Cross-service distributed transactions are orchestrated as asynchronous Sagas backed by Transactional Outbox; distributed 2PC anti-patterns are rejected.

### 6. Quantitative Blast Radius Assessment & Scoring
- **Blast Radius Tiering**: Every architectural initiative assigns an explicit Blast Radius score:
  - **Tier 1 (Localized)**: Isolated within a single internal module; zero consumer impact; immediate automated rollback.
  - **Tier 2 (Service-Internal)**: Affects internal service components or background tasks; consumers unaffected if bulkhead holds; rollback < 5 minutes.
  - **Tier 3 (Cross-Service)**: Affects multi-service APIs, database schema changes, or inter-agent communications; requires phased canary deployment.
  - **Tier 4 (Public / Tenant-Wide)**: Modifies public contracts, auth mechanisms, or tenant data boundaries; requires human sign-off, canary rollout, and instant kill-switch.
- **State Mutation Exposure**: Assessment evaluates exposure to permanent or irreversible state mutations (financial debits, data deletion, external provider calls).
- **Containment & Kill-Switch Controls**: Hard architectural kill-switches and feature-flag gates are designed into the topology to immediately quarantine failing components.

### 7. Service Level Objectives (SLO) & Performance Envelopes
- **Quantitative Availability**: Target availability (e.g., 99.95% uptime) defined along with explicit error budget allocation policies.
- **Latency Envelopes**: P50, P95, and P99 latency ceilings defined for synchronous paths (e.g., P95 < 200ms for API endpoints; P99 < 500ms).
- **Throughput & Capacity Ceilings**: Maximum concurrency, request-per-second (RPS) thresholds, and auto-scaling limits documented in `solution-brief.json`.
- **Token & Compute Budgets**: Agentic and LLM-powered components specify token consumption budgets (request, session, and tenant caps) with enforcement mechanisms.
- **Downstream CI/CD Gate Alignment**: Performance envelopes are translated into concrete measurable thresholds enforced during staging and canary verification.

### 8. Build vs Buy vs Partner & MCP Marketplace Evaluation
- **Build vs Buy Quadrant**: Rationale, operational overhead, vendor lock-in, and full cost-of-ownership explicitly documented.
- **Exit Strategy & Reversibility**: Exit cost, data portability, and replacement timelines calculated before committing to SaaS or third-party platforms.
- **MCP Marketplace Tool Provenance**:
  - Publisher identity verified; security audit status and code review history inspected.
  - Data residency and GDPR compliance of tool execution verified.
  - Rug-pull risk mitigated via version pinning and behavioral monitoring.
  - Tool exit cost evaluated (substitutability with alternative MCP servers or standard APIs).

### 9. Compliance & Regulatory Scoping
- **Regulatory Frameworks**: GDPR, PDPA, EU AI Act, and sector regulations mapped into explicit solution constraints.
- **Architectural vs Operational Controls**: Clear separation between controls enforced in code/architecture vs. organizational process.
- **EU AI Act Timeline Alignment**: Scoping aligns with the Digital Omnibus timeline (Article 50 transparency live August 2026; Annex III high-risk deadline December 2027).
- **Auditability & Traceability**: Solution incorporates tamper-evident logging, decision provenance, and 15-day decision reconstruction capability.
