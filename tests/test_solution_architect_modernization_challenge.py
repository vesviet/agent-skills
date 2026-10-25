#!/usr/bin/env python3
"""Challenge tests for the 2026-10 Solution Architect modernization round.

Guards the verified 2026-10-25 baseline:
- Stack currency aligned with the Backend Developer baseline: Go 1.27+
  (released 2026-08); previous-generation Go pins fail currency review.
- MCP marketplace adoption requires Streamable HTTP transport (MCP spec
  2025-03-26+); new HTTP+SSE deployments are rejected.
- Core AaC invariants (Structurizr/LikeC4, Little's Law, Agent ROI,
  EU AI Act timeline) remain intact.
"""

from __future__ import annotations

from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_FILE = REPO_ROOT / "core" / "roles" / "solution-architect.md"
CHECKLIST_FILE = REPO_ROOT / "core" / "roles" / "references" / "solution-architect-review-checklist.md"


def read(path: Path) -> str:
    assert path.exists(), f"{path} must exist"
    return path.read_text(encoding="utf-8")


class TestStackCurrency(unittest.TestCase):
    """Go 1.27+ baseline across role and checklist."""

    def test_01_go_127_present(self):
        role = read(ROLE_FILE)
        self.assertGreaterEqual(role.count("Go 1.27+"), 5)
        self.assertIn("Go 1.27+ Kratos", role)

    def test_02_no_previous_gen_go_pins(self):
        for path in (ROLE_FILE, CHECKLIST_FILE):
            self.assertNotIn("Go 1.25", read(path), f"{path.name} must not pin previous-generation Go")


class TestModernizationGates(unittest.TestCase):
    """Checklist gains the 2026-10 gates."""

    def test_01_gates_section(self):
        checklist = read(CHECKLIST_FILE)
        self.assertIn("### 10. 2026-10 Modernization Gates", checklist)
        for gate in ("Stack-Currency Gate", "MCP-Transport Gate", "GPU-Sizing-Currency Gate"):
            self.assertIn(gate, checklist)

    def test_02_mcp_streamable_http_gate(self):
        self.assertIn("Streamable HTTP (MCP spec 2025-03-26+)", read(CHECKLIST_FILE))

    def test_03_checklist_section_5_title(self):
        self.assertIn("### 5. Clean Architecture & Saga Orchestration (Go 1.27+ Kratos & Dapr)", read(CHECKLIST_FILE))


class TestCoreInvariantsIntact(unittest.TestCase):
    """AaC, capacity, and agentic-evaluation invariants must survive the round."""

    def test_01_aac_invariants(self):
        role = read(ROLE_FILE)
        for term in ("Structurizr DSL", "LikeC4", "Little's Law", "workspace.dsl"):
            self.assertIn(term, role)

    def test_02_agentic_evaluation_invariants(self):
        role = read(ROLE_FILE)
        for term in ("Agent ROI", "MCP Marketplace", "Value-Per-Token", "Transactional Outbox"):
            self.assertIn(term, role)

    def test_03_eu_ai_act_timeline_current(self):
        self.assertIn("Article 50 transparency live August 2026", read(CHECKLIST_FILE))


class TestFooter(unittest.TestCase):
    def test_01_footer_date(self):
        lines = [line.strip() for line in read(ROLE_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-25")


if __name__ == "__main__":
    unittest.main()
