# Physical Stocktake & Tolerance Governance

Operational standard and mathematical tolerance engine for store physical stocktakes, offline hardware barcode scanning, blind recount protocols, multi-tier approval workflows, and discrepancy accounting (TK 1381 / TK 3381) under Circular 200/2014/TT-BTC.

---

## 1. Store Hardware Architecture & Offline Scanning

Physical inventory stocktakes frequently occur in warehouse environments or store corners with intermittent Wi-Fi, dead zones, or high radio interference. The architecture must guarantee zero data loss, sub-millisecond barcode capture, and offline-first persistence.

```text
┌─────────────────────────────────────────────────────────┐
│ Store Client: Vanilla JS Offline PWA                     │
│ ┌──────────────────────┐      ┌──────────────────────┐  │
│ │ Hardware HID Scanner │ ───> │ Fast Keypress Buffer │  │
│ │ (USB / Bluetooth)    │      │ (<30ms burst detect) │  │
│ └──────────────────────┘      └──────────┬───────────┘  │
│                                          ▼              │
│ ┌────────────────────────────────────────────────────┐  │
│ │ Browser IndexedDB (Local Queue & Scanned Count)    │  │
│ └────────────────────────────────┬───────────────────┘  │
└──────────────────────────────────┼──────────────────────┘
                                   │ Service Worker Sync
                                   ▼ (Network Restored / LAN)
┌─────────────────────────────────────────────────────────┐
│ Store Edge Server: SQLite WAL Buffer                    │
│ - Instant non-blocking append (<2ms)                    │
│ - Idempotent scan deduplication by (session_id, scan_id)│
└─────────────────────────────────────────────────────────┘
```

### 1.1 Hardware HID Keyboard Wedge Protocol
Barcode scanners operate in **HID (Human Interface Device) Keyboard Wedge Mode**, firing keyboard events in micro-second bursts terminated by an `Enter` keystroke.

The Vanilla JS client intercepts rapid keypress bursts while rejecting manual keyboard typing:

```javascript
/**
 * Zero-dependency HID Barcode Scanner Listener for Vanilla JS PWA
 */
class BarcodeScannerListener {
  constructor(onBarcodeScanned) {
    this.buffer = '';
    this.lastCharTime = 0;
    this.burstThresholdMs = 35; // Maximum interval between characters from hardware scanners
    this.onBarcodeScanned = onBarcodeScanned;
    this.bindEvents();
  }

  bindEvents() {
    window.addEventListener('keydown', (event) => {
      const now = performance.now();
      const interval = now - this.lastCharTime;
      this.lastCharTime = now;

      if (event.key === 'Enter') {
        if (this.buffer.length >= 6) {
          event.preventDefault();
          this.processBarcode(this.buffer);
        }
        this.buffer = '';
        return;
      }

      // If characters arrive too slowly (>35ms), it is human typing, so reset
      if (interval > this.burstThresholdMs && this.buffer.length > 0) {
        this.buffer = '';
      }

      // Collect printable characters
      if (event.key.length === 1) {
        this.buffer += event.key;
      }
    });
  }

  async processBarcode(rawBarcode) {
    const cleanBarcode = rawBarcode.trim();
    // Validate barcode format (EAN-13 or Code-128)
    if (!/^[A-Za-z0-9\-_]{6,32}$/.test(cleanBarcode)) {
      console.warn('Invalid barcode format rejected:', cleanBarcode);
      return;
    }
    await this.onBarcodeScanned(cleanBarcode);
  }
}
```

---

## 2. Mathematical Variance & Tolerance Engine

For each SKU $i$ within an active stocktake session:

### 2.1 Variance Formulas
1. **Quantity Variance ($\Delta Q_i$)**:
   $$\Delta Q_i = Q_{i,\text{actual}} - Q_{i,\text{system}}$$
   - If $\Delta Q_i < 0$: Inventory Shortage (Hàng thiếu)
   - If $\Delta Q_i > 0$: Inventory Surplus (Hàng thừa)
   - If $\Delta Q_i = 0$: Absolute Match

2. **Absolute Quantity Variance Rate ($\text{VarRate}_{Q,i}$)**:
   $$\text{VarRate}_{Q,i} = \begin{cases} \frac{|\Delta Q_i|}{Q_{i,\text{system}}} \times 100\% & \text{if } Q_{i,\text{system}} > 0 \\ 100\% & \text{if } Q_{i,\text{system}} = 0 \text{ and } Q_{i,\text{actual}} > 0 \\ 0\% & \text{if } Q_{i,\text{system}} = 0 \text{ and } Q_{i,\text{actual}} = 0 \end{cases}$$

