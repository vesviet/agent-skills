# Core Web Vitals and Performance Guide

This guide provides technical reference specifications for auditing Core Web Vitals (CWV), diagnosing client-side rendering and hydration bottlenecks, and structuring engineering escalation tickets.

---

## 1. Core Web Vitals Standard Thresholds

Google's Core Web Vitals represent user-centric performance metrics measured at the **75th percentile** of page visits across mobile and desktop devices (Chrome User Experience Report / CrUX).

| Metric | Full Name | Good (Pass) | Needs Improvement | Poor | Primary Architectural Driver |
|--------|-----------|-------------|-------------------|------|-------------------------------|
| **LCP** | Largest Contentful Paint | $\le 2.5\text{ s}$ | $2.5 - 4.0\text{ s}$ | $> 4.0\text{ s}$ | Server TTFB, resource load delay, render-blocking CSS/JS, hero image optimization |
| **INP** | Interaction to Next Paint | $\le 200\text{ ms}$ | $200 - 500\text{ ms}$ | $> 500\text{ ms}$ | Main-thread JS execution, heavy hydration, long tasks (>50ms), un-debounced event listeners |
| **CLS** | Cumulative Layout Shift | $\le 0.10$ | $0.10 - 0.25$ | $> 0.25$ | Un-sized images/videos, FOIT/FOUT font shifts, dynamically injected banners/ads |

---

## 2. Largest Contentful Paint (LCP) Diagnostics

LCP marks the point in the page load timeline when the main content (hero image, heading text, or banner) has likely loaded.

### 2.1 The Four Sub-Parts of LCP
1. **Time to First Byte (TTFB)**: Server processing and initial HTML delivery (~40% of LCP budget).
2. **Resource Load Delay**: Time between initial HTML receipt and browser initiating the fetch for the LCP resource (<10%).
3. **Resource Load Duration**: Time taken to download the LCP asset (~40%).
4. **Element Render Delay**: Time between asset download completion and full paint on screen (<10%).

### 2.2 Optimization Interventions
- **Preload Critical Hero Assets**: Declare `<link rel="preload" as="image" href="..." fetchpriority="high">` in the document `<head>`.
- **Eliminate Render-Blocking CSS/JS**: Defer non-critical CSS, inline critical path styles, and load non-essential scripts asynchronously (`defer` or `type="module"`).
- **Modern Responsive Image Formats**: Serve AVIF or WebP with explicit `srcset` and `sizes` attributes matching device breakpoints.
- **Edge Caching**: Cache rendered HTML at edge CDN points (Cloudflare Pages/Workers) to compress TTFB to $< 100\text{ ms}$.

---

## 3. Interaction to Next Paint (INP) and Hydration Profiling

INP measures the responsiveness of a page to user interactions (clicks, taps, key presses) by assessing the longest latency between input and next visual frame update throughout the full session lifecycle.

### 3.1 JavaScript Hydration Bottlenecks
Modern full-stack frameworks (React, Next.js) often deliver pre-rendered SSR HTML, but the page remains unresponsive while the client-side JavaScript engine:
1. Downloads massive script bundles.
2. Parses and compiles JavaScript on the browser thread.
3. Attaches event listeners and reconciles virtual DOM trees (Hydration).

Any user click during this window encounters a frozen main thread, triggering severe INP degradation ($> 500\text{ ms}$).

### 3.2 Actionable Technical Remediation
- **Islands Architecture (Astro)**: Prefer static HTML by default; isolate interactivity into micro-islands using `client:idle`, `client:visible`, or `client:media` directives.
- **Break Up Long Tasks (>50ms)**: Yield execution back to the browser using `scheduler.yield()` or `setTimeout(..., 0)` inside heavy calculations.
- **De-prioritize Off-Screen Scripts**: Move third-party tracking scripts (GTM, analytics) to Web Workers (Partytown) or load via `requestIdleCallback`.

---

## 4. Cumulative Layout Shift (CLS) Diagnostics

CLS measures visual stability by calculating the sum total of all unexpected layout shift scores for every unexpected layout shift that occurs during the entire page lifespan.

$$\text{Layout Shift Score} = \text{Impact Fraction} \times \text{Distance Fraction}$$

### 4.1 Common CLS Root Causes and Fixes

#### A. Un-sized Images and Media
Browsers cannot allocate layout space before image assets finish downloading unless dimensions are declared.
- **Fix**: Always specify explicit `width` and `height` attributes on `<img>` and `<video>` elements, paired with CSS `aspect-ratio`:
  ```html
  <img src="/hero.webp" width="1200" height="630" style="aspect-ratio: 1200 / 630; width: 100%; height: auto;" alt="Guide" />
  ```

#### B. Web Font Shifts (FOUT / FOIT)
Late-swapping fallback fonts with custom web fonts can shift paragraph heights.
- **Fix**: Use `font-display: swap` in `@font-face`, accompanied by size adjust overrides (`size-adjust`, `ascent-override`, `descent-override`) to match fallback font metrics with the web font.

#### C. Dynamically Injected Banners and Ads
Injecting newsletter forms, cookie consent notices, or ads above existing content pushes page elements down.
- **Fix**: Reserve container space in CSS with static `min-height` or skeleton placeholders before dynamic elements mount.

---

## 5. Technical Escalation Ticket Formulation

When technical SEO audits uncover infrastructure or rendering issues that require developer intervention, the SEO Analyst structures tickets formatted for direct engineering triage.

### 5.1 Escalation Ticket Schema Mapping

Each ticket maps directly to the `technical_escalations` array in `contracts/schemas/seo-audit-report.json`:

```json
{
  "type": "core_web_vitals",
  "description": "LCP exceeds 3.4s on mobile product templates due to un-preloaded hero image and render-blocking font styles.",
  "owner": "frontend-developer",
  "priority": "must_do_before_publish"
}
```

### 5.2 Role Ownership and Priority Guidelines

| Target Problem Area | Designated Role Owner | Typical Priority Criteria |
|---------------------|-----------------------|----------------------------|
| Un-sized images, CLS shift containers, hydration INP, client bundle size | `frontend-developer` | `must_do_before_publish` if CLS > 0.25 or INP > 500ms |
| Server origin TTFB, edge caching, compression (Brotli), CDN routing, SSL | `devops-engineer` / `cloudflare-engineer` | `must_do_before_publish` if TTFB > 1000ms; `post_publish` if 500-1000ms |
| Redirect rules at edge, robots.txt routing, automated sitemap cron generation | `cloudflare-engineer` / `devops-engineer` | `must_do_before_publish` if canonical/redirect loop is present |
