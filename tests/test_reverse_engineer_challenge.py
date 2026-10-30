#!/usr/bin/env python3
"""Automated Challenge Test Suite for Reverse Engineer Role (Role #39) & SOTA 2026-2027 Standards (Milestone 3).

Validates and stress-tests:
1. Role Invariants:
   - Preamble (Title, Mission, Level, role-standard pointer).
   - Sequence of all 18 mandatory headings matching core/roles/role-standard.md.
   - Minimum item counts per section per validate-roles.py rules.
   - Deliverable routing, role boundaries, and collaboration patterns.
   - 12 architectural guardrail locks.
   - Clean markdown syntax (no tool names leaked in backticks outside code fences).
   - Valid footer format: 'Last updated: YYYY-MM-DD' on the final non-empty line.

2. Review Checklist:
   - Dedicated checklist file exists: core/roles/references/reverse-engineer-review-checklist.md.
   - Proper heading and linkage from reverse-engineer.md.
   - 6 comprehensive technical review sections.
   - Quantitative evaluation formulas (Shannon entropy, blast radius, DBI overhead, FSM coverage, deobfuscation ratio).
   - Verification commands table.

3. Skill Mappings:
   - Primary skill ownership: reverse-engineer-binary owned as Primary in core/skills/security-data/.
   - 9 supporting skills mapped and validated against physical disk.
   - No primary/supporting conflicts across roles.
   - Boundaries do not disclaim primary skills.

4. Registry and Adapters:
   - Registration in adapters/antigravity/role-skill-index.json.
   - All 6 aliases resolve cleanly to reverse-engineer.
   - Bitwise SHA-256 twin parity between adapter and A2A role-skill-index.json.
   - A2A 1.0 agent card validates against JSON Schema Draft 2020-12 with 0 errors.
   - Exactly 39 roles registered in core/a2a/.well-known/agent-registry.json.

5. Policy Boundaries:
   - Policy profile in core/policies/action-boundaries.yaml.
   - 3-tier action permissions (allowed, requires_approval, denied) are mutually exclusive.
   - Zero irreversible actions in allowed.
   - bypass_ai_guardrail explicitly in denied.
   - Tool coupling: write_file and create_file coupled.

6. Contract Compliance:
   - Reverse Engineering Attestation (REA) evidence ledger structure validation.
   - security-audit.json schema validation using jsonschema.Draft202012Validator.
   - Negative mutation testing on contract validation.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import yaml

# Path anchors
REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
REFERENCES_DIR = ROLES_DIR / "references"
SKILLS_DIR = CORE_DIR / "skills"
POLICIES_DIR = CORE_DIR / "policies"
CONTRACTS_DIR = CORE_DIR / "contracts" / "schemas"
A2A_DIR = CORE_DIR / "a2a"
REGISTRY_DIR = A2A_DIR / "registry"
WELL_KNOWN_DIR = A2A_DIR / ".well-known"
ADAPTERS_DIR = REPO_ROOT / "adapters"
SCRIPTS_DIR = CORE_DIR / "scripts"

# Core Invariant Constants
REQUIRED_SECTIONS = (
    "## Principal Expectations",
    "## Use This Role When",
    "## Core Responsibilities",
    "## Inputs Required",
    "## Outputs Produced",
    "## Deliverable Routing",
    "## Decision Boundaries",
    "## Role Boundaries",
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
)

MIN_ITEMS = {
    "## Principal Expectations": 4,
    "## Use This Role When": 3,
    "## Core Responsibilities": 4,
    "## Inputs Required": 4,
    "## Outputs Produced": 4,
    "## Decision Boundaries": 3,
    "## Collaboration": 3,
    "## Guardrails": 3,
    "### Primary Skills": 1,
    "## Review Checklist": 5,
    "## Anti-Patterns To Reject": 4,
    "## Role Handoff": 3,
    "## Definition Of Done": 4,
}

EXPECTED_LOCKS = [
    "BOUNDARY LOCK",
    "DEFENSIVE-SCOPE LOCK",
    "SANDBOX-CONFINEMENT LOCK",
    "AIR-GAP LOCK",
    "SOURCE-CODE-PRESENCE-GUARD LOCK",
    "REA-EVIDENCE-LEDGER LOCK",
    "NO-EXPLOIT-PAYLOAD LOCK",
    "ANTI-TAMPER-BYPASS LOCK",
    "DYNAMIC-INSTRUMENTATION-ISOLATION LOCK",
    "DEOBFUSCATION-AST-INTEGRITY LOCK",
    "EPHEMERAL-DISPOSAL LOCK",
    "IRREVERSIBLE ACTION LOCK",
]

EXPECTED_SUPPORTING_SKILLS = [
    "security-audit",
    "systematic-debugging",
    "skill-preflight-ast-check",
    "supply-chain-security",
    "prompt-injection-defense",
    "review-code",
    "performance-profiling",
    "conduct-research",
    "agent-delegation",
]

EXPECTED_ALIASES = [
    "reverse-engineer",
    "reverse-engineering",
    "re",
    "rev",
    "binary-analyst",
    "malware-analyst",
]

NEVER_ALLOWED = {
    "apply_iac",
    "delete_branch_main",
    "drop_database",
    "drop_storage_volume",
    "force_push",
    "modify_dns_production",
    "modify_secrets",
    "purge_cache_zone",
    "push_to_production",
    "rollback_deployment",
    "rotate_agent_credentials",
    "run_deployment",
    "run_migration",
    "terminate_instance",
}


def load_json(path: Path) -> dict:
    assert path.is_file(), f"Missing JSON file: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict:
    assert path.is_file(), f"Missing YAML file: {path}"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    assert path.is_file(), f"Missing file: {path}"
    return path.read_text(encoding="utf-8")


def strip_fenced_blocks(text: str) -> str:
    """Strip fenced code blocks handling multi-backtick delimiters."""
    lines: list[str] = []
    in_fence = False
    fence_pattern = re.compile(r"^`{3,}")
    for line in text.splitlines():
        if fence_pattern.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def bullet_count(section_text: str) -> int:
    return len(re.findall(r"(?m)^\s*[-*]\s+", section_text))


def extract_section(body: str, heading: str, *, level_aware: bool = True) -> str:
    """Extract text under heading. Level-aware ensures H2 sections encompass H3 subsections,
    and ignores headings located inside fenced code blocks."""
    marker = f"{heading}\n"
    start = body.find(marker)
    if start == -1:
        return ""
    start += len(marker)

    level = len(heading.split(" ", 1)[0]) if level_aware else 2
    lines = body[start:].splitlines(keepends=True)
    in_fence = False
    fence_len = 0
    collected: list[str] = []

    for line in lines:
        stripped = line.strip()
        m = re.match(r"^(`{3,})", stripped)
        if m:
            flen = len(m.group(1))
            if not in_fence:
                in_fence = True
                fence_len = flen
            elif flen >= fence_len:
                in_fence = False
                fence_len = 0
            collected.append(line)
            continue

        if not in_fence:
            hm = re.match(rf"^#{{2,{level}}} .+", stripped)
            if hm:
                break
        collected.append(line)

    return "".join(collected)


# ==============================================================================
# 1. ROLE STRUCTURAL INVARIANTS
# ==============================================================================

class TestReverseEngineerRoleInvariants(unittest.TestCase):
    """Test suite validating structural invariants and content standards of reverse-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "reverse-engineer.md"
        assert cls.role_path.is_file(), "core/roles/reverse-engineer.md must exist"
        cls.content = cls.role_path.read_text(encoding="utf-8")
        cls.clean_content = strip_fenced_blocks(cls.content)

    def test_01_preamble_structure(self):
        """Preamble must contain exact Title, Mission, Level, and role-standard link."""
        lines = [line.strip() for line in self.content.splitlines() if line.strip()]
        self.assertEqual(lines[0], "# Reverse Engineer", "First heading must be '# Reverse Engineer'")
        self.assertTrue(lines[1].startswith("Mission:"), "Second non-empty line must start with 'Mission:'")
        self.assertIn("Deconstruct compiled binaries", lines[1])
        self.assertTrue(lines[2].startswith("Level:"), "Third non-empty line must start with 'Level:'")
        self.assertIn("Principal", lines[2])
        self.assertEqual(
            lines[3],
            "This role must follow [role-standard](role-standard.md) first.",
            "Mandatory pointer to role-standard.md missing or malformed",
        )

    def test_02_all_18_mandatory_headings_in_order(self):
        """reverse-engineer.md must contain all 18 mandatory sections in exact sequence."""
        last_pos = -1
        for section in REQUIRED_SECTIONS:
            pos = self.content.find(section)
            self.assertNotEqual(pos, -1, f"Missing required section heading: '{section}'")
            self.assertGreater(pos, last_pos, f"Section out of order: '{section}'")
            last_pos = pos

    def test_03_minimum_item_counts_per_section(self):
        """All bulleted sections must meet or exceed minimum item counts."""
        for section, min_count in MIN_ITEMS.items():
            sect_text = extract_section(self.clean_content, section, level_aware=True)
            count = bullet_count(sect_text)
            self.assertGreaterEqual(
                count,
                min_count,
                f"Section '{section}' has {count} items; expected >= {min_count}",
            )

    def test_04_deliverable_routing_and_role_boundaries_tables(self):
        """Deliverable Routing and Role Boundaries tables must exist with correct columns and entries."""
        # Deliverable Routing
        routing_text = extract_section(self.content, "## Deliverable Routing", level_aware=True)
        self.assertIn("| Situation | Primary deliverable | Notes |", routing_text)
        self.assertIn("Binary vulnerability audit", routing_text)
        self.assertIn("Protocol reverse engineering", routing_text)
        self.assertIn("Malware or suspicious binary triage", routing_text)

        # Role Boundaries
        boundaries_text = extract_section(self.content, "## Role Boundaries", level_aware=True)
        self.assertIn("| Role | Owns | Does not own |", boundaries_text)
        self.assertIn("**Reverse Engineer**", boundaries_text)
        self.assertIn("**Security Engineer**", boundaries_text)
        self.assertIn("**Backend Developer**", boundaries_text)
        self.assertIn("**QA Engineer**", boundaries_text)

        # Collaboration
        collab_text = extract_section(self.content, "## Collaboration", level_aware=True)
        self.assertIn("Security Engineer", collab_text)
        self.assertIn("agent-delegation", collab_text)

    def test_05_guardrail_locks_enumeration(self):
        """reverse-engineer.md must define the 12 explicit SOTA reverse engineering locks."""
        locks_found = re.findall(r"\*\*([A-Z0-9_ -]+LOCK)\*\*", self.content)
        self.assertGreaterEqual(len(locks_found), 12, f"Found {len(locks_found)} locks; expected >= 12")
        self.assertLessEqual(len(locks_found), 24, f"Found {len(locks_found)} locks; expected <= 24")
        for lock in EXPECTED_LOCKS:
            self.assertIn(f"**{lock}**", self.content, f"Missing expected guardrail lock: **{lock}**")

    def test_06_markdown_clean_syntax_and_no_backtick_tool_leakage(self):
        """Real-world tool names must not be backticked outside code fences."""
        raw_backticks = re.findall(r"`([^`\n]+)`", self.clean_content)
        forbidden_tool_backticks = [
            "Ghidra", "IDA Pro", "Frida", "Wireshark", "TShark",
            "radare2", "rizin", "Jadx", "APKTool", "bpftrace", "angr", "Z3"
        ]
        for tool in forbidden_tool_backticks:
            self.assertNotIn(
                tool,
                raw_backticks,
                f"External tool '{tool}' must not be backticked outside code blocks",
            )
        # Template fenced block test
        template_text = extract_section(self.content, "## Output Template", level_aware=True)
        self.assertIn("```markdown", template_text, "Output template must contain fenced ```markdown block")

    def test_07_footer_timestamp_exact_format(self):
        """File must terminate with a valid 'Last updated: YYYY-MM-DD' footer."""
        non_empty = [line.strip() for line in self.content.splitlines() if line.strip()]
        self.assertTrue(non_empty, "File must not be empty")
        last_line = non_empty[-1]
        self.assertTrue(
            bool(re.match(r"^Last updated: \d{4}-\d{2}-\d{2}$", last_line)),
            f"Final line is '{last_line}'; expected 'Last updated: YYYY-MM-DD'",
        )


