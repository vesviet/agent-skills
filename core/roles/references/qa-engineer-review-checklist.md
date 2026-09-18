## Review Checklist

This reference checklist provides detailed test engineering, quality gates, and resilience validation criteria for QA engineering to meet 2027 Agentic SWE standards.

### Distributed System Validation
- acceptance criteria are **observable** and mapped to explicit assertions (clear pass/fail)
- critical user journeys include negative paths and boundary cases, not only happy paths
- permissions/roles/tenancy are validated where applicable (no unauthorized access)
- data correctness is verified (not only responses): invariants, constraints, and persistence state
- side effects are verified: events published/consumed, cache behavior, search indexing, downstream calls
- async flows are validated with eventual consistency in mind (timing windows and retries)
- compatibility is considered when relevant (mixed versions, schema evolution, safe migrations)
- defects include environment, reproduction, expected, actual, evidence, and suspected blast radius
- skipped checks and residual risk are explicit and justified
- release confidence is supported by evidence, not confidence language

### Systematic Root Cause Analysis (4-Phase Debugging)
- **Phase 1: Observation & Deterministic Reproduction**:
  - exact symptoms, error logs, stack traces, and environmental preconditions captured without alteration.
  - defect isolated to a minimal, deterministic reproduction script or automated reproduction test case.
  - reproduction consistency verified across repeated executions to eliminate timing or flaky environmental factors.
- **Phase 2: Architectural Hypothesis Formulation**:
  - code paths, component boundaries, and state transitions mapped to relevant architectural invariants.
  - explicit, testable, and falsifiable hypotheses formulated explaining the underlying causal mechanism.
  - surface-level symptoms strictly distinguished from fundamental root causes; superficial causes eliminated.
- **Phase 3: Targeted Experimentation & Falsification Testing**:
  - targeted instrumentation or assertions designed to prove or disprove each candidate hypothesis.
  - automated reproduction test authored and verified failing (Red phase) on the unfixed codebase.
  - failure mode verified to match the specific hypothesized defect rather than secondary compilation or runtime errors.
- **Phase 4: Root-Cause Correction & Recurrence Prevention**:
  - minimal, targeted fix applied directly to the root mechanism; speculative workarounds rejected.
  - fix verified passing the reproduction test (Green phase) and full regression suite without side-effect regressions.
  - architectural guards (invariants, schema validation, type constraints, lint rules) added to prevent recurrence.

### Verification Before Completion (VBC) & Empirical Evidence Gates
- **Empirical Execution Proof**:
  - fresh, un-cached test execution completed on the final codebase; reliance on stale or prior-turn passes strictly prohibited.
  - explicit exit code 0, complete command logs, and passing assertion traces captured and verified.
  - test environment verified for parity with production configuration, flags, and data dependencies.
- **Epistemic Doubt Enforcement**:
  - absence of visible errors treated as insufficient evidence of correctness; active boundary probing required.
  - code execution verified: confirmed that modified logic was actually traversed during the test run.
  - confirmation bias eliminated: verified that negative test assertions fail when defect conditions are present.
- **Zero False-Green Sign-Off**:
  - stateful side effects verified: persistence mutations, outbox messages, and cache updates explicitly asserted.
  - assertions audited to eliminate assertion theater (e.g. replacing trivial `toBeDefined()` checks with invariant evaluations).
  - all executed checks, commands, logs, and residual risks documented in `contracts/schemas/validation-result.json`.

### Pairwise Combinatorial Testing & Matrix Optimization
- **Factor Space & Boundary Level Modeling**:
  - input variables, configuration switches, environmental dimensions, and feature flags cataloged.
  - factor values partitioned into discrete equivalence classes and boundary values.
  - constraint rules specified to prune impossible, invalid, or mutually exclusive combinations.
- **Pairwise Covering Array Generation**:
  - combinatorial reduction algorithms (PyPICT, IPO) applied to generate optimal 2-way test matrices.
  - 100% pairwise interaction coverage across all factor pairs verified with minimal execution footprint.
  - higher-order N-way combinations (3-way/4-way) evaluated and applied for mission-critical or financial workflows.
- **Execution & Combinatorial Defect Isolation**:
  - generated test vectors mapped directly to table-driven automated test fixtures.
  - failing combinations analyzed to isolate interacting parameter pairs causing the defect.

### Mutation Testing Infrastructure
- **Mutation Testing Execution**: Stryker (JS/TS), Mutmut (Python), or cargo-mutants (Rust) is configured and executed against core modules.
- **Score Thresholds**: Core domain logic, authentication/authorization, and financial/invariant routines must achieve a mutation score ≥ 75–80%.
- **Assertion Quality Verification**: Mutation test reports are audited to confirm that surviving mutants are addressed with high-value assertions rather than superficial checks.
- **No Mock Mutation Evasion**: Tests do not mock away the core business logic under mutation testing; real execution paths are mutated.
- **CI Mutation Gate**: Mutation testing runs as a scheduled or PR-level gate on critical path changes, failing if the mutation score regresses.

