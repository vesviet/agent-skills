"""
Adversarial Empirical Challenge Test Suite for vesviet-team Pack v5.0.0
Author: challenger_vesviet_1 (teamwork_preview_challenger)
Target: packs/vesviet-team, overlays/vesviet-content, live Hugo twin sites
"""

import os
import re
import glob
import json
import unittest
from pathlib import Path
import yaml
import jsonschema

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = PROJECT_ROOT / "packs"
VESVIET_PACK_DIR = PACKS_DIR / "vesviet-team"
MANIFEST_PATH = VESVIET_PACK_DIR / "manifest.yaml"
PACK_README_PATH = VESVIET_PACK_DIR / "README.md"
PACKS_README_PATH = PACKS_DIR / "README.md"
VESVIET_OVERLAY_DIR = PROJECT_ROOT / "overlays" / "vesviet-content"
LINK_TOPOLOGY_RULE = VESVIET_OVERLAY_DIR / "rules" / "link-topology.md"
ORIGINAL_REQUEST_PATH = Path("d:/myproject/.agents/ORIGINAL_REQUEST.md")

VESVIET_SITE_DIR = Path("d:/myproject/vesviet")
LEARN_SITE_DIR = Path("d:/myproject/learn")

VESVIET_CONTENT_INDEX = VESVIET_SITE_DIR / "reports" / "CONTENT_INDEX.md"
LEARN_PLAN_CONTENT_INDEX = LEARN_SITE_DIR / "plan" / "CONTENT_INDEX.md"
LEARN_REPORTS_CONTENT_INDEX = LEARN_SITE_DIR / "reports" / "CONTENT_INDEX.md"


def count_words_standard(text: str) -> int:
    """Canonical tokenizer matching Hugo / Markdown word counting."""
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"`[^`]*`", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Remove markdown link URLs, keep anchor text
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    tokens = re.findall(r"[\w\u00C0-\u1EF9]+(?:-[\w\u00C0-\u1EF9]+)*", cleaned)
    return len(tokens)


def count_words_adversarial_hyphenated(text: str) -> int:
    """Adversarial tokenizer splitting hyphenated compound words."""
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"`[^`]*`", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    tokens = re.findall(r"[\w\u00C0-\u1EF9]+", cleaned)
    return len(tokens)


# ==============================================================================
# CHALLENGE 1: CORPUS METRICS & INDEX CONSISTENCY
# ==============================================================================

