# Prompts

This directory stores versioned prompt assets used by the `agent-prompt-lifecycle` skill (PromptOps).

## Layout

```
prompts/
  README.md
  golden/              # Evaluation fixtures for promoted prompt assets
    README.md
    <prompt-asset-id>/
      manifest.yaml    # version, role, skill, eval threshold
      cases/
        001-input.json    # input context for the eval case
        001-expected.json # expected behavior rubric (not exact match)
```

## Current Prompt Assets

| Asset ID | Role | Version | Min Pass Rate | Cases |
|----------|------|---------|---------------|-------|
| [agent-coordinator-phase-gate](golden/agent-coordinator-phase-gate/manifest.yaml) | `agent-coordinator` | 1.0.0 | 90% | 18 |

## How To Use

1. When you add or modify a prompt asset, create a subdirectory under `golden/` with a `manifest.yaml` and at least one `cases/` pair.
2. Run evaluation before promoting (see `agent-prompt-lifecycle` skill checklist).
3. Never store secrets or production customer data in case files.
4. Use rubric-based expected output — not brittle exact-string match.

Full authoring rules: `golden/README.md`

## Related Skill

- `agent-prompt-lifecycle` — `core/skills/agent/agent-prompt-lifecycle/SKILL.md`

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
