#!/usr/bin/env python3
"""Inject Output Contracts section into SKILL.md files that are missing it.

Resolves the repo root dynamically from the script's own location — works on
macOS, Linux, and Windows without hardcoded paths.

Usage:
    python3 core/scripts/inject_output_contracts.py
    python3 core/scripts/inject_output_contracts.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SKILL_DIRS: list[Path] = [
    ROOT / "core" / "skills" / "backend",
    ROOT / "core" / "skills" / "frontend",
    ROOT / "core" / "skills" / "platform",
]

IMPLEMENTATION_CONTRACT = """\
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"""

DEPLOYMENT_CONTRACT = """\
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"""


def inject(skill_dir: Path, *, dry_run: bool = False) -> tuple[int, int]:
    """Inject output contracts into SKILL.md files under skill_dir.

    Returns (injected, skipped) counts.
    """
    injected = 0
    skipped = 0

    is_platform = skill_dir.name == "platform"
    contract = DEPLOYMENT_CONTRACT if is_platform else IMPLEMENTATION_CONTRACT

    for path in sorted(skill_dir.rglob("SKILL.md")):
        content = path.read_text(encoding="utf-8")

        if "## Output Contracts" in content:
            print(f"  skip  {path.relative_to(ROOT)} — already has Output Contracts")
            skipped += 1
            continue

        if "## Related Skills" in content:
            updated = content.replace("## Related Skills", contract + "## Related Skills", 1)
        else:
            updated = content.rstrip() + "\n\n" + contract

        if dry_run:
            print(f"  would inject  {path.relative_to(ROOT)}")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"  injected  {path.relative_to(ROOT)}")
        injected += 1

    return injected, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject Output Contracts section into SKILL.md files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files.",
    )
    args = parser.parse_args()

    total_injected = 0
    total_skipped = 0

    for skill_dir in SKILL_DIRS:
        if not skill_dir.is_dir():
            print(f"warning: skill dir not found: {skill_dir.relative_to(ROOT)}", file=sys.stderr)
            continue
        print(f"\n{skill_dir.relative_to(ROOT)}/")
        n_inj, n_skip = inject(skill_dir, dry_run=args.dry_run)
        total_injected += n_inj
        total_skipped += n_skip

    verb = "Would inject" if args.dry_run else "Done."
    print(f"\n{verb}: {total_injected} files injected, {total_skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
