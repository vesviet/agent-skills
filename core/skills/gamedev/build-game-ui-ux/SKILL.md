---
name: build-game-ui-ux
description: Builds responsive game UI and HUD architectures featuring multi-resolution canvas scaling, 9-slice anchors, mobile and ultrawide safe-area margins, gamepad and keyboard focus navigation, and reactive dialogue or HUD overlays. Use when implementing game menus, HUD widgets, inventory grids, or controller-navigable interfaces.
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

# Build Game UI UX

Architect and implement resolution-independent game HUDs, menu stacks, and interactive overlays that support ultrawide and mobile aspect ratios, safe-area cutouts, and seamless gamepad/keyboard focus navigation.

## Core Rules

- **Event-Driven UI Decoupling**: Never poll gameplay entities inside UI `Update()` loops. Bind HUD widgets (health bars, ammo counters, cooldown radials, quest trackers) to explicit gameplay events or observable view-models so UI only redraws when state changes.
- **Resolution & Safe-Area Conformance**: Configure reference canvas scaling (e.g. $1920\times 1080$ or $2560\times 1440$ with expand/match width-or-height modes), 9-slice border sprites, and dynamic safe-area insets (`Screen.safeArea`, title-safe margins) across $16:9$, $21:9$, $32:9$, and notched mobile viewports.
- **Unbroken Focus Navigation Loops**: Every interactive screen must assign an explicit default focused element on open, maintain deterministic 4-way directional navigation (`Up`, `Down`, `Left`, `Right`), and restore focus to the invoking control when modal popups close.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing game UI/UX implementations.

## Suggested Process

### 1. Canvas Hierarchy, Anchors & Safe-Area Layout
Structure UI into layered sorting canvases (`WorldSpaceIndicators`, `GameplayHUD`, `ModalMenus`, `SystemNotifications`, `TransitionOverlay`). Pin HUD corners to a Safe-Area container node and use 9-slice sprite borders so panels scale cleanly without distorting corners.

### 2. Focus Graph & Multi-Device Navigation
Configure explicit focus neighbors for buttons, sliders, and scrollable inventory grids. Ensure opening any menu immediately calls `GrabFocus()` / `Select()` on the primary action button and blocks pointer-hover theft when operating in gamepad mode.

### 3. Reactive HUD & Pooled Floating Overlays
Drive health/mana bars with secondary delayed damage-trail bars and pooled floating combat text (FCT) widgets. Separate static background frames from frequently dirtied dynamic text/fill canvases to prevent full-canvas UI batch rebuilds every frame.

### 4. Accessibility & Scaling Verification
Expose text scaling ($100\%\text{--}150\%$), high-contrast HUD backgrounds, and colorblind-safe status iconography (pairing distinct shapes with colors). Test layouts headlessly or across simulated aspect ratios ($4:3$, $16:9$, $21:9$, mobile portrait/landscape).

## Output Contracts

When completing game UI and UX implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] HUD widgets update reactively via event subscriptions with zero per-frame polling
- [ ] Canvas anchors, 9-slice panels, and safe-area margins adapt cleanly to $16:9$, $21:9$, and mobile notches
- [ ] Gamepad and keyboard focus navigation operates deterministically without focus loss on modal close
- [ ] Dynamic HUD elements are isolated from static UI layers to minimize canvas batch rebuilds
- [ ] Floating combat text and transient notification popups use pre-warmed object pools
- [ ] UI supports text scaling and shape-reinforced indicators for colorblind accessibility

## Related Skills

- **abstract-input-actions**: routing UI navigation contexts and dynamic controller glyph prompts
- **integrate-dialogue-narrative**: rendering typewriter dialogue boxes, speaker portraits, and choice menus
- **tune-game-feel**: animating snappy UI transitions, button press juice, and audio feedback
