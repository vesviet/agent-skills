---
name: agent-a2a-protocol
description: Implement the full A2A 1.0 task lifecycle including Agent Card discovery, JSON-RPC invoke/stream, task get/list/cancel, SSE progress events, and Antigravity-compatible handoffs. Use when integrating multi-agent systems, exposing agent services, or operating as Antigravity with structured agent-to-agent communication.
---

# Agent A2a Protocol

Use this skill for **complete A2A 1.0** behavior beyond single-hop `agent-delegation`. Required for Antigravity deployments and Coordinator scatter-gather patterns.

## When to Use

- integrating multi-agent systems with structured A2A 1.0 communication
- exposing an agent service via Agent Cards and JSON-RPC invoke/stream
- operating as Antigravity and needing SSE progress + task handoffs
- coordinating scatter-gather across multiple agents

## Core Rules

- publish or consume **Agent Cards** (`agent-card.json`) before delegating
- use UUID v4 for `task_id` when targeting Antigravity AgentKit
- drive tasks through states: `submitted` → `working` → (`input-required` optional) → terminal
- terminal states: `completed`, `failed`, `canceled`
- stream long work via `a2a-task-progress.json` (SSE) when `interaction_mode` is `stream`
- wrap HTTP calls in `a2a-jsonrpc-envelope.json` (JSON-RPC 2.0)
- validate every artifact against the task's `output_schema_ref`
- never assume the worker has context beyond `input_data` and `messages`
- verify A2A v1.0 signed Agent Cards, reading acceptable authentication methods from the card's `securitySchemes` field (which may declare `bearer`, `oauth2`, `apiKey`, or OIDC)
- verify Agent Card JWS signatures by resolving the key from the card's `kid` / `jku` JWK Set; card signing is a spec **SHOULD**, and the signing algorithm is chosen by the issuer, not fixed by the spec
- publish streaming lifecycle events using the `event` enum in `contracts/schemas/a2a-task-progress.json`: `task.created`, `task.status`, `task.message`, `task.artifact`, `task.completed`, `task.failed`, `task.canceled`
- validate webhook push notification callbacks against the credentials declared in the task's `PushNotificationConfig.authentication`, and validate the callback URL against SSRF before registering it

**Spec vs pack convention.** The A2A specification streams `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` over SSE, with task states named `TASK_STATE_*`. The `task.*` event names and the `agent.invoke` / `agent.stream` JSON-RPC methods used throughout this pack are the **Antigravity adapter binding**, not spec wire names — the spec operations are `message/send`, `message/stream`, `tasks/get`, and `tasks/cancel`. When targeting a non-Antigravity A2A peer, use the spec names and treat this pack's names as a local alias layer.

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

### Signed Agent Cards

A2A v1.0 adds cryptographically signed Agent Cards to guarantee identity and configuration integrity:
- **Signature format**: Cards carry detached JWS signatures over the card canonicalized per RFC 8785 (JCS). The spec does **not** mandate a signing algorithm — read it from the JWS header rather than assuming one.
- **Key resolution**: Resolve the verification key from the JWS header's `kid` or `jku` pointing at a JWK Set. A pinned trusted key store is a spec **MAY**; adopt it as a local hardening measure and say so.
- **Conformance level**: Signature verification is a **SHOULD** in the spec, not a MUST. This pack raises it to a requirement for distributed deployments (see the coordinator's DELEGATE-VERIFICATION LOCK) — that is a pack-local tightening, not a spec quote.
- **Security Schemes**: The Agent Card JSON includes a `securitySchemes` field defining acceptable authentication methods. The spec permits `bearer`, `oauth2`, `apiKey`, and OpenID Connect — do not assume only the first two.

### Streaming Transport

For high-frequency and long-running communications:
- **Spec transport**: A2A streams over **Server-Sent Events** via `message/stream`, with `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` as the event payloads. gRPC and REST bindings also exist.
- **Pack binding**: this pack models each SSE payload as `a2a-task-progress.json` and reaches it through the Antigravity `agent.stream` method. Both are local aliases over `message/stream`.
- **No json-seq requirement**: `application/json-seq` (RFC 7464) is **not** part of the A2A specification. Do not negotiate it against a spec-conformant peer or claim it as required; use SSE unless a specific peer documents another framing.

### Task Lifecycle Events

- **Spec events**: `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent`, carrying states `TASK_STATE_SUBMITTED`, `TASK_STATE_WORKING`, `TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`, `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, `TASK_STATE_REJECTED`.
- **Pack events**: the `event` enum in `contracts/schemas/a2a-task-progress.json` — `task.created`, `task.status`, `task.message`, `task.artifact`, `task.completed`, `task.failed`, `task.canceled`. This is the authoritative list for pack-internal streaming; the schema, not this prose, is the source of truth.
- **Mapping**: `task.status` carries the spec's status transitions in its `state` field; `task.artifact` corresponds to `TaskArtifactUpdateEvent`. Translate at the adapter boundary when talking to an external A2A peer.

### Webhook Push Notifications

Webhook push notifications allow asynchronous updates to be pushed to the delegator:
- **Registration**: Tasks configure a webhook URL for status callbacks via `PushNotificationConfig`.
- **Authentication**: The spec authenticates callbacks using the credentials declared in `PushNotificationConfig.authentication`. There is no spec-defined signature header — an HMAC header such as `X-A2A-Signature` is a valid local hardening choice, but must be documented as pack-local rather than cited as protocol.
- **SSRF validation**: Validate the callback URL before registering it (reject internal/link-local targets); the spec calls this out explicitly as a required safeguard.

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
