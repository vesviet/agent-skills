#!/usr/bin/env python3
"""Tier 5 Adversarial Coverage Hardening & Stress Testing: Policy Engine.

Milestone 5 Empirical Challenger Test Suite.
Adversarial coverage for:
1. Dynamic <domain>_<action> prefix resolution & command-line override interactions.
2. SVID token extraction, precedence, injection resistance, and tamper-proofing.
3. OCSF Class UID 99001 JSON schema compliance, rule_id resolution, and audit resilience.
4. Role boundary enforcement, read_only tier downgrade, and irreversible action invariants.
5. SARIF 2.1.0 emission and CLI output modes.
6. Empirical verification of destructive pattern precedence and shadowing behaviors.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECK_POLICY_SCRIPT = REPO_ROOT / "core" / "scripts" / "hooks" / "check-policy.py"
VALIDATE_POLICIES_SCRIPT = REPO_ROOT / "core" / "scripts" / "validate-policies.py"
ACTION_BOUNDARIES_PATH = REPO_ROOT / "core" / "policies" / "action-boundaries.yaml"
MCP_TOOL_MAP_PATH = REPO_ROOT / "core" / "policies" / "mcp-tool-map.yaml"
ROLES_DIR = REPO_ROOT / "core" / "roles"


def run_check_policy(
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: float = 15.0,
) -> subprocess.CompletedProcess:
    """Execute check-policy.py with isolated environment."""
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    cmd = [sys.executable, str(CHECK_POLICY_SCRIPT)] + (args or [])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=merged_env,
        timeout=timeout,
        check=False,
    )


class TestPrefixResolutionAdversarial(unittest.TestCase):
    """Adversarial stress testing of dynamic <domain>_<action> prefix resolution."""

    def test_all_8_prefixes_resolve_to_expected_actions(self):
        """Empirically verify all 8 prefix patterns resolve to their exact mapped actions."""
        prefix_cases = [
            ("db_drop_customers", "drop_database"),
            ("db_migrate_v2", "run_migrations"),
            ("db_query_orders", "read_file"),
            ("fs_write_config", "write_file"),
            ("fs_read_secret", "read_file"),
            ("git_push_release", "git_push"),
            ("sec_rotate_keys", "modify_secrets"),
            ("agent_delegate_task_42", "delegate_task"),
        ]
        for tool_name, expected_action in prefix_cases:
            res = run_check_policy(
                ["--format", "json"],
                env={"AGENT_ACTIVE_ROLE": "agent-coordinator", "CURSOR_TOOL_NAME": tool_name},
            )
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            self.assertEqual(
                data.get("mapped_action"),
                expected_action,
                f"Tool '{tool_name}' did not resolve to '{expected_action}', got '{data.get('mapped_action')}'",
            )

    def test_false_prefix_lookalikes_do_not_match_prefix_rules(self):
        """Tool names missing the underscore delimiter MUST NOT match prefix patterns."""
        false_prefixes = [
            ("dbdrop_users", "drop_database"),
            ("dbmigrate_all", "run_migrations"),
            ("gitpush_branch", "git_push"),
            ("secrotate_cert", "modify_secrets"),
            ("agentdelegate_sub", "delegate_task"),
        ]
        for tool_name, forbidden_action in false_prefixes:
            res = run_check_policy(
                ["--format", "json"],
                env={"AGENT_ACTIVE_ROLE": "agent-coordinator", "CURSOR_TOOL_NAME": tool_name},
            )
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            self.assertNotEqual(
                data.get("mapped_action"),
                forbidden_action,
                f"False prefix '{tool_name}' erroneously matched '{forbidden_action}'",
            )

    def test_case_insensitivity_and_whitespace_in_prefixes(self):
        """Prefix matching must be robust to uppercase and leading/trailing whitespace."""
        test_matrix = [
            ("  DB_DROP_ARCHIVE  ", "drop_database"),
            ("  Db_Migrate_Schema\t", "run_migrations"),
            ("\tFS_READ_PAYLOAD  ", "read_file"),
            ("  SEC_ROTATE_CREDS  ", "modify_secrets"),
        ]
        for tool_name, expected_action in test_matrix:
            res = run_check_policy(
                ["--format", "json"],
                env={"AGENT_ACTIVE_ROLE": "agent-coordinator", "CURSOR_TOOL_NAME": tool_name},
            )
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            self.assertEqual(data.get("mapped_action"), expected_action)

    def test_destructive_command_override_takes_precedence_over_prefix(self):
        """Destructive command in CURSOR_COMMAND overrides innocent prefix tool."""
        res = run_check_policy(
            ["--format", "json"],
            env={
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "CURSOR_TOOL_NAME": "fs_read_log",
                "CURSOR_COMMAND": "drop database production_db",
            },
        )
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        self.assertEqual(data.get("mapped_action"), "drop_database")

    def test_git_push_force_override_on_git_push_prefix(self):
        """git_push_prefix with force flag in command elevates from git_push to force_push."""
        res = run_check_policy(
            ["--format", "json"],
            env={
                "AGENT_ACTIVE_ROLE": "backend-developer",
                "CURSOR_TOOL_NAME": "git_push_branch",
                "CURSOR_COMMAND": "git push --force origin main",
            },
        )
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        self.assertEqual(data.get("mapped_action"), "force_push")
        self.assertEqual(res.returncode, 1, "force_push must be denied for backend-developer")

    def test_git_push_coarse_pattern_shadowing_empirical_demonstration(self):
        """Empirically demonstrates that 'git push' shadows 'git push origin :main' due to pattern array ordering."""
        # Because 'git push' is placed at index 4 and 'git push origin :main' at index 7,
        # 'git push' matches first and returns push_to_production.
        res = run_check_policy(
            ["--format", "json"],
            env={
                "AGENT_ACTIVE_ROLE": "devops-engineer",
                "CURSOR_TOOL_NAME": "git_push_sync",
                "CURSOR_COMMAND": "git push origin :main",
            },
        )
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        # Document the actual current mapping:
        self.assertEqual(data.get("mapped_action"), "push_to_production")
        # For devops-engineer, delete_branch_main is denied (code 1), but push_to_production is requires_approval (code 2)
        self.assertEqual(res.returncode, 2, "Shadowed by git push into requires_approval")

    def test_php_artisan_migrate_fresh_shadowing_empirical_demonstration(self):
        """Empirically demonstrates that 'migrate' shadows 'php artisan migrate:fresh' (drop_database)."""
        # Because 'migrate' appears before 'php artisan migrate:fresh',
        # 'php artisan migrate:fresh' is classified as run_migration instead of drop_database.
        res = run_check_policy(
            ["--format", "json"],
            env={
                "AGENT_ACTIVE_ROLE": "backend-developer",
                "CURSOR_TOOL_NAME": "shell",
                "CURSOR_COMMAND": "php artisan migrate:fresh",
            },
        )
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        self.assertEqual(data.get("mapped_action"), "run_migration")
        self.assertEqual(res.returncode, 2, "Misclassified as run_migration (requires_approval) instead of drop_database (denied)")

    def test_unmapped_tool_fails_closed_to_requires_approval(self):
        """Completely unknown tool without keywords fails closed to requires_approval."""
        res = run_check_policy(
            ["--format", "json"],
            env={
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "CURSOR_TOOL_NAME": "hypothetical_quantum_entangler",
            },
        )
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        self.assertEqual(data.get("mapped_action"), "requires_approval")
        self.assertEqual(data.get("decision"), "requires_approval")
        self.assertEqual(res.returncode, 2)


class TestSvidExtractionAndSecurity(unittest.TestCase):
    """Adversarial stress testing of SVID token extraction, precedence, and tamper resistance."""

    def test_svid_env_var_precedence(self):
        """AGENT_SVID_UID has precedence over AGENT_SVID_TOKEN_ID and AGENT_ACTOR_UID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"
            env = {
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "CURSOR_TOOL_NAME": "fs_read_policy",
                "AGENT_SVID_UID": "spiffe://primary/uid-1",
                "AGENT_SVID_TOKEN_ID": "spiffe://secondary/token-2",
                "AGENT_ACTOR_UID": "spiffe://tertiary/actor-3",
            }
            res = run_check_policy(
                ["--emit-audit", "--audit-path", str(audit_file)],
                env=env,
            )
            self.assertEqual(res.returncode, 0)
            event = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(event["actor"]["user"]["uid"], "spiffe://primary/uid-1")

    def test_svid_fallback_to_token_id_and_actor_uid(self):
        """When AGENT_SVID_UID is absent, falls back to AGENT_SVID_TOKEN_ID then AGENT_ACTOR_UID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"
            # Fallback to AGENT_SVID_TOKEN_ID
            env = {
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "CURSOR_TOOL_NAME": "fs_read_policy",
                "AGENT_SVID_TOKEN_ID": "spiffe://fallback/token-id",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env)
            event = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(event["actor"]["user"]["uid"], "spiffe://fallback/token-id")

            # Fallback to AGENT_ACTOR_UID
            env2 = {
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "CURSOR_TOOL_NAME": "fs_read_policy",
                "AGENT_ACTOR_UID": "spiffe://fallback/actor-uid",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env2)
            event2 = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(event2["actor"]["user"]["uid"], "spiffe://fallback/actor-uid")

    def test_svid_default_deterministic_uri_format(self):
        """When no SVID env var is provided, defaults to spiffe://agent-skills/role/{role}."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"
            env = {
                "AGENT_ACTIVE_ROLE": "security-engineer",
                "CURSOR_TOOL_NAME": "fs_read_policy",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env)
            event = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(
                event["actor"]["user"]["uid"],
                "spiffe://agent-skills/role/security-engineer",
            )

    def test_svid_tamper_payload_escaped_cleanly(self):
        """Adversarial SVID payloads (SQL, XSS, control chars, unicode) must not corrupt JSONL output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"
            adversarial_svids = [
                "spiffe://evil.com/sa?q=<script>alert('xss')</script>",
                "spiffe://evil.com/sa'; DROP TABLE audit_logs; --",
                "spiffe://evil.com/sa?claim=test&signature=valid%20signature",
                "spiffe://agent/🤖_special_chars_«test»_日本語",
            ]
            for svid in adversarial_svids:
                env = {
                    "AGENT_ACTIVE_ROLE": "agent-coordinator",
                    "CURSOR_TOOL_NAME": "fs_read_test",
                    "AGENT_SVID_UID": svid,
                }
                res = run_check_policy(
                    ["--emit-audit", "--audit-path", str(audit_file)],
                    env=env,
                )
                self.assertEqual(res.returncode, 0)

            # Audit file must contain exactly 4 valid JSON lines
            lines = audit_file.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 4)
            for i, line in enumerate(lines):
                parsed = json.loads(line)
                self.assertEqual(parsed.get("class_uid"), 99001)
                self.assertEqual(parsed["actor"]["user"]["uid"], adversarial_svids[i])

    def test_svid_cannot_bypass_irreversible_action_boundary(self):
        """Cryptographic SVID presence must NEVER pre-authorize irreversible actions."""
        env = {
            "AGENT_ACTIVE_ROLE": "backend-developer",
            "AGENT_SVID_UID": "spiffe://agent-skills/role/admin-super-caller",
            "CURSOR_TOOL_NAME": "db_drop_users",
            "CURSOR_COMMAND": "drop database users",
        }
        res = run_check_policy(["--format", "json"], env=env)
        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
        self.assertEqual(data.get("decision"), "denied")
        self.assertEqual(res.returncode, 1, "Database drop MUST be denied even with SVID")


class TestOcsfAuditStructureAndIntegrity(unittest.TestCase):
    """Adversarial verification of OCSF Class UID 99001 event structure and schema compliance."""

    def test_ocsf_schema_fields_strict_compliance(self):
        """Verify all mandatory OCSF Class UID 99001 fields are present and valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"
            cmd = "git push origin feature/login"
            expected_hash = hashlib.sha256(cmd.encode("utf-8")).hexdigest()[:16]
            trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"

            env = {
                "AGENT_ACTIVE_ROLE": "devops-engineer",
                "AGENT_ACTOR_NAME": "devops-worker-01",
                "AGENT_SVID_UID": "spiffe://prod/sa/devops-worker",
                "AGENT_TRACE_ID": trace_id,
                "CURSOR_TOOL_NAME": "git_push_feature",
                "CURSOR_COMMAND": cmd,
            }
            res = run_check_policy(
                ["--emit-audit", "--audit-path", str(audit_file)],
                env=env,
            )
            self.assertIn(res.returncode, [1, 2])
            event = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])

            # Class and category
            self.assertEqual(event.get("class_uid"), 99001)
            self.assertEqual(event.get("category_uid"), 9)
            self.assertEqual(event.get("activity_id"), 1)
            self.assertIsInstance(event.get("time"), int)

            # Actor structure
            actor_user = event.get("actor", {}).get("user", {})
            self.assertEqual(actor_user.get("name"), "devops-worker-01")
            self.assertEqual(actor_user.get("type"), "Non-Human Identity")
            self.assertEqual(actor_user.get("uid"), "spiffe://prod/sa/devops-worker")

            # Action structure
            action = event.get("action", {})
            self.assertEqual(action.get("name"), "git_push")
            self.assertEqual(action.get("command_sha256_16"), expected_hash)

            # Status and severity
            self.assertIn(event.get("status"), ["requires_approval", "denied"])
            self.assertIn(event.get("status_code"), ["HITL_TRIGGERED", "POLICY_DENIED"])
            self.assertIn(event.get("severity_id"), [3, 4])

            # Metadata and rule_id
            metadata = event.get("metadata", {})
            self.assertEqual(metadata.get("policy_version"), "2.0.0")
            self.assertEqual(metadata.get("rule_id"), "policy.action_boundary.git_push")

            # Trace
            self.assertEqual(event.get("trace", {}).get("id"), trace_id)

    def test_ocsf_rule_id_resolution_variants(self):
        """Rule ID properly reflects standard, read_only downgrade, always_denied, and custom override."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.jsonl"

            # 1. Custom rule ID override via env var
            env_custom = {
                "AGENT_ACTIVE_ROLE": "agent-coordinator",
                "AGENT_POLICY_RULE_ID": "custom.regulatory.sox_404",
                "CURSOR_TOOL_NAME": "fs_read_report",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env_custom)
            ev1 = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(ev1["metadata"]["rule_id"], "custom.regulatory.sox_404")

            # 2. Read-only level downgrade
            env_ro = {
                "AGENT_ACTIVE_ROLE": "backend-developer",
                "AGENT_ACTIVE_ROLE_LEVEL": "read_only",
                "CURSOR_TOOL_NAME": "fs_write_code",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env_ro)
            ev2 = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(ev2["metadata"]["rule_id"], "policy.level.read_only_downgrade")

            # 3. Always denied action (bypass_ai_guardrail)
            env_guardrail = {
                "AGENT_ACTIVE_ROLE": "security-engineer",
                "CURSOR_TOOL_NAME": "bypass_ai_guardrail",
            }
            run_check_policy(["--emit-audit", "--audit-path", str(audit_file)], env=env_guardrail)
            ev3 = json.loads(audit_file.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(ev3["metadata"]["rule_id"], "compliance.safety.always_denied")

    def test_ocsf_audit_directory_auto_creation(self):
        """Audit logger automatically creates multi-level missing directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deep_path = Path(tmpdir) / "sub1" / "sub2" / "sub3" / "events.jsonl"
            self.assertFalse(deep_path.parent.exists())
            run_check_policy(
                ["--emit-audit", "--audit-path", str(deep_path)],
                env={"AGENT_ACTIVE_ROLE": "agent-coordinator", "CURSOR_TOOL_NAME": "fs_read_doc"},
            )
            self.assertTrue(deep_path.is_file())


