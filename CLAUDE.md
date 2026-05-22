# Agent Skills - Global Engineering Pack

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

## Mandatory Rules (Always-On)

Before ANY action, you MUST read and follow the rules in `core/rules/code.md`. Key constraints:

- **META-RULE**: Before finalizing any response or executing a command, verify the action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- Ensure all code changes pass local linters, unit tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards over defaults when they exist.

Full rules: `core/rules/code.md`

## Role System

When the user assigns you a Role, you MUST:

1. Read `core/roles/role-standard.md` first.
2. Read the specific role file from `core/roles/<role-name>.md`.
3. Follow the **SKILL TOOLBOX LOCK**: Only use Primary Skills listed in your role's Skill Toolbox. Supporting Skills require collaboration context. Skills outside the Toolbox require explicit user permission.
4. Follow the **BOUNDARY LOCK**: If a task falls outside your role's core responsibilities, politely decline and recommend the appropriate role.

Available roles: `core/roles/README.md`

## A2A 1.0 & Antigravity (v2.4)

When operating as an AI agent (including **Antigravity** or **Claude Code**) under this pack:

1. Read `adapters/antigravity/ANTIGRAVITY.md` when using Antigravity; use `core/a2a/.well-known/agent-registry.json` for discovery.
2. Output **structured JSON** from `core/contracts/schemas/` for handoffs.
3. Use **full A2A lifecycle** via `agent-a2a-protocol`: task, progress, status, artifact, cancel, optional push notifications.
4. **Delegate** with `agent-delegation` / `/agent-a2a-delegation` across role boundaries.
5. Obey **Policy-as-Code**: `action-boundaries.yaml` and `data-classification.yaml`; Cursor hooks optional via `adapters/cursor/hooks.template.json`.
6. Use **PromptOps** (`agent-prompt-lifecycle`) and **semantic memory** (`agent-semantic-memory`) when Coordinator or Technical Lead owns long-running work.

## Skills

Core skills live under `core/skills/`.
Overlay skills live under `overlays/`.

## Workflows

When executing a workflow from `core/workflows/`, you MUST:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time.
3. Mark each step as `[x]` and explain the result before moving to the next.
4. Respect the `Role:` tag on each step.

Available workflows: `core/workflows/README.md`

## Validation

```bash
python3 core/scripts/validate-all.py
python3 core/scripts/generate-a2a-registry.py
```

## Quick Reference

| Need | Go to |
|------|-------|
| Rules | `core/rules/code.md` |
| Antigravity | `adapters/antigravity/ANTIGRAVITY.md` |
| Cursor hooks | `adapters/cursor/README.md` |
| A2A registry | `core/a2a/.well-known/agent-registry.json` |
| Roles | `core/roles/README.md` |
| Skills | `core/skills/README.md` |
| Workflows | `core/workflows/README.md` |
