# setup-design-system — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Tailwind v4 CSS-First Configuration (2026)
- **`@theme` in CSS entrypoints**: Define all design tokens inside `@theme` — do NOT maintain `tailwind.config.js`
- **OKLCH perceptual color space**: Unified color palette with uniform contrast and predictable lightness across light/dark modes
- **CSS variable mapping for dark mode**: FORBID manual `dark:bg-*` / `dark:text-*` overrides; dark mode exclusively through `:root` and `.dark` CSS variable mapping

### W3C DTCG Token Format (2026)
- **Design Token Community Group format**: `{ "$value": ..., "$type": ... }` JSON for interoperability
- **Figma Variables + Style Dictionary + AI tools**: Token portability across design/engineering/AI
- **Functional naming**: `primary-500`, `text-foreground`, `border-border` — NOT `light-blue`, `#...` hex values

### GenUI Governance (2026)
- **AI component token conformance**: Verify (a) consumes design tokens, (b) forwards refs correctly, (c) includes required ARIA, (d) no duplicate class patterns
- **Automated axe-devtools scan**: Color contrast, screen reader labels, keyboard navigation
- **CSS pollution prevention**: Strip custom/inline/non-repo CSS files and rules
- **Peer review mandatory**: All AI-generated components reviewed for code style and safety
- **Treat as untrusted**: Every AI-generated component untrusted until passes conformance, a11y, visual regression

### Accessibility Integration (2026)
- **WCAG AA contrast check**: 4.5:1 text, 3:1 UI controls — before finalizing any token palette
- **Storybook 8+ with `a11y` + `chromatic` addons**: Mandatory CI gates
- **Primitives support accessibility by default**: ARIA attributes, semantic HTML, high contrast tokens

### Component Architecture (2026)
- **shadcn/ui v2 model**: Own component source under `src/components/ui/` — avoid black-box NPM bundles
- **`cn()` utility**: `clsx` + `tailwind-merge` on all component root elements
- **React 19 form actions**: `useActionState` for standard mutations
- **Headless UI libraries**: Radix UI, Headless UI for complex accessibility patterns

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Tailwind config mentioned | **Tailwind v4 `@theme` in CSS mandatory**: No `tailwind.config.js`; all tokens in CSS entrypoints |
| OKLCH mentioned | **OKLCH perceptual color space mandatory**: Uniform contrast, predictable lightness light/dark |
| Dark mode CSS variables | **Manual `dark:` overrides FORBIDDEN**: Dark mode exclusively via `:root` / `.dark` CSS variable mapping |
| DTCG format mentioned | **W3C DTCG format mandatory**: `{ "$value": ..., "$type": ... }` for Figma/Style Dictionary/AI interop |
| GenUI governance basic | **Full AI governance pipeline**: Token conformance + axe-devtools + CSS strip + peer review + visual regression |
| Storybook mentioned | **Storybook 8+ with `a11y` + `chromatic` mandatory CI gates** |
| shadcn model mentioned | **shadcn/ui v2 model**: Own source under `src/components/ui/`; no black-box NPM bundles |
| WCAG contrast | **WCAG AA check before token finalization**: 4.5:1 text, 3:1 UI controls |

### 2. New 2026 Patterns to Add
- **Tailwind v4 `@theme` Migration**: Move all tokens from `tailwind.config.js` to CSS `@theme` directive
- **OKLCH Palette Generation**: Brand guidelines → OKLCH tokens with uniform contrast ratios
- **CSS Variable Dark Mode**: `:root` + `.dark` mapping; remove all `dark:` utility overrides from components
- **DTCG Export Pipeline**: Tokens → DTCG JSON → Figma Variables / Style Dictionary / AI tools
- **GenUI CI Pipeline**: Token conformance lint → axe-devtools scan → CSS pollution check → Chromatic baseline → peer review
- **Storybook 8+ Configuration**: `a11y` addon, `chromatic` with TurboSnap, CI gate on visual regression
- **shadcn/ui v2 Component Structure**: `src/components/ui/` ownership; `cn()` utility; Radix/Headless UI primitives
- **Semantic Token Layer Enforcement**: Lint rule banning raw hex/color names in components; require semantic aliases

