"""
Empirical Challenger Test Suite for Milestone 1 Baseline Validation Fixes.

Empirically and adversarially tests the 5 baseline fixes applied in Milestone 1:
1. core/rules/code.md and AGENTS.md rule text and approval_gates parity group.
2. core/skills/mmo/setup-tracking-system/SKILL.md allowed-tools validation and peer parity.
3. core/roles/data-engineer.md backtick removal and regex reference validation.
4. core/roles/data-analyst.md section header typo fix.
5. End-to-end sensitivity of validate-all.py, validate-rules.py, validate-skills.py, and validate-roles.py.
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = ROOT.parent
SCRIPTS_DIR = ROOT / "core" / "scripts"


@contextlib.contextmanager
def temporary_file_mutation(path: Path, mutated_content: str):
    """Context manager for disk-level mutation testing with guaranteed atomic restoration."""
    original_content = path.read_text(encoding="utf-8")
    try:
        path.write_text(mutated_content, encoding="utf-8")
        yield
    finally:
        path.write_text(original_content, encoding="utf-8")


class TestBaselineInvariants(unittest.TestCase):
    """Verify that all 5 baseline fixes are present, uncorrupted, and conformant."""

    def test_01_code_md_has_approval_gate_rule(self):
        code_md = ROOT / "core" / "rules" / "code.md"
        self.assertTrue(code_md.exists(), "core/rules/code.md must exist")
        content = code_md.read_text(encoding="utf-8")
        required = (
            "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit"
        )
        self.assertIn(required, content)

    def test_02_agents_md_has_approval_gate_rule(self):
        agent_skills_agents = ROOT / "AGENTS.md"
        workspace_agents = WORKSPACE_ROOT / "AGENTS.md"

        self.assertTrue(agent_skills_agents.exists(), "agent-skills/AGENTS.md must exist")
        self.assertTrue(workspace_agents.exists(), "/home/user/personalized/AGENTS.md must exist")

        required = (
            "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit"
        )
        self.assertIn(required, agent_skills_agents.read_text(encoding="utf-8"))
        self.assertIn(required, workspace_agents.read_text(encoding="utf-8"))

    def test_03_mmo_setup_tracking_system_has_valid_tool(self):
        skill_file = ROOT / "core" / "skills" / "mmo" / "setup-tracking-system" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "setup-tracking-system/SKILL.md must exist")
        content = skill_file.read_text(encoding="utf-8")

        self.assertNotIn("run_database", content)
        self.assertIn("execute_command", content)

    def test_04_mmo_index_json_sync(self):
        index_json = ROOT / "core" / "skills" / "mmo" / "INDEX.json"
        self.assertTrue(index_json.exists(), "core/skills/mmo/INDEX.json must exist")
        data = json.loads(index_json.read_text(encoding="utf-8"))

        skills = {s["name"]: s for s in data.get("skills", [])}
        self.assertIn("setup-tracking-system", skills)
        tools = skills["setup-tracking-system"].get("allowed-tools", [])
        self.assertNotIn("run_database", tools)
        self.assertIn("execute_command", tools)

    def test_05_data_engineer_no_backticks(self):
        de_file = ROOT / "core" / "roles" / "data-engineer.md"
        self.assertTrue(de_file.exists(), "core/roles/data-engineer.md must exist")
        content = de_file.read_text(encoding="utf-8")

        self.assertNotIn("`string` blob", content)
        self.assertNotIn("`distributed` mode", content)
        self.assertIn("string blob", content)
        self.assertIn("distributed mode", content)

    def test_06_data_analyst_heading_correct(self):
        da_file = ROOT / "core" / "roles" / "data-analyst.md"
        self.assertTrue(da_file.exists(), "core/roles/data-analyst.md must exist")
        content = da_file.read_text(encoding="utf-8")

        self.assertNotIn("## Outputs Produed", content)
        self.assertIn("## Outputs Produced", content)

    def test_07_all_17_gates_pass(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate-all.py"), "--format", "json"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"validate-all failed: {proc.stderr}\n{proc.stdout}")
        data = json.loads(proc.stdout)
        self.assertTrue(data.get("passed"), "Overall passed must be True")
        self.assertEqual(data.get("failed"), 0, "No gates may fail")
        self.assertEqual(data.get("total"), 17, "Expected exactly 17 validation gates")


class TestAdversarialSensitivityRuleValidation(unittest.TestCase):
    """Adversarially test that validate-rules.py strictly rejects regressions in code.md and AGENTS.md."""

    def test_08_mutation_code_md_missing_rule(self):
        code_md = ROOT / "core" / "rules" / "code.md"
        orig = code_md.read_text(encoding="utf-8")
        required_phrase = (
            "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit."
        )
        mutated = orig.replace(required_phrase, "")
        self.assertNotEqual(orig, mutated, "Replacement must take effect")

        with temporary_file_mutation(code_md, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-rules.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-rules.py must fail when code.md lacks required rule")
            self.assertIn("core/rules/code.md missing required rule text", proc.stdout)

    def test_09_mutation_code_md_partial_corrupted_rule(self):
        code_md = ROOT / "core" / "rules" / "code.md"
        orig = code_md.read_text(encoding="utf-8")
        required_phrase = (
            "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit."
        )
        corrupted = orig.replace(
            required_phrase,
            "Ensure all code changes pass linters before commit.",
        )
        with temporary_file_mutation(code_md, corrupted):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-rules.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-rules.py must fail on inexact rule wording")
            self.assertIn("core/rules/code.md missing required rule text", proc.stdout)

    def test_10_mutation_agents_md_missing_group(self):
        agents_md = ROOT / "AGENTS.md"
        orig = agents_md.read_text(encoding="utf-8")
        target_line = (
            "- Ensure all code changes pass local linters, unit tests, and build checks before creating a commit."
        )
        mutated = orig.replace(target_line, "")
        with temporary_file_mutation(agents_md, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-rules.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-rules.py must fail when AGENTS.md lacks approval_gates")
            self.assertIn("missing adapter parity group 'approval_gates'", proc.stdout)

    def test_11_mutation_agents_md_forbidden_words(self):
        agents_md = ROOT / "AGENTS.md"
        orig = agents_md.read_text(encoding="utf-8")
        mutated = orig + "\n<!-- Internal thought process here -->\n"
        with temporary_file_mutation(agents_md, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-rules.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-rules.py must catch forbidden wording")
            self.assertIn("contains forbidden wording: thought process", proc.stdout)


class TestAdversarialSensitivityMMOToolValidation(unittest.TestCase):
    """Adversarially test that validate-skills.py rejects invalid tools in setup-tracking-system."""

    def test_12_mutation_mmo_skill_run_database(self):
        skill_file = ROOT / "core" / "skills" / "mmo" / "setup-tracking-system" / "SKILL.md"
        orig = skill_file.read_text(encoding="utf-8")
        mutated = orig.replace("execute_command", "run_database")

        with temporary_file_mutation(skill_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-skills.py must reject run_database")
            self.assertIn("allowed-tools references unknown tool: run_database", proc.stdout)

    def test_13_mutation_mmo_skill_run_command_adversarial_prompt_trap(self):
        """
        The user prompt hinted '(use run_command or search_code)'.
        We stress-test whether 'run_command' is actually an invalid unmapped tool.
        """
        skill_file = ROOT / "core" / "skills" / "mmo" / "setup-tracking-system" / "SKILL.md"
        orig = skill_file.read_text(encoding="utf-8")
        mutated = orig.replace("execute_command", "run_command")

        with temporary_file_mutation(skill_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                proc.returncode,
                1,
                "validate-skills.py must reject run_command because it is not mapped in mcp-tool-map.yaml",
            )
            self.assertIn("allowed-tools references unknown tool: run_command", proc.stdout)

    def test_14_mmo_peer_parity_check(self):
        mmo_dir = ROOT / "core" / "skills" / "mmo"
        expected_tools = [
            "read_file",
            "write_file",
            "edit_file",
            "create_file",
            "search_code",
            "run_tests",
            "run_linter",
            "run_build",
            "execute_command",
        ]
        for skill_dir in mmo_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            text = skill_md.read_text(encoding="utf-8")
            for t in expected_tools:
                self.assertIn(t, text, f"Skill {skill_dir.name} missing tool {t}")


class TestAdversarialSensitivityDataRoles(unittest.TestCase):
    """Adversarially test sensitivity of role reference and structure validation."""

    def test_15_mutation_data_engineer_backtick_string(self):
        de_file = ROOT / "core" / "roles" / "data-engineer.md"
        orig = de_file.read_text(encoding="utf-8")
        mutated = orig.replace("string blob", "`string` blob", 1)

        with temporary_file_mutation(de_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-skills.py must fail on backticked string")
            self.assertIn("unknown referenced skill or local doc: string", proc.stdout)

    def test_16_mutation_data_engineer_backtick_distributed(self):
        de_file = ROOT / "core" / "roles" / "data-engineer.md"
        orig = de_file.read_text(encoding="utf-8")
        mutated = orig.replace("distributed mode", "`distributed` mode", 1)

        with temporary_file_mutation(de_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-skills.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-skills.py must fail on backticked distributed")
            self.assertIn("unknown referenced skill or local doc: distributed", proc.stdout)

    def test_17_mutation_data_analyst_typo_heading(self):
        da_file = ROOT / "core" / "roles" / "data-analyst.md"
        orig = da_file.read_text(encoding="utf-8")
        mutated = orig.replace("## Outputs Produced", "## Outputs Produed", 1)

        with temporary_file_mutation(da_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-roles.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-roles.py must fail on heading typo")
            self.assertIn("missing required section: ## Outputs Produced", proc.stdout)

    def test_18_mutation_data_analyst_missing_outputs_produced(self):
        da_file = ROOT / "core" / "roles" / "data-analyst.md"
        orig = da_file.read_text(encoding="utf-8")
        mutated = orig.replace("## Outputs Produced\n\n- `contracts/schemas/data-analysis-report.json`", "")

        with temporary_file_mutation(da_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-roles.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertIn("missing required section: ## Outputs Produced", proc.stdout)


class TestEndToEndSubprocessAllGatesFailOnRegression(unittest.TestCase):
    """Verify that validate-all.py detects and fails on any single regression."""

    def test_19_validate_all_fails_on_rule_regression(self):
        code_md = ROOT / "core" / "rules" / "code.md"
        orig = code_md.read_text(encoding="utf-8")
        required_phrase = (
            "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit."
        )
        mutated = orig.replace(required_phrase, "")

        with temporary_file_mutation(code_md, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-all.py"), "--format", "json"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-all.py must exit with code 1")
            data = json.loads(proc.stdout)
            self.assertFalse(data.get("passed"))
            self.assertGreaterEqual(data.get("failed"), 1)

    def test_20_validate_all_fails_on_skill_regression(self):
        skill_file = ROOT / "core" / "skills" / "mmo" / "setup-tracking-system" / "SKILL.md"
        orig = skill_file.read_text(encoding="utf-8")
        mutated = orig.replace("execute_command", "run_database")

        with temporary_file_mutation(skill_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-all.py"), "--format", "json"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-all.py must exit with code 1")
            data = json.loads(proc.stdout)
            self.assertFalse(data.get("passed"))
            self.assertGreaterEqual(data.get("failed"), 1)

    def test_21_validate_all_fails_on_role_regression(self):
        da_file = ROOT / "core" / "roles" / "data-analyst.md"
        orig = da_file.read_text(encoding="utf-8")
        mutated = orig.replace("## Outputs Produced", "## Outputs Produed")

        with temporary_file_mutation(da_file, mutated):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-all.py"), "--format", "json"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, "validate-all.py must exit with code 1")
            data = json.loads(proc.stdout)
            self.assertFalse(data.get("passed"))
            self.assertGreaterEqual(data.get("failed"), 1)


if __name__ == "__main__":
    unittest.main()
