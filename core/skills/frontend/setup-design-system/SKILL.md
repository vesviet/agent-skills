---
name: setup-design-system
description: Configure a scalable design system, styling framework, and component architecture for a frontend project. Use when initializing a new project, migrating to a unified CSS strategy, or setting up a component library (e.g., Tailwind, Storybook, Radix).
---

# Setup Design System

Use this skill when configuring the foundational styling architecture, design tokens, and component infrastructure of a frontend repository. This goes beyond adding a single component — it establishes the rules by which all future components will be built.

## When to Use

- initializing a new frontend project's styling
- migrating to a unified CSS strategy
- setting up a component library (Tailwind, Radix, Storybook)
- standardizing design tokens across the app

## Core Rules

- **Source of Truth:** define all design tokens inside `@theme` in CSS entrypoints (Tailwind v4 CSS-first config) or DTCG `{ "$value": ..., "$type": ... }` JSON format — do not maintain `tailwind.config.js` in Tailwind v4 projects
- **Consistency:** enforce a unified styling approach and reject mixed paradigms; use OKLCH perceptual color space for palette tokens to ensure uniform contrast and predictable color transitions
- **Semantic Token Layering:** components must consume semantic aliases (`--color-surface-primary`, `--color-text-body`) rather than raw primitive color names (`--color-blue-500`); use `:root` for CSS variables not needing utility mapping
- **Accessibility Integration:** design system primitives must support accessibility (ARIA attributes, semantic HTML, high contrast tokens) by default; run WCAG AA contrast check (4.5:1 text, 3:1 UI controls) before finalizing any token palette
- **Maintainability:** provide clear documentation on how to consume design tokens and base components; Storybook 8+ with `a11y` and `chromatic` addons as mandatory CI gates
- **Token Portability:** use W3C DTCG format for interoperability with Figma Variables, Style Dictionary, and AI-driven design tools
- **GenUI Governance:** AI-generated components (v0, Copilot, Lovable) must pass token conformance check before merge — no hardcoded hex values, px overrides, or shadow DOM leakage; verify the component (a) consumes design tokens, (b) forwards refs correctly, (c) includes required ARIA attributes, (d) does not introduce duplicate class patterns
- treat every AI-generated component as untrusted until it passes the token conformance, accessibility, and visual regression checks (OWASP ASI04)
- never include customer PII or auth tokens in design tokens, storybook stories, or Chromatic baselines (OWASP ASI03)
- enforce the W3C DTCG format for token portability; reject non-portable token definitions that lock the system to a single tool

## Output Contracts

When the design system is consumed by downstream components, a Storybook
deployment, or a multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output confirming token conformance, accessibility, and visual regression checks pass.
- For human-readable reports, the markdown design system setup summary already documented is the canonical format.
- The token format (CSS variables, Tailwind `@theme`, DTCG JSON, or styled-components) must be declared in the result so downstream agents know how to consume the tokens.

Skip emission for solo design system experiments that do not cross a role boundary.

## Failure Modes

- **Hardcoded values in components**: a component bypasses the design tokens with raw hex or magic numbers. Mitigation: enforce token usage via lint rules (`eslint-plugin-tailwindcss`, Stylelint, or `@design-tokens/eslint-plugin`); reject components that fail the lint.
- **Mixed styling paradigms**: utility-first and CSS-in-JS coexist without a clear boundary. Mitigation: enforce a unified approach; reject mixed paradigms.
- **Token names implementation-specific**: tokens use names like `light-blue` instead of functional names like `primary-500`. Mitigation: enforce functional naming; reject implementation-specific names.
- **No contrast check**: a color token pair fails WCAG AA contrast. Mitigation: run a WCAG contrast check on all color token pairs; fail tokens below 4.5:1 text or 3:1 UI controls.
- **AI component without conformance check**: an AI-generated component is merged without the token conformance check. Mitigation: require the GenUI review checklist in CONTRIBUTING.md; reject components without the review.
- **Visual regression baseline missing**: AI-generated components land without a visual baseline. Mitigation: require Chromatic or Percy baseline; reject merges without a passing baseline.
- **Accessibility addon skipped**: the Storybook a11y addon is disabled. Mitigation: require the a11y addon in the Storybook config; fail stories with missing ARIA.
- **CSS leakage**: a component's styles leak into global scope. Mitigation: enforce per-component style namespace; reject unscoped global selectors.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include customer PII, auth tokens, or sensitive identifiers in design tokens, storybook stories, or Chromatic baselines.
- **ASI04 Supply Chain**: AI-generated components must be schema-validated against the design system contract; treat unknown component patterns as untrusted.
- **ASI05 RCE Guard**: never construct token values, theme objects, or component variants from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the design system spec is consumed by every downstream component; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated component as "production-ready" without the conformance, accessibility, and visual regression checks; surface the AI provenance honestly.

