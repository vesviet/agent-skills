# implement-view-transitions — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### CSS View Transitions API (2026)
- **Native browser support**: `::view-transition-old`, `::view-transition-new` pseudo-elements
- **Composited motion only**: Strictly animate `transform` and `opacity`; **never** layout geometry (`width`, `height`, `top`, `left`, `margin`, `padding`)
- **`view-transition-name` uniqueness**: Globally unique across active elements; suffix with dynamic IDs (`hero-image-${item.id}`)

### React 19 ViewTransition (2026)
- **`<ViewTransition>` component**: `default="none"` mandatory; wrap content **before any DOM nodes**
- **Type-keyed transitions**: `name` prop for shared elements; `share="morph"` for morphing
- **Directional transitions**: `addTransitionType` (`nav-forward`, `nav-back`) inside `startTransition`
- **Fallback animations**: Defined for shared elements when matching target absent

### Performance Budgets (2026)
- **INP < 200ms**: DOM mutation callback in `startViewTransition` must execute < 50ms
- **No synchronous long tasks**: Wrap non-urgent transitions in `React.startTransition`; chunk with `scheduler.yield()`
- **Frequency-based animation budget**: Hotkeys (`Cmd+K`) = 0ms; micro-interactions = 100-150ms; overlays/drawers = 150-250ms; route transitions ≤ 400ms
- **Harmonic spring physics**: Mass m=1.0, near-critical damping (ζ ≈ 0.75-0.85); underdamped (ζ < 0.6) forbidden

### App Shell Isolation (2026)
- **Persistent elements**: Headers, sidebars, sticky controls pulled out of `root` transition group via unique `viewTransitionName`
- **Single smooth-scroll engine**: Strictly prohibit Lenis + Locomotive Scroll simultaneously; exactly one coordinator

### Reduced Motion Compliance (2026)
- **Mandatory `@media (prefers-reduced-motion: reduce)`**: Disable or instant-fade all animations
- **WCAG 2.2 AA**: Motion reduction compliance across all view transitions

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Composited motion mentioned | **Composited motion mandatory**: Only `transform`/`opacity`; layout property animations rejected in code review |
| Animation budget mentioned | **Frequency-based budget mandatory**: Hotkeys 0ms, micro 100-150ms, overlays 150-250ms, routes ≤400ms |
| Spring physics mentioned | **Harmonic springs mandatory**: m=1.0, ζ≈0.75-0.85; ζ<0.6 forbidden |
| Scroll engine mentioned | **Single coordinator mandatory**: Exactly one (Lenis or native CSS); race conditions prohibited |
| INP budget mentioned | **INP < 200ms with 50ms DOM mutation limit**: `React.startTransition` + `scheduler.yield()` for chunking |
| `default="none"` mentioned | **`default="none"` discipline mandatory**: All `<ViewTransition>` boundaries explicitly opt-in |
| Reduced motion mentioned | **Reduced motion fallback mandatory**: `@media (prefers-reduced-motion: reduce)` in every transition stylesheet |

### 2. New 2026 Patterns to Add
- **React 19 `<ViewTransition>` Integration**: Type-keyed boundaries, `default="none"`, pre-DOM-node placement
- **Shared Element Morphing**: Dynamic `name={`entity-hero-${id}`}`, `share="morph"`, fallback `enter`/`exit` classes
- **Directional Route Transitions**: `addTransitionType` (`nav-forward`/`nav-back`) with `startTransition`
- **Suspense Reveal Transitions**: Skeleton → content without layout jumps
- **Layout Displacement Morphs**: Dynamic list add/remove/reorder animations
- **Performance Verification**: INP/LCP/CLS under 4x CPU throttling; 60/120fps compositor verification
- **Security Validation**: `view-transition-name` sanitization against CSS injection; transition type allowlist

