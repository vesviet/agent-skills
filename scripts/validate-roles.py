#!/usr/bin/env python3
"""Validate role definitions and role-to-skill mappings."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLE_ROOT = ROOT / "role"
SKILLS_ROOT = ROOT / "skills"
WORKFLOWS_ROOT = ROOT / "workflows"

REQUIRED_SECTIONS = (
    "## Principal Expectations",
    "## Use This Role When",
    "## Core Responsibilities",
    "## Inputs Required",
    "## Outputs Produced",
    "## Decision Boundaries",
    "## Collaboration",
    "## Guardrails",
    "## Skill Toolbox",
    "### Primary Skills",
    "### Supporting Skills (use when collaborating)",
    "## Output Template",
    "## Review Checklist",
    "## Anti-Patterns To Reject",
    "## Role Handoff",
    "## Definition Of Done",
)

MIN_ITEMS = {
    "## Principal Expectations": 4,
    "## Use This Role When": 3,
    "## Core Responsibilities": 4,
    "## Inputs Required": 4,
    "## Outputs Produced": 4,
    "## Decision Boundaries": 3,
    "## Collaboration": 3,
    "## Guardrails": 3,
    "### Primary Skills": 1,
    "## Review Checklist": 5,
    "## Anti-Patterns To Reject": 4,
    "## Role Handoff": 3,
    "## Definition Of Done": 4,
}

ROLE_SLUG_ALIASES = {
    "sre": {"site-reliability-engineer"},
    "site-reliability-engineer": {"sre"},
}


def slug(text: str) -> str:
    value = text.strip().lower().replace("&", "and")
    value = value.replace("/", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def equivalent_role_slug(left: str, right: str) -> bool:
    return left == right or right in ROLE_SLUG_ALIASES.get(left, set())


def strip_fenced_blocks(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def section_text(body: str, heading: str) -> str:
    marker = f"{heading}\n"
    start = body.find(marker)
    if start == -1:
        return ""
    start += len(marker)

    level = len(heading.split(" ", 1)[0])
    next_pattern = re.compile(rf"(?m)^#{{2,{level}}} .+")
    match = next_pattern.search(body, start)
    if match:
        return body[start : match.start()]
    return body[start:]


def bullet_count(text: str) -> int:
    return len(re.findall(r"(?m)^- .+", text))


def collect_skill_names() -> set[str]:
    names: set[str] = set()
    for path in SKILLS_ROOT.glob("*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name: ([a-z0-9-]+)$", text)
        if match:
            names.add(match.group(1))
    return names


def collect_workflow_names() -> set[str]:
    return {
        path.stem
        for path in WORKFLOWS_ROOT.glob("*.md")
        if path.name != "README.md"
    }


def role_files() -> list[Path]:
    return sorted(
        path
        for path in ROLE_ROOT.glob("*.md")
        if path.name not in {"README.md", "role-standard.md"}
    )


def validate_role(path: Path, known_skills: set[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    body = path.read_text(encoding="utf-8")
    errors: list[str] = []

    body_without_fences = strip_fenced_blocks(body)
    h1_lines = [line for line in body_without_fences.splitlines() if line.startswith("# ")]
    if len(h1_lines) != 1:
        errors.append("must contain exactly one H1 role title")
    elif not equivalent_role_slug(path.stem, slug(h1_lines[0].lstrip("# "))):
        errors.append(f"H1 title does not match filename: {h1_lines[0]}")

    if not re.search(r"(?m)^Mission: .+", body):
        errors.append("missing Mission line")
    if not re.search(r"(?m)^Level: .+", body):
        errors.append("missing Level line")
    if "This role must follow [role-standard](role-standard.md) first." not in body:
        errors.append("missing mandatory role-standard reference")

    last_index = -1
    for section in REQUIRED_SECTIONS:
        index = body.find(section)
        if index == -1:
            errors.append(f"missing required section: {section}")
            continue
        if index < last_index:
            errors.append(f"section out of order: {section}")
        last_index = index

    for section, minimum in MIN_ITEMS.items():
        content = section_text(body, section)
        if content and bullet_count(content) < minimum:
            errors.append(f"{section} should contain at least {minimum} bullet items")

    output_template = section_text(body, "## Output Template")
    if "## Output Template" in body and "```markdown" not in output_template:
        errors.append("Output Template should include a markdown fenced template")

    primary = re.findall(r"(?m)^- `([a-z0-9-]+)`", section_text(body, "### Primary Skills"))
    supporting = re.findall(r"(?m)^- `([a-z0-9-]+)`", section_text(body, "### Supporting Skills (use when collaborating)"))

    if not primary:
        errors.append("must define at least one Primary Skill")
    for skill in primary + supporting:
        if skill not in known_skills:
            errors.append(f"references unknown skill: {skill}")
    overlap = set(primary).intersection(supporting)
    for skill in sorted(overlap):
        errors.append(f"skill appears in both primary and supporting toolbox: {skill}")

    return [f"{rel}: {error}" for error in errors]


def validate_readme(role_paths: list[Path], workflows: set[str]) -> list[str]:
    path = ROLE_ROOT / "README.md"
    body = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for role_path in role_paths:
        expected_link = f"[{role_path.stem}]({role_path.name})"
        if expected_link not in body:
            errors.append(f"role/README.md: missing role listing for {role_path.name}")

    table_lines = [
        line for line in body.splitlines()
        if line.startswith("| ") and "`/" in line
    ]
    mapped_roles: set[str] = set()
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        mapped_roles.add(slug(cells[0]))
        for workflow in re.findall(r"`/([a-z0-9-]+)`", cells[1]):
            if workflow not in workflows:
                errors.append(f"role/README.md: unknown workflow reference: /{workflow}")

    for role_path in role_paths:
        h1 = role_path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        h1_slug = slug(h1)
        if not any(equivalent_role_slug(mapped, h1_slug) for mapped in mapped_roles):
            errors.append(f"role/README.md: missing workflow mapping for {h1}")

    if "## Role Authoring Standard" not in body:
        errors.append("role/README.md: missing Role Authoring Standard section")
    if "## Validation Gate" not in body:
        errors.append("role/README.md: missing Validation Gate section")

    return errors


def main() -> int:
    known_skills = collect_skill_names()
    workflows = collect_workflow_names()
    roles = role_files()
    errors: list[str] = []

    if not roles:
        errors.append("no role files found")
    if not known_skills:
        errors.append("no skills found for toolbox validation")

    for path in roles:
        errors.extend(validate_role(path, known_skills))

    errors.extend(validate_readme(roles, workflows))

    if errors:
        print("Role validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Role validation passed: {len(roles)} roles checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