# ==============================================================================
# 2. REVIEW CHECKLIST VERIFICATION
# ==============================================================================

class TestReverseEngineerReviewChecklist(unittest.TestCase):
    """Test suite verifying the dedicated reverse-engineer review checklist."""

    @classmethod
    def setUpClass(cls):
        cls.chk_path = REFERENCES_DIR / "reverse-engineer-review-checklist.md"
        assert cls.chk_path.is_file(), "core/roles/references/reverse-engineer-review-checklist.md must exist"
        cls.content = cls.chk_path.read_text(encoding="utf-8")

    def test_08_checklist_heading_and_role_link(self):
        """Checklist title must match role and be linked from reverse-engineer.md."""
        first_line = [l.strip() for l in self.content.splitlines() if l.strip()][0]
        self.assertTrue(
            first_line.startswith("# Reverse Engineer Review Checklist") or
            first_line.startswith("## Reverse Engineer Review Checklist"),
            f"Unexpected checklist heading: {first_line}",
        )
        role_text = read_text(ROLES_DIR / "reverse-engineer.md")
        self.assertIn("references/reverse-engineer-review-checklist.md", role_text)

    def test_09_all_six_technical_review_sections_present(self):
        """Checklist must include all 6 technical verification gates."""
        expected_sections = [
            "### 1. Air-Gapped Sandbox Confinement & Isolation Integrity",
            "### 2. Multi-Architecture Binary Triage & Static Decompilation",
            "### 3. Dynamic Binary Instrumentation & Non-Invasive Kernel Tracing",
            "### 4. Protocol Reverse Engineering & Wire Format Reconstruction",
            "### 5. Control Flow Deobfuscation & Symbolic Program Analysis",
            "### 6. Defect Classification, REA Evidence Ledger & Defensive Ethics",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.content, f"Missing checklist section: {sec}")

    def test_10_quantitative_evaluation_formulas(self):
        """Checklist must embed quantitative metrics and mathematical standards."""
        # Shannon Entropy
        self.assertIn("Shannon Entropy", self.content)
        self.assertIn("7.2", self.content)
        # Blast Radius
        self.assertIn("Blast Radius", self.content)
        self.assertIn("= 0", self.content)
        # DBI Overhead Factor
        self.assertIn("DBI Overhead Factor", self.content)
        self.assertIn("5.0", self.content)
        # Protocol State Coverage
        self.assertIn("Protocol State Coverage", self.content)
        self.assertIn("0.85", self.content)
        # Deobfuscation Ratio
        self.assertIn("Deobfuscation Ratio", self.content)
        self.assertIn("0.60", self.content)

    def test_11_verification_commands_table(self):
        """Checklist must include verification commands table with expected validation tools."""
        self.assertIn("| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |", self.content)
        self.assertIn("docker inspect", self.content)
        self.assertIn("rabin2 -S", self.content)
        self.assertIn("validate-contracts.py", self.content)


