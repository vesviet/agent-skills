---
description: Generic workflow for building, validating, releasing, and verifying a change
---

## Build & Deploy Workflow

Use this workflow when a change is ready to move from local verification into a shared environment.

### When To Use

- after a feature or bug fix is complete
- after code review approval
- before handing a change to QA or release owners

### Prerequisites

- local implementation is complete
- verification commands pass locally
- release risk is understood

### Critical Rules

- prefer the repo's official CI/CD path over ad hoc local release steps
- do not edit generated release metadata by hand unless the repo explicitly expects that
- do not create a commit until the user or local process explicitly allows that commit action
- do not push, create a tag, or publish a release until the user or local process explicitly allows that specific action

### Workflow Steps

#### 1. Run Pre-Release Checks

Role: **Backend Developer**, **Frontend Developer**

From the target repo, run the normal quality gates:

- tests
- lint or static analysis
- build
- contract generation if the repo uses it

Also check:

- no accidental debug code
- no transient files staged for release
- no local-only config or credentials leaked into the change

#### 2. Review Release Impact

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Confirm:

- public contracts remain compatible unless the release is intentionally breaking
- schema or config changes are accounted for
- release notes or changelog entries are updated if the repo expects them
- dependent services or clients have been considered

#### 3. Prepare The Release Artifact

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Depending on the repo, this may mean:

- pushing a branch
- opening a change request
- creating a version tag
- updating a release branch
- handing the change to an automated promotion pipeline

Follow the repo-local mechanism instead of assuming a specific Git provider or deployment repo.
Treat each remote or release-facing action as separately gated approval.

#### 4. Trigger Delivery

Role: **DevOps Engineer**

Use the repository's normal release path:

- CI pipeline
- deployment manifest update
- package publish
- release promotion job

Capture the release reference that matters locally, such as:

- commit SHA
- build number
- artifact version
- deployment revision

#### 5. Verify Rollout

Role: **DevOps Engineer**, **SRE**

After delivery starts:

- confirm the rollout reached the intended environment
- inspect logs and health checks
- verify critical dependencies are reachable
- run a focused smoke test on the changed path

Prefer repo-local dashboards, manifests, or service discovery entries over guessing direct URLs.

#### 6. Monitor And Decide

Role: **SRE**

For the first few minutes after rollout:

- watch error rates
- watch latency or resource spikes
- confirm no alerts or regressions appear

If problems appear:

- pause further promotion
- compare the current revision with the last known good one
- follow the repo's rollback or recovery procedure

#### 7. Record Outcome

Role: **Technical Lead**, **Technical Writer**

Capture:

- what was released
- where it was released
- how it was verified
- any follow-up work or residual risk

### Rollback Guidance

If rollback is needed:

- use the repo's standard rollback path first
- avoid manual edits that bypass the normal source of truth
- verify recovery using the same smoke checks as the forward deploy

### Checklist

- [ ] pre-release checks completed
- [ ] release impact reviewed
- [ ] release artifact prepared through the repo-local path
- [ ] delivery triggered with explicit approval when required
- [ ] rollout verified in the target environment
- [ ] monitoring reviewed for regressions
- [ ] outcome and residual risk recorded

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)
- [Troubleshooting](troubleshooting.md)
- [Hotfix Production](hotfix-production.md)

### Related Skills

- **review-code**: Review release-impacting implementation changes
- **commit-code**: Prepare approved changes for delivery
- **troubleshoot-service**: Investigate failures during validation or rollout
- **review-service**: Confirm broad release readiness before shipping
