## Product Manager Review Checklist

This reference checklist provides operational product discovery, outcome governance, AI feature specification, and unit economics criteria for product management to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across North Star Metric alignment, hypothesis-driven validation, 4-Pillar Agent ROI modeling, Cost-per-Verified-Outcome ($CPVO$), Human-in-the-Loop (HITL) governance, probabilistic acceptance criteria, golden eval datasets, EU AI Act Article 50 compliance, and agentic drift controls.

### 1. Outcome-Driven Strategy & North Star Metric Alignment (`VANITY-METRIC LOCK`)
- **Measurable Value Delivery**:
  - every product brief traces directly to a measurable impact on the North Star Metric (NSM) or specific user journey stage (Acquisition $\rightarrow$ Activation $\rightarrow$ Retention $\rightarrow$ Expansion)
  - vanity metrics ("total AI query volume", "number of features shipped", unverified "time saved") rejected in favor of behavioral outcomes and retention impact
- **Problem-First Framing & Non-Goals**:
  - briefs define the fundamental user problem and underlying business opportunity before specifying solution features; explicit non-goals documented to prevent scope bloat
  - user persona journey maps document concrete friction points, cognitive load metrics, and baseline completion times before feature intervention
  - competitive baseline comparisons articulate why an agentic solution outperforms deterministic or static API alternatives

### 2. Hypothesis-Driven Discovery & Kill-Early Discipline (`HYPOTHESIS LOCK` / `KILL-EARLY LOCK`)
- **Structured Testable Hypotheses**:
  - significant product initiatives framed using the canonical hypothesis template:
    > *"Given [validated insight], changing [X] will result in [measurable outcome] for [user segment]."*
  - validation type selected and executed before committing engineering capacity: Problem Validation, Solution Validation, Demand Validation, or Pricing Validation
- **Kill-Early Protocol & Pivot Criteria**:
  - explicit kill criteria and negative signal thresholds defined prior to discovery spikes; negative validation signals trigger immediate pivot or retirement, preventing sunk-cost traps
  - customer discovery interviews ($\ge 5$ target domain users) transcribed, synthesized, and linked in `contracts/schemas/prd-spec.json`

### 3. 4-Pillar Agent ROI Framework (`AGENT-ROI-4PILLAR-LOCK`)
- **Mathematical Multi-Pillar Value Formulation**:
  - every autonomous agent or AI capability proposal must quantify ROI across the 4 canonical enterprise pillars:
    $$ROI_{\text{Agent}} = \frac{(\Delta \text{Labor Savings} + \Delta \text{Speed Value} + \Delta \text{Error Reduction} + \Delta \text{New Revenue}) - C_{\text{Agent Infra}}}{C_{\text{Agent Infra}}} \times 100\%$$
    1. **Labor Displacement/Augmentation**: reduction in human engineer or specialist hours ($H_{\text{saved}} \times \text{Hourly Rate}$)
    2. **Process Cycle Time Compression**: value generated from shipping hours/days earlier ($\Delta t_{\text{cycle}} \times \text{Opportunity Rate}$)
    3. **Error Remediation Savings**: reduction in production incidents and regression fix costs ($\Delta N_{\text{bugs}} \times \text{Avg Remediation Cost}$)
    4. **New Revenue Capacity**: incremental throughput enabled by 24/7 autonomous operations ($\Delta Q_{\text{throughput}} \times \text{Unit Margin}$)
  - proposals showing negative or unverified 4-pillar returns rejected prior to engineering allocation

### 4. Cost-per-Verified-Outcome ($CPVO$) & Token Unit Economics (`UNIT-ECONOMICS LOCK`)
- **Comprehensive Outcome Cost Accounting**:
  - product financial models must compute **Cost-per-Verified-Outcome** ($CPVO$) rather than naive raw token inference costs:
    $$CPVO = \frac{\sum (C_{\text{inference}} + C_{\text{eval}} + C_{\text{guardrails}} + C_{\text{HITL Review}})}{N_{\text{verified successful outcomes}}}$$
  - target $CPVO$ must maintain a minimum $60\%$ gross margin buffer against the customer willingness-to-pay baseline
- **PromQL Operational Telemetry**:
  ```promql
  # Real-time Cost-per-Verified-Outcome calculation
  sum(rate(ai_inference_cost_usd_total[1h]) + rate(human_review_cost_usd_total[1h])) 
  / (sum(rate(ai_verified_outcomes_total[1h])) > 0 or vector(1))
  ```

