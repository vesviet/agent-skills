#!/usr/bin/env python3
"""Generate a Mermaid dependency graph from skill cross-references."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "core" / "skills"


def main() -> int:
    edges: list[tuple[str, str]] = []

    for skill_path in sorted(SKILLS_ROOT.glob("*/*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        name_match = re.search(r"(?m)^name: ([a-z0-9-]+)$", text)
        if not name_match:
            continue
        name = name_match.group(1)

        for ref in re.findall(r"\*\*([a-z0-9-]+)\*\*:", text):
            if ref != name:
                edges.append((name, ref))

    if not edges:
        print("No skill cross-references found.", file=sys.stderr)
        return 1

    print("```mermaid")
    print("graph LR")
    for source, target in sorted(set(edges)):
        print(f"    {source} --> {target}")
    print("```")
    return 0


if __name__ == "__main__":
    sys.exit(main())
