---
name: debug-runtime-platform
description: Investigate deployment, environment, runtime, and rollout issues that are not purely application-code bugs. Use when the service behaves differently across environments or when deployment health is unclear.
---

# Debug Runtime Platform

Use this skill when the application code may be fine, but the running environment, rollout, or platform behavior is not.

## Core Rules

- compare desired state with running state before patching anything
- prefer low-risk inspection before invasive repair steps
- keep source-of-truth drift visible
- separate platform failure from application failure
- get explicit approval before risky production actions

## Suggested Process

### 1. Capture The Runtime Symptom

Collect:

- what environment is affected
- what health or rollout signal is failing
- whether the issue reproduces only after deploy
- what changed in code, config, or environment

### 2. Compare Desired And Running State

Check the repo's source of truth against what is actually live:

- revision or artifact version
- config values
- dependency endpoints
- environment-scoped settings
- health or readiness behavior

### 3. Isolate The Failure Layer

Decide whether the issue is mainly:

- rollout orchestration
- runtime config
- secret or credential wiring
- network or dependency reachability
- capacity or resource pressure
- application code surfaced by the platform

Use skill: `troubleshoot-service` if the evidence points back into application logic.

### 4. Repair The Smallest Safe Thing

Examples:

- reconcile source-of-truth config
- fix environment-specific wiring
- correct rollout metadata
- restore missing dependency access
- roll back to the last known good runtime state

### 5. Verify Recovery

Confirm:

- rollout completes
- health checks pass
- logs stabilize
- critical smoke checks succeed

## Checklist

- [ ] runtime symptom captured
- [ ] desired and running state compared
- [ ] failing layer isolated
- [ ] smallest safe repair applied
- [ ] rollout and health verified

## Related Skills

- **setup-deployment**: Fix or update the deployment source of truth
- **troubleshoot-service**: Investigate app-level failures behind runtime symptoms
- **review-service**: Check full release readiness after recovery
- **meeting-review**: Escalate cross-role runtime risk
- **commit-code**: Prepare source-of-truth fixes for delivery
