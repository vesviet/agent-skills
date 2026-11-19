#!/usr/bin/env python3
"""Verification suite for P1 Rulings-not-stalls and 7-Dimension Session Forensics."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DIAGNOSE_SCRIPT = REPO_ROOT / "core" / "scripts" / "diagnose-session.py"
COORDINATOR_ROLE = REPO_ROOT / "core" / "roles" / "agent-coordinator.md"
COORDINATOR_CHECKLIST = REPO_ROOT / "core" / "roles" / "references" / "agent-coordinator-review-checklist.md"
DELEGATION_SKILL = REPO_ROOT / "core" / "skills" / "agent" / "agent-delegation" / "SKILL.md"
OBSERVABILITY_SKILL = REPO_ROOT / "core" / "skills" / "agent" / "agent-observability" / "SKILL.md"
FORENSICS_REF = (
    REPO_ROOT
    / "core"
    / "skills"
    / "agent"
    / "agent-observability"
    / "references"
    / "session-forensics-7-dimensions.md"
)


class TestP1RulingsAndForensics(unittest.TestCase):
    """Tests for Rulings-not-stalls orchestration rules and diagnose-session.py forensics."""

    def test_01_diagnose_session_self_test_passes(self) -> None:
        self.assertTrue(DIAGNOSE_SCRIPT.is_file())
        proc = subprocess.run(
            [sys.executable, str(DIAGNOSE_SCRIPT), "--self-test"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("self-test passed", proc.stdout.lower())

    def test_02_diagnose_transcript_detects_all_7_dimensions_and_scrubs(self) -> None:
        synthetic_pat = "ghp" + "_" + "ForensicCheckToken1234567890ABCD"
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "transcript.jsonl"
            records = [
                {
                    "step_index": 1,
                    "type": "USER_INPUT",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:00Z",
                    "content": "/systematic-debugging fix timeout",
                },
                {
                    "step_index": 2,
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:05Z",
                    "tool_calls": [
                        {"name": "read_file", "arguments": {"Path": "core/skills/foundation/systematic-debugging/SKILL.md"}}
                    ],
                },
                {
                    "step_index": 3,
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:10Z",
                    "tool_calls": [{"name": "read_file", "arguments": {"Path": "src/worker.py"}}],
                },
                {
                    "step_index": 4,
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:12Z",
                    "tool_calls": [{"name": "read_file", "arguments": {"Path": "src/worker.py"}}],
                },
                {
                    "step_index": 5,
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:14Z",
                    "tool_calls": [{"name": "read_file", "arguments": {"Path": "src/worker.py"}}],
                },
                {
                    "step_index": 6,
                    "type": "PLANNER_RESPONSE",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:20Z",
                    "tool_calls": [{"name": "edit_file", "arguments": {"Path": "src/worker.py"}}],
                },
                {
                    "step_index": 7,
                    "type": "TOOL_RESULT",
                    "status": "ERROR",
                    "created_at": "2026-11-19T08:00:25Z",
                    "content": f"Command exited with code 1 token={synthetic_pat} ops@example.com",
                },
                {
                    "step_index": 8,
                    "type": "USER_INPUT",
                    "status": "DONE",
                    "created_at": "2026-11-19T08:00:35Z",
                    "content": "Wait, do not skip tests; fix that first",
                },
            ]
            log_file.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(DIAGNOSE_SCRIPT), str(log_file), "--scrub", "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            dims = report["dimensions"]
            self.assertEqual(
                set(dims.keys()),
                {
                    "skill_timeline",
                    "plan_adherence",
                    "repeated_work",
                    "stumbles",
                    "quality_evidence",
                    "request_conflicts",
                    "cost_and_time",
                },
            )
            self.assertGreaterEqual(dims["skill_timeline"]["count"], 2)
            self.assertEqual(dims["plan_adherence"]["mutated_files_count"], 1)
            self.assertEqual(dims["repeated_work"]["flagged_loops"], 1)
            self.assertEqual(dims["stumbles"]["count"], 1)
            self.assertEqual(dims["stumbles"]["items"][0]["citation"], "transcript.jsonl:7")
            self.assertFalse(dims["quality_evidence"]["verified_after_last_edit"])
            self.assertEqual(dims["request_conflicts"]["count"], 1)
            self.assertEqual(dims["cost_and_time"]["duration_seconds"], 35.0)
            self.assertTrue(report["scrubbed"])
            self.assertGreaterEqual(report["redactions_count"], 2)
            self.assertNotIn(synthetic_pat, proc.stdout)
            self.assertNotIn("ops@example.com", proc.stdout)

    def test_03_diagnose_otel_spans_markdown_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spans_file = Path(tmp) / "spans.jsonl"
            spans = [
                {
                    "trace_id": "1" * 32,
                    "span_id": "2" * 16,
                    "operation": "invoke_agent",
                    "role": "agent-coordinator",
                    "status": "OK",
                    "duration_ms": 250.0,
                    "tokens": {"input": 1200, "output": 300},
                    "cost_usd": 0.0081,
                },
                {
                    "trace_id": "1" * 32,
                    "span_id": "3" * 16,
                    "operation": "execute_tool",
                    "role": "qa-engineer",
                    "tool": "run_tests",
                    "status": "ERROR",
                    "duration_ms": 500.0,
                    "error": "pytest exited 1",
                    "tokens": {"input": 400, "output": 100},
                    "cost_usd": 0.0027,
                },
            ]
            spans_file.write_text("\n".join(json.dumps(s) for s in spans) + "\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(DIAGNOSE_SCRIPT), str(spans_file), "--format", "markdown"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("7-Dimension Session Forensics Report", proc.stdout)
            self.assertIn("spans.jsonl:2", proc.stdout)
            self.assertIn("2000", proc.stdout)

    def test_04_coordinator_and_delegation_codify_rulings_not_stalls(self) -> None:
        coord = COORDINATOR_ROLE.read_text(encoding="utf-8")
        chk = COORDINATOR_CHECKLIST.read_text(encoding="utf-8")
        deleg = DELEGATION_SKILL.read_text(encoding="utf-8")

        self.assertIn("Rulings, Not Stalls", coord)
        self.assertIn("4 Hard Stop Conditions", coord)
        self.assertIn("Ruling: <what was decided>", coord)
        self.assertIn("Rulings, Not Stalls", chk)
        self.assertIn("diagnose-session.py", chk)

        self.assertIn("Rulings, Not Stalls", deleg)
        self.assertIn("## Red Flags", deleg)
        self.assertLess(len(deleg.splitlines()), 200)
        self.assertLess(DELEGATION_SKILL.stat().st_size, 20_000)

    def test_05_agent_observability_integrates_7_dimension_forensics(self) -> None:
        obs = OBSERVABILITY_SKILL.read_text(encoding="utf-8")
        self.assertTrue(FORENSICS_REF.is_file())
        self.assertIn("session-forensics-7-dimensions.md", obs)
        self.assertIn("core/scripts/diagnose-session.py", obs)
        self.assertIn("## Red Flags", obs)
        self.assertLess(len(obs.splitlines()), 200)
        self.assertLess(OBSERVABILITY_SKILL.stat().st_size, 20_000)


if __name__ == "__main__":
    unittest.main()
