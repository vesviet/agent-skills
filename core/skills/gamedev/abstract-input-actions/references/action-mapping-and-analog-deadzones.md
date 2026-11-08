# Input Action Mapping & Scaled Radial Deadzones (2026)

## 1. Architectural Foundations: Hardware Decoupling

Gameplay systems must never query physical device hardware keys (e.g., `Key_W`, `Gamepad_Button_South`). Input systems enforce a three-tier decoupling pipeline:

```
Physical Devices (KBM, Xbox, DualSense, Touch)
                      │
                      ▼
Raw Input Polling (DirectInput, XInput, Gamepad API)
                      │
                      ▼
Scaled Radial Deadzone & Coordinate Normalization
                      │
                      ▼
Context-Filtered Semantic Actions (Jump, Move, Fire)
                      │
                      ▼
Gameplay Consumer Systems (Character, UI, Vehicle)
```

## 2. Scaled Radial Deadzone Algorithm

Per-axis deadzone filtering introduces cardinal axis snapping, destroying subtle diagonal analog stick movement. The scaled radial deadzone algorithm operates on the complete 2D magnitude:

$$\vec{v} = (x, y), \quad \|\vec{v}\| = \sqrt{x^2 + y^2}$$

$$\vec{v}_{\text{filtered}} = \begin{cases} 
(0, 0) & \text{if } \|\vec{v}\| \le d_{\text{min}} \\
\frac{\vec{v}}{\|\vec{v}\|} & \text{if } \|\vec{v}\| \ge d_{\text{max}} \\
\frac{\vec{v}}{\|\vec{v}\|} \cdot \left( \frac{\|\vec{v}\| - d_{\text{min}}}{d_{\text{max}} - d_{\text{min}}} \right) & \text{otherwise}
\end{cases}$$

Where standard default parameters are:
- Inner deadzone: $d_{\text{min}} = 0.15$ (filters mechanical stick drift).
- Outer deadzone: $d_{\text{max}} = 0.95$ (ensures maximum velocity reach without physical strain).

## 3. Input Context Hierarchy

Actions belong to semantic Contexts:
- `GameplayContext`: Jump, Move, Attack, Dodge.
- `UIContext`: Navigate, Confirm, Cancel, TabNext.
- `DialogueContext`: AdvanceDialogue, Skip, ChooseOption.

Context priority stacks prevent gameplay input leakage when interacting with inventory or modal menus.

## 4. Multi-Device Hot-Swapping & Disconnect Safeguards

1. Listen to device connect/disconnect events (`gamepadconnected`, `gamepaddisconnected`).
2. When the active gameplay controller disconnects during combat or real-time simulation:
   - Immediately dispatch `InputDeviceDisconnectedEvent`.
   - Freeze kinematic simulation and trigger the system pause menu.
   - Dynamically swap UI prompt glyphs to the fallback device (e.g., KBM or connected Gamepad 2).
