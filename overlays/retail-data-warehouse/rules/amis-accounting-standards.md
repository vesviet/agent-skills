# MISA AMIS Accounting Standards & Omnichannel Revenue Recognition

Operational standard and statutory accounting compliance rules for synchronizing omnichannel retail data (physical POS, Shopee, TikTok Shop) with MISA AMIS ERP. This rule enforces Vietnamese Accounting Standard 14 (VAS 14), Circular 200/2014/TT-BTC, Circular 133/2016/TT-BTC, strict delivery-time revenue recognition, 3-tier voucher decomposition, separate selling expense classification (TK 641), pretax unit price isolation, and inventory costing controls (TK 1561 / TK 632).

---

## 1. VAS 14 Revenue Recognition Invariant

### 1.1 Statutory Criteria (Circular 200 / VAS 14)
Under Vietnamese Accounting Standard No. 14 (VAS 14 — *Revenue and Other Income*) and Circular 200/2014/TT-BTC (Article 79), revenue from goods sales (`TK 5111` / `TK 5112`) must be recognized if and only if **all five** statutory criteria are satisfied simultaneously:
1. The enterprise has transferred to the buyer the significant risks and rewards of ownership of the goods.
2. The enterprise retains neither continuing managerial involvement to the degree usually associated with ownership nor effective control over the goods sold.
3. The amount of revenue can be measured reliably.
4. It is probable that the economic benefits associated with the transaction will flow to the enterprise.
5. The costs incurred or to be incurred in respect of the transaction can be measured reliably.

### 1.2 The Strict Delivery Confirmation Invariant
In omnichannel e-commerce (Shopee, TikTok Shop, Web POS):
- **Mandatory Recognition Point**: Revenue and corresponding Cost of Goods Sold (COGS) **MUST ONLY BE RECOGNIZED** when an order reaches a terminal, confirmed completion state (`Delivered` / `Completed` / `Hoàn thành`).
- **STRICT PROHIBITION**: It is strictly prohibited to recognize sales revenue for orders currently in transit (`In Transit` / `Shipping` / `Đang vận chuyển`). While in transit, customer refusal, package damage, or delivery failure can occur, meaning risks and rewards of ownership remain with the merchant.

### 1.3 Statutory Journal Entries by Order Lifecycle State

#### Phase 1: Order Pack & Dispatch (In Transit)
Goods leaving the warehouse are transferred to suspense inventory `TK 157` (*Hàng gửi đi bán*). Zero revenue is recognized.
- **Inventory Transfer**:
  - `Debit TK 157` (*Hàng gửi đi bán*): Cost of dispatched goods
  - `Credit TK 1561` (*Giá mua hàng hóa*): Cost of dispatched goods

#### Phase 2: Successful Delivery Confirmation (`Completed`)
Upon customer receipt confirmation via platform webhook or 3PL API:
- **Sales Revenue & Receivables Recognition**:
  - `Debit TK 1388 (Shopee / TikTok Shop)` or `Debit TK 131 (POS Customer)`: Total gross order receivable
  - `Credit TK 5111` (*Doanh thu bán hàng hóa*): Net pretax revenue
  - `Credit TK 33311` (*Thuế GTGT đầu ra*): Output VAT payable
- **COGS Derecognition**:
  - `Debit TK 632` (*Giá vốn hàng bán*): Historical inventory cost
  - `Credit TK 157` (*Hàng gửi đi bán*): Historical inventory cost

#### Phase 3: Delivery Failure / Customer Return (`Returned` / `Cancelled`)
When a shipment fails or is rejected by the customer:
- **Inventory Return**:
  - `Debit TK 1561` (*Giá mua hàng hóa*): Cost of returned goods
  - `Credit TK 157` (*Hàng gửi đi bán*): Cost of returned goods
- Zero revenue and zero COGS entries are recorded. If a customer return occurs post-completion, issue a statutory Sales Return voucher (`TK 5212` / `TK 33311` / `TK 1388`).

---

## 2. 3-Tier E-Commerce Voucher Decomposition

E-commerce platforms (Shopee, TikTok Shop) allow stacking multiple promotional discounts on a single checkout. Aggregating these discounts into a single flat reduction distorts statutory revenue, falsifies receivables, and creates severe tax penalties.

All automated sync pipelines must decompose discounts into three distinct economic tiers:

