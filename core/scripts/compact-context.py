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
import uuid
from pathlib import Path
from typing import Any

SCHEMA_FILE = Path(__file__).resolve().parent.parent / "contracts" / "schemas" / "compact-working-state.json"
SPILLOVER_DIR = Path(".agent/outputs")
MAX_TOOL_OUTPUT_BYTES = 4096  # 4 KB threshold
DEFAULT_TOKEN_BUDGET = 1000   # ~4,000 characters
DEFAULT_HEAD_RATIO = 0.20
DEFAULT_TAIL_RATIO = 0.80

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
    text: str,
    head_lines: int | None = None,
    tail_lines: int | None = None,
    head_ratio: float = DEFAULT_HEAD_RATIO,
    tail_ratio: float = DEFAULT_TAIL_RATIO,
    budget_lines: int = 20,
) -> str:
    """Apply Head-Tail Syntax-Aware Truncation (TOC) to verbose output text."""
    lines = text.splitlines()

    if head_lines is None and tail_lines is None:
        head_lines = max(1, int(round(budget_lines * head_ratio)))
        tail_lines = max(1, int(round(budget_lines * tail_ratio)))
    elif head_lines is None:
        head_lines = 5
    elif tail_lines is None:
        tail_lines = 15

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


def _line_based_toc_truncate(
    text: str,
    budget_lines: int = 20,
    head_ratio: float = DEFAULT_HEAD_RATIO,
    tail_ratio: float = DEFAULT_TAIL_RATIO,
) -> str:
    """Line-based 20% Head / 80% Tail TOC formatting with explicit banners."""
    lines = text.splitlines()
    if len(lines) <= budget_lines:
        return text

    head_n = max(1, int(round(budget_lines * head_ratio)))
    tail_n = max(1, int(round(budget_lines * tail_ratio)))

    if head_n + tail_n >= len(lines):
        return text

    head_lines = lines[:head_n]
    tail_lines = lines[-tail_n:] if tail_n > 0 else []
    omitted_lines = len(lines) - head_n - tail_n

    formatted_parts = [
        f"--- HEAD (First {head_n} lines) ---",
        *head_lines,
        f"... [Truncated {omitted_lines} lines of execution output] ...",
        f"--- TAIL (Last {tail_n} lines) ---",
        *tail_lines,
    ]
    return "\n".join(formatted_parts)


