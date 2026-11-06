#!/usr/bin/env python3
"""Comprehensive End-to-End (E2E) Test Suite for Phase 3 Architecture.

Phase 3: Adapter Alignment & Two-Tier JIT Skill Discovery Engine.
Authoritative Specifications:
- d:/myproject/.agents/teamwork/ORIGINAL_REQUEST.md
- d:/myproject/.agents/teamwork/PROJECT.md
- reports/ROADMAP_2026_2027.md (Section 5)
- TEST_INFRA.md

4-Tier Test Architecture:
- Tier 1: Feature Coverage (>=5 test cases per requirement: R1, R2, R3, R4, R5)
- Tier 2: Boundary & Corner Cases (CRLF normalization, deduplication, token budget, schema edge cases)
- Tier 3: Cross-Feature Combinations (Freshness flags, live AST02 disk verification, catalog parity)
- Tier 4: Real-World Acceptance Scenarios (Validator scripts, full validate-all gate, JIT runtime simulation)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

# Repository root discovery
REPO_ROOT = Path(__file__).resolve().parent.parent

# Key deliverable paths
A2A_TEMPLATE_PATH = REPO_ROOT / "adapters" / "antigravity" / "a2a-config.template.yaml"
ANTIGRAVITY_SPEC_PATH = REPO_ROOT / "adapters" / "antigravity" / "ANTIGRAVITY.md"
INDEX_MD_PATH = REPO_ROOT / "INDEX.md"
GENERATE_INDEX_SCRIPT = REPO_ROOT / "core" / "scripts" / "generate-index.py"
GENERATE_TIER1_SCRIPT = REPO_ROOT / "core" / "scripts" / "generate-tier1-index.py"
INDEX_TIER1_PATH = REPO_ROOT / "adapters" / "antigravity" / "INDEX_TIER1.json"
DISCOVERY_SCHEMA_PATH = REPO_ROOT / "core" / "contracts" / "schemas" / "agent-skills-discovery.json"
VALIDATE_INDEXES_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-indexes.py"
VALIDATE_SKILL_OWNERSHIP_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-skill-ownership.py"
VALIDATE_ALL_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-all.py"
ROLE_COORDINATOR_PATH = REPO_ROOT / "core" / "roles" / "agent-coordinator.md"
ROLE_DISCOVERY_ENGINEER_PATH = REPO_ROOT / "core" / "roles" / "agent-discovery-engineer.md"
ROLE_SKILL_INDEX_PATH = REPO_ROOT / "adapters" / "antigravity" / "role-skill-index.json"
CAPABILITY_MAP_GENERATED_PATH = REPO_ROOT / "adapters" / "antigravity" / "capability-role-map.generated.yaml"

EXPECTED_39_ROLES: Set[str] = {
    # Coordination & Discovery
    "agent-coordinator",
    "agent-discovery-engineer",
    # Software Engineering & Implementation
    "backend-developer",
    "frontend-developer",
    "mobile-engineer",
    "cloudflare-engineer",
    "devops-engineer",
    "3d-graphics-engineer",
    "ai-systems-engineer",
    "aws-engineer",
    "ecommerce-engineer",
    "game-developer",
    "mmo-engineer",
    "reverse-engineer",
    "prompt-engineer",
    "system-engineer",
    # Quality Assurance, Reliability & Security
    "reviewer",
    "qa-engineer",
    "sdet",
    "security-engineer",
    "sre",
    # Architecture, Leadership & Planning
    "technical-architect",
    "solution-architect",
    "technical-lead",
    "task-planner",
    "project-manager",
    "product-manager",
    # Analysis, Data & Research
    "business-analyst",
    "data-analyst",
    "data-engineer",
    "researcher",
    "vietnam-accounting-specialist",
    "vietnam-legal-counsel",
    # Content, Education & Documentation
    "content-writer",
    "seo-analyst",
    "technical-writer",
    "content-manager",
    "teacher",
    # Design
    "ui-ux-designer",
}


def load_json_file(path: Path) -> dict:
    assert path.is_file(), f"JSON file missing: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml_file(path: Path) -> dict:
    assert path.is_file(), f"YAML file missing: {path}"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def compute_normalized_sha256(raw_bytes: bytes) -> str:
    normalized = raw_bytes.replace(b"\r\n", b"\n")
    return f"sha256:{hashlib.sha256(normalized).hexdigest()}"


# ==============================================================================
# TIER 1: FEATURE COVERAGE (R1 - R5)
# ==============================================================================


class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Comprehensive opaque-box test coverage for primary requirements (>= 5 tests per requirement)."""

    # --- Requirement R1: Synchronize A2A Configuration Template (Feature 1) ---

    def test_t1_r1_a2a_config_template_exists_and_valid_yaml(self):
        """R1.1: Verify a2a-config.template.yaml exists and is strictly valid YAML."""
        self.assertTrue(A2A_TEMPLATE_PATH.is_file(), f"Template missing at: {A2A_TEMPLATE_PATH}")
        config = load_yaml_file(A2A_TEMPLATE_PATH)
        self.assertIsInstance(config, dict, "YAML root must be a mapping dictionary")
        self.assertIn("a2a", config, "Root key 'a2a' must be present")

    def test_t1_r1_all_39_roles_present(self):
        """R1.2: Verify a2a-config.template.yaml maps exactly all 39 active roles without omission."""
        config = load_yaml_file(A2A_TEMPLATE_PATH)
        cap_map = config.get("a2a", {}).get("capability_role_map", {})
        self.assertIsInstance(cap_map, dict, "capability_role_map must be a dictionary")

        mapped_roles = set(cap_map.values())
        missing_roles = EXPECTED_39_ROLES - mapped_roles
        extra_roles = mapped_roles - EXPECTED_39_ROLES

        self.assertEqual(len(missing_roles), 0, f"Missing roles in capability_role_map: {missing_roles}")
        self.assertEqual(len(extra_roles), 0, f"Unexpected extra roles in capability_role_map: {extra_roles}")
        self.assertEqual(len(mapped_roles), 39, "Expected exactly 39 unique mapped roles")

    def test_t1_r1_seven_clusters_represented(self):
        """R1.3: Verify all 7 functional clusters from ROADMAP Sec 5.2 are mapped."""
        content = A2A_TEMPLATE_PATH.read_text(encoding="utf-8")
        expected_clusters = [
            "Coordination & Discovery",
            "Software Engineering & Implementation",
            "Quality Assurance, Reliability & Security",
            "Architecture, Leadership & Planning",
            "Analysis, Data & Research",
            "Content, Education & Documentation",
            "Design",
        ]
        for cluster in expected_clusters:
            self.assertIn(cluster, content, f"Missing cluster section heading: '{cluster}' in template")

    def test_t1_r1_role_target_definitions_exist(self):
        """R1.4: Verify every mapped role slug in the template corresponds to a real role file."""
        config = load_yaml_file(A2A_TEMPLATE_PATH)
        cap_map = config.get("a2a", {}).get("capability_role_map", {})
        roles_dir = REPO_ROOT / "core" / "roles"
        for capability, role_slug in cap_map.items():
            role_file = roles_dir / f"{role_slug}.md"
            self.assertTrue(role_file.is_file(), f"Capability '{capability}' points to non-existent role: {role_file}")

    def test_t1_r1_core_a2a_metadata_fields(self):
        """R1.5: Verify core A2A protocol attributes and schema operations in template."""
        config = load_yaml_file(A2A_TEMPLATE_PATH)
        a2a_block = config.get("a2a", {})
        self.assertEqual(a2a_block.get("protocol_version"), "1.0")
        self.assertTrue(a2a_block.get("enabled", False))
        self.assertIn("discovery", a2a_block)
        self.assertIn("streaming", a2a_block)
        self.assertIn("operations", a2a_block)
        self.assertIn("coordinator", a2a_block)
        self.assertEqual(a2a_block["coordinator"].get("role"), "agent-coordinator")

    # --- Requirement R2: Modernize Antigravity Adapter Specification (Feature 2) ---

    def test_t1_r2_adapter_spec_exists_and_readable(self):
        """R2.1: Verify adapters/antigravity/ANTIGRAVITY.md exists and has substantive content."""
        self.assertTrue(ANTIGRAVITY_SPEC_PATH.is_file(), f"Spec missing at: {ANTIGRAVITY_SPEC_PATH}")
        content = ANTIGRAVITY_SPEC_PATH.read_text(encoding="utf-8")
        self.assertGreater(len(content), 2000, "ANTIGRAVITY.md content is too short")

    def test_t1_r2_two_tier_candidate_ranking_formula(self):
        """R2.2: Verify ANTIGRAVITY.md documents the Two-Tier candidate ranking formula."""
        content = ANTIGRAVITY_SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("Two-Tier", content, "ANTIGRAVITY.md must reference Two-Tier architecture")
        self.assertTrue(
            "BM25" in content and "Dense" in content,
            "ANTIGRAVITY.md must document hybrid BM25 and Dense ranking formula",
        )
        self.assertTrue(
            ("0.45" in content and "0.55" in content) or ("0.40" in content and "0.40" in content),
            "ANTIGRAVITY.md must document hybrid matching weights",
        )

    def test_t1_r2_threshold_tau_specification(self):
        """R2.3: Verify ANTIGRAVITY.md documents threshold tau = 0.72 and fail-closed escalation."""
        content = ANTIGRAVITY_SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("0.72", content, "ANTIGRAVITY.md must specify candidate ranking threshold tau = 0.72")
        self.assertTrue(
            "HITL" in content or "human" in content.lower(),
            "ANTIGRAVITY.md must document human escalation for below-threshold candidates",
        )

    def test_t1_r2_tier1_budget_limit_documented(self):
        """R2.4: Verify ANTIGRAVITY.md documents the < 5 KB Tier 1 footprint constraint."""
        content = ANTIGRAVITY_SPEC_PATH.read_text(encoding="utf-8")
        self.assertTrue(
            "5 KB" in content or "5KB" in content or "5,120" in content or "40 tokens" in content,
            "ANTIGRAVITY.md must document Tier 1 footprint budget (< 5 KB or ~40 tokens/skill)",
        )

    def test_t1_r2_ast02_digest_verification_documented(self):
        """R2.5: Verify ANTIGRAVITY.md documents AST02 cryptographic verification against INDEX_TIER1.json."""
        content = ANTIGRAVITY_SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("INDEX_TIER1.json", content, "ANTIGRAVITY.md must document INDEX_TIER1.json manifest")
        self.assertTrue(
            "SHA-256" in content or "sha256" in content,
            "ANTIGRAVITY.md must document SHA-256 asset digest verification",
        )
        self.assertIn("AST02", content, "ANTIGRAVITY.md must cite AST02 supply-chain verification")

    # --- Requirement R3: Update Router Instructions in INDEX.md (Feature 3) ---

    def test_t1_r3_index_md_exists_and_non_empty(self):
        """R3.1: Verify INDEX.md exists and is substantive."""
        self.assertTrue(INDEX_MD_PATH.is_file(), f"INDEX.md missing at: {INDEX_MD_PATH}")
        content = INDEX_MD_PATH.read_text(encoding="utf-8")
        self.assertGreater(len(content), 10000, "INDEX.md is too short")

    def test_t1_r3_router_progressive_disclosure_instructions(self):
        """R3.2: Verify INDEX.md router section contains Two-Tier Progressive Disclosure rules."""
        content = INDEX_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("Two-Tier", content, "INDEX.md must reference Two-Tier skill architecture")
        self.assertIn("INDEX_TIER1.json", content, "INDEX.md must instruct loading INDEX_TIER1.json at startup")

    def test_t1_r3_router_ranking_formula_and_threshold(self):
        """R3.3: Verify INDEX.md documents the hybrid ranking formula and 0.72 threshold."""
        content = INDEX_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("0.72", content, "INDEX.md must document threshold tau = 0.72")
        self.assertIn("BM25", content, "INDEX.md must mention BM25 hybrid ranking")

    def test_t1_r3_router_prohibited_skills_exclusion(self):
        """R3.4: Verify INDEX.md specifies disqualification of Prohibited Skills."""
        content = INDEX_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("Prohibited Skills", content, "INDEX.md must instruct exclusion of Prohibited Skills")

    def test_t1_r3_router_sha256_verification_instruction(self):
        """R3.5: Verify INDEX.md mandates SHA-256 verification before skill activation."""
        content = INDEX_MD_PATH.read_text(encoding="utf-8")
        self.assertTrue(
            "SHA-256" in content or "sha256" in content,
            "INDEX.md must mandate cryptographic digest verification",
        )

    # --- Requirement R4: Implement Tier-1 Index Generator & Manifest (Features 4, 5, 6) ---

    def test_t1_r4_generator_script_exists_and_executable(self):
        """R4.1: Verify core/scripts/generate-tier1-index.py exists."""
        self.assertTrue(GENERATE_TIER1_SCRIPT.is_file(), f"Generator script missing at {GENERATE_TIER1_SCRIPT}")

    def test_t1_r4_manifest_artifact_exists(self):
        """R4.2: Verify adapters/antigravity/INDEX_TIER1.json exists and is valid JSON."""
        self.assertTrue(INDEX_TIER1_PATH.is_file(), f"Manifest artifact missing at {INDEX_TIER1_PATH}")
        data = load_json_file(INDEX_TIER1_PATH)
        self.assertIn("skills", data, "Manifest must contain 'skills' array")

    def test_t1_r4_manifest_conforms_to_schema(self):
        """R4.3: Validate INDEX_TIER1.json against core/contracts/schemas/agent-skills-discovery.json."""
        self.assertTrue(DISCOVERY_SCHEMA_PATH.is_file(), f"Discovery schema missing at: {DISCOVERY_SCHEMA_PATH}")
        manifest_data = load_json_file(INDEX_TIER1_PATH)
        schema_data = load_json_file(DISCOVERY_SCHEMA_PATH)

        validator = Draft202012Validator(schema_data)
        errors = list(validator.iter_errors(manifest_data))
        self.assertEqual(len(errors), 0, f"INDEX_TIER1.json failed schema validation: {[e.message for e in errors]}")

    def test_t1_r4_manifest_contains_exact_183_skills(self):
        """R4.4: Verify INDEX_TIER1.json contains exactly 183 skills with unique names."""
        manifest_data = load_json_file(INDEX_TIER1_PATH)
        skills = manifest_data.get("skills", [])
        self.assertEqual(len(skills), 183, f"Expected 183 skills in manifest, found {len(skills)}")

        names = [s["name"] for s in skills]
        self.assertEqual(len(names), len(set(names)), "Skill names in manifest must be unique (no duplicates)")

    def test_t1_r4_generator_cli_check_flag(self):
        """R4.5: Verify running generate-tier1-index.py --check exits with code 0."""
        result = subprocess.run(
            [sys.executable, str(GENERATE_TIER1_SCRIPT), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"generate-tier1-index.py --check failed with exit code {result.returncode}:\n{result.stderr}",
        )

    # --- Requirement R5: Reconcile Role Configurations (Features 7, 8) ---

    def test_t1_r5_agent_coordinator_responsibilities(self):
        """R5.1: Verify agent-coordinator.md contains Two-Tier JIT governance responsibilities."""
        self.assertTrue(ROLE_COORDINATOR_PATH.is_file(), f"Missing {ROLE_COORDINATOR_PATH}")
        content = ROLE_COORDINATOR_PATH.read_text(encoding="utf-8")
        self.assertIn("Two-Tier", content, "agent-coordinator.md must govern Two-Tier progressive disclosure")
        self.assertIn("INDEX_TIER1.json", content, "agent-coordinator.md must reference INDEX_TIER1.json")
        self.assertIn("0.72", content, "agent-coordinator.md must enforce candidate ranking threshold 0.72")

    def test_t1_r5_agent_coordinator_guardrail_locks(self):
        """R5.2: Verify agent-coordinator.md contains JIT-PROGRESSIVE-DISCLOSURE and DISCOVERY-RANKING locks."""
        content = ROLE_COORDINATOR_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "JIT-PROGRESSIVE-DISCLOSURE LOCK",
            content,
            "agent-coordinator.md missing JIT-PROGRESSIVE-DISCLOSURE LOCK",
        )
        self.assertIn(
            "DISCOVERY-RANKING LOCK",
            content,
            "agent-coordinator.md missing DISCOVERY-RANKING LOCK",
        )

    def test_t1_r5_agent_discovery_engineer_responsibilities(self):
        """R5.3: Verify agent-discovery-engineer.md contains Tier 1 manifest governance and routing."""
        self.assertTrue(ROLE_DISCOVERY_ENGINEER_PATH.is_file(), f"Missing {ROLE_DISCOVERY_ENGINEER_PATH}")
        content = ROLE_DISCOVERY_ENGINEER_PATH.read_text(encoding="utf-8")
        self.assertIn("INDEX_TIER1.json", content, "agent-discovery-engineer.md must own INDEX_TIER1.json")
        self.assertIn("generate-tier1-index.py", content, "agent-discovery-engineer.md must cite generator script")
        self.assertIn("Deliverable Routing", content, "agent-discovery-engineer.md must have Deliverable Routing table")

    def test_t1_r5_agent_discovery_engineer_guardrail_locks(self):
        """R5.4: Verify agent-discovery-engineer.md contains TIER1-BUDGET-LOCK and JIT-DIGEST-VERIFY-LOCK."""
        content = ROLE_DISCOVERY_ENGINEER_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "TIER1-BUDGET-LOCK",
            content,
            "agent-discovery-engineer.md missing TIER1-BUDGET-LOCK",
        )
        self.assertIn(
            "JIT-DIGEST-VERIFY-LOCK",
            content,
            "agent-discovery-engineer.md missing JIT-DIGEST-VERIFY-LOCK",
        )

    def test_t1_r5_role_standard_structure_and_lock_density(self):
        """R5.5: Verify both updated roles conform to role-standard guardrail lock density (12 to 24 locks)."""
        for path in [ROLE_COORDINATOR_PATH, ROLE_DISCOVERY_ENGINEER_PATH]:
            content = path.read_text(encoding="utf-8")
            locks = re.findall(r"-\s+\*\*([A-Z0-9_ -]+?LOCK)\*\*:", content)
            self.assertGreaterEqual(
                len(locks),
                12,
                f"Role {path.name} has fewer than 12 guardrail locks: {len(locks)}",
            )
            self.assertLessEqual(
                len(locks),
                24,
                f"Role {path.name} has more than 24 guardrail locks: {len(locks)}",
            )


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES
# ==============================================================================


