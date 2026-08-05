# R3F Stack Overlay

Reserved namespace for the React Three Fiber / Three.js skill cluster scheduled to migrate out of `core/skills/frontend/` at the next major version (v4.0.0).

## Status

**Stub (3.5.0+).** Skills still live in core:

- `core/skills/frontend/debug-3d-scene/`
- `core/skills/frontend/integrate-r3f-three-legacy/`
- `core/skills/frontend/optimize-3d-assets/`

Do not start new skills here until the v4.0.0 migration executes.

## Why This Overlay Exists

Core skill naming rules prefer generic names over stack-specific names. The three skills above name a specific stack (R3F, Three.js, WebGL) and are better modeled as a stack overlay per `core/skills/README.md` → "Move stack-specific or org-specific variants into overlays when they are not portable".

## Migration Checklist (for v4.0.0)

When this overlay becomes live, the migration must:

1. Move the three skill folders verbatim into `overlays/r3f-stack/skills/<skill-name>/`.
2. Update the `3d-graphics-engineer` role toolbox to reference the new paths.
3. Update `overlays/obj-configurator/skills/develop-obj-feature/SKILL.md` references.
4. Update `core/skills/README.md` counts (94 core → 91 core, 7 overlay → 10 overlay).
5. Update `core/a2a/registry/3d-graphics-engineer.agent-card.json`.
6. Bump `VERSION` to 4.0.0 and regenerate the A2A registry.
7. Run `python3 core/scripts/validate-all.py` end-to-end.

## Consumers

- `overlays/obj-configurator/` — OBJ 3D Configurator (Astro + R3F/Three.js) will declare this as a stack dependency in v4.0.0.
- Any future R3F/Three.js project overlay should declare `r3f-stack` as a stack dependency.