def syntax_aware_toc_truncate(
    text: str,
    budget_chars: int = 4000,
    budget_lines: int | None = None,
    head_ratio: float = DEFAULT_HEAD_RATIO,
    tail_ratio: float = DEFAULT_TAIL_RATIO,
    spill_to_disk: bool = True,
    call_id: str | None = None,
    spill_dir: Path | str | None = None,
    retained_items: int | None = None,
) -> str:
    """Apply syntax-aware 20% Head / 80% Tail TOC truncation with 4 KB disk spillover.

    Preserves:
      - Valid JSON array and object structures (injecting structured _truncated marker).
      - Markdown code fence opening language tags and closing ``` fences.
      - Terminal failure frames and exception lines in error stack traces.
      - Disk spillover to .agent/outputs/<call_id>.log for outputs > 4,096 bytes (4 KB).
    """
    if not text:
        return text

    raw_bytes = len(text.encode("utf-8"))
    lines = text.splitlines()
    total_lines = len(lines)

    # 1. Disk spillover check (> 4,096 bytes)
    spill_notice = ""
    if spill_to_disk and raw_bytes > MAX_TOOL_OUTPUT_BYTES:
        cid = call_id or f"cmd_{uuid.uuid4().hex[:8]}"
        out_dir = Path(spill_dir) if spill_dir else SPILLOVER_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        spill_file = out_dir / f"{cid}.log"
        spill_file.write_text(text, encoding="utf-8")
        spill_notice = (
            f"[OUTPUT TRUNCATED: {total_lines} lines ({raw_bytes} bytes) spilled to {spill_file.as_posix()}]\n"
        )

    # 2. Check if text is short enough that no truncation is needed
    eff_budget_lines = budget_lines if budget_lines is not None else 20
    if raw_bytes <= budget_chars and total_lines <= eff_budget_lines and not (text.strip().startswith("{") or text.strip().startswith("[")):
        return f"{spill_notice}{text}" if spill_notice else text

    # 3. Structured JSON handling
    stripped = text.strip()
    is_fenced_json = False
    fenced_open = ""
    fenced_close = ""

    # Check for markdown fenced json
    if stripped.startswith("```json") and stripped.endswith("```"):
        first_newline = stripped.find("\n")
        if first_newline != -1:
            fenced_open = stripped[: first_newline + 1]
            fenced_close = "\n```"
            json_body = stripped[first_newline + 1 : -3].strip()
            try:
                json.loads(json_body)
                stripped = json_body
                is_fenced_json = True
            except Exception:
                pass

    if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
        try:
            parsed = json.loads(stripped)
            json_modified = False

            if isinstance(parsed, list) and len(parsed) > 10:
                k_items = retained_items if retained_items is not None else 10
                k_items = min(k_items, len(parsed) - 1)
                head_count = max(1, int(round(k_items * head_ratio)))
                tail_count = max(1, int(round(k_items * tail_ratio)))
                if head_count + tail_count >= len(parsed):
                    tail_count = max(1, len(parsed) - head_count - 1)
                omitted = len(parsed) - head_count - tail_count
                if omitted > 0:
                    marker = {"_truncated": f"... [{omitted} items omitted for context compaction] ..."}
                    parsed = parsed[:head_count] + [marker] + parsed[-tail_count:]
                    json_modified = True

            elif isinstance(parsed, dict):
                for k, v in list(parsed.items()):
                    if isinstance(v, list) and len(v) > 10:
                        k_items = retained_items if retained_items is not None else 10
                        k_items = min(k_items, len(v) - 1)
                        head_count = max(1, int(round(k_items * head_ratio)))
                        tail_count = max(1, int(round(k_items * tail_ratio)))
                        if head_count + tail_count >= len(v):
                            tail_count = max(1, len(v) - head_count - 1)
                        omitted = len(v) - head_count - tail_count
                        if omitted > 0:
                            marker = {"_truncated": f"... [{omitted} items omitted for context compaction] ..."}
                            parsed[k] = v[:head_count] + [marker] + v[-tail_count:]
                            json_modified = True

            if json_modified:
                formatted_json = json.dumps(parsed, indent=2)
                if is_fenced_json:
                    formatted_json = f"{fenced_open}{formatted_json}{fenced_close}"
                return f"{spill_notice}{formatted_json}" if spill_notice else formatted_json

        except Exception:
            pass

    # 4. Code fence preservation (entire text is single fence)
    fence_pattern = re.compile(r"^(```[a-zA-Z0-9_\-\.]*\n)([\s\S]*?)(\n?```)$")
    m = fence_pattern.match(stripped)
    if m:
        open_tag = m.group(1)
        body = m.group(2)
        close_tag = "\n```" if not m.group(3).startswith("\n") else m.group(3)
        body_truncated = _line_based_toc_truncate(
            body,
            budget_lines=eff_budget_lines,
            head_ratio=head_ratio,
            tail_ratio=tail_ratio,
        )
        wrapped = f"{open_tag}{body_truncated}{close_tag}"
        return f"{spill_notice}{wrapped}" if spill_notice else wrapped

    # 5. Embedded code fences in mixed text
    if "```" in text:
        pattern = re.compile(r"(```[a-zA-Z0-9_\-\.]*\n)([\s\S]*?)(```)")
        def _replace(match: re.Match[str]) -> str:
            op = match.group(1)
            b = match.group(2)
            cl = match.group(3)
            tb = _line_based_toc_truncate(
                b,
                budget_lines=eff_budget_lines,
                head_ratio=head_ratio,
                tail_ratio=tail_ratio,
            )
            return f"{op}{tb}\n{cl}"
        fenced_res = pattern.sub(_replace, text)
        return f"{spill_notice}{fenced_res}" if spill_notice else fenced_res

    # 6. Standard line-based 20% Head / 80% Tail TOC
    truncated_lines = _line_based_toc_truncate(
        text,
        budget_lines=eff_budget_lines,
        head_ratio=head_ratio,
        tail_ratio=tail_ratio,
    )
    if spill_notice:
        return f"{spill_notice.rstrip()}\n{truncated_lines}"
    return truncated_lines


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


