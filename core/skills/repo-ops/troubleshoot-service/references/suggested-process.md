# Troubleshoot Service — Suggested Process (Reference)

## Suggested Process

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

For the per-layer failure pattern library (Build/Generation, Startup,
Runtime, Data/Persistence, Dependency/Network, Environment/Rollout), the
diagnostic decision tree, the K8s diagnostic signals, the distributed-trace
rule, and the AI log analysis advisory, see
[`common-failure-areas.md`](common-failure-areas.md).


