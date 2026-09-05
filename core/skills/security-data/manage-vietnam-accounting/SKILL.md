---
name: manage-vietnam-accounting
description: Prepare and review Vietnam accounting controls, accounting-regime evidence, reconciliations, invoice data, period-close workpapers, and retention records without executing filings or external accounting actions. Use when a Vietnamese entity needs an accounting-domain handoff, control review, or implementation-ready accounting rule clarification.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Manage Vietnam Accounting

Use this skill when a Vietnamese accounting workflow needs a traceable domain review before requirements, software changes, reporting, period close, or a human-authorized external action.

## Core Rules

- treat financial account numbers, taxpayer identifiers, invoice credentials, payroll details, and customer PII as restricted data; do not place their values in prompts, logs, contracts, or agent memory
- identify legal entity, accounting period, applicable regime (Circular 200/2014, Circular 133/2016, Circular 132/2018), and effective source version before evaluating postings, invoices, or closes
- govern Decision 345/QD-BTC VFRS transition: maintain pure VAS statutory general ledgers and isolate VFRS adjustments (IFRS 16 leases, IFRS 9 ECL, IFRS 15 revenue) in a dual-reporting layer
- validate incoming e-invoice XML against Decision 1450/QD-TCT, verify XMLDSig X.509 signatures, perform real-time GDT portal queries (`hoadondientu.gdt.gov.vn`), and screen vendor tax status (Status 03/04 on `tracuunnt.gdt.gov.vn`)
- enforce non-cash bank transfer payment rule (Circular 219/2013, Circular 96/2015) for invoices $\ge$ 20,000,000 VND, requiring bank payment vouchers (Ủy nhiệm chi)
- execute deterministic PO-GRN-Invoice 3-way matching with zero unit price variance tolerance; manage Goods Received Not Invoiced (GRNI) cut-off accruals (Debit TK 152/156, Credit TK 331) without VAT
- enforce Decree 132/2020 30% EBITDA net interest deduction cap for associated enterprises, applying zero deduction for negative EBITDA and maintaining the 5-year carry-forward register
- enforce period close invariants: allocate TK 242 prepaid expenses ($\le$ 36 months), compute TK 214 depreciation per Circular 45 brackets, and assert Account 911 ending balance is strictly zero
- enforce immutable WORM storage with SHA-256 snapshotting and reverse-and-repost accounting; prohibit direct SQL UPDATE or DELETE on posted general ledgers
- **AI-ACCOUNTING-GUARDRAIL**: Treat all AI-generated entries as drafts requiring human accountant review; require Chief Accountant and Legal Representative HITL approval tokens for period locks and filings

## Output Contracts

When completing a scoped accounting review or period close, emit the appropriate contract:

- **`contracts/schemas/accounting-compliance-review.json`** — Machine-readable compliance review with source versions, gates, findings, retention classification, required approvals, assumptions, exceptions, and a scoped disclaimer. Set `produced_by_role: vietnam-accounting-specialist`.
- **`contracts/schemas/period-end-closing-report.json`** — Machine-readable financial period-end closing report capturing trial balance reconciliations, closing entries, Account 911 clearing, financial statements, and HITL approval token. Set `produced_by_role: vietnam-accounting-specialist`.

## Suggested Process

### 1. Confirm Scope And Data Boundary
Capture legal entity, period, reporting purpose (VAS statutory vs VFRS dual reporting), and review scope. Classify data with `data-classification.yaml` and mask PII and credentials.

### 2. Lock Accounting Regime And VFRS Dual-Reporting Layer
Confirm candidate regime (Circular 200, 133, or 132). For Circular 133, enforce prohibition of TK 621, 622, 623, 627, 641. For entities transitioning under Decision 345/QD-BTC, maintain separate VFRS adjustment schedules. See detailed guidance in [`references/vas-vfrs-chart-of-accounts.md`](references/vas-vfrs-chart-of-accounts.md).

### 3. E-Invoice Validation And Taxpayer Screening
Parse raw XML against Decision 1450 schema, verify XMLDSig X.509 signature and CA validity, query GDT portal API, screen vendor tax status on `tracuunnt.gdt.gov.vn`, track Form 04/SS-HDDT, and assert bank payment order for vouchers $\ge$ 20M VND. See detailed guidance in [`references/e-invoice-risk-playbook.md`](references/e-invoice-risk-playbook.md).

### 4. Deterministic 3-Way Matching And Accruals
Reconcile PO, GRN, and vendor invoice. Block price variances (0.00% threshold). Post period-end GRNI accruals (Debit TK 152/156, Credit TK 331 with zero VAT) and goods in transit (TK 151). See detailed guidance in [`references/three-way-matching-and-controls.md`](references/three-way-matching-and-controls.md).

