# Information Gain & 3-Tier Decay Triage Playbook

This playbook establishes the operational protocols for enforcing the Top 10 SERP Information Gain Gate (≥75/100 non-commodity threshold) and triaging content decay across search engines and generative AI citation surfaces.

---

## 1. Top 10 SERP Information Gain Differential Protocol

In an era saturated with automated AI paraphrasing, publishing articles that merely restate existing search engine results creates zero brand authority, risks algorithmic de-indexing (Google Helpful Content / Core Updates), and produces zero citations in generative AI engines (Google AI Overviews, SearchGPT, Perplexity).

Every proposed content brief must pass the **Top 10 SERP Information Gain Gate** before production begins.

```
       Candidate Topic Proposal
                  │
                  ▼
   [ Analyze Top 10 SERP Competitors ]
                  │
                  ▼
      [ Map SERP Consensus Floor ]
(What everyone already says = 0 Value)
                  │
                  ▼
 [ Evaluate 5 Information Gain Vectors ]
  1. Primary Telemetry & Benchmarks
  2. Production Architecture & Code
  3. Counter-Consensus Trade-Offs
  4. Real Incident & Postmortem Data
  5. Interactive Tools & Calculators
                  │
                  ▼
       [ Calculate Non-Commodity Score ]
           /                 \
     Score ≥ 75/100     Score < 75/100
          │                  │
          ▼                  ▼
 [ Commission Brief ]   [ REJECT / REVISE ]
```

### 1.1 The Five Information Gain Vectors

To achieve a passing score, a piece of content must contribute original, uncopied intellectual property across at least one (preferably two) of the following five vectors:

1. **Vector 1: Primary Telemetry & Empirical Benchmarks**:
   - Original hardware measurements, electrical power draws, acoustic measurements, or load-test latency curves.
   - *Production Standard*: Must disclose test methodology, hardware specifications, ambient temperature, sampling duration, and raw tool output (e.g. Hioki 3334 power analyzer, RION NL-52 sound level meter, k6/wrk2 load profiles).

2. **Vector 2: Proprietary Architecture & Production Code**:
   - Concrete configuration files, production diffs, eBPF scripts, or minimal reproducible GitHub repositories.
   - *Production Standard*: Real, executable code solving an edge-case problem that documentation glosses over; zero synthetic pseudo-code.

3. **Vector 3: Counter-Consensus Trade-Off Analysis**:
   - Rigorous, data-backed refutation of widespread industry dogma or vendor marketing claims.
   - *Production Standard*: Demonstrating specifically *where* a popular architectural pattern fails, costs more, or introduces unstated operational burdens (e.g. "Why Microservices Doubled Our AWS Egress Fees and Tripled Latency").

4. **Vector 4: Production Incident & Postmortem Teardowns**:
   - Firsthand accounts of system failures, cascading outage timelines, exact root-cause discoveries, and postmortem remediations.
   - *Production Standard*: Verifiable timelines, exact log extracts, and architectural changes implemented to prevent recurrence.

5. **Vector 5: Interactive Models, Calculators & Tools**:
   - Embedded client-side calculators, sizing simulators, or config file generators.
   - *Production Standard*: Solves a complex mathematical or operational estimation problem directly on the page (e.g. HVAC sizing calculator compliant with TCVN 7830:2021, Kubernetes cluster RAM cost estimator).

---

### 1.2 Non-Commodity Scoring Rubric (0–100)

| Score Tier | Evaluation Criteria | Production Decision |
| :--- | :--- | :--- |
| **85–100 (Exceptional)** | Contributes ≥2 original empirical vectors (e.g. raw hardware benchmarks + downloadable production config). Defines the industry benchmark. | **Approved Immediately**; designated as high-priority core pillar asset. |
| **75–84 (Strong)** | Contributes ≥1 verifiable empirical vector (e.g. firsthand incident postmortem or novel trade-off data). Clearly distinct from SERP baseline. | **Approved for Drafting**; satisfies all gateway requirements. |
| **50–74 (Moderate)** | Well-written synthesis, but relies entirely on publicly available documentation without proprietary telemetry or unique operational data. | **REJECTED**; writer must partner with engineering SME to source proprietary proof. |
| **< 50 (Commodity Skyscraper)** | Paraphrased regurgitation of top 5 Google search results. Zero information gain; pure search engine spam. | **REJECTED PERMANENTLY**; brief cancelled. |

---

## 2. The 3-Tier Content Decay Triage Framework

Content is a depreciating asset. Code samples become outdated, search algorithms shift, and generative AI engines continually recalibrate citation sources. Content Managers must audit portfolio inventory across three distinct decay vectors:

