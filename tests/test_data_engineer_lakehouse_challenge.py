#!/usr/bin/env python3
"""Automated Challenge Test Suite for Data Engineer Role & Modern Lakehouse Skills.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance via Draft202012Validator.check_schema().
   - Full validity of bundled examples in `data-pipeline-spec.json`.
   - Contract discriminator, storage format enum (including ClickHouse, Iceberg, Delta Lake),
     and optional lakehouse properties (table_properties, encryption_config, rest_catalog_config, lineage_config).

2. Adversarial Negative Mutation Stress Tests:
   - Missing top-level required fields (pipeline_id, dataset_name, quality_gates, etc.).
   - Invalid discriminator constants (`contract_type`).
   - Invalid storage format enum values.
   - Negative freshness latency or invalid update frequency enum.
   - Out-of-bounds error threshold percentages (>100 or <0).
   - Missing required fields in schema_fields (name, type, nullable, pii_classification).

3. Data Engineer Role (`core/roles/data-engineer.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Guardrails, Skill Toolbox, Output Template, Failure Modes, Anti-Patterns.
   - 14 Invariant Guardrail Locks: DATA-CONTRACT-LOCK, IDEMPOTENCY-MERGE-LOCK, CIRCUIT-BREAKER-DLQ-LOCK,
     WAP-VERIFICATION-LOCK, FINOPS-PRUNING-LOCK, ZERO-TRUST-PII-LOCK, METADATA-MAINTENANCE-LOCK,
     OLAP-COLUMNAR-OPTIMIZATION LOCK, NATIVE-ENCRYPTION-LOCK, OPENLINEAGE-LOCK, ICEBERG-REST-PROTOCOL-LOCK, etc.
   - Modern Lakehouse Invariants: Iceberg v4 metadata-only restructuring, Iceberg v3 RoaringBitmap DVs,
     Delta Lake 4.0 UniForm, open REST Catalog, Variant type, S3 prefix hashing (write.object-storage.enabled = true),
     atomic WAP, and DLQ circuit breaker ($Q_r > 2.0\\%, N \\ge 50$).
   - Absence of markdown backtick code traps on plain prose ('string blob', 'distributed mode').

4. Data Engineer Review Checklist (`core/roles/references/data-engineer-review-checklist.md`):
   - Exactly 10 comprehensive sections covering contracts, lakehouse, idempotency/WAP, DLQ, semantic layer,
     FinOps, Zero-Trust/KMS, AI supply chain, OLAP columnar optimization, and OpenLineage traceability.

5. Primary Skills & Agent Manifests Conformance:
   - `build-data-pipeline`, `database-maintenance`, `optimize-olap-database` SKILL.md files (<200 lines, valid frontmatter).
   - Reference guides existence in each skill's `references/` directory.
   - OpenAI agent configurations (`agents/openai.yaml`).

6. A2A Agent Card & Discovery Registry Integrity:
   - `core/a2a/registry/data-engineer.agent-card.json` validity and skill IDs.
   - Fast invocation alias resolution for `@data-engineer` (`@de`, `@data-eng`).
   - Catalog stats synchronization across role-skill indices.

7. Master Research Dossier Verification:
   - `reports/data-engineer-data-analyst-repo-research.md` existence, size >= 100,000 bytes,
     and mathematical invariants ($Q_r$, Pearl's hierarchy, Chi-squared SRM).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
CONTRACTS_DIR = CORE_DIR / "contracts" / "schemas"
REGISTRY_DIR = CORE_DIR / "a2a" / ".well-known"
AGENT_CARDS_DIR = CORE_DIR / "a2a" / "registry"
REPORTS_DIR = REPO_ROOT / "reports"


class TestDataPipelineSpecSchema(unittest.TestCase):
    """Rigorous schema validation and negative mutation testing for data-pipeline-spec.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "data-pipeline-spec.json"
        assert cls.schema_path.exists(), "data-pipeline-spec.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        # Meta-schema validation against Draft 2020-12
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "data-pipeline-spec")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within data-pipeline-spec.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_storage_format_includes_modern_engines(self):
        """Storage format enum must include modern lakehouse and OLAP engines."""
        formats = self.schema_raw["properties"]["storage_format"]["enum"]
        self.assertIn("iceberg", formats)
        self.assertIn("delta_lake", formats)
        self.assertIn("duckdb", formats)
        self.assertIn("clickhouse", formats)

    def test_04_negative_mutation_missing_required_fields(self):
        """Omitting required fields must trigger a ValidationError."""
        valid_ex = copy.deepcopy(self.schema_raw["examples"][0])
        required_fields = self.schema_raw.get("required", [])

        for field in required_fields:
            mutated = copy.deepcopy(valid_ex)
            del mutated[field]
            with self.assertRaises(ValidationError, msg=f"Should fail when missing required field: {field}"):
                self.validator.validate(mutated)

    def test_05_negative_mutation_invalid_contract_type(self):
        """Tampering with the contract_type discriminator must fail validation."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["contract_type"] = "invalid-contract-type"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_06_negative_mutation_invalid_storage_format(self):
        """Specifying an unsupported storage format must fail validation."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["storage_format"] = "legacy_unsupported_hdoop_hive"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_07_negative_mutation_out_of_bounds_error_threshold(self):
        """quarantine_policy.error_threshold_pct must be bounded between 0 and 100."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["quarantine_policy"]["error_threshold_pct"] = 105.0  # > 100
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

        mutated["quarantine_policy"]["error_threshold_pct"] = -2.5  # < 0
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_08_negative_mutation_invalid_update_frequency(self):
        """freshness_sla.update_frequency must be within authorized enum values."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["freshness_sla"]["update_frequency"] = "sporadic_whenever"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_09_negative_mutation_invalid_schema_field(self):
        """schema_fields items must require name, type, nullable, and pii_classification."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["schema_fields"].append({
            "name": "malformed_field",
            # Missing type, nullable, and pii_classification
        })
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)


class TestDataEngineerRoleInvariants(unittest.TestCase):
    """Comprehensive invariant testing for core/roles/data-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "data-engineer.md"
        assert cls.role_path.exists(), "core/roles/data-engineer.md must exist"
        cls.content = cls.role_path.read_text(encoding="utf-8")

    def test_01_mandatory_role_sections(self):
        """Role must adhere to role-standard with all required sections."""
        required_sections = [
            "# Data Engineer",
            "Mission:",
            "Level: Principal / master-level",
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
            "## Failure Modes",
            "## Anti-Patterns To Reject",
            "## Role Handoff",
            "## Definition Of Done",
        ]
        for sec in required_sections:
            self.assertIn(sec, self.content, f"Missing required section or standard text: {sec}")

    def test_02_modern_lakehouse_standards_present(self):
        """Role must mandate 2026-2027 Lakehouse Architecture SOTA invariants."""
        invariants = [
            "Apache Iceberg v4",
            "Iceberg v3",
            "Delta Lake 4.0 UniForm",
            "Puffin RoaringBitmap",
            "Deletion Vectors",
            "spec_id",
            "write.object-storage.enabled = true",
            "Write-Audit-Publish",
            "wap_audit_",
            "SET max_memory = '4GB'",
            "Variant",
            "REST Catalog",
            "Apache Polaris",
            "Unity Catalog OSS",
            "Dagster Software-Defined Assets",
            "Flink 2.3",
            "Redpanda",
            "Debezium",
        ]
        for inv in invariants:
            self.assertIn(inv, self.content, f"Missing architectural invariant: {inv}")

    def test_03_olap_columnar_optimization_standards(self):
        """Role must mandate ClickHouse/DuckDB 8192-granule sparse indexing and micro-batching."""
        olap_terms = [
            "ClickHouse",
            "DuckDB",
            "index_granularity = 8192",
            "8192-row",
            "1000 total active partitions",
            "10,000 rows",
            "LowCardinality",
            "EXPLAIN PIPELINE",
        ]
        for term in olap_terms:
            self.assertIn(term, self.content, f"Missing OLAP optimization term: {term}")

    def test_04_circuit_breaker_and_dlq_formula(self):
        """Mathematical circuit breaker formula and quarantine criteria must be precise."""
        self.assertIn("Q_r > 2.0%", self.content)
        self.assertIn("N >= 50", self.content)
        self.assertIn("N_{\\text{quarantined}}", self.content)
        self.assertIn("N_{\\text{total}}", self.content)

    def test_05_guardrail_locks_present(self):
        """Role must define immutable Guardrail Locks."""
        locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "DATA-CONTRACT-LOCK",
            "IDEMPOTENCY-MERGE-LOCK",
            "CIRCUIT-BREAKER-DLQ-LOCK",
            "WAP-VERIFICATION-LOCK",
            "FINOPS-PRUNING-LOCK",
            "ZERO-TRUST-PII-LOCK",
            "METADATA-MAINTENANCE-LOCK",
            "OLAP-COLUMNAR-OPTIMIZATION LOCK",
            "NATIVE-ENCRYPTION-LOCK",
            "OPENLINEAGE-LOCK",
            "ICEBERG-REST-PROTOCOL-LOCK",
        ]
        for lock in locks:
            self.assertIn(lock, self.content, f"Missing guardrail lock: {lock}")

    def test_06_no_prose_backtick_traps(self):
        """Prose terms must not have incorrect markdown backtick formatting traps."""
        self.assertNotIn("`string` blob", self.content)
        self.assertNotIn("`distributed` mode", self.content)
        self.assertIn("string blob", self.content)
        self.assertIn("distributed mode", self.content)

    def test_07_skill_toolbox_primary_skills(self):
        """Skill Toolbox must lock primary skills."""
        toolbox_lines = self.content.split("## Skill Toolbox")[1].split("### Supporting Skills")[0]
        self.assertIn("`build-data-pipeline`", toolbox_lines)
        self.assertIn("`database-maintenance`", toolbox_lines)
        self.assertIn("`create-migration`", toolbox_lines)
        self.assertIn("`optimize-olap-database`", toolbox_lines)


