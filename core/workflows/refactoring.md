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

#### 5. Execute Incrementally

Role: **Backend Developer**, **Frontend Developer**

After each meaningful step:

- rerun the most relevant tests
- rebuild the affected package or service
- compare behavior against the baseline

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

Do not create a commit until the user or local process explicitly allows that commit action.
Do not push, tag, or publish until the user or local process explicitly allows that specific action.

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