| Voucher Tier | Economic Sponsor | Accounting Impact | Statutory Recording in MISA AMIS |
|:---|:---|:---|:---|
| **Tier 1: Shop Voucher** | Merchant / Seller | Trade discount reducing merchant revenue | Deducted from `TK 5111` or booked as `Debit TK 5211` (*Chiết khấu thương mại*) |
| **Tier 2: Platform Voucher** | Shopee / TikTok Shop | Platform marketing subsidy; does NOT reduce merchant gross revenue | Included in Gross Sales (`Credit TK 5111` + `Credit TK 33311`); voucher amount booked as receivable `Debit TK 1388` |
| **Tier 3: Shipping Subsidy** | Platform / 3PL | Pass-through logistics subsidy paid directly to carrier | Excluded entirely from merchandise sales (`TK 5111`). If routed through settlement, recorded in clearing `TK 1388 / TK 3388` |

### 2.1 Voucher Decomposition Python Implementation
```python
"""Decompose e-commerce checkout line items into statutory 3-tier accounting buckets."""

from decimal import Decimal, ROUND_HALF_EVEN
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderFinancialDecomposition:
    gross_merchandise_pretax: Decimal
    output_vat: Decimal
    shop_discount_pretax: Decimal
    platform_voucher_receivable: Decimal
    customer_paid_cash: Decimal
    net_sales_revenue: Decimal

def decompose_order_vouchers(
    item_gross_price: Decimal,
    quantity: int,
    vat_rate: Decimal,
    shop_voucher_gross: Decimal,
    platform_voucher_gross: Decimal,
) -> OrderFinancialDecomposition:
    """Calculates statutory accounting buckets under VAS 14.
    
    All gross figures are VAT-inclusive; pretax values are derived deterministically.
    """
    one = Decimal("1.00")
    vat_divisor = one + vat_rate

    # 1. Total gross merchandise value
    total_gross = item_gross_price * Decimal(quantity)
    gross_pretax = (total_gross / vat_divisor).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    # 2. Tier 1: Shop Voucher (Trade discount reducing revenue)
    shop_discount_pretax = (shop_voucher_gross / vat_divisor).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )

    # Statutory Net Pretax Sales Revenue (TK 5111)
    net_sales_pretax = gross_pretax - shop_discount_pretax
    output_vat = (net_sales_pretax * vat_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    # 3. Tier 2: Platform Voucher (Receivable from platform, does not reduce revenue)
    platform_receivable = platform_voucher_gross

    # 4. Customer Cash Settlement (COD or payment gateway)
    customer_cash = (total_gross - shop_voucher_gross - platform_voucher_gross).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )

    return OrderFinancialDecomposition(
        gross_merchandise_pretax=gross_pretax,
        output_vat=output_vat,
        shop_discount_pretax=shop_discount_pretax,
        platform_voucher_receivable=platform_receivable,
        customer_paid_cash=customer_cash,
        net_sales_revenue=net_sales_pretax,
    )
```

---

## 3. Selling Expenses: Platform Fees in TK 641 (No-Netting Mandate)

### 3.1 The Strict Prohibition Against Netting
E-commerce platforms deduct transaction fees, commission fees, payment processing fees, and affiliate fees directly from the merchant's payout balance.
- **NO NETTING RULE**: Under Circular 200/2014/TT-BTC (Article 79) and tax regulations issued by the General Department of Taxation, **expenses must never be netted against gross revenue**.
- Netting platform fees against sales revenue artificially deflates statutory turnover, distorts audited gross profit margins, and violates corporate income tax (CIT) and value-added tax (VAT) reporting requirements.

### 3.2 Standard Statutory Journal Entries for Platform Settlement

```text
1. Recognizing Sales & Platform Receivables upon Delivery:
   Debit TK 1388 (Chi tiết: Sàn TMĐT Shopee/TikTok):     1,100,000 VND
       Credit TK 5111 (Doanh thu bán lẻ):                 1,000,000 VND
       Credit TK 33311 (Thuế GTGT đầu ra 10%):              100,000 VND

2. Recording Platform Service Fees (Based on Platform E-Invoice):
   Debit TK 6417 / TK 6418 (Chi phí dịch vụ bán hàng sàn):   50,000 VND
   Debit TK 1331 (Thuế GTGT đầu vào được khấu trừ 10%):       5,000 VND
       Credit TK 1388 (Cấn trừ công nợ sàn):                 55,000 VND

3. Bank Cash Payout Receipt (Net Remittance from Platform):
   Debit TK 1121 (Tiền gửi ngân hàng):                  1,045,000 VND
       Credit TK 1388 (Thu hồi dứt điểm công nợ sàn):    1,045,000 VND
```

---

## 4. Pretax Unit Price Isolation (Double VAT Prevention on MISA AMIS)

### 4.1 Root Cause of Double VAT Distortion
MISA AMIS ERP calculates sales VAT automatically using the line item formula:
$$\text{VAT Amount} = \text{UnitPrice} \times \text{Quantity} \times \text{VAT Rate}$$

