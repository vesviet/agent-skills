"""
Skill Content Regression Test Suite (P0 Quality Gate).

Verifies all 169 core skills against foundational invariants:
1. Valid YAML frontmatter (name, description, allowed-tools).
2. All referenced scripts physically exist on disk (zero phantom scripts).
3. All referenced companion files in references/ and examples/ resolve.
4. Core content quality standards (line bounds, H1 matching, required sections).
5. Zero hardcoded OS-specific absolute paths (cross-platform portability).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "core" / "skills"

SKILL_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
TOOL_NAME_RE = re.compile(r"^[a-z0-9_]{1,64}$")
WINDOWS_PATH_RE = re.compile(r"\b[A-Za-z]:\\[a-zA-Z0-9_\\.-]+")

REQUIRED_SECTIONS = [
    "## Core Rules",
    "## Suggested Process",
    "## Checklist",
    "## Related Skills",
]


def strip_fenced_blocks(text: str) -> str:
    """Remove fenced code blocks so code comments do not pollute markdown header checks."""
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


class TestSkillContentRegression(unittest.TestCase):
    """Programmatic quality gate for skill markdown files across core/skills."""

    @classmethod
    def setUpClass(cls):
        cls.skill_files = sorted(SKILLS_DIR.glob("*/*/SKILL.md"))
        cls.skill_names = {s.parent.name for s in cls.skill_files}

    def test_01_core_skills_inventory_count(self):
        """Must discover exactly 169 core skills across 22 categories."""
        self.assertEqual(
            len(self.skill_files),
            169,
            f"Expected exactly 169 core skills, discovered {len(self.skill_files)}",
        )

    def test_02_valid_yaml_frontmatter(self):
        """Every skill must contain valid YAML frontmatter with required keys."""
        for skill_path in self.skill_files:
            rel = skill_path.relative_to(REPO_ROOT)
            text = skill_path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{rel}: Must start with frontmatter '---'")

            parts = text.split("---\n", 2)
            self.assertGreaterEqual(len(parts), 3, f"{rel}: Malformed frontmatter delimiters")

            try:
                fm = yaml.safe_load(parts[1])
            except Exception as e:
                self.fail(f"{rel}: YAML parse error: {e}")

            self.assertIsInstance(fm, dict, f"{rel}: Frontmatter must be a dictionary")

            name = fm.get("name")
            self.assertTrue(name, f"{rel}: Missing 'name' in frontmatter")
            self.assertEqual(name, skill_path.parent.name, f"{rel}: Name mismatch with directory")
            self.assertTrue(SKILL_NAME_RE.fullmatch(name), f"{rel}: Invalid name format: {name}")

            desc = fm.get("description", "")
            self.assertTrue(desc, f"{rel}: Missing 'description' in frontmatter")
            self.assertLessEqual(len(desc), 1024, f"{rel}: Description exceeds 1024 characters")
            self.assertIn("Use when ", desc, f"{rel}: Description must contain 'Use when ' clause")
            self.assertFalse(desc.startswith(("I ", "You ")), f"{rel}: Description must be 3rd person")

            tools = fm.get("allowed-tools")
            self.assertIsInstance(tools, list, f"{rel}: 'allowed-tools' must be a list")
            self.assertGreater(len(tools), 0, f"{rel}: 'allowed-tools' cannot be empty")
            for t in tools:
                self.assertTrue(TOOL_NAME_RE.fullmatch(t), f"{rel}: Invalid tool name: {t}")

    def test_03_no_phantom_script_references(self):
        """All helper scripts referenced in SKILL.md must physically exist in scripts/."""
        phantom_errors = []

        for skill_path in self.skill_files:
            rel = skill_path.relative_to(REPO_ROOT)
            text = skill_path.read_text(encoding="utf-8")
            scripts_dir = skill_path.parent / "scripts"

            matches = re.findall(
                r"(?:Run|run|python|python3|via|execute)\s+`?([a-zA-Z0-9_-]+\.py)`?",
                text,
            )

            for script_name in matches:
                # Exclude root validator scripts or tool examples
                if (
                    script_name.startswith("validate-")
                    or script_name in {
                        "generate-index.py",
                        "generate-tier1-index.py",
                        "openrouter_worker.py",
                        "script.py",
                        "inspect_rig.py",
                    }
                ):
                    continue

                target_script = scripts_dir / script_name
                target_root = skill_path.parent / script_name

                if not target_script.exists() and not target_root.exists():
                    phantom_errors.append(f"{rel}: Phantom script '{script_name}' not found on disk")

        self.assertEqual(phantom_errors, [], "Discovered phantom script references in SKILL.md files")

    def test_04_no_broken_references_or_examples_links(self):
        """All relative markdown paths pointing to references/ or examples/ must resolve."""
        broken_links = []

        for skill_path in self.skill_files:
            rel = skill_path.relative_to(REPO_ROOT)
            text = skill_path.read_text(encoding="utf-8")

            clean_text = strip_fenced_blocks(text)

            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", clean_text)
            for _, target in links:
                if "references/" in target or "examples/" in target:
                    clean_target = target.split("#")[0].split("?")[0]
                    resolved = (skill_path.parent / clean_target).resolve()
                    if not resolved.exists():
                        broken_links.append(f"{rel}: Broken link '{target}' -> {resolved}")

            inline_refs = re.findall(r"`(references/[^`#?]+)`", clean_text) + re.findall(
                r"`(examples/[^`#?]+)`", clean_text
            )
            for p in inline_refs:
                resolved = (skill_path.parent / p).resolve()
                if not resolved.exists():
                    broken_links.append(f"{rel}: Broken reference path '{p}' -> {resolved}")

        self.assertEqual(broken_links, [], "Discovered broken references/examples paths in SKILL.md")

    def test_05_content_quality_and_structure_standards(self):
        """SKILL.md must have appropriate length, single H1, and required sections."""
        quality_errors = []

        for skill_path in self.skill_files:
            rel = skill_path.relative_to(REPO_ROOT)
            text = skill_path.read_text(encoding="utf-8")
            lines = text.splitlines()

            if len(lines) < 30:
                quality_errors.append(f"{rel}: Content too short ({len(lines)} lines)")
            if len(lines) >= 200:
                quality_errors.append(f"{rel}: Exceeds 200 lines ({len(lines)} lines)")

            clean_text = strip_fenced_blocks(text)
            h1_lines = [l for l in clean_text.splitlines() if l.startswith("# ")]
            if len(h1_lines) != 1:
                quality_errors.append(f"{rel}: Must contain exactly one H1 header")

            for sec in REQUIRED_SECTIONS:
                if sec not in text:
                    quality_errors.append(f"{rel}: Missing required section '{sec}'")

            checklist_items = re.findall(r"(?m)^- \[ \] .+", text)
            if len(checklist_items) < 5:
                quality_errors.append(f"{rel}: Checklist has fewer than 5 items ({len(checklist_items)})")

        self.assertEqual(quality_errors, [], "Content quality standards violations found")

    def test_06_zero_hardcoded_windows_paths(self):
        """Zero SKILL.md files may contain hardcoded absolute Windows drive paths."""
        win_path_violations = []

        for skill_path in self.skill_files:
            rel = skill_path.relative_to(REPO_ROOT)
            text = skill_path.read_text(encoding="utf-8")
            matches = WINDOWS_PATH_RE.findall(text)
            if matches:
                win_path_violations.append(f"{rel}: Contains hardcoded Windows paths: {matches}")

        self.assertEqual(win_path_violations, [], "Discovered non-portable hardcoded Windows paths")


if __name__ == "__main__":
    unittest.main()
