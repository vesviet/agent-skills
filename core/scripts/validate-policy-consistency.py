#!/usr/bin/env python3
"""Cross-check action-boundaries.yaml against the role files and the irreversible-action
standard in role-standard.md.

Catches the drift class where a role's policy profile is copy-pasted, inverts a tier,
or marks an irreversible action as pre-authorized.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from common import CORE_ROOT, ROOT

POLICY_PATH = CORE_ROOT / "policies" / "action-boundaries.yaml"
TOOL_MAP_PATH = CORE_ROOT / "policies" / "mcp-tool-map.yaml"
ROLE_ROOT = CORE_ROOT / "roles"

# Actions that role-standard.md classifies as irreversible. No role may hold these
# under `allowed`; they must be gated or denied.
NEVER_ALLOWED = {
    "apply_iac",
    "delete_branch_main",
    "drop_database",
    "drop_storage_volume",
    "force_push",
    "modify_dns_production",
    "modify_secrets",
    "purge_cache_zone",
    "push_to_production",
    "rollback_deployment",
    "rotate_agent_credentials",
    "run_deployment",
    "run_migration",
    "terminate_instance",
}

# Actions denied for every role without exception.
ALWAYS_DENIED = {"bypass_ai_guardrail"}

# Every role must place these verbs in exactly one tier.
MUST_CLASSIFY = {"delegate_task", "bypass_ai_guardrail"}


def role_files() -> list[Path]:
    return sorted(
        p for p in ROLE_ROOT.glob("*.md") if p.name not in {"README.md", "role-standard.md"}
    )


def main() -> int:
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
    roles = policy.get("roles") or {}
    errors: list[str] = []

    rel = POLICY_PATH.relative_to(ROOT)

    # 1. every role file has a policy profile and vice versa
    role_names = {p.stem for p in role_files()}
    for missing in sorted(role_names - set(roles)):
        errors.append(f"{rel}: no policy profile for role {missing}")
    for extra in sorted(set(roles) - role_names):
        errors.append(f"{rel}: policy profile {extra} has no role file in core/roles/")

    for name, profile in sorted(roles.items()):
        allowed = set(profile.get("allowed") or [])
        gated = set(profile.get("requires_approval") or [])
        denied = set(profile.get("denied") or [])

        # 2. no verb in two tiers at once
        for a, b, label in ((allowed, gated, "allowed+requires_approval"),
                            (allowed, denied, "allowed+denied"),
                            (gated, denied, "requires_approval+denied")):
            overlap = a & b
            if overlap:
                errors.append(f"{rel}: {name}: {sorted(overlap)} listed in {label}")

        # 3. irreversible actions are never pre-authorized
        for action in sorted(allowed & NEVER_ALLOWED):
            errors.append(
                f"{rel}: {name}: '{action}' is irreversible per core/roles/role-standard.md"
                " and must not be under allowed"
            )

        # 4. always-denied actions
        for action in sorted(ALWAYS_DENIED):
            if action in allowed or action in gated:
                errors.append(f"{rel}: {name}: '{action}' must be denied for every role")

        # 5. required verbs classified
        classified = allowed | gated | denied
        for action in sorted(MUST_CLASSIFY - classified):
            errors.append(f"{rel}: {name}: '{action}' is not classified in any tier")

        # 6. a role that can write must be able to create its own output artifacts
        if "write_file" in allowed and "create_file" not in allowed:
            errors.append(
                f"{rel}: {name}: write_file is allowed but create_file is not"
                " — a role that may overwrite files should be able to create them"
            )

    # 7. every action referenced by the tool map exists somewhere in the policy
    tool_map = yaml.safe_load(TOOL_MAP_PATH.read_text(encoding="utf-8"))
    known: set[str] = set()
    for profile in roles.values():
        for tier in ("allowed", "requires_approval", "denied"):
            known |= set(profile.get(tier) or [])
    mapped: set[str] = set()
    for value in (tool_map.get("tool_actions") or tool_map.get("tools") or {}).values():
        if isinstance(value, str):
            mapped.add(value)
    for entry in tool_map.get("destructive_patterns") or []:
        if isinstance(entry, dict) and entry.get("action"):
            mapped.add(entry["action"])
    for action in sorted(mapped - known):
        errors.append(
            f"{TOOL_MAP_PATH.relative_to(ROOT)}: maps to action '{action}'"
            f" which no role classifies in {rel}"
        )

    if errors:
        print("Policy consistency validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Policy consistency validation passed: {len(roles)} role profiles checked"
        " against role files, irreversible-action standard, and the MCP tool map."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
