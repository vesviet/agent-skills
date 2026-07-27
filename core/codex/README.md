# Codex Adapter — Agent Skills Pack

OpenAI Codex reads `AGENTS.md` (the shared open standard) as its rule source — for both coding tasks and Code Review custom rules. The pack's root `AGENTS.md` therefore drives Codex behavior with no additional rule file required.

## Files

| File | Purpose |
|------|---------|
| `AGENTS.md` (repo root) | Always-on rules, role system, A2A, and pack navigation (shared open standard; also read by Cursor, Kilo Code, Windsurf, and VS Code Copilot) |
| `core/codex/.a2a-config.json` | Codex A2A 1.0 discovery config (registry URL, sync/notification timing, pack version) |
| `core/skills/*/*/agents/openai.yaml` | Per-skill Codex interface adapters — invoke skills via `$skill-name` |

## Setup

1. Ensure `AGENTS.md` is at the repository root (it is, in this pack). Codex reads the nearest `AGENTS.md` in the directory tree.
2. Point Codex A2A discovery at the pack registry via `core/codex/.a2a-config.json`. Regenerate the registry after role edits:
   ```bash
   python3 core/scripts/generate-a2a-registry.py
   ```
3. Invoke skills with `$skill-name` (e.g. `$add-api-endpoint`); each skill ships an `agents/openai.yaml` interface descriptor.

## Rules, Policy, and A2A

Codex must honor the same operating contract as every other adapter:

- Rules source of truth: `core/rules/code.md` (mirrored in `AGENTS.md`).
- Policy-as-Code: check `core/policies/action-boundaries.yaml` and `core/policies/data-classification.yaml` before state-changing actions; map tools via `core/policies/mcp-tool-map.yaml`.
- A2A 1.0: discover agents via `core/a2a/.well-known/agent-registry.json`; use the `agent-a2a-protocol` skill for the full task lifecycle; emit structured handoffs from `core/contracts/schemas/`.

Parity with other adapters is enforced by `core/scripts/validate-rules.py` (see `core/adapter-parity.md`).

## Related

- Adapter parity standard: `core/adapter-parity.md`
- Cursor / Kiro adapter: `adapters/cursor/README.md`
- Claude adapter: `adapters/claude/CLAUDE_ADAPTER.md`
- Antigravity adapter: `adapters/antigravity/ANTIGRAVITY.md`
