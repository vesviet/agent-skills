---
name: manage-scene-lifecycle
description: Orchestrate scene hierarchies, asynchronous level streaming, additive scene loading, and resource disposal lifecycles. Use when managing scene transitions, additive loading, VRAM cleanup, or dependency injection across scenes.
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

# Manage Scene Lifecycle

Architect and coordinate scene lifecycles, additive level streaming, transition animations, and explicit resource disposal across production game engines.

## Core Rules

- **Asynchronous Non-Blocking Streaming**: Never freeze the main render thread during scene transitions or asset loading. Load scenes in background threads or via asynchronous promises while displaying smooth transition feedback.
- **Explicit Lifecycle Hooks**: Enforce clean lifecycle callbacks for every scene and level chunk: `OnPreload()`, `OnInitialize()`, `OnActivate()`, `OnDeactivate()`, and `OnDisposed()`.
- **Zero VRAM/RAM Leaks**: Disconnect all signal observers, event listeners, and timers before unloading a scene. Force explicit disposal of orphan textures, meshes, and audio streams to prevent memory creep.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when implementing scene management systems.

## Suggested Process

### 1. Scene Coordinator Architecture
Create a root scene manager service decoupled from individual level nodes. Implement scene stacks for menus, HUD overlays, pause screens, and active gameplay levels.

### 2. Additive Level Streaming
Partition large worlds into spatial streaming volumes or grid chunks. Additively load adjacent chunks based on player camera bounding boxes and asynchronously unload distant sectors.

### 3. Transition & Pre-Warming Orchestration
Coordinate screen fades, loading screens, and shader pre-warming:
- Fade out screen and mute scene audio buses.
- Unload previous scene entities and invoke garbage collection during transition blackouts.
- Instantiate new scene hierarchy and await first draw before fading in.

### 4. Dependency Injection & Service Scoping
Pass runtime dependencies (player session, save data reference, audio manager) explicitly to loaded scenes via injection context rather than relying on global mutable singletons.

## Output Contracts

When completing scene lifecycle management, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Scene loading executes asynchronously without stalling the main render thread
- [ ] Additive level chunks load and unload cleanly based on player proximity
- [ ] All signals, event bus subscriptions, and timers disconnect upon scene unload
- [ ] Unused textures and mesh buffers are explicitly purged from GPU VRAM
- [ ] Dependencies are injected cleanly into newly instantiated scene root nodes
- [ ] Loading screen and transition animations maintain stable frame pacing

## Related Skills

- **integrate-game-engine**: engine project structure and asset importer presets
- **implement-save-persistence**: preserving persistent state across scene reloads
