#!/usr/bin/env python3
"""Cursor/Antigravity hook: check tool action against action-boundaries.yaml.

Resolution order:
  1. Check destructive_patterns in mcp-tool-map.yaml (highest priority)
  2. Look up tool name in tool_actions mapping in mcp-tool-map.yaml
  3. Fallback: infer from tool name keywords

2026 upgrades:
- --format text|json|sarif output modes (SARIF 2.1.0 for GitHub Code Scanning)
- exit code 2 for script errors vs 1 for policy violations (0/1/2 convention)
- W3C Trace Context trace_id propagation in JSON/SARIF output
- AGENT_ACTIVE_ROLE_LEVEL env var for tier-aware policy checks
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


TOOL_NAME = "agent-pack-policy-hook"
TOOL_VERSION = "4.0.0"


def pack_root() -> Path:
    env = os.environ.get("AGENT_SKILLS_ROOT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3]


def _parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", "'"):
        return value[1:-1]
    return value


def _parse_yaml_minimal(text: str) -> dict:
    """Parse the mapping/list YAML subset used by the bundled policy files."""
    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((len(raw_line) - len(raw_line.lstrip(" ")), stripped))

    def parse_node(index: int, indent: int):
        if index >= len(lines) or lines[index][0] < indent:
            return None, index
        is_list = lines[index][0] == indent and lines[index][1].startswith("- ")
        value: dict | list = [] if is_list else {}

        while index < len(lines) and lines[index][0] == indent:
            _, content = lines[index]
            if is_list:
                if not content.startswith("- "):
                    break
                item = content[2:].strip()
                if ":" in item:
                    key, raw_value = item.split(":", 1)
                    entry = {key.strip(): _parse_scalar(raw_value)}
                    index += 1
                    if index < len(lines) and lines[index][0] > indent:
                        child, index = parse_node(index, lines[index][0])
                        if isinstance(child, dict):
                            entry.update(child)
                    value.append(entry)
                    continue
                value.append(_parse_scalar(item))
                index += 1
                continue

            if ":" not in content:
                index += 1
                continue
            key, raw_value = content.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value:
                value[key] = _parse_scalar(raw_value)
            elif index < len(lines) and lines[index][0] > indent:
                child, index = parse_node(index, lines[index][0])
                value[key] = child
            else:
                value[key] = {}
        return value, index

    parsed, _ = parse_node(0, 0)
    return parsed if isinstance(parsed, dict) else {}


def load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text) or {}
    return _parse_yaml_minimal(text)


def load_boundaries(root: Path) -> dict:
    path = root / "core" / "policies" / "action-boundaries.yaml"
    if not path.is_file():
        return {}
    data = load_yaml(path)
    return data.get("roles", {})


def load_mcp_tool_map(root: Path) -> dict:
    path = root / "core" / "policies" / "mcp-tool-map.yaml"
    if not path.is_file():
        return {}
    return load_yaml(path)


def map_tool_to_action(tool_name: str, command: str, mcp_map: dict) -> str:
    """Resolve tool name + command to a policy action ID.

    Order:
      1. destructive_patterns (command substring match — highest priority)
      2. tool_actions lookup by tool_name
      3. Keyword fallback
    """
    cmd_lower = (command or "").lower()

    for entry in mcp_map.get("destructive_patterns", []):
        pattern = entry.get("pattern", "").lower()
        if pattern and pattern in cmd_lower:
            return entry.get("action", "run_build")

    tool_actions = mcp_map.get("tool_actions", {})
    tool_lower = (tool_name or "").lower()
    if tool_lower in tool_actions:
        return tool_actions[tool_lower]

    if any(kw in tool_lower for kw in ("read", "grep", "search", "find", "fetch", "get")):
        return "read_file"
    if any(kw in tool_lower for kw in ("delete", "remove", "rm")):
        return "delete_file"
    if any(kw in tool_lower for kw in ("create",)):
        return "create_file"
    if any(kw in tool_lower for kw in ("write", "edit", "update", "save")):
        return "write_file"

    return "write_file"


def check_action(role: str, action: str, boundaries: dict) -> str:
    """Return 'allowed', 'requires_approval', or 'denied'."""
    role_policy = boundaries.get(role, {})
    if action in role_policy.get("denied", []):
        return "denied"
    if action in role_policy.get("requires_approval", []):
        return "requires_approval"
    if action in role_policy.get("allowed", []):
        return "allowed"
    return "requires_approval"


def emit_sarif(result: dict, decision: str) -> None:
    """Emit SARIF 2.1.0 output for GitHub Code Scanning integration."""
    level = "error" if decision == "denied" else "warning" if decision == "requires_approval" else "note"
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": TOOL_NAME,
                        "version": TOOL_VERSION,
                        "rules": [
                            {
                                "id": "policy-check",
                                "name": "AgentPolicyCheck",
                                "shortDescription": {"text": "Agent role action boundary check"},
                            }
                        ],
                    }
                },
                "results": [
                    {
                        "ruleId": "policy-check",
                        "level": level,
                        "message": {"text": result["message"]},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": "core/policies/action-boundaries.yaml",
                                        "uriBaseId": "%SRCROOT%",
                                    }
                                }
                            }
                        ],
                        "partialFingerprints": {
                            "roleActionHash": f"{result['role']}:{result['mapped_action']}",
                        },
                    }
                ]
                if decision != "allowed"
                else [],
            }
        ],
    }
    print(json.dumps(sarif))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check agent tool action against action-boundaries.yaml."
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "sarif"],
        default="json",
        help="Output format (default: json). Use 'sarif' for GitHub Code Scanning.",
    )
    args = parser.parse_args()

    role = os.environ.get("AGENT_ACTIVE_ROLE", "agent-coordinator")
    tool = os.environ.get("CURSOR_TOOL_NAME", os.environ.get("TOOL_NAME", "write"))
    command = os.environ.get("CURSOR_COMMAND", "")
    trace_id = os.environ.get("AGENT_TRACE_ID", "")

    root = pack_root()
    boundaries_path = root / "core" / "policies" / "action-boundaries.yaml"
    if not boundaries_path.is_file():
        print("policy check skipped: no boundaries file", file=sys.stderr)
        return 0

    try:
        boundaries = load_boundaries(root)
        mcp_map = load_mcp_tool_map(root)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR loading policy files: {exc}", file=sys.stderr)
        return 2

    action = map_tool_to_action(tool, command, mcp_map)
    decision = check_action(role, action, boundaries)

    result = {
        "advisory": False,
        "role": role,
        "tool": tool,
        "command": command[:120] if command else "",
        "mapped_action": action,
        "decision": decision,
        "message": f"Action '{action}' for role '{role}': {decision}",
        **({"trace_id": trace_id} if trace_id else {}),
    }

    if args.format == "json":
        print(json.dumps(result))
    elif args.format == "sarif":
        emit_sarif(result, decision)
    else:
        print(result["message"])

    if decision == "denied":
        if args.format == "text":
            print(f"POLICY DENIED: role '{role}' cannot perform '{action}'", file=sys.stderr)
        return 1

    if decision == "requires_approval":
        if args.format == "text":
            print(
                f"POLICY APPROVAL REQUIRED: role '{role}' needs approval for '{action}'",
                file=sys.stderr,
            )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