3. **Monetary Value Variance ($\Delta V_i$)**:
   $$\Delta V_i = \Delta Q_i \times \text{CostPrice}_i$$
   $$\text{AbsValueVariance}_i = |\Delta Q_i| \times \text{CostPrice}_i$$

4. **Store Session Absolute Value Variance Rate ($\text{VarRate}_{V,\text{total}}$)**:
   $$\text{VarRate}_{V,\text{total}} = \frac{\sum_{i=1}^{N} |\Delta Q_i| \times \text{CostPrice}_i}{\sum_{i=1}^{N} (Q_{i,\text{system}} \times \text{CostPrice}_i)} \times 100\%$$

---

## 3. Blind Recount Trigger Thresholds

### 3.1 The Anti-Anchoring Recount Protocol
Confirmation bias is the primary cause of stocktake fraud and erroneous reconciliations in retail. If counters know the system theoretical stock or know that another counter reported 4 units, they tend to stop counting early ("anchoring effect").

**The Blind Recount Mandate**:
- When a blind recount is triggered for SKU $i$, the recount auditor's device displays **ONLY** the SKU Master Metadata (Barcode, SKU Code, Item Name, Location/Bin).
- The auditor's interface **STRICTLY HIDES**:
  1. The theoretical system stock ($Q_{i,\text{system}}$).
  2. The initial counted quantity ($Q_{i,\text{actual}}$ from Counter 1).
  3. The monetary variance value.
- The recount must be conducted by an independent counter or store auditor who did not perform the first scan.

### 3.2 Quantitative Trigger Thresholds

| Trigger Tier | SKU Scope / Condition | Tolerance Threshold | Mandatory Action |
|:---|:---|:---|:---|
| **Threshold A: High-Value / High-Risk SKUs** | Unit cost $\text{CostPrice}_i \ge 1,000,000\text{ VND}$ or serialized electronics / luxury | **Zero Tolerance ($0$)** | Any difference $|\Delta Q_i| \ge 1$ unit immediately locks the SKU and triggers a mandatory Blind Recount. |
| **Threshold B: Standard Retail SKUs** | Unit cost $\text{CostPrice}_i < 1,000,000\text{ VND}$ (FMCG, Apparel, Accessories) | $\text{VarRate}_{Q,i} > 2.0\%$ **OR** $|\Delta V_i| > 500,000\text{ VND}$ | Automatically flagged for Blind Recount before session review can proceed. |
| **Threshold C: Store Session Global Variance** | Total store audit session across all catalog SKUs | $\text{VarRate}_{V,\text{total}} > 0.5\%$ | Entire session is blocked from closure; escalates to Internal Audit for storewide recount sampling. |

---

## 4. Multi-Tier Approval Workflow

A stocktake session transitions through explicit lifecycle states:
$$\text{draft} \longrightarrow \text{in\_progress} \longrightarrow \text{review} \overset{\text{recount triggered}}{\underset{\text{recount resolved}}{\rightleftharpoons}} \text{recount} \longrightarrow \text{closed}$$

```text
[ draft ]
    │
    ▼ (Initiated by Shift Leader)
[ in_progress ]  <─── Hardware barcode scanning (PWA / IndexedDB)
    │
    ▼ (Counting Completed)
[ review ] ────── (Threshold A/B/C Breached) ─────> [ recount ]
    │                                                   │
    │ <──────── (Independent Blind Recount Passed) ─────┘
    │
    ├─► Net Variance < 5,000,000 VND: Approved by Store Manager
    │
    └─► Net Variance >= 5,000,000 VND or Threshold A Breach:
        Escalated to Inventory Control Director (HITL Sign-off)
            │
            ▼
        [ closed ] ───> Automatic Posting to MISA AMIS (TK 1381 / TK 3381)
```

### 4.1 Tiered Authority Matrix
- **Tier 1: Store Auditor / Shift Leader**: Initiates session, assigns store bin zones, conducts barcode scanning, locks scan input, submits session to review (`in_progress` $\rightarrow$ `review`).
- **Tier 2: Store Manager / Chief Accountant**: Evaluates variance report. Dispatches blind recount tasks (`review` $\rightarrow$ `recount`). Has signing authority to close sessions if and only if:
  - Total absolute value variance $\sum |\Delta V_i| < 5,000,000\text{ VND}$.
  - Zero unresolved Threshold A (high-value) discrepancies exist.
