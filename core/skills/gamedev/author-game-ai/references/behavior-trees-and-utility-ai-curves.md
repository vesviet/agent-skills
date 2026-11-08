# Behavior Trees & Utility AI Curves (2026)

## 1. Dual AI Architecture: Tactical Trees vs Continuous Scoring

Modern game AI combines discrete Behavior Trees (BT) for hierarchical state progression with continuous Utility AI response curves for multi-criteria trade-offs:

```
┌────────────────────────────────────────────────────────┐
│                   BEHAVIOR TREE                        │
│                     [Root: ?]                          │
│                    /         \                         │
│         [Combat Seq: ->]    [Patrol Seq: ->]           │
│          /            \                                │
│   (Target In Range?)  [Utility Action Selector]        │
└───────────────────────────────┬────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────┐
│                  UTILITY AI EVALUATOR                  │
│   Score(Action) = w_1*U(dist) * w_2*U(hp) * w_3*U(agg) │
│   Selected: Attack Melee (0.82) vs Cast Spell (0.45)   │
└────────────────────────────────────────────────────────┘
```

## 2. Stateless Nodes & Typed Blackboard Separation

- **Stateless Tree Principle**: Behavior Tree nodes (`Selector`, `Sequence`, `ActionNode`, `Decorator`) are instantiated once and shared across thousands of agent instances.
- **Typed Blackboard**: All runtime dynamic memory resides in the agent's `Blackboard`:
  - `target_id: string | null`
  - `last_seen_pos: Vector3`
  - `alert_level: float (0.0 to 1.0)`
  - `cooldown_timers: Map<string, float>`

## 3. Utility AI Response Curves

Utility factors are mapped to normalized scores $U \in [0.0, 1.0]$ via mathematical response curves:
1. **Linear Curve**: $U(x) = mx + c$ (direct proportional scaling).
2. **Quadratic / Exponential**: $U(x) = x^k$ (sharp thresholding; e.g. urgency spikes when health drops below 20%).
3. **Logistic Sigmoid**: $U(x) = \frac{1}{1 + e^{-k(x - x_0)}}$ (smooth S-curve transitions).

Combined Utility calculation uses geometric mean or product with compensation exponents:
$$\text{Score} = \prod_{i=1}^n \left( U_i(x_i) \right)^{w_i}$$

## 4. Time-Sliced Pathfinding & Token Systems

- **Budgeted Scheduler**: Central queue capping path planning execution to $\le 2.0\text{ms}$ per frame.
- **Squad Token Pools**: Limits concurrent melee attack tokens (e.g., max 2 attackers), forcing remaining squad members into flanking or suppressive fire behaviors to eliminate unfair dogpiling.
