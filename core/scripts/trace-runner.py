#!/usr/bin/env python3
"""Agent Trace Runner for agent-skills (OpenTelemetry GenAI 2026/2027 SOTA).

Provides end-to-end distributed tracing, causal span tree tracking,
FinOps token cost attribution, schema validation, and OTLP export for multi-agent workflows.

Capabilities:
1. W3C Trace Context generation & propagation (trace_id: 32 hex, span_id: 16 hex).
2. Nested causal span lifecycle management (invoke_agent -> plan -> execute_tool -> a2a_task).
3. OTel GenAI Semantic Conventions (gen_ai.request.model, gen_ai.usage.*, cost_usd).
4. Automated schema validation against `core/contracts/schemas/agent-trace-span.json`.
5. ASCII trace tree visualization with latency, token usage, and status indicators.
6. Execution wrapper (`exec`) to trace real shell commands and scripts in real time.
7. FinOps analytics dashboard (`stats`) aggregating costs, tokens, and model distribution.
8. Standard OpenTelemetry OTLP JSON export (`export`) for telemetry collectors.
9. Python programmatic API with `@traced` function decorator and ContextVar propagation.
"""

from __future__ import annotations

import argparse
import contextvars
import functools
import json
import os
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Generator

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

# Ensure robust UTF-8 encoding across Windows runners and non-UTF8 consoles
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OBSERVABILITY_DIR = REPO_ROOT / "core" / "observability"
SPANS_DIR = OBSERVABILITY_DIR / "spans"
SCHEMA_PATH = REPO_ROOT / "core" / "contracts" / "schemas" / "agent-trace-span.json"
VERSION_PATH = REPO_ROOT / "VERSION"

# Model pricing catalog ($ per 1M tokens) [Input, Output, CacheRead, Reasoning]
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-3-7-sonnet": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "reasoning": 15.0},
    "claude-3-5-sonnet": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "reasoning": 15.0},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.0, "cache_read": 0.08, "reasoning": 4.0},
    "gpt-4o": {"input": 2.50, "output": 10.0, "cache_read": 1.25, "reasoning": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.075, "reasoning": 0.60},
    "deepseek-r1": {"input": 0.55, "output": 2.19, "cache_read": 0.14, "reasoning": 2.19},
    "deepseek-v3": {"input": 0.27, "output": 1.10, "cache_read": 0.07, "reasoning": 1.10},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40, "cache_read": 0.025, "reasoning": 0.40},
}

_active_runner_ctx: contextvars.ContextVar[TraceRunner | None] = contextvars.ContextVar(
    "active_trace_runner", default=None
)


def get_pack_version() -> str:
    """Return the active version of the agent-skills pack."""
    if VERSION_PATH.is_file():
        return VERSION_PATH.read_text(encoding="utf-8").strip()
    return "5.8.0"


def generate_trace_id() -> str:
    """Generate a standard W3C 32-character hexadecimal trace ID."""
    return uuid.uuid4().hex


def generate_span_id() -> str:
    """Generate a standard W3C 16-character hexadecimal span ID."""
    return uuid.uuid4().hex[:16]


def calculate_cost_usd(
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read_tokens: int = 0,
    reasoning_tokens: int = 0,
) -> float:
    """Calculate token cost in USD based on standard model pricing."""
    pricing = MODEL_PRICING.get(model.lower())
    if not pricing:
        pricing = MODEL_PRICING["claude-3-5-haiku"]

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    cache_cost = (cache_read_tokens / 1_000_000) * pricing.get("cache_read", 0.0)
    reasoning_cost = (reasoning_tokens / 1_000_000) * pricing.get("reasoning", pricing["output"])

    return round(input_cost + output_cost + cache_cost + reasoning_cost, 6)


