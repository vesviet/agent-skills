# Deterministic 3-Way Matching, Related-Party Governance & Audit Controls Playbook

## 1. Deterministic PO-GRN-Invoice 3-Way Matching Protocol

Procurement and payables governance requires algorithmic reconciliation across three independent evidentiary documents before an accounts payable obligation is approved for disbursement.

```
+-------------------+      +-------------------+      +-------------------+
|  Purchase Order   |      |   Goods Receipt   |      |   Vendor E-Invoice|
|       (PO)        |      |    Note (GRN)     |      |       (INV)       |
+-------------------+      +-------------------+      +-------------------+
          \                          |                          /
           \                         |                         /
            v                        v                        v
      +--------------------------------------------------------------+
      |             Deterministic 3-Way Matching Engine              |
      | - Line item SKU & description cross-reference                |
      | - Quantity reconciliation (PO Qty >= GRN Qty >= Inv Qty)     |
      | - Unit price invariance check (PO Price == Inv Price)        |
      | - VAT rate cross-check (PO Tax Rate == Inv Tax Rate)         |
      | - Payment term verification & vendor bank verification       |
      +--------------------------------------------------------------+
                                     |
                                     v
                 +-------------------+-------------------+
                 |                                       |
           [Match Passed]                         [Match Failed]
                 |                                       |
                 v                                       v
         Approved for Booking                    Exception Routing
          & Payment Schedule                    & AP Payment Freeze
```

### Matching Data Attributes
1. **Header Attributes**: Vendor Tax Identification Number (MST bên bán), Currency code (VND/USD), Payment Terms, Delivery Address.
2. **Line Item Attributes**:
   - Item Master SKU / Part Number.
   - Item description.
   - Invoiced Quantity vs Received Quantity vs Ordered Quantity.
   - Unit price exclusive of VAT.
   - VAT rate (0%, 5%, 8%, 10%, non-taxable).
   - Line subtotal, VAT amount, and total gross amount.

---

## 2. Price and Quantity Variance Tolerance Gates

Automated gates prevent unauthorized disbursements and inventory misstatements.

### Tolerance Matrix
| Dimension | Item Category | Tolerance Threshold | System Enforcement Behavior |
| :--- | :--- | :--- | :--- |
| **Unit Price Variance** | All goods and services | **Strict 0.00%** | Hard block. Any unit price discrepancy requires an approved PO Change Order signed by Procurement Director before payment. |
| **Quantity Variance** | Discrete items (machinery, electronics, finished goods) | **Strict 0.00%** | Hard block on excess quantity. Match and approve invoice up to PO quantity; quarantine excess in unapproved payables. |
| **Quantity Variance** | Bulk commodities (fuels, chemicals, cement, grains) | **Maximum 0.50%** | Automatic pass if within 0.50% loss/expansion limit established in master contract; invoice amount adjusted to actual GRN. |
| **Tax Rate Variance** | All items | **Strict 0.00%** | Hard block. If invoice VAT rate differs from PO tax schedule, reject invoice and require vendor replacement. |

### Exception Remediation Workflows
- **Over-Billing (Price Discrepancy)**:
  - Invoice unit price exceeds PO: Automated block. Alert sent to Buyer and Accounts Payable. Vendor must either issue an adjustment invoice (Hóa đơn điều chỉnh giảm) or procurement must submit an approved contract addendum.
- **Over-Delivery (Quantity Discrepancy)**:
  - Received quantity exceeds PO: Warehouse records actual receipt on GRN. Matching engine matches invoice only up to PO quantity. The excess quantity is held in quarantine inventory (`TK 152 / 156` detail sub-account: `Hàng chờ xử lý`) with matching credit in `TK 3388` (Phải trả khác), not released for production until approved.

---

## 3. Goods Received Not Invoiced (GRNI) Accrual Management

A critical period-end cut-off control occurs when inventory is physically received and accepted at the warehouse, but the vendor e-invoice has not yet been received by the accounting period close.

### Regulatory Cut-Off Mandate (Circular 200/2014/TT-BTC)
To uphold the accrual principle (Cơ sở dồn tích) and matching principle (Nguyên tắc phù hợp), raw materials and merchandise in the warehouse must be recognized in the period they are received, regardless of whether an invoice is present.

### Provisional Accrual Accounting Workflow

