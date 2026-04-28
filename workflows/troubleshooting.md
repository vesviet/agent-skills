---
description: Workflow for diagnosing build, startup, runtime, and platform issues in a reusable way
---

## Troubleshooting Workflow

Use this workflow when a service, toolchain, or rollout behaves unexpectedly and you need a disciplined way to isolate the problem.

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

#### 2. Determine The Failure Stage

Role: **SRE**, **Backend Developer**

Classify the issue first:

- build or generation
- startup or dependency initialization
- runtime logic
- data or migration
- environment or platform

Use skill: `navigate-service` if the code path is not familiar yet.

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

### Related Workflows

- [Build & Deploy](build-deploy.md)
- [Service Review & Release](service-review-release.md)
- [Hotfix Production](hotfix-production.md)

### Related Skills

- troubleshoot-service
- navigate-service
- review-code
- meeting-review
