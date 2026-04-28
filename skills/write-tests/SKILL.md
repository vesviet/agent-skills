---
name: write-tests
description: Add or update tests by following repo-local test conventions, choosing the right test scope, isolating dependencies, and validating risky paths before delivery
---

# Write Tests Skill

Use this skill when adding, updating, or strengthening tests for a code change.

## When to Use

- new business logic needs coverage
- a bug fix needs regression protection
- a refactor needs a safety net
- an integration boundary needs validation
- missing edge-case coverage is increasing release risk

## Core Rules

- follow repo-local testing conventions before introducing a new style
- test behavior and risk, not just line coverage
- prefer the smallest test scope that proves the requirement
- isolate dependencies when a unit test should not rely on external systems
- do not commit test changes unless the user or repo-local process explicitly allows that commit action
- do not push test changes unless the user or repo-local process explicitly allows that push action

## First Questions To Answer

1. What behavior or risk needs protection?
2. Is this best covered by a unit, integration, contract, or end-to-end test?
3. Which dependencies should be real, stubbed, mocked, or faked?
4. What edge cases are most likely to break?
5. What existing test patterns in the repo should be reused?

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

## Suggested Process

### Step 1: Inspect Existing Test Patterns

Before writing new tests:

- find nearby tests in the same area
- match local naming and fixture patterns
- reuse local helpers, builders, or fixtures when they are clear and stable

### Step 2: Identify The Required Cases

At minimum, consider:

- happy path
- validation failures
- dependency failures
- edge cases around empty, nil, zero, or missing values
- backward compatibility or migration-sensitive cases when relevant

### Step 3: Choose A Dependency Strategy

Use the lightest useful option:

- real dependency for narrow integration coverage
- fake or stub for simple, predictable behavior
- mock when interaction shape or call expectations matter

Do not assume a specific mocking framework. Follow the repo's local toolchain if it has one.

### Step 4: Write Deterministic Tests

Keep tests stable:

- avoid hidden time dependencies
- avoid random data unless it is seeded and controlled
- avoid environment coupling unless the test is explicitly integration scoped
- ensure cleanup is handled for files, processes, and shared state

### Step 5: Verify The Right Signals

Assert the behavior that matters:

- returned value or state transition
- visible side effect
- persisted change
- emitted event or outbound call
- error type or message shape when that is contractually important

### Step 6: Run The Appropriate Validation

Run the local commands for the test scope you changed:

- targeted package or module tests first
- broader test suite if the risk is wider
- coverage or benchmark checks only when the repo actually uses them for the change type

### Step 7: Capture Remaining Gaps

If some risk is still untested, note it explicitly:

- difficult-to-reproduce integration path
- missing fixture support
- shared environment dependency
- follow-up test needed after a larger refactor

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

## What To Capture In Your Output

When reporting test work, include:

- test scope chosen
- behaviors covered
- important edge cases added
- commands run
- remaining validation gaps

## Checklist

- [ ] existing local test patterns reviewed
- [ ] right test scope chosen
- [ ] happy path covered
- [ ] error or edge cases covered
- [ ] dependency strategy chosen intentionally
- [ ] tests run successfully
- [ ] remaining gaps documented if any

## Quick Reference

Use this when adding tests quickly:

- inspect nearby tests
- identify risky behaviors
- choose unit or integration scope
- isolate dependencies appropriately
- add happy path and failure path coverage
- run targeted tests

## Related Skills

- **commit-code**: Prepare test changes for delivery
- **review-service**: Check whether coverage is sufficient for release risk
- **troubleshoot-service**: Debug failing or flaky tests
- **review-code**: Review whether tests match the change risk
- **navigate-service**: Understand the target flow before adding tests
