---
description: QA validation workflow from implemented feature or fix through test coverage audit, risk-based test planning, execution, and release confidence verdict
---

## QA Validation Workflow

Use this workflow after a feature or fix has been implemented and is ready for quality validation before merge or release. QA Validation goes beyond running tests — it audits coverage gaps, derives a risk-based test plan, validates observable behavior (including side effects), and produces an explicit release confidence verdict.

### When To Use

- a feature implementation is complete and needs QA sign-off before merge
- a bug fix must be validated and regression-checked before shipping
- a release candidate needs a full validation pass before promotion
- test coverage for a changed area is unknown or suspected to be insufficient
- an AI/LLM behavior change needs non-deterministic validation

### Prerequisites

- the implementation is complete in a testable branch or environment
- acceptance criteria or expected behavior is documented (from requirements, brief, or ticket)
- a lower environment (staging, test, dev) is available to test against
- the test suite runs and can be executed locally or in CI

### Workflow Steps

#### 1. Understand What Changed And Why

Role: **QA Engineer**

Before writing any test plan:

- read the acceptance criteria or feature description
- identify the changed files, modules, services, and APIs
- understand what business behavior the change is supposed to produce
- identify what was deliberately left out of scope
- note any known edge cases, performance concerns, or backward compatibility risks

Use skill: `navigate-service` if the change scope is not fully visible.

#### 2. Audit Existing Test Coverage

Role: **QA Engineer**, **Backend Developer**

Assess what coverage already exists for the changed area:

- what unit tests cover the changed logic?
- what integration tests cover the changed API or service interaction?
- what contract tests exist for the changed public interface?
- are there end-to-end tests for the affected user flow?
- are there regression tests for previously reported bugs in this area?

Use skill: `write-tests` to identify and fill coverage gaps.

Classify coverage gaps:

- **Critical gap**: no test covers a high-risk behavior or failure path
- **Important gap**: a test exists but does not cover a significant edge case
- **Follow-Up gap**: minor coverage improvement that can be deferred

#### 3. Derive A Risk-Based Test Plan

Role: **QA Engineer**

Prioritize testing effort by risk, not by code size:

- **Happy path**: core success scenario — must pass before any other tests
- **Validation and boundary failures**: invalid inputs, edge values, rate limits, empty states
- **Side effects**: database writes, cache invalidation, events published, downstream calls
- **Distributed system concerns**: retries, idempotency, eventual consistency, duplicate delivery, timeouts
- **Backward compatibility**: does the change break any existing consumer of the changed interface?
- **Security boundary**: does the change affect auth, authz, or input validation?
- **Accessibility**: if UI is affected — does it meet WCAG 2.2 compliance? (use `accessibility-review` skill)

For AI/LLM behavior changes, add:

- **Property-based assertions**: validate output properties (tone, safety, structure, relevance) — not exact strings
- **Golden dataset regression**: run against the version-controlled golden dataset and compare pass rate
- **Trajectory evaluation**: for multi-step agents, validate tool-call sequence and decision logic

Document the test plan explicitly: what scenarios, at what layer, in what environment.

#### 4. Prepare The Test Environment

Role: **QA Engineer**, **Backend Developer**

Confirm before running tests:

- the correct branch and revision is deployed to the target environment
- test data is seeded or available (use representative data — never production PII)
- feature flags match the expected configuration for the test
- migrations have run and the schema is at the expected state
- external dependencies (mocks, stubs, or real integrations) are reachable

#### 5. Execute The Test Plan

Role: **QA Engineer**

Use skill: `write-tests`

Run in this order:

1. **Automated suite first**: run existing unit, integration, and contract tests — do not proceed if pre-existing tests fail
2. **New tests for coverage gaps**: run newly written tests for the critical and important gaps
3. **Manual exploratory charter**: for high-risk paths and UX flows, run a structured exploratory session — not ad hoc clicking
4. **Side effect verification**: confirm non-response side effects (DB writes, event emissions, cache state) are correct
5. **Regression pass**: run the regression checklist for areas adjacent to the change

For each test failure:

- record the exact reproduction steps
- classify as: regression (broke previously working behavior), new bug (unintended behavior in new code), or expected failure (known limitation)
- do not suppress failures — every failure is a signal

#### 6. Validate AI / LLM Behavior (If Applicable)

Role: **QA Engineer**

When the change involves LLM pipelines, AI agents, or AI-generated output:

- run property-based validation — check output properties (tone, factual grounding, safety, structure), not exact string matches
- run the golden dataset: compare the model or prompt change against the version-controlled baseline
- calculate pass rate against the golden dataset — if it regresses below the threshold, block the change
- evaluate multi-step agent trajectories: tool-call sequence, decision logic, error recovery
- validate that non-deterministic outputs stay within acceptable behavioral bounds

Document the LLM-as-Judge methodology used and calibration against human annotations if applicable.

#### 7. Document Findings And Evidence

Role: **QA Engineer**

For each defect found:

- title and severity (Critical, High, Medium, Low)
- reproduction steps (minimal and reliable)
- expected vs actual behavior
- evidence (screenshot, log, request/response, DB state)
- suspected scope: is this limited to the changed code, or does it suggest a deeper issue?

Distinguish:

- **Blocking defect**: must be fixed before merge or release
- **Important defect**: should be fixed — can be released with documented risk if stakeholder acknowledges
- **Follow-Up defect**: can be tracked and fixed post-release

#### 8. Produce Release Confidence Verdict

Role: **QA Engineer**

Use skill: `write-tests`

Emit `test-report.json` with:

- test plan summary (what was tested, what was not, and why)
- pass/fail counts by layer (unit, integration, e2e, exploratory)
- blocking and important defects with status
- coverage gaps addressed and remaining
- AI/LLM validation results if applicable
- explicit release confidence verdict:

| Verdict | Meaning |
|---------|---------|
| **Confident to release** | All blocking defects resolved, important defects acknowledged |
| **Conditional release** | Important defects present but stakeholder accepts documented risk |
| **Block release** | One or more blocking defects unresolved — do not ship |

The verdict must be explicit — "no obvious issues" is not a release confidence verdict.

### Checklist

- [ ] acceptance criteria and change scope understood
- [ ] existing test coverage audited — gaps classified (Critical/Important/Follow-Up)
- [ ] risk-based test plan derived — happy path, failures, side effects, distributed concerns
- [ ] test environment confirmed — correct revision, data, flags, migrations
- [ ] automated suite passes
- [ ] new tests for critical coverage gaps written and pass
- [ ] exploratory testing charter executed for high-risk flows
- [ ] side effect verification completed (DB, events, cache, downstream)
- [ ] AI/LLM property-based validation and golden dataset run (if applicable)
- [ ] defect findings documented with severity and reproduction steps
- [ ] test-report.json emitted with release confidence verdict

### Related Workflows

- [add-new-feature](add-new-feature.md)
- [tech-repo-review](tech-repo-review.md)
- [service-review-release](service-review-release.md)
- [build-deploy](build-deploy.md)

### Related Skills

- **write-tests**: Design and implement tests for coverage gaps
- **navigate-service**: Understand the changed code before deriving the test plan
- **review-code**: Review test code quality and coverage logic
- **accessibility-review**: Validate WCAG 2.2 compliance when UI is affected
- **agent-quality-gate**: Validate artifacts in agentic pipelines
