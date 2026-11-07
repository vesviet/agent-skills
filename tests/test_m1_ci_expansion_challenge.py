#!/usr/bin/env python3
"""Adversarial Challenger Test Suite for Milestone 1: Master CI Validation Expansion (R1).

Empirically challenges:
1. Master CI Validation Expansion (core/scripts/validate-all.py):
   - Injected failure propagation (sequential, parallel, JSON, and SARIF modes).
   - Fail-fast (--fail-fast) early termination mechanics.
   - Concurrency stress testing under parallel ThreadPoolExecutor execution.
   - SARIF 2.1.0 schema and rule compliance for validate_discovery_manifests.
   - CLI argument validation and boundary invariants.
2. Discovery Manifest Validator (core/scripts/validate-discovery-manifests.py):
   - Live discovery manifest compliance (adapters/antigravity/INDEX_TIER1.json).
   - Opportunistic .well-known manifest validation.
   - Fail-closed behavior on tampered or invalid discovery manifests.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_ALL_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-all.py"
VALIDATE_DISCOVERY_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-discovery-manifests.py"
TIER1_MANIFEST_PATH = REPO_ROOT / "adapters" / "antigravity" / "INDEX_TIER1.json"
WELL_KNOWN_DIR = REPO_ROOT / ".well-known" / "agent-skills"
WELL_KNOWN_MANIFEST = WELL_KNOWN_DIR / "index.json"


def run_master_validator(args: Optional[List[str]] = None, timeout: float = 60.0) -> subprocess.CompletedProcess:
    """Execute validate-all.py with arguments."""
    cmd = [sys.executable, str(VALIDATE_ALL_SCRIPT)] + (args or [])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=timeout,
        check=False,
    )


def run_discovery_validator(args: Optional[List[str]] = None, timeout: float = 30.0) -> subprocess.CompletedProcess:
    """Execute validate-discovery-manifests.py with arguments."""
    cmd = [sys.executable, str(VALIDATE_DISCOVERY_SCRIPT)] + (args or [])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=timeout,
        check=False,
    )


# ==============================================================================
# GROUP 1: Master CI Registration & Clean Baseline
# ==============================================================================


class TestDiscoveryManifestValidatorInMasterCi(unittest.TestCase):
    """Verifies that validate-discovery-manifests.py is properly wired into validate-all.py."""

    def test_validator_registration_and_count(self):
        """validate-all.py VALIDATORS tuple must contain exactly 21 validators including validate-discovery-manifests.py."""
        code = VALIDATE_ALL_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"validate-discovery-manifests.py"', code)

        # Parse VALIDATORS tuple directly
        import ast
        tree = ast.parse(code)
        validators = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "VALIDATORS":
                        if isinstance(node.value, ast.Tuple):
                            validators = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
        self.assertEqual(len(validators), 21, f"Expected 21 validators in VALIDATORS tuple, found {len(validators)}")
        self.assertIn("validate-discovery-manifests.py", validators)
        self.assertEqual(validators[-1], "validate-discovery-manifests.py", "Expected validate-discovery-manifests.py to be registered at index 20")

    def test_clean_master_validator_sequential_exit_0(self):
        """validate-all.py in default text mode passes with exit code 0."""
        proc = run_master_validator(timeout=60.0)
        self.assertEqual(proc.returncode, 0, f"validate-all.py failed in sequential mode:\n{proc.stdout}\n{proc.stderr}")
        self.assertIn("Discovery manifest validation passed: adapters/antigravity/INDEX_TIER1.json", proc.stdout)
        self.assertIn("All core validators passed.", proc.stdout)

    def test_clean_master_validator_json_format(self):
        """validate-all.py --format json outputs complete and schema-valid JSON report with 21 passed validators."""
        proc = run_master_validator(["--format", "json"], timeout=60.0)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data.get("tool"), "agent-pack-validator")
        self.assertTrue(data.get("passed"))
        self.assertEqual(data.get("failed"), 0)
        self.assertEqual(data.get("total"), 21)
        self.assertEqual(len(data.get("results", [])), 21)

        # Locate validate-discovery-manifests.py in results
        results_by_name = {r["name"]: r for r in data["results"]}
        self.assertIn("validate-discovery-manifests.py", results_by_name)
        dm_result = results_by_name["validate-discovery-manifests.py"]
        self.assertTrue(dm_result["passed"])
        self.assertEqual(dm_result["exit_code"], 0)
        self.assertEqual(len(dm_result["errors"]), 0)

    def test_clean_master_validator_sarif_format(self):
        """validate-all.py --format sarif outputs SARIF 2.1.0 with 21 rules and empty results on clean repo."""
        proc = run_master_validator(["--format", "sarif"], timeout=60.0)
        self.assertEqual(proc.returncode, 0)
        sarif = json.loads(proc.stdout)
        self.assertEqual(sarif.get("version"), "2.1.0")
        self.assertEqual(sarif.get("$schema"), "https://json.schemastore.org/sarif-2.1.0.json")
        runs = sarif.get("runs", [])
        self.assertEqual(len(runs), 1)

        rules = runs[0].get("tool", {}).get("driver", {}).get("rules", [])
        self.assertEqual(len(rules), 21)
        rule_ids = {r["id"] for r in rules}
        self.assertIn("validate_discovery_manifests", rule_ids)

        rule = next(r for r in rules if r["id"] == "validate_discovery_manifests")
        self.assertEqual(rule.get("name"), "Validate Discovery Manifests")
        self.assertEqual(rule.get("shortDescription", {}).get("text"), "Agent pack validator: validate-discovery-manifests.py")
        self.assertEqual(rule.get("defaultConfiguration", {}).get("level"), "error")

        # Zero findings in clean state
        self.assertEqual(len(runs[0].get("results", [])), 0)


# ==============================================================================
# GROUP 2: Injected Failure Propagation
# ==============================================================================


class TestInjectedFailurePropagation(unittest.TestCase):
    """Stress tests failure propagation across all modes when validate-discovery-manifests.py fails."""

    def test_injected_failure_propagates_sequential_text_mode(self):
        """When an invalid discovery manifest is injected, validate-all.py text mode exits 1."""
        WELL_KNOWN_DIR.mkdir(parents=True, exist_ok=True)
        try:
            # Write invalid discovery manifest with missing required fields
            WELL_KNOWN_MANIFEST.write_text(
                json.dumps({"contract_type": "agent-skills-discovery", "skills": []}),
                encoding="utf-8",
            )
            proc = run_master_validator(["--parallel"], timeout=45.0)
            self.assertEqual(proc.returncode, 1, f"Expected returncode 1 on invalid manifest, got {proc.returncode}")
            self.assertIn("Discovery manifest validation failed", proc.stdout + proc.stderr)
            self.assertNotIn("All core validators passed.", proc.stdout)
        finally:
            if WELL_KNOWN_MANIFEST.exists():
                WELL_KNOWN_MANIFEST.unlink()
            if WELL_KNOWN_DIR.exists() and not any(WELL_KNOWN_DIR.iterdir()):
                WELL_KNOWN_DIR.rmdir()
            if WELL_KNOWN_DIR.parent.exists() and not any(WELL_KNOWN_DIR.parent.iterdir()):
                WELL_KNOWN_DIR.parent.rmdir()

    def test_injected_failure_propagates_json_mode(self):
        """When discovery manifest validation fails, --format json reports passed=False, failed=1, and exit_code=1."""
        WELL_KNOWN_DIR.mkdir(parents=True, exist_ok=True)
        try:
            WELL_KNOWN_MANIFEST.write_text(
                json.dumps({"contract_type": "agent-skills-discovery", "invalid_key": True}),
                encoding="utf-8",
            )
            proc = run_master_validator(["--parallel", "--format", "json"], timeout=45.0)
            self.assertEqual(proc.returncode, 1)
            data = json.loads(proc.stdout)
            self.assertFalse(data["passed"])
            self.assertEqual(data["failed"], 1)
            self.assertEqual(data["total"], 21)

            dm_entry = next(r for r in data["results"] if r["name"] == "validate-discovery-manifests.py")
            self.assertFalse(dm_entry["passed"])
            self.assertEqual(dm_entry["exit_code"], 1)
        finally:
            if WELL_KNOWN_MANIFEST.exists():
                WELL_KNOWN_MANIFEST.unlink()
            if WELL_KNOWN_DIR.exists() and not any(WELL_KNOWN_DIR.iterdir()):
                WELL_KNOWN_DIR.rmdir()
            if WELL_KNOWN_DIR.parent.exists() and not any(WELL_KNOWN_DIR.parent.iterdir()):
                WELL_KNOWN_DIR.parent.rmdir()

    def test_injected_failure_propagates_sarif_mode(self):
        """When discovery manifest validation fails, --format sarif records result with ruleId='validate_discovery_manifests' and level='error'."""
        WELL_KNOWN_DIR.mkdir(parents=True, exist_ok=True)
        try:
            WELL_KNOWN_MANIFEST.write_text(
                json.dumps({"contract_type": "agent-skills-discovery", "skills": "not_an_array"}),
                encoding="utf-8",
            )
            proc = run_master_validator(["--parallel", "--format", "sarif"], timeout=45.0)
            self.assertEqual(proc.returncode, 1)
            sarif = json.loads(proc.stdout)
            results = sarif["runs"][0]["results"]
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["ruleId"], "validate_discovery_manifests")
            self.assertEqual(results[0]["level"], "error")
            self.assertEqual(
                results[0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
                "core/scripts/validate-discovery-manifests.py",
            )
            self.assertIn("Discovery manifest validation failed", results[0]["message"]["text"])
        finally:
            if WELL_KNOWN_MANIFEST.exists():
                WELL_KNOWN_MANIFEST.unlink()
            if WELL_KNOWN_DIR.exists() and not any(WELL_KNOWN_DIR.iterdir()):
                WELL_KNOWN_DIR.rmdir()
            if WELL_KNOWN_DIR.parent.exists() and not any(WELL_KNOWN_DIR.parent.iterdir()):
                WELL_KNOWN_DIR.parent.rmdir()

    def test_tampered_tier1_manifest_fails_closed(self):
        """Tampering with INDEX_TIER1.json digest triggers fail-closed in both validate-all and standalone validator."""
        orig_bytes = TIER1_MANIFEST_PATH.read_bytes()
        try:
            doc = json.loads(orig_bytes.decode("utf-8"))
            # Tamper with first skill digest
            doc["skills"][0]["digest"] = "sha256:" + "f" * 64
            TIER1_MANIFEST_PATH.write_text(json.dumps(doc, indent=2), encoding="utf-8")

            # 1. Standalone validator must fail closed
            proc_standalone = run_discovery_validator()
            self.assertEqual(proc_standalone.returncode, 1)
            self.assertIn("digest mismatch", proc_standalone.stderr + proc_standalone.stdout)

            # 2. Master CI parallel JSON mode must fail closed
            proc_master = run_master_validator(["--parallel", "--format", "json"], timeout=45.0)
            self.assertEqual(proc_master.returncode, 1)
            data = json.loads(proc_master.stdout)
            self.assertFalse(data["passed"])
            dm_entry = next(r for r in data["results"] if r["name"] == "validate-discovery-manifests.py")
            self.assertFalse(dm_entry["passed"])
            self.assertEqual(dm_entry["exit_code"], 1)
        finally:
            TIER1_MANIFEST_PATH.write_bytes(orig_bytes)


# ==============================================================================
# GROUP 3: Fail-Fast Interruption Mechanics
# ==============================================================================


class TestFailFastMechanics(unittest.TestCase):
    """Verifies that --fail-fast interrupts immediately upon validator failure."""

    def test_fail_fast_on_early_validator_stops_subsequent_execution(self):
        """When an early validator fails, --fail-fast halts after 1 validator instead of executing all 21."""
        claude_md = REPO_ROOT / "CLAUDE.md"
        claude_bak = REPO_ROOT / "CLAUDE.md.challenger_bak"
        claude_md.rename(claude_bak)
        try:
            # 1. Without fail-fast: all 21 validators run
            proc_no_ff = run_master_validator(["--format", "json"], timeout=60.0)
            self.assertEqual(proc_no_ff.returncode, 1)
            data_no_ff = json.loads(proc_no_ff.stdout)
            self.assertEqual(data_no_ff["total"], 21, "Without fail-fast, all 21 validators must run")

            # 2. With fail-fast: halts immediately on validator #1 (validate-rules.py)
            proc_ff = run_master_validator(["--fail-fast", "--format", "json"], timeout=30.0)
            self.assertEqual(proc_ff.returncode, 1)
            data_ff = json.loads(proc_ff.stdout)
            self.assertEqual(data_ff["total"], 1, "With fail-fast, execution must halt on the very first failure")
            self.assertFalse(data_ff["passed"])
            self.assertEqual(data_ff["results"][0]["name"], "validate-rules.py")
        finally:
            if claude_bak.exists():
                claude_bak.rename(claude_md)

    def test_fail_fast_on_discovery_manifest_failure(self):
        """When validate-discovery-manifests.py is the failing validator, --fail-fast stops and returns code 1."""
        WELL_KNOWN_DIR.mkdir(parents=True, exist_ok=True)
        try:
            WELL_KNOWN_MANIFEST.write_text(json.dumps({"invalid": True}), encoding="utf-8")
            proc = run_master_validator(["--fail-fast"], timeout=45.0)
            self.assertEqual(proc.returncode, 1)
            self.assertNotIn("All core validators passed.", proc.stdout)
        finally:
            if WELL_KNOWN_MANIFEST.exists():
                WELL_KNOWN_MANIFEST.unlink()
            if WELL_KNOWN_DIR.exists() and not any(WELL_KNOWN_DIR.iterdir()):
                WELL_KNOWN_DIR.rmdir()
            if WELL_KNOWN_DIR.parent.exists() and not any(WELL_KNOWN_DIR.parent.iterdir()):
                WELL_KNOWN_DIR.parent.rmdir()


# ==============================================================================
# GROUP 4: Parallel Concurrency Stress Testing
# ==============================================================================


class TestParallelConcurrencyStress(unittest.TestCase):
    """Stress tests validate-all.py --parallel under load, checking for race conditions and buffer corruption."""

    def test_repeated_parallel_runs_stability(self):
        """Running validate-all.py --parallel 5 consecutive times yields zero buffer corruption, zero race conditions, and exit code 0."""
        for iteration in range(5):
            t0 = time.monotonic()
            proc = run_master_validator(["--parallel"], timeout=30.0)
            dt = time.monotonic() - t0
            self.assertEqual(
                proc.returncode,
                0,
                f"Iteration {iteration + 1} failed in parallel mode:\n{proc.stdout}\n{proc.stderr}",
            )
            self.assertIn("All core validators passed.", proc.stdout)
            self.assertIn("Discovery manifest validation passed:", proc.stdout)
            # Parallel execution must complete rapidly (< 15 seconds)
            self.assertLess(dt, 15.0, f"Iteration {iteration + 1} took too long: {dt:.2f}s")

    def test_concurrent_multi_process_stress(self):
        """Launching 4 concurrent processes of validate-all.py --parallel simultaneously completes cleanly with code 0."""
        procs = [
            subprocess.Popen(
                [sys.executable, str(VALIDATE_ALL_SCRIPT), "--parallel"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(REPO_ROOT),
            )
            for _ in range(4)
        ]

        for idx, p in enumerate(procs):
            stdout, stderr = p.communicate(timeout=45.0)
            self.assertEqual(
                p.returncode,
                0,
                f"Concurrent process {idx} failed (code {p.returncode}):\n{stdout}\n{stderr}",
            )
            self.assertIn("All core validators passed.", stdout)
            self.assertIn("Discovery manifest validation passed:", stdout)

    def test_parallel_mode_preserves_validator_output_order(self):
        """validate-all.py --parallel must buffer and emit validator results in exact VALIDATORS registration order."""
        proc = run_master_validator(["--parallel", "--format", "json"], timeout=30.0)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        names = [r["name"] for r in data["results"]]

        code = VALIDATE_ALL_SCRIPT.read_text(encoding="utf-8")
        import ast
        tree = ast.parse(code)
        expected_validators = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "VALIDATORS":
                        if isinstance(node.value, ast.Tuple):
                            expected_validators = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]

        self.assertEqual(names, expected_validators, "Parallel execution results must preserve deterministic registration order")


# ==============================================================================
# GROUP 5: SARIF Schema Compliance & Rule Derivation
# ==============================================================================


class TestSarifSchemaCompliance(unittest.TestCase):
    """Verifies SARIF 2.1.0 specification adherence and dynamic rule ID derivation."""

    def test_sarif_210_structural_invariants(self):
        """SARIF output must strictly conform to SARIF 2.1.0 schema specification."""
        proc = run_master_validator(["--format", "sarif"], timeout=45.0)
        self.assertEqual(proc.returncode, 0)
        sarif = json.loads(proc.stdout)

        self.assertEqual(sarif.get("$schema"), "https://json.schemastore.org/sarif-2.1.0.json")
        self.assertEqual(sarif.get("version"), "2.1.0")

        runs = sarif.get("runs")
        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 1)

        tool = runs[0].get("tool", {})
        driver = tool.get("driver", {})
        self.assertEqual(driver.get("name"), "agent-pack-validator")
        self.assertEqual(driver.get("version"), "4.1.0")

        rules = driver.get("rules", [])
        self.assertEqual(len(rules), 21)
        for r in rules:
            self.assertIn("id", r)
            self.assertIn("name", r)
            self.assertIn("shortDescription", r)
            self.assertIn("defaultConfiguration", r)
            self.assertEqual(r["defaultConfiguration"].get("level"), "error")

    def test_sarif_rule_id_derivation_deterministic(self):
        """Each validator script name 'validate-foo-bar.py' must map to SARIF rule ID 'validate_foo_bar'."""
        proc = run_master_validator(["--parallel", "--format", "sarif"], timeout=30.0)
        self.assertEqual(proc.returncode, 0)
        sarif = json.loads(proc.stdout)
        rules = sarif["runs"][0]["tool"]["driver"]["rules"]
        rule_ids = [r["id"] for r in rules]

        # Expected rule ID derivation
        expected_rule_ids = [
            "validate_rules",
            "validate_skills",
            "validate_roles",
            "validate_workflows",
            "validate_packs",
            "validate_overlays",
            "validate_2026_compliance",
            "validate_contracts",
            "validate_a2a_compliance",
            "validate_agent_cards",
            "validate_standardization",
            "validate_version_sync",
            "validate_indexes",
            "validate_policy_consistency",
            "validate_skill_ownership",
            "validate_skill_sections",
            "validate_contract_coverage",
            "validate_golden_evals",
            "validate_thirdparty_skills",
            "validate_skill_security",
            "validate_discovery_manifests",
        ]
        self.assertEqual(rule_ids, expected_rule_ids)


# ==============================================================================
# GROUP 6: CLI Argument Boundaries & Edge Cases
# ==============================================================================


class TestCliArgumentBoundaries(unittest.TestCase):
    """Verifies CLI argument parsing error paths and boundaries."""

    def test_invalid_format_flag_exits_2(self):
        """Passing an unsupported --format value exits with code 2."""
        proc = run_master_validator(["--format", "unsupported_xml"], timeout=15.0)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("invalid choice", proc.stderr + proc.stdout)

    def test_unknown_cli_flag_exits_2(self):
        """Passing an unrecognized option exits with code 2."""
        proc = run_master_validator(["--unrecognized-option-xyz"], timeout=15.0)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unrecognized arguments", proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