class TraceRunner:
    """Engine for executing and recording OpenTelemetry GenAI agent traces."""

    def __init__(
        self,
        trace_id: str | None = None,
        session_id: str | None = None,
        service_name: str = "agent-skills",
        validate_schema: bool = True,
    ) -> None:
        self.trace_id = trace_id or generate_trace_id()
        self.session_id = session_id or f"session-{self.trace_id[:8]}"
        self.service_name = service_name
        self.service_version = get_pack_version()
        self.validate_schema = validate_schema
        self.spans: list[dict[str, Any]] = []
        self._span_stack: list[str] = []
        self._validator: Any = None
        self._token: contextvars.Token[TraceRunner | None] | None = None

        if self.validate_schema and Draft202012Validator and SCHEMA_PATH.is_file():
            try:
                schema_json = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
                self._validator = Draft202012Validator(schema_json)
            except Exception:
                self._validator = None

        SPANS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_active(cls) -> TraceRunner | None:
        """Return the current active TraceRunner in context."""
        return _active_runner_ctx.get()

    def __enter__(self) -> TraceRunner:
        self._token = _active_runner_ctx.set(self)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._token:
            _active_runner_ctx.reset(self._token)
            self._token = None

    @property
    def current_parent_span_id(self) -> str | None:
        """Return the current parent span ID from the active stack."""
        return self._span_stack[-1] if self._span_stack else None

    @contextmanager
    def span(
        self,
        operation: str,
        role: str,
        span_kind: str = "INTERNAL",
        model: str = "claude-3-7-sonnet",
        input_tokens: int = 0,
        output_tokens: int = 0,
        reasoning_tokens: int = 0,
        cache_read_tokens: int = 0,
        cache_creation_tokens: int = 0,
        tool_name: str | None = None,
        tool_action: str | None = None,
        task_id: str | None = None,
        extra_attributes: dict[str, Any] | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Context manager to start, time, track, and record a trace span."""
        span_id = generate_span_id()
        parent_id = self.current_parent_span_id
        start_time = datetime.now(timezone.utc).isoformat()
        t0 = time.monotonic()

        self._span_stack.append(span_id)

        span_data: dict[str, Any] = {
            "trace_id": self.trace_id,
            "span_id": span_id,
            **({"parent_span_id": parent_id} if parent_id else {}),
            "session_id": self.session_id,
            "role": role,
            "operation": operation,
            "span_kind": span_kind,
            "start_time": start_time,
            "status": "ok",
            "resource": {
                "service.name": self.service_name,
                "service.version": self.service_version,
            },
            "attributes": {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "reasoning_tokens": reasoning_tokens,
                "cache_read_tokens": cache_read_tokens,
                "cache_creation_tokens": cache_creation_tokens,
                "finish_reasons": ["stop"],
                **({"tool_name": tool_name} if tool_name else {}),
                **({"tool.action": tool_action} if tool_action else {}),
                **({"task_id": task_id} if task_id else {}),
                **(extra_attributes or {}),
            },
        }

        try:
            yield span_data
        except Exception as exc:
            span_data["status"] = "error"
            span_data["attributes"]["error_type"] = type(exc).__name__
            span_data["attributes"]["error_message"] = str(exc)
            raise
        finally:
            duration_ms = round((time.monotonic() - t0) * 1000, 2)
            span_data["end_time"] = datetime.now(timezone.utc).isoformat()
            span_data["attributes"]["duration_ms"] = duration_ms

            attrs = span_data["attributes"]
            cost = calculate_cost_usd(
                model=attrs.get("model", model),
                input_tokens=attrs.get("input_tokens", 0),
                output_tokens=attrs.get("output_tokens", 0),
                cache_read_tokens=attrs.get("cache_read_tokens", 0),
                reasoning_tokens=attrs.get("reasoning_tokens", 0),
            )
            attrs["cost_usd"] = cost

            if self._validator:
                errors = list(self._validator.iter_errors(span_data))
                if errors:
                    span_data["attributes"]["schema_validation_errors"] = [e.message for e in errors]

            self.spans.append(span_data)
            self._persist_span(span_data)
            self._span_stack.pop()

    def validate_span_schema(self, span: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate an individual span against agent-trace-span schema."""
        if not self._validator:
            return True, []
        errors = [e.message for e in self._validator.iter_errors(span)]
        return len(errors) == 0, errors

    def _persist_span(self, span_data: dict[str, Any]) -> None:
        """Append span to the session's JSONL trace file."""
        log_file = SPANS_DIR / f"{self.trace_id}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(span_data, ensure_ascii=False) + "\n")

    def export_summary(self) -> dict[str, Any]:
        """Aggregate token usage, total duration, and cost across all recorded spans."""
        total_input = sum(s["attributes"].get("input_tokens", 0) for s in self.spans)
        total_output = sum(s["attributes"].get("output_tokens", 0) for s in self.spans)
        total_reasoning = sum(s["attributes"].get("reasoning_tokens", 0) for s in self.spans)
        total_cache_read = sum(s["attributes"].get("cache_read_tokens", 0) for s in self.spans)
        total_cost = sum(s["attributes"].get("cost_usd", 0.0) for s in self.spans)
        total_duration = sum(s["attributes"].get("duration_ms", 0.0) for s in self.spans)
        has_errors = any(s["status"] == "error" for s in self.spans)

        return {
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "span_count": len(self.spans),
            "status": "error" if has_errors else "ok",
            "total_duration_ms": round(total_duration, 2),
            "total_cost_usd": round(total_cost, 6),
            "tokens": {
                "input": total_input,
                "output": total_output,
                "reasoning": total_reasoning,
                "cache_read": total_cache_read,
                "total": total_input + total_output,
            },
        }

    def to_otlp_json(self) -> dict[str, Any]:
        """Convert recorded spans to standard OpenTelemetry OTLP JSON (v1/traces)."""
        otlp_spans: list[dict[str, Any]] = []

        for span in self.spans:
            attrs = span.get("attributes", {})
            otlp_attrs = []
            for k, v in attrs.items():
                if isinstance(v, bool):
                    val_node = {"boolValue": v}
                elif isinstance(v, int):
                    val_node = {"intValue": v}
                elif isinstance(v, float):
                    val_node = {"doubleValue": v}
                elif isinstance(v, list):
                    val_node = {"arrayValue": {"values": [{"stringValue": str(x)} for x in v]}}
                else:
                    val_node = {"stringValue": str(v)}
                otlp_attrs.append({"key": k, "value": val_node})

            # Map to OTel GenAI standard conventions
            otlp_attrs.extend([
                {"key": "gen_ai.operation.name", "value": {"stringValue": span.get("operation", "")}},
                {"key": "gen_ai.agent.name", "value": {"stringValue": span.get("role", "")}},
            ])

            start_iso = span.get("start_time", "")
            end_iso = span.get("end_time", "")
            try:
                start_dt = datetime.fromisoformat(start_iso)
                start_nano = str(int(start_dt.timestamp() * 1_000_000_000))
            except Exception:
                start_nano = "0"

            try:
                end_dt = datetime.fromisoformat(end_iso)
                end_nano = str(int(end_dt.timestamp() * 1_000_000_000))
            except Exception:
                end_nano = start_nano

            status_code = 1 if span.get("status") == "ok" else 2

            otlp_span: dict[str, Any] = {
                "traceId": span["trace_id"],
                "spanId": span["span_id"],
                "name": span["operation"],
                "kind": 1,  # SPAN_KIND_INTERNAL
                "startTimeUnixNano": start_nano,
                "endTimeUnixNano": end_nano,
                "attributes": otlp_attrs,
                "status": {"code": status_code},
            }
            if span.get("parent_span_id"):
                otlp_span["parentSpanId"] = span["parent_span_id"]

            otlp_spans.append(otlp_span)

        return {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": self.service_name}},
                            {"key": "service.version", "value": {"stringValue": self.service_version}},
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {
                                "name": "agent-skills.trace-runner",
                                "version": self.service_version,
                            },
                            "spans": otlp_spans,
                        }
                    ],
                }
            ]
        }

    def print_trace_tree(self) -> None:
        """Render a formatted ASCII causal tree of all spans in the current trace."""
        print_spans_tree(self.spans, self.export_summary())


