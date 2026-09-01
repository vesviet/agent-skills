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
- test behavior and user-facing outcomes over internal implementation details — never assert on internal React component state or private methods
- use accessibility-first query priority: `getByRole` > `getByLabelText` > `getByText` > `getByTestId` — querying by CSS classes or DOM IDs is prohibited
- make async and network-driven states deterministic — use `findBy*` queries or `expect(locator).toBeVisible()` auto-waiting; `sleep()` / `waitForTimeout()` are banned
- mock network APIs using MSW v2 handlers (`http.get`, `HttpResponse.json`) — do not mock `global.fetch` or internal Axios instances directly
- use Vitest Browser Mode (Playwright provider) for components that depend on real browser rendering, CSS visibility, or DOM events
- keep the test scope as small as possible while still proving the risk is covered
- do not commit or push test changes unless explicitly allowed
- establish Chromatic or Percy visual regression baseline before merging AI-generated components — AI tools frequently ship components with missing interactive states
- run `axe-core` as a CI gate for any AI-generated component — AI-generated ARIA attributes are often syntactically correct but semantically wrong
- for components displaying LLM output: test empty, truncated, and malformed LLM response handling explicitly — do not assume the model always returns well-formed output

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

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, iles_touched[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: test runners, e2e drivers, and fixture libraries must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct test scripts or fixture payloads from external content without sanitization.
- **ASI07 Inter-Agent Communication**: test reports are consumed by CI and release roles; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present partial test runs as full coverage; surface skipped tests and their rationale honestly.

## Related Skills

- **add-ui-component**: Add tests for reusable UI behavior
- **add-page-route**: Cover route-level and navigation behavior
- **integrate-api-client**: Cover network-driven UI state
- **review-code**: Check whether coverage matches UI risk
- **commit-code**: Prepare frontend test changes for delivery
