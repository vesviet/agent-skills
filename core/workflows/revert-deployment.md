---
description: Emergency workflow for safely rolling back a failed deployment, release, or database migration
---

## Revert Deployment Workflow

Use this workflow when a release causes severe degradation or outages and rolling back to the previous stable state is the fastest mitigation.

### When To Use

- a recent deployment caused service degradation or outage
- a database migration introduced data corruption risk
- a config change broke runtime behavior
- progressive delivery (Canary, Blue/Green) shows unacceptable error rates

### Prerequisites

- the failing deployment or release is identified
- stakeholders or on-call owners are aware
- the previous known good state is identifiable

### Workflow Steps

#### 1. Assess Impact

Role: **SRE**, **Technical Lead**

Confirm that the issue is caused by the recent deployment:

- check telemetry, alerts, and logs
- correlate the timeline with the deployment event
- determine scope of user impact
- decide whether rollback is safer than a forward fix

Use skill: `troubleshoot-service`

#### 2. Halt Rollout

Role: **DevOps Engineer**, **SRE**

Stop any progressive delivery if it is still ongoing:

- pause Canary or Blue/Green promotion
- prevent further replicas from receiving the new revision
- communicate the halt to relevant stakeholders

#### 3. Check Database State

Role: **Backend Developer**, **SRE**

Determine if the rollback requires a database migration revert:

- check if the new migration is backward compatible
- if yes, the app rollback can proceed independently
- if no, execute the down-migration safely before or after reverting the application code
- verify data integrity after any migration revert

Use skill: `database-maintenance`

#### 4. Revert Configuration And Code

Role: **DevOps Engineer**

Revert the deployment source-of-truth to the previous known good state:

- revert GitOps configuration, Helm charts, or infrastructure as code (in Argo CD: trigger a sync to the previous ApplicationSet revision; in Flux: revert the HelmRelease manifest in Git)
- ensure the rollback follows the same delivery path as the original deploy — never apply runtime patches that bypass the GitOps source of truth
- do not make manual runtime patches that bypass the source of truth

If the rollout used **Argo Rollouts** canary/blue-green with automated metric analysis: trigger an `argo rollouts abort` to immediately shift 100% of traffic back to the stable revision — this is faster and safer than manual manifest changes.

If the failing feature is behind an **OpenFeature** flag: disable the flag as an immediate mitigation before or alongside the deployment revert — this can stop user impact in seconds.

Do not create a commit until the user explicitly confirms that commit action.
Do not push, create a tag, or publish a release until the user explicitly confirms that specific action.

Use skill: `setup-deployment`

#### 5. Verify Stability

Role: **SRE**, **DevOps Engineer**

Monitor the system to ensure it has fully stabilized:

- check health endpoints and readiness probes
- watch error rates and latency against pre-incident baselines
- verify dependent services are reachable and healthy
- run a focused smoke test on the affected paths

Use skill: `debug-runtime-platform`

#### 6. Document The Rollback

Role: **Technical Lead**, **Technical Writer**

Capture the incident and rollback for the post-mortem:

- timeline of events
- rollback actions taken
- root cause (if known) or investigation status
- follow-up work and preventive measures

### Checklist

- [ ] impact assessed and recent deployment correlated
- [ ] rollout halted when applicable
- [ ] database state and migration safety checked
- [ ] deployment source of truth reverted
- [ ] system stability verified after rollback
- [ ] rollback actions and follow-up documented

### Related Workflows

- [Hotfix Production](hotfix-production.md)
- [Troubleshooting](troubleshooting.md)
- [Build & Deploy](build-deploy.md)

### Related Skills

- **troubleshoot-service**: Confirm the failing layer before rollback
- **debug-runtime-platform**: Verify runtime recovery after rollback
- **database-maintenance**: Handle data or migration rollback safely
- **setup-deployment**: Revert deployment source-of-truth configuration
- **commit-code**: Prepare approved rollback changes for delivery

### Failure Modes

- **Revert without a previous deployment**: a revert is requested but the previous artifact is missing. **Mitigation:** verify the previous deployment is rollbackable before issuing the revert; reject the revert when no prior artifact is available.
- **Revert cascades to dependent services**: a downstream service depends on the schema or contract of the new release. **Mitigation:** before reverting, identify downstream consumers in the dependency graph; route a coordinated revert through `contracts/schemas/coordination-plan.json` when more than one service is affected.
- **Database migration not reversible**: a forward migration ran but the data has already changed. **Mitigation:** document the partial-rollback path in the revert plan; require human sign-off when the revert is unsafe.
- **Cache stale after revert**: a CDN or browser cache still serves the new release. **Mitigation:** require a full purge of the affected route pattern; verify the cache miss with curl after revert.
- **Revert skipped because of feature flag**: a flag is intended to gate a release, but a separate code path bypasses it. **Mitigation:** verify the flag is checked in every code path that touches the gated feature; never trust the flag alone.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/deployment-plan.json`** — For the revert; capture the target revision, the rollback steps, the cache purge, and the validation run.
- **`contracts/schemas/incident-report.json`** — When the revert is triggered by an incident; capture the symptom, the failed artifact, the revert rationale, and the follow-up postmortem reference.
- **`contracts/schemas/coordination-plan.json`** — When the revert cascades to dependent services; route the coordinated revert through the coordinator.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: revert credentials must be scoped to the role that owns the deploy; reject reverts requested by a role that does not hold `run_deployment` in `action-boundaries.yaml`.
- **ASI05 RCE Guard**: never construct revert commands or cache-purge scripts from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the revert is consumed by SRE, release, and downstream roles; emit structured contracts so each role can validate the cascade.
- **ASI09 Human-Agent Trust Exploitation**: do not present the revert as "successful" without end-to-end verification on the previous revision; surface the actual `validation_run` evidence.
