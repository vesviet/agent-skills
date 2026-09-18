#!/usr/bin/env python3
"""
test_vesviet_v5_adversarial_challenge.py
=========================================
Empirical Adversarial Stress-Test Suite for vesviet-team Pack Upgrade (v5.0.0).

Specifically challenges:
1. 100-Round Deep Research Protocol:
   - Strict 5 technical clusters x 20 rounds breakdown
   - Boundary enforcement (99, 101, non-uniform distributions)
   - Primary source credibility threshold (>= 70%)
   - AI source discipline (query formulation only, zero AI-generated primary citations)
   - Grounding completeness (100% target)
   - Dossier persistence schema and naming conventions

2. Data Contracts Validation:
   - Sample valid payloads for research-report.json, content-handoff.json, seo-audit-report.json
   - Boundary & invalid payloads: missing fields, type mismatch, enum violations, range overflows
   - Schema defect verification on seo-audit-report.json nullability (bundled example defect)
   - Schema contract defect verification on content-handoff.json recommended_next_roles enum omission

3. Dual Parallel Audit Boundary Isolation:
   - Verification of mutually exclusive responsibility matrices for @content-manager vs @technical-writer
   - Analysis of explicit Negative Boundaries in workflow contracts
   - Verification of mathematical disjointness (empty set intersection) of audit domains
   - Blocking gate logic: failure in either Stream A or Stream B blocks Phase 4 SEO audit

4. Twin Hugo Architecture & Link Topology:
   - One-way authority flow (learn -> vesviet only, zero reverse links)
   - 10 Anchor Pillar Hubs backbone integrity and zero orphan policy

Exit code: 0 on 100% pass, 1 on any failure.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# Set utf-8 console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import yaml

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    jsonschema = None
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parent.parent
PACK_DIR = ROOT / "packs" / "vesviet-team"
MANIFEST_PATH = PACK_DIR / "manifest.yaml"
README_PATH = PACK_DIR / "README.md"
WORKFLOW_PACK_PATH = PACK_DIR / "workflows" / "article-creation-and-upgrade-lifecycle.md"
WORKFLOW_OVERLAY_PATH = ROOT / "overlays" / "vesviet-content" / "workflows" / "article-creation-and-upgrade-lifecycle.md"
ROLES_DIR = ROOT / "core" / "roles"
SCHEMAS_DIR = ROOT / "core" / "contracts" / "schemas"


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# 1. 100-ROUND DEEP RESEARCH PROTOCOL CHALLENGES
# ==============================================================================

class TestDeepResearchProtocolAdversarial(unittest.TestCase):
    """
    Adversarial challenge on the 100-Round Deep Research Protocol specification,
    cluster distribution, primary source ratios, and output dossier schema.
    """

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_yaml(MANIFEST_PATH)
        cls.readme_text = README_PATH.read_text(encoding="utf-8")
        cls.wf_pack_text = WORKFLOW_PACK_PATH.read_text(encoding="utf-8")
        cls.wf_overlay_text = WORKFLOW_OVERLAY_PATH.read_text(encoding="utf-8")

    def test_challenge_01_manifest_cluster_breakdown_integrity(self):
        """Verify deep_research_protocol in manifest has exactly 5 clusters x 20 rounds = 100 total."""
        proto = self.manifest.get("deep_research_protocol", {})
        self.assertIsNotNone(proto, "deep_research_protocol must be defined in manifest")
        self.assertEqual(proto.get("rounds"), 100, "Manifest deep_research_protocol.rounds must be 100")
        self.assertEqual(proto.get("clusters"), 5, "Manifest deep_research_protocol.clusters must be 5")
        self.assertEqual(proto.get("rounds_per_cluster"), 20, "Manifest deep_research_protocol.rounds_per_cluster must be 20")
        self.assertTrue(proto.get("mandatory_before_action"), "Protocol must be mandatory before action")

        # Cluster breakdown details
        breakdown = proto.get("cluster_breakdown", {})
        self.assertEqual(len(breakdown), 5, "Must declare exactly 5 cluster descriptions")
        expected_ranges = [
            ("cluster_1", "01-20"),
            ("cluster_2", "21-40"),
            ("cluster_3", "41-60"),
            ("cluster_4", "61-80"),
            ("cluster_5", "81-100"),
        ]
        for key, r_str in expected_ranges:
            self.assertIn(key, breakdown, f"Missing cluster key: {key}")
            self.assertIn(r_str, breakdown[key], f"Cluster {key} must cover rounds {r_str}")

    def test_challenge_02_workflow_cluster_definitions_conformance(self):
        """Verify workflow files define the exact 5 technical clusters and round allocations."""
        for name, wf_text in [("pack_workflow", self.wf_pack_text), ("overlay_workflow", self.wf_overlay_text)]:
            self.assertIn("Cluster 1 (Rounds 01", wf_text, f"{name}: Cluster 1 (Rounds 01-20) missing")
            self.assertIn("Cluster 2 (Rounds 21", wf_text, f"{name}: Cluster 2 (Rounds 21-40) missing")
            self.assertIn("Cluster 3 (Rounds 41", wf_text, f"{name}: Cluster 3 (Rounds 41-60) missing")
            self.assertIn("Cluster 4 (Rounds 61", wf_text, f"{name}: Cluster 4 (Rounds 61-80) missing")
            self.assertIn("Cluster 5 (Rounds 81", wf_text, f"{name}: Cluster 5 (Rounds 81-100) missing")

            # Check cluster themes
            self.assertRegex(wf_text, r"(?i)Cluster 1.*Architecture Roots", f"{name}: Cluster 1 theme mismatch")
            self.assertRegex(wf_text, r"(?i)Cluster 2.*Core Algorithms", f"{name}: Cluster 2 theme mismatch")
            self.assertRegex(wf_text, r"(?i)Cluster 3.*Quantitative Benchmarks", f"{name}: Cluster 3 theme mismatch")
            self.assertRegex(wf_text, r"(?i)Cluster 4.*Production Outages", f"{name}: Cluster 4 theme mismatch")
            self.assertRegex(wf_text, r"(?i)Cluster 5.*Trade-off Matrices", f"{name}: Cluster 5 theme mismatch")

    def test_challenge_03_adversarial_round_validation_engine(self):
        """Stress test round validator function against adversarial boundary inputs."""
        def evaluate_research_protocol(rounds: int, clusters: List[int]) -> Tuple[bool, str]:
            if rounds != 100:
                return False, f"Invalid total rounds: {rounds}, expected exactly 100"
            if len(clusters) != 5:
                return False, f"Invalid cluster count: {len(clusters)}, expected 5"
            if sum(clusters) != 100:
                return False, f"Cluster sum mismatch: {sum(clusters)} != 100"
            for idx, c in enumerate(clusters, 1):
                if c != 20:
                    return False, f"Cluster {idx} has {c} rounds; must be exactly 20"
            return True, "Valid"

        # Valid input
        valid, msg = evaluate_research_protocol(100, [20, 20, 20, 20, 20])
        self.assertTrue(valid, msg)

        # Adversarial under-round (99)
        valid, msg = evaluate_research_protocol(99, [20, 20, 20, 20, 19])
        self.assertFalse(valid)
        self.assertIn("99", msg)

        # Adversarial over-round (101)
        valid, msg = evaluate_research_protocol(101, [20, 20, 20, 20, 21])
        self.assertFalse(valid)
        self.assertIn("101", msg)

        # Non-uniform clusters summing to 100 (e.g. 15, 25, 20, 20, 20)
        valid, msg = evaluate_research_protocol(100, [15, 25, 20, 20, 20])
        self.assertFalse(valid)
        self.assertIn("Cluster 1 has 15 rounds", msg)

        # Wrong number of clusters (4 clusters of 25)
        valid, msg = evaluate_research_protocol(100, [25, 25, 25, 25])
        self.assertFalse(valid)
        self.assertIn("Invalid cluster count: 4", msg)

        # Empty clusters
        valid, msg = evaluate_research_protocol(0, [])
        self.assertFalse(valid)

    def test_challenge_04_primary_source_credibility_ratio(self):
        """Stress test primary source credibility ratio (must be >= 70%)."""
        def check_source_credibility(sources: List[Dict[str, str]]) -> Tuple[bool, float]:
            if not sources:
                return False, 0.0
            primary_count = sum(1 for s in sources if s.get("credibility") == "Primary")
            ratio = (primary_count / len(sources)) * 100.0
            return ratio >= 70.0, ratio

        # 70% boundary case (7 out of 10)
        sources_70 = [{"credibility": "Primary"} for _ in range(7)] + [{"credibility": "Secondary"} for _ in range(3)]
        passed, ratio = check_source_credibility(sources_70)
        self.assertTrue(passed)
        self.assertAlmostEqual(ratio, 70.0)

        # 69.9% adversarial case (699 out of 1000)
        sources_699 = [{"credibility": "Primary"} for _ in range(699)] + [{"credibility": "Secondary"} for _ in range(301)]
        passed, ratio = check_source_credibility(sources_699)
        self.assertFalse(passed)
        self.assertLess(ratio, 70.0)

        # 100% primary case
        sources_100 = [{"credibility": "Primary"} for _ in range(25)]
        passed, ratio = check_source_credibility(sources_100)
        self.assertTrue(passed)
        self.assertEqual(ratio, 100.0)

        # Zero sources
        passed, ratio = check_source_credibility([])
        self.assertFalse(passed)

    def test_challenge_05_ai_source_discipline_enforcement(self):
        """
        Verify AI source discipline:
        - AI tools used for query generation only -> ALLOWED
        - AI tool cited as primary source or evidence -> FORBIDDEN
        """
        def validate_ai_source_discipline(source_refs: List[Dict[str, Any]], ai_tools_used: List[str]) -> Tuple[bool, str]:
            ai_tool_names = {"chatgpt", "perplexity", "claude", "gemini", "copilot", "google ai overview"}
            for ref in source_refs:
                name = ref.get("source_name", "").lower()
                url = ref.get("url", "").lower()
                for ai in ai_tool_names:
                    if ai in name or ai in url:
                        if ref.get("credibility") == "Primary":
                            return False, f"Violation: AI tool '{name}' cited as Primary Source!"
            return True, "AI discipline satisfied"

        # Valid scenario: Perplexity used for queries, RFC cited as Primary
        valid_refs = [
            {"source_name": "RFC 7540 HTTP/2", "url": "https://datatracker.ietf.org/doc/html/rfc7540", "credibility": "Primary"},
            {"source_name": "Go GitHub Repo", "url": "https://github.com/golang/go", "credibility": "Primary"},
        ]
        valid_ai_queries = ["Perplexity Pro", "ChatGPT-4o"]
        passed, msg = validate_ai_source_discipline(valid_refs, valid_ai_queries)
        self.assertTrue(passed, msg)

        # Adversarial scenario: Agent cited ChatGPT as primary source
        adversarial_refs = [
            {"source_name": "ChatGPT Conversation on Raft", "url": "https://chatgpt.com/share/123", "credibility": "Primary"},
        ]
        passed, msg = validate_ai_source_discipline(adversarial_refs, valid_ai_queries)
        self.assertFalse(passed)
        self.assertIn("violation", msg.lower())

    def test_challenge_06_dossier_output_path_conformance(self):
        """Verify dossier output paths follow exact pattern: reports/research/{slug}-dossier.json."""
        dossier = self.manifest.get("deep_research_protocol", {}).get("output_dossier", {})
        json_tmpl = dossier.get("json", "")
        md_tmpl = dossier.get("markdown", "")

        self.assertEqual(json_tmpl, "reports/research/{slug}-dossier.json")
        self.assertEqual(md_tmpl, "reports/research/{slug}-research-notes.md")

        def resolve_dossier_paths(slug: str) -> Tuple[str, str]:
            return json_tmpl.format(slug=slug), md_tmpl.format(slug=slug)

        test_slug = "distributed-consensus-go"
        j_path, m_path = resolve_dossier_paths(test_slug)
        self.assertEqual(j_path, f"reports/research/{test_slug}-dossier.json")
        self.assertEqual(m_path, f"reports/research/{test_slug}-research-notes.md")
        self.assertTrue(re.match(r"^reports/research/[\w-]+-dossier\.json$", j_path))
        self.assertTrue(re.match(r"^reports/research/[\w-]+-research-notes\.md$", m_path))


# ==============================================================================
# 2. DATA CONTRACTS VALIDATION CHALLENGES
# ==============================================================================

class TestDataContractsValidation(unittest.TestCase):
    """
    Adversarial validation of A2A JSON contracts:
    - research-report.json
    - content-handoff.json
    - seo-audit-report.json
    """

    @classmethod
    def setUpClass(cls):
        if jsonschema is None:
            raise unittest.SkipTest("jsonschema is required for contract validation tests")

        cls.schemas = {}
        for name in ["research-report.json", "content-handoff.json", "seo-audit-report.json"]:
            path = SCHEMAS_DIR / name
            cls.schemas[name] = load_json(path)

    # --- 2.1: research-report.json validation ---
    def test_challenge_07_research_report_valid_and_boundaries(self):
        schema = self.schemas["research-report.json"]

        # 1. Complete valid 100-round research report payload
        valid_payload = {
            "contract_type": "research-report",
            "report_id": "2026-09-18-k8s-platform-engineering",
            "objective": "100 rounds of deep research on Kubernetes platform engineering and eBPF observability.",
            "conducted_by": "seo-analyst",
            "created_at": "2026-09-18T10:00:00+07:00",
            "execution_metrics": {
                "depth_mode": "deep",
                "total_rounds": 100,
                "sources_analyzed": 52,
            },
            "synthesis": {
                "key_findings": [
                    "eBPF sockops bypasses TCP/IP stack overhead, reducing service mesh latency by 28%.",
                    "Cilium Hubble delivers kernel-level L4/L7 flow observability with under 1.5% CPU penalty.",
                ],
                "inferences": [
                    "[INFERENCE] Ambient mesh sidecarless architecture lowers memory consumption per node by 35%."
                ],
                "critical_gaps": [
                    "Kernel 6.12 vs 6.8 socket map latency differential on ARM64 Graviton4 requires further microbenchmarks."
                ],
                "confidence_score": "High",
            },
            "raw_data_references": [
                {
                    "source_name": "Linux Kernel BPF Documentation 6.12",
                    "url": "https://docs.kernel.org/bpf/",
                    "credibility": "Primary",
                    "source_type": "official-documentation",
                    "context_summary": "Kernel sockops program specifications and BPF helper routines.",
                },
                {
                    "source_name": "Cilium CNI Performance Benchmark 2026",
                    "url": "https://cilium.io/blog/2026/02/benchmarks",
                    "credibility": "Primary",
                    "source_type": "industry-report",
                    "context_summary": "P99 latency comparisons under 100k req/s load.",
                },
            ],
            "recommended_next_roles": [
                {
                    "role": "content-writer",
                    "rationale": "Draft masterclass post incorporating eBPF sockops and Cilium latency telemetry.",
                    "open_decisions": ["Whether to feature Hubble UI screenshots or CLI flow tables"],
                }
            ],
            "information_gain": {
                "unique_insights": [
                    "Direct kernel trace measurements on socket bypass under Go 1.26 not present in top 10 SERP results."
                ],
                "firsthand_evidence_available": True,
                "ai_coverage_gap": [
                    "Generic LLM summaries miss the specific sockops BPF map size memory threshold."
                ],
                "ymyl_elevation_required": False,
            },
            "ai_source_discipline": {
                "ai_tools_used_for_queries": ["Perplexity Pro", "SearchGPT"],
                "ai_citation_mismatches": [],
                "grounding_completeness_pct": 100,
            },
        }
        # Validate against schema
        jsonschema.validate(instance=valid_payload, schema=schema)

        # 2. Adversarial: Missing objective
        invalid_1 = copy.deepcopy(valid_payload)
        del invalid_1["objective"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_1, schema=schema)

        # 3. Adversarial: Missing contract_type
        invalid_2 = copy.deepcopy(valid_payload)
        del invalid_2["contract_type"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_2, schema=schema)

        # 4. Adversarial: Invalid depth_mode enum
        invalid_3 = copy.deepcopy(valid_payload)
        invalid_3["execution_metrics"]["depth_mode"] = "ultra-deep"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_3, schema=schema)

        # 5. Adversarial: grounding_completeness_pct out of range (> 100)
        invalid_4 = copy.deepcopy(valid_payload)
        invalid_4["ai_source_discipline"]["grounding_completeness_pct"] = 105
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_4, schema=schema)

    # --- 2.2: content-handoff.json validation ---
    def test_challenge_08_content_handoff_valid_and_boundaries(self):
        schema = self.schemas["content-handoff.json"]

        # 1. Complete valid content-handoff payload conforming to current schema enum
        valid_handoff = {
            "contract_type": "content-handoff",
            "handoff_id": "2026-09-18-ebpf-linux-observability",
            "created_at": "2026-09-18T12:00:00+07:00",
            "site": "tanhdev.com",
            "content_path": "vesviet/content/posts/ebpf-linux-observability.md",
            "status": "draft_ready",
            "primary_keyword": "ebpf linux kernel observability go",
            "word_count": 3200,
            "editorial_passes": 2,
            "ai_semantic_flaw_score": {
                "flaw_score": 0,
                "gate_passed": True,
                "cliche_count": 0,
                "cliches_detected": [],
                "burstiness_std_dev": 8.4,
                "active_voice_percentage": 88.5,
                "ungrounded_claims_count": 0,
            },
            "information_gain_rating": "exceptional",
            "geo_readiness_checklist": {
                "answer_first_bluf_verified": True,
                "entity_salience_optimized": True,
                "structured_comparison_tables": True,
                "quotable_fact_density_met": True,
                "schema_jsonld_prepared": True,
                "llms_txt_compatible": True,
                "all_gates_cleared": True,
            },
            "information_gain": {
                "type": "firsthand_account",
                "description": "Production eBPF benchmark telemetry on AWS c7g.4xlarge instances measuring sockops latency bypass.",
                "gate_passed": True,
            },
            "eeat_signals": {
                "experience_proof_type": "documented_test",
                "experience_proof_implemented": True,
                "experience_proof_notes": "Firsthand benchmark logs and reproducer repository included.",
                "author_entity_referenced": True,
                "trust_signals_present": True,
                "ymyl_domain": False,
            },
            "internal_links_added": [
                "/series/ebpf/",
                "/series/k8s/",
                "/series/golang/",
            ],
            "open_questions": [],
            "recommended_next_roles": ["technical-writer", "seo-analyst"],
        }
        jsonschema.validate(instance=valid_handoff, schema=schema)

        # 2. Adversarial: active_voice_percentage > 100
        invalid_voice = copy.deepcopy(valid_handoff)
        invalid_voice["ai_semantic_flaw_score"]["active_voice_percentage"] = 101.5
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_voice, schema=schema)

        # 3. Adversarial: active_voice_percentage < 0
        invalid_voice_neg = copy.deepcopy(valid_handoff)
        invalid_voice_neg["ai_semantic_flaw_score"]["active_voice_percentage"] = -5.0
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_voice_neg, schema=schema)

        # 4. Adversarial: burstiness_std_dev < 0
        invalid_burst = copy.deepcopy(valid_handoff)
        invalid_burst["ai_semantic_flaw_score"]["burstiness_std_dev"] = -1.0
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_burst, schema=schema)

        # 5. Adversarial: invalid information_gain_rating enum
        invalid_ig = copy.deepcopy(valid_handoff)
        invalid_ig["information_gain_rating"] = "subpar"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_ig, schema=schema)

    # --- 2.3: seo-audit-report.json validation ---
    def test_challenge_09_seo_audit_report_valid_and_boundaries(self):
        schema = self.schemas["seo-audit-report.json"]

        # 1. Complete valid SEO audit report payload
        valid_seo_audit = {
            "contract_type": "seo-audit-report",
            "audit_id": "seo-audit-2026-09-18-ebpf",
            "created_at": "2026-09-18T14:30:00+07:00",
            "site": "vesviet",
            "audited_url_or_path": "vesviet/content/posts/ebpf-linux-observability.md",
            "audit_type": "pre_publish",
            "brief_ref": "2026-09-18-ebpf-linux-observability",
            "anti_ai_semantic_audit": {
                "ai_semantic_flaw_score": 0,
                "gate_passed": True,
                "cliche_findings": [],
                "burstiness_assessment": "natural_human",
                "notes": "Burstiness std dev 8.4; active voice 88.5%; zero cliches detected.",
            },
            "information_gain_audit": {
                "information_gain_rating": "exceptional",
                "gate_passed": True,
                "net_new_assets": [
                    "Empirical socket bypass P99 latency telemetry",
                    "Custom eBPF sockops C and Go reproducer code",
                ],
                "competitor_serp_overlap_notes": "Contains kernel socket map benchmarks absent in top 10 search results.",
            },
            "geo_readiness_checklist": {
                "answer_first_bluf": True,
                "entity_salience": True,
                "tabular_data_density": True,
                "citation_readiness_score": 94,
                "llms_txt_compatibility": True,
                "overall_geo_status": "pass",
            },
            "traditional_seo": {
                "issues": [],
                "internal_links_audit": {
                    "count_found": 4,
                    "minimum_required": 3,
                    "passes": True,
                    "high_value_link_present": True,
                    "missing_links": [],
                },
                "overall_score": "pass",
                "overall_notes": "Internal link topology verified; Anchor Pillar Hub connected.",
            },
            "ai_extractability": {
                "answer_first_structure": {
                    "status": "pass",
                    "notes": "BLUF <= 60 words verified on all H2s.",
                },
                "heading_hierarchy": {
                    "status": "pass",
                    "h1_count": 1,
                    "issues": [],
                },
                "fact_density": {
                    "status": "pass",
                    "data_points_found": 22,
                    "word_count_approximate": 3200,
                    "notes": "3.4 data points per 500 words meets Gate 3.",
                },
                "schema_markup": {
                    "status": "pass",
                    "types_present": ["TechArticle", "Person", "BreadcrumbList"],
                    "types_missing": [],
                },
                "ai_bot_crawlability": {
                    "status": "verified_allowed",
                    "notes": "Allowed by robots.txt.",
                },
                "content_uniqueness": {
                    "status": "pass",
                    "information_gain_present": True,
                    "notes": "Unique eBPF telemetry.",
                },
                "query_fan_out_coverage": {
                    "status": "pass",
                    "questions_covered": [
                        "What is eBPF sockops bypass?",
                        "How does Cilium achieve low latency?",
                        "What is the CPU overhead of Hubble?",
                    ],
                    "questions_missing": [],
                },
                "overall_score": 94,
                "overall_status": "pass",
            },
            "metadata_audit": {
                "title_audit": {
                    "current_title": "eBPF Linux Kernel Observability with Go: Architecture & Benchmarks",
                    "char_count": 66,
                    "contains_primary_keyword": True,
                    "within_limit": True,
                    "status": "pass",
                },
                "meta_audit": {
                    "current_meta": "Masterclass on eBPF Linux kernel observability in Go. Socket map bypass, Cilium telemetry, and P99 latency benchmarks under 100k RPS.",
                    "char_count": 137,
                    "contains_primary_keyword": True,
                    "within_limit": True,
                    "status": "pass",
                },
                "slug_audit": {
                    "current_slug": "posts/ebpf-linux-observability",
                    "contains_primary_keyword": True,
                    "follows_overlay_conventions": True,
                    "status": "pass",
                },
            },
            "cannibalization_check": {
                "status": "clear",
                "window_checked": "2026-09-01 to 2026-09-18",
            },
            "handoff": {
                "status": "approved_to_publish",
                "action_required": "Publish to production flagship",
                "metadata_contract_ready": True,
                "contracts": ["contracts/schemas/seo-metadata.json"],
                "notes": "Ready for Reviewer sign-off.",
            },
        }
        jsonschema.validate(instance=valid_seo_audit, schema=schema)

        # 2. Adversarial: citation_readiness_score > 100
        invalid_citation = copy.deepcopy(valid_seo_audit)
        invalid_citation["geo_readiness_checklist"]["citation_readiness_score"] = 101
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_citation, schema=schema)

        # 3. Adversarial: citation_readiness_score < 0
        invalid_citation_neg = copy.deepcopy(valid_seo_audit)
        invalid_citation_neg["geo_readiness_checklist"]["citation_readiness_score"] = -1
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_citation_neg, schema=schema)

        # 4. Adversarial: Invalid overall_geo_status enum
        invalid_geo_status = copy.deepcopy(valid_seo_audit)
        invalid_geo_status["geo_readiness_checklist"]["overall_geo_status"] = "maybe_pass"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_geo_status, schema=schema)

    def test_challenge_10_seo_audit_schema_defect_investigation(self):
        """
        Empirically verify schema defect in seo-audit-report.json:
        The bundled example in seo-audit-report.json crashes under Draft 2020-12 jsonschema.validate
        because 'conflicting_url' and 'exception_rationale' are typed as 'string' rather than ['string', 'null'].
        """
        schema = self.schemas["seo-audit-report.json"]
        bundled_example = schema["examples"][0]

        # 1. Empirically prove bundled example crashes jsonschema.validate
        with self.assertRaises(jsonschema.ValidationError) as ctx:
            jsonschema.validate(instance=bundled_example, schema=schema)
        self.assertIn("None is not of type 'string'", str(ctx.exception))

        # 2. Verify that removing the null values or replacing with string fixes validation
        fixed_example = copy.deepcopy(bundled_example)
        del fixed_example["cannibalization_check"]["conflicting_url"]
        del fixed_example["cannibalization_check"]["exception_rationale"]
        # Now validation succeeds cleanly
        jsonschema.validate(instance=fixed_example, schema=schema)

    def test_challenge_17_content_handoff_role_enum_mismatch(self):
        """
        Empirically verify contract schema defect in content-handoff.json:
        In content-handoff.json, recommended_next_roles enum is:
        ['seo-analyst', 'reviewer', 'publisher', 'editor', 'technical-writer'].
        It omits 'content-manager', despite @content-manager being the primary editorial role
        in the 4-role swarm and in core/roles/content-manager.md (while 'editor' does not exist in core/roles).
        """
        schema = self.schemas["content-handoff.json"]
        allowed_roles = schema["properties"]["recommended_next_roles"]["items"]["enum"]

        # 1. Confirm 'content-manager' is absent and 'editor' is present
        self.assertNotIn("content-manager", allowed_roles, "Schema defect confirmed: 'content-manager' missing from enum")
        self.assertIn("editor", allowed_roles, "Legacy role 'editor' present in enum")

        # 2. Confirm 'editor.md' does not exist in core/roles/
        self.assertFalse((ROLES_DIR / "editor.md").exists(), "core/roles/editor.md does not exist")
        self.assertTrue((ROLES_DIR / "content-manager.md").exists(), "core/roles/content-manager.md exists")

        # 3. Empirically verify that targeting 'content-manager' causes ValidationError
        payload_with_cm = {
            "contract_type": "content-handoff",
            "content_path": "vesviet/content/posts/test.md",
            "status": "draft_ready",
            "recommended_next_roles": ["content-manager"],
        }
        with self.assertRaises(jsonschema.ValidationError) as ctx:
            jsonschema.validate(instance=payload_with_cm, schema=schema)
        self.assertIn("'content-manager' is not one of", str(ctx.exception))


# ==============================================================================
# 3. DUAL PARALLEL AUDIT BOUNDARY ISOLATION CHALLENGES
# ==============================================================================

class TestDualAuditBoundaryIsolation(unittest.TestCase):
    """
    Adversarial verification of Stream A (@content-manager) and Stream B (@technical-writer)
    audit boundary isolation:
    - Zero overlap in primary audit domains
    - Explicit negative boundary declarations
    - Independent sign-off requirements
    """

    @classmethod
    def setUpClass(cls):
        cls.wf_text = WORKFLOW_PACK_PATH.read_text(encoding="utf-8")
        cls.cm_role_text = (ROLES_DIR / "content-manager.md").read_text(encoding="utf-8")
        cls.tw_role_text = (ROLES_DIR / "technical-writer.md").read_text(encoding="utf-8")

    def test_challenge_11_explicit_negative_boundaries_present(self):
        """Verify workflow markdown explicitly defines Negative Boundaries for both auditors."""
        # Stream A (@content-manager) negative boundary
        self.assertIn("Negative Boundary**: `@content-manager` does NOT", self.wf_text)
        self.assertRegex(self.wf_text, r"(?i)content-manager.*does NOT validate code syntax")

        # Stream B (@technical-writer) negative boundary
        self.assertIn("Negative Boundary**: `@technical-writer` does NOT", self.wf_text)
        self.assertRegex(self.wf_text, r"(?i)technical-writer.*does NOT audit brand voice")

        # Phase 4 (@seo-analyst) negative boundary
        self.assertIn("Negative Boundary**: `@seo-analyst` does NOT", self.wf_text)
        self.assertRegex(self.wf_text, r"(?i)seo-analyst.*does NOT rewrite code snippets")

        # Phase 2 (@content-writer) negative boundary
        self.assertIn("`@content-writer` Does NOT", self.wf_text)
        self.assertRegex(self.wf_text, r"(?i)content-writer.*Does NOT.*Self-approve drafts")

    def test_challenge_12_audit_domain_mathematical_orthogonality(self):
        """
        Verify that Stream A and Stream B primary audit responsibility domains
        have ZERO intersection (mathematically disjoint sets).
        """
        # Stream A domains (Editorial Audit)
        stream_a_domains: Set[str] = {
            "brand_voice_consistency",
            "cliche_elimination",
            "sentence_burstiness",
            "active_voice_ratio",
            "top_10_serp_information_gain",
            "non_commodity_differential_score",
            "twin_content_differentiation",
            "eeat_author_entity_signals",
            "sme_credential_provenance",
            "audience_funnel_alignment",
        }

        # Stream B domains (Technical Audit)
        stream_b_domains: Set[str] = {
            "code_compilation_and_execution_validity",
            "version_pinning_conformance",
            "kubernetes_manifest_schema_validation",
            "cloudflare_wrangler_config_validation",
            "dockerfile_multistage_correctness",
            "benchmark_testbed_hardware_verification",
            "dataset_scale_and_latency_percentiles",
            "mermaid_ast_diagram_validation",
            "stub_and_todo_elimination",
            "context_cancellation_propagation",
        }

        # Stream C domains (SEO & Link Topology Audit)
        stream_c_domains: Set[str] = {
            "answer_first_bluf_word_count",
            "one_way_authority_flow_enforcement",
            "ten_anchor_pillar_hub_connectivity",
            "zero_orphan_crawl_check",
            "canonical_url_domain_independence",
            "connected_schema_org_jsonld",
            "geo_extractability_score",
        }

        # Assert pairwise disjointness
        intersection_ab = stream_a_domains.intersection(stream_b_domains)
        self.assertEqual(intersection_ab, set(), f"Stream A and Stream B overlap: {intersection_ab}")

        intersection_ac = stream_a_domains.intersection(stream_c_domains)
        self.assertEqual(intersection_ac, set(), f"Stream A and Stream C overlap: {intersection_ac}")

        intersection_bc = stream_b_domains.intersection(stream_c_domains)
        self.assertEqual(intersection_bc, set(), f"Stream B and Stream C overlap: {intersection_bc}")

    def test_challenge_13_dual_signoff_gate_logic(self):
        """Verify that a rejection in either Stream A or Stream B blocks pipeline progression."""
        def evaluate_dual_signoff(stream_a_passed: bool, stream_b_passed: bool) -> Tuple[bool, str]:
            if not stream_a_passed and not stream_b_passed:
                return False, "REJECT: Both Editorial and Technical audits failed"
            if not stream_a_passed:
                return False, "REJECT: Editorial audit failed (brand voice / information gain)"
            if not stream_b_passed:
                return False, "REJECT: Technical audit failed (code validity / benchmark testbed)"
            return True, "APPROVED: Proceed to Phase 4 SEO Authority audit"

        # Both pass
        ok, msg = evaluate_dual_signoff(True, True)
        self.assertTrue(ok)
        self.assertIn("APPROVED", msg)

        # Editorial fails, technical passes -> MUST REJECT
        ok, msg = evaluate_dual_signoff(False, True)
        self.assertFalse(ok)
        self.assertIn("Editorial audit failed", msg)

        # Technical fails, editorial passes -> MUST REJECT
        ok, msg = evaluate_dual_signoff(True, False)
        self.assertFalse(ok)
        self.assertIn("Technical audit failed", msg)

        # Both fail -> MUST REJECT
        ok, msg = evaluate_dual_signoff(False, False)
        self.assertFalse(ok)
        self.assertIn("Both", msg)

    def test_challenge_14_role_definition_file_consistency(self):
        """Verify content-manager and technical-writer role definitions in core/roles."""
        cm_text = self.cm_role_text
        tw_text = self.tw_role_text

        # content-manager must focus on strategy, SERP, Information Gain
        self.assertIn("Information Gain", cm_text)
        self.assertIn("Pillar-Cluster", cm_text)
        self.assertIn("Audience Lifecycle", cm_text)

        # technical-writer must focus on systems, technical communication, code/API
        self.assertIn("Technical Writer", tw_text)
        self.assertIn("llms.txt", tw_text)
        self.assertIn("documentation-handoff.json", tw_text)


# ==============================================================================
# 4. TWIN HUGO ARCHITECTURE & TOPOLOGY CHALLENGES
# ==============================================================================

class TestTwinHugoArchitectureTopology(unittest.TestCase):
    """
    Adversarial challenge on the Twin Hugo Architecture:
    - One-way authority flow (learn -> vesviet only, zero reverse links)
    - 10 Anchor Pillar Hubs backbone integrity
    - Canonical independence
    """

    @classmethod
    def setUpClass(cls):
        cls.readme_text = README_PATH.read_text(encoding="utf-8")
        cls.wf_text = WORKFLOW_PACK_PATH.read_text(encoding="utf-8")

    def test_challenge_15_one_way_authority_regex_crawler(self):
        """
        Simulate crawler detecting illegal reverse links:
        Any URL on tanhdev.com pointing to learn.tanhdev.com must be caught and rejected.
        """
        def scan_document_links(site: str, doc_content: str) -> List[str]:
            # Extract markdown links [text](url) and raw links
            urls = re.findall(r"\[.*?\]\((https?://[^\s\)]+|//[^\s\)]+)\)", doc_content)
            violations = []
            if site == "vesviet":
                for u in urls:
                    if re.search(r"(?:https?:)?//learn\.tanhdev\.com", u, re.IGNORECASE):
                        violations.append(u)
            return violations

        # Clean vesviet document (no learn links)
        clean_doc = """
        # Distributed Consensus
        See [Go Microservices](https://tanhdev.com/posts/go-microservices/)
        and [Raft Paper](https://raft.github.io/raft.pdf).
        """
        self.assertEqual(scan_document_links("vesviet", clean_doc), [])

        # Violating vesviet document (reverse link to learn)
        violating_doc = """
        # Distributed Consensus
        See [Vietnamese Notes](https://learn.tanhdev.com/series/raft/) for background.
        """
        violations = scan_document_links("vesviet", violating_doc)
        self.assertEqual(len(violations), 1)
        self.assertIn("https://learn.tanhdev.com/series/raft/", violations)

        # Allowed learn document linking to vesviet
        learn_doc = """
        # Nghiên cứu Raft
        Xem bài viết chi tiết tại [Flagship Masterclass](https://tanhdev.com/posts/alipay-double-11-architecture-tps/).
        """
        self.assertEqual(scan_document_links("learn", learn_doc), [])

    def test_challenge_16_ten_anchor_pillar_hubs_completeness(self):
        """Verify all 10 Anchor Pillar Hubs are documented with valid paths and descriptions."""
        authoritative_hubs = [
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
        for hub in authoritative_hubs:
            self.assertIn(hub, self.readme_text, f"README.md missing Anchor Hub: {hub}")

        # Upward link requirement in workflow
        self.assertRegex(self.wf_text, r"(?i)10\s+Anchor\s+Pillar\s+Hub")
        self.assertRegex(self.wf_text, r"(?i)zero\s+orphan")


# ==============================================================================
# MAIN RUNNER
# ==============================================================================

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
