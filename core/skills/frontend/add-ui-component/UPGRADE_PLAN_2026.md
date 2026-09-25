# add-ui-component — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### React 19 / RSC Component Architecture (2026)
- **RSC Leaf Pattern**: Push `"use client"` as deep as possible; maximize Server-side rendering
- **RSC at top, client leaves**: Interactive Client Components passed as children/props into Server Components
- **Minimize client-side state high in tree**: Avoid unnecessary re-renders
- **React 19 form actions**: `<form action={submitAction}>`, `useActionState` for standard mutations
- **`useOptimistic` hook**: Optimistic updates for data mutations

### AI-Generated Component Governance (2026)
- **Token Conformance Check**: Verify AI components consume design tokens (no hardcoded hex, px, shadow DOM leakage)
- **Automated axe-devtools Scan**: Color contrast, screen reader labels, keyboard navigation
- **CSS Pollution Prevention**: Strip custom/inline/non-repo CSS files and rules
- **Peer Code Review Mandatory**: All AI-generated components reviewed for code style and safety

### Lit v3 Web Components Bridging (2026)
- **`@lit/react` wrapper**: Expose Lit v3 Web Components cleanly as React components
- **Properties/events/lifecycle mapping**: Correct React props and callbacks mapping
- **Cleanup verification**: Event listener detachment on unmount

### Anti-Slop Component Mechanics (2026)
- **Full-height hero/banner**: ALWAYS enforce `min-h-[100dvh]` to avoid mobile viewport jumping
- **Continuous motion isolation**: NEVER use `useState` for pointer physics, scroll progress, mouse movement; bind to `motion/react` values (`useMotionValue`, `useTransform`)
- **Tactile feedback**: `:active` transform (`scale-[0.98]` or `-translate-y-[1px]`) on interactive elements
- **CTA label wrapping**: Primary CTA labels never wrap to multiple lines on desktop
- **Icon library restriction**: Approved only (@phosphor-icons/react, hugeicons-react, @radix-ui/react-icons); no hand-rolled SVG icons

### Composition Patterns (2026)
- **Compound Components**: `Dialog.Root`, `Dialog.Content`, `Dialog.Trigger` with Radix-style `asChild` slot delegation
- **shadcn v4 `FieldGroup` + `Field`**: Replace legacy `FormItem`/`FormControl` boilerplate
- **React 19 `useId()`**: Deterministic label/description/error linking compatible with Server Actions
- **`InputGroup`**: Prefix/suffix addons, action buttons, dropdowns with `:focus-within` rings

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| RSC leaf pattern mentioned | **RSC leaf pattern mandatory**: `"use client"` pushed as deep as possible; RSC at top |
| AI component governance basic | **Full AI governance**: Token conformance, axe-devtools scan, CSS pollution strip, peer review |
| Lit v3 bridging mentioned | **`@lit/react` wrapper mandatory**: Properties/events/lifecycle mapped; cleanup verified |
| Anti-slop mechanics basic | **Full anti-slop**: `min-h-[100dvh]`, motion/react for continuous values, `:active` transform, CTA no-wrap, approved icons only |
| Composition patterns | **shadcn v4 `FieldGroup`/`Field` + `useId()` + `InputGroup`**: Modern form layouts |

### 2. New 2026 Patterns to Add
- **RSC/Client Component Boundary**: Explicit boundary definition with `"use client"` at leaves
- **React 19 `useActionState` + `useOptimistic`**: Form mutations with pending state, optimistic updates
- **Server Actions Integration**: `<form action={serverFn}>` with progressive enhancement
- **Composite Components**: Server UI with client slots (TanStack Start pattern)
- **Motion/React for Continuous Values**: `useMotionValue`, `useTransform` instead of `useState`
- **Approved Icon Library Enforcement**: Lint rule restricting to @phosphor-icons, hugeicons, @radix-ui/react-icons
- **`min-h-[100dvh]` for Hero Sections**: Lint rule for full-height components
- **`:active` Transform Requirement**: Lint rule for interactive element tactile feedback

### 3. Checklist Additions
- [ ] Similar component pattern reviewed (RSC/client boundary aware)
- [ ] Component contract defined with RSC/client classification
- [ ] Accessibility and semantics checked (axe-devtools scan passes)
- [ ] State boundaries kept clear (client state only in `"use client"` components)
- [ ] Styling follows local system (design tokens, no hardcoded values)
- [ ] Anti-slop mechanics verified: `min-h-[100dvh]`, continuous motion on motion/react, tactile `:active`, no CTA wrapping, approved icons
- [ ] Performance impact considered (bundle size, lazy loading, CLS, RSC streaming)
- [ ] AI-generated component governance: token conformance, axe-devtools scan, CSS pollution stripped, peer review completed
- [ ] Lit v3 Web Components wrapped with `@lit/react` if used
- [ ] shadcn v4 `FieldGroup` + `Field` with `useId()` for forms
- [ ] `InputGroup` for compound inputs with `:focus-within` rings
- [ ] Tests: render, interactions, a11y states, prop/slot variations
- [ ] `implementation-result.json` emitted with component props/events summary

### 4. Failure Mode Additions
- **RSC boundary leak**: Client component imported in Server Component without `"use client"`. Mitigation: Lint rule enforcing `"use client"` at boundary; type-check import graph.
- **AI component token violation**: Hardcoded colors/spacing in AI-generated component. Mitigation: Automated token conformance check in CI; reject non-conforming.
- **Continuous motion on useState**: `useState` for scroll/pointer causing re-render storms. Mitigation: Lint rule banning `useState` for continuous values; require `motion/react`.
- **CSS pollution from AI**: Inline styles or custom CSS files in AI output. Mitigation: Automated strip of non-repo CSS; reject components with style leakage.
- **Lit v3 cleanup failure**: Event listeners not detached on unmount. Mitigation: `@lit/react` wrapper verification; test unmount cleanup.
- **CTA label wrapping**: Primary CTA wraps on desktop. Mitigation: Lint rule for `whitespace-nowrap` on primary CTA; visual regression test.
- **Hand-rolled SVG icons**: Custom SVG icons bypassing design system. Mitigation: Lint rule restricting to approved icon libraries.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: RSC/client classification, AI governance checks passed, anti-slop verification, icon library compliance

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | RSC leaf pattern enforcement (`"use client"` depth) | High |
| P0 | AI component governance pipeline (token, axe, CSS, review) | High |
| P0 | Anti-slop mechanics lint rules (`min-h-[100dvh]`, motion/react, `:active`, CTA, icons) | High |
| P1 | React 19 `useActionState` + `useOptimistic` integration | Medium |
| P1 | shadcn v4 `FieldGroup`/`Field` + `useId()` migration | Medium |
| P1 | `@lit/react` wrapper for Web Components | Medium |
| P1 | Composite Components (Server UI + client slots) | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test RSC boundary with `"use client"` at various depths
- Run axe-devtools scan on AI-generated components
- Verify `min-h-[100dvh]` on hero components across viewports
- Verify `motion/react` for continuous motion (no `useState` for scroll/pointer)
- Verify approved icon library restriction lint rule
- Test `@lit/react` wrapper unmount cleanup
- Test React 19 `useActionState` form with Server Function