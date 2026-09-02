---
description: Workflow for structural improvements that preserve behavior
---

## Refactoring Workflow

Use this workflow when improving structure, readability, modularity, or maintainability without intentionally changing externally visible behavior.

### Prerequisites

- the current behavior is understood well enough to preserve
- baseline verification exists or can be added first
- the target area has a clear reason to change

### Workflow Steps

#### 1. Define The Goal

Role: **Technical Lead**, **Technical Architect**

State the narrow objective:

- split a large file or function
- isolate a dependency
- reduce duplication
- improve naming or boundaries
- prepare for a future feature safely

If the goal includes behavior change, use a feature workflow instead.

#### 2. Establish A Safety Net

Role: **Backend Developer**, **Frontend Developer**

Use skill: `write-tests`

Before moving code:

- add or strengthen tests around the current behavior
- identify critical edge cases
- record performance-sensitive paths if relevant

#### 3. Understand The Existing Structure

Role: **Technical Lead**, **Backend Developer**

Use skill: `navigate-service`

Map:

- current call flow
- dependency edges
- side effects
- public entry points

#### 4. Choose The Smallest Refactor Sequence

Role: **Technical Lead**

Prefer a series of safe, reviewable steps:

- rename first
- extract next
- move code after tests are stable
- delete dead code last

Avoid mixing structural cleanup with new business logic.

When AI coding assistants (Cursor Agent, GitHub Copilot Agent) are used for large renames or extractions: scope them to a single pass with an explicit instruction constraint file (`AGENTS.md` / `.cursorrules`) listing which files and layers are in scope. Always review the full diff before merging — AI refactors can silently introduce behavioral changes in edge paths.

#### 5. Execute Incrementally

Role: **Backend Developer**, **Frontend Developer**

After each meaningful step:

- rerun the most relevant tests
- rebuild the affected package or service
- compare behavior against the baseline

If the refactor touches **service API boundaries or event contracts**: run **Pact v4** or **Specmatic** contract tests to confirm no consumer-breaking changes were introduced — structural refactors often break wire format or field naming in ways that unit tests miss.

Use skill: `review-code` when the change alters boundaries or ownership between layers.

#### 6. Check Secondary Effects

Role: **Reviewer**, **SRE**

If the refactor touches hot paths, shared code, or contracts:

- verify performance did not regress
- verify logs, metrics, or error shapes still make sense
- verify downstream callers still compile and behave correctly

Use skill: `performance-profiling` if the path is latency-sensitive.

#### 7. Prepare Delivery

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Before committing:

- remove temporary scaffolding
- confirm no accidental behavior changes slipped in
- update docs when code organization changes matter to teammates

Do not create a commit until the user explicitly confirms that commit action.
Do not push, tag, or publish until the user explicitly confirms that specific action.

### Checklist

- [ ] goal limited to structural improvement
- [ ] safety-net tests added or confirmed
- [ ] current structure mapped
- [ ] refactor broken into safe steps
- [ ] tests and build rerun during execution
- [ ] performance checked if needed
- [ ] docs updated if needed

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)

### Related Skills

- **navigate-service**: Understand the current structure before refactoring
- **write-tests**: Establish behavior-preserving safety coverage
- **review-code**: Review boundary and ownership changes
- **performance-profiling**: Check performance-sensitive refactors
- **commit-code**: Prepare approved refactor changes for delivery

### Failure Modes

- **Behavior changed during refactor**: a refactor introduces a user-visible behavior change. **Mitigation:** the refactor must be behavior-preserving; the diff is verified against the existing test suite and acceptance criteria before the change is shipped.
- **Refactor expands scope**: a refactor pulls in unrelated changes (style fixes, dependency bumps). **Mitigation:** split into separate PRs; the refactor PR is rejected if it touches unrelated code.
- **Test coverage missing for the refactored path**: the refactor deletes or moves code without preserving the test coverage. **Mitigation:** the refactor PR must include a passing test for the new structure; reject the PR if a path is uncovered.
- **Performance regression undetected**: a refactor slows the hot path. **Mitigation:** run the benchmark before and after the refactor; reject the change if the regression exceeds the agreed budget.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/implementation-result.json`** — capture the behavior-preservation evidence, the test coverage delta, the benchmark before/after, and the files touched.
- **`contracts/schemas/code-review-finding.json`** (adapted for refactor) — when the refactor surfaces a structural concern; capture the smell, the proposed resolution, and the trade-off.

### Security Guardrails (OWASP ASI)

- **ASI05 RCE Guard**: never construct refactored code, scripts, or test fixtures from external or user-supplied content without strict schema validation; reject string-concatenated refactors.
- **ASI07 Inter-Agent Communication**: the refactor result is consumed by code review and release roles; emit a structured contract so each consumer can validate the behavior-preservation evidence.
- **ASI09 Human-Agent Trust Exploitation**: do not present a refactor as "safe" without the behavior-preservation evidence and the test coverage delta; surface the residual risk honestly.

