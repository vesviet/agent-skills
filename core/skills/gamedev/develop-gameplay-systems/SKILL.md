---
name: develop-gameplay-systems
description: Build deterministic, high-performance gameplay systems, character controllers, state machines, and combat mechanics across game engines. Use when implementing player movement, mechanics, physics interactions, or game loops.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Develop Gameplay Systems

Implement modular, testable gameplay systems and character controllers that maintain deterministic simulation, clean component boundaries, and strict frame-rate independence.

## Core Rules

- **Fixed Timestep Determinism**: Always update physics, collision detection, and spatial queries inside fixed tick loops (`_physics_process` in Godot, `FixedUpdate` in Unity, sub-stepped ticks in Unreal/custom engines). Never bind movement speed directly to variable render delta times.
- **Hierarchical State Isolation**: Model player states (Idle, Run, Jump, Fall, Attack, Stunned) via explicit state machines. Transitions must be driven by verified inputs and conditions, never by ambient variable mutations.
- **Zero GC in Hot Loops**: Pre-allocate collision queries, raycast hit buffers, and vectors. Do not instantiate heap objects, closures, or temporary arrays inside update loops.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing gameplay system slices.

## Suggested Process

### 1. Frame Budget & Timestep Setup
Define target fixed tick rate ($60\text{Hz}$ or $120\text{Hz}$). Ensure kinematic velocity integration follows:
$$\vec{x}_{t+1} = \vec{x}_t + \vec{v}_t \cdot \Delta t_{\text{fixed}}$$
Apply gravity and terminal velocity limits consistently.

### 2. State Machine Assembly
Implement state interfaces with explicit `Enter()`, `Update(delta)`, `FixedUpdate(fixed_delta)`, and `Exit()` lifecycles. Ensure state transitions broadcast events rather than tightly coupling downstream components.

### 3. Spatial Query & Collision Layering
Configure distinct physics collision layers (Player, Enemies, WorldGeometry, Projectiles, Triggers). Use non-allocating raycasts (`PhysicsServer2D/3D`, `Physics.RaycastNonAlloc`) with layer masks to prevent unnecessary broadphase checks.

### 4. Headless Verification
Write unit tests for state transitions and math logic. Run tests via headless engine runner or test harness to verify zero state regressions.

## Output Contracts

When completing a gameplay system implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Movement and physics logic executes exclusively in fixed timestep functions
- [ ] Character controller handles slope limits, wall sliding, and ceiling bonks cleanly
- [ ] State machine enforces single-active-state invariants and validated transitions
- [ ] Collision matrix prevents unnecessary layer pair checks
- [ ] No allocations occur inside `Update` or `FixedUpdate` hot loops
- [ ] Headless test suite passes with zero exit errors

## Related Skills

- **tune-game-feel**: layered audiovisual responsiveness and timing buffers
- **integrate-game-engine**: engine lifecycle integration and headless runner execution
- **optimize-3d-assets**: mesh and texture budget conformance
