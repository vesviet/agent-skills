# Prioritization Scoring, Kano Modeling & Kill-Early Protocol

> Authoritative reference guide for quantitative product prioritization, multi-criteria decision matrices, and objective roadmap governance.

---

## 1. Calibrated RICE Prioritization

The RICE framework enables objective ranking across disparate product initiatives.

$$\\text{RICE Score} = \\frac{\\text{Reach} \\times \\text{Impact} \\times \\text{Confidence}}{\\text{Effort}}$$

### Component Calibration Guidelines

#### 1. Reach (Number per Quarter)
- Count unique users or accounts who will experience the feature within a single 90-day cycle.
- Source exclusively from product analytics (e.g. Mixpanel, PostHog, Amplitude). Never guess.

#### 2. Impact (Discrete Tier Rubric)
| Tier | Score | Qualitative Benchmark |
|---|:---:|---|
| **Massive** | `3.0` | Fundamental step-change; directly alters core customer workflow or multiplies retention. |
| **High** | `2.0` | Significant improvement noticeable to majority of active users; measurable conversion lift. |
| **Medium** | `1.0` | Meaningful quality-of-life upgrade; noticeable to target sub-segment. |
| **Low** | `0.5` | Minor convenience feature or visual enhancement. |
| **Minimal** | `0.25`| Niche edge-case resolution affecting small percentage of interactions. |

#### 3. Confidence (Objective Data Grounding)
| Tier | Factor | Evidentiary Requirement |
|---|:---:|---|
| **High Data** | `1.0` (100%) | Validated via controlled A/B experiment, production prototype telemetry, or >50 customer interviews. |
| **Medium Data**| `0.8` (80%)  | Validated via qualitative user research (8-12 Mom Test interviews) + analytics correlation. |
| **Low / Speculative**| `0.5` (50%)| Early hypothesis supported by anecdotal feedback or competitor benchmarking. |
| **Pure Guess** | `< 0.2` (20%)| Unvalidated assumption. **Must be routed back to Discovery before scoring.** |

#### 4. Effort (Person-Months)
- Total sum of engineering, design, product, QA, and security review months.
- Minimum granularity: `0.5` person-months (approx 2 weeks for 1 engineer).

---

## 2. Kano Model Analysis

The Kano Model prevents teams from over-investing in table-stakes features while under-investing in competitive differentiators.

```
       Customer Satisfaction
               ▲
               │          [ Delighter / Attractive ]
               │                 /
               │                /  [ Performance / One-Dimensional ]
               │               /  /
 ──────────────┼──────────────/──/──────────────► Feature Execution
  Dysfunctional│             /  /               Functional
               │            /  /
               │           /  /  [ Must-Be / Basic Hygiene ]
               │          /  /  /
               │
               ▼ Dissatisfaction
```

### Classification Rubric
1. **Must-Be (M)**: Expected baselines (e.g. password reset, TLS encryption, data export). Fulfilling them creates zero extra delight, but omitting them destroys user trust.
2. **Performance (P)**: Linear satisfaction (e.g. query response latency, battery efficiency, search accuracy). The more and faster, the happier the customer.
3. **Attractive (A)**: Unanticipated value (e.g. magical AI summarization, automated error auto-healing). Creates distinct delight and viral organic advocacy.
4. **Indifferent (I)**: Users do not care whether it exists. Must be purged from backlogs.
5. **Reverse (R)**: Causes dissatisfaction when added (e.g. intrusive modals, noisy notification popups).

---

## 3. Weighted Scoring Decision Matrix (Build vs. Buy / Vendor Selection)

Use Multi-Criteria Decision Analysis (MCDA) when evaluating architectural choices or vendor contracts.

```markdown
| Evaluation Criterion | Weight (w) | Option A: In-House Build | Option B: Vendor SaaS | Option C: Open-Source Fork |
|---|:---:|:---:|:---:|:---:|
| Strategic Alignment & IP Control | 25% | 5 (1.25) | 2 (0.50) | 4 (1.00) |
| Speed to Market (Time to First Value) | 25% | 2 (0.50) | 5 (1.25) | 3 (0.75) |
| Total Cost of Ownership (3-Year TCO) | 20% | 2 (0.40) | 3 (0.60) | 4 (0.80) |
| Security, Privacy & EU AI Act Compliance | 20% | 5 (1.00) | 3 (0.60) | 4 (0.80) |
| Maintenance & Operational Overhead | 10% | 2 (0.20) | 5 (0.50) | 2 (0.20) |
| **Weighted Total** | **100%** | **3.35** | **3.45** | **3.55** |
```

### Sensitivity Analysis Stress-Test
- Identify the criterion with the highest weight.
- Adjust weight by +20% and -20% while re-normalizing other weights.
- If the winning option flips under minor perturbations, declare the decision as "sensitive" and conduct a targeted proof-of-concept (PoC).

---

## 4. The Kill-Early Protocol

Sunk-cost fallacy is the leading cause of failed product roadmaps. The Kill-Early Protocol enforces rational detachment.

### Protocol Rules
1. **Pre-Committed Kill Thresholds**: Every prioritized initiative must specify at least two measurable failure gates before engineering begins:
   - *Adoption Threshold*: Minimum weekly active users (WAU) within 30 days post-launch.
   - *Outcome Threshold*: Minimum conversion or retention lift after 1,000 completed sessions.
2. **Review Cadence**: Mandatory checkpoint at Day 14 and Day 45 post-launch.
3. **The 3 Legitimate Post-Review Actions**:
   - **Scale**: Metrics met or exceeded; allocate capacity to optimize and institutionalize.
   - **Pivot**: Hypothesis partially confirmed, but friction identified; allocate strictly 1 sprint for targeted refinement.
   - **Kill**: Metrics failed failure thresholds; shut down feature, archive code, document key learnings, and return capacity to roadmap.
