"""
Comprehensive Challenge Test Suite for shoppe-team Pack (v5.0.0, Schema v2).
Validates:
1. Manifest Schema v2 compliance, 15 keys, tags, compatibility, governance.
2. Overlay resolution order and disk presence.
3. Activation markers for shoppe ecosystem and live repository consistency.
4. Enterprise README depth (>5000 chars), 4 microservices, 5 VAS financial invariants,
   17 operational roles, Brand Mascot Sóc Mót, and valid Mermaid diagram.
5. Tri-Engine lifecycle workflow structure, 5 phases, contracts, and OWASP ASI security guardrails.
6. Ecosystem integration in packs/README.md and PACK_STATUS.md.
7. Adversarial resilience and negative mutation validation.
"""

import re
import unittest
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = PROJECT_ROOT / "packs"
PACKS_README = PACKS_DIR / "README.md"
PACK_STATUS = PROJECT_ROOT / "PACK_STATUS.md"

SHOPPE_DIR = PACKS_DIR / "shoppe-team"
SHOPPE_MANIFEST = SHOPPE_DIR / "manifest.yaml"
SHOPPE_README = SHOPPE_DIR / "README.md"
SHOPPE_WORKFLOW = SHOPPE_DIR / "workflows" / "shoppe-tri-engine-lifecycle.md"
SHOPPE_REPO = Path("D:/myproject/shoppe")


