# PCI DSS v4.0.1 and Agentic Checkout Specifications (2026)

## 1. Regulatory & Compliance Architecture

### 1.1 PCI DSS v4.0.1 Core Requirements
Compliance with Payment Card Industry Data Security Standard (PCI DSS) v4.0.1 is mandatory across all checkout touchpoints:

- **Requirement 6.4.3 (Script Integrity on Payment Pages)**:
  - All JavaScript executed within payment contexts (both first-party and third-party) must be explicitly inventoried with legitimate business justification.
  - Scripts must be loaded with **Subresource Integrity (SRI)** hashes (`integrity="sha384-..."`) and cryptographically bound via a per-request strict **Content Security Policy (CSP)** nonce (`script-src 'nonce-<random-b64>' 'strict-dynamic'`).
  - Inline event handlers (`onclick`, `onload`) are strictly prohibited.
- **Requirement 11.6.1 (Client-Side Tamper Detection)**:
  - Implement continuous or weekly automated integrity checks comparing live script hashes and HTTP headers against canonical deployment baselines.
  - Immediate alerting on unauthorized script injection or DOM tampering (Magecart / digital skimming mitigation).
- **SAQ A Scope Boundaries**:
  - Entire cardholder data environment (CDE) must be fully outsourced to validated third-party payment processors using hosted fields, iframes, or modal redirects.
  - Zero raw Primary Account Numbers (PAN), CVV/CVC, or track data may enter the merchant runtime, application memory, or logging layer.

---

## 2. Agentic Commerce Protocols (ACP & UCP)

### 2.1 Protocol Topology
Modern commerce systems support autonomous agent transactions across two interoperable frameworks:
- **Agentic Commerce Protocol (ACP)** (OpenAI / Stripe): Optimized for headless, tool-driven instant checkout inside conversational runtimes.
- **Universal Commerce Protocol (UCP v2026-08-25)**: Open standard (Apache 2.0) compatible with Agent-to-Agent (A2A 1.0), AP2 v0.2, and Model Context Protocol (MCP).

### 2.2 Autonomous Payment Gates & Risk Controls
- **Pre-Authorization Limits**: Each agent session must operate within an explicit credit line or balance authorization token (e.g., maximum $500 per transaction, $2,000 per 24 hours).
- **Merchant of Record (MoR)**: Explicit declaration of MoR for tax remittance, chargeback liability, and regulatory reporting on agent-initiated sales.
- **AP2 v0.2 (Human-Not-Present FIDO Token)**: Autonomous checkout uses pre-authorized cryptographic assertions bound to the user's biometric authenticator, bypassing interactive browser challenges.

---

## 3. Risk-Based Authentication & Frictionless 3DS

### 3.1 EMV 3DS 2.3.1 Specification
- Over 100 contextual attributes transmitted in the 3DS request: device fingerprint, behavioral telemetry, IP velocity, browser plugins, account age, shipping/billing address match.
- **Strong Customer Authentication (SCA) Exemption Engine**:
  - *Low-Value Transactions*: Transactions < €30 or regional equivalent.
  - *Transaction Risk Analysis (TRA)*: Qualified acquirer exemption for low-fraud merchant tiers.
  - *Trusted Beneficiary / Whitelisting*: Customer-approved merchant exemptions.

---

## 4. Address Validation Lifecycle

Address validation must occur as an isolated, mandatory gate **prior** to tax calculation or shipping carrier quotation:
1. **Normalization**: Parse street lines, postal codes, and regional subdivisions via Loqate, Google Maps Address Validation, or Smarty Streets.
2. **Subcode Resolution**: Evaluate granular API subcodes (`MISSING_SECONDARY_UNIT`, `INVALID_POSTAL_CODE`, `UNCONFIRMED_STREET`). Reject or prompt correction before downstream processing.
3. **Delivery Point Validation (DPV)**: Confirm mailable delivery point status (`DPV: Y`).

---

## 5. Tax Engine & Economic Nexus Decision Tree

### 5.1 Tax Engine Selection Matrix
- **Stripe Tax**: Recommended for digital-native merchants operating entirely on Stripe infrastructure; automated registration and instant calculation.
- **TaxJar**: Multi-channel retailers (combining custom e-commerce with Shopify/Amazon); automated filing support.
- **Avalara AvaTax**: Enterprise systems with complex supply chains, custom ERPs (SAP, NetSuite), cross-border VAT/GST, and specialized commodity exemptions.

### 5.2 Economic Nexus 80% Early-Warning System
- Monitor state-by-state gross receipts and transaction frequencies.
- Trigger automatic alert and compliance ticket when volume reaches 80% of statutory nexus thresholds (e.g., $80,000 revenue or 160 transactions in $100K/200-transaction jurisdictions).

---

## 6. Vietnam Regulatory Compliance (Decree 248/2026/ND-CP)

- **Seller Identity Verification**: Digital identity verification mandatory for all marketplace sellers prior to catalog listing and payout clearance.
- **Platform Disclosures**: Public display of platform rights, resolution dispute standards, transparent pricing structures, and affiliate partner relationships.
- **Electronic ID Integration**: Electronic citizen ID verification (VNeID level 2) enforced for commercial sellers and live streamers.
