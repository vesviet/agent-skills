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

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-02
