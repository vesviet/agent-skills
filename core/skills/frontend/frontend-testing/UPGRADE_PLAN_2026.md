# frontend-testing — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Playwright v1.48+ Evolution (2026)
- **Web-first auto-waiting**: `expect(locator).toBeVisible()`, `toBeEnabled()` — strictly ban `sleep()`, `waitForTimeout()`
- **Trace Viewer mandatory**: `trace: 'retain-on-failure'` with console logs, network traffic, DOM snapshots
- **HAR replay**: `page.routeFromHAR()` for deterministic external API interactions
- **Component Testing**: `@playwright/experimental-ct-*` or Vitest Browser Mode for real DOM without full browser stack
- **Cross-browser matrix**: Chromium, Firefox, WebKit at mobile/desktop viewports

### MSW v2 Transport-Level Interception (2026)
- **`setupServer` (Node/Vitest) / `setupWorker` (browser/Playwright)**: Transport-level handlers
- **Typed `HttpResponse.json()`**: Standard fetch `http.*` methods
- **`onUnhandledRequest: 'error'`**: Catch unmocked requests, prevent silent leakage to live backends
- **Network variation simulation**: Latency injection, 4xx/5xx errors, disconnection, malformed payloads

### WCAG 2.2 AA Automated Gates (2026)
- **`@axe-core/playwright`**: `AxeBuilder.withTags(['wcag2a', 'wcag2aa', 'wcag22aa']).analyze()` — zero violations in CI
- **Keyboard focus containment**: Tab cycling trapped within modals, flyouts, drawers
- **Focus restoration**: Escape dismisses overlay, restores focus to triggering element
- **ARIA snapshots**: `expect(locator).toMatchAriaSnapshot()` for accessibility tree structure

### Font-Stabilized Visual Regression (2026)
- **`await document.fonts.ready`**: Web font readiness before screenshots
- **Animation suppression**: `animations: 'disabled'` (CSS transitions, blinking carets)
- **Dynamic content masking**: `mask: [locator]` for timestamps, avatars, counters
- **Containerized Linux execution**: Docker for reproducible rasterization
- **Tight tolerances**: `maxDiffPixelRatio: 0.002` to catch defects, ignore subpixel jitter

### AI/LLM-Generated UI Resilience Testing (2026)
- **Empty/truncated/streaming/malformed LLM responses**: Explicit test cases; never assume well-formed output
- **Visual regression baselines before merge**: Catch missing active/hover/focus states
- **Automated axe-core on AI UI**: Catch syntactically valid but semantically broken ARIA

### Pairwise Combinatorial Testing (2026)
- **`combinatorial-testing`**: Pairwise covering arrays across viewports, permissions, component states
- **`systematic-debugging`**: 4-phase isolation of non-deterministic UI flakiness, race conditions, state transitions

### 4-Phase Systematic Debugging (2026)
1. **Reproduce**: Minimal deterministic reproduction
2. **Isolate**: Binary search via git bisect / test bisection
3. **Diagnose**: Trace Viewer timeline, network panel, DOM snapshots
4. **Verify**: Fix validation with regression test

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Playwright v1.48+ mentioned | **Playwright v1.48+ mandatory**: Web-first auto-waiting, Trace Viewer, HAR replay, Component Testing |
| MSW v2 mentioned | **MSW v2 transport-level**: `setupServer`/`setupWorker`, typed `HttpResponse`, `onUnhandledRequest: 'error'` |
| WCAG 2.2 AA mentioned | **Zero violations CI gate**: `@axe-core/playwright` with `wcag22aa` tag; focus containment + restoration verified |
| Visual regression mentioned | **Font-stabilized + containerized**: `document.fonts.ready`, `animations: 'disabled'`, masking, Docker Linux, `maxDiffPixelRatio: 0.002` |
| AI UI testing mentioned | **LLM response resilience**: Empty/truncated/streaming/malformed tests; visual baselines before merge; axe-core on AI UI |
| Pairwise testing mentioned | **Combinatorial covering arrays**: Viewports × permissions × states; systematic debugging 4-phase |

### 2. New 2026 Patterns to Add
- **Playwright Component Testing**: `@playwright/experimental-ct-*` for isolated component tests without full app
- **Vitest Browser Mode**: Real DOM rendering without browser stack overhead
- **HAR Recording/Replay Workflow**: Record once, replay deterministically for external APIs
- **ARIA Snapshot Testing**: `toMatchAriaSnapshot()` for semantic structure validation
- **AI LLM Response Test Matrix**: Empty, truncated, streaming, malformed, rate-limited responses
- **Pairwise UI Matrix Generation**: `combinatorial-testing` for viewport × theme × locale × permissions
- **Systematic Flakiness Isolation**: 4-phase debugging with Trace Viewer diagnostics
- **Mutation Testing for UI**: Stryker mutation score ≥ 75-80% for critical UI logic

