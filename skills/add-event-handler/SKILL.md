---
name: add-event-handler
description: Add or modify event publishers, consumers, or subscriber flows by following the repo's event contract, delivery semantics, idempotency rules, and rollout constraints. Use for event-driven service work.
---

# Add Event Handler

Use this skill when a change involves publishing an event, consuming one, or extending an event-driven workflow.

## Core Rules

- follow the repo's event naming and payload conventions
- preserve compatibility for existing consumers when evolving payloads
- make idempotency explicit for event consumers
- keep transport concerns separate from business decisions
- document ordering, retry, and failure behavior when it matters

## Suggested Process

### 1. Understand The Event Boundary

Identify:

- producer and consumer ownership
- source-of-truth event contract
- delivery guarantees and retry model
- whether ordering matters

### 2. Update Or Define The Event Contract

Change only what is needed:

- event name or topic reference
- payload schema
- versioning metadata when the repo uses it

Prefer additive evolution over breaking payload changes.

### 3. Implement Publish Or Consume Logic

For publishers:

- emit the event from the correct business boundary
- keep payload shaping explicit
- avoid publishing partial or inconsistent state

For consumers:

- deserialize safely
- validate required fields
- route into the correct internal flow
- handle duplicates and retries intentionally

### 4. Check Failure Behavior

Verify:

- what happens on partial failure
- whether retries are safe
- whether dead-letter or replay behavior exists
- whether downstream side effects need deduplication

### 5. Add Tests

Use skill: `write-tests`

Cover:

- valid payload handling
- invalid or incomplete payloads
- duplicate delivery or retry-sensitive paths
- side-effect safety

## Checklist

- [ ] event boundary understood
- [ ] contract updated safely
- [ ] publisher or consumer logic implemented
- [ ] idempotency considered
- [ ] failure and retry behavior checked
- [ ] tests added or updated

## Related Skills

- **navigate-service**: Trace existing event patterns in the repo
- **write-tests**: Add regression coverage for event behavior
- **review-code**: Review compatibility and idempotency risk
- **troubleshoot-service**: Debug failed consumers or publish flow issues
- **commit-code**: Prepare the event change for delivery