## Suggested Process

### 1. Define Design Tokens
- Map brand guidelines to technical design tokens (CSS variables, Tailwind config, or DTCG-format theme objects).
- Define a strict naming convention for colors (functional names like `primary-500`, `text-muted` rather than `light-blue`).
- Establish spacing, typography, and breakpoint scales.
- Export tokens to a format readable by both engineering (CSS variables) and design (Figma Variables or tokens JSON).

### 2. Configure the Styling Framework
- Initialize the chosen styling framework (`tailwind.config.js`, Sass variables, styled-components theme).
- Wire the defined design tokens into the framework.
- Configure global CSS resets and base styles.
- Set up linting rules to enforce token usage: `eslint-plugin-tailwindcss`, Stylelint custom rules, or `@design-tokens/eslint-plugin`.

### 3. Build Foundational Primitives
- Create the lowest-level UI primitives (Buttons, Inputs, Layout wrappers) that consume the design system tokens.
- Ensure these primitives expose standard native attributes (forwarding refs, spreading props).
- Integrate headless UI libraries (Radix UI, Headless UI) if complex accessibility patterns are required.
- Add variant props using a type-safe pattern (cva, Tailwind Variants, or similar) rather than string unions.

### 4. Set Up Component Documentation
- Initialize Storybook or equivalent with the `a11y` addon enabled.
- Write stories for foundational primitives covering: default, hover, focus, disabled, error states.
- Configure Chromatic or Percy for visual regression baseline (especially important if AI tooling generates components).

### 5. Validate the Architecture
- Run linting rules to confirm no hardcoded values in primitives.
- Run the accessibility addon against all stories — fail any component with missing ARIA or contrast violations.
- Run a WCAG color contrast check on all color token pairs.

## Output Format

```markdown
## Design System Setup — <Project Name>

Token format: [CSS variables / Tailwind / DTCG JSON / styled-components]
Styling framework: [Tailwind / CSS Modules / CSS-in-JS / Sass]
Component library: [Radix / Headless UI / custom / none]
Documentation: [Storybook / none]

### Token Architecture
- Color: <naming convention and scale>
- Spacing: <scale>
- Typography: <scale>

### Linting Gates
- [ ] Token-enforcement lint rule configured
- [ ] Stylelint or eslint-plugin-tailwindcss active
- [ ] WCAG contrast check passing for all color token pairs

### AI Governance (2025-2026)
- [ ] GenUI token conformance check defined
- [ ] AI-generated component review checklist added to CONTRIBUTING.md
- [ ] Storybook a11y + visual regression CI gate active

### Residual Decisions
- <any token or framework choice deferred>
```

## Anti-Patterns To Reject

- hardcoding hex values in components instead of consuming design tokens
- mixing utility-first and CSS-in-JS styling without explicit boundary rules
- accepting AI-generated components without verifying token conformance and accessibility
- skipping visual regression baseline — AI-generated components frequently have missing states
- defining tokens with implementation-specific names (`light-blue`) instead of functional names (`primary-500`)

## Checklist

- [ ] design tokens (colors, spacing, typography) defined and centralized
- [ ] token naming convention is functional, not implementation-specific
- [ ] styling framework configured to use the centralized design tokens
- [ ] global resets and base styles applied
- [ ] foundational UI primitives built and consume the token system
- [ ] primitives support standard accessibility patterns natively (ARIA, refs, props spread)
- [ ] linter or formatter configured to enforce token usage and styling consistency
- [ ] WCAG color contrast check passes for all token color pairs
- [ ] Storybook or equivalent initialized with a11y addon and all primitive states documented
- [ ] AI-generated component review process defined (2025-2026)
## Related Skills

- **add-ui-component**: Add or evolve a reusable UI component using the design system established by this skill.
- **frontend-testing**: Add visual regression or interaction tests for the design system primitives.
- **accessibility-review**: Audit the foundational primitives to ensure they meet WCAG criteria.
- **design-review**: Validate design token choices against brand guidelines and user needs before implementation.