```
+---------------------------------------------------------------------------------------+
| 3-TIER CONTENT DECAY VECTORS & ACTION MATRIX                                          |
+---------------------------------------------------------------------------------------+
| [Tier 1: Algorithmic SERP Decay] ====> >3 rank drop or >25% MoM organic traffic drop  |
| [Tier 2: Generative Citation]    ====> ≥15% citation drop in AI engines over 30 days  |
| [Tier 3: Factual & Temporal]     ====> >18-month stats, deprecated APIs, broken links |
+---------------------------------------------------------------------------------------+
```

### 2.1 Tier 1: Algorithmic SERP Decay
- **Diagnostic Triggers**:
  - Primary target keyword drops >3 positions on Google SERP over a 30-day moving window.
  - Organic clicks/impressions in Google Search Console decline >25% Month-over-Month (MoM) without seasonal explanation.
- **Root Causes**:
  - Search intent shift (e.g. query moved from conceptual definition to software tool comparison).
  - Competitor published a superior asset scoring higher on Information Gain.
  - SERP feature displacement (Google AI Overviews or Video Packs occupying organic real estate above the fold).
- **Remediation Action**: **Structural Rewrite or Expansion** within **30 days**. Re-evaluate Top 10 SERP consensus, inject new Information Gain vectors, and refresh heading structures.

---

### 2.2 Tier 2: Generative Engine / GEO Citation Decay
- **Diagnostic Triggers**:
  - Citation frequency drops ≥15% across Google AI Overviews, SearchGPT, and Perplexity over a 30-day tracking window.
  - Brand or domain disappears from generative comparison queries ("Best edge database for Astro").
- **Root Causes**:
  - Missing atomic BLUF answer block (≤60 words) at section openings, preventing LLM passage extraction.
  - Low factual density (<3 verifiable data points per 500 words).
  - Missing Schema.org entity markup (`about` and `mentions` Wikidata tags).
  - Lack of markdown comparison tables (LLMs heavily weight structured tabular data for synthesis).
- **Remediation Action**: **GEO Optimization Sprint** within **30 days**. Inject atomic answer blocks, add markdown comparison tables, and refresh Wikidata entity bindings.

---

### 2.3 Tier 3: Factual & Temporal Decay
- **Diagnostic Triggers**:
  - Content references framework or library versions that are deprecated or unsupported.
  - Sourced statistics or industry survey figures are >18 months old.
  - Automated link crawler detects HTTP 404/410 non-200 outbound links.
- **Root Causes**:
  - Natural software obsolescence; platform breaking changes; expired research links.
- **Remediation Action**: **Quick Patch** within **15 days**. Bump dependency versions, verify code snippets against current LTS runtime, update data points to latest annual figures, and repair broken hyperlinks.

---

## 3. Remediation Action Types, SLAs & ROT Pruning

When auditing portfolio inventory, assign every URL to one of four lifecycle actions governed by strict Service Level Agreements (SLAs):

| Action Classification | Trigger & Condition | Scope of Work | Enforceable SLA |
| :--- | :--- | :--- | :--- |
| **1. Quick Patch** | Tier 3 decay; broken links, outdated stats, minor version bump | Update facts, replace stale numbers, fix links, verify CLI flags | **≤15 days** from triage |
| **2. Structural Rewrite** | Tier 1 or Tier 2 decay on high-value asset; high historical authority | Re-run Top 10 SERP audit; inject fresh telemetry; restructure BLUF and schema | **≤30 days** from triage |
| **3. Consolidation (301)**| Keyword cannibalization; 2–3 thin articles competing for same query | Merge strongest sections into primary pillar; implement 301 redirect on deprecated URLs | **≤20 days** from triage |
| **4. Decommission (410)** | Zero traffic, zero backlinks, outdated topic, ROT trivial asset | Issue HTTP 410 Gone; remove internal links; reclaim crawl equity | **≤10 days** from triage |

### 3.1 ROT Pruning Methodology (Redundant, Outdated, Trivial)

Zombie pages that generate zero traffic and hold zero backlinks harm site-wide crawl efficiency and dilute domain topical authority. Apply the ROT criteria monthly:

- **Redundant (Cannibalizing)**:
  - URLs targeting identical search queries with overlapping title tags. Merge them into the highest-performing URL via permanent 301 redirects.
- **Outdated (Beyond Economical Repair)**:
  - Articles covering abandoned technologies, retired product lines, or one-off event announcements from >2 years ago. If they hold external backlinks, 301 redirect to the closest thematic pillar. If zero backlinks, return HTTP 410 Gone.
- **Trivial (Low Quality / Zero Engagement)**:
  - 300-word thin posts that generate <5 organic visits over a 180-day window and score <40 on Information Gain. Decommission permanently with HTTP 410 Gone.
