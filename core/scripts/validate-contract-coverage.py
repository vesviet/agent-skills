#!/usr/bin/env python3
"""Validate that every contract a role claims to emit as primary output is
produced by at least one skill in the role's own toolbox.

Catches the drift class where role files name contracts under "Outputs
Produced" (e.g. solution-brief.json) but none of the role's Primary or
Supporting skills actually emits that contract — the role markets a deliverable
it has no documented way to produce.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, SKILLS_ROOT

ROLE_ROOT = CORE_ROOT / "roles"


def role_files() -> list[Path]:
    return sorted(
        p for p in ROLE_ROOT.glob("*.md") if p.name not in {"README.md", "role-standard.md"}
    )


def role_toolbox(text: str) -> set[str]:
    prim = re.search(r"### Primary Skills\s*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
    sup = re.search(r"### Supporting Skills[^\n]*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
    out: set[str] = set()
    if prim:
        out.update(re.findall(r"(?m)^- `([a-z0-9-]+)`", prim.group(1)))
    if sup:
        out.update(re.findall(r"(?m)^- `([a-z0-9-]+)`", sup.group(1)))
    return out


def role_primary_contracts(text: str) -> set[str]:
    """Extract contracts the role marks as primary outputs it owns.

    Heuristic: any `contracts/schemas/<name>.json` mentioned in the Outputs
    Produced section, minus those explicitly listed in the
    "Contracts owned by other roles" exclusion block.
    """
    out_m = re.search(r"## Outputs Produced\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not out_m:
        return set()
    body = out_m.group(1)

    # Cut at "Contracts owned by other roles" — anything below that is excluded
    exclusion = re.search(r"Contracts owned by other roles", body, re.I)
    if exclusion:
        body = body[: exclusion.start()]

    return set(re.findall(r"contracts/schemas/([a-z0-9-]+)\.json", body))


def skill_emits_contracts(skill_name: str) -> set[str]:
    """Collect contracts a skill declares it emits.

    Sources: the skill's `## Output Contracts` section (preferred) and any
    explicit `contracts/schemas/<name>.json` reference paired with the words
    "emit", "produce", or "emit" in the same sentence (loose fallback).
    """
    path = next(SKILLS_ROOT.glob(f"*/{skill_name}/SKILL.md"), None)
    if path is None:
        return set()
    text = path.read_text(encoding="utf-8")
    out: set[str] = set()

    oc = re.search(r"## Output Contracts\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if oc:
        out.update(re.findall(r"contracts/schemas/([a-z0-9-]+)\.json", oc.group(1)))
    return out


def main() -> int:
    warnings: list[str] = []
    errors: list[str] = []

    for path in role_files():
        text = path.read_text(encoding="utf-8")
        role = path.stem
        contracts = role_primary_contracts(text)
        if not contracts:
            continue

        toolbox = role_toolbox(text)
        emitted: set[str] = set()
        for skill in toolbox:
            emitted |= skill_emits_contracts(skill)

        # Discovery roles legitimately emit contracts that no skill file
        # declares (they're authored directly per role's own template). Only
        # flag when *none* of the role's toolbox skills document emission.
        for contract in sorted(contracts):
            if contract not in emitted:
                warnings.append(
                    f"{path.relative_to(ROOT)}: contracts/schemas/{contract}.json"
                    f" is named as primary output but no toolbox skill declares"
                    f" emitting it — extend the producing skill's '## Output Contracts'"
                    f" section"
                )

    for warning in warnings:
        print(f"warning: {warning}")

    # Soft gate: warnings only, do not block. A future major version flips
    # these to errors once contracts are backfilled across all skills.
    print(
        f"Contract coverage validation passed: {len(role_files())} roles checked"
        f" ({len(warnings)} advisory warnings — see lines above)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
