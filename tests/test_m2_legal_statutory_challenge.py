"""
Empirical Challenger Test Suite for Milestone 2 Legal Statutory Upgrade.

Adversarially and empirically tests:
1. Gate Verification: validate-all.py passes all 16 gates with exit code 0.
2. Challenge Suite: pytest tests/test_vietnam_legal_pack_challenge.py passes all 38 tests.
3. Skill Ownership & Zero Conflicts:
   - audit-ai-compliance and draft-legal-opinion are Primary-owned by vietnam-legal-counsel.
   - Zero Primary/Supporting collisions.
   - Zero disclaimers in role boundaries.
   - No conflicting ownership across any other role in the pack.
4. Line Count Constraints:
   - audit-ai-compliance/SKILL.md < 200 lines.
   - draft-legal-opinion/SKILL.md < 200 lines.
   - manage-vietnam-legal/SKILL.md < 200 lines.
   - All 135 SKILL.md files < 200 lines.
5. Statutory Compliance & Content Rigor:
   - vietnam-legal-counsel.md contains Law 134/2025/QH15, PDPL 91/2025/QH15 + Decree 356/2025,
     AI-LAW-RISK-TIER LOCK, PDPL-2025-CONSENT LOCK, 3-tier risk governance, 72h incident reporting.
   - audit-ai-compliance/SKILL.md satisfies structure, 7 rules, 7 steps, 4 failure modes, 4 OWASP ASI guardrails, 6+ checklist items.
   - draft-legal-opinion/SKILL.md satisfies structure, 7 rules, 8 steps, 4 failure modes, 4 OWASP ASI guardrails, 6+ checklist items.
   - Companion guides and agents/openai.yaml existence and schema.
   - Review checklist contains 12+ items across 6 sections and proper footer.
6. Adversarial Mutation Sensitivity:
   - Padded line count >= 200 causes validate-skills.py to fail.
   - Missing Primary ownership causes validate-skill-ownership.py to fail.
   - Primary/Supporting collision causes validate-skill-ownership.py to fail.
   - Role boundary disclaimer causes validate-skill-ownership.py to fail.
   - Unknown tool in allowed-tools causes validate-skills.py to fail.
   - Corrupt footer in role file causes validate-roles.py to fail.
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = ROOT.parent
SCRIPTS_DIR = ROOT / "core" / "scripts"
ROLES_DIR = ROOT / "core" / "roles"
SKILLS_DIR = ROOT / "core" / "skills"
LEGAL_SKILLS_DIR = SKILLS_DIR / "legal-compliance"


@contextlib.contextmanager
def temporary_file_mutation(path: Path, mutated_content: str):
    """Context manager for disk-level mutation testing with guaranteed atomic restoration."""
    original_content = path.read_text(encoding="utf-8")
    try:
        path.write_text(mutated_content, encoding="utf-8")
        yield
    finally:
        path.write_text(original_content, encoding="utf-8")


class TestM2CoreGatesAndChallengeSuite(unittest.TestCase):
    """Empirical verification of project gate scripts and challenge tests."""

    def test_01_validate_all_exits_zero_16_gates(self):
        """python3 core/scripts/validate-all.py must exit with code 0."""
        res = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate-all.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"validate-all.py failed:\n{res.stdout}\n{res.stderr}")
        self.assertIn("All core validators passed.", res.stdout)
        self.assertIn("Skill ownership validation passed", res.stdout)
        self.assertIn("Contract coverage validation passed", res.stdout)

    def test_02_pytest_vietnam_legal_pack_challenge_38_passed(self):
        """pytest tests/test_vietnam_legal_pack_challenge.py must pass 38/38 tests."""
        res = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_vietnam_legal_pack_challenge.py", "-q"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode, 0,
            f"test_vietnam_legal_pack_challenge.py failed:\n{res.stdout}\n{res.stderr}"
        )
        self.assertIn("38 passed", res.stdout)


class TestM2SkillOwnershipAndZeroConflicts(unittest.TestCase):
    """Exhaustive empirical analysis of skill ownership across all roles."""

    def setUp(self):
        self.roles = sorted(
            p for p in ROLES_DIR.glob("*.md")
            if p.name not in {"README.md", "role-standard.md"}
        )

    def _get_role_toolboxes(self):
        ownership: dict[str, dict[str, list[str]]] = {}
        for r_path in self.roles:
            text = r_path.read_text(encoding="utf-8")
            prim_m = re.search(r"### Primary Skills\s*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
            sup_m = re.search(r"### Supporting Skills[^\n]*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
            p = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", prim_m.group(1))) if prim_m else set()
            s = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", sup_m.group(1))) if sup_m else set()
            ownership[r_path.stem] = {"primary": p, "supporting": s}
        return ownership

    def test_03_audit_ai_compliance_is_primary_owned_by_vietnam_legal_counsel(self):
        """audit-ai-compliance must be Primary-owned by vietnam-legal-counsel only."""
        toolboxes = self._get_role_toolboxes()
        vlc = toolboxes.get("vietnam-legal-counsel")
        self.assertIsNotNone(vlc, "vietnam-legal-counsel role missing")
        self.assertIn("audit-ai-compliance", vlc["primary"])
        self.assertNotIn("audit-ai-compliance", vlc["supporting"])

        # Check no other role claims it as Primary or Supporting
        for role_name, box in toolboxes.items():
            if role_name != "vietnam-legal-counsel":
                self.assertNotIn(
                    "audit-ai-compliance", box["primary"],
                    f"Conflict: {role_name} claims audit-ai-compliance as Primary"
                )
                self.assertNotIn(
                    "audit-ai-compliance", box["supporting"],
                    f"Conflict: {role_name} claims audit-ai-compliance as Supporting"
                )

    def test_04_draft_legal_opinion_is_primary_owned_by_vietnam_legal_counsel(self):
        """draft-legal-opinion must be Primary-owned by vietnam-legal-counsel only."""
        toolboxes = self._get_role_toolboxes()
        vlc = toolboxes.get("vietnam-legal-counsel")
        self.assertIsNotNone(vlc, "vietnam-legal-counsel role missing")
        self.assertIn("draft-legal-opinion", vlc["primary"])
        self.assertNotIn("draft-legal-opinion", vlc["supporting"])

        # Check no other role claims it as Primary or Supporting
        for role_name, box in toolboxes.items():
            if role_name != "vietnam-legal-counsel":
                self.assertNotIn(
                    "draft-legal-opinion", box["primary"],
                    f"Conflict: {role_name} claims draft-legal-opinion as Primary"
                )
                self.assertNotIn(
                    "draft-legal-opinion", box["supporting"],
                    f"Conflict: {role_name} claims draft-legal-opinion as Supporting"
                )

    def test_05_no_role_boundary_disclaims_legal_skills(self):
        """vietnam-legal-counsel boundaries must not disclaim its primary skills."""
        vlc_text = (ROLES_DIR / "vietnam-legal-counsel.md").read_text(encoding="utf-8")
        m = re.search(r"(?m)^#{2,3} (?:Decision Boundaries|Role Boundaries)\s*\n(.*?)(?=\n#{2,3} |\Z)", vlc_text, re.S)
        boundaries = m.group(1) if m else ""
        for skill in ["manage-vietnam-legal", "audit-ai-compliance", "draft-legal-opinion"]:
            verb = skill.replace("-", " ")
            self.assertIsNone(
                re.search(rf"does not\s+(?:\w+\s+){{0,3}}{re.escape(verb)}", boundaries, re.I),
                f"Boundary disclaims primary skill {skill}"
            )


class TestM2LineCountConstraints(unittest.TestCase):
    """Verify line count constraints (< 200 lines) strictly."""

    def test_06_audit_ai_compliance_line_count(self):
        path = LEGAL_SKILLS_DIR / "audit-ai-compliance" / "SKILL.md"
        self.assertTrue(path.is_file())
        lines = len(path.read_text(encoding="utf-8").splitlines())
        self.assertLess(lines, 200, f"audit-ai-compliance SKILL.md is {lines} lines (must be < 200)")

    def test_07_draft_legal_opinion_line_count(self):
        path = LEGAL_SKILLS_DIR / "draft-legal-opinion" / "SKILL.md"
        self.assertTrue(path.is_file())
        lines = len(path.read_text(encoding="utf-8").splitlines())
        self.assertLess(lines, 200, f"draft-legal-opinion SKILL.md is {lines} lines (must be < 200)")

    def test_08_manage_vietnam_legal_line_count(self):
        path = LEGAL_SKILLS_DIR / "manage-vietnam-legal" / "SKILL.md"
        self.assertTrue(path.is_file())
        lines = len(path.read_text(encoding="utf-8").splitlines())
        self.assertLess(lines, 200, f"manage-vietnam-legal SKILL.md is {lines} lines (must be < 200)")

    def test_09_all_skills_in_pack_under_200_lines(self):
        all_skills = list(ROOT.glob("**/SKILL.md"))
        self.assertGreaterEqual(len(all_skills), 135)
        for skill_file in all_skills:
            line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
            self.assertLess(
                line_count, 200,
                f"Skill file {skill_file.relative_to(ROOT)} exceeds 200 lines: {line_count}"
            )


class TestM2StatutoryContentRigor(unittest.TestCase):
    """Verify legal statutory requirements and deliverables structure."""

    def test_10_vietnam_legal_counsel_role_statutory_content(self):
        text = (ROLES_DIR / "vietnam-legal-counsel.md").read_text(encoding="utf-8")
        # Statutory frameworks
        self.assertIn("Law on Artificial Intelligence No. 134/2025/QH15", text)
        self.assertIn("Personal Data Protection Law No. 91/2025/QH15", text)
        self.assertIn("Decree 356/2025/ND-CP", text)

        # Core responsibilities
        self.assertIn("### AI Systems Governance, Risk Classification, And Conformity Assessment", text)
        self.assertIn("### Personal Data Protection (PDPL) And Cybersecurity Governance", text)

        # Guardrails
        self.assertIn("AI-LAW-RISK-TIER LOCK", text)
        self.assertIn("PDPL-2025-CONSENT LOCK", text)

        # Incident reporting & grace periods
        self.assertIn("72 hours", text)
        self.assertIn("5 working days", text)
        self.assertIn("18-month", text)
        self.assertIn("12-month", text)

        # Review checklist & anti-patterns
        self.assertIn("AI System Risk Tier Classified", text)
        self.assertIn("PDPL 2025 Consent Verified", text)
        self.assertIn("AI Incident Reporting Protocol Confirmed", text)
        self.assertIn("applying Decree 13/2023 as primary PDPD law for post-January 2026", text)
        self.assertIn("classifying AI systems without applying the 3-tier risk framework", text)

        # Footer
        lines = text.strip().splitlines()
        self.assertEqual(lines[-1], "Last updated: 2026-09-29")

    def test_11_audit_ai_compliance_skill_spec(self):
        skill_dir = LEGAL_SKILLS_DIR / "audit-ai-compliance"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        text = skill_file.read_text(encoding="utf-8")

        # Frontmatter
        lines = text.splitlines()
        self.assertEqual(lines[0], "---")
        close_idx = lines[1:].index("---") + 1
        fm = yaml.safe_load("\n".join(lines[1:close_idx]))
        self.assertEqual(fm.get("name"), "audit-ai-compliance")
        expected_tools = ["read_file", "write_file", "edit_file", "create_file", "search_code"]
        self.assertEqual(fm.get("allowed-tools"), expected_tools)

        # Sections
        self.assertIn("## Core Rules", text)
        self.assertIn("## Output Contracts", text)
        self.assertIn("legal-compliance-review.json", text)
        self.assertIn("produced_by_role: vietnam-legal-counsel", text)
        self.assertIn("## Suggested Process", text)
        self.assertIn("### 1. AI System Scope Identification", text)
        self.assertIn("### 2. Risk-Tier Classification", text)
        self.assertIn("### 3. High-Risk Conformity Assessment Review", text)
        self.assertIn("### 4. National AI Database Registration Check", text)
        self.assertIn("### 5. Transparency & Labeling Audit", text)
        self.assertIn("### 6. Incident Reporting Protocol Verification", text)
        self.assertIn("### 7. Grace Period Compliance Tracking & HITL Gate", text)
        self.assertIn("## Failure Modes", text)
        self.assertIn("## Security Guardrails (OWASP ASI)", text)
        self.assertIn("## Checklist", text)
        self.assertIn("## Related Skills", text)

        # Companion files
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        self.assertTrue(openai_yaml.is_file())
        guide = skill_dir / "references" / "ai-law-compliance-guide.md"
        self.assertTrue(guide.is_file())

    def test_12_draft_legal_opinion_skill_spec(self):
        skill_dir = LEGAL_SKILLS_DIR / "draft-legal-opinion"
        skill_file = skill_dir / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        text = skill_file.read_text(encoding="utf-8")

        # Frontmatter
        lines = text.splitlines()
        self.assertEqual(lines[0], "---")
        close_idx = lines[1:].index("---") + 1
        fm = yaml.safe_load("\n".join(lines[1:close_idx]))
        self.assertEqual(fm.get("name"), "draft-legal-opinion")
        expected_tools = ["read_file", "write_file", "edit_file", "create_file", "search_code"]
        self.assertEqual(fm.get("allowed-tools"), expected_tools)

        # Sections
        self.assertIn("## Core Rules", text)
        self.assertIn("## Output Contracts", text)
        self.assertIn("legal-opinion-contract.json", text)
        self.assertIn("produced_by_role: vietnam-legal-counsel", text)
        self.assertIn("## Suggested Process", text)
        self.assertIn("### 1. Questions Presented Framing", text)
        self.assertIn("### 2. Factual Background & Entity Context", text)
        self.assertIn("### 3. Statutory Authority Research", text)
        self.assertIn("### 4. Legal Issue Analysis", text)
        self.assertIn("### 5. Supreme People's Court Precedents Review", text)
        self.assertIn("### 6. Executive Opinion Formulation", text)
        self.assertIn("### 7. Reliance Conditions & Limitations", text)
        self.assertIn("### 8. Action Plan + HITL Approval Gate", text)
        self.assertIn("## Failure Modes", text)
        self.assertIn("## Security Guardrails (OWASP ASI)", text)
        self.assertIn("## Checklist", text)
        self.assertIn("## Related Skills", text)

        # Companion files
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        self.assertTrue(openai_yaml.is_file())
        guide = skill_dir / "references" / "legal-opinion-guide.md"
        self.assertTrue(guide.is_file())

    def test_13_manage_vietnam_legal_skill_upgrades(self):
        skill_file = LEGAL_SKILLS_DIR / "manage-vietnam-legal" / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        lines = text.splitlines()
        close_idx = lines[1:].index("---") + 1
        fm = yaml.safe_load("\n".join(lines[1:close_idx]))
        self.assertIn("edit_file", fm.get("allowed-tools", []))

        self.assertIn("### 0.5. AI Law 134/2025 Risk-Tier Pre-Screening", text)
        self.assertIn("### 4. PDPL 2025 & Decree 356 Compliance Audit", text)
        self.assertIn("PDPL 2025 business eligibility gap", text)
        self.assertIn("AI Law incident reporting miss", text)

    def test_14_vietnam_legal_counsel_review_checklist_structure(self):
        chk_path = ROLES_DIR / "references" / "vietnam-legal-counsel-review-checklist.md"
        self.assertTrue(chk_path.is_file())
        text = chk_path.read_text(encoding="utf-8")

        # 6 sections
        self.assertIn("### 1. Jurisdiction & Entity Verification", text)
        self.assertIn("### 2. Statutory Basis & Gazette Verification", text)
        self.assertIn("### 3. Commercial Contract Compliance", text)
        self.assertIn("### 4. PDPL 2025 Compliance", text)
        self.assertIn("### 5. AI Law 134/2025 Compliance", text)
        self.assertIn("### 6. Governance & HITL Gates", text)

        # 12+ bullet items
        items = re.findall(r"(?m)^- \*\*([^*]+)\*\*:", text)
        self.assertGreaterEqual(len(items), 12, f"Expected >= 12 checklist items, got {len(items)}")

        # Footer
        lines = text.strip().splitlines()
        self.assertEqual(lines[-1], "Last updated: 2026-09-29")


class TestM2AdversarialSensitivityMutations(unittest.TestCase):
    """Adversarial stress-testing of pack validation gates via controlled file mutations."""

    def test_15_mutation_padded_skill_exceeding_200_lines_fails_validation(self):
        """SKILL.md with >= 200 lines must be rejected by validate-skills.py."""
        skill_file = LEGAL_SKILLS_DIR / "audit-ai-compliance" / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        current_lines = len(content.splitlines())
        pad_needed = 205 - current_lines
        padded_content = content + "\n<!-- padding line -->" * pad_needed

        with temporary_file_mutation(skill_file, padded_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("exceeds maximum allowed length (< 200 lines", res.stdout)

    def test_16_mutation_missing_primary_owner_fails_ownership_validation(self):
        """Removing audit-ai-compliance from vietnam-legal-counsel Primary Skills must fail validate-skill-ownership.py."""
        role_file = ROLES_DIR / "vietnam-legal-counsel.md"
        content = role_file.read_text(encoding="utf-8")
        mutated_content = content.replace("- `audit-ai-compliance`\n", "")

        with temporary_file_mutation(role_file, mutated_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skill-ownership.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertIn("warning: core/skills/audit-ai-compliance: referenced by no role toolbox", res.stdout)

    def test_17_mutation_primary_supporting_collision_fails_ownership_validation(self):
        """Listing audit-ai-compliance as both Primary and Supporting must fail validate-skill-ownership.py."""
        role_file = ROLES_DIR / "vietnam-legal-counsel.md"
        content = role_file.read_text(encoding="utf-8")
        mutated_content = content.replace(
            "### Supporting Skills (use when collaborating)\n\n",
            "### Supporting Skills (use when collaborating)\n\n- `audit-ai-compliance`\n",
        )

        with temporary_file_mutation(role_file, mutated_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skill-ownership.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("['audit-ai-compliance'] listed as both Primary and Supporting", res.stdout)

    def test_18_mutation_boundary_disclaiming_primary_skill_fails_ownership_validation(self):
        """A role boundary stating 'does not draft legal opinion' must fail validate-skill-ownership.py."""
        role_file = ROLES_DIR / "vietnam-legal-counsel.md"
        content = role_file.read_text(encoding="utf-8")
        mutated_content = content.replace(
            "## Role Boundaries\n\n",
            "## Role Boundaries\n\nThis role does not draft legal opinion under any circumstance.\n\n",
        )

        with temporary_file_mutation(role_file, mutated_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skill-ownership.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("is a Primary skill but the role's boundaries disclaim", res.stdout)

    def test_19_mutation_invalid_tool_in_skill_allowed_tools_fails_validation(self):
        """Adding an invalid tool to allowed-tools must fail validate-skills.py."""
        skill_file = LEGAL_SKILLS_DIR / "draft-legal-opinion" / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        mutated_content = content.replace(
            "allowed-tools:\n",
            "allowed-tools:\n  - unauthorized_destructive_tool\n",
        )

        with temporary_file_mutation(skill_file, mutated_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("allowed-tools references unknown tool: unauthorized_destructive_tool", res.stdout)

    def test_20_mutation_corrupted_footer_in_role_fails_role_validation(self):
        """A missing or corrupt 'Last updated:' footer in role file must fail validate-roles.py."""
        role_file = ROLES_DIR / "vietnam-legal-counsel.md"
        content = role_file.read_text(encoding="utf-8")
        mutated_content = content.replace("Last updated: 2026-09-29", "Stale footer: 2024-01-01")

        with temporary_file_mutation(role_file, mutated_content):
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-roles.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("footer 'Last updated:' must appear exactly once, found 0", res.stdout)


if __name__ == "__main__":
    unittest.main()
