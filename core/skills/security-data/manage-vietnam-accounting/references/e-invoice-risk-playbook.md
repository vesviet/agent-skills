# Vietnam E-Invoice Compliance & Risk Management Playbook

## 1. Regulatory Framework and Legal Authorities

This playbook establishes the operational and automated control standards for electronic invoice (e-invoice / Hóa đơn điện tử) processing, cryptographic signature validation, tax status verification, and audit readiness under Vietnamese law.

### Governing Regulations
- **Decree 123/2020/ND-CP** (Government): Regulations on invoices, records, and e-invoice mandates.
- **Circular 78/2021/TT-BTC** (Ministry of Finance): Guidelines on the implementation of Decree 123/2020/ND-CP.
- **Decision 1450/QD-TCT** (General Department of Taxation - GDT): Technical standard on data format and XML component schemas for electronic invoices.
- **Decision 1510/QD-TCT** (GDT): Amendments and updates to technical specifications and data formats.
- **Law on Tax Administration No. 38/2019/QH14**: Tax registration, invoice obligations, and sanctions for fraudulent invoice usage.
- **Circular 219/2013/TT-BTC & Circular 96/2015/TT-BTC**: Non-cash payment verification rules for Value Added Tax (VAT) deduction and Corporate Income Tax (CIT) expense deductibility.

---

## 2. E-Invoice Architecture and XML Data Component Schema

Under Decision 1450/QD-TCT, all valid electronic invoices in Vietnam must be structured as XML documents with UTF-8 encoding. The canonical XML tree structure consists of:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<HDon>
  <DLHDon Id="data_payload_id">
    <TTChung>
      <PBan>2.0.0</PBan>
      <THDon>Hóa đơn giá trị gia tăng</THDon>
      <KHMSHDon>1</KHMSHDon>
      <KHHDon>C26TAA</KHHDon>
      <SHDon>00000123</SHDon>
      <NLap>2026-09-05</NLap>
      <DVTTe>VND</DVTTe>
      <TGia>1.0</TGia>
      <HTTToan>TM/CK</HTTToan>
    </TTChung>
    <NDHDon>
      <NBan>
        <Ten>CÔNG TY TNHH NHÀ CUNG CẤP TIÊU BIỂU</Ten>
        <MST>0101234567</MST>
        <DChi>Số 1 Phố Tài Chính, Quận Hoàn Kiếm, Hà Nội</DChi>
        <STKNHang>0011001234567</STKNHang>
        <TNHang>Vietcombank - Sở Giao Dịch</TNHang>
      </NBan>
      <NMua>
        <Ten>CÔNG TY CỔ PHẦN DOANH NGHIỆP MUA HÀNG</Ten>
        <MST>0309876543</MST>
        <DChi>Số 88 Đường Công Nghệ, Quận 1, TP. Hồ Chí Minh</DChi>
      </NMua>
      <DSHHDVu>
        <HHDVu>
          <STT>1</STT>
          <THHDVu>Dịch vụ tư vấn giải pháp phần mềm quản trị</THHDVu>
          <DVT>Gói</DVT>
          <SLuong>1</SLuong>
          <DGia>50000000</DGia>
          <Tien>50000000</Tien>
          <TSuat>10%</TSuat>
        </HHDVu>
      </DSHHDVu>
      <TToan>
        <TgTCThue>50000000</TgTCThue>
        <TgTThue>5000000</TgTThue>
        <TgTTTBSo>55000000</TgTTTBSo>
        <TgTTTBChu>Năm mươi lăm triệu đồng chẵn</TgTTTBChu>
      </TToan>
    </NDHDon>
    <TTKhac />
  </DLHDon>
  <DSCKS>
    <NBan>
      <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo>
          <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" />
          <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />
          <Reference URI="#data_payload_id">
            <Transforms>
              <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
            </Transforms>
            <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />
            <DigestValue>base64_encoded_digest_string==</DigestValue>
          </Reference>
        </SignedInfo>
        <SignatureValue>base64_encoded_signature_string==</SignatureValue>
        <KeyInfo>
          <X509Data>
            <X509Certificate>base64_encoded_x509_cert==</X509Certificate>
          </X509Data>
        </KeyInfo>
      </Signature>
    </NBan>
  </DSCKS>
