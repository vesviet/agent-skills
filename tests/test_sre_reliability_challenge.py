#!/usr/bin/env python3
"""Automated Challenge Test Suite for Site Reliability Engineer (SRE) Modernization & 2026-2027 Reliability Standards.

Validates and stress-tests:
1. SRE Role Invariants (core/roles/sre.md):
   - Role-standard structure, mission, level, monotonic sections.
   - 5 Guardrail Locks (SLO-INTEGRITY LOCK, MWMBR-BURN-RATE LOCK, CHAOS-VERIFICATION LOCK, EBPF-TELEMETRY LOCK, INCIDENT-POSTMORTEM LOCK).
   - Modern SRE core responsibilities across 4 SOTA pillars.
   - Primary skills toolbox including orchestrate-chaos-experiment.
   - Boundaries, deliverables, and role footer date.

2. SRE Review Checklist Completeness (core/roles/references/sre-review-checklist.md):
   - All 6 structured sections.
   - 14+ actionable criteria with technical keywords (MWMBR, eBPF, OTel GenAI, 5 Whys, Chaos Mesh).
   - Exact footer date.

3. Incident Report Schema Meta & Examples (core/contracts/schemas/incident-report.json):
   - Draft 2020-12 meta-schema compliance.
   - Bundled examples 100% compliant with format checker.
   - Modern reliability properties: metrics, error_budget_impact, trace_context, root_cause_analysis, action_items.

4. Incident Report Adversarial Mutations:
   - Required field deletion, invalid discriminator, invalid enums, negative metrics,
     malformed trace context, invalid RCA taxonomy, invalid action item fields, fuzzing.

5. Chaos Engineering Skill Structure (core/skills/platform/orchestrate-chaos-experiment/):
   - SKILL.md under 200 lines, valid frontmatter, required sections.
   - Companion files (agents/openai.yaml, references/chaos-engineering-guide.md).
   - Single Primary owner ('sre') with 0 conflicts.

6. SRE Alias Resolution & Registry Sync:
   - Fast invocation aliases in generate-index.py.
   - A2A agent card and registry entry for sre.
   - README catalog counts and zero drift on generate-index.py --check.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
CONTRACTS_DIR = CORE_DIR / "contracts" / "schemas"
REGISTRY_DIR = CORE_DIR / "a2a" / ".well-known"
AGENT_CARDS_DIR = CORE_DIR / "a2a" / "registry"
SCRIPTS_DIR = CORE_DIR / "scripts"


class TestSRERoleInvariants(unittest.TestCase):
    """Verify core/roles/sre.md structure, guardrail locks, and responsibilities."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "sre.md"
        assert cls.role_path.exists(), f"Role file missing: {cls.role_path}"
        cls.content = cls.role_path.read_text(encoding="utf-8")

    def test_01_role_file_exists_and_standard_structure(self):
        """Verifies core/roles/sre.md has 1 H1, Mission, Level, role-standard ref, and all 17 required sections in order."""
        body_without_fences = re.sub(r"```.*?```", "", self.content, flags=re.S)
        h1_lines = [l.strip() for l in body_without_fences.splitlines() if l.strip().startswith("# ")]
        self.assertEqual(len(h1_lines), 1, "Must contain exactly one H1 role title")
        self.assertEqual(h1_lines[0], "# Site Reliability Engineer")

        self.assertRegex(self.content, r"(?m)^Mission: .+", "Must contain Mission line")
        self.assertRegex(self.content, r"(?m)^Level: .+", "Must contain Level line")
        self.assertIn(
            "This role must follow [role-standard](role-standard.md) first.",
            self.content,
            "Must reference role-standard",
        )

        required_sections = [
            "## Principal Expectations",
            "## Use This Role When",
            "## Core Responsibilities",
            "## Inputs Required",
            "## Outputs Produced",
            "## Deliverable Routing",
            "## Decision Boundaries",
            "## Collaboration",
            "## Guardrails",
            "## Skill Toolbox",
            "### Primary Skills",
            "### Supporting Skills (use when collaborating)",
            "## Output Template",
            "## Review Checklist",
            "## Anti-Patterns To Reject",
            "## Role Handoff",
            "## Definition Of Done",
        ]

        last_idx = -1
        for section in required_sections:
            idx = self.content.find(section)
            self.assertNotEqual(idx, -1, f"Missing required section: {section}")
            self.assertGreater(idx, last_idx, f"Section out of order: {section}")
            last_idx = idx

    def test_02_mandatory_guardrail_locks(self):
        """Verifies SLO-INTEGRITY LOCK, MWMBR-BURN-RATE LOCK, CHAOS-VERIFICATION LOCK, EBPF-TELEMETRY LOCK, INCIDENT-POSTMORTEM LOCK, and base locks."""
        mandatory_locks = [
            "SLO-INTEGRITY LOCK",
            "MWMBR-BURN-RATE LOCK",
            "CHAOS-VERIFICATION LOCK",
            "EBPF-TELEMETRY LOCK",
            "INCIDENT-POSTMORTEM LOCK",
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "TRACE LOCK",
            "UNCERTAINTY LOCK",
            "AI-SLO LOCK",
            "ERROR-BUDGET LOCK",
        ]
        for lock in mandatory_locks:
            self.assertIn(lock, self.content, f"Guardrail Lock '{lock}' not found in sre.md")

    def test_03_modern_sre_core_responsibilities(self):
        """Verifies MWMBR error budget governance, eBPF socket profiling, OTel v1.30+ GenAI conventions (gen_ai.usage.tokens, TTFT), and automated chaos."""
        keywords = [
            "Multi-Window Multi-Burn-Rate",
            "MWMBR",
            "eBPF",
            "socket profiling",
            "gen_ai.usage.tokens",
            "TTFT",
            "Chaos Mesh",
            "steady-state",
            "automated runbooks",
            "5 Whys",
        ]
        for kw in keywords:
            self.assertIn(kw, self.content, f"Keyword '{kw}' missing from sre.md")

    def test_04_primary_skills_toolbox(self):
        """Verifies sre.md primary skills include: debug-runtime-platform, troubleshoot-service, add-telemetry-instrumentation, performance-profiling, incident-report, orchestrate-chaos-experiment."""
        primary_skills = [
            "debug-runtime-platform",
            "troubleshoot-service",
            "add-telemetry-instrumentation",
            "performance-profiling",
            "incident-report",
            "orchestrate-chaos-experiment",
        ]
        toolbox_match = re.search(r"### Primary Skills\s*\n\n(.*?)(?=\n### |\n## )", self.content, re.S)
        self.assertIsNotNone(toolbox_match, "Could not extract Primary Skills section")
        primary_block = toolbox_match.group(1)
        for skill in primary_skills:
            self.assertIn(f"`{skill}`", primary_block, f"Primary skill '{skill}' missing from sre.md")

        # Zero overlap check
        supporting_match = re.search(r"### Supporting Skills.*?\n\n(.*?)(?=\n## )", self.content, re.S)
        self.assertIsNotNone(supporting_match, "Could not extract Supporting Skills section")
        supporting_block = supporting_match.group(1)
        for skill in primary_skills:
            self.assertNotIn(f"`{skill}`", supporting_block, f"Skill '{skill}' cannot be both Primary and Supporting")

    def test_05_role_boundaries_and_deliverables(self):
        """Verifies Deliverable Routing (incident-report.json), Decision Boundaries, Role Boundaries (SRE, DevOps, QA, Cloudflare), and Role Handoff."""
        self.assertIn("incident-report.json", self.content)
        self.assertIn("## Role Boundaries", self.content)
        self.assertIn("DevOps Engineer", self.content)
        self.assertIn("Cloudflare Engineer", self.content)
        self.assertIn("QA Engineer", self.content)
        self.assertIn("Backend Developer", self.content)

    def test_06_role_footer_date(self):
        """Verifies footer is exactly 'Last updated: 2026-10-05' as the final non-empty line."""
        non_empty = [l.strip() for l in self.content.splitlines() if l.strip()]
        self.assertEqual(non_empty[-1], "Last updated: 2026-10-05")