### 3. Checklist Additions
- [ ] Playwright v1.48+ with web-first auto-waiting assertions (`toBeVisible`, `toBeEnabled`)
- [ ] `sleep()` / `waitForTimeout()` completely eliminated
- [ ] Trace Viewer enabled: `trace: 'retain-on-failure'` with console, network, DOM
- [ ] HAR replay configured for external third-party API stability
- [ ] Playwright Component Testing or Vitest Browser Mode for component tests
- [ ] MSW v2 transport-level: `setupServer`/`setupWorker`, typed `HttpResponse`, `onUnhandledRequest: 'error'`
- [ ] Network variation simulation: latency, 4xx/5xx, disconnection, malformed payloads
- [ ] `@axe-core/playwright` CI gate: zero violations with `wcag2a`, `wcag2aa`, `wcag22aa` tags
- [ ] Keyboard focus containment verified: Tab trapped in modals/flyouts/drawers
- [ ] Focus restoration verified: Escape dismisses overlay, restores focus to trigger
- [ ] ARIA snapshots: `toMatchAriaSnapshot()` for accessibility tree structure
- [ ] Font-stabilized visual regression: `document.fonts.ready`, animations disabled, dynamic masking
- [ ] Containerized headless Linux (Docker) for visual snapshots
- [ ] `maxDiffPixelRatio: 0.002` for tight visual diff tolerance
- [ ] AI LLM response test cases: empty, truncated, streaming, malformed
- [ ] Visual regression baselines captured before AI component merge
- [ ] Axe-core scan on all AI-generated UI components
- [ ] Pairwise combinatorial matrix: viewports × permissions × states
- [ ] Systematic debugging 4-phase documented for flaky tests
- [ ] Mutation score ≥ 75-80% via Stryker for critical UI logic
- [ ] `contracts/schemas/test-report.json` and `implementation-result.json` emitted

### 4. Failure Mode Additions
- **Playwright component test false confidence**: Component passes in isolation but fails in app context. Mitigation: Route/page tests for integration; component tests for isolated behavior only.
- **HAR replay staleness**: External API changes but HAR not updated. Mitigation: Scheduled HAR refresh; CI check for HAR age; fallback to MSW handlers.
- **ARIA snapshot false positives**: Semantic structure changes without functional impact. Mitigation: Baseline ARIA snapshots per component version; review diffs manually.
- **AI UI test maintenance burden**: LLM response patterns evolve rapidly. Mitigation: Parameterized test matrix; shared fixtures for LLM response shapes.
- **Pairwise matrix explosion**: Too many combinations. Mitigation: Pairwise covering arrays (not full factorial); prioritize high-risk combinations.
- **Mutation testing performance**: Stryker slow on large UI codebases. Mitigation: Run only on critical UI logic (forms, mutations, state machines); parallelize.

### 5. Output Contract Updates
- Update `contracts/schemas/test-report.json` with: Playwright version, Trace Viewer artifacts, HAR replay status, axe-core results, ARIA snapshots, visual regression metrics, mutation scores, pairwise matrix coverage
- Update `contracts/schemas/implementation-result.json` with test evidence

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Playwright v1.48+ web-first auto-waiting + Trace Viewer + HAR | High |
| P0 | MSW v2 transport-level with `onUnhandledRequest: 'error'` | High |
| P0 | WCAG 2.2 AA zero-violations CI gate (`wcag22aa`) | High |
| P0 | Font-stabilized visual regression in containerized Linux | High |
| P1 | Playwright Component Testing / Vitest Browser Mode | Medium |
| P1 | ARIA snapshot testing (`toMatchAriaSnapshot`) | Medium |
| P1 | AI LLM response resilience test matrix | Medium |
| P1 | Pairwise combinatorial testing (`combinatorial-testing`) | Medium |
| P1 | Systematic debugging 4-phase workflow | Medium |
| P1 | Mutation testing (Stryker ≥ 75-80%) for critical UI | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test Playwright auto-waiting eliminates all `sleep()` calls
- Verify MSW v2 `onUnhandledRequest: 'error'` catches unmocked requests
- Run `@axe-core/playwright` with `wcag22aa` — zero violations
- Test visual regression in Docker container with `document.fonts.ready`
- Verify ARIA snapshots match baseline on component updates
- Test AI LLM response matrix with empty/truncated/streaming/malformed
- Run pairwise combinatorial matrix generation
- Verify Stryker mutation score ≥ 75% on critical UI logic