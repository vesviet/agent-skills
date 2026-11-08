#!/usr/bin/env python3
"""Validate that every generated or hand-maintained artifact reports the pack VERSION.

Catches the drift class where VERSION is bumped but the A2A registry, agent cards,
or adapter templates are not regenerated.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT

VERSION_PATH = ROOT / "VERSION"


def pack_version() -> str:
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def check_agent_cards(version: str) -> list[str]:
    errors: list[str] = []
    cards = sorted((CORE_ROOT / "a2a" / "registry").glob("*.agent-card.json"))
    if not cards:
        return ["core/a2a/registry: no agent cards found"]
    for card in cards:
        data = json.loads(card.read_text(encoding="utf-8"))
        got = data.get("version")
        if got != version:
            errors.append(
                f"{card.relative_to(ROOT)}: version {got!r} != VERSION {version!r}"
                " (run core/scripts/generate-a2a-registry.py)"
            )
    return errors


def check_registry(version: str) -> list[str]:
    path = CORE_ROOT / "a2a" / ".well-known" / "agent-registry.json"
    if not path.is_file():
        return [f"{path.relative_to(ROOT)}: missing"]
    data = json.loads(path.read_text(encoding="utf-8"))
    got = data.get("pack_version")
    if got != version:
        return [
            f"{path.relative_to(ROOT)}: pack_version {got!r} != VERSION {version!r}"
            " (run core/scripts/generate-a2a-registry.py)"
        ]
    return []


# Files that state the pack version in prose or config and must be kept in sync.
# Each entry: (path, regex with one capture group holding the version)
PINNED = [
    ("adapters/antigravity/a2a-config.template.yaml", r"pack_version:\s*\"([0-9.]+)\""),
    ("adapters/claude/CLAUDE_ADAPTER.md", r"Pack version:\s*\*\*([0-9.]+)\*\*"),
    ("AGENTS.md", r"pack\s+([0-9]+\.[0-9]+\.[0-9]+)\)"),
    ("USER_GUIDE_v2.md", r"pack\s+([0-9]+\.[0-9]+\.[0-9]+)\)"),
    ("USER_GUIDE_v2.md", r"Pack version \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*"),
    ("README.md", r"\*\*Version ([0-9]+\.[0-9]+\.[0-9]+)\*\*"),
    ("CLAUDE.md", r"Pack version:\s*\*\*([0-9.]+)\*\*"),
    (".cursorrules", r"pack\s+([0-9]+\.[0-9]+\.[0-9]+)\)"),
    ("core/codex/.a2a-config.json", r"\"pack_version\":\s*\"([0-9.]+)\""),
    ("PACK_STATUS.md", r"VERSION \| `([0-9]+\.[0-9]+\.[0-9]+)`"),
]


def check_pinned(version: str) -> list[str]:
    errors: list[str] = []
    for rel, pattern in PINNED:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{rel}: missing (expected to pin the pack version)")
            continue
        text = path.read_text(encoding="utf-8")
        found = re.findall(pattern, text)
        if not found:
            errors.append(f"{rel}: no pack version found matching {pattern!r}")
            continue
        for got in found:
            if got != version:
                errors.append(f"{rel}: states {got!r} != VERSION {version!r}")
    return errors


def check_package_json(version: str) -> list[str]:
    path = ROOT / "package.json"
    if not path.is_file():
        return ["package.json: missing"]
    got = json.loads(path.read_text(encoding="utf-8")).get("version")
    if got != version:
        return [f"package.json: version {got!r} != VERSION {version!r}"]
    return []


def check_changelog(version: str) -> list[str]:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^##\s*\[?v?([0-9]+\.[0-9]+\.[0-9]+)", text)
    if not match:
        return ["CHANGELOG.md: no version heading found"]
    if match.group(1) != version:
        return [
            f"CHANGELOG.md: newest entry {match.group(1)!r} != VERSION {version!r}"
        ]
    return []


def check_no_stray_versions(version: str) -> list[str]:
    """Flag files that mention a pack-shaped version other than VERSION in a
    context that reads like the pack's own version."""
    errors: list[str] = []
    pattern = re.compile(r"agent-skills[ @v]+([0-9]+\.[0-9]+\.[0-9]+)")
    skip_parts = {".git", "__pycache__", "node_modules", ".agents"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or set(path.parts) & skip_parts:
            continue
        if path.suffix not in (".md", ".json", ".yaml", ".yml") and path.name != ".cursorrules":
            continue
        if path.name == "CHANGELOG.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for got in pattern.findall(text):
            if got != version:
                errors.append(
                    f"{path.relative_to(ROOT)}: references pack {got!r} != VERSION {version!r}"
                )
    return errors


def get_actual_catalog_counts() -> dict[str, int]:
    """Compute physical disk counts of catalog entities across agent-skills."""
    core_skills = len(list((CORE_ROOT / "skills").glob("*/*/SKILL.md")))
    overlay_skills = len(list(ROOT.glob("overlays/**/skills/*/SKILL.md")))
    total_skills = core_skills + overlay_skills
    workflows = len([
        p for p in (CORE_ROOT / "workflows").glob("*.md")
        if p.name not in ("README.md", "INDEX.md", "CONTRIBUTING.md")
    ])
    schemas = len(list((CORE_ROOT / "contracts" / "schemas").glob("*.json")))
    packs = len([p for p in (ROOT / "packs").iterdir() if p.is_dir()])
    overlays = len([p for p in (ROOT / "overlays").iterdir() if p.is_dir()])
    roles = len([
        p for p in (CORE_ROOT / "roles").glob("*.md")
        if p.name not in ("README.md", "role-standard.md", "INDEX.md")
    ])
    return {
        "roles": roles,
        "total_skills": total_skills,
        "core_skills": core_skills,
        "overlay_skills": overlay_skills,
        "workflows": workflows,
        "schemas": schemas,
        "packs": packs,
        "overlays": overlays,
    }


def validate_agents_catalog_counts(path: Path, label: str, counts: dict[str, int]) -> list[str]:
    """Verify that an AGENTS.md / CLAUDE.md document declares correct catalog counts matching disk counts."""
    if not path.is_file():
        return [f"{label}: file not found at {path}"]

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Summary line declarations
    roles_m = re.search(r"\*\*(\d+)\s*Roles\*\*", text)
    if roles_m:
        val = int(roles_m.group(1))
        exp = counts["roles"]
        if val != exp:
            errors.append(f"{label}: declared {val} Roles != actual {exp}")
    else:
        errors.append(f"{label}: missing '**<N> Roles**' declaration")

    skills_m = re.search(r"\*\*(\d+)\s*Skills\*\*", text)
    if skills_m:
        val = int(skills_m.group(1))
        exp = counts["total_skills"]
        if val != exp:
            errors.append(f"{label}: declared {val} Skills != actual {exp}")
    else:
        errors.append(f"{label}: missing '**<N> Skills**' declaration")

    core_m = re.search(r"\[(\d+)\s*Core|\((\d+)\s*Core", text)
    if core_m:
        val = int(core_m.group(1) or core_m.group(2))
        exp = counts["core_skills"]
        if val != exp:
            errors.append(f"{label}: declared {val} Core skills != actual {exp}")
    else:
        errors.append(f"{label}: missing '[<N> Core' or '(<N> Core' declaration")

    ov_m = re.search(r"\+\s*(\d+)\s*Overlays?[\]\)]", text)
    if ov_m:
        val = int(ov_m.group(1))
        exp = counts["overlay_skills"]
        if val != exp:
            errors.append(f"{label}: declared {val} Overlay skills != actual {exp}")
    else:
        errors.append(f"{label}: missing '+ <N> Overlays]' declaration")

    wf_m = re.search(r"\*\*(\d+)\s*Workflows\*\*", text)
    if wf_m:
        val = int(wf_m.group(1))
        exp = counts["workflows"]
        if val != exp:
            errors.append(f"{label}: declared {val} Workflows != actual {exp}")
    else:
        errors.append(f"{label}: missing '**<N> Workflows**' declaration")

    schema_m = re.search(r"\*\*(\d+)\s*(?:Data\s+Contract\s+)?Schemas\*\*", text)
    if schema_m:
        val = int(schema_m.group(1))
        exp = counts["schemas"]
        if val != exp:
            errors.append(f"{label}: declared {val} Schemas != actual {exp}")
    else:
        errors.append(f"{label}: missing '**<N> (Data Contract )Schemas**' declaration")

    packs_m = re.search(r"\*\*(\d+)\s*Packs\*\*", text)
    if packs_m:
        val = int(packs_m.group(1))
        exp = counts["packs"]
        if val != exp:
            errors.append(f"{label}: declared {val} Packs != actual {exp}")

    overlays_m = re.search(r"\*\*(\d+)\s*Overlays\*\*", text)
    if overlays_m:
        val = int(overlays_m.group(1))
        exp = counts["overlays"]
        if val != exp:
            errors.append(f"{label}: declared {val} Overlays != actual {exp}")

    # 2. Section mentions
    core_sec_m = re.search(r"Core skills\s*\((\d+)\s*across\s*22\s*categories\)", text)
    if core_sec_m:
        val = int(core_sec_m.group(1))
        exp = counts["core_skills"]
        if val != exp:
            errors.append(f"{label}: section declared {val} Core skills != actual {exp}")

    ov_sec_m = re.search(
        r"(?:Optional repo-specific|Overlay-specific) skills\s*\((\d+)\s*across\s*(\d+)\s*overlays\)",
        text,
    )
    if ov_sec_m:
        val1 = int(ov_sec_m.group(1))
        exp1 = counts["overlay_skills"]
        if val1 != exp1:
            errors.append(f"{label}: section declared {val1} Overlay skills != actual {exp1}")
        val2 = int(ov_sec_m.group(2))
        exp2 = counts["overlays"]
        if val2 != exp2:
            errors.append(f"{label}: section declared {val2} Overlays != actual {exp2}")

    return errors


def check_catalog_counts() -> list[str]:
    """Validate that in-repo AGENTS.md, workspace AGENTS.md, and in-repo CLAUDE.md match actual disk catalog counts."""
    counts = get_actual_catalog_counts()
    errors: list[str] = []

    # 1. In-repo AGENTS.md (mandatory)
    in_repo_agents = ROOT / "AGENTS.md"
    errors += validate_agents_catalog_counts(in_repo_agents, "AGENTS.md", counts)

    # 2. Workspace AGENTS.md (validated whenever present in workspace root)
    workspace_agents = ROOT.parent / "AGENTS.md"
    if workspace_agents.is_file():
        errors += validate_agents_catalog_counts(workspace_agents, "workspace AGENTS.md", counts)

    # 3. In-repo CLAUDE.md (validated whenever present)
    in_repo_claude = ROOT / "CLAUDE.md"
    if in_repo_claude.is_file():
        errors += validate_agents_catalog_counts(in_repo_claude, "CLAUDE.md", counts)

    return errors


def main() -> int:
    version = pack_version()
    errors: list[str] = []
    errors += check_registry(version)
    errors += check_agent_cards(version)
    errors += check_pinned(version)
    errors += check_package_json(version)
    errors += check_changelog(version)
    errors += check_no_stray_versions(version)
    errors += check_catalog_counts()

    if errors:
        print("Version and catalog sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Version and catalog sync validation passed: VERSION {version} consistent across registry, "
        f"cards, adapters, package.json, changelog, and AGENTS.md catalog counts."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
