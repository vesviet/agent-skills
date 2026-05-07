#!/usr/bin/env python3
"""Validate global rules and adapter mirrors."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "core" / "rules" / "code.md"
ADAPTERS = (
    ROOT / ".cursorrules",
    ROOT / ".cursor" / "rules" / "agent-skills.md",
    ROOT / "CLAUDE.md",
    ROOT / "AGENTS.md",
    ROOT / ".github" / "copilot-instructions.md",
)

SOURCE_REQUIRED = (
    "trigger: always_on",
    'glob: "**"',
    "Before finalizing any response or executing a command, verify the action against `core/rules/code.md`",
    "Do not create a commit unless the user explicitly confirms",
    "Do not push commits, create tags, or publish releases unless the user explicitly confirms",
    "Ensure all code changes pass local linters, unit tests, and build checks before creating a commit",
    "Do not expose secrets, credentials, tokens, private keys, or sensitive internal values",
    "Do not mention agents, AI workflow, review labels, severity labels, task trackers",
    "Prefer repo-local standards, templates, and workflows when they exist",
    "Do not invent repository conventions, paths, branching models, or release rules",
    "Keep code comments implementation-focused and useful",
)

ADAPTER_GROUPS = {
    "rule_source": (
        "core/rules/code.md",
    ),
    "meta_rule": (
        "Before finalizing any response or executing a command",
        "halt and ask the user",
    ),
    "approval_gates": (
        "create a commit unless the user explicitly confirms",
        "push",
        "publish",
        "Ensure all code changes pass local linters",
    ),
    "artifact_safety": (
        "expose secrets",
        "mention agents, AI workflow",
        "Prefer repo-local standards",
    ),
    "role_enforcement": (
        "role-standard",
        "Skill Toolbox",
        "core responsibilities",
    ),
    "workflow_discipline": (
        "checklist",
        "ONE step at a time",
        "Role:",
    ),
}

FORBIDDEN = (
    "thought process",
    "P0/P1/P2",
)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def validate_source() -> list[str]:
    text = SOURCE.read_text(encoding="utf-8")
    flat = normalized(text)
    errors: list[str] = []

    for required in SOURCE_REQUIRED:
        if normalized(required) not in flat:
            errors.append(f"core/rules/code.md missing required rule text: {required}")

    for forbidden in FORBIDDEN:
        if forbidden in text:
            errors.append(f"core/rules/code.md contains forbidden wording: {forbidden}")

    if text.count("---") < 2:
        errors.append("core/rules/code.md missing frontmatter delimiters")

    return errors


def validate_adapters() -> list[str]:
    errors: list[str] = []
    for path in ADAPTERS:
        if not path.exists():
            errors.append(f"missing adapter file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        flat = normalized(text)
        rel = path.relative_to(ROOT)
        for group_name, required_items in ADAPTER_GROUPS.items():
            missing = [
                required
                for required in required_items
                if normalized(required) not in flat
            ]
            if missing:
                errors.append(
                    f"{rel} missing adapter parity group '{group_name}': {', '.join(missing)}"
                )
        for forbidden in FORBIDDEN:
            if forbidden in text:
                errors.append(f"{rel} contains forbidden wording: {forbidden}")
    return errors


def main() -> int:
    errors = validate_source() + validate_adapters()

    if errors:
        print("Rules validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Rules validation passed: source and adapters checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
