#!/usr/bin/env python3
"""Adversarial Verification Suite for Milestone M2.

Empirical verification of:
1. Clean execution and idempotence of generate-a2a-registry.py and generate-index.py.
2. Proper binding and extractability of legal schemas in A2A registry and agent cards.
3. Perfect catalog count synchronization in core/skills/README.md vs disk.
4. Comprehensive statutory content and structural invariants for Vietnam Legal Counsel.
5. Exit code 0 of validate-all.py (all 16+ gates).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
SCHEMAS_DIR = CORE_DIR / "contracts" / "schemas"
ROLES_DIR = CORE_DIR / "roles"
SKILLS_DIR = CORE_DIR / "skills"
A2A_DIR = CORE_DIR / "a2a"
REGISTRY_DIR = A2A_DIR / "registry"
WELL_KNOWN_DIR = A2A_DIR / ".well-known"
ADAPTERS_DIR = REPO_ROOT / "adapters"
SCRIPTS_DIR = CORE_DIR / "scripts"


def load_json(path: Path) -> dict:
    assert path.is_file(), f"Missing JSON file: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict:
    assert path.is_file(), f"Missing YAML file: {path}"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ==============================================================================
# 1. GENERATOR CLEAN EXECUTION & IDEMPOTENCE
# ==============================================================================

class TestGeneratorExecutionAndIdempotence:
    """Empirically test that registry and index generators run cleanly and produce no drift."""

    def test_generate_a2a_registry_runs_cleanly(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate-a2a-registry.py")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"generate-a2a-registry.py failed:\n{result.stderr}\n{result.stdout}"
        assert "Generated 35 agent cards" in result.stdout
        assert "Canonical A2A endpoint:" in result.stdout

    def test_generate_index_runs_cleanly(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate-index.py")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"generate-index.py failed:\n{result.stderr}\n{result.stdout}"
        assert "Loaded 35 roles, 135 skills, 25 workflows, 54 schemas." in result.stdout

    def test_generate_index_check_flag(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate-index.py"), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"generate-index.py --check detected stale files:\n{result.stderr}\n{result.stdout}"
        assert "Generated artifacts are up to date." in result.stdout


# ==============================================================================
# 2. SCHEMA BINDING & EXTRACTABILITY IN A2A REGISTRY
# ==============================================================================

class TestSchemaBindingAndExtractability:
    """Verify that legal-compliance-review.json and legal-opinion-contract.json are bound and extractable."""

    def test_schemas_exist_and_are_valid_draft202012(self):
        for schema_name in ["legal-compliance-review.json", "legal-opinion-contract.json"]:
            path = SCHEMAS_DIR / schema_name
            assert path.is_file(), f"Schema file not found: {path}"
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"

    def test_vietnam_legal_counsel_agent_card_schema_bindings(self):
        card_path = REGISTRY_DIR / "vietnam-legal-counsel.agent-card.json"
        assert card_path.is_file(), f"Missing agent card: {card_path}"
        card = load_json(card_path)

        # 1. defaultOutputSchemas must contain both schemas
        default_schemas = card.get("defaultOutputSchemas", [])
        assert "legal-compliance-review.json" in default_schemas
        assert "legal-opinion-contract.json" in default_schemas

        # 2. Each legal skill in the card must bind these schemas
        skills = {s["id"]: s for s in card.get("skills", [])}
        assert "manage-vietnam-legal" in skills
        assert "audit-ai-compliance" in skills
        assert "draft-legal-opinion" in skills

        for skill_id in ["manage-vietnam-legal", "audit-ai-compliance", "draft-legal-opinion"]:
            refs = skills[skill_id].get("output_schema_refs", [])
            assert "legal-compliance-review.json" in refs, f"{skill_id} missing legal-compliance-review.json ref"
            assert "legal-opinion-contract.json" in refs, f"{skill_id} missing legal-opinion-contract.json ref"

    def test_a2a_role_skill_indexes_include_schemas(self):
        for index_path in [
            WELL_KNOWN_DIR / "role-skill-index.json",
            ADAPTERS_DIR / "antigravity" / "role-skill-index.json",
        ]:
            data = load_json(index_path)
            schemas = data.get("schemas", {})
            assert "legal-compliance-review.json" in schemas, f"Missing in {index_path}"
            assert "legal-opinion-contract.json" in schemas, f"Missing in {index_path}"

            rev_entry = schemas["legal-compliance-review.json"]
            assert rev_entry["file"] == "core/contracts/schemas/legal-compliance-review.json"
            assert (REPO_ROOT / rev_entry["file"]).is_file()

            op_entry = schemas["legal-opinion-contract.json"]
            assert op_entry["file"] == "core/contracts/schemas/legal-opinion-contract.json"
            assert (REPO_ROOT / op_entry["file"]).is_file()

    def test_schema_extractability_and_sample_validation(self):
        """Simulate an external client extracting schemas from A2A card and validating payloads."""
        card = load_json(REGISTRY_DIR / "vietnam-legal-counsel.agent-card.json")
        for schema_ref in card["defaultOutputSchemas"]:
            schema_file = SCHEMAS_DIR / schema_ref
            assert schema_file.is_file()
            schema = load_json(schema_file)
            validator = Draft202012Validator(schema)

            # Test validating bundled example
            examples = schema.get("examples", [])
            assert len(examples) > 0
            for eg in examples:
                validator.validate(eg)

            # Adversarial test: verify that missing required field is rejected
            bad_eg = dict(examples[0])
            del bad_eg["contract_type"]
            with pytest.raises(ValidationError):
                validator.validate(bad_eg)


# ==============================================================================
# 3. CATALOG COUNTS VS DISK REALITY
# ==============================================================================

class TestCatalogCountsAccuracy:
    """Verify that core/skills/README.md catalog counts match disk exactly."""

    def test_core_skills_readme_summary_line(self):
        readme_text = (SKILLS_DIR / "README.md").read_text(encoding="utf-8")
        counts_match = re.search(
            r"\*\*Counts:\*\*\s*(\d+)\s*portable core skills.*?core/skills/.*?\+\s*(\d+)\s*overlay skills.*?=\s*\*\*(\d+)\s*total\*\*",
            readme_text,
        )
        assert counts_match is not None, "Counts summary line missing or malformed in core/skills/README.md"
        core_c, overlay_c, total_c = (int(g) for g in counts_match.groups())

        # Count disk
        disk_core = sum(
            1 for p in SKILLS_DIR.glob("*/*/SKILL.md")
            if p.is_file()
        )
        disk_overlay = sum(
            1 for p in REPO_ROOT.glob("overlays/*/skills/*/SKILL.md")
            if p.is_file()
        )
        assert core_c == disk_core == 123, f"Core counts mismatch: README declared {core_c}, disk has {disk_core}"
        assert overlay_c == disk_overlay == 12, f"Overlay counts mismatch: README declared {overlay_c}, disk has {disk_overlay}"
        assert total_c == disk_core + disk_overlay == 135

    def test_legal_compliance_category_count_and_items(self):
        readme_text = (SKILLS_DIR / "README.md").read_text(encoding="utf-8")
        m = re.search(r"### Legal Compliance \((\d+)\)", readme_text)
        assert m is not None, "### Legal Compliance (N) section missing in core/skills/README.md"
        assert int(m.group(1)) == 3, f"Legal Compliance count should be 3, found {m.group(1)}"

        # Verify disk directory
        legal_dir = SKILLS_DIR / "legal-compliance"
        skills_on_disk = sorted(d.name for d in legal_dir.iterdir() if d.is_dir() and (d / "SKILL.md").is_file())
        assert skills_on_disk == ["audit-ai-compliance", "draft-legal-opinion", "manage-vietnam-legal"]

        # Verify listed in section
        legal_section = readme_text.split("### Legal Compliance (3)")[1].split("##")[0]
        for s in skills_on_disk:
            assert f"- `{s}`" in legal_section

    def test_all_categories_in_readme_match_disk(self):
        readme_text = (SKILLS_DIR / "README.md").read_text(encoding="utf-8")
        sections = re.split(r"(?m)^### ", readme_text)[1:]

        for s in sections:
            header = s.split("\n", 1)[0].strip()
            m = re.match(r"([A-Za-z ]+) \((\d+)\)", header)
            if not m:
                continue
            cat_name = m.group(1).strip()
            declared_count = int(m.group(2))

            # Normalize to directory name
            dir_name = cat_name.lower().replace(" and ", "-").replace(" ", "-")
            if dir_name == "domain-cluster-notes":
                continue

            target_dir = SKILLS_DIR / dir_name
            if not target_dir.is_dir():
                continue

            disk_skills = [d.name for d in target_dir.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()]
            assert len(disk_skills) == declared_count, (
                f"Category {cat_name} ({dir_name}) count mismatch: declared {declared_count}, disk {len(disk_skills)}"
            )


# ==============================================================================
# 4. STATUTORY CONTENT & SKILL IMPLEMENTATION INVARIANTS
# ==============================================================================

class TestStatutoryContentAndSkillInvariants:
    """Verify specific required statutory references and structure."""

    def test_audit_ai_compliance_skill(self):
        skill_dir = SKILLS_DIR / "legal-compliance" / "audit-ai-compliance"
        skill_file = skill_dir / "SKILL.md"
        assert skill_file.is_file()

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 200, f"SKILL.md exceeds 200 lines: {len(lines)}"

        content = "\n".join(lines)
        assert "name: audit-ai-compliance" in content
        assert "Law on Artificial Intelligence No. 134/2025/QH15" in content
        assert "contracts/schemas/legal-compliance-review.json" in content
        assert "produced_by_role: vietnam-legal-counsel" in content

        # Check tools
        meta, _body, _err = parse_frontmatter(content)
        assert set(meta.get("allowed-tools", [])) == {"read_file", "write_file", "edit_file", "create_file", "search_code"}

        # Companion files
        assert (skill_dir / "agents" / "openai.yaml").is_file()
        assert (skill_dir / "references" / "ai-law-compliance-guide.md").is_file()

    def test_draft_legal_opinion_skill(self):
        skill_dir = SKILLS_DIR / "legal-compliance" / "draft-legal-opinion"
        skill_file = skill_dir / "SKILL.md"
        assert skill_file.is_file()

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 200, f"SKILL.md exceeds 200 lines: {len(lines)}"

        content = "\n".join(lines)
        assert "name: draft-legal-opinion" in content
        assert "contracts/schemas/legal-opinion-contract.json" in content
        assert "produced_by_role: vietnam-legal-counsel" in content

        meta, _body, _err = parse_frontmatter(content)
        assert set(meta.get("allowed-tools", [])) == {"read_file", "write_file", "edit_file", "create_file", "search_code"}

        assert (skill_dir / "agents" / "openai.yaml").is_file()
        assert (skill_dir / "references" / "legal-opinion-guide.md").is_file()

    def test_manage_vietnam_legal_skill_upgrades(self):
        skill_file = SKILLS_DIR / "legal-compliance" / "manage-vietnam-legal" / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert len(lines) < 200

        assert "0.5. AI Law 134/2025 Risk-Tier Pre-Screening" in content
        assert "PDPL 2025 & Decree 356 Compliance Audit" in content
        assert "PDPL 2025 business eligibility gap" in content
        assert "AI Law incident reporting miss" in content

        meta, _body, _err = parse_frontmatter(content)
        assert "edit_file" in meta.get("allowed-tools", [])

    def test_statutory_checklists_content(self):
        checklist_path = SKILLS_DIR / "legal-compliance" / "manage-vietnam-legal" / "references" / "statutory-checklists.md"
        assert checklist_path.is_file()
        content = checklist_path.read_text(encoding="utf-8")

        assert "PDPL No. 91/2025/QH15 + Decree 356/2025/ND-CP" in content
        assert "5. AI Law No. 134/2025/QH15 Compliance Checklist" in content
        assert "5.1 Risk-Tier Classification Matrix" in content
        assert "5.2 High-Risk AI Obligations Checklist" in content
        assert "5.3 Medium-Risk AI Obligations Checklist" in content
        assert "5.4 Incident Reporting Timeline Table" in content
        assert "5.5 Grace Period Compliance Tracker" in content
        assert "5.6 Regulatory Authority Governance Architecture" in content

    def test_vietnam_legal_counsel_role(self):
        role_path = ROLES_DIR / "vietnam-legal-counsel.md"
        content = role_path.read_text(encoding="utf-8")

        # Primary skills
        assert "- `manage-vietnam-legal`" in content
        assert "- `audit-ai-compliance`" in content
        assert "- `draft-legal-opinion`" in content

        # Guardrails
        assert "AI-LAW-RISK-TIER LOCK" in content
        assert "PDPL-2025-CONSENT LOCK" in content

        # Single Last updated footer
        footers = re.findall(r"(?m)^Last updated: \d{4}-\d{2}-\d{2}$", content)
        assert len(footers) == 1, f"Expected exactly one Last updated footer, found {len(footers)}"
        assert content.strip().endswith(footers[0]), "Footer is not the last line of the role file"

    def test_review_checklist_expansion(self):
        checklist_path = ROLES_DIR / "references" / "vietnam-legal-counsel-review-checklist.md"
        assert checklist_path.is_file()
        content = checklist_path.read_text(encoding="utf-8")

        # 6 sections
        for s in [
            "1. Jurisdiction & Entity Verification",
            "2. Statutory Basis & Gazette Verification",
            "3. Commercial Contract Compliance",
            "4. PDPL 2025 Compliance",
            "5. AI Law 134/2025 Compliance",
            "6. Governance & HITL Gates",
        ]:
            assert s in content, f"Missing {s}"

        # 12+ checklist items (bullets)
        items = re.findall(r"(?m)^- \*\*", content)
        assert len(items) >= 12, f"Expected >= 12 checklist items, found {len(items)}"

        # Single footer
        assert content.strip().endswith("Last updated: 2026-09-29")


# ==============================================================================
# 5. FAST INVOCATION ALIASES
# ==============================================================================

class TestFastInvocationAliases:
    """Verify alias routing in role-skill-index.json."""

    def test_new_skill_aliases(self):
        index = load_json(WELL_KNOWN_DIR / "role-skill-index.json")
        skill_aliases = index.get("skill_aliases", {})

        expected = {
            "audit-ai-compliance": ["audit-ai-compliance"],
            "audit_ai_compliance": ["audit-ai-compliance"],
            "ai_law_audit": ["audit-ai-compliance"],
            "ai_risk_classification": ["audit-ai-compliance"],
            "vietnam_ai_compliance": ["audit-ai-compliance"],
            "draft-legal-opinion": ["draft-legal-opinion"],
            "draft_legal_opinion": ["draft-legal-opinion"],
            "legal_opinion": ["draft-legal-opinion"],
            "legal_opinion_drafting": ["draft-legal-opinion"],
        }
        for alias, target in expected.items():
            assert skill_aliases.get(alias) == target, f"Alias @{alias} mapped to {skill_aliases.get(alias)}, expected {target}"


# ==============================================================================
# 6. ALL CORE VALIDATORS VIA VALIDATE-ALL.PY
# ==============================================================================

class TestValidateAllGate:
    """Empirically execute validate-all.py and assert exit code 0."""

    def test_validate_all_exits_code_zero(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate-all.py")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"validate-all.py failed with code {result.returncode}:\n{result.stderr}\n{result.stdout}"
        assert "All core validators passed." in result.stdout


# ==============================================================================
# 7. ADVERSARIAL SENSITIVITY MUTATION ORACLES
# ==============================================================================

class TestAdversarialSensitivityMutations:
    """Demonstrate that validation oracles fail when invariants are violated."""

    def test_corrupted_readme_category_count_fails_validation(self):
        readme = SKILLS_DIR / "README.md"
        orig = readme.read_text(encoding="utf-8")
        try:
            bad_readme = orig.replace("### Legal Compliance (3)", "### Legal Compliance (4)")
            readme.write_text(bad_readme, encoding="utf-8")
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-indexes.py")],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
            )
            assert res.returncode != 0
            assert "Legal Compliance (4)" in res.stdout
        finally:
            readme.write_text(orig, encoding="utf-8")

    def test_stale_index_aliases_fails_check(self):
        script = SCRIPTS_DIR / "generate-index.py"
        orig_script = script.read_text(encoding="utf-8")
        try:
            bad_script = orig_script.replace(
                "\"legal_opinion_drafting\": [\"draft-legal-opinion\"],",
                "\"legal_opinion_drafting\": [\"draft-legal-opinion\"],\n    \"stale_unregistered_alias\": [\"draft-legal-opinion\"],",
            )
            script.write_text(bad_script, encoding="utf-8")
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "generate-index.py"), "--check"],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
            )
            assert res.returncode != 0
            assert "Stale generated artifacts" in res.stdout
        finally:
            script.write_text(orig_script, encoding="utf-8")

    def test_corrupted_schema_required_field_fails_contract_validation(self):
        schema = SCHEMAS_DIR / "legal-compliance-review.json"
        orig_schema = schema.read_text(encoding="utf-8")
        try:
            bad_schema = orig_schema.replace("\"required\": [", "\"required\": [\"non_existent_key_12345\", ")
            schema.write_text(bad_schema, encoding="utf-8")
            res = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-contracts.py")],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
            )
            assert res.returncode != 0
            assert "missing required property non_existent_key_12345" in res.stdout
        finally:
            schema.write_text(orig_schema, encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    if not text.startswith("---"):
        return {}, text, ["missing frontmatter"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text, ["malformed frontmatter"]
    try:
        data = yaml.safe_load(parts[1]) or {}
        return data, parts[2], []
    except Exception as exc:
        return {}, text, [str(exc)]
