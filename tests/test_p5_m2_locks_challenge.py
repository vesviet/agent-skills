#!/usr/bin/env python3
"""Empirical Challenger Test Suite: Milestone 2 Guardrail Lock Density & Universal Locks.

Phase 5: Requirement R3 Verification
Audits all 39 role files in `core/roles/` (excluding README.md and role-standard.md)
to assert:
1. Exactly 39 role definition files are present.
2. Every role satisfies 12 <= named_locks <= 24.
3. Every role contains all 7 universal guardrail locks:
   - BOUNDARY
   - SECURITY (or AGENTIC-SECURITY)
   - AST10-SKILL-SECURITY
   - LETHAL-TRIFECTA
   - IRREVERSIBLE-ACTION
   - MINIMAL-FOOTPRINT
   - LEAST-AGENCY
4. Mutation / sensitivity tests verify that boundary violations and missing
   universal locks are deterministically caught.
"""

from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path

# Configure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"

# Strict pattern from mission prompt: ^- \*\*[A-Z0-9_\-]+(?: LOCK)?\*\*:
STRICT_LOCK_PATTERN = re.compile(r"^-\s+\*\*([A-Z0-9_\-]+(?: LOCK)?)\*\*:", re.M)

# Permissive pattern used by validate-roles.py: ^- \*\*([A-Z0-9_\-\s\(\)]+LOCK)\*\*:
VALIDATE_LOCK_PATTERN = re.compile(r"^-\s+\*\*([A-Z0-9_\-\s\(\)]+LOCK)\*\*:", re.M)

