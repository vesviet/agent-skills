# R3F Stack Overlay

React Three Fiber / Three.js / WebGL+WebGPU skill cluster. Provides 3D rendering skills for projects using the R3F ecosystem.

## Tech Stack (2026)

- **Three.js**: r171+ — `WebGPURenderer` production-ready with automatic WebGL 2 fallback
- **React Three Fiber**: **v9** — React 19 compatible; `state.gl` → `state.renderer`
- **@react-three/drei**: **v10** (v11 alpha) — `OrbitControls`, `Environment`, `useGLTF`, `useTexture` stable
- **WebGPU**: ✅ **Production-ready** — all major browsers (Chrome, Edge, Firefox, Safari)
- **TSL (Three Shader Language)**: Write shaders once → compiles to WGSL (WebGPU) + GLSL (WebGL)
- **Physics**: `@react-three/rapier v2` — R3F v9 + React 19 compatible
- **Postprocessing**: `@react-three/postprocessing` — TSL-based effects for WebGPU

## 2026: WebGPU Adoption Strategy

```jsx
// ✅ Zero-config WebGPU with automatic WebGL 2 fallback
import { Canvas } from '@react-three/fiber'
import { WebGPURenderer } from 'three/webgpu'

<Canvas
  gl={(canvas) => new WebGPURenderer({ canvas, antialias: true })}
>
  {/* Scene renders via WebGPU where available, WebGL 2 elsewhere */}
</Canvas>
```

Deploy WebGPU for all new projects — the built-in fallback ensures production safety across all browsers.

## R3F v9 Breaking Change

```jsx
// ❌ v8 pattern
const { gl } = useThree()  // WebGLRenderer

// ✅ v9 pattern
const { renderer } = useThree()  // unified WebGL/WebGPU renderer
```

## TSL Shader Language (Three.js r171+)

```js
import { positionLocal, vec4, sin, time } from 'three/tsl'

// Write once → WGSL (WebGPU) + GLSL (WebGL) compilation
const material = new MeshStandardNodeMaterial()
material.colorNode = vec4(sin(positionLocal.x.add(time)), 0.5, 0.8, 1.0)
```

## Skills

- `debug-3d-scene` — debug R3F/Three.js scene graph, rendering, WebGPU pipelines, Spector.js
- `integrate-r3f-three-legacy` — integrate legacy Three.js code with R3F idioms
- `optimize-3d-assets` — compress, decimate, and bundle 3D models for web delivery

## Consumers

- `core/roles/3d-graphics-engineer.md` — sole Primary owner of these skills
- `overlays/obj-configurator/` — Astro + R3F/Three.js product configurator
- Any future R3F/Three.js project overlay should declare `r3f-stack` as a stack dependency

## Migration History

- **v4.0.0**: Skills moved from `core/skills/frontend/<name>/` to `overlays/r3f-stack/skills/<name>/`.
  Core frontend taxonomy reduced from 8 to 5 skills.
  3d-graphics-engineer role toolbox paths now resolve via overlay.

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
