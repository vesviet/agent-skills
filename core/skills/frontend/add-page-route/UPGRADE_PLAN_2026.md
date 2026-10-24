# add-page-route — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### React 19 / RSC Integration (2026)
- **React 19.2 stable** (June 2026 with Expo SDK 56): Server Components, `use()`, `useActionState`, `useOptimistic`, `<form> Actions`
- **RSC Leaf Pattern**: Push `"use client"` as deep as possible; RSC at top, interactive client components as children
- **TanStack Start RSC**: `createServerFn`, Flight streams, `renderToReadableStream`, composite components with slots
- **React 19 `use()` hook**: Read promises directly in Server-rendered components for RSC streaming
- **React 19 `useActionState`**: Form actions with pending state, error handling, progressive enhancement

### Routing Evolution (2026)
- **TanStack Router v2** / **React Router v7**: Type-safe routing, `validateSearch` with Zod `.catch()` fallbacks
- **Expo Router v4+**: File-based routing replacing React Navigation; nested layouts, route groups, `useLocalSearchParams`
- **Next.js 15 App Router**: Server Actions, `use cache`, `unstable_cache`, streaming with Suspense
- **Loader pattern mandatory**: Hoist data loading to loader functions — no `useEffect` fetches after mount (layout shift waterfalls)

### Type-Safe Navigation (2026)
- **Type-safe primitives only**: `<Link to="..." />`, `navigate({ to: '...' })` — never untyped string concatenation
- **URL search params validation**: Zod schemas with `.catch()` fallbacks in `validateSearch`
- **AI-generated route validation**: Auth guard completeness, data loading pattern match, cache invalidation, URL param validation

### View Transitions (2026)
- **CSS View Transitions API**: Native, `::view-transition-old/new`, composited properties only (`transform`, `opacity`)
- **React 19 `ViewTransition`**: `default="none"`, wrap before DOM nodes, unique names with dynamic IDs
- **INP budget < 200ms**: DOM mutation callback < 50ms; `React.startTransition` + `scheduler.yield()`
- **Reduced motion**: `@media (prefers-reduced-motion: reduce)` mandatory

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| TanStack Router v2 / React Router v7 basic | **RSC-aware routing**: React 19 `use()` in Server Components, TanStack Start `createServerFn`, Expo Router file-based |
| Loader pattern mentioned | **Loader pattern mandatory**: Hoist data loading to loaders; no `useEffect` primary fetches |
| Type-safe navigation | **Zod `validateSearch` with `.catch()` fallbacks**: Raw URL params are user-controlled input |
| AI-generated route validation | **Comprehensive AI audit**: Auth guards, data loading, cache invalidation, URL validation |
| View transitions reference | **CSS View Transitions + React 19 `ViewTransition`**: Composited motion only, INP < 200ms, reduced motion |

### 2. New 2026 Patterns to Add
- **RSC Page Architecture**: Server Components at route level, `"use client"` pushed to leaves
- **TanStack Start Server Functions**: `createServerFn` for route data, Flight stream rendering
- **React 19 Form Actions**: `<form action={submitAction}>`, `useActionState` for progressive enhancement
- **Expo Router v4+ Patterns**: File-based routes, `useLocalSearchParams`, nested layout.tsx
- **URL Parameter Validation**: Zod schemas with `.catch()` fallbacks in `validateSearch` for all search params
- **CSS View Transitions Integration**: `startViewTransition`, `ViewTransition` boundaries, `view-transition-name` uniqueness
- **AI Route Generation Audit Checklist**: Auth guard, loader pattern, cache invalidation, URL validation

### 3. Checklist Additions
- [ ] Route follows repo RSC pattern (Server Components at top, client leaves)
- [ ] Data loading hoisted to loader / Server Function — no `useEffect` primary fetches
- [ ] Type-safe navigation: `<Link to="..." />`, `navigate({ to: '...' })` only
- [ ] URL search params validated with Zod `.catch()` fallbacks in `validateSearch`
- [ ] Loading, empty, error, unauthorized states explicit
- [ ] SEO/SSR verified for public routes: meta tags, OG, SSG behavior, canonical tags
- [ ] CSS View Transitions: composited properties only, INP < 200ms, reduced motion override
- [ ] React 19 `ViewTransition` boundaries: `default="none"`, wrap before DOM nodes, unique dynamic names
- [ ] AI-generated route audit: auth guards complete, loader pattern matched, cache invalidation on mutations, URL params validated
- [ ] Direct URL access works; back/forward navigation correct
- [ ] Tests: route render, guard/auth behavior, page transitions, failure/empty states
- [ ] `contracts/schemas/implementation-result.json` emitted

### 4. Failure Mode Additions
- **RSC hydration mismatch**: Server/Client tree divergence. Mitigation: `"use client"` boundary at correct leaf; avoid server-only APIs in shared components.
- **Loader waterfall**: Sequential loaders causing cascade delays. Mitigation: Parallelize independent loaders; use `Promise.all` in loader.
- **Zod validation too strict**: Valid URLs rejected by over-constrained schemas. Mitigation: `.catch()` fallbacks with sensible defaults; log validation failures.
- **CSS View Transition INP violation**: DOM mutation > 50ms. Mitigation: `React.startTransition` + `scheduler.yield()`; chunk streaming work.
- **AI route missing auth guard**: Anonymous access to protected route. Mitigation: Mandatory AI audit checklist; reject routes without auth wrapper.
- **Expo Router layout drift**: Nested layout.tsx not matching route hierarchy. Mitigation: Lint rule for layout nesting consistency.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: RSC boundary location, loader functions, Zod schemas, View Transition config

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | RSC leaf pattern enforcement (`"use client"` depth) | High |
| P0 | Loader pattern mandatory (no `useEffect` fetches) | High |
| P0 | Zod `validateSearch` with `.catch()` fallbacks | High |
| P0 | AI route generation audit checklist | Medium |
| P1 | CSS View Transitions + React 19 integration | Medium |
| P1 | TanStack Start Server Functions for route data | Medium |
| P1 | Expo Router v4+ file-based routing patterns | Medium |
| P2 | React 19 `useActionState` form integration | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test RSC hydration with `"use client"` at various depths
- Validate Zod `validateSearch` rejects malformed URLs with fallbacks
- Benchmark INP with CSS View Transitions under 4x CPU throttling
- Test AI route generation audit catches missing auth guards