</HDon>
```

### Schema Compliance Assertions
1. **Root `<HDon>`**: Must contain `<DLHDon>` (data payload) and `<DSCKS>` (digital signatures container).
2. **Invoice Symbol (`<KHHDon>`)**: Exactly 6 alphanumeric characters:
   - Character 1: Invoice class (`C` for invoice with GDT code, `K` for invoice without GDT code).
   - Character 2-3: Last two digits of the issuance year (e.g. `24` for 2024, `26` for 2026).
   - Character 4: Invoice category (`T` for commercial enterprise, `D` for specific post/telecom, `L` for lottery, `M` for cash register e-invoice).
   - Character 5-6: Enterprise internal character identifier (`AA`, `BB`, etc.).
3. **Invoice Number (`<SHDon>`)**: Exactly 8 digits padded with leading zeros (e.g., `00000123`).
4. **Totals Verification**: Gross payment amount (`<TgTTTBSo>`) must equal net amount before tax (`<TgTCThue>`) plus total VAT (`<TgTThue>`).

---

## 3. Cryptographic Signature and XMLDSig Protocol

Every electronic invoice received must undergo automated cryptographic verification before entry into the accounts payable subledger (TK 331) or input VAT ledger (TK 133).

```
+------------------+     Extract      +-----------------------+
| E-Invoice XML    | ---------------> | <DLHDon> Payload      |
+------------------+                  +-----------------------+
         |                                        |
         | Read Signature                         | Calculate SHA-256 Digest
         v                                        v
+------------------+                  +-----------------------+
| <DSCKS> Signature| <--- Compare --- | Calculated Digest     |
| Digest & Cert    |      Digest      +-----------------------+
+------------------+
         |
         | Validate X.509
         v
+-------------------------------------------------------------+
| 1. Issuer signed by Vietnam National Root CA (NEAC)         |
| 2. Current timestamp within [NotBefore, NotAfter]           |
| 3. Signing timestamp matches invoice issuance date          |
| 4. OCSP / CRL check confirms certificate is active          |
| 5. Subject DN MST matches Seller MST in <DLHDon>            |
+-------------------------------------------------------------+
```

### Cryptographic Verification Steps
1. **Canonicalization and Digest Verification**:
   - Locate the `<DLHDon>` node matching the Reference URI attribute.
   - Canonicalize using Canonical XML 1.0 (`http://www.w3.org/TR/2001/REC-xml-c14n-20010315`).
   - Calculate SHA-256 digest of canonicalized XML payload.
   - Compare with `<DigestValue>` inside `<SignedInfo>`. Any byte discrepancy indicates payload tampering; flag as `CORRUPT_OR_ALTERED_PAYLOAD`.
2. **Signature Decryption and Validation**:
   - Extract public key from `<X509Certificate>` inside `<KeyInfo>`.
   - Verify RSA-SHA256 signature against canonicalized `<SignedInfo>`.
3. **X.509 Certificate Chain and Identity Trust**:
   - The digital certificate must be issued by a licensed Certificate Authority (CA) in Vietnam (e.g. VNPT-CA, Viettel-CA, FPT-CA, BKAV-CA, MISA-CA) rooted in the National Root Certification Authority (NEAC).
   - Validate that Subject Distinguished Name (DN) contains Tax Identification Number (`MST:<seller_tax_code>`) exactly matching `<NBan><MST>`.
4. **Certificate Validity Window and Revocation**:
   - Assert `NotBefore <= invoice_signing_date <= NotAfter`.
   - Query online OCSP responder or CRL distribution point to ensure certificate was not revoked prior to invoice signing.

---

## 4. Real-Time GDT Portal Verification Protocol

The enterprise accounting engine must interface with the national General Department of Taxation portal (`hoadondientu.gdt.gov.vn`) to verify legal authenticity and tax authority clearance.

### Query Parameter Protocol
For every incoming invoice, query the GDT portal with:
- `nbmst`: Seller Tax Identification Number (Mã số thuế bên bán)
- `khhdon`: Invoice Symbol (Ký hiệu hóa đơn)
- `shdon`: Invoice Number (Số hóa đơn)
- `tgtttbso`: Gross total payment amount (Tổng tiền thanh toán bằng số)

