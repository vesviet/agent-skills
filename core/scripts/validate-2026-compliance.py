#!/usr/bin/env python3
"""Validate 2026 agent standards: A2A, contracts, graph orchestration, and policy coverage."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, collect_skill_names, slug


ROLE_ROOT = CORE_ROOT / "roles"
POLICY_PATH = CORE_ROOT / "policies" / "action-boundaries.yaml"
TOOL_ORCH = CORE_ROOT / "skills" / "agent" / "agent-tool-orchestration" / "SKILL.md"
GRAPH_SKILL = CORE_ROOT / "skills" / "agent" / "agent-graph-orchestration" / "SKILL.md"
COORD_PLAN = CORE_ROOT / "contracts" / "schemas" / "coordination-plan.json"

COORDINATOR = "agent-coordinator"
COORDINATOR_PRIMARY = {"agent-delegation", "agent-graph-orchestration"}

A2A_MARKERS = (
    "Collaboration & A2A Delegation",
    "contracts/schemas/",
)

EXCLUDED_ROLES = {"README.md", "role-standard.md"}


def role_files() -> list[Path]:
    return sorted(
        p for p in ROLE_ROOT.glob("*.md") if p.name not in EXCLUDED_ROLES
    )


def policy_roles() -> set[str]:
    text = POLICY_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"^  ([a-z0-9-]+):\n", text, re.M))


def primary_skills(body: str) -> set[str]:
    match = re.search(r"### Primary Skills\n(.*?)(?=\n### |\n## )", body, re.S)
    if not match:
        return set()
    return set(re.findall(r"(?m)^- `([a-z0-9-]+)`", match.group(1)))


def has_a2a_or_contracts(body: str) -> bool:
    return any(marker in body for marker in A2A_MARKERS)


def validate_coordinator(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    body = path.read_text(encoding="utf-8")
    errors: list[str] = []
    primary = primary_skills(body)
    missing = COORDINATOR_PRIMARY - primary
    if missing:
        errors.append(f"{rel}: coordinator primary skills missing: {sorted(missing)}")
    if "coordination-plan.json" not in body:
        errors.append(f"{rel}: must reference coordination-plan.json")
    if "a2a-task.json" not in body:
        errors.append(f"{rel}: must reference a2a-task.json")
    if "Collaboration & A2A Delegation" not in body:
        errors.append(f"{rel}: missing Collaboration & A2A Delegation section")
    return errors


def validate_roles_a2a(role_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in role_paths:
        body = path.read_text(encoding="utf-8")
        if not has_a2a_or_contracts(body):
            errors.append(
                f"{path.relative_to(ROOT)}: missing 2026 handoff markers "
                "(Collaboration & A2A Delegation or contracts/schemas/)"
            )
    return errors


def validate_policy_coverage(role_paths: list[Path], policies: set[str]) -> list[str]:
    errors: list[str] = []
    for path in role_paths:
        stem = path.stem
        if stem not in policies:
            errors.append(f"action-boundaries.yaml: missing policy for role {stem}")
    extra = policies - {p.stem for p in role_paths}
    for stem in sorted(extra):
        errors.append(f"action-boundaries.yaml: policy for unknown role {stem}")
    return errors


def validate_infrastructure() -> list[str]:
    errors: list[str] = []
    if not GRAPH_SKILL.is_file():
        errors.append("missing skill: agent-graph-orchestration")
    if not COORD_PLAN.is_file():
        errors.append("missing contract: coordination-plan.json")
    if not TOOL_ORCH.is_file():
        errors.append("missing skill: agent-tool-orchestration")
    else:
        text = TOOL_ORCH.read_text(encoding="utf-8")
        if "action-boundaries.yaml" not in text:
            errors.append("agent-tool-orchestration must reference action-boundaries.yaml")
        if "data-classification.yaml" not in text:
            errors.append("agent-tool-orchestration must reference data-classification.yaml")
    known = collect_skill_names()
    if "agent-graph-orchestration" not in known:
        errors.append("agent-graph-orchestration not registered in skill index")
    return errors


def main() -> int:
    role_paths = role_files()
    policies = policy_roles()
    errors: list[str] = []

    if not role_paths:
        errors.append("no role files found")
    if not policies:
        errors.append("no policies found in action-boundaries.yaml")

    coordinator = ROLE_ROOT / f"{COORDINATOR}.md"
    if coordinator.is_file():
        errors.extend(validate_coordinator(coordinator))

    errors.extend(validate_roles_a2a(role_paths))
    errors.extend(validate_policy_coverage(role_paths, policies))
    errors.extend(validate_infrastructure())

    if errors:
        print("2026 compliance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"2026 compliance validation passed: {len(role_paths)} roles, "
        f"{len(policies)} policies, graph orchestration and coordinator A2A wired."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