# ==============================================================================
# 3. SKILL MAPPINGS & OWNERSHIP
# ==============================================================================

class TestReverseEngineerSkillMappings(unittest.TestCase):
    """Test suite validating primary/supporting skill taxonomy and ownership invariants."""

    @classmethod
    def setUpClass(cls):
        cls.role_content = read_text(ROLES_DIR / "reverse-engineer.md")

    def test_12_primary_skill_ownership_and_disk_structure(self):
        """reverse-engineer-binary must be owned as Primary and conform to skill standards."""
        skill_path = SKILLS_DIR / "security-data" / "reverse-engineer-binary" / "SKILL.md"
        self.assertTrue(skill_path.is_file(), f"Missing primary skill at {skill_path}")

        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, f"SKILL.md too long: {len(lines)} lines (max 200)")

        # Validate frontmatter
        self.assertTrue(lines[0].startswith("---"))
        self.assertIn("name: reverse-engineer-binary", content)
        self.assertIn("allowed-tools:", content)

        # Validate required sections
        self.assertIn("## When to Use", content)
        self.assertIn("## Core Rules", content)
        self.assertIn("## Suggested Process", content)
        self.assertIn("## Output Format", content)
        self.assertIn("## Failure Modes", content)
        self.assertIn("## Output Contracts", content)

    def test_13_all_nine_supporting_skills_exist_on_disk(self):
        """All 9 declared supporting skills must exist physically in core/skills/."""
        sup_text = extract_section(self.role_content, "### Supporting Skills (use when collaborating)", level_aware=True)
        declared_skills = re.findall(r"(?m)^- `([a-z0-9-]+)`", sup_text)
        self.assertEqual(len(declared_skills), 9, f"Expected 9 supporting skills, found {len(declared_skills)}")

        for skill in EXPECTED_SUPPORTING_SKILLS:
            self.assertIn(skill, declared_skills, f"Missing expected supporting skill: {skill}")
            matches = list(SKILLS_DIR.glob(f"*/*/{skill}/SKILL.md")) + list(SKILLS_DIR.glob(f"*/{skill}/SKILL.md"))
            self.assertTrue(len(matches) > 0, f"Supporting skill '{skill}' does not exist on disk")

    def test_14_no_primary_supporting_conflicts(self):
        """Primary and supporting skills for reverse-engineer must be mutually exclusive."""
        prim_text = extract_section(self.role_content, "### Primary Skills", level_aware=True)
        sup_text = extract_section(self.role_content, "### Supporting Skills (use when collaborating)", level_aware=True)
        primary = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", prim_text))
        supporting = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", sup_text))

        self.assertEqual(primary, {"reverse-engineer-binary"})
        self.assertEqual(primary & supporting, set(), "Primary and Supporting skills overlap")

    def test_15_boundaries_do_not_disclaim_primary_skill(self):
        """Role boundaries must not disclaim primary skill responsibilities."""
        boundaries = extract_section(self.role_content, "## Decision Boundaries", level_aware=True) + extract_section(self.role_content, "## Role Boundaries", level_aware=True)
        self.assertNotIn("does not reverse engineer", boundaries.lower())
        self.assertNotIn("does not analyze binaries", boundaries.lower())


