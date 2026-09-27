# Vietnam Statutory Checklists & Contract Vetting Rubrics

This reference document provides detailed statutory checklists, contract vetting rubrics, and Decree 13/2023/ND-CP audit procedures supporting the `manage-vietnam-legal` skill.

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

## 2. Decree 13/2023/ND-CP Personal Data Protection (PDPD) Audit Checklist

### 2.1 Core Invariants under Decree 13
- **Article 9 - Rights of Data Subjects**: 8 fundamental rights (know, consent, access, withdraw consent, delete, restrict processing, data provision, object).
- **Article 11 - Valid Consent**: Explicit, voluntary, opt-in consent; separate consent for each distinct processing purpose. Pre-ticked checkboxes are strictly void.
- **Article 24 - Data Processing Impact Assessment (DPIA)**:
  - Must formulate and maintain a DPIA dossier within 60 days of commencing processing (Form 04).
  - Dossier must be available for inspection by the Department of Cybersecurity and Hi-tech Crime Prevention (A05 MPS).
- **Article 25 - Outbound Cross-Border Data Transfer**:
  - Applies whenever personal data of Vietnamese citizens is transferred abroad (e.g. cloud regions in Singapore, AWS, GCP).
  - Form 06 dossier must be drafted, maintained, and submitted to A05 MPS within 60 days of the first transfer.
  - Annual compliance reports and notification of contact details of the Data Protection Officer (DPO).

### 2.2 DPIA Audit Matrix

| Step | Statutory Focus | Verification Requirement | Status |
|---|---|---|---|
| 1 | Article 11 | Opt-in consent mechanisms with separate checkboxes per purpose | Mandatory |
| 2 | Article 19 | Direct vs indirect processing of sensitive personal data (biometrics, banking) | Enhanced |
| 3 | Article 24 | Form 04 internal DPIA dossier compiled and maintained on file | Mandatory |
| 4 | Article 25 | Form 06 outbound transfer dossier submitted to A05 MPS | Mandatory |
| 5 | Article 26 | Data breach notification to A05 MPS within 72 hours of occurrence | Contingent |

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
