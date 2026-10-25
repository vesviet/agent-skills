#!/usr/bin/env python3
"""Challenge tests for the 2026-10 AWS Engineer modernization round.

Guards the verified 2026-10-25 AWS baseline:
- Silicon: Graviton5 (c9g/m9g/r9g — all GA by 2026-08) is the default generation;
  Trainium3 (trn3) UltraServers GA 2025-12 (4.4x Trn2); previous-generation
  defaults (Graviton4-first, Trainium2) require documented exceptions.
- Toolchain: OpenTofu v1.13+ (current 1.13.2, 2026-10-21), Crossplane v2.4+
  (namespaced Composite Resources; Claims deprecated since 2.0, Aug 2025).
- Compute: EKS Auto Mode (managed Karpenter) is the default for new clusters.
- Services: Bedrock AgentCore GA 2025-10, Nova 2 ARN scoping, Aurora DSQL GA
  2025-05, Database Savings Plans (up to 35%).
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_FILE = REPO_ROOT / "core" / "roles" / "aws-engineer.md"
CHECKLIST_FILE = REPO_ROOT / "core" / "roles" / "references" / "aws-engineer-review-checklist.md"
SKILL_FILE = REPO_ROOT / "core" / "skills" / "platform" / "aws-infrastructure" / "SKILL.md"


def read(path: Path) -> str:
    assert path.exists(), f"{path} must exist"
    return path.read_text(encoding="utf-8")


def frontmatter_version(path: Path) -> str | None:
    match = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', read(path), re.MULTILINE)
    return match.group(1) if match else None


class TestSiliconCurrency(unittest.TestCase):
    """Graviton5 and Trainium3 are the default generations; previous-gen needs exceptions."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.skill = read(SKILL_FILE)
        cls.checklist = read(CHECKLIST_FILE)

    def test_01_graviton5_first_lock(self):
        self.assertIn("GRAVITON5-FIRST-LOCK", self.role)
        self.assertIn("c9g, m9g, r9g", self.role)
        self.assertIn("GRAVITON5-FIRST-LOCK", self.skill)
        self.assertNotIn("GRAVITON4-FIRST-LOCK", self.role)
        self.assertNotIn("GRAVITON4-FIRST-LOCK", self.skill)

    def test_02_graviton4_only_as_fallback(self):
        self.assertIn("standardize on Graviton5-first compute", self.role)
        # Graviton4 may appear only inside explicit regional-availability fallback clauses
        for line in self.role.splitlines():
            if "Graviton4" in line:
                self.assertRegex(
                    line,
                    r"(not yet available|only where|permitted only|faster than|previous-generation|Graviton5)",
                    f"Graviton4 mention outside fallback framing: {line.strip()[:100]}",
                )

    def test_03_trainium3_current(self):
        self.assertIn("Trainium3 (trn3)", self.role)
        self.assertIn("4.4x", self.role)
        for text in (self.role, self.skill, self.checklist):
            self.assertNotIn("Trainium2 (trn2)", text)

    def test_04_inferentia2_kept_for_inference(self):
        self.assertIn("Inferentia2 (inf2)", self.role)


class TestToolchainCurrency(unittest.TestCase):
    """OpenTofu v1.13+ and Crossplane v2.4+ (namespaced XRs, Claims deprecated)."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.skill = read(SKILL_FILE)
        cls.checklist = read(CHECKLIST_FILE)

    def test_01_opentofu_113(self):
        for text in (self.role, self.skill, self.checklist):
            self.assertIn("OpenTofu v1.13+", text)
            self.assertNotIn("OpenTofu v1.8", text)

    def test_02_crossplane_24(self):
        for text in (self.role, self.skill, self.checklist):
            self.assertIn("Crossplane v2.4+", text)
            self.assertNotIn("Crossplane v1.16", text)

    def test_03_crossplane_claims_deprecated(self):
        self.assertIn("namespaced Composite Resources", self.role)
        self.assertIn("Claim type is deprecated", self.role)
        self.assertIn("Claim type is deprecated", self.checklist)

    def test_04_karpenter_v1x_not_v10(self):
        for text in (self.role, self.skill, self.checklist):
            self.assertNotIn("Karpenter v1.0+", text)


class TestEksAutoModeAndServices(unittest.TestCase):
    """EKS Auto Mode default, AgentCore, Nova 2, Aurora DSQL, Database Savings Plans."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.checklist = read(CHECKLIST_FILE)

    def test_01_eks_auto_mode_default(self):
        self.assertIn("EKS Auto Mode", self.role)
        self.assertIn("default new clusters to EKS Auto Mode", self.role)
        self.assertIn("EKS Auto Mode", read(SKILL_FILE))

    def test_02_checklist_yaml_uses_graviton5_families(self):
        self.assertIn('"c9g", "m9g", "r9g"', self.checklist)
        self.assertNotIn('"c8g", "m8g", "r8g"', self.checklist)

    def test_03_bedrock_agentcore(self):
        self.assertIn("Bedrock AgentCore (GA since 2025-10)", self.role)
        self.assertIn("8-hour", self.role)

    def test_04_nova_2_arn_scoping(self):
        self.assertIn("Nova 2", self.role)

    def test_05_aurora_dsql(self):
        self.assertIn("Amazon Aurora DSQL (GA since 2025-05)", self.role)
        self.assertIn("Aurora DSQL (GA since 2025-05", self.checklist)

    def test_06_database_savings_plans(self):
        self.assertIn("Database Savings Plans", self.role)
        self.assertIn("Database Savings Plans", self.checklist)

    def test_07_aws_currency_lock(self):
        self.assertIn("AWS-CURRENCY-LOCK", self.role)
        self.assertIn("re-validate the baseline quarterly", self.role)


class TestSkillVersionAndASITitles(unittest.TestCase):
    """aws-infrastructure skill is versioned with official OWASP ASI titles."""

    def test_01_skill_version(self):
        self.assertEqual(frontmatter_version(SKILL_FILE), "2.0.0")

    def test_02_official_asi_titles(self):
        text = read(SKILL_FILE)
        for title in (
            "ASI04 Agentic Supply Chain",
            "ASI05 Unexpected Code Execution",
            "ASI07 Insecure Inter-Agent Communication",
        ):
            self.assertIn(title, text, f"aws-infrastructure must use official title: {title}")
        for invented in ("ASI04 Supply Chain", "ASI05 RCE Guard", "ASI07 Inter-Agent Communication"):
            self.assertNotIn(invented, text, f"aws-infrastructure must not use invented title: {invented}")


class TestModernizationGatesAndFooter(unittest.TestCase):
    """Checklist gains the 2026-10 gates; role footer records the round."""

    def test_01_gates_section(self):
        checklist = read(CHECKLIST_FILE)
        self.assertIn("### 16. 2026-10 Modernization Gates", checklist)
        for gate in (
            "Silicon-Currency Gate",
            "Crossplane-2.x Gate",
            "OpenTofu-1.13 Gate",
            "Auto-Mode-Aware Autoscaling Gate",
            "Bedrock-AgentCore Gate",
            "Aurora-DSQL Gate",
        ):
            self.assertIn(gate, checklist)

    def test_02_no_stale_checklist_headers(self):
        checklist = read(CHECKLIST_FILE)
        self.assertNotIn("Graviton4-First Compute Standard", checklist)
        self.assertNotIn("### 7. Graviton4", checklist)

    def test_03_role_domains_count(self):
        role = read(ROLE_FILE)
        self.assertIn("all 16 architectural domains", role)

    def test_04_footer_date(self):
        lines = [line.strip() for line in read(ROLE_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-25")


if __name__ == "__main__":
    unittest.main()
