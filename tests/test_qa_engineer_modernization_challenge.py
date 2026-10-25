#!/usr/bin/env python3
"""Challenge tests for the 2026-10 QA Engineer / SDET modernization round.

Guards the verified 2026-10-25 QA stack baseline:
- Stack currency aligned with the Backend Developer baseline: Go 1.27+
  (released 2026-08) and PostgreSQL 18 Testcontainers (PG 19 GA planned
  2026-11-19); Go 1.25 / PostgreSQL 16 pins fail currency review.
- Browser automation on Playwright v1.64+ (1.64.1 released 2026-10-13);
  v1.48-era pins (Oct 2024) fail currency review.
- `write-tests` skill versioned 2.0.0 with official OWASP ASI titles.
- SDET role was audited clean (no stale version pins) and must stay untouched.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_FILE = REPO_ROOT / "core" / "roles" / "qa-engineer.md"
SDET_FILE = REPO_ROOT / "core" / "roles" / "sdet.md"
CHECKLIST_FILE = REPO_ROOT / "core" / "roles" / "references" / "qa-engineer-review-checklist.md"
SKILL_FILE = REPO_ROOT / "core" / "skills" / "foundation" / "write-tests" / "SKILL.md"


def read(path: Path) -> str:
    assert path.exists(), f"{path} must exist"
    return path.read_text(encoding="utf-8")


def frontmatter_version(path: Path) -> str | None:
    match = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', read(path), re.MULTILINE)
    return match.group(1) if match else None


class TestStackCurrency(unittest.TestCase):
    """Go 1.27+ / PostgreSQL 18 across role, checklist, and write-tests skill."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.checklist = read(CHECKLIST_FILE)
        cls.skill = read(SKILL_FILE)

    def test_01_go_127_everywhere(self):
        for text in (self.role, self.checklist, self.skill):
            self.assertIn("Go 1.27+", text)
            self.assertNotIn("Go 1.25", text)

    def test_02_postgres_18_everywhere(self):
        for text in (self.role, self.checklist, self.skill):
            self.assertIn("PostgreSQL 18", text)
            self.assertNotIn("PostgreSQL 16", text)

    def test_03_ephemeral_parity_mechanics_intact(self):
        self.assertIn("testcontainers/testcontainers-go", self.role)
        self.assertIn("InTx", self.role)
        self.assertIn("go test -v -race", self.role)
        self.assertIn("uber-go/goleak", self.role)


class TestPlaywrightCurrency(unittest.TestCase):
    """Playwright v1.64+ (1.64.1, 2026-10-13) replaces the v1.48-era pin."""

    def test_01_playwright_164(self):
        for path in (ROLE_FILE, CHECKLIST_FILE):
            text = read(path)
            self.assertIn("Playwright v1.64+", text)
            self.assertNotIn("Playwright v1.48", text)


class TestWriteTestsSkill(unittest.TestCase):
    """write-tests skill is versioned 2.0.0 with official OWASP ASI titles."""

    def test_01_skill_version(self):
        self.assertEqual(frontmatter_version(SKILL_FILE), "2.0.0")

    def test_02_official_asi_titles(self):
        text = read(SKILL_FILE)
        for title in (
            "ASI01 Agent Goal Hijack",
            "ASI04 Agentic Supply Chain",
            "ASI05 Unexpected Code Execution",
            "ASI07 Insecure Inter-Agent Communication",
        ):
            self.assertIn(title, text, f"write-tests must use official title: {title}")
        for invented in (
            "ASI01 Goal Hijack",
            "ASI04 Supply Chain",
            "ASI05 RCE Guard",
            "ASI07 Inter-Agent Communication",
        ):
            self.assertNotIn(invented, text, f"write-tests must not use invented title: {invented}")


class TestModernizationGatesAndFooter(unittest.TestCase):
    """Checklist gains the 2026-10 gates; role footer records the round."""

    def test_01_gates_section(self):
        checklist = read(CHECKLIST_FILE)
        self.assertIn("### 14. 2026-10 Modernization Gates", checklist)
        for gate in ("Stack-Currency Gate", "Playwright-Currency Gate", "Toolchain-Alignment Gate"):
            self.assertIn(gate, checklist)

    def test_02_footer_date(self):
        lines = [line.strip() for line in read(ROLE_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-25")


class TestSdetUntouchedGuard(unittest.TestCase):
    """SDET was audited clean of stale version pins; the round must not alter it."""

    def test_01_sdet_has_no_stale_pins(self):
        sdet = read(SDET_FILE)
        self.assertNotIn("Go 1.25", sdet)
        self.assertNotIn("PostgreSQL 16", sdet)
        self.assertNotIn("Playwright v1.48", sdet)

    def test_02_sdet_footer_unchanged(self):
        lines = [line.strip() for line in read(SDET_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-20")


if __name__ == "__main__":
    unittest.main()
