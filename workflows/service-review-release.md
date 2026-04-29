---
description: Complete workflow for reviewing service readiness and preparing a release
---

## Service Review & Release Workflow

Use this workflow before major releases, risky refactors, or periodic health checks on an important service.

### When To Use

- before a significant release
- before promoting a service to a higher-risk environment
- after large architectural or dependency changes
- during periodic readiness reviews

### Prerequisites

- the service or component to review is known
- access to the repo and relevant deployment sources of truth is available
- repo-local standards and release rules have been identified

### Workflow Steps

#### 1. Prepare The Review

Role: **Technical Lead**, **Reviewer**

Sync the latest local view of:

- the target service repo
- any directly related shared libraries
- deployment or release configuration repos, if they exist

Read the repo-local standards, release notes format, and review checklist if present.

#### 2. Understand The Service

Role: **Technical Lead**, **Technical Architect**

Use skill: `navigate-service`

Collect:

- high-level structure
- key dependencies
- public contracts
- data stores and migrations
- operational ownership boundaries

#### 3. Run A Full Review

Role: **Reviewer**, **Technical Lead**

Use skill: `review-service`

Focus on:

- correctness and data safety
- public contract compatibility
- dependency and configuration alignment
- observability, reliability, and rollback readiness
- test quality and release confidence

#### 4. Check Cross-Service Impact

Role: **Technical Architect**, **Security Engineer**

Review:

- consumers of the service's public APIs or events
- shared library version drift
- config or environment changes needed by adjacent systems
- migration or rollout ordering constraints

#### 5. Fix Or Track Findings

Role: **Backend Developer**, **Frontend Developer**

Use skill: `review-code`

For each important issue:

- decide whether it must block release
- implement the fix if it belongs in scope
- otherwise document the risk and owner explicitly

#### 6. Re-Run Quality Gates

Role: **QA Engineer**, **Backend Developer**

Verify with the repo's normal commands:

- tests
- coverage checks if the repo tracks them
- lint or static analysis
- build
- generated code or schema checks, if applicable

Use skill: `write-tests` if confidence is too low for the release risk.

#### 7. Confirm Release Readiness

Role: **Technical Lead**, **Product Manager**

Check that:

- config sources match the code
- health checks or equivalent runtime probes exist
- resource, capacity, or scaling assumptions are still valid
- rollback strategy is clear
- user-facing docs or release notes are updated if required

#### 8. Prepare The Release

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Before release:

- remove accidental local-only artifacts
- confirm generated files are intentional
- confirm versioning follows the repo's local rules
- capture a short release summary and known risks

Do not create a commit until the user or local process explicitly allows that commit action.
Do not push, create a tag, or publish a release entry until the user or local process explicitly allows that specific action.

#### 9. Verify After Release

Role: **DevOps Engineer**, **SRE**

After the release is shipped:

- confirm the intended revision is running
- verify health and smoke-test critical flows
- monitor for regressions
- capture any follow-up work immediately

### Review Output Template

```markdown
## Service Review: <service>

Date: YYYY-MM-DD
Reviewer: <name>
Status: Ready / Needs Work / Not Ready

### Issue Summary
- Blocking: <count>
- Important: <count>
- Follow-Up: <count>

### Blocking Issues
1. file:line - description

### High-Risk Issues
1. file:line - description

### Completed Actions
1. description

### Release Confidence
- tests: pass/fail
- build: pass/fail
- contracts: compatible/not compatible
- rollback plan: ready/not ready

### Follow-Up
1. description
```

### Checklist

- [ ] synced relevant source repos
- [ ] reviewed repo-local standards
- [ ] mapped service structure and dependencies
- [ ] listed Blocking, Important, and Follow-Up findings
- [ ] checked cross-service impact
- [ ] fixed or tracked blocking issues
- [ ] re-ran tests, build, and static checks
- [ ] confirmed rollout and rollback readiness
- [ ] updated user-visible docs if required
- [ ] verified the release after shipping

### Related Workflows

- [Build & Deploy](build-deploy.md)
- [Add New Feature](add-new-feature.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **review-service**: Run a full service readiness review
- **navigate-service**: Map the service before judging readiness
- **review-code**: Review and fix concrete implementation issues
- **write-tests**: Add coverage when release confidence is too low
- **commit-code**: Prepare approved release changes for delivery
