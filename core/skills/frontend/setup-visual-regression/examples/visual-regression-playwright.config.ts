/**
 * Production Playwright Visual Regression Configuration
 *
 * Implements:
 * - Deterministic visual diff settings (maxDiffPixelRatio: 0.002, threshold: 0.2)
 * - Cross-browser projects (Chromium, Firefox, WebKit) for Desktop (1280px) and Mobile (375px)
 * - Containerized path alignment with mcr.microsoft.com/playwright
 * - Diagnostic trace retention on failure
 */

import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/visual',
  snapshotDir: './tests/visual/snapshots',
  snapshotPathTemplate: '{snapshotDir}/{testFileDir}/{testFileName}-snapshots/{arg}-{projectName}{ext}',

  timeout: 30_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,

  reporter: [
    ['html', { outputFolder: 'playwright-visual-report', open: 'never' }],
    ['list'],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },

  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.002, // 0.2% max variance allowed
      threshold: 0.2, // Per-pixel color sensitivity
      animations: 'disabled', // Freeze all CSS animations and transitions
    },
  },

  projects: [
    // 1. Desktop Viewport (1280x800)
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      name: 'firefox-desktop',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      name: 'webkit-desktop',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1280, height: 800 },
      },
    },

    // 2. Mobile Viewport (iPhone 14 / Mobile Chrome 375x667)
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
        viewport: { width: 375, height: 667 },
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 14'],
        viewport: { width: 375, height: 667 },
      },
    },
  ],
});