### 3. Checklist Additions
- [ ] Design tokens (colors, spacing, typography) defined in CSS `@theme` (Tailwind v4) or DTCG JSON
- [ ] Token naming convention functional (`primary-500`, `text-foreground`) — not implementation-specific (`light-blue`)
- [ ] OKLCH perceptual color space used for palette; uniform contrast verified
- [ ] Dark mode exclusively via `:root` / `.dark` CSS variable mapping; zero `dark:` utility overrides in components
- [ ] Styling framework configured to use centralized design tokens
- [ ] Global resets and base styles applied
- [ ] Foundational UI primitives built consuming token system (`src/components/ui/`)
- [ ] Primitives support standard accessibility (ARIA, refs, props spread, Radix/Headless UI)
- [ ] `cn()` utility (`clsx` + `tailwind-merge`) on all component root elements
- [ ] Linting rules enforce token usage: `eslint-plugin-tailwindcss`, Stylelint, `@design-tokens/eslint-plugin`
- [ ] WCAG contrast check passes for ALL color token pairs (4.5:1 text, 3:1 UI controls)
- [ ] Storybook 8+ initialized with `a11y` addon; all primitive states documented
- [ ] Chromatic/TurboSnap configured for visual regression baseline (CI gate)
- [ ] GenUI governance: AI component token conformance + axe-devtools + CSS strip + peer review + visual baseline
- [ ] W3C DTCG format exported for Figma Variables / Style Dictionary / AI tool interop
- [ ] Token format declared in `implementation-result.json` (CSS variables / Tailwind / DTCG JSON / styled-components)
- [ ] `implementation-result.json` emitted with validation run confirming token conformance, a11y, visual regression

### 4. Failure Mode Additions
- **Tailwind v4 migration incomplete**: `tailwind.config.js` still referenced. Mitigation: Codemod to `@theme` in CSS; lint rule banning `tailwind.config.js` imports.
- **OKLCH contrast failure**: Token pair fails WCAG AA. Mitigation: Automated contrast check in token pipeline; fail tokens below 4.5:1/3:1.
- **Manual `dark:` override leakage**: Component uses `dark:bg-*`. Mitigation: Lint rule banning `dark:` utilities on core surfaces; require semantic token mapping.
- **DTCG export missing**: Tokens not portable to Figma/AI. Mitigation: CI step exporting DTCG JSON; verify import in Figma Variables.
- **AI component merged without governance**: Token violation, missing ARIA, CSS pollution. Mitigation: GenUI CI pipeline mandatory; reject without all gates passing.
- **Storybook a11y addon disabled**: Stories missing ARIA. Mitigation: Require a11y addon in Storybook config; fail stories with missing ARIA.
- **Visual regression baseline missing**: AI component lands without baseline. Mitigation: Require Chromatic/Percy baseline; reject merges without passing baseline.
- **CSS leakage**: Component styles leak to global scope. Mitigation: Per-component style namespace; reject unscoped global selectors.
- **Black-box NPM UI bundle**: Component from opaque package. Mitigation: Require source ownership under `src/components/ui/`; reject uncustomizable bundles.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: token format, styling framework, component library, documentation, linting gates, WCAG results, GenUI pipeline status

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Tailwind v4 `@theme` migration (no `tailwind.config.js`) | High |
| P0 | OKLCH perceptual color space with uniform contrast | High |
| P0 | Manual `dark:` overrides forbidden (CSS variable dark mode) | High |
| P0 | W3C DTCG token export pipeline | High |
| P0 | GenUI governance CI pipeline (token, axe, CSS, Chromatic, review) | High |
| P1 | Storybook 8+ with `a11y` + `chromatic` mandatory CI gates | High |
| P1 | shadcn/ui v2 model (`src/components/ui/` ownership) | Medium |
| P1 | Semantic token layer enforcement (lint rule) | Medium |
| P1 | WCAG AA contrast check before token finalization | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Verify `tailwind.config.js` not imported anywhere
- Run OKLCH contrast check on all token pairs (4.5:1 text, 3:1 UI)
- Lint rule catches `dark:` utility overrides in components
- DTCG JSON exports valid for Figma Variables import
- GenUI CI pipeline: token conformance → axe-devtools → CSS strip → Chromatic → review
- Storybook 8+ `a11y` addon runs on all stories; zero violations
- Chromatic/TurboSnap baseline passes for all primitives
- Visual regression CI gate blocks on diff