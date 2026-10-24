## Reviewer Review Checklist

This reference checklist provides detailed adversarial review rubrics, deep code inspection matrices, and security gates to meet 2027 Agentic SWE standards.

### 1. Adversarial Anti Vibe-Slop Review Rubric
AI coding tools frequently generate code that appears syntactically elegant, idiomatic, and compiles cleanly, but harbors subtle flaws ("vibe slop"). Reviewers must apply active adversarial scrutiny:
- **Tautological or Fake Test Assertions**: Detect tests that assert trivial truths (e.g., `expect(true).toBe(true)`, testing mocked values against mocks, or omitting negative branch checks).
- **Happy-Path Illusion**: Detect functions that cleanly execute the primary flow but omit null handling, boundary overflow protection, timeout handling, or partial error recovery.
- **Hallucinated Domain Semantics**: Scrutinize business logic for invented business rules, incorrect status transitions, or subtle assumptions not supported by the domain specification.
- **Swallowed Failures**: Catch empty `catch` blocks, generic default fallbacks that mask upstream errors, or logging without propagating failure context.
- **Shallow Interface Implementation**: Detect components or handlers where method stubs return dummy success objects or mock responses instead of real execution logic.

### 2. Mutation & Property Test Verification
- **Mutation Testing Verification**:
  - Core domain logic, security routines, and financial/invariant paths must achieve a mutation score ≥ 75–80% (via Stryker, Mutmut, or equivalent).
  - High line coverage without mutation survival proof is rejected for critical business paths.
  - Review mutation reports to confirm that killed mutants reflect genuine behavioral assertions, not accidental side-effect detection.
- **Property-Based Testing Verification**:
  - Invariants, state machines, serialization/deserialization, and mathematical calculations are tested via property-based test suites (such as fast-check, Hypothesis, or proptest).
  - Tests verify that round-trips, idempotency, and boundary invariances hold across randomized inputs.
  - Shrinkage examples from property tests are inspected to verify edge cases were properly remediated.

### 3. Deep Code Inspection Matrix (Concurrency, Leaks, N+1 Queries)
- **Concurrency & Race Conditions**:
  - Unsynchronized shared memory access or unprotected global/module-level mutable state.
  - Check-then-act (TOCTOU) races in database transactions or cache checks.
  - Missing lock acquisitions or inconsistent lock acquisition ordering causing deadlocks.
  - Unmanaged goroutines or background promises spawned without proper context cancellation.
- **Memory & Resource Leaks**:
  - Unclosed file descriptors, database connections, HTTP response bodies, or streams.
  - Event listeners, subscriptions, or timers registered without unmount/cleanup lifecycles.
  - Missing `AbortController` cancellation on async requests and streaming connections.
  - Accumulation of unbounded data in cache structures or global maps without eviction policies.
- **N+1 Database Queries**:
  - ORM lazy-loading loops in API endpoints, serializers, or batch tasks.
  - Missing batching or eager loading (`select_related`, `prefetch_related`, DataLoader).
  - Unbounded `SELECT *` queries executed inside iteration blocks.

### 4. OWASP ASI04 (Supply Chain) & ASI05 (Unexpected Execution) Gates
- **OWASP ASI04 (Supply Chain Security)**:
  - All newly introduced dependencies have verified provenance in official package registries.
  - No typo-squatted, unmaintained, or zero-reputation packages.
  - Lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`) are updated with exact hash integrity checks.
  - CI workflows and GitHub Actions are pinned to immutable commit SHAs, not mutable tags.
  - Third-party MCP servers are verified against the organizational allowlist.
- **OWASP ASI05 (Execution Sandbox Isolation & Unexpected Execution)**:
  - No dynamic string evaluation (`eval()`, `new Function()`, `exec()`, `shell=True`).
  - Agent-generated scripts, test runs, and database seeding execute inside hardened, ephemeral sandboxes with restricted network egress.
  - UI previews of third-party or AI-generated components run in sandboxed iframes (`sandbox="allow-scripts"` without `allow-same-origin`) or Web Workers.
  - Untrusted user input or LLM output is never passed directly to command shells or raw database query strings.

### 5. Scope Containment & API Existence Verification
- **Scope Creep Gate**:
  - Every modified file maps directly to the stated intent of the feature or bug fix.
  - Unrelated cleanup or drive-by refactoring in high-risk slices is rejected and required to be split into a separate PR.
- **API Existence Check**:
  - Every imported method, module, or configuration key exists in the current installed dependency versions.
  - No hallucinated parameters, deprecated methods, or non-existent endpoint URLs.

### 6. MCP Tool Contracts & LLM Structured Outputs
- **MCP Tool Contracts**:
  - SemVer version declared and incremented appropriately (major bump for breaking schema changes).
  - JSON Schema is the single source of truth for tool arguments and return values.
  - Tool behavioral guarantees (idempotency, rate limits, error envelopes) are documented.
- **LLM Structured Outputs**:
  - Provider-level constrained decoding enforced (native Structured Outputs or grammar constraints).
  - Runtime schema validation applied as defense-in-depth; no regular expression parsing.
