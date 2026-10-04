#!/usr/bin/env python3
"""Automated Challenge Test Suite for Business Analyst Role & Modern Requirements Engineering Standards.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance for `feature-ticket.json`.
   - Full validity of all bundled examples in `feature-ticket.json` (3 complete examples).
   - 2026-2027 modern requirements engineering properties in `feature-ticket.json`:
     `vertical_slice_metadata`, `event_storming_context`, `agentic_feature_spec`,
     `responsible_ai_spec`, `nfr_envelope`, and enhanced BDD acceptance criteria.

2. Adversarial Negative Mutation Stress Tests:
   - Missing required fields (contract_type, title, type, acceptance_criteria).
   - Invalid discriminator constant (`contract_type`).
   - Empty acceptance_criteria array (minItems: 1 violation).
   - Missing required fields in acceptance_criteria items (scenario, then).
   - Invalid enums (priority, type, eu_ai_act_tier, autonomy_level, slice_pattern, gdpr_legal_basis).
   - Missing required fields in agentic_feature_spec (autonomy_level, governance_justified_ceiling, kill_switch).
   - Out-of-bounds numerical thresholds (four_fifths_rule_dir_threshold < 0.8).

3. Business Analyst Role (`core/roles/business-analyst.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Use This Role When,
     Core Responsibilities, Inputs Required, Outputs Produced, Deliverable Routing,
     Decision Boundaries, Role Boundaries, Collaboration, Guardrails, Skill Toolbox,
     Output Template, Review Checklist, Failure Modes, Anti-Patterns, Role Handoff, Definition Of Done.
   - Modern Requirements Engineering across 7 pillars:
     1. Domain Discovery & Event Storming (Domain Events past tense, Commands imperative, Aggregates).
     2. Lean Decomposition & Vertical Slicing (Walking Skeletons, Elephant Carpentry 8 patterns, INVEST).
     3. Behavioral Acceptance Criteria & BDD / Gherkin (Single-Action Invariant, stateful invariants, BVA).
     4. AI & Agentic Systems Governance (Probabilistic AC, Golden Benchmarks, HITL triggers, MCP least-privilege).
     5. Responsible AI, Fairness & Data Governance (Four-Fifths Rule, XAI 4 pillars, GDPR Art 6, DPIA, ROPA).
     6. Bidirectional Traceability & Economic Prioritization (RTM DAG, BFS 3-hop blast radius, WSJF).
     7. Machine Handoff & Contract Delivery (`feature-ticket.json` Draft 2020-12, zero pseudo-requirements).
   - Guardrail Locks:
     BOUNDARY LOCK, SECURITY LOCK, IRREVERSIBLE ACTION LOCK, TRACE LOCK, UNCERTAINTY LOCK,
     OBSERVABLE-AC-LOCK, VERTICAL-SLICE-LOCK, EVENT-STORMING-LOCK, AI-AC-LOCK, HITL-SPEC-LOCK,
     ASSUMPTION-LOCK, EU-AI-ACT-LOCK, ARTICLE-50-DISCLOSURE-LOCK, AGENTIC-AUTONOMY-LOCK,
     AGENT-PERMISSIONS-LOCK, AGENT-KILL-SWITCH-LOCK, FAIRNESS-AC-LOCK, XAI-LOCK, DATA-CONSENT-LOCK,
     NON-FUNCTIONAL-SLO-LOCK.

4. Business Analyst Review Checklist (`core/roles/references/business-analyst-review-checklist.md`):
   - All 14 comprehensive SOTA sections present and rigorous.

5. Primary Skills & Agent Conformance:
   - `analyze-business-requirements`, `elicit-requirements`, `write-use-cases`, `trace-requirements-impact`,
     `ai-risk-assessment`, `build-story-map`.
   - Valid YAML frontmatter, line limits, allowed tools.

6. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/business-analyst.agent-card.json` validity and skill IDs.
   - Fast invocation alias resolution for `@ba`, `@business`, `@business-analyst`.

7. Research Dossier Verification:
   - `reports/business-analyst-repo-research.md` existence, size, and depth.
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


class TestFeatureTicketSchema(unittest.TestCase):
    """Rigorous schema validation and meta-schema compliance for feature-ticket.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "feature-ticket.json"
        assert cls.schema_path.exists(), "feature-ticket.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "feature-ticket")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All bundled examples within feature-ticket.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreaterEqual(len(examples), 3, "Schema must include at least 3 bundled examples")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_sota_2026_2027_schema_properties_presence(self):
        """Schema must define modern requirements engineering properties."""
        props = self.schema_raw.get("properties", {})
        expected_properties = [
            "vertical_slice_metadata",
            "event_storming_context",
            "agentic_feature_spec",
            "responsible_ai_spec",
            "nfr_envelope",
            "ai_feature_spec",
            "assumption_register",
            "acceptance_criteria",
            "business_rules",
            "actors",
        ]
        for prop in expected_properties:
            self.assertIn(prop, props, f"Missing expected schema property: {prop}")

        # Check acceptance_criteria items properties
        ac_items_props = props["acceptance_criteria"]["items"]["properties"]
        for ac_prop in ["scenario", "given", "when", "then", "tags", "and_conditions", "stateful_invariants", "failure_guarantee"]:
            self.assertIn(ac_prop, ac_items_props, f"acceptance_criteria items missing property: {ac_prop}")

    def test_04_example_3_agentic_reconciliation_coverage(self):
        """Example 3 must demonstrate full SOTA fields: vertical slicing, event storming, agentic spec, responsible AI, and NFRs."""
        ex3 = self.schema_raw["examples"][2]
        self.assertEqual(ex3["ticket_id"], "2026-10-05-agentic-reconciliation-assistant")
        self.assertIn("vertical_slice_metadata", ex3)
        self.assertTrue(ex3["vertical_slice_metadata"]["walking_skeleton"])
        self.assertEqual(ex3["vertical_slice_metadata"]["slice_pattern"], "workflow_step")

        self.assertIn("event_storming_context", ex3)
        self.assertEqual(ex3["event_storming_context"]["bounded_context"], "treasury_reconciliation")
        self.assertGreaterEqual(len(ex3["event_storming_context"]["domain_events"]), 3)

        self.assertIn("agentic_feature_spec", ex3)
        self.assertEqual(ex3["agentic_feature_spec"]["autonomy_level"], "L3_conditional")
        self.assertIn("kill_switch", ex3["agentic_feature_spec"])

        self.assertIn("responsible_ai_spec", ex3)
        self.assertGreaterEqual(ex3["responsible_ai_spec"]["four_fifths_rule_dir_threshold"], 0.8)

        self.assertIn("nfr_envelope", ex3)
        self.assertEqual(ex3["nfr_envelope"]["gdpr_article_6_legal_basis"], "legal_obligation")


