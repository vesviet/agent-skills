#!/usr/bin/env python3
"""Comprehensive unit test suite for core/scripts/compact-context.py.

Tests:
  - Head-Tail Tool Output Truncation (TOC) algorithm
  - Markdown code fence truncation
  - Schema #60 compact-working-state validation
  - In-context Markdown checkpoint formatting
  - CLI argument parsing, flags, and exit codes
"""

from __future__ import annotations

import json
import subprocess
import sys
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPACT_SCRIPT = REPO_ROOT / "core" / "scripts" / "compact-context.py"
SCHEMA_PATH = REPO_ROOT / "core" / "contracts" / "schemas" / "compact-working-state.json"

spec = importlib.util.spec_from_file_location("compact_context", COMPACT_SCRIPT)
compact_context = importlib.util.module_from_spec(spec)
sys.modules["compact_context"] = compact_context
spec.loader.exec_module(compact_context)

build_default_checkpoint = compact_context.build_default_checkpoint
format_markdown_checkpoint = compact_context.format_markdown_checkpoint
mask_old_observations = compact_context.mask_old_observations
merge_anchored_state = compact_context.merge_anchored_state
reconcile_modified_files = compact_context.reconcile_modified_files
redact_checkpoint_secrets = compact_context.redact_checkpoint_secrets
redact_secrets_in_text = compact_context.redact_secrets_in_text
scan_checkpoint_secrets = compact_context.scan_checkpoint_secrets
shannon_entropy = compact_context.shannon_entropy
truncate_code_fences = compact_context.truncate_code_fences
truncate_tool_output = compact_context.truncate_tool_output
validate_checkpoint_data = compact_context.validate_checkpoint_data


def run_compact(args: list[str], input_str: str | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(COMPACT_SCRIPT)] + args
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        input=input_str,
        capture_output=True,
        text=True,
        check=False,
    )


class TestTOCTruncation:
    """Tests for Head-Tail Tool Output Truncation (TOC) logic."""

    def test_short_output_retained_intact(self):
        lines = [f"Line {i}" for i in range(1, 15)]
        text = "\n".join(lines)
        truncated = truncate_tool_output(text, head_lines=5, tail_lines=15)
        assert truncated == text

    def test_long_output_truncated_with_marker(self):
        lines = [f"Line {i:03d}" for i in range(1, 101)]
        text = "\n".join(lines)
        truncated = truncate_tool_output(text, head_lines=5, tail_lines=15)
        out_lines = truncated.splitlines()

        # Head 5 lines
        assert out_lines[:5] == [f"Line {i:03d}" for i in range(1, 6)]
        # Truncation marker
        assert out_lines[5] == "... [Truncated 80 lines of execution output] ..."
        # Tail 15 lines
        assert out_lines[6:] == [f"Line {i:03d}" for i in range(86, 101)]
        assert len(out_lines) == 21

    def test_custom_head_tail_parameters(self):
        lines = [f"Step {i}" for i in range(1, 31)]
        text = "\n".join(lines)
        truncated = truncate_tool_output(text, head_lines=2, tail_lines=3)
        out_lines = truncated.splitlines()

        assert out_lines[:2] == ["Step 1", "Step 2"]
        assert out_lines[2] == "... [Truncated 25 lines of execution output] ..."
        assert out_lines[3:] == ["Step 28", "Step 29", "Step 30"]

    def test_tail_lines_zero(self):
        lines = [f"Line {i}" for i in range(1, 21)]
        text = "\n".join(lines)
        truncated = truncate_tool_output(text, head_lines=5, tail_lines=0)
        out_lines = truncated.splitlines()
        assert len(out_lines) == 6
        assert out_lines[:5] == [f"Line {i}" for i in range(1, 6)]
        assert out_lines[5] == "... [Truncated 15 lines of execution output] ..."

    def test_code_fences_truncation(self):
        inner_lines = "\n".join([f"Log line {i}" for i in range(1, 50)])
        doc = f"Intro text\n```text\n{inner_lines}\n```\nOutro text"
        truncated_doc = truncate_code_fences(doc, head_lines=5, tail_lines=15)

        assert "Intro text" in truncated_doc
        assert "Outro text" in truncated_doc
        assert "Truncated 29 lines" in truncated_doc


