# Continuous Collision Detection (CCD) & Substepping Specifications (2026)

## 1. Physics Solver Architecture & The Tunneling Problem

Discrete collision detection evaluates entity overlaps only at discrete timestep intervals $t_0, t_1, \dots$. When an object's per-tick displacement $\Delta x = v \cdot \Delta t$ exceeds its collision boundary thickness $2r$, discrete evaluation fails, resulting in "tunneling" (passing through solid obstacles without triggering collision events).

```
Discrete Collision Tunneling:
Tick t_0:  [Collider (r)] ────────► (Wall) ────────► Tick t_1:  [Collider (r)]
           (Before Wall)                                         (Passed Through!)

Continuous Collision Detection (CCD Swept Volume):
Tick t_0:  [=== Swept Capsule / Sphere Cast ============] (Wall)
           Collision Time-of-Impact (TOI) Detected at t_hit!
```

## 2. Continuous Collision Detection Strategies

1. **Swept Sphere / Capsule Casts**:
   - Sweeps a sphere or capsule along the entity's velocity vector $\vec{v}$.
   - Solves for the earliest Time-of-Impact (TOI) $\tau \in [0, \Delta t]$.
   - Caps movement at $\tau \cdot \vec{v}$ and generates contact normal at impact point.
2. **Speculative Contacts (Predictive Constraints)**:
   - Extends the collision envelope by the distance covered in the upcoming tick.
   - Adds contact constraints into the LCP solver before actual geometric penetration occurs.
   - Prevents tunneling with lower CPU overhead than repeated swept tests.

## 3. Substepping & Spiral of Death Prevention

When a frame experiences a CPU hitch or large physics delta, the accumulator loop must not enter an infinite substepping loop:
```cpp
const float FIXED_DELTA = 1.0f / 60.0f;
const int MAX_SUBSTEPS = 4; // Bounded substepping ceiling

accumulator += frame_delta;
int steps = 0;
while (accumulator >= FIXED_DELTA && steps < MAX_SUBSTEPS) {
    PhysicsWorld::StepSimulation(FIXED_DELTA);
    accumulator -= FIXED_DELTA;
    steps++;
}
if (accumulator >= FIXED_DELTA) {
    accumulator = 0.0f; // Drop excess time to prevent spiral of death
}
```

## 4. Contact Normal Stabilization & Ground Snapping

- Distinguish ground from steep walls: $\cos(\theta) = \vec{n}_{\text{contact}} \cdot \vec{u}_{\text{up}} \ge \cos(\theta_{\text{max\_slope}})$.
- Downward raycast snap distance ($0.2\text{m}$) prevents separation bounce when descending slopes or modular floor junctions.