# ==============================================================================
# 4. REGISTRY, ADAPTERS & DISCOVERY INTEGRATION
# ==============================================================================

class TestReverseEngineerRegistryAndAdapters(unittest.TestCase):
    """Test suite validating Antigravity adapters, A2A registry, and alias mappings."""

    def test_16_antigravity_adapter_registration(self):
        """reverse-engineer must be registered in adapters/antigravity/role-skill-index.json."""
        adapter_index = load_json(ADAPTERS_DIR / "antigravity" / "role-skill-index.json")
        roles = adapter_index.get("roles", {})
        self.assertIn("reverse-engineer", roles, "reverse-engineer missing from adapter role-skill-index.json")

        entry = roles["reverse-engineer"]
        self.assertEqual(entry.get("primary_skills"), ["reverse-engineer-binary"])
        self.assertIn("reverse-engineer-binary", entry.get("skills", []))
        self.assertEqual(len(entry.get("supporting_skills", [])), 9)

    def test_17_all_six_aliases_resolve_cleanly(self):
        """All 6 reverse engineer aliases must resolve to reverse-engineer."""
        adapter_index = load_json(ADAPTERS_DIR / "antigravity" / "role-skill-index.json")
        aliases = adapter_index.get("role_aliases", {})
        for alias in EXPECTED_ALIASES:
            self.assertIn(alias, aliases, f"Alias '{alias}' not found in role_aliases")
            self.assertEqual(
                aliases[alias],
                "reverse-engineer",
                f"Alias '{alias}' mapped to '{aliases[alias]}'; expected 'reverse-engineer'",
            )

    def test_18_twin_index_sha256_bitwise_parity(self):
        """adapters/antigravity/role-skill-index.json and core/a2a/.well-known/role-skill-index.json must be bitwise identical."""
        adapter_path = ADAPTERS_DIR / "antigravity" / "role-skill-index.json"
        a2a_path = WELL_KNOWN_DIR / "role-skill-index.json"

        hash_adapter = hashlib.sha256(adapter_path.read_bytes()).hexdigest()
        hash_a2a = hashlib.sha256(a2a_path.read_bytes()).hexdigest()

        self.assertEqual(
            hash_adapter,
            hash_a2a,
            "Twin parity violation: adapter and A2A role-skill-index.json SHA-256 hashes differ",
        )

    def test_19_a2a_agent_card_schema_conformance(self):
        """reverse-engineer.agent-card.json must validate cleanly against agent-card.json schema."""
        schema = load_json(CONTRACTS_DIR / "agent-card.json")
        card = load_json(REGISTRY_DIR / "reverse-engineer.agent-card.json")

        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(card))
        self.assertEqual(len(errors), 0, f"agent-card.json validation errors: {[e.message for e in errors]}")

        self.assertEqual(card.get("protocol_version"), "1.0")
        self.assertEqual(card.get("version"), "5.7.2")
        skill_ids = [s["id"] for s in card.get("skills", [])]
        self.assertIn("reverse-engineer-binary", skill_ids)
        self.assertIn("security-audit.json", card.get("defaultOutputSchemas", []))
        self.assertIn("api-contract-spec.json", card.get("defaultOutputSchemas", []))

    def test_20_agent_registry_catalog_count(self):
        """core/a2a/.well-known/agent-registry.json must contain exactly 39 registered agents."""
        registry = load_json(WELL_KNOWN_DIR / "agent-registry.json")
        agents = registry.get("agents", [])
        self.assertEqual(len(agents), 39, f"agent-registry.json contains {len(agents)} agents; expected 39")

        re_entries = [a for a in agents if a.get("role") == "reverse-engineer"]
        self.assertEqual(len(re_entries), 1, "reverse-engineer must appear exactly once in agent-registry.json")
        self.assertEqual(
            re_entries[0].get("agent_card"),
            "core/a2a/registry/reverse-engineer.agent-card.json",
        )


