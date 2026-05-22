# Cursor Adapter — Agent Skills Pack

## Files

| File | Purpose |
|------|---------|
| [hooks.template.json](hooks.template.json) | Copy to project `.cursor/hooks.json` for policy enforcement |
| Pack rules | `.cursorrules` + `.cursor/rules/agent-skills.md` at repo root |

## Setup

```bash
mkdir -p .cursor
cp adapters/cursor/hooks.template.json .cursor/hooks.json
# Edit hooks.json paths to point at your agent-skills checkout
```

Hooks enforce `action-boundaries.yaml` on `preToolUse` / `beforeMCPExecution` when scripts are enabled.

## Antigravity

Cursor and Antigravity share pack contracts. For A2A registry and Antigravity-specific config, also use [../antigravity/ANTIGRAVITY.md](../antigravity/ANTIGRAVITY.md).
