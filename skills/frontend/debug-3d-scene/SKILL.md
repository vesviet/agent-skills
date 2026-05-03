---
name: debug-3d-scene
description: Debug 3D scene behavior by tracing scene graph structure, transforms, raycasting, decals, materials, camera logic, render loops, and WebGL lifecycle issues. Use when a Three.js, React Three Fiber, WebGL, or WebGPU scene has rendering bugs, interaction bugs, clipping problems, context instability, or suspicious visual math.
---

# Debug 3D Scene

Use this skill when a 3D experience behaves incorrectly and the fix depends on understanding scene state, transforms, asset wiring, or render lifecycle rather than only surface UI symptoms.

## Core Rules

- capture the exact 3D symptom before changing code
- verify coordinate systems, transforms, and scene hierarchy instead of trusting visual intuition
- isolate whether the bug lives in assets, scene graph, interaction math, materials, or lifecycle
- treat shared materials, shaders, merged geometry, and reused interaction hooks as blast-radius multipliers
- verify the original issue and nearby scene regressions before closing the fix

## Suggested Process

### 1. Define The 3D Failure

Clarify:

- what the user sees versus what is expected
- whether the issue is visual, interactive, performance-related, or lifecycle-related
- which scene, model, decal, material, camera path, or device profile is affected
- what behavior must stay stable while fixing it

### 2. Classify The Failure Layer

Decide where the failure most likely lives:

- scene graph or parent-child transform logic
- mesh geometry, normals, UVs, or winding
- material, texture, shader, or decal projection logic
- camera, controls, frustum, or clipping setup
- pointer interaction, raycasting, drag logic, or DOM-to-canvas bridge
- loading lifecycle, async race, disposal, or WebGL context behavior

### 3. Trace The Real 3D State

Inspect only what matters:

- object hierarchy and local vs world transforms
- scale, rotation, quaternion, and matrix conversion paths
- material reuse, texture assignment, and shader assumptions
- render loop subscriptions and camera/control updates
- asset format differences such as OBJ vs GLTF/GLB

### 4. Check Shared-Risk Areas

Look for common 3D regression sources:

- reused materials or shaders
- merged geometry or portal-based decal projection
- texture flip, color space, or normal map conventions
- mirrored geometry, negative scale, or winding order
- event listener leaks, RAF duplication, or missing disposal

### 5. Form And Test A Narrow Hypothesis

Test one likely cause at a time:

- wrong local/world-space conversion
- incorrect mesh target for decal or raycast
- stale texture/material instance
- asset orientation or scale mismatch
- missed cleanup or duplicate render/update path

### 6. Verify The Fix

Re-check:

- original bug path
- nearby models or scenes using the same logic
- mobile or low-end GPU behavior if relevant
- memory or context stability if lifecycle changed

## Output Format

```markdown
# <Issue> - 3D Scene Debug Brief

## Symptom
- Expected behavior:
- Actual behavior:
- Affected scene / model / interaction:

## Failure Layer
- Suspected layer:
- Preserved behavior:

## Evidence
- Relevant files or systems:
- Transform / material / interaction observations:
- Shared-risk areas:

## Hypothesis
- Most likely root cause:
- Why:

## Verification
- Original issue re-checked:
- Nearby regressions re-checked:
- Residual risk:
```

## Checklist

- [ ] exact 3D symptom captured
- [ ] likely failure layer classified
- [ ] real scene state inspected
- [ ] shared-risk areas checked
- [ ] narrow hypothesis tested
- [ ] original issue and nearby regressions re-checked

## Related Skills

- **optimize-3d-assets**: Improve source assets when geometry or texture quality is the real problem
- **troubleshoot-service**: Debug non-graphics runtime or integration issues around the scene
- **frontend-testing**: Add regression checks around interaction-sensitive fixes
- **review-code**: Review risky transform, shader, or lifecycle changes
- **navigate-service**: Map the 3D code path before debugging
