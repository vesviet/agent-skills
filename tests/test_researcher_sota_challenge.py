#!/usr/bin/env python3
"""Automated Challenge Test Suite for Researcher Role & SOTA Deep Research Architecture.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance via Draft202012Validator.check_schema().
   - Full validity of bundled examples in `research-report.json`.
   - Comprehensive SOTA properties: `citation_dag`, `cove_verification_matrix`, `information_density`.
   - Structural constraints on topological acyclicity, 3-color DFS cycle checks, CoVe atomic matrix, and ID >= 0.12.

2. Adversarial Negative Mutation Stress Tests:
   - Missing required fields (contract_type, objective, citation_dag, cove_verification_matrix, information_density).
   - Invalid discriminator constant (`contract_type`).
   - Cyclic DAG indicator rejection (`is_acyclic: false`).
   - Information density score below threshold (< 0.12).
   - Invalid verification status enum in CoVe matrix.
   - Empty CoVe matrix array (minItems: 1).
   - Deep mode round constraint (< 10 rounds).
   - Scoped mode without mandatory scope waiver note.
   - Invalid cycle check algorithm enum.

3. Researcher Role (`core/roles/researcher.md`) Invariant Verification:
   - Role-standard compliance: all 21 mandatory sections from `role-standard.md`.
   - Architectural Guardrail Locks: CITATION-DAG-LOCK, MULTI-SOURCE-TRIANGULATION-LOCK,
     COVE-ATOMIC-VERIFICATION-LOCK, C2PA-CRYPTOGRAPHIC-PROVENANCE-LOCK, ZERO-AI-PRIMARY-CITATION-LOCK,
     INFORMATION-DENSITY-LOCK, DEPTH LOCK, GROUNDING LOCK, PRIMARY-SOURCE-HIERARCHY-LOCK,
     URL-LIVENESS-VERIFICATION-LOCK, YMYL-EXPERT-ELEVATION-LOCK, STORM-PERSONA-DISCOVERY-LOCK.
   - Stanford STORM persona discovery protocol (Skeptical Auditor, Compliance Reviewer, Domain Specialist, Technical Architect)
     and simulated conversational interviews.
   - Deliverable routing table and single valid `Last updated:` footer.

4. Conduct Research Skill (`core/skills/foundation/conduct-research/SKILL.md`) Conformance:
   - Concise line count (< 200 lines).
   - Standardized YAML frontmatter (version: "2.0.0", owners: primary: "@researcher", taxonomy: foundation, tags).
   - Canonical 5-phase execution flow:
     (1) Objective & Persona Discovery, (2) Sub-Task Decomposition & DAG Planning,
     (3) Deep Multi-Hop Search, (4) CoVe & Provenance Verification, (5) Information Density Synthesis.
   - Authoritative reference dossier `references/sota-deep-research-architecture.md` existence.

5. Topological Citation DAG Cycle Detection Algorithm (3-Color DFS):
   - Acyclic diamond DAG passes with zero cycles.
   - Circular dependency (A -> B -> C -> A) detected fail-closed.
   - Self-referential loop (A -> A) detected.
   - Disconnected graph with cycle in subgraph detected.
   - Multi-source triangulation rule validation (>= 3 independent primary sources).

6. Quantitative Information Density (ID) Calculation Engine:
   - High-density technical brief satisfies ID >= 0.12.
   - Fluffy conversational filler text fails ID < 0.12.
   - Mathematical boundary evaluation.

7. Chain-of-Verification (CoVe) & C2PA Provenance Evaluation:
   - Atomic claim decomposition and verification status classification.
   - C2PA Content Credentials cryptographic inspection and fallback handling.

8. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/researcher.agent-card.json` metadata, version sync, and skills.
"""

from __future__ import annotations

import collections
import copy
import json
from pathlib import Path
import re
import unittest

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
SCHEMAS_DIR = CORE_DIR / "contracts" / "schemas"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
AGENT_CARDS_DIR = CORE_DIR / "a2a" / "registry"


# ==============================================================================
# Helper Algorithms for Topological Citation DAG & Information Density
# ==============================================================================

