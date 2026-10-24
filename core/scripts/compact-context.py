#!/usr/bin/env python3
"""Deterministic CLI tool for agent context compaction and Head-Tail TOC truncation.

Conforms to Draft 2020-12 data contract `compact-working-state.json` (schema #60).
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_FILE = Path(__file__).resolve().parent.parent / "contracts" / "schemas" / "compact-working-state.json"

WORK_TYPES = {
    "feature",
    "bugfix",
    "refactor",
    "migration",
    "investigation",
    "release",
    "architecture",
    "audit",
}

PHASE_STATUSES = {"in_progress", "completed", "blocked", "paused"}
VERIFICATION_STATUSES = {"passed", "failed", "pending"}

REQUIRED_SLOTS = (
    "contract_type",
    "current_goal",
    "work_type",
    "phase_control",
    "active_constraints",
    "files_modified_and_inspected",
    "decisions_and_tradeoffs",
    "verification_and_evidence",
    "failed_attempts_and_antipatterns",
    "preserved_invariants",
    "next_single_safe_action",
)


def truncate_tool_output(
    text: str, head_lines: int = 5, tail_lines: int = 15
) -> str:
    """Apply Head-Tail Syntax-Aware Truncation (TOC) to verbose output text."""
    lines = text.splitlines()
    if len(lines) <= head_lines + tail_lines:
        return text

    head = lines[:head_lines]
    tail = lines[-tail_lines:] if tail_lines > 0 else []
    truncated_count = len(lines) - head_lines - tail_lines
    marker = f"... [Truncated {truncated_count} lines of execution output] ..."
    return "\n".join(head + [marker] + tail)


def truncate_code_fences(
    text: str, head_lines: int = 5, tail_lines: int = 15
) -> str:
    """Parse text and apply TOC truncation to markdown code fences containing verbose outputs."""
    pattern = re.compile(r"(```[a-zA-Z0-9_\-\.]*\n)([\s\S]*?)(```)")

    def replace_fence(match: re.Match[str]) -> str:
        open_fence = match.group(1)
        body = match.group(2)
        close_fence = match.group(3)
        truncated_body = truncate_tool_output(body, head_lines, tail_lines)
        return f"{open_fence}{truncated_body}\n{close_fence}"

    return pattern.sub(replace_fence, text)


def validate_checkpoint_data(
    data: Any, schema_path: Path | None = None
) -> list[str]:
    """Validate a candidate dictionary against the compact-working-state specification."""
    if not isinstance(data, dict):
        return ["checkpoint must be a JSON object"]

    errors: list[str] = []

    for slot in REQUIRED_SLOTS:
        if slot not in data:
            errors.append(f"missing required slot: {slot}")

    if data.get("contract_type") != "compact-working-state":
        errors.append(
            f"contract_type must be 'compact-working-state', got {data.get('contract_type')!r}"
        )

    if "current_goal" in data and not isinstance(data["current_goal"], str):
        errors.append("current_goal must be a string")

    work_type = data.get("work_type")
    if not isinstance(work_type, str) or work_type not in WORK_TYPES:
        errors.append(f"work_type {work_type!r} is not in valid enums: {sorted(WORK_TYPES)}")

    phase_ctrl = data.get("phase_control")
    if not isinstance(phase_ctrl, dict):
        errors.append("phase_control must be an object")
    else:
        for req in ("current_phase", "phase_name", "status"):
            if req not in phase_ctrl or phase_ctrl[req] is None:
                errors.append(f"phase_control missing required property: {req}")
        status = phase_ctrl.get("status")
        if not isinstance(status, str) or status not in PHASE_STATUSES:
            errors.append(f"phase_control.status {status!r} not in enums: {sorted(PHASE_STATUSES)}")

    constraints = data.get("active_constraints")
    if not isinstance(constraints, list):
        errors.append("active_constraints must be an array of strings")

    files_obj = data.get("files_modified_and_inspected")
    if not isinstance(files_obj, dict):
        errors.append("files_modified_and_inspected must be an object")
    else:
        for k in ("modified", "inspected"):
            arr = files_obj.get(k)
            if not isinstance(arr, list) or not all(isinstance(x, str) for x in arr):
                errors.append(f"files_modified_and_inspected.{k} must be an array of strings")

    decisions = data.get("decisions_and_tradeoffs")
    if not isinstance(decisions, list):
        errors.append("decisions_and_tradeoffs must be an array")
    else:
        for idx, item in enumerate(decisions):
            if not isinstance(item, dict):
                errors.append(f"decisions_and_tradeoffs[{idx}] must be an object")
            else:
                if "decision" not in item:
                    errors.append(f"decisions_and_tradeoffs[{idx}] missing decision")
                if "rationale" not in item:
                    errors.append(f"decisions_and_tradeoffs[{idx}] missing rationale")

    evidence = data.get("verification_and_evidence")
    if not isinstance(evidence, list):
        errors.append("verification_and_evidence must be an array")
    else:
        for idx, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"verification_and_evidence[{idx}] must be an object")
            else:
                if "command" not in item:
                    errors.append(f"verification_and_evidence[{idx}] missing command")
                if "exit_code" not in item or not isinstance(item["exit_code"], int):
                    errors.append(f"verification_and_evidence[{idx}] exit_code must be an integer")
                if "status" not in item:
                    errors.append(f"verification_and_evidence[{idx}] missing status")
                st = item.get("status")
                if not isinstance(st, str) or st not in VERIFICATION_STATUSES:
                    errors.append(f"verification_and_evidence[{idx}].status {st!r} not in enums: {sorted(VERIFICATION_STATUSES)}")

    failed = data.get("failed_attempts_and_antipatterns")
    if not isinstance(failed, list):
        errors.append("failed_attempts_and_antipatterns must be an array")
    else:
        for idx, item in enumerate(failed):
            if not isinstance(item, dict):
                errors.append(f"failed_attempts_and_antipatterns[{idx}] must be an object")
            else:
                if "attempt" not in item:
                    errors.append(f"failed_attempts_and_antipatterns[{idx}] missing attempt")
                if "failure_reason" not in item:
                    errors.append(f"failed_attempts_and_antipatterns[{idx}] missing failure_reason")

    invariants = data.get("preserved_invariants")
    if not isinstance(invariants, list):
        errors.append("preserved_invariants must be an array of strings")

    next_action = data.get("next_single_safe_action")
    if not isinstance(next_action, str):
        errors.append("next_single_safe_action must be a string")

    # Optional validation with schema file if present
    s_path = schema_path if schema_path else SCHEMA_FILE
    if s_path.exists():
        try:
            schema_json = json.loads(s_path.read_text(encoding="utf-8"))
            for req in schema_json.get("required", []):
                if req not in data:
                    err = f"schema required field missing: {req}"
                    if err not in errors:
                        errors.append(err)
        except Exception as exc:
            errors.append(f"warning: could not load schema file {s_path}: {exc}")

    return errors


def format_markdown_checkpoint(data: dict[str, Any]) -> str:
    """Format a 10-slot dictionary into standard in-context markdown checkpoint."""
    lines: list[str] = ["## Compact Working State", ""]

    lines.append("Current Goal:")
    goal = data.get("current_goal", "N/A")
    lines.append(f"- {goal}")
    lines.append("")

    lines.append("Work Type:")
    lines.append(f"- {data.get('work_type', 'feature')}")
    lines.append("")

    lines.append("Phase Control:")
    pc = data.get("phase_control", {})
    if isinstance(pc, dict):
        lines.append(f"- Current Phase: {pc.get('current_phase', 'N/A')}")
        if "total_phases" in pc:
            lines.append(f"- Total Phases: {pc.get('total_phases')}")
        lines.append(f"- Phase Name: {pc.get('phase_name', 'N/A')}")
        lines.append(f"- Status: {pc.get('status', 'in_progress')}")
        if "active_owner" in pc:
            lines.append(f"- Active Owner: {pc.get('active_owner')}")
    lines.append("")

    lines.append("Active Constraints:")
    constraints = data.get("active_constraints", [])
    if isinstance(constraints, list) and constraints:
        for c in constraints:
            lines.append(f"- {c}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Files Modified & Inspected:")
    files = data.get("files_modified_and_inspected", {})
    if isinstance(files, dict):
        mod = files.get("modified", [])
        insp = files.get("inspected", [])
        lines.append(f"- Modified: [{', '.join(str(x) for x in mod) if mod else 'None'}]")
        lines.append(f"- Inspected: [{', '.join(str(x) for x in insp) if insp else 'None'}]")
    lines.append("")

    lines.append("Decisions & Trade-offs:")
    decisions = data.get("decisions_and_tradeoffs", [])
    if isinstance(decisions, list) and decisions:
        for d in decisions:
            if isinstance(d, dict):
                dec_text = d.get("decision", "")
                rat_text = d.get("rationale", "")
                lines.append(f"- Decision: {dec_text} (Rationale: {rat_text})")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Verification & Evidence:")
    evidence = data.get("verification_and_evidence", [])
    if isinstance(evidence, list) and evidence:
        for e in evidence:
            if isinstance(e, dict):
                cmd = e.get("command", "")
                code = e.get("exit_code", 0)
                st = e.get("status", "passed")
                snip = e.get("verbatim_snippet", "")
                snip_str = f" | {snip}" if snip else ""
                lines.append(f"- [{cmd}]: Exit code [{code}], Status: [{st}]{snip_str}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Failed Attempts & Anti-Patterns:")
    failed = data.get("failed_attempts_and_antipatterns", [])
    if isinstance(failed, list) and failed:
        for f in failed:
            if isinstance(f, dict):
                att = f.get("attempt", "")
                reas = f.get("failure_reason", "")
                rule = f.get("preventive_rule", "")
                rule_str = f" -> Rule: {rule}" if rule else ""
                lines.append(f"- Attempt: {att} (Failed: {reas}){rule_str}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Preserved Invariants:")
    invariants = data.get("preserved_invariants", [])
    if isinstance(invariants, list) and invariants:
        for inv in invariants:
            lines.append(f"- {inv}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Next Single Safe Action:")
    next_action = data.get("next_single_safe_action", "N/A")
    lines.append(f"- {next_action}")

    return "\n".join(lines)


def build_default_checkpoint(
    goal: str = "Execute assigned milestone task",
    work_type: str = "feature",
    phase_name: str = "Implementation",
    next_action: str = "Run verification suite",
) -> dict[str, Any]:
    """Build a default valid checkpoint structure conforming to compact-working-state."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "contract_type": "compact-working-state",
        "checkpoint_id": f"CHK-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp": now_iso,
        "current_goal": goal,
        "work_type": work_type,
        "phase_control": {
            "current_phase": "active_phase",
            "total_phases": 1,
            "phase_name": phase_name,
            "status": "in_progress",
            "active_owner": "@agent-coordinator",
        },
        "active_constraints": [
            "Maintain minimal change principle",
            "Keep all modified skills under 200 lines",
        ],
        "files_modified_and_inspected": {
            "modified": [],
            "inspected": [],
        },
        "decisions_and_tradeoffs": [],
        "verification_and_evidence": [],
        "failed_attempts_and_antipatterns": [],
        "preserved_invariants": [
            "All existing validation gates must pass",
        ],
        "next_single_safe_action": next_action,
        "compaction_metrics": {
            "token_compression_ratio": 5.0,
            "critical_retention_rate": 1.0,
            "goal_drift_metric": 0.0,
            "tool_reinvocation_waste": 0.0,
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="compact-context.py",
        description="Deterministic CLI for agent context compaction, TOC truncation, and checkpoint validation.",
    )
    parser.add_argument(
        "--input", "-i",
        default=None,
        help="Path to input text/log/checkpoint file (default: stdin if not specified).",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path to write output result (default: stdout).",
    )
    parser.add_argument(
        "--truncate", "-t",
        action="store_true",
        help="Apply Head-Tail TOC truncation to the input text or code fences.",
    )
    parser.add_argument(
        "--head-lines",
        type=int,
        default=5,
        help="Number of initial lines to retain during TOC truncation (default: 5).",
    )
    parser.add_argument(
        "--tail-lines",
        type=int,
        default=15,
        help="Number of trailing lines to retain during TOC truncation (default: 15).",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the input JSON file against compact-working-state.json.",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create a scaffolded valid compact-working-state JSON checkpoint.",
    )
    parser.add_argument(
        "--goal",
        default="Execute assigned task",
        help="Goal for scaffolded checkpoint (used with --create).",
    )
    parser.add_argument(
        "--work-type",
        choices=sorted(WORK_TYPES),
        default="feature",
        help="Work type for scaffolded checkpoint (default: feature).",
    )
    parser.add_argument(
        "--next-action",
        default="Run verification command",
        help="Next single safe action for scaffolded checkpoint.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format: markdown (in-context checkpoint) or json (machine contract).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Creation mode
    if args.create:
        checkpoint = build_default_checkpoint(
            goal=args.goal,
            work_type=args.work_type,
            next_action=args.next_action,
        )
        if args.format == "json":
            out_str = json.dumps(checkpoint, indent=2) + "\n"
        else:
            out_str = format_markdown_checkpoint(checkpoint) + "\n"

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out_str, encoding="utf-8")
        else:
            sys.stdout.write(out_str)
        return 0

    # Read input from file or stdin
    raw_input: str
    if args.input:
        in_path = Path(args.input)
        if not in_path.exists():
            sys.stderr.write(f"Error: input file does not exist: {in_path}\n")
            return 2
        raw_input = in_path.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            sys.stderr.write("Error: no input file provided and stdin is empty.\n")
            return 2
        raw_input = sys.stdin.read()

    # Validation mode
    if args.validate:
        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"Validation failed: input is not valid JSON: {exc}\n")
            return 1

        errors = validate_checkpoint_data(data)
        if errors:
            sys.stderr.write("Validation failed with errors:\n")
            for err in errors:
                sys.stderr.write(f"- {err}\n")
            return 1
        print("Validation passed: checkpoint conforms to compact-working-state.json.")
        return 0

    # Truncation mode
    if args.truncate:
        if "```" in raw_input:
            result = truncate_code_fences(raw_input, args.head_lines, args.tail_lines)
        else:
            result = truncate_tool_output(raw_input, args.head_lines, args.tail_lines)

        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result + ("\n" if not result.endswith("\n") else ""))
        return 0

    # If input is JSON checkpoint and user requested markdown or json format conversion
    try:
        data = json.loads(raw_input)
        if isinstance(data, dict) and data.get("contract_type") == "compact-working-state":
            if args.format == "markdown":
                out_str = format_markdown_checkpoint(data) + "\n"
            else:
                out_str = json.dumps(data, indent=2) + "\n"

            if args.output:
                Path(args.output).write_text(out_str, encoding="utf-8")
            else:
                sys.stdout.write(out_str)
            return 0
    except Exception:
        pass

    # Default fallback: apply TOC truncation
    truncated = truncate_tool_output(raw_input, args.head_lines, args.tail_lines)
    if args.output:
        Path(args.output).write_text(truncated, encoding="utf-8")
    else:
        sys.stdout.write(truncated + ("\n" if not truncated.endswith("\n") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
