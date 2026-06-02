---
name: incident-report
description: Capture, structure, and communicate an incident from triage through resolution and prevention. Use when a production failure, degradation, or security event requires a formal timeline, impact assessment, root cause analysis, and follow-up action items.
---

# Incident Report

Use this skill when a production incident, degradation, or security event requires structured documentation and handoff.

## When To Use

- a service failure, degradation, or data issue is affecting users or downstream systems
- an on-call or SRE investigation needs to be handed off to another team
- a postmortem or retrospective requires evidence-backed findings
- incident action items need owners and timelines to prevent recurrence

## Core Rules

- do not close an incident without explicit action items and owners
- timeline must be built from evidence (logs, metrics, alerts, commits) — not reconstructed from memory alone
- customer and business impact must be stated explicitly; do not hide scope
- root cause must be distinguished from contributing factors and trigger events
- never include plaintext secrets, credentials, or PII in incident artifacts
- use `contracts/schemas/incident-report.json` for structured handoff to Agent Coordinator or SRE

## Suggested Process

### 1. Triage And Scope

Answer immediately:

- what is broken or degraded?
- what users, data, or services are affected?
- what is the severity and urgency?
- who owns response and communication?

Set incident severity before proceeding:

- **P0 (Critical):** total outage or data loss affecting production users
- **P1 (High):** major feature unavailable or significant performance degradation
- **P2 (Medium):** partial degradation with workaround available
- **P3 (Low):** minor issue with no immediate user impact

### 2. Build The Timeline

Reconstruct events in chronological order using evidence:

- first signal (alert, user report, monitoring spike)
- when the problem actually started (may predate detection)
- key investigation steps and findings
- mitigation actions taken and their effect
- resolution or containment time
- communication milestones

Use log timestamps, metric graphs, deploy records, and alert history — not estimations.

### 3. Assess Impact

Document clearly:

- affected services, endpoints, or data sets
- user segments and estimated affected count
- business impact (revenue, SLA breach, data integrity)
- downstream systems that were secondarily affected
- duration of impact (detection-to-mitigation and detection-to-resolution)

### 4. Root Cause Analysis

Distinguish:

- **Trigger:** the immediate cause that started the incident
- **Root cause:** the underlying condition that made the trigger possible
- **Contributing factors:** conditions that worsened severity or delayed detection

Use the 5-Whys or similar technique to move past the symptom layer.
Do not accept "human error" as a root cause — identify the systemic gap.

### 5. Action Items And Prevention

For each gap found, define:

- specific action to prevent recurrence or reduce blast radius
- owner (role or person)
- target completion date
- priority (blocking the next release vs. longer-term hardening)

Categories to consider:

- detection gaps (missing alerts, unclear dashboards)
- reliability gaps (retry logic, circuit breakers, health checks)
- process gaps (missing runbooks, unclear escalation paths)
- code or config changes needed

## Output Format

```markdown
# <Service> — Incident Report

## Summary
- Severity:
- Status (Open / Resolved / Monitoring):
- Duration: <detection time> → <resolution time>
- Impact: <user or business scope>

## Timeline
| Time (UTC) | Event |
|------------|-------|
| | First signal |
| | Investigation started |
| | Mitigation applied |
| | Resolution confirmed |

## Impact Assessment
- Affected services:
- User or business impact:
- Downstream effects:
- Data integrity:

## Root Cause
- Trigger:
- Root cause:
- Contributing factors:

## What Went Well
- (Detection, response, or communication strengths)

## What Went Wrong
- (Detection, response, or communication gaps)

## Action Items
| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| P0 | | | |
| P1 | | | |
```

Emit `contracts/schemas/incident-report.json` when machine handoff to Agent Coordinator or SRE is required.

## Checklist

- [ ] incident severity assigned
- [ ] timeline built from evidence (logs, metrics, alerts)
- [ ] user and business impact explicitly stated
- [ ] root cause separated from trigger and contributing factors
- [ ] "5 Whys" or equivalent used to move past symptom layer
- [ ] action items have owners and target dates
- [ ] secrets and PII excluded from all artifacts
- [ ] incident-report.json emitted if structured handoff required

## Related Skills

- **troubleshoot-service**: Diagnose and contain the active failure
- **review-service**: Broader service health check after resolution
- **add-telemetry-instrumentation**: Address detection gaps identified in action items
- **meeting-review**: Run the postmortem session with the involved team
- **write-documentation**: Update runbooks with lessons learned
