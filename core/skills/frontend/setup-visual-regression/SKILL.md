---
name: setup-visual-regression
description: Configure automated visual diffing for UI components. Use to prevent unintended styling regressions across browser targets.
---

# Setup Visual Regression

Use this skill to integrate Playwright or Chromatic into the CI pipeline to enforce pixel-perfect UI consistency and block styling regressions.

## Core Rules
- **Component Isolation**: Test UI components in isolation (Storybook) alongside full-page visual regression tests.
- **Dynamic Content Masking**: Mask or stub dynamic content (e.g., dates, random IDs, dynamic ads) before capturing snapshots to prevent flaky tests.
- **Cross-Browser Coverage**: Configure the matrix to run snapshots across Chromium, WebKit, and Firefox engines at minimum mobile and desktop viewports.
- **Hard CI Gate**: Visual regression failures must block merges unless explicitly approved by a `ui-ux-designer` or `frontend-developer`.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `tests_added[]`, and `validation_run` output proving the visual baseline generation succeeded.

## Checklist
- [ ] Visual testing framework (Playwright/Chromatic) installed and configured.
- [ ] Dynamic content masking implemented for stability.
- [ ] Viewport and browser matrix configured.
- [ ] CI/CD pipeline updated to enforce the visual gate.
- [ ] `implementation-result.json` emitted.
