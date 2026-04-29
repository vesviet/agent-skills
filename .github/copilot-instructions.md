# Agent Skills — Global Engineering Pack

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

## Mandatory Rules

Before ANY action, follow these rules (source: `rules/code.md`):

- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards, templates, and workflows when they exist.
- Do not invent repository conventions not present in the active codebase.
- Keep code comments implementation-focused, under 3 lines, and avoid restating the code.

## Role System

When a Role is assigned:

1. Read `role/role-standard.md` first.
2. Read `role/<role-name>.md` for the specific role.
3. Only use skills listed in the role's **Skill Toolbox** (Primary Skills for direct use, Supporting Skills for collaboration).
4. Decline tasks outside the role's core responsibilities and recommend the correct role.

Roles index: `role/README.md`

## Skills

Organized under `skills/` by taxonomy:

- `skills/agent/` — context management, memory compaction, tool orchestration, quality gates, handoff
- `skills/foundation/` — commit, review, test, navigate, troubleshoot
- `skills/backend/` — API, events, integrations, scaffolding
- `skills/frontend/` — UI, pages, API client, testing
- `skills/platform/` — deployment, runtime debug, telemetry
- `skills/security-data/` — secrets, database, security audit
- `skills/documentation/` — docs, tech radar

Each skill has a `SKILL.md`. Read it before executing.

## Workflows

When executing a workflow from `workflows/`:

1. Output a checklist for all steps.
2. Process one step at a time, mark complete, explain result.
3. Respect the `Role:` tag on each step.

Workflows index: `workflows/README.md`
