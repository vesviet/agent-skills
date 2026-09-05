# Spec-Driven Planning, Blast Radius Matrix & Milestone Gates — Reference

This reference provides actionable methodologies, scoring rubrics, and templates for technical leads breaking down delivery plans into deterministic, spec-driven execution slices.

---

## 1. Spec-Driven Breakdown Protocol

In 2027 Agentic SWE workflows, technical delivery breaks away from informal, conversational task assignment. Every implementation slice must be anchored to an immutable, machine-validated specification before any implementation code is authored.

### 1.1 Invariant Contract Freeze
Before any implementation slice is dispatched to developer or agent roles:
1. **Contract Invariance**: The interface contracts (`OpenAPI 3.1`, `JSON Schema`, or `Protobuf`) governing the slice must be authored, validated against meta-schemas, and frozen.
2. **Preserved Invariants**: Each slice must explicitly enumerate invariants that must not be violated (e.g., backward-compatible payload shapes, constant-time authentication checks, idempotency semantics).
3. **Specification Source of Truth**: Slices must link directly to `contracts/schemas/adr-spec.json`, `contracts/schemas/feature-ticket.json`, or local OpenAPI documents.

### 1.2 Vertical Thin Slicing
- **Anti-Pattern (Horizontal Layering)**: Slicing by architectural layer (e.g., Sprint 1: Database schemas; Sprint 2: API routes; Sprint 3: UI views). This defers integration feedback until the final stage and hides interface mismatches.
- **2027 Standard (Vertical Thin Slices)**: Every slice spans UI → API → Data layer, delivering an end-to-end executable path that satisfies a distinct user outcome.
- **Diff Ceiling**: Each slice must target **≤ 400 lines of diff** to ensure thorough reviewability and keep context within optimal cognitive and model attention limits.

---

## 2. Blast Radius & Regression Risk Matrix

Technical plans must systematically evaluate the potential downstream impact of every slice across four primary dimensions.

| Dimension | Evaluation Criteria | Risk Scoring | Mitigation / Containment |
|---|---|---|---|
| **Consumer Fanout** | Number of internal and external services or clients consuming modified endpoints or data models | **High** (>5 consumers)<br>**Medium** (2–5 consumers)<br>**Low** (1 consumer or internal only) | Consumer-driven contract tests (Pact), feature flag isolation, backward-compatible dual-write |
| **Failure Domain** | Ability of failures in this slice to cascade to unrelated business features or shared state | **High** (shared database/core middleware)<br>**Medium** (isolated module with shared bus)<br>**Low** (fully isolated bounded context) | Circuit breakers, strict bulkheads, isolated tenant namespaces |
| **Mutation Vulnerability** | Legacy or upstream code paths modified that lack mutation-tested coverage | **High** (mutation score < 50% or untested)<br>**Medium** (mutation score 50%–74%)<br>**Low** (mutation score ≥ 75%) | Pre-implementation test hardening; introduce characterization tests before slice dispatch |
| **Data Migration Risk** | Schema changes, table locks, column renames, or volume of backfilled records | **High** (destructive or table-locking change)<br>**Medium** (expand/contract with async backfill)<br>**Low** (additive nullable column) | Mandatory Expand/Contract pattern; zero-downtime dual-read/dual-write phases |

### 2.1 Regression Matrix Worksheet Template
For each slice in `technical-delivery-plan.json`, include:
```json
{
  "slice_id": "SLICE-01",
  "name": "order-cancellation-endpoint",
  "blast_radius": {
    "score": "medium",
    "impacted_modules": ["services/order", "services/billing", "events/notifications"],
    "failure_domain": "bounded to order domain; isolated from payment processing",
    "mutation_hotspots": ["services/order/domain/state_machine.py"],
    "data_migration_safety": "additive status enum; no backfill required"
  }
}
```

---

## 3. Sequential Intermediate Milestone Gates

Implementation progress between dependent slices must be governed by automated milestone verification gates. Progression is prohibited until gate criteria are verified.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Gate 1:         │       │ Gate 2:         │       │ Gate 3:         │       │ Gate 4:         │
│ Contract Freeze ├──────►│ Red Test in     ├──────►│ Green Impl in   ├──────►│ Mutation & Blast│
│ & Spec Invariant│       │ Isolated Sandbox│       │ Level 0 Sandbox │       │ Verification    │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Gate 1: Contract & Spec Freeze
- Schemas validated with zero syntax, type, or lint errors (`validate-contracts.py`).
- Pre-conditions, post-conditions, and RFC 9457 error contracts explicitly defined.
- Signed off by Technical Lead / Architect.

### Gate 2: Red Test Verification in Sandbox
- Independent test suite authored by QA / developer matching the contract.
- Executed inside containerized sandbox (`core/policies/execution-sandbox.md`).
- **Must fail deterministically** against baseline code (confirming tests are not tautological).

### Gate 3: Green Implementation in Sandbox
- Implementation code authored to satisfy the failing tests.
- Executed in Level 0 air-gapped sandbox (`--network=none`, non-root user, read-only rootfs).
- All unit, integration, and contract tests pass (100% green).

### Gate 4: Mutation Threshold & Blast Radius Verification
- Mutation testing executed on critical business packages (Stryker / mutmut).
- Mutation kill score achieves **≥ 75–80%**.
- Pact `can-i-deploy` verification passes for all consumers in the blast radius.

---

## 4. Execution Sandbox Isolation Tier Mapping

Delivery plans must declare the required execution sandbox isolation tier for each implementation slice per `core/policies/execution-sandbox.md`:

1. **Tier 1 (Subprocess / Namespace)**: Documentation updates, pure linting, schema validation without untrusted code execution.
2. **Tier 2 (Container / Docker Air-Gapped)**: Standard application code modification, unit testing, integration testing. Must enforce non-root execution (`USER 1000:1000`), read-only root filesystems, and disabled network access (`--network=none`).
3. **Tier 3 (MicroVM / gVisor)**: Untrusted dependencies, dynamic code generation, third-party package upgrades, or changes executing arbitrary script inputs.

---

## 5. Three-Point Estimation & Balanced Delivery Signals

Plans must avoid brittle point estimates (e.g. "this takes 2 days") and instead capture uncertainty bounds:
- **P10 (Optimistic)**: Best-case scenario with zero dependency friction.
- **P50 (Expected)**: Realistic duration under normal operational cadence.
- **P90 (Pessimistic)**: Worst-case duration accounting for edge-case debugging, test remediation, and review feedback loops.

Track delivery performance against balanced **DORA** (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service) and **SPACE** dimensions to avoid optimizing speed at the expense of system resilience.
