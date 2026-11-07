#!/usr/bin/env python3
"""Automated Golden Benchmark Evaluation Test Suite.

Contains 15 unit test methods verifying each golden benchmark evaluation case across:
- Domain A: A2A v1.0.1+ uppercase state handling (TC-A2A-01 to TC-A2A-04)
- Domain B: Two-Tier JIT skill discovery accuracy (TC-JIT-01 to TC-JIT-04)
- Domain C: Stateless MCP prefix policy gating (TC-MCP-01 to TC-MCP-04)
- Domain D: Prompt prefix cache layer alignment (TC-CACHE-01 to TC-CACHE-03)

Executes live Draft 2020-12 schemas, live INDEX_TIER1.json, and live mcp-tool-map.yaml (zero mock facades).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest

import yaml

# Dynamically import run-eval-benchmark.py (contains hyphens)
SKILL_DIR = Path(__file__).resolve().parents[1]
runner_path = SKILL_DIR / "scripts" / "run-eval-benchmark.py"

spec = importlib.util.spec_from_file_location("run_eval_benchmark", runner_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load runner from {runner_path}")
run_eval_benchmark = importlib.util.module_from_spec(spec)
sys.modules["run_eval_benchmark"] = run_eval_benchmark
spec.loader.exec_module(run_eval_benchmark)

BenchmarkEvaluator = run_eval_benchmark.BenchmarkEvaluator
find_repo_root = run_eval_benchmark.find_repo_root


class TestGoldenBenchmarks(unittest.TestCase):
    """Test suite executing the 15 golden evaluation benchmark test cases."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = find_repo_root()
        cls.eval_dir = cls.repo_root / "core" / "skills" / "ai-agent" / "agent-evaluation"
        cls.manifest_path = cls.eval_dir / "resources" / "eval-benchmarks" / "eval-manifest.yaml"
        cls.cases_path = cls.eval_dir / "resources" / "eval-benchmarks" / "eval-cases.json"
        cls.output_path = cls.repo_root / "output" / "agent-eval-report.json"

        cls.manifest = yaml.safe_load(cls.manifest_path.read_text(encoding="utf-8"))
        cls.cases_data = json.loads(cls.cases_path.read_text(encoding="utf-8"))
        cls.cases_by_id = {c["case_id"]: c for c in cls.cases_data["cases"]}

        cls.evaluator = BenchmarkEvaluator(
            repo_root=cls.repo_root,
            manifest_path=cls.manifest_path,
            cases_path=cls.cases_path,
            output_path=cls.output_path,
        )

    # -------------------------------------------------------------------------
    # Suite Governance & Stratification Tests
    # -------------------------------------------------------------------------
    def test_suite_total_cases_and_stratification(self) -> None:
        """Verify exactly 15 test cases with 6 Nominal (40%), 6 Edge (40%), 3 Hostile/Safety (20%)."""
        cases = self.cases_data["cases"]
        self.assertEqual(len(cases), 15, "Expected exactly 15 test cases")

        strat = {"nominal": 0, "edge": 0, "hostile_safety": 0}
        domains = {"a2a_uppercase_state": 0, "jit_skill_discovery": 0, "mcp_prefix_policy": 0, "prompt_prefix_cache": 0}

        for c in cases:
            tier = c["tier"]
            dom = c["domain"]
            self.assertIn(tier, strat, f"Unknown tier {tier} in {c['case_id']}")
            self.assertIn(dom, domains, f"Unknown domain {dom} in {c['case_id']}")
            strat[tier] += 1
            domains[dom] += 1

        self.assertEqual(strat["nominal"], 6, "Expected 6 Nominal test cases (40%)")
        self.assertEqual(strat["edge"], 6, "Expected 6 Edge test cases (40%)")
        self.assertEqual(strat["hostile_safety"], 3, "Expected 3 Hostile/Safety test cases (20%)")

        self.assertEqual(domains["a2a_uppercase_state"], 4, "Domain A must have 4 test cases")
        self.assertEqual(domains["jit_skill_discovery"], 4, "Domain B must have 4 test cases")
        self.assertEqual(domains["mcp_prefix_policy"], 4, "Domain C must have 4 test cases")
        self.assertEqual(domains["prompt_prefix_cache"], 3, "Domain D must have 3 test cases")

    # -------------------------------------------------------------------------
    # Domain A: A2A v1.0.1+ Uppercase State Handling (TC-A2A-01 to TC-A2A-04)
    # -------------------------------------------------------------------------
    def test_tc_a2a_01_uppercase_state_ingestion(self) -> None:
        """TC-A2A-01: A2A v1.0.1 Uppercase State Ingestion (TASK_STATE_SUBMITTED)."""
        case = self.cases_by_id["TC-A2A-01"]
        res = self.evaluator.evaluate_a2a_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["schema_validation_passed"])
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_a2a_02_streaming_task_status_update_event(self) -> None:
        """TC-A2A-02: Streaming TaskStatusUpdateEvent with TASK_STATE_WORKING."""
        case = self.cases_by_id["TC-A2A-02"]
        res = self.evaluator.evaluate_a2a_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["schema_validation_passed"])
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_a2a_03_terminal_task_completion_artifact(self) -> None:
        """TC-A2A-03: Terminal Task Completion with Artifact Handoff."""
        case = self.cases_by_id["TC-A2A-03"]
        res = self.evaluator.evaluate_a2a_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["schema_validation_passed"])
        self.assertTrue(res["assertions"]["must_not_include_passed"])

    def test_tc_a2a_04_terminal_task_cancellation_lifecycle(self) -> None:
        """TC-A2A-04: Terminal Task Failure & Cancellation Lifecycle."""
        case = self.cases_by_id["TC-A2A-04"]
        res = self.evaluator.evaluate_a2a_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["schema_validation_passed"])
        self.assertTrue(res["assertions"]["must_include_passed"])

    # -------------------------------------------------------------------------
    # Domain B: Two-Tier JIT Skill Discovery Accuracy (TC-JIT-01 to TC-JIT-04)
    # -------------------------------------------------------------------------
    def test_tc_jit_01_api_endpoint_high_confidence_match(self) -> None:
        """TC-JIT-01: High-Confidence Match for API Endpoint Development (add-api-endpoint)."""
        case = self.cases_by_id["TC-JIT-01"]
        res = self.evaluator.evaluate_jit_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])
        self.assertTrue(res["assertions"]["schema_validation_passed"])  # Digest verified

    def test_tc_jit_02_vllm_inference_high_confidence_match(self) -> None:
        """TC-JIT-02: High-Confidence Match for vLLM Inference (deploy-vllm-inference)."""
        case = self.cases_by_id["TC-JIT-02"]
        res = self.evaluator.evaluate_jit_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])
        self.assertTrue(res["assertions"]["schema_validation_passed"])  # Digest verified

    def test_tc_jit_03_role_prohibited_skill_disqualification(self) -> None:
        """TC-JIT-03: Active Role Prohibited Skill Disqualification (create-migration)."""
        case = self.cases_by_id["TC-JIT-03"]
        res = self.evaluator.evaluate_jit_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_jit_04_low_confidence_fail_closed_gate(self) -> None:
        """TC-JIT-04: Low-Confidence Ambiguous Query Fail-Closed Gate (< 0.72)."""
        case = self.cases_by_id["TC-JIT-04"]
        res = self.evaluator.evaluate_jit_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    # -------------------------------------------------------------------------
    # Domain C: Stateless MCP Prefix Policy Gating (TC-MCP-01 to TC-MCP-04)
    # -------------------------------------------------------------------------
    def test_tc_mcp_01_safe_read_prefix_routing(self) -> None:
        """TC-MCP-01: Dynamic Prefix Routing for Safe Read Operations (^fs_read_.*)."""
        case = self.cases_by_id["TC-MCP-01"]
        res = self.evaluator.evaluate_mcp_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_mcp_02_critical_mutation_prefix_routing(self) -> None:
        """TC-MCP-02: Dynamic Prefix Routing for Critical Mutation (^db_drop_.*)."""
        case = self.cases_by_id["TC-MCP-02"]
        res = self.evaluator.evaluate_mcp_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_mcp_03_destructive_pattern_precedence(self) -> None:
        """TC-MCP-03: Destructive Pattern Substring Precedence Over Prefix."""
        case = self.cases_by_id["TC-MCP-03"]
        res = self.evaluator.evaluate_mcp_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_mcp_04_unmapped_tool_fail_closed_fallback(self) -> None:
        """TC-MCP-04: Unmapped Tool Name Fail-Closed Zero-Trust Fallback."""
        case = self.cases_by_id["TC-MCP-04"]
        res = self.evaluator.evaluate_mcp_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    # -------------------------------------------------------------------------
    # Domain D: Prompt Prefix Cache Layer Alignment (TC-CACHE-01 to TC-CACHE-03)
    # -------------------------------------------------------------------------
    def test_tc_cache_01_six_layer_volatility_hierarchy(self) -> None:
        """TC-CACHE-01: Deterministic 6-Layer Volatility Hierarchy Compliance."""
        case = self.cases_by_id["TC-CACHE-01"]
        res = self.evaluator.evaluate_cache_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_cache_02_dynamic_header_cache_busting_detection(self) -> None:
        """TC-CACHE-02: Header Timestamp / Nonce Cache-Busting Detection."""
        case = self.cases_by_id["TC-CACHE-02"]
        res = self.evaluator.evaluate_cache_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    def test_tc_cache_03_deterministic_tool_alphabetical_sorting(self) -> None:
        """TC-CACHE-03: Deterministic Tool Definition Alphabetical Sorting."""
        case = self.cases_by_id["TC-CACHE-03"]
        res = self.evaluator.evaluate_cache_case(case)
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["score"], 1.0)
        self.assertTrue(res["assertions"]["must_include_passed"])

    # -------------------------------------------------------------------------
    # Full Suite Integration & Schema Verification
    # -------------------------------------------------------------------------
    def test_full_suite_execution_and_schema_conformance(self) -> None:
        """Execute the entire 15-case suite, asserting pass rate and agent-eval-report.json conformance."""
        report = self.evaluator.run_suite()
        summary = report["summary_scores"]

        self.assertEqual(summary["total_executed"], 15)
        self.assertEqual(summary["passed_count"], 15)
        self.assertEqual(summary["failed_count"], 0)
        self.assertEqual(summary["pass_rate"], 1.0)
        self.assertEqual(summary["verdict"], "passed")
        self.assertEqual(summary["release_gate_recommendation"], "promote")
        self.assertGreaterEqual(summary["overall_score"], 0.85)

        # Validate emitted report against Draft 2020-12 schema
        errors = self.evaluator.validate_schema("core/contracts/schemas/agent-eval-report.json", report)
        self.assertEqual(len(errors), 0, f"agent-eval-report schema errors: {errors}")


if __name__ == "__main__":
    unittest.main()
