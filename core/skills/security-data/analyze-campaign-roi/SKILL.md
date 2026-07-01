---
name: analyze-campaign-roi
description: Analyze S2S conversion data, monitor ad account die-rates, and autonomously calculate/optimize campaign ROI based on proxy and API costs.
---

# Analyze Campaign ROI

Use this skill to perform financial and risk analysis of MMO campaigns, combining revenue metrics with operational costs (proxies, AI APIs, account replacements) to determine true profitability.

## Core Rules

- **DATA-CLASSIFICATION**: Campaign revenue and tracking data must be treated as highly sensitive. Do not expose API keys or raw profit margins in untrusted logs or unencrypted channels.

## Suggested Process

1. **Data Ingestion**: Pull conversion and revenue data from trackers (Voluum, Binom) or directly from affiliate networks via API.
2. **Cost Calculation**: Aggregate daily ad spend, proxy bandwidth costs, API consumption costs (e.g., OpenAI tokens), and the amortized cost of replacing banned accounts ("die-rate").
3. **True ROI Calculation**: Subtract all operational costs from the raw revenue to determine the True ROI.
4. **Optimization Strategy**: Identify underperforming campaigns, bad proxy subnets, or creatives with high ban rates, and generate actionable recommendations to pause or scale.

## Checklist

- [ ] Revenue data is successfully ingested from S2S trackers.
- [ ] Operational costs (proxies, API, die-rate) are factored into the ROI calculation.
- [ ] Sensitive financial data is handled securely.
- [ ] Actionable recommendations (pause/scale) are generated.

## Related Skills

- `setup-tracking-system`: For configuring the data sources analyzed by this skill.
- `analyze-data`: For generic data analysis tasks outside of MMO context.
