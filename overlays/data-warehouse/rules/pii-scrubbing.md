# PII Scrubbing & Data Sanitization at Lakehouse Boundary

Operational standard and data engineering protocol for sanitizing Personally Identifiable Information (PII) at the Bronze-to-Silver Lakehouse boundary. This rule enforces compliance with Vietnam's Decree 13/2023/ND-CP on Personal Data Protection, salted HMAC-SHA256 phone hashing with `RETAIL_PII_SALT`, synthetic pseudonymization, geographic truncation, and automated data quality circuit breakers.

---

## 1. Regulatory Context: Decree 13/2023/ND-CP

### 1.1 Statutory Principles
Vietnam's Decree No. 13/2023/ND-CP (*Nghị định về bảo vệ dữ liệu cá nhân*) establishes rigorous legal requirements governing the processing, storage, and cross-system transmission of personal data:
1. **Data Minimization (Nguyên tắc hạn chế dữ liệu)**: Enterprises must only process personal data that is strictly necessary for the declared business objective.
2. **Storage Limitation (Nguyên tắc giới hạn lưu trữ)**: Direct identifiers (citizen names, personal mobile numbers, residential addresses) must not be retained in open, general-purpose analytical repositories or data lakes.
3. **Purpose Limitation & Confidentiality**: Customer PII gathered for order fulfillment must not be exposed to general business intelligence analysts, external BI tools (Metabase/PowerBI), or AI agent reasoning contexts without cryptographic pseudonymization.

---

## 2. Ingested Omnichannel Data Surface

Retail raw streams ingest customer data from three primary surfaces:
- **E-Commerce Platforms (Shopee Open API, TikTok Shop Partner API)**: Buyer username, recipient full name, recipient phone number, detailed delivery street address, postal code.
- **Physical POS / Store CRM**: Member loyalty card number, full name, phone number, email address, national identity card number (CCCD/CMND if collected for high-value tax invoicing).
- **Delivery Logistics / 3PL Tracking (GHN, GHTK, Viettel Post, Shopee Xpress)**: Real-time driver handoff logs, consignee phone numbers, and geolocation notes.

---

## 3. Lakehouse Boundary & Scrubbing Architecture

To guarantee zero PII leakage into analytics marts or LLM agent prompts, data processing is strictly segregated at the lakehouse boundary:

```text
┌─────────────────────────────────────────────────────────┐
│ Omnichannel Ingestion Streams (Shopee, TikTok, POS)     │
└──────────────────────────┬──────────────────────────────┘
                           │ (Encrypted TLS 1.3)
                           ▼
┌─────────────────────────────────────────────────────────┐
│ Bronze Layer: Raw Landing Zone (Encrypted at Rest)     │
│ - Immutable landing files (Parquet / JSON)              │
│ - Strictly quarantined: ZERO analyst / AI agent access  │
│ - Retention limited to 30 days statutory fulfillment   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
         [ Automated PII Scrubbing Pipeline ]
         - Normalization & HMAC-SHA256 with RETAIL_PII_SALT
         - Pseudonymization: CUST-XXXXXX
         - Geographic Truncation to Province/District
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ Silver Layer: Cleaned & Sanitized Parquet               │
│ - Fully pseudonymized & generalized dataset             │
│ - Verified by automated Regex PII Leakage Gate          │
│ - Open for DuckDB OLAP queries, BI, and AI agents       │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ Gold Layer: Dimensional Data Marts & Aggregations       │
│ - Daily sales by district, customer cohort LTV metrics  │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Scrubbing Techniques & Algorithmic Standards

### 4.1 Salted HMAC-SHA256 Hashing for Phone Numbers
Phone numbers represent the universal customer identifier across physical retail stores and digital marketplaces, but are classified as sensitive PII.

#### Normalization Invariant:
Prior to hashing, all phone numbers must be stripped of extraneous characters and formatted into canonical E.164-compatible Vietnamese mobile notation:
1. Strip all spaces, hyphens, periods, and parentheses.
2. Replace leading `+84` or `84` with `0` (or standardize to canonical `84XXXXXXXXX` format).
3. Verify that the result matches valid 10-digit Vietnamese carrier prefixes:
   `03x`, `05x`, `07x`, `08x`, `09x` (e.g., `0912345678` $\rightarrow$ `84912345678`).

#### Hashing & Pepper Discipline:
- **Algorithm**: `HMAC-SHA256(canonical_phone, secret_salt)`
- **Secret Pepper/Salt**: Sourced exclusively from the environment variable `RETAIL_PII_SALT`.
- **Mandate**: Plain `SHA256(phone)` without a high-entropy salt is strictly prohibited because phone numbers have a small keyspace ($\approx 10^8$ possibilities) subject to rainbow table reversal.
- **Security Constraint**: `RETAIL_PII_SALT` must never be logged, printed in error messages, or committed to source control.

```python
"""Salted HMAC-SHA256 phone normalization and pseudonymization engine."""

from __future__ import annotations

import hmac
import hashlib
import os
import re
from typing import Optional

