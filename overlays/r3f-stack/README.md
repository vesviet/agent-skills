# R3F Stack Overlay

React Three Fiber / Three.js / WebGL skill cluster. Migrated out of `core/skills/frontend/` in v4.0.0 per stack-overlay naming rules.

## Skills

- `debug-3d-scene` — debug R3F/Three.js scene graph and rendering issues
- `integrate-r3f-three-legacy` — integrate legacy Three.js code with R3F idioms
- `optimize-3d-assets` — compress, decimate, and bundle 3D models for web delivery

## Consumers

- `core/roles/3d-graphics-engineer.md` — sole Primary owner of these skills
- `overlays/obj-configurator/` — Astro + R3F/Three.js product configurator consumes this overlay as a stack dependency
- any future R3F/Three.js project overlay should declare `r3f-stack` as a stack dependency

## Migration (v4.0.0)

This overlay became live in v4.0.0:

1. Skills moved verbatim from `core/skills/frontend/<name>/` to `overlays/r3f-stack/skills/<name>/`.
2. Core frontend taxonomy reduced from 8 to 5 skills.
3. `3d-graphics-engineer` role toolbox paths now resolve via overlay; role semantics unchanged.

The naming rule that motivated this move: core skills must be stack-generic; these three explicitly name a stack (R3F/Three.js/WebGL).
