---
name: program-game-shaders
description: Author high-performance vertex and fragment shaders across GLSL, HLSL, and Godot Shader Language for UV distortion, dissolve, outlines, and depth effects. Use when programming custom game materials, screen-space post-processing, or GPU visual effects.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Program Game Shaders

Author deterministic, GPU-friendly vertex and fragment shaders across GLSL, HLSL, and engine shader graphs while preventing warp divergence and fragment overdraw.

## Core Rules

- **Branchless ALU Operations**: Eliminate dynamic `if/else` branching inside fragment shaders where condition variables vary per pixel. Use hardware intrinsics (`step()`, `smoothstep()`, `mix()` / `lerp()`, `clamp()`) to preserve GPU SIMD wave occupancy.
- **Precision & Coordinate Discipline**: Declare explicit precision qualifiers (`highp` for world/UV coordinates, `mediump` or `half` for color/normals on mobile). Explicitly document coordinate space transitions (Object, World, View, Clip, Screen, Tangent).
- **Overdraw & Depth Preservation**: Avoid discarding fragments (`discard` / `clip()`) in opaque passes when alpha blending or early-Z rejection can be preserved, as pixel discards disable hardware Early-Z optimizations on tile-based mobile GPUs.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing shader and material pipeline implementations.

## Suggested Process

### 1. Coordinate Space & Vertex Displacement
Perform geometric deformations (foliage wind sway, wave displacement, billboarding) in the vertex shader rather than per-pixel when mesh tessellation is sufficient:
- Transform vertices from local space to world space, apply periodic displacement offsets, and project back to clip space.
- Recompute or approximate perturbed vertex normals for accurate downstream lighting.

### 2. UV Distortion & Dissolve Surface Effects
Construct branchless surface manipulation in the fragment stage:
- **UV Panning & Distortion**: Sample a seamless flow or noise texture (`vec2 distortion = (texture(u_noise, v_uv + TIME * u_speed).rg * 2.0 - 1.0) * u_strength`) and offset base UV coordinates.
- **Edge-Lit Dissolve**: Compare noise luminance against a normalized dissolve threshold using `smoothstep()` to blend an HDR emissive edge ramp before alpha clipping.

### 3. Outline & Depth Buffer Manipulation
Implement crisp silhouettes and intersection effects:
- **Inverted-Hull Outlines**: Extrude back-facing vertices along smoothed vertex normals in a secondary pass (`pos.xyz += normal * u_outline_width`).
- **Depth-Intersection Foam / Shields**: Linearize hardware depth buffer samples and compare against fragment eye depth (`abs(scene_depth - frag_depth)`) to render soft particles and contact highlights.

### 4. Shader Pre-Warming & Variant Stripping
Register active shader variants in a startup pre-warm manifest to compile PSOs (Pipeline State Objects) during loading screens, eliminating first-frame shader compilation stutter.

## Output Contracts

When completing game shader programming, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Fragment shaders avoid divergent dynamic branching in favour of `step()`, `smoothstep()`, and `mix()`
- [ ] Coordinate spaces (Object, World, View, Clip, Tangent) are explicitly transformed without matrix mismatches
- [ ] Depth buffer linearization matches the target graphics API clip-space convention ($[0, 1]$ vs $[-1, 1]$)
- [ ] Alpha clip and discard operations are isolated to dedicated alpha-test render queues
- [ ] Uniform buffers and material parameters expose clear min/max range hints for artists
- [ ] Shader variants are pre-warmed to prevent runtime PSO compilation hitches

## Related Skills

- **render-webgl-threejs**: custom GLSL shader material integration and post-processing passes
- **profile-game-performance**: GPU fragment overdraw and shader instruction profiling