def traced(
    role: str = "agent-coordinator",
    operation: str = "execute_tool",
    tool_name: str | None = None,
    model: str = "claude-3-7-sonnet",
) -> Callable:
    """Decorator to trace a Python function execution inside a TraceRunner span."""
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            runner = TraceRunner.get_active()
            name = tool_name or fn.__name__
            if runner:
                with runner.span(operation=operation, role=role, tool_name=name, model=model):
                    return fn(*args, **kwargs)
            else:
                with TraceRunner() as new_runner:
                    with new_runner.span(operation=operation, role=role, tool_name=name, model=model):
                        return fn(*args, **kwargs)
        return wrapper
    return decorator


def print_spans_tree(spans: list[dict[str, Any]], summary: dict[str, Any] | None = None) -> None:
    """Print an ASCII hierarchy of spans with timing and FinOps metrics."""
    if not spans:
        print("No spans recorded in this trace.")
        return

    by_id: dict[str, dict[str, Any]] = {s["span_id"]: s for s in spans}
    children_map: dict[str | None, list[dict[str, Any]]] = {}
    for s in spans:
        p_id = s.get("parent_span_id")
        children_map.setdefault(p_id, []).append(s)

    trace_id = spans[0]["trace_id"]
    print("=" * 80)
    print(f" AGENT TRACE RUNNER: {trace_id}")
    print("=" * 80)

    def safe_print(text: str) -> None:
        try:
            print(text)
        except UnicodeEncodeError:
            ascii_text = (
                text.replace("✓", "[OK]")
                .replace("✗", "[FAIL]")
                .replace("└── ", "`-- ")
                .replace("├── ", "|-- ")
                .replace("│   ", "|   ")
                .replace("│", "|")
                .replace("—", "-")
            )
            print(ascii_text.encode("ascii", errors="replace").decode("ascii"))

    def render_node(node: dict[str, Any], prefix: str = "", is_last: bool = True) -> None:
        attrs = node.get("attributes", {})
        status_icon = "✓" if node.get("status") == "ok" else "✗"
        dur = attrs.get("duration_ms", 0.0)
        cost = attrs.get("cost_usd", 0.0)
        tokens = attrs.get("input_tokens", 0) + attrs.get("output_tokens", 0)
        role = node.get("role", "unknown")
        op = node.get("operation", "op")
        tool = attrs.get("tool_name", "")
        detail = f"[{tool}]" if tool else ""

        connector = "└── " if is_last else "├── "
        line = (
            f"{prefix}{connector}[{status_icon}] {op} ({role}) {detail} "
            f"— {dur}ms | {tokens} tok | ${cost:.5f}"
        )
        safe_print(line)

        new_prefix = prefix + ("    " if is_last else "│   ")
        children = children_map.get(node["span_id"], [])
        for idx, child in enumerate(children):
            render_node(child, new_prefix, idx == len(children) - 1)

    roots = [s for s in spans if not s.get("parent_span_id") or s.get("parent_span_id") not in by_id]
    for idx, root in enumerate(roots):
        render_node(root, "", idx == len(roots) - 1)

    if summary:
        print("-" * 80)
        print(
            f"SUMMARY: {summary['span_count']} Spans | "
            f"Total Duration: {summary['total_duration_ms']}ms | "
            f"Total Tokens: {summary['tokens']['total']} "
            f"(in: {summary['tokens']['input']}, out: {summary['tokens']['output']}, cache: {summary['tokens']['cache_read']}) | "
            f"Total Cost: ${summary['total_cost_usd']:.5f} | "
            f"Status: {summary['status'].upper()}"
        )
        print("=" * 80)


