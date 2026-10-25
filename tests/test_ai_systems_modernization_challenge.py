"""
Challenge suite for the 2026-10 AI Systems Engineer modernization.

Verifies: 2026 frontier model lineage (GPT-6 / Claude 5.x generation replaces
Claude 3.5 / GPT-4o pins), vLLM engine currency (V1 default, v0.32+), DRA GA
(resource.k8s.io/v1, not beta v1alpha3), KEDA-not-HPA alignment with
system-design, MCP Streamable HTTP transport (SSE deprecated), Pillar 8
context engineering + CONTEXT-ENGINEERING-LOCK, 2026 agentic benchmark
calibration (tau2-bench pass^k, Terminal-Bench 2.0), and current open-weight
model generation.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE = ROOT / "core" / "roles" / "ai-systems-engineer.md"
CHECKLIST = ROOT / "core" / "roles" / "references" / "ai-systems-engineer-review-checklist.md"
SKILL_VLLM = ROOT / "core" / "skills" / "ai" / "deploy-vllm-inference" / "SKILL.md"
SKILL_EVAL = ROOT / "core" / "skills" / "ai-agent" / "agent-evaluation" / "SKILL.md"
SKILL_CTX = ROOT / "core" / "skills" / "ai-agent" / "context-optimization" / "SKILL.md"
SKILL_RISK = ROOT / "core" / "skills" / "foundation" / "ai-risk-assessment" / "SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestModelLineage(unittest.TestCase):
    def test_01_stale_2024_model_pins_removed(self):
        role = read(ROLE)
        self.assertNotIn("Claude 3.5", role)
        self.assertNotIn("GPT-4o", role)
        checklist = read(CHECKLIST)
        self.assertNotIn("Claude 3.5", checklist)
        self.assertNotIn("GPT-4o", checklist)

    def test_02_current_frontier_generation_pinned(self):
        role = read(ROLE)
        self.assertIn("Claude Opus 5.5", role)
        self.assertIn("GPT-6", role)
        self.assertIn("Gemini 4", role)

    def test_03_current_open_weight_generation(self):
        role = read(ROLE)
        for model in ("GLM-5", "DeepSeek-V4", "Qwen3.8", "gpt-oss"):
            self.assertIn(model, role, msg=f"missing open-weight generation pin: {model}")
        # DeepSeek-R1 remains referenced as the historical teacher lineage
        self.assertIn("DeepSeek-R1", role)


class TestEngineCurrency(unittest.TestCase):
    def test_04_vllm_v1_default_and_current(self):
        role = read(ROLE)
        skill = read(SKILL_VLLM)
        self.assertIn("v0.32+", role)
        self.assertIn("default since early 2025", role)
        self.assertIn("v0.32+", skill)
        self.assertIn("VLLM_USE_V1=1", skill)  # legacy escape hatch documented

    def test_05_dra_ga_api(self):
        skill = read(SKILL_VLLM)
        role = read(ROLE)
        self.assertIn("apiVersion: resource.k8s.io/v1", skill)
        self.assertNotIn("apiVersion: resource.k8s.io/v1alpha3", skill)
        self.assertIn("GA v1.34", role)

    def test_06_keda_alignment(self):
        role = read(ROLE)
        skill = read(SKILL_VLLM)
        self.assertIn("KEDA-NOT-HPA", role)
        self.assertIn("KEDA", skill)


class TestTransportAndContext(unittest.TestCase):
    def test_07_streamable_http_replaces_sse(self):
        role = read(ROLE)
        self.assertIn("Streamable HTTP", role)
        self.assertIn("2025-03-26", role)
        self.assertNotIn("over Server-Sent Events (SSE) or stdio", role)
        self.assertNotIn("(SSE / stdio)", role)

    def test_08_pillar_8_context_engineering(self):
        role = read(ROLE)
        self.assertIn("Pillar 8: Context Engineering & Agent Memory (2026)", role)
        for term in ("compaction", "Just-in-Time Retrieval", "context rot", "Sub-Agent Context Isolation"):
            self.assertIn(term, role, msg=f"missing context engineering term: {term}")

    def test_09_context_engineering_lock(self):
        self.assertIn("CONTEXT-ENGINEERING-LOCK", read(ROLE))

    def test_10_context_optimization_skill_upgraded(self):
        skill = read(SKILL_CTX)
        self.assertIn("version: 2.0.0", skill)
        self.assertIn("Anthropic-aligned", skill)
        self.assertIn("compaction", skill)
        self.assertIn("just-in-time retrieval", skill.lower())


class TestEvalCalibration(unittest.TestCase):
    def test_11_benchmark_landscape_pinned(self):
        role = read(ROLE)
        self.assertIn("τ²-bench", role)
        self.assertIn("Terminal-Bench 2.0", role)
        self.assertIn("pass^k", role)

    def test_12_agent_evaluation_skill_upgraded(self):
        skill = read(SKILL_EVAL)
        self.assertIn("version: 2.0.0", skill)
        self.assertIn("pass^k", skill)
        self.assertIn("τ²-bench", skill)
        self.assertIn("Terminal-Bench 2.0", skill)


class TestChecklistAndVersions(unittest.TestCase):
    def test_13_checklist_modernization_gates(self):
        body = read(CHECKLIST)
        self.assertIn("### 16. 2026-10 Modernization Gates", body)
        for gate in (
            "Model-Lineage Gate",
            "Engine-Currency Gate",
            "Transport Gate",
            "Context-Engineering Gate",
            "Eval-Calibration Gate",
        ):
            self.assertIn(gate, body)

    def test_14_skill_versions_and_bounds(self):
        self.assertIn('version: "2.0.0"', read(SKILL_VLLM))
        for path in (SKILL_VLLM, SKILL_EVAL, SKILL_CTX):
            line_count = len(read(path).splitlines())
            self.assertLess(line_count, 200, msg=f"{path.name} exceeds 200 lines")

    def test_15_role_footer_date(self):
        self.assertIn("Last updated: 2026-10-25", read(ROLE))

    def test_16_ai_risk_assessment_untouched(self):
        # ai-risk-assessment was already current (EU AI Act Article 50 / 2027-2028
        # deadlines) and must remain intact by this modernization.
        body = read(SKILL_RISK)
        self.assertIn("Article 50", body)
        self.assertIn("2 August 2026", body)


if __name__ == "__main__":
    unittest.main()
