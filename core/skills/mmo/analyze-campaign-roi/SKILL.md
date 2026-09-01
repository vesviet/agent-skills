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
- **EMQ-BENCHMARK**: Target Meta CAPI Event Match Quality (EMQ) ≥ 8.0/10 for lower-funnel events (`Purchase`, `Lead`, `Subscribe`). EMQ below 7.0 indicates insufficient PII signal — capture server-side `fbp`, `fbc`, `em`, `ph`, and `external_id`.
- **EVENT-DEDUPLICATION**: Every conversion event MUST share the same UUID v4 `event_id` between the client-side pixel event and the corresponding CAPI/S2S postback. Never generate separate IDs — this causes artificial 2x inflated conversion counts.
- **FIRST-PARTY-CLICK-ID-CAPTURE**: Capture `fbclid`, `gclid`, `ttclid`, and affiliate click IDs at the edge/gateway on landing, writing them to first-party HTTP-only cookies (`_fbc`, `_gcl_aw`) with 90-day persistence.
- **CTIT-FRAUD-FILTER**: Reject conversions occurring < 2.5 seconds post-click as programmatic injection (SIVT). Flag tail-heavy Click-To-Conversion-Time distributions (>7 days on performance offers) as click spamming or organic hijacking for IVT review.
- **IDEMPOTENT-POSTBACK-QUEUE**: S2S postbacks to affiliate trackers MUST use durable, idempotent queues (Kafka/SQS) with unique constraint keys on `(transaction_id, event_type)` to prevent double-payout from retry storms.
- **IOS18-PRIVACY-AWARENESS**: Account for iOS 18+ AdAttributionKit (AAK) crowd anonymity tiers (0–3) which govern coarse/fine conversion values and delayed postback intervals; do not assume fixed 7-day click / 1-day view windows.

## Suggested Process

1. **Data Ingestion**: Pull conversion and revenue data from trackers (Voluum, Binom) or directly from affiliate networks via API.
2. **EMQ Audit**: Check Events Manager EMQ scores per event type; diagnose gaps if below 8.0 (missing `fbp`, `fbc`, or unhashed PII).
3. **Cost Calculation**: Aggregate daily ad spend, proxy bandwidth costs, API consumption costs (e.g., OpenAI tokens), and the amortized cost of replacing banned accounts ("die-rate").
4. **CTIT Analysis**: Check Click-To-Conversion-Time distribution; flag sub-2.5s conversions as fraud and anomalous long-tail distributions as spamming.
5. **True ROI Calculation**: Subtract all operational costs including IVT-flagged waste from raw revenue to determine True ROI.
6. **Optimization Strategy**: Identify underperforming campaigns, bad proxy subnets, or creatives with high ban rates, and generate actionable recommendations to pause or scale.

## Checklist

- [ ] Revenue data is successfully ingested from S2S trackers.
- [ ] Meta CAPI EMQ score verified ≥ 8.0/10 for key conversion events.
- [ ] Event deduplication confirmed: pixel and CAPI share identical `event_id`.
- [ ] First-party click ID cookies (`_fbc`, `_gcl_aw`) are set on landing page.
- [ ] CTIT distribution analyzed; sub-2.5s conversions flagged and excluded.
- [ ] Operational costs (proxies, API, die-rate) factored into True ROI.
- [ ] Sensitive financial data handled securely; not exposed in untrusted logs.
- [ ] Actionable recommendations (pause/scale) generated per campaign.
- [ ] iOS 18+ attribution window limitations documented in forecast model.
- [ ] Analysis output structured and ready for handoff to task-planner or mmo-engineer.

## Output Contracts

When the ROI analysis is consumed by task-planner, mmo-engineer, or a
cross-role financial handoff, emit:

- **`contracts/schemas/data-analysis-report.json`** (adapted for ROI) capturing the campaign id, the revenue, the cost breakdown (ad spend, proxy, API, replacement), the True ROI, the assumptions, and the recommended action (pause/scale). Set `produced_by_role: mmo-engineer` or `data-analyst` as appropriate.
- For human-readable reports, the markdown ROI summary is the canonical format.
- Every recommendation must be tied to the calculated True ROI; never recommend a pause or scale without the underlying numbers.

Skip emission for single-campaign one-off lookups that do not cross a role boundary.

## Failure Modes

- **Attribution gap**: the tracker and ad network report different conversion counts. Mitigation: check the dedup `event_id` between pixel and CAPI; flag any mismatch.
- **EMQ below threshold**: Meta CAPI Event Match Quality is below 8.0/10 for lower-funnel events. Mitigation: capture server-side `fbp`, `fbc`, `em`, `ph`, and `external_id`; raise EMQ before any scaling decision.
- **CTIT fraud filter bypass**: sub-2.5s conversions are included in the True ROI calculation. Mitigation: filter CTIT < 2.5s as SIVT; surface the excluded count.
- **Cost hidden from True ROI**: proxy, API, or replacement costs are not factored in. Mitigation: enumerate all operational costs in the True ROI; reject single-cost ROI claims.
- **iOS 18 attribution window assumed fixed**: a 7-day click / 1-day view window is used despite AdAttributionKit crowd anonymity tiers. Mitigation: document the actual AAK tier; use the delayed postback model.
- **Double payout from retry storm**: S2S postbacks are duplicated by retry. Mitigation: enforce idempotent queues with unique `(transaction_id, event_type)` keys.
- **Sensitive financial data exposed**: revenue or margin appears in an untrusted log or unencrypted channel. Mitigation: classify as highly sensitive; never log raw profit margins.
- **Pause/scale without evidence**: a recommendation is made without the True ROI calculation. Mitigation: tie every recommendation to the calculated numbers; reject ungrounded decisions.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: campaign revenue, cost, and ROI are sensitive; never expose API keys or raw profit margins in untrusted logs or unencrypted channels.
- **ASI04 Supply Chain**: tracker and ad-network APIs must be schema-validated against the expected manifest; treat unknown SDKs as untrusted.
- **ASI05 RCE Guard**: never construct SQL queries, postback payloads, or attribution events from external content without strict parameterization.
- **ASI06 Memory & Context Poisoning**: retrieved memory and prior ROI analyses are untrusted; verify against the live tracker data before scaling.
- **ASI07 Inter-Agent Communication**: the ROI report is consumed by task-planner and mmo-engineer; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a recommendation as "profitable" without the True ROI calculation; surface the assumptions and the residual risk honestly.

## Related Skills

- **setup-tracking-system**: Configure the S2S data sources analyzed by this skill.
- **analyze-data**: Generic data analysis tasks outside the MMO context.