# ==============================================================================
# 5. POLICY BOUNDARIES & ACTION PERMISSIONS
# ==============================================================================

class TestReverseEngineerPolicyBoundaries(unittest.TestCase):
    """Test suite validating action boundaries policy rules and safety tiers."""

    @classmethod
    def setUpClass(cls):
        cls.policy = load_yaml(POLICIES_DIR / "action-boundaries.yaml")
        cls.profile = cls.policy.get("roles", {}).get("reverse-engineer")
        assert cls.profile is not None, "reverse-engineer profile missing from action-boundaries.yaml"
        cls.allowed = set(cls.profile.get("allowed", []))
        cls.requires_approval = set(cls.profile.get("requires_approval", []))
        cls.denied = set(cls.profile.get("denied", []))

    def test_21_three_tiers_mutually_exclusive(self):
        """allowed, requires_approval, and denied tiers must have zero pairwise overlap."""
        self.assertGreater(len(self.allowed), 0, "allowed list must not be empty")
        self.assertGreater(len(self.requires_approval), 0, "requires_approval list must not be empty")
        self.assertGreater(len(self.denied), 0, "denied list must not be empty")

        self.assertEqual(self.allowed & self.requires_approval, set(), "allowed and requires_approval overlap")
        self.assertEqual(self.allowed & self.denied, set(), "allowed and denied overlap")
        self.assertEqual(self.requires_approval & self.denied, set(), "requires_approval and denied overlap")

    def test_22_zero_irreversible_actions_in_allowed(self):
        """None of the universally irreversible actions may be in allowed."""
        overlap = self.allowed & NEVER_ALLOWED
        self.assertEqual(overlap, set(), f"Irreversible actions found in allowed: {overlap}")

    def test_23_ai_guardrail_bypass_denied(self):
        """bypass_ai_guardrail must be explicitly denied."""
        self.assertIn("bypass_ai_guardrail", self.denied)
        self.assertNotIn("bypass_ai_guardrail", self.allowed)
        self.assertNotIn("bypass_ai_guardrail", self.requires_approval)

    def test_24_tool_coupling_file_creation_and_write(self):
        """write_file and create_file must be consistently coupled."""
        if "write_file" in self.allowed:
            self.assertIn("create_file", self.allowed, "write_file is allowed but create_file is not")
        self.assertEqual(
            "write_file" in self.allowed,
            "create_file" in self.allowed,
            "write_file and create_file must reside in the same permission tier",
        )