class TestCheckpointValidation:
    """Tests for validating checkpoints against compact-working-state.json."""

    def test_valid_default_checkpoint_passes(self):
        ckpt = build_default_checkpoint(
            goal="Upgrade agent-memory-compaction",
            work_type="feature",
            next_action="Run test suite",
        )
        errors = validate_checkpoint_data(ckpt, SCHEMA_PATH)
        assert errors == [], f"Validation errors: {errors}"

    def test_missing_required_slot_fails(self):
        ckpt = build_default_checkpoint()
        del ckpt["next_single_safe_action"]
        errors = validate_checkpoint_data(ckpt, SCHEMA_PATH)
        assert any("next_single_safe_action" in e for e in errors)

    def test_invalid_contract_type_fails(self):
        ckpt = build_default_checkpoint()
        ckpt["contract_type"] = "unsupported-contract"
        errors = validate_checkpoint_data(ckpt, SCHEMA_PATH)
        assert any("contract_type must be 'compact-working-state'" in e for e in errors)

    def test_invalid_work_type_enum_fails(self):
        ckpt = build_default_checkpoint()
        ckpt["work_type"] = "invalid_work_type"
        errors = validate_checkpoint_data(ckpt, SCHEMA_PATH)
        assert any("work_type 'invalid_work_type' is not in valid enums" in e for e in errors)

    def test_invalid_phase_status_enum_fails(self):
        ckpt = build_default_checkpoint()
        ckpt["phase_control"]["status"] = "unknown_status"
        errors = validate_checkpoint_data(ckpt, SCHEMA_PATH)
        assert any("status 'unknown_status' not in enums" in e for e in errors)

    def test_unhashable_types_do_not_crash(self):
        base = build_default_checkpoint()
        base["work_type"] = ["feature"]
        errors = validate_checkpoint_data(base, SCHEMA_PATH)
        assert any("work_type" in e for e in errors)

        base2 = build_default_checkpoint()
        base2["phase_control"]["status"] = {"invalid": "status"}
        errors2 = validate_checkpoint_data(base2, SCHEMA_PATH)
        assert any("phase_control.status" in e for e in errors2)

        base3 = build_default_checkpoint()
        base3["verification_and_evidence"] = [{"command": "pytest", "exit_code": 0, "status": ["passed"]}]
        errors3 = validate_checkpoint_data(base3, SCHEMA_PATH)
        assert any("verification_and_evidence[0].status" in e for e in errors3)

    def test_null_required_slots_fail(self):
        null_slots = [
            "work_type",
            "phase_control",
            "files_modified_and_inspected",
            "decisions_and_tradeoffs",
            "verification_and_evidence",
            "failed_attempts_and_antipatterns",
        ]
        for slot in null_slots:
            bad = build_default_checkpoint()
            bad[slot] = None
            errors = validate_checkpoint_data(bad, SCHEMA_PATH)
            assert len(errors) > 0, f"Expected validation errors for {slot}=None, got none"
            assert any(slot in e for e in errors), f"Expected {slot} in errors, got {errors}"

    def test_verification_evidence_missing_status_fails(self):
        bad = build_default_checkpoint()
        bad["verification_and_evidence"] = [{"command": "pytest", "exit_code": 0}]
        errors = validate_checkpoint_data(bad, SCHEMA_PATH)
        assert any("missing status" in e for e in errors)