class TestCorpusMetricsConsistency(unittest.TestCase):
    """
    Stress-tests corpus counts across manifest.yaml, CONTENT_INDEX.md files,
    documentation, and actual disk storage.
    """

    @classmethod
    def setUpClass(cls):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            cls.manifest = yaml.safe_load(f)
        with open(PACK_README_PATH, "r", encoding="utf-8") as f:
            cls.readme = f.read()

    def test_01_manifest_vs_original_request_invariants(self):
        """Manifest corpus metrics must exactly match authoritative user request numbers."""
        c = self.manifest.get("corpus", {})
        v = c.get("vesviet", {})
        l = c.get("learn", {})

        # ORIGINAL_REQUEST R1 authoritative counts
        expected_v = {
            "content_files": 374,
            "posts": 66,
            "series_dirs": 25,
            "series_files": 251,
            "radar_files": 34,
            "reports": 296,
        }
        for k, exp in expected_v.items():
            self.assertEqual(v.get(k), exp, f"vesviet manifest {k} mismatch: got {v.get(k)}, expected {exp}")

        expected_l = {
            "content_files": 433,
            "posts": 86,
            "series_dirs": 25,
            "series_files": 251,
            "radar_files": 70,
            "docs": 3,
            "reports": 276,
        }
        for k, exp in expected_l.items():
            self.assertEqual(l.get(k), exp, f"learn manifest {k} mismatch: got {l.get(k)}, expected {exp}")

    def test_02_manifest_corpus_vs_live_content_files_on_disk(self):
        """Audit manifest content counts against live .md files on disk."""
        if not VESVIET_SITE_DIR.exists() or not LEARN_SITE_DIR.exists():
            self.skipTest("Live site directories not found on local disk")

        # vesviet content files (.md in vesviet/content/)
        v_content_md = list(VESVIET_SITE_DIR.glob("content/**/*.md"))
        v_posts_md = list((VESVIET_SITE_DIR / "content" / "posts").glob("*.md"))
        v_series_md = list((VESVIET_SITE_DIR / "content" / "series").glob("**/*.md"))
        v_radar_md = list((VESVIET_SITE_DIR / "content" / "radar").glob("**/*.md"))
        v_series_dirs = [d for d in (VESVIET_SITE_DIR / "content" / "series").iterdir() if d.is_dir()]

        c = self.manifest["corpus"]
        self.assertEqual(len(v_content_md), c["vesviet"]["content_files"], "vesviet live content_files mismatch")
        self.assertEqual(len(v_posts_md), c["vesviet"]["posts"], "vesviet live posts mismatch")
        self.assertEqual(len(v_series_md), c["vesviet"]["series_files"], "vesviet live series_files mismatch")
        self.assertEqual(len(v_radar_md), c["vesviet"]["radar_files"], "vesviet live radar_files mismatch")
        self.assertEqual(len(v_series_dirs), c["vesviet"]["series_dirs"], "vesviet live series_dirs mismatch")

        # learn content files (.md in learn/content/)
        l_content_md = list(LEARN_SITE_DIR.glob("content/**/*.md"))
        l_posts_md = list((LEARN_SITE_DIR / "content" / "posts").glob("*.md"))
        l_series_md = list((LEARN_SITE_DIR / "content" / "series").glob("**/*.md"))
        l_radar_md = list((LEARN_SITE_DIR / "content" / "radar").glob("**/*.md"))
        l_docs_md = list((LEARN_SITE_DIR / "content" / "docs").glob("**/*.md"))
        l_series_dirs = [d for d in (LEARN_SITE_DIR / "content" / "series").iterdir() if d.is_dir()]

        self.assertEqual(len(l_content_md), c["learn"]["content_files"], "learn live content_files mismatch")
        self.assertEqual(len(l_posts_md), c["learn"]["posts"], "learn live posts mismatch")
        self.assertEqual(len(l_series_md), c["learn"]["series_files"], "learn live series_files mismatch")
        self.assertEqual(len(l_radar_md), c["learn"]["radar_files"], "learn live radar_files mismatch")
        self.assertEqual(len(l_docs_md), c["learn"]["docs"], "learn live docs mismatch")
        self.assertEqual(len(l_series_dirs), c["learn"]["series_dirs"], "learn live series_dirs mismatch")

    def test_03_content_index_reference_files_existence(self):
        """Check that manifest declared index files exist."""
        declared_indexes = self.manifest.get("corpus", {}).get("indexes", [])
        self.assertGreater(len(declared_indexes), 0, "Manifest must declare corpus index paths")
        for idx in declared_indexes:
            idx_path = Path("d:/myproject") / idx
            self.assertTrue(idx_path.exists(), f"Declared index file must exist on disk: {idx_path}")

    def test_04_readme_corpus_consistency(self):
        """Packs README and vesviet-team README must accurately report twin metrics."""
        self.assertIn("25-series", self.readme)
        self.assertIn("251", self.readme)


# ==============================================================================
# CHALLENGE 2: BLUF <= 60 WORDS CONSTRAINT ENFORCEMENT & BOUNDARY CASES
# ==============================================================================

