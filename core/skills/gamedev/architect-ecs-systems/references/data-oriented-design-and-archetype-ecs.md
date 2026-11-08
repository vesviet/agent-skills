# Data-Oriented Design & Archetype ECS Architecture (2026)

## 1. Principles of Data-Oriented Design (DOD)

Object-Oriented Programming (OOP) distributes component data across fragmented heap objects, inducing continuous CPU L1/L2 cache misses through pointer chasing. Data-Oriented Design organizes data strictly around hardware memory hierarchies:

```
OOP (Fragmented Heap Pointers)
  [Entity 1 Pointer] ──► Heap [ Transform | Health | AIState ]  (Cache Miss)
  [Entity 2 Pointer] ──► Heap [ Transform | Health | AIState ]  (Cache Miss)

DOD / Archetype Storage (Contiguous Memory Arrays)
  Archetype [Transform, Velocity, Health]:
    Transforms: [ T1 | T2 | T3 | T4 | T5 | T6 ... ] (Packed L1 Cache Lines)
    Velocities: [ V1 | V2 | V3 | V4 | V5 | V6 ... ] (SIMD Vectorizable)
    Healths:    [ H1 | H2 | H3 | H4 | H5 | H6 ... ] (Contiguous Buffer)
```

## 2. Archetype vs Sparse Set Memory Layouts

1. **Archetype Storage (Bevy, Flecs, Unity DOTS)**:
   - Entities with the exact same component combination reside in a shared archetype chunk.
   - Iteration speed is maximal ($O(1)$ sequential memory access).
   - Component addition/removal incurs an archetype move (migrating entity data to another chunk).
2. **Sparse Set Storage (EnTT)**:
   - Each component type maintains a dense array of data and a sparse index array.
   - Fast component addition/removal ($O(1)$) with slightly lower cache locality than pure archetypes.

## 3. Structural Mutations & Command Buffers

Directly creating entities, destroying entities, or adding/removing components while systems iterate archetype tables corrupts array iterators.
- **Invariant**: All structural modifications are recorded into a `Commands` / `CommandBuffer` queue.
- **Synchronization Points**: Command buffers flush strictly at stage boundaries (`PreUpdate -> Update -> PostUpdate`), maintaining immutable memory layouts during active parallel iterations.

## 4. Multi-Threading & Borrow Checker Rules

- **Disjoint Queries**: Two systems may execute in parallel if and only if their mutable component borrow sets are disjoint:
  $$\text{System A}(\text{Mut}\langle X\rangle, \text{Ref}\langle Y\rangle) \parallel \text{System B}(\text{Mut}\langle Z\rangle, \text{Ref}\langle Y\rangle) \iff X \cap Z = \emptyset$$
- **Read-Only Concurrency**: Any number of systems may concurrently read `Ref<Y>` without contention or locking overhead.
