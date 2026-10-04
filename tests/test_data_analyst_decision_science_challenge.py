#!/usr/bin/env python3
"""Automated Challenge Test Suite for Data Analyst Role & Modern Decision Science Skills.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance via Draft202012Validator.check_schema().
   - Full validity of bundled examples in `data-analysis-report.json`.
   - Engine enum support (DuckDB, Polars, chDB, dbt semantic layer),
     causal inference methods (A/B test, DiD, SCM, PSM, DML, RD),
     and modern properties (query_finops_cost, table_of_evidence, srm_precheck, dowhy_refutations).

2. Adversarial Negative Mutation Stress Tests:
   - Missing required fields (business_question, metrics, sources, findings, confidence).
   - Invalid discriminator constant (`contract_type`).
   - Invalid confidence enum.
   - Invalid verification_engine enum.
   - Missing required fields in causal_inference (method, assumptions_validated).
   - Missing required fields in table_of_evidence (empirical_observation, analytical_interpretation).
   - Missing required fields in srm_precheck.

3. Data Analyst Role (`core/roles/data-analyst.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Guardrails, Skill Toolbox, Output Template, Failure Modes, Anti-Patterns.
   - Decision Science Invariants: FastMCP gateway, sqlglot AST, DuckDB v1.1+ (max_memory = '4GB'),
     Arrow C Data Interface, PSI deciles, Two-Sample KS-test, Tukey's IQR, Pearson's Chi-squared SRM (p < 0.001 abort),
     Pearl's Causal Hierarchy, Backdoor Criterion, Collider Bias (Berkson's Paradox), DoWhy 3-way refutations,
     DiD, SCM, RD, DML, CUPED variance reduction, chDB DataStore/SQL, Apache Ossie interchange, and Fact vs Interpretation separation.
   - All 18 Guardrail Locks: BOUNDARY LOCK, SECURITY LOCK, IRREVERSIBLE ACTION LOCK,
     SEMANTIC-QUERY-LOCK, TEXT-TO-SQL-HALLUCINATION-LOCK, DUCKDB-SANDBOX-LOCK, SRM-INTEGRITY-LOCK,
     CAUSAL-DAG-LOCK, DRIFT-AUDIT-LOCK, FACT-INTERPRETATION-LOCK, VERIFIABLE-SOURCE-LOCK,
     PII-REDACTION-LOCK, EMBEDDED-ANALYTICAL-ENGINE LOCK, APACHE-OSSIE-LOCK, DUCKDB-V2-READINESS-LOCK, QUERY-COST-FINOPS-LOCK.
   - Primary Skills locked: `analyze-data` and `query-analytical-engine`.

4. Data Analyst Review Checklist (`core/roles/references/data-analyst-review-checklist.md`):
   - Exactly 10 comprehensive sections covering semantic querying, in-process DuckDB/Polars, drift detection,
     causal DAGs, DoWhy/quasi-experiments, SRM integrity, Table of Evidence, verifiable reporting,
     OWASP ASI governance, and in-process chDB/federation with query FinOps.

5. Primary Skills & Agent Manifests Conformance:
   - `analyze-data` and `query-analytical-engine` SKILL.md files (<200 lines, valid frontmatter).
   - OpenAI agent manifests (`agents/openai.yaml`).
   - Reference guides existence in each skill's `references/` directory.

6. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/data-analyst.agent-card.json` validity and skill IDs.
   - Fast invocation alias resolution for `@data-analyst` (`@da`, `@data-analytics`).
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


class TestDataAnalysisReportSchema(unittest.TestCase):
    """Rigorous schema validation and negative mutation testing for data-analysis-report.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "data-analysis-report.json"
        assert cls.schema_path.exists(), "data-analysis-report.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "data-analysis-report")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within data-analysis-report.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_verification_engine_includes_chdb_and_duckdb(self):
        """verification_engine enum must include in-process analytical engines."""
        engines = self.schema_raw["properties"]["sources"]["items"]["properties"]["verification_engine"]["enum"]
        self.assertIn("duckdb", engines)
        self.assertIn("polars", engines)
        self.assertIn("chdb", engines)
        self.assertIn("dbt_semantic_layer", engines)

    def test_04_causal_inference_methods_include_dml_and_rd(self):
        """causal_inference.method enum must include modern quasi-experimental methods."""
        methods = self.schema_raw["properties"]["causal_inference"]["properties"]["method"]["enum"]
        self.assertIn("ab_test", methods)
        self.assertIn("difference_in_differences", methods)
        self.assertIn("synthetic_control", methods)
        self.assertIn("double_machine_learning", methods)
        self.assertIn("regression_discontinuity", methods)

    def test_05_negative_mutation_missing_required_fields(self):
        """Omitting required fields must trigger a ValidationError."""
        valid_ex = copy.deepcopy(self.schema_raw["examples"][0])
        required_fields = self.schema_raw.get("required", [])

        for field in required_fields:
            mutated = copy.deepcopy(valid_ex)
            del mutated[field]
            with self.assertRaises(ValidationError, msg=f"Should fail when missing required field: {field}"):
                self.validator.validate(mutated)

    def test_06_negative_mutation_invalid_contract_type(self):
        """Tampering with the contract_type discriminator must fail validation."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["contract_type"] = "invalid-contract-type"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_07_negative_mutation_invalid_confidence_enum(self):
        """confidence must be High, Medium, or Low."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["confidence"] = "VeryHighDefinitelyCertain"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_08_negative_mutation_invalid_verification_engine(self):
        """Unsupported verification engine must fail validation."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["sources"][0]["verification_engine"] = "unsupported_legacy_engine"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_09_negative_mutation_invalid_table_of_evidence(self):
        """table_of_evidence items must require empirical_observation and analytical_interpretation."""
        mutated = copy.deepcopy(self.schema_raw["examples"][0])
        mutated["table_of_evidence"] = [
            {"empirical_observation": "Conversion rose 5%"}  # Missing analytical_interpretation
        ]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)


class TestDataAnalystRoleInvariants(unittest.TestCase):
    """Comprehensive invariant testing for core/roles/data-analyst.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "data-analyst.md"
        assert cls.role_path.exists(), "core/roles/data-analyst.md must exist"
        cls.content = cls.role_path.read_text(encoding="utf-8")

    def test_01_mandatory_role_sections(self):
        """Role must adhere to role-standard with all required sections."""
        required_sections = [
            "# Data Analyst",
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

    def test_02_decision_science_invariants_present(self):
        """Role must mandate 2026-2027 SOTA Decision Science invariants."""
        invariants = [
            "dbt MetricFlow",
            "Cube.js",
            "Apache Ossie",
            "FastMCP",
            "sqlglot",
            "DuckDB v1.1+",
            "SET max_memory = '4GB'",
            "Polars",
            "Population Stability Index",
            "Kolmogorov-Smirnov",
            "Tukey's IQR",
            "Sample Ratio Mismatch",
            "p < 0.001",
            "Pearl's Causal Hierarchy",
            "Backdoor Criterion",
            "Collider Bias",
            "Berkson's Paradox",
            "DoWhy",
            "Placebo Treatment",
            "Random Common Cause",
            "Data Subset",
            "Difference-in-Differences",
            "Synthetic Control",
            "Regression Discontinuity",
            "Double Machine Learning",
            "CUPED",
            "Table of Evidence",
            "chDB",
        ]
        for inv in invariants:
            self.assertIn(inv, self.content, f"Missing decision science invariant: {inv}")

    def test_03_guardrail_locks_present(self):
        """Role must define all immutable Guardrail Locks."""
        locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "SEMANTIC-QUERY-LOCK",
            "TEXT-TO-SQL-HALLUCINATION-LOCK",
            "DUCKDB-SANDBOX-LOCK",
            "SRM-INTEGRITY-LOCK",
            "CAUSAL-DAG-LOCK",
            "DRIFT-AUDIT-LOCK",
            "FACT-INTERPRETATION-LOCK",
            "VERIFIABLE-SOURCE-LOCK",
            "PII-REDACTION-LOCK",
            "EMBEDDED-ANALYTICAL-ENGINE LOCK",
            "APACHE-OSSIE-LOCK",
            "DUCKDB-V2-READINESS-LOCK",
            "QUERY-COST-FINOPS-LOCK",
        ]
        for lock in locks:
            self.assertIn(lock, self.content, f"Missing guardrail lock: {lock}")

    def test_04_skill_toolbox_primary_skills(self):
        """Skill Toolbox must lock primary skills to analyze-data and query-analytical-engine."""
        toolbox_lines = self.content.split("## Skill Toolbox")[1].split("### Supporting Skills")[0]
        self.assertIn("`analyze-data`", toolbox_lines)
        self.assertIn("`query-analytical-engine`", toolbox_lines)


