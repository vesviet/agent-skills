# UI Design System Overlay

Composable overlay for the `ui-ux-designer` role when work must follow a **brand or project design system** in addition to core UX rules.

This overlay does not replace `core/roles/ui-ux-designer.md`. Compose it with core and any project overlay (for example overlays/maydiengiaisaigon for Elomus e-commerce).

## Scope

- Flow vs component deliverable conventions
- When to emit ux-flow-spec.json vs ui-component-spec.json
- Pointer to project-specific palette, typography, and component patterns

## Included

- `rules/handoff-conventions.md` — Contract layering and Frontend handoff order

## Activation

```
Role: ui-ux-designer
Overlay: overlays/ui-design-system
```

Add a **project** design overlay when one exists:

```
Overlay: overlays/maydiengiaisaigon
```

Read that project's rules/elomus-design-system.md (or equivalent) before finalizing visual and interaction specs.

## Project Design Overlays (examples)

| Overlay | Use when |
| ------- | -------- |
| overlays/maydiengiaisaigon | Máy Điện Giải Sài Gòn / Elomus Laravel storefront |
| (repo-local rules) | Any app with documented tokens in overlays/ or docs/ |

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
