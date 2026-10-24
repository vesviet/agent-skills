# Agent Skills - Global Engineering Rules (Kilo Code)

Kilo Code loads project instructions from `AGENTS.md` (the shared open standard) and from every file under `.kilocode/rules/`. This file is a Kilo-native mirror of `core/rules/code.md`; when it and the source disagree, the source wins.

## Mandatory Constraints

- **META-RULE**: Before finalizing any response or executing a command, verify your action against `core/rules/code.md`. If any step violates a rule, halt and ask the user.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- NEVER commit `.dev.vars`, `.env`, or other local environment files; verify `git status` and keep them in `.gitignore`.
- Repo-local rules override these defaults when they are explicitly present.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards over defaults when they exist.
- Do not invent repository conventions not present in the active codebase.
- Prefer no comment over comments that merely restate the code; keep each code comment implementation-focused and within 3 lines unless a longer doc comment, file header, or tooling directive is required.

## Role And Skill Enforcement

When a Role is assigned:

1. Read `core/roles/role-standard.md` first, then `core/roles/<role-name>.md`.
2. **SKILL TOOLBOX LOCK**: Only use Primary Skills from your Skill Toolbox. Supporting Skills require collaboration context. Unlisted skills require explicit user permission.
3. **BOUNDARY LOCK**: Decline tasks outside your role's core responsibilities and recommend the appropriate role.

## Workflow Execution

When executing a workflow:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time, mark `[x]`, explain the result.
3. Respect the `Role:` tag on each step.

## Policy-as-Code And A2A

- Policy: check `core/policies/action-boundaries.yaml` and `core/policies/data-classification.yaml` before any state-changing action; `core/policies/mcp-tool-map.yaml` maps tool names to policy actions.
- Configure Kilo Code MCP servers to expose pack tools; discovery via `core/a2a/.well-known/agent-registry.json`.
- Full A2A lifecycle via the `agent-a2a-protocol` skill; emit structured handoffs from `core/contracts/schemas/` — not prose-only for delivery artifacts.

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

Last updated: 2026-09-01