class TestRoleBoundariesAndLevelDowngrade(unittest.TestCase):
    """Adversarial stress testing of role boundaries, role-level downgrade, and irreversible actions."""

    def test_read_only_level_downgrades_mutating_actions_across_roles(self):
        """Under AGENT_ACTIVE_ROLE_LEVEL=read_only, all mutating actions downgrade to denied."""
        mutating_actions = [
            ("backend-developer", "fs_write_app", "write_file"),
            ("frontend-developer", "write_file", "write_file"),
            ("devops-engineer", "run_build", "run_build"),
            ("qa-engineer", "run_tests", "run_tests"),
            ("mobile-engineer", "install_dependency", "install_dependency"),
            ("game-developer", "run_dev_server", "run_dev_server"),
        ]
        for role, tool_name, mapped in mutating_actions:
            env = {
                "AGENT_ACTIVE_ROLE": role,
                "AGENT_ACTIVE_ROLE_LEVEL": "read_only",
                "CURSOR_TOOL_NAME": tool_name,
            }
            res = run_check_policy(["--format", "json"], env=env)
            self.assertEqual(
                res.returncode,
                1,
                f"Role {role} mutating tool {tool_name} was not downgraded to denied (exit code 1)",
            )
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            self.assertEqual(data.get("decision"), "denied")
            self.assertEqual(data.get("level_modifier"), "downgraded_to_denied")

    def test_read_only_level_preserves_allowed_for_read_only_actions(self):
        """Under read_only level, actions in READ_ONLY_ACTIONS stay allowed if role normally allows them."""
        safe_actions = [
            ("agent-coordinator", "fs_read_manifest", "read_file"),
            ("backend-developer", "fs_read_source", "read_file"),
            ("security-engineer", "search_code", "search_code"),
            ("agent-coordinator", "verify_svid_token", "verify_svid_token"),
            ("devops-engineer", "emit_ocsf_audit", "emit_ocsf_audit"),
        ]
        for role, tool_name, mapped in safe_actions:
            env = {
                "AGENT_ACTIVE_ROLE": role,
                "AGENT_ACTIVE_ROLE_LEVEL": "read_only",
                "CURSOR_TOOL_NAME": tool_name,
            }
            res = run_check_policy(["--format", "json"], env=env)
            self.assertEqual(
                res.returncode,
                0,
                f"Role {role} read action {tool_name} failed under read_only: {res.stdout}",
            )
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            self.assertEqual(data.get("decision"), "allowed")
            self.assertEqual(data.get("level_modifier"), "none")

    def test_irreversible_actions_never_allowed_across_all_39_roles(self):
        """Verify that zero roles out of 39 have drop_database, modify_secrets, push_to_production, or force_push in allowed."""
        boundaries = yaml.safe_load(ACTION_BOUNDARIES_PATH.read_text(encoding="utf-8")) or {}
        roles = boundaries.get("roles", {})
        self.assertEqual(len(roles), 39, "Expected 39 role profiles in action-boundaries.yaml")

        irreversible = ["drop_database", "modify_secrets", "push_to_production", "force_push"]
        for role_name, profile in roles.items():
            allowed = set(profile.get("allowed") or [])
            for action in irreversible:
                self.assertNotIn(
                    action,
                    allowed,
                    f"CRITICAL: Role '{role_name}' has irreversible action '{action}' in allowed tier!",
                )

    def test_drop_database_and_force_push_strictly_denied_for_all_roles(self):
        """drop_database and force_push must be strictly denied for every single role."""
        boundaries = yaml.safe_load(ACTION_BOUNDARIES_PATH.read_text(encoding="utf-8")) or {}
        roles = boundaries.get("roles", {})
        for role_name, profile in roles.items():
            denied = set(profile.get("denied") or [])
            self.assertIn(
                "drop_database",
                denied,
                f"Role '{role_name}' must have drop_database in denied tier",
            )
            self.assertIn(
                "force_push",
                denied,
                f"Role '{role_name}' must have force_push in denied tier",
            )

    def test_bypass_ai_guardrail_strictly_denied_for_all_roles(self):
        """bypass_ai_guardrail must be strictly denied for every role without exception."""
        boundaries = yaml.safe_load(ACTION_BOUNDARIES_PATH.read_text(encoding="utf-8")) or {}
        roles = boundaries.get("roles", {})
        for role_name, profile in roles.items():
            denied = set(profile.get("denied") or [])
            allowed = set(profile.get("allowed") or [])
            gated = set(profile.get("requires_approval") or [])
            self.assertIn(
                "bypass_ai_guardrail",
                denied,
                f"Role '{role_name}' must have bypass_ai_guardrail in denied",
            )
            self.assertNotIn("bypass_ai_guardrail", allowed)
            self.assertNotIn("bypass_ai_guardrail", gated)

    def test_zero_tier_overlap_across_all_39_roles(self):
        """No action verb can appear in more than one tier for any role."""
        boundaries = yaml.safe_load(ACTION_BOUNDARIES_PATH.read_text(encoding="utf-8")) or {}
        roles = boundaries.get("roles", {})
        for role_name, profile in roles.items():
            allowed = set(profile.get("allowed") or [])
            gated = set(profile.get("requires_approval") or [])
            denied = set(profile.get("denied") or [])

            self.assertEqual(allowed & gated, set(), f"Role '{role_name}' has allowed & gated overlap")
            self.assertEqual(allowed & denied, set(), f"Role '{role_name}' has allowed & denied overlap")
            self.assertEqual(gated & denied, set(), f"Role '{role_name}' has gated & denied overlap")


