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

Role: **SRE**, **Technical Lead**

Ask:

- is production impact active right now?
- is this a customer-visible outage or severe degradation?
- can the issue be mitigated by rollback or configuration first?

If the answer is no, use the normal delivery workflow instead.

#### 2. Contain The Blast Radius

Role: **SRE**, **DevOps Engineer**

Choose the least risky mitigation available first:

- **disable via OpenFeature flag first** (takes seconds, no deployment) — if the failing path is behind a feature flag, disable it immediately before assessing rollback vs hotfix
- rollback to the last known good release (in Argo CD: `argo rollouts abort` for progressive delivery; in GitOps: revert the manifest commit)
- disable the failing path with config or a feature flag
- isolate or scale down only the affected workload
- route traffic away from the failing dependency when the platform allows it

Record the **DORA MTTR clock start** at the moment production impact is confirmed — this is used for post-incident DORA reporting.

Use the repo's approved production control path.

#### 3. Identify The Smallest Valid Fix

Role: **Backend Developer**, **Frontend Developer**

Use skill: `troubleshoot-service`

**Distributed-trace-first**: retrieve the trace for the failing request before reading raw logs. The span tree immediately shows which service and which layer failed, cutting diagnosis time significantly.

Rules:

- fix only the incident, not adjacent cleanup
- avoid opportunistic refactors
- prefer a reversible change
- keep the delta as small as possible

#### 4. Verify The Fix Quickly

Role: **Backend Developer**, **Reviewer**

Before shipping:

- run the narrowest useful test set first
- build the changed component
- exercise the failing path locally or in a lower environment if time allows
- confirm the fix does not obviously expand blast radius

Use skill: `review-code`

#### 5. Ship Through The Normal Emergency Path

Role: **Backend Developer**, **DevOps Engineer**

Use skill: `commit-code`

Deliver using the repo's approved emergency release path:

- hotfix branch
- release branch
- rollback deployment
- emergency config push

Do not create a commit until the user explicitly confirms that commit action.
Do not push, create a tag, or publish a release until the user explicitly confirms that specific action.

#### 6. Monitor Recovery

Role: **SRE**, **DevOps Engineer**

After deployment:

- watch service health and key alerts
- verify the affected path behaves correctly
- compare error rate and latency against the incident window
- keep monitoring until the system is stable

#### 7. Close The Incident Properly

Role: **Technical Lead**, **Technical Writer**

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

### Checklist

- [ ] severity and production impact confirmed
- [ ] blast radius contained with the least risky mitigation
- [ ] smallest valid fix identified
- [ ] narrow verification completed
- [ ] emergency delivery path followed with explicit approvals
- [ ] recovery monitored until stable
- [ ] incident summary and preventive follow-up captured

### Related Workflows

- [Troubleshooting](troubleshooting.md)
- [Service Review & Release](service-review-release.md)
- [Build & Deploy](build-deploy.md)

### Related Skills

- **troubleshoot-service**: Isolate the incident cause quickly
- **review-code**: Review risky hotfix changes before shipping
- **commit-code**: Prepare approved hotfix changes for delivery
- **meeting-review**: Escalate cross-role incident decisions

### Failure Modes

- **Hotfix without rollback verified**: an urgent fix ships but the previous deployment is not rollbackable. **Mitigation:** verify the rollback path before the hotfix; reject the deploy when the path is not confirmed.
- **Hotfix bypasses review**: an urgent fix is merged without reviewer sign-off. **Mitigation:** pre-authorize a small responder set; require at least one reviewer outside the responder set to sign off; surface the bypass in the postmortem.
- **Permanent feature flag**: a hotfix flag ships without a `cleanup_target_date`. **Mitigation:** every flag must carry an ISO 8601 cleanup date; CI must reject the hotfix if any flag is permanent.
- **Customer-impact metric not captured**: a hotfix closes the incident without recording the customer impact. **Mitigation:** capture DORA Change Failure Rate, MTTR, and customer impact in the incident report before the incident is closed.
- **Postmortem skipped**: the hotfix is shipped but the root cause is never recorded. **Mitigation:** require a postmortem in `contracts/schemas/incident-report.json` within 72 hours of the hotfix.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/incident-report.json`** — Required fields: symptom, suspected layer, checks performed, root cause, fix applied, verification result, and follow-up items.
- **`contracts/schemas/deployment-plan.json`** — For the hotfix deploy; capture infrastructure changes, config updates, and validation runs.
- **`contracts/schemas/implementation-result.json`** — For the hotfix code change; capture change summary, files touched, and the validation run.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: hotfix credentials must be scoped to the responder set; reject deploys that request broader scopes than the role's `action-boundaries.yaml` profile allows.
- **ASI05 RCE Guard**: never construct hotfix scripts or rollback commands from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the hotfix is consumed by incident response and release roles; emit structured `incident-report.json` and `deployment-plan.json` so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the hotfix as "resolved" without end-to-end verification and customer impact evidence; surface the residual risk honestly.