### 3. Checklist Additions
- [ ] View transitions animate exclusively composited properties (`transform`, `opacity`)
- [ ] Interaction to Next Paint verified under budget (INP < 200ms under 4x CPU throttling)
- [ ] All targeted `<ViewTransition>` boundaries declare `default="none"`
- [ ] `<ViewTransition>` components placed before any host DOM nodes
- [ ] `name` attributes for shared elements dynamically scoped and globally unique
- [ ] Persistent headers/navigation/sidebars isolated with unique `viewTransitionName`
- [ ] `@media (prefers-reduced-motion: reduce)` overrides verified in browser
- [ ] Hierarchical navigations mapped with typed directional transitions (`nav-forward`/`nav-back`)
- [ ] Fallback animations defined for shared elements when matching target absent
- [ ] Frequency-based animation budget enforced (hotkeys 0ms, micro 100-150ms, overlays 150-250ms, routes ≤400ms)
- [ ] Harmonic spring physics: mass 1.0, damping 0.75-0.85
- [ ] Single smooth-scroll engine (Lenis or native CSS) — not both
- [ ] Security: `view-transition-name` sanitized; transition types allowlisted
- [ ] `performance-audit.json` and `implementation-result.json` emitted and validated

### 4. Failure Mode Additions
- **Layout thrashing from CSS property animation**: `height`/`width` animated during transition. Mitigation: Code review rejects layout animations; replace with scale/translate transforms.
- **Duplicate `view-transition-name` collision**: Two active items render `name="hero-image"`. Mitigation: Require dynamic ID parameterization (`name={`hero-${id}`}`).
- **Unintended global crossfade**: Unconfigured `<ViewTransition>` fades on background revalidation. Mitigation: Enforce `default="none"` on all boundaries.
- **Persistent header jump**: Sticky nav stretches/slides during page change. Mitigation: Pull header into independent transition group via `viewTransitionName: "header"`.
- **Spring physics violation**: Underdamped cartoonish bouncing (ζ < 0.6). Mitigation: Design system enforces ζ ≈ 0.75-0.85; lint rule for spring config.
- **INP budget breach**: DOM mutation > 50ms inside `startViewTransition`. Mitigation: `React.startTransition` + `scheduler.yield()` chunking; profile with 4x CPU throttling.
- **CSS injection via `view-transition-name`**: Unescaped string interpolation. Mitigation: Sanitize dynamic names against pattern; reject unsafe characters.

### 5. Output Contract Updates
- Update `contracts/schemas/ui-component-spec.json` with transition boundaries, names, triggers, type maps
- Update `contracts/schemas/performance-audit.json` with INP, LCP, CLS, compositor frame-rate measurements
- Update `contracts/schemas/implementation-result.json` with CSS recipes, behavioral test evidence

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Composited motion only enforcement (code review gate) | High |
| P0 | Frequency-based animation budget with harmonic springs | High |
| P0 | React 19 `<ViewTransition>` with `default="none"` discipline | High |
| P0 | Shared element morphing with dynamic unique names | High |
| P0 | INP < 200ms with 50ms DOM mutation limit | High |
| P1 | Directional route transitions (`nav-forward`/`nav-back`) | Medium |
| P1 | App shell isolation (persistent elements) | Medium |
| P1 | Suspense reveal transitions (skeleton → content) | Medium |
| P1 | Layout displacement morphs (list add/remove/reorder) | Medium |
| P1 | Reduced motion fallback in every transition stylesheet | Medium |
| P2 | Security validation for dynamic names | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Benchmark INP/LCP/CLS under 4x CPU throttling with view transitions
- Verify `default="none"` on all `<ViewTransition>` boundaries
- Verify `<ViewTransition>` wraps content before DOM nodes
- Verify unique dynamic `view-transition-name` for shared elements
- Verify persistent elements isolated from root transition group
- Verify `@media (prefers-reduced-motion: reduce)` disables animations
- Verify harmonic spring physics (mass 1.0, damping 0.75-0.85)
- Verify single smooth-scroll engine (no Lenis + Locomotive conflict)
- Security test: `view-transition-name` sanitization against CSS injection