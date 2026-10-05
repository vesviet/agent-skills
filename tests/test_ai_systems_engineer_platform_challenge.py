#!/usr/bin/env python3
"""Automated Challenge Test Suite for AI Systems Engineer Role & 2026-2027 SOTA Standards.

Validates and stress-tests:
1. AI Systems Engineer Role (`core/roles/ai-systems-engineer.md`) Invariant Verification:
   - Role-standard compliance: Mission, Level, Principal Expectations, Use This Role When,
     Core Responsibilities, Inputs Required, Outputs Produced, Deliverable Routing,
     Decision Boundaries, Role Boundaries, Collaboration, Guardrails, Skill Toolbox,
     Output Template, Review Checklist, Failure Modes, Anti-Patterns To Reject,
     Role Handoff, Definition Of Done.
   - The 4+ Mandatory Architectural Guardrail Locks:
     `VLLM-CACHE-LOCK`, `GPU-DRA-LOCK`, `SLM-DISTILLATION-LOCK`, `AI-GOVERNANCE-LOCK`.
   - Core and supplemental locks: `BOUNDARY LOCK`, `SECURITY LOCK`, `IRREVERSIBLE ACTION LOCK`,
     `DATA PRIVACY LOCK`, `FINOPS LOCK`, `EVAL GATE LOCK`, `STRUCTURED OUTPUT LOCK`.
   - 7 SOTA Pillars in Core Responsibilities:
     1. High-Throughput Model Serving with vLLM v1 & PagedAttention v3
     2. Dynamic Chunked Prefill & Head-of-Line Blocking Elimination
     3. Hierarchical Radix Tree Prefix Caching & Multi-Tier KV Offloading
     4. Hardware Slicing, NVIDIA MIG & Kubernetes 1.31+ DRA
     5. SLM Knowledge Distillation from DeepSeek-R1 & Hybrid Routing
     6. FastMCP Server Architecture & Streaming Tool Sandboxing
     7. LiteLLM Spend Governance, FinOps & Queue-Depth HPA Autoscaling
   - Primary Skills locked: `deploy-vllm-inference`, `setup-llm-gateway`, `setup-gpu-finops`,
     `implement-structured-outputs`, `build-mcp-server`.
   - Deliverables emitted: `system-design-spec.json`, `test-report.json`, `performance-audit.json`.
   - Footer date: `Last updated: 2026-10-05`.

2. AI Systems Engineer Review Checklist (`core/roles/references/ai-systems-engineer-review-checklist.md`):
   - All 14 SOTA verification sections.
   - Precision technical keywords: `PagedAttention`, `chunked prefill`, `Radix Tree`, `MIG`,
     `DRA`, `CEL`, `DeepSeek-R1`, `FastMCP`, `LiteLLM`, `RoCEv2`, `OpenCost`, `DCGM`, `tmpfs`, `Outlines`.

3. Exclusive Skill `deploy-vllm-inference` (`core/skills/ai/deploy-vllm-inference/`):
   - `SKILL.md` frontmatter, length bounds (< 200 lines), allowed-tools.
   - Required H2 sections: `## When to Use`, `## Core Rules`, `## Suggested Process`,
     `## Checklist`, `## Related Skills`.
   - Production manifests and reference guide (`agents/openai.yaml`, `references/vllm-production-guide.md`).

4. A2A Agent Card & Fast Invocation Integrity:
   - `core/a2a/registry/ai-systems-engineer.agent-card.json` structure, exposed skills, and output schemas.
   - Agent discovery in `agent-registry.json`.
   - Role-skill mapping and fast invocation aliases (@ai, @ml, @llm, deploy_vllm_inference, vllm)
     in both core and adapter `role-skill-index.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
CONTRACTS_DIR = CORE_DIR / "contracts" / "schemas"
REGISTRY_DIR = CORE_DIR / "a2a" / ".well-known"
AGENT_CARDS_DIR = CORE_DIR / "a2a" / "registry"
ADAPTERS_DIR = REPO_ROOT / "adapters"


class TestAISystemsEngineerRoleInvariants(unittest.TestCase):
    """Authoritative invariant testing for core/roles/ai-systems-engineer.md."""

    @classmethod
    def setUpClass(cls):
        cls.role_path = ROLES_DIR / "ai-systems-engineer.md"
        assert cls.role_path.exists(), "ai-systems-engineer.md must exist"
        cls.role_content = cls.role_path.read_text(encoding="utf-8")

    def test_01_standard_role_sections(self):
        """Role must contain all 19 standard sections per role-standard.md."""
        sections = [
            "# AI Systems Engineer",
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
            "VLLM-CACHE-LOCK",
            "GPU-DRA-LOCK",
            "SLM-DISTILLATION-LOCK",
            "AI-GOVERNANCE-LOCK",
        ]
        for lock in mandatory_locks:
            self.assertIn(lock, self.role_content, f"Missing mandatory SOTA lock: {lock}")

    def test_03_core_guardrail_locks_present(self):
        """Role must enforce foundational guardrail locks."""
        core_locks = [
            "BOUNDARY LOCK",
            "SECURITY LOCK",
            "IRREVERSIBLE ACTION LOCK",
            "DATA PRIVACY LOCK",
            "FINOPS LOCK",
            "EVAL GATE LOCK",
            "STRUCTURED OUTPUT LOCK",
        ]
        for lock in core_locks:
            self.assertIn(lock, self.role_content, f"Missing core guardrail lock: {lock}")

    def test_04_seven_sota_pillars_present(self):
        """Role must detail all 7 SOTA Pillars in Core Responsibilities."""
        pillar_terms = [
            "Pillar 1: High-Throughput Model Serving with vLLM v1 & PagedAttention v3",
            "Pillar 2: Dynamic Chunked Prefill & Head-of-Line Blocking Elimination",
            "Pillar 3: Hierarchical Radix Tree Prefix Caching & Multi-Tier KV Offloading",
            "Pillar 4: Hardware Slicing, NVIDIA MIG & Kubernetes 1.31+ DRA",
            "Pillar 5: SLM Knowledge Distillation from DeepSeek-R1 & Hybrid Routing",
            "Pillar 6: FastMCP Server Architecture & Streaming Tool Sandboxing",
            "Pillar 7: LiteLLM Spend Governance, FinOps & Queue-Depth HPA Autoscaling",
        ]
        for pillar in pillar_terms:
            self.assertIn(pillar, self.role_content, f"Missing SOTA pillar: {pillar}")

    def test_05_primary_skills_locked(self):
        """Primary skills toolbox must contain exclusive and core AI systems skills."""
        expected_skills = [
            "`deploy-vllm-inference`",
            "`setup-llm-gateway`",
            "`setup-gpu-finops`",
            "`implement-structured-outputs`",
            "`build-mcp-server`",
        ]
        for skill in expected_skills:
            self.assertIn(skill, self.role_content, f"Missing primary skill in toolbox: {skill}")

    def test_06_emitted_contract_schemas_defined(self):
        """Role must declare ownership of its emitted contract schemas."""
        emitted_schemas = [
            "system-design-spec.json",
            "test-report.json",
            "performance-audit.json",
        ]
        for schema in emitted_schemas:
            self.assertIn(schema, self.role_content, f"Missing emitted schema reference: {schema}")

    def test_07_footer_maintenance_date(self):
        """Role must have authoritative maintenance date: Last updated: 2026-10-05."""
        self.assertIn("Last updated: 2026-10-05", self.role_content)


class TestAISystemsEngineerReviewChecklist(unittest.TestCase):
    """Invariant testing for core/roles/references/ai-systems-engineer-review-checklist.md."""

    @classmethod
    def setUpClass(cls):
        cls.checklist_path = ROLES_DIR / "references" / "ai-systems-engineer-review-checklist.md"
        assert cls.checklist_path.exists(), "ai-systems-engineer-review-checklist.md must exist"
        cls.checklist_content = cls.checklist_path.read_text(encoding="utf-8")

    def test_01_all_14_sections_present(self):
        """Checklist must contain all 14 comprehensive SOTA verification sections."""
        expected_sections = [
            "### 1. High-Throughput Model Serving Engine (vLLM v1 C++ Core & Lock-Free IPC)",
            "### 2. Memory Virtualization & PagedAttention v3 (Hopper TMA & FP8 Slabs)",
            "### 3. Dynamic Chunked Prefill & Head-of-Line Blocking Mitigation",
            "### 4. Hierarchical Prefix Caching & Radix Tree Block Management",
            "### 5. Multi-Tier Distributed KV Cache Offloading (RoCEv2 RDMA Fabric)",
            "### 6. Hardware Virtualization, GPU Slicing & Kubernetes 1.31+ DRA",
            "### 7. Small Language Model (SLM) Knowledge Distillation & DeepSeek-R1 CoT",
            "### 8. Hybrid Edge/Cloud Inference Routing & Cost Optimization",
            "### 9. FastMCP Server Architecture & Streaming Tool Sandboxing",
            "### 10. Centralized AI Gateway Orchestration & LiteLLM Spend Governance",
            "### 11. Structured Outputs & Constrained Decoding",
            "### 12. Continuous Empirical Evaluation (CI/CD Evals)",
            "### 13. GPU FinOps, DCGM Observability & Queue-Depth Autoscaling",
            "### 14. Production Kubernetes AI Serving Deployment & StatefulSets",
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.checklist_content, f"Missing checklist section: {sec}")

    def test_02_technical_depth_keywords_present(self):
        """Checklist must contain all mandatory technical depth keywords."""
        keywords = [
            "PagedAttention",
            "chunked prefill",
            "Radix Tree",
            "MIG",
            "DRA",
            "CEL",
            "DeepSeek-R1",
            "FastMCP",
            "LiteLLM",
            "RoCEv2",
            "OpenCost",
            "DCGM",
            "tmpfs",
            "Outlines",
            "TMA",
            "SPSC",
            "FP8",
            "vllm:num_requests_waiting",
            "StatefulSet",
        ]
        for kw in keywords:
            self.assertIn(kw, self.checklist_content, f"Missing technical keyword in checklist: {kw}")


class TestDeployVLLMInferenceSkill(unittest.TestCase):
    """Validation of exclusive skill core/skills/ai/deploy-vllm-inference/."""

    @classmethod
    def setUpClass(cls):
        cls.skill_dir = SKILLS_DIR / "ai" / "deploy-vllm-inference"
        cls.skill_path = cls.skill_dir / "SKILL.md"
        assert cls.skill_path.exists(), "deploy-vllm-inference/SKILL.md must exist"
        cls.skill_content = cls.skill_path.read_text(encoding="utf-8")

    def test_01_skill_frontmatter_and_line_count(self):
        """SKILL.md must have valid frontmatter, allowed-tools, and length < 200 lines."""
        lines = self.skill_content.splitlines()
        self.assertLess(len(lines), 200, f"deploy-vllm-inference SKILL.md must be < 200 lines, got {len(lines)}")
        self.assertTrue(self.skill_content.startswith("---"), "Must start with YAML frontmatter")

        # Parse YAML frontmatter
        parts = self.skill_content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Frontmatter must be enclosed by ---")
        meta = yaml.safe_load(parts[1])
        self.assertEqual(meta.get("name"), "deploy-vllm-inference")
        self.assertIn("allowed-tools", meta)
        self.assertIsInstance(meta["allowed-tools"], list)
        self.assertGreater(len(meta["allowed-tools"]), 0)

    def test_02_required_h2_sections_present(self):
        """SKILL.md must contain all standard H2 sections."""
        required_h2 = [
            "## When to Use",
            "## Core Rules",
            "## Suggested Process",
            "## Checklist",
            "## Related Skills",
        ]
        for h2 in required_h2:
            self.assertIn(h2, self.skill_content, f"Missing required H2 section: {h2}")

    def test_03_core_rules_content(self):
        """SKILL.md must specify critical invariants in Core Rules."""
        core_rule_terms = [
            "VLLM_USE_V1=1",
            "chunked prefill",
            "--enable-prefix-caching=true",
            "--gpu-memory-utilization",
            "0.88",
            "0.90",
            "/dev/shm",
            "16GiB",
            "NVIDIA MIG",
            "Dynamic Resource Allocation (DRA)",
            "queue-depth",
        ]
        for term in core_rule_terms:
            self.assertIn(term, self.skill_content, f"Missing rule term in SKILL.md: {term}")

    def test_04_openai_agent_config(self):
        """Skill must include valid agents/openai.yaml interface specification."""
        agent_yaml_path = self.skill_dir / "agents" / "openai.yaml"
        self.assertTrue(agent_yaml_path.exists(), "agents/openai.yaml must exist")
        data = yaml.safe_load(agent_yaml_path.read_text(encoding="utf-8"))
        self.assertIn("interface", data)
        interface = data["interface"]
        self.assertEqual(interface.get("display_name"), "Deploy vLLM Inference")
        self.assertIn("short_description", interface)
        self.assertIn("default_prompt", interface)

    def test_05_reference_guide_validity(self):
        """Skill must include comprehensive production reference guide."""
        guide_path = self.skill_dir / "references" / "vllm-production-guide.md"
        self.assertTrue(guide_path.exists(), "references/vllm-production-guide.md must exist")
        guide_content = guide_path.read_text(encoding="utf-8")
        self.assertGreater(len(guide_content.splitlines()), 200, "Reference guide must be substantial (>200 lines)")

        guide_keywords = [
            "PagedAttention v3",
            "Hopper",
            "TMA",
            "Radix Tree",
            "RoCEv2",
            "ResourceClaimTemplate",
            "StatefulSet",
            "HorizontalPodAutoscaler",
            "DCGM_FI_DEV_FB_USED",
        ]
        for kw in guide_keywords:
            self.assertIn(kw, guide_content, f"Missing keyword in reference guide: {kw}")


class TestAISystemsEngineerAgentCardAndRegistry(unittest.TestCase):
    """Validation of A2A Agent Card, Discovery Registry, and Alias Resolution."""

    @classmethod
    def setUpClass(cls):
        cls.agent_card_path = AGENT_CARDS_DIR / "ai-systems-engineer.agent-card.json"
        assert cls.agent_card_path.exists(), "ai-systems-engineer.agent-card.json must exist"
        cls.agent_card = json.loads(cls.agent_card_path.read_text(encoding="utf-8"))

    def test_01_agent_card_structure(self):
        """Agent card must have correct id, contract_type, name, and output schemas."""
        self.assertEqual(self.agent_card.get("contract_type"), "agent-card")
        self.assertEqual(self.agent_card.get("name"), "ai-systems-engineer")
        self.assertEqual(self.agent_card.get("id"), "pack://agent-skills/core/roles/ai-systems-engineer")
        output_schemas = self.agent_card.get("defaultOutputSchemas", [])
        for schema in ["performance-audit.json", "system-design-spec.json", "test-report.json"]:
            self.assertIn(schema, output_schemas)

    def test_02_agent_card_skills_exposure(self):
        """Agent card must expose deploy-vllm-inference and primary AI systems skills."""
        card_skills = [s.get("id") for s in self.agent_card.get("skills", [])]
        expected_skills = [
            "deploy-vllm-inference",
            "setup-llm-gateway",
            "setup-gpu-finops",
            "implement-structured-outputs",
            "build-mcp-server",
        ]
        for exp in expected_skills:
            self.assertIn(exp, card_skills, f"Missing skill in agent card: {exp}")

    def test_03_agent_registry_listing(self):
        """ai-systems-engineer must be listed in agent-registry.json."""
        registry_path = REGISTRY_DIR / "agent-registry.json"
        self.assertTrue(registry_path.exists(), "agent-registry.json must exist")
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        agent_roles = [a.get("role") for a in reg.get("agents", [])]
        self.assertIn("ai-systems-engineer", agent_roles, "ai-systems-engineer must be listed in agent-registry.json")

    def test_04_role_skill_index_mapping(self):
        """role-skill-index.json must map ai-systems-engineer to its primary skills in core and adapter."""
        for path in [REGISTRY_DIR / "role-skill-index.json", ADAPTERS_DIR / "antigravity" / "role-skill-index.json"]:
            self.assertTrue(path.exists(), f"{path} must exist")
            idx = json.loads(path.read_text(encoding="utf-8"))
            roles_map = idx.get("roles", {})
            self.assertIn("ai-systems-engineer", roles_map, f"ai-systems-engineer missing from {path}")
            ai_skills = roles_map["ai-systems-engineer"].get("skills", [])
            self.assertIn("deploy-vllm-inference", ai_skills)
            self.assertIn("setup-llm-gateway", ai_skills)
            self.assertIn("setup-gpu-finops", ai_skills)
            self.assertIn("implement-structured-outputs", ai_skills)
            self.assertIn("build-mcp-server", ai_skills)

    def test_05_fast_invocation_alias_resolution(self):
        """Fast invocation aliases @ai, @ml, @llm and skill aliases must resolve correctly."""
        for path in [REGISTRY_DIR / "role-skill-index.json", ADAPTERS_DIR / "antigravity" / "role-skill-index.json"]:
            idx = json.loads(path.read_text(encoding="utf-8"))
            role_aliases = idx.get("role_aliases", {})
            self.assertEqual(role_aliases.get("ai"), "ai-systems-engineer", "@ai must resolve to ai-systems-engineer")
            self.assertEqual(role_aliases.get("ml"), "ai-systems-engineer", "@ml must resolve to ai-systems-engineer")
            self.assertEqual(role_aliases.get("llm"), "ai-systems-engineer", "@llm must resolve to ai-systems-engineer")

            skill_aliases = idx.get("skill_aliases", {})
            self.assertEqual(skill_aliases.get("deploy_vllm_inference"), ["deploy-vllm-inference"])
            self.assertEqual(skill_aliases.get("deploy-vllm"), ["deploy-vllm-inference"])
            self.assertEqual(skill_aliases.get("vllm"), ["deploy-vllm-inference"])
            self.assertEqual(skill_aliases.get("vllm_inference"), ["deploy-vllm-inference"])
            self.assertEqual(skill_aliases.get("paged_attention"), ["deploy-vllm-inference"])
            self.assertEqual(skill_aliases.get("radix_cache"), ["deploy-vllm-inference"])



class TestAdversarialEdgeCaseCoverage(unittest.TestCase):
    """Empirical adversarial stress testing and negative edge case validation."""

    @classmethod
    def setUpClass(cls):
        cls.role_content = (ROLES_DIR / "ai-systems-engineer.md").read_text(encoding="utf-8")
        cls.checklist_content = (ROLES_DIR / "references" / "ai-systems-engineer-review-checklist.md").read_text(encoding="utf-8")
        cls.skill_content = (SKILLS_DIR / "ai" / "deploy-vllm-inference" / "SKILL.md").read_text(encoding="utf-8")

    def test_01_unchunked_prefill_blocked_by_vllm_cache_lock(self):
        """Monolithic/unchunked prompt prefill must be strictly prohibited and blocked."""
        # Must be explicitly forbidden in VLLM-CACHE-LOCK
        self.assertIn("monolithic prompt prefill without chunking is strictly prohibited", self.role_content)
        # Must be treated as an anti-pattern
        self.assertIn("Monolithic prefill without chunking", self.role_content)
        # Must be treated as a documented failure mode with mitigation
        self.assertIn("Head-of-Line Blocking and TPOT Spikes in Monolithic Serving", self.role_content)
        # Chunked prefill must be mandatory in skill core rules
        self.assertIn("--enable-chunked-prefill=true", self.skill_content)
        self.assertIn("--max-num-batched-tokens 2048", self.skill_content)

    def test_02_vram_utilization_exceeding_90_blocked(self):
        """VRAM utilization > 0.90 must be strictly blocked to prevent catastrophic CUDA OOM."""
        # Role guardrail lock ceiling
        self.assertIn("--gpu-memory-utilization must be capped between 0.88 and 0.90", self.role_content)
        # Checklist explicitly rejects 0.95+
        self.assertIn("setting 0.95+ strictly rejected", self.checklist_content)
        # Skill core rule caps between 0.88 and 0.90
        self.assertIn("cap `--gpu-memory-utilization` between `0.88` and `0.90`", self.skill_content)

    def test_03_software_time_slicing_blocked_by_gpu_dra_lock(self):
        """Software time-slicing on multi-tenant production GPU must be strictly blocked by GPU-DRA-LOCK."""
        self.assertIn("unpartitioned software time-slicing", self.role_content)
        self.assertIn("prohibit unpartitioned software time-slicing", self.role_content)
        # Checklist strictly prohibits software time-slicing
        self.assertIn("software time-slicing on shared GPUs strictly prohibited", self.checklist_content)
        # Skill core rules prohibit software time-slicing
        self.assertIn("software time-slicing on production inference is prohibited", self.skill_content)
        # Mandates physical hardware partitioning via MIG or K8s 1.31+ DRA
        self.assertIn("3g.40gb", self.role_content)
        self.assertIn("Dynamic Resource Allocation", self.role_content)

    def test_04_direct_provider_bypass_blocked_by_ai_governance_lock(self):
        """Bypassing central gateway with direct provider calls or hardcoded keys must be blocked."""
        self.assertIn("bypass the centralized LLM gateway", self.role_content)
        self.assertIn("strictly prohibit direct provider calls", self.role_content)
        self.assertIn("Unmonitored direct provider calls", self.role_content)
        # Mandates cost-attribution headers and circuit breakers
        self.assertIn('"x-team-id"', self.role_content)
        self.assertIn('"x-service-name"', self.role_content)
        self.assertIn('"x-budget-tier"', self.role_content)
        self.assertIn("<= 10% of the daily budget", self.role_content)

    def test_05_quantized_slm_accuracy_drop_blocked_by_slm_distillation_lock(self):
        """Distilled SLM accuracy below 98.5% of FP16 baseline must be blocked from production release."""
        self.assertIn(">= 98.5% benchmark accuracy relative to FP16 baselines", self.role_content)
        self.assertIn("Reasoning Degradation in Quantized Distilled SLMs", self.role_content)
        self.assertIn("Ungrounded SLM distillation", self.role_content)
        # Must require <think> reasoning tokens from DeepSeek-R1
        self.assertIn("<think>", self.role_content)
        self.assertIn("DeepSeek-R1", self.role_content)

    def test_06_role_section_ordering_strict_compliance(self):
        """All 19 standard role sections plus optional sections must follow role-standard.md ordering."""
        expected_ordered_sections = [
            "# AI Systems Engineer",
            "Mission:",
            "Level:",
            "This role must follow [role-standard](role-standard.md) first.",
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
            "## Failure Modes",
            "## Anti-Patterns To Reject",
            "## Role Handoff",
            "## Definition Of Done",
            "Last updated: 2026-10-05",
        ]
        indices = [self.role_content.find(s) for s in expected_ordered_sections]
        for s, idx in zip(expected_ordered_sections, indices):
            self.assertNotEqual(idx, -1, f"Section {s} must be present in role file")
        for i in range(len(indices) - 1):
            self.assertLess(
                indices[i],
                indices[i + 1],
                f"Section '{expected_ordered_sections[i]}' must precede '{expected_ordered_sections[i + 1]}'",
            )

    def test_07_skill_allowed_tools_and_action_boundaries_compliance(self):
        """deploy-vllm-inference allowed-tools must exist in mcp-tool-map.yaml and be allowed in action-boundaries.yaml."""
        parts = self.skill_content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        allowed_tools = meta.get("allowed-tools", [])

        tool_map_file = CORE_DIR / "policies" / "mcp-tool-map.yaml"
        action_boundaries_file = CORE_DIR / "policies" / "action-boundaries.yaml"

        tool_map = yaml.safe_load(tool_map_file.read_text(encoding="utf-8"))
        actions = tool_map.get("tool_actions", {})

        boundaries = yaml.safe_load(action_boundaries_file.read_text(encoding="utf-8"))
        ai_policy = boundaries.get("roles", {}).get("ai-systems-engineer", {})
        allowed_actions = set(ai_policy.get("allowed", []))
        denied_actions = set(ai_policy.get("denied", []))

        for tool in allowed_tools:
            self.assertIn(tool, actions, f"Tool {tool} must be defined in mcp-tool-map.yaml")
            mapped_action = actions[tool]
            self.assertNotIn(
                mapped_action,
                denied_actions,
                f"Tool {tool} maps to denied action {mapped_action} for ai-systems-engineer",
            )
            self.assertIn(
                mapped_action,
                allowed_actions,
                f"Tool {tool} maps to action {mapped_action} which is not in allowed list for ai-systems-engineer",
            )


if __name__ == "__main__":
    unittest.main()

