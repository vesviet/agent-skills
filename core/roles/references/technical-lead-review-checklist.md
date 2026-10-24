## Technical Lead Review Checklist

This reference checklist provides detailed evaluation criteria for delivery planning, technical execution governance, and release gating to meet 2027 Agentic SWE standards.

### 1. Spec-Driven Breakdown
- **1:1 Contract Mapping**: Every implementation slice maps directly to an immutable contract specification (`api-contract-spec.json`, `feature-ticket.json`, or `schema-migration.json`).
- **Contract Freezing Gate**: Implementation is blocked until contract schemas and acceptance criteria are finalized and locked; no slice begins under fluid interface definitions.
- **Atomic Slice Scoping**: Slices are sized for focused execution and review; each slice owns a single logical interface or behavioral boundary.
- **Explicit Dependency Graph**: Inter-slice dependencies and sequence constraints are declared with unambiguous preceding artifacts required before execution.
- **Contract Conformance Oracles**: Every slice defines explicit contract validation steps ensuring that emitted artifacts conform strictly to the declared schemas.

### 2. Failure Domain Enforcement
- **Boundary Containment**: Slices strictly respect architectural failure domains; no slice introduces hidden synchronous coupling across isolated domain boundaries.
- **Bulkhead Preservation**: Execution logic preserves local thread pools, database connection budgets, and isolate boundaries without cross-domain leakage.
- **Asynchronous Decoupling**: Inter-domain mutations are implemented via idempotent asynchronous events or background jobs rather than blocking synchronous HTTP calls.
- **Fallback Verification**: Fallback and degradation paths specified in the architecture are verified as functional within each slice before merging.
- **State Mutation Quarantine**: Irreversible state changes are isolated and gated behind two-phase commit or transactional outbox patterns.

### 3. Blast Radius Assessment Matrix
- **Standardized Tier Evaluation**: Every slice in `technical-delivery-plan.json` evaluates its blast radius tier:
  - **Tier 1 (Localized)**: Purely internal logic or private utilities; zero external consumer impact; instant rollback without side effects.
  - **Tier 2 (Service-Internal)**: Internal API or service behavior change; confined to single service boundaries; rollback time < 5 minutes.
  - **Tier 3 (Cross-Service)**: Public or shared API, database schema migration, or event payload evolution; requires phased canary deployment and active telemetry monitoring.
  - **Tier 4 (Public / Core Infrastructure)**: Auth/authz, payments, tenant boundaries, or core routing; requires dual-review, canary ramp, automated circuit-breakers, and emergency kill-switch.
- **User Population & Blast Containment**: Proportion of user base exposed during initial canary rollout is explicitly capped (e.g., 1% -> 5% -> 25% -> 100%).
- **Automated Rollback Triggers**: Metric thresholds (e.g., error rate > 0.5%, P99 latency > 2× baseline, alert firing) are wired to trigger automated rollback without human intervention.
- **Kill-Switch Verification**: Feature flags and kill-switches are verified in staging before production canary rollout.

### 4. SLO Budget Gates & CI/CD Performance Verification
- **Architectural SLO Translation**: Architectural SLOs are translated into actionable, measurable CI/CD performance budgets per slice:
  - **API Latency Budgets**: Synthetic endpoint latency tests enforce P95 and P99 ceilings in staging pipelines.
  - **Database Query Budgets**: Query count assertions fail builds if N+1 queries or unindexed table scans occur.
  - **Core Web Vitals Budgets**: Frontend slices enforce INP (<200ms), LCP (<2.5s), and CLS (<0.1) budgets in CI.
  - **Resource Consumption Ceilings**: CPU, memory, and token limits per request are benchmarked against slice budgets.
- **Release-Blocking Gates**: Breaches of performance or latency budgets are treated as release blockers, not deferred optimization tickets.

### 5. AI Oversight, Trust Zones & Comprehension Debt Governance
- **Trust Zone Classification**: Every slice is assigned to an explicit trust zone:
  - **Restricted**: Auth, encryption, payment, data isolation, and security-critical paths; mandatory deep-dive human review; no autonomous agent merges.
  - **Standard**: Business logic, API endpoints, UI state machines; intent and assumption review; automated guardrail enforcement.
  - **Low-risk**: Scaffolding, boilerplate, non-critical utilities; standard automated lint and test validation.
- **Comprehension Debt Management**:
  - Developers must be able to explain the logic, invariants, and edge-case handling of all committed code.
  - AI-generated code without verified understanding is logged as comprehension debt in the Debt Register.
  - Restricted-zone comprehension debt is P0 and must be resolved within the current sprint.
- **Anti Vibe-Slop Verification**: Active screening for code that compiles and passes superficial tests but contains latent logic flaws or hallucinated boundaries.

### 6. Definition of Ready (DoR) & Progressive Delivery Gates
- **DoR Checklist Verification**:
  - Contracts locked and schema valid (`api-contract-spec.json`, `feature-ticket.json`).
  - Failure domain and bulkhead boundaries verified.
  - Blast radius tier and rollback trigger criteria defined.
  - Ephemeral execution sandboxes prepared for test execution.
- **Progressive Delivery Execution**:
  - Feature flag defined with an ISO 8601 cleanup target date.
  - Canary audience and rollout schedule documented.
  - Observability signals (metrics, logs, traces) active before traffic ramp begins.
