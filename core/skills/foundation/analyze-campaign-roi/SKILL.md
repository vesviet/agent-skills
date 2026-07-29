---
name: analyze-campaign-roi
description: Analyze S2S conversion data, monitor ad account die-rates, and calculate campaign ROI based on proxy and API costs. Use when evaluating campaign profitability, diagnosing tracking attribution gaps, comparing offer performance, or deciding to pause or scale ad spend.
---

# Analyze Campaign ROI

Use this skill to perform financial and risk analysis of MMO campaigns, combining revenue metrics with operational costs (proxies, AI APIs, account replacements) to determine true profitability.

## Legal & Compliance Notice

This skill analyzes financial data only and does not itself execute any platform-facing technique. "Die-rate" here means the observed rate of account restrictions from any cause; factoring it into ROI is a financial modeling practice, not an endorsement of any technique that causes it. See `deploy-mmo-infrastructure`, `manage-mmo-assets`, and `deploy-proxyware-fleet` for the compliance notices covering the underlying infrastructure and asset-management techniques.

## When to Use

- evaluating whether a campaign is actually profitable after costs
- diagnosing attribution gaps between tracker and ad network
- comparing offer/creative performance to decide pause vs scale
- monitoring account "die-rate" and replacement cost trends
- preparing a profitability handoff for task-planner or mmo-engineer

## Example (True ROI calculation)

```python
revenue      = 4200.0
ad_spend     = 1800.0
proxy_cost   = 220.0
api_cost     = 95.0
die_rate     = 0.12      # 12% of accounts banned
acct_cost    = 40.0
replace_cost = die_rate * acct_cost * 50  # 50 accounts in rotation

true_roi = (revenue - ad_spend - proxy_cost - api_cost - replace_cost) / (ad_spend + proxy_cost + api_cost + replace_cost)
print(f"True ROI: {true_roi:.2%}")
```

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
- [ ] Sensitive financial data is handled securely and not exposed in untrusted logs.
- [ ] Actionable recommendations (pause/scale) are generated for each campaign.
- [ ] Underperforming proxy subnets or creatives are identified.
- [ ] Analysis output is structured and ready for handoff to task-planner or mmo-engineer.

## Related Skills

- **setup-tracking-system**: Configure the S2S data sources analyzed by this skill.
- **analyze-data**: Generic data analysis tasks outside the MMO context.
