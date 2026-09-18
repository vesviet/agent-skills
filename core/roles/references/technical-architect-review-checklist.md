## Technical Architect Review Checklist

This reference checklist provides detailed evaluation criteria for structural system design, enterprise Model Context Protocol (MCP) server architecture, recursive multi-agent decomposition, disk-backed persistent planning, and evolutionary architecture fitness functions to meet 2027 Agentic SWE standards.

### 1. Structural Design, System Boundaries & Architecture-as-Code (AaC)
- **Explicit System Boundaries**: Service boundaries, interface contracts, data ownership, and dependency directions are declared unambiguously in `contracts/schemas/adr-spec.json`.
- **Machine-Readable Contract Artifacts**: Downstream engineering teams are provided with machine-verifiable contract schemas (`architecture-options.json`, `adr-spec.json`) before slice breakdown.
- **Cellular & Shared-Nothing Isolation**: Multi-tenant or high-scale systems ($\ge 99.95\%$ availability) enforce shared-nothing cellular partitions with zero synchronous cross-cell RPC dependencies.
- **Migration & Rollback Blueprint**: Every architectural change specifies a concrete data migration strategy and an automated, zero-loss rollback plan with quantified blast-radius impact.
- **Impacted Consumers Enumerated**: All internal services, external consumers, and API contract references (`api_contract_refs`) affected by boundary moves are explicitly cataloged.

### 2. Enterprise MCP Server Architecture & Tool Surface Contracts (`architect-mcp-server`)
- **Action-Oriented Domain Prefixes**: Tool names strictly adhere to `<domain>_<action>` naming (e.g., `db_query_records`, `order_create_invoice`, `git_checkout_branch`), preventing namespace collision across multi-server environments.
- **Strict Schema Validation (Zod / Pydantic)**: Every tool declares strict input parameter schemas and output return types; unvalidated freeform JSON blobs are rejected (`MCP-SERVER-CONTRACT LOCK`).
- **Structured Content Schemas (`outputSchema` / `structuredContent`)**: Tools emit structured JSON content conforming to declared `outputSchema` rather than unstructured text dumps, ensuring machine-parsable consumption by agent callers.
- **Actionable Error Ergonomics**: Error responses provide typed error categories (transient vs. permanent), machine-readable error codes, and explicit remediation hints guiding caller agents to self-correct parameters without human intervention.
- **Tool Granularity Calibration**: Tools are designed at single-action granularity; bloated "god-tools" packing disparate operations and microscopic "chatty" tools requiring excessive round-trips are eliminated.
- **Resource & Prompt Architecture**: Read-only contexts expose URI-addressable resources (`resources/read`) and reusable prompt workflows (`prompts/get`) with parameter validation.

### 3. MCP Stateless Transport, State Externalization (SEP-2567) & Auth Boundaries (RFC 8707)
- **Stateless HTTP Transport Default**: MCP implementations default to stateless streamable HTTP transport adhering to the MCP 2026-07-28 core specification; stateful stdio/SSE is restricted to local development.
- **Externalized State Handles (SEP-2567)**: Any residual session state or multi-turn context is externalized to high-performance distributed storage (Redis, Cloudflare D1, PostgreSQL); zero in-memory sticky-session affinity.
- **OAuth 2.1 RFC 8707 Resource Indicators**: Client tokens bound to specific MCP server resource indicators; servers prohibited from replaying bearer tokens to downstream services or chained MCP tools.
- **Enterprise-Managed Authorization SSO**: Centralized authorization gateway implemented for deployments managing $\ge 3$ MCP servers, enforcing uniform RBAC/ABAC tool invocation policies.
- **Supply-Chain Registry Governance**: Production MCP tool dependencies originate exclusively from allowlisted, audited registries with publisher verification, code-signing, and version pinning (`MCP-REGISTRY LOCK`).
- **Shadow MCP Detection**: Network and edge proxy observability configured to detect and block unauthorized, unmanaged MCP endpoints attempting connection to agent runtimes (`MCP-GATEWAY LOCK`).

### 4. Recursive System & Task Decomposition (DAG Execution, 100+ Files / 50K+ Tokens) (`decompose-agentic-system`)
- **Hierarchical DAG Topology**: Large-scale multi-file, high-token tasks are decomposed into a directed acyclic graph (DAG) of sub-agent scopes; cyclic agent loops are prohibited (`AGENTIC-DECOMPOSITION LOCK`).
- **Deterministic Dependency Gating**: Downstream child sub-agents execute only after upstream dependency outputs validate against schema contracts; premature speculative execution is blocked.
- **Blast-Radius Perimeter Isolation**: Each sub-agent scope operates within an isolated sandbox (container, process namespace, or directory boundary); lateral access across unassigned directories is denied (`BLAST-RADIUS LOCK`).
- **Invariant Pre- and Post-Conditions**: Automated invariant assertions are executed at phase boundaries; DAG execution halts immediately if an architectural invariant fails.
- **State Checkpointing**: Intermediate sub-agent artifacts and execution states are checkpointed to durable storage, enabling resumption from the last valid checkpoint upon agent failure.

