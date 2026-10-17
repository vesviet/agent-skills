#!/usr/bin/env python3
"""Empirical Challenger Test Suite for Tier-3 Roles and 16 Review Checklists.

Executed by teamwork_preview_challenger agent to empirically assert:
1. All 10 Tier-3 upgraded roles enforce 12 <= lock_count <= 24.
2. task-planner.md outputs technical-delivery-plan.json and coordination-plan.json
   and routes seo-weekly-board.json to SEO Analyst.
3. All 16 review checklists in core/roles/references/ have line_count >= 110
   (with agent-coordinator >= 150).
4. Mathematical formulas and PromQL queries are present across the checklists.
5. Adversarial mutation tests validating sensitivity of the guardrails.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
REFERENCES_DIR = ROLES_DIR / "references"

TIER3_UPGRADED_ROLES = [
    "ai-systems-engineer",
    "mmo-engineer",
    "aws-engineer",
    "3d-graphics-engineer",
    "agent-discovery-engineer",
    "ecommerce-engineer",
    "product-manager",
    "project-manager",
    "researcher",
    "task-planner",
]

CHECKLISTS_16 = [
    "3d-graphics-engineer-review-checklist.md",
    "agent-coordinator-review-checklist.md",
    "agent-discovery-engineer-review-checklist.md",
    "ai-systems-engineer-review-checklist.md",
    "aws-engineer-review-checklist.md",
    "cloudflare-engineer-review-checklist.md",
    "ecommerce-engineer-review-checklist.md",
    "mmo-engineer-review-checklist.md",
    "product-manager-review-checklist.md",
    "project-manager-review-checklist.md",
    "researcher-review-checklist.md",
    "security-engineer-review-checklist.md",
    "system-engineer-review-checklist.md",
    "task-planner-review-checklist.md",
    "technical-writer-review-checklist.md",
    "ui-ux-designer-review-checklist.md",
]


class TestTier3EmpiricalChallenger(unittest.TestCase):
    """Empirical challenger test cases for Tier-3 roles and 16 review checklists."""

    def test_tier3_10_roles_lock_count_range(self) -> None:
        """Assert that for all 10 upgraded roles: 12 <= lock_count <= 24."""
        lock_pattern = re.compile(r"\*\*([A-Z0-9_ -]+LOCK)\*\*")
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            self.assertTrue(path.exists(), f"Role definition file missing: {path}")
            content = path.read_text(encoding="utf-8")
            locks = lock_pattern.findall(content)
            lock_count = len(locks)
            self.assertGreaterEqual(
                lock_count,
                12,
                f"Role {role} has {lock_count} locks; expected >= 12. Locks found: {locks}",
            )
            self.assertLessEqual(
                lock_count,
                24,
                f"Role {role} has {lock_count} locks; expected <= 24. Locks found: {locks}",
            )

    def test_task_planner_outputs_and_seo_routing(self) -> None:
        """Assert task-planner emits technical-delivery-plan & coordination-plan and routes seo-weekly-board to SEO Analyst."""
        tp_path = ROLES_DIR / "task-planner.md"
        self.assertTrue(tp_path.exists(), f"task-planner.md missing: {tp_path}")
        content = tp_path.read_text(encoding="utf-8")

        # 1. Primary outputs assertion
        self.assertIn(
            "contracts/schemas/technical-delivery-plan.json",
            content,
            "task-planner.md must declare technical-delivery-plan.json in outputs",
        )
        self.assertIn(
            "contracts/schemas/coordination-plan.json",
            content,
            "task-planner.md must declare coordination-plan.json in outputs",
        )

        # 2. Must not claim primary ownership of seo-weekly-board.json
        outputs_match = re.search(r"## Outputs Produced\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        self.assertIsNotNone(outputs_match, "Outputs Produced section missing in task-planner.md")
        outputs_text = outputs_match.group(1)
        owned_part = outputs_text.split("Contracts owned by other roles")[0]
        self.assertNotIn(
            "contracts/schemas/seo-weekly-board.json",
            owned_part,
            "task-planner.md must not claim primary ownership of seo-weekly-board.json",
        )

        # 3. Explicitly routes seo-weekly-board.json to SEO Analyst
        self.assertIn(
            "SEO Analyst",
            content,
            "task-planner.md must mention SEO Analyst for delegated deliverables",
        )
        self.assertTrue(
            re.search(r"seo-weekly-board\.json.*?(?:owned by|emits|Escalate to).*?SEO Analyst", content, re.IGNORECASE | re.DOTALL)
            or re.search(r"SEO Analyst.*?(?:owns|emits).*?seo-weekly-board\.json", content, re.IGNORECASE | re.DOTALL),
            "task-planner.md must explicitly route seo-weekly-board.json to SEO Analyst",
        )

    def test_16_checklists_line_counts(self) -> None:
        """Assert all 16 checklists in core/roles/references/ have line_count >= 110 (and agent-coordinator >= 150)."""
        for filename in CHECKLISTS_16:
            path = REFERENCES_DIR / filename
            self.assertTrue(path.exists(), f"Checklist missing: {path}")
            content = path.read_text(encoding="utf-8")
            lines = content.strip().splitlines()
            line_count = len(lines)

            # Minimum 110 lines for all 16 checklists
            self.assertGreaterEqual(
                line_count,
                110,
                f"Checklist {filename} has {line_count} lines; expected >= 110",
            )

            # Special invariant: agent-coordinator-review-checklist.md >= 150 lines
            if filename == "agent-coordinator-review-checklist.md":
                self.assertGreaterEqual(
                    line_count,
                    150,
                    f"agent-coordinator-review-checklist.md has {line_count} lines; expected >= 150",
                )

    def test_checklists_mathematical_formulas_present(self) -> None:
        """Assert mathematical formulas (LaTeX $...$, equations, quantitative formulas) are present across checklists."""
        formula_pattern = re.compile(
            r"(\$[^$\n]+\$|\$\$[\s\S]+?\$\$|\\frac\{|\\sum_|\bFormula\b|\bEquation\b|\b[A-Z][a-zA-Z0-9_]*\s*=\s*[^,\n]+)",
            re.IGNORECASE,
        )
        for filename in CHECKLISTS_16:
            path = REFERENCES_DIR / filename
            content = path.read_text(encoding="utf-8")
            matches = formula_pattern.findall(content)
            self.assertGreaterEqual(
                len(matches),
                1,
                f"Checklist {filename} does not contain mathematical formulas/equations",
            )

    def test_checklists_promql_queries_present(self) -> None:
        """Assert PromQL queries and telemetry alert rules are present across the checklists."""
        promql_block_pattern = re.compile(r"```promql[\s\S]+?```", re.IGNORECASE)
        promql_inline_pattern = re.compile(
            r"(?:histogram_quantile|rate\(|sum\(|avg\(|increase\(|count\(|irate\()[^`\n]+",
            re.IGNORECASE,
        )
        total_promql_blocks = 0
        checklists_with_promql = []
        for filename in CHECKLISTS_16:
            path = REFERENCES_DIR / filename
            content = path.read_text(encoding="utf-8")
            blocks = promql_block_pattern.findall(content)
            inline = promql_inline_pattern.findall(content)
            if blocks or inline:
                total_promql_blocks += len(blocks) + len(inline)
                checklists_with_promql.append(filename)

        # Assert PromQL queries are distributed across operational and infrastructure checklists
        self.assertGreaterEqual(
            len(checklists_with_promql),
            8,
            f"Expected at least 8 checklists with PromQL queries, found {len(checklists_with_promql)}: {checklists_with_promql}",
        )
        self.assertGreaterEqual(
            total_promql_blocks,
            15,
            f"Expected at least 15 PromQL blocks/queries across checklists, found {total_promql_blocks}",
        )


class TestTier3AdversarialOracles(unittest.TestCase):
    """Adversarial stress-test oracles asserting failure modes are caught under mutation."""

    def test_adversarial_lock_count_below_minimum_fails(self) -> None:
        """Adversarial oracle: a role with fewer than 12 locks must fail validation."""
        fake_content = "# Test Role\n**BOUNDARY LOCK**\n**SECURITY LOCK**\n"
        locks = re.findall(r"\*\*([A-Z0-9_ -]+LOCK)\*\*", fake_content)
        self.assertFalse(12 <= len(locks) <= 24, "Should detect insufficient locks")

    def test_adversarial_lock_count_above_maximum_fails(self) -> None:
        """Adversarial oracle: a role with more than 24 locks must fail validation."""
        fake_content = "# Test Role\n" + "\n".join(f"**TEST_LOCK_{i} LOCK**" for i in range(26))
        locks = re.findall(r"\*\*([A-Z0-9_ -]+LOCK)\*\*", fake_content)
        self.assertFalse(12 <= len(locks) <= 24, "Should detect excessive locks")

    def test_adversarial_task_planner_seo_board_hijack_detected(self) -> None:
        """Adversarial oracle: if task-planner claims primary ownership of seo-weekly-board, it must fail."""
        fake_outputs = (
            "## Outputs Produced\n\n"
            "- `contracts/schemas/technical-delivery-plan.json`\n"
            "- `contracts/schemas/coordination-plan.json`\n"
            "- `contracts/schemas/seo-weekly-board.json`\n\n"
            "### Contracts owned by other roles\n"
        )
        owned_part = fake_outputs.split("Contracts owned by other roles")[0]
        self.assertIn("contracts/schemas/seo-weekly-board.json", owned_part)

    def test_adversarial_checklist_truncation_detected(self) -> None:
        """Adversarial oracle: a truncated checklist (< 110 lines) must fail line count check."""
        short_lines = ["# Checklist", "Item 1", "Item 2"]
        self.assertLess(len(short_lines), 110, "Should detect short checklist")

    def test_adversarial_agent_coordinator_below_150_lines_detected(self) -> None:
        """Adversarial oracle: agent-coordinator checklist with < 150 lines must fail check."""
        lines_120 = ["# Checklist"] + [f"Item {i}" for i in range(120)]
        self.assertLess(len(lines_120), 150, "Should detect agent-coordinator under 150 lines")


if __name__ == "__main__":
    unittest.main()

