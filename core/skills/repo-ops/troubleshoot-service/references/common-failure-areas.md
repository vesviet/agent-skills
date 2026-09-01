# Troubleshoot Service — Common Failure Areas (Reference)

Per-layer failure pattern library extracted from `SKILL.md` to keep the
main file under 200 lines. Load this file when triaging an unfamiliar
incident, when authoring a runbook, or when training a new on-call
engineer.

## Build Or Generation

- stale generated artifacts
- missing tools or wrong tool versions
- bad imports or package references
- incompatible dependency changes

## Startup Or Initialization

- missing env vars or secrets
- invalid config values
- bootstrap ordering problems
- failed dependency connections

## Runtime Behavior

- unhandled edge cases
- stale assumptions in business logic
- race conditions or concurrency bugs
- incorrect error handling

## Data Or Persistence

- schema drift
- unsafe migration ordering
- missing indexes or bad query shape
- serialization or data-shape mismatches

## Dependency Or Network

- upstream contract drift
- DNS, routing, or auth failures
- timeout and retry misconfiguration
- partial availability of a downstream system

## Environment Or Rollout

- wrong revision deployed
- config source out of sync with code
- incomplete rollout
- missing runtime permissions or side resources

## Diagnostic Decision Tree

```text
Service issue
|- Build or generation failure
|- Startup or initialization failure
|- Runtime correctness failure
|- Data or dependency failure
`- Environment or rollout failure
```

## K8s Diagnostic Signals

`kubectl describe pod` events show `OOMKilled`, `CrashLoopBackOff`, and `ImagePullBackOff` with reasons. CPU throttling (visible in `kubectl top`) is a frequent cause of latency spikes that do not appear in application logs.

## Distributed Trace First

When a service behaves unexpectedly, start with the distributed trace (Jaeger, Tempo, Datadog APM) before reading logs — the trace shows the exact causal chain across services and identifies the first failure point.

## AI Log Analysis Advisory

Use AI-powered log summarization (Datadog Bits AI, Elastic AI Assistant) to surface signal from high-volume log noise. Always verify any AI-identified root cause against raw evidence before acting.
