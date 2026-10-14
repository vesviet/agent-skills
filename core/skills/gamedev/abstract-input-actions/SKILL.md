---
name: abstract-input-actions
description: Abstracts hardware-agnostic input action mappings, chorded and buffered inputs, radial analog deadzones, runtime rebindable bindings, and multi-device hot-swap handling. Use when building input managers, controller support, keybinding menus, or accessibility input remapping.
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

# Abstract Input Actions

Design and implement hardware-agnostic input action layers that unify keyboard/mouse, gamepads, and touch controls with radial deadzone filtering, chorded bindings, runtime remapping, and seamless device hot-swapping.

## Core Rules

- **Strict Hardware Decoupling**: Gameplay systems must query semantic action states (`Jump`, `MoveVector`, `PrimaryAttack`, `Interact`) rather than polling raw hardware keycodes or button indices directly.
- **Scaled Radial Deadzones**: Filter 2D analog thumbstick inputs using scaled radial deadzones rather than independent per-axis axial deadzones to eliminate cardinal axis snapping and preserve smooth $360^\circ$ directional control.
- **Graceful Device Hot-Swapping**: Detect controller connection, disconnection, and active device switching automatically. Pause active gameplay immediately when the primary controller disconnects during action sequences.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing input abstraction implementations.

## Suggested Process

### 1. Action Context & Semantic Map Definition
Group semantic actions into mutually exclusive or stackable Input Contexts (`GameplayContext`, `UIContext`, `DialogueContext`, `VehicleContext`). Enable or disable contexts via state changes so menu navigation never triggers character jumps or attacks.

### 2. Analog Deadzone & Chorded Input Processing
Normalize raw analog stick vectors $\vec{v}$ against inner ($d_{\text{min}}$) and outer ($d_{\text{max}}$) deadzones:
$$\vec{v}_{\text{out}} = \frac{\vec{v}}{\|\vec{v}\|} \cdot \text{clamp}\left(\frac{\|\vec{v}\| - d_{\text{min}}}{d_{\text{max}} - d_{\text{min}}}, 0, 1\right)$$
Support composite bindings (2D D-pad/WASD vectors), chorded inputs (`Modifier + Button`), and press/hold/tap interaction timers.

### 3. Runtime Rebinding & Conflict Validation
Provide an interactive rebind listener that captures physical hardware actuation, blocks reserved system keys, detects duplicate binding conflicts within the same context, and serializes custom user binding overrides to persistent storage.

### 4. Multi-Device Disconnect & Prompt Synchronization
Monitor hardware device change events (`InputDeviceChanged`). Broadcast active device type events (`KeyboardMouse`, `GamepadXbox`, `GamepadDualSense`, `Touch`) to dynamically swap on-screen UI button glyphs and trigger pause safeguards on disconnect.

## Output Contracts

When completing input action abstraction, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Gameplay scripts query semantic action maps with zero hardcoded raw keycode polls
- [ ] Input contexts cleanly isolate Gameplay, UI, and Dialogue input consumption
- [ ] Analog stick processing uses scaled radial deadzones without cardinal axis snapping
- [ ] Runtime keybinding remapping detects conflicts and persists user overrides across sessions
- [ ] Controller disconnection automatically pauses active gameplay and updates UI glyph prompts
- [ ] Headless unit tests verify deadzone math, chorded action triggers, and context switching

## Related Skills

- **develop-gameplay-systems**: consuming semantic action states in character controllers
- **tune-game-feel**: integrating input buffering and coyote time windows with action maps
- **build-game-ui-ux**: updating dynamic controller glyph prompts and focus navigation
