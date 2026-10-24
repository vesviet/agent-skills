# Advanced Testing Methodologies — Reference

This reference documents 2027 Agentic SWE testing standards: Independent Test Authoring (Anti-Tautological TDD), Property-Based Testing (PBT), Edge Case Synthesis taxonomy, Mutation Testing execution, and Sandbox isolation.

---

## 1. Independent Test Authoring (Anti-Tautological TDD)

### 1.1 The Risk: Test-Implementation Co-Leakage
When an AI agent writes both the implementation and its tests within the same context or turn, tests frequently inherit the agent's hallucinations, unverified assumptions, and off-by-one errors. The resulting tests are **tautological** — they pass because they verify what the code *does*, not what the specification *demands*.

### 1.2 The Protocol
1. **Spec-Isolated Authoring**: Tests must be authored directly from the immutable contract (`OpenAPI 3.1`, `JSON Schema`, `Protobuf`, or `feature-ticket.json`), independently from the implementation logic.
2. **Strict Red Phase Verification**: Author the test suite and execute it inside the sandbox against the baseline codebase *before* any implementation code is introduced.
3. **Deterministic Failure Proof**: The test suite must fail with expected assertions (e.g. `MethodNotImplemented`, missing field, assertion mismatch). If a new test passes against baseline code without implementation changes, it is either redundant or tautological and must be investigated.
4. **Implementation Phase (Green)**: Author minimal code to turn tests green without altering the test assertions to match the code.

---

## 2. Property-Based Testing (PBT)

Property-Based Testing replaces hardcoded example assertions with mathematical and structural invariant properties verified across hundreds or thousands of automatically generated inputs.

### 2.1 Tooling
- **TypeScript / JavaScript**: `fast-check`
- **Python**: `Hypothesis`
- **Go**: `RapidCheck` / `testing/quick`
- **Rust**: `proptest` / `quickcheck`

### 2.2 Core Invariant Classes

| Invariant Class | Mathematical Definition | Concrete Software Example |
|---|---|---|
| **Round-Trip Serialization** | $f^{-1}(f(x)) == x$ | Serialize to JSON/Protobuf then deserialize; parse URL query string then format back. Output must identically match input. |
| **Idempotence** | $f(f(x)) == f(x)$ | Applying formatters, cleanups, state updates, payment reconciliation, or database upserts twice yields identical state to applying once. |
| **State Transition Invariants** | $\forall s, a: \text{Valid}(s) \implies \text{Valid}(\text{Next}(s, a))$ | State machine guarantees (e.g. account balance $\ge 0$, order total equals sum of line items plus tax, no ghost states). |
| **Metamorphic Relations** | $f(x \cup y) \equiv f(x) \oplus f(y)$ | Searching with narrower filter returns subset of wider search; sorting an already sorted array yields same array. |
| **Error Monotonicity** | Invalid input $x$ always produces RFC 9457 error regardless of extra optional parameters. | Fuzzing optional query params never bypasses mandatory validation checks. |

### 2.3 Automated Test Case Shrinking
When a property fails, the PBT engine automatically shrinks the failure input to the minimal reproducible counterexample (e.g. shrinking a 500-character random string with complex Unicode to `"\x00"` or `"\n"`), vastly reducing debugging overhead.

---

## 3. Systematic Edge Case Synthesis Taxonomy

Rather than relying on ad-hoc brainstorming, synthesize edge cases systematically across these six boundary categories:

### 3.1 Numeric & Memory Bounds
- Integer extremes: `0`, `-1`, `1`, `MAX_INT32`, `MIN_INT32`, `MAX_INT64`, `MIN_INT64`, `2^53 - 1` (JavaScript `Number.MAX_SAFE_INTEGER`).
- Floating point hazards: `+0.0`, `-0.0`, `NaN`, `+Infinity`, `-Infinity`, subnormal floats, catastrophic cancellation in financial calculations (mandate Decimal / BigNumber).
- Off-by-one indices: `0`, `len - 1`, `len`, `len + 1`, empty slices, capacity vs length discrepancies.

### 3.2 Unicode, Strings & Formatting
- Multi-byte encodings: UTF-8 4-byte astral characters (emojis `👨‍👩‍👧‍👦`, supplementary plane symbols).
- Text direction: Right-to-Left (RTL) strings (Arabic, Hebrew) mixed with LTR (BiDi text).
- Invisible characters: Zero-width joiners (`\u200D`), zero-width spaces (`\u200B`), soft hyphens.
- Unicode normalization: Strings differing in NFC vs NFD forms (e.g. `é` as `\u00E9` vs `e\u0301`).
- Special string payloads: SQL injection patterns (`' OR 1=1 --`), path traversal (`../../etc/passwd`), null bytes (`\0`).

### 3.3 Temporal & Clock Anomalies
- Calendar transitions: Leap years (Feb 29), non-leap century years (1900, 2100), year-end roll-overs (Dec 31 23:59:59 → Jan 1 00:00:00).
- Clock adjustments: Daylight Saving Time (DST) forward/backward leaps, leap seconds, negative time diffs due to NTP clock synchronization jumps.
- Timezone offsets: Non-hour timezone offsets (e.g. UTC+05:30, UTC+08:45), parsing timestamps missing timezone specifiers.

### 3.4 Concurrency, State & Resource Bounds
- Race conditions: Concurrent identical writes (duplicate key / TOCTOU bugs).
- Connection starvation: Pool exhaustion under simulated slow database queries.
- Truncated streams: Premature HTTP client disconnection mid-payload.
- Re-entrancy: Nested calls during event emission or hook execution.

---

## 4. Mutation Testing Operational Guide

Code coverage metrics (lines, branches) only prove code was *executed*; mutation testing proves tests *assert correctness*.

### 4.1 How It Works
Mutation tools introduce deliberate synthetic faults (mutants) into production code:
- Inverting conditionals (`if (a > b)` $\to$ `if (a <= b)`)
- Swapping arithmetic operators (`+` $\to$ `-`)
- Removing function calls or early-returning `null` / `void`
- Altering boundary conditions (`>=` $\to$ `>`)

### 4.2 Quality Gate & Scoring
$$\text{Mutation Score} = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \times 100\%$$

- **Enforcement Rule**: Critical business logic, authentication, financial math, and core parsers must achieve **≥ 75–80% mutation kill score**.
- **Surviving Mutants Analysis**:
  - *Genuine Bug / Missing Assertion*: Code modified without any test failure. Add targeted assertions.
  - *Equivalent Mutant*: Code mutated into semantically equivalent behavior (e.g., optimization that produces identical results). Annotate or ignore.
- **Tools**: Stryker (TypeScript/JavaScript/C#), `mutmut` / `cosmic-ray` (Python), `cargo-mutants` (Rust), `go-mutesting` (Go).

---

## 5. Physical Sandbox Execution Isolation

All test suites must execute within containerized isolation per `core/policies/execution-sandbox.md`:
- **Network Isolation**: `--network=none` for all unit and integration tests. Network calls must be mocked via MSW v2 or local fixtures.
- **Unprivileged Runtime**: Tests must execute under non-root UID (`USER 1000:1000`).
- **Filesystem Protection**: Read-only root filesystem (`--read-only`), with ephemeral writes restricted to in-memory `tmpfs` mounts at `/tmp`.
- **Zero Ambient Secrets**: Environment variables must contain only test fixture tokens, never ambient developer or production cloud credentials.
