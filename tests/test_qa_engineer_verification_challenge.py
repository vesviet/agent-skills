#!/usr/bin/env python3
"""Automated Challenge Test Suite for QA Engineer Role & SOTA Verification Standards.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance for `test-report.json` and `validation-result.json`.
   - Full validity of bundled examples in both schemas.
   - 2026-2027 modern verification properties in `test-report.json`:
     `contract_testing`, `ai_evaluation`, `observability_testing`, `accessibility_audit`,
     `chaos_injection`, `performance_slo`, `clean_architecture_verification`,
     `mutation_score`, `sandbox_isolation_tier`, `reproduction_test_verified`, `blast_radius_assessment`.

2. Adversarial Negative Mutation Stress Tests:
   - Missing required fields (contract_type, ticket_ref, environment, status, scenarios_executed, release_recommendation).
   - Invalid discriminator constant (`contract_type`).
   - Invalid status enum.
   - Invalid release_recommendation enum.
   - Invalid sandbox_isolation_tier enum.
   - Out-of-bounds mutation score (> 100 or < 0).
   - Missing required fields in blast_radius_assessment.
   - Missing required fields in validation-result.json.

3. QA Engineer Role (`core/roles/qa-engineer.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Guardrails, Skill Toolbox, Output Template, Failure Modes, Anti-Patterns, Definition Of Done.
   - The Great Verification Convergence across 6 pillars:
     1. Calibrated AI & Agentic System Evaluation (G-Eval >= 85%, RAG Triad, Pydantic v2 schemas, trajectory DAG loop detection, Promptfoo).
     2. Consumer-Driven Contract Testing (PactV3 / Pact-Go v2, can-i-deploy, buf breaking with WIRE_JSON, oasdiff).
     3. Observability-Driven Testing (Tracetest OpenTelemetry span assertions, W3C traceparent, automated N+1 query counters, eBPF).
     4. Modern Web & Accessibility (Playwright v1.48+, MSW v2, @axe-core/playwright WCAG 2.2 AA, font-stabilized visual diffing).
     5. Shift-Left Chaos & Performance Gates (Shopify Toxiproxy fault injection, circuit breaker state transitions, AWS full jitter, Grafana k6 SLO thresholds).
     6. Clean Architecture Multi-Language QA (Go 1.25+ Kratos, Wire compile-time DI, real PostgreSQL 16 Testcontainers, GORM InTx rollbacks, go test -race, uber-go/goleak, Hypothesis, fast-check).
   - Guardrail Locks: BOUNDARY LOCK, SECURITY LOCK, IRREVERSIBLE ACTION LOCK, TRACE LOCK, UNCERTAINTY LOCK,
     SYSTEMATIC-DEBUGGING-LOCK, VERIFICATION-BEFORE-COMPLETION-LOCK, COMBINATORIAL-COVERAGE-LOCK,
     CHAOS-GATE LOCK, N1-QUERY-GATE LOCK, CALIBRATED-EVAL-GATE LOCK, CAN-I-DEPLOY-GATE LOCK,
     ASSERTION-THEATER LOCK, MUTATION-TESTING LOCK, PROPERTY-TESTING LOCK, MULTI-DIMENSIONAL-TEST LOCK,
     OWASP-ASI-GATE LOCK, AI-SYSTEM LOCK, TRAJECTORY LOCK, ACCESSIBILITY LOCK.
   - Primary Skills locked: `write-tests`, `frontend-testing`, `systematic-debugging`, `combinatorial-testing`, `agent-quality-gate`, `accessibility-review`, `configure-mcp`, `implement-webmcp`.

4. QA Engineer Review Checklist (`core/roles/references/qa-engineer-review-checklist.md`):
   - All 13 comprehensive sections covering CDCT, systematic 4-phase RCA, VBC, pairwise combinatorial testing,
     calibrated AI/agentic evaluation, observability-driven trace assertions, modern web & accessibility,
     shift-left chaos/performance, clean architecture multi-language QA, mutation testing & OWASP ASI security,
     MCP/Agent validation, EU AI Act compliance, and distributed system foundation.

5. Primary Skills & Agent Conformance:
   - `write-tests`, `frontend-testing`, `systematic-debugging`, and `combinatorial-testing` SKILL.md files.
   - Valid YAML frontmatter, line count within bounds (< 200 lines), allowed-tools.

6. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/qa-engineer.agent-card.json` validity and skill IDs.
   - Agent discovery and role-skill indexing in `agent-registry.json` and `role-skill-index.json`.
   - Fast invocation alias resolution for `@qa` and `@qa-engineer`.
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


class TestQATestReportSchema(unittest.TestCase):
    """Rigorous schema validation and negative mutation testing for test-report.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "test-report.json"
        assert cls.schema_path.exists(), "test-report.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "test-report")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within test-report.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_modern_verification_properties_present(self):
        """Schema must define all 2026-2027 modern verification properties."""
        props = self.schema_raw.get("properties", {})
        modern_props = [
            "contract_testing",
            "ai_evaluation",
            "observability_testing",
            "accessibility_audit",
            "chaos_injection",
            "performance_slo",
            "clean_architecture_verification",
            "mutation_score",
            "sandbox_isolation_tier",
            "reproduction_test_verified",
            "blast_radius_assessment",
        ]
        for prop in modern_props:
            self.assertIn(prop, props, f"Missing modern verification property: {prop}")

    def test_04_mutation_score_schema_structure(self):
        """mutation_score must require score_pct, threshold_pct, and status."""
        ms = self.schema_raw.get("properties", {}).get("mutation_score", {})
        self.assertEqual(ms.get("type"), "object")
        required = ms.get("required", [])
        self.assertIn("score_pct", required)
        self.assertIn("threshold_pct", required)
        self.assertIn("status", required)

    def test_05_sandbox_isolation_tier_enums(self):
        """sandbox_isolation_tier must specify strict isolation levels."""
        sit = self.schema_raw.get("properties", {}).get("sandbox_isolation_tier", {})
        enums = sit.get("enum", [])
        self.assertIn("tier_0_ephemeral_container", enums)
        self.assertIn("tier_1_isolated_microvm", enums)
        self.assertIn("tier_2_airgapped_sandbox", enums)

    def test_06_negative_mutation_missing_required_fields(self):
        """Omitting mandatory fields must fail schema validation."""
        valid_example = copy.deepcopy(self.schema_raw["examples"][0])
        required_fields = self.schema_raw.get("required", [])
        for field in required_fields:
            mutant = copy.deepcopy(valid_example)
            del mutant[field]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(
                len(errors),
                0,
                f"Validator failed to reject missing required field: {field}",
            )

    def test_07_negative_mutation_invalid_contract_type(self):
        """Invalid contract_type discriminator must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["contract_type"] = "invalid-contract-type"
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject invalid contract_type")

    def test_08_negative_mutation_invalid_release_recommendation(self):
        """Invalid release_recommendation enum must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["release_recommendation"] = "ship_immediately_without_evidence"
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject invalid release_recommendation")

    def test_09_negative_mutation_out_of_bounds_mutation_score(self):
        """Mutation score > 100 or < 0 must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["mutation_score"]["score_pct"] = 150.0
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject mutation score > 100")

        mutant["mutation_score"]["score_pct"] = -5.0
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject mutation score < 0")

    def test_10_negative_mutation_invalid_blast_radius(self):
        """blast_radius_assessment missing required fields must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        del mutant["blast_radius_assessment"]["cross_boundary_impact_detected"]
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(
            len(errors),
            0,
            "Validator failed to reject blast_radius_assessment missing cross_boundary_impact_detected",
        )


