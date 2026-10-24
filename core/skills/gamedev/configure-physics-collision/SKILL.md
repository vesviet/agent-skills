---
name: configure-physics-collision
description: Configures deterministic fixed timestep tuning, Continuous Collision Detection (CCD), spatial query layers, kinematic substepping, raycasting, and contact normal stabilization. Use when tuning physics engines, resolving fast-mover tunneling, setting collision matrices, or stabilizing character ground contacts.
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

# Configure Physics Collision

Configure and optimize 2D and 3D physics simulation pipelines, collision matrices, Continuous Collision Detection (CCD), and spatial query routines for deterministic, jitter-free gameplay.

## Core Rules

- **Fixed Timestep & Substepping Discipline**: Lock physics solver ticks to a deterministic interval ($60\text{Hz}$ or $120\text{Hz}$) with bounded kinematic substepping. Render frames must interpolate visual transforms between previous and current physics ticks rather than advancing physics on variable delta times.
- **Sparse Collision Matrix Layering**: Explicitly assign bitmask layers (e.g. `Player`, `Enemy`, `WorldStatic`, `Projectile`, `Trigger`, `Hitbox`) and disable non-interacting layer pairs in the broadphase matrix to minimize sweep-and-prune overhead.
- **CCD for High-Velocity Bodies**: Enable swept-sphere or speculative Continuous Collision Detection (CCD) on projectiles and high-speed actors whose per-tick displacement exceeds half their collider radius.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing physics and collision configurations.

## Suggested Process

### 1. Timestep, Solver Iterations & Substepping Setup
Configure the physics world tick rate ($\Delta t_{\text{fixed}} = 16.66\text{ms}$ or $8.33\text{ms}$), velocity/position solver iteration counts, and maximum allowed substeps per frame to prevent spiral-of-death freezes during CPU spikes.

### 2. Broadphase Collision Matrix & Collider Topology
Define named collision layers and masks in version-controlled project settings. Replace complex concave triangle meshes on dynamic bodies with compound primitive colliders (capsules, boxes, spheres, or convex hulls) to guarantee stable manifold generation.

### 3. Raycasting, ShapeCasts & Contact Normal Stabilization
Use pre-allocated, non-allocating spatial queries (`RaycastNonAlloc`, `PhysicsDirectSpaceState`) filtered by explicit layer masks:
- Filter contact normals by floor angle threshold ($\theta \le \theta_{\text{max\_slope}}$) to distinguish walkable ground from steep walls.
- Apply snap-to-ground rays and depenetration skin widths to eliminate seam catching on tiled or modular geometry.

### 4. CCD & Headless Tunneling Verification
Configure speculative or swept CCD on fast-moving bodies. Execute automated headless physics tests firing high-velocity colliders against thin geometry barriers to verify zero tunneling and consistent contact impulse resolution.

## Output Contracts

When completing physics and collision configuration, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Physics tick rate and solver substep limits are locked to deterministic fixed intervals
- [ ] Broadphase collision matrix explicitly disables unneeded layer-pair evaluations
- [ ] High-velocity projectiles and actors use Continuous Collision Detection (CCD) without tunneling
- [ ] Raycasts and shape casts use zero-allocation buffers and explicit bitmask filters
- [ ] Kinematic contact normals stabilize slope walking, step-up snapping, and internal mesh seams
- [ ] Headless test suite validates collision responses and zero-tunneling invariants

## Related Skills

- **develop-gameplay-systems**: kinematic character controllers and fixed-tick movement loops
- **architect-ecs-systems**: batching spatial queries across contiguous component buffers
- **profile-game-performance**: profiling physics broadphase and solver frame budgets
