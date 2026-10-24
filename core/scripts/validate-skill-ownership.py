#!/usr/bin/env python3
"""Validate skill ownership across roles and workflows.

Catches three drift classes the other validators miss:
  1. A skill that no role holds as Primary (nobody owns it, so Supporting use is unresolvable).
  2. A role that lists the same skill as both Primary and Supporting.
  3. A role whose Decision Boundaries disclaim a responsibility that one of its
     Primary skills grants (the content-manager `write-article` class of bug).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, SKILLS_ROOT

ROLE_ROOT = CORE_ROOT / "roles"
WORKFLOW_ROOT = CORE_ROOT / "workflows"


def role_files() -> list[Path]:
    return sorted(
        p for p in ROLE_ROOT.glob("*.md") if p.name not in {"README.md", "role-standard.md"}
    )


def core_skill_names() -> set[str]:
    return {p.parent.name for p in SKILLS_ROOT.glob("*/*/SKILL.md")}


def toolbox(text: str) -> tuple[set[str], set[str]]:
    prim = re.search(r"### Primary Skills\s*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
    sup = re.search(r"### Supporting Skills[^\n]*\n(.*?)(?=\n### |\n## |\Z)", text, re.S)
    p = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", prim.group(1))) if prim else set()
    s = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", sup.group(1))) if sup else set()
    return p, s


def section(text: str, heading: str) -> str:
    m = re.search(rf"(?m)^#{{2,3}} {re.escape(heading)}\s*\n(.*?)(?=\n#{{2,3}} |\Z)", text, re.S)
    return m.group(1) if m else ""


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skills = core_skill_names()

    primary_owners: dict[str, list[str]] = {name: [] for name in skills}
    supporting_users: dict[str, list[str]] = {name: [] for name in skills}

    for path in role_files():
        text = path.read_text(encoding="utf-8")
        prim, sup = toolbox(text)
        rel = path.relative_to(ROOT)

        both = prim & sup
        if both:
            errors.append(f"{rel}: {sorted(both)} listed as both Primary and Supporting")

        for name in prim:
            if name in primary_owners:
                primary_owners[name].append(path.stem)
        for name in sup:
            if name in supporting_users:
                supporting_users[name].append(path.stem)

        # A Primary skill must not be disclaimed by the role's own boundaries.
        boundaries = section(text, "Decision Boundaries") + section(text, "Role Boundaries")
        for name in sorted(prim):
            verb = name.replace("-", " ")
            if re.search(rf"does not\s+(?:\w+\s+){{0,3}}{re.escape(verb)}", boundaries, re.I):
                errors.append(
                    f"{rel}: '{name}' is a Primary skill but the role's boundaries"
                    f" disclaim '{verb}' — a Primary skill authorizes direct execution"
                )

    # Every skill used as Supporting must have at least one Primary owner to delegate to.
    for name, users in sorted(supporting_users.items()):
        if users and not primary_owners[name]:
            errors.append(
                f"core/roles: '{name}' is Supporting for {users} but Primary for no role"
                " — Supporting use requires a Primary owner to delegate to"
            )

    # Skills with no owner at all are dead inventory; report as a warning.
    for name in sorted(skills):
        if not primary_owners[name] and not supporting_users[name]:
            warnings.append(f"core/skills/{name}: referenced by no role toolbox")

    # Every skill a workflow step names must be reachable from a role tagged on that step.
    for path in sorted(WORKFLOW_ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for m in re.finditer(r"(?m)^#### \d+\..*?$", text):
            start = m.start()
            nxt = text.find("\n#### ", start + 1)
            body = text[start: nxt if nxt != -1 else len(text)]
            role_line = re.search(r"(?m)^Role:\s*(.+)$", body)
            if not role_line:
                errors.append(f"{rel}: step {m.group(0).strip()!r} has no Role: tag")
                continue
            tagged = {
                r.strip().lower().replace(" ", "-").replace("/", "-")
                for r in re.findall(r"\*\*(.+?)\*\*", role_line.group(1))
            }
            named = set(re.findall(r"skill:\s*`([a-z0-9-]+)`", body))
            for skill in sorted(named & skills):
                reachable = any(
                    skill in primary_owners.get(skill, []) or role in primary_owners[skill]
                    or role in supporting_users[skill]
                    for role in tagged
                )
                if not reachable:
                    errors.append(
                        f"{rel}: step {m.group(0).strip()!r} names skill '{skill}'"
                        f" which is in no toolbox of the tagged role(s) {sorted(tagged)}"
                    )

    for warning in warnings:
        print(f"warning: {warning}")

    if errors:
        print("Skill ownership validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    owned = sum(1 for v in primary_owners.values() if v)
    print(
        f"Skill ownership validation passed: {owned}/{len(skills)} core skills have a Primary owner;"
        " no Primary/Supporting conflicts; workflow steps resolve to tagged-role toolboxes."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
