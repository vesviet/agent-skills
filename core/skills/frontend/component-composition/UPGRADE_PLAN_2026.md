# component-composition — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### React 19 Idioms (Mandatory 2026)
- **No `forwardRef`**: Pass `ref` as standard prop in React 19
- **`use(Context)` instead of `useContext()`**: Direct context reading
- **`<Context value={...}>` instead of `<Context.Provider>`**: Simplified provider syntax
- **`useId()` for deterministic IDs**: Label/description/error linking compatible with Server Actions
- **Server Actions compatible forms**: `useActionState`, `useOptimistic`, `<form action={...}>`

### shadcn v4 Form Architecture (2026)
- **`FieldGroup` + `Field`**: Replace legacy v3 nested `FormItem`/`FormControl` boilerplate
- **React 19 `useId()`**: Deterministic label, description, error linking
- **`InputGroup`**: Prefix/suffix addons, action buttons, dropdowns with unified flex containers and `:focus-within` rings

### Compound Component Evolution (2026)
- **Base UI `render` prop vs Radix `asChild`**: Use Base UI `render` prop when children need internal headless state injection or polymorphic tags; Radix `asChild` (`Slot`) for single-child delegation without state projection
- **Context interface facets**: `{ state, actions, meta }` — read-only data, callbacks/mutations, references (DOM refs, unique IDs, active indices)
- **Headless hooks extraction**: `useDialog`, `useDropdown` returning `{ state, actions, triggerProps, contentProps }` with keyboard bindings (Escape, Enter, Arrows) and ARIA attributes

### Anti-Boolean Prop Sprawl Enforcement (2026)
- **Strict ban**: Boolean flags toggling internal layout (`isThread`, `hasBadge`, `isHeader`, `withIcon`, `isLoadingModal`) — max 2 booleans for purely stylistic states
- **Compound component replacement**: `Component.Root`, `Component.Trigger`, `Component.Content`, `Component.Close`
- **Explicit pre-composed variants**: `ThreadComposer`, `ChannelComposer` for common use cases

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| React 19 idioms mentioned | **React 19 idioms mandatory**: No `forwardRef`, `use(Context)`, `<Context value>`, `useId()` for forms |
| shadcn v3 form layouts | **shadcn v4 `FieldGroup` + `Field`**: Replace legacy `FormItem`/`FormControl`; `useId()` for linking |
| Base UI vs Radix mentioned | **Decision framework**: Base UI `render` prop for state injection/polymorphic tags; Radix `asChild` for single-child delegation |
| Headless hooks mentioned | **Standardized headless hooks**: `useDialog`, `useDropdown` returning `{ state, actions, triggerProps, contentProps }` with keyboard/ARIA |
| Anti-boolean prop sprawl | **Max 2 booleans for stylistic states only**: Layout-altering booleans banned; compound refactor required |

### 2. New 2026 Patterns to Add
- **React 19 Migration Checklist**: `forwardRef` → standard `ref` prop; `useContext()` → `use(Context)`; `<Context.Provider>` → `<Context value>`; `useId()` for forms
- **shadcn v4 Form Migration**: `FieldGroup` + `Field` pattern with `useId()`; `InputGroup` for compound inputs
- **Context Interface Contract**: Three-facet interface (`state`, `actions`, `meta`) with TypeScript types
- **Headless Hook Library**: Reusable `useDialog`, `useDropdown`, `useCombobox`, `useTabs` with keyboard/ARIA
- **Base UI vs Radix Decision Tree**: When to use `render` prop (state injection, polymorphic) vs `asChild` (delegation)
- **Variant Composition Strategy**: Pre-composed variants for common cases; primitives for custom layouts

### 3. Checklist Additions
- [ ] Component avoids boolean prop proliferation; max <= 2 booleans for purely stylistic states
- [ ] Complex multi-region layout structured as compound component (`Root`, `Trigger`, `Content`, etc.)
- [ ] State management decoupled from UI via context provider interface (`state`, `actions`, `meta`)
- [ ] Interactive triggers support `asChild` slot delegation without illegal DOM wrapper nesting
- [ ] Event handlers and refs merged safely via `composeEventHandlers` and `composeRefs`
- [ ] Keyboard navigation and WAI-ARIA roles handled deterministically via headless hook or primitive
- [ ] **React 19 idioms used**: direct `ref` prop, `use(Context)` hook, `<Context value={...}>`, `useId()` for forms
- [ ] shadcn v4 `FieldGroup` + `Field` with `useId()` for form layouts
- [ ] `InputGroup` for compound inputs with `:focus-within` rings
- [ ] Base UI `render` prop used for state injection/polymorphic tags; Radix `asChild` for single-child delegation
- [ ] Headless hooks extracted: `useDialog`, `useDropdown` returning `{ state, actions, triggerProps, contentProps }`
- [ ] Explicit pre-composed variants provided for common high-frequency use cases
- [ ] Behavioral interaction tests verify compound composition and accessibility contracts
- [ ] `ui-component-spec.json` and `implementation-result.json` emitted and validated

### 4. Failure Mode Additions
- **React 19 migration incomplete**: `forwardRef` or `useContext()` remains in codebase. Mitigation: Codemod for `forwardRef` removal; lint rule for `use(Context)` vs `useContext()`.
- **shadcn v3 form legacy**: `FormItem`/`FormControl` boilerplate persists. Mitigation: Codemod for `FieldGroup`/`Field` migration; lint rule banning legacy form components.
- **Base UI/Radix misuse**: `render` prop used for simple delegation; `asChild` used when state injection needed. Mitigation: Decision tree in code review; documented pattern examples.
- **Headless hook state leakage**: Internal state exposed in hook return. Mitigation: Strict return type `{ state, actions, triggerProps, contentProps }`; no internal state exposure.
- **Context null pointer**: Subcomponent rendered outside Provider. Mitigation: Context consumer hook throws diagnostic error (`useComposerContext must be used within Composer.Provider`).
- **Event handler collision in slot**: Child `onClick` overwrites trigger `onClick`. Mitigation: Always `composeEventHandlers`; test with custom child components.
- **Ref forwarding broken in `asChild`**: Custom child loses ref binding. Mitigation: `composeRefs` supporting callback and object refs; test with `forwardRef` components.

### 5. Output Contract Updates
- Update `contracts/schemas/ui-component-spec.json` with: React 19 idiom compliance, shadcn v4 form pattern, context interface, headless hook signatures, Base UI/Radix decision

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | React 19 idioms migration (no `forwardRef`, `use(Context)`, `useId()`) | High |
| P0 | shadcn v4 `FieldGroup` + `Field` form migration | High |
| P0 | Anti-boolean prop sprawl enforcement (max 2 stylistic) | High |
| P1 | Context interface contract (`state`, `actions`, `meta`) | Medium |
| P1 | Headless hook library standardization | Medium |
| P1 | Base UI `render` prop vs Radix `asChild` decision framework | Medium |
| P1 | Explicit pre-composed variants for common use cases | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test React 19 codemod removes all `forwardRef` and `useContext()`
- Verify shadcn v4 `FieldGroup`/`Field` renders with `useId()` linking
- Test Base UI `render` prop state injection vs Radix `asChild` delegation
- Verify headless hooks return correct interface with keyboard/ARIA
- Test context consumer throws diagnostic error outside Provider
- Test `composeEventHandlers`/`composeRefs` with custom children