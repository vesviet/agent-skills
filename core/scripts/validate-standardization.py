#!/usr/bin/env python3
"""Validate pack standardization target (>=90% coverage checklist)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, collect_skill_names


ROLE_ROOT = CORE_ROOT / "roles"
AGENT_SKILL_PREFIX = "agent-"

ADAPTERS = (
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / ".cursorrules",
    ROOT / ".cursor" / "rules" / "agent-skills.md",
    ROOT / ".github" / "copilot-instructions.md",
)

REQUIRED_PATHS = (
    ROOT / "adapters" / "antigravity" / "ANTIGRAVITY.md",
    ROOT / "adapters" / "cursor" / "hooks.template.json",
    CORE_ROOT / "prompts" / "golden" / "README.md",
    CORE_ROOT / "policies" / "mcp-tool-map.yaml",
    CORE_ROOT / "contracts" / "schemas" / "a2a-push-notification-config.json",
    CORE_ROOT / "contracts" / "schemas" / "a2a-task-cancel.json",
    CORE_ROOT / "contracts" / "schemas" / "agent-trace-span.json",
)

ORPHAN_SKILLS_MUST_BE_WIRED = ("agent-prompt-lifecycle", "agent-semantic-memory")

ROLES_NEEDING_CONTRACTS = (
    "qa-engineer",
    "agent-coordinator",
)


def agent_skills_in_roles() -> tuple[set[str], set[str]]:
    agent_skills = {n for n in collect_skill_names() if n.startswith(AGENT_SKILL_PREFIX)}
    used: set[str] = set()
    for path in ROLE_ROOT.glob("*.md"):
        if path.name in {"README.md", "role-standard.md"}:
            continue
        body = path.read_text(encoding="utf-8")
        for skill in agent_skills:
            if f"`{skill}`" in body:
                used.add(skill)
    return agent_skills, used


def adapter_parity() -> list[str]:
    errors: list[str] = []
    needles = ("antigravity", "agent-registry", "agent-a2a-protocol")
    for path in ADAPTERS:
        if not path.is_file():
            errors.append(f"missing adapter: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        missing = [n for n in needles if n not in text]
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)} missing: {', '.join(missing)}"
            )
    return errors


def role_contract_checks() -> list[str]:
    errors: list[str] = []
    for stem in ROLES_NEEDING_CONTRACTS:
        path = ROLE_ROOT / f"{stem}.md"
        body = path.read_text(encoding="utf-8")
        if stem == "qa-engineer" and "validation-result.json" not in body:
            errors.append(f"{stem}.md: missing validation-result.json reference")
    return errors


def score_report(agent_skills: set[str], used: set[str]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checks = 0
    passed = 0

    def check(ok: bool, label: str) -> None:
        nonlocal checks, passed
        checks += 1
        if ok:
            passed += 1
        elif label:
            errors.append(label)

    for path in REQUIRED_PATHS:
        check(path.is_file(), f"missing: {path.relative_to(ROOT)}")

    for skill in ORPHAN_SKILLS_MUST_BE_WIRED:
        check(skill in used, f"skill not wired to any role: {skill}")

    orphan = agent_skills - used
    check(len(orphan) == 0, f"agent skills unused: {sorted(orphan)}")

    adapter_errors = adapter_parity()
    check(len(adapter_errors) == 0, "")
    errors.extend(adapter_errors)

    contract_errors = role_contract_checks()
    check(len(contract_errors) == 0, "")
    errors.extend(contract_errors)

    pct = int((passed / checks) * 100) if checks else 0
    return pct, errors


def main() -> int:
    agent_skills, used = agent_skills_in_roles()
    pct, errors = score_report(agent_skills, used)

    print(f"Standardization score: {pct}% ({len(agent_skills)} agent skills, {len(used)} wired)")

    if pct < 90:
        print("Standardization below 90% target:")
        for e in errors:
            print(f"- {e}")
        return 1

    if errors:
        print("Warnings (score >= 90%):")
        for e in errors:
            print(f"- {e}")

    print("Standardization validation passed (>=90%).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
