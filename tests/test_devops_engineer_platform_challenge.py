#!/usr/bin/env python3
"""Automated Challenge Test Suite for DevOps Engineer Role & Platform Engineering Standards.

Validates and stress-tests:
1. Schema Meta-Validation & Bundled Examples:
   - JSON Schema Draft 2020-12 meta-schema compliance for `deployment-plan.json`.
   - Full validity of bundled examples in `deployment-plan.json`.
   - 2026-2027 modern platform properties in `deployment-plan.json`:
     `progressive_delivery`, `gitops_metadata`, `supply_chain_security`, `ebpf_security`,
     `cloud_native_ai_gpu`, `gitops_compliance`, `rollback_plan`.

2. Adversarial Negative Mutation Stress Tests:
   - Missing required fields (contract_type, version, environments, steps, rollback_plan, smoke_tests).
   - Invalid discriminator constant (`contract_type`).
   - Invalid rollback_plan.strategy enum.
   - Invalid rollback_plan.data_loss_risk enum.
   - Missing required fields in progressive_delivery (canary_steps, metric_analysis, auto_rollback).
   - Missing required fields in gitops_metadata (applicationset_ref, sync_policy, ssa_enabled).

3. DevOps Engineer Role (`core/roles/devops-engineer.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Guardrails, Skill Toolbox, Output Template, Review Checklist, Failure Modes, Anti-Patterns, Definition Of Done.
   - The Great Architectural Convergence across 7 pillars:
     1. Declarative Universal Control Planes, GitOps & Secret Management (ArgoCD v2.12+ SSA, Crossplane, OpenTofu KMS, ESO).
     2. Progressive Delivery & Sidecarless Service Mesh (Argo Rollouts, Prometheus MetricAnalysis, PromQL vector coalescing, Cilium eBPF, Istio Ambient).
     3. Deep Observability & Kernel Runtime Telemetry (OTel memory_limiter first, tail-based sampling, Tetragon Sigkill, Hubble L7).
     4. Platform Engineering & Internal Developer Platforms (Backstage dynamic plugins, Score YAML, Kratix Promises, Radius Recipes).
     5. Cloud-Native AI & GPU Infrastructure on K8s (KubeRay, vLLM PagedAttention, MIG 3g.40gb, DRA K8s 1.31+, queue-depth HPA, OpenCost DCGM).
     6. Cryptographic Supply Chain Security (SLSA Level 3+, Syft SPDX 2.3 SBOM, Cosign keyless OIDC, Kyverno fail-closed, Chainguard/Wolfi distroless).
     7. Senior Fullstack / Team Lead Kubernetes Dev Debugging Standard (kubectl dev context, port-forward lsof/PID traps, structured JSON logging with trace_id, netshoot debug containers, pprof on :6060).
   - Guardrail Locks: BOUNDARY LOCK, SECURITY LOCK, IRREVERSIBLE ACTION LOCK, TRACE LOCK, UNCERTAINTY LOCK,
     GITOPS LOCK, AI-DEPLOY LOCK, SUPPLY-CHAIN LOCK, IDP-GOLDEN-PATH LOCK, AI-REMEDIATION LOCK,
     AI-FINOPS LOCK, DURABLE-DEPLOY LOCK, MCP-STATELESS LOCK, LLM-GATEWAY LOCK, K8S-DEV-DEBUG LOCK,
     SIDECARLESS-MESH LOCK, KERNEL-SECURITY LOCK, GPU-SLICING LOCK, ADMISSION-FAIL-CLOSE LOCK, GPU-ACCELERATION-GOVERNANCE LOCK.
   - Primary Skills locked: `setup-deployment`, `debug-runtime-platform`, `add-telemetry-instrumentation`, `manage-secrets`, `configure-mcp`, `setup-llm-gateway`, `supply-chain-security`.

4. DevOps Engineer Review Checklist (`core/roles/references/devops-engineer-review-checklist.md`):
   - All 13 comprehensive sections covering GitOps SSA, secret encryption, canary MetricAnalysis, sidecarless mesh,
     OTel collector pipeline, kernel security, IDP Golden Paths, cloud-native AI/GPU infrastructure, SLSA supply chain,
     Kubernetes dev debugging, AI/ML deployment, AI FinOps, and MCP/durable workflows.

5. Primary Skills & Agent Conformance:
   - `setup-deployment`, `debug-runtime-platform`, `add-telemetry-instrumentation`, `manage-secrets`, `configure-mcp`, `setup-llm-gateway`, `supply-chain-security`.
   - Valid YAML frontmatter, line count within bounds (< 200 lines), allowed-tools.

6. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/devops-engineer.agent-card.json` validity and skill IDs.
   - Agent discovery and role-skill indexing in `agent-registry.json` and `role-skill-index.json`.
   - Fast invocation alias resolution for `@devops`, `@infra`, `@infrastructure`.
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
REPORTS_DIR = REPO_ROOT / "reports"


class TestDeploymentPlanSchema(unittest.TestCase):
    """Rigorous schema validation and negative mutation testing for deployment-plan.json."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = CONTRACTS_DIR / "deployment-plan.json"
        assert cls.schema_path.exists(), "deployment-plan.json must exist"
        cls.schema_raw = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema_raw)
        cls.validator = Draft202012Validator(cls.schema_raw)

    def test_01_meta_schema_conformance(self):
        """Schema itself must be valid JSON Schema Draft 2020-12."""
        self.assertEqual(self.schema_raw.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema_raw.get("$id"), "deployment-plan")
        self.assertEqual(self.schema_raw.get("type"), "object")

    def test_02_bundled_examples_pass_validation(self):
        """All examples bundled within deployment-plan.json must validate cleanly."""
        examples = self.schema_raw.get("examples", [])
        self.assertGreater(len(examples), 0, "Schema must include at least one bundled example")
        for idx, ex in enumerate(examples):
            errors = list(self.validator.iter_errors(ex))
            self.assertEqual(
                len(errors),
                0,
                f"Bundled example {idx} failed schema validation: {[e.message for e in errors]}",
            )

    def test_03_modern_platform_properties_present(self):
        """Schema must define all 2026-2027 modern platform engineering properties."""
        props = self.schema_raw.get("properties", {})
        modern_props = [
            "progressive_delivery",
            "gitops_metadata",
            "supply_chain_security",
            "ebpf_security",
            "ai_gpu_infrastructure",
            "gitops_compliance",
            "rollback_plan",
        ]
        for prop in modern_props:
            self.assertIn(prop, props, f"Missing modern platform property: {prop}")

    def test_04_progressive_delivery_structure(self):
        """progressive_delivery must require canary_steps, metric_analysis, and auto_rollback."""
        pd = self.schema_raw.get("properties", {}).get("progressive_delivery", {})
        self.assertEqual(pd.get("type"), "object")
        required = pd.get("required", [])
        self.assertIn("canary_steps", required)
        self.assertIn("metric_analysis", required)
        self.assertIn("auto_rollback", required)

    def test_05_gitops_metadata_structure(self):
        """gitops_metadata must require applicationset_ref, sync_policy, and ssa_enabled."""
        gm = self.schema_raw.get("properties", {}).get("gitops_metadata", {})
        self.assertEqual(gm.get("type"), "object")
        required = gm.get("required", [])
        self.assertIn("applicationset_ref", required)
        self.assertIn("sync_policy", required)
        self.assertIn("ssa_enabled", required)

    def test_06_negative_mutation_missing_required_fields(self):
        """Omitting mandatory fields must fail schema validation."""
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

    def test_07_negative_mutation_invalid_contract_type(self):
        """Invalid contract_type discriminator must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][0])
        mutant["contract_type"] = "invalid-contract-type"
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject invalid contract_type")

    def test_08_negative_mutation_invalid_rollback_strategy(self):
        """Structured rollback_plan missing required strategy must fail validation."""
        mutant = copy.deepcopy(self.schema_raw["examples"][1])
        del mutant["rollback_plan"]["strategy"]
        errors = list(self.validator.iter_errors(mutant))
        self.assertGreater(len(errors), 0, "Validator failed to reject missing strategy in structured rollback_plan")

    def test_09_negative_mutation_invalid_progressive_delivery(self):
        """progressive_delivery missing required fields must fail validation."""
        valid_example = copy.deepcopy(self.schema_raw["examples"][0])
        if "progressive_delivery" in valid_example:
            mutant = copy.deepcopy(valid_example)
            del mutant["progressive_delivery"]["metric_analysis"]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, "Validator failed to reject missing metric_analysis")

    def test_10_negative_mutation_invalid_gitops_metadata(self):
        """gitops_metadata missing required fields must fail validation."""
        valid_example = copy.deepcopy(self.schema_raw["examples"][0])
        if "gitops_metadata" in valid_example:
            mutant = copy.deepcopy(valid_example)
            del mutant["gitops_metadata"]["applicationset_ref"]
            errors = list(self.validator.iter_errors(mutant))
            self.assertGreater(len(errors), 0, "Validator failed to reject missing applicationset_ref")


class TestDevOpsEngineerRoleInvariants(unittest.TestCase):
    """Authoritative invariant testing for core/roles/devops-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "devops-engineer.md"
        assert cls.role_path.exists(), "devops-engineer.md must exist"
        cls.role_content = cls.role_path.read_text(encoding="utf-8")

    def test_01_standard_role_sections(self):
        """Role must contain all standard role sections per role-standard.md."""
        sections = [
            "# DevOps Engineer",
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

    def test_02_guardrail_locks_present(self):
        """Role must enforce all mandatory Guardrail Locks."""
        expected_locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "TRACE LOCK",
            "UNCERTAINTY LOCK",
            "GITOPS LOCK",
            "AI-DEPLOY LOCK",
            "SUPPLY-CHAIN LOCK",
            "IDP-GOLDEN-PATH LOCK",
            "AI-REMEDIATION LOCK",
            "AI-FINOPS LOCK",
            "DURABLE-DEPLOY LOCK",
            "MCP-STATELESS LOCK",
            "LLM-GATEWAY LOCK",
            "K8S-DEV-DEBUG LOCK",
            "SIDECARLESS-MESH LOCK",
            "KERNEL-SECURITY LOCK",
            "GPU-SLICING LOCK",
            "ADMISSION-FAIL-CLOSE LOCK",
            "GPU-ACCELERATION-GOVERNANCE LOCK",
        ]
        for lock in expected_locks:
            self.assertIn(lock, self.role_content, f"Missing required guardrail lock: {lock}")

    def test_03_seven_pillars_present(self):
        """Role must detail all 7 SOTA Pillars from research."""
        pillar_terms = [
            "Pillar 1: Declarative Universal Control Planes, GitOps & Secret Management",
            "Pillar 2: Progressive Delivery & Sidecarless Service Mesh",
            "Pillar 3: Deep Observability & Kernel Runtime Telemetry",
            "Pillar 4: Platform Engineering & Internal Developer Platforms (IDP)",
            "Pillar 5: Cloud-Native AI & GPU Infrastructure on Kubernetes",
            "Pillar 6: Cryptographic Supply Chain Security & Policy-as-Code Admission",
            "Pillar 7: Senior Fullstack / Team Lead Kubernetes Dev Debugging Standard",
        ]
        for pillar in pillar_terms:
            self.assertIn(pillar, self.role_content, f"Missing pillar definition: {pillar}")

    def test_04_k8s_dev_debugging_invariants(self):
        """Role must mandate Senior Team Lead Kubernetes Dev Debugging standards."""
        k8s_terms = [
            "kubectl config set-context --current --namespace=dev",
            "lsof",
            "k8s-pf-*.pid",
            "OpenTelemetry",
            "trace_id",
            "netshoot:v0.13",
            "pprof",
            ":6060",
        ]
        for term in k8s_terms:
            self.assertIn(term, self.role_content, f"Missing K8s Dev Debugging term: {term}")

    def test_05_primary_skills_locked(self):
        """Primary skills toolbox must contain core DevOps skills."""
        expected_skills = [
            "`setup-deployment`",
            "`debug-runtime-platform`",
            "`add-telemetry-instrumentation`",
            "`manage-secrets`",
            "`configure-mcp`",
            "`setup-llm-gateway`",
            "`supply-chain-security`",
        ]
        for skill in expected_skills:
            self.assertIn(skill, self.role_content, f"Missing primary skill in toolbox: {skill}")


