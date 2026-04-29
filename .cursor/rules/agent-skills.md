---
trigger: always_on
glob: "**"
description: "Global engineering rules from the agent-skills pack. Enforces commit safety, code standards, role/skill boundaries, and workflow execution discipline."
---

# Agent Skills — Global Engineering Rules

## Source of Truth

All rules originate from `rules/code.md`. This file is a Cursor-native mirror.

## Mandatory Constraints

- **META-RULE**: Before finalizing any response or executing a command, verify your action against `rules/code.md`. If any step violates a rule, halt and ask the user.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards over defaults when they exist.
- Do not invent repository conventions not present in the active codebase.
- Keep code comments implementation-focused, under 3 lines.

## Role & Skill Enforcement

Use `skills/agent/` for agent operating discipline such as context management, memory compaction, tool orchestration, quality gates, and handoff summaries.

When a Role is assigned:

1. Read `role/role-standard.md` first, then `role/<role-name>.md`.
2. **SKILL TOOLBOX LOCK**: Only use Primary Skills from your Skill Toolbox. Supporting Skills require collaboration context. Unlisted skills require explicit user permission.
3. **BOUNDARY LOCK**: Decline tasks outside your role's core responsibilities and recommend the appropriate role.

## Workflow Execution

When executing a workflow:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time, mark `[x]`, explain the result.
3. Respect the `Role:` tag on each step.