### 5. Blast Radius Classification & Mandatory HITL Governance (`HITL LOCK` / `BLAST-RADIUS-TIER-LOCK`)
- **4-Tier Autonomous Blast Radius Modeling**:
  | Tier | Classification | Blast Radius Impact | Operating Mode | Approval Requirement |
  | :--- | :--- | :--- | :--- | :--- |
  | **Tier 1** | Suggestion / Read-Only | Zero systemic risk | Autonomous draft | None (passive user review) |
  | **Tier 2** | Localized Workspace Mutation | Contained within user session | Autonomous execution | Reversible via single-click undo |
  | **Tier 3** | Shared System Mutation | Affects team configuration or DB schema | Pauses execution | Technical Lead explicit approval |
  | **Tier 4** | Irreversible / Financial | Production deployments, money movement | Blocked fail-closed | Cryptographic dual sign-off |
- **High-Stakes Domain Prohibition**:
  - fully autonomous execution in high-stakes domains (financial transactions, employment/hiring decisions, medical/legal advice) is strictly prohibited

### 6. Probabilistic Acceptance Criteria & Quality Envelopes (`PROBABILISTIC-ACCEPTANCE LOCK`)
- **Statistical Quality Targets & Hallucination Ceilings**:
  - generative AI features define probabilistic acceptance envelopes with statistical confidence intervals ($p < 0.05$):
    - precision $\ge 90\%$, recall $\ge 85\%$, and F1 score $\ge 0.87$ on benchmark evaluation corpora
    - maximum hallucination tolerance threshold locked at $< 1.0\%$ on verified ground truth
    - P95 latency envelopes and graceful degradation fallbacks specified for high-load windows
- **Continuous Evaluation Harness Configuration**:
  ```yaml
  # promptfoo evaluation configuration gate
  prompts: [prompts/system-v2.txt]
  providers: [anthropic:claude-3-5-sonnet-20241022]
  tests: evals/golden/feature-cases.yaml
  assert:
    - type: latency
      threshold: 3000
    - type: llm-rubric
      value: "Does not invent fake policy numbers or hallucinate non-existent features"
      threshold: 0.95
  ```

### 7. Golden Evaluation Datasets & Benchmark Curation (`EVAL-DATASET LOCK`)
- **Git-Versioned Benchmark Repositories**:
  - product managers must curate and version Golden Evaluation datasets ($\ge 100$ ground-truth test cases) covering edge cases, adversarial prompts, and diverse domain inputs
  - automated CI/CD eval gates block prompt or model migrations if benchmark score regresses by $> 2.0\%$

### 8. EU AI Act Article 50 & Transparency Compliance (`ARTICLE-50 TRANSPARENCY LOCK`)
- **Mandatory AI Disclosure Notices**:
  - conversational AI interfaces and synthetic content generators specify prominent user-facing disclosure notices complying with EU AI Act Article 50 (live August 2026)
  - machine-readable provenance metadata (`data-ai-generated="true"`) and C2PA Content Credentials cryptographic watermarking incorporated into PRD specifications

### 9. Agentic PRD Goal & Constraint Envelopes vs Static Task Lists
- **Goal-Oriented Specification Structure**:
  - PRDs for agentic features specify Goal & Constraint Envelopes rather than rigid procedural steps:
    ```json
    {
      "feature_id": "auto-reconciliation-v2",
      "target_objective": "Reconcile daily payment gateway settlements against internal ledger",
      "constraints": {
        "max_discrepancy_cents": 0,
        "max_runtime_minutes": 15,
        "blast_radius_tier": 3,
        "hitl_approval_required_above_cents": 50000
      },
      "evaluation_dataset_ref": "evals/golden/payment-reconciliation-v2.json"
    }
    ```

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **4-Pillar ROI Margin** | $ROI_{\text{Agent}} \ge 200\%$ | Financial modeling spreadsheet audit | All 4 pillars quantified with data |
| **CPVO Unit Margin** | Gross margin $\ge 60\%$ | Billing & token telemetry audit | $CPVO \le 0.40 \times \text{Price}$ |
| **Golden Eval Dataset** | Cases $\ge 100$, Git-versioned | `ls evals/golden/*.json \| wc -l` | $\ge 100$ verified ground-truth pairs |
| **Hallucination Ceiling**| Hallucination rate $< 1.0\%$ | `promptfoo eval -c eval-config.yaml` | Hallucination $< 1.0\%$ on golden set |
| **EU Article 50 Gate**  | C2PA & banner present | DOM inspector / `c2patool inspect` | Disclosure visible; metadata signed |
| **PRD Contract Schema** | Valid `prd-spec.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
| **HITL Tier Boundaries** | Blast radius $\le \text{Tier 2}$ | Security policy validator | Tier 3/4 require explicit approval |
| **Kill Criteria Defined**| Clear pivot metric set | PRD review rubric sign-off | Documented quantitative kill signal |
