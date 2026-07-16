---
name: add-event-handler
description: Add or modify event publishers, consumers, or subscriber flows by following the repo's event contract, delivery semantics, idempotency rules, and rollout constraints. Use for event-driven service work.
---

# Add Event Handler

Use this skill when a change involves publishing an event, consuming one, or extending an event-driven workflow.

## When to Use

- adding event publishers or consumers
- modifying subscriber flows
- enforcing idempotency / delivery semantics
- event-driven service work

## Core Rules

- follow the repo's event naming and payload conventions
- preserve compatibility for existing consumers when evolving payloads
- make idempotency explicit for event consumers
- keep transport concerns separate from business decisions
- document ordering, retry, and failure behavior when it matters
- if the repo uses a schema registry (Avro, Protobuf, JSON Schema), register or update the event schema before publishing
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting

### 2025-2026: AI-Generated Event Handlers and Agentic Event Flows

- **AI-generated event schema validation:** when AI tools generate event payload schemas or consumer logic, validate the generated schema against the repo's event contract before merging — LLMs frequently generate plausible but incompatible field names or data types that break existing consumers silently.
- **Idempotency guards for AI-triggered event floods:** agentic workflows can trigger event bursts when retrying failed tasks autonomously — ensure all consumers are idempotent by event ID (not just by content hash) so that agent retry loops do not produce duplicate side effects.
- **AI-orchestrated event choreography review:** when an agent orchestrates a sequence of events across services (e.g., agent-coordinator pattern), validate that the event chain has a defined termination condition and does not create unbounded feedback loops between event producers and consumers.
- **Dead-letter handling for agent-driven events:** require explicit DLQ (dead-letter queue) routing for events emitted by agentic systems — agent failures that silently drop events are harder to diagnose than human-authored failures; make the failure path observable.

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
- [ ] contract updated safely (schema registry updated if applicable)
- [ ] publisher or consumer logic implemented
- [ ] idempotency considered
- [ ] failure and retry behavior checked
- [ ] observability instrumented (OTel span on publish/consume)
- [ ] tests added or updated

## Related Skills

- **navigate-service**: Trace existing event patterns in the repo
- **write-tests**: Add regression coverage for event behavior
- **review-code**: Review compatibility and idempotency risk
- **add-telemetry-instrumentation**: Wire OTel spans for publish/consume operations
- **troubleshoot-service**: Debug failed consumers or publish flow issues
- **commit-code**: Prepare the event change for delivery