#### Step 1: Period Cut-Off Date (Dec 31)
Identify all GRNs created on or before cut-off date lacking a matched vendor invoice.
- **Provisional Journal Entry**:
  - `Debit TK 152` (Raw materials) or `TK 156` (Merchandise)
  - `Credit TK 331` (Accounts Payable - GRNI clearing sub-account)
- **Amount**: Valued at PO contract unit price $\times$ received quantity.
- **CRITICAL TAX RULE**: **DO NOT accrue input VAT (TK 133)** at this step. Input VAT can only be recorded when a valid electronic invoice XML exists.

#### Step 2: Subsequent Period Upon Invoice Arrival (e.g. Jan 08)
When the vendor issues the e-invoice and the XML is validated:
- **Reversal of Provisional Entry**:
  - `Debit TK 152 / 156` (Negative amount / red ink) or `Credit TK 152 / 156`
  - `Credit TK 331` (Negative amount) or `Debit TK 331`
- **Actual Invoice Booking**:
  - `Debit TK 152 / 156`: Actual invoice cost.
  - `Debit TK 133`: Input VAT per verified XML.
  - `Credit TK 331`: Accounts Payable to Vendor.

---

## 4. Goods in Transit (TK 151) Cut-Off Accounting

The inverse cut-off scenario occurs when the vendor has issued the invoice, ownership has transferred to the buyer (e.g., under FOB shipping point or accepted invoice), but physical goods have not arrived at the warehouse by the period close.

### Accounting Treatment under Circular 200 Article 26
1. **At Period Cut-Off Date (Dec 31)**:
   - Invoice received and approved, but warehouse confirms goods not received:
     - `Debit TK 151` (Hàng mua đang đi đường - Goods in transit)
     - `Debit TK 133` (Input VAT deductible per verified invoice)
     - `Credit TK 331` (Accounts Payable) or `Credit TK 112` (Bank Transfer)
   - *Note*: Never debit TK 152 or TK 156 prior to physical inspection and GRN sign-off.
2. **In Subsequent Period Upon Warehouse Delivery**:
   - Physical receipt at warehouse and GRN issued:
     - `Debit TK 152` (Raw materials) or `TK 156` (Merchandise)
     - `Credit TK 151` (Goods in transit cleared)

---

## 5. Decree 132/2020 Associated Enterprise Governance and 30% EBITDA Cap

Under **Decree 132/2020/ND-CP** (Government regulations on tax administration for enterprises with related-party transactions):

### Associated Enterprise Relationship Criteria (Article 5)
Enterprises are deemed related parties (Giao dịch liên kết) if satisfying any of the following criteria:
1. **Equity Holding**: One enterprise directly or indirectly holds **at least 25%** of the owner's equity of the other enterprise.
2. **Substantial Debt and Guarantee**:
   - One enterprise lends to or guarantees the other enterprise, provided the loan amount is **at least 10%** of the borrower's equity AND constitutes **more than 50%** of the borrower's total medium- and long-term debts.
3. **Executive Management Control**: One enterprise appoints more than 50% of the board of directors or executive management of the other enterprise.
4. **Exclusive Supply or Distribution**: One enterprise controls over 50% of purchases or sales of the other enterprise through exclusive contracts.

### 30% EBITDA Net Interest Expense Limitation (Article 16)
For enterprises with related-party transactions, total deductible loan interest expense for Corporate Income Tax (CIT) purposes is capped.

#### A. Mathematical Formula
$$\text{Net Interest Expense} = \text{Total Loan Interest Expense} - \text{Total Deposit & Lending Interest Income}$$

$$\text{EBITDA} = \text{Net Operating Profit} + \text{Net Interest Expense} + \text{Depreciation & Amortization (TK 214 + TK 242)}$$

$$\text{Deductible Interest Cap} = 30\% \times \text{EBITDA}$$

If $\text{Net Interest Expense} > 30\% \times \text{EBITDA}$:
- The excess net interest is **non-deductible** for current year CIT.
- The non-deductible amount must be entered into **Box B4** of CIT Return Form 03/TNDN.

#### B. Negative or Zero EBITDA Rule
Under Decree 132/2020/ND-CP Article 16 Clause 3:
> If EBITDA is zero or negative ($\text{EBITDA} \le 0$), allowable deductible net interest expense is strictly **0 VND**.
- The entire net interest expense for the year is non-deductible in the current period and must be carried forward.

