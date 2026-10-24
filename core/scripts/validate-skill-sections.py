#!/usr/bin/env python3
"""Validate governance section coverage on all core and overlay skills."""

from __future__ import annotations

import re
import sys

from common import ROOT, collect_skill_files, strip_fenced_blocks

REQUIRED_SECTIONS = ("Failure Modes", "Output Contracts", "Security Guardrails")


def missing_sections(body: str) -> list[str]:
    text = strip_fenced_blocks(body)
    return [
        section
        for section in REQUIRED_SECTIONS
        if not re.search(rf"(?m)^#{{2,3}} {re.escape(section)}\b", text)
    ]


def main() -> int:
    errors: list[str] = []
    checked = 0
    for path in collect_skill_files():
        checked += 1
        missing = missing_sections(path.read_text(encoding="utf-8"))
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")

    if errors:
        print(f"Skill governance sections missing in {len(errors)}/{checked} skills:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Skill-sections validation passed: {checked} skills carry all required governance sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
