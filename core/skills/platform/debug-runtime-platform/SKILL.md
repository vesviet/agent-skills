---
name: debug-runtime-platform
description: Investigate deployment, environment, runtime, and rollout issues that are not purely application-code bugs. Use when the service behaves differently across environments or when deployment health is unclear.
---

# Debug Runtime Platform

Use this skill when the application code may be fine, but the running environment, rollout, or platform behavior is not.

## When to Use

- a service behaves differently across staging and production
- deployment health is unclear after a rollout
- the failure looks like config/secret/network, not app logic
- you need to compare desired state (git) with running state (cluster)
- a rollback or reconcile is required before escalating to app debugging

## Example (compare desired vs running on Kubernetes)

```bash
kubectl rollout status deploy/checkout
kubectl get deploy checkout -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl describe pod -l app=checkout | grep -E "Image:|Env:|Warning"
kubectl logs --previous deploy/checkout   # crash-loop before last restart
helm diff upgrade checkout ./charts/checkout   # detect git vs live drift
```

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
\n### 2026: Runtime Platform Debugging Additions

- **Kubernetes debugging toolkit:** Use `kubectl describe pod` for events, `kubectl logs --previous` for crash-loop containers, `kubectl exec -it` for interactive diagnosis, and `kubectl top pods --containers` for per-container CPU/memory without external tools.
- **Helm drift detection:** Use `helm diff upgrade` (with the helm-diff plugin) to preview changes before applying. Use `helm status` to verify the deployed revision, `helm history` to see rollback targets, and compare `helm get values` against the values file in git to detect config drift.
- **AI-assisted log analysis:** Pipe logs to LLM-powered analysis tools (such as Datadog Bits AI, Elastic AI Assistant, or Grafana Sift) to surface anomaly patterns. Treat AI-generated diagnosis as a starting hypothesis requiring human validation before any remediation.
- **CF-specific patterns:** For Cloudflare Workers, use `wrangler tail --format json` piped to `jq` tool for structured log filtering. Use `wrangler deployments list` to identify the exact deployment revision in production.\n