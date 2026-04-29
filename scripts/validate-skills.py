#!/usr/bin/env python3
"""Validate the engineering skill pack without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
REQUIRED_SECTIONS = (
    "## Core Rules",
    "## Suggested Process",
    "## Checklist",
    "## Related Skills",
)
KNOWN_WORKFLOWS = {
    "add-new-feature",
    "build-deploy",
    "hotfix-production",
    "refactoring",
    "revert-deployment",
    "service-review-release",
    "setup-new-service",
    "troubleshooting",
}
PLACEHOLDER_REFS = {
    "description",
}


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, str], str, list[str]]:
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

    body = "\n".join(lines[end + 1 :])
    return metadata, body, errors


def slug_from_h1(line: str) -> str:
    title = line.lstrip("#").strip().lower()
    title = title.replace("&", "and")
    title = re.sub(r"[^a-z0-9]+", "-", title)
    return title.strip("-")


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
    next_heading = body.find("\n## ", start)
    if next_heading == -1:
        return body[start:]
    return body[start:next_heading]


def collect_skill_names(skill_files: list[Path]) -> set[str]:
    names: set[str] = set()
    for path in skill_files:
        metadata, _, _ = parse_frontmatter(path, path.read_text(encoding="utf-8"))
        name = metadata.get("name")
        if name:
            names.add(name)
    return names


def validate_skill(path: Path, known_skills: set[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    metadata, body, errors = parse_frontmatter(path, text)

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if not name:
        errors.append("missing frontmatter field: name")
    elif not SKILL_NAME_RE.fullmatch(name):
        errors.append("name must be lowercase letters, numbers, and hyphens, max 64 chars")
    elif path.parent.name != name:
        errors.append(f"name does not match directory name: {path.parent.name}")

    if not description:
        errors.append("missing frontmatter field: description")
    else:
        if len(description) > 1024:
            errors.append("description exceeds 1024 characters")
        if "Use when " not in description and "Use for " not in description:
            errors.append('description must include a trigger phrase such as "Use when" or "Use for"')
        if description.startswith(("I ", "You ")):
            errors.append("description must be written in third person")

    body_without_fences = strip_fenced_blocks(body)
    h1_lines = [line for line in body_without_fences.splitlines() if line.startswith("# ")]
    if len(h1_lines) != 1:
        errors.append("body must contain exactly one H1 title")
    elif name and slug_from_h1(h1_lines[0]) != name:
        errors.append(f"H1 title does not match skill name: {h1_lines[0]}")
    elif h1_lines[0].endswith(" Skill"):
        errors.append("H1 title should not end with 'Skill'")

    if len(body.splitlines()) > 500:
        errors.append("SKILL.md body exceeds 500 lines")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"missing required section: {section}")

    checklist = section_text(body, "## Checklist")
    checklist_items = re.findall(r"(?m)^- \[ \] .+", checklist)
    if "## Checklist" in body and len(checklist_items) < 5:
        errors.append("Checklist should contain at least 5 actionable items")

    related = section_text(body, "## Related Skills")
    related_items = re.findall(r"(?m)^- \*\*([a-z0-9-]+)\*\*: .+", related)
    if "## Related Skills" in body and not related_items:
        errors.append("Related Skills should use '- **skill-name**: description' items")
    for related_name in related_items:
        if related_name not in known_skills:
            errors.append(f"Related Skills references unknown skill: {related_name}")

    use_skill_refs = re.findall(r"Use skill: `([a-z0-9-]+)`", body)
    for ref in use_skill_refs:
        if ref not in known_skills:
            errors.append(f"inline skill reference is unknown: {ref}")

    return [f"{rel}: {error}" for error in errors]


def validate_skill_references(known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    for folder in ("role", "workflows"):
        for path in sorted((ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for ref in re.findall(r"`([a-z0-9-]+)`", text):
                if ref in KNOWN_WORKFLOWS or ref in PLACEHOLDER_REFS:
                    continue
                if ref not in known_skills and (ROOT / folder / f"{ref}.md").exists() is False:
                    errors.append(f"{path.relative_to(ROOT)}: unknown referenced skill or local doc: {ref}")
    return errors


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    errors: list[str] = []

    if not skill_files:
        errors.append("no skill files found under skills/*/*/SKILL.md")

    known_skills = collect_skill_names(skill_files)

    for path in skill_files:
        errors.extend(validate_skill(path, known_skills))

    errors.extend(validate_skill_references(known_skills))

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {len(skill_files)} skills checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
