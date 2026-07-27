# OTel GenAI Semantic Conventions — Agent Observability Guide

This document maps the **OpenTelemetry GenAI Semantic Conventions** (experimental, mid-2026) to the agent-skills observability model, providing actionable guidance for instrumenting agent sessions, multi-agent graphs, and MCP tool calls.

## Status

The OTel GenAI Semantic Conventions carry **Development** status (the current OTel term for what was previously labeled *experimental*), as of mid-2026. They are widely adopted by Datadog, Honeycomb, New Relic, LangChain, and CrewAI, but the API surface may still change. **Pin your convention version** in instrumentation code to avoid silent data breakage during updates.

The GenAI conventions now live in their own repository (moved out of the main `semantic-conventions` repo): [open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai). Authoritative sources: `docs/gen-ai/gen-ai-spans.md` (spans), `docs/gen-ai/mcp.md` (MCP), and `docs/registry/attributes/gen-ai.md` (attribute registry). When this guide and the upstream spec disagree, the upstream spec wins.

---

## Span Model

Every agent session is represented as a **trace of nested spans**. Use the spec's `gen_ai.operation.name` enum values — not invented names:

```
[ROOT SPAN] gen_ai.operation.name = "invoke_agent"   (gen_ai.agent.name = "backend-developer")
  ├─ [CHILD SPAN] gen_ai.operation.name = "chat" | "generate_content"   (LLM inference)
  ├─ [CHILD SPAN] gen_ai.operation.name = "execute_tool"   (gen_ai.tool.name = "write_file")
  ├─ [CHILD SPAN] gen_ai.operation.name = "invoke_agent"   (sub-agent delegation; new linked trace)
  │     └─ [ROOT SPAN] gen_ai.operation.name = "invoke_agent"   (gen_ai.agent.name = "reviewer")
  └─ [CHILD SPAN] gen_ai.operation.name = "plan" | "invoke_workflow"   (planning / workflow step)
```

Valid `gen_ai.operation.name` values (spec registry): `chat`, `generate_content`, `text_completion`, `embeddings`, `retrieval`, `create_agent`, `invoke_agent`, `invoke_workflow`, `plan`, `execute_tool`, and the memory operations (`create_memory`, `search_memory`, `update_memory`, `upsert_memory`, `delete_memory`, `create_memory_store`, `delete_memory_store`). There is no `llm_inference`, `tool_call`, `handoff`, `stream`, or `delegation` value.

---

## Standard Attribute Namespaces

Use only spec-defined `gen_ai.*` attributes for vendor-neutral compatibility. **Do not invent new `gen_ai.*` keys** — the namespace is reserved by OpenTelemetry. Pack-specific fields must use a distinct namespace (see "Pack extensions" below).

### Inference Spans (`chat` / `generate_content` / `text_completion` / `embeddings`)
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.operation.name` | string | Required. `chat`, `generate_content`, `text_completion`, or `embeddings` |
| `gen_ai.provider.name` | string | Required. Provider flavor: `anthropic`, `openai`, `gcp.gemini`, `gcp.vertex_ai`, `aws.bedrock`, etc. **Replaces the deprecated `gen_ai.system`** |
| `gen_ai.request.model` | string | Requested model identifier |
| `gen_ai.response.model` | string | Model that produced the response |
| `gen_ai.usage.input_tokens` | int | Input tokens consumed (includes cached tokens) |
| `gen_ai.usage.output_tokens` | int | Output tokens generated |
| `gen_ai.usage.reasoning.output_tokens` | int | Reasoning/thinking tokens (reasoning models); included in `output_tokens` |
| `gen_ai.usage.cache_read.input_tokens` | int | Input tokens served from a provider-managed cache |
| `gen_ai.response.finish_reasons` | string[] | Array of stop reasons (**plural** — e.g. `["stop"]`, `["stop","length"]`) |
| `gen_ai.conversation.id` | string | Session/thread id for correlating messages in a conversation |

### Agent Spans (`create_agent` / `invoke_agent` / `plan` / `invoke_workflow`)
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.operation.name` | string | `create_agent`, `invoke_agent`, `plan`, `invoke_workflow`, or `execute_tool` |
| `gen_ai.agent.name` | string | Human-readable agent name (map to the role slug, e.g. `backend-developer`) |
| `gen_ai.agent.id` | string | Session-scoped agent identity (NHI ID) |
| `gen_ai.conversation.id` | string | Coordination session id — correlate with `coordination-plan.json` |

> Cross-span correlation uses the **standard OTel `trace_id`** (span context), not a custom `gen_ai.trace_id`. There is no `gen_ai.trace_id` attribute in the spec. Use `gen_ai.conversation.id` to tie spans to a coordination session/thread.

