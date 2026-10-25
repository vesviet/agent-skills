#!/usr/bin/env python3
"""Challenge tests for the 2026-10 Content Manager modernization round.

Guards the verified 2026-10-25 content-governance baseline:
- EU AI Act Article 50 transparency obligations are LIVE (in force since
  2026-08-02; grace period to 2026-12 for pre-existing generative systems);
  C2PA published its AI-content labeling implementation guide in 2026-07.
- GEO citation tracking covers Google AI Overviews AND AI Mode, ChatGPT Search
  (the current OpenAI product name; "SearchGPT" is obsolete), and Perplexity.
- Share of Model (SoM) tracked alongside AI Share of Voice (AI SOV).
- All six content/* skills are versioned 2.0.0 with official OWASP ASI titles.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_FILE = REPO_ROOT / "core" / "roles" / "content-manager.md"
REVIEW_CHECKLIST = REPO_ROOT / "core" / "roles" / "references" / "content-manager-review-checklist.md"
GOVERNANCE = REPO_ROOT / "core" / "roles" / "references" / "content-manager-governance-standards.md"
CONTENT_SKILLS = REPO_ROOT / "core" / "skills" / "content"
SEARCHGPT_FREE_FILES = [
    ROLE_FILE,
    REVIEW_CHECKLIST,
    GOVERNANCE,
    CONTENT_SKILLS / "design-content-strategy" / "SKILL.md",
    CONTENT_SKILLS / "design-content-strategy" / "references" / "information-gain-and-decay-triage.md",
    CONTENT_SKILLS / "optimize-seo" / "SKILL.md",
    CONTENT_SKILLS / "optimize-seo" / "references" / "geo-ai-citation-playbook.md",
    CONTENT_SKILLS / "optimize-seo" / "references" / "process-and-checklist.md",
    CONTENT_SKILLS / "write-article" / "SKILL.md",
    CONTENT_SKILLS / "audit-content" / "references" / "information-gain-rubric.md",
]
SKILL_NAMES = [
    "audit-content",
    "design-content-strategy",
    "optimize-seo",
    "repurpose-content",
    "write-article",
    "write-copy",
]


def read(path: Path) -> str:
    assert path.exists(), f"{path} must exist"
    return path.read_text(encoding="utf-8")


def frontmatter_version(path: Path) -> str | None:
    match = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', read(path), re.MULTILINE)
    return match.group(1) if match else None


class TestArticle50Live(unittest.TestCase):
    """Article 50 is in force (2026-08-02) with C2PA as the marking path."""

    def test_01_live_obligation_framing(self):
        role = read(ROLE_FILE)
        self.assertIn("in force since 2026-08-02", role)
        self.assertIn("grace period to 2026-12", role)
        self.assertIn("C2PA implementation guide (2026-07)", role)

    def test_02_gates_section(self):
        checklist = read(REVIEW_CHECKLIST)
        self.assertIn("### 2026-10 Modernization Gates", checklist)
        for gate in ("Article-50-Live Gate", "GEO-Engine-Currency Gate", "SoM-Metric Gate", "ASI-Title Gate"):
            self.assertIn(gate, checklist)


class TestGEOEngineCurrency(unittest.TestCase):
    """AI Mode + ChatGPT Search tracked; obsolete SearchGPT naming rejected."""

    def test_01_current_engine_set(self):
        for path in (ROLE_FILE, REVIEW_CHECKLIST, GOVERNANCE):
            text = read(path)
            self.assertIn("AI Mode", text)
            self.assertIn("ChatGPT Search", text)

    def test_02_no_searchgpt_in_scope(self):
        for path in SEARCHGPT_FREE_FILES:
            self.assertNotIn("SearchGPT", read(path), f"{path.name} must not use the obsolete SearchGPT name")

    def test_03_som_metric(self):
        self.assertIn("Share of Model (SoM)", read(ROLE_FILE))


class TestSkillVersionsAndASITitles(unittest.TestCase):
    """Six content skills versioned 2.0.0 with official OWASP ASI titles."""

    def test_01_all_skills_versioned(self):
        for name in SKILL_NAMES:
            skill = CONTENT_SKILLS / name / "SKILL.md"
            self.assertEqual(frontmatter_version(skill), "2.0.0", f"{name} must declare version 2.0.0")

    def test_02_official_asi_titles(self):
        official = [
            "ASI01 Agent Goal Hijack",
            "ASI03 Identity & Privilege Abuse",
            "ASI07 Insecure Inter-Agent Communication",
        ]
        for name in SKILL_NAMES:
            text = read(CONTENT_SKILLS / name / "SKILL.md")
            for title in official:
                self.assertIn(title, text, f"{name} must use official title: {title}")

    def test_03_no_invented_or_truncated_titles(self):
        banned = [
            "ASI01 Goal Hijack",
            "ASI03 Identity & Confidentiality Abuse",
            "ASI04 Supply Chain",
            "ASI05 RCE Guard",
            "ASI07 Inter-Agent Communication",
            "ASI09 Trust Exploitation",
        ]
        for name in SKILL_NAMES:
            text = read(CONTENT_SKILLS / name / "SKILL.md")
            for title in banned:
                self.assertNotIn(title, text, f"{name} must not use non-official title: {title}")


class TestRoleFooter(unittest.TestCase):
    """Role footer records the round; mission timeframe extended to 2027."""

    def test_01_footer_date(self):
        lines = [line.strip() for line in read(ROLE_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-25")

    def test_02_mission_timeframe(self):
        self.assertIn("2025–2027", read(ROLE_FILE))


if __name__ == "__main__":
    unittest.main()
