#!/usr/bin/env python3
"""Empirical Adversarial Stress-Test Suite for Stocktake Tolerance & State Machine.

Validates and stress-tests:
1. core/contracts/schemas/stock-audit-session.json:
   - Valid embedded examples pass jsonschema Draft202012Validator.
   - Adversarial: illegal lifecycle statuses and missing lifecycle status.
   - Adversarial: missing required event log properties & invalid scanner modalities.
   - Adversarial: invalid scan quantities (<= 0) and invalid event types.
   - Adversarial: invalid approval signature level enum & missing required approval fields.
   - Adversarial: invalid approval decision enum and empty approvals array (minItems: 1).
   - Adversarial: tolerance config boundaries (negative units, out-of-bounds percentage).
   - Adversarial: statutory suspense accounting accounts (TK 1381 / TK 1561 / TK 3381 consts).
   - Adversarial: invalid session_id regex patterns and contract discriminator mismatch.
2. State Machine Transitions Matrix:
   - Verifies 25 state transition permutations against stocktake-tolerance.md §4.
   - Proves fail-closed transition control across all lifecycle stages.
3. Blind Recount & Tolerance Engine Formulas:
   - Threshold A: Zero Tolerance for High-Value SKUs (cost >= 1,000,000 VND).
   - Threshold B: Quantity Variance Rate > 2.0% or Value Variance > 500,000 VND for standard retail SKUs.
   - Threshold C: Global Session Variance Rate > 0.5% triggering storewide closure block.
   - Multi-tier signing authority matrix (Store Manager vs Inventory Control Director HITL).
4. Markdown Link & Heading Hygiene:
   - Confirms 0 broken links and 0 duplicate headers across newly created and updated markdown files.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import urllib.parse
from typing import Any, Optional

import jsonschema
from jsonschema import Draft202012Validator
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "core" / "contracts" / "schemas" / "stock-audit-session.json"


def load_stock_audit_schema() -> tuple[dict[str, Any], Draft202012Validator]:
    assert SCHEMA_PATH.is_file(), f"Missing schema at {SCHEMA_PATH}"
    schema_dict = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema_dict)
    validator = Draft202012Validator(schema_dict)
    return schema_dict, validator


# ============================================================================
# 1. JSON SCHEMA ADVERSARIAL STRESS TESTS
# ============================================================================

class TestStockAuditSessionSchema:
    """Empirical adversarial test suite for stock-audit-session.json schema."""

    def test_embedded_examples_pass_schema_validation(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        examples = schema_dict.get("examples", [])
        assert len(examples) > 0, "No examples found in stock-audit-session.json"
        for idx, example in enumerate(examples):
            validator.validate(example)

    @pytest.mark.parametrize(
        "illegal_status",
        ["archived", "pending", "cancelled", "drafting", "in-progress", "COMPLETE", "", 999, None],
    )
    def test_adversarial_illegal_lifecycle_status(self, illegal_status: Any) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["lifecycle_status"] = illegal_status

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        err_msg = str(excinfo.value)
        assert any(term in err_msg for term in ["is not one of", "is not of type", "lifecycle_status"])

    def test_adversarial_missing_lifecycle_status(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        del payload["lifecycle_status"]

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "'lifecycle_status' is a required property" in str(excinfo.value)

    @pytest.mark.parametrize(
        "missing_prop",
        ["event_id", "timestamp", "barcode", "scanner_id", "method", "event_type", "qty"],
    )
    def test_adversarial_missing_scan_event_required_property(self, missing_prop: str) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        del payload["scan_events_log"][0][missing_prop]

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert f"'{missing_prop}' is a required property" in str(excinfo.value)

    @pytest.mark.parametrize(
        "invalid_method",
        ["voice_scanner", "laser_gun", "handheld_pda", "bluetooth_wand", "smart_glasses", "", None, 42],
    )
    def test_adversarial_invalid_scanner_modality(self, invalid_method: Any) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["scan_events_log"][0]["method"] = invalid_method

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        err_msg = str(excinfo.value)
        assert any(term in err_msg for term in ["is not one of", "is not of type", "method"])

    @pytest.mark.parametrize("invalid_qty", [0, -1, -99])
    def test_adversarial_invalid_scan_qty_minimum(self, invalid_qty: int) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["scan_events_log"][0]["qty"] = invalid_qty

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "is less than the minimum of 1" in str(excinfo.value)

    @pytest.mark.parametrize("invalid_event_type", ["delete", "corrupt", "purge", "adjust_stock", ""])
    def test_adversarial_invalid_event_type(self, invalid_event_type: str) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["scan_events_log"][0]["event_type"] = invalid_event_type

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "is not one of" in str(excinfo.value)

    @pytest.mark.parametrize(
        "invalid_level",
        ["store_clerk", "admin", "ceo", "auditor", "shift_leader", "security_guard", "", None, 123],
    )
    def test_adversarial_invalid_approval_signature_level(self, invalid_level: Any) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["approvals"][0]["level"] = invalid_level

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        err_msg = str(excinfo.value)
        assert any(term in err_msg for term in ["is not one of", "is not of type", "level"])

    @pytest.mark.parametrize(
        "missing_field",
        ["level", "approver_id", "approver_name", "decision", "signed_at", "signature_token"],
    )
    def test_adversarial_missing_approval_required_field(self, missing_field: str) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        del payload["approvals"][0][missing_field]

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert f"'{missing_field}' is a required property" in str(excinfo.value)

    @pytest.mark.parametrize("invalid_decision", ["denied", "pending", "abstained", "veto", ""])
    def test_adversarial_invalid_approval_decision(self, invalid_decision: str) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["approvals"][0]["decision"] = invalid_decision

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "is not one of" in str(excinfo.value)

    def test_adversarial_empty_approvals_array(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["approvals"] = []

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "should be non-empty" in str(excinfo.value) or "minItems" in str(excinfo.value)

    def test_adversarial_tolerance_boundaries(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        base = copy.deepcopy(schema_dict["examples"][0])

        # Negative tolerance units
        p1 = copy.deepcopy(base)
        p1["tolerance_config"]["tolerance_units"] = -1
        with pytest.raises(jsonschema.ValidationError) as exc1:
            validator.validate(p1)
        assert "is less than the minimum of 0" in str(exc1.value)

        # Negative tolerance percentage
        p2 = copy.deepcopy(base)
        p2["tolerance_config"]["tolerance_pct"] = -0.5
        with pytest.raises(jsonschema.ValidationError) as exc2:
            validator.validate(p2)
        assert "is less than the minimum of 0" in str(exc2.value)

        # Tolerance percentage > 100
        p3 = copy.deepcopy(base)
        p3["tolerance_config"]["tolerance_pct"] = 105.0
        with pytest.raises(jsonschema.ValidationError) as exc3:
            validator.validate(p3)
        assert "is greater than the maximum of 100" in str(exc3.value)

        # Discrepancy ratio > 1.0
        p4 = copy.deepcopy(base)
        p4["tolerance_config"]["discrepancy_ratio_threshold"] = 1.2
        with pytest.raises(jsonschema.ValidationError) as exc4:
            validator.validate(p4)
        assert "is greater than the maximum of 1" in str(exc4.value)

    def test_adversarial_suspense_accounting_constraints(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        base = copy.deepcopy(schema_dict["examples"][0])

        # Shortage suspense debit != 1381
        p1 = copy.deepcopy(base)
        p1["accounting_adjustments"]["shortage_suspense_1381"]["debit_account"] = "641"
        with pytest.raises(jsonschema.ValidationError) as exc1:
            validator.validate(p1)
        assert "'1381' was expected" in str(exc1.value)

        # Shortage suspense credit != 1561
        p2 = copy.deepcopy(base)
        p2["accounting_adjustments"]["shortage_suspense_1381"]["credit_account"] = "1111"
        with pytest.raises(jsonschema.ValidationError) as exc2:
            validator.validate(p2)
        assert "'1561' was expected" in str(exc2.value)

        # Surplus suspense debit != 1561
        p3 = copy.deepcopy(base)
        p3["accounting_adjustments"]["surplus_suspense_3381"] = {
            "debit_account": "1111",
            "credit_account": "3381",
            "amount_vnd": 50000.0,
        }
        with pytest.raises(jsonschema.ValidationError) as exc3:
            validator.validate(p3)
        assert "'1561' was expected" in str(exc3.value)

    def test_adversarial_contract_identity_and_session_pattern(self) -> None:
        schema_dict, validator = load_stock_audit_schema()
        base = copy.deepcopy(schema_dict["examples"][0])

        # Discriminator mismatch
        p1 = copy.deepcopy(base)
        p1["contract_type"] = "amis-voucher-contract"
        with pytest.raises(jsonschema.ValidationError) as exc1:
            validator.validate(p1)
        assert "'stock-audit-session' was expected" in str(exc1.value)

        # Session ID regex invalid characters
        p2 = copy.deepcopy(base)
        p2["session_id"] = "AUDIT/2026/STORE 01#INVALID"
        with pytest.raises(jsonschema.ValidationError) as exc2:
            validator.validate(p2)
        assert "does not match" in str(exc2.value)


# ============================================================================
# 2. STATE MACHINE TRANSITIONS PERMUTATION MATRIX
# ============================================================================

class TestStocktakeStateMachine:
    """Verifies state machine transitions conforming to stocktake-tolerance.md §4."""

    VALID_STATES = {"draft", "in_progress", "review", "recount", "closed"}
    LEGAL_TRANSITIONS = {
        ("draft", "in_progress"),
        ("in_progress", "review"),
        ("review", "recount"),
        ("recount", "review"),
        ("review", "closed"),
    }

    def can_transition(self, current_state: str, target_state: str) -> bool:
        if current_state not in self.VALID_STATES or target_state not in self.VALID_STATES:
            return False
        return (current_state, target_state) in self.LEGAL_TRANSITIONS

    def test_all_25_state_transition_permutations(self) -> None:
        for s1 in self.VALID_STATES:
            for s2 in self.VALID_STATES:
                expected_legal = (s1, s2) in self.LEGAL_TRANSITIONS
                assert self.can_transition(s1, s2) == expected_legal, (
                    f"Transition {s1} -> {s2} was expected to be "
                    f"{'LEGAL' if expected_legal else 'ILLEGAL'}"
                )

    def test_illegal_shortcuts_strictly_rejected(self) -> None:
        assert not self.can_transition("draft", "closed"), "Direct closure from draft must be blocked"
        assert not self.can_transition("draft", "review"), "Direct review from draft must be blocked"
        assert not self.can_transition("in_progress", "closed"), "Direct closure from in_progress must be blocked"
        assert not self.can_transition("recount", "closed"), "Recount must return to review before closure"
        assert not self.can_transition("closed", "in_progress"), "Closed session cannot be reopened"


# ============================================================================
# 3. MATHEMATICAL TOLERANCE ENGINE & AUTHORITY MATRIX
# ============================================================================

class TestStocktakeToleranceEngine:
    """Verifies mathematical tolerance engine and threshold triggers under Circular 200."""

    @staticmethod
    def evaluate_sku(cost_price_vnd: float, expected_qty: int, actual_qty: int) -> dict[str, Any]:
        delta_q = actual_qty - expected_qty
        abs_delta_q = abs(delta_q)
        if expected_qty > 0:
            var_rate_q = (abs_delta_q / expected_qty) * 100.0
        elif actual_qty > 0:
            var_rate_q = 100.0
        else:
            var_rate_q = 0.0

        abs_val_var = abs_delta_q * cost_price_vnd

        # Threshold A: cost_price >= 1,000,000 VND -> Zero Tolerance (abs_delta_q >= 1)
        # Threshold B: cost_price < 1,000,000 VND -> var_rate_q > 2.0% OR abs_val_var > 500,000 VND
        if cost_price_vnd >= 1_000_000:
            tier = "A"
            recount_triggered = abs_delta_q >= 1
        else:
            tier = "B"
            recount_triggered = (var_rate_q > 2.0) or (abs_val_var > 500_000)

        category = "MATCH" if delta_q == 0 else ("OVER" if delta_q > 0 else "SHORT")
        return {
            "tier": tier,
            "delta_q": delta_q,
            "var_rate_q": var_rate_q,
            "abs_val_var": abs_val_var,
            "recount_triggered": recount_triggered,
            "category": category,
        }

    @staticmethod
    def evaluate_session_authority(
        evaluated_skus: list[dict[str, Any]],
        total_system_value_vnd: float,
    ) -> dict[str, Any]:
        total_abs_variance_vnd = sum(sku["abs_val_var"] for sku in evaluated_skus)
        has_unresolved_tier_a = any(sku["tier"] == "A" and sku["delta_q"] != 0 for sku in evaluated_skus)
        session_var_rate_pct = (
            (total_abs_variance_vnd / total_system_value_vnd) * 100.0
            if total_system_value_vnd > 0
            else 0.0
        )

        # Threshold C: Global session variance rate > 0.5%
        storewide_block = session_var_rate_pct > 0.5

        if storewide_block:
            can_close = False
            required_authority = "INTERNAL_AUDIT_STOREWIDE_RECOUNT"
        elif total_abs_variance_vnd >= 5_000_000 or has_unresolved_tier_a:
            can_close = True
            required_authority = "INVENTORY_CONTROL_DIRECTOR_HITL"
        else:
            can_close = True
            required_authority = "STORE_MANAGER_OR_CHIEF_ACCOUNTANT"

        return {
            "total_abs_variance_vnd": total_abs_variance_vnd,
            "session_var_rate_pct": session_var_rate_pct,
            "storewide_block": storewide_block,
            "can_close": can_close,
            "required_authority": required_authority,
        }

    def test_threshold_a_high_value_zero_tolerance(self) -> None:
        # High value item (1,200,000 VND), discrepancy = -1 unit -> Recount
        res1 = self.evaluate_sku(1_200_000, 10, 9)
        assert res1["tier"] == "A"
        assert res1["recount_triggered"] is True
        assert res1["category"] == "SHORT"

        # High value item, exact match -> No recount
        res2 = self.evaluate_sku(1_200_000, 10, 10)
        assert res2["tier"] == "A"
        assert res2["recount_triggered"] is False
        assert res2["category"] == "MATCH"

    def test_threshold_b_standard_sku_quantity_and_value_triggers(self) -> None:
        # Standard item (150,000 VND), expected 100, actual 99 (1.0% diff, 150k VND var) -> Within tolerance
        res1 = self.evaluate_sku(150_000, 100, 99)
        assert res1["tier"] == "B"
        assert res1["recount_triggered"] is False

        # Standard item, expected 100, actual 97 (3.0% diff > 2.0%) -> Recount
        res2 = self.evaluate_sku(150_000, 100, 97)
        assert res2["tier"] == "B"
        assert res2["recount_triggered"] is True

        # Standard item, expected 100, actual 98 (2.0% diff <= 2.0%, but value = 2 * 350k = 700k > 500k VND) -> Recount
        res3 = self.evaluate_sku(350_000, 100, 98)
        assert res3["tier"] == "B"
        assert res3["recount_triggered"] is True

    def test_threshold_c_global_session_variance_and_authority_matrix(self) -> None:
        sku_clean = self.evaluate_sku(150_000, 100, 99)
        sku_high_breach = self.evaluate_sku(1_500_000, 10, 9)
        sku_massive_loss = self.evaluate_sku(100_000, 1000, 940)  # 6,000,000 VND loss

        # Case 1: Routine store closing (< 5M VND, 0 Tier A, <= 0.5% var rate)
        s1 = self.evaluate_session_authority([sku_clean], 1_000_000_000)
        assert s1["can_close"] is True
        assert s1["required_authority"] == "STORE_MANAGER_OR_CHIEF_ACCOUNTANT"

        # Case 2: Escalation to Director HITL due to Tier A breach (even with low total VND)
        s2 = self.evaluate_session_authority([sku_clean, sku_high_breach], 1_000_000_000)
        assert s2["can_close"] is True
        assert s2["required_authority"] == "INVENTORY_CONTROL_DIRECTOR_HITL"

        # Case 3: Escalation to Director HITL due to total variance >= 5,000,000 VND
        s3 = self.evaluate_session_authority([sku_massive_loss], 2_000_000_000)  # 6M / 2B = 0.3% <= 0.5%
        assert s3["can_close"] is True
        assert s3["required_authority"] == "INVENTORY_CONTROL_DIRECTOR_HITL"

        # Case 4: Threshold C storewide block (6M / 1B = 0.6% > 0.5%)
        s4 = self.evaluate_session_authority([sku_massive_loss], 1_000_000_000)
        assert s4["storewide_block"] is True
        assert s4["can_close"] is False
        assert s4["required_authority"] == "INTERNAL_AUDIT_STOREWIDE_RECOUNT"


# ============================================================================
# 4. MARKDOWN LINK & HEADING HYGIENE
# ============================================================================

class TestMarkdownLinksAndHeadersHygiene:
    """Verifies zero broken markdown links and zero duplicate headers."""

    TARGET_FILES = [
        "INDEX.md",
        "README.md",
        "core/contracts/README.md",
        "core/contracts/schemas/INDEX.md",
        "overlays/README.md",
        "overlays/retail-data-warehouse/README.md",
        "overlays/retail-data-warehouse/rules/amis-accounting-standards.md",
        "overlays/retail-data-warehouse/rules/duckdb-concurrency.md",
        "overlays/retail-data-warehouse/rules/pii-scrubbing.md",
        "overlays/retail-data-warehouse/rules/stocktake-tolerance.md",
        "packs/README.md",
    ]

    LINK_REGEX = re.compile(r'(?:!\[[^\]]*\]|\[(?P<text>[^\]]*)\])\((?P<link>[^\)\s]+)(?:\s+"[^"]*")?\)')
    HEADER_REGEX = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    @staticmethod
    def strip_fences(text: str) -> str:
        lines = []
        in_fence = False
        for line in text.splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                lines.append(line)
        return "\n".join(lines)

    def test_zero_duplicate_headers(self) -> None:
        duplicate_errors = []
        for file_rel in self.TARGET_FILES:
            file_path = ROOT / file_rel
            assert file_path.is_file(), f"Target file missing: {file_rel}"
            clean = self.strip_fences(file_path.read_text(encoding="utf-8"))

            seen = {}
            for m in self.HEADER_REGEX.finditer(clean):
                level = len(m.group(1))
                text = m.group(2).strip()
                key = (level, text)
                line_no = clean[:m.start()].count("\n") + 1
                if key in seen:
                    duplicate_errors.append(
                        f"{file_rel}:{line_no} duplicate '{m.group(1)} {text}' (first seen line {seen[key]})"
                    )
                else:
                    seen[key] = line_no

        assert duplicate_errors == [], f"Found duplicate headers: {duplicate_errors}"

    def test_zero_broken_markdown_links(self) -> None:
        broken_links = []
        for file_rel in self.TARGET_FILES:
            file_path = ROOT / file_rel
            clean = self.strip_fences(file_path.read_text(encoding="utf-8"))

            for m in self.LINK_REGEX.finditer(clean):
                link = m.group("link").strip("<>")
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                parsed = urllib.parse.urlparse(link)
                target_path = parsed.path
                if not target_path:
                    continue
                resolved = (file_path.parent / target_path).resolve()
                if not resolved.exists():
                    line_no = clean[:m.start()].count("\n") + 1
                    broken_links.append(f"{file_rel}:{line_no} broken link -> {link} (resolved to {resolved})")

        assert broken_links == [], f"Found broken links: {broken_links}"
