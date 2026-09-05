# AI Semantic Flaw Score Rubric (0–100 Penalty Deduction Matrix)

Reference scoring framework for `audit-content` and the `content-manager` role. Used during content refreshes and pre-publish audits to detect and eliminate machine-generated patterns, stylistic slop, and ungrounded assertions.

---

## 1. Five-Dimension Penalty Matrix

The AI Semantic Flaw Score begins at **0 penalty points** (perfect human-grade score) and accumulates penalties across five distinct flaw dimensions.

| Dimension | Evaluation Criteria | Penalty Weight | Max Deduction |
| :--- | :--- | :--- | :--- |
| **1. Cliché Density** | Occurrence of banned AI clichés ("delve", "tapestry", "testament", "unlock", "game-changer", "beacon", "pinnacle", "foster", "realm", "harness", "navigating the landscape"). | -10 points per cliché | -40 points |
| **2. Cadence Uniformity** | Monotonous sentence lengths lacking 20/60/20 burstiness. Standard deviation of sentence length < 5.0 words, or ≥3 consecutive sentences of identical word count. | -15 to -25 points | -25 points |
| **3. Vagueness & Fluff Ratio** | Empty transitional filler ("In today's fast-paced digital world", "Needless to say", "At the end of the day") or generic summaries without technical specifics. | -5 points per paragraph | -20 points |
| **4. Hallucination & Speculation Risk** | Unsubstantiated metrics, unverified library versions, fabricated command-line flags, or claims marked `[UNVERIFIED]`. | -15 points per claim | -30 points |
| **5. Passive Voice & Hedging** | Active voice below 85%, or excessive epistemic hedging ("it could perhaps be argued that it might assist"). | -5 to -15 points | -15 points |

---

## 2. Quality Gate Thresholds & Actions

The total flaw score dictates the editorial action:

```
Total Flaw Score = Cliché Deduction + Cadence Deduction + Vagueness Deduction + Hallucination Deduction + Passive Deduction
```

| Total Flaw Score | Quality Classification | Gate Decision | Required Remediation |
| :---: | :--- | :---: | :--- |
| **0 – 15** | **Clean / Human-Grade** | **PASS** | Publishable. Minor phrasing polish optional. |
| **16 – 30** | **Minor AI Flaws** | **CONDITIONAL** | Manual editorial pass required: strip clichés, vary sentence rhythm, verify flagged claims. |
| **> 30** | **Severe AI Slop** | **REJECT / FAIL** | Automatic rejection. Draft must be rewritten from scratch or re-delegated with empirical constraints. |

---

## 3. Remediation Protocols

1. **Clichés**: Replace with concrete engineering terms or delete the sentence if it provides no informational value.
2. **Cadence**: Split run-on compound sentences into punchy statements (<12 words) and combine adjacent fragments into rich trade-off comparisons (>25 words).
3. **Vagueness**: Replace abstract adjectives with exact metrics, production telemetry, or specific architectural components.
4. **Hallucination**: Check every statistic against Tier 1/2 sources. If not verifiable, delete the claim immediately.
5. **Passive Voice**: Identify the true actor (e.g., "The Redis thread", "The kernel", "The database engine") and place it as the grammatical subject.
