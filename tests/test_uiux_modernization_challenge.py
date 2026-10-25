"""
Challenge suite for the 2026-10 UI/UX Designer modernization (5.7.0 candidate).

Verifies: ux-flow-spec agentic_autonomy/agent_operability/dark_pattern_review
fields, DTCG 2025.10 pinning across role + skills + token schema, ADA Title II
(2026-04 extension) compliance locks, dark-pattern regulatory locks,
Agents-as-Users dual-audience operability, and AI-era usability research
validity rules.
"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE = ROOT / "core" / "roles" / "ui-ux-designer.md"
UX_FLOW_SCHEMA = ROOT / "core" / "contracts" / "schemas" / "ux-flow-spec.json"
TOKENS_SCHEMA = ROOT / "core" / "contracts" / "schemas" / "design-tokens-spec.json"

PRIMARY_SKILLS = (
    "core/skills/foundation/design-ux-flow/SKILL.md",
    "core/skills/foundation/design-review/SKILL.md",
    "core/skills/frontend/design-system-engineering/SKILL.md",
    "core/skills/frontend/anti-ui-slop-finish-gate/SKILL.md",
    "core/skills/document/pptx/SKILL.md",
    "core/skills/frontend/design-md-specification/SKILL.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestUxFlowSchemaModernization(unittest.TestCase):
    """The AUTONOMY-TIER LOCK requires schema fields that must actually exist."""

    def setUp(self):
        self.schema = json.loads(read(UX_FLOW_SCHEMA))

    def test_01_agentic_autonomy_autonomy_tier_exists(self):
        props = self.schema["properties"]
        self.assertIn("agentic_autonomy", props)
        tier = props["agentic_autonomy"]["properties"]["autonomy_tier"]
        self.assertEqual(
            tier["enum"], ["Suggest", "Verify", "Delegate", "Automate"]
        )
        self.assertIn("autonomy_tier", props["agentic_autonomy"]["required"])

    def test_02_agentic_autonomy_supporting_fields(self):
        props = props = self.schema["properties"]["agentic_autonomy"]["properties"]
        for field in ("tier_indicator", "tier_upgrade_path", "background_agent_surfaces"):
            self.assertIn(field, props)

    def test_03_agent_operability_field_exists(self):
        props = self.schema["properties"]["agent_operability"]["properties"]
        for field in ("agent_entry_points", "machine_readable_affordances", "agent_courtesy_rules"):
            self.assertIn(field, props)

    def test_04_dark_pattern_review_field_exists(self):
        self.assertIn("dark_pattern_review", self.schema["properties"])


class TestTokensSchemaDtcgPin(unittest.TestCase):
    """Design tokens must pin the DTCG Format Module 2025.10 stable release."""

    def setUp(self):
        self.schema = json.loads(read(TOKENS_SCHEMA))

    def test_05_dtcg_format_field_pins_2025_10(self):
        dtcg = self.schema["properties"]["dtcg_format"]["properties"]
        self.assertEqual(dtcg["format_version"]["const"], "2025.10")
        for field in ("value_type_syntax", "interchange_validated"):
            self.assertIn(field, dtcg)


class TestRoleModernization(unittest.TestCase):
    """New 2026-10 locks and compliance facts in the ui-ux-designer role."""

    def setUp(self):
        self.role = read(ROLE)

    def test_06_new_locks_present(self):
        for lock in (
            "DTCG-FORMAT LOCK",
            "DARK-PATTERN-COMPLIANCE LOCK",
            "ADA-TITLE-II LOCK",
            "DUAL-AUDIENCE LOCK",
        ):
            self.assertIn(lock, self.role)

    def test_07_ada_title_ii_dates_reflect_2026_extension(self):
        self.assertIn("2027-04-26", self.role)
        self.assertIn("2028-04-26", self.role)
        self.assertIn("WCAG 2.1 AA", self.role)

    def test_08_wcag3_stays_watch_item_not_target(self):
        self.assertIn("WCAG 3.0 remains a W3C Working Draft", self.role)
        self.assertIn("WCAG 2.2 AA as the conformance target", self.role)

    def test_09_dark_pattern_is_regulatory_dimension(self):
        self.assertIn("DSA Art 25/26", self.role)
        self.assertIn("FTC", self.role)
        self.assertIn("dark_pattern_review", self.role)

    def test_10_synthetic_user_anti_pattern(self):
        self.assertIn("synthetic-user results as usability evidence", self.role)

    def test_11_agent_operability_in_role(self):
        self.assertIn("agent_operability", self.role)
        self.assertIn("Agents-as-Users", self.role)


class TestSkillsModernization(unittest.TestCase):
    """Primary skills carry the modernization and a version field."""

    def test_12_primary_skills_have_versions(self):
        for rel in PRIMARY_SKILLS:
            text = read(ROOT / rel)
            self.assertRegex(text, r"(?m)^version: [0-9]+\.[0-9]+\.[0-9]+$", rel)

    def test_13_design_system_engineering_pins_dtcg_2025_10(self):
        text = read(ROOT / "core/skills/frontend/design-system-engineering/SKILL.md")
        self.assertIn("Format Module 2025.10", text)
        self.assertIn("$value", text)
        self.assertIn("Terrazzo", text)

    def test_14_design_ux_flow_agents_as_users(self):
        text = read(ROOT / "core/skills/foundation/design-ux-flow/SKILL.md")
        self.assertIn("Agents-as-Users", text)
        self.assertIn("agent_operability", text)
        self.assertIn("dark_pattern_review", text)
        self.assertIn("2025.10", text)

    def test_15_design_review_research_validity(self):
        text = read(ROOT / "core/skills/foundation/design-review/SKILL.md")
        self.assertIn("Synthetic-user validity lock", text)
        self.assertIn("UMUX-Lite", text)
        self.assertIn("2025.10", text)

    def test_16_anti_slop_gate_dark_pattern_regulatory(self):
        text = read(ROOT / "core/skills/frontend/anti-ui-slop-finish-gate/SKILL.md")
        self.assertIn("DSA Art 25/26", text)
        self.assertIn("dark_pattern_review", text)


class TestReferenceChecklist(unittest.TestCase):
    def test_17_checklist_has_modernization_gates(self):
        text = read(ROOT / "core/roles/references/ui-ux-designer-review-checklist.md")
        self.assertIn("2026-10 Modernization Gates", text)
        self.assertIn("DTCG Format Conformance", text)
        self.assertIn("Agents-as-Users Operability", text)


if __name__ == "__main__":
    unittest.main()