class TestMarkdownFormatting:
    """Tests for in-context Markdown checkpoint rendering."""

    def test_format_markdown_contains_all_10_slots(self):
        ckpt = build_default_checkpoint(
            goal="Test in-context checkpoint rendering",
            work_type="bugfix",
            next_action="Execute git diff",
        )
        ckpt["files_modified_and_inspected"]["modified"] = ["core/skills/agent/SKILL.md"]
        ckpt["files_modified_and_inspected"]["inspected"] = ["core/contracts/README.md"]
        ckpt["decisions_and_tradeoffs"] = [
            {"decision": "Use 10-slot schema", "rationale": "Zero semantic drift"}
        ]
        ckpt["verification_and_evidence"] = [
            {"command": "pytest", "exit_code": 0, "status": "passed", "verbatim_snippet": "10 passed"}
        ]
        ckpt["failed_attempts_and_antipatterns"] = [
            {"attempt": "Recursive summary", "failure_reason": "Context drift"}
        ]

        md = format_markdown_checkpoint(ckpt)
        assert "## Compact Working State" in md
        assert "Current Goal:" in md
        assert "Test in-context checkpoint rendering" in md
        assert "Work Type:" in md
        assert "bugfix" in md
        assert "Phase Control:" in md
        assert "Active Constraints:" in md
        assert "Files Modified & Inspected:" in md
        assert "core/skills/agent/SKILL.md" in md
        assert "Decisions & Trade-offs:" in md
        assert "Zero semantic drift" in md
        assert "Verification & Evidence:" in md
        assert "pytest" in md
        assert "Failed Attempts & Anti-Patterns:" in md
        assert "Context drift" in md
        assert "Preserved Invariants:" in md
        assert "Next Single Safe Action:" in md
        assert "Execute git diff" in md

    def test_format_markdown_with_non_string_files(self):
        ckpt = build_default_checkpoint()
        ckpt["files_modified_and_inspected"]["modified"] = [123, True]
        ckpt["files_modified_and_inspected"]["inspected"] = [456]
        md = format_markdown_checkpoint(ckpt)
        assert "123, True" in md
        assert "456" in md


class TestCLIIntegration:
    """Tests for CLI flags, commands, and exit codes."""

    def test_help_flag_exits_0(self):
        res = run_compact(["--help"])
        assert res.returncode == 0
        assert "usage: compact-context.py" in res.stdout
        assert "--truncate" in res.stdout
        assert "--validate" in res.stdout
        assert "--create" in res.stdout

    def test_missing_input_file_exits_2(self):
        res = run_compact(["--input", "/path/to/missing_file.log"])
        assert res.returncode == 2
        assert "Error: input file does not exist" in res.stderr

    def test_create_and_validate_pipeline(self):
        create_res = run_compact(["--create", "--format", "json", "--goal", "Pipeline test"])
        assert create_res.returncode == 0
        val_res = run_compact(["--validate"], input_str=create_res.stdout)
        assert val_res.returncode == 0
        assert "Validation passed" in val_res.stdout

    def test_truncate_cli_flag(self):
        lines = [f"Trace log {i}" for i in range(1, 50)]
        input_data = "\n".join(lines)
        res = run_compact(["--truncate"], input_str=input_data)
        assert res.returncode == 0
        assert "Trace log 1" in res.stdout
        assert "Truncated 29 lines" in res.stdout
        assert "Trace log 49" in res.stdout

    def test_truncate_cli_tail_lines_zero(self):
        lines = [f"Trace row {i}" for i in range(1, 21)]
        input_data = "\n".join(lines)
        res = run_compact(["--truncate", "--head-lines", "5", "--tail-lines", "0"], input_str=input_data)
        assert res.returncode == 0
        out_lines = res.stdout.strip().splitlines()
        assert len(out_lines) == 6
        assert out_lines[0] == "Trace row 1"
        assert "Truncated 15 lines" in out_lines[5]


