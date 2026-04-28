---
name: troubleshoot-service
description: Troubleshoot build, startup, runtime, dependency, and configuration issues by isolating the failing layer, validating assumptions, and confirming recovery
---

# Troubleshoot Service Skill

Use this skill when a service fails to build, starts incorrectly, behaves unexpectedly at runtime, or breaks because of dependency, environment, or rollout problems.

## When to Use

- builds fail
- startup crashes or exits early
- runtime behavior is incorrect
- dependency calls fail or time out
- configuration or environment mismatches are suspected
- rollout succeeds technically but the service still does not behave correctly

## Core Rules

- capture the exact symptom before changing anything
- isolate one failure layer at a time
- prefer the smallest confirming check over broad guesswork
- compare with the last known good state whenever possible
- verify recovery after the fix, not just the absence of one error message

## Diagnostic Decision Tree

```text
Service issue
|- Build or generation failure
|- Startup or initialization failure
|- Runtime correctness failure
|- Data or dependency failure
`- Environment or rollout failure
```

## Suggested Troubleshooting Flow

### Step 1: Capture The Symptom

Collect:

- the exact command, request, or scenario that fails
- the first meaningful error message
- relevant logs or traces
- when the issue started
- what changed recently

### Step 2: Classify The Failure

Decide which layer is currently failing:

- build or code generation
- bootstrap or initialization
- request or job execution
- persistence or data shape
- dependency or network path
- environment, config, or rollout

Use skill: `navigate-service` if the code path is not yet clear.

### Step 3: Check The Simplest Explanations First

Verify:

- the expected revision is actually running
- required config and secrets are present
- dependencies are reachable
- generated files or migrations are current
- the failing path can be reproduced consistently

### Step 4: Compare With Last Known Good

Look for differences in:

- recent code changes
- dependency versions
- schema or migration state
- runtime config
- deployment or release metadata

### Step 5: Isolate The Failing Slice

Reduce the problem to the smallest useful scope:

- one package or build target
- one endpoint or handler
- one job or event consumer
- one query or write path
- one external dependency

This usually reveals whether the root cause is in code, data, config, or environment.

### Step 6: Form And Test A Hypothesis

Examples:

- generated artifacts are stale
- a dependency contract changed
- a migration and the running code are out of sync
- a config value is missing or malformed
- a timeout or retry policy is too aggressive
- the wrong environment or resource revision is live

Test one hypothesis at a time and record what confirmed or rejected it.

### Step 7: Apply The Smallest Safe Fix

Once the root cause is clear:

- make the narrowest change that resolves the issue
- avoid unrelated cleanup during incident handling
- rerun the failing scenario immediately

Use skill: `review-code` when the fix touches risky code paths.

### Step 8: Verify Recovery

Confirm:

- the original failure is resolved
- no nearby regressions appeared
- logs and health signals look normal
- dependent flows still work

### Step 9: Capture Follow-Up

If the issue exposed a process or design gap, note:

- missing tests
- missing alerts or dashboards
- weak config validation
- unsafe rollout assumptions
- missing runbook or documentation updates

## Common Failure Areas

### Build Or Generation

- stale generated artifacts
- missing tools or wrong tool versions
- bad imports or package references
- incompatible dependency changes

### Startup Or Initialization

- missing env vars or secrets
- invalid config values
- bootstrap ordering problems
- failed dependency connections

### Runtime Behavior

- unhandled edge cases
- stale assumptions in business logic
- race conditions or concurrency bugs
- incorrect error handling

### Data Or Persistence

- schema drift
- unsafe migration ordering
- missing indexes or bad query shape
- serialization or data-shape mismatches

### Dependency Or Network

- upstream contract drift
- DNS, routing, or auth failures
- timeout and retry misconfiguration
- partial availability of a downstream system

### Environment Or Rollout

- wrong revision deployed
- config source out of sync with code
- incomplete rollout
- missing runtime permissions or side resources

## What To Capture In Your Output

When reporting troubleshooting work, include:

- symptom
- suspected layer
- checks performed
- root cause
- fix applied
- verification result
- follow-up items

## Checklist

- [ ] exact symptom captured
- [ ] failure layer identified
- [ ] logs or traces reviewed
- [ ] recent changes compared
- [ ] smallest failing slice isolated
- [ ] root cause confirmed
- [ ] fix applied
- [ ] recovery verified

## Quick Reference

Use this for rapid troubleshooting:

- capture the exact error
- decide which layer is failing
- compare against last known good
- isolate one narrow failing path
- test one hypothesis
- verify the recovery

## Related Skills

- **navigate-service**: Understand the target flow before debugging
- **review-code**: Review a risky fix before landing it
- **commit-code**: Prepare the fix for delivery
- **performance-profiling**: Investigate latency, memory, or load-related failures
- **meeting-review**: Escalate for structured technical review