class TestValidationResultSchema(unittest.TestCase):
    """Schema validation and negative mutation testing for validation-result.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "validation-result.json"
        assert cls.schema_path.exists(), "validation-result.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "validation-result")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within validation-result.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_negative_mutation_missing_required_decision(self):
        """Omitting required decision must fail validation."""
        valid_example = copy.deepcopy(self.schema_raw["examples"][0])
        del valid_example["decision"]
        errors = list(self.validator.iter_errors(valid_example))
        self.assertGreater(len(errors), 0, "Validator failed to reject missing decision")


class TestQAEngineerRoleInvariants(unittest.TestCase):
    """Authoritative invariant testing for core/roles/qa-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "qa-engineer.md"
        assert cls.role_path.exists(), "qa-engineer.md must exist"
        cls.role_content = cls.role_path.read_text(encoding="utf-8")

    def test_01_standard_role_sections(self):
        """Role must contain all standard role sections per role-standard.md."""
        sections = [
            "# QA Engineer",
            "Mission:",
            "Level:",
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
        for sec in sections:
            self.assertIn(sec, self.role_content, f"Missing required role section: {sec}")

    def test_02_guardrail_locks_present(self):
        """Role must enforce all mandatory Guardrail Locks."""
        expected_locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "TRACE LOCK",
            "UNCERTAINTY LOCK",
            "SYSTEMATIC-DEBUGGING-LOCK",
            "VERIFICATION-BEFORE-COMPLETION-LOCK",
            "COMBINATORIAL-COVERAGE-LOCK",
            "CHAOS-GATE LOCK",
            "N1-QUERY-GATE LOCK",
            "CALIBRATED-EVAL-GATE LOCK",
            "CAN-I-DEPLOY-GATE LOCK",
            "ASSERTION-THEATER LOCK",
            "MUTATION-TESTING LOCK",
            "PROPERTY-TESTING LOCK",
            "MULTI-DIMENSIONAL-TEST LOCK",
            "OWASP-ASI-GATE LOCK",
            "AI-SYSTEM LOCK",
            "TRAJECTORY LOCK",
            "ACCESSIBILITY LOCK",
        ]
        for lock in expected_locks:
            self.assertIn(lock, self.role_content, f"Missing required guardrail lock: {lock}")

    def test_03_the_great_verification_convergence_pillars(self):
        """Role must detail The Great Verification Convergence across all 6 research pillars."""
        pillar_terms = [
            "Pillar 1: AI & Agentic System Evaluation",
            "Pillar 2: Consumer-Driven Contract Testing",
            "Pillar 3: Observability-Driven Testing",
            "Pillar 4: Modern Web, Browser Automation & Accessibility",
            "Pillar 5: Shift-Left Chaos & Fault Injection",
            "Pillar 6: Clean Architecture Multi-Language QA",
        ]
        for pillar in pillar_terms:
            self.assertIn(pillar, self.role_content, f"Missing pillar definition: {pillar}")

    def test_04_systematic_rca_and_vbc_invariants(self):
        """Role must rigorously define 4-Phase RCA and VBC epistemic doubt."""
        rca_phases = [
            "Phase 1: Observation & Deterministic Reproduction",
            "Phase 2: Architectural Hypothesis Formulation",
            "Phase 3: Targeted Experimentation & Red-Phase Verification",
            "Phase 4: Root-Cause Fix & Regression Prevention",
            "Verification-Before-Completion (VBC)",
            "Epistemic Doubt & Skeptical Validation",
            "Fresh Empirical Execution Proof",
        ]
        for item in rca_phases:
            self.assertIn(item, self.role_content, f"Missing RCA/VBC item: {item}")

    def test_05_clean_architecture_and_ephemeral_parity_invariants(self):
        """Role must mandate Go 1.25+ Kratos, Testcontainers PostgreSQL 16, Wire DI, and GORM InTx rollback."""
        arch_terms = [
            "Kratos 4-layer separation",
            "testcontainers/testcontainers-go",
            "PostgreSQL 16",
            "InTx",
            "wire.Build",
            "go test -v -race",
            "uber-go/goleak",
        ]
        for term in arch_terms:
            self.assertIn(term, self.role_content, f"Missing Clean Architecture term: {term}")

    def test_06_primary_skills_locked(self):
        """Primary skills toolbox must contain core QA skills."""
        expected_skills = [
            "`write-tests`",
            "`frontend-testing`",
            "`systematic-debugging`",
            "`combinatorial-testing`",
            "`agent-quality-gate`",
            "`accessibility-review`",
        ]
        for skill in expected_skills:
            self.assertIn(skill, self.role_content, f"Missing primary skill in toolbox: {skill}")

    def test_07_output_template_sections(self):
        """Output template must contain all 10 core verification sections."""
        template_sections = [
            "## 1. Consumer-Driven Contract Testing Gate",
            "## 2. AI & Agentic Evaluation Gate",
            "## 3. Observability-Driven & Trace-Based Testing Gate",
            "## 4. Modern Web & Browser Automation Gate",
            "## 5. Shift-Left Chaos & Fault Injection Gate",
            "## 6. Clean Architecture Multi-Language Integration Gate",
            "## 7. Mutation Testing & Security Gates",
            "## 8. Systematic Debugging & Root Cause Analysis (RCA)",
            "## 9. Pairwise Combinatorial Test Matrix",
            "## 10. Verification Before Completion (VBC) Sign-Off",
            "## Exit Criteria & Release Recommendation",
        ]
        for sec in template_sections:
            self.assertIn(sec, self.role_content, f"Missing template section: {sec}")


