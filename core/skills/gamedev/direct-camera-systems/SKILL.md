---
name: direct-camera-systems
description: Directs 2D and 3D virtual camera systems including frame-rate independent smooth dampening, deadzone framing, velocity look-ahead lead targeting, confinement bounds, room transitions, and multi-target zoom framing. Use when implementing follow cameras, cinematic transitions, lock-on targeting, or 3D spring arms.
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

# Direct Camera Systems

Architect and tune responsive 2D and 3D virtual camera directors that combine critically damped tracking, deadzone composition, look-ahead velocity framing, level boundary confinement, and collision-safe spring arms.

## Core Rules

- **Frame-Rate Independent Damping**: Never use naive linear interpolation (`lerp(a, b, 0.1)`) with raw frame delta time. Always use exponential decay (`lerp(a, b, 1.0 - exp(-lambda * dt))`) or critically damped spring solvers so camera tracking matches across $60\text{Hz}$, $144\text{Hz}$, and $240\text{Hz}$ displays.
- **Late-Update Execution Order**: Evaluate camera positioning and orientation strictly after physics interpolation and target movement have completed for the frame (`LateUpdate` or post-process tick) to prevent visual jitter.
- **Non-Destructive Shake & Impulse Layering**: Apply camera trauma, recoil, and screen shake as additive local transform offsets on a child rig node so base tracking coordinates remain uncorrupted.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing camera system implementations.

## Suggested Process

### 1. Virtual Camera Rig & Deadzone Framing
Construct a virtual camera priority blending system. Configure screen-space deadzones (inner soft zone where small player adjustments do not pan the camera, and outer hard zone that clamps the target inside the frame).

### 2. Critically Damped Tracking & Look-Ahead Lead
Project a look-ahead target offset along the player's smoothed velocity or aim vector:
$$\vec{p}_{\text{desired}} = \vec{p}_{\text{target}} + \vec{v}_{\text{smoothed}} \cdot t_{\text{lead}}$$
Advance the camera toward $\vec{p}_{\text{desired}}$ using critically damped spring integration or exponential decay, applying asymmetric vertical damping for platformer jump arcs.

### 3. Confinement Bounds, Room Transitions & 3D Occlusion
Clamp camera frustum edges against 2D/3D level bounding volumes (`Polygon2D` or `AABB` confiners) so out-of-bounds void areas remain hidden. For 3D cameras, attach sphere-cast spring arms to pull the camera forward cleanly when occluded by walls.

### 4. Multi-Target Group Framing
Compute the dynamic bounding box enclosing all active targets (e.g. co-op players or boss encounters). Interpolate the camera focal point to the weighted centroid and adjust orthographic size or FOV/distance within clamped `[min_zoom, max_zoom]` limits.

## Output Contracts

When completing camera system implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Camera smoothing uses exponential decay or critically damped springs for frame-rate independence
- [ ] Camera updates execute in post-movement `LateUpdate` stages with zero physics tick jitter
- [ ] Screen-space deadzones and velocity look-ahead offsets prevent motion sickness during micro-movements
- [ ] Confiner volumes and 3D sphere-cast spring arms prevent camera clipping through level geometry
- [ ] Multi-target framing smoothly interpolates centroid position and clamped zoom limits
- [ ] Additive shake/impulse offsets respect user accessibility reduction sliders

## Related Skills

- **tune-game-feel**: layering trauma-based screen shake and impact impulses onto camera rigs
- **develop-gameplay-systems**: synchronizing camera orientation with character movement vectors
- **manage-scene-lifecycle**: blending virtual cameras across room and scene transitions
