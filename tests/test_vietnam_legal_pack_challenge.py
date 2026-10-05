#!/usr/bin/env python3
"""Comprehensive Automated Challenge Test Suite for Vietnam Legal Counsel Pack (Milestone 5 - R5).

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance via Draft202012Validator.check_schema().
   - Full validity of bundled examples in `legal-compliance-review.json` and `legal-opinion-contract.json`.
   - Format validation including RFC-3339 date strings.

2. Adversarial Negative Mutation Stress Tests:
   - Missing top-level and nested required fields across all contract schemas.
   - Invalid discriminator constants (`contract_type`, `metadata.jurisdiction`).
   - Invalid enum values (`compliance_status`, `risk_matrix[].severity`, `risk_matrix[].status`, `metadata.status`).
   - Out-of-bounds arrays and invalid date formats.

3. Registry & Catalog Invariant Consistency:
   - Exact catalog counts: 35 roles in `core/roles/`, 35 agents in `core/a2a/.well-known/agent-registry.json`,
     and 35 agent cards in `core/a2a/registry/`.
   - Stats synchronization in `core/a2a/.well-known/role-skill-index.json` (35 roles, 133 skills, 54 schemas).
   - Stats synchronization in `adapters/antigravity/role-skill-index.json` (35 roles, 133 skills, 54 schemas).
   - Master Index header invariants in `INDEX.md`.

4. Fast Invocation Alias Resolution:
   - Role aliases: `"vietnam-legal-counsel"`, `"lawyer"`, `"luat-su"`, `"legal"`, `"legal-counsel"` -> `"vietnam-legal-counsel"`.
   - Skill aliases: `"manage-vietnam-legal"`, `"legal"`, `"luat"`, `"vietnam_legal"`, `"manage_vietnam_legal"`, `"vietnam-legal"` -> `["manage-vietnam-legal"]`.

5. A2A Agent Card & Action Boundaries Governance:
   - Schema validity and A2A 1.0 protocol compliance of `vietnam-legal-counsel.agent-card.json`.
   - Action boundary tier isolation: strictly disjoint `allowed`, `requires_approval`, and `denied` lists.
   - Enforce irreversible action locks (never allowed) and specific legal governance prohibitions in denied tier.

6. Artifact Existence, Statutory Citations & Structural Conformance:
   - `reports/vietnam-legal-counsel-repo-research.md` (>= 100,000 bytes with comprehensive statutory citations).
   - `core/roles/vietnam-legal-counsel.md` (role-standard compliance, skill toolbox lock, guardrails).
   - `core/skills/legal-compliance/manage-vietnam-legal/SKILL.md` (< 200 lines, valid frontmatter).
   - `core/skills/legal-compliance/manage-vietnam-legal/references/statutory-checklists.md` (checklists and rubrics).
   - Documentation catalog cross-referencing in `core/roles/README.md`, `core/skills/README.md`, and `core/contracts/README.md`.
"""

from __future__ import annotations

import copy
import glob
import json
import os
from pathlib import Path
import random
import re
import string
from typing import Any, Dict, List

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import pytest
import yaml

# Base directory roots
REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
SCHEMAS_DIR = CORE_DIR / "contracts" / "schemas"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
A2A_DIR = CORE_DIR / "a2a"
REGISTRY_DIR = A2A_DIR / "registry"
WELL_KNOWN_DIR = A2A_DIR / ".well-known"
POLICIES_DIR = CORE_DIR / "policies"
ADAPTERS_DIR = REPO_ROOT / "adapters"
REPORTS_DIR = REPO_ROOT / "reports"


def load_json(path: Path) -> dict:
    assert path.is_file(), f"File does not exist: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path) -> dict:
    assert path.is_file(), f"File does not exist: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ==============================================================================
# 1. SCHEMA VALIDATION TESTS
# ==============================================================================

class TestVietnamLegalSchemaValidation:
    """Validates schemas against Draft 2020-12 meta-schema and tests bundled examples."""

    @pytest.fixture(scope="class")
    def compliance_review_schema(self) -> dict:
        schema_path = SCHEMAS_DIR / "legal-compliance-review.json"
        return load_json(schema_path)

    @pytest.fixture(scope="class")
    def legal_opinion_schema(self) -> dict:
        schema_path = SCHEMAS_DIR / "legal-opinion-contract.json"
        return load_json(schema_path)

    def test_schemas_draft202012_meta_validation(
        self, compliance_review_schema: dict, legal_opinion_schema: dict
    ):
        """Both legal contract schemas must be valid JSON Schema Draft 2020-12 definitions."""
        # Meta-schema check throws SchemaError if schema itself is malformed
        Draft202012Validator.check_schema(compliance_review_schema)
        Draft202012Validator.check_schema(legal_opinion_schema)

        assert compliance_review_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert legal_opinion_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"

    def test_legal_compliance_review_bundled_examples(self, compliance_review_schema: dict):
        """All bundled examples in legal-compliance-review.json must validate cleanly."""
        examples = compliance_review_schema.get("examples", [])
        assert len(examples) > 0, "legal-compliance-review.json must bundle at least one example"

        validator = Draft202012Validator(
            compliance_review_schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        )
        for idx, example in enumerate(examples):
            # Must not raise ValidationError
            validator.validate(example)
            assert example["contract_type"] == "legal-compliance-review"
            assert example["compliance_status"] in ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT"]

    def test_legal_opinion_contract_bundled_examples(self, legal_opinion_schema: dict):
        """All bundled examples in legal-opinion-contract.json must validate cleanly."""
        examples = legal_opinion_schema.get("examples", [])
        assert len(examples) > 0, "legal-opinion-contract.json must bundle at least one example"

        validator = Draft202012Validator(
            legal_opinion_schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        )
        for idx, example in enumerate(examples):
            validator.validate(example)
            assert example["contract_type"] == "legal-opinion-contract"
            assert example["metadata"]["status"] in [
                "DRAFT", "UNDER_REVIEW", "FINAL", "SUPERSEDED",
                "draft", "under_review", "final", "superseded"
            ]


