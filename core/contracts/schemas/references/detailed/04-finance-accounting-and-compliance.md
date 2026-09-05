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
