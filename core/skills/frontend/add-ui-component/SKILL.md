---
name: add-ui-component
description: Add or evolve a reusable UI component by following the repo's design system, composition patterns, accessibility rules, and state boundaries. Use when building frontend components or shared presentation elements.
---

# Add UI Component

Use this skill when a frontend change needs a new reusable component or a meaningful update to an existing one.

## When to Use

- building a new reusable UI component
- evolving a shared presentation element
- following the design system + a11y rules
- defining component state boundaries

## Core Rules

- follow the repo's existing design system before inventing a new pattern
- prefer composition over one-off duplication — use compound component patterns (`Dialog.Root`, `Dialog.Content`) over prop-soup mega-components with dozens of boolean flags
- base interactive components on headless accessibility primitives (Radix UI, Base UI, Ark UI) for WAI-ARIA roles, keyboard focus management, and escape key handling — do not reinvent focus trap logic
- own component source under `src/components/ui/` (shadcn/ui v2 model); avoid black-box NPM UI bundles that cannot be customized or tree-shaken
- apply `cn()` utility (clsx + tailwind-merge) to all component root elements for safe Tailwind class merging without specificity conflicts
- keep accessibility, semantics, and keyboard behavior explicit
- keep styling and state responsibilities narrow and understandable
- consider performance impact: bundle size, lazy loading, and layout shift (CLS)
- prefer React 19 form actions and `useActionState` for standard form mutations over heavy client-side form wrappers
- update visual or interaction tests when the component contract changes
- if any code in this change was AI-generated, validate it per the risk tier defined in the frontend-developer role before accepting

## Suggested Process

### 1. Inspect A Similar Component

Find a nearby component that matches:

- visual hierarchy
- state complexity
- prop or input pattern
- styling system
- test approach

### 2. Define The Component Contract

Require or construct a **UI Component Spec** (via `contracts/schemas/ui-component-spec.json`). When a parent **UX Flow Spec** exists (`contracts/schemas/ux-flow-spec.json`), match `flow_id` and honor `component_spec_refs`. Clarify:

- what the component renders
- what inputs it accepts
- what events or callbacks it emits
- what states it must support
- whether it is presentational, stateful, or compositional

### 3. Build The Smallest Useful Version

Start with:

- semantic structure
- the main visual state
- required interactions
- loading, empty, error, or disabled states if relevant

Avoid prematurely adding variant complexity the first consumer does not need.

### 4. Integrate Styling And Accessibility

Check:

- semantic element choice
- focus behavior
- keyboard support
- aria labels or relationships where needed
- responsive behavior in the repo's style system

### 5. Connect State Carefully

If the component needs state:

- keep transient UI state local when possible
- avoid reaching directly into global state unless the repo expects it
- separate data fetching from pure presentation when the repo uses that pattern

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- render behavior
- important interaction paths
- accessibility-sensitive states
- prop or slot/children variations that are easy to break

## 2026 Component Architecture

### 2026: RSC Boundary Placement Leaf Pattern
- Push the "use client" directive as deep down the React component tree as possible (the leaf pattern) to maximize Server-side rendering (SSR) benefits.
- Keep React Server Components (RSC) at the top of the tree, and pass Interactive Client Components down as children or props into those Server Components.
- Minimize the amount of client-side state managed high up in the component tree to avoid unnecessary re-renders.

### 2026: AI-Generated Component Governance Checklist
- Verify that AI-generated UI components conform strictly to existing design tokens and color scales.
- Run an automated axe-devtools scan to catch color contrast, screen reader labels, and keyboard navigation issues.
- Strip any custom, inline, or non-repository CSS files and rules to prevent style pollution.
- Conduct a peer code review on all generated components to ensure they meet project code style and safety standards.

### 2026: Lit v3 Web Components Bridging
- Wrap Lit v3 Web Components in a React wrapper using the `@lit/react` library to expose them cleanly as React components.
- Ensure that properties, events, and lifecycle hooks are mapped correctly to React props and callbacks.
- Verify component cleanup and event listener detachment are executed correctly when components unmount.

## Checklist

- [ ] similar component pattern reviewed
- [ ] component contract defined
- [ ] accessibility and semantics checked
- [ ] state boundaries kept clear
- [ ] styling follows local system
- [ ] performance impact considered (bundle size, lazy loading, CLS)
- [ ] tests added or updated
- [ ] `implementation-result.json` emitted for the change slice (see Output Contracts)

## Failure Modes

- **Token hardcoding**: a component bypasses the design system with raw values. **Mitigation:** enforce token-enforcement lint rules; reject components that fail the lint.
- **AI component without conformance check**: an AI-generated component is merged without the GenUI review. **Mitigation:** require the review checklist; reject components without the review.
- **Visual regression baseline missing**: a UI change ships without a visual baseline. **Mitigation:** require a Chromatic or Percy baseline; reject merges without a passing baseline.
- **Critical state missing**: a component omits one of the required UI states. **Mitigation:** enforce the state checklist; reject specs that skip a state.

## Output Contracts

When this skill runs inside a coordinated slice planned by Technical Lead or gated by Reviewer, emit:

- **`contracts/schemas/implementation-result.json`** — one artifact per change slice. Include `change_summary`, `files_touched[]`, `components_added[]` with props/events summary, `tests_added[]`, `preserved_behavior[]` (call out a11y semantics, layout shifts, or public prop surface kept unchanged), `validation_run` (commands + result). Reference any `ui-component-spec.json` consumed from UI/UX Designer so downstream roles can trace spec-to-code fidelity.

Skip emission for solo exploratory UI work with no planned handoff.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-generated component may try to reframe the user goal through off-brand copy or behavior. Cross-check the component against the source feature ticket.
- **ASI04 Supply Chain**: AI component generators, UI libraries, and dependency versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct component variants, props, or styles from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the component contract is consumed by design system and Storybook agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated component as "production-ready" without the conformance, accessibility, and visual regression checks; surface the AI provenance honestly.

## Related Skills

- **add-page-route**: Place the new component into a page or route flow
- **integrate-api-client**: Connect UI state to backend data safely
- **frontend-testing**: Add UI and interaction coverage
- **review-code**: Review accessibility and maintainability risk
- **design-ux-flow**: Upstream ux-flow-spec and ui-component-spec from UI/UX Designer
- **commit-code**: Prepare the component change for delivery
