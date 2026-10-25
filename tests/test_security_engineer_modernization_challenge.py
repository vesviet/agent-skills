"""
Challenge suite for the 2026-10 Security Engineer modernization.

Verifies: the official OWASP Top 10 for Agentic Applications 2026 list in the
security-audit skill (and eradication of invented ASI titles), EU Cyber
Resilience Act readiness gates (2026-09-11 reporting / 2026-12-11 main
obligations / 2027-12-11 SBOM), post-quantum readiness (NIST IR 8547
2030/2035, X25519MLKEM768 hybrid TLS, CBOM inventory, ML-DSA FIPS 204),
CaMeL capability confinement, GenAI Red Teaming Manual v1.0 alignment, and
the extended security-audit.json contract blocks.
"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE = ROOT / "core" / "roles" / "security-engineer.md"
CHECKLIST = ROOT / "core" / "roles" / "references" / "security-engineer-review-checklist.md"
SCHEMA = ROOT / "core" / "contracts" / "schemas" / "security-audit.json"
SKILL_AUDIT = ROOT / "core" / "skills" / "security-data" / "security-audit" / "SKILL.md"
SKILL_SECRETS = ROOT / "core" / "skills" / "security-data" / "manage-secrets" / "SKILL.md"
SKILL_PID = ROOT / "core" / "skills" / "security-data" / "prompt-injection-defense" / "SKILL.md"
ROLE_STANDARD = ROOT / "core" / "roles" / "role-standard.md"

OFFICIAL_ASI_TITLES = (
    "ASI01 Agent Goal Hijack",
    "ASI02 Tool Misuse & Exploitation",
    "ASI03 Identity & Privilege Abuse",
    "ASI04 Agentic Supply Chain",
    "ASI05 Unexpected Code Execution",
    "ASI06 Memory & Context Poisoning",
    "ASI07 Insecure Inter-Agent Communication",
    "ASI08 Cascading Failures",
    "ASI09 Human-Agent Trust Exploitation",
    "ASI10 Rogue Agents",
)

INVENTED_ASI_TITLES = (
    "ASI02 Agent Impersonation",
    "ASI03 Excessive Agency",
    "ASI02 Excessive Agency",
    "ASI06 Data Leakage",
    "ASI07 Cascading Delegation",
    "ASI08 Missing HITL",
    "ASI09 Insecure Retrieval",
    "ASI10 Observability Gaps",
)

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional dependency
    jsonschema = None


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestAsiCorrectness(unittest.TestCase):
    """The security-audit skill must carry the official ASI 2026 list."""

    def test_01_official_asi_list_in_audit_skill(self):
        body = read(SKILL_AUDIT)
        for title in OFFICIAL_ASI_TITLES:
            self.assertIn(title, body, msg=f"missing official title: {title}")

    def test_02_audit_skill_core_rules_pure(self):
        body = read(SKILL_AUDIT)
        core_rules = body.split("## Core Rules", 1)[1].split("## Suggested Process", 1)[0]
        for title in INVENTED_ASI_TITLES:
            self.assertNotIn(title, core_rules, msg=f"invented title in Core Rules: {title}")

    def test_03_invented_asi_labels_eradicated(self):
        for md in (ROOT / "core").rglob("*.md"):
            body = read(md)
            for title in INVENTED_ASI_TITLES:
                self.assertNotIn(
                    f"**{title}**",
                    body,
                    msg=f"'{title}' still used as a guardrail label in {md}",
                )

    def test_04_role_threat_table_uses_2025_llm_map(self):
        role = read(ROLE)
        self.assertIn("LLM06/ASI02", role)
        self.assertIn("LLM10 Unbounded Consumption", role)
        self.assertNotIn("(LLM03/ASI02)", role)
        self.assertNotIn("(LLM04)", role)

    def test_05_role_standard_asi_baseline_intact(self):
        standard = read(ROLE_STANDARD)
        for asi_id in ("ASI01", "ASI05", "ASI10"):
            self.assertIn(asi_id, standard)
        self.assertIn("Rogue Agents", standard)


class TestCraCoverage(unittest.TestCase):
    def test_06_role_cra_section_and_dates(self):
        role = read(ROLE)
        self.assertIn("EU Cyber Resilience Act (CRA) Product Compliance", role)
        for date in ("2026-09-11", "2026-12-11", "2027-12-11"):
            self.assertIn(date, role)
        self.assertIn("€15M or 2.5%", role)

    def test_07_cra_lock_present(self):
        self.assertIn("CRA-REPORTING LOCK", read(ROLE))

    def test_08_audit_skill_cra_rule(self):
        body = read(SKILL_AUDIT)
        self.assertIn("EU-CRA-REPORTING", body)
        self.assertIn("2026-09-11", body)


class TestPqcCoverage(unittest.TestCase):
    def test_09_role_pqc_section_pins(self):
        role = read(ROLE)
        self.assertIn("Post-Quantum Cryptography (PQC) Readiness Review", role)
        for pin in (
            "NIST IR 8547",
            "X25519MLKEM768",
            "CBOM",
            "ML-DSA",
            "FIPS 204",
            "2030",
            "2035",
        ):
            self.assertIn(pin, role, msg=f"missing PQC pin: {pin}")

    def test_10_pqc_lock_present(self):
        self.assertIn("PQC-TRANSITION LOCK", read(ROLE))

    def test_11_secrets_crypto_agility(self):
        body = read(SKILL_SECRETS)
        self.assertIn("PQC crypto-agility", body)
        self.assertIn("CBOM", body)
        self.assertIn("version: 2.0.0", body)


class TestSchemaModernization(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(read(SCHEMA))

    def test_12_new_blocks_present(self):
        props = self.schema["properties"]
        for block in ("asi_review", "pqc_readiness", "cra_compliance", "owasp_baseline"):
            self.assertIn(block, props)

    def test_13_audit_type_enum_extended(self):
        enum = self.schema["properties"]["audit_type"]["enum"]
        self.assertIn("agentic_ai_review", enum)
        self.assertIn("infrastructure_review", enum)

    def test_14_finding_fields_extended(self):
        finding_props = self.schema["properties"]["findings"]["items"]["properties"]
        for field in ("exploit_path", "blast_radius", "owasp_ref", "status"):
            self.assertIn(field, finding_props)

    def test_15_required_subfields(self):
        props = self.schema["properties"]
        self.assertEqual(
            props["pqc_readiness"]["required"],
            ["crypto_inventory_present", "hybrid_tls_enabled", "migration_plan_present"],
        )
        self.assertEqual(props["cra_compliance"]["required"], ["in_scope"])
        self.assertEqual(props["asi_review"]["required"], ["asi_items_checked"])

    def test_16_examples_conform(self):
        examples_text = json.dumps(self.schema.get("examples", []))
        for stale in ("audit_id", "owasp_checks", "overall_status", "recommendation"):
            self.assertNotIn(stale, examples_text)
        for example in self.schema["examples"]:
            for field in ("contract_type", "target", "audit_type", "findings", "overall_risk_score"):
                self.assertIn(field, example)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_17_examples_validate_against_schema(self):
        validator = jsonschema.Draft202012Validator(self.schema)
        for example in self.schema["examples"]:
            validator.validate(example)


class TestChecklistAndSkillPins(unittest.TestCase):
    def test_18_checklist_modernization_gates(self):
        body = read(CHECKLIST)
        self.assertIn("2026-10 Modernization Gates", body)
        for gate in (
            "ASI Correctness Gate",
            "CRA Reporting Gate",
            "PQC Transition Gate",
            "Red Teaming Alignment Gate",
            "LLM Top 10 2025 Gate",
        ):
            self.assertIn(gate, body)

    def test_19_pid_skill_camel_and_red_team_manual(self):
        body = read(SKILL_PID)
        self.assertIn("CaMeL", body)
        self.assertIn("arXiv:2503.18813", body)
        self.assertIn("GenAI Red Teaming Manual v1.0", body)
        self.assertIn("version: 2.0.0", body)

    def test_20_role_pins_and_versions(self):
        role = read(ROLE)
        self.assertIn("version: 2.0.0", read(SKILL_AUDIT))
        self.assertIn("Last updated: 2026-10-25", role)
        self.assertIn("OWASP Top 10:2025", role)
        self.assertIn("GenAI Red Teaming Manual v1.0", role)
        self.assertIn("Agent Control Standard (2026-09-01)", role)


if __name__ == "__main__":
    unittest.main()
