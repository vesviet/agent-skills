# Playwright, MSW v2, and Automated Accessibility Testing Standards (2026)

## 1. Web-First E2E Automation (Playwright v1.48+)

### 1.1 Auto-Waiting & Timing Discipline
- **Absolute Ban on Fixed Timeouts**: `page.waitForTimeout()` and arbitrary `sleep()` statements are strictly prohibited. Tests must rely exclusively on web-first auto-waiting assertions:
  ```typescript
  await expect(page.getByRole('button', { name: 'Submit Order' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Submit Order' })).toBeEnabled();
  ```
- **Diagnostic Trace Retention**: Configure `trace: 'retain-on-failure'` in `playwright.config.ts`. Retain DOM snapshots, network waterfalls, and console logs exclusively when assertions fail, minimizing CI storage bloat.
- **HAR Network Replay**: Record third-party network traffic during sandbox sessions and replay via `page.routeFromHAR('fixtures/payments.har')` to decouple tests from external vendor flakiness.

---

## 2. Transport-Level Network Interception (MSW v2)

### 2.1 Boundary Isolation & Error Simulation
Mock Service Worker (MSW) v2 intercepts network traffic at the Node `fetch` transport level:
- **Strict Leakage Prevention**: Enforce `onUnhandledRequest: 'error'` in test runner setup to immediately fail any test issuing unmocked network calls to production services.
- **Typed Handlers & Network Faults**:
  ```typescript
  import { http, HttpResponse, delay } from 'msw';

  export const handlers = [
    http.get('/api/v1/orders/:id', async () => {
      await delay(50); // Simulate network latency
      return HttpResponse.json({ id: 'ord_123', status: 'shipped' });
    }),
    http.post('/api/v1/checkout', () => {
      return new HttpResponse(null, { status: 504, statusText: 'Gateway Timeout' });
    }),
  ];
  ```

---

## 3. Automated Accessibility Gates (WCAG 2.2 Level AA)

### 3.1 axe-core & ARIA Snapshot Assertions
- **Automated CI Gate**: Integrate `@axe-core/playwright` into E2E specs to assert zero accessibility violations:
  ```typescript
  import AxeBuilder from '@axe-core/playwright';

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
  ```
- **Keyboard Focus Containment**: In modal dialogs, Tab key navigation must cycle strictly within the active dialog. Pressing `Escape` must dismiss the modal and restore focus to the triggering element.
- **Semantic ARIA Snapshots**: Assert DOM accessibility tree semantics using Playwright ARIA snapshots:
  ```typescript
  await expect(page.getByRole('dialog')).toMatchAriaSnapshot(`
    - dialog "Confirm Deletion":
      - heading "Are you sure?" [level=2]
      - button "Cancel"
      - button "Delete"
  `);
  ```

---

## 4. Font-Stabilized Visual Regression Protocol

- **Font Readiness**: Await font rasterization before capturing snapshots:
  ```typescript
  await page.evaluate(() => document.fonts.ready);
  ```
- **Animation Disabling & Masking**: Disable all transitions (`animations: 'disabled'`) and mask non-deterministic elements (timestamps, avatars):
  ```typescript
  await expect(page).toHaveScreenshot('checkout-review.png', {
    mask: [page.locator('[data-testid="live-timestamp"]')],
    maxDiffPixelRatio: 0.002,
    animations: 'disabled',
  });
  ```
- **Containerized Headless Linux**: All visual regression test runs must execute in Docker containerized Linux environments to eliminate anti-aliasing variations between macOS and Linux CI workers.