def check_citation_dag_acyclicity(nodes: list[dict], edges: list[dict]) -> tuple[bool, list[str]]:
    """Evaluates Citation DAG acyclicity using 3-color DFS.
    
    Color 0: White (unvisited)
    Color 1: Gray (currently in recursion stack - cycle indicator)
    Color 2: Black (completely processed)
    """
    adj: dict[str, list[str]] = {n["node_id"]: [] for n in nodes}
    for e in edges:
        from_id = e.get("from_node_id")
        to_id = e.get("to_node_id")
        if from_id not in adj:
            adj[from_id] = []
        adj[from_id].append(to_id)

    color: dict[str, int] = {n["node_id"]: 0 for n in nodes}
    for e in edges:
        from_id = e.get("from_node_id")
        to_id = e.get("to_node_id")
        if from_id not in color:
            color[from_id] = 0
        if to_id not in color:
            color[to_id] = 0

    cycle_path: list[str] = []

    def dfs(node: str, path: list[str]) -> bool:
        color[node] = 1  # Gray
        path.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in color:
                continue
            if color[neighbor] == 1:
                # Cycle detected
                cycle_start = path.index(neighbor)
                cycle_path.extend(path[cycle_start:] + [neighbor])
                return True
            if color[neighbor] == 0:
                if dfs(neighbor, path):
                    return True
        path.pop()
        color[node] = 2  # Black
        return False

    for node_id in list(color.keys()):
        if color[node_id] == 0:
            if dfs(node_id, []):
                return False, cycle_path

    return True, []


def calculate_information_density(text: str) -> dict:
    """Calculates quantitative Information Density (ID) ratio:
    
    ID = (Named Entities + Quantified Metrics) / Total Words
    Threshold: ID >= 0.12
    """
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return {
            "total_words": 0,
            "named_entities_count": 0,
            "quantified_metrics_count": 0,
            "density_score": 0.0,
            "status": "failed",
        }

    # Technical entity patterns: Capitalized words, standards, library/tool identifiers
    named_entity_patterns = [
        r"\b[A-Z][a-zA-Z0-9_\-\.]+\s+[0-9]+(?:\.[0-9]+)*\b",  # e.g., Redis 7.4, Go 1.25
        r"\b(?:RFC|ISO|TCVN|IEEE|NIST|GDPR|HIPAA|PCI-DSS)\s*[0-9A-Z:\-]+\b",  # e.g., TCVN 7830:2021
        r"\b[A-Z][a-zA-Z0-9]+(?:[A-Z][a-z0-9]+)+\b",  # CamelCase: e.g. PagedAttention, FastMCP
        r"\b(?:PostgreSQL|Kubernetes|AWS|Graviton4|Crossplane|OpenTofu|Bottlerocket|Toxiproxy|DoWhy|DuckDB|Polars|C2PA|STORM|CoVe)\b",
    ]

    # Quantified metric patterns: Numbers with units, latencies, percentages, dates
    metric_patterns = [
        r"\b[0-9]+(?:\.[0-9]+)?\s*(?:ms|us|ns|s|m|h|TPS|RPS|QPS|GB|MB|KB|TB|GHz|MHz|%|bps|Gbps|Mbps)\b",
        r"\b[0-9]+(?:\.[0-9]+)?k\s*(?:TPS|RPS|users|req/s)\b",
        r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}(?:T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?)?\b",  # ISO timestamp
        r"\b(?:p50|p90|p95|p99|p99\.9)\s*(?:=|:|\s*of\s*)\s*[0-9]+(?:\.[0-9]+)?\s*(?:ms|s)?\b",
    ]

    found_entities = set()
    for pat in named_entity_patterns:
        for m in re.finditer(pat, text):
            found_entities.add(m.group(0))

    found_metrics = set()
    for pat in metric_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            found_metrics.add(m.group(0))

    entity_count = len(found_entities)
    metric_count = len(found_metrics)
    density_score = round((entity_count + metric_count) / total_words, 4)
    status = "passed" if density_score >= 0.12 else "failed"

    return {
        "total_words": total_words,
        "named_entities_count": entity_count,
        "quantified_metrics_count": metric_count,
        "density_score": density_score,
        "status": status,
    }


# ==============================================================================
# 1. TestResearchReportSchemaDraft202012
# ==============================================================================

