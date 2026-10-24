---
name: integrate-game-engine
description: Bridge game architecture across engines, manage headless test runners, configure export pipelines, and enforce asset normalization. Use when configuring Godot, Unity, Unreal, or Web game engine builds and headless test runners.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Integrate Game Engine

Manage engine-level lifecycles, cross-platform export presets, headless automated verification, and asset importer pipelines across production game engines.

## Core Rules

- **Headless-First Verification**: Every gameplay module or system must be verifiable without launching a graphical window (`godot --headless --run-tests`, Unity `-batchmode -nographics`, Unreal `-nullrhi`). Headless test suites must return standard OS exit codes ($0 = \text{success}$).
- **Deterministic Asset Import**: Asset import settings (texture compression, sprite slice rectangles, audio sample rates, 3D glTF mesh optimizations) must be codified in version-controlled config files (`.import`, `.meta`, `.uasset` manifests), never edited ad-hoc.
- **Strict Frame Budgeting**: Configure target engine frame limits (e.g. $16.6\text{ms}$ budget for $60\text{FPS}$, $8.3\text{ms}$ for $120\text{FPS}$). Enforce maximum draw call ceilings ($\le 250$ on mobile, $\le 2000$ on desktop).
- **Engine-Agnostic Core Boundary**: Structure game state, data models, and business logic into pure libraries or decoupled modules that interact with engine nodes exclusively through thin adapter interfaces.

## Suggested Process

### 1. Engine Detection & Project Fingerprinting
Inspect project root signals to identify the active engine:
- Godot: `project.godot`
- Unity: `Assets/` and `ProjectSettings/ProjectVersion.txt`
- Unreal: `*.uproject`
- Web: `package.json` with `phaser`, `pixi.js`, or `three`
- Other: `Cargo.toml` (`bevy`), `conf.lua` (`love2d`), `*.py` (`pygame`)

### 2. Headless Test Runner Integration
Set up an automated CI test harness:
```bash
# Example Godot 4.x headless runner
godot --headless --path . -s tests/run_suite.gd --quit-after 500
```
Verify stdout parses test assertions and exits with non-zero on failure.

### 3. Asset Pipeline & Texture Optimization
Enforce automated texture compression:
- Desktop: BC7 / DXT5
- Mobile: ASTC (4x4 or 6x6) / ETC2
- Web: KTX2 / Basis Universal
Verify texture sizes are power-of-two (POT) to ensure mipmap generation and GPU alignment.

### 4. Build Pipeline Automation
Configure export profiles for targeted platforms (Windows, Linux, macOS, WebAssembly/HTML5, Mobile). Ensure debug symbols are stripped in release builds and assets are packed into binary archives (`.pck`, Addressables bundles, `.pak`).

## Output Contracts

When completing engine integration or build automation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Headless test runner executes in CI with exit code $0$ on passing suites
- [ ] Texture compression and import settings are committed to version control
- [ ] Target framerate budget and VSync configurations are explicitly set
- [ ] Export templates strip editor code and debug asserts in release configurations
- [ ] Binary package size complies with platform store distribution limits

## Related Skills

- **develop-gameplay-systems**: core gameplay loops and fixed-timestep execution
- **tune-game-feel**: audiovisual feedback calibration and accessibility settings
