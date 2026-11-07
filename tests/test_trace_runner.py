#!/usr/bin/env python3
"""Unit and integration tests for TraceRunner (OpenTelemetry GenAI SOTA)."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACE_RUNNER_PATH = REPO_ROOT / "core" / "scripts" / "trace-runner.py"

# Import trace-runner module dynamically
spec = importlib.util.spec_from_file_location("trace_runner", str(TRACE_RUNNER_PATH))
trace_module = importlib.util.module_from_spec(spec)
sys.modules["trace_runner"] = trace_module
spec.loader.exec_module(trace_module)

TraceRunner = trace_module.TraceRunner
generate_trace_id = trace_module.generate_trace_id
generate_span_id = trace_module.generate_span_id
calculate_cost_usd = trace_module.calculate_cost_usd
MODEL_PRICING = trace_module.MODEL_PRICING


class TestTraceRunnerBasics:
    """Validate core ID generation and FinOps token costing."""

    def test_w3c_trace_and_span_ids(self):
        trace_id = generate_trace_id()
        assert len(trace_id) == 32
        int(trace_id, 16)  # Verify valid hex

        span_id = generate_span_id()
        assert len(span_id) == 16
        int(span_id, 16)  # Verify valid hex

    def test_calculate_cost_usd_known_models(self):
        # 1M input, 1M output for claude-3-7-sonnet ($3 in, $15 out = $18)
        cost = calculate_cost_usd(
            "claude-3-7-sonnet",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
        )
        assert cost == pytest.approx(18.0, rel=1e-4)

        # DeepSeek-R1 (0.55 in, 2.19 out = 2.74)
        cost_r1 = calculate_cost_usd(
            "deepseek-r1",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
        )
        assert cost_r1 == pytest.approx(2.74, rel=1e-4)

    def test_calculate_cost_usd_fallback(self):
        # Unknown model falls back to haiku pricing ($0.80 in, $4.00 out)
        cost_unknown = calculate_cost_usd(
            "unknown-custom-model",
            input_tokens=1_000_000,
            output_tokens=1_000_000,
        )
        assert cost_unknown == pytest.approx(4.80, rel=1e-4)


class TestTraceRunnerSpanLifecycle:
    """Validate span nesting, parent-child linking, and schema validation."""

    def test_nested_causal_spans(self):
        runner = TraceRunner(service_name="test-skills", validate_schema=True)

        with runner.span(
            operation="invoke_agent",
            role="agent-coordinator",
            task_id="task-root-001",
            model="claude-3-7-sonnet",
            input_tokens=1000,
            output_tokens=200,
        ) as root_span:
            root_id = root_span["span_id"]
            assert "parent_span_id" not in root_span or root_span.get("parent_span_id") is None

            with runner.span(
                operation="plan",
                role="task-planner",
                model="claude-3-5-haiku",
                input_tokens=500,
                output_tokens=150,
            ) as child_span:
                child_id = child_span["span_id"]
                assert child_span["parent_span_id"] == root_id

                with runner.span(
                    operation="execute_tool",
                    role="task-planner",
                    tool_name="read_file",
                ) as grand_child_span:
                    assert grand_child_span["parent_span_id"] == child_id

        assert len(runner.spans) == 3
        # Check order of completion: grand_child -> child -> root
        assert runner.spans[0]["operation"] == "execute_tool"
        assert runner.spans[1]["operation"] == "plan"
        assert runner.spans[2]["operation"] == "invoke_agent"

        # Validate schema compliance for all generated spans
        if runner._validator:
            for span in runner.spans:
                errors = list(runner._validator.iter_errors(span))
                assert not errors, f"Span failed schema validation: {[e.message for e in errors]}"

    def test_span_error_handling(self):
        runner = TraceRunner(validate_schema=True)

        with pytest.raises(ValueError, match="Simulated tool error"):
            with runner.span(
                operation="execute_tool",
                role="backend-developer",
                tool_name="run_command",
            ):
                raise ValueError("Simulated tool error")

        assert len(runner.spans) == 1
        span = runner.spans[0]
        assert span["status"] == "error"
        assert "Simulated tool error" in span["attributes"]["error_message"]
        assert span["attributes"]["error_type"] == "ValueError"


class TestTraceRunnerCLI:
    """Validate CLI execution and commands."""

    def test_cli_demo_and_validate(self):
        result = subprocess.run(
            [sys.executable, str(TRACE_RUNNER_PATH), "demo"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0
        assert "AGENT TRACE RUNNER" in result.stdout
        assert "SUMMARY: 9 Spans" in result.stdout

        # Extract trace_id from output
        lines = result.stdout.splitlines()
        trace_id = None
        for line in lines:
            if "AGENT TRACE RUNNER:" in line:
                trace_id = line.split(":")[-1].strip()
                break

        assert trace_id is not None, "Failed to extract trace_id from demo"

        # Validate saved trace
        val_result = subprocess.run(
            [sys.executable, str(TRACE_RUNNER_PATH), "validate", trace_id],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert val_result.returncode == 0
        assert "All 9 spans conform strictly to agent-trace-span schema Draft 2020-12" in val_result.stdout
