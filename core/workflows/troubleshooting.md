---
description: Workflow for diagnosing build, startup, runtime, and platform issues in a reusable way
---

## Troubleshooting Workflow

Use this workflow when a service, toolchain, or rollout behaves unexpectedly and you need a disciplined way to isolate the problem.

### Prerequisites

- the failing command, request, deployment, or user-visible behavior can be described
- access to relevant code, logs, or runtime evidence is available
- the team is willing to test one hypothesis at a time

### Quick Diagnostic Tree

```text
Issue?
|- Build or generation failure
|- Startup or config failure
|- Runtime correctness failure
|- Dependency or data failure
`- Platform or rollout failure
```

### Workflow Steps

#### 1. Capture The Symptom

Role: **SRE**, **Backend Developer**, **Frontend Developer**

Write down:

- the exact failing command or user-visible behavior
- the first observed error
- when the issue started
- what changed recently
- whether the issue reproduces consistently

**Distributed-trace-first**: before reading logs, retrieve the distributed trace for the failing request (Jaeger, Tempo, Zipkin, or OTel-native). The trace span tree reveals the exact failing layer and inter-service call timing without reading thousands of log lines. Only fall back to raw logs when no trace is available or the failure occurs before the trace is emitted.

For log analysis: AI-assisted log tools (Elastic AI Assistant, Splunk AI, Grafana Sift) can correlate high-volume telemetry and surface anomaly patterns in seconds. Treat AI-suggested root causes as **advisory** — validate with a concrete reproduction before applying a fix.

#### 2. Determine The Failure Stage

Role: **SRE**, **Backend Developer**

Classify the issue first:

- build or generation
- startup or dependency initialization
- runtime logic
- data or migration
- environment or platform

Use skill: `navigate-service` if the code path is not familiar yet.

For Kubernetes targets: use the diagnostic signals triad — `kubectl describe pod`, `kubectl events --namespace`, and `kubectl logs --previous` — before port-forwarding or exec-ing into containers. Check `/health/live` and `/health/ready` probes for pod state.

#### 3. Check The Simplest Explanations

Role: **DevOps Engineer**, **SRE**

Verify:

- the correct branch, revision, and config are in use
- required dependencies are reachable
- the needed env vars or secrets are present
- generated files or migrations are up to date
- the failing service is actually running the revision you expect

#### 4. Compare With The Last Known Good State

Role: **DevOps Engineer**, **Backend Developer**

Look at:

- recent commits
- recent config changes
- dependency version changes
- deployment or rollout changes
- migration history

This often narrows the search faster than reading large parts of the codebase.

#### 5. Isolate The Layer

Role: **Backend Developer**, **Frontend Developer**

Test the smallest meaningful slice:

- build one package or target
- run a focused test
- call one endpoint or one use case
- validate one query or one migration
- check one dependency at a time

Use skill: `troubleshoot-service`

#### 6. Form And Test A Hypothesis

Role: **Backend Developer**, **SRE**

For each likely cause:

- state the hypothesis clearly
- run one check that can confirm or reject it
- record what changed after the check

Avoid changing multiple things at once while investigating.

#### 7. Apply The Fix

Role: **Backend Developer**, **Frontend Developer**

When the cause is confirmed:

- make the smallest safe change
- rerun the failing scenario
- rerun nearby verification to catch regressions

Use skill: `review-code` if the fix touches risky code paths.

#### 8. Verify Recovery

Role: **SRE**, **DevOps Engineer**

Confirm:

- the original symptom is gone
- no new errors were introduced
- logs and health signals look normal
- dependent flows still work

#### 9. Capture Follow-Up

Role: **Technical Lead**, **Technical Writer**

If the incident exposed a gap, note:

- missing test coverage
- missing observability
- fragile config assumptions
- missing documentation or runbook steps

### Common Failure Areas

#### Build Or Generation

- stale generated files
- missing tools
- dependency version drift
- invalid imports or module references

#### Startup

- bad config values
- missing env vars or secrets
- dependency connectivity
- bootstrap order problems

#### Runtime

- invalid assumptions in business logic
- unhandled edge cases
- timeout or retry behavior
- data shape mismatches

#### Data

- migration ordering
- schema drift
- transaction boundaries
- unsafe rollout of destructive changes

#### Platform

- wrong revision deployed
- mismatched runtime config
- failed health checks
- dependency not available in the target environment

### Escalation Triggers

Escalate quickly when:

- the issue affects multiple services
- data integrity is at risk
- customer impact is active
- the rollback path is unclear
- the local team needs a cross-role decision

Use skill: `meeting-review` when you need structured multi-role analysis.

### Checklist

- [ ] exact symptom captured
- [ ] failure stage classified
- [ ] simplest explanations checked
- [ ] last known good state compared
- [ ] smallest failing layer isolated
- [ ] hypothesis tested with evidence
- [ ] smallest safe fix applied when root cause is known
- [ ] recovery verified
- [ ] follow-up gaps captured

### Related Workflows

- [Build & Deploy](build-deploy.md)
- [Service Review & Release](service-review-release.md)
- [Hotfix Production](hotfix-production.md)

### Related Skills

- **troubleshoot-service**: Diagnose service-level failures
- **navigate-service**: Map unfamiliar code paths before debugging
- **review-code**: Review risky fixes before delivery
- **meeting-review**: Escalate cross-role investigation decisions

### Failure Modes

- **Symptom before change**: a fix is applied before the symptom is captured. **Mitigation:** capture the exact symptom, the first meaningful error, and the recent changes before any change.
- **Multiple layers changed**: build, config, and code are all modified in one incident response. **Mitigation:** isolate one failure layer at a time; avoid unrelated cleanup during incident handling.
- **Fix not verified**: the fix is applied but recovery is not confirmed. **Mitigation:** verify recovery end-to-end; rerun the failing scenario; check for nearby regressions.
- **AI log summary trusted blindly**: an AI log summarization tool returns a root cause that is acted on without verification. **Mitigation:** verify every AI-identified root cause against raw evidence (logs, traces, metrics) before acting.
- **Distributed trace ignored**: the distributed trace shows the failing hop, but the engineer reads only logs. **Mitigation:** distributed-trace-first; let the trace identify the first failure point; require `trace_id` in the incident report.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/incident-report.json`** — Required fields: symptom, suspected layer, checks performed, root cause, fix applied, verification result, and follow-up items.
- **`contracts/schemas/implementation-result.json`** — For the fix code change; capture change summary, files touched, and the validation run.
- **`contracts/schemas/coordination-plan.json`** — When the troubleshooting cascades to multiple services or requires multi-role review; route through the coordinator.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a debug session may drift into changing application code outside the incident's scope. **Mitigation:** scope every debug change to the failing layer; open a separate task for unrelated fixes.
- **ASI03 Identity & Privilege Abuse**: production debugging credentials must be scoped to the SRE / on-call role; reject ad-hoc privilege escalation in the debug session.
- **ASI07 Inter-Agent Communication**: the incident report is consumed by SRE and DevOps roles; emit a structured `incident-report.json` so each role can validate the recovery.
- **ASI09 Human-Agent Trust Exploitation**: do not present the fix as "resolved" without end-to-end verification; surface the residual risk and the unverified checks honestly.
