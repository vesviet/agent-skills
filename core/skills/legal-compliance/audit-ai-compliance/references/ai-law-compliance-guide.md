# Vietnam Law on Artificial Intelligence No. 134/2025/QH15 Compliance Guide

This guide details the statutory obligations, classification methodology, and compliance procedures under Vietnam's Law on Artificial Intelligence No. 134/2025/QH15 (effective March 1, 2026).

## 1. Statutory Framework & Scope

- **Governing Law**: Law on Artificial Intelligence No. 134/2025/QH15.
- **Effective Date**: March 1, 2026.
- **Lead Regulatory Authority**: Ministry of Science and Technology (MoST / *Bộ Khoa học và Công nghệ*).
- **Coordinating Authority**: Ministry of Public Security (MPS / *Bộ Công an* - Department A05) for cybersecurity and data privacy.
- **Applicability**: All domestic and foreign organizations developing, providing, deploying, or utilizing AI systems or automated decision-making engines in Vietnam or affecting Vietnamese citizens.

## 2. Three-Tier Risk Framework

| Risk Tier | Scope & Qualifying Criteria | Core Obligations | Grace Period |
| :--- | :--- | :--- | :--- |
| **High-Risk** | Critical infrastructure, healthcare diagnostic/treatment, automated credit scoring & financial lending, education assessment, biometric categorization & emotion recognition, autonomous vehicles, law enforcement. | Mandatory conformity assessment (*đánh giá sự phù hợp*); National AI Database registration; continuous risk monitoring; technical documentation logging; local presence or authorized representative for foreign providers. | 18 months (until Sep 1, 2027) for Health/Edu/Finance; 12 months (until Mar 1, 2027) for others. |
| **Medium-Risk** | Customer-facing conversational agents (chatbots), recommendation systems, algorithmic content feeds, automated translation, non-critical enterprise analytics. | User transparency disclosure (informing users of AI interaction); AI-generated content watermarking/labeling; regular operational reporting; sample audit readiness. | 12 months (until Mar 1, 2027). |
| **Low-Risk** | Internal software development tools, spam filters, basic heuristic automation, search indexing. | Adherence to national AI ethical principles; voluntary labeling; minimal reporting. | 12 months (until Mar 1, 2027). |

## 3. High-Risk AI Conformity Assessment & Registration

### 3.1 Conformity Assessment Obligations
1. **Technical Documentation**: Comprehensive system architecture, model training methodology, dataset lineage, and performance evaluation metrics.
2. **Safety & Robustness Testing**: Verification of cybersecurity defenses against prompt injection, adversarial evasion, and unauthorized output manipulation.
3. **Data Governance Audit**: Alignment with PDPL No. 91/2025/QH15 regarding training data consent, data minimization, and bias mitigation.
4. **Third-Party Evaluation**: Certification by a MoST-accredited conformity assessment body prior to commercial rollout.

### 3.2 National AI Database Registration
- High-risk systems must be registered on the National AI Database portal hosted by MoST.
- Registration requires submitting the system identifier, deployment scope, risk mitigation plan, conformity certificate, and designated contact person.
- Foreign providers must submit the corporate registration of their Vietnamese branch, subsidiary, or notarized Authorized Representative agreement.

## 4. Transparency & Content Labeling Mandates

- **AI Interaction Notification**: Any system interacting directly with human users must inform the user clearly and conspicuously at the inception of the interaction that they are communicating with an AI system.
- **AI-Generated Content Labeling**: Text, images, audio, deepfakes, and videos generated or synthetically manipulated by AI must include:
  1. Human-perceptible disclaimer badges or visual/audio watermarks.
  2. Machine-readable cryptographic metadata indicating AI provenance.

## 5. Incident Reporting Timelines

| Severity Class | Criteria | Mandatory Timeline | Recipient Body |
| :--- | :--- | :--- | :--- |
| **Urgent Incident** | Loss of life, bodily harm, critical infrastructure disruption, systemic financial loss, or uncontrolled model deviation. | **Within 72 hours** of initial detection | Department of High Technology (MoST) & National Cyber Security Center (MPS) |
| **Serious Incident** | Substantial personal data leakage, discriminatory bias impacting large user groups, or persistent algorithmic malfunction. | **Within 5 working days** of detection | MoST Regulatory Inspection Portal |

## 6. Statutory Penalties & Enforcement

- **Administrative Fines**: Up to VND 2,000,000,000 for organizational non-compliance with conformity assessment, registration, or labeling mandates.
- **Revenue-Based Penalties**: Fines up to 5% of prior year's gross revenue for systemic cross-border violations or reckless deployment of uncertified High-risk AI.
- **Operational Sanctions**: Temporary suspension of service operation, revocation of digital domain licenses, or blacklisting of foreign provider endpoints.
