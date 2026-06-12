# Antigravity Adapter — Agent Skills Pack

Use this adapter when running **Google Antigravity** (or Antigravity-compatible IDEs) with the agent-skills engineering pack.

## Quick Start

1. Install or link this pack into your workspace.
2. Copy templates into the active project:

```bash
mkdir -p .antigravity
cp adapters/antigravity/rules.template.md .antigravity/rules.md
cp adapters/antigravity/a2a-config.template.yaml .antigravity/a2a-config.yaml
```

3. Generate the role registry:

```bash
python3 core/scripts/generate-a2a-registry.py
```

4. Assign roles via Antigravity agent picker or prompt: `Act as @backend-developer`.

## Mandatory Behavior (Antigravity + Pack)

When operating under this pack in Antigravity:

1. Read `core/rules/code.md` before state-changing actions.
2. Read `core/roles/role-standard.md` then `core/roles/<role>.md` when a role is assigned.
3. Emit **structured JSON contracts** from `core/contracts/schemas/` for handoffs — not prose-only.
4. Use **A2A full lifecycle** via `agent-a2a-protocol` and `agent-delegation`:
   - Submit: `a2a-task.json` (`state: submitted`)
   - Stream: `a2a-task-progress.json` events while `working`
   - Complete: `a2a-artifact.json` + `a2a-task-status.json`
   - Cancel: set `state: canceled` with `cancel_reason`
5. Discover workers via `core/a2a/.well-known/agent-registry.json` and per-role `*.agent-card.json`.
6. Obey `core/policies/action-boundaries.yaml` and `data-classification.yaml`.

## A2A Config Block

Antigravity projects may declare:

```yaml
# .antigravity/a2a-config.yaml (from template)
a2a:
  enabled: true
  protocol_version: "1.0"
  registry: "core/a2a/.well-known/agent-registry.json"
  default_interaction_mode: stream
  default_risk_tier: engineering
```

Map each capability `id` to a pack role slug (see generated agent cards).

## JSON-RPC Methods (Wire Deployments)

When exposing HTTP services (Cloudflare Workers, AgentKit):

| Method | Pack schema |
|--------|-------------|
| `agent.getCard` | `agent-card.json` |
| `agent.invoke` | `a2a-jsonrpc-envelope.json` → `a2a-task.json` |
| `agent.stream` | SSE of `a2a-task-progress.json` |
| `tasks/get` | `a2a-task-status.json` |
| `tasks/list` | array of `a2a-task-status.json` |
| `tasks/cancel` | updates `a2a-task-status.json` |

## Coordinator Pattern

For end-to-end delivery, assign **Agent Coordinator**:

- Publishes `coordination-plan.json`
- Issues `a2a-task.json` per phase with `assignee_agent_card` from registry
- Validates `a2a-artifact.json` before phase `completed`

## References

- Pack contracts: `core/contracts/README.md`
- A2A skill: `core/skills/agent/agent-a2a-protocol/SKILL.md`
- User guide: `USER_GUIDE_v2.md` (full contract table and role examples)
- Official A2A: https://a2a-protocol.org/latest/specification/
