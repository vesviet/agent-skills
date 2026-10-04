## Review Checklist

This reference checklist provides detailed test engineering, quality gates, and resilience validation criteria for QA engineering to meet 2026–2027 Agentic SWE and Principal Verification standards. It synthesizes The Great Verification Convergence across deterministic contracts, calibrated AI evaluation, trace-based assertions, shift-left chaos, empirical verification-before-completion gates, pairwise combinatorial optimization, and clean architecture isolation.

### 1. Consumer-Driven Contract Testing (CDCT) & Wire Evolution
- **PactV3 / Pact-Go v2 Protocol Compliance**:
  - consumer contracts define structural type matchers (`MatchersV3.like`, `MatchersV3.regex`, `MatchersV3.iso8601`) rather than brittle literal value assertions
  - provider verification suites in Go Kratos and TypeScript implement isolated `ProviderState` handlers to set up test state without persistent data contamination
  - Pact contract files are published to the central Pact Broker with semantic versioning and environment tagging
- **Pact Broker can-i-deploy Release Gate**:
  - `pact-broker can-i-deploy` verification CLI executed in CI/CD release pipelines
  - matrix compatibility verified between consumer version and deployed provider versions across staging, canary, and production environments; fail-closed on unverified contracts
- **Protobuf Wire Compatibility & Schema Evolution**:
  - `buf breaking --against '.git#branch=origin/main'` executed in CI against all Protobuf and gRPC interface definitions
  - `WIRE_JSON` rule sets enforced to detect field tag renumbering, field type mutations, and reserved tag violations before merge
- **OpenAPI 3.1 & AsyncAPI 3.0 Verification**:
  - REST API contract diffs verified via `oasdiff breaking --fail-on ERR` to reject backward-incompatible endpoint changes
  - asynchronous event payloads validated against central AsyncAPI schema registries, asserting event type, routing key, schema version, and envelope compliance

### 2. Systematic Root Cause Analysis (4-Phase Debugging)
- **Phase 1: Observation & Deterministic Reproduction**:
  - exact symptoms, error logs, stack traces, and environmental preconditions captured without alteration
  - defect isolated to a minimal, deterministic reproduction script or automated reproduction test case
  - reproduction consistency verified across repeated executions to eliminate timing or flaky environmental factors
- **Phase 2: Architectural Hypothesis Formulation**:
  - code paths, component boundaries, and state transitions mapped to relevant architectural invariants
  - explicit, testable, and falsifiable hypotheses formulated explaining the underlying causal mechanism
  - surface-level symptoms strictly distinguished from fundamental root causes; superficial patches rejected
- **Phase 3: Targeted Experimentation & Falsification Testing**:
  - targeted instrumentation or assertions designed to prove or disprove each candidate hypothesis
  - automated reproduction test authored and verified failing (Red phase) on the unfixed baseline codebase
  - failure mode verified to match the specific hypothesized defect rather than secondary compilation or runtime errors
- **Phase 4: Root-Cause Correction & Recurrence Prevention**:
  - minimal, surgical fix applied directly to the root mechanism; speculative workarounds rejected
  - fix verified passing the reproduction test (Green phase) and full adjacent regression suite without side-effect regressions
  - architectural guards (invariants, schema validation, type constraints, lint rules) added to prevent recurrence

### 3. Verification Before Completion (VBC) & Epistemic Doubt Gates
- **Empirical Execution Proof**:
  - fresh, un-cached test execution completed on the final codebase; reliance on stale or prior-turn passes strictly prohibited
  - explicit exit code 0, complete command logs, and passing assertion traces captured and verified
  - test environment verified for parity with production configuration, flags, and data dependencies
- **Epistemic Doubt Enforcement**:
  - absence of visible errors treated as insufficient evidence of correctness; active boundary probing required
  - code execution verified: confirmed that modified logic was actually traversed during the test run
  - confirmation bias eliminated: verified that negative test assertions fail when defect conditions are present
- **Zero False-Green Sign-Off**:
  - stateful side effects verified: persistence mutations, outbox messages, and cache updates explicitly asserted
  - assertions audited to eliminate assertion theater (e.g. replacing trivial `toBeDefined()` checks with invariant evaluations)
  - all executed checks, commands, logs, and residual risks documented in `contracts/schemas/validation-result.json` and `contracts/schemas/test-report.json`

