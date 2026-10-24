#!/usr/bin/env python3
"""Validate full A2A 1.0 pack compliance and Antigravity adapter artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT


REQUIRED_SCHEMAS = (
    "agent-card.json",
    "a2a-task.json",
    "a2a-artifact.json",
    "a2a-task-status.json",
    "a2a-task-progress.json",
    "a2a-message.json",
    "a2a-jsonrpc-envelope.json",
    "a2a-push-notification-config.json",
    "a2a-task-cancel.json",
    "agent-trace-span.json",
    "coordination-plan.json",
)

REQUIRED_PATHS = (
    CORE_ROOT / "skills" / "agent" / "agent-a2a-protocol" / "SKILL.md",
    CORE_ROOT / "a2a" / "README.md",
    ROOT / "adapters" / "antigravity" / "ANTIGRAVITY.md",
    ROOT / "adapters" / "antigravity" / "rules.template.md",
    ROOT / "adapters" / "antigravity" / "a2a-config.template.yaml",
    ROOT / "adapters" / "cursor" / "hooks.template.json",
    CORE_ROOT / "workflows" / "agent-a2a-delegation.md",
    CORE_ROOT / "policies" / "mcp-tool-map.yaml",
)

REGISTRY = CORE_ROOT / "a2a" / ".well-known" / "agent-registry.json"
COORDINATOR = CORE_ROOT / "roles" / "agent-coordinator.md"
TOOL_ORCH = CORE_ROOT / "skills" / "agent" / "agent-tool-orchestration" / "SKILL.md"


def main() -> int:
    errors: list[str] = []
    schemas_dir = CORE_ROOT / "contracts" / "schemas"

    for name in REQUIRED_SCHEMAS:
        if not (schemas_dir / name).is_file():
            errors.append(f"missing schema: {name}")

    for path in REQUIRED_PATHS:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if COORDINATOR.is_file():
        body = COORDINATOR.read_text(encoding="utf-8")
        for needle in ("agent-a2a-protocol", "a2a-task-status", "a2a-task-progress"):
            if needle not in body:
                errors.append(f"agent-coordinator.md: missing reference to {needle}")

    if TOOL_ORCH.is_file() and "agent-a2a-protocol" not in TOOL_ORCH.read_text(encoding="utf-8"):
        errors.append("agent-tool-orchestration should reference agent-a2a-protocol")

    if not REGISTRY.is_file():
        errors.append(
            "missing agent registry — run: python3 core/scripts/generate-a2a-registry.py"
        )
    else:
        try:
            reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
            agents = reg.get("agents", [])
            if len(agents) < 21:
                errors.append(f"agent registry has only {len(agents)} agents, expected 21")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid agent-registry.json: {exc}")

    antigravity_rules = ROOT / "adapters" / "antigravity" / "rules.template.md"
    if antigravity_rules.is_file():
        text = antigravity_rules.read_text(encoding="utf-8")
        for needle in ("a2a-task.json", "a2a-artifact.json", "UUID v4"):
            if needle not in text:
                errors.append(f"antigravity rules.template.md: missing {needle}")

    if errors:
        print("A2A full compliance validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("A2A full compliance validation passed (A2A 1.0 + Antigravity adapter).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
