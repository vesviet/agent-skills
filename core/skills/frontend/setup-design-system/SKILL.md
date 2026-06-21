---
name: setup-design-system
description: Configure a scalable design system, styling framework, and component architecture for a frontend project. Use when initializing a new project, migrating to a unified CSS strategy, or setting up a component library (e.g., Tailwind, Storybook, Radix).
---

# Setup Design System

Use this skill when configuring the foundational styling architecture, design tokens, and component infrastructure of a frontend repository. This goes beyond adding a single component—it establishes the rules by which all future components will be built.

## Core Rules

- **Source of Truth**: Establish a single source of truth for design tokens (colors, typography, spacing) and do not allow hardcoded magic values in components.
- **Consistency**: Enforce a unified styling approach (e.g., utility-first like Tailwind, CSS Modules, or CSS-in-JS) and reject mixed paradigms without clear boundaries.
- **Accessibility Integration**: Design system primitives must support accessibility (ARIA attributes, semantic HTML, high contrast tokens) by default.
- **Maintainability**: Provide clear documentation or guidelines on how to consume the design tokens and base components.

## Suggested Process

### 1. Define Design Tokens
- Map brand guidelines to technical design tokens (CSS variables, Tailwind config, or theme objects).
- Define a strict naming convention for colors (e.g., functional names like `primary-500`, `text-muted` rather than `light-blue`).
- Establish spacing, typography, and breakpoint scales.

### 2. Configure the Styling Framework
- Initialize the chosen styling framework (e.g., `tailwind.config.js`, Sass variables, styled-components theme).
- Wire the defined design tokens into the framework.
- Configure global CSS resets and base styles.

### 3. Build Foundational Primitives
- Create the lowest-level UI primitives (e.g., Buttons, Inputs, Layout wrappers) that consume the design system tokens.
- Ensure these primitives expose standard native attributes (forwarding refs, spreading props).
- Integrate headless UI libraries (e.g., Radix UI, Headless UI) if complex accessibility patterns are required.

### 4. Setup Component Documentation (Optional but Recommended)
- Initialize a component workspace or documentation tool like Storybook.
- Write stories/examples for the foundational primitives to demonstrate states (default, hover, disabled, active).

### 5. Validate the Architecture
- Verify that standard linting rules (like Prettier, Stylelint, or `eslint-plugin-tailwindcss`) are configured to enforce the styling standards.
- Test token updates to ensure changes cascade correctly throughout the application.

## Checklist

- [ ] design tokens (colors, spacing, typography) are defined and centralized
- [ ] styling framework is configured to use the centralized design tokens
- [ ] global resets and base styles are applied
- [ ] foundational UI primitives are built and consume the token system
- [ ] primitives support standard accessibility patterns natively
- [ ] linter or formatter is configured to enforce styling consistency
- [ ] component usage documentation (or Storybook) is initialized (if applicable)

## Related Skills

- **add-ui-component**: Add or evolve a reusable UI component using the design system established by this skill.
- **frontend-testing**: Add visual regression or interaction tests for the design system primitives.
- **accessibility-review**: Audit the foundational primitives to ensure they meet WCAG criteria.
