# A2A 1.0 Spec Details

Deep-dive reference for `agent-a2a-protocol`. Load this file when you need the exact spec behavior behind a pack convention — the SKILL.md Core Rules already state the pack-local aliases; this file has the spec-vs-pack mapping in full.

## Signed Agent Cards

A2A v1.0 adds cryptographically signed Agent Cards to guarantee identity and configuration integrity:

- **Signature format**: Cards carry detached JWS signatures over the card canonicalized per RFC 8785 (JCS). The spec does **not** mandate a signing algorithm — read it from the JWS header rather than assuming one.
- **Key resolution**: Resolve the verification key from the JWS header's `kid` or `jku` pointing at a JWK Set. A pinned trusted key store is a spec **MAY**; adopt it as a local hardening measure and say so.
- **Conformance level**: Signature verification is a **SHOULD** in the spec, not a MUST. This pack raises it to a requirement for distributed deployments (see the coordinator's DELEGATE-VERIFICATION LOCK) — that is a pack-local tightening, not a spec quote.
- **Security Schemes**: The Agent Card JSON includes a `securitySchemes` field defining acceptable authentication methods. The spec permits `bearer`, `oauth2`, `apiKey`, and OpenID Connect — do not assume only the first two.

## Streaming Transport

For high-frequency and long-running communications:

- **Spec transport**: A2A streams over **Server-Sent Events** via `message/stream`, with `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` as the event payloads. gRPC and REST bindings also exist.
- **Pack binding**: this pack models each SSE payload as `a2a-task-progress.json` and reaches it through the Antigravity `agent.stream` method. Both are local aliases over `message/stream`.
- **No json-seq requirement**: `application/json-seq` (RFC 7464) is **not** part of the A2A specification. Do not negotiate it against a spec-conformant peer or claim it as required; use SSE unless a specific peer documents another framing.

## Task Lifecycle Events

- **Spec events**: `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent`, carrying states `TASK_STATE_SUBMITTED`, `TASK_STATE_WORKING`, `TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`, `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, `TASK_STATE_REJECTED`.
- **Pack events**: the `event` enum in `contracts/schemas/a2a-task-progress.json` — `task.created`, `task.status`, `task.message`, `task.artifact`, `task.completed`, `task.failed`, `task.canceled`. This is the authoritative list for pack-internal streaming; the schema, not this prose, is the source of truth.
- **Mapping**: `task.status` carries the spec's status transitions in its `state` field; `task.artifact` corresponds to `TaskArtifactUpdateEvent`. Translate at the adapter boundary when talking to an external A2A peer.

## Webhook Push Notifications

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
