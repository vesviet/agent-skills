# Vietnamese Formal Legal Opinion Drafting Guide

This guide establishes the structural standard, statutory hierarchy, and governance rules for drafting formal legal opinions under Vietnamese law.

## 1. Formal Opinion Architecture

A formal legal opinion delivered under the `legal-opinion-contract.json` schema must maintain the following sections:

1. **Header & Identification**: Opinion identifier (e.g., `VLO-2026-001`), date, requesting entity, and authoring legal counsel designation.
2. **Questions Presented**: Numbered, tightly scoped legal questions specifying the precise statutory determinations sought.
3. **Factual Background & Documents Examined**: Summary of material facts, list of contracts/licenses inspected, and express factual assumptions taken as true.
4. **Statutory Basis & Gazette Sources**: Table of governing Laws, Decrees, Circulars, and Precedents with official gazette (*Công báo*) promulgation citations.
5. **Issue-by-Issue Legal Analysis**: Systematic statutory interpretation applied to each question presented, evaluating enforceability, penalties, and liabilities.
6. **Executive Opinion & Risk Assessment**: Authoritative bottom-line determination with risk grading (LOW, MEDIUM, HIGH, CRITICAL).
7. **Reliance Conditions & Qualifications**: Factual boundaries, reliance limitations, and express assumptions.
8. **Action Plan & Remediation Roadmap**: Actionable implementation steps with owners and target completion dates.
9. **Caveats & Non-Litigation Notices**: Non-litigation disclosure and licensed attorney Human-in-the-Loop (HITL) sign-off token.

## 2. Vietnamese Statutory Hierarchy & Construction Rules

In interpreting statutory authorities, legal counsel must follow the Law on Promulgation of Legislative Documents 2015 (amended 2020):

1. **Hierarchy (*Hiệu lực pháp lý*)**:
   - Constitution 2013 (*Hiến pháp*)
   - Codes & Laws (*Bộ luật, Luật*) passed by the National Assembly
   - Ordinances & Resolutions (*Pháp lệnh, Nghị quyết*) of the National Assembly Standing Committee
   - Decrees (*Nghị định*) of the Government
   - Decisions (*Quyết định*) of the Prime Minister
   - Circulars (*Thông tư*) of Ministries and Ministerial-level agencies

2. **Canons of Construction**:
   - *Lex superior derogat legi inferiori*: Higher legislative acts prevail over subordinate regulations in case of conflict.
   - *Lex specialis derogat legi generali*: Specialized statutory enactments (e.g., Commercial Law 2005, AI Law 134/2025) prevail over general enactments (Civil Code 2015) within their defined subject matter.
   - *Lex posterior derogat legi priori*: Newly enacted legislation prevails over earlier legislation governing the same subject matter when enacted by the same authority.

## 3. Application of Supreme People's Court Precedents (*Án lệ*)

- Under Resolution No. 04/2019/NQ-HDTP of the Council of Judges of the Supreme People's Court, published precedents (*Án lệ*) are binding on Vietnamese courts in cases with analogous factual and legal circumstances.
- Formal legal opinions must review published precedents relevant to contract interpretation, penalty caps, labor severance, and corporate resolutions to evaluate judicial enforceability risk.

## 4. Framing Reliance Conditions and Limiting Assumptions

Standard limiting assumptions must be explicitly incorporated into `factual_background.assumptions`:
- Authenticity and completeness of all original documents and conformity of copies to originals.
- Genuineness of all signatures and seals of authorized legal representatives.
- Absence of fraudulent intent, coercion, or undisclosed side agreements modifying the reviewed transactions.
- Opinions are rendered based on Vietnamese law in effect as of the date of issuance; no obligation to update upon subsequent legislative enactments unless retained for ongoing review.

## 5. Human-in-the-Loop (HITL) Gate & Non-Litigation Protocol

- **Advisory Workpaper Boundary**: Autonomous agents produce preliminary internal legal workpapers and drafts. They do not hold legal signing authority.
- **Mandatory Licensed Attorney Review**: Before an opinion is issued externally to clients, counterparties, or auditors, it must be reviewed and signed off by a licensed practicing Vietnamese attorney-at-law (*Luật sư có chứng chỉ hành nghề*).
- **Non-Litigation Disclaimer**: Every opinion artifact must embed the non-litigation notice stating that the deliverable represents internal advisory analysis and does not constitute judicial representation before courts or arbitration tribunals.
