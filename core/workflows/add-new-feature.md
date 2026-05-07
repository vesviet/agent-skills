---
description: Complete workflow for adding a new feature in a reusable service-oriented repository
---

## Add New Feature Workflow

This workflow guides a feature from requirements through rollout verification without assuming a specific framework, deployment platform, or repository layout.

### Prerequisites

- feature requirements are clear enough to implement
- target service or component is identified
- repo-local standards and templates have been located

### Workflow Steps

#### 1. Understand The Change

Role: **Product Manager**, **Business Analyst**, **Technical Lead**

Answer these first:

- What user or business problem is being solved?
- What public contract changes, if any, are required?
- What data model changes, if any, are required?
- What downstream services, jobs, or consumers are affected?
- What rollout and rollback risks exist?

Use skill: `navigate-service`

#### 2. Check Existing Patterns

Role: **Technical Lead**, **Technical Architect**

Before writing code:

- inspect similar features already present in the repo
- reuse existing request, validation, persistence, and test patterns
- read repo-local standards, ADRs, and service docs if available
- note any existing migration, release, or compatibility rules

#### 3. Plan The Implementation

Role: **Technical Lead**

Break the work into the minimum set of changes needed:

- contract changes
- business logic
- persistence or schema updates
- integrations with other services or shared libraries
- observability and documentation

If the feature changes persisted data, use skill: `create-migration`

#### 4. Implement The Change

Role: **Backend Developer**, **Frontend Developer**

Follow the local architecture instead of inventing a new one.

- update contracts only if needed
- keep validation near the boundary
- keep business rules in the repo's expected layer
- update persistence code in the local pattern
- reuse shared code before creating new helpers
- avoid hidden breaking changes in public interfaces

If the repo uses generated code, regenerate it with the local command after editing source definitions.

#### 5. Test The Change

Role: **Backend Developer**, **Frontend Developer**, **QA Engineer**

Use skill: `write-tests`

Cover at least:

- the happy path
- boundary and validation failures
- backward compatibility concerns
- migration or data edge cases when schema changes are involved
- the most important integration touchpoints

Run the repo's normal verification commands for:

- tests
- lint or static analysis
- build

#### 6. Review The Change

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Self-review checklist:

- architecture boundaries are still respected
- inputs are validated
- errors have useful context
- no secrets or repo-local assumptions were introduced
- tests cover the riskier paths
- docs or release notes are updated when needed

#### 7. Prepare Delivery

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Before committing or pushing:

- remove transient build artifacts if the repo produces them
- verify generated files are intentionally updated
- confirm migration ordering and rollback safety
- confirm contract changes are versioned appropriately
- follow the repo's release gate and approval requirements

Do not create a commit until the user or local policy explicitly allows that commit action.
Do not push, tag, or publish until the user or local policy explicitly allows that specific action.

#### 8. Verify Rollout

Role: **DevOps Engineer**, **SRE**

After the change is shipped:

- verify deployment or rollout status using the repo's source of truth
- check service health, logs, and critical signals
- run a focused smoke test for the feature
- confirm dependent systems still behave as expected

#### 9. Capture Follow-Up

Role: **Technical Lead**, **Technical Writer**

If the feature leaves known follow-up work:

- document deferred cleanup
- note temporary compatibility shims
- record rollout observations and any residual risk

### Common Failure Modes

#### Contract changed but consumers were not considered

- review dependent services and client code
- check compatibility expectations before release

#### Schema changed but migrations are unsafe

- verify ordering, backfill strategy, and rollback behavior
- avoid destructive data changes in a single risky step

#### Tests pass locally but rollout fails

- compare runtime config, env vars, and dependency availability
- check repo-local deployment manifests or release config

### Checklist

- [ ] change intent and affected contracts understood
- [ ] existing local patterns reviewed
- [ ] implementation plan scoped to the minimum useful change
- [ ] feature implemented in the local architecture
- [ ] tests and local verification completed
- [ ] change reviewed for correctness, security, and rollout risk
- [ ] delivery preparation followed explicit approval rules
- [ ] rollout verified after shipping
- [ ] follow-up work captured

### Related Workflows

- [Build & Deploy](build-deploy.md)
- [Service Review & Release](service-review-release.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **navigate-service**: Understand the target service or component
- **create-migration**: Add safe persistence changes when needed
- **write-tests**: Cover behavior and regression risk
- **review-code**: Review the implemented change
- **commit-code**: Prepare approved changes for delivery
