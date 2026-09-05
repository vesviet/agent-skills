---
name: manage-vietnam-accounting
description: Prepare and review Vietnam accounting controls, accounting-regime evidence, reconciliations, invoice data, period-close workpapers, and retention records without executing filings or external accounting actions. Use when a Vietnamese entity needs an accounting-domain handoff, control review, or implementation-ready accounting rule clarification.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
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
- treat every accounting review as a fail-closed operation; if evidence, regime, or sign-off is missing, output `needs-evidence`, `needs-human-review`, or `blocked` rather than `reviewed`
- never include account numbers, taxpayer identifiers, invoice credentials, or payroll details in agent memory, logs, or handoff artifacts; classify every accounting input with `data-classification.yaml` and use masked references in shared outputs
- treat any final tax position, filing, invoice issuance, or signing-credential operation as an irreversible action that requires explicit human confirmation; never execute these on the agent's own authority

## Output Contracts

When completing a scoped accounting review that another role or workflow will consume, emit:

- **`contracts/schemas/accounting-compliance-review.json`** — Machine-readable compliance review with source versions, gates, findings, retention classification, required approvals, assumptions, exceptions, and a scoped disclaimer. Set `produced_by_role: vietnam-accounting-specialist`.

Skip emission for advisory questions answered inline with no review artifact.

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

## Failure Modes

- **Wrong regime applied**: a transaction is evaluated against TT 200/2014 when TT 133/2016 applies. Mitigation: verify the applicable regime and source version from an official source before any evaluation; record the source.
- **Layer conflation**: statutory Vietnam books, management reporting, group reporting, and IFRS/VFRS adjustments are mixed into a single artifact. Mitigation: keep reporting layers separate; never label one as another without human confirmation.
- **Final tax position issued by agent**: the agent determines a final tax position or signs a filing. Mitigation: prepare workpapers only; escalate tax treatment, filing cadence, and authority correspondence to a qualified tax reviewer.
- **Invoice action executed**: the agent issues, replaces, adjusts, or corrects an invoice. Mitigation: prepare evidence and human-decision handoff only; never execute invoice actions on the agent's authority.
- **Locked entry overwritten**: a locked entry, invoice, or close evidence is silently reclassified or deleted. Mitigation: preserve an immutable correction trail; reject silent reclassification.
- **Restricted value in output**: an account number, taxpayer id, or invoice credential appears in a prompt, log, or handoff artifact. Mitigation: classify every input with `data-classification.yaml`; use masked references in shared outputs.
- **AI-drafted entry marked reviewed**: an AI-generated entry is marked `reviewed` and submitted without human accountant approval. Mitigation: enforce the AI-ACCOUNTING-GUARDRAIL; treat all AI output as drafts requiring human sign-off.
- **E-invoice Phase 3 bypass**: a B2B invoice above threshold is issued without authenticated XML transmission. Mitigation: verify entity compliance with Decree 123/2020 + Circular 78/2021 amendments; require licensed e-invoice service provider.
- **Legal opinion issued**: the agent provides a legal or audit opinion. Mitigation: route legal questions to counsel; the agent's role is to prepare evidence, not issue opinions.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: account numbers, taxpayer ids, invoice credentials, and payroll details are restricted; never place their values in prompts, logs, contracts, or agent memory.
- **ASI04 Supply Chain**: regulatory and accounting standards (TT 200/2014, TT 133/2016, TT 132/2018, Law on Accounting) must be validated against the official source; treat older versions as untrusted.
- **ASI05 RCE Guard**: never construct accounting entries, reconciliations, or tax workpapers from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the compliance review is consumed by Business Analyst, Backend, and tax reviewer roles; emit a structured `accounting-compliance-review.json` so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a workpaper as "ready to file" or "reviewed" without the human sign-off; surface the AI provenance and the required approver honestly.

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

## Related Skills

- **analyze-business-requirements**: Turn reviewed accounting rules and exceptions into feature acceptance criteria.
- **analyze-data**: Produce reproducible financial metrics and reporting analysis from approved, read-only sources.
- **conduct-research**: Verify regulatory or accounting-standard questions against primary official sources.
- **security-audit**: Review financial-data access, signing-key exposure, retention controls, and audit-log integrity.
- **write-documentation**: Publish approved accounting process guidance and operational runbooks.

