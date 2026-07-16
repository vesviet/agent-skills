---
name: frontend-testing
description: Add or improve frontend test coverage by choosing the right UI test scope, reusing local tooling, and validating rendering, interaction, accessibility, and network-driven states. Use when frontend behavior needs regression coverage or UI release confidence.
---

# Frontend Testing

Use this skill when adding or updating tests for frontend components, pages, routes, or client-driven state.

## When to Use

- frontend behavior needs regression coverage
- adding UI release confidence before ship
- validating rendering, interaction, or a11y states
- covering network-driven component states

## Core Rules

- follow the repo's existing frontend test stack before adding a new one
- test behavior and user-facing outcomes over internal implementation details
- keep the test scope as small as possible while still proving the risk is covered
- make async and network-driven states deterministic
- do not commit or push test changes unless explicitly allowed

### 2025-2026: Testing AI-Generated UI and GenUI Components

- **Visual regression baseline is mandatory for AI-generated components:** AI tools (v0, Copilot, Cursor) frequently ship components with missing interactive states (focus ring, disabled opacity, hover, loading spinner) — establish a Chromatic or Percy visual regression baseline before merging AI-generated components so regressions are caught automatically.
- **Probabilistic visual state testing:** for AI-powered UI features (personalized content, AI-generated copy, dynamic layouts driven by LLM), use visual snapshot tests with configurable tolerance thresholds rather than pixel-perfect matching — exact pixel matching fails when content varies.
- **Accessibility regression for AI-generated markup:** AI tools frequently generate ARIA attributes that are syntactically correct but semantically wrong (e.g., `role="button"` on a `<div>` with no `tabIndex`) — run `axe-core` or Playwright accessibility checks as part of the CI gate for any AI-generated component.
- **LLM-rendered content testing:** for components that display LLM output (chat bubbles, AI summaries, autocomplete suggestions), test that the component handles empty, truncated, and malformed LLM responses gracefully — do not assume the LLM always returns well-formed output.

## Choose The Right Test Scope

### Component Tests

Best for:

- rendering variants
- interaction behavior
- disabled, loading, or error states
- accessibility-sensitive markup

### Page Or Route Tests

Best for:

- route-level data loading
- guards and auth behavior
- layout integration
- navigation-driven state changes

### End-To-End Or Journey Tests

Best for:

- high-risk user flows
- cross-page flows
- release confidence for critical paths

Use them sparingly when smaller tests already cover the logic well.

## Suggested Process

### 1. Inspect Existing Frontend Tests

Match the local pattern for:

- render helpers
- providers and test wrappers
- mocking strategy
- interaction helpers
- accessibility assertions

### 2. Identify The Risky Behaviors

At minimum, consider:

- primary render path
- key interaction path
- loading and error states
- empty or no-permission states
- network or mutation side effects

### 3. Choose A Stable Dependency Strategy

Use the lightest valid approach:

- real rendering with mocked network boundary
- fake router or app shell
- fixture data for deterministic state
- end-to-end environment only when route or browser integration truly matters

### 4. Write Deterministic UI Tests

Keep tests stable by:

- avoiding fragile timing assumptions
- waiting on visible UI state, not arbitrary delays
- using realistic but minimal fixtures
- asserting what the user can perceive or trigger

### 5. Run The Right Validation

Run:

- targeted frontend tests first
- broader suite if shared UI or route infrastructure changed
- accessibility or visual checks if the repo uses them
- visual regression snapshots if the repo uses them (Chromatic, Percy, Playwright visual)

## Checklist

- [ ] existing test pattern reviewed
- [ ] right test scope chosen
- [ ] primary render path covered
- [ ] key interaction or failure state covered
- [ ] async behavior made deterministic
- [ ] tests run successfully

## Related Skills

- **add-ui-component**: Add tests for reusable UI behavior
- **add-page-route**: Cover route-level and navigation behavior
- **integrate-api-client**: Cover network-driven UI state
- **review-code**: Check whether coverage matches UI risk
- **commit-code**: Prepare frontend test changes for delivery