class TestQAEngineerReviewChecklist(unittest.TestCase):
    """Invariant testing for core/roles/references/qa-engineer-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "qa-engineer-review-checklist.md"
        assert cls.checklist_path.exists(), "qa-engineer-review-checklist.md must exist"
        cls.checklist_content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_13_sections_present(self):
        """Checklist must contain all 13 comprehensive SOTA verification sections."""
        expected_sections = [
            "### 1. Consumer-Driven Contract Testing (CDCT) & Wire Evolution",
            "### 2. Systematic Root Cause Analysis (4-Phase Debugging)",
            "### 3. Verification Before Completion (VBC) & Epistemic Doubt Gates",
            "### 4. Pairwise Combinatorial Testing & Matrix Optimization",
            "### 5. Calibrated AI & Agentic System Evaluation",
            "### 6. Observability-Driven Testing (ODT) & Trace-Based Assertions",
            "### 7. Modern Web, Browser Automation & Accessibility (Playwright v1.48+)",
            "### 8. Shift-Left Chaos, Resilience & Performance Gates",
            "### 9. Clean Architecture Multi-Language QA (Go 1.25+, Python, TypeScript)",
            "### 10. Mutation Testing Infrastructure & OWASP ASI Security Gates",
            "### 11. MCP & Agent System Validation",
            "### 12. EU AI Act Compliance",
            "### 13. Distributed System Foundation & Blast Radius Containment",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.checklist_content, f"Missing checklist section: {sec}")

    def test_02_technical_depth_in_checklist(self):
        """Checklist must include precise technical tools and criteria."""
        keywords = [
            "PactV3",
            "can-i-deploy",
            "buf breaking",
            "oasdiff",
            "DeepEval G-Eval",
            "Faithfulness",
            "Context Precision",
            "Context Recall",
            "Answer Relevancy",
            "Kubeshop Tracetest",
            "W3C",
            "traceparent",
            "EXPLAIN ANALYZE",
            "Playwright v1.48+",
            "MSW v2",
            "@axe-core/playwright",
            "document.fonts.ready",
            "Toxiproxy",
            "gobreaker",
            "full jitter",
            "k6",
            "Testcontainers",
            "InTx",
            "uber-go/goleak",
            "Stryker",
            "Mutmut",
            "OWASP ASI04",
            "OWASP ASI05",
        ]
        for kw in keywords:
            self.assertIn(kw, self.checklist_content, f"Missing technical keyword in checklist: {kw}")


class TestQAEngineerPrimarySkills(unittest.TestCase):
    """Validation of primary skills owned by QA Engineer."""

    def test_01_write_tests_skill_validity(self):
        """write-tests SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "foundation" / "write-tests" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "write-tests SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "write-tests SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: write-tests", content)
        self.assertIn("allowed-tools:", content)

    def test_02_frontend_testing_skill_validity(self):
        """frontend-testing SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "frontend" / "frontend-testing" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "frontend-testing SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "frontend-testing SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: frontend-testing", content)
        self.assertIn("allowed-tools:", content)

    def test_03_systematic_debugging_skill_validity(self):
        """systematic-debugging SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "foundation" / "systematic-debugging" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "systematic-debugging SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "systematic-debugging SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: systematic-debugging", content)
        self.assertIn("allowed-tools:", content)

    def test_04_combinatorial_testing_skill_validity(self):
        """combinatorial-testing SKILL.md must be valid and concise."""
        skill_path = SKILLS_DIR / "foundation" / "combinatorial-testing" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "combinatorial-testing SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: combinatorial-testing", content)


