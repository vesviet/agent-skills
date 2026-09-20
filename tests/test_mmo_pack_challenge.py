"""
Empirical Challenge Test Suite for mmo-growth-team Pack v5.0.0
Validates: Manifest schema v2, README depth, MMO Campaign Lifecycle workflow,
modernized MMO skills (<200 lines), fast aliases, contract schemas, and test suite zero-drift.
"""

import unittest
from pathlib import Path
import json
import yaml
import jsonschema
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = PROJECT_ROOT / "packs"
MMO_PACK_DIR = PACKS_DIR / "mmo-growth-team"
MMO_MANIFEST = MMO_PACK_DIR / "manifest.yaml"
MMO_README = MMO_PACK_DIR / "README.md"
PACKS_README = PACKS_DIR / "README.md"

CORE_DIR = PROJECT_ROOT / "core"
WORKFLOW_PATH = CORE_DIR / "workflows" / "mmo-campaign-lifecycle.md"
WORKFLOWS_README = CORE_DIR / "workflows" / "README.md"
ROOT_README = PROJECT_ROOT / "README.md"
SKILLS_DIR = CORE_DIR / "skills" / "mmo"
SCHEMAS_DIR = CORE_DIR / "contracts" / "schemas"
GENERATE_INDEX = CORE_DIR / "scripts" / "generate-index.py"
RESEARCH_DOC = PROJECT_ROOT / "mmo_2027_100_rounds_deep_research.md"


