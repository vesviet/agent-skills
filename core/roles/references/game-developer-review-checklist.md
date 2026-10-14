## Game Developer Review Checklist

This reference checklist provides operational verification gates and quantitative benchmarks for real-time gameplay engineering, character physics, state isolation, input responsiveness, technical art pipelines, dynamic audio, and engine publishing to meet SOTA 2026–2027 standards. It organizes quality gates across 5 core pillars corresponding to the 20 standardized skills and enforces the 4 non-negotiable domain architectural locks.

---

### Pillar 1: Core Architecture & Engine Lifecycles
*Enforces `GAME-LOOP-TIMESTEP-LOCK` and `STATE-MACHINE-ISOLATION-LOCK`*  
*Skills covered: `integrate-game-engine`, `develop-gameplay-systems`, `architect-ecs-systems`, `manage-scene-lifecycle`, `implement-save-persistence`*

- [ ] **Fixed Timestep Determinism (`GAME-LOOP-TIMESTEP-LOCK`)**:
  - All kinematic motion, rigid-body impulses, gravity integration, and collision raycasts execute strictly within fixed update loops (`_physics_process` in Godot, `FixedUpdate` in Unity, fixed sub-stepped ticks in Unreal/custom engines).
  - Variable render delta time (`delta` from render `_process` or `Update`) is prohibited from modifying physical positions, velocities, or collision shapes.
  - Visual smoothing across variable refresh rates ($60\text{Hz}$, $120\text{Hz}$, $144\text{Hz}$, $240\text{Hz}$) is achieved via transform interpolation/extrapolation buffers.
- [ ] **Hierarchical State Machine Isolation (`STATE-MACHINE-ISOLATION-LOCK`)**:
  - Gameplay modes (Title, Gameplay, Inventory, Dialogue, Cutscene, Paused) and actor states (Idle, Run, Jump, Fall, Attack, Stagger) are isolated in explicit state machines with validated transition guards.
  - Direct ambient variable mutation across states is strictly prohibited; state changes emit decoupled event bus signals.
  - Modal overlay states (pause menu, dialogue box, skill wheel) use push/pop state stacks without resetting underlying physics simulation.
- [ ] **Data-Oriented ECS Architecture (`architect-ecs-systems`)**:
  - Entities and components adhere to Structure of Arrays (SoA) layout for CPU cache locality; hot iteration queries avoid pointer chasing.
  - Archetypes and sparse sets minimize memory fragmentation during high-throughput entity creation and despawning.
- [ ] **Additive Scene & Lifecycle Management (`manage-scene-lifecycle`)**:
  - Level transitions and open-world chunks stream additively and asynchronously without blocking the main render thread.
  - Unloaded scenes, materials, audio stems, and GPU buffers explicitly register unloader hooks and flush references to eliminate VRAM leaks.
- [ ] **Atomic Save State Persistence (`implement-save-persistence`)**:
  - Save game serialization (JSON, Binary, MessagePack) writes to temporary files before atomic file rename to prevent corrupted save states on abrupt power loss.
  - Save data includes semver schema headers, automated forward migrations, and cryptographic HMAC/checksum validation to detect tampering.

---

### Pillar 2: Game Feel, Physics & Interaction
*Enforces `INPUT-ACTION-ABSTRACTION-LOCK`*  
*Skills covered: `tune-game-feel`, `configure-physics-collision`, `abstract-input-actions`, `direct-camera-systems`*

- [ ] **Input Action Decoupling & Buffering (`INPUT-ACTION-ABSTRACTION-LOCK` & `abstract-input-actions`)**:
  - Gameplay logic listens exclusively to semantic action bindings (e.g. `action_jump`, `action_fire`), completely decoupled from raw hardware scancodes.
  - Action input buffering window ($80\text{--}150\text{ms}$) caches early player inputs during uninterruptible animations or recoveries.
  - Analog thumbsticks apply inner circular deadzones ($0.15\text{--}0.25$) and outer sensitivity scaling; runtime key and gamepad rebinding is fully supported.
- [ ] **Tactile Game Feel & Micro-Feedback ("Juice") (`tune-game-feel`)**:
  - Coyote time window ($50\text{--}120\text{ms}$) grants jump execution immediately after walking off ledge boundaries.
  - Hit-stop micro-pauses ($2\text{--}8$ frames, $33\text{--}133\text{ms}$) freeze attacker/target animations on impact without freezing audio or background threads.
  - Screen shake uses rotational/Perlin noise with quadratic decay curves ($I(t) = I_0 \cdot (1-t)^2$), with accessible user-facing intensity toggles ($0\%\text{--}100\%$).
- [ ] **Collision Filtering & Query Optimization (`configure-physics-collision`)**:
  - Layer-mask interaction matrix explicitly disables inert collision pairs (e.g. Debris vs Debris, Trigger vs Trigger).
  - High-velocity projectiles enable Continuous Collision Detection (CCD) to eliminate tunneling; non-allocating query buffers (`RaycastNonAlloc`) prevent garbage generation.
- [ ] **Dynamic Virtual Camera Direction (`direct-camera-systems`)**:
  - Virtual camera uses dual-zone deadzones, target look-ahead lead, and critically damped spring smoothing to maintain player framing.
  - Camera occlusion raycasts prevent geometry clipping; framing bounds respect level bounding boxes.

---

### Pillar 3: AI, Gameplay Mechanics & UI/UX
*Enforces `STATE-MACHINE-ISOLATION-LOCK`*  
*Skills covered: `author-game-ai`, `design-procedural-generation`, `build-game-ui-ux`, `integrate-dialogue-narrative`*

