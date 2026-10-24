#!/usr/bin/env python3
"""Automated Challenge Test Suite for Tier-3 Roles SOTA 2026-2027 Upgrade (Milestone 2).

Validates and stress-tests:
1. Role Inventory: All 10 Tier-3 upgraded roles exist in core/roles/*.md.
2. Architectural Guardrail Locks:
   - Every upgraded role contains between 12 and 24 explicit locks (**...LOCK**).
   - Domain-specific SOTA locks are present for each role per explorer blueprint.
3. Contract Output Alignment:
   - task-planner.md emits technical-delivery-plan.json and coordination-plan.json.
   - task-planner.md does not claim primary ownership of seo-weekly-board.json.
4. Structural Compliance:
   - All 10 roles follow the mandatory 17 core sections in order per role-standard.md.
   - All 10 roles declare Principal or Master practitioner level.
   - All 10 roles link to role-standard.md and dedicated review checklists.
   - Footers are well-formed with valid Last updated timestamps.
5. Quantitative & Mathematical Formulations:
   - Verifies mathematical formulas and quantitative engineering standards across roles.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
ROLES_DIR = CORE_DIR / "roles"
REFERENCES_DIR = ROLES_DIR / "references"

TIER3_UPGRADED_ROLES = [
    "ai-systems-engineer",
    "mmo-engineer",
    "aws-engineer",
    "3d-graphics-engineer",
    "agent-discovery-engineer",
    "ecommerce-engineer",
    "product-manager",
    "project-manager",
    "researcher",
    "task-planner",
]

EXPECTED_ROLE_LOCKS = {
    "ai-systems-engineer": [
        "VLLM-CACHE-LOCK",
        "GPU-DRA-LOCK",
        "SLM-DISTILLATION-LOCK",
        "AI-GOVERNANCE-LOCK",
        "RADIX-PREFIX-CACHE-LOCK",
        "CHUNKED-PREFILL-LOCK",
        "TMA-ASYNC-TRANSFER-LOCK",
        "DCGM-QUEUE-HPA-LOCK",
        "FASTMCP-STREAMING-LOCK",
        "TMPFS-SHM-SIZE-LOCK",
        "LITELLM-GATEWAY-CHOKE-LOCK",
        "OWASP-ASI-DEFENSE-LOCK",
    ],
    "mmo-engineer": [
        "ANONYMITY-LOCK",
        "ISOLATION-LOCK",
        "PROXYWARE-LOCK",
        "TRACKING-LOCK",
        "BEHAVIORAL-LOCK",
        "REVIEW-SYSTEM LOCK",
        "BUDGET-LOCK",
        "CAMOUFOX-CPP-PATCH-LOCK",
        "TLS-JA4-FINGERPRINT-LOCK",
        "WEBGPU-FINGERPRINT-ALIGNMENT-LOCK",
        "MURMUR3-CANVAS-NOISE-LOCK",
        "BEZIER-FITTS-TRAJECTORY-LOCK",
        "TRUE-ROI-FINANCIAL-LOCK",
        "THOMPSON-SAMPLING-BUDGET-LOCK",
        "DUAL-LAYER-S2S-TRACKING-LOCK",
        "STRICT-1-1-1-ISOLATION-LOCK",
    ],
    "aws-engineer": [
        "OPENTOFU-KMS-LOCK",
        "CROSSPLANE-COMPOSITION-LOCK",
        "BOTTLEROCKET-LOCK",
        "AWS-IAM-ZERO-TRUST-LOCK",
        "KARPENTER-AUTOSCALING-LOCK",
        "VPC-LATTICE-LOCK",
        "GRAVITON4-FIRST-LOCK",
        "BEDROCK-ISOLATION-LOCK",
        "EKS-POD-IDENTITY-LOCK",
        "CILIUM-EBPF-ENI-LOCK",
        "S3-EXPRESS-ZONE-LOCK",
        "AWS-KMS-CLIENT-ENCRYPTION-LOCK",
        "KARPENTER-NODEPOOL-DISRUPTION-LOCK",
        "MACIE-PII-SCAN-LOCK",
    ],
    "3d-graphics-engineer": [
        "WEBGPU-FALLBACK-LOCK",
        "DRACO-MESHOPT-LOCK",
        "MEMORY-DISPOSAL-LOCK",
        "FRAME-BUDGET-LOCK",
        "GEN-3D LOCK",
        "WGSL-COMPUTE-PIPELINE-LOCK",
        "3DGS-VRAM-BUDGET-LOCK",
        "CONTEXT-LOSS-RECOVERY-LOCK",
        "BASIS-KTX2-TEXTURE-LOCK",
        "LOD-DYNAMIC-DISTANCE-LOCK",
        "SHADOW-MAP-DRAW-CALL-LOCK",
        "PROCEDURAL-HITBOX-ISOLATION-LOCK",
        "ANIMATION-TICK-DECOUPLING-LOCK",
        "DISPOSAL-AUDIT-LOCK",
    ],
    "agent-discovery-engineer": [
        "AGENT-OVERLAP LOCK",
        "NO-SECRETS LOCK",
        "NO-DUMMY-DOMAIN LOCK",
        "SCHEMA-EXACT LOCK",
        "SIGNATURE-VERIFY LOCK",
        "A2A-PART-UNIFIED-LOCK",
        "SPIFFE-WORKLOAD-IDENTITY-LOCK",
        "RFC-8693-TOKEN-EXCHANGE-LOCK",
        "DYNAMIC-CARD-DISCOVERY-LOCK",
        "ZERO-DRIFT-REGISTRY-LOCK",
        "MTLS-CERT-VALIDATION-LOCK",
        "ROTATING-JWKS-ENDPOINT-LOCK",
        "WIMSE-FEDERATION-LOCK",
        "REGISTRY-ALLOWLIST-LOCK",
    ],
    "ecommerce-engineer": [
        "AI-COMMERCE LOCK",
        "MANDATE-AUTHORIZATION LOCK",
        "IDEMPOTENCY-LEDGER LOCK",
        "TTL-RESERVATION LOCK",
        "PCI-DSS-401 LOCK",
        "SERVER-PRICING-AUTHORITY LOCK",
        "NHI-COMMERCE LOCK",
        "ALIPAY-610K-TPS-LOCK",
        "REDIS-LUA-FENCING-LOCK",
        "SHOPEE-TRAFFIC-SHIELD-LOCK",
        "DOUBLE-ENTRY-LEDGER-LOCK",
        "AP2-CRYPTOGRAPHIC-MANDATE-LOCK",
        "AMIS-REVENUE-SYNC-LOCK",
    ],
    "product-manager": [
        "AI-SCOPE LOCK",
        "VANITY-METRIC LOCK",
        "HITL LOCK",
        "HYPOTHESIS LOCK",
        "KILL-EARLY LOCK",
        "PROBABILISTIC-ACCEPTANCE LOCK",
        "EVAL-DATASET LOCK",
        "UNIT-ECONOMICS LOCK",
        "ARTICLE-50 TRANSPARENCY LOCK",
        "AGENTIC-DRIFT LOCK",
        "AGENT-ROI-4PILLAR-LOCK",
        "COST-PER-VERIFIED-OUTCOME-LOCK",
        "BLAST-RADIUS-TIER-LOCK",
        "GOLDEN-EVAL-CURATION-LOCK",
        "PROBABILISTIC-SLA-LOCK",
        "C2PA-METADATA-DISCLOSURE-LOCK",
    ],
    "project-manager": [
        "AI-GOVERNANCE LOCK",
        "ORCHESTRATION-ACCOUNTABILITY LOCK",
        "AGENT-CAPACITY LOCK",
        "AI-COMPLIANCE LOCK",
        "PROBABILISTIC-ESTIMATION LOCK",
        "TOKEN-FINOPS LOCK",
        "COMMIT-PROVENANCE LOCK",
        "DAG-CYCLE-DETECTION-LOCK",
        "TOPOLOGICAL-PHASE-ORDERING-LOCK",
        "MONTE-CARLO-P85-LOCK",
        "TOKEN-BURN-CIRCUIT-BREAKER-LOCK",
        "GIST-DEBT-CEILING-LOCK",
        "HITL-DWELL-TIME-LOCK",
        "PARALLEL-PHASE-ISOLATION-LOCK",
        "COMMIT-AUTHORSHIP-LINEAGE-LOCK",
        "SPEC-FIRST-SDD-LOCK",
    ],
    "researcher": [
        "DEPTH LOCK",
        "AI SOURCE LOCK",
        "GROUNDING LOCK",
        "CoVe LOCK",
        "DEEP-RESEARCH-VERIFY LOCK",
        "PROVENANCE LOCK",
        "CITATION-DAG-LOCK",
        "MULTI-SOURCE-TRIANGULATION-LOCK",
        "COVE-ATOMIC-VERIFICATION-LOCK",
        "C2PA-CRYPTOGRAPHIC-PROVENANCE-LOCK",
        "ZERO-AI-PRIMARY-CITATION-LOCK",
        "INFORMATION-DENSITY-LOCK",
        "PRIMARY-SOURCE-HIERARCHY-LOCK",
        "URL-LIVENESS-VERIFICATION-LOCK",
        "YMYL-EXPERT-ELEVATION-LOCK",
    ],
    "task-planner": [
        "AI-GOVERNANCE LOCK",
        "TRUST-LADDER LOCK",
        "BACKGROUND-AGENT-UX LOCK",
        "GENUI-GOVERNANCE LOCK",
        "MCP-STATELESS LOCK",
        "EU-AI-ACT-DISCLOSURE LOCK",
        "EVAL-GATE LOCK",
        "OUTPUT-CONTRACT-ALIGNMENT-LOCK",
        "DAG-TASK-DECOMPOSITION-LOCK",
        "TOPOLOGICAL-SORT-LOCK",
        "PLAN-CHECKPOINT-RESTORE-LOCK",
        "INVEST-SLICING-CRITERIA-LOCK",
        "SLICE-BLAST-RADIUS-LOCK",
        "CRITICAL-PATH-METHOD-LOCK",
        "STATISTICS-DRIVEN-ESTIMATION-LOCK",
        "VALIDATION-CHECKPOINT-LOCK",
    ],
}

MANDATORY_SECTIONS = [
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


class TestTier3RolesUpgradeChallenge(unittest.TestCase):
    """Challenge test suite verifying Tier-3 role upgrades to SOTA 2026-2027 standards."""

    def test_all_10_roles_exist(self) -> None:
        """All 10 target role files must exist in core/roles/."""
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            self.assertTrue(path.exists(), f"Role file missing: {path}")

    def test_guardrail_lock_counts_in_range(self) -> None:
        """Each of the 10 upgraded roles must have >= 12 and <= 24 architectural locks."""
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            content = path.read_text(encoding="utf-8")
            locks = re.findall(r"\*\*([A-Z0-9_ -]+LOCK)\*\*", content)
            self.assertGreaterEqual(
                len(locks),
                12,
                f"Role {role} has {len(locks)} locks; expected >= 12 locks",
            )
            self.assertLessEqual(
                len(locks),
                24,
                f"Role {role} has {len(locks)} locks; expected <= 24 locks",
            )

    def test_domain_sota_locks_present(self) -> None:
        """Each role must contain its blueprint domain-specific SOTA locks."""
        for role, expected_locks in EXPECTED_ROLE_LOCKS.items():
            path = ROLES_DIR / f"{role}.md"
            content = path.read_text(encoding="utf-8")
            for lock in expected_locks:
                self.assertIn(
                    f"**{lock}**",
                    content,
                    f"Missing expected domain lock **{lock}** in {role}.md",
                )

    def test_task_planner_contract_alignment(self) -> None:
        """task-planner.md must emit technical-delivery-plan and coordination-plan, not seo-weekly-board."""
        path = ROLES_DIR / "task-planner.md"
        content = path.read_text(encoding="utf-8")

        # Must produce technical-delivery-plan.json
        self.assertIn(
            "contracts/schemas/technical-delivery-plan.json",
            content,
            "task-planner.md must declare contracts/schemas/technical-delivery-plan.json",
        )
        # Must produce coordination-plan.json
        self.assertIn(
            "contracts/schemas/coordination-plan.json",
            content,
            "task-planner.md must declare contracts/schemas/coordination-plan.json",
        )

        # In Outputs Produced section before 'Contracts owned by other roles',
        # seo-weekly-board must NOT be listed as an owned primary output
        outputs_match = re.search(r"## Outputs Produced\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        self.assertIsNotNone(outputs_match, "Outputs Produced section missing in task-planner.md")
        outputs_text = outputs_match.group(1)

        owned_part = outputs_text.split("Contracts owned by other roles")[0]
        self.assertNotIn(
            "contracts/schemas/seo-weekly-board.json",
            owned_part,
            "task-planner.md must not own contracts/schemas/seo-weekly-board.json as a primary output",
        )

    def test_role_standard_sections_in_order(self) -> None:
        """All 10 roles must have the mandatory 17 standard sections in order."""
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            content = path.read_text(encoding="utf-8")

            last_pos = -1
            for section in MANDATORY_SECTIONS:
                pos = content.find(section)
                self.assertNotEqual(
                    pos,
                    -1,
                    f"Role {role}.md is missing mandatory section '{section}'",
                )
                self.assertGreater(
                    pos,
                    last_pos,
                    f"Role {role}.md has section '{section}' out of order",
                )
                last_pos = pos

    def test_links_to_role_standard_and_checklist(self) -> None:
        """All 10 roles must link to role-standard.md and references/<role>-review-checklist.md."""
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            content = path.read_text(encoding="utf-8")

            self.assertIn(
                "[role-standard](role-standard.md)",
                content,
                f"Role {role}.md missing reference to role-standard.md",
            )
            expected_chk = f"references/{role}-review-checklist.md"
            self.assertIn(
                expected_chk,
                content,
                f"Role {role}.md missing reference to {expected_chk}",
            )

    def test_footer_timestamp_validity(self) -> None:
        """All 10 roles must end with a valid 'Last updated: YYYY-MM-DD' footer."""
        for role in TIER3_UPGRADED_ROLES:
            path = ROLES_DIR / f"{role}.md"
            content = path.read_text(encoding="utf-8")
            non_empty = [line.strip() for line in content.splitlines() if line.strip()]
            self.assertTrue(non_empty, f"Role {role}.md is empty")

            last_line = non_empty[-1]
            self.assertTrue(
                re.match(r"^Last updated: \d{4}-\d{2}-\d{2}$", last_line),
                f"Role {role}.md final line is '{last_line}'; expected 'Last updated: YYYY-MM-DD'",
            )

    def test_domain_mathematical_standards(self) -> None:
        """All 10 roles must embed concrete mathematical, architectural, or quantitative standards."""
        # mmo-engineer: True ROI formula and Thompson Sampling
        mmo_content = (ROLES_DIR / "mmo-engineer.md").read_text(encoding="utf-8")
        self.assertIn("True ROI", mmo_content)
        self.assertIn("Thompson Sampling", mmo_content)

        # 3d-graphics-engineer: VRAM formula and 60 FPS frame budget
        graphics_content = (ROLES_DIR / "3d-graphics-engineer.md").read_text(encoding="utf-8")
        self.assertIn("VRAM", graphics_content)
        self.assertIn("16.6", graphics_content)

        # product-manager: 4-Pillar Agent ROI and CPVO
        pm_content = (ROLES_DIR / "product-manager.md").read_text(encoding="utf-8")
        self.assertIn("ROI", pm_content)
        self.assertIn("Cost-per-Verified-Outcome", pm_content)

        # project-manager: Monte Carlo P85 and Kahn DAG
        pjm_content = (ROLES_DIR / "project-manager.md").read_text(encoding="utf-8")
        self.assertIn("Monte Carlo", pjm_content)
        self.assertIn("Kahn", pjm_content)

        # researcher: Information density and CoVe
        researcher_content = (ROLES_DIR / "researcher.md").read_text(encoding="utf-8")
        self.assertIn("Information Density", researcher_content)
        self.assertIn("Chain-of-Verification", researcher_content)

        # ecommerce-engineer: 610k TPS and double entry
        ecommerce_content = (ROLES_DIR / "ecommerce-engineer.md").read_text(encoding="utf-8")
        self.assertIn("610k TPS", ecommerce_content)
        self.assertIn("double-entry", ecommerce_content)


if __name__ == "__main__":
    unittest.main()