class TestSREReviewChecklistCompleteness(unittest.TestCase):
    """Verify core/roles/references/sre-review-checklist.md structure and criteria."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "sre-review-checklist.md"
        assert cls.checklist_path.exists(), f"Checklist missing: {cls.checklist_path}"
        cls.content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_checklist_file_exists_and_sections(self):
        """Verifies core/roles/references/sre-review-checklist.md exists and has all 6 structured sections."""
        expected_sections = [
            "### 1. Service Level Objectives & MWMBR Error Budget Governance",
            "### 2. OpenTelemetry & eBPF Telemetry Observability",
            "### 3. Incident Detection, Containment & Root Cause Analysis (5 Whys)",
            "### 4. Chaos Engineering & Steady-State Failure Injection",
            "### 5. Automated Runbooks, Toil Reduction & Capacity Planning",
            "### 6. Machine Contract Artifacts & Postmortem Action Tracking",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.content, f"Section '{sec}' not found in sre-review-checklist.md")

    def test_02_checklist_criteria_count(self):
        """Verifies >= 14 actionable bullet criteria across the sections."""
        criteria = re.findall(r"(?m)^-\s+\*\*([^*]+)\*\*:", self.content)
        self.assertGreaterEqual(len(criteria), 14, f"Found only {len(criteria)} criteria, expected >= 14")

    def test_03_checklist_technical_keywords(self):
        """Verifies MWMBR, burn rate, eBPF, OpenTelemetry, TTFT, 5 Whys, Chaos Mesh, Litmus, blast radius, runbook, toil, incident-report.json, MTTD, MTTR."""
        keywords = [
            "MWMBR",
            "eBPF",
            "OpenTelemetry",
            "TTFT",
            "5 Whys",
            "Chaos Mesh",
            "Litmus",
            "blast radius",
            "runbook",
            "toil",
            "incident-report.json",
            "MTTD",
            "MTTR",
        ]
        for kw in keywords:
            self.assertTrue(
                bool(re.search(re.escape(kw), self.content, re.IGNORECASE)),
                f"Keyword '{kw}' missing from sre-review-checklist.md",
            )

    def test_04_checklist_footer_date(self):
        """Verifies footer is exactly 'Last updated: 2026-10-05'."""
        non_empty = [l.strip() for l in self.content.splitlines() if l.strip()]
        self.assertEqual(non_empty[-1], "Last updated: 2026-10-05")


class TestIncidentReportSchemaMetaAndExamples(unittest.TestCase):
    """Verify Draft 2020-12 meta-schema compliance and validity of bundled examples in incident-report.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "incident-report.json"
        assert cls.schema_path.exists(), f"Schema missing: {cls.schema_path}"
        cls.schema = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=Draft202012Validator.FORMAT_CHECKER)

    def test_01_meta_schema_conformance(self):
        """Validates $schema, $id, type object via Draft202012Validator.check_schema()."""
        self.assertEqual(self.schema.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema.get("$id"), "incident-report")
        self.assertEqual(self.schema.get("type"), "object")
        Draft202012Validator.check_schema(self.schema)

    def test_02_bundled_examples_pass_validation(self):
        """Validates all examples in incident-report.json with Draft202012Validator."""
        examples = self.schema.get("examples", [])
        self.assertGreaterEqual(len(examples), 1, "Schema must include at least one example")
        for i, example in enumerate(examples):
            errors = list(self.validator.iter_errors(example))
            self.assertEqual(
                len(errors),
                0,
                f"Example {i} failed validation with errors: {[e.message for e in errors]}",
            )

    def test_03_modern_reliability_properties_declared(self):
        """Verifies properties declare metrics, error_budget_impact, trace_context, root_cause_analysis, action_items."""
        props = self.schema.get("properties", {})
        expected_props = [
            "metrics",
            "error_budget_impact",
            "trace_context",
            "root_cause_analysis",
            "action_items",
        ]
        for p in expected_props:
            self.assertIn(p, props, f"Property '{p}' not declared in incident-report.json")
            self.assertIn(p, self.schema.get("required", []), f"Property '{p}' must be in top-level required list")