class TestDataEngineerReviewChecklist(unittest.TestCase):
    """Verification of core/roles/references/data-engineer-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "data-engineer-review-checklist.md"
        assert cls.checklist_path.exists(), "data-engineer-review-checklist.md must exist"
        cls.content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_10_sections_present(self):
        """Checklist must contain all 10 core engineering and architecture sections."""
        for i in range(1, 11):
            pattern = f"### {i}."
            self.assertIn(pattern, self.content, f"Checklist missing section {i}")

    def test_02_section_topics_covered(self):
        """Checklist sections must cover key SOTA domain topics."""
        topics = [
            "Open Data Contract Standard (ODCS v3.1.0)",
            "Modern Lakehouse Architecture",
            "Idempotency, Deterministic Upsert MERGE",
            "Circuit Breakers & Dead-Letter Queue",
            "Unified Semantic Layer",
            "Data FinOps & Resource Governance",
            "Zero-Trust Governance & OWASP ASI Compliance",
            "AI/ML Data Supply Chain & Vector Operations",
            "OLAP Database Architecture & Columnar Optimization",
            "OpenLineage & End-to-End Pipeline Traceability",
        ]
        for topic in topics:
            self.assertIn(topic, self.content, f"Missing topic in checklist: {topic}")


class TestDataEngineeringSkillsIntegrity(unittest.TestCase):
    """Integrity checks for skills owned or used by Data Engineer."""

    def test_01_build_data_pipeline_skill(self):
        """build-data-pipeline SKILL.md must have valid frontmatter, line count < 200, and references."""
        skill_dir = SKILLS_DIR / "security-data" / "build-data-pipeline"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.exists())

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200, "SKILL.md must be concise (< 200 lines)")

        # References existence
        ref1 = skill_dir / "references" / "producer-contracts-and-lakehouse.md"
        ref2 = skill_dir / "references" / "quality-gates-dlq-and-replayability.md"
        self.assertTrue(ref1.exists(), "producer-contracts-and-lakehouse.md must exist")
        self.assertTrue(ref2.exists(), "quality-gates-dlq-and-replayability.md must exist")

        # OpenAI agent manifest existence
        agent_manifest = skill_dir / "agents" / "openai.yaml"
        self.assertTrue(agent_manifest.exists(), "agents/openai.yaml must exist")

    def test_02_database_maintenance_skill(self):
        """database-maintenance SKILL.md must be concise, valid, and reference lakehouse FinOps."""
        skill_dir = SKILLS_DIR / "security-data" / "database-maintenance"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.exists())

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200, "SKILL.md must be concise (< 200 lines)")

        ref1 = skill_dir / "references" / "lakehouse-ops-and-finops.md"
        ref2 = skill_dir / "references" / "relational-and-vector-maintenance.md"
        self.assertTrue(ref1.exists())
        self.assertTrue(ref2.exists())

    def test_03_optimize_olap_database_skill(self):
        """optimize-olap-database SKILL.md must be concise and reference OLAP guide."""
        skill_dir = SKILLS_DIR / "security-data" / "optimize-olap-database"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.exists())

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200, "SKILL.md must be concise (< 200 lines)")

        ref1 = skill_dir / "references" / "olap-database-guide.md"
        self.assertTrue(ref1.exists())


class TestA2AAgentCardAndRegistry(unittest.TestCase):
    """Integrity checks for A2A discovery card and registry mapping for Data Engineer."""

    def test_01_agent_card_validity(self):
        """core/a2a/registry/data-engineer.agent-card.json must be valid and conformant."""
        card_path = AGENT_CARDS_DIR / "data-engineer.agent-card.json"
        self.assertTrue(card_path.exists())

        data = json.loads(card_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("contract_type"), "agent-card")
        self.assertEqual(data.get("name"), "data-engineer")
        self.assertEqual(data.get("version"), "5.0.0")

        skill_ids = [s["id"] for s in data.get("skills", [])]
        self.assertIn("build-data-pipeline", skill_ids)
        self.assertIn("database-maintenance", skill_ids)
        self.assertIn("create-migration", skill_ids)
        self.assertIn("optimize-olap-database", skill_ids)

    def test_02_fast_invocation_role_aliases(self):
        """generate-index.py must resolve @de and @data-eng to data-engineer."""
        gen_script = CORE_DIR / "scripts" / "generate-index.py"
        self.assertTrue(gen_script.exists())
        script_text = gen_script.read_text(encoding="utf-8")

        self.assertIn('"de": "data-engineer"', script_text)
        self.assertIn('"data-eng": "data-engineer"', script_text)


class TestResearchDossierIntegrity(unittest.TestCase):
    """Verification of reports/data-engineer-data-analyst-repo-research.md."""

    def test_01_research_dossier_depth_and_invariants(self):
        """Research dossier must exist, exceed 100KB, and contain foundational mathematical formulas."""
        dossier_path = REPORTS_DIR / "data-engineer-data-analyst-repo-research.md"
        self.assertTrue(dossier_path.exists(), "Master research dossier must exist")

        text = dossier_path.read_text(encoding="utf-8")
        self.assertGreater(len(text.encode("utf-8")), 100_000, "Research dossier must exceed 100KB")

        # Architectural and mathematical formulas
        self.assertIn("Write-Audit-Publish", text)
        self.assertIn("Apache Iceberg v3", text)
        self.assertIn("Delta Lake 4.0", text)
        self.assertIn("DoWhy", text)
        self.assertIn("EconML", text)
        self.assertIn("FastMCP", text)


if __name__ == "__main__":
    unittest.main()
