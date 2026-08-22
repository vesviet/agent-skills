---
name: manage-vietnam-accounting
description: Prepare and review Vietnam accounting controls, accounting-regime evidence, reconciliations, invoice data, period-close workpapers, and retention records without executing filings or external accounting actions. Use when a Vietnamese entity needs an accounting-domain handoff, control review, or implementation-ready accounting rule clarification.
---

# Manage Vietnam Accounting

Use this skill when a Vietnamese accounting workflow needs a traceable domain review before requirements, software changes, reporting, period close, or a human-authorized external action.

## Core Rules

- treat financial account numbers, taxpayer identifiers, invoice credentials, payroll details, and customer PII as restricted data; do not place their values in prompts, logs, contracts, or agent memory
- identify the legal entity, accounting period, applicable accounting regime, and effective source version before evaluating a posting, invoice, close, or report
- treat TT 200/2014, TT 133/2016, TT 132/2018, Law on Accounting, e-invoice rules, and tax rules as versioned inputs; verify applicability and amendments from official sources before making a material claim
- distinguish statutory Vietnam books, management reporting, group reporting, and IFRS/VFRS adjustments; never label one as another without human confirmation
- prepare accounting evidence and tax workpapers, but do not determine a final tax position, sign or submit filings, issue invoices, operate signing credentials, or provide a legal or audit opinion
- fail closed: if the accounting regime, evidence, source version, or approval is missing, output `needs-evidence`, `needs-human-review`, or `blocked` rather than `reviewed`
- preserve an immutable correction trail: do not overwrite, delete, or silently reclassify locked entries, invoices, or close evidence
- **AI-ACCOUNTING-GUARDRAIL**: When AI-assisted tools generate accounting entries, reconciliations, or tax workpapers, treat all AI output as a draft requiring human accountant review and approval. Never mark AI-drafted entries as `reviewed` or submit them directly to accounting systems without HITL approval.
- **E-INVOICE-PHASE-3**: Verify entity compliance with Vietnam e-invoice Phase 3 mandate (Decree 123/2020 + Circular 78/2021 amendments); all B2B invoices above threshold MUST be transmitted via authenticated XML through a licensed e-invoice service provider with tax authority real-time validation.

## Suggested Process

### 1. Confirm Scope And Data Boundary

Capture the legal entity, period, requested decision, scope, and whether the work concerns accounting records, invoices, reconciliation, financial statements, tax workpapers, or retention.

Classify inputs before processing. Use masked references in artifacts and request a secure, human-operated environment if restricted values are required.

### 2. Lock The Regulatory And Accounting Basis

Verify from an official source or an approved internal policy register:

- accounting regime: TT 200/2014, TT 133/2016, TT 132/2018, or another confirmed regime
- effective date, amendments, and transitional rules relevant to the accounting period
- VAS versus statutory, management, group, or IFRS/VFRS reporting purpose
- applicable e-invoice and tax evidence requirements, without deciding a tax position

Record the source version and any unresolved applicability question.

### 3. Review Evidence And Accounting Controls

For each scoped transaction or close area, check the available evidence, approval path, cut-off, debit/credit mapping, tax-code reference, counterparty/master-data reference, and audit trail.

Reconcile applicable areas such as bank, accounts receivable, accounts payable, inventory, fixed assets, payroll, tax payable, invoice register, and general ledger. Record differences, evidence gaps, and an owner for resolution.

### 4. Apply Invoice And Tax Boundaries

For e-invoice work, determine only whether the evidence supports a human decision on issuance, replacement, adjustment, or correction. Check the invoice state, source evidence, transmission log, and approval requirement first.

For tax work, prepare reconciled accounting inputs and flag exceptions. Escalate tax treatment, filing cadence, deductions, incentives, transfer pricing, foreign-contractor, and authority-correspondence questions to a qualified tax reviewer.

### 5. Prepare The Controlled Handoff

Emit `contracts/schemas/accounting-compliance-review.json` when another role or workflow needs a machine-readable review. Include source versions, gates, findings, retention classification, required approvals, assumptions, exceptions, and a scoped disclaimer.

Route implementation rules to Business Analyst and Backend/E-commerce Engineer, data/reporting questions to Data Analyst, tax questions to a qualified tax reviewer, legal questions to counsel, and security/retention controls to Security Engineer or platform owners.

## Output Schema

Use: `contracts/schemas/accounting-compliance-review.json`

## Checklist

- [ ] legal entity, accounting period, scope, and reporting purpose are explicit
- [ ] applicable accounting regime and source version are confirmed or marked `needs-human-review`
- [ ] statutory, management, group, and IFRS/VFRS reporting layers are not conflated
- [ ] evidence, cut-off, account mapping, approval, and audit trail checks are documented for every scoped area
- [ ] reconciliation differences are evidenced, assigned, and not silently netted or written off
- [ ] invoice actions are not executed; required human approval and current invoice state are recorded
- [ ] tax workpapers are clearly separated from final tax positions, filing decisions, and legal advice
- [ ] retention classification, access controls, and legal-hold check are documented before any archival or deletion proposal
- [ ] restricted values are absent from outputs, logs, prompts, and agent memory
- [ ] accounting-compliance-review.json records source versions, gates, exceptions, residual risk, and required approvals

## Output Contracts

When completing an accounting regime review, reconciliation check, or period-close workpaper verification, emit:

- **`contracts/schemas/accounting-compliance-review.json`** — Emitted when conducting a Vietnam statutory accounting compliance review, audit trail check, reconciliation verification, or tax workpaper evaluation. Set `produced_by_role: vietnam-accounting-specialist`.

Skip emission for informal financial queries that do not form part of statutory or management close records.

## Related Skills

- **analyze-business-requirements**: Turn reviewed accounting rules and exceptions into feature acceptance criteria.
- **analyze-data**: Produce reproducible financial metrics and reporting analysis from approved, read-only sources.
- **conduct-research**: Verify regulatory or accounting-standard questions against primary official sources.
- **security-audit**: Review financial-data access, signing-key exposure, retention controls, and audit-log integrity.
- **write-documentation**: Publish approved accounting process guidance and operational runbooks.

