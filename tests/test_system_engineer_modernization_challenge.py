"""
Challenge suite for the 2026-10 System Engineer modernization.

Verifies: KV-cache offloading tiering locks and schema fields, speculative
decoding acceptance gating, DRA GA pinning (v1.34/v1.36/v1.37), Agent Router
(ex-Envoy AI Gateway) inference routing, rack-scale Blackwell capacity
horizon, and OTel Profiles (public Alpha 2026-03) continuous profiling
guidance.
"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE = ROOT / "core" / "roles" / "system-engineer.md"
SCHEMA = ROOT / "core" / "contracts" / "schemas" / "system-design-spec.json"

PRIMARY_SKILLS = (
    "core/skills/platform/system-design/SKILL.md",
    "core/skills/foundation/performance-profiling/SKILL.md",
    "core/skills/platform/add-telemetry-instrumentation/SKILL.md",
    "core/skills/platform/setup-gpu-finops/SKILL.md",
    "core/skills/platform/setup-llm-gateway/SKILL.md",
    "core/skills/platform/supply-chain-security/SKILL.md",
    "core/skills/platform/debug-runtime-platform/SKILL.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSchemaModernization(unittest.TestCase):
    """Fields the role mandates must exist in system-design-spec.json."""

    def setUp(self):
        self.schema = json.loads(read(SCHEMA))

    def test_01_kv_cache_tiering_field(self):
        props = self.schema["properties"]["ai_infrastructure"]["properties"]
        self.assertIn("kv_cache_tiering", props)

    def test_02_speculative_decoding_field(self):
        props = self.schema["properties"]["ai_infrastructure"]["properties"]
        self.assertIn("speculative_decoding", props)

    def test_03_example_autoscaling_uses_keda_signals(self):
        example = json.dumps(self.schema.get("examples", []))
        self.assertIn("KEDA", example)
        self.assertIn("queue depth", example)


class TestRoleModernization(unittest.TestCase):
    def setUp(self):
        self.role = read(ROLE)

    def test_04_new_locks_present(self):
        for lock in (
            "KV-CACHE-TIERING LOCK",
            "SPECULATIVE-DECODING-ACCEPTANCE LOCK",
        ):
            self.assertIn(lock, self.role)

    def test_05_llm_d_in_serving_table(self):
        self.assertIn("llm-d", self.role)

    def test_06_dra_ga_versions_pinned(self):
        self.assertIn("v1.34", self.role)
        self.assertIn("v1.36", self.role)

    def test_07_agent_router_rename_noted(self):
        self.assertIn("Agent Router", self.role)
        self.assertIn("Envoy AI Gateway", self.role)

    def test_08_blackwell_capacity_horizon(self):
        self.assertIn("GB300", self.role)

    def test_09_speculative_decoding_gates_on_acceptance(self):
        self.assertIn("6.5x", self.role)
        self.assertIn("acceptance", self.role)


class TestSkillsModernization(unittest.TestCase):
    def test_10_primary_skills_have_versions(self):
        for rel in PRIMARY_SKILLS:
            text = read(ROOT / rel)
            self.assertRegex(text, r"(?m)^version: [0-9]+\.[0-9]+\.[0-9]+$", rel)

    def test_11_system_design_rules(self):
        text = read(ROOT / "core/skills/platform/system-design/SKILL.md")
        self.assertIn("KV-CACHE-TIERING (2026)", text)
        self.assertIn("SPECULATIVE-DECODING-DECISION (2026)", text)
        self.assertIn("DRA-GPU-ALLOCATION (2026)", text)

    def test_12_gpu_finops_cost_levers(self):
        text = read(ROOT / "core/skills/platform/setup-gpu-finops/SKILL.md")
        self.assertIn("KV-CACHE-OFFLOAD-COST (2026)", text)
        self.assertIn("SPECULATIVE-DECODING-THROUGHPUT (2026)", text)
        self.assertIn("RACK-SCALE-PRICING (2026)", text)

    def test_13_llm_gateway_agent_router(self):
        text = read(ROOT / "core/skills/platform/setup-llm-gateway/SKILL.md")
        self.assertIn("Agent Router", text)
        self.assertIn("InferencePool", text)

    def test_14_profiling_otel_alpha_and_acceptance(self):
        text = read(ROOT / "core/skills/foundation/performance-profiling/SKILL.md")
        self.assertIn("public Alpha since 2026-03", text)
        self.assertIn("Parca", text)
        self.assertIn("acceptance", text)

    def test_15_telemetry_profiles_alpha(self):
        text = read(ROOT / "core/skills/platform/add-telemetry-instrumentation/SKILL.md")
        self.assertIn("public Alpha since 2026-03", text)


class TestReferenceChecklist(unittest.TestCase):
    def test_16_checklist_has_modernization_gates(self):
        text = read(ROOT / "core/roles/references/system-engineer-review-checklist.md")
        self.assertIn("2026-10 Modernization Gates", text)
        self.assertIn("KV-Cache Tiering", text)
        self.assertIn("DRA GPU Allocation", text)


if __name__ == "__main__":
    unittest.main()
