---
name: optimize-3d-assets
description: Optimize 3D assets and rendering inputs by reviewing model formats, geometry density, texture memory, material strategy, compression, and loading behavior. Use when a 3D web experience suffers from heavy OBJ/GLTF assets, texture bloat, long load times, frame drops, or unnecessary GPU and memory pressure.
---

# Optimize 3D Assets

Use this skill when the main problem is not scene logic alone, but the cost or quality of the 3D assets flowing into the runtime.

## Core Rules

- optimize the biggest asset bottlenecks first instead of micro-tuning unrelated code
- measure format, memory, and loading assumptions before reducing quality
- prefer stable, production-safe asset improvements over ad hoc runtime hacks
- make visual trade-offs explicit before lowering fidelity
- check downstream effects on materials, decals, UVs, and interaction anchors when assets change

## Suggested Process

### 1. Identify The Asset Bottleneck

Clarify whether the pressure comes from:

- raw model format such as OBJ instead of GLB/GLTF
- excessive polycount or duplicated geometry
- large diffuse/normal/roughness textures
- too many material instances or draw calls
- slow decode, parse, or network load path

### 2. Inspect Current Asset Strategy

Review:

- file formats in use
- texture resolutions and counts
- material model and normal-map usage
- compression or lack of compression
- whether asset loading matches target device constraints

### 3. Choose The Right Optimization Path

Prefer the narrowest useful improvement:

- convert OBJ to GLB/GLTF when runtime and pipeline support it
- reduce texture size or format cost
- consolidate materials when visually acceptable
- remove unnecessary geometry detail or hidden parts
- add LOD or simplified mobile variants when required

### 4. Check Runtime Assumptions

Verify:

- texture flip and color-space expectations
- normals, UVs, and decal targets remain valid
- material replacement will not break shading or overlays
- camera fit and interaction anchors survive asset changes

### 5. Produce A Safe Optimization Summary

Leave behind:

- what was heavy
- what changed
- what visual trade-offs were accepted
- what scenes or devices need re-checking

## Output Format

```markdown
# <Asset or Scene> - 3D Asset Optimization Brief

## Current Cost
- Asset type and format:
- Main bottleneck:
- Target devices or budgets:

## Optimization Plan
- Geometry changes:
- Texture or material changes:
- Format / compression changes:
- Runtime assumptions to preserve:

## Impact Review
- Visual trade-offs:
- Scenes / decals / materials to re-check:
- Mobile or low-end GPU considerations:

## Verification
- Load-time or memory expectations:
- Frame-rate expectations:
- Residual risk:
```

## Checklist

- [ ] main asset bottleneck identified
- [ ] current format and memory strategy inspected
- [ ] narrowest useful optimization path chosen
- [ ] runtime assumptions and visual constraints preserved
- [ ] impacted scenes or overlays identified
- [ ] verification expectations and residual risk captured

## Related Skills

- **debug-3d-scene**: Diagnose scene issues when the bottleneck is not purely asset weight
- **navigate-service**: Locate asset-loading and material-wiring code paths
- **frontend-testing**: Re-check UI and interaction behavior after asset changes
- **review-code**: Review material, loader, or runtime trade-offs
- **troubleshoot-service**: Investigate delivery or environment issues affecting asset loading
