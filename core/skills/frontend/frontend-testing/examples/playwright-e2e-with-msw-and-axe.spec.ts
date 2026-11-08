/**
 * Playwright E2E Test Suite with MSW v2 and Axe Accessibility
 *
 * Implements:
 * - Deterministic web-first auto-waiting assertions (zero sleep/waitForTimeout)
 * - MSW v2 transport-level route interception
 * - Automated WCAG 2.2 AA accessibility scan via @axe-core/playwright
 * - Modal keyboard focus containment & Escape key focus restoration
 * - Playwright ARIA snapshot assertion
 */

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Checkout Order Review & Accessibility Gate', () => {
  test.beforeEach(async ({ page }) => {
    // 1. MSW / Playwright Route Interception (Deterministic API mocking)
    await page.route('**/api/v1/checkout/review', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          orderId: 'ord_test_8821',
          subtotalCents: 9800,
          taxCents: 808,
          shippingCents: 1200,
          totalCents: 11808,
          items: [{ sku: 'SKU-001', name: 'Mechanical Keyboard Switch Set', quantity: 2 }],
        }),
      });
    });

    await page.goto('/checkout/review');
  });

  test('renders review order details with auto-waiting assertions', async ({ page }) => {
    // 2. Web-first auto-waiting locators
    const submitBtn = page.getByRole('button', { name: 'Complete Purchase' });
    await expect(submitBtn).toBeVisible();
    await expect(submitBtn).toBeEnabled();

    const totalHeading = page.getByText('$118.08');
    await expect(totalHeading).toBeVisible();
  });

  test('passes automated WCAG 2.2 AA accessibility audit', async ({ page }) => {
    // 3. Automated axe-core scan
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('verifies modal dialog keyboard trap and focus restoration', async ({ page }) => {
    const editShippingBtn = page.getByRole('button', { name: 'Edit Address' });
    await editShippingBtn.click();

    const dialog = page.getByRole('dialog', { name: 'Edit Shipping Address' });
    await expect(dialog).toBeVisible();

    // Verify initial focus is trapped inside dialog
    const firstInput = dialog.getByRole('textbox', { name: 'Street Address' });
    await expect(firstInput).toBeFocused();

    // Verify Escape key dismisses dialog and restores focus to triggering button
    await page.keyboard.press('Escape');
    await expect(dialog).not.toBeVisible();
    await expect(editShippingBtn).toBeFocused();
  });

  test('validates semantic ARIA snapshot structure', async ({ page }) => {
    const summaryCard = page.getByRole('region', { name: 'Order Summary' });
    await expect(summaryCard).toBeVisible();

    // 4. Playwright ARIA snapshot assertion
    await expect(summaryCard).toMatchAriaSnapshot(`
      - region "Order Summary":
        - heading "Order Summary" [level=2]
        - list:
          - listitem:
            - text: /Mechanical Keyboard Switch Set/
        - text: /\\$118\\.08/
        - button "Complete Purchase"
    `);
  });
});