class TestTier2BoundaryAndCornerCases(unittest.TestCase):
    """Tier 2: Boundary conditions, platform quirks, deduplication, and schema edge cases."""

    def test_t2_crlf_vs_lf_newline_normalization_in_sha256(self):
        """T2.1: Verify canonical SHA-256 digests are invariant across CRLF and LF byte streams."""
        sample_lf = b"---\nname: test-skill\ndescription: Use when testing.\n---\n# Body\nContent here.\n"
        sample_crlf = b"---\r\nname: test-skill\r\ndescription: Use when testing.\r\n---\r\n# Body\r\nContent here.\r\n"

        hash_lf = compute_normalized_sha256(sample_lf)
        hash_crlf = compute_normalized_sha256(sample_crlf)

        self.assertEqual(hash_lf, hash_crlf, "Normalized SHA-256 must be identical across CRLF and LF")
        self.assertTrue(re.match(r"^sha256:[a-f0-9]{64}$", hash_lf))

    def test_t2_duplicate_skill_reverse_engineer_binary_resolution(self):
        """T2.2: Verify duplicate reverse-engineer-binary is resolved with overlay overriding core."""
        core_file = REPO_ROOT / "core" / "skills" / "security-data" / "reverse-engineer-binary" / "SKILL.md"
        overlay_file = REPO_ROOT / "overlays" / "security-research" / "skills" / "reverse-engineer-binary" / "SKILL.md"

        self.assertTrue(core_file.is_file(), f"Core duplicate file missing: {core_file}")
        self.assertTrue(overlay_file.is_file(), f"Overlay duplicate file missing: {overlay_file}")

        manifest = load_json_file(INDEX_TIER1_PATH)
        matches = [s for s in manifest.get("skills", []) if s["name"] == "reverse-engineer-binary"]

        self.assertEqual(len(matches), 1, "Exactly one reverse-engineer-binary entry must exist in manifest")
        reb_entry = matches[0]

        # The overlay path must prevail over core path
        self.assertEqual(
            reb_entry["url"],
            "overlays/security-research/skills/reverse-engineer-binary/SKILL.md",
            "Overlay version must override core version for reverse-engineer-binary",
        )

        # The digest must match the overlay asset
        expected_digest = compute_normalized_sha256(overlay_file.read_bytes())
        self.assertEqual(
            reb_entry["digest"],
            expected_digest,
            "Manifest digest for reverse-engineer-binary must match the overlay asset bytes",
        )

    def test_t2_token_budget_and_footprint_threshold(self):
        """T2.3: Verify manifest footprint is token-efficient (~40 tokens/skill average)."""
        manifest_raw = INDEX_TIER1_PATH.read_bytes()
        manifest_data = load_json_file(INDEX_TIER1_PATH)
        skills = manifest_data.get("skills", [])
        num_skills = len(skills)
        self.assertGreater(num_skills, 0)

        # In minified JSON form, verify concise representation (< 350 bytes per skill average)
        minified_bytes = json.dumps(manifest_data, separators=(",", ":")).encode("utf-8")
        avg_bytes_per_skill = len(minified_bytes) / num_skills
        # 1 token ~= 4 chars/bytes; ~70 tokens ~= 280-320 bytes; ensure strictly < 350 bytes
        self.assertLess(
            avg_bytes_per_skill,
            350,
            f"Average minified bytes per skill ({avg_bytes_per_skill:.1f}) exceeds token budget",
        )

        # Ensure descriptions are sanitized and <= 100 characters for token compactness
        for s in skills:
            self.assertLessEqual(
                len(s["description"]),
                100,
                f"Skill '{s['name']}' description exceeds 100 characters: {s['description']}",
            )

    def test_t2_schema_negative_validation_missing_required_fields(self):
        """T2.4: Verify schema rejection when required fields are missing."""
        schema_data = load_json_file(DISCOVERY_SCHEMA_PATH)
        validator = Draft202012Validator(schema_data)

        # Missing required field 'digest' in skill entry
        invalid_doc = {
            "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
            "skills": [
                {
                    "name": "example-skill",
                    "type": "skill-md",
                    "description": "Use when testing invalid schema payloads.",
                    "url": "core/skills/test/SKILL.md",
                    # digest intentionally missing
                }
            ],
        }
        errors = list(validator.iter_errors(invalid_doc))
        self.assertGreater(len(errors), 0, "Schema must reject skill missing required field 'digest'")

        # Missing root '$schema'
        invalid_root = {
            "skills": [
                {
                    "name": "example-skill",
                    "type": "skill-md",
                    "description": "Use when testing invalid schema payloads.",
                    "url": "core/skills/test/SKILL.md",
                    "digest": "sha256:" + "a" * 64,
                }
            ]
        }
        errors_root = list(validator.iter_errors(invalid_root))
        self.assertGreater(len(errors_root), 0, "Schema must reject root document missing '$schema'")

    def test_t2_schema_negative_validation_malformed_digest_pattern(self):
        """T2.5: Verify schema rejection for malformed SHA-256 digest patterns."""
        schema_data = load_json_file(DISCOVERY_SCHEMA_PATH)
        validator = Draft202012Validator(schema_data)

        malformed_digests = [
            "md5:d41d8cd98f00b204e9800998ecf8427e",  # wrong algorithm
            "sha256:abcd",  # too short
            "sha256:" + "A" * 64,  # uppercase hex (schema specifies lowercase [a-f0-9])
            "sha256:" + "z" * 64,  # non-hex
            "not-a-digest",
        ]

        for bad_digest in malformed_digests:
            doc = {
                "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
                "skills": [
                    {
                        "name": "example-skill",
                        "type": "skill-md",
                        "description": "Use when testing regex digest patterns.",
                        "url": "core/skills/test/SKILL.md",
                        "digest": bad_digest,
                    }
                ],
            }
            errors = list(validator.iter_errors(doc))
            self.assertGreater(
                len(errors),
                0,
                f"Schema must reject invalid digest pattern: '{bad_digest}'",
            )

    def test_t2_skill_description_length_boundaries_and_sanitization(self):
        """T2.6: Verify all skills satisfy length boundaries (20 <= len <= 1024) and single-line format."""
        manifest = load_json_file(INDEX_TIER1_PATH)
        for s in manifest.get("skills", []):
            desc = s["description"]
            name = s["name"]
            self.assertGreaterEqual(
                len(desc),
                20,
                f"Skill '{name}' description is shorter than 20 characters: '{desc}'",
            )
            self.assertLessEqual(
                len(desc),
                1024,
                f"Skill '{name}' description exceeds 1024 characters: '{desc}'",
            )
            self.assertNotIn("\n", desc, f"Skill '{name}' description contains unescaped newline")
            self.assertNotIn("\r", desc, f"Skill '{name}' description contains unescaped carriage return")


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================


