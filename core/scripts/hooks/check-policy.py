#!/usr/bin/env python3
"""Cursor/Antigravity hook: check tool action against action-boundaries.yaml.

Resolution order:
  1. Check destructive_patterns in mcp-tool-map.yaml (highest priority)
  2. Look up tool name in tool_actions mapping in mcp-tool-map.yaml
  3. Fallback: infer from tool name keywords

2026 upgrades (T1):
- text/json/sarif output modes (SARIF 2.1.0 for GitHub Code Scanning)
- Exit code convention: 0=allowed, 1=policy violation (denied), 2=approval required
- W3C Trace Context trace_id propagation in JSON/SARIF output
- AGENT_ACTIVE_ROLE_LEVEL env var for tier-aware policy checks:
    * read_only        - downgrade every non-allowed verdict to denied (block writes)
    * supervised       - leave requires_approval as requires_approval (default)
    * unsupervised     - no change
- --emit-audit flag writes a policy_decision.json (OCSF 99001) next to the audit log path
  so the action-boundaries audit trail in action-boundaries.yaml is actually emitted

2026 upgrades (T2):
- Audit log includes command hash and trace_id
- --audit-path overrides the audit output path
- Level downgrade is logged in the result dict for downstream consumers
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


def check_action(role: str, action: str, boundaries: dict, role_level: str = "supervised") -> tuple:
    """Return (decision, level_modifier) where decision is 'allowed', 'requires_approval',
    or 'denied', and level_modifier is one of 'none', 'downgraded_to_denied'.

    AGENT_ACTIVE_ROLE_LEVEL semantics (2026):
        read_only      - any verdict other than 'allowed' is downgraded to 'denied'.
                         This is for sessions that may only observe, not act.
        supervised     - no change. Requires_approval stays requires_approval.
        unsupervised   - no change. Same as supervised (kept for explicitness).
    """
    role_policy = boundaries.get(role, {})
    if action in role_policy.get("denied", []):
        return ("denied", "none")
    if action in role_policy.get("requires_approval", []):
        decision = "requires_approval"
    elif action in role_policy.get("allowed", []):
        decision = "allowed"
    else:
        decision = "requires_approval"

    if role_level == "read_only" and decision != "allowed":
        return ("denied", "downgraded_to_denied")
    return (decision, "none")


def emit_sarif(result: dict, decision: str) -> None:
    """Emit SARIF 2.1.0 output for GitHub Code Scanning integration."""
    level = "error" if decision == "denied" else "warning" if decision == "requires_approval" else "note"
    sarif_result = {
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
                "results": [sarif_result] if decision != "allowed" else [],
            }
        ],
    }
    print(json.dumps(sarif))


def emit_audit_event(result: dict, decision: str, level_modifier: str, audit_path: Path) -> None:
    """Write a single OCSF 99001 audit event to the configured path.

    Best-effort: failures are reported to stderr but do not change the exit code,
    because the policy decision is the primary signal and the audit is a side effect.
    """
    try:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        import hashlib
        cmd_hash = hashlib.sha256((result.get("command") or "").encode("utf-8")).hexdigest()[:16]
        event = {
            "ocsf_class": "policy_decision",
            "class_uid": 99001,
            "activity": "evaluate",
            "type_uid": 99001,
            "severity": "error" if decision == "denied" else "warning" if decision == "requires_approval" else "info",
            "actor": {
                "type": "agent",
                "role": result.get("role", ""),
            },
            "resource": {
                "type": "tool",
                "name": result.get("tool", ""),
            },
            "action": {
                "name": result.get("mapped_action", ""),
                "command_sha256_16": cmd_hash,
            },
            "decision": decision,
            "level_modifier": level_modifier,
            "message": result.get("message", ""),
        }
        if result.get("trace_id"):
            event["trace"] = {"id": result["trace_id"]}
        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except OSError as exc:
        print(f"WARN: failed to write audit event: {exc}", file=sys.stderr)


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
    parser.add_argument(
        "--emit-audit",
        action="store_true",
        help="Append a policy_decision audit event in OCSF 99001 format to the audit path.",
    )
    parser.add_argument(
        "--audit-path",
        type=Path,
        default=Path("policy_decision.jsonl"),
        help="Path for --emit-audit (default: policy_decision.jsonl in the working directory).",
    )
    args = parser.parse_args()

    role = os.environ.get("AGENT_ACTIVE_ROLE", "agent-coordinator")
    role_level = os.environ.get("AGENT_ACTIVE_ROLE_LEVEL", "supervised").strip().lower()
    if role_level not in {"read_only", "supervised", "unsupervised"}:
        role_level = "supervised"
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
    decision, level_modifier = check_action(role, action, boundaries, role_level)

    result = {
        "advisory": False,
        "role": role,
        "role_level": role_level,
        "tool": tool,
        "command": command[:120] if command else "",
        "mapped_action": action,
        "decision": decision,
        "level_modifier": level_modifier,
        "message": f"Action '{action}' for role '{role}' (level={role_level}): {decision}",
        **({"trace_id": trace_id} if trace_id else {}),
    }

    if args.emit_audit:
        emit_audit_event(result, decision, level_modifier, args.audit_path)

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
