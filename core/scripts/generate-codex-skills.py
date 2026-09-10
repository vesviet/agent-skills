#!/usr/bin/env python3
"""Generate OpenAI Codex skill descriptors (agents/openai.yaml) for all core skills.

Ensures 100% of skills in core/skills can be invoked via $skill-name in Codex CLI.
Run with --check to verify that all skills have valid descriptors without writing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import CORE_ROOT, parse_frontmatter

ACRONYMS = {
    "a2a": "A2A",
    "api": "API",
    "mcp": "MCP",
    "ui": "UI",
    "ux": "UX",
    "seo": "SEO",
    "sre": "SRE",
    "qa": "QA",
    "hvac": "HVAC",
    "db": "DB",
    "sql": "SQL",
    "ci": "CI",
    "cd": "CD",
    "iac": "IaC",
    "pr": "PR",
}


def title_case(slug: str) -> str:
    words = slug.split("-")
    capitalized = [ACRONYMS.get(w.lower(), w.capitalize()) for w in words]
    return " ".join(capitalized)


def clean_description(desc: str) -> str:
    # Strip "Use when..." or "Use for..." trigger phrases for short description
    desc = desc.strip().strip('"').strip("'")
    for trigger in ["Use when", "Use for", "use when", "use for"]:
        if trigger in desc:
            desc = desc.split(trigger)[0].strip()
    if desc.endswith((".", ",", ";", ":")):
        desc = desc[:-1].strip()
    if len(desc) > 80:
        desc = desc[:77] + "..."
    return desc or "Execute specialized engineering skill"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OpenAI Codex descriptors for core skills.")
    parser.add_argument("--check", action="store_true", help="Check for missing descriptors without writing.")
    parser.add_argument("--all", action="store_true", help="Overwrite existing descriptors.")
    args = parser.parse_args()

    skills_root = CORE_ROOT / "skills"
    missing = []
    generated = 0
    updated = 0

    for category in sorted(skills_root.iterdir()):
        if not category.is_dir():
            continue
        for skill_dir in sorted(category.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue

            openai_yaml = skill_dir / "agents" / "openai.yaml"
            if not openai_yaml.is_file():
                missing.append(skill_dir)

            if args.check:
                continue

            if openai_yaml.is_file() and not args.all:
                continue

            meta, body, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            name = meta.get("name", skill_dir.name)
            raw_desc = meta.get("description", "")
            disp_name = title_case(name)
            short_desc = clean_description(raw_desc)
            prompt = f"Use ${name} to execute {disp_name.lower()} tasks in this codebase."

            content = (
                "interface:\n"
                f'  display_name: "{disp_name}"\n'
                f'  short_description: "{short_desc}"\n'
                f'  default_prompt: "{prompt}"\n'
            )

            (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
            openai_yaml.write_text(content, encoding="utf-8")
            if openai_yaml.is_file():
                updated += 1
            else:
                generated += 1

    if args.check:
        if missing:
            print(f"Missing agents/openai.yaml in {len(missing)} core skills:")
            for m in missing:
                print(f"  - {m.relative_to(CORE_ROOT)}")
            return 1
        print("All core skills have valid agents/openai.yaml descriptors.")
        return 0

    print(f"Codex descriptors updated: {updated} written/verified across core skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
