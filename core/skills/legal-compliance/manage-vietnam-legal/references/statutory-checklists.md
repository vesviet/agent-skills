# Vietnam Statutory Checklists & Contract Vetting Rubrics

This reference document provides detailed statutory checklists, contract vetting rubrics, PDPL No. 91/2025/QH15 + Decree 356/2025/ND-CP audit procedures, and Law on Artificial Intelligence No. 134/2025/QH15 compliance rubrics supporting the `manage-vietnam-legal` skill.

---

## 1. Commercial Contract Vetting Rubric (Dual-Track Regime)

### 1.1 Commercial Law 2005 vs Civil Code 2015 Classification
In Vietnamese jurisprudence, contract characterization determines permissible remedy structures:

| Criterion | Commercial Contracts (Commercial Law 2005) | Civil Contracts (Civil Code 2015) |
|---|---|---|
| **Governing Statute** | Law No. 36/2005/QH11 (*lex specialis*) | Law No. 91/2015/QH13 (*lex generalis*) |
| **Applicability** | At least one party is a profit-seeking merchant | Non-commercial or consumer transactions |
| **Penalty Cap (Phạt vi phạm)** | **Strictly capped at 8%** of the value of the breached contractual obligation portion (Article 301) | **Freely negotiable** without statutory percentage cap (Article 418) |
| **Damages (Bồi thường thiệt hại)** | Actual, direct loss plus direct profits foregone (Article 302); requires proof of actual damage | Full and timely compensation for actual loss (Article 419) |
| **Cumulative Remedies** | Penalty + Damages permitted only if explicitly agreed in contract (Article 307) | Permitted unless agreed otherwise |
| **Interest on Late Payment** | Average overdue loan interest rate on the market (Article 306) | 50% above basic rate or capped at 20%/year (Article 468) |

### 1.2 Mandatory Tripartite Remedy Architecture
To avoid invalidation of penalty clauses under Article 301 Commercial Law 2005, draft remedies using tripartite structuring:
1. **Contractual Penalty (Phạt vi phạm)**: Capped at exactly 8% of the breached milestone/delivery portion.
2. **Actual Damages (Bồi thường thiệt hại)**: Fully recoverable upon proof of direct, actual financial loss.
3. **Security Deposit Forfeiture (Mất tiền đặt cọc)**: Structured under Article 328 Civil Code 2015 as a security measure rather than a contractual penalty.

---

## 2. PDPL No. 91/2025/QH15 + Decree 356/2025/ND-CP Personal Data Protection Compliance Checklist

### 2.1 Core Invariants under PDPL 2025 & Decree 356
- **Legislative Transition**: Effective **January 1, 2026**, the Law on Personal Data Protection No. 91/2025/QH15 and Decree No. 356/2025/ND-CP supersede Decree 13/2023/ND-CP as Vietnam's governing personal data protection regime.
- **Universal Data Scope**: Covers personal data processing across both digital environments and non-digital formats (physical filing systems, paper records, offline biometric capture, audiovisual recordings).
- **Verifiable Consent Standard (Article 14 PDPL / Decree 356)**:
  - Consent is legally valid **only** if recorded through an immutable, auditable log capturing:
    1. *Time*: Exact ISO timestamp when consent was granted or revoked.
    2. *Content*: Explicit, granular disclosure of data types and processing purposes.
    3. *Act of Consent*: Clear affirmative opt-in action by the data subject.
  - Pre-ticked checkboxes, default consent, implied consent, and bundled terms (tying service provision to non-essential data processing) are strictly void.
- **Certificate of Business Eligibility (Article 28 PDPL / Decree 356)**:
  - Providing personal data processing services is classified as a conditional business investment sector.
  - Third-party processors, analytics providers, and cloud data intermediaries must obtain a **Certificate of Business Eligibility for Personal Data Processing Services** issued by the Ministry of Public Security (MPS - Department A05) prior to offering services.
- **Data Subject Rights & 2-Working-Day SLA (Article 10 PDPL / Decree 356)**:
  - Guarantees fundamental rights: right to know, consent, access, rectify, delete, restrict processing, data portability, object, and withdraw consent.
  - Data controllers and processors must acknowledge receipt and initiate substantive response to data subject rights requests within **2 working days**.
