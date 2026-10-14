---
name: tune-game-feel
description: Tune responsiveness, input buffering, screen shake, hit-stop, and audiovisual juice to maximize game feel and tactile player feedback. Use when adding polish, hit reactions, camera shake, coyote time, or feedback layers.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Tune Game Feel

Enhance player agency, perceived responsiveness, and sensory impact through structured "juice" pipelines without compromising deterministic simulation.

## Core Rules

- **Decoupled Juice Architecture**: Keep sensory polish (camera shake, freeze frames, particle bursts, chromatic aberration) strictly decoupled from core game mechanics and simulation state. Disabling juice must leave game logic fully intact.
- **Input Forgiveness Windows**: Implement coyote time ($50\text{--}120\text{ms}$) and input jump/action buffering ($80\text{--}150\text{ms}$) to absorb human timing variances and frame pacing drops.
- **Decay Curve Discipline**: Always drive screen shake and recoil with non-linear exponential or power decay curves ($I(t) = I_0 \cdot e^{-k t}$ or $(1-t)^2$) rather than linear decay to avoid robotic jarring.
- **Micro-Hit-Stop Limits**: Restrict hit-stop (frame freezing) to $2\text{--}8$ frames ($33\text{--}133\text{ms}$). Never freeze the entire engine process; pause only actor animation and movement timelines while keeping VFX active.

## Suggested Process

### 1. Timing Tolerances Calibration
Implement timer counters for:
- **Coyote Time**: Allow jumping shortly after leaving a ledge: `time_since_grounded <= coyote_threshold`.
- **Input Buffer**: Queue action presses: `time_since_pressed <= buffer_threshold`.
- **Variable Jump Cutoff**: When jump button is released early, scale downward gravity or cap upward velocity.

### 2. Multi-Tier Impact Response
Construct a unified feedback event bus triggered by combat or impact events:
- *Tier 1 (Light Impact)*: Audio click/swish + subtle sprite squash/stretch ($5\text{\%}$).
- *Tier 2 (Medium Impact)*: Positional particle burst + 2-frame hit-stop + directional screen shake ($2\text{px}$).
- *Tier 3 (Heavy / Critical)*: 6-frame hit-stop + radial camera impulse + sound ducking + chromatic flash.

### 3. Screen Shake Implementation
Use perceptual Perlin noise or rotational shake:
$$\text{offset}_x = \text{trauma}^2 \cdot \text{noise}_x(t), \quad \text{offset}_y = \text{trauma}^2 \cdot \text{noise}_y(t)$$
Dampen trauma continuously each frame: $\text{trauma} = \max(0, \text{trauma} - \text{decay} \cdot \Delta t)$.

### 4. Accessibility & Comfort Controls
Always expose user settings to scale or disable screen shake ($0\text{\%}\text{--}100\text{\%}$), flash effects, and motion blur for accessibility and photosensitivity compliance.

## Output Contracts

When completing game feel tuning, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Coyote time and jump buffering operate cleanly across edge cases
- [ ] Hit-stop pauses local target actor without locking audio or camera systems
- [ ] Screen shake trauma uses quadratic/exponential decay without gimbal lock
- [ ] Accessibility slider exists to completely toggle or scale screen shake
- [ ] Zero state desynchronization between visual interpolation and physics body

## Related Skills

- **develop-gameplay-systems**: foundation physics, kinematic bodies, and collision matrices
- **integrate-game-engine**: engine audio buses and particle system integration
