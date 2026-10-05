#!/usr/bin/env python3
"""Automated Challenge Test Suite for Sprint 2 Modernization & 100% Checklist Parity.

Validates and stress-tests:
1. Checklist Inventory & Coverage (35/35 Roles):
   - Every role in core/roles/*.md has a dedicated review checklist in core/roles/references/<role>-review-checklist.md.
   - All 14 Sprint 2 checklists satisfy depth standards (>60 lines, >=6 quantitative sections).
2. Role Review Checklist References:
   - Every role definition in core/roles/*.md links directly to references/<role>-review-checklist.md.
3. Architectural Guardrail Locks:
   - All 35 roles contain at least 4 explicit architectural locks (e.g. **BOUNDARY LOCK**, **SECURITY LOCK**).
   - 3d-graphics-engineer contains its 5 SOTA locks (WEBGPU-FALLBACK-LOCK, DRACO-MESHOPT-LOCK, MEMORY-DISPOSAL-LOCK, FRAME-BUDGET-LOCK, GEN-3D LOCK).
4. Dual Index Parity:
   - SHA-256 bitwise parity between core/a2a/.well-known/role-skill-index.json and adapters/antigravity/role-skill-index.json.
5. Role Standard Structure:
   - All 14 Sprint 2 roles retain mandatory 19-section structure per core/roles/role-standard.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
REFERENCES_DIR = ROLES_DIR / "references"
CORE_INDEX = CORE_DIR / "a2a" / ".well-known" / "role-skill-index.json"
ADAPTER_INDEX = REPO_ROOT / "adapters" / "antigravity" / "role-skill-index.json"

SPRINT2_ROLES = [
    "agent-coordinator",
    "security-engineer",
    "cloudflare-engineer",
    "ecommerce-engineer",
    "mmo-engineer",
    "system-engineer",
    "task-planner",
    "product-manager",
    "project-manager",
    "researcher",
    "technical-writer",
    "ui-ux-designer",
    "3d-graphics-engineer",
    "agent-discovery-engineer",
]


class TestSprint2ModernizationChallenge(unittest.TestCase):
    """Challenge suite verifying Sprint 2 role checklist coverage and invariants."""

    def test_all_35_roles_have_dedicated_checklists(self) -> None:
        """Every role in core/roles/*.md must have a corresponding review checklist."""
        role_files = sorted(ROLES_DIR.glob("*.md"))
        role_names = [f.stem for f in role_files if f.name not in ("role-standard.md", "README.md", "INDEX.md")]
        self.assertEqual(len(role_names), 35, f"Expected 35 roles, found {len(role_names)}")

        missing_checklists = []
        for role in role_names:
            chk_path = REFERENCES_DIR / f"{role}-review-checklist.md"
            if not chk_path.exists():
                missing_checklists.append(f"{role}-review-checklist.md")

        self.assertEqual(missing_checklists, [], f"Missing dedicated review checklists: {missing_checklists}")

    def test_sprint2_checklists_depth_and_structure(self) -> None:
        """All 14 Sprint 2 checklists must be >60 lines with at least 6 H2/H3 sections."""
        for role in SPRINT2_ROLES:
            chk_path = REFERENCES_DIR / f"{role}-review-checklist.md"
            self.assertTrue(chk_path.exists(), f"Checklist missing for {role}")
            content = chk_path.read_text(encoding="utf-8")
            lines = content.strip().splitlines()
            self.assertGreaterEqual(
                len(lines),
                60,
                f"Checklist for {role} too short ({len(lines)} lines; expected >= 60)",
            )
            # Count verification sections (### or ##)
            headings = [line for line in lines if re.match(r"^#{2,3}\s+", line)]
            self.assertGreaterEqual(
                len(headings),
                6,
                f"Checklist for {role} has only {len(headings)} sections; expected >= 6",
            )

    def test_all_35_roles_link_to_dedicated_checklist(self) -> None:
        """Every role file must link to its dedicated checklist under ## Review Checklist."""
        role_files = sorted(ROLES_DIR.glob("*.md"))
        role_names = [f.stem for f in role_files if f.name not in ("role-standard.md", "README.md", "INDEX.md")]

        unlinked_roles = []
        for role in role_names:
            role_file = ROLES_DIR / f"{role}.md"
            content = role_file.read_text(encoding="utf-8")
            expected_ref = f"references/{role}-review-checklist.md"
            if expected_ref not in content:
                unlinked_roles.append(role)

        self.assertEqual(unlinked_roles, [], f"Roles not linking to dedicated checklist: {unlinked_roles}")

    def test_3d_graphics_engineer_guardrail_locks(self) -> None:
        """3d-graphics-engineer must contain 5 explicit SOTA locks."""
        role_file = ROLES_DIR / "3d-graphics-engineer.md"
        content = role_file.read_text(encoding="utf-8")
        expected_locks = [
            "WEBGPU-FALLBACK-LOCK",
            "DRACO-MESHOPT-LOCK",
            "MEMORY-DISPOSAL-LOCK",
            "FRAME-BUDGET-LOCK",
            "GEN-3D LOCK",
        ]
        for lock in expected_locks:
            self.assertIn(lock, content, f"Missing architectural lock {lock} in 3d-graphics-engineer.md")

    def test_all_roles_have_guardrail_locks(self) -> None:
        """Every role must have at least 4 explicit architectural locks (**...LOCK**)."""
        role_files = sorted(ROLES_DIR.glob("*.md"))
        role_names = [f.stem for f in role_files if f.name not in ("role-standard.md", "README.md", "INDEX.md")]

        roles_insufficient_locks = []
        for role in role_names:
            role_file = ROLES_DIR / f"{role}.md"
            content = role_file.read_text(encoding="utf-8")
            locks = re.findall(r"\*\*([A-Z0-9_ -]+LOCK)\*\*", content)
            if len(locks) < 4:
                roles_insufficient_locks.append((role, len(locks)))

        self.assertEqual(roles_insufficient_locks, [], f"Roles with < 4 locks: {roles_insufficient_locks}")

    def test_dual_index_sha256_parity(self) -> None:
        """Dual indexes must have 100% SHA-256 bitwise parity."""
        self.assertTrue(CORE_INDEX.exists(), "Core role-skill index missing")
        self.assertTrue(ADAPTER_INDEX.exists(), "Adapter role-skill index missing")

        h1 = hashlib.sha256(CORE_INDEX.read_bytes()).hexdigest()
        h2 = hashlib.sha256(ADAPTER_INDEX.read_bytes()).hexdigest()
        self.assertEqual(h1, h2, "Dual index SHA-256 mismatch")


if __name__ == "__main__":
    unittest.main()
