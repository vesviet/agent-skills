# Test Patterns, AI Testing & Mocking Standards — Reference

This reference provides deep guidance on test scopes, testing trophy distribution, reusable test design patterns, AI/LLM evaluation strategies, and network boundary mocking.

---

## 1. Choose The Right Test Scope (Testing Trophy)

Align test distribution with the Testing Trophy: **heavy integration, focused unit, lean E2E, strict contract boundaries**.

### 1.1 Unit Tests
- **Best for**: Pure domain algorithms, mathematical calculations, schema validation logic, state machine transitions, and parsing.
- **Characteristics**: Extremely fast (sub-millisecond), in-memory, zero external I/O, zero network calls.
- **Guideline**: Test behavior and edge-case contracts, not internal private helper implementations.

### 1.2 Integration Tests
- **Best for**: Repository queries against real databases (testcontainers), HTTP handler wiring, middleware chains, serialization/deserialization boundaries, cache layer invalidation.
- **Characteristics**: Executes against ephemeral local services; verifies component collaboration.
- **Guideline**: Isolate using containerized sandbox fixtures; do not connect to external shared staging databases.

### 1.3 Contract & Inter-Service API Tests
- **Best for**: Request/response payload compatibility, versioned wire schemas, consumer/provider assumptions across microservices.
- **Tooling**: Pact contract testing.
- **Quality Gate**: Run Pact `can-i-deploy` verification in CI before merging service PRs.

### 1.4 End-To-End (E2E) Tests
- **Best for**: Critical user journeys, multi-service core flows, smoke testing deployment readiness.
- **Guideline**: Keep lean; E2E tests are slower and fragile. Never use E2E tests to verify edge-case branching that can be tested in unit or integration tests.

---

## 2. Good Testing Patterns

- **Table-Driven / Parameterized Tests**: Group related test inputs and expected outputs in a declarative table to exercise multiple boundary conditions cleanly.
- **Focused Fixtures**: Maintain fixtures with only the minimal fields required for the specific test scenario. Avoid mega-fixtures with 100 unused properties.
- **Object Mothers / Builders**: Use fluent builders with sensible defaults for complex domain models so tests only override the property being verified.
- **Regression Naming**: Name regression tests after the specific bug and behavior being protected (e.g., `test_order_cancellation_refunds_tax_when_partial_items_cancelled`).

---

## 3. Common Testing Mistakes & Anti-Patterns

1. **Testing Implementation Details**: Asserting that a private method was called or checking internal object fields instead of observing public behavior and side effects. Refactoring internal structure breaks the test even when behavior is unchanged.
2. **Over-Mocking**: Mocking simple pure functions, math utilities, or value objects that could be executed directly. Mocks should be reserved for external I/O and process boundaries.
3. **Mock Collusion**: Designing mocks that mirror the exact faulty logic of the code under test, leading to passing tests on broken code.
4. **Sleep-Based Timing**: Using `time.sleep()` or `setTimeout()` instead of condition polling, explicit synchronization, or event waiting, introducing flakiness.
5. **Coverage Theater**: Writing assertions like `expect(result).toBeDefined()` or chasing 100% line coverage without verifying actual business state changes.

---

## 4. AI & LLM Feature Testing Patterns

Testing probabilistic and generative components requires specialized validation techniques:

### 4.1 Structural Over Exact Assertions
- Model responses vary between versions and runs. Never assert on exact string equality.
- Assert on JSON schema compliance, mandatory keys, data types, and value bounds (e.g. word count bounds, sentiment polarity range).

### 4.2 Semantic & Classifier Evaluation
- Use property-based evaluations for qualitative requirements: language detection ("response is in Vietnamese"), toxic content filters, PII absence.
- For structured extraction, verify accuracy against labeled ground truth evaluation sets.

### 4.3 Golden-Set Baselines
- Maintain an immutable golden dataset representing production queries and expected output properties.
- Execute automated regression benchmarking before adopting any prompt change or model version upgrade.
- Flag any regression on the golden set as a release-blocking failure.

### 4.4 Deterministic CI Stubs (VCR Pattern)
- **Never call live LLM APIs during CI test runs**.
- Record real interactions once as sanitized network cassettes (VCR / Polly.js) and replay deterministically in CI.
- Test adversarial false-premise prompts and verify human-in-the-loop (HITL) fallback triggers execute correctly when confidence drops below thresholds.

---

## 5. Network Boundary Mocking Standards

- **MSW v2 (Mock Service Worker)**: The standard for HTTP network mocking in TypeScript/Node.js environments. Intercepts requests at the network transport layer rather than monkey-patching `global.fetch` or internal Axios clients.
- **Ephemeral Fixtures**: Use local mock servers (WireMock, Go `httptest.Server`, Python `responses` / `pytest-mock`) for deterministic failure injection (timeouts, HTTP 500/503 responses, corrupted JSON payloads).
