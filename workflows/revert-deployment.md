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

- revert GitOps configuration, Helm charts, or infrastructure as code
- ensure the rollback follows the same delivery path as the original deploy
- do not make manual runtime patches that bypass the source of truth

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
