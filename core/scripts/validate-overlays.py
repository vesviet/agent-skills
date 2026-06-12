#!/usr/bin/env python3
"""Validate overlay directories and their structure."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    errors: list[str] = []
    overlays_dir = ROOT / "overlays"

    if not overlays_dir.is_dir():
        print(f"Error: {overlays_dir} is not a directory.")
        return 1

    overlays: list[Path] = []

    for d in sorted(overlays_dir.iterdir()):
        if not d.is_dir():
            continue
        overlays.append(d)
        rel = d.relative_to(ROOT)

        # Check README.md
        readme = d / "README.md"
        if not readme.is_file():
            errors.append(f"{rel}: missing README.md")
        else:
            content = readme.read_text(encoding="utf-8").strip()
            if len(content) < 20:
                errors.append(f"{rel}: README.md is too short")
            if not content.startswith("# "):
                errors.append(f"{rel}: README.md must start with an h1 heading (# )")

        # Check rules/ directory
        rules_dir = d / "rules"
        if not rules_dir.is_dir():
            # Allow overlays to just provide other structures if explicitly designed so,
            # but usually they should have a rules dir. We'll enforce it for consistency.
            errors.append(f"{rel}: missing rules/ directory")
        else:
            rule_files = list(rules_dir.glob("*.md"))
            if not rule_files:
                errors.append(f"{rel}: rules/ directory exists but contains no markdown files")

    if not overlays:
        errors.append("no overlays found under overlays/")

    if errors:
        print("Overlay validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Overlay validation passed: {len(overlays)} overlays checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