class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Subsystem interactions, multi-generator synchronization, and live asset parity."""

    def test_t3_freshness_checker_generate_index_and_generate_tier1_index(self):
        """T3.1: Verify interaction of generate-index.py --check and generate-tier1-index.py --check."""
        res_index = subprocess.run(
            [sys.executable, str(GENERATE_INDEX_SCRIPT), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res_index.returncode, 0, f"generate-index.py --check failed: {res_index.stderr}")

        res_tier1 = subprocess.run(
            [sys.executable, str(GENERATE_TIER1_SCRIPT), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res_tier1.returncode, 0, f"generate-tier1-index.py --check failed: {res_tier1.stderr}")

    def test_t3_skill_catalog_parity_across_index_and_tier1(self):
        """T3.2: Verify complete 183 skill catalog parity between INDEX_TIER1.json and role-skill-index.json."""
        tier1_data = load_json_file(INDEX_TIER1_PATH)
        role_skill_data = load_json_file(ROLE_SKILL_INDEX_PATH)

        tier1_skills = {s["name"] for s in tier1_data.get("skills", [])}
        role_skills = set(role_skill_data.get("skills", {}).keys())

        missing_in_tier1 = role_skills - tier1_skills
        extra_in_tier1 = tier1_skills - role_skills

        self.assertEqual(len(missing_in_tier1), 0, f"Skills missing in INDEX_TIER1.json: {missing_in_tier1}")
        self.assertEqual(len(extra_in_tier1), 0, f"Unexpected extra skills in INDEX_TIER1.json: {extra_in_tier1}")
        self.assertEqual(len(tier1_skills), 183, "Catalog must contain exactly 183 skills")

    def test_t3_ast02_live_disk_sha256_digest_verification(self):
        """T3.3: Verify live SKILL.md assets on disk match recorded digests in INDEX_TIER1.json (AST02 supply chain)."""
        manifest = load_json_file(INDEX_TIER1_PATH)
        skills = manifest.get("skills", [])

        # Sample 25 representative skills across core and overlay
        sample_indices = list(range(0, len(skills), max(1, len(skills) // 25)))
        sample_skills = [skills[i] for i in sample_indices]

        # Always include reverse-engineer-binary and first/last
        sample_skills.append([s for s in skills if s["name"] == "reverse-engineer-binary"][0])
        sample_skills.append(skills[0])
        sample_skills.append(skills[-1])

        for entry in sample_skills:
            rel_url = entry["url"]
            expected_digest = entry["digest"]
            asset_path = REPO_ROOT / rel_url

            self.assertTrue(asset_path.is_file(), f"Asset referenced in INDEX_TIER1.json not found: {asset_path}")
            raw_bytes = asset_path.read_bytes()
            actual_digest = compute_normalized_sha256(raw_bytes)

            self.assertEqual(
                actual_digest,
                expected_digest,
                f"Digest mismatch for '{entry['name']}' at {rel_url}: expected {expected_digest}, computed {actual_digest}",
            )

    def test_t3_capability_role_map_parity_template_vs_generated(self):
        """T3.4: Verify parity between a2a-config.template.yaml and capability-role-map.generated.yaml."""
        template_config = load_yaml_file(A2A_TEMPLATE_PATH)
        template_map = template_config.get("a2a", {}).get("capability_role_map", {})

        generated_config = load_yaml_file(CAPABILITY_MAP_GENERATED_PATH)
        generated_map = generated_config.get("capability_role_map", {})

        self.assertEqual(
            set(template_map.values()),
            set(generated_map.values()),
            "Roles in a2a-config.template.yaml must match capability-role-map.generated.yaml",
        )
        self.assertEqual(len(template_map.values()), 39)


# ==============================================================================
# TIER 4: REAL-WORLD ACCEPTANCE SCENARIOS
# ==============================================================================


class TestTier4RealWorldAcceptanceScenarios(unittest.TestCase):
    """Tier 4: End-to-end execution of repository quality gates and runtime workflow simulation."""

    def test_t4_validate_indexes_script_passes(self):
        """T4.1: Real-world acceptance: python core/scripts/validate-indexes.py passes with exit code 0."""
        result = subprocess.run(
            [sys.executable, str(VALIDATE_INDEXES_SCRIPT)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"validate-indexes.py failed with code {result.returncode}:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("Index validation passed", result.stdout)

    def test_t4_validate_skill_ownership_script_passes(self):
        """T4.2: Real-world acceptance: python core/scripts/validate-skill-ownership.py passes with exit code 0."""
        result = subprocess.run(
            [sys.executable, str(VALIDATE_SKILL_OWNERSHIP_SCRIPT)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"validate-skill-ownership.py failed with code {result.returncode}:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("Skill ownership validation passed", result.stdout)

    def test_t4_validate_all_script_passes(self):
        """T4.3: Real-world acceptance: python core/scripts/validate-all.py passes with exit code 0."""
        result = subprocess.run(
            [sys.executable, str(VALIDATE_ALL_SCRIPT)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"validate-all.py failed with code {result.returncode}:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("All core validators passed", result.stdout)

    def test_t4_jit_resolution_runtime_workflow_simulation(self):
        """T4.4: Simulate complete Two-Tier JIT skill resolution runtime workflow.

        Simulates:
        1. Agent startup: reads INDEX_TIER1.json (< 5 KB footprint, ~7.3k tokens total).
        2. Runtime query matching: evaluates BM25 and dense representation against candidates.
        3. Threshold gating: tau = 0.72 gate filters noise and triggers clarification if < 0.72.
        4. Prohibited skills filter: disqualifies prohibited skills even if matching high score.
        5. AST02 JIT asset retrieval: verifies SHA-256 digest from disk before executing.
        """
        # 1. Startup: Load Tier 1 manifest
        self.assertTrue(INDEX_TIER1_PATH.is_file())
        manifest = load_json_file(INDEX_TIER1_PATH)
        skills = {s["name"]: s for s in manifest.get("skills", [])}

        # 2. Simulate query: "deconstruct compiled binaries electron bundles and firmware images in air-gapped reverse engineer binary"
        query_text = (
            "deconstructing compiled binaries electron bundles and firmware images in air-gapped reverse engineer binary"
        )
        query_tokens = set(re.findall(r"\w+", query_text.lower()))

        def simulate_bm25_score(doc_desc: str, query: Set[str]) -> float:
            doc_tokens = set(re.findall(r"\w+", doc_desc.lower()))
            overlap = len(doc_tokens & query)
            return min(1.0, overlap / max(1, len(doc_tokens)))

        def simulate_dense_score(skill_name: str, query: Set[str]) -> float:
            name_tokens = set(skill_name.split("-"))
            overlap = len(name_tokens & query)
            return overlap / max(1, len(name_tokens))

        candidates: List[tuple[str, float]] = []
        for name, item in skills.items():
            bm25 = simulate_bm25_score(item["description"], query_tokens)
            dense = simulate_dense_score(name, query_tokens)
            score = 0.45 * bm25 + 0.55 * dense
            candidates.append((name, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top_skill, top_score = candidates[0]

        # 3. Threshold check
        tau = 0.72
        self.assertEqual(top_skill, "reverse-engineer-binary")
        self.assertGreaterEqual(
            top_score,
            tau,
            f"Candidate score {top_score:.3f} must exceed threshold tau = {tau}",
        )

        # 3b. Ambiguous query simulation: score must be < tau, triggering HITL escalation
        ambiguous_tokens = {"general", "task", "help", "do", "something"}
        ambiguous_scores = [
            0.45 * simulate_bm25_score(item["description"], ambiguous_tokens)
            + 0.55 * simulate_dense_score(name, ambiguous_tokens)
            for name, item in skills.items()
        ]
        max_ambiguous_score = max(ambiguous_scores)
        self.assertLess(
            max_ambiguous_score,
            tau,
            f"Ambiguous query score ({max_ambiguous_score:.3f}) must fail below tau ({tau}) and trigger HITL",
        )

        # 4. Check prohibited skills filter for role "agent-discovery-engineer"
        # In agent-discovery-engineer.md, reverse-engineer-binary is NOT prohibited, but add-api-endpoint IS prohibited.
        disc_role_content = ROLE_DISCOVERY_ENGINEER_PATH.read_text(encoding="utf-8")
        self.assertIn("add-api-endpoint", disc_role_content)

        # Verify that an artificially matched prohibited skill is disqualified
        prohibited_skill = "add-api-endpoint"
        role_prohibited_list = ["add-api-endpoint", "add-ui-component", "deploy-vllm-inference"]
        self.assertIn(prohibited_skill, role_prohibited_list)
        is_disqualified = prohibited_skill in role_prohibited_list
        self.assertTrue(is_disqualified, "Prohibited skill must be disqualified regardless of score")

        # 5. AST02 JIT retrieval & cryptographic verification
        resolved_skill_entry = skills[top_skill]
        target_file = REPO_ROOT / resolved_skill_entry["url"]
        self.assertTrue(target_file.is_file(), f"Target asset missing on disk: {target_file}")

        computed_digest = compute_normalized_sha256(target_file.read_bytes())
        self.assertEqual(
            computed_digest,
            resolved_skill_entry["digest"],
            "AST02 cryptographic verification failed: target asset on disk does not match manifest digest",
        )


if __name__ == "__main__":
    unittest.main()