class TestMMOPackManifestAndMetadata(unittest.TestCase):
    """Challenge 1: Verify mmo-growth-team manifest against v5.0.0 & Schema v2 standards."""

    def setUp(self):
        self.assertTrue(MMO_MANIFEST.exists(), "mmo-growth-team/manifest.yaml must exist")
        with open(MMO_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_manifest_metadata(self):
        self.assertEqual(self.manifest.get("schema_version"), "2")
        self.assertEqual(self.manifest.get("version"), "5.0.0")
        self.assertEqual(self.manifest.get("name"), "mmo-growth-team")
        tags = self.manifest.get("tags", [])
        for required_tag in [
            "core",
            "mmo",
            "growth-engineering",
            "s2s-tracking",
            "stealth-automation",
            "anti-detect-browsers",
            "affiliate",
            "programmatic-seo",
            "traffic-arbitrage",
            "roi-optimization",
            "depin",
            "multi-agent-swarm",
        ]:
            self.assertIn(required_tag, tags)

    def test_roles_and_skills(self):
        focus = self.manifest.get("mmo_focus", {})
        primary_roles = focus.get("primary_roles", [])
        self.assertIn("mmo-engineer", primary_roles)
        self.assertIn("seo-analyst", primary_roles)
        self.assertIn("content-writer", primary_roles)
        self.assertIn("data-analyst", primary_roles)
        self.assertIn("security-engineer", primary_roles)
        self.assertIn("mmo-campaign-lifecycle", focus.get("workflows", []))

    def test_governance_block(self):
        gov = self.manifest.get("governance", {})
        self.assertEqual(gov.get("eu_ai_act_tier"), "minimal_risk")
        self.assertTrue(gov.get("human_oversight", {}).get("required"))
        self.assertEqual(gov.get("secret_handling"), "env_only")
        self.assertEqual(gov.get("audit_logging"), "required")
        self.assertEqual(gov.get("audit_format"), "otel-json")
        self.assertEqual(gov.get("retention_days"), 90)

    def test_research_protocol_and_pipeline(self):
        protocol = self.manifest.get("deep_research_protocol", {})
        self.assertEqual(protocol.get("rounds"), 100)
        self.assertEqual(protocol.get("clusters"), 5)
        self.assertEqual(protocol.get("rounds_per_cluster"), 20)

        pipeline = self.manifest.get("swarm_pipeline", {})
        self.assertEqual(len(pipeline), 5)
        for phase_key in ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5"]:
            self.assertIn(phase_key, pipeline)


class TestMMOPackReadMeAndOperatingStandard(unittest.TestCase):
    """Challenge 2: Verify packs/mmo-growth-team/README.md depth and pack spotlight."""

    def test_readme_depth_and_sections(self):
        self.assertTrue(MMO_README.exists(), "mmo-growth-team/README.md must exist")
        text = MMO_README.read_text(encoding="utf-8")
        self.assertGreater(len(text), 5000, "README must be comprehensive (>5000 chars)")
        self.assertIn("5-Phase", text)
        self.assertIn("S2S", text)
        self.assertIn("Blended ROAS", text)
        self.assertIn("100-Round", text)
        self.assertIn("Camoufox", text)
        self.assertIn("WebGPU", text)
        self.assertIn("```mermaid", text)

    def test_spotlight_in_packs_readme(self):
        content = PACKS_README.read_text(encoding="utf-8")
        self.assertIn("Pack Spotlight: mmo-growth-team (v5.0.0)", content)
        self.assertIn("`mmo-growth-team`", content)
        self.assertIn("## Available Packs (15)", content)


class TestMMOCampaignLifecycleWorkflow(unittest.TestCase):
    """Challenge 3: Verify core/workflows/mmo-campaign-lifecycle.md conformity."""

    def test_workflow_structure(self):
        self.assertTrue(WORKFLOW_PATH.exists(), "mmo-campaign-lifecycle.md must exist")
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("## MMO Campaign Lifecycle Workflow", text)
        self.assertIn("### Prerequisites", text)
        self.assertIn("### Workflow Steps", text)
        self.assertIn("### Checklist", text)
        self.assertIn("### Related Workflows", text)
        self.assertIn("### Related Skills", text)

    def test_workflow_steps_and_roles(self):
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        for step in ["#### 1. ", "#### 2. ", "#### 3. ", "#### 4. ", "#### 5. "]:
            self.assertIn(step, text)
        self.assertIn("Role: **MMO Engineer**", text)
        self.assertIn("Use skill: `conduct-research`", text)
        self.assertIn("Use skill: `setup-tracking-system`", text)
        self.assertIn("Use skill: `create-automation-script`", text)
        self.assertIn("Use skill: `analyze-campaign-roi`", text)

    def test_workflow_indexing(self):
        wf_readme = WORKFLOWS_README.read_text(encoding="utf-8")
        self.assertIn("[mmo-campaign-lifecycle](mmo-campaign-lifecycle.md)", wf_readme)
        root_readme = ROOT_README.read_text(encoding="utf-8")
        self.assertTrue(
            "- `/mmo-campaign-lifecycle`" in root_readme or "- /mmo-campaign-lifecycle" in root_readme,
            "Workflow /mmo-campaign-lifecycle must be listed in root README.md"
        )


class TestMMOSkillsModernizationAndLineLimits(unittest.TestCase):
    """Challenge 4: Verify 7 MMO skills line limits (<200 lines) and 2027 SOTA content."""

    def test_all_7_skills_line_count(self):
        expected_skills = [
            "setup-tracking-system",
            "create-automation-script",
            "deploy-mmo-infrastructure",
            "manage-mmo-assets",
            "deploy-proxyware-fleet",
            "generate-mmo-content",
            "analyze-campaign-roi",
        ]
        for skill in expected_skills:
            path = SKILLS_DIR / skill / "SKILL.md"
            self.assertTrue(path.exists(), f"Skill file {skill} must exist")
            lines = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLess(lines, 200, f"{skill} must be strictly < 200 lines (got {lines})")


class TestMMOFastAliasesAndIndexDrift(unittest.TestCase):
    """Challenge 5: Verify fast aliases and generate-index.py synchronization."""

    def test_fast_aliases_in_generator(self):
        text = GENERATE_INDEX.read_text(encoding="utf-8")
        # Skill aliases
        for alias in [
            "roi",
            "tracking",
            "stealth_automation",
            "mmo_infra",
            "proxy_fleet",
            "mmo_content",
            "mmo_assets",
            "s2s_tracking",
            "depin_bandwidth",
            "pseo_landing",
            "vcc_isolation",
            "mmo_campaign",
            "mmo_growth",
            "growth_stack",
        ]:
            self.assertIn(f'"{alias}":', text, f"Alias {alias} must be present in SKILL_ALIASES")

        # Role aliases
        for role_alias in ["growth-lead", "growth-engineer", "media-buyer", "affiliate-marketer"]:
            self.assertIn(f'"{role_alias}":', text, f"Role alias {role_alias} must be present in ROLE_ALIASES")


class TestMMOContractSchemasAndPayloads(unittest.TestCase):
    """Challenge 6: Verify contract schemas mmo-campaign-spec.json and mmo-roi-report.json."""

    def test_schemas_exist_and_validate(self):
        for schema_file in ["mmo-campaign-spec.json", "mmo-roi-report.json"]:
            path = SCHEMAS_DIR / schema_file
            self.assertTrue(path.exists(), f"Schema {schema_file} must exist")
            with open(path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            Draft202012Validator.check_schema(schema)
            # Verify examples validate against the schema
            examples = schema.get("examples", [])
            self.assertGreater(len(examples), 0, f"Schema {schema_file} must bundle examples")
            validator = Draft202012Validator(schema)
            for i, example in enumerate(examples):
                errors = list(validator.iter_errors(example))
                self.assertEqual(len(errors), 0, f"Example {i} in {schema_file} failed validation: {errors}")


class TestMMOResearchPersistence(unittest.TestCase):
    """Challenge 7: Verify existence and comprehensive depth of 100-round deep research artifact."""

    def test_research_artifact_exists_and_detailed(self):
        self.assertTrue(RESEARCH_DOC.exists(), "mmo_2027_100_rounds_deep_research.md must exist")
        text = RESEARCH_DOC.read_text(encoding="utf-8")
        self.assertGreater(len(text), 10000, "Research document must be comprehensive (>10000 chars)")
        self.assertIn("100", text)
        self.assertIn("Cluster 1", text)
        self.assertIn("Cluster 2", text)
        self.assertIn("Cluster 3", text)
        self.assertIn("Cluster 4", text)
        self.assertIn("Cluster 5", text)


if __name__ == "__main__":
    unittest.main()
