---
name: ai-risk-assessment
description: Assess AI/ML system risks using NIST AI RMF 1.0 (Govern/Map/Measure/Manage) and NIST AI 600-1 GenAI Profile (12 risk categories), classify EU AI Act risk tiers, and produce an AI risk register covering hallucination thresholds, model degradation signals, bias exposure, and compliance drift. Use when onboarding a new AI feature, scoping an AI system for delivery, or conducting a periodic AI governance audit.
---

# AI Risk Assessment

Use this skill when a product, feature, or system involves AI/ML components that require structured risk governance before delivery commitment or continued operation. Applies NIST AI RMF 1.0 and the NIST AI 600-1 GenAI Profile alongside EU AI Act risk classification.

## Core Rules

- **Not a checklist**: NIST AI RMF is a "thinking structure" — apply it to inform decisions, not to fill boxes mechanically.
- **Govern before Map**: establish accountability and policy boundaries before inventorying risks.
- **Classification first**: determine EU AI Act risk tier before writing any acceptance criteria; high-risk classification changes the delivery contract.
- **GenAI-specific**: for LLM/generative AI systems, apply all 12 NIST AI 600-1 risk categories — standard software risk assessments are insufficient.
- **Living register**: the AI risk register is a delivery artifact maintained throughout the system's lifecycle, not a one-time document.
- **HITL is mandatory for high-risk**: Human-in-the-Loop is not a UX preference — it is a regulatory requirement for EU AI Act high-risk systems.

### 2025-2026: Agentic AI Risk Extension

For agentic AI systems (autonomous agents, multi-agent workflows), extend the standard assessment with:
- **Autonomy tier**: declare the level of autonomous decision-making (supervised / semi-autonomous / fully autonomous)
- **Action reversibility audit**: classify every agent action as reversible or irreversible; irreversible actions require explicit human approval gates
- **OWASP ASI alignment**: map identified risks to OWASP ASI01–ASI10 threat categories
- **Cascading failure analysis**: for multi-agent systems, trace how a single agent failure propagates

## Suggested Process

Apply the NIST AI RMF 1.0 four functions in sequence:

### 1. Govern
Establish organizational accountability for AI risk:

```yaml
governance:
  owner: "[PM / Tech Lead / BA who is accountable]"
  policy_profile: "[acceptable-use / restricted / prohibited]"
  human_oversight_mechanism: "[HITL gates / monitoring / kill-switch]"
  review_cadence: "[monthly / quarterly / per-release]"
  escalation_path: "[who decides on risk acceptance]"
```

### 2. Map
Identify and contextualize AI risks:

```yaml
system_context:
  intended_use: "[primary task the AI is performing]"
  users_and_stakeholders: "[who is affected]"
  data_sources: "[training, validation, retrieval sources]"
  deployment_environment: "[edge / cloud / on-prem / hybrid]"
  dependency_chain: "[models, APIs, third-party services relied upon]"
```

### 3. Measure (NIST AI 600-1 — 12 GenAI Risk Categories)

Assess each category for relevance and severity:

| # | Risk Category | In Scope? | Severity | Mitigation |
|---|---|---|---|---|
| 1 | **Confabulation / Hallucination** | [yes/no] | [H/M/L] | |
| 2 | **CBRN Information Hazards** | [yes/no] | [H/M/L] | |
| 3 | **Cyberattacks / Malicious Code** | [yes/no] | [H/M/L] | |
| 4 | **Data Privacy Violations** | [yes/no] | [H/M/L] | |
| 5 | **Environmental Impacts** | [yes/no] | [H/M/L] | |
| 6 | **Harmful Bias & Homogenization** | [yes/no] | [H/M/L] | |
| 7 | **Human-AI Configuration Failures** | [yes/no] | [H/M/L] | |
| 8 | **Information Integrity (Disinformation)** | [yes/no] | [H/M/L] | |
| 9 | **Intellectual Property Infringement** | [yes/no] | [H/M/L] | |
| 10 | **Obscene / Harmful Content** | [yes/no] | [H/M/L] | |
| 11 | **Value Chain & Component Risks** | [yes/no] | [H/M/L] | |
| 12 | **Societal \& Macro-Level Harms** | [yes/no] | [H/M/L] | |

