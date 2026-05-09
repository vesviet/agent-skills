# Agent Skills - Global Engineering Pack

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

## Mandatory Rules (Always-On)

Before ANY action, you MUST read and follow the rules in `core/rules/code.md`. Key constraints:

- **META-RULE**: Before finalizing any response or executing a command, verify the action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- Ensure all code changes pass local linters, tests, and build checks before committing.
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

## A2A Delegation & Contracts (v2.0)

When operating as an AI agent (like Antigravity) under this pack, you MUST:
1. **Output Structured JSON Contracts**: When completing a task or handing off to another role, output the exact JSON schema defined in `core/contracts/schemas/` (e.g., `feature-ticket.json`, `test-report.json`, `api-contract-spec.json`). Do not output raw markdown for these deliverables.
2. **Utilize A2A Delegation**: If a task requires a skill outside your current role's Toolbox, explicitly delegate the sub-task to the appropriate role using the `agent-delegation` workflow.
3. **Obey Policy-as-Code Boundaries**: You are strictly bound by `core/policies/action-boundaries.yaml`. Restricted actions (dropping DBs, deploying to prod) MUST be halted pending human override.

## Skills

Core skills are organized under `core/skills/` by taxonomy:

- `core/skills/agent/`
- `core/skills/foundation/`
- `core/skills/backend/`
- `core/skills/frontend/`
- `core/skills/platform/`
- `core/skills/security-data/`
- `core/skills/documentation/`

Optional repo-specific skills live under `overlays/` and should only be loaded when the active repository actually needs them.

## Workflows

When executing a workflow from `core/workflows/`, you MUST:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time.
3. Mark each step as `[x]` and explain the result before moving to the next.
4. Respect the `Role:` tag on each step - that role owns the step.

Available workflows: `core/workflows/README.md`

## Quick Reference

| Need | Go to |
|------|-------|
| Rules (always-on) | `core/rules/code.md` |
| Role standard | `core/roles/role-standard.md` |
| All roles | `core/roles/README.md` |
| All skills | `core/skills/README.md` |
| All workflows | `core/workflows/README.md` |
| Overlay index | `overlays/README.md` |