class TestIncidentReportAdversarialMutations(unittest.TestCase):
    """Adversarial negative mutation testing to verify schema rejects corrupt inputs."""

    @classmethod
    def setUpClass(cls):
        schema_path = CONTRACTS_DIR / "incident-report.json"
        cls.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        cls.valid_example = copy.deepcopy(cls.schema["examples"][0])

    def test_01_negative_mutation_missing_top_level_required(self):
        """Deleting any required field raises ValidationError."""
        required_fields = self.schema.get("required", [])
        for field in required_fields:
            mutated = copy.deepcopy(self.valid_example)
            del mutated[field]
            with self.assertRaises(ValidationError, msg=f"Should reject payload missing '{field}'"):
                self.validator.validate(mutated)

    def test_02_negative_mutation_invalid_contract_type(self):
        """Corrupting contract_type discriminator raises ValidationError."""
        for invalid_val in ["deployment-plan", "invalid-type", "", 123]:
            mutated = copy.deepcopy(self.valid_example)
            mutated["contract_type"] = invalid_val
            with self.assertRaises(ValidationError):
                self.validator.validate(mutated)

    def test_03_negative_mutation_invalid_severity_enum(self):
        """Setting severity to 'CRITICAL', 'P0', 'LOW', '' raises ValidationError."""
        for invalid_sev in ["CRITICAL", "P0", "LOW", ""]:
            mutated = copy.deepcopy(self.valid_example)
            mutated["severity"] = invalid_sev
            with self.assertRaises(ValidationError):
                self.validator.validate(mutated)

    def test_04_negative_mutation_invalid_status_enum(self):
        """Setting status to 'open', 'closed', 'fixed' raises ValidationError."""
        for invalid_status in ["open", "closed", "fixed", "pending"]:
            mutated = copy.deepcopy(self.valid_example)
            mutated["status"] = invalid_status
            with self.assertRaises(ValidationError):
                self.validator.validate(mutated)

    def test_05_negative_mutation_invalid_metrics(self):
        """Negative mttd_seconds, non-number mttr_seconds, or missing mttm_seconds raises ValidationError."""
        # Negative mttd
        mutated1 = copy.deepcopy(self.valid_example)
        mutated1["metrics"]["mttd_seconds"] = -10
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated1)

        # String mttr
        mutated2 = copy.deepcopy(self.valid_example)
        mutated2["metrics"]["mttr_seconds"] = "fast"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated2)

        # Missing mttm
        mutated3 = copy.deepcopy(self.valid_example)
        del mutated3["metrics"]["mttm_seconds"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated3)

    def test_06_negative_mutation_invalid_error_budget(self):
        """Negative burn_rate_peak, budget_consumed_percentage > 100 or < 0, non-boolean slo_breached raises ValidationError."""
        mutated1 = copy.deepcopy(self.valid_example)
        mutated1["error_budget_impact"]["burn_rate_peak"] = -1
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated1)

        mutated2 = copy.deepcopy(self.valid_example)
        mutated2["error_budget_impact"]["budget_consumed_percentage"] = 105.0
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated2)

        mutated3 = copy.deepcopy(self.valid_example)
        mutated3["error_budget_impact"]["slo_breached"] = "true"  # string instead of boolean
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated3)

    def test_07_negative_mutation_invalid_trace_context(self):
        """Non-32-hex root_trace_id or non-16-hex culprit_span_id raises ValidationError against regex pattern."""
        mutated1 = copy.deepcopy(self.valid_example)
        mutated1["trace_context"]["root_trace_id"] = "not-a-32-hex-trace-id"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated1)

        mutated2 = copy.deepcopy(self.valid_example)
        mutated2["trace_context"]["culprit_span_id"] = "xyz"  # invalid length & chars
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated2)

    def test_08_negative_mutation_invalid_rca(self):
        """Invalid failure_category enum or empty five_whys array raises ValidationError."""
        mutated1 = copy.deepcopy(self.valid_example)
        mutated1["root_cause_analysis"]["failure_category"] = "unclassified_accident"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated1)

        mutated2 = copy.deepcopy(self.valid_example)
        mutated2["root_cause_analysis"]["five_whys"] = ["Single why"]  # minItems is 3
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated2)

    def test_09_negative_mutation_invalid_action_items(self):
        """Missing action_item_id, invalid priority enum, invalid target_completion_date raises ValidationError."""
        mutated1 = copy.deepcopy(self.valid_example)
        del mutated1["action_items"][0]["action_item_id"]
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated1)

        mutated2 = copy.deepcopy(self.valid_example)
        mutated2["action_items"][0]["priority"] = "URGENT"
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated2)

        mutated3 = copy.deepcopy(self.valid_example)
        mutated3["action_items"][0]["target_completion_date"] = "next-friday"  # not date format
        with self.assertRaises(ValidationError):
            self.validator.validate(mutated3)

    def test_10_randomized_adversarial_fuzzing(self):
        """25 randomized corrupt mutations all rejected by Draft202012Validator."""
        corruptions = [
            lambda p: p.pop("metrics", None),
            lambda p: p.pop("trace_context", None),
            lambda p: p["metrics"].update({"mttd_seconds": -random.randint(1, 1000)}),
            lambda p: p["error_budget_impact"].update({"budget_consumed_percentage": 100 + random.randint(1, 50)}),
            lambda p: p["trace_context"].update({"root_trace_id": "0" * 31}),
            lambda p: p["trace_context"].update({"culprit_span_id": "g" * 16}),  # non-hex
            lambda p: p["root_cause_analysis"].update({"failure_category": "non_existent_failure_mode"}),
            lambda p: p["action_items"][0].update({"priority": "P9"}),
            lambda p: p.update({"severity": "SEV-5"}),
            lambda p: p.update({"status": "partially_resolved"}),
        ]
        for i in range(25):
            payload = copy.deepcopy(self.valid_example)
            corrupt = random.choice(corruptions)
            corrupt(payload)
            with self.assertRaises(ValidationError, msg=f"Fuzz iteration {i} should fail validation"):
                self.validator.validate(payload)

    def test_11_adversarial_w3c_trace_id_boundary_and_corruption(self):
        """W3C trace ID mutations (31-hex, 33-hex, non-hex, missing, span ID corrupted) are rejected."""
        # 31-hex chars
        m = copy.deepcopy(self.valid_example)
        m["trace_context"]["root_trace_id"] = "a" * 31
        with self.assertRaises(ValidationError, msg="31-char trace ID must be rejected"):
            self.validator.validate(m)

        # 33-hex chars
        m = copy.deepcopy(self.valid_example)
        m["trace_context"]["root_trace_id"] = "a" * 33
        with self.assertRaises(ValidationError, msg="33-char trace ID must be rejected"):
            self.validator.validate(m)

        # Non-hex characters
        for non_hex in ["g" * 32, "z" * 32, "4bf92f3577b34da6a3ce929d0e0e473g", "1234567890123456789012345678901-"]:
            m = copy.deepcopy(self.valid_example)
            m["trace_context"]["root_trace_id"] = non_hex
            with self.assertRaises(ValidationError, msg=f"Non-hex trace ID '{non_hex}' must be rejected"):
                self.validator.validate(m)

        # Missing root_trace_id
        m = copy.deepcopy(self.valid_example)
        del m["trace_context"]["root_trace_id"]
        with self.assertRaises(ValidationError, msg="Missing root_trace_id must be rejected"):
            self.validator.validate(m)

        # Span ID boundary mutations (15-hex, 17-hex, non-hex, missing)
        for bad_span in ["b" * 15, "b" * 17, "h" * 16, ""]:
            m = copy.deepcopy(self.valid_example)
            m["trace_context"]["culprit_span_id"] = bad_span
            with self.assertRaises(ValidationError, msg=f"Corrupt span ID '{bad_span}' must be rejected"):
                self.validator.validate(m)

        m = copy.deepcopy(self.valid_example)
        del m["trace_context"]["culprit_span_id"]
        with self.assertRaises(ValidationError, msg="Missing culprit_span_id must be rejected"):
            self.validator.validate(m)

    def test_12_adversarial_negative_duration_metrics(self):
        """Negative duration values (MTTD < 0, MTTR < 0, MTTM < 0) are strictly rejected."""
        for field in ["mttd_seconds", "mttm_seconds", "mttr_seconds"]:
            for negative_val in [-0.001, -1, -500, -86400]:
                m = copy.deepcopy(self.valid_example)
                m["metrics"][field] = negative_val
                with self.assertRaises(ValidationError, msg=f"Negative {field}={negative_val} must be rejected"):
                    self.validator.validate(m)

    def test_13_adversarial_out_of_bounds_error_budget_metrics(self):
        """Out-of-bounds error budget metrics (< 0%, > 100%, negative burn rate) are rejected."""
        # budget_consumed_percentage < 0
        for negative_pct in [-0.001, -1.0, -100.0]:
            m = copy.deepcopy(self.valid_example)
            m["error_budget_impact"]["budget_consumed_percentage"] = negative_pct
            with self.assertRaises(ValidationError, msg=f"Budget consumed < 0 ({negative_pct}%) must be rejected"):
                self.validator.validate(m)

        # budget_consumed_percentage > 100
        for excess_pct in [100.001, 101.0, 250.0]:
            m = copy.deepcopy(self.valid_example)
            m["error_budget_impact"]["budget_consumed_percentage"] = excess_pct
            with self.assertRaises(ValidationError, msg=f"Budget consumed > 100 ({excess_pct}%) must be rejected"):
                self.validator.validate(m)

        # burn_rate_peak < 0
        for negative_burn in [-0.001, -1.0, -50.0]:
            m = copy.deepcopy(self.valid_example)
            m["error_budget_impact"]["burn_rate_peak"] = negative_burn
            with self.assertRaises(ValidationError, msg=f"Negative burn rate {negative_burn} must be rejected"):
                self.validator.validate(m)

    def test_14_adversarial_rca_taxonomy_and_5_whys_boundaries(self):
        """Invalid RCA taxonomy enums and five_whys chains (< 3 items) are rejected."""
        # Invalid taxonomy enums
        for invalid_cat in ["unknown", "hardware_failure", "human_error", "network_glitch", "", 123]:
            m = copy.deepcopy(self.valid_example)
            m["root_cause_analysis"]["failure_category"] = invalid_cat
            with self.assertRaises(ValidationError, msg=f"Invalid RCA taxonomy '{invalid_cat}' must be rejected"):
                self.validator.validate(m)

        # five_whys < 3 items
        for short_chain in [[], ["Single root cause"], ["Why 1", "Why 2"]]:
            m = copy.deepcopy(self.valid_example)
            m["root_cause_analysis"]["five_whys"] = short_chain
            with self.assertRaises(ValidationError, msg=f"5 Whys with {len(short_chain)} items must be rejected"):
                self.validator.validate(m)

    def test_15_adversarial_action_items_corruption(self):
        """Corrupted action items (missing verification mechanism, invalid priority, invalid calendar dates) are rejected."""
        # Missing verification_mechanism
        m = copy.deepcopy(self.valid_example)
        del m["action_items"][0]["verification_mechanism"]
        with self.assertRaises(ValidationError, msg="Action item missing verification_mechanism must be rejected"):
            self.validator.validate(m)

        # Invalid priority enum
        for bad_prio in ["P4", "P-1", "CRITICAL", "HIGH", "LOW", "URGENT", ""]:
            m = copy.deepcopy(self.valid_example)
            m["action_items"][0]["priority"] = bad_prio
            with self.assertRaises(ValidationError, msg=f"Invalid priority '{bad_prio}' must be rejected"):
                self.validator.validate(m)

        # Invalid calendar dates (2026-02-29 non-leap year, invalid months/days)
        for bad_date in ["2026-02-29", "2026-13-01", "2026-04-31", "2026-00-10", "tomorrow", "2026/10/05"]:
            m = copy.deepcopy(self.valid_example)
            m["action_items"][0]["target_completion_date"] = bad_date
            with self.assertRaises(ValidationError, msg=f"Invalid calendar date '{bad_date}' must be rejected"):
                self.validator.validate(m)

    def test_16_edge_case_valid_payloads(self):
        """Valid boundary payloads (0s MTTD/MTTR, 0% budget, 100% budget, valid leap date, exact 3 whys) validate cleanly."""
        # Boundary 1: 0s detection, mitigation, resolution and 0% budget consumed
        m1 = copy.deepcopy(self.valid_example)
        m1["metrics"]["mttd_seconds"] = 0
        m1["metrics"]["mttm_seconds"] = 0
        m1["metrics"]["mttr_seconds"] = 0
        m1["error_budget_impact"]["burn_rate_peak"] = 0.0
        m1["error_budget_impact"]["budget_consumed_percentage"] = 0.0
        m1["error_budget_impact"]["slo_breached"] = False
        m1["root_cause_analysis"]["five_whys"] = ["Why 1: load spike", "Why 2: no rate limit", "Why 3: missing middleware"]
        errors1 = list(self.validator.iter_errors(m1))
        self.assertEqual(len(errors1), 0, f"Valid 0s and 0% boundary failed: {[e.message for e in errors1]}")

        # Boundary 2: 100% budget consumed, multi-day MTTR (10 days = 864,000s), valid leap year date (2028-02-29)
        m2 = copy.deepcopy(self.valid_example)
        m2["metrics"]["mttr_seconds"] = 864000.0
        m2["error_budget_impact"]["budget_consumed_percentage"] = 100.0
        m2["error_budget_impact"]["burn_rate_peak"] = 56.4
        m2["error_budget_impact"]["slo_breached"] = True
        m2["action_items"][0]["target_completion_date"] = "2028-02-29"
        errors2 = list(self.validator.iter_errors(m2))
        self.assertEqual(len(errors2), 0, f"Valid 100% budget and leap date failed: {[e.message for e in errors2]}")


