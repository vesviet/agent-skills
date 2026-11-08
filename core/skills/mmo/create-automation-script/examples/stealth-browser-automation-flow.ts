import { chromium, Page } from 'playwright';

// Helper: Bezier curve point interpolation for mouse movement
function cubicBezier(t: number, p0: number, p1: number, p2: number, p3: number): number {
  return (
    Math.pow(1 - t, 3) * p0 +
    3 * Math.pow(1 - t, 2) * t * p1 +
    3 * (1 - t) * Math.pow(t, 2) * p2 +
    Math.pow(t, 3) * p3
  );
}

export class StealthAutomationFlow {
  private cdpUrl: string;

  constructor(cdpUrl: string = 'http://127.0.0.1:9222') {
    this.cdpUrl = cdpUrl;
  }

  // Humanized typing simulation with variable inter-key latency
  public async humanType(page: Page, selector: string, text: string) {
    await page.click(selector);
    for (const char of text) {
      await page.keyboard.press(char);
      const delay = 80 + Math.random() * 160; // 80ms - 240ms jitter
      await new Promise((r) => setTimeout(r, delay));
    }
  }

  // Humanized mouse movement using Cubic Bezier trajectories
  public async humanMove(page: Page, targetX: number, targetY: number, steps: number = 25) {
    const startX = 100;
    const startY = 100;

    // Randomize control points
    const cp1X = startX + (targetX - startX) * 0.25 + (Math.random() * 40 - 20);
    const cp1Y = startY + (targetY - startY) * 0.1 + (Math.random() * 40 - 20);
    const cp2X = startX + (targetX - startX) * 0.75 + (Math.random() * 40 - 20);
    const cp2Y = startY + (targetY - startY) * 0.9 + (Math.random() * 40 - 20);

    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const curX = cubicBezier(t, startX, cp1X, cp2X, targetX);
      const curY = cubicBezier(t, startY, cp1Y, cp2Y, targetY);
      await page.mouse.move(curX, curY);
      await new Promise((r) => setTimeout(r, 10 + Math.random() * 15));
    }
  }

  public async executeSession(targetUrl: string) {
    // Connect over CDP to avoid runtime webdriver detection
    const browser = await chromium.connectOverCDP(this.cdpUrl);
    const context = browser.contexts()[0] || (await browser.newContext());
    const page = await context.newPage();

    console.log(`Navigating to ${targetUrl} via stealth CDP connection...`);
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });

    // Execute humanized interaction sequence
    await this.humanMove(page, 450, 320);
    await new Promise((r) => setTimeout(r, 600));

    await browser.close();
  }
}
