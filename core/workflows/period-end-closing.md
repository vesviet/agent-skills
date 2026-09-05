---
description: End-to-end Vietnam accounting period closing: subledger cut-off, 3-way matching, revaluations, accruals, revenue/expense closing to TK 911, Decree 132 EBITDA cap, B01-B09 statements, and dual HITL sign-off.
---

## Period-End Closing Workflow

Use this workflow to execute a compliant, deterministic period-end financial closing cycle under Vietnamese Accounting Standards (VAS / Circular 200 / Circular 133) and the 2027 VFRS roadmap (Decision 345/QD-BTC), ensuring statutory compliance, zero-balance clearing, immutable audit trails, and segregation of duties.

### When To Use

- Monthly, quarterly, or annual accounting period close for Vietnamese legal entities
- Preparation of statutory financial statements (B01-DN, B02-DN, B03-DN, B09-DN)
- Reconciliation and clearing of temporary accounts (TK 511, TK 521, TK 632, TK 641, TK 642, TK 811, TK 821, TK 911)
- Year-end tax finalization and Decree 132/2020/ND-CP net interest deduction limitation review
- Period locking with immutable cryptographic audit logging and dual human-in-the-loop (HITL) digital sign-off

### Prerequisites

- Access to general ledger, subledgers (AR, AP, Inventory, Fixed Assets, Cash/Bank, Payroll), and ERP posting journals
- Access to electronic invoice XML repository, General Department of Taxation (GDT) verification services, and bank statements
- Active accounting regime confirmed (Circular 200/2014/TT-BTC, Circular 133/2016/TT-BTC, or Circular 132/2018/TT-BTC)
- Reference exchange rates from primary transacting commercial banks as of the closing date
- Asset and prepaid expense master registers with historical depreciation and amortization schedules
- Authorization tokens and cryptographic credentials for Chief Accountant and Legal Representative

### Workflow Steps

#### 1. Subledger Cut-Off & Period Ingestion

Role: **Vietnam Accounting Specialist**

Enforce strict transaction cut-off and ingest source transaction records across all accounting subsystems:

- Freeze transaction posting for the closing period; reject backdated journal entries without explicit supervisor override.
- Verify that all sales invoices, purchase invoices, warehouse receipts, and payment orders dated on or before the cut-off date are ingested.
- Audit input electronic invoices against Decree 123/2020/ND-CP and Circular 78/2021/TT-BTC:
  - validate Decision 1450/QD-TCT XML structure and verify digital signatures against trusted certificate authorities.
  - perform automated lookup on the GDT portal (`hoadondientu.gdt.gov.vn`) to confirm invoice existence and tax authority approval code (`MCCQT`).
  - screen vendor tax codes against the national tax registry (`tracuunnt.gdt.gov.vn`) to identify suspended (status 03) or runaway (status 04) entities.
  - verify non-cash payment vouchers (Ủy nhiệm chi) for all B2B invoices with gross value $\ge$ 20,000,000 VND per Circular 219/2013/TT-BTC.
- Classify any cut-off discrepancies into standard severity levels:
  - **Blocking**: suspended vendor invoice claimed for VAT deduction, missing non-cash payment proof for large invoice, or unrecorded transaction dated within the period.
  - **Important**: minor timestamp drift at cut-off boundary with immaterial tax impact.
  - **Follow-Up**: missing secondary vendor contact metadata.

Use skill: `manage-vietnam-accounting`

#### 2. Deterministic 3-Way Matching & Variance Resolution

Role: **Vietnam Accounting Specialist**

Execute algorithmic 3-way matching across procurement and inventory documents:

- Match Purchase Orders (PO), Goods Receipt Notes (GRN / Phiếu nhập kho), and Vendor Electronic Invoices across item codes, quantities, unit prices, and VAT rates.
- Enforce strict variance tolerances:
  - **Price Variance**: 0.00% allowable variance; block payment authorization if invoice unit price exceeds PO unit price without approved contract addendum.
  - **Quantity Variance**: 0.00% for discrete units; maximum $\le 0.50\%$ for bulk commodities within contract shrink margins.
- Manage cut-off inventory accruals:
  - **Goods Received Not Invoiced (GRNI)**: post provisional accrual for warehouse receipts without invoice at cut-off (Debit TK 152/156, Credit TK 331 without input VAT accrual); tag for automatic reversal upon invoice receipt in next period.
  - **Goods in Transit**: post goods purchased and accepted where ownership transferred but physical receipt is pending at cut-off (Debit TK 151, Debit TK 133, Credit TK 331/112).