def test_spillover_on_large_payload() -> None:
    line = "Line of debug trace output from long execution " * 4 + "\n"
    payload = line * 50 + "Terminal error: exit code 1\n"
    raw_bytes = len(payload.encode("utf-8"))
    assert raw_bytes > MAX_TOOL_OUTPUT_BYTES, f"Payload must exceed 4 KB, got {raw_bytes} bytes"

    test_cid = "test_spill_call_synth"
    spill_path = SPILLOVER_DIR / f"{test_cid}.log"
    try:
        res = syntax_aware_toc_truncate(payload, spill_to_disk=True, call_id=test_cid)

        expected_spill_file = f".agent/outputs/{test_cid}.log"
        assert "[OUTPUT TRUNCATED:" in res, "Spillover header missing from result"
        assert f"spilled to {expected_spill_file}" in res, f"Spill path '{expected_spill_file}' missing from result"
        assert f"({raw_bytes} bytes)" in res, "Byte count missing from spill header"

        assert spill_path.exists(), f"Spill file {spill_path} was not created on disk"
        assert spill_path.read_text(encoding="utf-8") == payload, "Spill file content does not match original payload"

        # Verify payload <= 4 KB does NOT spill
        small_payload = "Short log message\nline 2\n"
        res_small = syntax_aware_toc_truncate(small_payload, spill_to_disk=True, call_id="small_call")
        assert "[OUTPUT TRUNCATED:" not in res_small, "Small payload (< 4 KB) should not trigger spillover"
        assert not (SPILLOVER_DIR / "small_call.log").exists(), "Small call file should not be created"
    finally:
        if spill_path.exists():
            spill_path.unlink()


def test_head_tail_distribution() -> None:
    lines = [f"Step {i:03d}: processing event data" for i in range(1, 101)]
    text = "\n".join(lines)

    budget_lines = 20
    truncated = syntax_aware_toc_truncate(
        text,
        budget_lines=budget_lines,
        head_ratio=0.20,
        tail_ratio=0.80,
        spill_to_disk=False,
    )

    assert "--- HEAD (First 4 lines) ---" in truncated, "Head banner missing"
    assert "--- TAIL (Last 16 lines) ---" in truncated, "Tail banner missing"
    assert "... [Truncated 80 lines of execution output] ..." in truncated, "Truncation marker missing"

    assert "Step 001: processing event data" in truncated
    assert "Step 004: processing event data" in truncated
    assert "Step 005: processing event data" not in truncated

    assert "Step 084: processing event data" not in truncated
    assert "Step 085: processing event data" in truncated
    assert "Step 100: processing event data" in truncated

    head_count = 4
    tail_count = 16
    assert head_count / (head_count + tail_count) == 0.20
    assert tail_count / (head_count + tail_count) == 0.80


def test_json_structural_integrity() -> None:
    items = [{"id": i, "val": f"item_{i:02d}", "active": True} for i in range(50)]
    json_text = json.dumps(items)

    truncated_json = syntax_aware_toc_truncate(
        json_text,
        retained_items=10,
        head_ratio=0.20,
        tail_ratio=0.80,
        spill_to_disk=False,
    )

    parsed = json.loads(truncated_json)
    assert isinstance(parsed, list), "Parsed result must remain a JSON list"

    trunc_markers = [item for item in parsed if isinstance(item, dict) and "_truncated" in item]
    assert len(trunc_markers) == 1, "Must contain exactly one _truncated marker object"
    assert "items omitted" in trunc_markers[0]["_truncated"]

    assert parsed[0]["id"] == 0
    assert parsed[1]["id"] == 1
    tail_ids = [item["id"] for item in parsed[3:]]
    assert tail_ids == list(range(42, 50))

    obj = {
        "status": "success",
        "records": [{"idx": i, "data": f"record_{i}"} for i in range(30)],
        "metadata": {"total": 30, "page": 1},
    }
    obj_text = json.dumps(obj)
    truncated_obj_str = syntax_aware_toc_truncate(obj_text, retained_items=10, spill_to_disk=False)
    parsed_obj = json.loads(truncated_obj_str)
    assert isinstance(parsed_obj, dict), "Parsed result must remain a JSON object"
    assert parsed_obj["status"] == "success"
    assert parsed_obj["metadata"]["total"] == 30
    assert any("_truncated" in item for item in parsed_obj["records"]), "Nested array must contain truncation marker"


def test_code_fence_enclosure() -> None:
    inner_code = "\n".join([f"    x_{i} = calculate_value({i})" for i in range(1, 60)])
    fenced_block = f"```python\ndef process_batch():\n{inner_code}\n    return True\n```"

    res1 = truncate_code_fences(fenced_block, head_lines=4, tail_lines=16)
    assert res1.startswith("```python\n"), "Opening code fence with language tag must be preserved"
    assert res1.endswith("\n```"), "Closing code fence must be preserved"
    assert "def process_batch():" in res1, "Head code must be preserved"
    assert "return True" in res1, "Tail code must be preserved"
    assert "Truncated" in res1

    doc = f"# Execution Log\nPre-fence description\n{fenced_block}\nPost-fence conclusion."
    res2 = syntax_aware_toc_truncate(doc, spill_to_disk=False)
    assert "```python\n" in res2, "Opening fence must not be corrupted"
    assert "\n```" in res2, "Closing fence must not be corrupted"


