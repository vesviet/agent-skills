---
name: develop-obj-feature
description: Develop features for the OBJ 3D Product Configurator — an Astro + React Three Fiber app with Three.js engine, Redux/Zustand state, and Prisma backend. Use when modifying 3D scenes, decals, UI panels, or design persistence.
---

# Develop OBJ Feature

Use this skill when building or modifying features in the OBJ 3D Product Configurator.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/obj-configurator/rules/obj-project-rules.md`
- GLB format only for 3D models — no OBJ/MTL in new work
- Sprite-based preview during drag — never recalculate DecalGeometry per frame
- Memoize React components to prevent re-renders during 3D interaction
- Dispose Three.js resources on unmount (geometries, materials, textures)
- Debounce continuous transforms to 100ms before dispatching to Redux/Zustand

## Suggested Process

### 1. Identify layer — 3D engine, UI panel, state slice, Prisma schema, or Astro page
### 2. Read existing code in `src/design-hub/` for the relevant subsystem
### 3. Implement following engine rules and performance constraints
### 4. Test at 60fps — profile with Chrome DevTools if needed
### 5. Run `npm run check` before commit

## Checklist

- [ ] GLB format used for all new 3D models
- [ ] Three.js resources properly disposed on unmount
- [ ] React components memoized where appropriate
- [ ] Continuous transforms debounced before store dispatch
- [ ] Sprite-based preview used during drag operations
- [ ] Canvas DPR capped at 2 on mobile
- [ ] Prisma schema changes include migration
- [ ] `npm run check` passes

## Related Skills

- **debug-3d-scene**: debug Three.js rendering and material issues
- **optimize-3d-assets**: optimize models and textures for performance
- **integrate-r3f-three-legacy**: bridge R3F and legacy Three.js code
- **review-code**: review against project conventions
- **commit-code**: commit with proper conventions
