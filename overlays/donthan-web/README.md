# Donthan Web Overlay

Project-specific conventions for **Donthan.com** — a web-first live-streaming platform with desktop-priority UX.

**Status:** Active (standalone — no stack overlay dependency)

## Scope

This overlay applies when working on the Donthan.com front-end. It overrides or extends `core/` defaults for:

- Layout architecture (web-first, no mobile-first bottom-nav patterns)
- UX conventions for desktop livestream interfaces
- Component and navigation patterns optimised for wide-viewport streaming layouts

## Rules

| Rule file | Applies to |
|---|---|
| [donthan-web-ux-conventions.md](rules/donthan-web-ux-conventions.md) | UI/UX Designer, Frontend Developer |

## Activation

Load this overlay when the active repository is `donthan-web` or when the user explicitly references Donthan.com UX work. No pack currently wraps this overlay — activate manually or create `packs/donthan-team/manifest.yaml` when a team pack is needed.

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