#### C. 5-Year Carry-Forward Register
- Non-deductible net interest expense can be carried forward continuously for a maximum of **05 consecutive years**, starting from the year following the disallowed year.
- In subsequent years, carry-forward interest is deductible up to the limit where:
  $$(\text{Current Net Interest} + \text{Carried-Forward Interest}) \le 30\% \times \text{EBITDA}_{\text{current}}$$
- Any carried-forward interest not utilized within 5 years expires permanently.

#### D. Transfer Pricing Documentation & Safe Harbors
- Enterprises with related-party transactions must prepare:
  - Form 01/ND132: Information on related-party relationships and transactions.
  - Form 02/ND132: Local File.
  - Form 03/ND132: Master File.
  - Form 04/ND132: Country-by-Country Report (CbCR).
- **Safe Harbor Exemption**: Enterprises are exempt from preparing Forms 02, 03, 04 if:
  - Total annual revenue $< 50 \text{ billion VND}$ AND total related-party transaction value $< 30 \text{ billion VND}$.

---

## 6. Immutable Digital Audit Trail and Forensic Controls

Under the Law on Accounting No. 88/2015/QH13 (Articles 13 & 14) and modern cybersecurity standards:

### Write-Once-Read-Many (WORM) Principles
1. **Prohibition of Destructive Mutations**:
   - Direct SQL `UPDATE` or `DELETE` statements on posted journal entries (`so_cai`, `so_nhat_ky_chung`) are programmatically prohibited by database constraints and IAM policies.
   - Any correction of an error in a posted voucher must be executed through:
     - **Reversing voucher (Bút toán đảo / Bút toán ghi số âm)**, or
     - **Supplementary adjustment voucher (Bút toán bổ sung)** with an explicit foreign key reference to the original voucher ID.
2. **Cryptographic Period Snapshotting**:
   - At period close, calculate a SHA-256 Merkle root across all posted vouchers, subledger balances, and trial balances.
   - Store the snapshot digest in tamper-evident storage. Any modification of historical rows invalidates the Merkle root.

### OCSF 99001 Financial Audit Event Logging
All accounting state transitions must emit an Open Cybersecurity Schema Framework (OCSF) Category 9 (Financial & Compliance) audit event:

```json
{
  "class_uid": 99001,
  "class_name": "Financial Ledger Mutation",
  "category_uid": 9,
  "category_name": "Compliance & Audit",
  "activity_id": 1,
  "activity_name": "Post Journal Voucher",
  "time": "2026-09-05T14:38:00Z",
  "actor": {
    "user": {
      "name": "nguyen.van.a",
      "account_id": "ACC-789",
      "role": "vietnam-accounting-specialist"
    }
  },
  "ledger_record": {
    "voucher_id": "PKT-202609-0042",
    "period": "2026-09",
    "debit_account": "1521",
    "credit_account": "3311",
    "amount": 50000000.00,
    "currency": "VND",
    "payload_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  "hitl_approval": {
    "approved_by": "tran.thi.b",
    "role": "chief-accountant",
    "token": "HITL-APPR-99214-SIGN"
  }
}
```

### Segregation of Duties (SoD) & Non-Discretionary HITL Gate
- **Creator vs Approver Separation**: The system enforces that the user ID or agent ID that prepared the journal entry cannot be the approver.
- **Autonomous AI Boundary**: AI agents may perform automated 3-way matching, variance calculations, and draft period closing packages. However, **final period closure and tax return submissions strictly require human digital signatures** from the Chief Accountant (Kế toán trưởng) and Legal Representative (Người đại diện theo pháp luật).

---

## 7. Controls Verification Checklist

- [ ] Deterministic 3-way match asserts 0.00% unit price variance and within-tolerance quantity.
- [ ] GRNI accrual at period cut-off books Debit TK 152/156, Credit TK 331 with zero VAT accrual.
- [ ] Goods in transit at cut-off books Debit TK 151 and Debit TK 133; clears to TK 152/156 on receipt.
- [ ] Related-party relationships identified against Decree 132 Article 5 criteria.
- [ ] Net interest expense capped at 30% EBITDA; negative EBITDA forces 0 VND deduction.
- [ ] Disallowed interest tracked in 5-year carry-forward register.
- [ ] Direct database updates/deletes blocked; reverse-and-repost accounting enforced.
- [ ] OCSF 99001 audit events emitted for all ledger adjustments.
- [ ] Chief Accountant HITL sign-off token verified prior to period lock.