### Property-Based Testing for Business Invariants
- **Randomized Invariant Verification**: Property-based testing (via fast-check, Hypothesis, or proptest) is implemented for complex algorithms, data transformers, and parsers.
- **Round-Trip Properties**: Serialization, deserialization, encryption, and encoding transformations verify that `decode(encode(x)) == x` across thousands of generated inputs.
- **Idempotency Properties**: Operations declared as idempotent verify that `apply(apply(state, action), action) == apply(state, action)`.
- **State Transition Invariants**: Deterministic state machines verify that invalid transitions are rejected for all arbitrary sequence permutations.
- **Counter-Example Shrinking**: When a property test fails, minimal shrinking examples are captured and added to the regression test suite.

### Multi-Dimensional Testing Matrix (Concurrency, Leaks, N+1 Queries)
- **Concurrency & Race Conditions**:
  - High-concurrency stress test runs (e.g., k6, Locust, or Go routine hammers) verify thread safety and race detector compliance (`-race` flag).
  - Check-then-act operations are tested under parallel execution to verify transaction isolation and optimistic locking.
- **Memory & Resource Leak Testing**:
  - Heap allocation profiling and long-running burn-in tests verify memory usage remains flat over extended load.
  - Streaming endpoints and event listeners are tested under rapid connection abort cycles to verify socket and memory cleanup.
- **N+1 Database Query Verification**:
  - Automated test assertions verify query counts per endpoint (e.g., asserting max queries ≤ 3 regardless of list size).
  - Bulk operations and list endpoints are tested with variable payload sizes (1, 10, 100 items) to verify linear or constant query scaling.

### OWASP ASI04 (Supply Chain) & ASI05 (Unexpected Execution) Gates
- **ASI04 Supply Chain Verification**:
  - All project dependencies are verified against lockfile integrity hashes; dependency audit passes with zero critical/high CVEs.
  - GitHub Actions, container base images, and external build dependencies are pinned to immutable commit SHAs.
  - Third-party MCP servers are validated against the organizational allowlist and verified registry provenance.
- **ASI05 Unexpected Execution & Sandbox Verification**:
  - Automated sandbox escape tests verify that agent-generated scripts and test runners cannot access host environments or unauthorized network ports.
  - Dynamic string evaluation and shell execution paths are actively probed for injection vectors.
  - Test suites execute within ephemeral container sandboxes with network egress restricted to authorized mock endpoints.

### AI / LLM System Validation (when applicable)
- property-based assertions defined (no exact-match assertions for non-deterministic outputs)
- golden dataset version-controlled and seeded with production failures
- LLM-as-Judge calibrated against human benchmarks before use as a deployment gate
- trajectory evaluation conducted for multi-step agents (not just final output)
- tool-call accuracy validated (parameters, selection, no unauthorized chaining)
- hallucination cascade mitigation verified at intermediate steps
- context window exhaustion simulated for multi-turn interactions
- adversarial tool-chaining and privilege escalation test cases included
- CI/CD regression gate configured against golden dataset
- **CI eval gate passes** for prompt/model/tool changes (golden dataset, calibrated judge ≥85%)

### MCP & Agent Validation (when applicable)
- **MCP stateless protocol validated**: HTTP transport, externalized session state, registry allowlist
- **WebMCP validated**: context emission, action allowlist, HITL modals, background sync, origin validation
- **A2A contract tests pass**: schema validation, behavioral invariants, error envelope for all agent boundaries
- **MCP schema drift detection**: pinned schemas diff-checked in CI against live registry

### EU AI Act Compliance (when AI features in scope)
- Article 50 disclosure UI validated: `<AIDisclosureBanner>` before first interaction, plain language
- C2PA marking verified on AI-generated media (deadline 2026-12-02)
- Annex type identified with correct deadline (Annex III: 2027-12-02; Annex I: 2028-08-02)
- `data-ai-generated="true"` attributes on AI-rendered containers

### Resilience & Chaos Engineering (when applicable)
- chaos experiment charter documented (hypothesis, fault type, scope, success criteria, result)
- graceful degradation validated under controlled fault injection
- recovery behavior validated: system returns to health without manual intervention within MTTR target
- shift-right rollback trigger criteria defined and observable in production telemetry
- production near-misses surfaced and added to golden dataset or regression checklist

### Accessibility (WCAG 2.2, when UI is in scope)
- automated a11y scan completed (contrast, ARIA, heading structure, alt text)
- keyboard-only navigation tested for critical flows
- screen reader walkthrough conducted for P0 user journeys
- WCAG 2.2 new criteria checked: Focus Not Obscured, Dragging Movements, Target Size
- a11y defects classified with same severity framework as functional defects
