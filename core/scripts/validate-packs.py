#!/usr/bin/env python3
"""Validate pack manifests and their references."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    errors: list[str] = []
    packs_dir = ROOT / "packs"
    manifests: list[Path] = []

    for manifest in sorted(packs_dir.glob("*/manifest.yaml")):
        manifests.append(manifest)
        text = manifest.read_text(encoding="utf-8")
        rel = manifest.relative_to(ROOT)

        if "name:" not in text:
            errors.append(f"{rel}: missing 'name' field")
        if "description:" not in text:
            errors.append(f"{rel}: missing 'description' field")
        if "includes:" not in text:
            errors.append(f"{rel}: missing 'includes' field")

        for line in text.splitlines():
            stripped = line.strip().lstrip("- ")
            if stripped == "core":
                if not (ROOT / "core").is_dir():
                    errors.append(f"{rel}: referenced path does not exist: core")
            elif stripped.startswith("overlays/"):
                if not (ROOT / stripped).is_dir():
                    errors.append(f"{rel}: referenced overlay does not exist: {stripped}")

    if not manifests:
        errors.append("no pack manifests found under packs/*/manifest.yaml")

    if errors:
        print("Pack validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Pack validation passed: {len(manifests)} packs checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
