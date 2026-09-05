---
name: write-tests
description: Add or update tests by following repo-local test conventions, choosing the right test scope, isolating dependencies, and validating risky paths before delivery. Use when behavior needs regression coverage or release confidence.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Write Tests

Use this skill to author independent, property-verified, and mutation-tested test suites that provide regression resilience.

## When to Use

- new business logic, API endpoint, or data transformation needs coverage
- practicing Red-Green TDD with independent test authoring prior to implementation
- verifying mathematical and structural invariants via Property-Based Testing (PBT)
- synthesizing combinatorial boundary and edge-case suites
- enforcing mutation test kill thresholds (≥75–80%) on critical packages
- executing test suites inside isolated sandboxes

## Core Rules

- **Independent test authoring (Anti-Tautological TDD)**: author tests directly from immutable contracts/specs *before* writing code; verify tests fail deterministically (Red phase) against baseline to prevent test-implementation co-leakage
- **Property-based testing (PBT)**: verify invariants (round-trip serialization, idempotence, state transition constraints) using generative engines (`fast-check`, `Hypothesis`, `RapidCheck`) with automatic shrinking
- **Edge case synthesis**: systematically synthesize boundary cases across numeric extremes, Unicode/RTL/invisible characters, temporal/timezone shifts, and concurrency hazards
- **Mutation testing quality gate**: enforce mutation score ≥75–80% via Stryker, mutmut, or cargo-mutants on core libraries; raw line coverage without mutation kill rate is insufficient
- **Physical sandbox execution**: all test executions must run inside isolated Level 0 air-gapped containers (`--network=none`, non-root user, read-only rootfs) per `core/policies/execution-sandbox.md`
- **Testing Trophy distribution**: focus on heavy integration, focused unit, and lean E2E; isolate external HTTP dependencies via MSW v2 or local fixtures
- **AI/LLM feature testing**: use structural assertions (JSON shape, bounds) over exact string equality; evaluate semantic properties with classifiers; stub LLM calls in CI with VCR cassettes
- run Pact `can-i-deploy` checks in CI for inter-service contract verification
- deep methodologies and pattern guides: [`references/advanced-testing-methodologies.md`](references/advanced-testing-methodologies.md) and [`references/patterns-and-ai-testing.md`](references/patterns-and-ai-testing.md)

## Suggested Process

### Step 1: Spec Review & Test Scoping

Read the contract spec (`OpenAPI 3.1`, `JSON Schema`, or ticket). Select test scope using the Testing Trophy (unit for pure domain rules, integration for queries/handlers, contract for APIs).

### Step 2: Independent Test Authoring (Red Phase)

Write deterministic tests based solely on the specification before changing implementation code. Run tests in the execution sandbox to confirm they fail as expected.

### Step 3: Property & Edge Case Synthesis

Formulate property-based invariants (idempotence, round-trip). Synthesize boundary cases covering numeric extremes, Unicode, timezone shifts, and empty/nil structures per [`references/advanced-testing-methodologies.md`](references/advanced-testing-methodologies.md).

### Step 4: Implement & Verify (Green Phase)

Author minimal implementation to satisfy the tests. Execute the test suite inside the Level 0 air-gapped sandbox (`--network=none`) to verify green status.

### Step 5: Mutation Testing & Coverage Audit

Run mutation tests (Stryker / mutmut) across changed packages. Verify mutation kill score reaches ≥75–80%. Eliminate surviving non-equivalent mutants by tightening assertions.

### Step 6: Emit Test Report

Generate test artifacts. Report execution results and coverage metrics to downstream coordinating roles.

## Checklist

- [ ] tests authored independently from spec and verified failing (Red phase) before implementation
- [ ] property-based tests (PBT) formulated for core data invariants and transformations
- [ ] edge case synthesis applied across numeric, Unicode, temporal, and concurrency boundaries
- [ ] mutation testing executed with kill score meeting or exceeding ≥75–80% threshold
- [ ] tests executed inside isolated Level 0 air-gapped sandbox (`--network=none`, non-root)
- [ ] network boundaries mocked with MSW v2 or local fixtures; no unmanaged live I/O in CI
- [ ] AI/LLM tests use structural/property assertions with VCR cassettes for CI determinism
- [ ] inter-service API changes verified with Pact contract checks
- [ ] `test-report.json` emitted and validated against schema

## Output Contracts

When executing or updating automated tests for behavior verification, emit:

- **`contracts/schemas/test-report.json`** — Documents test suite configurations, pass/fail execution results, mutation scores, coverage metrics, and identified test failures. Set `produced_by_role` to the executing role.

Skip emission for rapid local test iterations during interactive development.

## Failure Modes

- **Tautological / co-leaked tests**: agent writes implementation and tests together, encoding hallucinations into assertions. Mitigation: mandate independent test authoring and verify Red failure before green implementation.
- **Coverage theater without mutation testing**: 100% line coverage achieved with hollow assertions. Mitigation: enforce mutation score ≥75–80% on critical packages.
- **Live external network calls in CI**: tests hit live third-party APIs. Mitigation: enforce Level 0 airgap (`--network=none`) and MSW v2 stubs in CI.
- **Brittle E2E tests for unit logic**: slow UI tests written for internal domain calculations. Mitigation: push assertions down to unit/integration levels per Testing Trophy.
- **Flaky sleep-based waits**: tests rely on arbitrary timing. Mitigation: replace sleeps with explicit polling and event synchronization.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-check test assertions against source spec to prevent locking in unintentional drift or malicious scope changes.
- **ASI04 Supply Chain**: validate test fixtures, VCR cassettes, and mocking libraries against project manifests; reject untrusted test packages.
- **ASI05 RCE Guard**: test suites must run inside an isolated sandbox per `core/policies/execution-sandbox.md` without root privileges.
- **ASI07 Inter-Agent Communication**: emit structured `test-report.json` for CI and reviewer verification.
- **ASI09 Human-Agent Trust Exploitation**: surface skipped tests, surviving mutants, and mock fidelity limitations transparently.

## Related Skills

- **commit-code**: Prepare test changes for delivery
- **review-service**: Check whether coverage is sufficient for release risk
- **troubleshoot-service**: Debug failing or flaky tests
- **review-code**: Review whether tests match the change risk
- **navigate-service**: Understand the target flow before adding tests
