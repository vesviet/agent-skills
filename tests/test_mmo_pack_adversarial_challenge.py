"""
Adversarial Challenge & Stress Test Suite for MMO Ecosystem (v5.0.0).

Empirical verification covering:
1. Strict line count assertions (< 200 lines) for all 7 modernized MMO skills.
2. Adversarial schema fuzzing against mmo-campaign-spec.json and mmo-roi-report.json
   via Draft202012Validator:
   - Missing required fields (root and nested objects) -> ValidationError
   - Invalid discriminator ('const' violations) -> ValidationError
   - Negative amounts & out-of-bounds metrics -> ValidationError
   - Corrupted regex patterns and enums -> ValidationError
   - Valid payloads pass cleanly
3. Fast alias resolution across adapters/antigravity/role-skill-index.json.
4. Non-trivial assertion verification for test_mmo_pack_challenge.py.
"""

import ast
import copy
import json
import unittest
from pathlib import Path
import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "core" / "skills" / "mmo"
ROLES_DIR = PROJECT_ROOT / "core" / "roles"
WORKFLOWS_DIR = PROJECT_ROOT / "core" / "workflows"
SCHEMAS_DIR = PROJECT_ROOT / "core" / "contracts" / "schemas"
INDEX_PATH = PROJECT_ROOT / "adapters" / "antigravity" / "role-skill-index.json"
CHALLENGE_TEST_FILE = PROJECT_ROOT / "tests" / "test_mmo_pack_challenge.py"

MMO_SKILL_NAMES = [
    "setup-tracking-system",
    "create-automation-script",
    "deploy-mmo-infrastructure",
    "manage-mmo-assets",
    "deploy-proxyware-fleet",
    "generate-mmo-content",
    "analyze-campaign-roi",
]


class TestMMOSkillLineLimitsAdversarial(unittest.TestCase):
    """Stress test: Every MMO skill must strictly have < 200 lines."""

    def test_all_mmo_skills_under_200_lines(self):
        line_counts = {}
        for skill_name in MMO_SKILL_NAMES:
            skill_file = SKILLS_DIR / skill_name / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"SKILL.md missing for {skill_name}")
            content = skill_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            count = len(lines)
            line_counts[skill_name] = count
            self.assertLess(
                count,
                200,
                f"Skill '{skill_name}' exceeds line limit: {count} lines >= 200"
            )
            self.assertGreater(
                count,
                50,
                f"Skill '{skill_name}' is suspiciously short: {count} lines"
            )


