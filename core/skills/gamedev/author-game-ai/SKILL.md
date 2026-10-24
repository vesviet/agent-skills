---
name: author-game-ai
description: Authors modular game AI architectures using Behavior Trees (BT), shared and local blackboards, Utility AI response curves, local steering behaviors, and time-sliced NavMesh or A* pathfinding budgets. Use when implementing NPC decision-making, combat squad tactics, crowd steering, or pathfinding agents.
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

# Author Game AI

Design and implement scalable, debuggable non-player character (NPC) intelligence combining Behavior Trees, Utility AI scoring, blackboard memory separation, local avoidance steering, and budgeted pathfinding.

## Core Rules

- **Strict Blackboard Decoupling**: Behavior Tree nodes and Utility AI evaluators must remain stateless definitions shared across agent instances. Store all per-agent state, sensory targets, and cooldown timestamps in typed Blackboard structures.
- **Time-Sliced Pathfinding & Perception Budgets**: Never allow dozens of AI agents to compute full `A*` or NavMesh paths or line-of-sight raycast sweeps on the same frame. Route requests through a budgeted scheduler capped at a fixed millisecond ceiling per tick.
- **Fairness & Telegraphing Readability**: Separate AI sensory perception from omniscient world state. Enforce reaction delays, vision cone checks, and explicit attack wind-up telegraphs so player encounters feel fair and readable.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing game AI implementations.

## Suggested Process

### 1. Blackboard & Sensory Perception Pipeline
Define individual and squad-level Blackboard schemas (`target_entity`, `last_known_position`, `alert_level`, `combat_role`). Update sensory stimuli (vision cones, spatial audio events, damage aggro) at throttled tick intervals ($5\text{--}10\text{Hz}$) rather than every render frame.

### 2. Behavior Tree & Utility AI Construction
Build hierarchical Behavior Trees (`Selector`, `Sequence`, `Parallel`, `Decorator`) returning deterministic `Success`, `Failure`, or `Running` states. Where tactical action selection requires continuous trade-offs, evaluate normalized Utility AI response curves ($U \in [0, 1]$) across distance, health, and threat factors.

### 3. Budgeted Pathfinding & Local Steering
Query `A*` grids or Navigation Meshes asynchronously via a central path queue. Combine macro path corridor following with local context steering or Reciprocal Velocity Obstacles (RVO) so agents navigate around dynamic obstacles without clumping.

### 4. Squad Coordination & Headless Simulation Testing
Implement squad token pools (e.g. limiting simultaneous melee attackers to $2$ tokens while remaining NPCs strafe or flank). Validate decision trees and pathfinding convergence using deterministic headless simulation tests.

## Output Contracts

When completing game AI implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Behavior Tree and Utility AI logic nodes are stateless and read/write state via Blackboards
- [ ] Pathfinding queries and sensory raycasts are throttled through a per-frame budget scheduler
- [ ] NPC perception respects vision cones, occlusion raycasts, and configurable reaction delays
- [ ] Local steering and RVO avoidance prevent agent overlapping and corridor deadlocks
- [ ] Squad combat token systems prevent unfair simultaneous enemy dogpiling
- [ ] Headless automated tests verify BT state transitions, utility scoring, and path resolution

## Related Skills

- **develop-gameplay-systems**: integrating AI movement intents with shared character controllers
- **configure-physics-collision**: executing non-allocating vision cone and obstacle raycasts
- **architect-ecs-systems**: batch-updating large AI crowds and boid steering in contiguous arrays
