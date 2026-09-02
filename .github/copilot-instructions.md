# Agent Skills - Global Engineering Pack

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

## Mandatory Rules

Before ANY action, follow these rules (source: `core/rules/code.md`):

- **META-RULE**: Before finalizing any response or executing a command, verify your action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- NEVER commit `.dev.vars`, `.env`, or other local environment files; verify `git status` and keep them in `.gitignore`.
- Repo-local rules override these defaults when they are explicitly present.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards, templates, and workflows when they exist.
- Do not invent repository conventions not present in the active codebase.
- Prefer no comment over comments that merely restate the code; keep each code comment implementation-focused and within 3 lines unless a longer doc comment, file header, or tooling directive is required.

## Role System

When a Role is assigned:

1. Read `core/roles/role-standard.md` first.
2. Read `core/roles/<role-name>.md` for the specific role.
3. Follow the **SKILL TOOLBOX LOCK**: Only use Primary Skills listed in the role's Skill Toolbox. Supporting Skills require collaboration context. Skills outside the Toolbox require explicit user permission.
4. Follow the **BOUNDARY LOCK**: If a task falls outside your role's core responsibilities, politely decline and recommend the appropriate role.

Roles index: `core/roles/README.md`

## Skills

Organized under `core/skills/` by taxonomy:

- `core/skills/agent/`
- `core/skills/foundation/`
- `core/skills/backend/`
- `core/skills/frontend/`
- `core/skills/platform/`
- `core/skills/commerce/`
- `core/skills/security-data/`
- `core/skills/documentation/`
- `core/skills/education/`

Overlay-specific skills live under `overlays/` and should be loaded only when the target repository needs them.

## Workflows

When executing a workflow from `core/workflows/`:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time.
3. Mark each step as `[x]` and explain the result before moving to the next.
4. Respect the `Role:` tag on each step.

Workflows index: `core/workflows/README.md`

## A2A 1.0 And Antigravity

- Agent registry: `core/a2a/.well-known/agent-registry.json`
- Protocol skill: `agent-a2a-protocol`
- Antigravity adapter: `adapters/antigravity/ANTIGRAVITY.md`
- Emit JSON contracts from `core/contracts/schemas/` for cross-role handoffs
- Policy: `core/policies/action-boundaries.yaml`, `core/policies/data-classification.yaml`

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