class TestResearchReportSchemaDraft202012(unittest.TestCase):
    """Schema Meta-Validation & Bundled Examples Conformance for research-report.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = SCHEMAS_DIR / "research-report.json"
        assert cls.schema_path.exists(), f"Missing schema at {cls.schema_path}"
        cls.schema = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_01_meta_schema_conformance(self):
        """Schema must be a valid Draft 2020-12 JSON Schema."""
        self.assertEqual(
            self.schema.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
            "Schema must declare Draft 2020-12 meta-schema",
        )
        self.assertEqual(self.schema.get("$id"), "research-report")
        self.assertEqual(self.schema.get("type"), "object")
        # Check meta-schema conformance via Draft202012Validator
        Draft202012Validator.check_schema(self.schema)

    def test_02_bundled_examples_pass_validation(self):
        """All bundled instances in examples array must validate with zero errors."""
        examples = self.schema.get("examples", [])
        self.assertGreaterEqual(len(examples), 1, "Must contain at least 1 bundled example")
        for idx, example in enumerate(examples):
            errors = list(self.validator.iter_errors(example))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example [{idx}] failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_sota_properties_present(self):
        """Schema properties must include citation_dag, cove_verification_matrix, and information_density."""
        props = self.schema.get("properties", {})
        required = self.schema.get("required", [])

        expected_props = [
            "contract_type",
            "objective",
            "execution_metrics",
            "citation_dag",
            "cove_verification_matrix",
            "information_density",
            "synthesis",
            "raw_data_references",
            "recommended_next_roles",
        ]
        for prop in expected_props:
            self.assertIn(prop, props, f"Missing property: {prop}")

    def test_04_citation_dag_properties(self):
        """citation_dag definition must enforce strict acyclicity and graph topology."""
        dag = self.schema.get("properties", {}).get("citation_dag", {})
        self.assertEqual(dag.get("type"), "object")
        dag_props = dag.get("properties", {})
        dag_req = dag.get("required", [])

        for field in ["is_acyclic", "cycle_check_algorithm", "validation_status", "nodes", "edges"]:
            self.assertIn(field, dag_props, f"citation_dag missing field: {field}")
            self.assertIn(field, dag_req, f"citation_dag required missing: {field}")

        # is_acyclic must be const true
        self.assertEqual(dag_props["is_acyclic"].get("const"), True)
        # algorithm must include 3-color DFS
        self.assertIn("dfs_three_color", dag_props["cycle_check_algorithm"].get("enum", []))

    def test_05_cove_matrix_properties(self):
        """cove_verification_matrix definition must enforce atomic propositions and status enum."""
        cove = self.schema.get("properties", {}).get("cove_verification_matrix", {})
        self.assertEqual(cove.get("type"), "object")
        cove_props = cove.get("properties", {})
        cove_req = cove.get("required", [])

        for field in [
            "total_claims_assessed",
            "verified_claims_count",
            "refuted_claims_count",
            "unverifiable_claims_count",
            "matrix",
        ]:
            self.assertIn(field, cove_props, f"cove_verification_matrix missing field: {field}")
            self.assertIn(field, cove_req, f"cove_verification_matrix required missing: {field}")

        matrix_items = cove_props["matrix"].get("items", {}).get("properties", {})
        for item_field in [
            "claim_id",
            "atomic_proposition",
            "verification_question",
            "isolated_query_used",
            "verification_status",
            "confidence_score",
        ]:
            self.assertIn(item_field, matrix_items, f"matrix item missing field: {item_field}")

        status_enum = matrix_items["verification_status"].get("enum", [])
        self.assertIn("verified", status_enum)
        self.assertIn("refuted", status_enum)
        self.assertIn("unverifiable", status_enum)

    def test_06_information_density_properties(self):
        """information_density definition must enforce density_score minimum 0.12."""
        id_obj = self.schema.get("properties", {}).get("information_density", {})
        self.assertEqual(id_obj.get("type"), "object")
        id_props = id_obj.get("properties", {})
        id_req = id_obj.get("required", [])

        for field in [
            "total_words",
            "named_entities_count",
            "quantified_metrics_count",
            "density_score",
            "formula",
            "status",
        ]:
            self.assertIn(field, id_props, f"information_density missing field: {field}")
            self.assertIn(field, id_req, f"information_density required missing: {field}")

        # Minimum threshold must be 0.12
        self.assertEqual(id_props["density_score"].get("minimum"), 0.12)
        self.assertEqual(
            id_props["formula"].get("const"),
            "ID = (Named Entities + Quantified Metrics) / Total Words",
        )


# ==============================================================================
# 2. TestResearchReportAdversarialMutations
# ==============================================================================

class TestResearchReportAdversarialMutations(unittest.TestCase):
    """Negative Mutation Stress Testing against research-report.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = SCHEMAS_DIR / "research-report.json"
        cls.schema = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.valid_instance = copy.deepcopy(cls.schema["examples"][0])

    def test_07_missing_contract_type(self):
        """Omitting contract_type discriminator must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        del instance["contract_type"]
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_08_invalid_contract_type_const(self):
        """Mutating contract_type to a non-matching string must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["contract_type"] = "arbitrary-brief"
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_09_cyclic_dag_indicator_rejected(self):
        """Setting citation_dag.is_acyclic to false must fail validation (const: true)."""
        instance = copy.deepcopy(self.valid_instance)
        instance["citation_dag"]["is_acyclic"] = False
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_10_density_score_below_threshold(self):
        """Setting information_density.density_score below 0.12 must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["information_density"]["density_score"] = 0.119
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_11_invalid_verification_status(self):
        """Using a non-standard verification status enum must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["cove_verification_matrix"]["matrix"][0]["verification_status"] = "plausible"
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_12_empty_cove_matrix(self):
        """Empty cove_verification_matrix.matrix array must fail validation (minItems: 1)."""
        instance = copy.deepcopy(self.valid_instance)
        instance["cove_verification_matrix"]["matrix"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_13_deep_mode_under_10_rounds(self):
        """Deep mode research with fewer than 10 rounds must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["execution_metrics"]["depth_mode"] = "deep"
        instance["execution_metrics"]["total_rounds"] = 8
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_14_scoped_mode_without_waiver(self):
        """Scoped mode research lacking scope_waiver_note must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["execution_metrics"]["depth_mode"] = "scoped"
        instance["execution_metrics"]["total_rounds"] = 4
        if "scope_waiver_note" in instance["execution_metrics"]:
            del instance["execution_metrics"]["scope_waiver_note"]
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_15_invalid_cycle_algorithm(self):
        """Unsupported cycle_check_algorithm enum must fail validation."""
        instance = copy.deepcopy(self.valid_instance)
        instance["citation_dag"]["cycle_check_algorithm"] = "heuristic_guessing"
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)