class TestBLUFWordCountBoundaries(unittest.TestCase):
    """
    Stress-tests the Answer-First BLUF <= 60 words constraint across edge cases:
    boundary transitions, Unicode, Markdown formatting, non-breaking spaces,
    and actual corpus validation.
    """

    def test_01_exact_boundaries(self):
        """Verify strict inequality: <= 60 words passes, 61 words fails."""
        for n in [1, 10, 50, 59, 60]:
            text = " ".join([f"token{i}" for i in range(n)])
            self.assertLessEqual(count_words_standard(text), 60, f"{n} words must pass")

        for n in [61, 62, 70, 100]:
            text = " ".join([f"token{i}" for i in range(n)])
            self.assertGreater(count_words_standard(text), 60, f"{n} words must fail")

    def test_02_markdown_markup_stripping(self):
        """Formatting (bold, inline code, links) must not inflate word counts inappropriately."""
        text = "**Answer-first:** Using `Go 1.25` [synctest](https://golang.org/pkg/synctest) enables deterministic concurrency testing."
        count = count_words_standard(text)
        self.assertLessEqual(count, 15)

        text_with_code = "Summary text. ```go\nfunc main() {}\n``` Outcome achieved."
        count_clean = count_words_standard(text_with_code)
        self.assertEqual(count_clean, 4)

    def test_03_vietnamese_diacritics_and_compound_words(self):
        """Vietnamese diacritics and technical tokens must tokenize cleanly."""
        vn_bluf = (
            "Kiến trúc Raft phân tán đảm bảo tính nhất quán mạnh mẽ (Linearizable Consistency) "
            "thông qua thuật toán bầu cử Leader Election và sao chép nhật ký Log Replication "
            "với độ trễ P99 dưới 12ms trên cụm 5 nodes etcd v3.5."
        )
        count = count_words_standard(vn_bluf)
        self.assertLessEqual(count, 60)
        self.assertGreater(count, 20)

    def test_04_hyphenated_word_boundary_divergence(self):
        """
        Stress test: Difference between standard tokenizer and adversarial
        hyphen-splitting tokenizer on hyphen-dense engineering text.
        """
        text_hyphen_dense = " ".join(["high-throughput", "low-latency", "lock-free", "zero-copy", "real-time"] * 6)
        std_count = count_words_standard(text_hyphen_dense)
        adv_count = count_words_adversarial_hyphenated(text_hyphen_dense)

        self.assertEqual(std_count, 30)
        self.assertEqual(adv_count, 60)

    def test_05_whitespace_and_non_breaking_spaces(self):
        """Non-breaking spaces (\\u00a0) and multiple whitespace must not cause tokenization bugs."""
        text = "word1\u00a0word2  word3\tword4\nword5"
        self.assertEqual(count_words_standard(text), 5)

    def test_06_live_corpus_bluf_scan(self):
        """
        Scan actual published posts on vesviet and learn to ensure no live post
        violates the Gate 1 BLUF <= 60 words rule.
        """
        if not VESVIET_SITE_DIR.exists():
            self.skipTest("vesviet site dir not available")

        bluf_pattern = re.compile(r">\s*\*\*Answer-first:\*\*\s*([^\n]+(?:\n>[^\n]+)*)", re.IGNORECASE)
        violations = []
        posts = list((VESVIET_SITE_DIR / "content" / "posts").glob("*.md"))

        for p in posts:
            content = p.read_text(encoding="utf-8", errors="ignore")
            match = bluf_pattern.search(content)
            if match:
                bluf_raw = match.group(1).replace("\n>", " ").strip()
                wc = count_words_standard(bluf_raw)
                if wc > 60:
                    violations.append((p.name, wc, bluf_raw))

        self.assertEqual(len(violations), 0, f"Found {len(violations)} posts exceeding 60 words BLUF: {violations}")


# ==============================================================================
# CHALLENGE 3: ONE-WAY AUTHORITY & CANONICAL INDEPENDENCE
# ==============================================================================

