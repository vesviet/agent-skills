# Agent Observability

This directory contains observability resources for agent sessions.

## Contents

- **[otel-genai.md](otel-genai.md)** — OpenTelemetry GenAI Semantic Conventions mapping: span model, attribute namespaces, MCP tool tracing, multi-agent handoff spans, and collection rules. **Start here** when adding tracing to a new role or tool.
- Local JSONL trace logs written by `core/scripts/hooks/log-trace-span.py` (when Cursor hooks are enabled) — do not commit these files.

## Schema

Span structure: `contracts/schemas/agent-trace-span.json`

## Related

- OTel GenAI guide: `observability/otel-genai.md`
- Trace-span skill: `skills/agent/agent-observability/`
- Data classification: `policies/data-classification.yaml`

Do not commit span files — they may contain paths from active sessions.