def run_demo_trace() -> int:
    """Run an end-to-end multi-agent delegation trace demo simulating a feature delivery."""
    runner = TraceRunner(service_name="agent-skills-demo")

    print(f"Executing Multi-Agent Workflow Trace: {runner.trace_id}...")

    # Root span: Agent Coordinator orchestrates feature
    with runner.span(
        operation="invoke_agent",
        role="agent-coordinator",
        model="claude-3-7-sonnet",
        input_tokens=1850,
        output_tokens=320,
        reasoning_tokens=180,
        task_id="feat-auth-token-rotation",
    ):
        time.sleep(0.01)

        # Child 1: Planning phase
        with runner.span(
            operation="plan",
            role="task-planner",
            model="claude-3-7-sonnet",
            input_tokens=940,
            output_tokens=410,
            reasoning_tokens=220,
            cache_read_tokens=450,
        ):
            time.sleep(0.005)

        # Child 2: Technical Architecture Review
        with runner.span(
            operation="a2a_task",
            role="technical-architect",
            model="claude-3-7-sonnet",
            input_tokens=2100,
            output_tokens=680,
            cache_read_tokens=1500,
        ):
            time.sleep(0.01)
            with runner.span(
                operation="execute_tool",
                role="technical-architect",
                tool_name="read_file",
                tool_action="Read existing auth architecture",
                input_tokens=350,
                output_tokens=80,
            ):
                time.sleep(0.005)

        # Child 3: Backend Implementation
        with runner.span(
            operation="a2a_task",
            role="backend-developer",
            model="claude-3-7-sonnet",
            input_tokens=3200,
            output_tokens=950,
            reasoning_tokens=420,
            cache_read_tokens=2400,
        ):
            time.sleep(0.015)
            with runner.span(
                operation="execute_tool",
                role="backend-developer",
                tool_name="edit_file",
                tool_action="Implement JWT rotation in auth_service.py",
                input_tokens=600,
                output_tokens=120,
            ):
                time.sleep(0.005)

            with runner.span(
                operation="execute_tool",
                role="backend-developer",
                tool_name="execute_command",
                tool_action="pytest tests/test_auth_rotation.py",
                input_tokens=250,
                output_tokens=40,
            ):
                time.sleep(0.01)

        # Child 4: QA Gate & Verification
        with runner.span(
            operation="a2a_task",
            role="qa-engineer",
            model="claude-3-5-haiku",
            input_tokens=1200,
            output_tokens=260,
        ):
            time.sleep(0.005)
            with runner.span(
                operation="execute_tool",
                role="qa-engineer",
                tool_name="run_tests",
                tool_action="Verify test matrix",
                input_tokens=400,
                output_tokens=60,
            ):
                time.sleep(0.008)

    runner.print_trace_tree()
    print(f"\nTrace log saved to: {SPANS_DIR / f'{runner.trace_id}.jsonl'}")
    return 0