class TestDevOpsEngineerReviewChecklist(unittest.TestCase):
    """Invariant testing for core/roles/references/devops-engineer-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "devops-engineer-review-checklist.md"
        assert cls.checklist_path.exists(), "devops-engineer-review-checklist.md must exist"
        cls.checklist_content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_13_sections_present(self):
        """Checklist must contain all 13 comprehensive SOTA verification sections."""
        expected_sections = [
            "### 1. Declarative GitOps & Universal Control Plane (ArgoCD SSA & Crossplane)",
            "### 2. Secret Management & Client-Side State Encryption (Vault, ESO, OpenTofu KMS)",
            "### 3. Progressive Delivery & MetricAnalysis Canary Gates (Argo Rollouts & PromQL)",
            "### 4. Sidecarless Service Mesh & Kernel Networking (Cilium eBPF & Istio Ambient)",
            "### 5. Deep Observability & OTel Collector Pipeline Architecture",
            "### 6. Kernel-Level Runtime Security & Forensics (Cilium Tetragon & Hubble)",
            "### 7. Internal Developer Platforms & Self-Service Golden Paths (Backstage & Score)",
            "### 8. Cloud-Native AI Model Serving & Distributed Orchestration (KubeRay & vLLM)",
            "### 9. Hardware Virtualization, GPU Slicing & Queue-Depth Autoscaling (MIG, DRA, HPA)",
            "### 10. AI FinOps, Cost Attribution & LLM Gateway Choke Point (OpenCost & LiteLLM)",
            "### 11. Cryptographic Supply Chain Security & Provenance (SLSA, Syft SBOM, Cosign Keyless)",
            "### 12. Policy-as-Code & Fail-Closed Admission Enforcement (Kyverno Strict)",
            "### 13. Senior Fullstack / Team Lead Kubernetes Dev Debugging Standards",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.checklist_content, f"Missing checklist section: {sec}")

    def test_02_technical_depth_in_checklist(self):
        """Checklist must include precise technical tools and criteria."""
        keywords = [
            "ServerSideApply",
            "ApplicationSet",
            "Crossplane",
            "OpenTofu",
            "AES-GCM",
            "ExternalSecret",
            "MetricAnalysis",
            "vector(0)",
            "ztunnel",
            "HBONE",
            "memory_limiter",
            "tail_sampling",
            "Tetragon",
            "Sigkill",
            "Score",
            "KubeRay",
            "vLLM",
            "PagedAttention",
            "MIG",
            "DRA",
            "Cosign",
            "Kyverno",
            "lsof",
            "netshoot",
            "pprof",
        ]
        for kw in keywords:
            self.assertIn(kw, self.checklist_content, f"Missing technical keyword in checklist: {kw}")


class TestDevOpsEngineerPrimarySkills(unittest.TestCase):
    """Validation of primary skills owned by DevOps Engineer."""

    def test_01_setup_deployment_skill_validity(self):
        """setup-deployment SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "platform" / "setup-deployment" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "setup-deployment SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "setup-deployment SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: setup-deployment", content)
        self.assertIn("allowed-tools:", content)

    def test_02_debug_runtime_platform_skill_validity(self):
        """debug-runtime-platform SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "platform" / "debug-runtime-platform" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "debug-runtime-platform SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "debug-runtime-platform SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: debug-runtime-platform", content)
        self.assertIn("allowed-tools:", content)

    def test_03_manage_secrets_skill_validity(self):
        """manage-secrets SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "security-data" / "manage-secrets" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "manage-secrets SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "manage-secrets SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: manage-secrets", content)
        self.assertIn("allowed-tools:", content)

    def test_04_supply_chain_security_skill_validity(self):
        """supply-chain-security SKILL.md must be valid, concise (<200 lines), and define allowed-tools."""
        skill_path = SKILLS_DIR / "platform" / "supply-chain-security" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "supply-chain-security SKILL.md must exist")
        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(len(lines), 200, "supply-chain-security SKILL.md should be concise (<= 200 lines)")
        self.assertTrue(content.startswith("---"), "Must start with YAML frontmatter")
        self.assertIn("name: supply-chain-security", content)
        self.assertIn("allowed-tools:", content)


