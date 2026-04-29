#!/usr/bin/env python3
"""Validate workflow structure, role ownership, and references."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_ROOT = ROOT / "workflows"
ROLE_ROOT = ROOT / "role"
SKILLS_ROOT = ROOT / "skills"

REQUIRED_SECTIONS = (
    "### Prerequisites",
    "### Workflow Steps",
    "### Checklist",
    "### Related Workflows",
    "### Related Skills",
)

ROLE_ALIASES = {
    "SRE": "Site Reliability Engineer",
}

README_PLACEHOLDERS = {
    "description",
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text, ["missing YAML frontmatter"]
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, text, ["unterminated YAML frontmatter"]

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, "\n".join(lines[end + 1 :]), errors


def section_text(body: str, heading: str) -> str:
    marker = f"{heading}\n"
    start = body.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    level = len(heading.split(" ", 1)[0])
    match = re.search(rf"(?m)^#{{1,{level}}} .+", body[start:])
    if match:
        return body[start : start + match.start()]
    return body[start:]


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


def slug(text: str) -> str:
    value = text.strip().lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def collect_skill_names() -> set[str]:
    names: set[str] = set()
    for path in SKILLS_ROOT.glob("*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name: ([a-z0-9-]+)$", text)
        if match:
            names.add(match.group(1))
    return names


def collect_role_names() -> set[str]:
    names: set[str] = set()
    for path in ROLE_ROOT.glob("*.md"):
        if path.name in {"README.md", "role-standard.md"}:
            continue
        first_line = path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        names.add(first_line)
    return names


def workflow_files() -> list[Path]:
    return sorted(path for path in WORKFLOWS_ROOT.glob("*.md") if path.name != "README.md")


def validate_workflow(path: Path, workflows: set[str], skills: set[str], roles: set[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    metadata, body, errors = parse_frontmatter(text)

    description = metadata.get("description", "")
    if not description:
        errors.append("missing description frontmatter")
    elif len(description) > 240:
        errors.append("description should stay concise")

    body_without_fences = strip_fenced_blocks(body)
    h2_lines = [line for line in body_without_fences.splitlines() if line.startswith("## ")]
    if len(h2_lines) != 1:
        errors.append("body must contain exactly one H2 workflow title")
    elif not h2_lines[0].endswith(" Workflow"):
        errors.append("workflow title should end with 'Workflow'")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"missing required section: {section}")

    step_numbers = [int(match) for match in re.findall(r"(?m)^#### (\d+)\. ", body)]
    if not step_numbers:
        errors.append("workflow must define numbered #### steps")
    elif step_numbers != list(range(1, len(step_numbers) + 1)):
        errors.append("workflow step numbers must be sequential from 1")

    step_blocks = re.split(r"(?m)^#### \d+\. .+$", body)
    step_headings = re.findall(r"(?m)^#### \d+\. .+$", body)
    for heading, block in zip(step_headings, step_blocks[1:]):
        role_line = re.search(r"(?m)^Role: (.+)$", block)
        if not role_line:
            errors.append(f"{heading} missing Role line")
            continue
        for role in re.findall(r"\*\*([^*]+)\*\*", role_line.group(1)):
            canonical = ROLE_ALIASES.get(role, role)
            if canonical not in roles:
                errors.append(f"{heading} references unknown role: {role}")

    checklist = section_text(body, "### Checklist")
    checklist_items = re.findall(r"(?m)^- \[ \] .+", checklist)
    if "### Checklist" in body and len(checklist_items) < max(5, min(len(step_numbers), 10)):
        errors.append("Checklist should cover the workflow's major steps")

    related_workflows = re.findall(r"\]\(([a-z0-9-]+)\.md\)", section_text(body, "### Related Workflows"))
    for workflow in related_workflows:
        if workflow not in workflows:
            errors.append(f"Related Workflows references unknown workflow: {workflow}")

    related_skills = re.findall(r"(?m)^- \*\*([a-z0-9-]+)\*\*: .+", section_text(body, "### Related Skills"))
    if "### Related Skills" in body and not related_skills:
        errors.append("Related Skills should use '- **skill-name**: description' items")
    for skill in related_skills:
        if skill not in skills:
            errors.append(f"Related Skills references unknown skill: {skill}")

    inline_skills = re.findall(r"Use skill: `([a-z0-9-]+)`", body)
    for skill in inline_skills:
        if skill not in skills:
            errors.append(f"inline skill reference is unknown: {skill}")

    if re.search(r"\bP[0-9]\b", body):
        errors.append("workflow should not use P0/P1/P2 labels; use Blocking, Important, Follow-Up")

    return [f"{rel}: {error}" for error in errors]


def validate_readme(workflows: set[str], skills: set[str]) -> list[str]:
    path = WORKFLOWS_ROOT / "README.md"
    body = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for workflow in workflows:
        if f"]({workflow}.md)" not in body:
            errors.append(f"workflows/README.md missing listing for {workflow}.md")

    for skill in re.findall(r"`([a-z0-9-]+)`", body):
        if skill in README_PLACEHOLDERS:
            continue
        if skill not in skills:
            errors.append(f"workflows/README.md references unknown skill: {skill}")

    if "## Workflow Authoring Standard" not in body:
        errors.append("workflows/README.md missing Workflow Authoring Standard section")
    if "## Validation Gate" not in body:
        errors.append("workflows/README.md missing Validation Gate section")

    return errors


def main() -> int:
    paths = workflow_files()
    workflows = {path.stem for path in paths}
    skills = collect_skill_names()
    roles = collect_role_names()
    errors: list[str] = []

    if not paths:
        errors.append("no workflow files found")

    for path in paths:
        errors.extend(validate_workflow(path, workflows, skills, roles))
    errors.extend(validate_readme(workflows, skills))

    if errors:
        print("Workflow validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Workflow validation passed: {len(paths)} workflows checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