- **Tier 3: Inventory Control Director / Internal Audit**: Mandatory Human-In-The-Loop (HITL) cryptographic approval for any session where total absolute variance $\ge 5,000,000\text{ VND}$ or where a Threshold A SKU variance was confirmed.

---

## 5. Discrepancy Accounting (Circular 200/2014/TT-BTC)

Once a stocktake session reaches the `closed` state, all physical-to-book variances must be formally booked to statutory suspense accounts in MISA AMIS ERP:

### 5.1 Inventory Shortage (*Hàng thiếu chờ xử lý*)
When physical count is lower than book inventory ($Q_{\text{actual}} < Q_{\text{system}}$):
1. **Initial Suspense Entry upon Session Closure**:
   - `Debit TK 1381` (*Tài sản thiếu chờ xử lý*): Total shortage value $\sum |\Delta V_{\text{shortage}}|$
   - `Credit TK 1561` (*Giá mua hàng hóa*): Total shortage value $\sum |\Delta V_{\text{shortage}}|$
2. **Post-Investigation Resolution Entries**:
   - **Case A (Individual Employee Liability)**: Deducted from wages or collected in cash:
     - `Debit TK 334` (*Phải trả người lao động*) or `Debit TK 1388` (*Phải thu khác*)
     - `Credit TK 1381` (*Tài sản thiếu chờ xử lý*)
   - **Case B (Insurance Indemnity)**:
     - `Debit TK 1121` (*Tiền gửi ngân hàng*) or `Debit TK 1388` (*Phải thu công ty bảo hiểm*)
     - `Credit TK 1381`
   - **Case C (Unavoidable Operational Shrinkage within Approved Norm)**:
     - `Debit TK 632` (*Giá vốn hàng bán* — Chi phí hao hụt định mức)
     - `Credit TK 1381`

### 5.2 Inventory Surplus (*Hàng thừa chờ xử lý*)
When physical count exceeds book inventory ($Q_{\text{actual}} > Q_{\text{system}}$):
1. **Initial Suspense Entry upon Session Closure**:
   - `Debit TK 1561` (*Giá mua hàng hóa*): Total surplus value $\sum \Delta V_{\text{surplus}}$
   - `Credit TK 3381` (*Tài sản thừa chờ xử lý*): Total surplus value $\sum \Delta V_{\text{surplus}}$
2. **Post-Investigation Resolution Entries**:
   - **Case A (Supplier Shipment Overage)**: Formalized into purchase invoice:
     - `Debit TK 3381` (*Tài sản thừa chờ xử lý*)
     - `Credit TK 331` (*Phải trả người bán*)
   - **Case B (Unidentified Cause / System Timing Difference)**: Recognized as other corporate income:
     - `Debit TK 3381` (*Tài sản thừa chờ xử lý*)
     - `Credit TK 711` (*Thu nhập khác*)

---

## 6. Output Contract Schema Mapping

Stock audit sessions, scan logs, and closure approvals are structured according to `core/contracts/schemas/stock-audit-session.json`:

```json
{
  "session_id": "AUDIT-20260905-HN01",
  "store_id": "STORE_HANOI_01",
  "audit_date": "2026-09-05",
  "status": "closed",
  "metrics": {
    "total_skus_counted": 450,
    "total_system_quantity": 3200,
    "total_actual_quantity": 3192,
    "quantity_variance": -8,
    "total_system_value_vnd": 640000000.0,
    "total_actual_value_vnd": 637800000.0,
    "absolute_value_variance_vnd": 2200000.0,
    "session_variance_rate_pct": 0.34
  },
  "recount_triggered": true,
  "recount_skus": ["SKU-JACKET-BLK-L"],
  "approvals": [
    {
      "tier": "tier_2_store_manager",
      "approver_id": "MGR_042",
      "approved_at": "2026-09-05T21:30:00Z",
      "digital_signature": "sig_mgr_98f12a"
    }
  ],
  "accounting_posted": {
    "voucher_shortage_id": "PK1381_20260905_01",
    "voucher_surplus_id": null
  }
}
```

---

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `core/skills/security-data/manage-vietnam-accounting/SKILL.md` and the `stock-audit-session.json` schema.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/security-data/manage-vietnam-accounting/SKILL.md` and the `stock-audit-session.json` schema.

Last updated: 2026-09-05