class TestSarifOutputAndCliModes(unittest.TestCase):
    """Stress testing of SARIF 2.1.0 output mode and CLI formatting."""

    def test_sarif_output_on_allowed_verdict(self):
        """SARIF output on allowed verdict produces valid SARIF JSON with empty results list."""
        env = {
            "AGENT_ACTIVE_ROLE": "agent-coordinator",
            "CURSOR_TOOL_NAME": "fs_read_doc",
        }
        res = run_check_policy(["--format", "sarif"], env=env)
        self.assertEqual(res.returncode, 0)
        sarif = json.loads(res.stdout)
        self.assertEqual(sarif.get("version"), "2.1.0")
        self.assertEqual(sarif.get("$schema"), "https://json.schemastore.org/sarif-2.1.0.json")
        runs = sarif.get("runs", [])
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["results"], [])

    def test_sarif_output_on_denied_verdict(self):
        """SARIF output on denied verdict produces rule error result."""
        env = {
            "AGENT_ACTIVE_ROLE": "backend-developer",
            "CURSOR_TOOL_NAME": "db_drop_users",
        }
        res = run_check_policy(["--format", "sarif"], env=env)
        self.assertEqual(res.returncode, 1)
        sarif = json.loads(res.stdout)
        runs = sarif.get("runs", [])
        self.assertEqual(len(runs), 1)
        results = runs[0].get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("level"), "error")
        self.assertEqual(results[0].get("ruleId"), "policy-check")

    def test_sarif_output_on_approval_required_verdict(self):
        """SARIF output on requires_approval verdict produces rule warning result for devops-engineer."""
        env = {
            "AGENT_ACTIVE_ROLE": "devops-engineer",
            "CURSOR_TOOL_NAME": "git_push_feature",
        }
        res = run_check_policy(["--format", "sarif"], env=env)
        self.assertEqual(res.returncode, 2)
        sarif = json.loads(res.stdout)
        runs = sarif.get("runs", [])
        results = runs[0].get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("level"), "warning")

    def test_text_output_format_on_denial(self):
        """Text format prints POLICY DENIED to stderr."""
        env = {
            "AGENT_ACTIVE_ROLE": "backend-developer",
            "CURSOR_TOOL_NAME": "db_drop_users",
        }
        res = run_check_policy(["--format", "text"], env=env)
        self.assertEqual(res.returncode, 1)
        self.assertIn("POLICY DENIED:", res.stderr)


if __name__ == "__main__":
    unittest.main()