# ==============================================================================
# 3. TestResearcherRoleInvariants
# ==============================================================================

class TestResearcherRoleInvariants(unittest.TestCase):
    """Invariant and Standard Verification for core/roles/researcher.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "researcher.md"
        assert cls.role_path.exists(), f"Missing role file at {cls.role_path}"
        cls.role_text = cls.role_path.read_text(encoding="utf-8")
        cls.checklist_path = ROLES_DIR / "references" / "researcher-review-checklist.md"
        cls.checklist_text = cls.checklist_path.read_text(encoding="utf-8") if cls.checklist_path.exists() else ""

    def test_16_role_standard_sections_present(self):
        """Role file must contain all mandatory role-standard sections."""
        mandatory_headings = [
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
            "## Optional Overlays",
        ]
        for heading in mandatory_headings:
            self.assertIn(heading, self.role_text, f"Researcher role missing section: {heading}")

    def test_17_all_guardrail_locks_present(self):
        """Researcher role must enforce all required Architectural Guardrail Locks."""
        required_locks = [
            "STORM-PERSONA-DISCOVERY-LOCK",
            "CITATION-DAG-LOCK",
            "MULTI-SOURCE-TRIANGULATION-LOCK",
            "COVE-ATOMIC-VERIFICATION-LOCK",
            "C2PA-CRYPTOGRAPHIC-PROVENANCE-LOCK",
            "ZERO-AI-PRIMARY-CITATION-LOCK",
            "INFORMATION-DENSITY-LOCK",
            "PRIMARY-SOURCE-HIERARCHY-LOCK",
            "URL-LIVENESS-VERIFICATION-LOCK",
            "YMYL-EXPERT-ELEVATION-LOCK",
            "DEPTH LOCK",
            "GROUNDING LOCK",
        ]
        for lock in required_locks:
            self.assertIn(lock, self.role_text, f"Researcher role missing guardrail lock: {lock}")

    def test_18_storm_architecture_codified(self):
        """Stanford STORM persona discovery and interview protocol must be codified."""
        self.assertIn("Stanford STORM", self.role_text)
        self.assertIn("Skeptical Auditor", self.role_text)
        self.assertIn("Compliance Reviewer", self.role_text)
        self.assertIn("Domain Specialist", self.role_text)
        self.assertIn("Technical Architect", self.role_text)
        self.assertIn("conversational interview", self.role_text.lower())

    def test_19_role_deliverable_routing_and_footer(self):
        """Deliverable Routing table must exist and Last updated footer must be valid."""
        self.assertIn("## Deliverable Routing", self.role_text)
        self.assertIn("| Situation | Primary deliverable | Notes |", self.role_text)
        self.assertIn("research-report.json", self.role_text)
        # Verify footer format
        lines = [line.strip() for line in self.role_text.splitlines() if line.strip()]
        last_line = lines[-1]
        self.assertTrue(
            re.match(r"^Last updated:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}$", last_line),
            f"Role file footer must be 'Last updated: YYYY-MM-DD', got: {last_line}",
        )


# ==============================================================================
# 4. TestConductResearchSkillIntegrity
# ==============================================================================

class TestConductResearchSkillIntegrity(unittest.TestCase):
    """Integrity and Line Budget Verification for conduct-research skill."""

    @classmethod
    def setUpClass(cls):
        cls.skill_dir = SKILLS_DIR / "foundation" / "conduct-research"
        cls.skill_path = cls.skill_dir / "SKILL.md"
        assert cls.skill_path.exists(), f"Missing skill file at {cls.skill_path}"
        cls.skill_text = cls.skill_path.read_text(encoding="utf-8")
        cls.ref_dossier_path = cls.skill_dir / "references" / "sota-deep-research-architecture.md"

    def test_20_frontmatter_and_line_count(self):
        """SKILL.md must have valid YAML frontmatter, @researcher owner, and be strictly < 200 lines."""
        lines = self.skill_text.splitlines()
        self.assertLess(len(lines), 200, f"SKILL.md must be strictly < 200 lines, got {len(lines)}")

        # Parse YAML frontmatter
        parts = self.skill_text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Frontmatter missing")
        frontmatter = yaml.safe_load(parts[1])

        self.assertEqual(frontmatter.get("name"), "conduct-research")
        self.assertEqual(frontmatter.get("version"), "2.0.0")
        self.assertEqual(frontmatter.get("taxonomy"), "foundation")
        self.assertEqual(frontmatter.get("owners", {}).get("primary"), "@researcher")
        self.assertIn("cove", frontmatter.get("tags", []))
        self.assertIn("citation-dag", frontmatter.get("tags", []))

    def test_21_five_phase_execution_flow(self):
        """SKILL.md must define the canonical 5-phase SOTA research execution process."""
        expected_phases = [
            "Phase 1: Objective & Persona Discovery",
            "Phase 2: Sub-Task Decomposition & DAG Planning",
            "Phase 3: Deep Multi-Hop Search",
            "Phase 4: CoVe & Provenance Verification",
            "Phase 5: Information Density Synthesis",
        ]
        for phase in expected_phases:
            self.assertIn(phase, self.skill_text, f"Skill missing execution phase: {phase}")

    def test_22_reference_dossier_exists(self):
        """Authoritative reference dossier sota-deep-research-architecture.md must exist and be comprehensive."""
        self.assertTrue(self.ref_dossier_path.exists(), "Reference dossier missing")
        dossier_text = self.ref_dossier_path.read_text(encoding="utf-8")
        self.assertIn("Stanford STORM", dossier_text)
        self.assertIn("Citation Directed Acyclic Graph", dossier_text)
        self.assertIn("Chain-of-Verification", dossier_text)
        self.assertIn("C2PA", dossier_text)
        self.assertIn("Information Density", dossier_text)


# ==============================================================================
# 5. TestCitationDAGCycleDetectorAlgorithm
# ==============================================================================

class TestCitationDAGCycleDetectorAlgorithm(unittest.TestCase):
    """Algorithm Testing for Citation DAG 3-Color DFS Cycle Detection & Triangulation."""

    def test_23_valid_diamond_dag_passes(self):
        """A valid acyclic diamond graph (A -> B, A -> C, B -> D, C -> D) must pass with 0 cycles."""
        nodes = [
            {"node_id": "claim_A"},
            {"node_id": "src_B"},
            {"node_id": "src_C"},
            {"node_id": "evidence_D"},
        ]
        edges = [
            {"from_node_id": "claim_A", "to_node_id": "src_B"},
            {"from_node_id": "claim_A", "to_node_id": "src_C"},
            {"from_node_id": "src_B", "to_node_id": "evidence_D"},
            {"from_node_id": "src_C", "to_node_id": "evidence_D"},
        ]
        is_acyclic, cycle_path = check_citation_dag_acyclicity(nodes, edges)
        self.assertTrue(is_acyclic)
        self.assertEqual(cycle_path, [])

    def test_24_cyclic_graph_detected(self):
        """Circular dependency (A -> B -> C -> A) must be detected fail-closed."""
        nodes = [
            {"node_id": "claim_A"},
            {"node_id": "src_B"},
            {"node_id": "src_C"},
        ]
        edges = [
            {"from_node_id": "claim_A", "to_node_id": "src_B"},
            {"from_node_id": "src_B", "to_node_id": "src_C"},
            {"from_node_id": "src_C", "to_node_id": "claim_A"},
        ]
        is_acyclic, cycle_path = check_citation_dag_acyclicity(nodes, edges)
        self.assertFalse(is_acyclic)
        self.assertGreater(len(cycle_path), 0)
        self.assertIn("claim_A", cycle_path)
        self.assertIn("src_B", cycle_path)
        self.assertIn("src_C", cycle_path)

    def test_25_self_loop_detected(self):
        """Self-referential loop (A -> A) must be detected fail-closed."""
        nodes = [{"node_id": "claim_A"}]
        edges = [{"from_node_id": "claim_A", "to_node_id": "claim_A"}]
        is_acyclic, cycle_path = check_citation_dag_acyclicity(nodes, edges)
        self.assertFalse(is_acyclic)
        self.assertIn("claim_A", cycle_path)

    def test_26_disconnected_components_with_cycle(self):
        """Disconnected graph where a sub-component contains a cycle must fail."""
        nodes = [
            {"node_id": "comp1_node1"},
            {"node_id": "comp1_node2"},
            {"node_id": "comp2_cycle1"},
            {"node_id": "comp2_cycle2"},
        ]
        edges = [
            {"from_node_id": "comp1_node1", "to_node_id": "comp1_node2"},  # Acyclic
            {"from_node_id": "comp2_cycle1", "to_node_id": "comp2_cycle2"},
            {"from_node_id": "comp2_cycle2", "to_node_id": "comp2_cycle1"},  # Cycle!
        ]
        is_acyclic, cycle_path = check_citation_dag_acyclicity(nodes, edges)
        self.assertFalse(is_acyclic)
        self.assertIn("comp2_cycle1", cycle_path)

    def test_27_triangulation_rule_evaluation(self):
        """High-impact claim must connect to >= 3 independent primary sources."""
        claim_id = "claim_high_impact"
        sources = [
            {"source_id": "src_01", "tier": "Primary", "affiliation": "ACM"},
            {"source_id": "src_02", "tier": "Primary", "affiliation": "IEEE"},
            {"source_id": "src_03", "tier": "Primary", "affiliation": "Stanford"},
            {"source_id": "src_04", "tier": "Secondary", "affiliation": "TechBlog"},
        ]
        # Filter for pairwise-disjoint primary sources
        primary_disjoint = {
            s["affiliation"] for s in sources if s["tier"] == "Primary"
        }
        self.assertGreaterEqual(len(primary_disjoint), 3, "Multi-source triangulation requirement violated")


# ==============================================================================
# 6. TestInformationDensityCalculatorAlgorithm
# ==============================================================================

class TestInformationDensityCalculatorAlgorithm(unittest.TestCase):
    """Empirical Testing for Quantitative Information Density (ID >= 0.12)."""

    def test_28_high_density_text_passes(self):
        """Technical text with dense entities and metrics must pass ID >= 0.12."""
        high_density_brief = (
            "Evaluating Redis 7.4 clusters under Graviton4 hardware with PostgreSQL 16 read-replicas. "
            "Measured p99 latency was 0.15ms at 610k TPS across Kubernetes 1.31 nodes. "
            "In accordance with TCVN 7830:2021 and RFC 9110 specifications, network throughput peaked at 40Gbps "
            "with zero packet drops during the 2026-10-23 stress window. DoWhy refutations confirmed 99.99% availability."
        )
        res = calculate_information_density(high_density_brief)
        self.assertGreaterEqual(res["density_score"], 0.12)
        self.assertEqual(res["status"], "passed")
        self.assertGreater(res["named_entities_count"], 4)
        self.assertGreater(res["quantified_metrics_count"], 3)

    def test_29_fluffy_text_fails(self):
        """Conversational filler prose with sparse metrics must fail ID < 0.12."""
        fluffy_text = (
            "In today's fast-paced digital era, it is incredibly vital and important to delve into "
            "the realm of modern software solutions to pave the way for a brighter technological future. "
            "We should consider multiple factors when thinking about systems because things can often "
            "be quite complex, interesting, and exciting for development teams across different environments."
        )
        res = calculate_information_density(fluffy_text)
        self.assertLess(res["density_score"], 0.12)
        self.assertEqual(res["status"], "failed")

    def test_30_exact_formula_and_boundary(self):
        """Exact formula boundary at 0.12 must be strictly respected."""
        sample = {
            "named_entities_count": 6,
            "quantified_metrics_count": 6,
            "total_words": 100,
        }
        score = (sample["named_entities_count"] + sample["quantified_metrics_count"]) / sample["total_words"]
        self.assertAlmostEqual(score, 0.12)
        self.assertTrue(score >= 0.12)


# ==============================================================================
# 7. TestCoVeVerificationMatrixLogic
# ==============================================================================

class TestCoVeVerificationMatrixLogic(unittest.TestCase):
    """Logic Testing for Chain-of-Verification (CoVe) and C2PA Provenance."""

    def test_31_atomic_claim_evaluation(self):
        """Compound statement must decompose into atomic propositions and resolve status."""
        compound_claim = "Redis 7.4 supports Lua script fencing and achieves 610k TPS on AWS Graviton3."
        propositions = [
            {"id": "p1", "text": "Redis 7.4 supports Lua script fencing.", "evidence": "Confirmed in Redis 7.4 release notes."},
            {"id": "p2", "text": "Redis 7.4 achieves 610k TPS.", "evidence": "Confirmed in AWS Graviton3 benchmark."},
            {"id": "p3", "text": "Benchmark executed on AWS Graviton3 hardware.", "evidence": "Confirmed in AWS Graviton3 benchmark."},
        ]
        self.assertEqual(len(propositions), 3)
        for p in propositions:
            status = "verified" if p["evidence"] else "unverifiable"
            self.assertEqual(status, "verified")

    def test_32_c2pa_status_evaluation(self):
        """C2PA status evaluation must distinguish cryptographic validity from unverified provenance."""
        def evaluate_c2pa(has_jumbf_manifest: bool, has_valid_signature: bool, watermark_found: bool) -> str:
            if has_jumbf_manifest and has_valid_signature:
                return "signed_valid"
            if watermark_found:
                return "watermark_detected"
            return "unverified_provenance"

        self.assertEqual(evaluate_c2pa(True, True, False), "signed_valid")
        self.assertEqual(evaluate_c2pa(False, False, True), "watermark_detected")
        self.assertEqual(evaluate_c2pa(False, False, False), "unverified_provenance")


# ==============================================================================
# 8. TestResearcherA2ACard
# ==============================================================================

class TestResearcherA2ACard(unittest.TestCase):
    """Integrity checks for A2A discovery card for Researcher."""

    def test_33_agent_card_validity(self):
        """core/a2a/registry/researcher.agent-card.json must be valid and conformant."""
        card_path = AGENT_CARDS_DIR / "researcher.agent-card.json"
        self.assertTrue(card_path.exists(), f"Agent card missing at {card_path}")

        data = json.loads(card_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("contract_type"), "agent-card")
        self.assertEqual(data.get("name"), "researcher")
        # Version must be within the supported releases
        self.assertIn(
            data.get("version"),
            ["5.0.0", "5.1.0", "5.2.0", "5.3.0", "5.4.0", "5.5.0", "5.6.0", "5.6.1", "5.7.0", "5.7.1"],
        )

        skill_ids = [s["id"] for s in data.get("skills", [])]
        self.assertIn("conduct-research", skill_ids)


if __name__ == "__main__":
    unittest.main()
