#!/usr/bin/env python3
"""Validate the engineering skill pack without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import (
    ROOT,
    CORE_ROOT,
    SKILLS_ROOT,
    collect_skill_files,
    collect_skill_names,
    parse_frontmatter,
    section_text,
    slug,
    strip_fenced_blocks,
)


SKILL_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
REQUIRED_SECTIONS = (
    "## Core Rules",
    "## Suggested Process",
    "## Checklist",
    "## Related Skills",
)
KNOWN_WORKFLOWS = {
    "add-new-feature",
    "agent-a2a-delegation",
    "build-deploy",
    "content-audit",
    "content-publishing",
    "data-migration",
    "dependency-upgrade",
    "hotfix-production",
    "qa-validation",
    "refactoring",
    "revert-deployment",
    "security-incident-response",
    "seo-content-lifecycle",
    "seo-keyword-brief",
    "service-review-release",
    "setup-new-service",
    "tech-repo-review",
    "troubleshooting",
}
PLACEHOLDER_REFS = {
    "description",
    "true",
    "false",
    "yes",
    "no",
    "carry-over",
    "up",
    "down",
    "confidential",
    "restricted",
    "pip-audit",
    "npm audit",
    "high-risk",
    "deep",
    "scoped",
    "markdown-brief",
    "findings",
    "confidence",
    "slug",
    # Well-known endpoint identifiers used inside core/roles/*.md prose (URIs, not skills)
    "oauth-protected-resource",
    "oauth-authorization-server",
    "api-catalog",
    "data-ai-generated",
}


def slug_from_h1(line: str) -> str:
    title = line.lstrip("#").strip().lower()
    title = title.replace("&", "and")
    title = re.sub(r"[^a-z0-9]+", "-", title)
    return title.strip("-")


def validate_skill(path: Path, known_skills: set[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    metadata, body, errors = parse_frontmatter(text)

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
    for folder in ("roles", "workflows"):
        for path in sorted((CORE_ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for ref in re.findall(r"`([a-z0-9-]+)`", text):
                if ref in KNOWN_WORKFLOWS or ref in PLACEHOLDER_REFS:
                    continue
                if ref not in known_skills and (CORE_ROOT / folder / f"{ref}.md").exists() is False:
                    errors.append(f"{path.relative_to(ROOT)}: unknown referenced skill or local doc: {ref}")
    return errors


def main() -> int:
    skill_files = collect_skill_files()
    errors: list[str] = []

    if not skill_files:
        errors.append("no skill files found under core/skills/*/*/SKILL.md or overlays/*/skills/*/SKILL.md")

    known_skills = collect_skill_names()

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
