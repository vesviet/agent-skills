---
name: frontend-testing
description: Add or improve frontend test coverage by choosing the right UI test scope, reusing local tooling, and validating rendering, interaction, accessibility, and network-driven states. Use when frontend behavior needs regression coverage or UI release confidence.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Frontend Testing

Use this skill when adding or updating tests for frontend components, pages, routes, or client-driven state.

## When to Use

- frontend behavior needs regression coverage or UI release confidence
- adding modern Playwright v1.48+ E2E, HAR network replay, or component tests
- enforcing automated WCAG 2.2 AA accessibility gates and keyboard focus management
- implementing font-stabilized visual regression snapshots across viewports
- intercepting client network requests via MSW v2 transport-level handlers
- validating complex state transitions, optimistic UI updates, or form error flows
- optimizing multi-viewport, theme, and localization UI permutation matrices via pairwise combinatorial testing
- diagnosing and isolating flaky frontend interactions or race conditions using 4-phase systematic debugging

## Core Rules

- **User-facing behavior over internal implementation**:
  - test observable user outcomes; never assert on internal component state, private methods, or CSS classes.
  - use accessibility-first query priority: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`.
  - ban querying by raw CSS selectors or DOM IDs unless targeting third-party uninstrumented embeds.
- **Modern Playwright v1.48+ web-first automation**:
  - make async assertions deterministic with auto-waiting locators (`expect(locator).toBeVisible()`, `expect(locator).toBeEnabled()`).
  - strictly ban arbitrary delays (`sleep()`, `page.waitForTimeout()`); wait for explicit UI state or network idle predicates.
  - configure Trace Viewer to capture diagnostics on failure (`trace: 'retain-on-failure'`) along with console logs and network traffic.
  - record and replay deterministic network interactions via HAR (`page.routeFromHAR()`) for external third-party API stability.
  - leverage Playwright Component Testing (`@playwright/experimental-ct-*`) or Vitest Browser Mode for real DOM rendering without full browser stack overhead.
- **MSW v2 transport-level network interception**:
  - intercept network requests via MSW v2 (`setupServer` for Node/Vitest, `setupWorker` for browser dev/Playwright).
  - author handlers with standard fetch `http.*` methods and typed `HttpResponse.json()`.
  - enforce `onUnhandledRequest: 'error'` to catch unmocked requests and prevent silent leakage to live backends.
  - simulate realistic network variations: latency injection, HTTP 4xx/5xx errors, network disconnection, and malformed payloads.
- **Automated WCAG 2.2 AA accessibility gates**:
  - run `@axe-core/playwright` (`AxeBuilder.withTags(['wcag2a', 'wcag2aa', 'wcag22aa']).analyze()`) in CI with zero violations.
  - verify keyboard focus containment: Tab cycling must be trapped within modal dialogs, flyouts, and drawers while open.
  - verify focus restoration: pressing Escape must dismiss the overlay and restore keyboard focus to the triggering element.
  - validate accessibility trees and semantic landmarks using Playwright ARIA snapshots (`expect(locator).toMatchAriaSnapshot()`).
- **Font-stabilized visual regression snapshots**:
  - await web font readiness before capturing screenshots (`await page.evaluate(() => document.fonts.ready)`).
  - suppress CSS animations, transitions, and blinking text carets (`animations: 'disabled'`).
  - mask volatile or dynamic elements (timestamps, random avatars, counters) using `mask: [locator]`.
  - execute snapshot suites inside containerized headless Linux environments (Docker) to eliminate cross-OS rasterization diffs.
  - configure tight pixel difference tolerances (`maxDiffPixelRatio: 0.002`) to catch genuine visual defects while ignoring subpixel jitter.
- **AI & LLM-generated UI component resilience**:
  - test empty, truncated, streaming, and malformed LLM responses explicitly; never assume well-formed model output.
  - establish visual regression baselines before merging AI-generated components to catch missing active/hover/focus states.
  - mandate automated axe-core scans on AI-generated UI to catch syntactically valid but semantically broken ARIA attributes.
- **Pairwise UI matrix & systematic defect isolation**:
  - use `combinatorial-testing` to generate pairwise covering arrays across viewports, user permissions, and component states.
  - use `systematic-debugging` to isolate non-deterministic UI flakiness, race conditions, and state transition errors.
- **Scope discipline & change governance**:
  - keep test scope minimal while proving risk coverage; never commit or push test changes without explicit confirmation.

## Choose The Right Test Scope

### Component Tests

Best for:
- isolated rendering variants, props validation, and interactive state changes
- Playwright Component Testing (`@playwright/experimental-ct-*`) or Vitest Browser Mode
- disabled, loading, and error states; a11y-sensitive markup and focus traps
- validating ARIA states, role attributes, and keyboard focus handling at the unit level
- rapid feedback during component development without full app bundling

### Page Or Route Tests

Best for:
- route data loading, navigation guards, and auth session state
- layout integration, responsive breakpoints, and client-side URL routing transitions
- mock API contract integration with MSW v2 handlers or recorded HAR replays
- validating page-level metadata, canonical tags, and breadcrumb hierarchy

### End-To-End Or Journey Tests

Best for:
- high-risk end-to-end user journeys spanning multiple page boundaries
- cross-browser verification (Chromium, Firefox, WebKit) with Playwright Trace Viewer enabled
- multi-role interactions (e.g. buyer checkout and admin order review in parallel contexts)
- critical path release confidence (use sparingly when smaller tests provide sufficient proof)

## Suggested Process

### 1. Inspect Existing Frontend Tests

Match local patterns for:
- test runner and browser provider (Playwright v1.48+, Vitest browser mode)
- render helpers, wrapper providers, router mocks, and test fixtures
- network mocking setup (MSW v2 server/worker handlers and request schemas)
- assertion libraries, custom matchers, and accessibility assertions
- visual snapshot configurations and containerized execution parameters

### 2. Identify Risky Behaviors & Accessibility Invariants

At minimum, evaluate:
- primary rendering paths and interactive state transitions
- error, empty, loading, timeout, and degraded network states
- optimistic UI updates, local cache invalidations, and form validation boundaries
- WCAG 2.2 AA compliance: color contrast, keyboard focus traps, Escape key restoration
- visual regression sensitivity (custom web fonts, transitions, dynamic date/avatar content)
- internationalization and bidirectional text (RTL/LTR) layout reflows

### 3. Choose A Stable Dependency Strategy

Use the lightest valid approach:
- MSW v2 transport-level handlers with `onUnhandledRequest: 'error'` for deterministic API mocking
- HAR recording and replay (`page.routeFromHAR()`) for external third-party API stability
- isolated browser contexts per test worker to prevent cookie, session, or local storage leakage
- minimal deterministic fixture data for component and route state
- containerized headless browser environment (Docker Linux) for reproducible visual snapshots

### 4. Write Deterministic UI & Accessibility Tests

Keep tests stable by:
- relying on web-first auto-waiting locators (`toBeVisible()`) instead of arbitrary delays
- validating modal keyboard focus containment (Tab cycling) and trigger restoration on Escape
- asserting zero axe-core violations with `@axe-core/playwright` (`AxeBuilder.analyze()`)
- stabilizing visual snapshots with `document.fonts.ready`, `animations: 'disabled'`, and element masking
- verifying ARIA structure with Playwright snapshot assertions (`toMatchAriaSnapshot()`)

### 5. Run Validation & Capture Diagnostic Artifacts

Execute:
- targeted component and route tests first for fast feedback loops
- full browser suite with Playwright Trace Viewer capturing failure traces (`trace: 'retain-on-failure'`)
- inspect Playwright Trace Viewer timeline, network panel, and DOM snapshots on failure
- automated WCAG 2.2 AA accessibility audit and containerized visual snapshot comparisons
- linter and typecheck before finalizing test deliverables

## Checklist

- [ ] existing frontend test stack and scope reviewed
- [ ] MSW v2 transport interception configured with `onUnhandledRequest: 'error'`
- [ ] Playwright v1.48+ auto-waiting assertions used with `sleep()` / `waitForTimeout()` eliminated
- [ ] Playwright Trace Viewer enabled with `trace: 'retain-on-failure'` and HAR replay for network paths
- [ ] automated WCAG 2.2 AA scan passes with zero violations via `@axe-core/playwright`
- [ ] keyboard focus management verified (Tab contained in modals, Escape restores focus to trigger)
- [ ] accessibility tree structure verified via Playwright ARIA snapshots (`toMatchAriaSnapshot()`)
- [ ] visual regression snapshots font-stabilized via `document.fonts.ready`, animations disabled, dynamic elements masked
- [ ] tests executed and passing cleanly in containerized headless environment

## Failure Modes

- **Coverage theater**: achieving high line coverage without exercising critical failure paths. **Mitigation:** enforce the Testing Trophy and verify mutation score ≥ 75-80% via Stryker for critical UI logic.
- **Font anti-aliasing snapshot flakiness**: cross-platform OS rasterization causes false-positive 1px visual diffs. **Mitigation:** await `document.fonts.ready`, disable animations, execute in containerized Linux, and set `maxDiffPixelRatio: 0.002`.
- **Inaccessible modal focus trap & focus loss**: keyboard focus escapes modal into background DOM or is lost on close. **Mitigation:** run `@axe-core/playwright` CI gate, assert Tab cycling containment, and verify Escape key focus restoration.
- **Unhandled network leakage**: tests leak unmocked network requests causing flaky timeouts. **Mitigation:** enforce MSW v2 with `onUnhandledRequest: 'error'` and use HAR replay for stable external responses.
- **Flaky sleep-based waits**: arbitrary `waitForTimeout()` creates race conditions in CI. **Mitigation:** replace with Playwright web-first locators and auto-waiting assertions.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/test-report.json** — Comprehensive frontend test report documenting test suite results (unit, component, e2e, accessibility, visual), failure traces, mutation scores, and WCAG compliance.
- **contracts/schemas/implementation-result.json** — Emitted when frontend tests accompany feature delivery, capturing `change_summary`, `files_touched[]`, and `validation_run`. Set `produced_by_role` to the emitting role.

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
- **combinatorial-testing**: Generate pairwise matrices for viewport, device, and UI state combinations
- **systematic-debugging**: Isolate and debug flaky browser interactions and rendering race conditions
- **develop-mobile-app**: Test mobile components, navigation flows, and offline states using React Native Testing Library
