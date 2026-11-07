#!/usr/bin/env python3
"""Adversarial Challenger Test Suite for Milestone 4 (Phase 4 Policy-as-Code Hardening).

Empirically challenges core/scripts/validate-policies.py against:
1. Baseline valid execution (text & json formats, 39 roles, exit code 0).
2. CLI edge cases (--help, invalid formats, unrecognized flags, missing files, malformed YAML).
3. Mutation attacks using isolated temporary YAML fixtures:
   - Irreversible actions (drop_database, modify_secrets, force_push) injected into allowed.
   - Tier overlap (allowed+denied, allowed+requires_approval, requires_approval+denied).
   - Violation of ALWAYS_DENIED (bypass_ai_guardrail in allowed or requires_approval).
   - Incomplete MUST_CLASSIFY verb coverage.
   - Violation of write_file without create_file invariant.
   - Role inventory drift (phantom role in policy, missing role in policy).
   - MCP tool map drift (tool_actions or prefix_patterns mapping to actions not in policy).
   - JSON report schema integrity on multi-mutation failures.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_POLICIES_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-policies.py"
ACTION_BOUNDARIES_PATH = REPO_ROOT / "core" / "policies" / "action-boundaries.yaml"
MCP_TOOL_MAP_PATH = REPO_ROOT / "core" / "policies" / "mcp-tool-map.yaml"
ROLES_DIR = REPO_ROOT / "core" / "roles"


def run_validator(args: List[str] = None) -> subprocess.CompletedProcess:
    """Execute validate-policies.py with specified arguments."""
    cmd = [sys.executable, str(VALIDATE_POLICIES_SCRIPT)] + (args or [])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=30.0,
        check=False,
    )


class TestValidatePoliciesCliAndBaseline(unittest.TestCase):
    """Adversarial and boundary test coverage for CLI flags, defaults, and error exits."""

    def test_baseline_text_execution(self):
        """Verify default CLI runs cleanly with exit code 0 and announces 39 role profiles."""
        proc = run_validator()
        self.assertEqual(
            proc.returncode,
            0,
            f"Expected exit code 0, got {proc.returncode}.\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}",
        )
        self.assertIn("39 role profiles checked", proc.stdout)
        self.assertIn("Policy consistency validation passed", proc.stdout)

    def test_baseline_json_execution(self):
        """Verify --format json outputs strictly valid schema matching specification."""
        proc = run_validator(["--format", "json"])
        self.assertEqual(
            proc.returncode,
            0,
            f"Expected exit code 0, got {proc.returncode}.\nSTDOUT: {proc.stdout}",
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data.get("validator"), "validate-policies")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertTrue(data.get("passed"))
        self.assertEqual(data.get("exit_code"), 0)
        self.assertEqual(data.get("role_profiles_checked"), 39)
        self.assertEqual(data.get("errors"), [])
        self.assertEqual(data.get("error_count"), 0)

    def test_cli_help_flag(self):
        """Verify --help exits with 0 and prints informative usage."""
        proc = run_validator(["--help"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("usage: validate-policies.py", proc.stdout)
        self.assertIn("--format", proc.stdout)
        self.assertIn("--policy-path", proc.stdout)
        self.assertIn("--tool-map-path", proc.stdout)

    def test_cli_invalid_format_choice(self):
        """Verify invalid choice for --format exits with 2 per standard argparse."""
        proc = run_validator(["--format", "xml"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("invalid choice: 'xml'", proc.stderr)

    def test_cli_unrecognized_argument(self):
        """Verify unrecognized flags trigger exit code 2."""
        proc = run_validator(["--unrecognized-flag-xyz"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unrecognized arguments", proc.stderr)

    def test_cli_missing_policy_file(self):
        """Verify non-existent --policy-path causes exit code 1 with clean error."""
        bogus_path = REPO_ROOT / "core" / "policies" / "non_existent_policy.yaml"
        proc = run_validator(["--policy-path", str(bogus_path)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Policy file not found", proc.stdout + proc.stderr)

    def test_cli_missing_tool_map_file(self):
        """Verify non-existent --tool-map-path causes exit code 1 with clean error."""
        bogus_path = REPO_ROOT / "core" / "policies" / "non_existent_tool_map.yaml"
        proc = run_validator(["--tool-map-path", str(bogus_path)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("MCP tool map not found", proc.stdout + proc.stderr)

    def test_cli_missing_roles_dir(self):
        """Verify non-existent --roles-dir causes policy profile mismatch errors."""
        bogus_dir = REPO_ROOT / "core" / "non_existent_roles_dir"
        proc = run_validator(["--roles-dir", str(bogus_dir)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("policy profile", proc.stdout)

    def test_cli_malformed_yaml_policy(self):
        """Verify syntax error in YAML policy file is caught and exits 1 without crashing."""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write("roles:\n  backend-developer:\n    - unaligned:\n      [bad indentation")
            tmp_path = Path(f.name)
        try:
            proc = run_validator(["--policy-path", str(tmp_path)])
            self.assertEqual(proc.returncode, 1)
            self.assertIn("Failed to parse YAML", proc.stdout)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_cli_malformed_yaml_tool_map(self):
        """Verify syntax error in YAML tool map is caught and exits 1 without crashing."""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write("mcp_tool_routing:\n  prefix_patterns: [unclosed list")
            tmp_path = Path(f.name)
        try:
            proc = run_validator(["--tool-map-path", str(tmp_path)])
            self.assertEqual(proc.returncode, 1)
            self.assertIn("Failed to parse YAML", proc.stdout)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


class TestValidatePoliciesMutations(unittest.TestCase):
    """Adversarial stress-testing of policy logic via synthetic mutations in temporary files."""

    def setUp(self):
        self.original_policy_data = yaml.safe_load(ACTION_BOUNDARIES_PATH.read_text(encoding="utf-8"))
        self.original_tool_map_data = yaml.safe_load(MCP_TOOL_MAP_PATH.read_text(encoding="utf-8"))
        self.temp_files: List[Path] = []

    def tearDown(self):
        for path in self.temp_files:
            if path.exists():
                path.unlink()

    def _write_temp_policy(self, data: Dict[str, Any]) -> Path:
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)
            tmp_path = Path(f.name)
        self.temp_files.append(tmp_path)
        return tmp_path

    def _write_temp_tool_map(self, data: Dict[str, Any]) -> Path:
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)
            tmp_path = Path(f.name)
        self.temp_files.append(tmp_path)
        return tmp_path

    def test_mutation_irreversible_drop_database_in_allowed(self):
        """Adversarial: Injecting irreversible drop_database into allowed must be rejected with exit code 1."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "backend-developer"
        if "drop_database" in policy["roles"][target_role].get("denied", []):
            policy["roles"][target_role]["denied"].remove("drop_database")
        policy["roles"][target_role]["allowed"].append("drop_database")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"{target_role}: 'drop_database' is irreversible", proc.stdout)
        self.assertIn("must not be under allowed", proc.stdout)

    def test_mutation_irreversible_modify_secrets_in_allowed(self):
        """Adversarial: Injecting irreversible modify_secrets into allowed must be rejected with exit code 1."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "security-engineer"
        if "modify_secrets" in policy["roles"][target_role].get("requires_approval", []):
            policy["roles"][target_role]["requires_approval"].remove("modify_secrets")
        policy["roles"][target_role]["allowed"].append("modify_secrets")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"{target_role}: 'modify_secrets' is irreversible", proc.stdout)

    def test_mutation_irreversible_force_push_in_allowed(self):
        """Adversarial: Injecting irreversible force_push into allowed must be rejected with exit code 1."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "devops-engineer"
        if "force_push" in policy["roles"][target_role].get("denied", []):
            policy["roles"][target_role]["denied"].remove("force_push")
        policy["roles"][target_role]["allowed"].append("force_push")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"{target_role}: 'force_push' is irreversible", proc.stdout)

    def test_mutation_tier_overlap_allowed_and_denied(self):
        """Adversarial: Placing an action in both allowed and denied must be rejected."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "backend-developer"
        policy["roles"][target_role]["denied"].append("search_code")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("search_code", proc.stdout)
        self.assertIn("allowed+denied", proc.stdout)

    def test_mutation_tier_overlap_allowed_and_requires_approval(self):
        """Adversarial: Placing an action in both allowed and requires_approval must be rejected."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "frontend-developer"
        policy["roles"][target_role]["requires_approval"].append("write_file")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("write_file", proc.stdout)
        self.assertIn("allowed+requires_approval", proc.stdout)

    def test_mutation_tier_overlap_requires_approval_and_denied(self):
        """Adversarial: Placing an action in both requires_approval and denied must be rejected."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "qa-engineer"
        policy["roles"][target_role]["denied"].append("delete_file")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("delete_file", proc.stdout)
        self.assertIn("requires_approval+denied", proc.stdout)

    def test_mutation_always_denied_placed_in_allowed(self):
        """Adversarial: bypass_ai_guardrail in allowed must trigger ALWAYS_DENIED check."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "agent-coordinator"
        policy["roles"][target_role]["denied"].remove("bypass_ai_guardrail")
        policy["roles"][target_role]["allowed"].append("bypass_ai_guardrail")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("'bypass_ai_guardrail' must be denied for every role", proc.stdout)

    def test_mutation_always_denied_placed_in_requires_approval(self):
        """Adversarial: bypass_ai_guardrail in requires_approval must trigger ALWAYS_DENIED check."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "security-engineer"
        policy["roles"][target_role]["denied"].remove("bypass_ai_guardrail")
        policy["roles"][target_role]["requires_approval"].append("bypass_ai_guardrail")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("'bypass_ai_guardrail' must be denied for every role", proc.stdout)

    def test_mutation_must_classify_verb_unclassified(self):
        """Adversarial: Omitting delegate_task from all tiers of a role must be rejected."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "technical-writer"
        for tier in ("allowed", "requires_approval", "denied"):
            if "delegate_task" in policy["roles"][target_role].get(tier, []):
                policy["roles"][target_role][tier].remove("delegate_task")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"{target_role}: 'delegate_task' is not classified in any tier", proc.stdout)

    def test_mutation_write_without_create_invariant(self):
        """Adversarial: Role allowing write_file without create_file must fail invariant 6."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        target_role = "prompt-engineer"
        policy["roles"][target_role]["allowed"].remove("create_file")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"{target_role}: write_file is allowed but create_file is not", proc.stdout)

    def test_mutation_phantom_role_in_policy(self):
        """Adversarial: A role declared in action-boundaries.yaml without core/roles/*.md must fail."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        policy["roles"]["phantom-arbitrary-role"] = {
            "allowed": ["read_file", "search_code"],
            "requires_approval": [],
            "denied": ["bypass_ai_guardrail", "delegate_task"],
        }

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("policy profile phantom-arbitrary-role has no role file", proc.stdout)

    def test_mutation_missing_role_in_policy(self):
        """Adversarial: A role defined in core/roles/*.md missing from action-boundaries.yaml must fail."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        del policy["roles"]["agent-coordinator"]

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("no policy profile for role agent-coordinator", proc.stdout)

    def test_mutation_tool_map_maps_to_action_unclassified_by_any_role(self):
        """Adversarial: tool_actions pointing to an action not classified in any role must fail."""
        tool_map = yaml.safe_load(yaml.safe_dump(self.original_tool_map_data))
        tool_map["tool_actions"]["fictitious_tool"] = "completely_unknown_action_xyz"

        tmp_tool_map = self._write_temp_tool_map(tool_map)
        proc = run_validator(["--tool-map-path", str(tmp_tool_map)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("maps to action 'completely_unknown_action_xyz' which no role classifies", proc.stdout)

    def test_mutation_tool_map_prefix_pattern_unclassified_action(self):
        """Adversarial: prefix_patterns pointing to an action not in policy must fail."""
        tool_map = yaml.safe_load(yaml.safe_dump(self.original_tool_map_data))
        tool_map["mcp_tool_routing"]["prefix_patterns"].append(
            {"pattern": r"^audit_emit_.*", "action": "unclassified_audit_action_abc", "risk": "low"}
        )

        tmp_tool_map = self._write_temp_tool_map(tool_map)
        proc = run_validator(["--tool-map-path", str(tmp_tool_map)])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("maps to action 'unclassified_audit_action_abc' which no role classifies", proc.stdout)

    def test_mutation_json_schema_on_failure(self):
        """Adversarial: Multi-mutation failure in JSON mode yields well-structured error payload."""
        policy = yaml.safe_load(yaml.safe_dump(self.original_policy_data))
        policy["roles"]["backend-developer"]["allowed"].append("drop_database")
        policy["roles"]["security-engineer"]["allowed"].append("modify_secrets")

        tmp_policy = self._write_temp_policy(policy)
        proc = run_validator(["--policy-path", str(tmp_policy), "--format", "json"])
        self.assertEqual(proc.returncode, 1)

        payload = json.loads(proc.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual(payload["exit_code"], 1)
        self.assertGreaterEqual(payload["error_count"], 2)
        self.assertIsInstance(payload["errors"], list)
        errors_text = " ".join(payload["errors"])
        self.assertIn("backend-developer: 'drop_database' is irreversible", errors_text)
        self.assertIn("security-engineer: 'modify_secrets' is irreversible", errors_text)


if __name__ == "__main__":
    unittest.main()
