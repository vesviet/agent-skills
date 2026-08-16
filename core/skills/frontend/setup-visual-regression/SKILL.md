---
name: setup-visual-regression
description: Configure automated visual diffing for UI components and pages. Use when establishing pixel-level regression testing, cross-browser snapshot baselines, or CI visual gates.
---

# Setup Visual Regression

Use this skill to integrate Playwright or Chromatic into the CI pipeline to enforce pixel-perfect UI consistency and block styling regressions.

## Core Rules

- **Component Isolation**: Test UI components in isolation (Storybook) alongside full-page visual regression tests.
- **Dynamic Content Masking**: Mask or stub dynamic content (e.g., dates, random IDs, dynamic ads) before capturing snapshots to prevent flaky tests.
- **Cross-Browser Coverage**: Configure the matrix to run snapshots across Chromium, WebKit, and Firefox engines at minimum mobile and desktop viewports.
- **Hard CI Gate**: Visual regression failures must block merges unless explicitly approved by a `ui-ux-designer` or `frontend-developer`.
- **Deterministic Environment**: Generate and compare baselines in fixed Docker/container environments to avoid host OS font rendering variations.

## Suggested Process

### 1. Select and Install Visual Diffing Engine

Choose and install the appropriate framework based on repo architecture:
- Playwright Test (`@playwright/test`) with `toHaveScreenshot()` for full-page and integrated route diffs.
- Chromatic / Storybook Test Runner for isolated design system component snapshot suites.
- Configure snapshot storage directories and threshold tolerances (e.g., `maxDiffPixelRatio: 0.01`).

### 2. Define Viewport and Browser Matrix

Configure responsive test parameters:
- Set up standard viewport configurations (Mobile: 375x667, Tablet: 768x1024, Desktop: 1280x800).
- Enable cross-browser execution across Chromium, WebKit, and Firefox.
- Configure color scheme variants (light mode and dark mode) where supported.

### 3. Implement Dynamic Content Masking & Mocking

Eliminate snapshot non-determinism:
- Disable CSS animations and transitions during test runs (`animations: 'disabled'`).
- Mask dynamic elements such as timestamps, user avatars, and fluctuating numeric feeds using test selectors (`mask: [page.locator('.timestamp')]`).
- Stub network API responses to serve fixed mock data.

### 4. Capture Initial Baselines in Containerized Environment

Generate canonical reference snapshots:
- Run baseline capture scripts inside the project's official Docker container or CI image to guarantee identical font rendering.
- Verify baseline image quality, cropping, and full-page layout coverage.
- Commit initial reference snapshots to the repository or artifact registry per project policy.

### 5. Integrate CI Pipeline Gate

Configure automated workflow execution:
- Add a visual regression step to CI workflows triggered on pull requests touching frontend assets.
- Configure visual diff artifact uploads on failure to simplify PR review.
- Set up failure reporting that links directly to visual comparison summaries.

### 6. Establish Baseline Update & Approval Workflow

Document snapshot maintenance procedures:
- Define the CLI command for regenerating baselines when intentional UI changes land (e.g., `npm run test:visual -- -u`).
- Enforce mandatory reviewer sign-off from designated UI/UX or frontend leads before updating baselines.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `tests_added[]`, and `validation_run` output proving the visual baseline generation succeeded.

## Checklist

- [ ] Visual testing framework (Playwright/Chromatic) installed and configured.
- [ ] Viewport matrix (mobile, tablet, desktop) and browser targets configured.
- [ ] Dynamic content masking and animation disabling implemented to prevent flakes.
- [ ] Network mocks configured for deterministic state rendering.
- [ ] Baseline snapshots generated in containerized environment.
- [ ] CI pipeline step configured as a hard quality gate blocking visual regressions.
- [ ] `implementation-result.json` emitted.

## Related Skills

- **frontend-testing**: Complement visual diffs with functional and interaction unit/integration tests
- **accessibility-review**: Pair visual regression testing with automated axe-core accessibility gates
- **add-ui-component**: Validate new or modified UI components against visual snapshot baselines
- **design-review**: Review visual snapshot diffs against design specifications and design tokens
- **review-code**: Audit visual test coverage and snapshot approval evidence during code review
