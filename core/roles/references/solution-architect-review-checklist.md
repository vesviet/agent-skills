## Solution Architect Review Checklist

This reference checklist provides detailed evaluation criteria for solution architectures designed to meet 2027 Agentic SWE standards.

### 1. Spec-Driven Architecture (SDA)
- **Immutable Spec Prerequisite**: Solution design establishes machine-readable contract schemas (`contracts/schemas/`) as the single source of truth before engineering work begins.
- **Formal Specification Coverage**: Business rules, state transitions, event payloads, and data formats are formally specified in schema contracts rather than informal text.
- **Contract Boundary Freezing**: Schema contracts are frozen and version-controlled; changes require formal schema versioning and deprecation procedures.
- **Spec Drift Prevention**: Fitness functions and schema validation checks are defined to detect runtime or implementation divergence from the formal specification.
- **Deterministic Validation**: Downstream engineering teams are provided with machine-verifiable contract artifacts (`solution-brief.json`, `api-contract-spec.json`) to drive slice generation.

### 2. Failure Domain Isolation (FDI) & Bulkhead Architecture
- **Boundary Partitioning**: Distributed services and autonomous agent execution boundaries are decoupled with zero cross-domain synchronous cascading failure paths.
- **Bulkhead Patterns**: Critical capabilities are isolated in separate execution environments, thread pools, and connection pools to prevent resource exhaustion from spreading.
- **Asynchronous Decoupling**: Inter-domain mutations and long-running workflows use asynchronous messaging (event streams, message brokers) with bounded retry and dead-letter queues.
- **Graceful Degradation Tiers**: System defines explicit degradation behaviors when dependent services or upstream AI providers fail (e.g., cached reads, deterministic rule-based fallbacks).
- **Circuit Breaker Policies**: Outbound integration boundaries define circuit breakers with explicit trip thresholds, half-open probe intervals, and fallback responses.

### 3. Immutable API & Contract Boundaries
- **Pre-Implementation Contract Lock**: Public API endpoints and inter-service contracts are declared and locked in `api-contract-spec.json` prior to coding slices.
- **Strict Backward Compatibility**: Contract changes follow SemVer; additive changes preserve backward compatibility; breaking changes require co-existing version endpoints.
- **Deprecation Windows**: Deprecation timelines and sunset policies are explicitly declared for all external and inter-service interfaces.
- **Client Impact Analysis**: Every contract alteration includes a mapped inventory of upstream and downstream consumers with migration obligations documented.
- **Validation Oracles**: Machine-readable JSON Schemas (or OpenAPI specifications) provide unambiguous validation oracles for automated client generation and testing.

### 4. Quantitative Blast Radius Assessment & Scoring
- **Blast Radius Tiering**: Every architectural initiative assigns an explicit Blast Radius score:
  - **Tier 1 (Localized)**: Isolated within a single internal module; zero consumer impact; immediate automated rollback.
  - **Tier 2 (Service-Internal)**: Affects internal service components or background tasks; consumers unaffected if bulkhead holds; rollback < 5 minutes.
  - **Tier 3 (Cross-Service)**: Affects multi-service APIs, database schema changes, or inter-agent communications; requires phased canary deployment.
  - **Tier 4 (Public / Tenant-Wide)**: Modifies public contracts, auth mechanisms, or tenant data boundaries; requires human sign-off, canary rollout, and instant kill-switch.
- **State Mutation Exposure**: Assessment evaluates exposure to permanent or irreversible state mutations (financial debits, data deletion, external provider calls).
- **Containment & Kill-Switch Controls**: Hard architectural kill-switches and feature-flag gates are designed into the topology to immediately quarantine failing components.

### 5. Service Level Objectives (SLO) & Performance Envelopes
- **Quantitative Availability**: Target availability (e.g., 99.95% uptime) defined along with explicit error budget allocation policies.
- **Latency Envelopes**: P50, P95, and P99 latency ceilings defined for synchronous paths (e.g., P95 < 200ms for API endpoints; P99 < 500ms).
- **Throughput & Capacity Ceilings**: Maximum concurrency, request-per-second (RPS) thresholds, and auto-scaling limits documented in `solution-brief.json`.
- **Token & Compute Budgets**: Agentic and LLM-powered components specify token consumption budgets (request, session, and tenant caps) with enforcement mechanisms.
- **Downstream CI/CD Gate Alignment**: Performance envelopes are translated into concrete measurable thresholds enforced during staging and canary verification.

### 6. Build vs Buy vs Partner & MCP Marketplace Evaluation
- **Build vs Buy Quadrant**: Rationale, operational overhead, vendor lock-in, and full cost-of-ownership explicitly documented.
- **Exit Strategy & Reversibility**: Exit cost, data portability, and replacement timelines calculated before committing to SaaS or third-party platforms.
- **MCP Marketplace Tool Provenance**:
  - Publisher identity verified; security audit status and code review history inspected.
  - Data residency and GDPR compliance of tool execution verified.
  - Rug-pull risk mitigated via version pinning and behavioral monitoring.
  - Tool exit cost evaluated (substitutability with alternative MCP servers or standard APIs).

### 7. Compliance & Regulatory Scoping
- **Regulatory Frameworks**: GDPR, PDPA, EU AI Act, and sector regulations mapped into explicit solution constraints.
- **Architectural vs Operational Controls**: Clear separation between controls enforced in code/architecture vs. organizational process.
- **EU AI Act Timeline Alignment**: Scoping aligns with the Digital Omnibus timeline (Article 50 transparency live August 2026; Annex III high-risk deadline December 2027).
- **Auditability & Traceability**: Solution incorporates tamper-evident logging, decision provenance, and 15-day decision reconstruction capability.