# ==============================================================================
# 6. CONTRACT COMPLIANCE & REA EVIDENCE LEDGER
# ==============================================================================

class TestReverseEngineerContractCompliance(unittest.TestCase):
    """Test suite validating REA ledger templates and security-audit.json contract schemas."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "security-audit.json"
        assert cls.schema_path.is_file(), "security-audit.json must exist"
        cls.schema = load_json(cls.schema_path)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        cls.role_content = read_text(ROLES_DIR / "reverse-engineer.md")

    def test_25_rea_evidence_ledger_structure(self):
        """Output template must define all mandatory Reverse Engineering Artifact sections."""
        template_text = extract_section(self.role_content, "## Output Template", level_aware=True)
        required_rea_headers = [
            "## Artifact Identification",
            "## Execution Environment & Provenance",
            "## Static Attack Surface & Imports",
            "## Decompilation & Control Flow Analysis",
            "## Vulnerability & Defect Matrix",
            "## Interface Specification (Reconstructed)",
            "## Defensive Recommendations",
        ]
        for header in required_rea_headers:
            self.assertIn(header, template_text, f"REA Output Template missing section: {header}")

    def test_26_bundled_security_audit_examples_validate(self):
        """All bundled examples in security-audit.json must validate without errors."""
        examples = self.schema.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include bundled examples")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(len(errors), 0, f"Bundled example {idx} invalid: {[e.message for e in errors]}")

    def test_27_synthetic_rea_vulnerability_payload_validates(self):
        """A synthetic REA vulnerability report conforming to reverse engineer output must validate."""
        synthetic_rea_finding = {
            "contract_type": "security-audit",
            "target": "closed_source_libcrypto.so.1.0",
            "audit_type": "code_review",
            "findings": [
                {
                    "vulnerability": "Stack buffer overflow in parse_header",
                    "severity": "high",
                    "cwe_id": "CWE-120",
                    "description": "Unchecked memcpy at 0x00401A20 into a 64-byte stack buffer allows control flow hijacking",
                    "exploit_path": "crafted network packet -> parse_header -> unbounded copy -> RIP overwrite",
                    "blast_radius": "remote code execution in sandboxed daemon process",
                    "owasp_ref": "ASI05:2026",
                    "status": "open",
                    "remediation": "Replace memcpy with bounds-checked copy or clamp header length"
                }
            ],
            "compliance_violations": [],
            "overall_risk_score": "high",
            "owasp_baseline": "2025",
            "asi_review": {
                "asi_items_checked": ["ASI05", "ASI06"],
                "mcp_servers_pinned": True,
                "max_blast_radius": "sandboxed microVM memory space"
            }
        }
        errors = list(self.validator.iter_errors(synthetic_rea_finding))
        self.assertEqual(len(errors), 0, f"Synthetic REA contract failed validation: {[e.message for e in errors]}")

    def test_28_negative_mutation_missing_required_fields_rejected(self):
        """Mutations omitting mandatory contract fields must be rejected by validator."""
        base_payload = {
            "contract_type": "security-audit",
            "target": "firmware_blob.bin",
            "audit_type": "code_review",
            "findings": [],
            "overall_risk_score": "pass"
        }
        # Baseline must pass
        self.assertEqual(len(list(self.validator.iter_errors(base_payload))), 0)

        # Mutate: missing contract_type
        mutant = copy.deepcopy(base_payload)
        del mutant["contract_type"]
        self.assertGreater(len(list(self.validator.iter_errors(mutant))), 0)

        # Mutate: missing target
        mutant = copy.deepcopy(base_payload)
        del mutant["target"]
        self.assertGreater(len(list(self.validator.iter_errors(mutant))), 0)

        # Mutate: invalid severity enum
        mutant = copy.deepcopy(base_payload)
        mutant["findings"] = [{
            "vulnerability": "test",
            "severity": "catastrophic",  # invalid enum
            "description": "desc",
            "remediation": "fix"
        }]
        self.assertGreater(len(list(self.validator.iter_errors(mutant))), 0)


if __name__ == "__main__":
    unittest.main()
