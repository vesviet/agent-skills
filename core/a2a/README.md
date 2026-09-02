# A2A Registry And Antigravity Integration

This directory holds generated **Agent Cards** and the pack-level registry for A2A 1.0 discovery.

## Layout

```
a2a/
  README.md
  .well-known/
    agent-registry.json    # Index of all role agent cards
  registry/
    <role>.agent-card.json   # Generated per role
```

## Generate Registry

From repository root:

```bash
python3 core/scripts/generate-a2a-registry.py
```

Regenerates cards from `core/roles/*.md` and `core/skills/*/SKILL.md` metadata.

## Antigravity Usage

1. Copy `adapters/antigravity/rules.template.md` to your project as `.antigravity/rules.md`.
2. Merge `adapters/antigravity/a2a-config.template.yaml` into project agent config.
3. Point Antigravity at `core/a2a/.well-known/agent-registry.json` for role discovery.
4. Use `agent-a2a-protocol` skill for invoke/stream/cancel lifecycle.

## Pack-Local vs HTTP

In IDE workflows, agents often hand off via **files** (`a2a-task.json`, `a2a-artifact.json`) rather than HTTP. Agent Card `url` fields use the `pack://agent-skills/...` scheme for documentation and registry lookup. Deployed Antigravity services should replace `url` with real HTTPS endpoints.

## Spec Compliance Scope

The agent cards generated here are **pack-internal discovery manifests for IDE/CLI use**, not spec-compliant A2A 1.0 `AgentCard` documents. Specifically:

- The A2A 1.0 spec's `AgentCard` uses `supportedInterfaces` (a list of `{url, protocolBinding, protocolVersion}`) and `securitySchemes` (a map of `SecurityScheme` objects). This pack's cards use a single `url` string plus `authentication: {schemes: [...]}` instead — a simpler shape suited to file-based, single-transport IDE handoffs.
- Fields such as `stateTransitionHistory`, `contract_type`, `role_file`, `policy_profile`, and `defaultOutputSchemas` are **pack-local extensions** with no equivalent in the A2A 1.0 spec.
- The `protocol_version` field on each card reflects **this pack's** adherence level to A2A lifecycle concepts (task states, JSON-RPC envelope shape), not a claim that the card itself is byte-for-byte spec-compliant and ready to interoperate with an external A2A peer out of the box.
- Task lifecycle states (`submitted`, `working`, `input-required`, `completed`, `failed`, `canceled`) and the general request/response shape do follow the A2A 1.0 model; the divergence is in the `AgentCard` discovery document shape, not the task protocol itself.

If you need to interoperate with an external A2A 1.0 peer, transform these pack-local cards into spec-shaped `AgentCard` documents at the adapter boundary rather than publishing them as-is.

## Schemas

| Schema | Purpose |
|--------|---------|
| `agent-card.json` | Discovery manifest |
| `a2a-task.json` | Submit / delegate work |
| `a2a-task-status.json` | Get / list task state |
| `a2a-task-progress.json` | SSE streaming events |
| `a2a-message.json` | Task conversation parts |
| `a2a-artifact.json` | Worker deliverable |
| `a2a-jsonrpc-envelope.json` | JSON-RPC wire wrapper |

Full skill: `core/skills/agent/agent-a2a-protocol/SKILL.md`

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
