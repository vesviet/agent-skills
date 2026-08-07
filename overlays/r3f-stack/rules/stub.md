---
description: "Active rules for the r3f-stack overlay after the v4.0.0 migration moved the three R3F skills out of core."
---

# R3F Stack Conventions

- Skills under this overlay assume a React + R3F/Three.js target. Do not load them for vanilla Three.js, Babylon.js, or non-React projects.
- 3D performance budgets (60fps / 1M triangles / 4MB gzipped) are defaults; tighten per project.
- When adding a new R3F skill, keep the naming pattern `<verb>-<noun>` and stick to R3F-idiomatic guidance (declarative scene graph, useFrame, drei helpers).
- Coordinate with `overlays/obj-configurator` for product-configurator specifics.
