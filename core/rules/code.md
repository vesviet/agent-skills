---
trigger: always_on
glob: "**"
description: "Minimal global rules for commit and publish approval, user-visible wording, and code comment hygiene."
---

# Rules

- **META-RULE**: Before finalizing any response or executing a command, verify the action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission.
- Do not create a commit unless the user explicitly confirms that specific commit action.
- Do not push commits, create tags, or publish releases unless the user explicitly confirms that specific action.
- Repo-local rules override these defaults when they are explicitly present.
- **POLICY-AS-CODE**: Obey `core/policies/action-boundaries.yaml` and `core/policies/data-classification.yaml` before executing any state-changing actions.
- Ensure all code changes pass local linters, unit tests, and build checks before creating a commit.
- Prefer repo-local standards, templates, and workflows when they exist.
- Do not invent repository conventions, paths, branching models, or release rules that are not present in the active codebase.
- Do not mention agents, AI workflow, review labels, severity labels, task trackers, or other internal process metadata in commit messages, changelog text, release notes, or other user-visible change notes.
- Do not expose secrets, credentials, tokens, private keys, or sensitive internal values in commits, comments, changelogs, release notes, or other user-visible artifacts.
- **NEVER commit `.dev.vars`, `.env`, or any other local environment files.** Always verify `git status` and ensure they are added to `.gitignore`.
- Prefer no comment over comments that merely restate the code.
- Keep code comments implementation-focused and useful.
- Do not mention agents, review labels, severity labels, or task trackers in code comments.
- Keep each code comment within 3 lines unless a longer comment is required for doc comments, file headers, or tooling directives.

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

Last updated: 2026-09-02