# Universal locks definitions
REQUIRED_UNIVERSAL_LOCKS = (
    ("BOUNDARY", re.compile(r"^-\s+\*\*BOUNDARY(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("SECURITY", re.compile(r"^-\s+\*\*(?:AGENTIC-)?SECURITY(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("AST10-SKILL-SECURITY", re.compile(r"^-\s+\*\*AST10-SKILL-SECURITY(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("LETHAL-TRIFECTA", re.compile(r"^-\s+\*\*LETHAL[- ]TRIFECTA(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("IRREVERSIBLE-ACTION", re.compile(r"^-\s+\*\*IRREVERSIBLE[- ]ACTION(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("MINIMAL-FOOTPRINT", re.compile(r"^-\s+\*\*MINIMAL[- ]FOOTPRINT(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
    ("LEAST-AGENCY", re.compile(r"^-\s+\*\*LEAST[- ]AGENCY(?:\s+LOCK|-LOCK)?\*\*:", re.M | re.I)),
)


def get_role_files() -> list[Path]:
    """Find all 39 role files excluding README.md and role-standard.md."""
    return sorted(
        p for p in ROLES_DIR.glob("*.md")
        if p.name not in {"README.md", "role-standard.md"}
    )


def extract_guardrails_section(content: str) -> str:
    """Extract text within ## Guardrails section."""
    match = re.search(r"## Guardrails\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    return match.group(1) if match else ""


class TestM2LockCalibrations(unittest.TestCase):
    """Empirical challenge tests for role guardrail lock density and universal locks."""

    def test_role_count_is_exactly_39(self) -> None:
        """Verify exactly 39 role files exist in core/roles/."""
        roles = get_role_files()
        self.assertEqual(
            len(roles),
            39,
            f"Expected exactly 39 role files, found {len(roles)}: {[r.name for r in roles]}"
        )

    def test_strict_lock_density_bounds(self) -> None:
        """Assert that for EVERY file, 12 <= lock_count <= 24 using the prompt's strict pattern."""
        roles = get_role_files()
        for role_path in roles:
            content = role_path.read_text(encoding="utf-8")
            gtext = extract_guardrails_section(content)
            self.assertTrue(len(gtext) > 0, f"Role {role_path.name} has empty ## Guardrails section")

            locks = STRICT_LOCK_PATTERN.findall(gtext)
            count = len(locks)
            self.assertGreaterEqual(
                count,
                12,
                f"Role {role_path.name} strict lock count {count} < 12. Locks: {locks}"
            )
            self.assertLessEqual(
                count,
                24,
                f"Role {role_path.name} strict lock count {count} > 24. Locks: {locks}"
            )

    def test_validate_script_lock_density_bounds(self) -> None:
        """Assert that for EVERY file, 12 <= lock_count <= 24 using validate-roles.py pattern."""
        roles = get_role_files()
        for role_path in roles:
            content = role_path.read_text(encoding="utf-8")
            gtext = extract_guardrails_section(content)

            locks = VALIDATE_LOCK_PATTERN.findall(gtext)
            count = len(locks)
            self.assertGreaterEqual(
                count,
                12,
                f"Role {role_path.name} validate-pattern lock count {count} < 12. Locks: {locks}"
            )
            self.assertLessEqual(
                count,
                24,
                f"Role {role_path.name} validate-pattern lock count {count} > 24. Locks: {locks}"
            )

    def test_all_seven_universal_locks_present(self) -> None:
        """Assert that for EVERY file, all 7 universal locks are present as standalone named bullets."""
        roles = get_role_files()
        for role_path in roles:
            content = role_path.read_text(encoding="utf-8")
            gtext = extract_guardrails_section(content)

            missing = []
            for lock_name, pattern in REQUIRED_UNIVERSAL_LOCKS:
                if not pattern.search(gtext):
                    missing.append(lock_name)

            self.assertEqual(
                missing,
                [],
                f"Role {role_path.name} is missing universal locks: {missing}"
            )

    def test_no_duplicate_locks_within_any_role(self) -> None:
        """Assert that no role file contains duplicate named locks."""
        roles = get_role_files()
        for role_path in roles:
            content = role_path.read_text(encoding="utf-8")
            gtext = extract_guardrails_section(content)

            raw_locks = re.findall(r"^-\s+\*\*([^*]+)\*\*:", gtext, re.M)
            seen = set()
            duplicates = []
            for lk in raw_locks:
                if lk in seen:
                    duplicates.append(lk)
                seen.add(lk)

            self.assertEqual(
                duplicates,
                [],
                f"Role {role_path.name} contains duplicate locks: {duplicates}"
            )

    def test_adversarial_mutation_overflow_detection(self) -> None:
        """Verify that injecting an extra lock into a role with 24 locks triggers a failure."""
        sample_role = ROLES_DIR / "agent-discovery-engineer.md"
        content = sample_role.read_text(encoding="utf-8")
        gtext = extract_guardrails_section(content)
        locks = VALIDATE_LOCK_PATTERN.findall(gtext)
        self.assertEqual(len(locks), 24, "Pre-condition: sample role must have exactly 24 locks")

        # Mutate by appending an extra synthetic lock
        mutated_gtext = gtext + "\n- **SYNTHETIC-OVERFLOW-LOCK**: test overflow\n"
        mutated_locks = VALIDATE_LOCK_PATTERN.findall(mutated_gtext)
        self.assertEqual(len(mutated_locks), 25)
        # Verify boundary assertion fails
        with self.assertRaises(AssertionError):
            self.assertLessEqual(len(mutated_locks), 24)

    def test_adversarial_mutation_missing_universal_detection(self) -> None:
        """Verify that removing a universal lock triggers a failure."""
        sample_role = ROLES_DIR / "agent-coordinator.md"
        content = sample_role.read_text(encoding="utf-8")
        gtext = extract_guardrails_section(content)

        # Mutate by stripping out the LETHAL-TRIFECTA LOCK line
        mutated_gtext = re.sub(
            r"^-\s+\*\*LETHAL[- ]TRIFECTA(?:\s+LOCK|-LOCK)?\*\*:.*$",
            "",
            gtext,
            flags=re.M,
        )

        missing = []
        for lock_name, pattern in REQUIRED_UNIVERSAL_LOCKS:
            if not pattern.search(mutated_gtext):
                missing.append(lock_name)

        self.assertIn("LETHAL-TRIFECTA", missing)


def generate_audit_table() -> str:
    """Generate Markdown and ASCII audit table for handoff reporting."""
    roles = get_role_files()
    lines = [
        "| # | Role File | Strict Locks | Validate Locks | Density Check (12-24) | Universals (7/7) | Verdict |",
        "|---|-----------|:------------:|:--------------:|:---------------------:|:----------------:|:-------:|",
    ]

    for idx, role_path in enumerate(roles, 1):
        content = role_path.read_text(encoding="utf-8")
        gtext = extract_guardrails_section(content)

        strict_locks = STRICT_LOCK_PATTERN.findall(gtext)
        val_locks = VALIDATE_LOCK_PATTERN.findall(gtext)

        strict_cnt = len(strict_locks)
        val_cnt = len(val_locks)

        density_ok = (12 <= strict_cnt <= 24) and (12 <= val_cnt <= 24)

        found_universals = sum(1 for _, pat in REQUIRED_UNIVERSAL_LOCKS if pat.search(gtext))
        universals_ok = (found_universals == 7)

        verdict = "PASS" if (density_ok and universals_ok) else "FAIL"

        lines.append(
            f"| {idx:02d} | `{role_path.name}` | {strict_cnt} | {val_cnt} | "
            f"{'PASS' if density_ok else 'FAIL'} | {found_universals}/7 | **{verdict}** |"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 5 / MILESTONE 2: EMPIRICAL CHALLENGER AUDIT REPORT")
    print("=" * 80)
    table = generate_audit_table()
    print(table)
    print("=" * 80)

    # Run unittests
    unittest.main(argv=[sys.argv[0], "-v"])
