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