### Tax Authority Code (`MCCQT`) Validation
For invoices with tax authority code (`Hóa đơn có mã của cơ quan thuế`):
- Verify the 34-character hexadecimal code generated by GDT (`MCCQT`).
- If an invoice is designated as type `1` (có mã) but lacks a valid `<MCCQT>`, or the code fails GDT verification, reject invoice.

### GDT Status Code Reference
| Code | Vietnamese Status Description | Technical Meaning | Accounting Engine Action |
| :--- | :--- | :--- | :--- |
| `00` | Hóa đơn hợp lệ | Valid invoice cleared by GDT | Proceed with 3-way matching and booking |
| `01` | Hóa đơn không tồn tại | Invoice not found in GDT database | **BLOCKING**: Reject voucher; freeze payment |
| `02` | Hóa đơn đã bị xóa bỏ / hủy | Invoice marked canceled on GDT | **BLOCKING**: Prohibit payment and VAT credit |
| `03` | Hóa đơn đã bị thay thế | Invoice replaced by another invoice | Flag original as VOID; locate replacement |
| `04` | Hóa đơn đã bị điều chỉnh | Invoice adjusted by supplementary invoice | Require linked adjustment invoice before booking |

---

## 5. Taxpayer Fraud Screening and Status Registry

To protect the enterprise against bogus invoices, tax disallowance, and penalties under Law on Tax Administration No. 38/2019/QH14, vendor tax codes must be screened in real time against `tracuunnt.gdt.gov.vn`.

### GDT Taxpayer Status Classifications
- **Status `00` (NNT đang hoạt động)**: Normal operating taxpayer. Eligible for standard commercial transactions.
- **Status `01` (NNT ngừng hoạt động nhưng chưa hoàn thành thủ tục)**: Ceased business without tax clearance. Requires verification of transaction reality.
- **Status `02` (NNT tạm ngừng kinh doanh có thời hạn)**: Temporarily suspended. Verify whether invoice date falls within the officially registered suspension window. If invoice issued during suspension, treat as invalid.
- **Status `03` (NNT ngừng hoạt động, cơ quan thuế thông báo khóa MST)**: Tax code locked by tax authority. **BLOCKING**.
- **Status `04` (NNT không hoạt động tại địa chỉ đã đăng ký / Bỏ trốn)**: Runaway taxpayer who abandoned registered address. **BLOCKING**.

### Risk Enforcement Rules (Official Letters 117/TCT-CS & 2121/TCT-CS)
1. **Invoices Dated Post-Notice**: If an invoice is dated on or after the date the tax authority published an announcement of runaway status (Status 04) or tax code revocation (Status 03):
   - Input VAT (TK 133) cannot be credited under any circumstances.
   - Cost is strictly non-deductible for Corporate Income Tax (reported in Box B4 of Form 03/TNDN).
   - Accounts payable disbursement (TK 331) must be halted immediately.
2. **Invoices Dated Pre-Notice**: If an invoice was issued prior to the runaway/suspension date:
   - Must assemble an indisputable Proof of Reality dossier: signed purchase contract, warehouse receipt note signed by custodian, transport bill of lading / vehicle registration, proof of bank transfer from buyer's account to seller's registered account, and goods inspection minute.
   - If dossier is incomplete, mark as `HIGH_RISK_TAX_CONTINGENCY` and establish a tax provision.

---

## 6. Form 04/SS-HDDT Discrepancy Tracking

Under Circular 78/2021/TT-BTC Article 7 and Decree 123/2020/ND-CP Article 19, sellers may submit Form 04/SS-HDDT (Thông báo hóa đơn điện tử có sai sót) to report invoice errors, cancellations, or replacements.

### The Unilateral Cancellation Vulnerability
Vendors may unilaterally submit Form 04/SS-HDDT to cancel or replace an invoice without notifying the buyer, after the buyer has already recorded the purchase and declared input VAT.

### Automated Reconciliation Protocol
1. **Weekly Automated Polling**:
   - The accounting system must execute scheduled polling against the GDT portal for all open accounts payable (TK 331) and current-quarter tax vouchers.
2. **Discrepancy Remediation Workflow**:
   - **Cancellation Detected (Status `02`)**:
     1. Issue immediate `BLOCKING_AUDIT_ALERT`.
     2. Freeze pending vendor disbursements on TK 331.
     3. Post reversing journal entry for input VAT: Debit TK 811 (suspense) / Credit TK 133.
     4. Notify procurement and legal to demand vendor explanation and replacement invoice.
   - **Replacement Detected (Status `03`)**:
     1. Mark original invoice record as `SUPERSEDED`.
     2. Require entry of replacing invoice XML citing original invoice symbol and number.
     3. Perform automated reconciliation between original and replacement lines.

