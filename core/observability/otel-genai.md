# OTel GenAI Semantic Conventions — Agent Observability Guide

This document maps the **OpenTelemetry GenAI Semantic Conventions** (experimental, mid-2026) to the agent-skills observability model, providing actionable guidance for instrumenting agent sessions, multi-agent graphs, and MCP tool calls.

## Status

The OTel GenAI Semantic Conventions are currently **experimental** (as of July 2026). They are widely adopted by Datadog, Honeycomb, New Relic, LangChain, and CrewAI but the API surface may still change. **Pin your convention version** in instrumentation code to avoid data breakage during updates.

Repository: [open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)

---

## Span Model

Every agent session is represented as a **trace of nested spans**:

```
[ROOT SPAN] gen_ai.agent.name = "backend-developer"
  ├─ [CHILD SPAN] gen_ai.operation.name = "llm_inference"
  ├─ [CHILD SPAN] gen_ai.operation.name = "tool_call" (tool: write_file)
  ├─ [CHILD SPAN] gen_ai.operation.name = "sub_agent_delegation"
  │     └─ [ROOT SPAN] gen_ai.agent.name = "reviewer" (new trace, linked)
  └─ [CHILD SPAN] gen_ai.operation.name = "handoff"
```

---

## Standard Attribute Namespaces

Use only `gen_ai.*` namespaces for vendor-neutral compatibility:

### LLM Inference Spans
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.system` | string | Model provider (e.g., `anthropic`, `openai`, `google`) |
| `gen_ai.request.model` | string | Requested model identifier |
| `gen_ai.usage.input_tokens` | int | Input tokens consumed |
| `gen_ai.usage.output_tokens` | int | Output tokens generated |
| `gen_ai.response.finish_reason` | string | Why generation stopped (e.g., `stop`, `max_tokens`) |

### Agent Session Spans
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.agent.name` | string | Role slug (matches `agent-registry.json` role) |
| `gen_ai.agent.id` | string | Session-scoped agent identity (NHI ID) |
| `gen_ai.agent.version` | string | Pack version (e.g., `2.12.0`) |
| `gen_ai.operation.name` | string | Operation type: `invoke`, `stream`, `handoff`, `delegation` |
| `gen_ai.trace_id` | string | Coordination trace ID from `coordination-plan.json` |

### Tool Call Spans
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.tool.name` | string | Tool identifier (maps to `mcp-tool-map.yaml` key) |
| `gen_ai.tool.call.id` | string | Unique call ID |
| `gen_ai.tool.result.status` | string | `success`, `error`, `denied` |
| `gen_ai.tool.policy_action` | string | Policy action checked (from `action-boundaries.yaml`) |

### MCP Tool Call Spans (New in OTel GenAI SIG 2026)
| Attribute | Type | Description |
|---|---|---|
| `mcp.server.name` | string | MCP server identifier |
| `mcp.tool.name` | string | Tool name as declared in server card |
| `mcp.protocol_version` | string | MCP version in use |
| `mcp.request.id` | string | Request ID from MCP envelope |

### Multi-Agent Handoff Spans
| Attribute | Type | Description |
|---|---|---|
| `gen_ai.delegate.from_role` | string | Delegating agent role |
| `gen_ai.delegate.to_role` | string | Receiving agent role |
| `gen_ai.delegate.task_id` | string | A2A task ID (`a2a-task.json`) |
| `gen_ai.delegate.artifact_schema` | string | Expected output schema ref |

---

## Mapping to Pack Schema

The `contracts/schemas/agent-trace-span.json` schema covers:

- `trace_id` → root trace for correlation with `coordination-plan.json` `goal.trace_id`
- `span_id` → unique span identifier
- `role` → `gen_ai.agent.name`
- `operation` → `gen_ai.operation.name`
- `status` → `gen_ai.tool.result.status`

**Extension pattern**: Add `attributes` field to `agent-trace-span.json` instances to carry `gen_ai.*` attributes not in the base schema. Do not modify the base schema — use the `extensions` map field.

---

## Collection Rules

1. **Always emit**: root span per agent session, LLM inference spans, tool call spans for state-changing actions
2. **Conditionally emit**: MCP tool spans (when MCP tools are invoked), delegation spans (when A2A tasks are dispatched)
3. **Never include** in span attributes:
   - Secrets, tokens, API keys (classified `restricted` per `data-classification.yaml`)
   - PII (names, emails, phone numbers)
   - Full prompt/completion content in production (classified `internal` or higher)
4. **Span retention**: spans are session-scoped (`retention_in_context: session_only` for `internal` data)
5. **Do not commit span files**: local JSONL trace logs under `core/observability/` must be `.gitignore`d

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

*Last updated: 2026-07-01 | Aligned with OTel GenAI SIG experimental (mid-2026)*