# Vietnamese mobile regex (canonical 10-digit starting with 0, or with 84)
VN_PHONE_REGEX = re.compile(r"^(?:\+?84|0)(3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])([0-9]{7})$")


class PIIScrubbingError(ValueError):
    """Raised when PII normalization or hashing fails."""


def normalize_vietnam_phone(raw_phone: Optional[str]) -> Optional[str]:
    """Normalizes raw input to canonical format: 84XXXXXXXXX."""
    if not raw_phone:
        return None
    # Strip whitespace, dashes, dots, brackets
    cleaned = re.sub(r"[\s\-\.\(\)\+]", "", str(raw_phone))
    match = VN_PHONE_REGEX.match(cleaned)
    if not match:
        return None
    carrier_prefix, subscriber_number = match.groups()
    return f"84{carrier_prefix}{subscriber_number}"


def hash_phone_number(canonical_phone: Optional[str], salt: Optional[bytes] = None) -> Optional[str]:
    """Generates deterministic HMAC-SHA256 hash using RETAIL_PII_SALT."""
    if not canonical_phone:
        return None

    if salt is None:
        salt_str = os.environ.get("RETAIL_PII_SALT")
        if not salt_str:
            raise PIIScrubbingError("CRITICAL: RETAIL_PII_SALT environment variable is not configured.")
        salt = salt_str.encode("utf-8")

    return hmac.new(salt, canonical_phone.encode("utf-8"), hashlib.sha256).hexdigest()
```

---

### 4.2 Customer Name Pseudonymization
Direct names (e.g., "Nguyễn Văn A") are permanently decoupled from analytical records.
- **Rule**: Replace full customer name with synthetic deterministic token:
  `CUST-<first_8_chars_of_phone_hash>` (e.g., `CUST-A4F82B91`).
- **Anonymous Orders**: If an order has no associated phone number or customer identifier (e.g., anonymous cash POS transactions), assign `CUST-GUEST-ANON`.

---

### 4.3 Address Truncation & Geographic Generalization
Detailed residential addresses contain specific street numbers, building names, and alley coordinates that allow precise physical re-identification.
- **Generalization Rule**:
  - Strip all house numbers, building/apartment names, street names, and alley indicators (*Số nhà, Ngõ, Ngách, Hẻm, Đường*).
  - Retain **ONLY** the Province/City (*Tỉnh / Thành phố*) and District (*Quận / Huyện*).
  - Map standardized names to General Statistics Office of Vietnam (GSO) administrative division codes.
- **Example Transformation**:
  - Raw: `"Số 45, Ngõ 12, Phố Đội Cấn, Phường Liễu Giai, Quận Ba Đình, Hà Nội"`
  - Silver Lakehouse Record:
    ```json
    {
      "province_name": "Hà Nội",
      "province_gso_code": "01",
      "district_name": "Quận Ba Đình",
      "district_gso_code": "001"
    }
    ```
  - Enables accurate spatial logistics and regional purchasing analytics while eliminating re-identification.

---

## 5. Automated Verification Gates & Circuit Breakers

Every pipeline run promoting data from Bronze to Silver must execute an automated sanitization verification scan.

### 5.1 Validation Assertions
Before writing to Silver Parquet, the dataset is scanned for residual PII leakage:
1. **Phone Pattern Gate**: No column in Silver may contain a 10-digit number matching Vietnamese mobile prefixes (`/(?:0|\+?84)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b/`).
2. **Email Gate**: No column in Silver may match standard RFC 5322 email patterns.
3. **National Citizen ID Gate**: No column may contain 12-digit CCCD/CMND numbers (`/\b[0-9]{12}\b/`).

### 5.2 Circuit Breaker & Incident Quarantine
If any assertion fails:
- **Immediate Execution Halt**: The pipeline aborts immediately without committing the partition to Silver.
- **DLQ Quarantine**: The offending batch is moved into an encrypted Dead-Letter Queue (DLQ) for forensic investigation.
- **Security Incident Report**: Emit a structured security audit alert conforming to `core/contracts/schemas/security-audit.json`.

```python
"""Automated circuit breaker checking Silver Parquet batches for unscrubbed PII."""

import pyarrow as pa
import re

PHONE_LEAK_REGEX = re.compile(r"(?:0|\+?84)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b")
EMAIL_LEAK_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
CCCD_LEAK_REGEX = re.compile(r"\b[0-9]{12}\b")


def assert_zero_pii_leakage(table: pa.Table) -> None:
    """Verifies that no text columns in the Arrow Table contain raw PII patterns."""
    for col_name in table.column_names:
        field = table.field(col_name)
        if pa.types.is_string(field.type):
            for value in table[col_name].to_pylist():
                if not value:
                    continue
                str_val = str(value)
                if PHONE_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Phone number pattern found!")
                if EMAIL_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Email address pattern found!")
                if CCCD_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Citizen ID pattern found!")
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
  See `core/skills/security-data/build-data-pipeline/SKILL.md` and the `data-pipeline-spec.json` schema.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/security-data/build-data-pipeline/SKILL.md` and the `data-pipeline-spec.json` schema.

Last updated: 2026-09-05