- Route unresolved discrepancies to procurement and vendor managers for formal settlement.

Use skill: `manage-vietnam-accounting`

#### 3. Balance Reconciliations & Foreign Currency Revaluation

Role: **Vietnam Accounting Specialist**

Reconcile balance sheet accounts against external third-party statements and revalue foreign currency balances:

- Reconcile Cash in Bank (TK 112) against official bank statements and credit advices for every open bank account; prepare bank reconciliation workpapers identifying outstanding deposits and unpresented checks.
- Reconcile Accounts Receivable (TK 131) and Accounts Payable (TK 331) against customer and vendor balance confirmation letters (Biên bản đối chiếu công nợ); investigate balances older than 180 days for bad debt provisioning per Circular 48/2019/TT-BTC.
- Reconcile perpetual inventory subledgers (TK 15x) with physical warehouse count sheets; post inventory discrepancies (Debit/Credit TK 1381 or TK 3381) pending board approval.
- Execute year-end foreign currency monetary revaluation per Circular 200/2014/TT-BTC Article 69:
  - revalue foreign currency monetary assets (TK 1112, TK 1122, TK 128, TK 131 debit balances) using the actual buying rate of the commercial bank where transactions are conducted.
  - revalue foreign currency monetary liabilities (TK 331 credit balances, TK 341) using the actual selling rate of the primary lending commercial bank.
  - recognize revaluation differences in Foreign Exchange Differences (TK 413); transfer net gain to Financial Income (Credit TK 515) or net loss to Financial Expenses (Debit TK 635) at year-end closing. Do not revalue non-monetary items or advance payments.

Use skill: `manage-vietnam-accounting`

#### 4. Accrual Entries & Automated Amortization / Depreciation

Role: **Vietnam Accounting Specialist**

Calculate and post month-end cost center allocations, amortizations, and depreciation schedules:

- Automate prepaid expense amortization (TK 242):
  - amortize tools, office leases, equipment rentals, and repair expenditures straight-line into operating expense accounts (TK 641, TK 642, TK 627).
  - enforce the statutory maximum allocation period ceiling of **36 months** for CIT deductibility per Circular 96/2015/TT-BTC; flag any schedule exceeding 36 months as non-deductible for tax purposes.
- Automate fixed asset depreciation (TK 214):
  - calculate monthly straight-line or declining balance depreciation for all tangible (TK 211) and intangible (TK 213) assets per Circular 45/2013/TT-BTC.
  - verify asset useful lives against statutory minimum and maximum brackets in Appendix I of Circular 45/2013/TT-BTC.
- Post month-end payroll and social insurance accruals:
  - reconcile salary expenses (TK 622, TK 641, TK 642) against payroll summary sheets and gross salary payable (TK 334).
  - accrue statutory employer insurance contributions (TK 3383 Social Insurance 17.5%, TK 3384 Health Insurance 3%, TK 3386 Unemployment Insurance 1%, TK 3382 Trade Union 2%).

Use skill: `manage-vietnam-accounting`

#### 5. Revenue Deductions & Net Revenue Closing

Role: **Vietnam Accounting Specialist**

Close sales deductions and transfer net revenues into the profit and loss clearing account:

- Review and aggregate revenue deduction accounts:
  - Trade Discounts (TK 5211)
  - Sales Returns (TK 5212)
  - Sales Allowances (TK 5213)
- Transfer revenue deductions to Gross Revenue (TK 511):
  - Debit TK 511 (Revenue from goods sold and services rendered)
  - Credit TK 521 (TK 5211, TK 5212, TK 5213)
  - verify that ending balances for all TK 521 sub-accounts equal strictly 0.00 VND.
- Close Net Revenue and Financial/Other Income to Account 911 (Summary of Operations):
  - Debit TK 511 (Net revenue from sales and services)
  - Debit TK 515 (Financial income: interest, dividends, realized FX gains, revaluation gains)
  - Debit TK 711 (Other income: asset disposals, contract penalties received)
  - Credit TK 911 (Summary of operations)
  - verify that ending balances of TK 511, TK 515, and TK 711 equal strictly 0.00 VND.

Use skill: `manage-vietnam-accounting`

#### 6. Expense Closing to Account 911

Role: **Vietnam Accounting Specialist**

Close all operating, financial, and other expenses into the profit and loss clearing account:

- Close Cost of Goods Sold:
  - Debit TK 911 (Summary of operations)
  - Credit TK 632 (Cost of goods sold)