class TestMMOCampaignSpecSchemaAdversarial(unittest.TestCase):
    """Adversarial stress testing for mmo-campaign-spec.json schema."""

    def setUp(self):
        schema_path = SCHEMAS_DIR / "mmo-campaign-spec.json"
        self.assertTrue(schema_path.exists())
        self.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(self.schema)
        self.validator = Draft202012Validator(self.schema)
        self.valid_payload = copy.deepcopy(self.schema["examples"][0])

    def test_valid_payload_passes(self):
        errors = list(self.validator.iter_errors(self.valid_payload))
        self.assertEqual(len(errors), 0, f"Valid payload had unexpected errors: {errors}")

    def test_missing_top_level_required_fields(self):
        required_fields = self.schema.get("required", [])
        self.assertGreater(len(required_fields), 5)
        for field in required_fields:
            corrupted = copy.deepcopy(self.valid_payload)
            del corrupted[field]
            with self.subTest(missing_field=field):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(
                    len(errors),
                    0,
                    f"Removing top-level required field '{field}' should have raised ValidationError"
                )

    def test_missing_nested_required_fields(self):
        nested_checks = [
            ("network_platform", "platform_name"),
            ("network_platform", "payout_type"),
            ("network_platform", "base_payout_amount"),
            ("network_platform", "currency"),
            ("audience_targeting", "geos"),
            ("content_and_creative_spec", "page_type"),
            ("tracking_architecture", "tracker_type"),
            ("tracking_architecture", "s2s_endpoints"),
            ("tracking_architecture", "click_id_parameter"),
            ("tracking_architecture", "ctit_min_threshold_seconds"),
            ("infrastructure_and_stealth", "proxy_type"),
            ("infrastructure_and_stealth", "anti_detect_provider"),
            ("infrastructure_and_stealth", "canvas_noise_mode"),
            ("budget_and_economics", "daily_ad_spend_cap"),
            ("budget_and_economics", "target_blended_roas"),
            ("budget_and_economics", "max_acceptable_die_rate"),
            ("budget_and_economics", "currency"),
            ("risk_and_guardrails", "action_boundary_level"),
            ("risk_and_guardrails", "review_system_lock"),
            ("risk_and_guardrails", "data_classification"),
        ]
        for section, key in nested_checks:
            corrupted = copy.deepcopy(self.valid_payload)
            if key in corrupted[section]:
                del corrupted[section][key]
                with self.subTest(section=section, missing_nested_key=key):
                    errors = list(self.validator.iter_errors(corrupted))
                    self.assertGreater(
                        len(errors),
                        0,
                        f"Removing nested field '{section}.{key}' should have caused validation error"
                    )

    def test_invalid_contract_discriminator(self):
        corrupted = copy.deepcopy(self.valid_payload)
        corrupted["contract_type"] = "invalid-spec-discriminator"
        errors = list(self.validator.iter_errors(corrupted))
        self.assertGreater(len(errors), 0, "Invalid contract_type must fail validation")

    def test_invalid_review_system_lock_const(self):
        corrupted = copy.deepcopy(self.valid_payload)
        corrupted["risk_and_guardrails"]["review_system_lock"] = False
        errors = list(self.validator.iter_errors(corrupted))
        self.assertGreater(len(errors), 0, "review_system_lock=False must violate const:true")

    def test_negative_and_out_of_bounds_numbers(self):
        bad_numeric_cases = [
            ("network_platform", "base_payout_amount", -10.0, "base_payout_amount cannot be negative"),
            ("budget_and_economics", "daily_ad_spend_cap", -50.0, "daily_ad_spend_cap cannot be negative"),
            ("budget_and_economics", "target_blended_roas", 0.5, "target_blended_roas must be >= 1.0"),
            ("budget_and_economics", "max_acceptable_die_rate", -0.1, "max_acceptable_die_rate cannot be < 0"),
            ("budget_and_economics", "max_acceptable_die_rate", 1.5, "max_acceptable_die_rate cannot be > 1.0"),
            ("tracking_architecture", "ctit_min_threshold_seconds", 0.2, "ctit_min_threshold_seconds must be >= 1.0"),
        ]
        for section, key, bad_val, msg in bad_numeric_cases:
            corrupted = copy.deepcopy(self.valid_payload)
            corrupted[section][key] = bad_val
            with self.subTest(case=f"{section}.{key}={bad_val}"):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(len(errors), 0, msg)

    def test_regex_pattern_violations(self):
        bad_ids = ["INVALID_ID", "mmo_underscore", "mmo-UPPERCASE", "campaign-without-prefix"]
        for bad_id in bad_ids:
            corrupted = copy.deepcopy(self.valid_payload)
            corrupted["campaign_id"] = bad_id
            with self.subTest(campaign_id=bad_id):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(len(errors), 0, f"campaign_id '{bad_id}' must violate pattern")

    def test_enum_violations(self):
        bad_enums = [
            ("target_vertical", "crypto-ponzi"),
            ("risk_and_guardrails", "unknown-risk-tier", "action_boundary_level"),
        ]
        corrupted = copy.deepcopy(self.valid_payload)
        corrupted["target_vertical"] = "crypto-ponzi"
        self.assertGreater(len(list(self.validator.iter_errors(corrupted))), 0)


