# CAD Projection Overlay

Composable overlay for the `3d-graphics-engineer` role when generating precision engineering line art, CAD drawings, orthographic cross-sections, and isometric vector diagrams.

This overlay establishes mechanical drafting standards, SVG millimeter coordinate systems, and 3D-to-2D isometric projection matrix mathematics.

## Scope

- Scale-accurate SVG engineering drawing generation ($1\text{ unit} = 1\text{ mm}$)
- Landscape A3 ($420 \times 297\text{mm}$) sheet framing, margins, and title band grammar
- ISO 128 / ISO 5456 4-tier drafting stroke weight hierarchy ($0.35, 0.22, 0.16, 0.13\text{mm}$)
- Isometric transformation matrix projection ($\pm 30^\circ$ axes) and ellipse conjugate calculation
- Exploded assembly line drawings, hidden edge dashes, and dimension leader lines

## Included

- `rules/cad-conventions.md` — Strict drafting rules for SVG scale, line weights, and isometric axes
- `skills/isometric-svg-projection/SKILL.md` — Precision isometric vector projection skill

## Activation

```
Role: 3d-graphics-engineer
Overlay: overlays/cad-projection
```

Compose with `overlays/ui-design-system` or `overlays/r3f-stack` when technical drawings embed into web interfaces or 3D configurator workflows.

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

Last updated: 2026-10-15
