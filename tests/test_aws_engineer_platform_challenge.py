#!/usr/bin/env python3
"""Automated Challenge Test Suite for AWS Engineer Role & Cloud Architecture Standards.

Validates and stress-tests:
1. AWS Infrastructure Specification Schema (`core/contracts/schemas/aws-infra-spec.json`):
   - JSON Schema Draft 2020-12 meta-schema compliance.
   - Full validity of bundled examples.
   - Modern 2026-2027 cloud architecture properties:
     `resource_map`, `iam_roles`, `cost_attribution`, `monitoring_config`, `iac_reference`.
   - Adversarial negative mutation testing:
     - Missing mandatory root fields.
     - Invalid `contract_type` discriminator.
     - Invalid `aws_account` pattern (must be 12 digits).
     - Invalid `spec_id` UUID format.
     - Missing required fields in `resource_map` (vpc_id, private_subnet_ids).
     - Missing required fields in `iam_roles` items (role_name, role_arn, service_principal).
     - Missing required fields in `cost_attribution` (team, service, environment, cost_center).

2. AWS Engineer Role (`core/roles/aws-engineer.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Use This Role When,
     Core Responsibilities, Inputs Required, Outputs Produced, Deliverable Routing,
     Decision Boundaries, Role Boundaries, Collaboration, Guardrails, Skill Toolbox,
     Output Template, Review Checklist, Failure Modes, Anti-Patterns To Reject,
     Role Handoff, Definition Of Done.
   - The 4+ Mandatory Architectural Guardrail Locks:
     `OPENTOFU-KMS-LOCK`, `CROSSPLANE-COMPOSITION-LOCK`, `BOTTLEROCKET-LOCK`, `AWS-IAM-ZERO-TRUST-LOCK`.
   - Supplementary SOTA locks: `KARPENTER-AUTOSCALING-LOCK`, `VPC-LATTICE-LOCK`,
     `GRAVITON4-FIRST-LOCK`, `BEDROCK-ISOLATION-LOCK`, `FINOPS-LOCK`, `GITOPS-LOCK`.
   - Core locks: `BOUNDARY LOCK`, `SECURITY LOCK`, `IRREVERSIBLE ACTION LOCK`, `TRACE LOCK`, `UNCERTAINTY LOCK`.
   - Clear boundary and handoff contract with `devops-engineer`.
   - Primary skills locked: `aws-infrastructure`, `setup-deployment`, `add-telemetry-instrumentation`.
   - Footer date: `Last updated: 2026-10-05`.

3. AWS Engineer Review Checklist (`core/roles/references/aws-engineer-review-checklist.md`):
   - All 14 SOTA verification sections.
   - Precision technical keywords: `OpenTofu`, `KMS`, `Crossplane`, `Bottlerocket`,
     `dm-verity`, `SELinux`, `Control Tower`, `IAM Identity Center`, `Pod Identity`,
     `Karpenter`, `Graviton4`, `Trainium2`, `Inferentia2`, `VPC Lattice`, `Bedrock Guardrails`,
     `aws-infra-spec.json`.

4. AWS Infrastructure Primary Skill (`core/skills/platform/aws-infrastructure/`):
   - `SKILL.md` frontmatter, allowed-tools, line count (< 200 lines).
   - Required H2 sections: `## When to Use`, `## Core Rules`, `## Suggested Process`,
     `## Checklist`, `## Related Skills`.
   - Strict adherence to core locks and modern cloud invariants.

5. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/aws-engineer.agent-card.json` structure, skills list, and default output schemas.
   - Agent discovery in `agent-registry.json`.
   - Role-skill mapping and fast invocation aliases (@aws, @cloud, aws_infra, aws_infrastructure)
     in both core and adapter `role-skill-index.json`.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
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
ADAPTERS_DIR = REPO_ROOT / "adapters"


class TestAWSInfrastructureSkillAndSchema(unittest.TestCase):
    """Rigorous schema validation, negative mutation testing, and skill specification conformance."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "aws-infra-spec.json"
        assert cls.schema_path.exists(), "aws-infra-spec.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw, format_checker=Draft202012Validator.FORMAT_CHECKER)

        cls.skill_path = SKILLS_DIR / "platform" / "aws-infrastructure" / "SKILL.md"
        assert cls.skill_path.exists(), "aws-infrastructure/SKILL.md must exist"
        cls.skill_content = cls.skill_path.read_text(encoding="utf-8")

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "pack://agent-skills/core/contracts/schemas/aws-infra-spec.json")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within aws-infra-spec.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_modern_cloud_properties_present(self):
        """Schema must define all 2026-2027 modern cloud infrastructure properties."""
        props = self.schema_raw.get("properties", {})
        modern_props = [
            "contract_type",
            "spec_id",
            "system_name",
            "aws_account",
            "region",
            "resource_map",
            "iam_roles",
            "cost_attribution",
            "monitoring_config",
            "iac_reference",
        ]
        for prop in modern_props:
            self.assertIn(prop, props, f"Missing property in aws-infra-spec.json: {prop}")

    def test_04_negative_mutation_missing_required_fields(self):
        """Omitting mandatory root fields must fail schema validation."""
        valid_example = copy.deepcopy(self.schema_raw["examples"][0])
        required_fields = self.schema_raw.get("required", [])
        for field in required_fields:
            mutant = copy.deepcopy(valid_example)
            del mutant[field]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(
                len(errors),
                0,
                f"Validator failed to reject missing required field: {field}",
            )

    def test_05_negative_mutation_invalid_contract_type(self):
        """Invalid contract_type discriminator must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["contract_type"] = "invalid-contract-type"
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject invalid contract_type")

    def test_06_negative_mutation_invalid_aws_account_pattern(self):
        """AWS account ID not matching 12-digit pattern must fail validation."""
        for invalid_acct in ["12345", "1234567890123", "abcdefghijkl", "1234-5678-9012"]:
            mutant = copy.deepcopy(self.schema_raw["examples"][0])
            mutant["aws_account"] = invalid_acct
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, f"Validator failed to reject invalid aws_account: {invalid_acct}")

    def test_07_negative_mutation_invalid_spec_id_uuid(self):
        """Non-UUID spec_id must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["spec_id"] = "not-a-valid-uuid"
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject invalid spec_id")

    def test_08_negative_mutation_invalid_resource_map(self):
        """resource_map missing required fields (vpc_id, private_subnet_ids) must fail."""
        for req in ["vpc_id", "private_subnet_ids"]:
            mutant = copy.deepcopy(self.schema_raw["examples"][0])
            del mutant["resource_map"][req]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, f"Validator failed to reject missing resource_map field: {req}")

    def test_09_negative_mutation_invalid_iam_roles_item(self):
        """iam_roles item missing required fields must fail."""
        for req in ["role_name", "role_arn", "service_principal"]:
            mutant = copy.deepcopy(self.schema_raw["examples"][0])
            del mutant["iam_roles"][0][req]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, f"Validator failed to reject missing iam_roles item field: {req}")

    def test_10_negative_mutation_invalid_cost_attribution(self):
        """cost_attribution missing mandatory FinOps tags must fail."""
        for req in ["team", "service", "environment", "cost_center"]:
            mutant = copy.deepcopy(self.schema_raw["examples"][0])
            del mutant["cost_attribution"][req]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, f"Validator failed to reject missing cost_attribution tag: {req}")

    def test_11_aws_infrastructure_skill_validity(self):
        """aws-infrastructure SKILL.md must be concise (<200 lines), valid frontmatter, and contain required H2 sections."""
        lines = self.skill_content.splitlines()
        self.assertLess(len(lines), 200, f"SKILL.md must be < 200 lines, got {len(lines)}")
        self.assertTrue(self.skill_content.startswith("---"), "Must start with YAML frontmatter")

        parts = self.skill_content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        self.assertEqual(meta.get("name"), "aws-infrastructure")
        self.assertIn("allowed-tools", meta)

        required_h2 = [
            "## When to Use",
            "## Core Rules",
            "## Suggested Process",
            "## Checklist",
            "## Related Skills",
        ]
        for h2 in required_h2:
            self.assertIn(h2, self.skill_content, f"Missing required H2 section: {h2}")

        locks = [
            "OPENTOFU-KMS-LOCK",
            "CROSSPLANE-COMPOSITION-LOCK",
            "BOTTLEROCKET-LOCK",
            "AWS-IAM-ZERO-TRUST-LOCK",
            "KARPENTER-AUTOSCALING-LOCK",
            "GRAVITON4-FIRST-LOCK",
            "VPC-LATTICE-LOCK",
            "BEDROCK-ISOLATION-LOCK",
            "FINOPS-LOCK",
            "GITOPS-LOCK",
        ]
        for lock in locks:
            self.assertIn(lock, self.skill_content, f"Missing lock in SKILL.md: {lock}")