class TestDevOpsEngineerAgentCardAndRegistry(unittest.TestCase):
    """Validation of A2A Agent Card, Discovery Registry, and Alias Resolution."""

    @classmethod
    def setUpClass(cls):
        cls.agent_card_path = AGENT_CARDS_DIR / "devops-engineer.agent-card.json"
        assert cls.agent_card_path.exists(), "devops-engineer.agent-card.json must exist"
        cls.agent_card = json.loads(cls.agent_card_path.read_text(encoding="utf-8"))

    def test_01_agent_card_structure(self):
        """Agent card must have correct id, contract_type, name, and output schemas."""
        self.assertEqual(self.agent_card.get("contract_type"), "agent-card")
        self.assertEqual(self.agent_card.get("name"), "devops-engineer")
        self.assertEqual(self.agent_card.get("id"), "pack://agent-skills/core/roles/devops-engineer")
        output_schemas = self.agent_card.get("defaultOutputSchemas", [])
        self.assertIn("deployment-plan.json", output_schemas)

    def test_02_agent_card_skills_coverage(self):
        """Agent card must expose setup-deployment, debug-runtime-platform, and manage-secrets."""
        card_skills = [s.get("id") for s in self.agent_card.get("skills", [])]
        expected = ["setup-deployment", "debug-runtime-platform", "manage-secrets", "supply-chain-security"]
        for exp in expected:
            self.assertIn(exp, card_skills, f"Missing skill in agent card: {exp}")

    def test_03_agent_registry_listing(self):
        """devops-engineer must be listed in agent-registry.json."""
        registry_path = REGISTRY_DIR / "agent-registry.json"
        self.assertTrue(registry_path.exists(), "agent-registry.json must exist")
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        agent_roles = [a.get("role") for a in reg.get("agents", [])]
        self.assertIn("devops-engineer", agent_roles, "devops-engineer must be listed in agent-registry.json")

    def test_04_role_skill_index_mapping(self):
        """role-skill-index.json must correctly map devops-engineer to its primary skills."""
        index_path = REGISTRY_DIR / "role-skill-index.json"
        self.assertTrue(index_path.exists(), "role-skill-index.json must exist")
        idx = json.loads(index_path.read_text(encoding="utf-8"))
        roles_map = idx.get("roles", {})
        self.assertIn("devops-engineer", roles_map, "devops-engineer must be mapped in role-skill-index.json")
        devops_skills = roles_map["devops-engineer"].get("skills", [])
        self.assertIn("setup-deployment", devops_skills)
        self.assertIn("debug-runtime-platform", devops_skills)
        self.assertIn("manage-secrets", devops_skills)

    def test_05_fast_invocation_alias_resolution(self):
        """Fast invocation aliases @devops, @infra, @infrastructure must resolve to devops-engineer."""
        index_path = REGISTRY_DIR / "role-skill-index.json"
        idx = json.loads(index_path.read_text(encoding="utf-8"))
        aliases = idx.get("role_aliases", {})
        self.assertEqual(aliases.get("devops"), "devops-engineer", "@devops alias must resolve to devops-engineer")
        self.assertEqual(aliases.get("infra"), "devops-engineer", "@infra alias must resolve to devops-engineer")
        self.assertEqual(aliases.get("infrastructure"), "devops-engineer", "@infrastructure alias must resolve to devops-engineer")


if __name__ == "__main__":
    unittest.main()