---

## 7. Mandatory Non-Cash Bank Transfer Payment Rule

Under Circular 219/2013/TT-BTC (Article 15, amended by Circular 119/2014 and Circular 173/2016) and Circular 96/2015/TT-BTC (Article 4):

### The 20,000,000 VND Threshold
For any purchase transaction with an invoice total value of **20,000,000 VND or higher** (inclusive of VAT), the buyer is legally required to execute payment via bank transfer to preserve:
1. Input Value Added Tax credit (Khấu trừ thuế GTGT đầu vào).
2. Deductible business expense for Corporate Income Tax (Chi phí được trừ khi tính thuế TNDN).

### Documentary Requirements
- **Bank Payment Voucher (Ủy nhiệm chi / Giấy báo Nợ)**: Must show funds transferred directly from the buyer's bank account (registered with the tax authority under Form 08-MST) to the seller's registered bank account.
- **Multiple Invoices on Same Calendar Day**: If buyer purchases goods from the same seller across multiple invoices on the same day, and each invoice is under 20,000,000 VND but the **aggregate total is >= 20,000,000 VND**, all invoices must be settled via bank transfer. Cash payments are disqualified.

### Prohibited Payment Methods
- **Cash Deposit at Seller's Bank Branch**: Buyer cash deposited over the counter into seller's account does NOT qualify as non-cash bank transfer because funds did not originate from buyer's account.
- **Personal Account Transfers**: Payment from employee personal bank accounts is disqualified unless expressly authorized in enterprise financial regulations, supported by internal advance and reimbursement bank transfers.

### Legitimate Non-Cash Equivalents
1. **Contractual Debt Offsetting (Bù trừ công nợ)**: Must be specified in the master contract, evidenced by bilateral debt reconciliation minutes, with any residual balance >= 20M VND paid via bank transfer.
2. **Tripartite Settlement (Thanh toán ba bên)**: Requires a formal tripartite agreement executed prior to payment.

---

## 8. Automated E-Invoice Decision Gates and Risk Matrix

| Risk Factor | Assessment Criteria | Risk Level | Automated System Action |
| :--- | :--- | :--- | :--- |
| XML Schema Conformance | Non-conforming XML or missing mandatory tags per Dec 1450 | BLOCKING | Reject file ingestion; prompt user for valid XML |
| Cryptographic Signature | SHA-256 digest mismatch or invalid X.509 signature | BLOCKING | Reject invoice; flag as corrupted or tampered |
| Certificate Authority | CA not licensed by NEAC or certificate revoked on OCSP | BLOCKING | Reject invoice; alert procurement of invalid signature |
| GDT Invoice State | Status `01` (Not found) or `02` (Canceled) | BLOCKING | Halt AP booking; freeze payment to vendor |
| Vendor Tax Status | Vendor MST has Status `03` (Suspended) or `04` (Runaway) | BLOCKING | Disallow VAT credit & CIT deduction; alert legal |
| Non-Cash Rule Breach | Invoice >= 20M VND paid in cash | MATERIAL | Disallow VAT credit; adjust CIT Box B4 on tax return |
| Form 04/SS Discrepancy | Vendor filed cancellation post-recording | MATERIAL | Reverse VAT credit; hold vendor AP balance |
| Multiple Invoices Same Day | Aggregate >= 20M VND from same vendor paid in cash | MATERIAL | Disallow VAT deduction on all cash vouchers of that day |

---

## 9. Verification and Audit Trail Checklist

- [ ] Raw XML files archived in original WORM storage with SHA-256 hash preservation.
- [ ] Cryptographic signature validation log recorded with CA name, serial number, and timestamp.
- [ ] GDT portal lookup transaction ID and MCCQT recorded in AP voucher metadata.
- [ ] Vendor tax status snapshot verified on date of invoice issuance.
- [ ] Bank payment voucher (Ủy nhiệm chi) linked to invoice number in payment ledger.
- [ ] Form 04/SS-HDDT monitoring job configured to run weekly across open subledger items.
- [ ] Tripartite agreements and debt offsetting minutes attached for non-standard settlements.
