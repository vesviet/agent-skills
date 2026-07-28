#!/usr/bin/env python3
"""Run all core pack validators."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VALIDATORS = (
    "validate-rules.py",
    "validate-skills.py",
    "validate-roles.py",
    "validate-workflows.py",
    "validate-packs.py",
    "validate-overlays.py",
    "validate-2026-compliance.py",
    "validate-contracts.py",
    "validate-a2a-compliance.py",
    "validate-agent-cards.py",
    "validate-standardization.py",
    "validate-version-sync.py",
    "validate-indexes.py",
    "validate-policy-consistency.py",
    "validate-skill-ownership.py",
)


def main() -> int:
    for script in VALIDATORS:
        path = ROOT / script
        result = subprocess.run([sys.executable, str(path)], check=False)
        if result.returncode != 0:
            return result.returncode
    print("All core validators passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
