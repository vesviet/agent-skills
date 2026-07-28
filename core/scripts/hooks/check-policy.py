#!/usr/bin/env python3
"""Cursor/Antigravity hook: check tool action against action-boundaries.yaml.

Resolution order:
  1. Check destructive_patterns in mcp-tool-map.yaml (highest priority)
  2. Look up tool name in tool_actions mapping in mcp-tool-map.yaml
  3. Fallback: infer from tool name keywords
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


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

    # 1. Destructive pattern matching (command-level, highest priority)
    for entry in mcp_map.get("destructive_patterns", []):
        pattern = entry.get("pattern", "").lower()
        if pattern and pattern in cmd_lower:
            return entry.get("action", "run_build")

    # 2. tool_actions lookup
    tool_actions = mcp_map.get("tool_actions", {})
    tool_lower = (tool_name or "").lower()
    if tool_lower in tool_actions:
        return tool_actions[tool_lower]

    # 3. Keyword fallback (safe defaults)
    if any(kw in tool_lower for kw in ("read", "grep", "search", "find", "fetch", "get")):
        return "read_file"
    if any(kw in tool_lower for kw in ("delete", "remove", "rm")):
        return "delete_file"
    if any(kw in tool_lower for kw in ("create",)):
        return "create_file"
    if any(kw in tool_lower for kw in ("write", "edit", "update", "save")):
        return "write_file"

    return "write_file"  # safe default: assume write and let policy check it


def check_action(role: str, action: str, boundaries: dict) -> str:
    """Return 'allowed', 'requires_approval', or 'denied'."""
    role_policy = boundaries.get(role, {})
    if action in role_policy.get("denied", []):
        return "denied"
    if action in role_policy.get("requires_approval", []):
        return "requires_approval"
    if action in role_policy.get("allowed", []):
        return "allowed"
    # Default from policy
    return "requires_approval"


def main() -> int:
    role = os.environ.get("AGENT_ACTIVE_ROLE", "agent-coordinator")
    tool = os.environ.get("CURSOR_TOOL_NAME", os.environ.get("TOOL_NAME", "write"))
    command = os.environ.get("CURSOR_COMMAND", "")

    root = pack_root()
    boundaries_path = root / "core" / "policies" / "action-boundaries.yaml"
    if not boundaries_path.is_file():
        print("policy check skipped: no boundaries file", file=sys.stderr)
        return 0

    boundaries = load_boundaries(root)
    mcp_map = load_mcp_tool_map(root)

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
    }

    print(json.dumps(result))

    if decision == "denied":
        print(f"POLICY DENIED: role '{role}' cannot perform '{action}'", file=sys.stderr)
        return 1
    if decision == "requires_approval":
        print(
            f"POLICY APPROVAL REQUIRED: role '{role}' needs approval for '{action}'",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