In consumer retail (Shopee, TikTok Shop, POS counters), all displayed prices and customer payments are **VAT-inclusive (Gross)**.
- If an integration pipeline directly inputs `Price_gross` into MISA AMIS's `UnitPrice` field, MISA AMIS applies the tax rate a second time.
- *Example Disaster*: For a product sold at $110,000\text{ VND}$ (inclusive of $10\%$ VAT, true pretax = $100,000\text{ VND}$, true VAT = $10,000\text{ VND}$):
  - If $110,000$ is posted as `UnitPrice`: MISA AMIS computes $\text{VAT} = 11,000\text{ VND}$, resulting in total voucher amount $= 121,000\text{ VND}$!
  - This creates false tax liabilities, overstates customer invoices, and causes audit rejection.

### 4.2 Mandatory Pretax Formula & Banker's Rounding
The pretax unit price must be isolated prior to generating MISA AMIS voucher XML/JSON payloads:
$$\text{UnitPrice}_{\text{pretax}} = \frac{\text{UnitPrice}_{\text{gross}}}{1 + \text{VAT\_Rate}}$$

#### Rounding & Reconciliation Invariant:
1. Maintain unit prices with 4 decimal places during intermediate transformations.
2. Apply Banker's Rounding (`ROUND_HALF_EVEN`) to 2 decimal places (or integer VND) for line items.
3. Validate invoice reconciliation before submission to MISA AMIS:
   $$\left|\sum (\text{Line Pretax Amounts}) + \sum (\text{Line VAT}) - \text{Total Customer Paid}\right| = 0$$

---

## 5. Inventory Accounting: TK 1561 / TK 632

### 5.1 Costing Methods & Ledger Parity
- All retail inventory must be maintained under **TK 1561** (*Giá mua hàng hóa*) using either **Monthly Weighted Average** (*Bình quân gia quyền*) or **FIFO** (*Nhập trước xuất trước*).
- Every sales dispatch voucher synced to MISA AMIS must generate a paired inventory delivery note (*Phiếu xuất kho kiêm bán hàng*):
  - `Debit TK 632` (*Giá vốn hàng bán*)
  - `Credit TK 1561` (*Giá mua hàng hóa*)

### 5.2 Warehouse Code & SKU Mapping Standards
- MISA AMIS requires explicit warehouse codes (`StockCode`, e.g., `KHO_TONG`, `KHO_STORE_01`, `KHO_SHOPEE`).
- SKU codes must match between the Lakehouse Silver catalog and MISA AMIS inventory master data (`InventoryItemCode`). Unmapped SKUs must be routed to a quarantine reconciliation queue rather than posting to a generic placeholder.

---

## 6. MISA AMIS Sync Payload Schema Mapping

All outgoing vouchers to MISA AMIS must adhere to the structured schema defined in `core/contracts/schemas/amis-voucher-contract.json`:

```json
{
  "voucher_type": "delivery_note_cum_sales_invoice",
  "voucher_date": "2026-09-05",
  "posting_date": "2026-09-05",
  "channel": "shopee",
  "order_sn": "260905SHOPEE9981",
  "currency": "VND",
  "exchange_rate": 1.0,
  "customer_code": "CUST_SHOPEE_RETAIL",
  "customer_name": "Khách lẻ Shopee",
  "journal_entries": [
    {
      "debit_account": "1388",
      "credit_account": "5111",
      "amount": 250000.0,
      "description": "Doanh thu bán hàng đơn 260905SHOPEE9981"
    },
    {
      "debit_account": "1388",
      "credit_account": "33311",
      "amount": 25000.0,
      "description": "Thuế GTGT đầu ra 10% đơn 260905SHOPEE9981"
    },
    {
      "debit_account": "632",
      "credit_account": "1561",
      "amount": 160000.0,
      "description": "Giá vốn hàng bán đơn 260905SHOPEE9981"
    }
  ],
  "line_items": [
    {
      "inventory_item_code": "SKU-POLO-NAVY-M",
      "stock_code": "KHO_SHOPEE",
      "quantity": 1,
      "unit_price_pretax": 250000.0,
      "vat_rate": 0.10,
      "vat_amount": 25000.0,
      "cogs_amount": 160000.0
    }
  ]
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
  See `core/skills/security-data/manage-vietnam-accounting/SKILL.md` and the `amis-voucher-contract.json` schema.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/security-data/manage-vietnam-accounting/SKILL.md` and the `amis-voucher-contract.json` schema.

Last updated: 2026-09-05
