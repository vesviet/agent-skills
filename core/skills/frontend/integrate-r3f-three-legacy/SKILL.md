---
name: integrate-r3f-three-legacy
description: Integrate or migrate between React Three Fiber and legacy imperative Three.js code by controlling scene ownership, render loops, loaders, interaction state, and cleanup boundaries. Use when a 3D web app mixes R3F with older Three.js modules, global bridge state, or imperative scene utilities and needs safe coexistence or staged migration.
---

# Integrate R3F Three Legacy

Use this skill when a 3D frontend mixes React Three Fiber with older imperative Three.js code and the real work is defining safe boundaries between the two systems rather than only fixing one component in isolation.

## Core Rules

- define one clear owner for render loop, scene mutation, and disposal in each code path
- do not let legacy globals and React state mutate the same 3D objects without an explicit contract
- treat loaders, materials, controls, and decal logic as shared-risk areas when bridging old and new systems
- preserve current interaction behavior while reducing architectural overlap
- verify migration or bridge changes against nearby flows, not only the target scene

## Suggested Process

### 1. Map The Split Architecture

Identify:

- which files own the R3F canvas, scene, controls, and event flow
- which files still mutate Three.js objects imperatively
- what global stores, callbacks, or bridge objects connect UI and 3D state
- which behaviors must remain stable during the change

### 2. Classify The Boundary Problem

Decide what kind of mixed-system issue exists:

- duplicate scene ownership
- duplicate render/update loops
- state split across Redux, Zustand, globals, and object instances
- legacy utilities mutating meshes that R3F also manages
- loader/material/decal logic duplicated in both systems

### 3. Define Safe Ownership

For each concern, assign one owner:

- scene and camera ownership
- controls ownership
- model loading ownership
- material and texture mutation ownership
- interaction and raycast ownership
- cleanup and disposal ownership

### 4. Choose The Bridge Strategy

Use the smallest safe approach:

- **coexistence** when legacy code must remain temporarily but boundaries can be tightened
- **adapter layer** when legacy modules should be wrapped behind React-safe APIs
- **staged migration** when imperative scene logic should move gradually into hooks or components

### 5. Check High-Risk Shared Paths

Review:

- texture and material replacement logic
- decals, text rendering, and merged geometry helpers
- loaders that behave differently for OBJ versus GLTF/GLB
- event listeners, drag/drop handlers, and control enable/disable logic
- teardown for geometries, materials, textures, listeners, and cached assets

### 6. Verify Stability

Re-check:

- original bug or migration target
- adjacent tools using the same bridge state
- product switching, undo/redo, share/reload, or restore flows
- memory growth and duplicate listener/render-loop risk

## Output Format

```markdown
# <Change> - R3F Legacy Integration Brief

## Architecture Split
- R3F-owned areas:
- Legacy-owned areas:
- Shared bridge state:
- Preserved behavior:

## Boundary Risks
- Duplicate ownership:
- Shared mutable objects:
- Lifecycle or cleanup risks:
- Asset or material pipeline overlap:

## Integration Strategy
- Chosen approach:
- Why this approach is safer:
- What remains legacy for now:

## Verification
- Original issue or migration target checked:
- Adjacent flows re-checked:
- Memory / listener / render-loop checks:
- Residual risk:
```

## Checklist

- [ ] R3F and legacy ownership boundaries mapped
- [ ] duplicate ownership or mutation paths identified
- [ ] bridge strategy chosen explicitly
- [ ] shared-risk paths checked
- [ ] cleanup responsibility verified
- [ ] original path and nearby regressions re-checked

## Related Skills

- **debug-3d-scene**: Trace transform, decal, lifecycle, and interaction bugs inside mixed 3D systems
- **optimize-3d-assets**: Reduce asset and texture cost when migration work exposes pipeline inefficiencies
- **navigate-service**: Map the 3D codebase before choosing ownership boundaries
- **frontend-testing**: Add regression coverage around bridge-sensitive interactions
- **review-code**: Review risky lifecycle, ownership, and cleanup changes
