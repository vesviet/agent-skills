# Visual Regression Testing with Containerized Playwright & Dynamic Masking (2026)

## 1. Containerized Baseline Determinism

### 1.1 Cross-Platform Rasterization Drift
Sub-pixel anti-aliasing algorithms differ substantially between macOS (Core Graphics), Windows (DirectWrite), and Linux (FreeType):
- **Mandatory Docker Containerization**: Visual regression snapshots must be generated and compared inside the official Playwright Docker container:
  ```bash
  docker run --rm --network host -v $(pwd):/work/ -w /work/ \
    mcr.microsoft.com/playwright:v1.48.0-noble \
    npx playwright test --config=playwright.visual.config.ts
  ```
- Local developer workstation diffs must never be checked into git without containerized verification.

---

## 2. Flakiness Elimination & Dynamic Element Masking

### 2.1 Pre-Snapshot Stabilization Sequence
Before executing `toHaveScreenshot()`, tests must execute a 4-point stabilization sequence:
1. **Font Readiness**:
   ```typescript
   await page.evaluate(() => document.fonts.ready);
   ```
2. **Animation & Transition Disabling**:
   Configure `animations: 'disabled'` to freeze CSS keyframes, transitions, and SVG animations.
3. **Caret Hiding**: Suppress flashing input cursor carats (`caret-color: transparent`).
4. **Dynamic Masking**: Mask non-deterministic elements (timestamps, user avatars, live metrics):
   ```typescript
   await expect(page).toHaveScreenshot('dashboard-overview.png', {
     mask: [
       page.locator('[data-testid="live-timestamp"]'),
       page.locator('[data-testid="user-avatar"]'),
     ],
     maxDiffPixelRatio: 0.002,
     threshold: 0.2,
   });
   ```

---

## 3. Strict Tolerance Calibration & CI Gates

- **`threshold: 0.2`**: Perceptual color difference threshold per pixel in YIQ color space.
- **`maxDiffPixelRatio: 0.002`**: Allows maximum 0.2% total pixel variance across the entire viewport to absorb subpixel font rendering while catching real layout regressions.
- **Hard CI Failure**: Unapproved visual regressions fail CI builds, requiring explicit review from a UI/UX Designer or Frontend Developer before baseline update.
