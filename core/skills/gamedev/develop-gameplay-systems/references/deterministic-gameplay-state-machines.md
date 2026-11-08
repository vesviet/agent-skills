# Deterministic Gameplay State Machines & Kinematics (2026)

## 1. Architectural Foundations: Fixed-Timestep Simulation

Deterministic gameplay simulation requires complete decoupling of render framerates from physics calculation:

$$\Delta t_{\text{fixed}} = \frac{1}{\text{TickRate}} \quad (\text{typically } 60\text{Hz or } 120\text{Hz})$$

```
Render Frame (Variable Delta)
    │
    ├─► Accumulator += frame_delta
    │
    ▼
While Accumulator >= fixed_delta:
    ├─► Process Input Buffers
    ├─► Integrate Velocities: x_{t+1} = x_t + v_t * fixed_delta
    ├─► Resolve CCD & Kinematic Collisions
    ├─► Advance State Machine
    └─► Accumulator -= fixed_delta
    │
    ▼
Render Interpolation: alpha = Accumulator / fixed_delta
Render State = lerp(PreviousState, CurrentState, alpha)
```

## 2. Hierarchical State Machine (HSM) Invariants

1. **Single Active State Invariant**: At any discrete tick $t$, an entity possesses exactly one leaf state in its state hierarchy (e.g. `Root -> Grounded -> Moving`).
2. **Transition Authority**: State transitions can only occur via explicit transition triggers evaluated against deterministic condition flags (e.g., `is_on_floor`, `jump_buffered`, `stamina > 0`). Direct mutation of state flags from outside callers is prohibited.
3. **Lifecycle Contracts**:
   - `Enter(context)`: Pre-allocates resources, initializes timers, triggers animation events.
   - `PhysicsUpdate(delta)`: Evaluates motion vector, applies gravity, triggers collision queries.
   - `Exit()`: Resets timers, clears transient buffers, cancels incomplete actions.

## 3. Kinematic Motion & Collision Handling

- **Ground Contact Snapping**: Snap character to slopes within the maximum slope angle ($\theta \le 45^\circ$) to prevent airborne jitter when descending.
- **Coyote Time & Input Buffering**:
  - Coyote Time: Grace window (e.g., $100\text{ms}$) permitting jump initiation after walking off an edge.
  - Jump Buffering: Queue jump inputs received within $150\text{ms}$ before landing on ground.
- **Zero-Allocation Spatial Queries**: Pre-allocate raycast hit arrays and query shapes. Never instantiate temporary vector arrays or lambda closures in the fixed loop.