# ==============================================================================
# 2. ADVERSARIAL NEGATIVE MUTATION TESTS
# ==============================================================================

class TestVietnamLegalAdversarialMutations:
    """Stress-tests legal schemas against invalid, missing, and adversarial inputs."""

    @pytest.fixture(scope="class")
    def compliance_validator(self) -> Draft202012Validator:
        schema = load_json(SCHEMAS_DIR / "legal-compliance-review.json")
        return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)

    @pytest.fixture(scope="class")
    def compliance_base_example(self) -> dict:
        schema = load_json(SCHEMAS_DIR / "legal-compliance-review.json")
        return copy.deepcopy(schema["examples"][0])

    @pytest.fixture(scope="class")
    def opinion_validator(self) -> Draft202012Validator:
        schema = load_json(SCHEMAS_DIR / "legal-opinion-contract.json")
        return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)

    @pytest.fixture(scope="class")
    def opinion_base_example(self) -> dict:
        schema = load_json(SCHEMAS_DIR / "legal-opinion-contract.json")
        return copy.deepcopy(schema["examples"][0])

    # --- legal-compliance-review.json Negative Tests ---

    def test_compliance_review_missing_top_level_required(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Omitting any top-level required property in legal-compliance-review must raise ValidationError."""
        top_level_required = [
            "contract_type",
            "metadata",
            "compliance_status",
            "risk_matrix",
            "statutory_citations",
            "recommendations",
            "human_approval_gate",
        ]
        for field in top_level_required:
            mutated = copy.deepcopy(compliance_base_example)
            del mutated[field]
            with pytest.raises(ValidationError) as excinfo:
                compliance_validator.validate(mutated)
            assert field in excinfo.value.message or "is a required property" in excinfo.value.message

    def test_compliance_review_missing_nested_required(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Omitting required nested attributes in legal-compliance-review must raise ValidationError."""
        nested_cases = [
            # parent, child
            ("metadata", "entity"),
            ("metadata", "review_date"),
            ("metadata", "reviewer"),
            ("metadata", "jurisdiction"),
            ("metadata", "scope"),
            ("human_approval_gate", "required"),
            ("human_approval_gate", "approver"),
        ]
        for parent, child in nested_cases:
            mutated = copy.deepcopy(compliance_base_example)
            del mutated[parent][child]
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # Check required fields inside risk_matrix items
        risk_item_required = [
            "id", "pillar", "severity", "statutory_basis", "finding", "impact", "mitigation", "status"
        ]
        for req in risk_item_required:
            mutated = copy.deepcopy(compliance_base_example)
            del mutated["risk_matrix"][0][req]
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # Check required fields inside statutory_citations items
        citation_required = ["law", "article", "relevance"]
        for req in citation_required:
            mutated = copy.deepcopy(compliance_base_example)
            del mutated["statutory_citations"][0][req]
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_compliance_review_invalid_discriminator_const(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Invalid contract_type discriminator or jurisdiction const must fail validation."""
        invalid_types = ["legal-opinion-contract", "arbitrary-string", "compliance-audit", ""]
        for bad_type in invalid_types:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["contract_type"] = bad_type
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # metadata.jurisdiction has const "VN"
        invalid_jurisdictions = ["US", "SG", "VN-HN", "Vietnam", ""]
        for bad_jur in invalid_jurisdictions:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["metadata"]["jurisdiction"] = bad_jur
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_compliance_review_invalid_enums(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Invalid enums in compliance_status, severity, or status must fail validation."""
        # compliance_status enum: ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT"]
        bad_compliance_statuses = ["PENDING", "APPROVED", "FAILED", "compliant_with_notes", ""]
        for bad_status in bad_compliance_statuses:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["compliance_status"] = bad_status
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # risk severity enum
        bad_severities = ["BLOCKING", "EXTREME", "FATAL", "NEGLIGIBLE", ""]
        for bad_sev in bad_severities:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["risk_matrix"][0]["severity"] = bad_sev
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # risk status enum
        bad_risk_statuses = ["PENDING", "DEFERRED", "RESOLVED_TEMP", "IGNORE", ""]
        for bad_st in bad_risk_statuses:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["risk_matrix"][0]["status"] = bad_st
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_compliance_review_format_and_bounds(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Date formats and array bounds constraints must be enforced."""
        # review_date must be format: date
        mutated = copy.deepcopy(compliance_base_example)
        mutated["metadata"]["review_date"] = "not-a-date"
        with pytest.raises(ValidationError):
            compliance_validator.validate(mutated)

        # scope minItems: 1
        mutated = copy.deepcopy(compliance_base_example)
        mutated["metadata"]["scope"] = []
        with pytest.raises(ValidationError):
            compliance_validator.validate(mutated)

    # --- legal-opinion-contract.json Negative Tests ---

    def test_opinion_contract_missing_top_level_required(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Omitting any top-level required property in legal-opinion-contract must raise ValidationError."""
        top_level_required = [
            "contract_type",
            "metadata",
            "factual_background",
            "legal_issues",
            "conclusion_and_opinion",
            "caveats_and_disclaimers",
        ]
        for field in top_level_required:
            mutated = copy.deepcopy(opinion_base_example)
            del mutated[field]
            with pytest.raises(ValidationError) as excinfo:
                opinion_validator.validate(mutated)
            assert field in excinfo.value.message or "is a required property" in excinfo.value.message

    def test_opinion_contract_missing_nested_required(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Omitting required nested attributes in legal-opinion-contract must raise ValidationError."""
        nested_cases = [
            ("metadata", "opinion_id"),
            ("metadata", "subject"),
            ("metadata", "client_entity"),
            ("metadata", "counsel_name"),
            ("metadata", "date"),
            ("metadata", "status"),
            ("factual_background", "summary"),
            ("factual_background", "documents_reviewed"),
            ("factual_background", "assumptions"),
            ("conclusion_and_opinion", "executive_opinion"),
            ("conclusion_and_opinion", "conditions"),
            ("conclusion_and_opinion", "risk_assessment"),
            ("caveats_and_disclaimers", "non_litigation_notice"),
            ("caveats_and_disclaimers", "hitl_notice"),
        ]
        for parent, child in nested_cases:
            mutated = copy.deepcopy(opinion_base_example)
            del mutated[parent][child]
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

        # Check required fields inside legal_issues items
        issue_required = ["issue_id", "question", "statutory_analysis", "governing_laws"]
        for req in issue_required:
            mutated = copy.deepcopy(opinion_base_example)
            del mutated["legal_issues"][0][req]
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

    def test_opinion_contract_invalid_discriminator_const(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Invalid contract_type discriminator const must fail validation."""
        invalid_types = ["legal-compliance-review", "unauthorized-opinion", "opinion", ""]
        for bad_type in invalid_types:
            mutated = copy.deepcopy(opinion_base_example)
            mutated["contract_type"] = bad_type
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

    def test_opinion_contract_invalid_enums_and_formats(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Invalid lifecycle status enum or invalid date format must fail validation."""
        # metadata.status enum: ["DRAFT", "UNDER_REVIEW", "FINAL", "SUPERSEDED", ...]
        bad_statuses = ["PUBLISHED", "ARCHIVED", "APPROVED", "SIGNED", ""]
        for bad_st in bad_statuses:
            mutated = copy.deepcopy(opinion_base_example)
            mutated["metadata"]["status"] = bad_st
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

        # metadata.date must be valid date
        mutated = copy.deepcopy(opinion_base_example)
        mutated["metadata"]["date"] = "2026-13-45"
        with pytest.raises(ValidationError):
            opinion_validator.validate(mutated)

    def test_compliance_review_corrupt_discriminator_types(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Corrupting contract_type with non-string, null, or malformed types must fail validation."""
        fuzzed_types = [
            None,
            12345,
            True,
            False,
            ["legal-compliance-review"],
            {"type": "legal-compliance-review"},
            "",
            "legal_compliance_review",
            "LEGAL-COMPLIANCE-REVIEW",
        ]
        for bad_val in fuzzed_types:
            mutated = copy.deepcopy(compliance_base_example)
            mutated["contract_type"] = bad_val
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_opinion_contract_corrupt_discriminator_types(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Corrupting contract_type with non-string, null, or malformed types must fail validation."""
        fuzzed_types = [
            None,
            9999,
            True,
            False,
            ["legal-opinion-contract"],
            {"name": "opinion"},
            "",
            "legal_opinion_contract",
            "LEGAL-OPINION-CONTRACT",
        ]
        for bad_val in fuzzed_types:
            mutated = copy.deepcopy(opinion_base_example)
            mutated["contract_type"] = bad_val
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

    def test_compliance_review_exhaustive_date_fuzzing(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Fuzz review_date and approval_date with invalid calendar dates, bad delimiters, and malformed strings."""
        fuzzed_dates = [
            "2026-02-31",
            "2026-13-01",
            "2026-00-10",
            "2026-04-31",
            "2026/09/27",
            "27-09-2026",
            "2026-09-27T10:00:00Z",
            "not-a-date",
            "",
            123456,
            None,
        ]
        for bad_date in fuzzed_dates:
            # Test review_date
            mutated = copy.deepcopy(compliance_base_example)
            mutated["metadata"]["review_date"] = bad_date
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

            # Test human_approval_gate.approval_date
            mutated = copy.deepcopy(compliance_base_example)
            mutated["human_approval_gate"]["approval_date"] = bad_date
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_opinion_contract_exhaustive_date_fuzzing(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Fuzz metadata.date with invalid calendar dates, bad delimiters, and non-date formats."""
        fuzzed_dates = [
            "2026-02-31",
            "2026-13-01",
            "2026-00-10",
            "2026-04-31",
            "2026/09/27",
            "27-09-2026",
            "2026-09-27T10:00:00Z",
            "not-a-date",
            "",
            123456,
            None,
        ]
        for bad_date in fuzzed_dates:
            mutated = copy.deepcopy(opinion_base_example)
            mutated["metadata"]["date"] = bad_date
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

    def test_compliance_review_out_of_bounds_arrays_and_types(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Test array boundary constraints (minItems) and type safety when array fields receive non-arrays."""
        # scope minItems: 1
        mutated = copy.deepcopy(compliance_base_example)
        mutated["metadata"]["scope"] = []
        with pytest.raises(ValidationError):
            compliance_validator.validate(mutated)

        # non-array types for array properties
        array_fuzz_cases = [
            ("metadata", "scope", "single_scope_string"),
            ("risk_matrix", None, "not_an_array"),
            ("risk_matrix", None, {"id": "single_dict"}),
            ("statutory_citations", None, 12345),
            ("recommendations", None, "single_recommendation_string"),
        ]
        for parent, child, bad_val in array_fuzz_cases:
            mutated = copy.deepcopy(compliance_base_example)
            if child is None:
                mutated[parent] = bad_val
            else:
                mutated[parent][child] = bad_val
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_opinion_contract_out_of_bounds_arrays_and_types(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Test non-array types for array properties in legal-opinion-contract."""
        array_fuzz_cases = [
            ("factual_background", "documents_reviewed", "single_document_string"),
            ("factual_background", "assumptions", 999),
            ("legal_issues", None, "not_an_array"),
            ("legal_issues", None, {"issue_id": "single"}),
            ("conclusion_and_opinion", "conditions", True),
        ]
        for parent, child, bad_val in array_fuzz_cases:
            mutated = copy.deepcopy(opinion_base_example)
            if child is None:
                mutated[parent] = bad_val
            else:
                mutated[parent][child] = bad_val
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

    def test_opinion_contract_action_plan_nested_requirements(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """When action_plan is present, its required properties (steps) and step item constraints must be enforced."""
        # Missing steps
        mutated = copy.deepcopy(opinion_base_example)
        mutated["action_plan"] = {}
        with pytest.raises(ValidationError):
            opinion_validator.validate(mutated)

        # Step object missing required 'action'
        mutated = copy.deepcopy(opinion_base_example)
        mutated["action_plan"] = {"steps": [{"step_number": 1, "owner": "Operations"}]}
        with pytest.raises(ValidationError):
            opinion_validator.validate(mutated)

    def test_additional_unknown_properties_and_restricted_boundary(
        self,
        compliance_validator: Draft202012Validator,
        compliance_base_example: dict,
        opinion_validator: Draft202012Validator,
        opinion_base_example: dict,
    ):
        """Legal schemas allow auxiliary metadata without schema mutation, while restricted schemas reject unknown keys."""
        # 1. Open schema tolerance: legal-compliance-review accepts auxiliary metadata
        mutated_comp = copy.deepcopy(compliance_base_example)
        mutated_comp["__auxiliary_audit_id"] = "AUDIT-2026-X99"
        mutated_comp["extra_legal_tags"] = ["confidential", "board_review"]
        compliance_validator.validate(mutated_comp)  # must pass without raising

        # 2. Open schema tolerance: legal-opinion-contract accepts auxiliary metadata
        mutated_op = copy.deepcopy(opinion_base_example)
        mutated_op["__firm_reference_code"] = "FIRMVN-9988"
        mutated_op["custom_disclaimer_extra"] = "Additional internal notes"
        opinion_validator.validate(mutated_op)  # must pass without raising

        # 3. Restricted schema boundary: implementation-result.json defines additionalProperties: false
        impl_schema_path = SCHEMAS_DIR / "implementation-result.json"
        if impl_schema_path.is_file():
            impl_schema = load_json(impl_schema_path)
            impl_validator = Draft202012Validator(impl_schema)
            impl_example = copy.deepcopy(impl_schema.get("examples", [{}])[0])
            if impl_example:
                impl_example["__unauthorized_extra_key__"] = "injected_payload"
                with pytest.raises(ValidationError):
                    impl_validator.validate(impl_example)

    def test_compliance_review_randomized_adversarial_fuzzer(
        self, compliance_validator: Draft202012Validator, compliance_base_example: dict
    ):
        """Randomized fuzzer generating adversarial payloads across discriminators, enums, dates, and types."""
        rng = random.Random(2026)

        # 1. Fuzz corrupted discriminator strings
        for _ in range(25):
            bad_discriminator = "".join(rng.choices(string.ascii_letters + string.punctuation, k=16))
            if bad_discriminator == "legal-compliance-review":
                continue
            mutated = copy.deepcopy(compliance_base_example)
            mutated["contract_type"] = bad_discriminator
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # 2. Fuzz invalid compliance_status enums
        valid_statuses = {"COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT"}
        for _ in range(25):
            bad_status = "".join(rng.choices(string.ascii_uppercase, k=10))
            if bad_status in valid_statuses:
                continue
            mutated = copy.deepcopy(compliance_base_example)
            mutated["compliance_status"] = bad_status
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # 3. Fuzz invalid calendar dates (bad months 13-99, bad days 32-99)
        for _ in range(25):
            year = rng.randint(2020, 2035)
            month = rng.randint(13, 99)
            day = rng.randint(32, 99)
            bad_date = f"{year}-{month:02d}-{day:02d}"
            mutated = copy.deepcopy(compliance_base_example)
            mutated["metadata"]["review_date"] = bad_date
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

        # 4. Fuzz invalid risk_matrix severity enums
        valid_severities = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL", "critical", "high", "medium", "low"}
        for _ in range(25):
            bad_sev = "".join(rng.choices(string.ascii_uppercase, k=7))
            if bad_sev in valid_severities:
                continue
            mutated = copy.deepcopy(compliance_base_example)
            mutated["risk_matrix"][0]["severity"] = bad_sev
            with pytest.raises(ValidationError):
                compliance_validator.validate(mutated)

    def test_opinion_contract_randomized_adversarial_fuzzer(
        self, opinion_validator: Draft202012Validator, opinion_base_example: dict
    ):
        """Randomized fuzzer generating adversarial payloads for legal-opinion-contract."""
        rng = random.Random(2027)

        # 1. Fuzz corrupted discriminator strings
        for _ in range(25):
            bad_discriminator = "".join(rng.choices(string.ascii_letters + string.punctuation, k=16))
            if bad_discriminator == "legal-opinion-contract":
                continue
            mutated = copy.deepcopy(opinion_base_example)
            mutated["contract_type"] = bad_discriminator
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

        # 2. Fuzz invalid lifecycle status enums
        valid_statuses = {"DRAFT", "UNDER_REVIEW", "FINAL", "SUPERSEDED", "draft", "under_review", "final", "superseded"}
        for _ in range(25):
            bad_status = "".join(rng.choices(string.ascii_uppercase, k=8))
            if bad_status in valid_statuses:
                continue
            mutated = copy.deepcopy(opinion_base_example)
            mutated["metadata"]["status"] = bad_status
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)

        # 3. Fuzz invalid calendar dates (bad months 13-99, bad days 32-99)
        for _ in range(25):
            year = rng.randint(2020, 2035)
            month = rng.randint(13, 99)
            day = rng.randint(32, 99)
            bad_date = f"{year}-{month:02d}-{day:02d}"
            mutated = copy.deepcopy(opinion_base_example)
            mutated["metadata"]["date"] = bad_date
            with pytest.raises(ValidationError):
                opinion_validator.validate(mutated)



# ==============================================================================
# 3. REGISTRY & INVARIANT CONSISTENCY TESTS
# ==============================================================================

class TestVietnamLegalRegistryConsistency:
    """Verifies registry catalogs, stats synchronization, and INDEX invariants."""

    def test_exact_catalog_counts_35_roles_and_agents(self):
        """Exact catalog count must be 35 roles, 35 agent cards, and 35 registered agents."""
        role_files = [
            f for f in ROLES_DIR.glob("*.md")
            if f.name not in ("README.md", "role-standard.md")
        ]
        assert len(role_files) == 35, f"Expected exactly 35 role files under core/roles/, found {len(role_files)}"

        agent_cards = list(REGISTRY_DIR.glob("*.agent-card.json"))
        assert len(agent_cards) == 35, f"Expected exactly 35 agent cards under core/a2a/registry/, found {len(agent_cards)}"

        agent_registry = load_json(WELL_KNOWN_DIR / "agent-registry.json")
        registered_agents = agent_registry.get("agents", [])
        assert len(registered_agents) == 35, f"Expected exactly 35 agents in agent-registry.json, found {len(registered_agents)}"

        # Ensure vietnam-legal-counsel is present in all three
        role_slugs = [rf.stem for rf in role_files]
        assert "vietnam-legal-counsel" in role_slugs

        card_names = [c.name.replace(".agent-card.json", "") for c in agent_cards]
        assert "vietnam-legal-counsel" in card_names

        reg_roles = [a.get("role") for a in registered_agents]
        assert "vietnam-legal-counsel" in reg_roles

    def test_stats_consistency_role_skill_index(self):
        """Both core and adapter role-skill-index.json must record stats: 35 roles, 133 or 135 skills, 54 schemas."""
        core_index = load_json(WELL_KNOWN_DIR / "role-skill-index.json")
        adapter_index = load_json(ADAPTERS_DIR / "antigravity" / "role-skill-index.json")

        for name, index_doc in [("core", core_index), ("adapter", adapter_index)]:
            stats = index_doc.get("stats", {})
            assert stats.get("roles") == 35, f"{name} role-skill-index roles stat mismatch: got {stats.get('roles')}, expected 35"
            assert stats.get("skills") in (133, 135, 137, 138), f"{name} role-skill-index skills stat mismatch: got {stats.get('skills')}, expected 138"
            assert stats.get("schemas") == 54, f"{name} role-skill-index schemas stat mismatch: got {stats.get('schemas')}, expected 54"

    def test_index_md_header_counts(self):
        """INDEX.md header must declare Total Catalog: 35 Roles | 133, 135, 137 or 138 Skills | 25 Workflows | 54 Data Contracts."""
        index_md_path = REPO_ROOT / "INDEX.md"
        assert index_md_path.is_file()
        content = index_md_path.read_text(encoding="utf-8")

        # Strip bold asterisks for uniform matching
        stripped = content.replace("**", "")
        expected_headers = [
            "Total Catalog: 35 Roles | 138 Skills (126 Core + 12 Overlays) | 25 Workflows | 54 Data Contracts",
            "Total Catalog: 35 Roles | 137 Skills (125 Core + 12 Overlays) | 25 Workflows | 54 Data Contracts",
            "Total Catalog: 35 Roles | 135 Skills (123 Core + 12 Overlays) | 25 Workflows | 54 Data Contracts",
            "Total Catalog: 35 Roles | 133 Skills (121 Core + 12 Overlays) | 25 Workflows | 54 Data Contracts",
        ]
        assert any(h in stripped for h in expected_headers), f"INDEX.md header does not contain expected catalog counts: {stripped[:120]}"

    def test_index_md_role_and_skill_listings(self):
        """INDEX.md must list vietnam-legal-counsel and manage-vietnam-legal."""
        content = (REPO_ROOT / "INDEX.md").read_text(encoding="utf-8")
        assert "vietnam-legal-counsel" in content
        assert "manage-vietnam-legal" in content
        assert "legal-compliance-review.json" in content
        assert "legal-opinion-contract.json" in content

    def test_exact_catalog_counts_35_roles_133_skills_54_schemas_across_all_files(self):
        """Exhaustively verify exact catalog counts across all files, directories, registries, and stats headers."""
        # 1. 35 Role markdown files
        role_files = [f for f in ROLES_DIR.glob("*.md") if f.name not in ("README.md", "role-standard.md")]
        assert len(role_files) == 35, f"Expected 35 role files, got {len(role_files)}"

        # 2. 35 Agent cards
        agent_cards = list(REGISTRY_DIR.glob("*.agent-card.json"))
        assert len(agent_cards) == 35, f"Expected 35 agent cards, got {len(agent_cards)}"

        # 3. 35 Registered agents in agent-registry.json
        agent_registry = load_json(WELL_KNOWN_DIR / "agent-registry.json")
        assert len(agent_registry.get("agents", [])) == 35

        # 4. 35 Roles in role-skill-index.json (core and adapter)
        core_index = load_json(WELL_KNOWN_DIR / "role-skill-index.json")
        adapter_index = load_json(ADAPTERS_DIR / "antigravity" / "role-skill-index.json")
        assert core_index["stats"]["roles"] == 35
        assert len(core_index["roles"]) == 35
        assert adapter_index["stats"]["roles"] == 35
        assert len(adapter_index["roles"]) == 35

        # 5. Total skills: 121, 123, 125 or 126 core skills + 12 overlay skills
        core_skill_files = list(SKILLS_DIR.glob("**/SKILL.md"))
        assert len(core_skill_files) in (121, 123, 125, 126), f"Expected 121, 123, 125 or 126 core skills, got {len(core_skill_files)}"
        overlay_skill_files = list(REPO_ROOT.glob("overlays/**/SKILL.md"))
        assert len(overlay_skill_files) == 12, f"Expected 12 overlay skills, got {len(overlay_skill_files)}"

        assert core_index["stats"]["skills"] in (133, 135, 137, 138)
        assert len(core_index["skills"]) in (133, 135, 137, 138)
        assert adapter_index["stats"]["skills"] in (133, 135, 137, 138)
        assert len(adapter_index["skills"]) in (133, 135, 137, 138)

        # Verify all skill file paths in index exist on disk
        for skill_id, skill_meta in core_index["skills"].items():
            skill_path = REPO_ROOT / skill_meta["file"]
            assert skill_path.is_file(), f"Skill file missing for {skill_id}: {skill_path}"

        # 6. 54 Schemas in core/contracts/schemas/
        schema_files = list(SCHEMAS_DIR.glob("*.json"))
        assert len(schema_files) == 54, f"Expected 54 schema files, got {len(schema_files)}"
        assert core_index["stats"]["schemas"] == 54
        assert len(core_index.get("schemas", [])) == 54
        assert adapter_index["stats"]["schemas"] == 54
        assert len(adapter_index.get("schemas", [])) == 54

        for s in core_index.get("schemas", []):
            assert (SCHEMAS_DIR / s).is_file(), f"Schema file missing: {s}"



# ==============================================================================
# 4. ALIAS RESOLUTION TESTS
# ==============================================================================

class TestVietnamLegalAliasResolution:
    """Verifies fast invocation @<role> and @<skill> alias routing."""

    @pytest.fixture(scope="class")
    def core_index(self) -> dict:
        return load_json(WELL_KNOWN_DIR / "role-skill-index.json")

    @pytest.fixture(scope="class")
    def adapter_index(self) -> dict:
        return load_json(ADAPTERS_DIR / "antigravity" / "role-skill-index.json")

    def test_role_aliases_for_vietnam_legal_counsel(self, core_index: dict, adapter_index: dict):
        """All canonical role aliases must resolve to 'vietnam-legal-counsel'."""
        required_aliases = [
            "vietnam-legal-counsel",
            "lawyer",
            "luat-su",
            "legal",
            "legal-counsel",
        ]
        for name, index_doc in [("core", core_index), ("adapter", adapter_index)]:
            role_aliases = index_doc.get("role_aliases", {})
            for alias in required_aliases:
                target = role_aliases.get(alias)
                assert target == "vietnam-legal-counsel", (
                    f"In {name} index: alias '@{alias}' resolves to '{target}', expected 'vietnam-legal-counsel'"
                )

    def test_skill_aliases_for_manage_vietnam_legal(self, core_index: dict, adapter_index: dict):
        """All canonical skill aliases must resolve to ['manage-vietnam-legal']."""
        required_skill_aliases = [
            "manage-vietnam-legal",
            "legal",
            "luat",
            "vietnam_legal",
        ]
        for name, index_doc in [("core", core_index), ("adapter", adapter_index)]:
            skill_aliases = index_doc.get("skill_aliases", {})
            for alias in required_skill_aliases:
                target = skill_aliases.get(alias)
                assert target == ["manage-vietnam-legal"], (
                    f"In {name} index: alias '@{alias}' resolves to {target}, expected ['manage-vietnam-legal']"
                )

    def test_exhaustive_all_role_aliases_resolution(self, core_index: dict, adapter_index: dict):
        """Exhaustively verify that ALL role aliases in both core and adapter registries resolve to registered roles with disk files."""
        for name, index_doc in [("core", core_index), ("adapter", adapter_index)]:
            role_aliases = index_doc.get("role_aliases", {})
            roles = index_doc.get("roles", {})
            assert len(role_aliases) >= 100, f"{name} role_aliases count unexpectedly low: {len(role_aliases)}"

            for alias, target_role in role_aliases.items():
                assert target_role in roles, (
                    f"In {name} index: alias '@{alias}' targets unregistered role '{target_role}'"
                )
                role_file = REPO_ROOT / roles[target_role]["file"]
                assert role_file.is_file(), (
                    f"In {name} index: alias '@{alias}' targets role '{target_role}' but file missing: {role_file}"
                )

    def test_exhaustive_all_skill_aliases_resolution(self, core_index: dict, adapter_index: dict):
        """Exhaustively verify that ALL skill aliases in both core and adapter registries resolve to valid registered skills with disk files."""
        for name, index_doc in [("core", core_index), ("adapter", adapter_index)]:
            skill_aliases = index_doc.get("skill_aliases", {})
            skills = index_doc.get("skills", {})
            assert len(skill_aliases) >= 200, f"{name} skill_aliases count unexpectedly low: {len(skill_aliases)}"

            for alias, target_skills in skill_aliases.items():
                assert isinstance(target_skills, list) and len(target_skills) > 0, (
                    f"In {name} index: alias '@{alias}' does not map to a non-empty list: {target_skills}"
                )
                for skill_id in target_skills:
                    assert skill_id in skills, (
                        f"In {name} index: alias '@{alias}' targets unregistered skill '{skill_id}'"
                    )
                    skill_file = REPO_ROOT / skills[skill_id]["file"]
                    assert skill_file.is_file(), (
                        f"In {name} index: alias '@{alias}' targets skill '{skill_id}' but file missing: {skill_file}"
                    )



# ==============================================================================
# 5. AGENT CARD & ACTION BOUNDARIES POLICY VERIFICATION
# ==============================================================================

class TestVietnamLegalAgentCardAndPolicy:
    """Verifies agent card schema compliance and action boundary disjointness."""

    def test_vietnam_legal_counsel_agent_card(self):
        """vietnam-legal-counsel.agent-card.json must exist, be valid JSON, and meet A2A 1.0 standard."""
        card_path = REGISTRY_DIR / "vietnam-legal-counsel.agent-card.json"
        assert card_path.is_file()
        card = load_json(card_path)

        # Validate agent card against agent-card.json schema
        agent_card_schema = load_json(SCHEMAS_DIR / "agent-card.json")
        Draft202012Validator(agent_card_schema).validate(card)

        assert card.get("contract_type") == "agent-card"
        assert card.get("name") == "vietnam-legal-counsel"
        assert card.get("protocol_version") == "1.0"
        assert card.get("id") == "pack://agent-skills/core/roles/vietnam-legal-counsel"
        assert card.get("role_file") == "core/roles/vietnam-legal-counsel.md"
        assert card.get("policy_profile") == "vietnam-legal-counsel"

        # Verify skills list contains manage-vietnam-legal
        skills = card.get("skills", [])
        skill_ids = [s.get("id") for s in skills]
        assert "manage-vietnam-legal" in skill_ids

        # Verify defaultOutputSchemas contains both legal contracts
        output_schemas = card.get("defaultOutputSchemas", [])
        assert "legal-compliance-review.json" in output_schemas
        assert "legal-opinion-contract.json" in output_schemas

    def test_action_boundaries_policy_verification(self):
        """action-boundaries.yaml must contain vietnam-legal-counsel with strictly disjoint tiers."""
        policy_path = POLICIES_DIR / "action-boundaries.yaml"
        policy = load_yaml(policy_path)
        roles = policy.get("roles", {})

        assert "vietnam-legal-counsel" in roles, "vietnam-legal-counsel must have a profile in action-boundaries.yaml"
        profile = roles["vietnam-legal-counsel"]

        allowed = set(profile.get("allowed", []))
        requires_approval = set(profile.get("requires_approval", []))
        denied = set(profile.get("denied", []))

        # 1. Non-empty tiers
        assert len(allowed) > 0, "allowed list must not be empty"
        assert len(requires_approval) > 0, "requires_approval list must not be empty"
        assert len(denied) > 0, "denied list must not be empty"

        # 2. Strict pairwise disjointness (zero overlap between tiers)
        overlap_ar = allowed & requires_approval
        overlap_ad = allowed & denied
        overlap_rd = requires_approval & denied

        assert overlap_ar == set(), f"Tiers allowed and requires_approval overlap: {overlap_ar}"
        assert overlap_ad == set(), f"Tiers allowed and denied overlap: {overlap_ad}"
        assert overlap_rd == set(), f"Tiers requires_approval and denied overlap: {overlap_rd}"

        # 3. Irreversible actions standard: Never allowed
        never_allowed_actions = {
            "apply_iac",
            "delete_branch_main",
            "drop_database",
            "drop_storage_volume",
            "force_push",
            "modify_secrets",
            "push_to_production",
            "run_migration",
            "terminate_instance",
        }
        for na in never_allowed_actions:
            assert na not in allowed, f"Irreversible action '{na}' cannot be pre-authorized under allowed"

        # 4. Mandatory AI guardrail check
        assert "bypass_ai_guardrail" in denied, "bypass_ai_guardrail must be strictly denied"

        # 5. Domain-specific legal guardrails
        assert "direct unauthorized litigation representation in court without power of attorney" in denied
        assert "executing binding corporate contracts without legal representative authorization" in denied
        assert "issuing binding legal opinions to third parties" in requires_approval
        assert "filing regulatory reports to government agencies (e.g. A05 MPS)" in requires_approval


# ==============================================================================
# 6. ARTIFACT EXISTENCE & STRUCTURE TESTS
# ==============================================================================

class TestVietnamLegalArtifactStructure:
    """Verifies physical presence, byte lengths, section structures, and checklists."""

    def test_research_dossier_existence_and_size(self):
        """reports/vietnam-legal-counsel-repo-research.md must exist, be >= 100,000 bytes, and cite key laws."""
        dossier_path = REPORTS_DIR / "vietnam-legal-counsel-repo-research.md"
        assert dossier_path.is_file(), f"Research report missing at {dossier_path}"

        byte_size = dossier_path.stat().st_size
        assert byte_size >= 100_000, f"Research report must be >= 100,000 bytes, got {byte_size} bytes"

        content = dossier_path.read_text(encoding="utf-8")
        # Verify citation of core statutory pillars
        required_statutes = [
            ("Doanh nghiệp 2020", "Law on Enterprises 2020"),
            ("Dân sự 2015", "Civil Code 2015"),
            ("Thương mại 2005", "Commercial Law 2005"),
            ("Lao động 2019", "Labor Code 2019"),
            ("13/2023/NĐ-CP", "Decree 13/2023/ND-CP"),
            ("An ninh mạng 2018", "Law on Cybersecurity 2018"),
            ("Trọng tài thương mại 2010", "VIAC"),
        ]
        for vn_term, en_term in required_statutes:
            assert (vn_term in content or en_term in content), (
                f"Research report missing citation for {vn_term} / {en_term}"
            )

    def test_role_specification_structure_and_sections(self):
        """core/roles/vietnam-legal-counsel.md must adhere to role-standard with all required sections."""
        role_path = ROLES_DIR / "vietnam-legal-counsel.md"
        assert role_path.is_file(), f"Role file missing at {role_path}"

        content = role_path.read_text(encoding="utf-8")

        required_headers = [
            "# Vietnam Legal Counsel",
            "Mission:",
            "Level: Principal / Master Legal Leadership",
            "## Principal Expectations",
            "## Use This Role When",
            "## Core Responsibilities",
            "## Inputs Required",
            "## Outputs Produced",
            "## Deliverable Routing",
            "## Decision Boundaries",
            "## Role Boundaries",
            "## Collaboration",
            "## Guardrails",
            "## Skill Toolbox",
            "## Output Template",
            "## Review Checklist",
            "## Anti-Patterns To Reject",
            "## Role Handoff",
            "## Definition Of Done",
        ]
        for header in required_headers:
            assert header in content, f"Role file missing required section: '{header}'"

        # Verify Skill Toolbox Lock
        assert "manage-vietnam-legal" in content
        assert "conduct-research" in content
        assert "analyze-business-requirements" in content
        assert "security-audit" in content
        assert "write-documentation" in content
        assert "agent-delegation" in content

        # Verify Guardrail Locks
        assert "NO-EXTERNAL-LEGAL-REPRESENTATION LOCK" in content
        assert "HUMAN-IN-THE-LOOP (HITL) GATE LOCK" in content
        assert "PENALTY-CAP-DIFFERENTIATION LOCK" in content

    def test_skill_definition_structure_and_line_count(self):
        """core/skills/legal-compliance/manage-vietnam-legal/SKILL.md must be < 200 lines with valid frontmatter."""
        skill_path = SKILLS_DIR / "legal-compliance" / "manage-vietnam-legal" / "SKILL.md"
        assert skill_path.is_file(), f"Skill file missing at {skill_path}"

        lines = skill_path.read_text(encoding="utf-8").splitlines()
        line_count = len(lines)
        assert line_count < 200, f"SKILL.md must be under 200 lines, got {line_count}"

        # Frontmatter validation
        assert lines[0] == "---", "SKILL.md must begin with YAML frontmatter delimiter '---'"
        closing_idx = -1
        for i in range(1, len(lines)):
            if lines[i] == "---":
                closing_idx = i
                break
        assert closing_idx != -1, "Frontmatter closing delimiter '---' not found"

        frontmatter_text = "\n".join(lines[1:closing_idx])
        fm = yaml.safe_load(frontmatter_text)
        assert fm.get("name") == "manage-vietnam-legal"
        assert "allowed-tools" in fm and len(fm["allowed-tools"]) > 0

        # Required skill sections
        full_content = "\n".join(lines)
        assert "# Manage Vietnam Legal" in full_content
        assert "## Core Rules" in full_content
        assert "## Output Contracts" in full_content
        assert "## Suggested Process" in full_content
        assert "## Failure Modes" in full_content
        assert "## Security Guardrails" in full_content
        assert "## Checklist" in full_content

    def test_statutory_checklists_reference_existence(self):
        """references/statutory-checklists.md must exist and contain detailed vetting rubrics."""
        ref_path = SKILLS_DIR / "legal-compliance" / "manage-vietnam-legal" / "references" / "statutory-checklists.md"
        assert ref_path.is_file(), f"Reference checklist missing at {ref_path}"

        content = ref_path.read_text(encoding="utf-8")
        assert len(content) > 1000, "statutory-checklists.md should contain detailed reference rubrics"
        assert "Article 301" in content
        assert "Decree 13/2023/ND-CP" in content
        assert "Law on Enterprises 2020" in content

    def test_catalog_documentation_cross_referencing(self):
        """Role, skill, and contract READMEs must cross-reference legal pack deliverables."""
        # 1. core/roles/README.md
        roles_readme = (ROLES_DIR / "README.md").read_text(encoding="utf-8")
        assert "vietnam-legal-counsel" in roles_readme

        # 2. core/skills/README.md
        skills_readme = (SKILLS_DIR / "README.md").read_text(encoding="utf-8")
        assert "manage-vietnam-legal" in skills_readme
        assert ("Legal Compliance (1)" in skills_readme or "Legal Compliance (3)" in skills_readme)

        # 3. core/contracts/README.md
        contracts_readme = (CORE_DIR / "contracts" / "README.md").read_text(encoding="utf-8")
        assert "legal-compliance-review.json" in contracts_readme
        assert "legal-opinion-contract.json" in contracts_readme

        # 4. core/contracts/schemas/INDEX.md
        schemas_index = (SCHEMAS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "legal-compliance-review.json" in schemas_index
        assert "legal-opinion-contract.json" in schemas_index
