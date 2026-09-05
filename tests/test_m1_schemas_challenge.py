#!/usr/bin/env python3
"""Empirical Adversarial Stress-Test Suite for Milestone 1 Schemas.

Validates and stress-tests:
1. period-end-closing-report.json
2. learning-assessment-report.json
3. accounting-compliance-review.json
4. learning-handoff.json

Tests categories:
- Valid bundled examples pass schema validation.
- Missing required fields fail validation.
- Invalid enum values fail validation.
- Negative numbers or out-of-bound numerical constraints fail validation.
- Bad regex patterns (e.g. invalid student_token, bad sha256) fail validation.
- Invalid date/datetime formats fail validation.
- Conditional schema constraints (allOf if-then) fail when conditions are violated.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

from dateutil import parser
import jsonschema
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "core" / "contracts" / "schemas"


def build_format_checker() -> jsonschema.FormatChecker:
    checker = copy.deepcopy(Draft202012Validator.FORMAT_CHECKER)

    @checker.checks("date-time")
    def _check_datetime(val: Any) -> bool:
        if not isinstance(val, str):
            return True
        try:
            parser.isoparse(val)
            return True
        except Exception:
            return False

    return checker


FORMAT_CHECKER = build_format_checker()


def load_schema(schema_name: str) -> tuple[dict, Draft202012Validator]:
    path = SCHEMAS_DIR / schema_name
    assert path.is_file(), f"Schema file not found: {path}"
    schema_dict = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema_dict, format_checker=FORMAT_CHECKER)
    return schema_dict, validator


def validate_payload(validator: Draft202012Validator, payload: dict) -> list[str]:
    return [err.message for err in validator.iter_errors(payload)]


# ============================================================================
# 1. period-end-closing-report.json Tests
# ============================================================================

def test_period_end_closing_report_valid_example():
    schema, validator = load_schema("period-end-closing-report.json")
    assert "examples" in schema and len(schema["examples"]) > 0
    for idx, ex in enumerate(schema["examples"]):
        errs = validate_payload(validator, ex)
        assert errs == [], f"Example {idx} failed validation: {errs}"


def test_period_end_closing_report_missing_required():
    schema, validator = load_schema("period-end-closing-report.json")
    base = copy.deepcopy(schema["examples"][0])

    top_level_required = [
        "contract_type",
        "closing_id",
        "entity",
        "period",
        "accounting_regime",
        "subledger_reconciliations",
        "closing_adjustments",
        "account_911_clearing",
        "financial_statements_package",
        "audit_trail",
        "hitl_approval",
        "data_classification",
    ]
    for req in top_level_required:
        mutated = copy.deepcopy(base)
        del mutated[req]
        errs = validate_payload(validator, mutated)
        assert any(req in e and "required" in e for e in errs), f"Expected missing required error for {req}, got: {errs}"

    # Nested required checks
    nested_cases = [
        ("entity", "legal_name"),
        ("period", "fiscal_year"),
        ("period", "closing_status"),
        ("accounting_regime", "regime_code"),
        ("closing_adjustments", "fixed_asset_depreciation"),
        ("account_911_clearing", "ending_911_balance"),
        ("account_911_clearing", "clearing_verified"),
        ("financial_statements_package", "b01_dn_balance_sheet"),
        ("audit_trail", "snapshot_hash_sha256"),
        ("hitl_approval", "chief_accountant_signature_token"),
    ]
    for parent, child in nested_cases:
        mutated = copy.deepcopy(base)
        del mutated[parent][child]
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected error when omitting {parent}.{child}, but validation passed!"


def test_period_end_closing_report_invalid_enums():
    schema, validator = load_schema("period-end-closing-report.json")
    base = copy.deepcopy(schema["examples"][0])

    enum_mutations = [
        ("period.period_type", lambda p: p["period"].update({"period_type": "biweekly"})),
        ("period.closing_status", lambda p: p["period"].update({"closing_status": "unapproved"})),
        ("accounting_regime.regime_code", lambda p: p["accounting_regime"].update({"regime_code": "US-GAAP"})),
        ("accounting_regime.transition_roadmap_stage", lambda p: p["accounting_regime"].update({"transition_roadmap_stage": "unknown_stage"})),
        ("subledger_reconciliations[0].ledger_name", lambda p: p["subledger_reconciliations"][0].update({"ledger_name": "crypto_wallet"})),
        ("subledger_reconciliations[0].status", lambda p: p["subledger_reconciliations"][0].update({"status": "pending"})),
        ("closing_adjustments.foreign_currency_revaluation.bank_rate_type", lambda p: p["closing_adjustments"]["foreign_currency_revaluation"].update({"bank_rate_type": "black_market_rate"})),
        ("hitl_approval.approval_status", lambda p: p["hitl_approval"].update({"approval_status": "auto_signed"})),
    ]

    for label, mutator in enum_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert any("is not one of" in e or "enum" in e for e in errs), f"Expected enum failure on {label}, got: {errs}"


def test_period_end_closing_report_numeric_bounds_and_consts():
    schema, validator = load_schema("period-end-closing-report.json")
    base = copy.deepcopy(schema["examples"][0])

    bound_mutations = [
        ("fiscal_year < 2000", lambda p: p["period"].update({"fiscal_year": 1999})),
        ("fiscal_year > 2100", lambda p: p["period"].update({"fiscal_year": 2101})),
        ("period_number < 1", lambda p: p["period"].update({"period_number": 0})),
        ("period_number > 12", lambda p: p["period"].update({"period_number": 13})),
        ("depreciation < 0", lambda p: p["closing_adjustments"]["fixed_asset_depreciation"].update({"tk_214_depreciation_amount": -500000})),
        ("prepaid_allocation < 0", lambda p: p["closing_adjustments"]["prepaid_expense_allocation"].update({"tk_242_allocated_amount": -10000})),
        ("grni_accrual < 0", lambda p: p["closing_adjustments"]["grni_accrual_balance"].update({"accrued_amount": -1})),
        ("ending_911_balance != 0", lambda p: p["account_911_clearing"].update({"ending_911_balance": 15000})),
        ("clearing_verified != True", lambda p: p["account_911_clearing"].update({"clearing_verified": False})),
        ("b01_is_balanced != True", lambda p: p["financial_statements_package"]["b01_dn_balance_sheet"].update({"is_balanced": False})),
        ("data_classification != restricted-metadata-only", lambda p: p.update({"data_classification": "public-open"})),
        ("subledger_reconciliations empty array", lambda p: p.update({"subledger_reconciliations": []})),
    ]

    for label, mutator in bound_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected validation failure for constraint '{label}', but passed!"


def test_period_end_closing_report_bad_regex_and_formats():
    schema, validator = load_schema("period-end-closing-report.json")
    base = copy.deepcopy(schema["examples"][0])

    pattern_mutations = [
        ("audit_trail.snapshot_hash_sha256 bad length", lambda p: p["audit_trail"].update({"snapshot_hash_sha256": "abcdef123456"})),
        ("audit_trail.snapshot_hash_sha256 non-hex chars", lambda p: p["audit_trail"].update({"snapshot_hash_sha256": "z" * 64})),
        ("entity.entity_reference invalid start char", lambda p: p["entity"].update({"entity_reference": "9-bad-start"})),
        ("period.from invalid date", lambda p: p["period"].update({"from": "not-a-date"})),
        ("period.to invalid date", lambda p: p["period"].update({"to": "2026-13-45"})),
        ("audit_trail.timestamp invalid date-time", lambda p: p["audit_trail"].update({"timestamp": "not-a-valid-datetime"})),
        ("hitl_approval.signed_at invalid date-time", lambda p: p["hitl_approval"].update({"signed_at": "invalid-timestamp"})),
    ]

    for label, mutator in pattern_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected regex/format failure for '{label}', but passed!"


# ============================================================================
# 2. learning-assessment-report.json Tests
# ============================================================================

def test_learning_assessment_report_valid_example():
    schema, validator = load_schema("learning-assessment-report.json")
    assert "examples" in schema and len(schema["examples"]) > 0
    for idx, ex in enumerate(schema["examples"]):
        errs = validate_payload(validator, ex)
        assert errs == [], f"Example {idx} failed validation: {errs}"


def test_learning_assessment_report_missing_required():
    schema, validator = load_schema("learning-assessment-report.json")
    base = copy.deepcopy(schema["examples"][0])

    top_level_required = [
        "contract_type",
        "assessment_id",
        "student_token",
        "subject",
        "topic",
        "assessment_type",
        "overall_score",
        "rubric_breakdown",
        "cognitive_error_diagnosis",
        "growth_mindset_feedback",
        "audit_metadata",
        "privacy_compliance",
    ]
    for req in top_level_required:
        mutated = copy.deepcopy(base)
        del mutated[req]
        errs = validate_payload(validator, mutated)
        assert any(req in e and "required" in e for e in errs), f"Expected missing required error for {req}, got: {errs}"

    # Nested required checks
    nested_cases = [
        ("overall_score", "raw_score"),
        ("overall_score", "max_score"),
        ("overall_score", "percentage"),
        ("overall_score", "proficiency_tier"),
        ("cognitive_error_diagnosis", "error_category"),
        ("growth_mindset_feedback", "rule_of_one_next_step"),
        ("audit_metadata", "verification_status"),
        ("privacy_compliance", "pii_redacted"),
        ("privacy_compliance", "ferpa_compliant"),
    ]
    for parent, child in nested_cases:
        mutated = copy.deepcopy(base)
        del mutated[parent][child]
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected error when omitting {parent}.{child}, but validation passed!"


def test_learning_assessment_report_invalid_enums():
    schema, validator = load_schema("learning-assessment-report.json")
    base = copy.deepcopy(schema["examples"][0])

    enum_mutations = [
        ("dok_level_evaluated", lambda p: p.update({"dok_level_evaluated": "dok_5"})),
        ("dok_level_evaluated lower", lambda p: p.update({"dok_level_evaluated": "dok_0"})),
        ("assessment_type", lambda p: p.update({"assessment_type": "pop_quiz"})),
        ("overall_score.proficiency_tier", lambda p: p["overall_score"].update({"proficiency_tier": "mastery_tier"})),
        ("rubric_breakdown[0].tier", lambda p: p["rubric_breakdown"][0].update({"tier": "flawless"})),
        ("rubric_breakdown[0].grading_hallucination_check", lambda p: p["rubric_breakdown"][0].update({"grading_hallucination_check": "hallucination_detected"})),
        ("cognitive_error_diagnosis.error_category", lambda p: p["cognitive_error_diagnosis"].update({"error_category": "careless_mistake"})),
        ("audit_metadata.verification_status", lambda p: p["audit_metadata"].update({"verification_status": "auto_approved"})),
    ]

    for label, mutator in enum_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert any("is not one of" in e or "enum" in e for e in errs), f"Expected enum failure on {label}, got: {errs}"


def test_learning_assessment_report_numeric_bounds_and_consts():
    schema, validator = load_schema("learning-assessment-report.json")
    base = copy.deepcopy(schema["examples"][0])

    bound_mutations = [
        ("raw_score < 0", lambda p: p["overall_score"].update({"raw_score": -1})),
        ("max_score < 0", lambda p: p["overall_score"].update({"max_score": -5})),
        ("percentage < 0", lambda p: p["overall_score"].update({"percentage": -0.1})),
        ("percentage > 100", lambda p: p["overall_score"].update({"percentage": 100.5})),
        ("rubric_breakdown[0].points_awarded < 0", lambda p: p["rubric_breakdown"][0].update({"points_awarded": -1})),
        ("rubric_breakdown[0].max_points < 0", lambda p: p["rubric_breakdown"][0].update({"max_points": -2})),
        ("rubric_breakdown empty array", lambda p: p.update({"rubric_breakdown": []})),
        ("zpd success_rate < 0", lambda p: p["zpd_progression"].update({"success_rate_moving_average": -0.05})),
        ("zpd success_rate > 1", lambda p: p["zpd_progression"].update({"success_rate_moving_average": 1.05})),
        ("spaced repetition interval < 1", lambda p: p["spaced_repetition_triggers"].update({"current_interval_days": 0})),
        ("spaced repetition easiness < 1.3", lambda p: p["spaced_repetition_triggers"].update({"easiness_factor": 1.29})),
        ("pii_redacted must be true", lambda p: p["privacy_compliance"].update({"pii_redacted": False})),
        ("ferpa_compliant must be true", lambda p: p["privacy_compliance"].update({"ferpa_compliant": False})),
    ]

    for label, mutator in bound_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected validation failure for constraint '{label}', but passed!"


def test_learning_assessment_report_bad_regex_and_formats():
    schema, validator = load_schema("learning-assessment-report.json")
    base = copy.deepcopy(schema["examples"][0])

    pattern_mutations = [
        ("student_token missing STU- prefix", lambda p: p.update({"student_token": "8f2e-2027"})),
        ("student_token contains whitespace", lambda p: p.update({"student_token": "STU-8f2e 2027"})),
        ("student_token is plain student real name (PII leak)", lambda p: p.update({"student_token": "Nguyen Van A"})),
        ("spaced_repetition_triggers.next_review_due invalid date", lambda p: p["spaced_repetition_triggers"].update({"next_review_due": "2026/09/12"})),
        ("audit_metadata.verification_timestamp invalid date-time", lambda p: p["audit_metadata"].update({"verification_timestamp": "yesterday-afternoon"})),
    ]

    for label, mutator in pattern_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected regex/format failure for '{label}', but passed!"


# ============================================================================
# 3. accounting-compliance-review.json Tests
# ============================================================================

def test_accounting_compliance_review_valid_example():
    schema, validator = load_schema("accounting-compliance-review.json")
    assert "examples" in schema and len(schema["examples"]) > 0
    for idx, ex in enumerate(schema["examples"]):
        errs = validate_payload(validator, ex)
        assert errs == [], f"Example {idx} failed validation: {errs}"


def test_accounting_compliance_review_missing_required():
    schema, validator = load_schema("accounting-compliance-review.json")
    base = copy.deepcopy(schema["examples"][0])

    top_level_required = [
        "contract_type",
        "review_id",
        "entity",
        "accounting_period",
        "scope",
        "accounting_regime",
        "source_version_register",
        "validation_gates",
        "data_classification",
        "status",
        "disclaimer",
    ]
    for req in top_level_required:
        mutated = copy.deepcopy(base)
        del mutated[req]
        errs = validate_payload(validator, mutated)
        assert any(req in e and "required" in e for e in errs), f"Expected missing required error for {req}, got: {errs}"


def test_accounting_compliance_review_invalid_enums():
    schema, validator = load_schema("accounting-compliance-review.json")
    base = copy.deepcopy(schema["examples"][0])

    enum_mutations = [
        ("reporting_framework.framework_type", lambda p: p["reporting_framework"].update({"framework_type": "US_GAAP"})),
        ("reporting_framework.vfrs_transition_status", lambda p: p["reporting_framework"].update({"vfrs_transition_status": "in_flight"})),
        ("e_invoice_verification.gdt_portal_status", lambda p: p["e_invoice_verification"].update({"gdt_portal_status": "forged"})),
        ("e_invoice_verification.vendor_tax_suspension_status", lambda p: p["e_invoice_verification"].update({"vendor_tax_suspension_status": "dissolved"})),
        ("three_way_matching.matching_status", lambda p: p["three_way_matching"].update({"matching_status": "partially_ignored"})),
        ("accounting_regime.name", lambda p: p["accounting_regime"].update({"name": "CIRCULAR-999"})),
        ("scope element", lambda p: p.update({"scope": ["invalid-scope-item"]})),
        ("status", lambda p: p.update({"status": "certified_complete"})),
    ]

    for label, mutator in enum_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert any("is not one of" in e or "enum" in e for e in errs), f"Expected enum failure on {label}, got: {errs}"


def test_accounting_compliance_review_conditional_logic():
    schema, validator = load_schema("accounting-compliance-review.json")
    base = copy.deepcopy(schema["examples"][0])

    # Case A: Scope includes "reconciliation" but reconciliations array is omitted
    mutated_a = copy.deepcopy(base)
    mutated_a["scope"] = ["reconciliation"]
    del mutated_a["reconciliations"]
    errs_a = validate_payload(validator, mutated_a)
    assert len(errs_a) > 0, "Expected failure when scope contains 'reconciliation' but reconciliations is omitted"

    # Case B: Scope includes "retention" but retention object is omitted
    mutated_b = copy.deepcopy(base)
    mutated_b["scope"] = ["retention"]
    del mutated_b["retention"]
    errs_b = validate_payload(validator, mutated_b)
    assert len(errs_b) > 0, "Expected failure when scope contains 'retention' but retention is omitted"

    # Case C: Scope includes "invoice" but required_human_approvals is omitted
    mutated_c = copy.deepcopy(base)
    mutated_c["scope"] = ["invoice"]
    del mutated_c["required_human_approvals"]
    errs_c = validate_payload(validator, mutated_c)
    assert len(errs_c) > 0, "Expected failure when scope contains 'invoice' but required_human_approvals is omitted"

    # Case D: Status is "reviewed" but human_confirmation is not "confirmed"
    mutated_d = copy.deepcopy(base)
    mutated_d["status"] = "reviewed"
    mutated_d["accounting_regime"]["human_confirmation"] = "required"
    mutated_d["findings"] = []
    mutated_d["validation_gates"] = [{"name": "scope-confirmed", "status": "passed"}]
    errs_d = validate_payload(validator, mutated_d)
    assert len(errs_d) > 0, "Expected failure when status is 'reviewed' but human_confirmation != 'confirmed'"

    # Case E: Status is "reviewed" but validation_gates contains blocked
    mutated_e = copy.deepcopy(base)
    mutated_e["status"] = "reviewed"
    mutated_e["accounting_regime"]["human_confirmation"] = "confirmed"
    mutated_e["findings"] = []
    mutated_e["validation_gates"] = [{"name": "scope-confirmed", "status": "blocked"}]
    errs_e = validate_payload(validator, mutated_e)
    assert len(errs_e) > 0, "Expected failure when status is 'reviewed' but validation gate is blocked"


def test_accounting_compliance_review_bad_regex_and_formats():
    schema, validator = load_schema("accounting-compliance-review.json")
    base = copy.deepcopy(schema["examples"][0])

    pattern_mutations = [
        ("entity.entity_reference starting with digit", lambda p: p["entity"].update({"entity_reference": "0-invalid-prefix"})),
        ("accounting_period.from invalid date", lambda p: p["accounting_period"].update({"from": "not-a-date"})),
        ("source_version_register verified_at invalid datetime", lambda p: p["source_version_register"][0].update({"verified_at": "not-iso-8601"})),
        ("data_classification != restricted-metadata-only", lambda p: p.update({"data_classification": "confidential-unrestricted"})),
    ]

    for label, mutator in pattern_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected regex/format failure for '{label}', but passed!"


# ============================================================================
# 4. learning-handoff.json Tests
# ============================================================================

def test_learning_handoff_valid_example():
    schema, validator = load_schema("learning-handoff.json")
    assert "examples" in schema and len(schema["examples"]) > 0
    for idx, ex in enumerate(schema["examples"]):
        errs = validate_payload(validator, ex)
        assert errs == [], f"Example {idx} failed validation: {errs}"


def test_learning_handoff_missing_required():
    schema, validator = load_schema("learning-handoff.json")
    base = copy.deepcopy(schema["examples"][0])

    top_level_required = [
        "contract_type",
        "subject",
        "grade",
        "topic",
        "artifact_type",
        "goals",
        "next_steps",
    ]
    for req in top_level_required:
        mutated = copy.deepcopy(base)
        del mutated[req]
        errs = validate_payload(validator, mutated)
        assert any(req in e and "required" in e for e in errs), f"Expected missing required error for {req}, got: {errs}"


def test_learning_handoff_grade_universal_types():
    schema, validator = load_schema("learning-handoff.json")
    base = copy.deepcopy(schema["examples"][0])

    # grade can be integer (1-12) or string (e.g. undergraduate, professional-engineering)
    valid_grades = [1, 5, 10, 12, "grade_10", "undergraduate", "graduate", "professional-engineering"]
    for g in valid_grades:
        mutated = copy.deepcopy(base)
        mutated["grade"] = g
        errs = validate_payload(validator, mutated)
        assert errs == [], f"Valid grade {g} failed: {errs}"

    # grade cannot be a boolean, object, or array
    invalid_grades = [True, False, ["grade_10"], {"tier": "k12"}]
    for g in invalid_grades:
        mutated = copy.deepcopy(base)
        mutated["grade"] = g
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Invalid grade type {g} unexpectedly passed!"


def test_learning_handoff_invalid_enums():
    schema, validator = load_schema("learning-handoff.json")
    base = copy.deepcopy(schema["examples"][0])

    enum_mutations = [
        ("artifact_type", lambda p: p.update({"artifact_type": "cheatsheet"})),
        ("learner_profile_level", lambda p: p.update({"learner_profile_level": "guru"})),
        ("zpd_assessment.scaffolding_tier", lambda p: p["zpd_assessment"].update({"scaffolding_tier": "tier_4_extreme"})),
        ("bloom_taxonomy_tier", lambda p: p.update({"bloom_taxonomy_tier": "memorize"})),
        ("dok_level", lambda p: p.update({"dok_level": "dok_99"})),
        ("ai_resistance_mechanisms element", lambda p: p.update({"ai_resistance_mechanisms": ["captcha_bypass"]})),
        ("audit_metadata.verification_status", lambda p: p["audit_metadata"].update({"verification_status": "unsupervised"})),
    ]

    for label, mutator in enum_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert any("is not one of" in e or "enum" in e for e in errs), f"Expected enum failure on {label}, got: {errs}"


def test_learning_handoff_numeric_bounds_and_formats():
    schema, validator = load_schema("learning-handoff.json")
    base = copy.deepcopy(schema["examples"][0])

    bound_mutations = [
        ("score_out_of_10 < 0", lambda p: p.update({"score_out_of_10": -0.5})),
        ("score_out_of_10 > 10", lambda p: p.update({"score_out_of_10": 10.5})),
        ("zpd success_moving_average < 0", lambda p: p["zpd_assessment"].update({"success_moving_average": -0.1})),
        ("zpd success_moving_average > 1", lambda p: p["zpd_assessment"].update({"success_moving_average": 1.1})),
        ("spaced_repetition_schedule.next_review_due invalid date", lambda p: p["spaced_repetition_schedule"].update({"next_review_due": "bad-date"})),
        ("audit_metadata.verification_timestamp invalid datetime", lambda p: p["audit_metadata"].update({"verification_timestamp": "timestamp-bad"})),
    ]

    for label, mutator in bound_mutations:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        errs = validate_payload(validator, mutated)
        assert len(errs) > 0, f"Expected validation failure for '{label}', but passed!"


# ============================================================================
# Standalone Runner & Summary Reporting
# ============================================================================

def test_deep_edge_case_attacks():
    """Deep adversarial boundary testing across all schemas."""
    # 1. Type fuzzing: floats where integers are strictly required
    _, v_closing = load_schema("period-end-closing-report.json")
    base_closing = copy.deepcopy(v_closing.schema["examples"][0])
    
    # Float in fiscal_year
    mut_float_year = copy.deepcopy(base_closing)
    mut_float_year["period"]["fiscal_year"] = 2026.5
    assert len(validate_payload(v_closing, mut_float_year)) > 0, "Float in fiscal_year should fail integer schema"

    # Float in period_number
    mut_float_period = copy.deepcopy(base_closing)
    mut_float_period["period"]["period_number"] = 3.5
    assert len(validate_payload(v_closing, mut_float_period)) > 0, "Float in period_number should fail integer schema"

    # Uppercase SHA-256 digest
    mut_upper_sha = copy.deepcopy(base_closing)
    mut_upper_sha["audit_trail"]["snapshot_hash_sha256"] = mut_upper_sha["audit_trail"]["snapshot_hash_sha256"].upper()
    assert len(validate_payload(v_closing, mut_upper_sha)) > 0, "Uppercase SHA256 should fail lowercase [a-f0-9]{64} pattern"

    # Non-zero ending 911 balance (e.g. 0.0001)
    mut_residual_911 = copy.deepcopy(base_closing)
    mut_residual_911["account_911_clearing"]["ending_911_balance"] = 0.0001
    assert len(validate_payload(v_closing, mut_residual_911)) > 0, "Residual Account 911 balance should fail const 0"

    # 2. Learning assessment student token boundary attacks
    _, v_asmt = load_schema("learning-assessment-report.json")
    base_asmt = copy.deepcopy(v_asmt.schema["examples"][0])

    # Truncated token with only prefix
    mut_empty_token = copy.deepcopy(base_asmt)
    mut_empty_token["student_token"] = "STU-"
    assert len(validate_payload(v_asmt, mut_empty_token)) > 0, "'STU-' with no suffix must fail + regex quantifier"

    # Disallowed special characters in token
    mut_special_token = copy.deepcopy(base_asmt)
    mut_special_token["student_token"] = "STU-user@domain.com"
    assert len(validate_payload(v_asmt, mut_special_token)) > 0, "Email/special char token must fail student_token regex"

    # String where boolean is expected
    mut_str_bool = copy.deepcopy(base_asmt)
    mut_str_bool["privacy_compliance"]["pii_redacted"] = "true"  # string instead of boolean True
    assert len(validate_payload(v_asmt, mut_str_bool)) > 0, "String 'true' must fail boolean const True"

    # Float in spaced repetition interval days
    mut_float_interval = copy.deepcopy(base_asmt)
    mut_float_interval["spaced_repetition_triggers"]["current_interval_days"] = 7.5
    assert len(validate_payload(v_asmt, mut_float_interval)) > 0, "Float in current_interval_days must fail integer schema"


ALL_TESTS: list[tuple[str, Callable[[], None]]] = [
    ("period-end-closing-report: valid bundled example", test_period_end_closing_report_valid_example),
    ("period-end-closing-report: missing required fields", test_period_end_closing_report_missing_required),
    ("period-end-closing-report: invalid enums", test_period_end_closing_report_invalid_enums),
    ("period-end-closing-report: numeric bounds and consts", test_period_end_closing_report_numeric_bounds_and_consts),
    ("period-end-closing-report: bad regex and date formats", test_period_end_closing_report_bad_regex_and_formats),
    ("learning-assessment-report: valid bundled example", test_learning_assessment_report_valid_example),
    ("learning-assessment-report: missing required fields", test_learning_assessment_report_missing_required),
    ("learning-assessment-report: invalid enums", test_learning_assessment_report_invalid_enums),
    ("learning-assessment-report: numeric bounds and consts", test_learning_assessment_report_numeric_bounds_and_consts),
    ("learning-assessment-report: bad regex and date formats", test_learning_assessment_report_bad_regex_and_formats),
    ("accounting-compliance-review: valid bundled example", test_accounting_compliance_review_valid_example),
    ("accounting-compliance-review: missing required fields", test_accounting_compliance_review_missing_required),
    ("accounting-compliance-review: invalid enums", test_accounting_compliance_review_invalid_enums),
    ("accounting-compliance-review: conditional allOf logic", test_accounting_compliance_review_conditional_logic),
    ("accounting-compliance-review: bad regex and date formats", test_accounting_compliance_review_bad_regex_and_formats),
    ("learning-handoff: valid bundled example", test_learning_handoff_valid_example),
    ("learning-handoff: missing required fields", test_learning_handoff_missing_required),
    ("learning-handoff: grade universal types (int/str)", test_learning_handoff_grade_universal_types),
    ("learning-handoff: invalid enums", test_learning_handoff_invalid_enums),
    ("learning-handoff: numeric bounds and formats", test_learning_handoff_numeric_bounds_and_formats),
    ("deep edge-case attacks: types, bounds, regex, and consts", test_deep_edge_case_attacks),
]


def main() -> int:
    print("=" * 80)
    print("EMPIRICAL ADVERSARIAL STRESS-TEST HARNESS: MILESTONE 1 SCHEMAS")
    print("=" * 80)
    passed_count = 0
    failed_count = 0
    failures: list[tuple[str, str]] = []

    for name, test_func in ALL_TESTS:
        try:
            test_func()
            print(f"  [PASS] {name}")
            passed_count += 1
        except AssertionError as exc:
            print(f"  [FAIL] {name}: {exc}")
            failed_count += 1
            failures.append((name, str(exc)))
        except Exception as exc:
            print(f"  [ERROR] {name}: {type(exc).__name__}: {exc}")
            failed_count += 1
            failures.append((name, f"Unexpected exception: {exc}"))

    print("-" * 80)
    print(f"Total Tests Executed: {len(ALL_TESTS)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print("=" * 80)

    if failed_count > 0:
        print("\nFAILURE SUMMARY:")
        for name, err in failures:
            print(f"- {name}: {err}")
        return 1
    else:
        print("\nALL ADVERSARIAL CHALLENGES PASSED EMPIRICALLY! SCHEMAS ARE ROBUST.")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