### 4. Manage
Prioritize and mitigate identified risks:

```yaml
risk_treatments:
  - risk: "Hallucination in user-facing output"
    treatment: "Output validation layer + human review for high-stakes decisions"
    owner: "Backend Developer + QA Engineer"
    deadline: "[sprint or date]"
    residual_risk: "[acceptable / requires escalation]"
```

## EU AI Act Risk Classification

Determine risk tier before delivery commitment:

| Tier | Examples | Compliance Obligations |
|---|---|---|
| **Unacceptable** | Social scoring, real-time biometric surveillance | **Prohibited** — do not build |
| **High-risk** | CV screening, credit scoring, safety-critical systems, autonomous agents in regulated domains | Conformity assessment, audit logging, HITL, bias assessment, QMS |
| **Limited-risk** | Chatbots, deepfakes with disclosure | Transparency obligations only |
| **Minimal-risk** | Spam filters, AI-powered games | Voluntary code of conduct |

```yaml
eu_ai_act:
  risk_tier: "[high-risk / limited-risk / minimal-risk / not-applicable]"
  classification_rationale: "[why this tier was assigned]"
  conformity_assessment_required: "[yes / no]"
  audit_logging_required: "[yes / no]"
  hitl_required: "[yes / no]"
  bias_assessment_required: "[yes / no]"
  target_compliance_date: "2027-12-02"  # standalone high-risk systems deadline
```

> ⚠️ **Deadline note**: EU AI Act high-risk system enforcement — standalone: 2 December 2027; embedded in products: 2 August 2028 (AI Omnibus update). Use this date in planning, not "2026."

## AI Risk Register Template

```yaml
ai_risk_register:
  system_id: "[slug or ticket ref]"
  assessment_date: "[YYYY-MM-DD]"
  assessor: "[role or person]"
  review_due: "[YYYY-MM-DD]"

  governance:
    owner: ""
    policy_profile: ""
    human_oversight_mechanism: ""

  eu_ai_act_tier: ""

  nist_600_1_risks:
    hallucination_threshold: "[% acceptable error rate before intervention]"
    model_degradation_signal: "[metric that triggers model review]"
    bias_exposure: "[groups or use cases with bias risk]"
    data_privacy_classification: "[PII sensitivity level]"
    ip_risk: "[training data provenance status]"

  owasp_asi_alignment:
    - asi_id: "ASI01"
      applicable: "[yes/no]"
      mitigation: ""

  compliance_drift_indicators:
    - signal: "[what to monitor]"
      threshold: "[when to escalate]"
      responsible: "[who monitors]"

  residual_risks:
    - risk: ""
      accepted_by: ""
      accepted_date: ""
      review_date: ""
```

## Checklist

- [ ] Governance owner assigned and accountability documented
- [ ] EU AI Act risk tier classified before any acceptance criteria written
- [ ] All 12 NIST AI 600-1 risk categories assessed for relevance and severity
- [ ] OWASP ASI01–ASI10 alignment completed for agentic systems
- [ ] Autonomy tier declared for agentic components (supervised / semi / fully autonomous)
- [ ] Action reversibility audit completed (irreversible actions identified)
- [ ] Hallucination threshold defined and measurable
- [ ] Model degradation signal defined and monitored
- [ ] HITL mechanism documented (if high-risk tier)
- [ ] AI risk register produced and stored alongside feature ticket
- [ ] Review cadence set for ongoing monitoring

## Output Format

Produce `contracts/schemas/ai-risk-register.json` (or YAML equivalent) when formal handoff is required. Include:
- `eu_ai_act_tier` field
- `nist_600_1_risks` section
- `owasp_asi_alignment` mapping
- `residual_risks` with acceptance sign-offs

## Related Skills

- **analyze-business-requirements**: BA is the first to apply EU AI Act tier classification in `feature-ticket.json`
- **security-audit**: full security review that incorporates AI risk register findings
- **conduct-research**: domain research on AI risk context, regulations, and comparable systems
- **agent-tool-orchestration**: agentic action inventory required by this assessment
