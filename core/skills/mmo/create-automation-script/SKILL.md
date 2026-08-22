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
- **STEALTH-LOCK**: Reject the use of outdated JS-injection stealth plugins (`playwright-stealth`) for critical operations. Rely strictly on CDP connections to Anti-Detect Browsers or C++ patched environments (Camoufox, AdsPower, Multilogin engines).
- **CDP-ATTACH-ONLY**: NEVER use runtime prototype overrides (`Object.defineProperty(navigator, 'webdriver', ...)`) or launch raw unpatched Playwright browsers. Always launch the Anti-Detect binary separately and connect using `chromium.connectOverCDP()`.
- **BEHAVIORAL-BIOMETRICS**: Mouse movements MUST follow Bézier/spline curves with acceleration, deceleration, and micro-overshoots. Form inputs MUST use non-deterministic inter-keystroke intervals (80–320 ms) with occasional backspace/correction patterns — never `page.fill()` or `element.value = ...` at 0 ms.
- **HARDWARE-PROFILE-CONSISTENCY**: The OS specified in the User-Agent MUST match the JA4/JA4T TLS fingerprint, platform fonts list, WebGL renderer string (`UNMASKED_RENDERER_WEBGL`), and screen geometry. Never pair a macOS UA with Linux FreeType fonts or Windows DirectX renderers.
- **WEBRTC-LEAK-PREVENTION**: Configure `disable_non_proxied_udp` or bind WebRTC ICE candidates directly to the residential proxy IP. Failing to prevent WebRTC leaks exposes the real datacenter host IP regardless of the proxy.

## Suggested Process

1. **Connection Strategy**: Do not use standard `playwright.chromium.launch()`. Use `playwright.chromium.connect_over_cdp()` to attach to a running Anti-Detect Browser profile (e.g., AdsPower API, Multilogin) or use a C++ stealth-patched engine (Camoufox).
2. **Behavioral Mimicry Implementation**: Implement Bézier curve mouse trajectory generators with variable step count and randomized overshoot restitution. Use non-deterministic inter-keystroke delays (80–320 ms). Avoid instantaneous form fills.
3. **Fingerprint Consistency Verification**: Run the browser profile against CreepJS, Incolumitas, and Pixelscan to verify zero fingerprint leaks before production. Confirm JA4 TLS fingerprint matches the declared User-Agent platform.
4. **WebRTC & DNS Leak Test**: Verify `disable_non_proxied_udp` is configured and all DNS resolution occurs remotely on the proxy exit node (no host DNS leaks).
5. **Headless Evasion Validation**: Run the profile against Cloudflare Turnstile managed challenge to verify stealth before production use.

## Checklist

- [ ] Script connects via CDP or uses a C++ patched engine (no raw Playwright launch).
- [ ] Bézier/spline mouse movements and 80–320 ms keystroke delays implemented.
- [ ] `playwright-stealth` JS-injection avoided; no `navigator.webdriver` overrides.
- [ ] Browser profile passes CreepJS, Incolumitas, and Pixelscan fingerprint checks.
- [ ] JA4/JA4T TLS fingerprint matches declared User-Agent platform.
- [ ] WebRTC ICE candidate leak prevention configured.
- [ ] Remote DNS resolution verified — no host DNS leak.
- [ ] Script passes Cloudflare Turnstile managed challenge before production.
- [ ] Error handling and retry logic included for network failures.

## Related Skills

- **deploy-mmo-infrastructure**: Provision the Anti-Detect Browsers the script will connect to.
- **turnstile-spin**: Handle Cloudflare Turnstile challenges encountered during automation.