def test_terminal_error_preservation() -> None:
    trace_lines = [
        "2026-11-05T23:40:00Z INFO Starting test runner...",
        "2026-11-05T23:40:01Z INFO Loading configuration from config.yaml",
    ]
    trace_lines.extend([f"2026-11-05T23:40:02Z DEBUG Step {i}: verification check passed" for i in range(1, 80)])
    trace_lines.extend([
        "Traceback (most recent call last):",
        '  File "core/executor.py", line 142, in run_task',
        "    result = task.execute()",
        '  File "core/task.py", line 55, in execute',
        "    raise AssertionError('Contract schema mismatch in step 81')",
        "AssertionError: Contract schema mismatch in step 81",
        "Command failed with exit code 1",
    ])
    full_trace = "\n".join(trace_lines)

    res = syntax_aware_toc_truncate(full_trace, budget_lines=20, spill_to_disk=False)

    assert "INFO Starting test runner..." in res
    assert "Step 40: verification check passed" not in res
    assert 'File "core/task.py", line 55, in execute' in res
    assert "raise AssertionError('Contract schema mismatch in step 81')" in res
    assert "AssertionError: Contract schema mismatch in step 81" in res
    assert "Command failed with exit code 1" in res


def run_synthetic_toc_tests() -> int:
    """Automated verification suite for Syntax-Aware TOC and 4 KB spillover."""
    print("Running synthetic TOC verification tests...")

    test_spillover_on_large_payload()
    print("  [PASS] Test a: Spillover on > 4 KB payload to .agent/outputs/")

    test_head_tail_distribution()
    print("  [PASS] Test b: 20/80 Head-Tail distribution")

    test_json_structural_integrity()
    print("  [PASS] Test c: JSON structural integrity preservation")

    test_code_fence_enclosure()
    print("  [PASS] Test d: Code fence enclosure")

    test_terminal_error_preservation()
    print("  [PASS] Test e: Terminal error preservation")

    print("Synthetic TOC verification passed: all 5 tests verified.")
    return 0


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
    parser.add_argument(
        "--test-synthetic-toc",
        action="store_true",
        help="Execute automated self-test suite verifying 20/80 Head-Tail TOC, 4 KB disk spillover, and syntax preservation.",
    )
    parser.add_argument(
        "--syntax-aware",
        action="store_true",
        help="Apply syntax-aware 20%% Head / 80%% Tail TOC truncation with disk spillover.",
    )
    parser.add_argument(
        "--head-ratio",
        type=float,
        default=DEFAULT_HEAD_RATIO,
        help=f"Ratio of token/line budget allocated to Head during syntax-aware TOC (default: {DEFAULT_HEAD_RATIO}).",
    )
    parser.add_argument(
        "--tail-ratio",
        type=float,
        default=DEFAULT_TAIL_RATIO,
        help=f"Ratio of token/line budget allocated to Tail during syntax-aware TOC (default: {DEFAULT_TAIL_RATIO}).",
    )
    parser.add_argument(
        "--call-id",
        default=None,
        help="Tool execution call identifier used for .agent/outputs/<call_id>.log spillover filenames.",
    )
    parser.add_argument(
        "--spill",
        action="store_true",
        default=True,
        help="Enable disk spillover to .agent/outputs/ for outputs exceeding 4 KB (default: True).",
    )
    parser.add_argument(
        "--no-spill",
        action="store_false",
        dest="spill",
        help="Disable disk spillover for outputs exceeding 4 KB.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Automated self-test mode
    if args.test_synthetic_toc:
        return run_synthetic_toc_tests()

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
    if args.truncate or args.syntax_aware:
        raw_bytes = len(raw_input.encode("utf-8"))
        if args.syntax_aware or (raw_bytes > MAX_TOOL_OUTPUT_BYTES and args.spill):
            result = syntax_aware_toc_truncate(
                raw_input,
                head_ratio=args.head_ratio,
                tail_ratio=args.tail_ratio,
                spill_to_disk=args.spill,
                call_id=args.call_id,
            )
        elif "```" in raw_input:
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
    raw_bytes = len(raw_input.encode("utf-8"))
    if raw_bytes > MAX_TOOL_OUTPUT_BYTES and args.spill:
        truncated = syntax_aware_toc_truncate(
            raw_input,
            head_ratio=args.head_ratio,
            tail_ratio=args.tail_ratio,
            spill_to_disk=True,
            call_id=args.call_id,
        )
    else:
        truncated = truncate_tool_output(raw_input, args.head_lines, args.tail_lines)

    if args.output:
        Path(args.output).write_text(truncated, encoding="utf-8")
    else:
        sys.stdout.write(truncated + ("\n" if not truncated.endswith("\n") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
