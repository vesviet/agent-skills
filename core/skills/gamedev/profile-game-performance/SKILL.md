---
name: profile-game-performance
description: Profile and optimize CPU/GPU frame budgets, eliminate garbage collection stalls, batch draw calls, manage LODs, and audit VRAM footprints. Use when diagnosing frame drops, stutter, high draw calls, or memory leaks in game engines.
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

# Profile Game Performance

Systematically diagnose CPU simulation bottlenecks, GPU rendering stalls, garbage collection frame spikes, and VRAM leaks to certify strict frame-time budgets ($16.6\text{ms}$ for $60\text{FPS}$, $8.3\text{ms}$ for $120\text{FPS}$).

## Core Rules

- **Measure Before Optimizing**: Capture baseline P50, P95, and P99 frame times, draw call counts, physics step duration, and RAM/VRAM allocations before altering code or assets.
- **Zero Per-Frame Heap Allocations**: Eliminate temporary object allocations, string concatenations, LINQ/array closures, and unpooled instantiations inside `_process`, `_physics_process`, or `Update` loops to keep GC pauses at $0\text{ms}$.
- **Draw Call & Overdraw Ceilings**: Consolidate materials, enable GPU instancing / static batching, and enforce hierarchical Level of Detail (LOD) and frustum/occlusion culling to respect platform draw call budgets.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` (and `contracts/schemas/performance-audit.json` when certifying performance gates).

## Suggested Process

### 1. Frame Time Breakdown (CPU vs. GPU Bound)
Isolate the primary bottleneck using engine profilers, RenderDoc, or Tracy:
- **CPU Game/Physics Bound**: High script update time, excessive broadphase collision pairs, or unthrottled AI pathfinding ticks.
- **CPU Render-Thread Bound**: Excessive draw calls ($> 250$ mobile, $> 2000$ desktop) or frequent material/shader state switches.
- **GPU Bound**: High fragment overdraw from stacked transparent particles, unoptimized post-processing passes, or excessive shadow-caster cascades.

### 2. Memory & Garbage Collection Elimination
Audit heap allocation callstacks during worst-case combat or streaming scenarios:
- Replace runtime `Instantiate`/`Destroy` or `queue_free` spikes with pre-warmed object pools and static ring buffers for raycast hits and spatial queries.

### 3. Draw Call Batching & Mesh LOD Configuration
Configure 3-to-4 discrete mesh LOD tiers (`LOD0` $100\%$, `LOD1` $50\%$, `LOD2` $25\%$, `LOD3` impostor/culled) based on screen-space coverage height, and merge static environment meshes sharing materials.

### 4. Automated Benchmark Regression Verification
Run a deterministic headless or fixed-camera benchmark flythrough scene that records frame-time percentiles and fails CI if P99 frame time regresses beyond threshold.

## Output Contracts

When completing game performance profiling and optimization, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Frame-time P95 and P99 metrics meet target platform budget ($16.6\text{ms}$ for $60\text{FPS}$ or $8.3\text{ms}$ for $120\text{FPS}$)
- [ ] Hot update and physics loops record zero recurring heap allocations or GC spikes
- [ ] Static batching, GPU instancing, and texture atlases keep draw calls within platform ceilings
- [ ] 3D meshes and terrain chunks configure distance/screen-size LOD transitions and culling
- [ ] Transparent particle overdraw and real-time shadow casters are bounded and profiled
- [ ] Before/after telemetry metrics are recorded in the implementation handoff

## Related Skills

- **architect-ecs-systems**: data-oriented cache locality and zero-allocation entity queries
- **program-game-shaders**: GPU overdraw reduction and shader complexity optimization