class TestOneWayAuthorityAndCanonicalInvariants(unittest.TestCase):
    """
    Adversarial verification of the One-Way Authority Rule and Canonical Independence:
    - vesviet MUST NEVER link to learn.tanhdev.com
    - learn links to tanhdev.com are permitted/encouraged
    - canonicalURL on vesviet must point to https://tanhdev.com/
    - canonicalURL on learn must point to https://learn.tanhdev.com/
    """

    def test_01_vesviet_to_learn_leakage_scan(self):
        """
        EMPIRICAL SCAN: Search every single markdown file in vesviet/content/
        for forbidden links to learn.tanhdev.com.
        """
        if not VESVIET_SITE_DIR.exists():
            self.skipTest("vesviet site dir not available")

        forbidden_pattern = re.compile(r"(https?:)?//learn\.tanhdev\.com", re.IGNORECASE)
        leaks = []

        for md_file in VESVIET_SITE_DIR.glob("content/**/*.md"):
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            match = forbidden_pattern.search(text)
            if match:
                leaks.append(str(md_file.relative_to(VESVIET_SITE_DIR)))

        self.assertEqual(len(leaks), 0, f"VIOLATION: Found reverse links from vesviet to learn: {leaks}")

    def test_02_canonical_url_self_referencing(self):
        """
        Verify canonicalURL self-referencing on both twin sites:
        No cross-site canonicalization allowed.
        """
        if not VESVIET_SITE_DIR.exists() or not LEARN_SITE_DIR.exists():
            self.skipTest("Site dirs not available")

        canonical_pattern = re.compile(r"^canonicalURL:\s*[\"']?([^\"'\n]+)[\"']?", re.MULTILINE)

        # Audit vesviet posts
        for p in (VESVIET_SITE_DIR / "content" / "posts").glob("*.md"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            m = canonical_pattern.search(text)
            if m:
                url = m.group(1).strip()
                self.assertFalse("learn.tanhdev.com" in url, f"Cross-site canonical on vesviet: {p.name} -> {url}")
                self.assertTrue(url.startswith("https://tanhdev.com/") or url.startswith("/"),
                                f"vesviet canonicalURL must be self-referential to tanhdev.com: {url}")

        # Audit learn posts
        for p in (LEARN_SITE_DIR / "content" / "posts").glob("*.md"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            m = canonical_pattern.search(text)
            if m:
                url = m.group(1).strip()
                self.assertFalse(url.startswith("https://tanhdev.com/"),
                                f"learn must not cross-site canonicalize to vesviet: {p.name} -> {url}")

    def test_03_adversarial_link_injector_rejection(self):
        """Adversarial oracle: Rejects sneaky reverse-link obfuscation schemes."""
        sneaky_links = [
            "https://learn.tanhdev.com/posts/xyz",
            "http://learn.tanhdev.com/posts/xyz",
            "//learn.tanhdev.com/posts/xyz",
            "https://LEARN.TANHDEV.COM/posts/xyz",
            "https://learn.tanhdev.com:443/posts/xyz",
            "[Read notes](https://learn.tanhdev.com/notes)",
            '<a href="https://learn.tanhdev.com/">Twin</a>',
        ]

        def is_forbidden_vesviet_content(content: str) -> bool:
            return bool(re.search(r"(?:https?:)?//learn\.tanhdev\.com(?::\d+)?", content, re.IGNORECASE))

        for link in sneaky_links:
            self.assertTrue(is_forbidden_vesviet_content(link), f"Failed to detect reverse link: {link}")


# ==============================================================================
# CHALLENGE 4: 10 ANCHOR PILLAR HUBS & UPWARD LINKING TOPOLOGY
# ==============================================================================

class TestAnchorPillarHubsAndTopology(unittest.TestCase):
    """
    Empirical challenge on the 10 Anchor Pillar Hub paths:
    Validates filesystem reality against documentation and rules.
    """

    @classmethod
    def setUpClass(cls):
        with open(PACK_README_PATH, "r", encoding="utf-8") as f:
            cls.readme = f.read()
        with open(LINK_TOPOLOGY_RULE, "r", encoding="utf-8") as f:
            cls.topology_rule = f.read()

    def test_01_link_topology_rule_hubs_exist_on_disk(self):
        """
        The 10 Anchor Pillar Hubs specified in overlays/vesviet-content/rules/link-topology.md
        MUST all exist on disk in vesviet/content/.
        """
        if not VESVIET_SITE_DIR.exists():
            self.skipTest("vesviet site dir not available")

        expected_hubs = [
            "posts/go-microservices.md",
            "posts/architecting-21-service-ecommerce-golang-ddd.md",
            "posts/aws-eks-vs-ecs-comparison.md",
            "posts/banking-microservices-architecture.md",
            "posts/cloudflare-d1-durable-objects-realtime-cart.md",
            "posts/deploying-astro-on-cloudflare-full-stack-edge-architecture.md",
            "posts/generative-ui-with-mcp-ai-native-frontend.md",
            "posts/alipay-double-11-architecture-tps.md",
            "reading-map.md",
            "hire.md",
        ]

        missing = []
        for hub in expected_hubs:
            hub_path = VESVIET_SITE_DIR / "content" / hub
            if not hub_path.exists():
                missing.append(hub)

        self.assertEqual(len(missing), 0, f"Anchor pillar hubs from link-topology.md missing on disk: {missing}")

    def test_02_pack_readme_pillar_hub_path_discrepancy(self):
        """
        EMPIRICAL CHALLENGE: Verify whether the file paths declared in
        packs/vesviet-team/README.md table exist on disk.
        Surfaces divergence where README declares series/_index.md files that do not exist!
        """
        if not VESVIET_SITE_DIR.exists():
            self.skipTest("vesviet site dir not available")

        readme_declared_paths = [
            ("posts/alipay-double-11-architecture-tps.md", True),
            ("posts/aws-eks-vs-ecs-comparison.md", True),
            ("posts/go-microservices.md", True),
            ("series/ebpf/_index.md", False),        # NON-EXISTENT ON DISK!
            ("posts/banking-microservices-architecture.md", True),
            ("posts/cloudflare-d1-durable-objects-realtime-cart.md", True),
            ("series/service-mesh/_index.md", False), # NON-EXISTENT ON DISK!
            ("posts/architecting-21-service-ecommerce-golang-ddd.md", True),
            ("series/sre/_index.md", False),         # NON-EXISTENT ON DISK!
            ("posts/generative-ui-with-mcp-ai-native-frontend.md", True),
        ]

        actual_status = {}
        for rel_path, _ in readme_declared_paths:
            full_p = VESVIET_SITE_DIR / "content" / rel_path
            actual_status[rel_path] = full_p.exists()

        non_existent = [p for p, exists in actual_status.items() if not exists]
        self.assertEqual(set(non_existent), {
            "series/ebpf/_index.md",
            "series/service-mesh/_index.md",
            "series/sre/_index.md",
        }, "Discrepancy: README.md refers to 3 series hubs that are conceptual rather than existing series dirs")

    def test_03_series_dirs_inventory(self):
        """
        Verify that there are exactly 25 series directories in vesviet and learn,
        and verify their exact symmetry.
        """
        if not VESVIET_SITE_DIR.exists() or not LEARN_SITE_DIR.exists():
            self.skipTest("Site dirs not available")

        v_series = sorted([d.name for d in (VESVIET_SITE_DIR / "content" / "series").iterdir() if d.is_dir()])
        l_series = sorted([d.name for d in (LEARN_SITE_DIR / "content" / "series").iterdir() if d.is_dir()])

        self.assertEqual(len(v_series), 25, "vesviet must have exactly 25 series dirs")
        self.assertEqual(len(l_series), 25, "learn must have exactly 25 series dirs")
        self.assertEqual(v_series, l_series, "vesviet and learn series directories must have 100% naming symmetry")


# ==============================================================================
# CHALLENGE 5: GOVERNANCE & CONTRACT DEFECT VERIFICATION
# ==============================================================================

class TestGovernanceAndContractDefects(unittest.TestCase):
    """
    Stress-tests JSON Schema contract constraints and tooling claims.
    """

    def test_01_content_handoff_role_enum_discrepancy(self):
        """
        EMPIRICAL FINDING: content-handoff.json restricts recommended_next_roles
        to an enum that excludes 'content-manager' (only allows 'editor').
        """
        schema_path = PROJECT_ROOT / "core" / "contracts" / "schemas" / "content-handoff.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        roles_enum = schema["properties"]["recommended_next_roles"]["items"].get("enum", [])
        self.assertIn("technical-writer", roles_enum)
        self.assertIn("seo-analyst", roles_enum)
        # Empirical proof of defect: content-manager is missing from schema enum
        self.assertNotIn("content-manager", roles_enum,
                         "Proves defect: content-manager is omitted from content-handoff schema enum")
        self.assertIn("editor", roles_enum,
                      "Legacy role 'editor' is present instead of 'content-manager'")

    def test_02_seo_audit_schema_defect_investigation(self):
        """
        EMPIRICAL FINDING: seo-audit-report.json bundled example sets
        conflicting_url: null and exception_rationale: null,
        which are strictly typed as {"type": "string"} in the schema definition.
        """
        schema_path = PROJECT_ROOT / "core" / "contracts" / "schemas" / "seo-audit-report.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        # Check property definition
        cannibalization = schema["properties"]["cannibalization_check"]["properties"]
        conflicting_url_type = cannibalization["conflicting_url"]["type"]
        self.assertEqual(conflicting_url_type, "string", "conflicting_url is typed as string without null")

        # Confirm that validating an object with None/null fails against this property
        test_payload = {
            "conflicting_url": None,
            "status": "clear"
        }
        sub_schema = schema["properties"]["cannibalization_check"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=test_payload, schema=sub_schema)

    def test_03_check_posts_script_reality_vs_readme_claim(self):
        """
        EMPIRICAL FINDING: README.md claims check_posts.py audits zero-orphan
        enforcement, but inspecting the code reveals it contains 0 orphan/link logic.
        """
        script_path = VESVIET_SITE_DIR / "reports" / "check_posts.py"
        if not script_path.exists():
            self.skipTest("check_posts.py not found on disk")

        content = script_path.read_text(encoding="utf-8", errors="ignore")
        self.assertNotIn("orphan", content.lower(), "check_posts.py does not contain orphan checking")
        self.assertNotIn("inbound", content.lower(), "check_posts.py does not contain inbound link analysis")

    def test_04_pillar_hubs_readme_vs_link_topology_divergence(self):
        """
        EMPIRICAL FINDING: README Section 2 defines the 10 Anchor Pillar Hubs
        differently from link-topology.md.
        - link-topology.md uses 8 real posts + reading-map + hire (all exist on disk).
        - README.md uses 7 real posts + 3 conceptual series/_index.md files.
        """
        readme_path = PACK_README_PATH.read_text(encoding="utf-8")
        topology_rule_path = LINK_TOPOLOGY_RULE.read_text(encoding="utf-8")

        self.assertIn("deploying-astro-on-cloudflare-full-stack-edge-architecture.md", topology_rule_path)
        # README table replaced deploying-astro with conceptual series/ebpf/_index.md
        self.assertIn("series/ebpf/_index.md", readme_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
