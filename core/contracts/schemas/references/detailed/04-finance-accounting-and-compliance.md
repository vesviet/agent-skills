# Finance, Accounting & Compliance



#### `accounting-compliance-review.json`

**Vietnam Accounting Compliance Review**
Structured review from Vietnam Accounting Specialist for a defined legal entity and accounting period. Captures accounting-regime confirmation, source-version evidence, reconciliation status, period-close gates, retention controls, exceptions, and required human approvals. It provides no tax filing decision, legal opinion, audit assurance, or authorization to sign, submit, issue, replace, adjust, void, or delete a live record.

Required fields: `contract_type`, `review_id`, `entity`, `accounting_period`, `scope`, `accounting_regime`, `source_version_register`, `validation_gates`, `status`, `disclaimer`
✅ Has example

#### `period-end-closing-report.json`

**Period-End Closing Report**
Structured deliverable emitted by Vietnam Accounting Specialist upon executing period-end closing. Captures subledger cut-offs, deterministic 3-way matching reconciliations, monetary foreign currency revaluations, automated amortization (TK 242) and depreciation (TK 214), revenue deductions and expense clearing to Account 911, Decree 132 30% EBITDA net interest expense deduction cap verification, post-closing trial balance equality, statutory financial statements package (B01-DN through B09-DN), and dual HITL digital sign-off approval tokens from Chief Accountant and Legal Representative.

Required fields: `contract_type`, `closing_id`, `entity`, `period`, `accounting_regime`, `subledger_reconciliations`, `closing_adjustments`, `account_911_clearing`, `financial_statements_package`, `audit_trail`, `hitl_approval`, `data_classification`
Size: 17,053 bytes
✅ Has example

#### `amis-voucher-contract.json`

**AMIS Accounting Voucher Contract**
Enterprise financial schema for multi-channel retail vouchers (Sales Invoices, Delivery Notes cum Sales Invoices, Receipt Vouchers, and Platform Fee Allocations) exported to MISA AMIS ERP, enforcing VAS 14 revenue recognition, 3-tier voucher breakdown, pre-tax VAT decomposition, and strict debit-credit balance verification.

Required fields: `contract_type`, `batch_id`, `accounting_period`, `legal_entity`, `accounting_regime`, `channel`, `summary`, `vouchers`
✅ Has example

#### `stock-audit-session.json`

**Stock Audit Session Contract**
Physical inventory stocktake contract governing the entire audit lifecycle (draft, in_progress, review, recount, closed), offline PWA/HID barcode event streams, tolerance thresholds, anti-anchoring blind recounts, variance reconciliation, TK 1381/3381 suspense accounting, and multi-tier approval sign-offs.

Required fields: `contract_type`, `session_id`, `store_code`, `store_name`, `audit_type`, `lifecycle_status`, `created_by`, `created_at`, `tolerance_config`, `reconciliation_summary`, `items_variance`, `approvals`
✅ Has example

#### `legal-compliance-review.json`

**Vietnam Legal Compliance Review**
Structured machine-readable legal and regulatory compliance assessment emitted by Vietnam Legal Counsel covering corporate governance, commercial contracts, labor relations, intellectual property, personal data protection (PDPD Decree 13/2023/ND-CP), and cybersecurity. Captures statutory citations, risk matrices, mitigation recommendations, and mandatory HITL approval gates. It provides no external court representation, unauthorized litigation advocacy, or authority to execute binding corporate contracts.

Required fields: `contract_type`, `metadata`, `compliance_status`, `risk_matrix`, `statutory_citations`, `recommendations`, `human_approval_gate`
✅ Has example

#### `legal-opinion-contract.json`

**Vietnam Legal Opinion Contract**
Structured machine-readable formal legal opinion emitted by Vietnam Legal Counsel analyzing specific legal issues, statutory interpretation, factual background, risk assessments, and caveats under Vietnamese law. Requires Human-In-The-Loop review and sign-off by a qualified practicing lawyer before external reliance or execution.

Required fields: `contract_type`, `metadata`, `factual_background`, `legal_issues`, `conclusion_and_opinion`, `caveats_and_disclaimers`
✅ Has example


