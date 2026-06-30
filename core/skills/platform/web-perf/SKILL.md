---
name: web-perf
description: Analyzes web page performance using Chrome DevTools MCP — measuring Core Web Vitals (LCP, INP, CLS), identifying render-blocking resources, network dependency chains, and caching issues to produce specific, actionable optimization recommendations. Use when auditing Lighthouse scores, debugging slow page loads, profiling Core Web Vitals regressions, or validating performance improvements before release.
---

# Web Perf

Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps.

Your knowledge of web performance metrics, thresholds, and tooling APIs may be outdated. **Prefer retrieval over pre-training** when citing specific numbers or recommendations.

## Core Rules
- Verify MCP tools are available (`navigate_page` or `performance_start_trace`) before starting.
- Verify claims by checking network requests, DOM, or codebase — then state findings definitively.
- Confirm something is unused in the trace before suggesting its removal.
- Skip render-blocking resources with 0ms estimated impact from recommendations.
- Cite specific resource names and sizes (e.g. "compress hero.png (450KB) to WebP") instead of generic advice.
- **Always distinguish between lab data (Lighthouse, DevTools) and field data (CrUX, RUM)** — Lighthouse scores do not always reflect real-user experience; always note which you are reporting.

### 2025-2026: INP as Primary Responsiveness Metric

- **INP (Interaction to Next Paint) replaced FID as the Core Web Vitals responsiveness metric in March 2024** — do not reference FID as the current standard; it is deprecated.
- **INP thresholds:** good < 200ms | needs improvement 200–500ms | poor > 500ms.
- **INP attribution:** use the `performance_analyze_insight` or Chrome DevTools Performance panel to identify the long-task source behind poor INP — common causes are synchronous JavaScript in event handlers, forced layout/reflow on input, and React 17 or earlier event delegation patterns.
- **AI-generated performance analysis validation:** when using AI tools (e.g., LLM-based performance audit summaries) to summarize trace data, verify all recommendations against the actual network waterfall and trace — AI summaries frequently misattribute the root cause when multiple bottlenecks are present.
- **INP optimization patterns (2025):** React 18 concurrent rendering, `scheduler.yield()`, `isInputPending()`, input debouncing with `requestAnimationFrame`, and splitting long tasks with `setTimeout(0)` are the primary INP fixes; confirm which pattern applies before recommending.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| web.dev | `https://web.dev/articles/vitals` | Core Web Vitals thresholds, definitions, INP guide |
| Chrome DevTools docs | `https://developer.chrome.com/docs/devtools/performance` | Tooling APIs, trace analysis |
| Lighthouse scoring | `https://developer.chrome.com/docs/lighthouse/performance/performance-scoring` | Score weights, metric thresholds |
| CrUX dashboard | `https://developer.chrome.com/docs/crux` | Field data by origin and URL |

## Suggested Process

### 1. Set Up Measurement Baseline
- Navigate to the target URL using Chrome DevTools MCP.
- Record both a cold-load trace (empty cache) and a warm-load trace (cached assets).
- Capture field data from CrUX if available — note the gap between lab and field.

### 2. Analyze Core Web Vitals
- Call `performance_analyze_insight` to classify each CWV against good/needs-improvement/poor thresholds.
- For **LCP**: identify the LCP element, its discovery time, load delay, and render delay. Check if it is an `<img>` with missing `fetchpriority="high"` or a background-image (not optimizable by the browser).
- For **INP**: attribute the worst interaction event to its long-task source. Check for layout thrash, synchronous JS on input, and un-yielded event handlers.
- For **CLS**: identify the shifted element and its layout instability source (missing width/height, late-injected content, ad slots, web fonts).

### 3. Inspect Network and Resource Chain
- List render-blocking scripts and stylesheets with estimated ms impact.
- Identify uncompressed or oversized images; check format (WebP, AVIF preferred).
- Check caching headers (Cache-Control, ETag) for static assets.
- Find unused CSS/JS — confirm via Coverage tab before recommending removal.

### 4. Produce Actionable Recommendations
- Order fixes by impact: fixes with >100ms estimated gain first.
- Cite specific resource names, sizes, and file paths — no generic recommendations.
- State whether each fix requires code change, build config change, or CDN config change.

### 5. Validate Improvements
- Re-record trace after implementing fixes.
- Compare before/after for each metric — report delta, not just the new number.

## Output Format

```markdown
## Web Performance Audit — <URL>

Measurement type: [lab / field / both]
Tool: Chrome DevTools MCP | Lighthouse | CrUX

### Core Web Vitals
| Metric | Value | Status | Data Source |
|--------|-------|--------|-------------|
| LCP | Xs | good/NI/poor | lab/field |
| INP | Xms | good/NI/poor | lab/field |
| CLS | X | good/NI/poor | lab/field |

### Root Causes (ordered by impact)
1. <specific resource or code path> — <estimated impact>ms
2. ...

### Recommendations
- [ ] Fix: <specific action> — <file/resource> — impact: ~Xms
- [ ] ...

### Skipped
- <resource> — 0ms estimated impact

### Residual Risk
- <any metric still in poor range after fixes>
```

## Anti-Patterns To Reject

- reporting Lighthouse score as the only measure without noting it is lab data
- recommending removal of a resource before confirming it is unused in the trace
- citing FID instead of INP for responsiveness measurement (deprecated March 2024)
- providing generic advice ("reduce JavaScript bundle size") without naming the specific file and size
- attributing INP issues to the wrong cause (e.g., blaming render-blocking when the actual cause is a synchronous event handler)

## Checklist

- [ ] Chrome DevTools trace recorded (cold-load and warm-load if needed)
- [ ] Core Web Vitals classified with correct thresholds (INP, not FID)
- [ ] LCP, INP, and CLS root causes attributed to specific code or resources
- [ ] Render-blocking scripts and stylesheets identified with ms impact
- [ ] Image assets checked for format (WebP/AVIF) and size
- [ ] Recommendations ordered by estimated impact
- [ ] Lab vs. field data distinction stated in the report
- [ ] Before/after comparison run after implementing fixes

## Related Skills

- **wrangler**: Check deployment compatibility parameters and cache settings for Workers-hosted assets.
- **debug-workers-edge**: Inspect edge runtime response headers affecting TTFB.
- **performance-profiling**: Use for backend latency profiling that contributes to TTFB and LCP load delay.