def exec_command_trace(
    cmd_args: list[str],
    role: str = "backend-developer",
    tool: str = "execute_command",
    model: str = "claude-3-7-sonnet",
) -> int:
    """Execute a real shell command, capturing timing and output under a traced span."""
    if not cmd_args:
        print("Error: No command provided to exec.")
        return 1

    runner = TraceRunner(service_name="agent-skills-exec")
    cmd_str = " ".join(cmd_args)
    print(f"Tracing Execution: {cmd_str} (Role: {role}, Tool: {tool})...\n")

    exit_code = 0
    with runner.span(
        operation="invoke_agent",
        role=role,
        model=model,
        task_id=f"exec-{uuid.uuid4().hex[:6]}",
    ):
        with runner.span(
            operation="execute_tool",
            role=role,
            tool_name=tool,
            tool_action=cmd_str,
            model=model,
        ) as tool_span:
            t0 = time.monotonic()
            try:
                proc = subprocess.run(
                    cmd_args,
                    shell=False,
                    text=True,
                    capture_output=True,
                )
                exit_code = proc.returncode
                stdout_len = len(proc.stdout)
                stderr_len = len(proc.stderr)

                if proc.stdout:
                    print(proc.stdout, end="")
                if proc.stderr:
                    print(proc.stderr, file=sys.stderr, end="")

                # Approximate token usage based on command output characters
                approx_tokens = max(10, (stdout_len + stderr_len) // 4)
                tool_span["attributes"]["input_tokens"] = 150
                tool_span["attributes"]["output_tokens"] = approx_tokens
                tool_span["attributes"]["exit_code"] = exit_code

                if exit_code != 0:
                    tool_span["status"] = "error"
                    tool_span["attributes"]["error_type"] = "ProcessExecutionError"
                    tool_span["attributes"]["error_message"] = f"Command exited with code {exit_code}"
            except Exception as exc:
                exit_code = 1
                tool_span["status"] = "error"
                tool_span["attributes"]["error_type"] = type(exc).__name__
                tool_span["attributes"]["error_message"] = str(exc)
                print(f"Execution error: {exc}", file=sys.stderr)

    print("\n" + "=" * 80)
    runner.print_trace_tree()
    print(f"Trace recorded to: {SPANS_DIR / f'{runner.trace_id}.jsonl'}")
    return exit_code


def list_traces() -> int:
    """List all captured trace sessions in core/observability/spans/."""
    if not SPANS_DIR.exists():
        print(f"No traces found: directory {SPANS_DIR} does not exist.")
        return 0

    trace_files = sorted(SPANS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not trace_files:
        print("No trace files found in core/observability/spans/.")
        return 0

    print("=" * 80)
    print(f" STORED AGENT TRACES ({len(trace_files)} sessions)")
    print("=" * 80)
    print(f"{'Trace ID':<34} | {'Spans':<6} | {'Cost ($)':<10} | {'Tokens':<8} | {'Last Modified'}")
    print("-" * 80)

    for p in trace_files[:25]:
        spans: list[dict[str, Any]] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    spans.append(json.loads(line))
                except Exception:
                    pass

        span_count = len(spans)
        total_tokens = sum(s.get("attributes", {}).get("input_tokens", 0) + s.get("attributes", {}).get("output_tokens", 0) for s in spans)
        total_cost = sum(s.get("attributes", {}).get("cost_usd", 0.0) for s in spans)
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        print(f"{p.stem:<34} | {span_count:<6} | ${total_cost:<9.5f} | {total_tokens:<8} | {mtime}")

    print("=" * 80)
    return 0


def stats_traces() -> int:
    """Aggregate FinOps and observability metrics across all recorded trace sessions."""
    if not SPANS_DIR.exists():
        print(f"No traces directory found at {SPANS_DIR}.")
        return 0

    trace_files = list(SPANS_DIR.glob("*.jsonl"))
    if not trace_files:
        print("No trace sessions found in core/observability/spans/.")
        return 0

    all_spans: list[dict[str, Any]] = []
    for p in trace_files:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    all_spans.append(json.loads(line))
                except Exception:
                    pass

    total_sessions = len(trace_files)
    total_spans = len(all_spans)
    total_cost = sum(s.get("attributes", {}).get("cost_usd", 0.0) for s in all_spans)
    total_input = sum(s.get("attributes", {}).get("input_tokens", 0) for s in all_spans)
    total_output = sum(s.get("attributes", {}).get("output_tokens", 0) for s in all_spans)
    total_reasoning = sum(s.get("attributes", {}).get("reasoning_tokens", 0) for s in all_spans)
    total_cache = sum(s.get("attributes", {}).get("cache_read_tokens", 0) for s in all_spans)

    ok_spans = sum(1 for s in all_spans if s.get("status") == "ok")
    err_spans = sum(1 for s in all_spans if s.get("status") == "error")
    success_rate = (ok_spans / total_spans * 100) if total_spans else 100.0

    # Role breakdown
    role_metrics: dict[str, dict[str, Any]] = {}
    for s in all_spans:
        r = s.get("role", "unknown")
        entry = role_metrics.setdefault(r, {"spans": 0, "tokens": 0, "cost": 0.0})
        entry["spans"] += 1
        entry["tokens"] += s.get("attributes", {}).get("input_tokens", 0) + s.get("attributes", {}).get("output_tokens", 0)
        entry["cost"] += s.get("attributes", {}).get("cost_usd", 0.0)

    # Model breakdown
    model_metrics: dict[str, dict[str, Any]] = {}
    for s in all_spans:
        m = s.get("attributes", {}).get("model", "unknown")
        entry = model_metrics.setdefault(m, {"spans": 0, "tokens": 0, "cost": 0.0})
        entry["spans"] += 1
        entry["tokens"] += s.get("attributes", {}).get("input_tokens", 0) + s.get("attributes", {}).get("output_tokens", 0)
        entry["cost"] += s.get("attributes", {}).get("cost_usd", 0.0)

    print("=" * 80)
    print(" AGENT TRACE RUNNER — OBSERVABILITY & FINOPS DASHBOARD")
    print("=" * 80)
    print(f"Total Sessions    : {total_sessions}")
    print(f"Total Spans       : {total_spans} (OK: {ok_spans}, ERROR: {err_spans}, Success: {success_rate:.1f}%)")
    print(f"Total Tokens      : {total_input + total_output:,} (Input: {total_input:,}, Output: {total_output:,}, Cache: {total_cache:,})")
    print(f"Aggregate Cost    : ${total_cost:.5f}")
    print("-" * 80)
    print("FINOPS ATTRIBUTION BY ROLE:")
    print(f"{'Role':<30} | {'Spans':<6} | {'Tokens':<10} | {'Cost ($)':<10}")
    print("-" * 80)
    for r, data in sorted(role_metrics.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"{r:<30} | {data['spans']:<6} | {data['tokens']:<10} | ${data['cost']:<9.5f}")

    print("-" * 80)
    print("MODEL DISTRIBUTION:")
    print(f"{'Model':<30} | {'Spans':<6} | {'Tokens':<10} | {'Cost ($)':<10}")
    print("-" * 80)
    for m, data in sorted(model_metrics.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"{m:<30} | {data['spans']:<6} | {data['tokens']:<10} | ${data['cost']:<9.5f}")
    print("=" * 80)
    return 0


def view_trace(trace_id: str) -> int:
    """Read and visualize a stored trace by ID."""
    trace_file = SPANS_DIR / f"{trace_id}.jsonl"
    if not trace_file.is_file():
        matches = list(SPANS_DIR.glob(f"{trace_id}*.jsonl"))
        if len(matches) == 1:
            trace_file = matches[0]
        else:
            print(f"Error: Trace '{trace_id}' not found in {SPANS_DIR}.")
            return 1

    spans: list[dict[str, Any]] = []
    for line in trace_file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            spans.append(json.loads(line))

    total_input = sum(s.get("attributes", {}).get("input_tokens", 0) for s in spans)
    total_output = sum(s.get("attributes", {}).get("output_tokens", 0) for s in spans)
    total_cost = sum(s.get("attributes", {}).get("cost_usd", 0.0) for s in spans)
    total_dur = sum(s.get("attributes", {}).get("duration_ms", 0.0) for s in spans)
    has_error = any(s.get("status") == "error" for s in spans)

    summary = {
        "span_count": len(spans),
        "total_duration_ms": round(total_dur, 2),
        "total_cost_usd": round(total_cost, 6),
        "status": "error" if has_error else "ok",
        "tokens": {
            "input": total_input,
            "output": total_output,
            "total": total_input + total_output,
            "cache_read": sum(s.get("attributes", {}).get("cache_read_tokens", 0) for s in spans),
        },
    }

    print_spans_tree(spans, summary)
    return 0


def export_trace(trace_id: str, format_type: str = "otlp", output_path: str | None = None) -> int:
    """Export a stored trace into standard OpenTelemetry OTLP JSON or summary JSON."""
    trace_file = SPANS_DIR / f"{trace_id}.jsonl"
    if not trace_file.is_file():
        matches = list(SPANS_DIR.glob(f"{trace_id}*.jsonl"))
        if len(matches) == 1:
            trace_file = matches[0]
        else:
            print(f"Error: Trace '{trace_id}' not found.")
            return 1

    spans = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    runner = TraceRunner(trace_id=trace_file.stem, validate_schema=False)
    runner.spans = spans

    if format_type.lower() == "otlp":
        data = runner.to_otlp_json()
    else:
        data = {
            "summary": runner.export_summary(),
            "spans": runner.spans,
        }

    formatted = json.dumps(data, indent=2, ensure_ascii=False)
    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(formatted, encoding="utf-8")
        print(f"Exported trace {trace_file.stem} ({format_type.upper()}) to: {out_file.resolve()}")
    else:
        print(formatted)

    return 0


def validate_trace(trace_id: str) -> int:
    """Validate all spans in a trace file against agent-trace-span.json schema."""
    if not Draft202012Validator:
        print("Error: jsonschema library is required for validation.")
        return 1

    trace_file = SPANS_DIR / f"{trace_id}.jsonl"
    if not trace_file.is_file():
        matches = list(SPANS_DIR.glob(f"{trace_id}*.jsonl"))
        if len(matches) == 1:
            trace_file = matches[0]
        else:
            print(f"Error: Trace '{trace_id}' not found.")
            return 1

    schema_json = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema_json)

    spans = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors_total = 0

    print(f"Validating trace '{trace_file.stem}' ({len(spans)} spans) against {SCHEMA_PATH.name}...")
    for idx, span in enumerate(spans):
        errors = list(validator.iter_errors(span))
        if errors:
            print(f"  [FAIL] Span {idx + 1} ({span.get('span_id')}): {[e.message for e in errors]}")
            errors_total += len(errors)
        else:
            print(f"  [PASS] Span {idx + 1} ({span.get('span_id')} - {span.get('operation')} by {span.get('role')})")

    if errors_total == 0:
        print(f"\nAll {len(spans)} spans conform strictly to agent-trace-span schema Draft 2020-12.")
        return 0
    print(f"\nValidation failed with {errors_total} schema errors.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="trace-runner",
        description="OpenTelemetry GenAI Agent Trace Runner for agent-skills",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # demo
    subparsers.add_parser("demo", help="Execute an end-to-end multi-agent trace demo")

    # list
    subparsers.add_parser("list", help="List all stored trace sessions")

    # stats
    subparsers.add_parser("stats", help="Aggregate FinOps & observability metrics across all traces")

    # view
    view_p = subparsers.add_parser("view", help="View ASCII span tree for a given trace ID")
    view_p.add_argument("trace_id", help="W3C trace ID or prefix")

    # validate
    val_p = subparsers.add_parser("validate", help="Validate trace spans against agent-trace-span schema")
    val_p.add_argument("trace_id", help="W3C trace ID or prefix")

    # export
    exp_p = subparsers.add_parser("export", help="Export trace to standard OTel OTLP JSON or summary")
    exp_p.add_argument("trace_id", help="W3C trace ID or prefix")
    exp_p.add_argument("--format", choices=["otlp", "json"], default="otlp", help="Export format")
    exp_p.add_argument("--output", help="Output file path (default stdout)")

    # exec
    exec_p = subparsers.add_parser("exec", help="Execute a shell command with live span tracing")
    exec_p.add_argument("--role", default="backend-developer", help="Agent role executing the command")
    exec_p.add_argument("--tool", default="execute_command", help="Tool name")
    exec_p.add_argument("--model", default="claude-3-7-sonnet", help="Model used")
    exec_p.add_argument("cmd", nargs=argparse.REMAINDER, help="Command and arguments to execute")

    args = parser.parse_args()

    if args.command == "demo" or not args.command:
        return run_demo_trace()
    elif args.command == "list":
        return list_traces()
    elif args.command == "stats":
        return stats_traces()
    elif args.command == "view":
        return view_trace(args.trace_id)
    elif args.command == "validate":
        return validate_trace(args.trace_id)
    elif args.command == "export":
        return export_trace(args.trace_id, format_type=args.format, output_path=args.output)
    elif args.command == "exec":
        cmd = args.cmd
        if cmd and cmd[0] == "--":
            cmd = cmd[1:]
        return exec_command_trace(cmd, role=args.role, tool=args.tool, model=args.model)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
