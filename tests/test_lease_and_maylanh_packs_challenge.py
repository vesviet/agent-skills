"""
Comprehensive Challenge Test Suite for lease-team and maylanhtreotuong-team Packs v5.0.0
Validates: Manifest schemas, live repo metrics, README depth, workflow contracts, and pack spotlights.
"""

import unittest
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = PROJECT_ROOT / "packs"
PACKS_README = PACKS_DIR / "README.md"

LEASE_DIR = PACKS_DIR / "lease-team"
LEASE_MANIFEST = LEASE_DIR / "manifest.yaml"
LEASE_README = LEASE_DIR / "README.md"
LEASE_WORKFLOW = LEASE_DIR / "workflows" / "publish-lease-content.md"
LEASE_REPO = Path("D:/myproject/leaseinvietnam")

MAYLANH_DIR = PACKS_DIR / "maylanhtreotuong-team"
MAYLANH_MANIFEST = MAYLANH_DIR / "manifest.yaml"
MAYLANH_README = MAYLANH_DIR / "README.md"
MAYLANH_WORKFLOW = MAYLANH_DIR / "workflows" / "publish-maylanhtreotuong-content.md"
MAYLANH_REPO = Path("D:/myproject/maylanhtreotuong")


class TestLeaseTeamPackV5(unittest.TestCase):
    """Rigorous tests for lease-team pack v5.0.0."""

    def setUp(self):
        self.assertTrue(LEASE_MANIFEST.exists(), "lease-team/manifest.yaml must exist")
        with open(LEASE_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_manifest_metadata(self):
        self.assertEqual(self.manifest.get("schema_version"), "2")
        self.assertEqual(self.manifest.get("version"), "5.0.0")
        self.assertEqual(self.manifest.get("name"), "lease-team")
        self.assertIn("content", self.manifest.get("tags", []))
        self.assertIn("seo", self.manifest.get("tags", []))
        self.assertIn("expat-housing", self.manifest.get("tags", []))

    def test_manifest_roles_and_skills(self):
        cf = self.manifest.get("content_focus", {})
        primary_roles = cf.get("primary_roles", [])
        self.assertIn("content-writer", primary_roles)
        self.assertIn("seo-analyst", primary_roles)
        self.assertIn("content-manager", primary_roles)
        self.assertIn("task-planner", primary_roles)
        self.assertIn("publish-lease-content", cf.get("workflows", []))

    def test_readme_depth_and_sections(self):
        self.assertTrue(LEASE_README.exists(), "lease-team/README.md must exist")
        text = LEASE_README.read_text(encoding="utf-8")
        self.assertGreater(len(text), 5000, "README must be comprehensive")
        self.assertIn("5-Pillar", text)
        self.assertIn("AnswerFirst", text)
        self.assertIn("Intelligence", text)
        self.assertIn("Information", text)
        self.assertIn("Insights", text)
        self.assertIn("Neighborhoods", text)
        self.assertIn("Integration", text)
        self.assertIn("Decree 95/2024/ND-CP", text)

    def test_workflow_contract(self):
        self.assertTrue(LEASE_WORKFLOW.exists(), "publish-lease-content.md must exist")
        wf_text = LEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Phase 1: Planning", wf_text)
        self.assertIn("Phase 2: Masterclass Drafting", wf_text)
        self.assertIn("Phase 3: Parallel Editorial & Legal Audit", wf_text)
        self.assertIn("Phase 4: GEO/AEO", wf_text)
        self.assertIn("Phase 5: Build Verification", wf_text)

    def test_live_corpus_consistency(self):
        if LEASE_REPO.exists():
            posts = list((LEASE_REPO / "src" / "data" / "post").rglob("*.md*"))
            properties = list((LEASE_REPO / "src" / "data" / "property").rglob("*.md*"))
            corpus = self.manifest.get("corpus", {}).get("leaseinvietnam", {})
            self.assertEqual(len(posts), corpus.get("posts"))
            self.assertEqual(len(properties), corpus.get("properties"))


class TestMayLanhTreoTuongPackV5(unittest.TestCase):
    """Rigorous tests for maylanhtreotuong-team pack v5.0.0."""

    def setUp(self):
        self.assertTrue(MAYLANH_MANIFEST.exists(), "maylanhtreotuong-team/manifest.yaml must exist")
        with open(MAYLANH_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_manifest_metadata(self):
        self.assertEqual(self.manifest.get("schema_version"), "2")
        self.assertEqual(self.manifest.get("version"), "5.0.0")
        self.assertEqual(self.manifest.get("name"), "maylanhtreotuong-team")
        self.assertIn("hvac", self.manifest.get("tags", []))
        self.assertIn("cloudflare", self.manifest.get("tags", []))
        self.assertIn("vietnam", self.manifest.get("tags", []))

    def test_manifest_roles_and_skills(self):
        cf = self.manifest.get("content_focus", {})
        primary_roles = cf.get("primary_roles", [])
        self.assertIn("content-writer", primary_roles)
        self.assertIn("seo-analyst", primary_roles)
        self.assertIn("content-manager", primary_roles)
        self.assertIn("task-planner", primary_roles)
        self.assertIn("publish-maylanhtreotuong-content", cf.get("workflows", []))

    def test_readme_depth_and_sections(self):
        self.assertTrue(MAYLANH_README.exists(), "maylanhtreotuong-team/README.md must exist")
        text = MAYLANH_README.read_text(encoding="utf-8")
        self.assertGreater(len(text), 5000, "README must be comprehensive")
        self.assertIn("TCVN 7830:2021", text)
        self.assertIn("ASHRAE Standard 55-2023", text)
        self.assertIn("CSPF", text)
        self.assertIn("Hioki 3334", text)
        self.assertIn("RION NL-52", text)
        self.assertIn("7 Strict Silo", text)

    def test_workflow_contract(self):
        self.assertTrue(MAYLANH_WORKFLOW.exists(), "publish-maylanhtreotuong-content.md must exist")
        wf_text = MAYLANH_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Phase 1: Silo Topic Assignment", wf_text)
        self.assertIn("Phase 2: Technical Drafting", wf_text)
        self.assertIn("Phase 3: Parallel Editorial & HVAC Engineering Audit", wf_text)
        self.assertIn("Phase 4: Strict Silo & Schema.org Audit", wf_text)
        self.assertIn("Phase 5: Build Verification", wf_text)

    def test_live_corpus_consistency(self):
        if MAYLANH_REPO.exists():
            posts = list((MAYLANH_REPO / "src" / "data" / "post").rglob("*.md*"))
            products = list((MAYLANH_REPO / "src" / "data" / "product").rglob("*.md*"))
            corpus = self.manifest.get("corpus", {}).get("maylanhtreotuong", {})
            self.assertEqual(len(posts), corpus.get("posts"))
            self.assertEqual(len(products), corpus.get("products"))


class TestPackEcosystemSpotlights(unittest.TestCase):
    """Ensure packs/README.md correctly spotlights all upgraded packs."""

    def test_spotlights_in_packs_readme(self):
        self.assertTrue(PACKS_README.exists())
        content = PACKS_README.read_text(encoding="utf-8")
        self.assertIn("Pack Spotlight: vesviet-team (v5.0.0)", content)
        self.assertIn("Pack Spotlight: lease-team (v5.0.0)", content)
        self.assertIn("Pack Spotlight: maylanhtreotuong-team (v5.0.0)", content)
        self.assertIn("5-Pillar Content Framework", content)
        self.assertIn("TCVN 7830:2021", content)


if __name__ == "__main__":
    unittest.main()