class TestMMOROIReportSchemaAdversarial(unittest.TestCase):
    """Adversarial stress testing for mmo-roi-report.json schema."""

    def setUp(self):
        schema_path = SCHEMAS_DIR / "mmo-roi-report.json"
        self.assertTrue(schema_path.exists())
        self.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(self.schema)
        self.validator = Draft202012Validator(self.schema)
        self.valid_payload = copy.deepcopy(self.schema["examples"][0])

    def test_valid_payload_passes(self):
        errors = list(self.validator.iter_errors(self.valid_payload))
        self.assertEqual(len(errors), 0, f"Valid ROI payload had unexpected errors: {errors}")

    def test_missing_top_level_required_fields(self):
        required_fields = self.schema.get("required", [])
        self.assertGreater(len(required_fields), 5)
        for field in required_fields:
            corrupted = copy.deepcopy(self.valid_payload)
            del corrupted[field]
            with self.subTest(missing_field=field):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(
                    len(errors),
                    0,
                    f"Removing top-level field '{field}' from ROI report should raise ValidationError"
                )

    def test_missing_nested_operational_costs(self):
        op_keys = ["proxy_bandwidth_cost", "ai_token_api_cost", "account_die_rate_amortized_cost"]
        for key in op_keys:
            corrupted = copy.deepcopy(self.valid_payload)
            del corrupted["financial_metrics"]["operational_costs"][key]
            with self.subTest(missing_operational_cost=key):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(
                    len(errors),
                    0,
                    f"Removing operational cost '{key}' should trigger ValidationError"
                )

    def test_invalid_contract_discriminator(self):
        corrupted = copy.deepcopy(self.valid_payload)
        corrupted["contract_type"] = "unsupported-report-type"
        errors = list(self.validator.iter_errors(corrupted))
        self.assertGreater(len(errors), 0, "Invalid contract_type must fail validation")

    def test_negative_operational_costs_and_metrics(self):
        bad_cases = [
            ("financial_metrics.operational_costs.proxy_bandwidth_cost", ["financial_metrics", "operational_costs", "proxy_bandwidth_cost"], -10.0),
            ("financial_metrics.operational_costs.ai_token_api_cost", ["financial_metrics", "operational_costs", "ai_token_api_cost"], -5.0),
            ("financial_metrics.operational_costs.account_die_rate_amortized_cost", ["financial_metrics", "operational_costs", "account_die_rate_amortized_cost"], -25.0),
            ("attribution_and_tracking_health.total_clicks", ["attribution_and_tracking_health", "total_clicks"], -1),
            ("attribution_and_tracking_health.total_conversions", ["attribution_and_tracking_health", "total_conversions"], -10),
            ("attribution_and_tracking_health.event_match_quality_score (negative)", ["attribution_and_tracking_health", "event_match_quality_score"], -0.5),
            ("attribution_and_tracking_health.event_match_quality_score (>10)", ["attribution_and_tracking_health", "event_match_quality_score"], 10.5),
            ("attribution_and_tracking_health.ctit_sivt_excluded_count", ["attribution_and_tracking_health", "ctit_sivt_excluded_count"], -3),
            ("account_health_and_infra.active_profiles", ["account_health_and_infra", "active_profiles"], -1),
            ("account_health_and_infra.banned_profiles_period", ["account_health_and_infra", "banned_profiles_period"], -2),
            ("account_health_and_infra.die_rate_percentage (>100)", ["account_health_and_infra", "die_rate_percentage"], 110.0),
            ("account_health_and_infra.die_rate_percentage (<0)", ["account_health_and_infra", "die_rate_percentage"], -1.0),
            ("optimization_decision.next_budget_allocation", ["optimization_decision", "next_budget_allocation"], -100.0),
        ]
        for label, path_keys, bad_val in bad_cases:
            corrupted = copy.deepcopy(self.valid_payload)
            target = corrupted
            for k in path_keys[:-1]:
                target = target[k]
            target[path_keys[-1]] = bad_val
            with self.subTest(case=label):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(len(errors), 0, f"Case '{label}' with value {bad_val} must be rejected")

    def test_regex_pattern_violations(self):
        bad_ids = ["ROI_UPPERCASE", "roi_with_underscores", "report-without-prefix", "roi-$$$"]
        for bad_id in bad_ids:
            corrupted = copy.deepcopy(self.valid_payload)
            corrupted["report_id"] = bad_id
            with self.subTest(report_id=bad_id):
                errors = list(self.validator.iter_errors(corrupted))
                self.assertGreater(len(errors), 0, f"report_id '{bad_id}' must violate pattern")