class TestThreeTierCompactionAndSecurity:
    """Tests for secret/entropy redaction, Tier 1 observation masking, and Tier 2 iterative merge."""

    def test_secret_and_shannon_entropy_redaction(self):
        high_ent = "aB9$kL2mP8qR4tV6xZ1cN3bM5yW7jH"
        assert shannon_entropy("aaaaaaa") == 0.0
        assert shannon_entropy(high_ent) > 4.5

        raw = (
            "token=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
            "hex=4f8a9c12d3e4567890abcdef1234567890abcdef12 "
            "safe=core/skills/agent/agent-memory-compaction/SKILL.md"
        )
        scrubbed, count = redact_secrets_in_text(raw)
        assert count >= 2
        assert "ghp_" not in scrubbed
        assert "4f8a9c12d3e4567890abcdef1234567890abcdef12" not in scrubbed
        assert "core/skills/agent/agent-memory-compaction/SKILL.md" in scrubbed

    def test_validate_cli_rejects_unredacted_secret(self, tmp_path):
        ckpt = build_default_checkpoint(goal="Safe goal")
        ckpt["active_constraints"].append("leak ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        assert len(scan_checkpoint_secrets(ckpt)) == 1
        ckpt_file = tmp_path / "leaky.json"
        ckpt_file.write_text(json.dumps(ckpt), encoding="utf-8")

        res = run_compact(["--validate", "-i", str(ckpt_file)])
        assert res.returncode == 1
        assert "Unredacted secret" in res.stderr

    def test_tier1_observation_masking_cli(self, tmp_path):
        turns_file = tmp_path / "turns.json"
        turns = [
            {"role": "user", "content": "Investigate failing build"},
            {"role": "tool", "call_id": "call_old", "exit_code": 1, "content": "Z" * 1200},
            {"role": "assistant", "content": "Found failing test"},
            {"role": "tool", "call_id": "call_recent", "exit_code": 0, "content": "R" * 1200},
        ]
        turns_file.write_text(json.dumps(turns), encoding="utf-8")
        res = run_compact([
            "--mask-observations",
            "--recent-turns", "2",
            "--spill-dir", str(tmp_path / "spill"),
            "-i", str(turns_file),
        ])
        assert res.returncode == 0
        out_turns = json.loads(res.stdout)
        assert out_turns[1]["observation_masked"] is True
        assert "[OBSERVATION MASKED: 1200 bytes" in out_turns[1]["content"]
        assert (tmp_path / "spill" / "call_old.log").exists()
        assert out_turns[3]["content"] == "R" * 1200

    def test_tier2_iterative_merge_cli_and_goal_lock(self, tmp_path):
        prev = build_default_checkpoint(goal="Canonical root objective", next_action="Inspect step 1")
        prev["files_modified_and_inspected"]["modified"] = ["core/a.py"]
        prev["decisions_and_tradeoffs"] = [{"decision": "Keep API stable", "rationale": "Backcompat"}]
        prev_file = tmp_path / "prev.json"
        prev_file.write_text(json.dumps(prev), encoding="utf-8")

        delta = {
            "current_goal": "Replaced drifting objective",
            "files_modified_and_inspected": {
                "modified": ["core/a.py", "core/b.py"],
                "inspected": ["core/c.py"],
            },
            "decisions_and_tradeoffs": [
                {"decision": "Keep API stable", "rationale": "Backcompat"},
                {"decision": "Add delta merge", "rationale": "Preserve prior slots"},
            ],
            "next_single_safe_action": "Run pytest suite",
        }
        delta_file = tmp_path / "delta.json"
        delta_file.write_text(json.dumps(delta), encoding="utf-8")

        res = run_compact(["--merge", str(prev_file), "-i", str(delta_file), "--format", "json"])
        assert res.returncode == 0
        merged = json.loads(res.stdout)
        assert merged["current_goal"] == "Canonical root objective"
        assert merged["files_modified_and_inspected"]["modified"] == ["core/a.py", "core/b.py"]
        assert len(merged["decisions_and_tradeoffs"]) == 2
        assert merged["next_single_safe_action"] == "Run pytest suite"
        assert merged["compaction_metrics"]["compaction_tier"] == "iterative_delta_merge"
        assert validate_checkpoint_data(merged) == []

    def test_reconcile_modified_files_with_real_git_repo(self, tmp_path):
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)
        (tmp_path / "tracked.py").write_text("print('hi')\n", encoding="utf-8")
        reconciled, git_ok = reconcile_modified_files(
            {"modified": ["existing.py"], "inspected": ["read.py"]},
            repo_root=tmp_path,
        )
        assert git_ok is True
        assert reconciled["modified"] == ["existing.py", "tracked.py"]
        assert reconciled["inspected"] == ["read.py"]