class TestShoppeManifestSchemaV2(unittest.TestCase):
    """Challenge 1: Verify shoppe-team manifest Schema v2 conformity and metadata."""

    def setUp(self):
        self.assertTrue(SHOPPE_MANIFEST.exists(), "packs/shoppe-team/manifest.yaml must exist")
        with open(SHOPPE_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_01_manifest_exists(self):
        self.assertTrue(SHOPPE_MANIFEST.is_file(), "manifest.yaml must be a file")

    def test_02_schema_v2_and_version(self):
        self.assertEqual(self.manifest.get("schema_version"), "2")
        self.assertEqual(self.manifest.get("version"), "5.0.0")

    def test_03_metadata_identity(self):
        self.assertEqual(self.manifest.get("name"), "shoppe-team")
        desc = self.manifest.get("description", "").lower()
        self.assertIn("tri-engine", desc)
        self.assertIn("motdeal", desc)

    def test_04_required_schema_v2_keys(self):
        required_keys = [
            "schema_version",
            "name",
            "description",
            "version",
            "tags",
            "author",
            "maintained_by",
            "license",
            "homepage",
            "compatibility",
            "includes",
            "capabilities",
            "data_classification",
            "activation",
            "governance",
        ]
        for key in required_keys:
            self.assertIn(key, self.manifest, f"Manifest missing Schema v2 required key: {key}")

    def test_05_tags_taxonomy(self):
        tags = self.manifest.get("tags", [])
        expected_tags = [
            "core",
            "ecommerce",
            "affiliate",
            "cashback",
            "tri-engine",
            "motdeal",
            "double-entry-ledger",
            "vietqr",
            "fastapi",
            "k3s",
        ]
        for tag in expected_tags:
            self.assertIn(tag, tags, f"Tags taxonomy missing expected tag: {tag}")

    def test_06_compatibility_bounds(self):
        compat = self.manifest.get("compatibility", {})
        self.assertEqual(compat.get("min_pack_version"), "4.0.0")
        self.assertEqual(compat.get("max_pack_version"), "5.x")
        self.assertEqual(compat.get("requires_schema"), "2")

    def test_07_capabilities_coverage(self):
        caps = self.manifest.get("capabilities", [])
        expected_caps = [
            "double-entry-ledger",
            "scraper-anti-waf",
            "pwa-chatbot",
            "programmatic-seo",
            "vietqr-napas-247",
            "k3s-docker-ops",
        ]
        for cap in expected_caps:
            self.assertIn(cap, caps, f"Capabilities missing expected entry: {cap}")
        self.assertTrue(
            any("reconciliation" in c for c in caps),
            "Capabilities must cover reconciliation (e.g., t1-reconciliation)",
        )

    def test_08_governance_block(self):
        gov = self.manifest.get("governance", {})
        self.assertEqual(gov.get("eu_ai_act_tier"), "minimal_risk")
        self.assertEqual(gov.get("audit_logging"), "required")
        self.assertEqual(gov.get("audit_format"), "otel-json")
        self.assertEqual(gov.get("retention_days"), 90)
        self.assertEqual(gov.get("secret_handling"), "env_only")

        human = gov.get("human_oversight", {})
        self.assertTrue(human.get("required"), "Human oversight must be required")
        gate_actions = human.get("gate_actions", [])
        self.assertTrue(any("migration" in a for a in gate_actions), "Gate actions must include database migration")
        self.assertTrue(any("production" in a for a in gate_actions), "Gate actions must include production deploy")
        self.assertTrue(any("secret" in a for a in gate_actions), "Gate actions must include secret modification")

        data_policy = PROJECT_ROOT / gov.get("data_policy", "")
        action_policy = PROJECT_ROOT / gov.get("action_policy", "")
        self.assertTrue(data_policy.exists(), f"Referenced data policy must exist: {data_policy}")
        self.assertTrue(action_policy.exists(), f"Referenced action policy must exist: {action_policy}")


class TestShoppeOverlayResolution(unittest.TestCase):
    """Challenge 2: Verify includes order, overlay existence, and validate-packs.py compatibility."""

    def setUp(self):
        with open(SHOPPE_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_01_includes_order(self):
        includes = self.manifest.get("includes", [])
        self.assertGreaterEqual(len(includes), 2, "Includes must contain core and overlays")
        self.assertEqual(includes[0], "core", "First entry in includes MUST be 'core'")

    def test_02_overlays_exist_on_disk(self):
        includes = self.manifest.get("includes", [])
        self.assertIn("overlays/seo-publishing", includes)
        self.assertIn("overlays/ui-design-system", includes)
        for inc in includes:
            if inc == "core":
                self.assertTrue((PROJECT_ROOT / "core").is_dir(), "core directory must exist")
            elif inc.startswith("overlays/"):
                self.assertTrue((PROJECT_ROOT / inc).is_dir(), f"Referenced overlay directory {inc} must exist on disk")

    def test_03_validate_packs_script_compatibility(self):
        text = SHOPPE_MANIFEST.read_text(encoding="utf-8")
        errors = []
        if "name:" not in text:
            errors.append("missing 'name' field")
        if "description:" not in text:
            errors.append("missing 'description' field")
        if "includes:" not in text:
            errors.append("missing 'includes' field")

        for line in text.splitlines():
            stripped = line.strip().lstrip("- ")
            if stripped == "core":
                if not (PROJECT_ROOT / "core").is_dir():
                    errors.append("referenced path does not exist: core")
            elif stripped.startswith("overlays/"):
                if not (PROJECT_ROOT / stripped).is_dir():
                    errors.append(f"referenced overlay does not exist: {stripped}")

        self.assertEqual(errors, [], f"validate-packs.py algorithm detected errors: {errors}")


class TestShoppeActivationMarkers(unittest.TestCase):
    """Challenge 3: Verify activation strategy, markers, globs, and consistency with shoppe repo."""

    def setUp(self):
        with open(SHOPPE_MANIFEST, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_01_activation_strategy(self):
        act = self.manifest.get("activation", {})
        self.assertEqual(act.get("strategy"), "marker_first")

    def test_02_activation_markers_list(self):
        markers = self.manifest.get("activation", {}).get("markers", [])
        expected_markers = [
            "deal-bot-dispatcher/requirements.txt",
            "cashback-api-gateway/requirements.txt",
            "cashback-pwa-web/package.json",
            "pseo-nextjs-engine/package.json",
            "motdeal.com",
        ]
        for marker in expected_markers:
            self.assertIn(marker, markers, f"Activation markers missing: {marker}")

    def test_03_activation_glob_patterns(self):
        globs = self.manifest.get("activation", {}).get("glob_patterns", [])
        self.assertTrue(
            any("*.py" in g for g in globs),
            "Activation glob patterns must cover Python files (*.py)",
        )
        self.assertTrue(
            any("ts" in g for g in globs),
            "Activation glob patterns must cover TypeScript/TSX files",
        )

    def test_04_live_repo_markers_consistency(self):
        if SHOPPE_REPO.exists():
            repo_markers = [
                "deal-bot-dispatcher/requirements.txt",
                "cashback-api-gateway/requirements.txt",
                "cashback-pwa-web/package.json",
                "pseo-nextjs-engine/package.json",
            ]
            for rm in repo_markers:
                target = SHOPPE_REPO / rm
                self.assertTrue(target.exists(), f"Live marker {rm} must exist in {SHOPPE_REPO}")


class TestShoppeReadmeEnterpriseDepth(unittest.TestCase):
    """Challenge 4: Verify README enterprise depth, microservices, 5 VAS invariants, and 17 roles."""

    def setUp(self):
        self.assertTrue(SHOPPE_README.exists(), "packs/shoppe-team/README.md must exist")
        self.text = SHOPPE_README.read_text(encoding="utf-8")

    def test_01_readme_exists_and_depth(self):
        self.assertGreaterEqual(
            len(self.text),
            5000,
            f"README.md length ({len(self.text)} chars) must exceed 5000 characters",
        )

    def test_02_zero_placeholders(self):
        forbidden_placeholders = [
            "[TBD]",
            "TODO",
            "FIXME",
            "<placeholder>",
            "dummy_impl",
            "mock_impl",
        ]
        for ph in forbidden_placeholders:
            self.assertNotIn(ph, self.text, f"README.md contains forbidden placeholder: {ph}")

    def test_03_four_microservices_documented(self):
        microservices = [
            "deal-bot-dispatcher",
            "cashback-api-gateway",
            "cashback-pwa-web",
            "pseo-nextjs-engine",
        ]
        for ms in microservices:
            self.assertIn(ms, self.text, f"Microservice {ms} must be documented in README.md")

    def test_04_five_vas_invariants_documented(self):
        # Code reference assertions
        self.assertIn("ledger_engine.py", self.text)
        self.assertIn("state_machine.py", self.text)
        self.assertIn("withdrawals.py", self.text)
        self.assertIn("layout.tsx", self.text)

        # Invariant exception names and constraints
        self.assertIn("LedgerUnbalancedException", self.text)
        self.assertIn("NegativeBalanceException", self.text)
        self.assertIn("chk_user_clawback_debt_positive", self.text)
        self.assertIn("with_for_update", self.text)
        self.assertIn("motdeal.com", self.text)

    def test_05_seventeen_operational_roles(self):
        roles = [
            "researcher",
            "reviewer",
            "seo-analyst",
            "product-manager",
            "project-manager",
            "business-analyst",
            "solution-architect",
            "technical-architect",
            "technical-lead",
            "backend-developer",
            "frontend-developer",
            "sre",
            "system-engineer",
            "task-planner",
            "teacher",
            "content-manager",
            "content-writer",
        ]
        for role in roles:
            self.assertIn(f"@{role}", self.text, f"Operational role @{role} must be present in README.md")

        # Mascot branding
        self.assertIn("Sóc Mót", self.text, "Brand mascot Sóc Mót must be documented")

    def test_06_mermaid_diagram(self):
        self.assertIn("```mermaid", self.text, "README.md must contain a Mermaid diagram block")
        self.assertIn("flowchart", self.text, "Mermaid diagram must use flowchart syntax")


class TestShoppeTriEngineLifecycleWorkflow(unittest.TestCase):
    """Challenge 5: Verify lifecycle workflow frontmatter, mandatory sections, 5 phases, and OWASP ASI."""

    def setUp(self):
        self.assertTrue(SHOPPE_WORKFLOW.exists(), "Workflow file must exist")
        self.text = SHOPPE_WORKFLOW.read_text(encoding="utf-8")

    def test_01_workflow_file_exists(self):
        self.assertTrue(SHOPPE_WORKFLOW.is_file())

    def test_02_workflow_frontmatter_and_heading(self):
        self.assertTrue(self.text.startswith("---"), "Workflow must begin with YAML frontmatter")
        self.assertIn("description:", self.text)
        self.assertIn("shoppe-tri-engine-lifecycle", self.text)
        self.assertIn("Lifecycle", self.text)

    def test_03_mandatory_sections(self):
        mandatory = [
            "Prerequisites",
            "Workflow Steps",
            "Checklist",
            "Related Workflows",
            "Related Skills",
            "Failure Modes",
            "Output Contracts",
            "Security Guardrails",
        ]
        for sec in mandatory:
            self.assertTrue(
                any(sec.lower() in line.lower() for line in self.text.splitlines()),
                f"Workflow missing mandatory section: {sec}",
            )
        self.assertIn("OWASP ASI", self.text)

    def test_04_five_phases_coverage(self):
        phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]
        for p in phases:
            self.assertIn(p, self.text, f"Workflow must define {p}")
        self.assertIn("Ingestion", self.text)
        self.assertIn("Ledger", self.text)
        self.assertIn("PWA", self.text)
        self.assertIn("SEO", self.text)
        self.assertIn("Reconciliation", self.text)

    def test_05_contracts_and_owasp_guardrails(self):
        contracts = [
            "feature-ticket.json",
            "api-contract-spec.json",
            "implementation-result.json",
            "period-end-closing-report.json",
        ]
        for contract in contracts:
            self.assertIn(contract, self.text, f"Workflow must cite output contract: {contract}")

        owasp_guards = ["ASI01", "ASI02", "ASI03", "ASI05", "ASI06", "ASI09"]
        for guard in owasp_guards:
            self.assertIn(guard, self.text, f"Workflow must cite OWASP guardrail: {guard}")


class TestShoppeEcosystemIntegrationAndSpotlight(unittest.TestCase):
    """Challenge 6: Verify registration in packs/README.md, spotlight, PACK_STATUS.md, and version sync."""

    def test_01_packs_readme_registration(self):
        self.assertTrue(PACKS_README.exists())
        content = PACKS_README.read_text(encoding="utf-8")
        self.assertIn("`shoppe-team`", content)
        self.assertIn("[manifest.yaml](shoppe-team/manifest.yaml)", content)
        self.assertIn("## Available Packs (17)", content)

    def test_02_packs_readme_spotlight(self):
        content = PACKS_README.read_text(encoding="utf-8")
        self.assertIn("### Pack Spotlight: shoppe-team (v5.0.0)", content)
        self.assertIn("Tri-Engine", content)
        self.assertIn("Sóc Mót", content)

    def test_03_pack_status_registration(self):
        self.assertTrue(PACK_STATUS.exists())
        content = PACK_STATUS.read_text(encoding="utf-8")
        self.assertIn("shoppe-team", content)
        self.assertIn("17 packs", content)

    def test_04_version_sync_compliance(self):
        version_pattern = re.compile(r"agent-skills[ @v]+([0-9]+\.[0-9]+\.[0-9]+)")
        for file_path in SHOPPE_DIR.rglob("*"):
            if file_path.is_file() and file_path.suffix in (".md", ".yaml", ".yml", ".json"):
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                for match in version_pattern.finditer(text):
                    referenced_version = match.group(1)
                    self.assertEqual(
                        referenced_version,
                        "5.0.0",
                        f"{file_path}: references pack version {referenced_version} != 5.0.0",
                    )


class TestShoppeAdversarialResilience(unittest.TestCase):
    """Challenge 7: Negative mutation tests and security resilience."""

    def setUp(self):
        self.manifest_text = SHOPPE_MANIFEST.read_text(encoding="utf-8")

    def _run_manifest_validator_rules(self, text: str) -> list[str]:
        errors = []
        if "name:" not in text:
            errors.append("missing 'name' field")
        if "description:" not in text:
            errors.append("missing 'description' field")
        if "includes:" not in text:
            errors.append("missing 'includes' field")

        for line in text.splitlines():
            stripped = line.strip().lstrip("- ")
            if stripped == "core":
                if not (PROJECT_ROOT / "core").is_dir():
                    errors.append("referenced path does not exist: core")
            elif stripped.startswith("overlays/"):
                if not (PROJECT_ROOT / stripped).is_dir():
                    errors.append(f"referenced overlay does not exist: {stripped}")
        return errors

    def test_01_negative_missing_name_rejected(self):
        mutated = "\n".join(line for line in self.manifest_text.splitlines() if not line.startswith("name:"))
        errors = self._run_manifest_validator_rules(mutated)
        self.assertTrue(any("missing 'name' field" in e for e in errors))

    def test_02_negative_missing_includes_rejected(self):
        mutated = "\n".join(line for line in self.manifest_text.splitlines() if not line.startswith("includes:"))
        errors = self._run_manifest_validator_rules(mutated)
        self.assertTrue(any("missing 'includes' field" in e for e in errors))

    def test_03_negative_nonexistent_overlay_rejected(self):
        mutated = self.manifest_text + "\n  - overlays/nonexistent-invalid-overlay-12345\n"
        errors = self._run_manifest_validator_rules(mutated)
        self.assertTrue(any("referenced overlay does not exist" in e for e in errors))

    def test_04_negative_unauthorized_domain_leak(self):
        # Assert no unauthorized fake domains are set as primary target
        unauthorized_domains = [
            "motdeal.net",
            "shoppe.vn",
            "shopee-fake.com",
            "shopee.com.vn",
        ]
        for domain in unauthorized_domains:
            self.assertNotIn(domain, self.manifest_text)
            self.assertNotIn(domain, SHOPPE_WORKFLOW.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
