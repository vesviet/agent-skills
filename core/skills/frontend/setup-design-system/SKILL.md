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

- **Source of Truth:** establish a single source of truth for design tokens (colors, typography, spacing) and do not allow hardcoded magic values in components.
- **Consistency:** enforce a unified styling approach (e.g., utility-first like Tailwind, CSS Modules, or CSS-in-JS) and reject mixed paradigms without clear boundaries.
- **Accessibility Integration:** design system primitives must support accessibility (ARIA attributes, semantic HTML, high contrast tokens) by default.
- **Maintainability:** provide clear documentation or guidelines on how to consume design tokens and base components.
- **Token Portability:** prefer token formats that can be exported or consumed by multiple tools (design, code, documentation); avoid coupling tokens to a single framework's runtime.

### 2025-2026: GenUI Governance and W3C Design Token Standard

- **W3C Design Token Community Group (DTCG) format is the emerging standard (2024-2025):** use `{ "$value": ..., "$type": ... }` format for token definitions when setting up a new token system — this enables interoperability with Figma Variables, Style Dictionary, and AI-driven design tools.
- **GenUI governance:** when AI tools generate UI components (Copilot, v0, Lovable, Cursor), require each generated component to pass the design system's token conformance check before merge — no hardcoded hex values, px overrides, or shadow DOM leakage from AI-generated markup.
- **AI-generated component review checklist:** verify that AI-generated primitives (a) consume design tokens instead of magic values, (b) forward refs correctly, (c) include required ARIA attributes, and (d) do not introduce duplicate or conflicting class utility patterns.
- **Token audit gate:** before finalizing a new design system setup, run a token audit to ensure color contrast ratios meet WCAG AA (4.5:1 for normal text, 3:1 for large text) — many AI-generated palettes fail this check.
- **Storybook AI integration:** if using Storybook 8+, configure the `a11y` and `chromatic` addons as mandatory CI gates — AI-generated components frequently ship with missing interactive states (focus, hover, disabled) that only visual regression testing catches.

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

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, iles_touched[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **add-ui-component**: Add or evolve a reusable UI component using the design system established by this skill.
- **frontend-testing**: Add visual regression or interaction tests for the design system primitives.
- **accessibility-review**: Audit the foundational primitives to ensure they meet WCAG criteria.
- **design-review**: Validate design token choices against brand guidelines and user needs before implementation.