- [ ] **Time-Sliced AI & Navigation Budgets (`author-game-ai`)**:
  - NPC pathfinding (A*, NavMesh) and environmental queries are rate-limited and time-sliced ($\le 5\text{--}10\text{Hz}$ per agent) with spatial caching.
  - AI decision architectures (Behavior Trees, Utility AI, GOAP) operate with isolated blackboard state; sensory vision cones avoid expensive linear sweeps each frame.
- [ ] **Deterministic Procedural Generation (`design-procedural-generation`)**:
  - Procedural level generation (BSP dungeons, Cellular Automata caves, Wave Function Collapse) is strictly seeded and reproducible from a 64-bit integer seed.
  - Generated room graphs guarantee solvability and path connectivity between spawn, objectives, and exits before level activation.
- [ ] **Resolution-Independent UI & Focus Navigation (`build-game-ui-ux`)**:
  - HUD and menu canvases scale responsively across standard $16:9$, ultrawide $21:9$, and mobile aspect ratios with safe-area notch insets.
  - Gamepad and keyboard menus maintain an unbroken 4-way navigation DAG with explicit initial focus and modal return memory.
- [ ] **Branching Narrative & Dialogue Integration (`integrate-dialogue-narrative`)**:
  - Dialogue nodes (Ink, Yarn Spinner) decouple narrative text from code; condition evaluators execute within sandboxed variable environments.
  - Localization string catalogs support runtime language switching without requiring game restarts or text truncation.

---

### Pillar 4: Graphics, Shaders & Technical Art
*Skills covered: `program-game-shaders`, `inspect-blender-rigs-motion`, `render-webgl-threejs`, `generate-game-assets-pipeline`*

- [ ] **Shader Precision & Instruction Budgets (`program-game-shaders`)**:
  - Shaders use medium precision (`mediump` / `half`) for colors and UVs where possible, reserving `highp` / `float` for world-space positions.
  - Branching inside fragment shaders is replaced with step/lerp/mix operations; uniform buffers (UBOs) pack data to 16-byte alignments.
- [ ] **Blender Armature & Rig Hygiene (`inspect-blender-rigs-motion`)**:
  - Mesh transforms and armatures have unit scale `(1.0, 1.0, 1.0)`, zero rotation, and origin at world zero `(0, 0, 0)` prior to engine export.
  - Bone rolls are aligned; vertex skinning weights are normalized with a hard ceiling of $\le 4$ weights per vertex; root motion curves isolate ground-plane translation.
- [ ] **WebGL & WebGPU Scene Architecture (`render-webgl-threejs`)**:
  - High-frequency instances use `InstancedMesh` to consolidate draw calls; KTX2 / Basis Universal GPU textures and Draco/Meshopt geometry decode asynchronously.
  - Explicit `.dispose()` calls release geometries, materials, and render targets upon scene unmount, handling `webglcontextlost` gracefully.
- [ ] **Asset Pipeline Optimization (`generate-game-assets-pipeline`)**:
  - Automated asset pipelines generate hierarchical Level of Detail (LOD) chains and pack UI/sprite atlases with power-of-two dimensions and 2px bleed padding.

---

### Pillar 5: Audio, Performance & Publishing
*Enforces `MEMORY-ASSET-LIFECYCLE-LOCK`*  
*Skills covered: `mix-dynamic-game-audio`, `profile-game-performance`, `automate-game-publishing`*

- [ ] **Zero-Allocation Hot Loops & GC Elimination (`MEMORY-ASSET-LIFECYCLE-LOCK`)**:
  - High-frequency entities (projectiles, damage text, impact VFX, audio voices) use pre-warmed object pools.
  - Zero heap allocations occur in `Update()`, `FixedUpdate()`, or render loops; garbage collection pause times remain under $2\text{ms}$.
- [ ] **Frame Timing & Profiling Budgets (`profile-game-performance`)**:
  - Frame time meets hardware targets: $\le 16.6\text{ms}$ for $60\text{FPS}$, $\le 8.3\text{ms}$ for $120\text{FPS}$; CPU simulation consumes $\le 25\%$ of frame time.
  - Draw calls are capped at $\le 250$ for mobile, $\le 2,000$ for desktop; performance audit is emitted via `contracts/schemas/performance-audit.json`.
- [ ] **Dynamic Audio Mixing & Bus Routing (`mix-dynamic-game-audio`)**:
  - Sound playback routes through hierarchical buses (Master, Music, SFX, Voice, Ambience) with sidechain ducking for dialogue and combat impacts.
  - 3D spatial attenuation applies inverse-square curves; voice-stealing algorithms prevent channel exhaustion during high-density combat.
- [ ] **Automated Headless CI & Publishing (`automate-game-publishing` & `integrate-game-engine`)**:
  - Headless test harness runs in CI (`godot --headless`, Unity `-batchmode -nographics`, Unreal `-nullrhi`) and exits with code 0.
  - Multi-platform packaging produces signed release builds (SteamPipe, Butler, mobile bundles) with automated debug symbol archiving.

---

### Verification Sign-Off Table

| Pillar | Gate Focus | Primary Architectural Lock | Result (PASS / FAIL) |
|---|---|---|:---:|
| Pillar 1 | Core Architecture & Engine Lifecycles | `GAME-LOOP-TIMESTEP-LOCK`, `STATE-MACHINE-ISOLATION-LOCK` | PASS |
| Pillar 2 | Game Feel, Physics & Interaction | `INPUT-ACTION-ABSTRACTION-LOCK` | PASS |
| Pillar 3 | AI, Gameplay Mechanics & UI/UX | `STATE-MACHINE-ISOLATION-LOCK` | PASS |
| Pillar 4 | Graphics, Shaders & Technical Art | Pipeline Asset Hygiene | PASS |
| Pillar 5 | Audio, Performance & Publishing | `MEMORY-ASSET-LIFECYCLE-LOCK` | PASS |
