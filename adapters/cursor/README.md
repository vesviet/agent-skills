# Cursor / Kiro Adapter — Agent Skills Pack

## Files

| File | Purpose |
|------|---------|
| [`hooks.template.json`](hooks.template.json) | Cursor-format hook template — copy to `.cursor/hooks.json` and adjust paths |
| Pack rules | `.cursor/rules/agent-skills.md` (always-on `.mdc` rule mirror) |

> **`.cursorrules` is deprecated** as of Cursor late 2025. Migrate to `.cursor/rules/*.mdc` with YAML frontmatter. The static `.cursorrules` file is no longer read by current Cursor versions.

The pack also ships **Kiro-native hooks** at `.kiro/hooks/` (see Kiro section below).

---

## `.mdc` Rules Format (2026)

Rules live in `.cursor/rules/*.mdc` with YAML frontmatter:

```markdown
---
description: "Brief description of when to apply this rule"
globs: ["internal/**/*.go", "api/**/*.proto"]
alwaysApply: false
---
# Rule content here
```

**Activation modes:**

| Mode | Frontmatter | Behavior |
|------|-------------|----------|
| Always Apply | `alwaysApply: true` | Injected into every chat session |
| Auto Attached | `alwaysApply: false` + `globs:` | Injected when working on matching files |
| Agent Requested | `description:` only (no `globs`) | AI decides to use based on description |
| Manual | None | User invokes with `@rule-name` |

---

## Cursor Setup

```bash
# Already done for agent-skills repo itself:
# .cursor/hooks.json  ← instantiated from this template

# For other projects using this pack:
mkdir -p .cursor
cp adapters/cursor/hooks.template.json .cursor/hooks.json
# Edit AGENT_SKILLS_ROOT to the absolute path of this pack checkout
```

### What the hooks do

| Hook event | Action | Effect |
|------------|--------|--------|
| `sessionStart` | `echo` reminder | Prompt to load `core/rules/code.md` |
| `beforeReadFile` | `check-policy.py` | Blocks reads on sensitive file patterns (`.env`, `*.pem`, `*.key`) |
| `preToolUse` | `check-policy.py` | Blocks `requires_approval` (exit 2) and `denied` (exit 1) write/delete actions |
| `beforeShellExecution` | `check-policy.py` | Policy check for all shell commands — use instead of `preToolUse` for newer Cursor |
| `beforeMCPExecution` | `check-policy.py` | Same check for MCP tool calls |
| `afterFileEdit` | `log-trace-span.py` | Appends JSONL span for file modifications |
| `beforeSubmitPrompt` | `check-policy.py` | Final policy advisory before prompt submission |
| `postToolUse` | `log-trace-span.py` | Appends JSONL span to `core/observability/spans/` |
| `stop` | `log-trace-span.py` | Flush trace on agent stop |
| `sessionEnd` | `log-trace-span.py` | Final trace flush on session close |

> **Enforcement note:** Hooks **block** agent actions via non-zero exit codes. `.mdc` rules only suggest — hooks enforce. Keep `check-policy.py` exit-code semantics: 0=allowed, 1=denied, 2=requires_approval.

### Environment variables used

| Variable | Default | Purpose |
|----------|---------|---------|
| `AGENT_SKILLS_ROOT` | auto-detected | Absolute path to this pack |
| `AGENT_ACTIVE_ROLE` | `agent-coordinator` | Current role slug for policy check |
| `AGENT_TRACE_ID` | `""` (auto UUID) | Trace correlation ID for span grouping |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | `genai` | Enable OTel GenAI semantic conventions |

---

## Kiro Setup

Kiro hooks live at `.kiro/hooks/*.json` and use Kiro's native hook format.

The pack ships 3 hooks under `.kiro/hooks/`:

| File | Trigger | Action |
|------|---------|--------|
| `role-gate.json` | `preTaskExecution` | Remind agent to load rules + role + policy before acting |
| `policy-check.json` | `preToolUse` (write, shell) | Run `check-policy.py` enforcement check |
| `trace-span.json` | `postToolUse` (*) | Append trace span JSONL |

```bash
# Copy to your project (or symlink):
mkdir -p /your-project/.kiro/hooks
cp /path/to/agent-skills/.kiro/hooks/*.json /your-project/.kiro/hooks/
# Edit AGENT_SKILLS_ROOT in policy-check.json and trace-span.json
```

Or use the Kiro Hook UI (`Open Kiro Hook UI` in command palette) to add individually.

---

## Policy enforcement logic

```
preToolUse / beforeMCPExecution
  │
  ├── check destructive_patterns (mcp-tool-map.yaml) by command substring
  ├── lookup tool name in tool_actions map
  └── fallback to keyword inference
        │
        ├── action in role.denied       → exit 1 (POLICY DENIED)
        ├── action in role.requires_approval → exit 2 (POLICY APPROVAL REQUIRED)
        └── action in role.allowed      → silent pass, exit 0
```

Script: `core/scripts/hooks/check-policy.py`
Policy: `core/policies/action-boundaries.yaml`
Tool map: `core/policies/mcp-tool-map.yaml`

---

## A2A + Antigravity + Claude

Cursor, Kiro, and Claude Code share the same pack contracts. For A2A registry and Antigravity-specific config, also use [`../antigravity/ANTIGRAVITY.md`](../antigravity/ANTIGRAVITY.md). For Claude Code setup, see [`../claude/CLAUDE_ADAPTER.md`](../claude/CLAUDE_ADAPTER.md).

```bash
# Antigravity quick setup:
mkdir -p .antigravity
cp adapters/antigravity/rules.template.md .antigravity/rules.md
cp adapters/antigravity/a2a-config.template.yaml .antigravity/a2a-config.yaml
python3 core/scripts/generate-a2a-registry.py
```

---

## Verify setup

```bash
# Run from the pack root so AGENT_SKILLS_ROOT resolves to it:
# Test check-policy.py directly:
AGENT_SKILLS_ROOT="$PWD" \
  AGENT_ACTIVE_ROLE=backend-developer \
  CURSOR_TOOL_NAME=write_file \
  python3 core/scripts/hooks/check-policy.py

# Test trace span:
AGENT_SKILLS_ROOT="$PWD" \
  AGENT_ACTIVE_ROLE=agent-coordinator \
  python3 core/scripts/hooks/log-trace-span.py

# Run full A2A compliance check:
python3 core/scripts/validate-a2a-compliance.py
```
