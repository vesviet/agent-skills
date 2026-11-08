# NIST AI RMF 1.0 & EU AI Act Risk Taxonomy (2026)

## 1. Overview & Dual Governance Framework

Governing production AI/ML systems requires harmonizing the NIST AI Risk Management Framework (NIST AI RMF 1.0 / NIST AI 600-1) with statutory mandates under the EU AI Act (Regulation EU 2024/1689).

```
┌────────────────────────────────────────────────────────┐
│                   NIST AI RMF 1.0                      │
│   GOVERN ──────► MAP ──────► MEASURE ──────► MANAGE    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   EU AI ACT TIERS                      │
│  Unacceptable ──► High-Risk ──► Limited ──► Minimal    │
│  (Prohibited)     (Conformity)  (Art. 50)   (Codes)    │
└────────────────────────────────────────────────────────┘
```

## 2. NIST AI 600-1 Generative AI Profile (12 Risk Dimensions)

1. **Confabulation / Hallucination**: Ungrounded, fabricated factual assertions. Measurable via hallucination rate benchmarks and factuality metrics.
2. **CBRN Information Hazards**: Proliferation of chemical, biological, radiological, or nuclear weapons blueprints.
3. **Cyberattacks / Malicious Code**: Autonomous vulnerability generation, automated exploitation payloads, and unverified code execution.
4. **Data Privacy Violations**: PII extraction via model inversion, membership inference, and training data memorization.
5. **Environmental Impacts**: Carbon emissions and energy footprint during training and inference lifecycle.
6. **Harmful Bias & Homogenization**: Algorithmic discrimination, stereotyping, and lack of representation.
7. **Human-AI Configuration Failures**: Overreliance (automation bias), underreliance, and cognitive degradation.
8. **Information Integrity**: Machine-generated synthetic disinformation, deepfakes, and societal manipulation.
9. **Intellectual Property Infringement**: Copyrighted training corpus reproduction and patent infringement.
10. **Obscene / Harmful Content**: Hate speech, harassment, self-harm, and CSAM generation.
11. **Value Chain & Component Risks**: Vulnerabilities in upstream foundational models, tokenizer poison, and model supply chain drift.
12. **Societal & Macro-Level Harms**: Labor market disruption, critical infrastructure dependencies, and democratic system degradation.

## 3. EU AI Act Statutory Classifications & Deadlines

- **Prohibited Systems (Art. 5)**: Real-time biometric identification in public spaces, social scoring, behavioral manipulation causing harm.
- **High-Risk Systems (Annex III)**: Autonomous hiring/recruitment tools, credit scoring algorithms, essential public benefit allocation, autonomous critical infrastructure.
  - *Obligations*: Formal Fundamental Rights Impact Assessment (FRIA), continuous quality management system (QMS), automated audit logging for 6+ months, mandatory human-in-the-loop (HITL) kill switches.
  - *Deadlines*: Standalone high-risk systems: 2 December 2027; products embedded under Union harmonization legislation: 2 August 2028.
- **Limited-Risk Systems (Art. 50)**: User-facing chatbots, synthetic audio/video, AI-generated text.
  - *Obligations (Enforceable from August 2026)*: Conspicuous machine-readable labeling and watermarking (C2PA standard).

## 4. Agentic Autonomy & Reversibility Analysis

For multi-agent systems, risk classification must evaluate action irreversibility:
- **Reversible Actions**: Read operations, draft generations, internal cache mutations. Supervised autonomy permitted.
- **Irreversible Actions**: Financial transactions, permanent database mutations, external email/notification transmissions. Mandatory HITL confirmation gate before execution.
