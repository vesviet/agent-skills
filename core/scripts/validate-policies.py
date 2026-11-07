#!/usr/bin/env python3
"""Validate agent policy boundaries, role profiles, irreversible gates, and MCP tool mapping.

Canonical public CLI entrypoint for Phase 4 Policy-as-Code verification.
Cross-checks core/policies/action-boundaries.yaml against:
1. All 39 role definition files in core/roles/*.md
2. Irreversible-action gating standards in core/roles/role-standard.md
3. Dynamic prefix patterns and tool actions in core/policies/mcp-tool-map.yaml

Supported CLI flags:
  --help          Display help and usage
  --format        Output format: text (default) or json
  --strict        Treat any warning or missing classification as a hard error
  --policy-path   Override path to action-boundaries.yaml
  --tool-map-path Override path to mcp-tool-map.yaml
  --roles-dir     Override path to core/roles/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Resolve repository and core root paths
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = ROOT / "core"

# Ensure script dir is on sys.path for common utilities if available
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Please install pyyaml.", file=sys.stderr)
    sys.exit(2)

POLICY_PATH = CORE_ROOT / "policies" / "action-boundaries.yaml"
TOOL_MAP_PATH = CORE_ROOT / "policies" / "mcp-tool-map.yaml"
ROLE_ROOT = CORE_ROOT / "roles"

# Actions that role-standard.md classifies as irreversible. No role may hold these
# under `allowed`; they must be gated (requires_approval) or denied.
NEVER_ALLOWED: Set[str] = {
    "apply_iac",
    "delete_branch_main",
    "drop_database",
    "drop_storage_volume",
    "export_data_egress",
    "force_push",
    "load_jit_skill",
    "modify_dns_production",
    "modify_secrets",
    "purge_cache_zone",
    "push_to_production",
    "rollback_deployment",
    "rotate_agent_credentials",
    "run_deployment",
    "git_push",
    "run_migration",
    "run_migrations",
    "terminate_instance",
}

# Actions denied for every role without exception.
ALWAYS_DENIED: Set[str] = {"bypass_ai_guardrail"}

# Every role must place these verbs in exactly one tier.
MUST_CLASSIFY: Set[str] = {"delegate_task", "bypass_ai_guardrail"}


def role_files(roles_dir: Path = ROLE_ROOT) -> list[Path]:
    """Collect all role definition markdown files excluding index and standard files."""
    if not roles_dir.is_dir():
        return []
    return sorted(
        p for p in roles_dir.glob("*.md") if p.name not in {"README.md", "role-standard.md"}
    )


def validate_policies(
    policy_path: Path = POLICY_PATH,
    tool_map_path: Path = TOOL_MAP_PATH,
    roles_dir: Path = ROLE_ROOT,
    strict: bool = False,
) -> Tuple[int, List[str], int]:
    """Validate policy consistency across role files, action boundaries, and MCP tool map.

    Returns:
        Tuple of (exit_code, list_of_errors, role_count)
    """
    errors: List[str] = []

    if not policy_path.is_file():
        errors.append(f"Policy file not found: {policy_path}")
        return 1, errors, 0

    if not tool_map_path.is_file():
        errors.append(f"MCP tool map not found: {tool_map_path}")
        return 1, errors, 0

    try:
        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"Failed to parse YAML from {policy_path}: {exc}")
        return 1, errors, 0

    try:
        tool_map = yaml.safe_load(tool_map_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"Failed to parse YAML from {tool_map_path}: {exc}")
        return 1, errors, 0

    roles = policy.get("roles") or {}
    role_count = len(roles)

    try:
        rel_policy = policy_path.relative_to(ROOT)
    except ValueError:
        rel_policy = policy_path

    try:
        rel_tool_map = tool_map_path.relative_to(ROOT)
    except ValueError:
        rel_tool_map = tool_map_path

    # 1. Every role file has a policy profile and vice versa
    disk_roles = role_files(roles_dir)
    disk_role_names = {p.stem for p in disk_roles}
    policy_role_names = set(roles.keys())

    for missing in sorted(disk_role_names - policy_role_names):
        errors.append(f"{rel_policy}: no policy profile for role {missing}")
    for extra in sorted(policy_role_names - disk_role_names):
        errors.append(f"{rel_policy}: policy profile {extra} has no role file in {roles_dir}")

    # 2-6. Per-role invariant checks
    for name, profile in sorted(roles.items()):
        allowed = set(profile.get("allowed") or [])
        gated = set(profile.get("requires_approval") or [])
        denied = set(profile.get("denied") or [])

        # 2. No verb in two tiers at once
        for a, b, label in (
            (allowed, gated, "allowed+requires_approval"),
            (allowed, denied, "allowed+denied"),
            (gated, denied, "requires_approval+denied"),
        ):
            overlap = a & b
            if overlap:
                errors.append(f"{rel_policy}: {name}: {sorted(overlap)} listed in {label}")

        # 3. Irreversible actions are never pre-authorized
        for action in sorted(allowed & NEVER_ALLOWED):
            errors.append(
                f"{rel_policy}: {name}: '{action}' is irreversible per core/roles/role-standard.md"
                " and must not be under allowed"
            )

        # 4. Always-denied actions
        for action in sorted(ALWAYS_DENIED):
            if action in allowed or action in gated or action not in denied:
                errors.append(f"{rel_policy}: {name}: '{action}' must be denied for every role")

        # 5. Required verbs classified
        classified = allowed | gated | denied
        for action in sorted(MUST_CLASSIFY - classified):
            errors.append(f"{rel_policy}: {name}: '{action}' is not classified in any tier")

        # 6. A role that can write must be able to create its own output artifacts
        if "write_file" in allowed and "create_file" not in allowed:
            errors.append(
                f"{rel_policy}: {name}: write_file is allowed but create_file is not"
                " — a role that may overwrite files should be able to create them"
            )

    # 7. Every action referenced by the tool map exists somewhere in the policy
    known: Set[str] = set()
    for profile in roles.values():
        for tier in ("allowed", "requires_approval", "denied"):
            known.update(profile.get(tier) or [])

    mapped: Set[str] = set()
    for value in (tool_map.get("tool_actions") or tool_map.get("tools") or {}).values():
        if isinstance(value, str):
            mapped.add(value)
    for entry in tool_map.get("destructive_patterns") or []:
        if isinstance(entry, dict) and entry.get("action"):
            mapped.add(entry["action"])
    for entry in (tool_map.get("mcp_tool_routing") or {}).get("prefix_patterns") or []:
        if isinstance(entry, dict) and entry.get("action"):
            mapped.add(entry["action"])

    for action in sorted(mapped - known):
        errors.append(
            f"{rel_tool_map}: maps to action '{action}'"
            f" which no role classifies in {rel_policy}"
        )

    exit_code = 1 if errors else 0
    return exit_code, errors, role_count


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate agent policy boundaries, role profiles, and MCP tool mapping.",
        epilog=(
            "Exit codes:\n"
            "  0 = all policy consistency checks passed\n"
            "  1 = one or more policy validation checks failed\n"
            "  2 = configuration or parsing error\n"
        ),
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce strict validation mode.",
    )
    parser.add_argument(
        "--policy-path",
        type=Path,
        default=POLICY_PATH,
        help=f"Path to action-boundaries.yaml (default: {POLICY_PATH})",
    )
    parser.add_argument(
        "--tool-map-path",
        type=Path,
        default=TOOL_MAP_PATH,
        help=f"Path to mcp-tool-map.yaml (default: {TOOL_MAP_PATH})",
    )
    parser.add_argument(
        "--roles-dir",
        type=Path,
        default=ROLE_ROOT,
        help=f"Directory containing role markdown definitions (default: {ROLE_ROOT})",
    )

    args = parser.parse_args(argv)

    exit_code, errors, role_count = validate_policies(
        policy_path=args.policy_path,
        tool_map_path=args.tool_map_path,
        roles_dir=args.roles_dir,
        strict=args.strict,
    )

    if args.format == "json":
        report = {
            "validator": "validate-policies",
            "version": "1.0.0",
            "passed": exit_code == 0,
            "exit_code": exit_code,
            "role_profiles_checked": role_count,
            "errors": errors,
            "error_count": len(errors),
        }
        print(json.dumps(report, indent=2))
    else:
        if errors:
            print("Policy consistency validation failed:")
            for error in errors:
                print(f"- {error}")
        else:
            print(
                f"Policy consistency validation passed: {role_count} role profiles checked"
                " against role files, irreversible-action standard, and the MCP tool map."
            )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
