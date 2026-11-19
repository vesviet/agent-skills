#!/usr/bin/env python3
"""7-Dimension Session Forensics CLI for agent-skills.

Analyzes Antigravity session transcripts (transcript.jsonl) or OpenTelemetry
GenAI span logs (core/observability/spans/<trace_id>.jsonl) across 7 dimensions:
1. skill_timeline    2. plan_adherence   3. repeated_work   4. stumbles
5. quality_evidence  6. request_conflicts 7. cost_and_time

Every emitted finding includes an exact file:line citation. Supports --scrub
redaction for safe issue-tracker sharing and --self-test verification.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-(?:proj-|live-|test-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{20,}\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
)

VERIFY_CMD_RE = re.compile(
    r"\b(pytest|unittest|validate-all\.py|npm\s+test|node\s+--test|go\s+test|cargo\s+test|vitest|jest|hugo|eslint|ruff|mypy)\b",
    re.IGNORECASE,
)

CORRECTION_RE = re.compile(
    r"\b(no,|nope|stop|wait|don't|do not|wrong|instead|revert|actually|fix that|not what|sai rồi|dừng|sửa lại|không phải)\b",
    re.IGNORECASE,
)

SLASH_CMD_RE = re.compile(r"(?:^|\s)(/[a-z][a-z0-9-]{1,40})\b")
ROLE_OR_SKILL_RE = re.compile(r"([A-Za-z0-9_./\\-]+(?:SKILL\.md|core[\\/]+roles[\\/]+[a-z0-9-]+\.md))")


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = Counter(value)
    length = len(value)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())


def scrub_text(text: str) -> tuple[str, int]:
    redactions = 0
    result = text
    for pat in SECRET_PATTERNS:
        matches = pat.findall(result)
        if matches:
            redactions += len(matches)
            result = pat.sub("[REDACTED]", result)

    def _replace_high_entropy(match: re.Match[str]) -> str:
        nonlocal redactions
        tok = match.group(0)
        if "/" in tok or "\\" in tok or "." in tok:
            return tok
        if len(tok) >= 24 and shannon_entropy(tok) > 4.5:
            redactions += 1
            return "[REDACTED:ENTROPY]"
        return tok

    result = re.sub(r"\b[A-Za-z0-9_\-+=]{24,}\b", _replace_high_entropy, result)
    return result, redactions


def scrub_obj(obj: Any) -> tuple[Any, int]:
    if isinstance(obj, str):
        return scrub_text(obj)
    if isinstance(obj, list):
        total = 0
        out = []
        for item in obj:
            v, c = scrub_obj(item)
            out.append(v)
            total += c
        return out, total
    if isinstance(obj, dict):
        total = 0
        out = {}
        for k, val in obj.items():
            v, c = scrub_obj(val)
            out[k] = v
            total += c
        return out, total
    return obj, 0


def parse_iso_ts(raw: str | None) -> float | None:
    if not raw or not isinstance(raw, str):
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def detect_schema(records: list[tuple[int, dict[str, Any]]]) -> str:
    for _, rec in records:
        if "span_id" in rec and "trace_id" in rec:
            return "otel_spans"
        if "step_index" in rec or "tool_calls" in rec or "type" in rec:
            return "antigravity_transcript"
    return "unknown"


def _cite(source_label: str, line_no: int) -> str:
    return f"{source_label}:{line_no}"


def analyze_transcript(
    records: list[tuple[int, dict[str, Any]]], source_label: str
) -> dict[str, Any]:
    skill_timeline: list[dict[str, Any]] = []
    plan_refs: list[dict[str, Any]] = []
    mutated_files: list[dict[str, Any]] = []
    call_counter: Counter[str] = Counter()
    call_lines: dict[str, list[int]] = {}
    stumbles: list[dict[str, Any]] = []
    request_conflicts: list[dict[str, Any]] = []
    verify_runs: list[dict[str, Any]] = []
    last_edit_line = 0
    last_verify_pass_line = 0
    timestamps: list[float] = []

    for line_no, rec in records:
        cite = _cite(source_label, line_no)
        ts = parse_iso_ts(rec.get("created_at"))
        if ts is not None:
            timestamps.append(ts)

        rec_type = str(rec.get("type", ""))
        status = str(rec.get("status", ""))
        content = str(rec.get("content", "") or "")

        if status.upper() == "ERROR" or "Command exited with code 1" in content or "AssertionError" in content:
            stumbles.append(
                {
                    "citation": cite,
                    "type": rec_type or "step",
                    "status": status or "ERROR",
                    "excerpt": content[:160].replace("\n", " "),
                }
            )

        if rec_type == "USER_INPUT":
            for cmd in SLASH_CMD_RE.findall(content):
                skill_timeline.append({"citation": cite, "event": "slash_command", "target": cmd})
            if CORRECTION_RE.search(content):
                request_conflicts.append({"citation": cite, "excerpt": content[:160].replace("\n", " ")})

        for match in ROLE_OR_SKILL_RE.findall(content):
            skill_timeline.append({"citation": cite, "event": "context_reference", "target": match})

        tool_calls = rec.get("tool_calls") or []
        if isinstance(tool_calls, list):
            for tc in tool_calls:
                if not isinstance(tc, dict):
                    continue
                name = str(tc.get("name") or tc.get("tool") or "unknown")
                args = tc.get("arguments") or tc.get("args") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {"raw": args}
                if not isinstance(args, dict):
                    args = {"raw": str(args)}

                sig = f"{name}:{json.dumps(args, sort_keys=True, ensure_ascii=False)}"
                call_counter[sig] += 1
                call_lines.setdefault(sig, []).append(line_no)

                path_arg = str(args.get("Path") or args.get("path") or "")
                if path_arg:
                    if "SKILL.md" in path_arg or "/roles/" in path_arg.replace("\\", "/"):
                        skill_timeline.append({"citation": cite, "event": name, "target": path_arg})
                    if any(k in path_arg.lower() for k in ("plan", "spec", "coordination-plan")):
                        plan_refs.append({"citation": cite, "tool": name, "path": path_arg})
                    if name in ("edit_file", "write_file"):
                        last_edit_line = max(last_edit_line, line_no)
                        mutated_files.append({"citation": cite, "tool": name, "path": path_arg})

                cmd_arg = str(args.get("CommandLine") or args.get("command") or "")
                if cmd_arg and VERIFY_CMD_RE.search(cmd_arg):
                    passed = status.upper() != "ERROR"
                    if passed:
                        last_verify_pass_line = max(last_verify_pass_line, line_no)
                    verify_runs.append(
                        {"citation": cite, "command": cmd_arg[:140], "status": status or "DONE"}
                    )

    repeated_work = [
        {
            "signature": sig[:160],
            "count": cnt,
            "citations": [_cite(source_label, ln) for ln in call_lines[sig][:5]],
        }
        for sig, cnt in call_counter.most_common()
        if cnt >= 3
    ]

    duration_s = round(max(timestamps) - min(timestamps), 2) if len(timestamps) >= 2 else 0.0
    verified_after_last_edit = (last_edit_line == 0) or (last_verify_pass_line > last_edit_line)

    return {
        "schema": "antigravity_transcript",
        "source": source_label,
        "dimensions": {
            "skill_timeline": {"count": len(skill_timeline), "events": skill_timeline[:25]},
            "plan_adherence": {
                "plan_references": plan_refs[:15],
                "mutated_files_count": len(mutated_files),
                "mutated_files": mutated_files[:25],
            },
            "repeated_work": {"flagged_loops": len(repeated_work), "items": repeated_work[:15]},
            "stumbles": {"count": len(stumbles), "items": stumbles[:20]},
            "quality_evidence": {
                "verification_runs": len(verify_runs),
                "last_edit_citation": _cite(source_label, last_edit_line) if last_edit_line else None,
                "last_verify_citation": _cite(source_label, last_verify_pass_line) if last_verify_pass_line else None,
                "verified_after_last_edit": verified_after_last_edit,
                "runs": verify_runs[:15],
            },
            "request_conflicts": {"count": len(request_conflicts), "items": request_conflicts[:15]},
            "cost_and_time": {
                "total_steps": len(records),
                "duration_seconds": duration_s,
                "error_rate_pct": round((len(stumbles) / max(len(records), 1)) * 100.0, 2),
                "total_tokens": None,
                "cost_usd": None,
            },
        },
    }


def analyze_otel_spans(
    records: list[tuple[int, dict[str, Any]]], source_label: str
) -> dict[str, Any]:
    skill_timeline: list[dict[str, Any]] = []
    mutated_files: list[dict[str, Any]] = []
    call_counter: Counter[str] = Counter()
    call_lines: dict[str, list[int]] = {}
    stumbles: list[dict[str, Any]] = []
    verify_runs: list[dict[str, Any]] = []
    total_tokens = 0
    total_cost = 0.0
    total_duration_ms = 0.0
    roles_seen: Counter[str] = Counter()

    for line_no, rec in records:
        cite = _cite(source_label, line_no)
        op = str(rec.get("operation", "unknown"))
        role = str(rec.get("role", "unknown"))
        tool = str(rec.get("tool") or rec.get("attributes", {}).get("tool.name") or "")
        status = str(rec.get("status", "OK"))
        roles_seen[role] += 1

        if op in ("invoke_agent", "plan") or role != "unknown":
            skill_timeline.append({"citation": cite, "event": op, "target": f"@{role}"})

        sig = f"{role}:{op}:{tool or rec.get('name', '')}"
        call_counter[sig] += 1
        call_lines.setdefault(sig, []).append(line_no)

        if status.upper() != "OK":
            stumbles.append(
                {
                    "citation": cite,
                    "type": op,
                    "status": status,
                    "excerpt": str(rec.get("error") or rec.get("attributes", {}).get("error.message") or status)[:160],
                }
            )

        attrs = rec.get("attributes") if isinstance(rec.get("attributes"), dict) else {}
        cmd = str(attrs.get("command") or attrs.get("tool.command") or "")
        if cmd and VERIFY_CMD_RE.search(cmd):
            verify_runs.append({"citation": cite, "command": cmd[:140], "status": status})
        if tool in ("edit_file", "write_file"):
            mutated_files.append({"citation": cite, "tool": tool, "path": str(attrs.get("path", "unknown"))})

        usage = rec.get("tokens") if isinstance(rec.get("tokens"), dict) else {}
        inp = int(usage.get("input", attrs.get("gen_ai.usage.input_tokens", 0)) or 0)
        out = int(usage.get("output", attrs.get("gen_ai.usage.output_tokens", 0)) or 0)
        total_tokens += inp + out
        total_cost += float(rec.get("cost_usd", attrs.get("gen_ai.usage.cost_usd", 0.0)) or 0.0)
        total_duration_ms += float(rec.get("duration_ms", 0.0) or 0.0)

    repeated_work = [
        {
            "signature": sig[:160],
            "count": cnt,
            "citations": [_cite(source_label, ln) for ln in call_lines[sig][:5]],
        }
        for sig, cnt in call_counter.most_common()
        if cnt >= 3
    ]

    return {
        "schema": "otel_spans",
        "source": source_label,
        "dimensions": {
            "skill_timeline": {"count": len(skill_timeline), "events": skill_timeline[:25]},
            "plan_adherence": {
                "roles_distribution": dict(roles_seen),
                "mutated_files_count": len(mutated_files),
                "mutated_files": mutated_files[:25],
            },
            "repeated_work": {"flagged_loops": len(repeated_work), "items": repeated_work[:15]},
            "stumbles": {"count": len(stumbles), "items": stumbles[:20]},
            "quality_evidence": {
                "verification_runs": len(verify_runs),
                "verified_after_last_edit": True if not mutated_files or verify_runs else False,
                "runs": verify_runs[:15],
            },
            "request_conflicts": {"count": 0, "items": []},
            "cost_and_time": {
                "total_steps": len(records),
                "duration_seconds": round(total_duration_ms / 1000.0, 3),
                "error_rate_pct": round((len(stumbles) / max(len(records), 1)) * 100.0, 2),
                "total_tokens": total_tokens,
                "cost_usd": round(total_cost, 6),
            },
        },
    }


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    records: list[tuple[int, dict[str, Any]]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
            if isinstance(obj, dict):
                records.append((idx, obj))
        except json.JSONDecodeError:
            records.append((idx, {"type": "PARSE_ERROR", "status": "ERROR", "content": stripped[:160]}))
    return records


def diagnose_file(path: Path, scrub: bool = False) -> dict[str, Any]:
    records = load_jsonl(path)
    schema = detect_schema(records)
    label = path.name
    report = analyze_otel_spans(records, label) if schema == "otel_spans" else analyze_transcript(records, label)
    redactions = 0
    if scrub:
        report, redactions = scrub_obj(report)
    report["scrubbed"] = scrub
    report["redactions_count"] = redactions
    return report


def render_markdown(report: dict[str, Any]) -> str:
    dims = report["dimensions"]
    ct = dims["cost_and_time"]
    qe = dims["quality_evidence"]
    lines = [
        f"# 7-Dimension Session Forensics Report (`{report['source']}`)",
        "",
        f"- **Schema**: `{report['schema']}` | **Scrubbed**: `{report['scrubbed']}` (`{report['redactions_count']}` redactions)",
        f"- **Steps / Spans**: `{ct['total_steps']}` | **Duration**: `{ct['duration_seconds']}s` | **Error Rate**: `{ct['error_rate_pct']}%`",
        f"- **Tokens / Cost**: `{ct['total_tokens']}` tokens / `${ct['cost_usd']}` USD",
        "",
        "## Dimension Summary",
        "",
        "| # | Dimension | Signal |",
        "|---|---|---|",
        f"| 1 | `skill_timeline` | {dims['skill_timeline']['count']} skill/role events |",
        f"| 2 | `plan_adherence` | {dims['plan_adherence']['mutated_files_count']} mutated file events |",
        f"| 3 | `repeated_work` | {dims['repeated_work']['flagged_loops']} repeated loop(s) (>=3x) |",
        f"| 4 | `stumbles` | {dims['stumbles']['count']} error/failure event(s) |",
        f"| 5 | `quality_evidence` | {qe['verification_runs']} verification run(s); verified_after_last_edit=`{qe['verified_after_last_edit']}` |",
        f"| 6 | `request_conflicts` | {dims['request_conflicts']['count']} user correction/reversal signal(s) |",
        f"| 7 | `cost_and_time` | {ct['total_steps']} steps, {ct['duration_seconds']}s, {ct['error_rate_pct']}% errors |",
    ]

    if dims["stumbles"]["items"]:
        lines += ["", "## Cited Stumbles"]
        for item in dims["stumbles"]["items"][:10]:
            lines.append(f"- `{item['citation']}` [{item['status']}]: {item['excerpt']}")

    if dims["repeated_work"]["items"]:
        lines += ["", "## Repeated Work Loops"]
        for item in dims["repeated_work"]["items"][:10]:
            cites = ", ".join(f"`{c}`" for c in item["citations"])
            lines.append(f"- `{item['count']}x` `{item['signature']}` ({cites})")

    if dims["request_conflicts"]["items"]:
        lines += ["", "## User Corrections / Request Conflicts"]
        for item in dims["request_conflicts"]["items"][:10]:
            lines.append(f"- `{item['citation']}`: {item['excerpt']}")

    return "\n".join(lines) + "\n"


def run_self_test() -> int:
    synthetic_secret = "ghp" + "_" + "SelfTestToken1234567890ABCDEFGH"
    with tempfile.TemporaryDirectory() as tmp:
        t_path = Path(tmp) / "transcript.jsonl"
        rows = [
            {"step_index": 1, "type": "USER_INPUT", "status": "DONE", "created_at": "2026-11-19T10:00:00Z", "content": "/review-code check auth"},
            {"step_index": 2, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:05Z", "tool_calls": [{"name": "read_file", "arguments": {"Path": "core/skills/repo-ops/review-code/SKILL.md"}}]},
            {"step_index": 3, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:10Z", "tool_calls": [{"name": "read_file", "arguments": {"Path": "app.py"}}]},
            {"step_index": 4, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:12Z", "tool_calls": [{"name": "read_file", "arguments": {"Path": "app.py"}}]},
            {"step_index": 5, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:14Z", "tool_calls": [{"name": "read_file", "arguments": {"Path": "app.py"}}]},
            {"step_index": 6, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:20Z", "tool_calls": [{"name": "edit_file", "arguments": {"Path": "app.py"}}]},
            {"step_index": 7, "type": "TOOL_RESULT", "status": "ERROR", "created_at": "2026-11-19T10:00:25Z", "content": f"AssertionError leak {synthetic_secret} user@example.com"},
            {"step_index": 8, "type": "USER_INPUT", "status": "DONE", "created_at": "2026-11-19T10:00:30Z", "content": "No, revert that change and run pytest"},
            {"step_index": 9, "type": "PLANNER_RESPONSE", "status": "DONE", "created_at": "2026-11-19T10:00:40Z", "tool_calls": [{"name": "run_command", "arguments": {"CommandLine": "python -m pytest tests/ -q"}}]},
        ]
        t_path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        rep = diagnose_file(t_path, scrub=True)
        dims = rep["dimensions"]
        assert rep["schema"] == "antigravity_transcript"
        assert dims["skill_timeline"]["count"] >= 2
        assert dims["repeated_work"]["flagged_loops"] == 1
        assert dims["stumbles"]["count"] == 1
        assert dims["quality_evidence"]["verified_after_last_edit"] is True
        assert dims["request_conflicts"]["count"] == 1
        assert rep["redactions_count"] >= 2
        assert synthetic_secret not in json.dumps(rep)

        s_path = Path(tmp) / "trace.jsonl"
        spans = [
            {"trace_id": "a" * 32, "span_id": "b" * 16, "operation": "invoke_agent", "role": "agent-coordinator", "status": "OK", "duration_ms": 420.0, "tokens": {"input": 1000, "output": 200}, "cost_usd": 0.006},
            {"trace_id": "a" * 32, "span_id": "c" * 16, "operation": "execute_tool", "role": "backend-developer", "tool": "run_tests", "status": "ERROR", "duration_ms": 180.0, "error": "exit 1", "tokens": {"input": 500, "output": 100}, "cost_usd": 0.003},
        ]
        s_path.write_text("\n".join(json.dumps(r) for r in spans) + "\n", encoding="utf-8")
        s_rep = diagnose_file(s_path, scrub=False)
        assert s_rep["schema"] == "otel_spans"
        assert s_rep["dimensions"]["cost_and_time"]["total_tokens"] == 1800
        assert s_rep["dimensions"]["stumbles"]["count"] == 1
    print("Session forensics self-test passed: transcript + OTel spans + scrub verified.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="7-Dimension Session Forensics for agent-skills")
    parser.add_argument("input_path", nargs="?", help="Path to transcript.jsonl or OTel spans .jsonl")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--scrub", action="store_true", help="Redact secrets, high-entropy tokens, and emails")
    parser.add_argument("--self-test", action="store_true", help="Run built-in forensic verification tests")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.input_path:
        parser.error("Provide input_path or pass --self-test")

    target = Path(args.input_path)
    if not target.is_file():
        sys.stderr.write(f"Error: file not found: {target}\n")
        return 1

    report = diagnose_file(target, scrub=args.scrub)
    if args.format == "json":
        sys.stdout.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
