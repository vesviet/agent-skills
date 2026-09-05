# Vietnam Accounting Standards (VAS) & VFRS Chart of Accounts Governance

## 1. Vietnamese Accounting Regimes Landscape

Vietnamese corporate accounting is governed by statutory accounting regimes promulgated by the Ministry of Finance (MoF). Selecting and maintaining the correct accounting regime is a mandatory legal invariant under the Law on Accounting No. 88/2015/QH13.

### Accounting Regimes Comparison
| Feature | Circular 200/2014/TT-BTC | Circular 133/2016/TT-BTC | Circular 132/2018/TT-BTC |
| :--- | :--- | :--- | :--- |
| **Target Entities** | Large and medium enterprises, listed corporations, public interest entities | Small and Medium Enterprises (SMEs) | Micro-enterprises (Doanh nghiệp siêu nhỏ) |
| **Account Code Structure** | Standard 4-digit accounts (e.g., TK 1111, 1121, 6421) | Simplified 3-digit accounts (e.g., TK 111, 112, 642) | Ultra-simplified 3-digit accounts |
| **Cost Gathering Method** | Multi-account cost gathering (TK 621, 622, 623, 627) | Single-account pooling (TK 154 only) | Direct expense recognition or simplified TK 154 |
| **Selling Expense Account** | Separate Account: TK 641 | Sub-account: TK 6421 | Gathered into general expenses |
| **Statutory Financial Statements** | B01-DN, B02-DN, B03-DN, B09-DN | B01a-DNN / B01b-DNN, B02-DNN, B09-DNN | Optional simplified B01-DNSN or tax-only records |
| **Policy Consistency Requirement** | Fiscal year consistency; changes must be reported in B09 | Fiscal year consistency; changes must be reported in B09 | Annual consistency |

### Forbidden SME Accounts under Circular 133
Circular 133/2016/TT-BTC explicitly prohibits the use of specific cost accounts that exist under Circular 200. Accounting engines and ERP systems must enforce these structural barriers:

1. **Manufacturing Cost Accounts**:
   - `TK 621` (Chi phí nguyên liệu, vật liệu trực tiếp): **FORBIDDEN under TT 133**.
   - `TK 622` (Chi phí nhân công trực tiếp): **FORBIDDEN under TT 133**.
   - `TK 623` (Chi phí sử dụng máy thi công): **FORBIDDEN under TT 133**.
   - `TK 627` (Chi phí sản xuất chung): **FORBIDDEN under TT 133**.
   - *Statutory Rule*: Under Circular 133, all direct raw materials, direct labor, machinery, and production overhead must be recorded directly into **`TK 154` (Chi phí sản xuất, kinh doanh dở dang)** using distinct detail tracking codes (e.g., `TK 1541`, `1542`, `1543`).
2. **Selling Expense Account**:
   - `TK 641` (Chi phí bán hàng): **FORBIDDEN under TT 133**.
   - *Statutory Rule*: Selling expenses must be posted to **`TK 6421` (Chi phí bán hàng)** within general administrative account `TK 642`. Management administrative costs are recorded in **`TK 6422` (Chi phí quản lý doanh nghiệp)**.

---

## 2. Decision 345/QD-BTC VFRS Transition Dual-Reporting Layer

Decision 345/QD-BTC approves the national roadmap for applying International Financial Reporting Standards (IFRS) in Vietnam, establishing Vietnam Financial Reporting Standards (VFRS).

```
+-------------------------------------------------------------------------+
|                  Enterprise Transaction / Ledger Event                  |
+-------------------------------------------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                                                                         |
| Layer 1: Statutory VAS (Circular 200)                                   |
| - Historical cost convention                                            |
| - Off-balance operating leases                                          |
| - Circular 48 aging-bracket bad debt provisions                         |
| - Legal tax basis for CIT return (Form 03/TNDN)                         |
|                                                                         |
+-------------------------------------------------------------------------+
                                     |
                                     v Deterministic Bridge & Adjustments
+-------------------------------------------------------------------------+
| Layer 2: VFRS / IFRS Reconciliation Layer                               |
| - IFRS 16: Right-of-Use Asset & Lease Liability                         |
| - IFRS 9: Forward-looking Expected Credit Loss (ECL)                    |
| - IFRS 15: 5-Step Revenue Recognition & Contract Assets/Liabilities     |
| - Fair value measurements & Deferred Tax adjustments                    |
+-------------------------------------------------------------------------+
```

### Key Standard Divergences & Deterministic Adjustments

#### A. Lease Accounting (IFRS 16 vs VAS 06)
- **Statutory VAS (Circular 200)**:
  - Operating leases are expensed on a straight-line basis to profit and loss:
    - `Debit TK 642 / 641`: Monthly rental expense.
    - `Credit TK 112 / 331`: Bank payment or vendor payable.
  - No asset or liability is recognized on the balance sheet.
