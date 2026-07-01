---
name: create-automation-script
description: Build Playwright/Puppeteer automation scripts that connect via CDP to Anti-Detect browsers or use C++ patched engines. Implements behavioral mimicry to bypass AI detection.
---

# Create Automation Script

Use this skill to develop the core engine for MMO automation (farming, scraping, ad deployment) with an absolute focus on stealth and evading advanced bot-detection systems.

## Core Rules

- **BEHAVIORAL-LOCK**: Any script interacting with high-trust platforms (Meta, Google, TikTok) MUST include organic delays and mouse movement emulation. Never execute instantaneous actions.
- **STEALTH-LOCK**: Reject the use of outdated JS-injection stealth plugins (`playwright-stealth`) for critical operations. Rely strictly on CDP connections to Anti-Detect Browsers or C++ patched environments.

## Suggested Process

1. **Connection Strategy**: Do not use standard `playwright.chromium.launch()`. Instead, use `playwright.chromium.connect_over_cdp()` to attach to an already running Anti-Detect Browser profile (e.g., AdsPower API) or use a C++ stealth-patched engine (e.g., Camoufox).
2. **Behavioral Mimicry Implementation**: Inject randomized delays (e.g., `delay: 100-500ms`) between typing actions. Avoid instantaneous form fills. Implement Bezier curve-based mouse movements and organic scrolling patterns.
3. **Headless Evasion Validation**: If forced to run headless, ensure the engine is specifically patched to hide headless markers (like `navigator.webdriver`).
4. **Execution Test**: Run the script against a bot-detection test page (e.g., CreepJS or Cloudflare Turnstile) to verify stealth capabilities before production use.

## Checklist

- [ ] Script connects via CDP or uses a C++ patched engine (no raw Playwright).
- [ ] Randomized delays and human-like typing/scrolling are implemented.
- [ ] `playwright-stealth` JS-injection is avoided.
- [ ] Script passes basic bot-detection tests.

## Related Skills

- `deploy-mmo-infrastructure`: For provisioning the Anti-Detect Browsers the script will connect to.
- `turnstile-spin`: For handling Cloudflare challenges.
