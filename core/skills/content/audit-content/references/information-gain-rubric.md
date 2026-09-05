# Information Gain Score Rubric (100-Point SERP Diff Matrix)

Reference evaluation matrix for `audit-content` and the `content-manager` role. Measures the net-new value that a refreshed or newly-drafted article contributes beyond existing Top 10 SERP results.

---

## 1. Five-Vector Information Gain Scoring Matrix

The Information Gain Score evaluates an article across five empirical vectors, awarding up to **100 points**:

| Vector | Description | Point Weight | Scoring Criteria |
| :--- | :--- | :---: | :--- |
| **1. Novel Empirical Data & Benchmarks** | Proprietary performance benchmarks, throughput curves, latency percentiles, or cost analyses not found on the SERP. | **0 – 35 pts** | 30–35: Original multi-variable benchmarks with reproducible scripts.<br>15–29: Targeted performance metrics or load testing results.<br>0–14: Re-cited public benchmarks or generic statistics. |
| **2. Production Telemetry & Case Evidence** | Firsthand logs, architecture post-mortems, real-world failure modes, or production incident analyses. | **0 – 25 pts** | 20–25: Full incident timeline, stack trace, and post-mortem telemetry.<br>10–19: Firsthand production deployment notes with specific metrics.<br>0–9: Hypothetical examples or sanitized generic stories. |
| **3. Proprietary Architecture & Frameworks** | Novel system topologies, decision trees, bespoke state machines, or original code patterns. | **0 – 20 pts** | 16–20: Original architectural decision tree or custom algorithmic pattern.<br>8–15: Customized adaptation of an industry pattern with trade-off analysis.<br>0–7: Standard boilerplate architecture diagram. |
| **4. Contrarian / Nuanced Trade-Offs** | Direct challenge to conventional wisdom, documenting hidden failure modes, edge cases, and architectural caveats. | **0 – 10 pts** | 8–10: Validated contrarian analysis with empirical counter-evidence.<br>4–7: Detailed edge case breakdown with known operational limits.<br>0–3: Conventional consensus echoing without caveat analysis. |
| **5. SME Verification & Practitioner Insight** | Direct commentary or authored synthesis from named subject matter experts with verified credentials. | **0 – 10 pts** | 8–10: Named principal engineer / architect quote or byline with verified GitHub/LinkedIn.<br>4–7: Attributed quotes from credible industry peers.<br>0–3: Unattributed quotes or anonymous opinions. |

---

## 2. Information Gain Rating Tiers & Thresholds

```
Total Information Gain Score = Vector 1 + Vector 2 + Vector 3 + Vector 4 + Vector 5
```

| Score Band | Rating | Gate Decision | Rationale & Action |
| :---: | :--- | :---: | :--- |
| **85 – 100** | **Exceptional** | **PASS** | High citability for Google AI Overviews and SearchGPT; industry-defining reference piece. |
| **70 – 84** | **Strong** | **PASS** | Clear information gain verified against top 10 competitors; approved for publication. |
| **50 – 69** | **Moderate** | **FAIL / HOLD** | Contains minor unique elements but largely overlaps with top 10 SERP; requires additional telemetry or benchmarks. |
| **30 – 49** | **Low** | **FAIL / REJECT** | Derivative synthesis of existing articles; must not be published. |
| **0 – 29** | **Zero** | **FAIL / REJECT** | Direct paraphrasing or skyscraper regurgitation of competitors; immediate rejection. |

### Minimum Passing Threshold
- An article or content refresh must achieve **≥ 70 points** (rating: **"strong"** or **"exceptional"**) to clear the Information Gain Quality Gate.

---

## 3. SERP Diff Audit Methodology

1. **Top 10 Competitor Baseline**: Scan the top 10 organic results for the target query. Extract the core arguments, shared diagrams, and commonly cited statistics.
2. **Overlap Isolation**: Identify sections in the draft that merely repeat what the top 5 competitors already state.
3. **Net-New Delta Verification**: Verify that the article introduces at least **two concrete assets** (e.g., telemetry chart, custom benchmark, decision matrix) absent from the competitor set.
4. **Contract Recording**: Document `information_gain_rating` and `net_new_assets` in `contracts/schemas/content-handoff.json` or `contracts/schemas/content-audit-report.json`.