### Tool Execution Spans (`execute_tool`)
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.operation.name` | string | Required. `execute_tool` |
| `gen_ai.tool.name` | string | Required. Tool name |
| `gen_ai.tool.call.id` | string | Unique call ID (if available) |
| `gen_ai.tool.type` | string | `function`, `extension`, or `datastore` |
| `gen_ai.tool.description` | string | Tool description (if available) |
| `gen_ai.tool.call.arguments` | any | Opt-in, sensitive — parameters passed to the tool |
| `gen_ai.tool.call.result` | any | Opt-in, sensitive — result returned by the tool |
| `error.type` | string | On error — error class. Tool outcome is expressed via **span status + `error.type`**, not a custom `gen_ai.tool.result.status` |

### MCP Tool Spans
MCP has its own conventions (`docs/gen-ai/mcp.md` in the GenAI repo); an `execute_tool` span for an MCP tool MAY be complemented by dedicated MCP instrumentation that traces `initialize`, `tools/list`, and `tools/call`. Verify exact attribute names against `mcp.md` before instrumenting — the following are illustrative:

| Attribute | Type | Description |
|---|---|---|
| `mcp.method.name` | string | MCP method (e.g. `tools/call`, `tools/list`) |
| `mcp.tool.name` | string | Tool name as declared in the server card |
| `mcp.request.id` | string | Request ID from the MCP JSON-RPC envelope |

### Pack Extensions (not part of OTel semconv)

The pack carries a few fields OTel does not define. Record these under a **pack-specific namespace** (e.g. `agentskills.*`) so they never collide with the reserved `gen_ai.*` namespace, and store them in the `extensions` map of `agent-trace-span.json`:

| Attribute | Description |
|---|---|
| `agentskills.tool.policy_action` | Policy action checked against `action-boundaries.yaml` (`allowed` / `requires_approval` / `denied`) |
| `agentskills.delegate.from_role` / `.to_role` | A2A delegation roles (the delegation itself is an `invoke_agent` span) |
| `agentskills.delegate.task_id` | A2A task ID (`a2a-task.json`) |
| `agentskills.delegate.artifact_schema` | Expected output schema ref |

---

## Mapping to Pack Schema

The `contracts/schemas/agent-trace-span.json` schema covers:

- `trace_id` → standard OTel trace context; correlate a coordination session via `gen_ai.conversation.id` (set from `coordination-plan.json` `goal.trace_id`)
- `span_id` → unique span identifier
- `role` → `gen_ai.agent.name`
- `operation` → `gen_ai.operation.name` (must be a valid enum value — see Span Model)
- `status` → OTel span status; on failure also set `error.type` (there is no `gen_ai.tool.result.status`)

**Extension pattern**: Carry spec `gen_ai.*` attributes not in the base schema, plus pack-specific `agentskills.*` fields, in the `extensions` map of `agent-trace-span.json`. Do not modify the base schema, and do not mint new `gen_ai.*` keys — that namespace is owned by OpenTelemetry.

---

## Collection Rules

1. **Always emit**: root span per agent session (`invoke_agent`), inference spans (`chat`/`generate_content`), `execute_tool` spans for state-changing actions
2. **Conditionally emit**: MCP tool spans (when MCP tools are invoked), sub-agent spans (`invoke_agent` when A2A tasks are dispatched), `plan`/`invoke_workflow` spans for orchestration
3. **Content capture is off by default**: the message-content attributes — `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.tool.call.arguments`, `gen_ai.tool.call.result` — are Opt-In and flagged sensitive by the spec. Enable them only behind an explicit opt-in (e.g. `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`), and in production prefer external content storage with references on the span over inline capture.
4. **Never include** in span attributes:
   - Secrets, tokens, API keys (classified `restricted` per `data-classification.yaml`)
   - PII (names, emails, phone numbers)
   - Full prompt/completion content in production (classified `internal` or higher) unless the opt-in above is deliberately enabled for a non-production environment
5. **Span retention**: spans are session-scoped (`retention_in_context: session_only` for `internal` data)
6. **Do not commit span files**: local JSONL trace logs under `core/observability/` must be `.gitignore`d

---

## Recommended Tooling (2026)

| Use case | Tool |
|---|---|
| Local dev tracing | [OpenLIT](https://openlit.io) — zero-config OTel collector for LLM apps |
| Cloud observability | Datadog LLM Observability, Honeycomb Agent Timeline |
| Schema validation | `npx ajv validate -s contracts/schemas/agent-trace-span.json -d my-span.json` |
| Cursor hook logging | `core/scripts/hooks/log-trace-span.py` |

---

## Skill Reference

The `agent-observability` skill (`core/skills/agent/agent-observability/`) operationalizes this guide. Use that skill when adding tracing instrumentation to a new role or tool integration.

---

## Related Standards

- OTel GenAI SIG: [opentelemetry.io/docs/specs/semconv/gen-ai/](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- A2A 1.0 trace correlation: `core/a2a/README.md`
- Pack schema: `contracts/schemas/agent-trace-span.json`
- Data classification: `core/policies/data-classification.yaml`
- MCP tool mapping: `core/policies/mcp-tool-map.yaml`

*Last updated: 2026-07-27 | Aligned with the OTel GenAI semantic conventions (Development status; `open-telemetry/semantic-conventions-genai`, mid-2026)*