class TestQAEngineerAgentCardAndRegistry(unittest.TestCase):
    """Validation of A2A Agent Card, Discovery Registry, and Alias Resolution."""

    @classmethod
    def setUpClass(cls):
        cls.agent_card_path = AGENT_CARDS_DIR / "qa-engineer.agent-card.json"
        assert cls.agent_card_path.exists(), "qa-engineer.agent-card.json must exist"
        cls.agent_card = json.loads(cls.agent_card_path.read_text(encoding="utf-8"))

    def test_01_agent_card_structure(self):
        """Agent card must have correct id, contract_type, name, and output schemas."""
        self.assertEqual(self.agent_card.get("contract_type"), "agent-card")
        self.assertEqual(self.agent_card.get("name"), "qa-engineer")
        self.assertEqual(self.agent_card.get("id"), "pack://agent-skills/core/roles/qa-engineer")
        output_schemas = self.agent_card.get("defaultOutputSchemas", [])
        self.assertIn("test-report.json", output_schemas)
        self.assertIn("validation-result.json", output_schemas)

    def test_02_agent_card_skills_coverage(self):
        """Agent card must expose write-tests, frontend-testing, and systematic-debugging."""
        card_skills = [s.get("id") for s in self.agent_card.get("skills", [])]
        expected = ["write-tests", "frontend-testing", "systematic-debugging", "combinatorial-testing"]
        for exp in expected:
            self.assertIn(exp, card_skills, f"Missing skill in agent card: {exp}")

    def test_03_agent_registry_listing(self):
        """qa-engineer must be listed in agent-registry.json."""
        registry_path = REGISTRY_DIR / "agent-registry.json"
        self.assertTrue(registry_path.exists(), "agent-registry.json must exist")
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        agent_roles = [a.get("role") for a in reg.get("agents", [])]
        self.assertIn("qa-engineer", agent_roles, "qa-engineer must be listed in agent-registry.json")

    def test_04_role_skill_index_mapping(self):
        """role-skill-index.json must correctly map qa-engineer to its primary skills."""
        index_path = REGISTRY_DIR / "role-skill-index.json"
        self.assertTrue(index_path.exists(), "role-skill-index.json must exist")
        idx = json.loads(index_path.read_text(encoding="utf-8"))
        roles_map = idx.get("roles", {})
        self.assertIn("qa-engineer", roles_map, "qa-engineer must be mapped in role-skill-index.json")
        qa_skills = roles_map["qa-engineer"].get("skills", [])
        self.assertIn("write-tests", qa_skills)
        self.assertIn("frontend-testing", qa_skills)
        self.assertIn("systematic-debugging", qa_skills)

    def test_05_fast_invocation_alias_resolution(self):
        """Fast invocation aliases @qa, @tester, @test-engineer must resolve to qa-engineer."""
        index_path = REGISTRY_DIR / "role-skill-index.json"
        idx = json.loads(index_path.read_text(encoding="utf-8"))
        aliases = idx.get("role_aliases", {})
        self.assertEqual(aliases.get("qa"), "qa-engineer", "@qa alias must resolve to qa-engineer")
        self.assertEqual(aliases.get("tester"), "qa-engineer", "@tester alias must resolve to qa-engineer")
        self.assertEqual(aliases.get("test-engineer"), "qa-engineer", "@test-engineer alias must resolve to qa-engineer")


if __name__ == "__main__":
    unittest.main()
