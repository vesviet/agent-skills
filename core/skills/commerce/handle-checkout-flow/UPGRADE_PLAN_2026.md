# handle-checkout-flow — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### PCI DSS v4.0.1 (Effective March 31, 2025)
- **Requirement 6.4.3**: All JavaScript on payment pages must be inventoried, justified, and loaded with Subresource Integrity (SRI) hashes + strict CSP nonce (`script-src 'nonce-...'`)
- **Requirement 11.6.1**: Automated tamper detection monitoring payment page HTTP headers and client-side scripts at least weekly (or continuously) for Magecart/formjacking detection
- SAQ A eligibility criteria updated (Jan 2025) — Requirements 6.4.3 and 11.6.1 removed from SAQ A for qualifying merchants

### Agentic Commerce Protocol (ACP) & Universal Commerce Protocol (UCP)
- **ACP** (OpenAI + Stripe, announced Sep 2025): Agentic Commerce Protocol for AI agents to execute purchases
- **UCP** (Google + partners, launched Jan 2026): Universal Commerce Protocol, Apache 2.0, compatible with A2A, AP2, MCP
- **Latest UCP v2026-08-25**: Multi-vertical foundations, grocery/location capabilities, 3DS2 flows, payment schedules, split payments, granular consent, loyalty support (breaking schema changes)
- **AP2 v0.2** (Apr 2026): Agent Payments Protocol donated to FIDO Alliance, Human Not Present payments for autonomous pre-authorized transactions

### EMV 3DS 2.3.1
- 100+ context attributes for frictionless risk-based authentication (>85% challenge-free)
- SCA exemption engine: Low-Value, TRA (Transaction Risk Analysis), Trusted Beneficiary

### Address Validation Lifecycle (Mandatory 2026)
- Must occur BEFORE tax calculation or shipping carrier requests
- API Standards: Google Maps Address Validation, Loqate, Smarty Streets
- Error handling: precise error subcodes for missing apartment numbers, invalid zip codes

### Tax Calculation Decision Tree (2026)
- **Stripe Tax**: Startups/mid-market within Stripe ecosystem, quick integration
- **TaxJar**: Multi-channel merchants (Shopify + custom), moderate volume, standard ERP
- **Avalara AvaTax**: Enterprise, high volume, complex Nexus, custom ERP, localized tax

### Economic Nexus Threshold Monitoring
- Track US state-by-state transaction count and sales volume programmatically
- Alert at 80% of threshold (e.g., 200 transactions or $100,000 sales)
- Most states: $100K sales OR 200 transactions (some dropped transaction count)

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| PCI DSS v4.0 references | Update to **PCI DSS v4.0.1** with 6.4.3 and 11.6.1 specifics |
| EMV 3DS generic | Specify **EMV 3DS 2.3.1** with 100+ context attributes |
| Agentic checkout mention | Add **ACP/UCP protocol integration** with pre-authorization gates, MoR assignment, programmatic checkout |
| Address validation | Add **mandatory address validation lifecycle** before tax/shipping |
| Tax engine selection | Add **decision tree** (Stripe Tax vs TaxJar vs Avalara) |
| Nexus monitoring | Add **80% threshold alerting** with automated registration triggers |

### 2. New 2026 Patterns to Add
- **Agentic Checkout Architecture** section (already partially there, expand with ACP/UCP specifics)
- **Address Validation Lifecycle** as mandatory isolated step
- **Stripe Tax / TaxJar / Avalara Decision Tree** with selection criteria
- **Economic Nexus Threshold Monitoring** with 80% alerting
- **Vietnam Decree 248/2026/ND-CP compliance** (seller identity verification, platform obligations)

### 3. Checklist Additions
- [ ] PCI DSS v4.0.1 Requirement 6.4.3: SRI hashes + CSP nonce on all payment page scripts
- [ ] PCI DSS v4.0.1 Requirement 11.6.1: Automated tamper detection (weekly/continuous)
- [ ] ACP/UCP protocol support for agentic checkout flows
- [ ] Pre-authorization gates and spending limits per agent session
- [ ] Merchant of Record (MoR) assignment for agentic transactions
- [ ] Programmatic checkout without interactive browser sessions
- [ ] Address validation via Google Maps/Loqate/Smarty Streets BEFORE tax/shipping
- [ ] Tax engine selection based on decision tree criteria
- [ ] Economic nexus monitoring at 80% threshold with alerts
- [ ] Vietnam Decree 248/2026 compliance: seller identity verification

### 4. Failure Mode Additions
- **Agentic checkout fraud**: Unauthorized agent spending beyond limits → Mitigation: Pre-authorization gates, spending limits, MoR assignment
- **Address validation bypass**: Tax/shipping calculated on invalid address → Mitigation: Mandatory validation gate before calculation
- **Nexus threshold breach**: Unregistered tax collection → Mitigation: 80% alerting, auto-registration workflow
- **PCI script injection**: Magecart via unverified third-party scripts → Mitigation: SRI + CSP nonce + weekly automated scanning

### 5. Output Contract Updates
- Add `contracts/schemas/agentic-commerce-spec.json` for ACP/UCP endpoints
- Add `contracts/schemas/address-validation-spec.json` for validation API contract
- Add `contracts/schemas/tax-engine-spec.json` for selected tax engine integration

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Update PCI DSS references to v4.0.1 with 6.4.3/11.6.1 specifics | Low |
| P0 | Add ACP/UCP agentic checkout architecture section | Medium |
| P0 | Add mandatory address validation lifecycle | Medium |
| P1 | Add tax engine decision tree (Stripe Tax/TaxJar/Avalara) | Medium |
| P1 | Add economic nexus 80% threshold monitoring | Medium |
| P1 | Add Vietnam Decree 248/2026 compliance notes | Low |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new specs | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)