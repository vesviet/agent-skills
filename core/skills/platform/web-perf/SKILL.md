---
name: web-perf
description: Analyzes web page performance using Chrome DevTools MCP — measuring Core Web Vitals (LCP, INP, CLS), identifying render-blocking resources, network dependency chains, and caching issues to produce specific, actionable optimization recommendations. Use when auditing Lighthouse scores, debugging slow page loads, profiling Core Web Vitals regressions, or validating performance improvements before release.
---

# Web Perf

Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps.

Your knowledge of web performance metrics, thresholds, and tooling APIs may be outdated. **Prefer retrieval over pre-training** when citing specific numbers or recommendations.

## Core Rules
- Verify MCP tools are available (`navigate_page` or `performance_start_trace`) before starting.
- Verify claims by checking network requests, DOM, or codebase—then state findings definitively.
- Confirm something is unused in the trace before suggesting its removal.
- Skip render-blocking resources with 0ms estimated impact from recommendations.
- Cite specific resource names and sizes (e.g. "compress hero.png (450KB) to WebP") instead of generic advice.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| web.dev | `https://web.dev/articles/vitals` | Core Web Vitals thresholds, definitions |
| Chrome DevTools docs | `https://developer.chrome.com/docs/devtools/performance` | Tooling APIs, trace analysis |
| Lighthouse scoring | `https://developer.chrome.com/docs/lighthouse/performance/performance-scoring` | Score weights, metric thresholds |

## Suggested Process
1. Navigate to the target URL using Chrome DevTools.
2. Record a performance trace on reload to capture cold-load metrics.
3. Call `performance_analyze_insight` to check Core Web Vitals metrics.
4. List and inspect network requests to discover render-blocking paths and dependencies.
5. Take accessibility tree snapshots to audit elements' contrast and ARIA labels.

## Checklist
- [ ] Chrome DevTools trace was recorded and fetched.
- [ ] Core Web Vitals are analyzed and thresholds classified.
- [ ] Render-blocking scripts and stylesheets are identified.
- [ ] Image assets and media dimensions are checked for layout shifts (CLS).
- [ ] Accessibility tree contrast and name attributes are validated.

## Related Skills
- **wrangler**: Check deployment compatibility parameters and cache settings.
- **debug-workers-edge**: Inspect edge runtime response headers.