### 5. Disk-Backed Persistent Planning & Anti-Context-Rot Architecture (`planning-with-files`)
- **Durable Disk-Backed State**: Task execution plans, task manifests, and dependency status live in durable disk markdown files (`plan.md`, `task.md`, `progress.md`, `briefing.md`) rather than volatile LLM context windows (`CONTEXT-ROT-RESISTANCE LOCK`).
- **Compaction & Truncation Survival**: Agent architectures guarantee full operational recovery after context window compaction, truncation, or session clear (`/clear`) by reading state from disk.
- **Deterministic Completion Gates**: Tasks close only when empirical evidence (compiler exit code 0, test pass output, schema validator success) is written to the verification block; agent self-declaration of completion is invalid.
- **Atomic Progress Logging**: Execution heartbeats and progress updates record monotonic timestamps, exact artifact URIs, and step transitions, preventing false-positive progress reporting.

### 6. Non-Human Identity (NHI) Lifecycle, Autonomy Tiers & Blast-Radius Isolation
- **Scoped NHI Provisioning**: Every autonomous agent in production possesses an individual Non-Human Identity with dedicated credentials; shared agent credentials are strictly forbidden.
- **3-Tier Autonomy Classification**:
  - *Tier 1 (Supervised)*: Human operator must approve every tool call and state change.
  - *Tier 2 (Semi-Autonomous)*: Agent operates autonomously for read and local file edits; human approval required for irreversible actions (migrations, production pushes, credential access).
  - *Tier 3 (Fully Autonomous)*: Execution is strictly bound by hard infrastructure policy limits; unprivileged sandboxes only.
- **Credential Lifecycle Governance**: Provisioning, automated short-lived token issuance, rotation cadence, and emergency revocation procedures are codified in the ADR.
- **Immutable Tool-Call Audit Trail**: Every tool call, parameter payload, execution timestamp, and response status is recorded in an immutable, queryable audit log.

### 7. Evolutionary Architecture & Automated Fitness Functions (Cedar, OPA, Calibrated LLM-as-Judge)
- **100% ADR Fitness Function Coverage**: Every structural constraint declared in an ADR maps to an automated fitness function in the CI/CD pipeline (`FITNESS-FUNCTION LOCK`).
- **Framework Selection Appropriateness**:
  - *Cedar (AWS)*: Applied to mathematical verification of agent trust boundaries, credential delegation chains, and NHI access policies.
  - *OPA/Rego*: Applied to general-purpose boundary enforcement, dependency rules, and schema compliance gates.
  - *ArchUnit / Custom Linters*: Applied to compile-time code layer separation and package import invariants.
- **Living ADR Machine-Readability**: ADR documents embed machine-readable constraint blocks parsed by automated pipeline linters.
- **Agentic Fitness Function Calibration**: LLM-as-judge fitness functions are calibrated against 20–50 historical pull requests in observation mode before being granted merge-blocking authority.

### 8. AI-Native Inference Placement, FinOps & Eval Frameworks
- **Inference Placement Decision Matrix**: ADR documents trade-offs for Edge vs. Cloud vs. Hybrid inference against the 6 core criteria: latency, data residency, model size, context window, cost model, and capability ceiling (`EDGE-INFERENCE LOCK`).
- **FinOps & Token Budget Governance**: Per-request token caps, session budgets, prompt caching (Automatic Prefix Caching), and model tiered routing (frontier vs. domain-specific vs. quantized) are specified (`INFERENCE-FINOPS LOCK`).
- **Architectural Eval Framework**: ADR defines acceptable output ranges, golden test dataset baselines, and behavioral drift alert thresholds before AI components are approved.
- **Orchestration vs. Inference Separation**: Routing, fallback state machines, circuit breakers, and HITL gates are implemented in infrastructure code, never embedded in LLM prompt strings (`INFERENCE-ORCHESTRATION LOCK`).

### 9. Privacy-by-Design, Auditability & Regulatory Governance (EU AI Act Digital Omnibus)
- **Data Minimization & Schema Masking**: Schemas expose strictly necessary fields for consuming services; PII fields require explicit architectural justification (`PRIVACY-BY-DEFAULT LOCK`).
- **EU AI Act Timeline Alignment**: Scoping reflects the Digital Omnibus regulation timeline (Regulation (EU) 2026/1744):
  - *Article 50 Transparency*: Mandatory AI-generated disclosures live as of August 2026.
  - *Synthetic Content Grace Period*: Watermarking grace period active until 2 December 2026.
  - *Annex III Standalone High-Risk AI*: Obligations deferred to 2 December 2027.
  - *Annex I Embedded High-Risk AI*: Product obligations deferred to 2 August 2028.
- **15-Day Decision Reconstruction**: Audit logging maintains cryptographic provenance allowing full reconstruction of any automated high-risk decision within 15 days of occurrence.
