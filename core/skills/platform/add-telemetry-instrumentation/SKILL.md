---
name: add-telemetry-instrumentation
description: Add or update logging, metrics, and tracing by following the repo's observability patterns. Use when a service, feature, endpoint, job, or integration needs operational visibility.
---

# Add Telemetry Instrumentation

Use this skill when code changes need matching observability so operators can understand traffic, failures, latency, and dependency behavior.

## Core Rules

- follow the repo's existing logging, metrics, and tracing patterns
- instrument important boundaries rather than every line of code
- keep telemetry names, labels, and dimensions stable enough for dashboards and alerts
- avoid high-cardinality labels unless the repo explicitly supports them
- never log secrets, credentials, tokens, or unnecessary sensitive data

## Suggested Process

### 1. Identify Critical Paths

Determine the key entrypoints, dependency calls, background jobs, and failure domains that need visibility.

### 2. Add Structured Logging

Add logs for meaningful state changes, warnings, and errors.

Prefer repo-local conventions for:

- log levels
- correlation IDs or request IDs
- structured fields
- error wrapping or stack capture

### 3. Add Metrics

Add or update metrics that help answer operational questions:

- request, job, or event counts
- latency or duration distributions
- failure counts by stable reason
- dependency call outcomes

### 4. Add Tracing

Instrument spans across service boundaries, external API calls, database queries, or long-running internal operations when the repo uses tracing.

### 5. Check Operational Usefulness

Verify that the telemetry can support dashboards, alerts, incident triage, and release verification without creating noise.

### 6. Validate Sensitive Data Handling

Confirm that logs, metrics labels, and trace attributes do not expose secrets, credentials, tokens, or unnecessary personal data.

## Checklist

- [ ] existing telemetry pattern reviewed
- [ ] critical paths identified
- [ ] structured logs added or updated
- [ ] metrics added or updated
- [ ] tracing added or updated when the repo uses tracing
- [ ] sensitive data exposure checked
- [ ] dashboards, alerts, or runbooks updated when needed

## Related Skills

- **debug-runtime-platform**: Investigate runtime behavior using telemetry evidence
- **setup-deployment**: Wire telemetry config into runtime source of truth
- **performance-profiling**: Measure latency, throughput, or resource bottlenecks
- **security-audit**: Review sensitive data exposure risk
- **commit-code**: Prepare telemetry changes for delivery
