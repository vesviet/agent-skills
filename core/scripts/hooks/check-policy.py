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
      3. Dynamic regex patterns in mcp_tool_routing.prefix_patterns
      4. Generic remote MCP call fallback
      5. Keyword fallback heuristics
      6. Fail-closed default action (mcp_tool_routing.default_action or 'requires_approval')
    """
    cmd_lower = (command or "").strip().lower()
    tool_lower = (tool_name or "").strip().lower()

    # 1. Check destructive patterns in command line (highest priority)
    if any(p in cmd_lower for p in ("rm -rf", "rm -r", "rmdir", "del /f", "del /s")):
        return "delete_file"

    for entry in mcp_map.get("destructive_patterns", []):
        pattern = entry.get("pattern", "").lower()
        if pattern and pattern in cmd_lower:
            # If the pattern is coarse "git push", but the tool is an explicit git_push prefix tool
            # and not a force push, defer to the prefix pattern action (git_push)
            if pattern == "git push" and tool_lower.startswith("git_push_") and not any(
                p in cmd_lower for p in ("--force", "-f", ":main", ":master")
            ):
                continue
            return entry.get("action", "run_build")

    # 2. Direct tool_actions lookup
    tool_actions = mcp_map.get("tool_actions", {})
    if tool_lower in tool_actions:
        return tool_actions[tool_lower]

    # Direct action verb check if tool name is already a policy action
    known_actions = mcp_map.get("known_actions")
    if known_actions and tool_lower in known_actions:
        return tool_lower
    if tool_lower in {
        "verify_svid_token",
        "execute_stateless_mcp",
        "export_data_egress",
        "load_jit_skill",
        "spill_context_disk",
        "emit_ocsf_audit",
    }:
        return tool_lower

    # 3. Dynamic <domain>_<action> prefix resolution
    routing = mcp_map.get("mcp_tool_routing", {})
    for entry in routing.get("prefix_patterns", []):
        regex = entry.get("pattern", "")
        if regex:
            try:
                if re.search(regex, tool_lower):
                    return entry.get("action", "requires_approval")
            except re.error:
                continue

    # 4. Remote MCP generic call fallback
    if tool_lower in ("mcp_call", "call_mcp_tool", "execute_stateless_mcp"):
        return routing.get("default_action", "requires_approval")

    # 5. Keyword heuristics
    if any(kw in tool_lower for kw in ("read", "grep", "search", "find", "fetch", "get")):
        return "read_file"
    if any(kw in tool_lower for kw in ("delete", "remove", "rm")):
        return "delete_file"
    if any(kw in tool_lower for kw in ("create",)):
        return "create_file"
    if any(kw in tool_lower for kw in ("write", "edit", "update", "save")):
        return "write_file"

    # 6. Fail-closed default action
    return routing.get("default_action", "requires_approval")


READ_ONLY_ACTIONS = {
    "read_file",
    "search_code",
    "read_database",
    "emit_ocsf_audit",
    "query_db",
    "verify_svid_token",
}


def check_action(role: str, action: str, boundaries: dict, role_level: str = "supervised") -> tuple:
    """Return (decision, level_modifier) where decision is 'allowed', 'requires_approval',
    or 'denied', and level_modifier is one of 'none', 'downgraded_to_denied'.

    AGENT_ACTIVE_ROLE_LEVEL semantics (2026):
        read_only      - any verdict other than 'allowed' is downgraded to 'denied'.
                         Also, any write/mutating action is downgraded to 'denied'.
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

    if role_level == "read_only":
        if decision != "allowed" or action not in READ_ONLY_ACTIONS:
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


def resolve_rule_id(role: str, action: str, level_modifier: str) -> str:
    """Determine the policy rule_id for OCSF metadata."""
    env_rule = os.environ.get("AGENT_POLICY_RULE_ID")
    if env_rule:
        return env_rule
    if level_modifier == "downgraded_to_denied":
        return "policy.level.read_only_downgrade"
    if action == "bypass_ai_guardrail":
        return "compliance.safety.always_denied"
    return f"policy.action_boundary.{action}"


def emit_audit_event(result: dict, decision: str, level_modifier: str, audit_path: Path) -> None:
    """Write a single OCSF Class UID 99001 audit event to the configured path.

    Best-effort: failures are reported to stderr with 'WARN:' but do not change
    the exit code, preserving policy decision as the primary signal.
    """
    try:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        import hashlib
        import time

        role = result.get("role", "agent-coordinator")
        actor_name = os.environ.get("AGENT_ACTOR_NAME") or role
        actor_uid = (
            os.environ.get("AGENT_SVID_UID")
            or os.environ.get("AGENT_SVID_TOKEN_ID")
            or os.environ.get("AGENT_ACTOR_UID")
            or f"spiffe://agent-skills/role/{role}"
        )
        mapped_action = result.get("mapped_action", "")
        cmd_hash = hashlib.sha256((result.get("command") or "").encode("utf-8")).hexdigest()[:16]
        severity_id = 1 if decision == "allowed" else 3 if decision == "requires_approval" else 4
        status_code = (
            "ALLOWED" if decision == "allowed"
            else "HITL_TRIGGERED" if decision == "requires_approval"
            else "POLICY_DENIED"
        )
        rule_id = resolve_rule_id(role, mapped_action, level_modifier)

        event = {
            "class_uid": 99001,
            "category_uid": 9,
            "activity_id": 1,
            "time": int(time.time()),
            "severity_id": severity_id,
            "actor": {
                "user": {
                    "name": actor_name,
                    "type": "Non-Human Identity",
                    "uid": actor_uid,
                }
            },
            "action": {
                "name": mapped_action,
                "command_sha256_16": cmd_hash,
            },
            "status": decision,
            "status_code": status_code,
            "message": result.get("message", ""),
            "metadata": {
                "policy_version": "2.0.0",
                "rule_id": rule_id,
            },
            "resource": {
                "type": "tool",
                "name": result.get("tool", ""),
            },
            "decision": decision,
            "level_modifier": level_modifier,
        }

        if result.get("trace_id"):
            event["trace"] = {"id": result["trace_id"]}

        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except Exception as exc:
        print(f"WARN: failed to write audit event: {exc}", file=sys.stderr)


def main() -> int:
    default_audit_path = pack_root() / ".agent" / "audit" / "policy-events.jsonl"
    env_audit_path = os.environ.get("AGENT_AUDIT_LOG_PATH")
    if env_audit_path:
        default_audit_path = Path(env_audit_path)

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
        default=default_audit_path,
        help="Path for --emit-audit (default: .agent/audit/policy-events.jsonl in pack root).",
    )
    args = parser.parse_args()

    raw_role = os.environ.get("AGENT_ACTIVE_ROLE")
    role = raw_role.strip() if raw_role else "agent-coordinator"
    if not role:
        role = "agent-coordinator"

    role_level = os.environ.get("AGENT_ACTIVE_ROLE_LEVEL", "supervised").strip().lower()
    if role_level not in {"read_only", "supervised", "unsupervised"}:
        role_level = "supervised"

    raw_tool = os.environ.get("CURSOR_TOOL_NAME")
    if raw_tool is None:
        raw_tool = os.environ.get("TOOL_NAME", "write")
    tool = raw_tool.strip()

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
        known = set()
        for prof in boundaries.values():
            if isinstance(prof, dict):
                for t in ("allowed", "requires_approval", "denied"):
                    known.update(prof.get(t) or [])
        mcp_map["known_actions"] = known
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR loading policy files: {exc}", file=sys.stderr)
        return 2

    if role not in boundaries and role.lower() in boundaries:
        role = role.lower()

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
