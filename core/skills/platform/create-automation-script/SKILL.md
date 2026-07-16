---
name: create-automation-script
description: Build Playwright/Puppeteer automation scripts that connect via CDP to Anti-Detect browsers or use C++ patched engines. Implements behavioral mimicry to bypass AI detection. Use when building multi-account automation, login flows, ad account warm-up sequences, or scraping high-trust platforms.
---

# Create Automation Script

Use this skill to develop the core engine for MMO automation (farming, scraping, ad deployment) with an absolute focus on stealth and evading advanced bot-detection systems.

## When to Use

- building multi-account login or warm-up automation
- scripting ad account creation/deployment at scale
- scraping high-trust platforms (Meta, Google, TikTok)
- connecting to an Anti-Detect Browser via CDP instead of a raw launch
- validating stealth before a production run against bot-detection pages

## Example (CDP connection + behavioral delays)

```typescript
import { chromium } from "playwright";

const browser = await chromium.connectOverCDP("http://adspower-gw:50325");
const context = browser.contexts()[0];
const page = await context.newPage();

// organic, randomized typing — never instant fill
await page.click("#email");
for (const ch of "user@example.com") {
  await page.keyboard.type(ch, { delay: 100 + Math.random() * 400 });
}
await page.mouse.move(200, 300, { steps: 12 }); // Bezier-like path
```

## Core Rules

- **BEHAVIORAL-LOCK**: Any script interacting with high-trust platforms (Meta, Google, TikTok) MUST include organic delays and mouse movement emulation. Never execute instantaneous actions.
- **STEALTH-LOCK**: Reject the use of outdated JS-injection stealth plugins (`playwright-stealth`) for critical operations. Rely strictly on CDP connections to Anti-Detect Browsers or C++ patched environments.

## Suggested Process

1. **Connection Strategy**: Do not use standard `playwright.chromium.launch()`. Instead, use `playwright.chromium.connect_over_cdp()` to attach to an already running Anti-Detect Browser profile (e.g., AdsPower API) or use a C++ stealth-patched engine (e.g., Camoufox).
2. **Behavioral Mimicry Implementation**: Inject randomized delays (e.g., `delay: 100-500ms`) between typing actions. Avoid instantaneous form fills. Implement Bezier curve-based mouse movements and organic scrolling patterns.
3. **Headless Evasion Validation**: If forced to run headless, ensure the engine is specifically patched to hide headless markers (like `navigator.webdriver`).
4. **Execution Test**: Run the script against a bot-detection test page (e.g., CreepJS or Cloudflare Turnstile) to verify stealth capabilities before production use.

## Checklist

- [ ] Script connects via CDP or uses a C++ patched engine (no raw Playwright launch).
- [ ] Randomized delays and human-like typing/scrolling are implemented.
- [ ] playwright-stealth JS-injection is avoided for high-risk operations.
- [ ] Script passes basic bot-detection tests (CreepJS, Cloudflare Turnstile).
- [ ] Script includes error handling and retry logic for network failures.
- [ ] CDP connection to Anti-Detect Browser profile is verified before execution.

## Related Skills

- **deploy-mmo-infrastructure**: Provision the Anti-Detect Browsers the script will connect to.
- **turnstile-spin**: Handle Cloudflare Turnstile challenges encountered during automation.
