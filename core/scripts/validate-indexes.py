#!/usr/bin/env python3
"""Validate that index documents actually cover what exists on disk.

Catches the drift class where a skill, schema, overlay, or pack is added but its
index entry and the declared counts are not updated.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, SKILLS_ROOT

SKILLS_INDEX = SKILLS_ROOT / "README.md"
CONTRACTS_INDEX = CORE_ROOT / "contracts" / "README.md"
OVERLAYS_INDEX = ROOT / "overlays" / "README.md"
PACKS_INDEX = ROOT / "packs" / "README.md"
ROOT_README = ROOT / "README.md"


def core_skills_by_category() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for category in sorted(p for p in SKILLS_ROOT.iterdir() if p.is_dir()):
        names = sorted(
            d.name for d in category.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()
        )
        if names:
            out[category.name] = names
    return out


def overlay_skills() -> list[str]:
    return sorted(p.parent.name for p in ROOT.glob("overlays/*/skills/*/SKILL.md"))


def check_skills_index() -> list[str]:
    errors: list[str] = []
    text = SKILLS_INDEX.read_text(encoding="utf-8")
    by_cat = core_skills_by_category()
    core_names = [n for names in by_cat.values() for n in names]
    ov_names = overlay_skills()

    # 1. every skill on disk is listed
    listed = set(re.findall(r"`([a-z0-9-]+)`", text))
    for category, names in by_cat.items():
        for name in names:
            if name not in listed:
                errors.append(f"core/skills/README.md: missing {category}/{name}")

    # 2. no listed bullet points at a skill that does not exist
    bullets = set(re.findall(r"(?m)^- `([a-z0-9-]+)`\s*$", text))
    on_disk = set(core_names) | set(ov_names)
    for name in sorted(bullets - on_disk):
        errors.append(f"core/skills/README.md: lists `{name}` which has no SKILL.md")

    # 3. the Counts line matches reality
    counts = re.search(
        r"\*\*Counts:\*\*\s*(\d+)\s*portable core skills.*?\+\s*(\d+)\s*overlay skills.*?=\s*\*\*(\d+)\s*total\*\*",
        text,
        re.S,
    )
    if not counts:
        errors.append("core/skills/README.md: Counts line not found or unparseable")
    else:
        declared_core, declared_ov, declared_total = (int(g) for g in counts.groups())
        if declared_core != len(core_names):
            errors.append(
                f"core/skills/README.md: Counts declares {declared_core} core skills, found {len(core_names)}"
            )
        if declared_ov != len(ov_names):
            errors.append(
                f"core/skills/README.md: Counts declares {declared_ov} overlay skills, found {len(ov_names)}"
            )
        if declared_total != len(core_names) + len(ov_names):
            errors.append(
                f"core/skills/README.md: Counts declares total {declared_total},"
                f" found {len(core_names) + len(ov_names)}"
            )

    # 4. per-category heading counts match, e.g. "### Agent (21)"
    #    A category may be split across a main heading plus H4 sub-headings, so
    #    sum every count that appears between this H3 and the next H3.
    sections = re.split(r"(?m)^### ", text)
    for chunk in sections[1:]:
        head = chunk.split("\n", 1)[0]
        m = re.match(r"(.+?)\s*\((\d+)\)\s*$", head)
        if not m:
            continue
        label = m.group(1).strip().lower().replace(" and ", "-").replace(" ", "-")
        category = {"security-data": "security-data"}.get(label, label)
        if category not in by_cat:
            continue
        declared = int(m.group(2))
        sub = sum(
            int(n) for n in re.findall(r"(?m)^#### .+?\((\d+)\)\s*$", chunk)
        )
        actual = len(by_cat[category])
        if declared + sub != actual and declared != actual:
            errors.append(
                f"core/skills/README.md: '### {head}' declares {declared}"
                f"{f' + {sub} in sub-headings' if sub else ''}, found {actual} on disk"
            )
    return errors


def check_contracts_index() -> list[str]:
    errors: list[str] = []
    text = CONTRACTS_INDEX.read_text(encoding="utf-8")
    schemas = sorted((CORE_ROOT / "contracts" / "schemas").glob("*.json"))
    for schema in schemas:
        if schema.name not in text and schema.stem not in text:
            errors.append(
                f"core/contracts/README.md: missing row for {schema.name}"
                " (see CONTRIBUTING.md 'Adding a New Contract')"
            )
    return errors


def check_overlays_and_packs() -> list[str]:
    errors: list[str] = []
    ov_text = OVERLAYS_INDEX.read_text(encoding="utf-8")
    root_text = ROOT_README.read_text(encoding="utf-8")
    for path in sorted(p for p in (ROOT / "overlays").iterdir() if p.is_dir()):
        if path.name not in ov_text:
            errors.append(f"overlays/README.md: missing {path.name}")
        if path.name not in root_text:
            errors.append(f"README.md: overlay {path.name} not listed")

    pk_text = PACKS_INDEX.read_text(encoding="utf-8")
    for path in sorted(p for p in (ROOT / "packs").iterdir() if p.is_dir()):
        if path.name not in pk_text:
            errors.append(f"packs/README.md: missing {path.name}")
    return errors


def check_role_and_workflow_indexes() -> list[str]:
    errors: list[str] = []
    roles_text = (CORE_ROOT / "roles" / "README.md").read_text(encoding="utf-8")
    for path in sorted((CORE_ROOT / "roles").glob("*.md")):
        if path.name in ("README.md", "role-standard.md"):
            continue
        if path.stem not in roles_text:
            errors.append(f"core/roles/README.md: missing {path.stem}")

    wf_text = (CORE_ROOT / "workflows" / "README.md").read_text(encoding="utf-8")
    root_text = ROOT_README.read_text(encoding="utf-8")
    for path in sorted((CORE_ROOT / "workflows").glob("*.md")):
        if path.name == "README.md":
            continue
        if path.stem not in wf_text:
            errors.append(f"core/workflows/README.md: missing {path.stem}")
        if path.stem not in root_text:
            errors.append(f"README.md: workflow /{path.stem} not listed")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_skills_index()
    errors += check_contracts_index()
    errors += check_overlays_and_packs()
    errors += check_role_and_workflow_indexes()

    if errors:
        print("Index validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Index validation passed: skills, contracts, roles, workflows, overlays, packs all indexed with correct counts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