class TestAWSEngineerRoleInvariants(unittest.TestCase):
    """Authoritative invariant testing for core/roles/aws-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "aws-engineer.md"
        assert cls.role_path.exists(), "aws-engineer.md must exist"
        cls.role_content = cls.role_path.read_text(encoding="utf-8")

    def test_01_standard_role_sections(self):
        """Role must contain all 19 standard sections per role-standard.md."""
        sections = [
            "# AWS Engineer",
            "Mission:",
            "Level:",
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
            "## Output Template",
            "## Review Checklist",
            "## Failure Modes",
            "## Anti-Patterns To Reject",
            "## Role Handoff",
            "## Definition Of Done",
        ]
        for sec in sections:
            self.assertIn(sec, self.role_content, f"Missing required role section: {sec}")

    def test_02_mandatory_sota_locks_present(self):
        """Role must enforce the 4+ mandatory SOTA 2026-2027 Architectural Guardrail Locks."""
        mandatory_locks = [
            "OPENTOFU-KMS-LOCK",
            "CROSSPLANE-COMPOSITION-LOCK",
            "BOTTLEROCKET-LOCK",
            "AWS-IAM-ZERO-TRUST-LOCK",
        ]
        for lock in mandatory_locks:
            self.assertIn(lock, self.role_content, f"Missing mandatory SOTA lock: {lock}")

    def test_03_supplementary_and_core_locks_present(self):
        """Role must enforce supplementary and core guardrail locks."""
        expected_locks = [
            "KARPENTER-AUTOSCALING-LOCK",
            "VPC-LATTICE-LOCK",
            "GRAVITON4-FIRST-LOCK",
            "BEDROCK-ISOLATION-LOCK",
            "FINOPS-LOCK",
            "GITOPS-LOCK",
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "TRACE LOCK",
            "UNCERTAINTY LOCK",
        ]
        for lock in expected_locks:
            self.assertIn(lock, self.role_content, f"Missing guardrail lock: {lock}")

    def test_04_boundary_and_handoff_with_devops_engineer(self):
        """Role must explicitly define boundaries and handoff contract with devops-engineer."""
        terms = [
            "DevOps Engineer",
            "aws-infra-spec.json",
            "deployment-plan.json",
            "ArgoCD",
            "GitOps",
        ]
        for term in terms:
            self.assertIn(term, self.role_content, f"Missing DevOps handoff term: {term}")

    def test_05_primary_skills_locked(self):
        """Primary skills toolbox must contain core AWS engineering skills."""
        expected_skills = [
            "`aws-infrastructure`",
            "`setup-deployment`",
            "`add-telemetry-instrumentation`",
        ]
        for skill in expected_skills:
            self.assertIn(skill, self.role_content, f"Missing primary skill in toolbox: {skill}")

    def test_06_footer_maintenance_date(self):
        """Role must have authoritative maintenance date: Last updated: 2026-10-05."""
        self.assertIn("Last updated: 2026-10-05", self.role_content)


class TestAWSEngineerReviewChecklist(unittest.TestCase):
    """Invariant testing for core/roles/references/aws-engineer-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "aws-engineer-review-checklist.md"
        assert cls.checklist_path.exists(), "aws-engineer-review-checklist.md must exist"
        cls.checklist_content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_14_sections_present(self):
        """Checklist must contain all 14 comprehensive SOTA verification sections."""
        expected_sections = [
            "### 1. OpenTofu v1.8+ Client-Side State Encryption & IaC Architecture (`OPENTOFU-KMS-LOCK`)",
            "### 2. Universal Cloud Control Planes & Crossplane v1.16+ Go Compositions (`CROSSPLANE-COMPOSITION-LOCK`)",
            "### 3. Bottlerocket Distroless Node OS & EKS Host Security (`BOTTLEROCKET-LOCK`)",
            "### 4. AWS IAM Zero-Trust, Identity Center & Access Governance (`AWS-IAM-ZERO-TRUST-LOCK`)",
            "### 5. AWS EKS Pod Identity (v1.31+) & Workload Credential Federation",
            "### 6. Karpenter v1.0+ Declarative Autoscaling & Compute Architecture",
            "### 7. Graviton4, Trainium2 & Inferentia2 Compute Acceleration",
            "### 8. Sidecarless Service Networking with AWS VPC Lattice (Gateway API)",
            "### 9. Enterprise Multi-Account Architecture, Control Tower & SCP Guardrails",
            "### 10. Cloud Storage, Database Resiliency & KMS Encryption at Rest",
            "### 11. Amazon Bedrock & AI/ML Managed Infrastructure Isolation",
            "### 12. AWS FinOps Engineering & Cost Attribution Governance",
            "### 13. Cloud-Native Observability, Telemetry & AWS Config Compliance",
            "### 14. Machine Contract Artifacts & DevOps Handoff (`aws-infra-spec.json`)",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.checklist_content, f"Missing checklist section: {sec}")

    def test_02_technical_depth_keywords_present(self):
        """Checklist must contain all mandatory technical depth keywords."""
        keywords = [
            "OpenTofu",
            "KMS",
            "Crossplane",
            "Bottlerocket",
            "dm-verity",
            "SELinux",
            "Control Tower",
            "IAM Identity Center",
            "Pod Identity",
            "Karpenter",
            "Graviton4",
            "Trainium2",
            "Inferentia2",
            "VPC Lattice",
            "Bedrock",
            "Guardrails v2",
            "aws-infra-spec.json",
            "PrivateLink",
            "AFT",
            "ADOT",
        ]
        for kw in keywords:
            self.assertIn(kw, self.checklist_content, f"Missing technical keyword in checklist: {kw}")