### 4. Pairwise Combinatorial Testing & Matrix Optimization
- **Factor Space & Boundary Level Modeling**:
  - input variables, configuration switches, environmental dimensions, and feature flags cataloged
  - factor values partitioned into discrete equivalence classes and boundary values
  - constraint rules specified to prune impossible, invalid, or mutually exclusive combinations
- **Pairwise Covering Array Generation**:
  - combinatorial reduction algorithms (PyPICT, IPO) applied to generate optimal 2-way test matrices
  - 100% pairwise interaction coverage across all factor pairs verified with minimal execution footprint
  - exponential Cartesian explosion $O(V^K)$ reduced down to logarithmic test suites $O(K \log V)$
- **Higher-Order N-Way Invariant Testing**:
  - higher-order N-way combinations (3-way/4-way) evaluated and applied for safety-critical, financial, or authentication workflows
  - failing combinations analyzed to isolate interacting parameter pairs causing the defect

### 5. Calibrated AI & Agentic System Evaluation
- **Calibrated LLM-as-a-Judge**:
  - automated LLM-as-a-judge evaluators (DeepEval G-Eval, Prometheus-2) use explicit rubric decomposition into Chain-of-Thought scoring steps (1 to 5 scale)
  - statistical calibration achieving $\ge 85\%$ agreement (Cohen's Kappa $\ge 0.85$ or Pearson $r \ge 0.85$) against human ground-truth ratings on a minimum 100-sample benchmark set before CI merge
  - verbosity, length, and sycophancy biases mitigated via logprob-weighted length normalization
- **RAG Triad & Grounding Verification**:
  - retrieval-augmented generation pipelines meet grounding thresholds in CI:
    - Faithfulness $\ge 0.85$ (generated claims mathematically entailed by retrieved context)
    - Context Precision $\ge 0.85$ (relevant retrieved chunks rank higher than irrelevant chunks)
    - Context Recall $\ge 0.85$ (ground-truth facts captured within retrieved context)
    - Answer Relevancy $\ge 0.85$ (semantic similarity between query and response embeddings)
  - exact-match or superficial regex checks on generated text strictly prohibited; property-based semantic assertions enforced
- **Agent Trajectory & Multi-Step Execution QA**:
  - intermediate tool-call invocation order validated against directed acyclic graph (DAG) precedence rules
  - tool invocation payload arguments validated against strict Pydantic v2 / JSON Schema specifications
  - automated cycle and loop detection executed via sequence N-gram matching and consecutive state hashing to terminate infinite ping-pong loops
  - A2A inter-agent contract schemas (`contracts/schemas/a2a-*.json`) validated to prevent schema drift
- **Prompt Regression & Red-Teaming**:
  - automated prompt regression test suites executed via Promptfoo against OWASP LLM01–LLM10 vulnerabilities
  - context window exhaustion simulated for multi-turn interactions
  - adversarial tool-chaining and privilege escalation test cases included

### 6. Observability-Driven Testing (ODT) & Trace-Based Assertions
- **Trace-Based Assertions via Kubeshop Tracetest**:
  - OpenTelemetry distributed traces evaluated as test oracles, asserting full trace DAGs rather than superficial HTTP status codes
  - Tracetest DSL specs assert span hierarchy: `HTTP Entrypoint` $\rightarrow$ `Service Adapter` $\rightarrow$ `GORM Database` $\rightarrow$ `Dapr/Kafka Outbox Publisher`
  - span attributes (HTTP status, database table, SQL operation, message topic) and span latency SLO budgets (database query $< 50\text{ms}$, total handler $< 200\text{ms}$) verified
- **W3C Trace Context Propagation**:
  - unbroken propagation of W3C `traceparent` and `tracestate` headers verified across HTTP, gRPC, and asynchronous message hops
  - zero orphan spans and zero broken trace graphs in asynchronous worker queues and event consumers
- **Automated $N+1$ Database Query Prevention**:
  - automated query counters embedded into database integration test suites, intercepting GORM/SQL statement execution
  - constant $O(1)$ query complexity enforced relative to collection size $N$; maximum query budgets enforced per endpoint
  - zero unindexed sequential scans (`Seq Scan`) on critical database tables asserted via automated `EXPLAIN ANALYZE` execution plan inspection
- **eBPF Kernel-Level Runtime Inspection**:
  - Cilium Tetragon and Beyla sensors integrated in test environments to monitor system calls (`sys_enter_connect`, `sys_enter_execve`)
  - execution sandboxes verified to make zero unauthorized network egress connections or unexpected subprocess spawns

### 7. Modern Web, Browser Automation & Accessibility (Playwright v1.48+)
- **Playwright v1.48+ Automation Standards**:
  - browser tests executed in isolated browser contexts with automated Trace Viewer capture on test failure
  - transport-level network interception enforced via Mock Service Worker (MSW v2) or HAR network replay; application-level monkey-patching of `window.fetch` strictly prohibited
  - arbitrary sleep calls (`page.waitForTimeout`) eliminated; Playwright web-first assertions with locator auto-waiting (`await expect(locator).toBeVisible()`) enforced
  - multi-context actor orchestration supported to simulate concurrent multi-user/multi-agent interactions in real time
- **Automated WCAG 2.2 AA Accessibility Gates**:
  - automated `@axe-core/playwright` accessibility audits executed across all primary pages and dynamic component states; builds with critical or serious violations rejected
  - keyboard navigation flows verified: logical Tab order sequence asserted, modal dialogs trap keyboard focus within boundaries, and Escape key restores focus to the trigger element
  - screen reader accessibility tree verified using Playwright ARIA snapshots (`expect(locator).toMatchAriaSnapshot()`)
  - WCAG 2.2 new criteria checked: Focus Not Obscured (2.4.11), Target Size (2.5.8), Accessible Authentication (3.3.8), Dragging Movements (2.5.7), Redundant Entry (3.3.7)
- **Font-Stabilized Visual Regression Testing**:
  - false-positive visual diffs eliminated by awaiting font render stabilization (`document.fonts.ready`) before snapshot capture
  - dynamic UI elements (timestamps, user avatars, animated banners) masked with strict pixel diff tolerance thresholds ($\le 0.1\%$)
  - visual regression suites executed inside standardized Linux Docker containers to eliminate cross-platform font rendering divergence

### 8. Shift-Left Chaos, Resilience & Performance Gates
- **In-Test Network Fault Injection via Shopify Toxiproxy**:
  - Toxiproxy TCP proxies embedded into integration test setups to simulate network latency, jitter, bandwidth throttling, and TCP connection resets
  - circuit breaker finite state transitions verified (Sony gobreaker): `CLOSED` $\rightarrow$ `OPEN` upon breach of error rate threshold $\rightarrow$ single-canary probe in `HALF-OPEN` $\rightarrow$ `CLOSED` recovery
  - fallback execution paths asserted and downstream timeouts verified to return graceful degraded responses rather than unhandled panics or HTTP 500 crashes
- **Mathematical Exponential Backoff Verification**:
  - retry policies verified to implement AWS full jitter: $Sleep = \text{random}(0, \min(M, B \times 2^{\text{attempt}}))$ to mathematically prevent thundering herd collisions
  - client-side idempotency key propagation asserted across retry attempts
- **Distributed Performance Gates with Grafana k6**:
  - automated k6 load tests executed in CI pipelines enforcing strict Service Level Objectives (SLOs):
    - P95 latency $< 150\text{ms}$
    - P99 latency $< 300\text{ms}$
    - HTTP error rate $< 0.1\%$
  - k6 threshold rules configured to exit with non-zero exit code (exit code 99) upon SLO breach, blocking deployment

### 9. Clean Architecture Multi-Language QA (Go 1.25+, Python, TypeScript)
- **Go 1.25+ Kratos Clean Architecture Test Isolation**:
  - Kratos 4-layer separation strictly enforced: `api/` (contracts) $\rightarrow$ `internal/service` (adapters) $\rightarrow$ `internal/biz` (business invariants) $\rightarrow$ `internal/data` (GORM persistence)
  - zero database ORM (`gorm.DB`) leakage into `internal/biz`; domain invariants testable via pure unit tests with zero I/O
- **Ephemeral Database Parity via Testcontainers-Go**:
  - in-memory SQLite mocks replaced with real PostgreSQL 16 Alpine containers spun up programmatically via `testcontainers/testcontainers-go` managed by Ryuk reaper
  - complete engine feature parity ensured (JSONB operations, window functions, concurrency locks, indexing)
- **Zero-Dirty State with GORM `InTx` Rollbacks**:
  - each database integration test wrapped in an explicit transaction (`tx := db.Begin()`), repository operations executed within the transaction, and deferred `tx.Rollback()` invoked on teardown
  - zero test pollution and zero state bleeding guaranteed across parallel test executions without costly database truncations
- **Dependency Injection Isolation via Google Wire**:
  - custom Wire test provider sets (`wire.Build(ProviderSet, TestDBSet)`) inject ephemeral Testcontainers instances into services without modifying production wiring
- **Race Condition & Goroutine Leak Safety**:
  - all Go test suites executed with race detector enabled: `go test -v -race -timeout 300s ./...`
  - zero leaked background goroutines verified on test suite termination using `uber-go/goleak`
- **Cross-Language Property-Based Testing (PBT)**:
  - Python: pytest with Hypothesis for stateful state machine testing (`RuleBasedStateMachine`) and automatic minimal counter-example shrinking
  - TypeScript: Vitest with fast-check for serialization round-trips and algebraic invariant verification across 10,000 randomized iterations

### 10. Mutation Testing Infrastructure & OWASP ASI Security Gates
- **Mutation Testing Execution & Thresholds**:
  - mutation testing executed via Stryker (TypeScript), Mutmut (Python), cargo-mutants (Rust), or go-mutesting (Go) against core modules
  - mutation score threshold $\ge 75\text{--}80\%$ enforced on core business logic, financial calculations, authentication, and domain invariant routines
  - mutation test reports audited to confirm surviving mutants are killed with high-value behavioral assertions rather than superficial checks
  - zero mock mutation evasion: tests mutate real execution paths rather than mocked-out code stubs
- **OWASP ASI04 Supply Chain Verification**:
  - all project dependencies verified against lockfile integrity hashes; dependency audit passes with zero critical/high CVEs
  - GitHub Actions, container base images, and external build dependencies pinned to immutable commit SHAs
  - third-party MCP servers validated against organizational allowlist and verified registry provenance
- **OWASP ASI05 Unexpected Execution & Sandbox Verification**:
  - automated sandbox escape tests verify that agent-generated scripts and test runners cannot access host environments or unauthorized network ports
  - dynamic string evaluation and shell execution paths actively probed for injection vectors
  - test suites execute within ephemeral container sandboxes with network egress restricted to authorized mock endpoints

### 11. MCP & Agent System Validation (when applicable)
- **MCP stateless protocol validated**: HTTP transport, externalized session state, registry allowlist
- **WebMCP validated**: context emission, action allowlist, HITL modals, background sync, origin validation
- **A2A contract tests pass**: schema validation, behavioral invariants, error envelope for all agent boundaries
- **MCP schema drift detection**: pinned schemas diff-checked in CI against live registry

### 12. EU AI Act Compliance (when AI features in scope)
- **Article 50 disclosure UI validated**: `<AIDisclosureBanner>` before first interaction, plain language
- **C2PA marking verified**: verified on AI-generated media (deadline 2026-12-02)
- **Annex type identified**: correct compliance deadline tracked (Annex III: 2027-12-02; Annex I: 2028-08-02)
- **Metadata attributes verified**: `data-ai-generated="true"` attributes on AI-rendered containers

### 13. Distributed System Foundation & Blast Radius Containment
- acceptance criteria are **observable** and mapped to explicit assertions (clear pass/fail oracles)
- critical user journeys include negative paths and boundary cases, not only happy paths
- permissions, roles, and multi-tenancy are validated where applicable (no cross-tenant leakage)
- data correctness is verified (not only responses): invariants, constraints, and persistence state
- side effects are verified: events published/consumed, cache behavior, search indexing, downstream calls
- async flows are validated with eventual consistency in mind (timing windows and retries)
- defects include environment, reproduction steps, expected vs actual behavior, evidence, and suspected blast radius
- blast radius assessment verifies failure domain containment; zero cross-boundary impact detected
- skipped checks and residual risk are explicit, justified, and documented in `contracts/schemas/test-report.json`
- release confidence is supported by empirical evidence, not confidence language