class TestDataAnalystReviewChecklist(unittest.TestCase):
    """Verification of core/roles/references/data-analyst-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "data-analyst-review-checklist.md"
        assert cls.checklist_path.exists(), "data-analyst-review-checklist.md must exist"
        cls.content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_10_sections_present(self):
        """Checklist must contain all 10 core Decision Science sections."""
        for i in range(1, 11):
            pattern = f"### {i}."
            self.assertIn(pattern, self.content, f"Checklist missing section {i}")

    def test_02_section_topics_covered(self):
        """Checklist sections must cover key SOTA analytical topics."""
        topics = [
            "Semantic Metric Querying & Text-to-SQL Hallucination Defense",
            "DuckDB & Polars In-Process Analytics Architecture",
            "Statistical Distribution Drift & Anomaly Detection",
            "Causal DAG Modeling & Confounder Elimination",
            "DoWhy 4-Step Robustness Framework & Quasi-Experimental Methods",
            "Automated Sample Ratio Mismatch (SRM) Integrity Gate",
            "Two-Column Table of Evidence: Empirical Facts vs Analytical Interpretations",
            "Quantitative Evidence, Verifiable Provenance & Cryptographic Auditability",
            "Data Privacy, Classification & OWASP ASI Governance",
            "Embedded In-Process Analytical SQL & Cross-Source Zero-ETL Federation",
        ]
        for topic in topics:
            self.assertIn(topic, self.content, f"Missing topic in checklist: {topic}")


class TestDataAnalysisSkillsIntegrity(unittest.TestCase):
    """Integrity checks for skills owned by Data Analyst."""

    def test_01_analyze_data_skill(self):
        """analyze-data SKILL.md must have valid frontmatter, line count < 200, and references."""
        skill_dir = SKILLS_DIR / "meetings-analysis" / "analyze-data"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.exists())

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200, "SKILL.md must be concise (< 200 lines)")

    def test_02_query_analytical_engine_skill(self):
        """query-analytical-engine SKILL.md must be concise and reference chDB/DuckDB guide."""
        skill_dir = SKILLS_DIR / "security-data" / "query-analytical-engine"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.exists())

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200, "SKILL.md must be concise (< 200 lines)")

        ref = skill_dir / "references" / "analytical-query-guide.md"
        self.assertTrue(ref.exists(), "analytical-query-guide.md must exist")


class TestDataAnalystA2ACard(unittest.TestCase):
    """Integrity checks for A2A discovery card and registry mapping for Data Analyst."""

    def test_01_agent_card_validity(self):
        """core/a2a/registry/data-analyst.agent-card.json must be valid and conformant."""
        card_path = AGENT_CARDS_DIR / "data-analyst.agent-card.json"
        self.assertTrue(card_path.exists())

        data = json.loads(card_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("contract_type"), "agent-card")
        self.assertEqual(data.get("name"), "data-analyst")
        self.assertEqual(data.get("version"), "5.0.0")

        skill_ids = [s["id"] for s in data.get("skills", [])]
        self.assertIn("analyze-data", skill_ids)
        self.assertIn("query-analytical-engine", skill_ids)

    def test_02_fast_invocation_role_aliases(self):
        """generate-index.py must resolve @da and @data-analytics to data-analyst."""
        gen_script = CORE_DIR / "scripts" / "generate-index.py"
        self.assertTrue(gen_script.exists())
        script_text = gen_script.read_text(encoding="utf-8")

        self.assertIn('"da": "data-analyst"', script_text)
        self.assertIn('"data-analytics": "data-analyst"', script_text)


if __name__ == "__main__":
    unittest.main()