class TestChaosEngineeringSkillStructure(unittest.TestCase):
    """Verify core/skills/platform/orchestrate-chaos-experiment/ manifest and companions."""

    @classmethod
    def setUpClass(cls):
        cls.skill_dir = SKILLS_DIR / "platform" / "orchestrate-chaos-experiment"
        cls.skill_path = cls.skill_dir / "SKILL.md"
        assert cls.skill_path.exists(), f"SKILL.md missing: {cls.skill_path}"
        cls.text = cls.skill_path.read_text(encoding="utf-8")

    def test_01_skill_file_and_frontmatter(self):
        """Verifies core/skills/platform/orchestrate-chaos-experiment/SKILL.md exists, < 200 lines, valid YAML frontmatter with allowed-tools."""
        total_lines = len(self.text.splitlines())
        self.assertLess(total_lines, 200, f"SKILL.md must be < 200 lines, got {total_lines}")

        # Parse YAML frontmatter
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", self.text, re.S)
        self.assertIsNotNone(m, "Frontmatter missing")
        fm = yaml.safe_load(m.group(1))
        self.assertEqual(fm.get("name"), "orchestrate-chaos-experiment")
        self.assertIn("Use when ", fm.get("description", ""))
        self.assertIsInstance(fm.get("allowed-tools"), list)
        self.assertGreater(len(fm.get("allowed-tools")), 0)

    def test_02_skill_baseline_sections(self):
        """Verifies Core Rules (5+ rules), Suggested Process, Checklist, Related Skills, Security Guardrails (OWASP ASI), Output Contracts."""
        required = [
            "## When to Use",
            "## Core Rules",
            "## Suggested Process",
            "## Checklist",
            "## Failure Modes",
            "## Output Contracts",
            "## Security Guardrails (OWASP ASI)",
            "## Related Skills",
        ]
        for sec in required:
            self.assertIn(sec, self.text, f"Section '{sec}' missing in SKILL.md")

        # Check checklist items count
        checklist_items = re.findall(r"(?m)^-\s+\[ \]\s+", self.text)
        self.assertGreaterEqual(len(checklist_items), 5, "Checklist must have >= 5 items")

    def test_03_companion_files(self):
        """Verifies agents/openai.yaml and references/chaos-engineering-guide.md exist and are non-empty."""
        openai_path = self.skill_dir / "agents" / "openai.yaml"
        self.assertTrue(openai_path.exists(), f"Missing {openai_path}")
        openai_data = yaml.safe_load(openai_path.read_text(encoding="utf-8"))
        self.assertIn("interface", openai_data)
        self.assertIn("display_name", openai_data["interface"])

        ref_path = self.skill_dir / "references" / "chaos-engineering-guide.md"
        self.assertTrue(ref_path.exists(), f"Missing {ref_path}")
        ref_text = ref_path.read_text(encoding="utf-8")
        self.assertIn("Chaos Mesh", ref_text)
        self.assertIn("LitmusChaos", ref_text)
        self.assertIn("Steady-State Hypothesis", ref_text)

    def test_04_skill_ownership_uniqueness(self):
        """Verifies orchestrate-chaos-experiment has 'sre' as single Primary owner with 0 conflicts."""
        owners: list[str] = []
        for role_file in ROLES_DIR.glob("*.md"):
            role_text = role_file.read_text(encoding="utf-8")
            m = re.search(r"### Primary Skills\s*\n\n(.*?)(?=\n### |\n## )", role_text, re.S)
            if m and "`orchestrate-chaos-experiment`" in m.group(1):
                owners.append(role_file.stem)
        self.assertEqual(owners, ["sre"], f"Expected exactly ['sre'] as Primary owner, got {owners}")