class TestFeatureTicketNegativeMutations(unittest.TestCase):
    """Adversarial negative mutation stress testing for feature-ticket.json."""

    @classmethod
    def setUpClass(cls):
        schema_path = CONTRACTS_DIR / "feature-ticket.json"
        cls.schema_raw = json.loads(schema_path.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema_raw)
        cls.valid_base = copy.deepcopy(cls.schema_raw["examples"][2])

    def test_05_missing_contract_type(self):
        """Omitting contract_type discriminator must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["contract_type"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_06_invalid_contract_type_discriminator(self):
        """Invalid contract_type discriminator must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["contract_type"] = "invalid-ticket-spec"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_07_missing_title(self):
        """Omitting title must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["title"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_08_missing_type(self):
        """Omitting type must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["type"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_09_invalid_type_enum(self):
        """Invalid type enum value must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["type"] = "epic_narrative"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_10_missing_acceptance_criteria(self):
        """Omitting acceptance_criteria must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["acceptance_criteria"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_11_empty_acceptance_criteria(self):
        """Empty acceptance_criteria array must fail validation (minItems: 1)."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["acceptance_criteria"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_12_ac_item_missing_scenario(self):
        """Acceptance criteria item missing scenario must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["acceptance_criteria"][0]["scenario"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_13_ac_item_missing_then(self):
        """Acceptance criteria item missing then outcome must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["acceptance_criteria"][0]["then"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_14_invalid_priority_enum(self):
        """Invalid priority enum value must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["priority"] = "ultra-urgent"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_15_invalid_agentic_autonomy_level(self):
        """Invalid autonomy_level enum value must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["agentic_feature_spec"]["autonomy_level"] = "L6_omnipresent"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_16_agentic_spec_missing_required_kill_switch(self):
        """Omitting kill_switch in agentic_feature_spec must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        del mutated["agentic_feature_spec"]["kill_switch"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_17_invalid_vertical_slice_pattern(self):
        """Invalid slice_pattern enum value must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["vertical_slice_metadata"]["slice_pattern"] = "horizontal_database_tier"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_18_responsible_ai_dir_threshold_below_minimum(self):
        """Disparate impact ratio threshold below 0.8 must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["responsible_ai_spec"]["four_fifths_rule_dir_threshold"] = 0.65
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)

    def test_19_invalid_gdpr_legal_basis(self):
        """Invalid GDPR Article 6 legal basis enum must fail validation."""
        mutated = copy.deepcopy(self.valid_base)
        mutated["nfr_envelope"]["gdpr_article_6_legal_basis"] = "corporate_mandate"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated)


class TestBusinessAnalystRoleInvariants(unittest.TestCase):
    """Rigorous verification of core/roles/business-analyst.md structure and invariants."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "business-analyst.md"
        assert cls.role_path.exists(), "business-analyst.md must exist"
        cls.role_text = cls.role_path.read_text(encoding="utf-8")

    def test_20_role_standard_sections_presence(self):
        """Role must contain all required sections per role-standard.md."""
        expected_sections = [
            "# Business Analyst",
            "Mission:",
            "Level:",
            "This role must follow [role-standard](role-standard.md) first.",
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
        for section in expected_sections:
            self.assertIn(section, self.role_text, f"Missing required section: {section}")

    def test_21_guardrail_locks_declared(self):
        """All mandatory and modern SOTA guardrail locks must be declared."""
        expected_locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "TRACE LOCK",
            "UNCERTAINTY LOCK",
            "OBSERVABLE-AC-LOCK",
            "VERTICAL-SLICE-LOCK",
            "EVENT-STORMING-LOCK",
            "AI-AC-LOCK",
            "HITL-SPEC-LOCK",
            "ASSUMPTION-LOCK",
            "EU-AI-ACT-LOCK",
            "ARTICLE-50-DISCLOSURE-LOCK",
            "AGENTIC-AUTONOMY-LOCK",
            "AGENT-PERMISSIONS-LOCK",
            "AGENT-KILL-SWITCH-LOCK",
            "FAIRNESS-AC-LOCK",
            "XAI-LOCK",
            "DATA-CONSENT-LOCK",
            "NON-FUNCTIONAL-SLO-LOCK",
        ]
        for lock in expected_locks:
            self.assertIn(lock, self.role_text, f"Missing required Guardrail Lock: {lock}")

    def test_22_seven_pillars_in_core_responsibilities(self):
        """Core Responsibilities must articulate all 7 modern pillars."""
        expected_pillar_tokens = [
            "Domain Discovery & Ubiquitous Language (Event Storming)",
            "Lean Decomposition & Vertical Slicing",
            "Behavioral Acceptance Criteria & Specification by Example",
            "AI & Agentic Systems Governance",
            "Responsible AI, Fairness & Data Governance",
            "Bidirectional Traceability & Economic Prioritization",
            "Machine Handoff & Contract Delivery",
        ]
        for token in expected_pillar_tokens:
            self.assertIn(token, self.role_text, f"Core Responsibilities missing pillar: {token}")

    def test_23_fifteen_deadly_anti_patterns_present(self):
        """Role must warn against classic requirements engineering anti-patterns."""
        expected_anti_patterns = [
            "binary pass/fail acceptance criteria for stochastic AI/LLM",
            "omitting Human-in-the-Loop (HITL) escalation protocols",
            "horizontal architectural slicing",
            "entity smuggling across DDD bounded contexts",
            "relying on aggregate model accuracy while ignoring disparate impact",
            "granting enterprise agents session-level or persistent tool credentials",
            "skipping EU AI Act risk tiering and Article 50",
        ]
        for ap in expected_anti_patterns:
            self.assertIn(ap, self.role_text, f"Missing anti-pattern warning: {ap}")

    def test_24_maintenance_date(self):
        """Role must reflect modern maintenance date."""
        self.assertIn("Last updated: 2026-10-05", self.role_text)


class TestBusinessAnalystReviewChecklist(unittest.TestCase):
    """Rigorous verification of core/roles/references/business-analyst-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "business-analyst-review-checklist.md"
        assert cls.checklist_path.exists(), "business-analyst-review-checklist.md must exist"
        cls.checklist_text = cls.checklist_path.read_text(encoding="utf-8")

    def test_25_all_14_sota_sections_present(self):
        """Checklist must include all 14 comprehensive SOTA sections."""
        expected_sections = [
            "### 1. Requirements Quality & BABOK v3 Nine Criteria Compliance",
            "### 2. Stakeholder Discovery, Funnel Questioning & Tacit Knowledge Elicitation",
            "### 3. Cockburn Scoping & Karl Wiegers 13-Field Use Case Verification",
            "### 4. Domain-Driven Design (DDD) & Event Storming Invariants",
            "### 5. Vertical Slice Decomposition, Walking Skeletons & User Story Mapping",
            "### 6. Behavioral Acceptance Criteria (BDD / Gherkin) & Equivalence Partitioning",
            "### 7. AI/LLM Probabilistic Acceptance Criteria & Statistical Bounds",
            "### 8. Human-in-the-Loop (HITL) Governance & Escalation Protocols",
            "### 9. Agentic AI Autonomy (L1–L5), MCP Least-Privilege & Kill-Switch Safeguards",
            "### 10. Responsible AI, Bias Prevention (Four-Fifths Rule) & Explainability (XAI)",
            "### 11. Data Governance, GDPR Compliance & Privacy Lineage",
            "### 12. Bidirectional Traceability (RTM) & Change Request Impact Analysis (BFS)",
            "### 13. Non-Functional Requirements (NFR) & Architectural Envelopes",
            "### 14. Executable Contract Machine Handoff (`feature-ticket.json`) & Living Documentation",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.checklist_text, f"Review checklist missing section: {sec}")

    def test_26_checklist_verifiable_criteria_rigor(self):
        """Checklist must enforce concrete verifiable thresholds and terms."""
        verifiable_tokens = [
            "Four-Fifths Rule",
            "Single-Action Invariant",
            "User-Goal Level (Blue)",
            "Coffee-Break Test",
            "Breadth-First Search graph traversal",
            "BFS Blast Radius Analysis on Change Requests",
            "Weighted Shortest Job First",
            "L3 (Conditional) enforced as enterprise production ceiling",
            "Attenuated Authority Invariant",
            "Disparate Impact Ratio",
            r"\text{Risk Score} = \text{Impact} \times (6 - \text{Confidence})",
            "Draft 2020-12",
        ]
        for token in verifiable_tokens:
            self.assertIn(token, self.checklist_text, f"Checklist missing verifiable criteria: {token}")


class TestBusinessAnalystSkillsIntegrity(unittest.TestCase):
    """Verification of Business Analyst primary skills."""

    def test_27_primary_skills_exist_and_conform(self):
        """Primary skills must exist with valid YAML frontmatter and acceptable line lengths."""
        primary_skills = [
            ("analyze-business-requirements", SKILLS_DIR / "meetings-analysis" / "analyze-business-requirements" / "SKILL.md"),
            ("elicit-requirements", SKILLS_DIR / "business" / "elicit-requirements" / "SKILL.md"),
            ("write-use-cases", SKILLS_DIR / "business" / "write-use-cases" / "SKILL.md"),
            ("trace-requirements-impact", SKILLS_DIR / "business" / "trace-requirements-impact" / "SKILL.md"),
            ("ai-risk-assessment", SKILLS_DIR / "foundation" / "ai-risk-assessment" / "SKILL.md"),
            ("build-story-map", SKILLS_DIR / "product" / "build-story-map" / "SKILL.md"),
        ]
        for skill_id, skill_path in primary_skills:
            self.assertTrue(skill_path.exists(), f"Skill file does not exist: {skill_path}")
            text = skill_path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---"), f"Skill {skill_id} missing YAML frontmatter")
            parts = text.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"Skill {skill_id} frontmatter malformed")
            meta = yaml.safe_load(parts[1])
            self.assertEqual(meta.get("name"), skill_id)
            self.assertIn("description", meta)
            self.assertIn("allowed-tools", meta)
            # Ensure line count is bounded for context efficiency (< 200 lines)
            line_count = len(text.splitlines())
            self.assertLessEqual(line_count, 200, f"Skill {skill_id} exceeds 200 line limit ({line_count} lines)")


class TestBusinessAnalystA2ARegistryAndDiscovery(unittest.TestCase):
    """Verification of Agent Card, Registry Discovery, and Fast Invocation Aliases."""

    @classmethod
    def setUpClass(cls):
        cls.card_path = AGENT_CARDS_DIR / "business-analyst.agent-card.json"
        assert cls.card_path.exists(), "business-analyst.agent-card.json must exist"
        cls.card = json.loads(cls.card_path.read_text(encoding="utf-8"))

        cls.role_skill_index_path = REGISTRY_DIR / "role-skill-index.json"
        assert cls.role_skill_index_path.exists(), "role-skill-index.json must exist"
        cls.role_skill_index = json.loads(cls.role_skill_index_path.read_text(encoding="utf-8"))

    def test_28_agent_card_schema_and_skills(self):
        """Agent card must have correct metadata and reference valid skill IDs."""
        self.assertEqual(self.card.get("contract_type"), "agent-card")
        self.assertEqual(self.card.get("name"), "business-analyst")
        self.assertEqual(self.card.get("version"), "5.0.0")
        card_skills = [s["id"] for s in self.card.get("skills", [])]
        expected_skills = [
            "analyze-business-requirements",
            "elicit-requirements",
            "write-use-cases",
            "trace-requirements-impact",
            "ai-risk-assessment",
        ]
        for skill_id in expected_skills:
            self.assertIn(skill_id, card_skills, f"Agent card missing skill: {skill_id}")

    def test_29_fast_invocation_aliases(self):
        """role-skill-index.json must resolve @ba, @business, and @business-analyst."""
        role_aliases = self.role_skill_index.get("role_aliases", {})
        self.assertEqual(role_aliases.get("ba"), "business-analyst", "Alias @ba must resolve to business-analyst")
        self.assertEqual(role_aliases.get("business"), "business-analyst", "Alias @business must resolve to business-analyst")

        roles = self.role_skill_index.get("roles", {})
        self.assertIn("business-analyst", roles, "Role business-analyst must be registered in roles map")


class TestBusinessAnalystResearchDossier(unittest.TestCase):
    """Verification of reports/business-analyst-repo-research.md presence and depth."""

    @classmethod
    def setUpClass(cls):
        cls.dossier_path = REPORTS_DIR / "business-analyst-repo-research.md"
        assert cls.dossier_path.exists(), "business-analyst-repo-research.md must exist in reports/"
        cls.dossier_text = cls.dossier_path.read_text(encoding="utf-8")

    def test_30_research_dossier_presence_and_depth(self):
        """Research dossier must exist, have significant substance, and cover core domains."""
        self.assertGreaterEqual(len(self.dossier_text), 40000, "Research dossier must be >= 40 KB of deep research")
        required_dossier_topics = [
            "Pillar 1: Behavioral Acceptance Criteria & Specification by Example (BDD / Gherkin / ATDD)",
            "Pillar 2: Domain-Driven Design (DDD) & Event Storming for Requirements",
            "Pillar 3: AI & Agentic Systems Requirements Engineering (2025–2027 SOTA)",
            "Pillar 4: Lean/Agile Decomposition, Vertical Slicing & Continuous Discovery",
            "Pillar 5: Disciplined Stakeholder Elicitation & BABOK v3 Quality Governance",
            "Pillar 6: Requirements Traceability Matrix (RTM), Blast Radius Analysis & Backlog Prioritization",
            "Pillar 7: Executable Contracts, Machine Handoff & Anti-Pattern Catalog",
            "The 15 Deadly Requirements Anti-Patterns",
            "Karl Wiegers 13-Field Production Template",
            "Alistair Cockburn's 3 Goal Levels",
            "Four-Fifths Rule",
            "Weighted Shortest Job First",
        ]
        for topic in required_dossier_topics:
            self.assertIn(topic, self.dossier_text, f"Research dossier missing topic: {topic}")


if __name__ == "__main__":
    unittest.main()