- Close Financial Expenses:
  - Debit TK 911 (Summary of operations)
  - Credit TK 635 (Financial expenses: interest expenses, borrowing fees, realized FX losses)
- Close Selling and Administrative Expenses:
  - Under Circular 200: Debit TK 911 / Credit TK 641 (Selling expenses) and Credit TK 642 (General and administrative expenses).
  - Under Circular 133: Debit TK 911 / Credit TK 6421 (Selling expenses) and Credit TK 6422 (General and administrative expenses).
- Close Other Expenses:
  - Debit TK 911 (Summary of operations)
  - Credit TK 811 (Other expenses: tax fines, asset liquidation residual book values)
- Audit temporary expense accounts post-closing: verify that TK 632, TK 635, TK 641, TK 642, and TK 811 have ending balances of strictly 0.00 VND.

Use skill: `manage-vietnam-accounting`

#### 7. CIT Calculation, Decree 132 30% EBITDA Cap & Net Profit Closing

Role: **Vietnam Accounting Specialist**

Compute Corporate Income Tax, enforce related-party net interest expense limitations, and transfer net profit to undistributed earnings:

- Calculate accounting profit before tax on Account 911:
  $$\text{Accounting Profit Before Tax} = \sum \text{Credits on TK 911} - \sum \text{Debits on TK 911}$$
- Screen for related-party relationships under Decree 132/2020/ND-CP Article 5:
  - if related-party transactions exist, calculate EBITDA per statutory formula:
    $$\text{EBITDA} = \text{Operating Profit} + \text{Net Interest Expense} + \text{Depreciation/Amortization}$$
  - compute the 30% EBITDA net interest expense deduction cap per Decree 132/2020/ND-CP Article 16.
  - disallow net interest expense exceeding 30% EBITDA on CIT Return Form 03-1A/TNDN (Box B4); register excess interest for 5-year carry-forward tracking.
  - if EBITDA $\le 0$, net deductible interest expense is 0 VND; disallow 100% of net interest expense for the current tax year.
- Calculate tax adjustments (Permanent differences B1, B2, B4, B7; Temporary differences B8-B14) to determine Taxable Income.
- Compute Current Corporate Income Tax (CIT rate 20%):
  - Debit TK 8211 (Current corporate income tax expense) / Credit TK 3334 (CIT payable).
- Close CIT expense to Account 911:
  - Debit TK 911 / Credit TK 8211.
- Close Net Profit After Tax to Undistributed Earnings (TK 4212):
  - if net profit: Debit TK 911 / Credit TK 4212.
  - if net loss: Debit TK 4212 / Credit TK 911.
- **Strict Account 911 Clearing Verification**: verify that the post-closing ending balance of Account 911 is strictly **0.00 VND**. Block progression immediately if any residual balance remains.

Use skill: `manage-vietnam-accounting`

#### 8. Statutory Financial Statements Assembly & Dual HITL Digital Sign-Off Gate

Role: **Vietnam Accounting Specialist**

Assemble statutory financial statements, generate immutable audit hashes, and enforce dual human-in-the-loop approvals:

- Assemble the complete statutory financial statements package:
  - **B01-DN (Balance Sheet)**: verify the fundamental balance sheet equality:
    $$\text{Total Assets} = \text{Total Liabilities} + \text{Owner's Equity}$$
  - **B02-DN (Income Statement)**: verify revenue, COGS, expenses, and profit figures match closed general ledger balances.
  - **B03-DN (Cash Flow Statement)**: verify direct or indirect operating, investing, and financing cash flows, ensuring:
    $$\text{Net Cash Flow} = \text{Closing Cash Balance} - \text{Opening Cash Balance}$$
  - **B09-DN (Notes to Financial Statements)**: complete required accounting policy disclosures, related-party transaction breakdowns, and VFRS dual-layer adjustments per Decision 345/QD-BTC.
- Generate cryptographic post-closing trial balance snapshot:
  - compute SHA-256 digest of post-closing ledger balances and emit OCSF 99001 compliance audit event.
  - set write-once-read-many (WORM) immutable period lock flag.
- Execute Dual HITL Digital Sign-Off Gate:
  - transmit closing package and audit report to Chief Accountant and Legal Representative.
  - require explicit digital signature approval tokens from both authorities.
  - reject automated closing attempts lacking valid human authorization tokens.
- Emit structured closing deliverable `contracts/schemas/period-end-closing-report.json`.

Use skill: `manage-vietnam-accounting`

### Checklist

- [ ] Subledger transactions frozen and period cut-off date enforced across AR, AP, bank, inventory, and payroll
- [ ] Invoices validated for GDT registration, XML signature authenticity, vendor active tax status, and non-cash bank transfer vouchers ($\ge$ 20M VND)
- [ ] Deterministic 3-way matching completed with zero unit price variance and GRNI/goods-in-transit cut-off accruals posted
- [ ] Bank accounts, customer/vendor balances, and physical inventory reconciled with discrepancies documented
- [ ] Monetary foreign currency assets and liabilities revalued using Circular 200 Article 69 commercial bank exchange rates
- [ ] Prepaid expenses (TK 242) amortized adhering to Circular 96 36-month ceiling and fixed asset depreciation (TK 214) calculated per Circular 45 brackets
- [ ] Revenue deductions (TK 521) cleared to TK 511, and net revenues and other income closed to Account 911
- [ ] Operating, financial, and other expenses closed to Account 911 with temporary accounts showing zero ending balance
- [ ] Decree 132 30% EBITDA net interest cap evaluated and CIT calculated with tax adjustments (B1-B14)
- [ ] Account 911 ending balance verified to be strictly 0.00 VND prior to net profit closing to TK 4212
- [ ] Statutory financial statements (B01-B09) assembled with balance equality validated and cryptographic snapshot generated
- [ ] Dual HITL approval tokens secured from Chief Accountant and Legal Representative before immutable period lock

### Related Workflows

- [QA Validation](qa-validation.md)
- [Service Review Release](service-review-release.md)
- [Data Migration](data-migration.md)
- [Tech Repo Review](tech-repo-review.md)

### Related Skills

- **manage-vietnam-accounting**: Execute subledger reconciliations, 3-way matching, amortization, depreciation, closing entries, and financial statements
- **analyze-data**: Query transaction ledgers, investigate reconciliation variance anomalies, and compute EBITDA
- **database-maintenance**: Ensure immutable audit trail preservation and WORM ledger snapshotting
- **write-documentation**: Document accounting policy disclosures, period-closing workpapers, and explanatory notes
- **security-audit**: Audit compliance with non-cash payment rules, GDT e-invoice authenticity, and segregation of duties

### Failure Modes

- **Account 911 Residual Balance**: Account 911 has a non-zero balance post-closing due to omitted expense entries or rounding differences. **Mitigation:** block closing workflow gate; run automated trial balance reconciliation to locate and resolve discrepancies before profit transfer.
- **Unverified Bogus E-Invoice**: Invoices from suspended or runaway vendors claimed for tax deduction. **Mitigation:** automated GDT portal lookup and tax status screening blocking payment and VAT deduction.
- **Decree 132 Net Interest Cap Breach**: Enterprise deducts net interest expense exceeding 30% EBITDA in violation of transfer pricing rules. **Mitigation:** automated EBITDA calculation and Form 03-1A/TNDN Box B4 adjustment.
- **Unauthorized Autonomous Period Lock**: AI agent closes accounting period without human officer authorization. **Mitigation:** mandatory cryptographic sign-off gate requiring Chief Accountant and Legal Representative tokens.
- **Amortization Beyond Statutory Cap**: Prepaid expenses amortized over 48–60 months instead of statutory 36-month limit. **Mitigation:** programmatic validation enforcing 36-month allocation ceiling.

### Output Contracts

When this workflow completes, emit:

- **`contracts/schemas/period-end-closing-report.json`** — comprehensive period-end closing deliverable capturing subledger reconciliations, closing adjustments, Account 911 zero balance verification, statutory statements package, and dual HITL approval tokens.
- **`contracts/schemas/accounting-compliance-review.json`** — regulatory compliance review certifying accounting regime, e-invoice verification, 3-way matching, and transfer pricing interest cap.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: strictly enforce segregation of duties; do not allow autonomous agent processes or non-finance roles to execute period closing or ledger locking.
- **ASI05 RCE & Unauthorized Mutation**: prohibit direct SQL UPDATE/DELETE queries on posted ledgers; enforce immutable append-only and reverse-and-repost accounting adjustments.
- **ASI06 Memory & Context Poisoning**: prevent unverified invoice data or invalid bank statements from corrupting accounting memory stores and general ledger databases.
- **ASI07 Inter-Agent Communication**: exchange accounting status between agents exclusively through typed JSON contracts (`period-end-closing-report.json`).
- **ASI09 Human-Agent Trust Exploitation**: maintain an immutable cryptographic SHA-256 trial balance hash and mandate dual human sign-off before period closure.