- **VFRS / IFRS 16 Adjustment**:
  - Capitalize all leases with duration > 12 months:
    1. Calculate initial **Right-of-Use (ROU) Asset** and **Lease Liability** as the present value of future lease payments discounted at the incremental borrowing rate.
    2. Post adjustment entry:
       - `Debit ROU_Asset`
       - `Credit Lease_Liability`
    3. Monthly adjustment entries:
       - `Debit ROU_Amortization_Expense` / `Credit Accumulated_ROU_Amortization`
       - `Debit Interest_Expense` / `Credit Lease_Liability`
       - Reverse statutory VAS rental expense: `Credit Operating_Lease_Expense`

#### B. Financial Instruments & Expected Credit Loss (IFRS 9 vs Circular 48/2019)
- **Statutory VAS (Circular 48/2019/TT-BTC)**:
  - Provision for doubtful debts is strictly rule-based according to invoice overdue aging brackets:
    - Overdue 6 months to under 1 year: **30%** provision.
    - Overdue 1 year to under 2 years: **50%** provision.
    - Overdue 2 years to under 3 years: **70%** provision.
    - Overdue 3 years or more: **100%** provision.
  - Journal entry: `Debit TK 642` / `Credit TK 2293` (Dự phòng phải thu khó đòi).
- **VFRS / IFRS 9 Adjustment**:
  - Forward-looking Expected Credit Loss (ECL) model:
    - $ECL = PD \times LGD \times EAD$
    - Provision is recognized at Day 1 (12-month ECL) and transitions to Lifetime ECL upon significant increase in credit risk (SICR).
  - Adjustment entry posts delta between VAS Circular 48 provision and IFRS 9 ECL calculation.

#### C. Revenue Recognition (IFRS 15 vs VAS 14)
- **Statutory VAS (VAS 14 & Circular 200)**:
  - Revenue recognized upon transfer of significant risks and rewards of ownership, reliable measurement, and economic benefits probable. Frequently bound to statutory invoice issuance date.
- **VFRS / IFRS 15 Adjustment**:
  - Enforce the 5-Step Model:
    1. Identify the contract with a customer.
    2. Identify distinct performance obligations (PBOs).
    3. Determine the transaction price (including variable consideration).
    4. Allocate transaction price to performance obligations based on relative standalone selling prices (SSP).
    5. Recognize revenue when/as each performance obligation is satisfied over time or at a point in time.
  - Reclassify unfulfilled obligations to Contract Liabilities and earned unbilled revenue to Contract Assets.

---

## 3. Circular 96/2015 36-Month Legal Ceiling on Prepaid Expenses (TK 242)

Prepaid expenses represent expenditures incurred that benefit operating results across multiple accounting periods.

### Statutory Ceiling Mandate
Under **Circular 96/2015/TT-BTC** (Article 4, amending Circular 78/2014/TT-BTC Article 6):
> "For purchases of tools, equipment, office leases, and repair costs of fixed assets that do not satisfy the criteria for fixed asset recognition, expenditures must be allocated into business costs over a duration **not exceeding 36 months**."

### Operational Accounting Rules for TK 242
1. **Initial Recognition**:
   - `Debit TK 242` (Chi phí trả trước): Historical cost exclusive of VAT.
   - `Debit TK 1331`: Deductible input VAT (evidenced by verified XML e-invoice).
   - `Credit TK 112 / 331`: Payment or vendor liability.
2. **Monthly Straight-Line Allocation**:
   - Monthly amortization formula:
     $$\text{Monthly Allocation} = \frac{\text{Historical Cost}}{\text{Total Allocation Months}} \quad (\text{where } \text{Total Allocation Months} \le 36)$$
   - Allocation journal entry:
     - `Debit TK 642` (Administrative expenses) or `Debit TK 641` (Selling expenses) or `Debit TK 154` (Production costs).
     - `Credit TK 242` (Prepaid expenses).
3. **Book-Tax Differences on TK 242**:
   - **Internal Amortization > 36 Months**: If an enterprise amortizes office renovations over 60 months for management purposes, the tax authority strictly enforces the 36-month cap. Amortization expenses recorded in months 37–60 will be permanently disallowed for CIT deductions.
   - **Lump-Sum Write-Off Violation**: Expensing large prepaid tool or renovation costs (e.g., > 100M VND) in a single month violates the matching principle and will be challenged during tax audits.

---

## 4. Circular 45/2013 Fixed Asset Useful Life Depreciation Brackets (TK 214)

Under **Circular 45/2013/TT-BTC** (amended by Circular 147/2016/TT-BTC and Circular 28/2017/TT-BTC), tangible fixed assets must satisfy three concurrent conditions:
1. Future economic benefits are certain.
2. Useful life is estimated at **more than 01 year**.
3. Original historical cost is **30,000,000 VND or higher**.

### Statutory Useful Life Brackets (Circular 45 Appendix I)
Depreciation must be calculated within the minimum and maximum useful life brackets prescribed by the Ministry of Finance:

| Asset Class | Vietnamese Description | Statutory Useful Life Bracket |
| :--- | :--- | :--- |
| **Class A: Buildings & Structures** | Nhà cửa, vật kiến trúc | **10 to 50 years** (Industrial plants: 10–30 yrs; offices: 20–50 yrs) |
| **Class B: Machinery & Equipment** | Máy móc, thiết bị động lực | **3 to 20 years** (Manufacturing machines: 5–15 yrs) |
| **Class C: Transmission Equipment** | Phương tiện truyền dẫn | **4 to 10 years** (Power lines, pipelines, communications) |
| **Class D: Transport Equipment** | Thiết bị, phương tiện vận tải | **6 to 10 years** (Automobiles, trucks: 6–10 yrs) |
| **Class E: Office & IT Equipment** | Dụng cụ quản lý, máy vi tính | **3 to 8 years** (Laptops, servers, printers: 3–5 yrs) |
| **Class F: Intangible Assets** | Tài sản vô hình (phần mềm) | **2 to 20 years** (ERP software: 3–8 yrs; patents: legal duration) |

### Permitted Depreciation Methods
1. **Straight-Line Method (Khấu hao theo đường thẳng)**: Standard default method. Annual depreciation is uniform across the asset's registered useful life.
2. **Declining-Balance with Adjustment (Khấu hao theo số dư giảm dần có điều chỉnh)**: Permitted only for newly acquired machinery and equipment in high-tech or rapid technological innovation industries.
3. **Units-of-Production Method (Khấu hao theo sản lượng)**: Permitted when designed production capacity is established and annual production is predictable.

### Depreciation Allocation Entries (TK 214)
- Production equipment: `Debit TK 154` (TT 133) or `Debit TK 627` (TT 200) / `Credit TK 2141`.
- Selling vehicles/facilities: `Debit TK 6421` (TT 133) or `Debit TK 641` (TT 200) / `Credit TK 2141`.
- Head office & executive assets: `Debit TK 6422` (TT 133) or `Debit TK 642` (TT 200) / `Credit TK 2141`.

### Tax Non-Deductibility Threshold for Passenger Cars
Under Circular 96/2015/TT-BTC: For passenger cars with 9 seats or fewer (excluding cars used for commercial passenger transport, tourism, or hotel operations), depreciation corresponding to the portion of original historical cost exceeding **1,600,000,000 VND** (exclusive of VAT) is **non-deductible for CIT**.
- Annual excess depreciation must be tracked in the tax workpaper and added to taxable income via Box B4 on Form 03/TNDN.

---

## 5. Chart of Accounts Crosswalk and Structural Rules

When transitioning or consolidating ledgers between Circular 200, Circular 133, and VFRS dual reporting, apply the following canonical crosswalk:

| Transaction Nature | Circular 200 Account | Circular 133 Account | VFRS Dual Layer Equivalent |
| :--- | :--- | :--- | :--- |
| Direct Raw Materials | `TK 621` | `TK 154 (Sub 1541)` | `COGS / WIP Inventory` |
| Direct Labor Cost | `TK 622` | `TK 154 (Sub 1542)` | `COGS / WIP Inventory` |
| Manufacturing Overhead | `TK 627` | `TK 154 (Sub 1543)` | `COGS / WIP Inventory` |
| Selling Expenses | `TK 641` | `TK 6421` | `Operating Expenses (Selling)` |
| General Administration | `TK 642` | `TK 6422` | `Operating Expenses (Admin)` |
| Long-Term Leases | Off-balance (`TK 001`) | Off-balance (`TK 001`) | `ROU Asset / Lease Liability` |
| Doubtful Debt Provision | `TK 2293` (Age-based) | `TK 2293` (Age-based) | `ECL Allowance (IFRS 9)` |
| Prepaid Allocation (<=36m) | `TK 242` | `TK 242` | `Prepayments / Other Assets` |
| Fixed Asset Depreciation | `TK 214` | `TK 214` | `Accumulated Depreciation` |
| Cost of Goods Sold | `TK 632` | `TK 632` | `Cost of Sales` |
| Financial Income | `TK 515` | `TK 515` | `Finance Income` |
| Financial Expenses | `TK 635` | `TK 635` | `Finance Costs` |
| Period Profit Clearing | `TK 911` | `TK 911` | `Retained Earnings Clearing` |

---

## 6. Regulatory Verification and Audit Checklist

- [ ] Legal entity size, ownership structure, and confirmed accounting regime documented.
- [ ] Circular 133 validation asserts absence of TK 621, 622, 623, 627, and 641.
- [ ] VFRS adjustment schedules maintained independently without altering statutory VAS general ledger.
- [ ] Prepaid expense master register asserts all amortizations under TK 242 $\le$ 36 months.
- [ ] Fixed asset register verifies registered useful life falls within Circular 45 Appendix I brackets.
- [ ] Passenger vehicle depreciation over 1.6 billion VND threshold properly segregated for CIT Box B4.
- [ ] Subledgers for TK 242 and TK 214 reconcile mathematically to General Ledger control accounts.