class TestFastAliasResolutionAdversarial(unittest.TestCase):
    """Verify that every declared MMO alias in role-skill-index.json resolves correctly."""

    def setUp(self):
        self.assertTrue(INDEX_PATH.exists(), "role-skill-index.json must exist")
        self.index_data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        self.role_aliases = self.index_data.get("role_aliases", {})
        self.skill_aliases = self.index_data.get("skill_aliases", {})

    def test_all_mmo_role_aliases_resolve_to_existing_roles(self):
        mmo_role_aliases = {
            "mmo": "mmo-engineer",
            "affiliate": "mmo-engineer",
            "growth": "mmo-engineer",
            "growth-lead": "mmo-engineer",
            "growth-engineer": "mmo-engineer",
            "media-buyer": "mmo-engineer",
            "affiliate-marketer": "mmo-engineer",
        }
        for alias, expected_target in mmo_role_aliases.items():
            resolved = self.role_aliases.get(alias)
            self.assertEqual(
                resolved,
                expected_target,
                f"Role alias '{alias}' must resolve to '{expected_target}' (got '{resolved}')"
            )
            target_role_file = ROLES_DIR / f"{expected_target}.md"
            self.assertTrue(
                target_role_file.exists(),
                f"Resolved role file '{target_role_file}' does not exist on disk"
            )

    def test_all_mmo_skill_aliases_resolve_to_existing_skills(self):
        mmo_skill_aliases = {
            "roi": ["analyze-campaign-roi"],
            "tracking": ["setup-tracking-system"],
            "stealth_automation": ["create-automation-script"],
            "mmo_infra": ["deploy-mmo-infrastructure"],
            "proxy_fleet": ["deploy-proxyware-fleet"],
            "mmo_content": ["generate-mmo-content"],
            "mmo_assets": ["manage-mmo-assets"],
            "s2s_tracking": ["setup-tracking-system"],
            "depin_bandwidth": ["deploy-proxyware-fleet"],
            "pseo_landing": ["generate-mmo-content"],
            "vcc_isolation": ["manage-mmo-assets"],
            "mmo_campaign": ["setup-tracking-system", "generate-mmo-content", "analyze-campaign-roi"],
            "mmo_growth": ["deploy-mmo-infrastructure", "create-automation-script", "setup-tracking-system"],
            "growth_stack": ["setup-tracking-system", "analyze-campaign-roi"],
        }
        for alias, expected_targets in mmo_skill_aliases.items():
            resolved = self.skill_aliases.get(alias)
            self.assertEqual(
                resolved,
                expected_targets,
                f"Skill alias '{alias}' must resolve to '{expected_targets}' (got '{resolved}')"
            )
            for skill_id in resolved:
                skill_path = SKILLS_DIR / skill_id / "SKILL.md"
                self.assertTrue(
                    skill_path.exists(),
                    f"Resolved skill '{skill_id}' for alias '{alias}' does not exist at {skill_path}"
                )


class TestChallengeTestSuiteAuthenticity(unittest.TestCase):
    """Empirical audit of test_mmo_pack_challenge.py assertions."""

    def test_no_trivial_passes_and_high_assertion_density(self):
        self.assertTrue(CHALLENGE_TEST_FILE.exists())
        tree = ast.parse(CHALLENGE_TEST_FILE.read_text(encoding="utf-8"))

        assertions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr.startswith("assert"):
                    assertions.append((node.lineno, node.func.attr, ast.unparse(node)))
            elif isinstance(node, ast.Assert):
                assertions.append((node.lineno, "assert", ast.unparse(node)))

        self.assertGreaterEqual(
            len(assertions),
            50,
            f"Expected at least 50 assertions in test_mmo_pack_challenge.py (got {len(assertions)})"
        )

        trivial_patterns = {"assert True", "self.assertTrue(True)", "self.assertEqual(True, True)"}
        for lineno, kind, code in assertions:
            self.assertNotIn(
                code,
                trivial_patterns,
                f"Found trivial assertion at line {lineno}: {code}"
            )


if __name__ == "__main__":
    unittest.main()