class TestAWSEngineerAgentCardAndRegistry(unittest.TestCase):
    """Validation of A2A Agent Card, Discovery Registry, and Alias Resolution."""

    @classmethod
    def setUpClass(cls):
        cls.agent_card_path = AGENT_CARDS_DIR / "aws-engineer.agent-card.json"
        assert cls.agent_card_path.exists(), "aws-engineer.agent-card.json must exist"
        cls.agent_card = json.loads(cls.agent_card_path.read_text(encoding="utf-8"))

    def test_01_agent_card_structure(self):
        """Agent card must have correct id, contract_type, name, and output schemas."""
        self.assertEqual(self.agent_card.get("contract_type"), "agent-card")
        self.assertEqual(self.agent_card.get("name"), "aws-engineer")
        self.assertEqual(self.agent_card.get("id"), "pack://agent-skills/core/roles/aws-engineer")
        output_schemas = self.agent_card.get("defaultOutputSchemas", [])
        self.assertIn("aws-infra-spec.json", output_schemas)

    def test_02_agent_card_skills_exposure(self):
        """Agent card must expose aws-infrastructure, setup-deployment, and add-telemetry-instrumentation."""
        card_skills = [s.get("id") for s in self.agent_card.get("skills", [])]
        expected_skills = [
            "aws-infrastructure",
            "setup-deployment",
            "add-telemetry-instrumentation",
        ]
        for exp in expected_skills:
            self.assertIn(exp, card_skills, f"Missing skill in agent card: {exp}")

    def test_03_agent_registry_listing(self):
        """aws-engineer must be listed in agent-registry.json."""
        registry_path = REGISTRY_DIR / "agent-registry.json"
        self.assertTrue(registry_path.exists(), "agent-registry.json must exist")
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        agent_roles = [a.get("role") for a in reg.get("agents", [])]
        self.assertIn("aws-engineer", agent_roles, "aws-engineer must be listed in agent-registry.json")

    def test_04_role_skill_index_mapping(self):
        """role-skill-index.json must map aws-engineer to its primary skills in core and adapter."""
        for path in [REGISTRY_DIR / "role-skill-index.json", ADAPTERS_DIR / "antigravity" / "role-skill-index.json"]:
            self.assertTrue(path.exists(), f"{path} must exist")
            idx = json.loads(path.read_text(encoding="utf-8"))
            roles_map = idx.get("roles", {})
            self.assertIn("aws-engineer", roles_map, f"aws-engineer missing from {path}")
            aws_skills = roles_map["aws-engineer"].get("skills", [])
            self.assertIn("aws-infrastructure", aws_skills)
            self.assertIn("setup-deployment", aws_skills)
            self.assertIn("add-telemetry-instrumentation", aws_skills)

    def test_05_fast_invocation_alias_resolution(self):
        """Fast invocation aliases @aws, @cloud and skill aliases must resolve correctly."""
        for path in [REGISTRY_DIR / "role-skill-index.json", ADAPTERS_DIR / "antigravity" / "role-skill-index.json"]:
            idx = json.loads(path.read_text(encoding="utf-8"))
            role_aliases = idx.get("role_aliases", {})
            self.assertEqual(role_aliases.get("aws"), "aws-engineer", "@aws must resolve to aws-engineer")
            self.assertEqual(role_aliases.get("cloud"), "aws-engineer", "@cloud must resolve to aws-engineer")

            skill_aliases = idx.get("skill_aliases", {})
            self.assertEqual(skill_aliases.get("aws_infra"), ["aws-infrastructure"])
            self.assertEqual(skill_aliases.get("aws_infrastructure"), ["aws-infrastructure"])


if __name__ == "__main__":
    unittest.main()
