#!/usr/bin/env python3
"""Cursor/Antigravity hook: check tool action against action-boundaries.yaml."""

from __future__ import annotations

import json
import os
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


def load_boundaries(root: Path) -> dict:
    path = root / "core" / "policies" / "action-boundaries.yaml"
    text = path.read_text(encoding="utf-8")
    if yaml:
        data = yaml.safe_load(text)
        return data.get("roles", {})
    # minimal fallback without PyYAML
    roles: dict = {}
    current = None
    section = None
    for line in text.splitlines():
        if line.startswith("  ") and line.endswith(":") and not line.startswith("    "):
            current = line.strip().rstrip(":")
            roles[current] = {"allowed": [], "requires_approval": [], "denied": []}
            section = None
        elif current and line.strip().startswith("- "):
            item = line.strip()[2:]
            if "allowed:" in line or section == "allowed":
                pass
    return roles


def map_tool_to_action(tool_name: str, command: str) -> str:
    mcp_map = pack_root() / "core" / "policies" / "mcp-tool-map.yaml"
    action = "write_file"
    if "read" in tool_name.lower() or "grep" in tool_name.lower():
        action = "read_file"
    if "delete" in tool_name.lower():
        action = "delete_file"
    cmd = (command or "").lower()
    if "git push" in cmd:
        return "push_to_production"
    if "migrate" in cmd:
        return "run_migration"
    if "drop" in cmd and "database" in cmd:
        return "drop_database"
    return action


def main() -> int:
    role = os.environ.get("AGENT_ACTIVE_ROLE", "agent-coordinator")
    tool = os.environ.get("CURSOR_TOOL_NAME", os.environ.get("TOOL_NAME", "write"))
    command = os.environ.get("CURSOR_COMMAND", "")

    root = pack_root()
    boundaries_path = root / "core" / "policies" / "action-boundaries.yaml"
    if not boundaries_path.is_file():
        print("policy check skipped: no boundaries file", file=sys.stderr)
        return 0

    action = map_tool_to_action(tool, command)
    # Advisory mode: exit 0 but log — full block requires hook platform support
    print(
        json.dumps(
            {
                "advisory": True,
                "role": role,
                "mapped_action": action,
                "message": f"Verify {action} against action-boundaries.yaml for role {role}",
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