### 5. Related-Party Screening And Decree 132 EBITDA Cap
Identify Article 5 associated enterprises. Calculate EBITDA and net interest expense. Apply 30% cap, enter disallowed interest into CIT Box B4 (0 VND deduction if EBITDA $\le$ 0), and update 5-year carry-forward register.

### 6. Period-End Adjustments And Account 911 Clearing
Reconcile subledgers to GL. Allocate TK 242 ($\le$ 36-month cap). Compute TK 214 depreciation. Close revenue deductions (TK 521 $\rightarrow$ TK 511) and close revenue and expenses to Account 911. Assert Account 911 ending balance is exactly zero.

### 7. Financial Statements, WORM Snapshot And HITL Sign-Off
Assemble B01-DN, B02-DN, B03-DN, B09-DN with balance equality checks. Emit SHA-256 snapshot and OCSF 99001 audit event. Obtain Chief Accountant and Legal Representative HITL approval tokens before period lock.

## Failure Modes

- **Wrong regime applied**: Circular 200 accounts used in Circular 133 books. Mitigation: validate regime rules and block prohibited accounts (TK 621, 622, 627, 641).
- **Layer conflation**: statutory VAS books and VFRS adjustments mixed in a single ledger. Mitigation: maintain separate VFRS dual-reporting adjustment schedules.
- **Unverified e-invoice XML booked**: invoices recorded from PDF without XMLDSig check. Mitigation: enforce Decision 1450 XML parser, SHA-256 digests, and GDT status checks.
- **Non-cash payment breach**: invoice $\ge$ 20M VND settled in cash. Mitigation: require bank payment order (Ủy nhiệm chi); disallow VAT credit and CIT deduction.
- **Decree 132 EBITDA cap breach**: related-party net interest exceeding 30% EBITDA claimed for CIT. Mitigation: compute EBITDA cap and report excess in CIT Box B4.
- **Account 911 residual balance**: period locked with non-zero Account 911 balance. Mitigation: verify Account 911 balance is zero before closing gate approval.
- **Direct ledger mutation**: SQL UPDATE/DELETE on posted ledgers. Mitigation: enforce WORM storage and reverse-and-repost accounting.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: restricted financial and tax identifiers must never be placed in prompts, logs, or agent memory.
- **ASI04 Supply Chain**: validate tax regulations against official gazettes; verify XMLDSig certificates against NEAC root CA.
- **ASI05 RCE Guard**: parse XML payloads using hardened, non-evaluating XML parsers with external entity resolution disabled (XXE defense).
- **ASI07 Inter-Agent Communication**: emit structured, schema-validated contracts (`accounting-compliance-review.json` or `period-end-closing-report.json`).
- **ASI09 Human-Agent Trust Exploitation**: surface AI draft provenance; never represent books as closed without Chief Accountant HITL sign-off.

## Checklist

- [ ] legal entity, accounting period, scope, and reporting purpose are explicit
- [ ] applicable accounting regime and source version are confirmed or marked `needs-human-review`
- [ ] statutory VAS books and VFRS dual-reporting adjustments are isolated in separate layers
- [ ] e-invoice XML conforms to Decision 1450, signature is valid, and GDT lookup status is cleared
- [ ] vendor tax status is screened; suspended (03) and runaway (04) entities are blocked
- [ ] invoices $\ge$ 20M VND are verified against bank transfer vouchers (Ủy nhiệm chi)
- [ ] deterministic 3-way match passes with 0.00% price variance; GRNI accruals posted without VAT
- [ ] Decree 132 EBITDA net interest cap calculated; negative EBITDA zero-deduction rule enforced
- [ ] TK 242 allocation $\le$ 36 months, TK 214 depreciation within Circular 45 brackets, and Account 911 cleared to zero
- [ ] financial statements satisfy balance equality equations (B01, B02, B03, B09)
- [ ] immutable WORM snapshot generated, OCSF 99001 logged, and Chief Accountant HITL token verified
- [ ] output contract emitted: `accounting-compliance-review.json` or `period-end-closing-report.json`

## Related Skills

- **analyze-business-requirements**: Turn reviewed accounting rules and exceptions into feature acceptance criteria.
- **analyze-data**: Produce reproducible financial metrics and reporting analysis from approved, read-only sources.
- **conduct-research**: Verify regulatory or accounting-standard questions against primary official sources.
- **security-audit**: Review financial-data access, signing-key exposure, retention controls, and audit-log integrity.
- **write-documentation**: Publish approved accounting process guidance and operational runbooks.