- **Cross-Border Personal Data Transfer (Article 32 PDPL / Decree 356)**:
  - Outbound data transfers (including hosting Vietnamese citizens' data on overseas cloud infrastructure) mandate:
    1. Completing a Cross-Border Transfer Impact Assessment dossier.
    2. Enforceable data transfer agreement binding the overseas recipient to standards equal to or exceeding PDPL 2025.
    3. Dossier submission to Department A05 MPS and maintenance of annual compliance audit trails.
- **Revenue-Based Penalties & Sanctions**:
  - Serious violations (such as unlawful cross-border transfer, systemic unauthorized commercialization of personal data, or gross data leaks) incur administrative fines of **up to 5% of the preceding financial year's total enterprise revenue**.
  - In addition, statutory sanctions include suspension of data processing operations, revocation of the Certificate of Business Eligibility, and referral for criminal prosecution.
- **Backward Compatibility & Legacy Contracts**:
  - Contracts and Data Processing Agreements (DPAs) executed under Decree 13/2023/ND-CP prior to January 1, 2026 remain legally governed by the Decree 13 regime until their expiration, renewal, or material renegotiation, at which point full transition to PDPL 2025 is mandatory.

### 2.2 PDPL 2025 / Decree 356 Audit Matrix

| Step | Statutory Focus | Verification Requirement | SLA / Statutory Penalty | Status |
|---|---|---|---|---|
| 1 | Article 14 | Verifiable consent log: immutable capture of timestamp, specific content, and affirmative act; zero bundled or pre-ticked consent | Void consent; administrative fines | Mandatory |
| 2 | Article 28 | Certificate of Business Eligibility from MPS (A05) for entities providing data processing services | Immediate operational suspension + fines | Mandatory (Service Providers) |
| 3 | Article 20 | Sensitive personal data safeguards (biometrics, health, financial, location, political/religious beliefs) requiring heightened explicit consent | Enhanced technical controls + fines | Enhanced |
| 4 | Article 10 | Data subject request fulfillment pipeline (access, correction, deletion, withdrawal, objection) | **2 working days** acknowledgment SLA | Mandatory |
| 5 | Article 25 | Internal Personal Data Protection Impact Assessment (DPIA) dossier maintained and accessible for MPS inspection | Dossier available within 60 days of processing | Mandatory |
| 6 | Article 32 | Outbound cross-border data transfer impact assessment, recipient binding agreement, and A05 MPS filing | **Fines up to 5% of prior year's revenue** | Mandatory |
| 7 | Article 24 | Personal data breach incident response: containment, evidence preservation, and mandatory notification to A05 MPS | **72 hours** from incident detection | Contingent |
| 8 | Transition | Legacy contract audit: flag contracts referencing Decree 13/2023/ND-CP for PDPL gap analysis upon renewal | Mandatory upgrade upon renewal/amendment | Transition |

### 2.3 Penalty Comparison Schedule: Decree 13 vs PDPL 2025 + Decree 356

| Violation Category | Decree 13/2023/ND-CP (Legacy Regime) | PDPL No. 91/2025/QH15 + Decree 356 (Current Regime) |
|---|---|---|
| **Cross-Border Transfer Default** | Fixed administrative fine (VND 80-100 million) under Decree 14/2022/ND-CP | **Revenue-based fine up to 5% of preceding financial year's total revenue** |
| **Unlicensed Processing Services** | General corporate licensing penalties | **Mandatory operation suspension** + business eligibility certificate denial |
| **Defective / Bundled Consent** | Administrative warning or nominal fine; consent invalidation | Consent deemed legally void; administrative fines + mandatory data deletion |
| **Data Subject Request Delay** | Vague statutory timelines without explicit SLA penalties | Strict **2-working-day** response initiation SLA + non-compliance fines |
| **Systemic Data Breach / Leak** | Fixed fines capped per occurrence under general cybersecurity decrees | **Up to 5% enterprise revenue fine**, executive liability, criminal referral |

---

## 3. Corporate Governance & Capital Controls (Law on Enterprises 2020)

### 3.1 90-Day Capital Contribution Deadline
- **Statutory Deadlines**: Articles 47.2 (LLC) and 113.1 (JSC) mandate full contribution of subscribed charter capital within **90 days** from the issuance date of the Enterprise Registration Certificate (ERC).
- **Default Consequence**: If unfulfilled, the enterprise must register a capital reduction within **30 days** following the 90-day window. Shareholders failing to contribute remain jointly liable up to the unfulfilled capital subscription.

### 3.2 Related-Party Transactions (RPT) Screening (Article 167)
- **Board Approval**: Contracts between company and related parties (founders, major shareholders, executives) valuing `< 35%` of total asset value shown in latest financial statements.
- **Shareholder Approval**: Contracts valuing `>= 35%` of total asset value or transactions resulting in transaction value exceeding threshold.
- **Mandatory Recusal**: Interested board members and shareholders have no voting rights on the approval resolution.

---

## 4. Labor & Intellectual Property Checklists

### 4.1 Non-Disclosure (NDA) & Non-Compete (NCA) under Labor Code 2019
- **Article 21.2 Labor Code 2019**: Permits confidentiality and proprietary business information protection agreements.
- **NCA Enforceability**: Post-termination non-compete agreements are strictly scrutinized. Must include reasonable geographic scope, reasonable duration ($\le 12$ months), and financial compensation during the restricted period to withstand judicial challenge.

### 4.2 Software Copyright & IP Assignment (IP Law as amended 2022)
- Software code, architectures, and algorithms developed by employees or contractors belong to the employer only if explicitly created under work-for-hire or written assignment contracts (Articles 20, 21, 39 IP Law).
- Moral rights (right to name work, paternity right) cannot be transferred under Vietnamese law; only economic rights and certain publishing rights are assignable.

---

## 5. AI Law No. 134/2025/QH15 Compliance Checklist

### 5.1 Risk-Tier Classification Matrix
Under the Law on Artificial Intelligence No. 134/2025/QH15 (effective **March 1, 2026**), all AI systems, agentic workflows, and automated decision engines operating or deployed in Vietnam must be classified into a 3-tier risk framework:

| Risk Tier | Definition & Scope Criteria | System Examples | Statutory Obligations (Law 134/2025) | Non-Compliance Consequences |
|---|---|---|---|---|
| **Low-Risk AI** | Systems with minimal or negligible impact on human safety, fundamental rights, legal rights, or critical socio-economic systems. | Internal code auto-complete, spell-checkers, non-critical translation, UI layout optimizers, internal spam filters. | Adherence to national AI ethical principles (Decision 1290/QD-BKHCN); voluntary codes of conduct; general transparency. | Advisory guidance, voluntary remedial notices. |
| **Medium-Risk AI** | Systems interacting directly with natural persons, generating synthetic media / conversational output, or informing decisions affecting individuals without binding legal effect. | Customer-service chatbots, automated marketing copywriters, synthetic avatar generators, recommendation engines influencing consumer choice. | 1. Mandatory user transparency disclosures (notifying users they interact with an AI).<br>2. Mandatory labeling of AI-generated content (watermarking / metadata tagging).<br>3. Regular compliance self-assessments and reporting to MoST.<br>4. Sample audit logging and hallucination/bias mitigations. | Administrative fines up to VND 500 million; mandatory labeling rectification orders; temporary service suspension. |
| **High-Risk AI** | Systems operating in critical infrastructure, healthcare diagnostics, autonomous vehicles, biometric identification, credit scoring, recruitment/employment filtering, educational grading, law enforcement, or binding automated legal decisions. | Credit assessment engines, automated CV screening/ranking bots, biometric access systems, clinical diagnostic AI, automated loan/insurance underwriting. | 1. Mandatory pre-deployment conformity assessment.<br>2. Mandatory registration in the National AI Database portal.<br>3. Continuous operational monitoring and telemetry logging.<br>4. Human-in-the-loop (HITL) kill-switch controls.<br>5. Local presence / authorized legal representative in Vietnam for foreign providers. | Administrative fines up to VND 2 billion; **revenue-based fines for systemic violations**; product recall; permanent commercial ban in Vietnam. |

### 5.2 High-Risk AI Obligations Checklist
Any system classified as High-Risk AI under Law 134/2025/QH15 must satisfy five mandatory statutory pillars prior to commercial deployment:

- [ ] **1. Conformity Assessment (Article 18)**: Complete formal conformity assessment via an accredited testing organization or comprehensive internal conformity dossier proving:
  - Technical robustness, cybersecurity resilience, and fault tolerance.
  - Data governance, representativeness of training data, and algorithmic bias mitigations.
  - Predictability, explainability, and error-rate boundaries.
- [ ] **2. National AI Database Portal Registration (Article 22)**: Register the AI system on the National AI Database managed by the Ministry of Science and Technology (MoST):
  - Model architecture specifications, version register, and intended operational scope.
  - Contact details of the provider's registered legal representative in Vietnam.
  - Conformity assessment certificate and summary risk assessment report.
- [ ] **3. Continuous Operational Monitoring & Logging (Article 20)**:
  - Maintain automated telemetry logging recording model inputs, outputs, runtime performance, and system decisions.
  - Minimum audit log retention period of **24 months** stored in compliance with Vietnam data localization rules.
  - Establish automated drift detection alerting engineering and legal teams of out-of-distribution behaviors.
- [ ] **4. Human-in-the-Loop (HITL) & Override Controls (Article 21)**:
  - Design human override capabilities allowing authorized operators to halt, override, or roll back automated decisions.
  - Enforce mandatory human approval gates for irreversible actions (financial transfers, employment terminations, medical recommendations).
- [ ] **5. Local Presence for Foreign AI Providers (Article 26)**:
  - Foreign entities providing High-Risk AI services to users in Vietnam must establish a subsidiary, branch office, or designate an authorized Vietnamese legal representative with formal Power of Attorney to bear regulatory and legal accountability.

### 5.3 Medium-Risk AI Obligations Checklist
Systems classified as Medium-Risk AI must establish active transparency and auditing pipelines:

- [ ] **1. User Transparency Disclosure (Article 15)**:
  - Clearly and conspicuously inform natural persons at the initiation of interaction that they are communicating with an AI agent or synthetic conversational system.
  - Exception: Situations where the AI interaction is obvious from the context to an ordinary reasonable person.
- [ ] **2. AI-Generated Content Labeling (Article 16)**:
  - Embed detectable, tamper-resistant watermarks or machine-readable metadata (`data-ai-generated="true"`) in synthetic audio, visual, video, or deepfake content.
  - Display conspicuous visual badges on text or media generated or materially altered by AI.
- [ ] **3. Regular Compliance Reporting (Article 17)**:
  - Submit annual AI governance and compliance self-assessment reports to MoST detailing user safety metrics, incident logs, and vulnerability remediations.
- [ ] **4. Sample Auditing & Algorithmic Guardrails**:
  - Implement periodic automated and manual sampling of input prompts and outputs to verify adherence to Vietnamese cultural, ethical, and legal standards.
  - Maintain active prompt injection guards and content filtering against toxic, fraudulent, or unlawful generations.

### 5.4 Incident Reporting Timeline Table (Law 134/2025/QH15)
When an AI system malfunctions, causes harm, or suffers an uncontrolled operational event, the provider and deploying enterprise must follow statutory reporting timelines:

| Incident Classification | Triggering Criteria | Mandatory Statutory Deadline | Competent Regulatory Authority | Required Incident Dossier Content |
|---|---|---|---|---|
| **Urgent / Uncontrolled Incident** | • Imminent or actual threat to human life or bodily integrity.<br>• Major disruption of critical national infrastructure.<br>• Uncontrolled autonomous propagation or systemic model escape.<br>• Massive biometric or sensitive personal data breach. | **Within 72 hours** of incident detection | **Ministry of Science and Technology (MoST)**<br>*(and MPS - Department A05 if cybersecurity/data breach)* | 1. Incident identification and initial severity rating.<br>2. Root-cause hypothesis and affected model versions.<br>3. Immediate emergency containment measures taken (kill-switch activation, rollback).<br>4. Estimated user and societal impact assessment. |
| **Serious Incident** | • Material financial loss exceeding statutory thresholds.<br>• Systematic discriminatory bias or rights infringement affecting large user cohorts.<br>• Significant data corruption or unauthorized automated decisions.<br>• Sustained availability disruption of essential services. | **Within 5 working days** of incident identification | **Ministry of Science and Technology (MoST)** | 1. Comprehensive forensic root-cause analysis.<br>2. Impacted population census and remediation plan.<br>3. Model retraining, weight adjustment, or guardrail updates.<br>4. Measures implemented to prevent reoccurrence. |
| **Standard Operational Anomaly** | • Isolated prompt injection attempt successfully neutralized by guardrails.<br>• Minor transient drift within acceptable tolerances.<br>• Non-systemic user complaints resolved within standard SLA. | Record in internal audit logs; report in **Annual AI Report** | Internal Compliance Record / Annual MoST Filing | 1. Internal log entry with timestamp and trace ID.<br>2. Quarterly review by AI safety committee.<br>3. Telemetry trend monitoring. |

### 5.5 Grace Period Compliance Tracker

To facilitate transition and minimize business disruption, Law 134/2025/QH15 establishes phased grace periods from its effective date of **March 1, 2026**:

| Sector Category | Sector Scope | Statutory Grace Period | Final Mandatory Compliance Deadline | Phased Implementation Milestones |
|---|---|---|---|---|
| **Sensitive Sectors** | • Healthcare & Medical Diagnostics<br>• Education & Academic Evaluation<br>• Banking, Credit & Financial Services | **18 months** from effective date | **September 1, 2027** | • **Months 1–6 (Mar–Aug 2026)**: Complete AI inventory, risk-tier mapping, and gap analysis.<br>• **Months 7–12 (Sep 2026–Feb 2027)**: Complete conformity assessments, bias audits, and technical remediation.<br>• **Months 13–18 (Mar–Aug 2027)**: Submit National AI Database filings and secure MoST registration. |
| **General Sectors** | • E-Commerce & Retail<br>• Logistics & Transportation<br>• Media, Entertainment & MarTech<br>• Customer Support & CRM<br>• General Business Automation | **12 months** from effective date | **March 1, 2027** | • **Months 1–4 (Mar–Jun 2026)**: System classification, user transparency disclosure implementation.<br>• **Months 5–8 (Jul–Oct 2026)**: Content labeling pipeline deployment, audit logging infrastructure.<br>• **Months 9–12 (Nov 2026–Feb 2027)**: Pre-deployment testing and MoST portal filing verification. |

### 5.6 Regulatory Authority Governance Architecture

Compliance governance under the upgraded 2025–2026 statutory framework is shared between two primary state authorities:

```
                    ┌────────────────────────────────────────────────────────┐
                    │            GOVERNMENT OF VIETNAM (CHÍNH PHỦ)           │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
┌─────────────────────────────────┐                           ┌─────────────────────────────────┐
│  MINISTRY OF SCIENCE & TECH     │                           │   MINISTRY OF PUBLIC SECURITY   │
│           (MoST)                │                           │             (MPS)               │
│      Bộ Khoa học và Công nghệ   │                           │          Bộ Công an             │
├─────────────────────────────────┤                           ├─────────────────────────────────┤
│ • Lead Regulator for AI Law     │                           │ • Lead Regulator for PDPL       │
│   No. 134/2025/QH15             │                           │   No. 91/2025/QH15 & Decree 356 │
│ • National AI Database Portal   │                           │ • Department A05 Cybersecurity  │
│ • Conformity Assessment Bodies  │      INTER-AGENCY         │ • Certificate of Business       │
│ • AI Incident Reporting (72h/5d)│ ◄── COORDINATION & ─────► │   Eligibility (Data Processing) │
│ • AI Content Labeling Standards │     JOINT AUDITS          │ • Cross-Border Transfer Filings │
│ • Technical Standards & Ethics  │                           │ • Revenue-Based Penalties (5%)  │
│   (Decision 1290/QD-BKHCN)      │                           │ • Data Breach Investigation     │
└─────────────────────────────────┘                           └─────────────────────────────────┘
```

1. **Ministry of Science and Technology (MoST)**:
   - Primary governing authority for Law on Artificial Intelligence No. 134/2025/QH15.
   - Administers the National AI Database, accredits conformity assessment organizations, sets AI labeling technical standards, receives 72-hour urgent and 5-day serious incident filings, and monitors grace-period compliance.
2. **Ministry of Public Security (MPS - Department A05)**:
   - Primary governing authority for Personal Data Protection Law No. 91/2025/QH15, Decree 356/2025/ND-CP, Cybersecurity Law 2018, and Decree 53/2022/ND-CP.
   - Issues Certificates of Business Eligibility for data processing services, enforces verifiable consent standards, investigates data breaches, regulates outbound cross-border transfers, and assesses revenue-based fines (up to 5%).
3. **Inter-Agency Dual-Jurisdiction Protocol**:
   - When an AI system processes personal data of Vietnamese citizens, the enterprise must achieve dual compliance:
     - AI model conformity, transparency, and safety under MoST (Law 134/2025).
     - Data processing licensing, verifiable consent, and cross-border data transfer filing under MPS (PDPL 2025 / Decree 356).