class TestSREAliasResolutionAndRegistrySync(unittest.TestCase):
    """Verify alias mapping, A2A card registry sync, and zero index drift."""

    def test_01_role_aliases_resolve_sre(self):
        """Verifies @sre and @reliability resolve to 'sre'."""
        gen_script = SCRIPTS_DIR / "generate-index.py"
        text = gen_script.read_text(encoding="utf-8")
        self.assertIn('"sre": "sre"', text)
        self.assertIn('"reliability": "sre"', text)

    def test_02_skill_aliases_resolve_chaos(self):
        """Verifies @chaos, @orchestrate_chaos_experiment, @chaos_engineering resolve to ['orchestrate-chaos-experiment']."""
        gen_script = SCRIPTS_DIR / "generate-index.py"
        text = gen_script.read_text(encoding="utf-8")
        self.assertIn('"chaos": ["orchestrate-chaos-experiment"]', text)
        self.assertIn('"orchestrate_chaos_experiment": ["orchestrate-chaos-experiment"]', text)
        self.assertIn('"chaos_engineering": ["orchestrate-chaos-experiment"]', text)

    def test_03_agent_card_structure_and_skills(self):
        """Verifies sre.agent-card.json exists, valid JSON, includes orchestrate-chaos-experiment."""
        card_path = AGENT_CARDS_DIR / "sre.agent-card.json"
        self.assertTrue(card_path.exists(), f"Agent card missing: {card_path}")
        card = json.loads(card_path.read_text(encoding="utf-8"))
        skills = card.get("skills", [])
        skill_ids = [s.get("id") for s in skills if isinstance(s, dict)]
        self.assertIn("orchestrate-chaos-experiment", skill_ids)
        self.assertIn("incident-report", skill_ids)

    def test_04_agent_registry_listing(self):
        """Verifies 'sre' listed in agent-registry.json."""
        reg_path = REGISTRY_DIR / "agent-registry.json"
        self.assertTrue(reg_path.exists(), f"Registry missing: {reg_path}")
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        agents = reg.get("agents", [])
        agent_roles = [a.get("role") or a.get("name") for a in agents if isinstance(a, dict)]
        self.assertIn("sre", agent_roles)

    def test_05_skills_readme_catalog_counts(self):
        """Verifies core/skills/README.md matches disk (124 core, 12 overlays, 136 total; Platform (17))."""
        readme_path = SKILLS_DIR / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8")
        self.assertTrue(re.search(r"\b12[4-9] portable core skills\b", readme_text))
        self.assertTrue(re.search(r"\b13[6-9] total\b", readme_text))
        self.assertTrue(re.search(r"### Platform \((1[7-9]|[2-9]\d)\)", readme_text))
        self.assertIn("- `orchestrate-chaos-experiment`", readme_text)

    def test_06_index_synchronization_zero_drift(self):
        """Verifies generate-index.py --check exits 0."""
        res = subprocess.run(
            [sys.executable, "core/scripts/generate-index.py", "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"Index check reported drift:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
