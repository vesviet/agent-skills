---
description: Emergency workflow for hotfixing production issues with minimal blast radius
---

## Hotfix Production Workflow

Use this workflow only for true production emergencies where delaying the fix is riskier than taking the shortest safe path to recovery.

### When To Use

- production is unavailable or severely degraded
- a critical security issue needs immediate mitigation
- there is active data corruption or a strong risk of data loss
- the incident has meaningful customer impact

### Prerequisites

- the incident is real and scoped enough to act on
- stakeholders or on-call owners are aware
- the minimal safe fix or rollback path is understood

### Workflow Steps

#### 1. Confirm Severity

Ask:

- is production impact active right now?
- is this a customer-visible outage or severe degradation?
- can the issue be mitigated by rollback or configuration first?

If the answer is no, use the normal delivery workflow instead.

#### 2. Contain The Blast Radius

Choose the least risky mitigation available first:

- rollback to the last known good release
- disable the failing path with config or a feature flag
- isolate or scale down only the affected workload
- route traffic away from the failing dependency when the platform allows it

Use the repo's approved production control path.

#### 3. Identify The Smallest Valid Fix

Use skill: `troubleshoot-service`

Rules:

- fix only the incident, not adjacent cleanup
- avoid opportunistic refactors
- prefer a reversible change
- keep the delta as small as possible

#### 4. Verify The Fix Quickly

Before shipping:

- run the narrowest useful test set first
- build the changed component
- exercise the failing path locally or in a lower environment if time allows
- confirm the fix does not obviously expand blast radius

Use skill: `review-code`

#### 5. Ship Through The Normal Emergency Path

Use skill: `commit-code`

Deliver using the repo's approved emergency release path:

- hotfix branch
- release branch
- rollback deployment
- emergency config push

Do not create a commit until the user or local release process explicitly allows that commit action.
Do not push, create a tag, or publish a release until the user or local release process explicitly allows that specific action.

#### 6. Monitor Recovery

After deployment:

- watch service health and key alerts
- verify the affected path behaves correctly
- compare error rate and latency against the incident window
- keep monitoring until the system is stable

#### 7. Close The Incident Properly

After stabilization:

- merge or reconcile the hotfix back into the main development line
- update changelog or release notes if the repo expects them
- capture an incident summary and preventive follow-up

### Post-Incident Follow-Up

Record:

- root cause
- mitigation used
- final fix
- missing tests, monitoring, or process gaps

Schedule deeper cleanup separately from the hotfix itself.

### Related Workflows

- [Troubleshooting](troubleshooting.md)
- [Service Review & Release](service-review-release.md)
- [Build & Deploy](build-deploy.md)

### Related Skills

- troubleshoot-service
- review-code
- commit-code
- meeting-review
