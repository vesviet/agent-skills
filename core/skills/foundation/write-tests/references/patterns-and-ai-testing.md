# Write Tests — Reference

Deep material extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file when designing a new test suite, when adding AI/LLM test
patterns, or when reviewing the test pyramid for a service.

## Choose The Right Test Scope

### Unit Tests

Best for:

- business rules
- validation logic
- pure transformations
- branching behavior
- small state transitions

### Integration Tests

Best for:

- repository or query behavior
- serialization and contract boundaries
- framework wiring
- code that depends on a real database, queue, filesystem, or HTTP layer

### Contract Or API Tests

Best for:

- request and response compatibility
- versioned payloads
- consumer/provider assumptions

### End-To-End Tests

Best for:

- critical user journeys
- cross-service flows
- release confidence on high-risk paths

Use them sparingly because they are usually slower and more brittle.

## Good Testing Patterns

- table-driven or parameterized tests when many similar cases exist
- focused fixtures with only the fields the scenario needs
- builders or factories when setup is repetitive
- regression tests named after the behavior or bug being protected

## Common Testing Mistakes

1. Testing implementation details instead of behavior.
2. Over-mocking simple code paths that would be clearer with a fake or real helper.
3. Adding large, brittle end-to-end tests for logic that belongs in unit tests.
4. Relying on timing sleeps instead of explicit synchronization.
5. Chasing coverage numbers while missing the risky path.

## AI/LLM Test Patterns

When adding tests for AI/LLM features:

- Use structural assertion over content assertion — test JSON shape, field types, word count bounds, not exact string matches (model output changes between versions).
- Use property-based assertions ("response is in Vietnamese", "no PII present") checked by classifiers, not equality.
- Stub LLM API calls in CI with `vcr`-style fixtures — never call live LLM APIs in CI.
- Capture a golden-set baseline before any model update; flag outputs that degrade on the golden set as regressions.
- Test HITL trigger paths and hallucination boundary inputs (adversarial false-premise prompts) explicitly — do not leave fallback-to-human paths untested.
- For critical business libraries, enforce mutation score ≥ 75–80% via Stryker — raw coverage percentage is insufficient without mutation validation.
- For inter-service API compatibility, run Pact `can-i-deploy` checks in CI before merging service PRs.

## Network Boundary Mocking

- Use MSW v2 for network boundary mocking — do not mock `global.fetch` or internal Axios instances directly.
- For unit tests that should not rely on external systems, isolate dependencies with fakes/stubs; use real dependencies only for narrow integration coverage.
