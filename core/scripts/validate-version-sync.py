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
    skip_parts = {".git", "__pycache__", "node_modules"}
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


def main() -> int:
    version = pack_version()
    errors: list[str] = []
    errors += check_registry(version)
    errors += check_agent_cards(version)
    errors += check_pinned(version)
    errors += check_changelog(version)
    errors += check_no_stray_versions(version)

    if errors:
        print("Version sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Version sync validation passed: VERSION {version} consistent across registry, cards, adapters, changelog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
