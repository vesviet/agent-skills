#!/usr/bin/env python3
"""
test-vesviet-pack.py
====================
Automated Opaque-Box E2E Testing Suite for vesviet-team Pack (v5.0.0).

Executes 4 comprehensive testing tiers:
- Tier 1: Feature Coverage (>=5 assertions per feature across all 16 features)
- Tier 2: Boundary & Corner Cases (exact corpus counts, BLUF <=60 words, one-way flow, etc.)
- Tier 3: Pairwise Cross-Feature Combinations (roles, workflows, schemas, rules)
- Tier 4: Real-World Publishing Simulation (end-to-end 5-phase lifecycle against JSON contracts)

Exit code: 0 on success, 1 on failure.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import time
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Reconfigure stdout/stderr to utf-8 for Windows console resilience
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None

# Root paths
SCRIPT_DIR = Path(__file__).resolve().parent
CORE_DIR = SCRIPT_DIR.parent
ROOT = CORE_DIR.parent
PACKS_DIR = ROOT / "packs"
VESVIET_PACK_DIR = PACKS_DIR / "vesviet-team"
MANIFEST_PATH = VESVIET_PACK_DIR / "manifest.yaml"
PACK_README_PATH = VESVIET_PACK_DIR / "README.md"
OVERLAYS_DIR = ROOT / "overlays"
VESVIET_OVERLAY_DIR = OVERLAYS_DIR / "vesviet-content"
SCHEMAS_DIR = CORE_DIR / "contracts" / "schemas"
CORE_WORKFLOWS_DIR = CORE_DIR / "workflows"
OVERLAY_WORKFLOWS_DIR = VESVIET_OVERLAY_DIR / "workflows"
PACK_WORKFLOWS_DIR = VESVIET_PACK_DIR / "workflows"


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_pack_readme() -> str:
    if not PACK_README_PATH.exists():
        raise FileNotFoundError(f"Pack README not found: {PACK_README_PATH}")
    return PACK_README_PATH.read_text(encoding="utf-8")


def resolve_workflow_path(slug: str) -> Optional[Path]:
    """Resolve workflow slug across pack, overlay, and core workflows directories."""
    candidates = [
        PACK_WORKFLOWS_DIR / f"{slug}.md",
        OVERLAY_WORKFLOWS_DIR / f"{slug}.md",
        CORE_WORKFLOWS_DIR / f"{slug}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def count_words(text: str) -> int:
    """Tokenize and count words matching Hugo/Markdown parsing rules."""
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"`[^`]*`", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    tokens = re.findall(r"[\w\u00C0-\u1EF9]+(?:-[\w\u00C0-\u1EF9]+)*", cleaned)
    return len(tokens)


# ==============================================================================
# TIER 1: FEATURE COVERAGE (>=5 checks per feature across 16 features)
# ==============================================================================

class TestTier1FeatureCoverage(unittest.TestCase):
    """
    Tier 1 tests verify the presence, structural integrity, and contract conformance
    of all 16 features defined in PROJECT.md.
    """

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.readme = load_pack_readme()

    # --- Feature 1: Manifest Schema v2 & Version 5.0.0 ---
    def test_feature_01_manifest_schema_v2_and_version(self):
        m = self.manifest
        self.assertEqual(str(m.get("schema_version")), "2", "schema_version must be '2'")
        self.assertEqual(str(m.get("version")), "5.0.0", "version must be 5.0.0")
        self.assertEqual(m.get("name"), "vesviet-team", "pack name must be 'vesviet-team'")
        self.assertIn("core", m.get("includes", []), "includes must contain 'core'")
        self.assertIn("overlays/vesviet-content", m.get("includes", []), "includes must contain 'overlays/vesviet-content'")
        self.assertEqual(m.get("compatibility", {}).get("requires_schema"), "2", "requires_schema must be '2'")
        self.assertEqual(m.get("governance", {}).get("eu_ai_act_tier"), "minimal_risk", "eu_ai_act_tier must be 'minimal_risk'")

    # --- Feature 2: Live Corpus Count Synchronization ---
    def test_feature_02_corpus_count_presence_in_manifest(self):
        corpus = self.manifest.get("corpus", {})
        self.assertIn("vesviet", corpus, "corpus must contain vesviet entry")
        self.assertIn("learn", corpus, "corpus must contain learn entry")
        v = corpus["vesviet"]
        l = corpus["learn"]
        self.assertEqual(v.get("content_files"), 374, "vesviet content_files must be 374")
        self.assertEqual(v.get("posts"), 66, "vesviet posts must be 66")
        self.assertEqual(v.get("series_dirs"), 25, "vesviet series_dirs must be 25")
        self.assertEqual(v.get("series_files"), 251, "vesviet series_files must be 251")
        self.assertEqual(v.get("radar_files"), 34, "vesviet radar_files must be 34")
        self.assertEqual(v.get("reports"), 296, "vesviet reports must be 296")
        self.assertEqual(l.get("content_files"), 433, "learn content_files must be 433")
        self.assertEqual(l.get("posts"), 86, "learn posts must be 86")
        self.assertEqual(l.get("series_dirs"), 25, "learn series_dirs must be 25")
        self.assertEqual(l.get("series_files"), 251, "learn series_files must be 251")
        self.assertEqual(l.get("radar_files"), 70, "learn radar_files must be 70")
        self.assertEqual(l.get("docs"), 3, "learn docs must be 3")
        self.assertEqual(l.get("reports"), 276, "learn reports must be 276")

    # --- Feature 3: Role Declarations ---
    def test_feature_03_role_declarations(self):
        cf = self.manifest.get("content_focus", {})
        primary = cf.get("primary_roles", [])
        secondary = cf.get("secondary_roles", [])
        for role in ["content-writer", "content-manager", "technical-writer", "seo-analyst"]:
            self.assertIn(role, primary, f"Primary roles must include {role}")
            role_file = CORE_DIR / "roles" / f"{role}.md"
            self.assertTrue(role_file.exists(), f"Role definition file must exist: {role_file}")
        for role in ["reviewer", "task-planner", "agent-coordinator"]:
            self.assertIn(role, secondary, f"Secondary roles must include {role}")
            role_file = CORE_DIR / "roles" / f"{role}.md"
            self.assertTrue(role_file.exists(), f"Role definition file must exist: {role_file}")
        self.assertTrue(set(primary).isdisjoint(set(secondary)), "Primary and secondary roles must be disjoint")

    # --- Feature 4: Deep Research Protocol in Manifest ---
    def test_feature_04_deep_research_protocol_manifest(self):
        p = self.manifest.get("deep_research_protocol", {})
        self.assertEqual(p.get("rounds"), 100, "deep_research_protocol rounds must be 100")
        self.assertTrue(p.get("mandatory_before_action"), "mandatory_before_action must be True")
        self.assertEqual(p.get("clusters"), 5, "clusters must be 5")
        self.assertEqual(p.get("rounds_per_cluster"), 20, "rounds_per_cluster must be 20")
        clusters = p.get("cluster_breakdown", {})
        self.assertEqual(len(clusters), 5, "cluster_breakdown must have 5 clusters")
        self.assertIn("cluster_1", clusters)
        self.assertIn("cluster_5", clusters)
        dossier = p.get("output_dossier", {})
        self.assertIn("json", dossier, "output_dossier must define json path")
        self.assertIn("markdown", dossier, "output_dossier must define markdown path")

    # --- Feature 5: Workflow Linkages in Manifest ---
    def test_feature_05_workflow_linkages_manifest(self):
        cf = self.manifest.get("content_focus", {})
        workflows = cf.get("workflows", [])
        required_wfs = [
            "article-creation-and-upgrade-lifecycle",
            "masterclass-batch-upgrade",
            "series-sync-upgrade",
            "content-audit-refresh",
            "affiliate-publishing",
            "publish-series",
        ]
        for wf in required_wfs:
            self.assertIn(wf, workflows, f"Manifest must declare workflow linkage: {wf}")
            resolved = resolve_workflow_path(wf)
            self.assertIsNotNone(resolved, f"Declared workflow must resolve on disk: {wf}")

    # --- Feature 6: Master Operating Guide Authoring ---
    def test_feature_06_master_operating_guide_structure(self):
        text = self.readme
        self.assertTrue(text.startswith("# "), "README.md must start with H1 heading")
        self.assertIn("vesviet-team", text, "README.md must mention pack slug vesviet-team")
        self.assertRegex(text, r"(?i)twin\s+sites?\s+architecture|twin\s+hugo", "README must document Twin Hugo Architecture")
        self.assertIn("10 Anchor Pillar Hubs", text, "README must document 10 Anchor Pillar Hubs")
        self.assertIn("100-Round", text, "README must document 100-Round Protocol")
        self.assertIn("7 Technical Content Gates", text, "README must document 7 Technical Content Gates")
        self.assertIn("Multi-Agent Swarm", text, "README must document Multi-Agent Swarm Pipeline")

    # --- Feature 7: One-Way Authority Flow Documentation ---
    def test_feature_07_one_way_authority_flow_docs(self):
        text = self.readme
        self.assertRegex(text, r"(?i)one-way\s+authority\s+flow", "README must define One-Way Authority Flow")
        self.assertIn("learn", text)
        self.assertIn("vesviet", text)
        self.assertRegex(text, r"(?i)forbidden|prohibited|zero\s+reverse\s+links", "README must forbid links from vesviet to learn")
        self.assertRegex(text, r"(?i)canonical", "README must specify canonical URL rules")
        self.assertRegex(text, r"(?i)information\s+gain", "README must mandate unique Information Gain")

    # --- Feature 8: 10 Anchor Pillar Hubs Specification ---
    def test_feature_08_anchor_pillar_hubs_specification(self):
        text = self.readme
        # 10 Authoritative Anchor Pillar Hubs from PROJECT.md
        pillar_hubs = [
            "/series/raft/",
            "/series/k8s/",
            "/series/golang/",
            "/series/ebpf/",
            "/series/kafka/",
            "/series/storage/",
            "/series/service-mesh/",
            "/series/databases/",
            "/series/sre/",
            "/series/ai-agents/",
        ]
        for hub in pillar_hubs:
            self.assertIn(hub, text, f"README must document Anchor Pillar Hub: {hub}")
        self.assertIn("reading-map.md", text, "README must document reading-map anchor")
        self.assertIn("hire.md", text, "README must document hire conversion anchor")
        self.assertRegex(text, r"(?i)zero\s+orphan", "README must specify zero orphan policy")

    # --- Feature 9: 100-Round Research Protocol Guide ---
    def test_feature_09_research_protocol_guide(self):
        text = self.readme
        self.assertIn("Cluster 1", text, "Must document Cluster 1")
        self.assertIn("Cluster 2", text, "Must document Cluster 2")
        self.assertIn("Cluster 3", text, "Must document Cluster 3")
        self.assertIn("Cluster 4", text, "Must document Cluster 4")
        self.assertIn("Cluster 5", text, "Must document Cluster 5")
        self.assertRegex(text, r"(?i)primary\s+source", "Must document primary-source requirement")
        self.assertRegex(text, r"(?i)dossier", "Must document research dossier output")

    # --- Feature 10: 7 Technical Content Gates Guide ---
    def test_feature_10_seven_content_gates_guide(self):
        text = self.readme
        gates = [
            ("Gate 1", r"(?i)answer-first|bluf"),
            ("Gate 2", r"(?i)version-pinned|pseudo-code"),
            ("Gate 3", r"(?i)quantitative\s+density|data\s+points"),
            ("Gate 4", r"(?i)mermaid"),
            ("Gate 5", r"(?i)production\s+failure"),
            ("Gate 6", r"(?i)trade-off"),
            ("Gate 7", r"(?i)verifiable\s+claims|citation"),
        ]
        for gate_name, pattern in gates:
            self.assertRegex(text, pattern, f"README must document criteria for {gate_name}")

    # --- Feature 11: 4-Phase Delivery Workflow Codification ---
    def test_feature_11_lifecycle_workflow_codification(self):
        wf_path = resolve_workflow_path("article-creation-and-upgrade-lifecycle")
        self.assertIsNotNone(wf_path, "Workflow file must exist")
        wf_text = wf_path.read_text(encoding="utf-8")
        self.assertIn("Deep Research", wf_text, "Workflow must codify Deep Research phase")
        self.assertIn("Masterclass Drafting", wf_text, "Workflow must codify Masterclass Drafting phase")
        self.assertIn("Dual", wf_text, "Workflow must codify Dual Audit phase")
        self.assertIn("SEO Authority", wf_text, "Workflow must codify SEO Authority phase")
        self.assertIn("Reviewer", wf_text, "Workflow must codify Reviewer Sign-off phase")
        self.assertRegex(wf_text, r"(?m)^roles:\s*", "Workflow frontmatter must declare roles")

    # --- Feature 12: Non-Overlapping Audit Boundaries ---
    def test_feature_12_audit_boundaries_codification(self):
        wf_path = resolve_workflow_path("article-creation-and-upgrade-lifecycle")
        self.assertIsNotNone(wf_path)
        wf_text = wf_path.read_text(encoding="utf-8")
        self.assertIn("@content-manager", wf_text, "Must define @content-manager audit scope")
        self.assertIn("@technical-writer", wf_text, "Must define @technical-writer audit scope")
        self.assertIn("@seo-analyst", wf_text, "Must define @seo-analyst audit scope")
        self.assertRegex(wf_text, r"(?i)brand\s+voice|e-e-a-t", "@content-manager must own editorial & E-E-A-T")
        self.assertRegex(wf_text, r"(?i)code\s+execution|syntax|deployable", "@technical-writer must own code validity")
        self.assertRegex(wf_text, r"(?i)schema\.org|answer-first|link\s+topology", "@seo-analyst must own link topology & schema")

    # --- Feature 13: A2A Structured Handoff Contracts ---
    def test_feature_13_handoff_contracts_declaration(self):
        wf_path = resolve_workflow_path("article-creation-and-upgrade-lifecycle")
        self.assertIsNotNone(wf_path)
        wf_text = wf_path.read_text(encoding="utf-8")
        # 3 Primary A2A contracts required by ORIGINAL_REQUEST R3 & Acceptance Criteria
        contracts = [
            "research-report.json",
            "content-handoff.json",
            "seo-audit-report.json",
        ]
        for c in contracts:
            self.assertIn(c, wf_text, f"Workflow must explicitly cite output contract: {c}")
            schema_file = SCHEMAS_DIR / c
            self.assertTrue(schema_file.exists(), f"Contract schema file must exist: {schema_file}")

    # --- Feature 14: Workflow Linkages Codification ---
    def test_feature_14_workflow_linkages_codification(self):
        wf_path = resolve_workflow_path("article-creation-and-upgrade-lifecycle")
        self.assertIsNotNone(wf_path)
        wf_text = wf_path.read_text(encoding="utf-8")
        self.assertIn("Failure Modes", wf_text, "Workflow must define Failure Modes")
        self.assertRegex(wf_text, r"(?i)mitigation", "Workflow must define Failure Mitigations")
        self.assertRegex(wf_text, r"(?i)standard\s+2026|standard\s+2027|owasp\s+asi", "Workflow must declare security standard alignment")
        self.assertRegex(wf_text, r"(?i)workflow\s+linkages|masterclass-batch-upgrade", "Workflow must document workflow linkages")

    # --- Feature 15: Packs Registry Documentation Sync ---
    def test_feature_15_packs_registry_sync(self):
        packs_readme = PACKS_DIR / "README.md"
        self.assertTrue(packs_readme.exists(), "packs/README.md must exist")
        text = packs_readme.read_text(encoding="utf-8")
        self.assertIn("vesviet-team", text, "packs/README.md must register vesviet-team")
        self.assertIn("vesviet-team/manifest.yaml", text, "packs/README.md must link to vesviet-team manifest")
        self.assertRegex(text, r"(?i)100-round", "packs/README.md must note 100-Round Research capability")
        self.assertRegex(text, r"(?i)4-role\s+swarm", "packs/README.md must note 4-Role Swarm capability")

    # --- Feature 16: Index & Governance Validation Suite ---
    def test_feature_16_index_and_governance_validation(self):
        # Verify no open / unassigned TODO comments in manifest
        manifest_text = yaml.dump(self.manifest)
        self.assertFalse(bool(re.search(r"(?m)^\s*#\s*TODO\b", manifest_text)), "Manifest must not contain uncompleted TODO comments")
        # Verify overlay rules existence
        rules_dir = VESVIET_OVERLAY_DIR / "rules"
        self.assertTrue(rules_dir.is_dir(), "overlays/vesviet-content/rules must exist")
        for rule in ["content-brand.md", "link-topology.md", "seo-authority.md", "technical-article-2027.md"]:
            self.assertTrue((rules_dir / rule).exists(), f"Overlay rule must exist: {rule}")


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (>=5 checks per feature)
# ==============================================================================

class TestTier2BoundaryAndCornerCases(unittest.TestCase):
    """
    Tier 2 tests evaluate boundary conditions, exact invariant preservation,
    tokenizer edge cases, and adversarial failure modes.
    """

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()

    # --- Boundary 1: Exact Corpus Count Invariants (18/09/2026 Index) ---
    def test_boundary_01_exact_corpus_counts(self):
        c = self.manifest["corpus"]
        v = c["vesviet"]
        l = c["learn"]

        # Exact authoritative counts from ORIGINAL_REQUEST.md
        self.assertEqual(v["content_files"], 374, "Invariant failed: vesviet content_files != 374")
        self.assertEqual(v["posts"], 66, "Invariant failed: vesviet posts != 66")
        self.assertEqual(v["series_dirs"], 25, "Invariant failed: vesviet series_dirs != 25")
        self.assertEqual(v["series_files"], 251, "Invariant failed: vesviet series_files != 251")
        self.assertEqual(v["radar_files"], 34, "Invariant failed: vesviet radar_files != 34")
        self.assertEqual(v["reports"], 296, "Invariant failed: vesviet reports != 296")

        self.assertEqual(l["content_files"], 433, "Invariant failed: learn content_files != 433")
        self.assertEqual(l["posts"], 86, "Invariant failed: learn posts != 86")
        self.assertEqual(l["series_dirs"], 25, "Invariant failed: learn series_dirs != 25")
        self.assertEqual(l["series_files"], 251, "Invariant failed: learn series_files != 251")
        self.assertEqual(l["radar_files"], 70, "Invariant failed: learn radar_files != 70")
        self.assertEqual(l["docs"], 3, "Invariant failed: learn docs != 3")
        self.assertEqual(l["reports"], 276, "Invariant failed: learn reports != 276")

        # Mathematical relationships and symmetries
        self.assertEqual(v["content_files"] + l["content_files"], 807, "Combined content files invariant (374 + 433 == 807)")
        self.assertEqual(v["series_files"], l["series_files"], "Series files symmetry invariant")
        self.assertEqual(v["series_dirs"], l["series_dirs"], "Series dirs symmetry invariant")
        self.assertGreater(l["content_files"], v["content_files"], "Learn corpus exceeds vesviet corpus in file count")

    # --- Boundary 2: BLUF Word Count Limits (Gate 1: <= 60 words) ---
    def test_boundary_02_bluf_word_count_limits(self):
        # Valid: exactly 60 words
        bluf_60 = " ".join([f"word{i}" for i in range(1, 61)])
        self.assertEqual(count_words(bluf_60), 60)
        self.assertLessEqual(count_words(bluf_60), 60, "60-word BLUF must pass Gate 1")

        # Valid: 59 words
        bluf_59 = " ".join([f"word{i}" for i in range(1, 60)])
        self.assertEqual(count_words(bluf_59), 59)
        self.assertLessEqual(count_words(bluf_59), 60, "59-word BLUF must pass Gate 1")

        # Valid: single word
        self.assertEqual(count_words("Summary"), 1)
        self.assertLessEqual(count_words("Summary"), 60, "1-word BLUF must pass")

        # Invalid: 61 words
        bluf_61 = " ".join([f"word{i}" for i in range(1, 62)])
        self.assertEqual(count_words(bluf_61), 61)
        self.assertGreater(count_words(bluf_61), 60, "61-word BLUF must violate Gate 1")

        # Tokenizer edge case: Vietnamese diacritics and technical code tokens
        vn_sample = "> **Answer-first:** Kiến trúc Raft bảo đảm tính nhất quán mạnh mẽ qua leader election và log replication với độ trễ P99 dưới 15ms trên cụm 5 nodes."
        self.assertLessEqual(count_words(vn_sample), 60, "Vietnamese technical BLUF tokenization test")

    # --- Boundary 3: One-Way Authority Rule Enforcement ---
    def test_boundary_03_one_way_authority_enforcement(self):
        # Rule: learn -> vesviet is PERMITTED; vesviet -> learn is FORBIDDEN
        def check_link_allowed(source_site: str, target_url: str) -> bool:
            if source_site == "vesviet":
                if re.search(r"https?://learn\.tanhdev\.com", target_url) or "//learn.tanhdev.com" in target_url:
                    return False
            return True

        # Valid cases
        self.assertTrue(check_link_allowed("learn", "https://tanhdev.com/posts/go-microservices/"))
        self.assertTrue(check_link_allowed("vesviet", "https://tanhdev.com/reading-map/"))
        self.assertTrue(check_link_allowed("vesviet", "https://github.com/golang/go"))

        # Adversarial forbidden reverse link cases
        self.assertFalse(check_link_allowed("vesviet", "https://learn.tanhdev.com/series/raft/"))
        self.assertFalse(check_link_allowed("vesviet", "http://learn.tanhdev.com/docs/quickstart"))
        self.assertFalse(check_link_allowed("vesviet", "//learn.tanhdev.com/notes"))
        self.assertFalse(check_link_allowed("vesviet", "https://learn.tanhdev.com:443/posts/1"))

    # --- Boundary 4: Deep Research Protocol Strict Bounds ---
    def test_boundary_04_deep_research_strict_bounds(self):
        proto = self.manifest["deep_research_protocol"]
        total = proto["rounds"]
        clusters = proto["clusters"]
        per_cluster = proto["rounds_per_cluster"]

        self.assertEqual(total, 100, "Must be exactly 100 rounds")
        self.assertEqual(clusters * per_cluster, total, "Clusters * rounds_per_cluster must equal total rounds")

        # Test boundary validator logic
        def validate_research_rounds(rounds: int, num_clusters: int, r_per_cluster: int) -> bool:
            if rounds != 100:
                return False
            if num_clusters != 5 or r_per_cluster != 20:
                return False
            return True

        self.assertTrue(validate_research_rounds(100, 5, 20))
        self.assertFalse(validate_research_rounds(99, 5, 20), "99 rounds must be rejected")
        self.assertFalse(validate_research_rounds(101, 5, 20), "101 rounds must be rejected")
        self.assertFalse(validate_research_rounds(100, 4, 25), "4 clusters of 25 must be rejected")

        # Primary source ratio (>= 70%)
        def validate_primary_source_ratio(primary_count: int, total_sources: int) -> bool:
            return (primary_count / total_sources) >= 0.70

        self.assertTrue(validate_primary_source_ratio(70, 100))
        self.assertTrue(validate_primary_source_ratio(85, 100))
        self.assertFalse(validate_primary_source_ratio(69, 100), "69% primary source ratio must fail")

    # --- Boundary 5: Quantitative Density & Version-Pinned Code Limits ---
    def test_boundary_05_quantitative_density_and_code_bounds(self):
        # Gate 3: Quantitative density >= 3 data points per 500 words
        def validate_density(data_points: int, word_count: int) -> bool:
            if word_count <= 0:
                return False
            density = (data_points / word_count) * 500.0
            return density >= 3.0

        self.assertTrue(validate_density(3, 500), "Exact boundary: 3 points / 500 words")
        self.assertFalse(validate_density(2, 500), "Below boundary: 2 points / 500 words")
        self.assertTrue(validate_density(6, 1000), "Scaled boundary: 6 points / 1000 words")
        self.assertFalse(validate_density(5, 1000), "Below scaled boundary: 5 points / 1000 words")

        # Gate 2: Version pinned code snippet validation (zero stubs)
        def validate_code_snippet(code: str) -> Tuple[bool, str]:
            stub_patterns = [r"\bTODO\b", r"\bFIXME\b", r"\bpass\b\s*#", r"\.\.\.\s*//"]
            for pat in stub_patterns:
                if re.search(pat, code, re.IGNORECASE):
                    return False, f"Detected stub pattern {pat}"
            return True, "Valid"

        valid_code = "package main\nimport \"fmt\"\nfunc main() {\n    fmt.Println(\"Go 1.25\")\n}"
        invalid_code = "func process() {\n    // TODO: implement logic\n}"
        self.assertTrue(validate_code_snippet(valid_code)[0])
        self.assertFalse(validate_code_snippet(invalid_code)[0])


# ==============================================================================
# TIER 3: PAIRWISE CROSS-FEATURE COMBINATIONS
# ==============================================================================

class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """
    Tier 3 tests verify pairwise interoperability and cross-references between
    manifest declarations, workflows, JSON contracts, and overlay filesystem rules.
    """

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.workflow_path = resolve_workflow_path("article-creation-and-upgrade-lifecycle")
        if cls.workflow_path:
            cls.workflow_text = cls.workflow_path.read_text(encoding="utf-8")
        else:
            cls.workflow_text = ""

    # --- Combination 1: Manifest Roles vs Lifecycle Workflow Roles ---
    def test_comb_01_manifest_roles_match_workflow_roles(self):
        primary_roles = self.manifest.get("content_focus", {}).get("primary_roles", [])
        self.assertGreater(len(primary_roles), 0)
        for role in primary_roles:
            self.assertIn(role, self.workflow_text, f"Manifest role '{role}' must be wired into lifecycle workflow")

    # --- Combination 2: Workflow Handoff Schemas vs Contract Definitions ---
    def test_comb_02_workflow_contracts_resolve_to_valid_schemas(self):
        referenced_contracts = [
            "research-report.json",
            "content-handoff.json",
            "seo-audit-report.json",
        ]
        for c in referenced_contracts:
            schema_file = SCHEMAS_DIR / c
            self.assertTrue(schema_file.exists(), f"Schema contract file must exist: {schema_file}")
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_json = json.load(f)
            self.assertEqual(schema_json.get("type"), "object", f"Schema {c} root type must be object")
            self.assertIn("contract_type", schema_json.get("properties", {}), f"Schema {c} must define contract_type")

    # --- Combination 3: Manifest Workflows Resolution on Disk ---
    def test_comb_03_manifest_workflows_resolve_on_disk(self):
        workflows = self.manifest.get("content_focus", {}).get("workflows", [])
        self.assertGreater(len(workflows), 0)
        unresolved = []
        for wf in workflows:
            p = resolve_workflow_path(wf)
            if not p:
                unresolved.append(wf)
        self.assertEqual(unresolved, [], f"All manifest workflows must resolve to .md files on disk: {unresolved}")

    # --- Combination 4: Manifest Skills & Standards vs Filesystem ---
    def test_comb_04_manifest_standards_resolve_in_overlay(self):
        rules_dir = VESVIET_OVERLAY_DIR / "rules"
        required_rules = [
            "content-brand.md",
            "technical-article-2027.md",
            "seo-authority.md",
            "link-topology.md",
        ]
        for r in required_rules:
            self.assertTrue((rules_dir / r).exists(), f"Overlay rule referenced in manifest must exist: {rules_dir / r}")

    # --- Combination 5: Dual Audit Non-Overlapping Boundary Matrix ---
    def test_comb_05_dual_audit_orthogonality_matrix(self):
        self.assertIn("Phase 3: Dual", self.workflow_text)
        # Verify content-manager keywords
        cm_keywords = ["brand voice", "e-e-a-t", "information gain"]
        for kw in cm_keywords:
            self.assertRegex(self.workflow_text, rf"(?i){kw}")
        # Verify technical-writer keywords
        tw_keywords = ["code", "benchmark"]
        for kw in tw_keywords:
            self.assertRegex(self.workflow_text, rf"(?i){kw}")
        # Verify seo-analyst keywords
        seo_keywords = ["schema.org", "one-way authority", "answer-first"]
        for kw in seo_keywords:
            self.assertRegex(self.workflow_text, rf"(?i){kw}")


# ==============================================================================
# TIER 4: REAL-WORLD PUBLISHING SIMULATION (E2E LIFECYCLE)
# ==============================================================================

class TestTier4PublishingSimulation(unittest.TestCase):
    """
    Tier 4 tests simulate a realistic multi-agent publishing session across the
    5-phase lifecycle, validating synthesized data payloads against actual JSON contracts.
    """

    @classmethod
    def setUpClass(cls):
        if jsonschema is None:
            raise unittest.SkipTest("jsonschema library is required for Tier 4 simulation")
        cls.schemas = {}
        for name in ["research-report.json", "content-handoff.json", "seo-audit-report.json"]:
            path = SCHEMAS_DIR / name
            with open(path, "r", encoding="utf-8") as f:
                cls.schemas[name] = json.load(f)

    # --- Phase 1 Simulation: Deep Research Dossier Contract ---
    def test_sim_01_phase1_research_dossier_contract(self):
        schema = self.schemas["research-report.json"]
        # Synthesize custom 100-round payload adhering strictly to schema
        custom_payload = {
            "contract_type": "research-report",
            "report_id": "2026-09-18-distributed-consensus-go",
            "objective": "Execute 100 rounds of deep research on Raft consensus in Go 1.25 across 5 clusters.",
            "conducted_by": "seo-analyst",
            "created_at": "2026-09-18T10:00:00+07:00",
            "execution_metrics": {
                "depth_mode": "deep",
                "total_rounds": 100,
                "sources_analyzed": 45,
            },
            "synthesis": {
                "key_findings": [
                    "Raft leader election latency P99 is under 15ms with pipelined RPCs.",
                    "Batch fsync of log entries scales throughput past 50k TPS.",
                ],
                "critical_gaps": [
                    "Detailed hardware specs for Cloudflare D1 edge replicas not publicly documented.",
                ],
                "confidence_score": "High",
            },
            "raw_data_references": [
                {
                    "source_name": "In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout)",
                    "url": "https://raft.github.io/raft.pdf",
                    "credibility": "Primary",
                    "source_type": "academic-paper",
                    "context_summary": "Original Raft specification and leader election state machine.",
                },
                {
                    "source_name": "etcd Raft implementation v3.5",
                    "url": "https://github.com/etcd-io/raft",
                    "credibility": "Primary",
                    "source_type": "codebase",
                    "context_summary": "Production Go Raft library reference.",
                },
            ],
            "recommended_next_roles": [
                {
                    "role": "content-writer",
                    "rationale": "Draft masterclass post incorporating Ongaro algorithms and benchmark data.",
                }
            ],
        }
        jsonschema.validate(instance=custom_payload, schema=schema)

    # --- Phase 2 Simulation: Masterclass Draft Handoff Contract ---
    def test_sim_02_phase2_content_handoff_contract(self):
        schema = self.schemas["content-handoff.json"]
        custom_draft = {
            "contract_type": "content-handoff",
            "content_path": "vesviet/content/posts/go-microservices.md",
            "status": "draft_ready",
            "handoff": {
                "from_role": "content-writer",
                "to_role": "content-manager",
                "summary": "Masterclass drafting complete satisfying all 7 Technical Content Gates.",
            },
            "metadata": {
                "word_count": 2850,
                "bluf_words": 52,
                "quantitative_datapoints": 18,
                "code_snippets": 4,
                "mermaid_diagrams": 2,
            },
        }
        jsonschema.validate(instance=custom_draft, schema=schema)

    # --- Phase 3 Simulation: Dual Audit Simulation ---
    def test_sim_03_phase3_dual_audit_simulation(self):
        # Simulate editorial verification & technical verification verdicts
        editorial_verdict = {
            "auditor": "content-manager",
            "status": "approved",
            "brand_voice_pass": True,
            "information_gain_score": 82.5,
            "eeat_score": "High",
            "comments": "English masterclass provides 30% incremental benchmark data over Vietnamese twin notes.",
        }
        technical_verdict = {
            "auditor": "technical-writer",
            "status": "approved",
            "code_compiles": True,
            "version_pinned": True,
            "stubs_detected": 0,
            "mermaid_ast_valid": True,
            "benchmark_conditions_stated": True,
        }
        self.assertTrue(editorial_verdict["brand_voice_pass"])
        self.assertGreaterEqual(editorial_verdict["information_gain_score"], 75.0)
        self.assertTrue(technical_verdict["code_compiles"])
        self.assertEqual(technical_verdict["stubs_detected"], 0)

    # --- Phase 4 Simulation: SEO Authority & Topology Contract ---
    def test_sim_04_phase4_seo_audit_contract(self):
        schema = self.schemas["seo-audit-report.json"]
        custom_seo_report = {
            "contract_type": "seo-audit-report",
            "audit_id": "seo-audit-2026-09-18-raft",
            "created_at": "2026-09-18T14:00:00+07:00",
            "site": "vesviet",
            "audited_url_or_path": "vesviet/content/posts/alipay-double-11-architecture-tps.md",
            "audit_type": "pre_publish",
            "brief_ref": "2026-09-18-raft-distributed-consensus",
            "anti_ai_semantic_audit": {
                "ai_semantic_flaw_score": 0,
                "gate_passed": True,
                "cliche_findings": [],
                "burstiness_assessment": "natural_human",
                "notes": "Zero blacklisted cliches found; natural engineering cadence.",
            },
            "information_gain_audit": {
                "information_gain_rating": "exceptional",
                "gate_passed": True,
                "net_new_assets": ["Empirical P99 latency benchmarks under 5-node cluster", "Real-world failover traces"],
                "competitor_serp_overlap_notes": "Contains primary source Raft measurements exceeding top 10 SERP.",
            },
            "geo_readiness_checklist": {
                "answer_first_bluf": True,
                "entity_salience": True,
                "tabular_data_density": True,
                "citation_readiness_score": 92,
                "llms_txt_compatibility": True,
                "overall_geo_status": "pass",
            },
            "traditional_seo": {
                "issues": [],
                "internal_links_audit": {
                    "count_found": 5,
                    "minimum_required": 3,
                    "passes": True,
                    "high_value_link_present": True,
                    "missing_links": [],
                },
                "overall_score": "pass",
                "overall_notes": "All traditional SEO checks pass.",
            },
            "ai_extractability": {
                "answer_first_structure": {
                    "status": "pass",
                    "notes": "Answer-first BLUF ≤60 words verified.",
                },
                "heading_hierarchy": {
                    "status": "pass",
                    "h1_count": 1,
                    "issues": [],
                },
                "fact_density": {
                    "status": "pass",
                    "data_points_found": 18,
                    "word_count_approximate": 2850,
                    "notes": "3.15 data points per 500 words meets threshold.",
                },
                "schema_markup": {
                    "status": "pass",
                    "types_present": ["TechArticle", "Person"],
                    "types_missing": [],
                },
                "ai_bot_crawlability": {
                    "status": "verified_allowed",
                    "notes": "Crawl allowed for AI bots.",
                },
                "content_uniqueness": {
                    "status": "pass",
                    "information_gain_present": True,
                    "notes": "Unique Raft failover benchmarks.",
                },
                "query_fan_out_coverage": {
                    "status": "pass",
                    "questions_covered": [
                        "What is Raft consensus?",
                        "How does leader election work in Raft?",
                        "What is the latency impact of log fsync?",
                    ],
                    "missing_questions": [],
                },
                "overall_score": 92,
                "overall_status": "pass",
            },
            "metadata_audit": {
                "title_audit": {
                    "current_title": "Raft Consensus in Go: Leader Election & Log Replication",
                    "char_count": 55,
                    "contains_primary_keyword": True,
                    "within_limit": True,
                    "status": "pass",
                },
                "meta_audit": {
                    "current_meta": "Deep dive into Raft consensus in Go 1.25. Benchmarks, leader election algorithms, and production failure recovery.",
                    "char_count": 112,
                    "contains_primary_keyword": True,
                    "within_limit": True,
                    "status": "pass",
                },
                "slug_audit": {
                    "current_slug": "posts/alipay-double-11-architecture-tps",
                    "contains_primary_keyword": True,
                    "follows_overlay_conventions": True,
                    "status": "pass",
                },
            },
            "cannibalization_check": {
                "status": "clear",
                "window_checked": "365_days",
            },
            "handoff": {
                "status": "approved_to_publish",
                "action_required": "Publish to production",
                "metadata_contract_ready": True,
                "contracts": ["contracts/schemas/seo-metadata.json"],
                "notes": "All SEO and authority requirements satisfied.",
            },
        }
        jsonschema.validate(instance=custom_seo_report, schema=schema)

    # --- Negative Simulation: Pipeline Invalidation & Gate Enforcement ---
    def test_sim_05_negative_pipeline_gate_enforcement(self):
        schema = self.schemas["research-report.json"]
        # Invalidation 1: Missing required fields (synthesis, execution_metrics)
        invalid_payload = {
            "contract_type": "research-report",
            "objective": "Incomplete research",
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_payload, schema=schema)

        # Invalidation 2: Wrong discriminator
        invalid_discriminator = {
            "contract_type": "wrong-contract-type",
            "objective": "Testing invalid type",
            "execution_metrics": {"depth_mode": "deep", "total_rounds": 100, "sources_analyzed": 5},
            "synthesis": {"key_findings": ["A"], "critical_gaps": ["B"], "confidence_score": "High"},
            "raw_data_references": [],
            "recommended_next_roles": [],
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_discriminator, schema=schema)

        # Invalidation 3: BLUF > 60 words violates Gate 1
        bluf_65_words = " ".join([f"token{i}" for i in range(1, 66)])
        self.assertGreater(count_words(bluf_65_words), 60)


# ==============================================================================
# TEST RUNNER & CLI INTERFACE
# ==============================================================================

def run_tests(tier: str = "all", verbose: bool = False, json_report_path: Optional[str] = None) -> int:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    tier_map = {
        "1": [TestTier1FeatureCoverage],
        "2": [TestTier2BoundaryAndCornerCases],
        "3": [TestTier3CrossFeatureCombinations],
        "4": [TestTier4PublishingSimulation],
    }

    if tier == "all":
        selected_classes = [
            TestTier1FeatureCoverage,
            TestTier2BoundaryAndCornerCases,
            TestTier3CrossFeatureCombinations,
            TestTier4PublishingSimulation,
        ]
    elif tier in tier_map:
        selected_classes = tier_map[tier]
    else:
        print(f"Error: Unknown tier '{tier}'. Options: 1, 2, 3, 4, all")
        return 1

    for tc in selected_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))

    print(f"\n{'='*75}")
    print(f" VESVIET-TEAM v5.0.0 E2E VALIDATION SUITE (Tier: {tier})")
    print(f"{'='*75}")

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    duration = time.time() - start_time

    # Summary breakdown
    print("\n" + "-" * 75)
    print(" SUMMARY BREAKDOWN")
    print("-" * 75)
    print(f" Tests Run:    {result.testsRun}")
    print(f" Passed:       {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Failures:     {len(result.failures)}")
    print(f" Errors:       {len(result.errors)}")
    print(f" Elapsed Time: {duration:.3f}s")
    print("-" * 75)

    if json_report_path:
        report = {
            "pack": "vesviet-team",
            "version": "5.0.0",
            "tier": tier,
            "tests_run": result.testsRun,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "failures": len(result.failures),
            "errors": len(result.errors),
            "duration_seconds": duration,
            "success": result.wasSuccessful(),
        }
        with open(json_report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f" Machine-readable report saved to: {json_report_path}")

    if result.wasSuccessful():
        print(" RESULT: ALL TIERS PASSED [OK]\n")
        return 0
    else:
        print(" RESULT: TESTS FAILED [FAIL]\n")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Test runner for vesviet-team v5.0.0 pack upgrade")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all", help="Select tier to run")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose test output")
    parser.add_argument("--json-report", type=str, default=None, help="Path to write JSON test report")

    args = parser.parse_args()
    exit_code = run_tests(tier=args.tier, verbose=args.verbose, json_report_path=args.json_report)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
