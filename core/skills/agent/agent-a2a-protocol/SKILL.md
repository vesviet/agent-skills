---
name: agent-a2a-protocol
description: Implement the full A2A 1.0 task lifecycle including Agent Card discovery, JSON-RPC invoke/stream, task get/list/cancel, SSE progress events, and Antigravity-compatible handoffs. Use when integrating multi-agent systems, exposing agent services, or operating as Antigravity with structured agent-to-agent communication.
---

# Agent A2a Protocol

Use this skill for **complete A2A 1.0** behavior beyond single-hop `agent-delegation`. Required for Antigravity deployments and Coordinator scatter-gather patterns.

## Core Rules

- publish or consume **Agent Cards** (`agent-card.json`) before delegating
- use UUID v4 for `task_id` when targeting Antigravity AgentKit
- drive tasks through states: `submitted` → `working` → (`input-required` optional) → terminal
- terminal states: `completed`, `failed`, `canceled`
- stream long work via `a2a-task-progress.json` (SSE) when `interaction_mode` is `stream`
- wrap HTTP calls in `a2a-jsonrpc-envelope.json` (JSON-RPC 2.0)
- validate every artifact against the task's `output_schema_ref`
- never assume the worker has context beyond `input_data` and `messages`

## A2A Operations Map

| Operation | Pack artifact | When |
|-----------|---------------|------|
| Discover | `agent-card.json` / registry | Before delegate |
| Submit task | `a2a-task.json` | Delegate work |
| Stream progress | `a2a-task-progress.json` | `interaction_mode: stream` |
| Get status | `a2a-task-status.json` | Poll or audit |
| List tasks | `a2a-task-status.json[]` | Coordinator dashboards |
| Cancel | update status `canceled` | User abort / timeout |
| Deliver | `a2a-artifact.json` | Worker completion |

## Antigravity Integration

1. Load `core/a2a/.well-known/agent-registry.json`.
2. Resolve `assignee_role` → `core/a2a/registry/<role>.agent-card.json`.
3. Set `assignee_agent_card` on the task when using registry discovery.
4. Prefer `agent.stream` for engineering-tier tasks; `agent.invoke` for short sync work.
5. Apply `.antigravity/rules.md` from `adapters/antigravity/rules.template.md`.

Config template: `adapters/antigravity/a2a-config.template.yaml`.

## Suggested Process

### 1. Discover Worker Capabilities

Read Agent Card:

- `skills[].id` and `output_schema_refs`
- `capabilities.streaming`
- `policy_profile` for action boundaries

### 2. Submit Task

Compose `a2a-task.json`:

- `state: submitted`
- `interaction_mode`: `sync` | `stream` | `push`
- full `input_data`, `success_criteria`, `constraints`
- `parent_task_id` when part of `coordination-plan.json`

### 3. Monitor (Stream Or Poll)

**Stream:** emit progress events:

```json
{"event":"task.status","task_id":"...","state":"working","progress_percent":40}
```

**Poll:** build `a2a-task-status.json` with `messages` history.

### 4. Handle input-required

If worker needs delegator decision:

- set `state: input-required`
- append `a2a-message.json` with question
- resume with new message and `state: working`

### 5. Complete Or Fail

Worker returns `a2a-artifact.json`:

- set `status` and mirror `state`
- populate `parts` for multimodal results
- include `trace_id` and `token_usage`

Delegator validates `result` against `output_schema_ref`.

### 6. Cancel

On timeout or user abort:

- compose `a2a-task-cancel.json` with `task_id`, `cancel_reason`, optional `force`
- apply via `tasks/cancel` (JSON-RPC) or file update → `a2a-task-status.json` with `state: canceled`

### 7. Push Notifications (Long-Running)

When the client cannot hold SSE open:

- attach `a2a-push-notification-config.json` to the task
- worker emits terminal event to `callback_url` on completed / failed / canceled

## Scatter-Gather

Coordinator pattern:

1. Publish `coordination-plan.json` with parallel groups.
2. Submit child `a2a-task.json` per phase with shared `parent_task_id`.
3. Merge artifacts at join phase; block downstream until all branches `completed` or explicit `partial` acceptance.

## JSON-RPC Example (Wire)

Request:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "agent.invoke",
  "params": {
    "capability": "backend-implement",
    "task": { }
  }
}
```

Response result should embed `a2a-task-status.json` or `a2a-artifact.json`.

## Checklist

- [ ] worker Agent Card loaded from registry
- [ ] task_id is unique (UUID v4 for Antigravity)
- [ ] interaction_mode matches expected duration
- [ ] output_schema_ref points to existing pack schema
- [ ] streaming events emitted for engineering-tier long tasks
- [ ] get/list status available for in-flight audit
- [ ] cancel path defined for timeouts
- [ ] artifact validated before phase gate opens
- [ ] JSON-RPC errors use standard envelope on wire transports

## Observability

Emit `agent-trace-span.json` records (or JSONL via Cursor hooks) for material operations. Include `trace_id` on artifacts for correlation.

## Related Skills

- **agent-delegation**: Single-hop delegate with minimal ceremony
- **agent-graph-orchestration**: Phase graphs and parallel merge
- **agent-tool-orchestration**: Policy checks before tools
- **agent-observability**: trace_id and token_usage on artifacts
