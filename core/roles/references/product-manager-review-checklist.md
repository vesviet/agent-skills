## Product Manager Review Checklist

This reference checklist provides operational product discovery, outcome governance, AI feature specification, and unit economics criteria for product management to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across North Star Metric alignment, hypothesis-driven validation, Human-in-the-Loop (HITL) governance, probabilistic acceptance criteria, token unit economics, golden eval datasets, EU AI Act Article 50 compliance, and agentic drift controls.

### 1. Outcome-Driven Strategy & North Star Metric Alignment (`VANITY-METRIC LOCK`)
- **Measurable Value Delivery**:
  - every product brief traces directly to a measurable impact on the North Star Metric (NSM) or specific user journey stage (Acquisition $\rightarrow$ Activation $\rightarrow$ Retention $\rightarrow$ Expansion)
  - vanity metrics ("total AI query volume", "number of features shipped", unverified "time saved") rejected in favor of behavioral outcomes and retention impact
- **Problem-First Framing**:
  - briefs define the fundamental user problem and underlying business opportunity before specifying solution features; non-goals explicitly documented

### 2. Hypothesis-Driven Discovery & Kill-Early Discipline (`HYPOTHESIS LOCK` / `KILL-EARLY LOCK`)
- **Structured Testable Hypotheses**:
  - significant product initiatives framed using the canonical hypothesis template:
    > *"Given [validated insight], changing [X] will result in [measurable outcome] for [user segment]."*
  - validation type selected and executed before committing engineering capacity: Problem Validation, Solution Validation, Demand Validation, or Pricing Validation
- **Kill-Early Protocol**:
  - explicit kill criteria and negative signal thresholds defined prior to discovery spikes; negative validation signals trigger immediate pivot or retirement, preventing sunk-cost traps

### 3. AI Feature Scoping & Mandatory HITL Governance (`AI-SCOPE LOCK` / `HITL LOCK`)
- **Autonomous Action Boundaries**:
  - AI and agentic capabilities define explicit operating boundaries, allowed tool sets, and maximum autonomy levels
  - fallback behaviors specified for instances where model confidence falls below defined thresholds
- **Mandatory Human-in-the-Loop (HITL) Gates**:
  - high-stakes operations (financial transactions, employment/hiring decisions, medical/legal advice, user permission changes, production deployments) mandate explicit human confirmation interfaces; fully autonomous execution in high-stakes domains is prohibited

### 4. Probabilistic Acceptance Criteria & Quality Envelopes (`PROBABILISTIC-ACCEPTANCE LOCK`)
- **Statistical Tolerance Modeling**:
  - generative AI features define probabilistic acceptance criteria instead of naive binary pass/fail checks:
    - precision, recall, and F1 score targets on benchmark evaluation sets
    - maximum hallucination tolerance threshold (e.g. $\le 1.5\%$ on verified ground truth)
    - P95 latency envelopes and latency degradation fallbacks

### 5. Total Cost of Ownership (TCO) & Token Unit Economics (`UNIT-ECONOMICS LOCK`)
- **Cost-Per-Verified-Outcome Modeling**:
  - financial models evaluate the complete Total Cost of Ownership for AI workflows:
    $$\text{TCO} = \text{Inference Tokens} + \text{Agent Orchestration} + \text{Eval Gating} + \text{Human Review Dwell Time}$$
  - target cost-per-successful-transaction calculated and compared against traditional manual or deterministic API baselines to ensure positive unit margin

### 6. Golden Evaluation Datasets & Quality Baselines (`EVAL-DATASET LOCK`)
- **Versioned Benchmark Corpora**:
  - AI product requirements mandate the creation and maintenance of a versioned Golden Evaluation dataset reflecting real-world edge cases and adversarial queries
  - automated benchmark regression thresholds established; feature promotions blocked if evaluation pass rates drop below baseline

### 7. EU AI Act Article 50 Transparency & Regulatory Compliance (`ARTICLE-50 TRANSPARENCY LOCK`)
- **Mandatory AI Disclosure Notices**:
  - conversational AI interfaces and synthetic content generators specify prominent user-facing disclosure notices (EU AI Act Article 50) live as of August 2026
  - machine-readable provenance metadata (`data-ai-generated="true"`, C2PA digital watermarking) incorporated into functional requirements
- **Risk Tier Classification**:
  - feature classification documented against EU AI Act risk tiers (Prohibited, High-Risk Annex III, Specific Transparency Risk, Minimal Risk)

### 8. Agentic Drift Prevention & Autonomy Fencing (`AGENTIC-DRIFT LOCK`)
- **Failsafe Autonomy Boundaries**:
  - autonomous multi-step agents operate within bounded task graphs; runaway recursive loops prevented via maximum step counts and token caps
  - user override, pause, and undo affordances designed into all agentic workflows

### 9. PRD & Contract Specification Standards (`PRD-CONTRACT LOCK`)
- **Machine-Parsable Contract Handoff**:
  - product deliverables produce valid, schema-compliant `contracts/schemas/feature-ticket.json` and `contracts/schemas/prd-spec.json`
  - acceptance criteria define verifiable behavior, invariant preservation, and explicit negative / edge test scenarios
- **Cross-Functional Sign-Off Protocol**:
  - Technical Lead, UX Designer, and Business Analyst review gates completed before developer scheduling

### 10. Operational Failure Modes & Escalation Protocols
- **Degraded Experience Fallbacks**:
  - circuit breaker trip behavior specified when upstream model inference fails or exceeds P95 latency ceilings
  - deterministic static fallbacks and clear error states presented without exposing raw stack traces or internal model system prompts
