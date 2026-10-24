#!/usr/bin/env python3
"""Validate Golden Prompt Evaluation assets, manifests, and test cases.

Enforces late-2026 Agent Skills Specification (PromptOps / A2A 1.0):
- Manifest validity: prompt_id, version, role/target_role, skill/target_skill,
  min_pass_rate, cases_dir.
- Role and skill existence in core registries.
- Case file integrity: matching NNN-input.json and NNN-expected.json pairs (>=10 pairs per asset).
- Valid JSON syntax and non-empty assertions (must_include / required_tokens,
  must_not_include / forbidden_tokens).
- Schema references resolve to existing files in core/contracts/schemas/.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from common import CORE_ROOT, ROOT, collect_skill_names


GOLDEN_ROOT = CORE_ROOT / "prompts" / "golden"
ROLE_ROOT = CORE_ROOT / "roles"
SCHEMAS_DIR = CORE_ROOT / "contracts" / "schemas"

SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")


def validate_asset(asset_dir: Path, valid_roles: set[str], valid_skills: set[str]) -> tuple[list[str], int]:
    rel_dir = asset_dir.relative_to(ROOT)
    errors: list[str] = []
    manifest_path = asset_dir / "manifest.yaml"

    if not manifest_path.is_file():
        errors.append(f"{rel_dir}: missing manifest.yaml")
        return errors, 0

    try:
        manifest_text = manifest_path.read_text(encoding="utf-8")
        manifest = yaml.safe_load(manifest_text)
    except Exception as exc:
        errors.append(f"{rel_dir}/manifest.yaml: invalid YAML: {exc}")
        return errors, 0

    if not isinstance(manifest, dict):
        errors.append(f"{rel_dir}/manifest.yaml: manifest root must be a mapping")
        return errors, 0

    # 1. Manifest field checks
    prompt_id = manifest.get("prompt_id")
    if not prompt_id or not isinstance(prompt_id, str) or not SLUG_PATTERN.match(prompt_id):
        errors.append(f"{rel_dir}/manifest.yaml: invalid or missing prompt_id: {prompt_id!r}")

    version = manifest.get("version")
    if not version:
        errors.append(f"{rel_dir}/manifest.yaml: missing version")

    role = manifest.get("target_role") or manifest.get("role")
    if not role or role not in valid_roles:
        errors.append(f"{rel_dir}/manifest.yaml: unknown or missing role: {role!r}")

    skill = manifest.get("target_skill") or manifest.get("skill")
    if not skill or skill not in valid_skills:
        errors.append(f"{rel_dir}/manifest.yaml: unknown or missing skill: {skill!r}")

    # Min pass rate check (either top-level or under governance)
    min_pass = manifest.get("min_pass_rate")
    if min_pass is None and isinstance(manifest.get("governance"), dict):
        min_pass = manifest["governance"].get("min_pass_rate")

    if min_pass is None:
        errors.append(f"{rel_dir}/manifest.yaml: missing min_pass_rate")
    elif not isinstance(min_pass, (int, float)) or not (0.0 <= float(min_pass) <= 1.0):
        errors.append(f"{rel_dir}/manifest.yaml: min_pass_rate must be a float between 0.0 and 1.0, got: {min_pass!r}")

    # Contract schema reference check in governance
    if isinstance(manifest.get("governance"), dict):
        gov_schema = manifest["governance"].get("contract_schema")
        if gov_schema:
            schema_file = ROOT / gov_schema if not Path(gov_schema).is_absolute() else Path(gov_schema)
            if not schema_file.is_file() and not (SCHEMAS_DIR / Path(gov_schema).name).is_file():
                errors.append(f"{rel_dir}/manifest.yaml: governance.contract_schema file not found: {gov_schema}")

    # 2. Cases directory check
    cases_dir_name = manifest.get("cases_dir", "cases/")
    cases_dir = (asset_dir / cases_dir_name).resolve()

    if not cases_dir.is_dir():
        errors.append(f"{rel_dir}: cases directory not found at {cases_dir_name}")
        return errors, 0

    input_files = {p.name.split("-input.json")[0]: p for p in cases_dir.glob("*-input.json")}
    expected_files = {p.name.split("-expected.json")[0]: p for p in cases_dir.glob("*-expected.json")}

    all_keys = sorted(set(input_files.keys()) | set(expected_files.keys()))
    case_pairs = 0

    for key in all_keys:
        in_file = input_files.get(key)
        exp_file = expected_files.get(key)

        if not in_file:
            errors.append(f"{rel_dir}/{cases_dir_name}: missing input file for expected: {exp_file.name}")
            continue
        if not exp_file:
            errors.append(f"{rel_dir}/{cases_dir_name}: missing expected file for input: {in_file.name}")
            continue

        case_pairs += 1

        # Validate input file
        try:
            input_data = json.loads(in_file.read_text(encoding="utf-8"))
            if not isinstance(input_data, dict):
                errors.append(f"{rel_dir}/{cases_dir_name}/{in_file.name}: root must be a JSON object")
        except json.JSONDecodeError as exc:
            errors.append(f"{rel_dir}/{cases_dir_name}/{in_file.name}: invalid JSON: {exc}")

        # Validate expected file
        try:
            exp_data = json.loads(exp_file.read_text(encoding="utf-8"))
            if not isinstance(exp_data, dict):
                errors.append(f"{rel_dir}/{cases_dir_name}/{exp_file.name}: root must be a JSON object")
                continue

            # Must contain positive assertions
            has_must_include = (
                "must_include" in exp_data
                and isinstance(exp_data["must_include"], list)
                and len(exp_data["must_include"]) > 0
            )
            has_required_tokens = (
                "required_tokens" in exp_data
                and isinstance(exp_data["required_tokens"], list)
                and len(exp_data["required_tokens"]) > 0
            )
            if not (has_must_include or has_required_tokens):
                errors.append(
                    f"{rel_dir}/{cases_dir_name}/{exp_file.name}: must define non-empty 'must_include' or 'required_tokens'"
                )

            # Must contain negative assertions (may be empty or list)
            has_must_not_include = "must_not_include" in exp_data and isinstance(exp_data["must_not_include"], list)
            has_forbidden_tokens = "forbidden_tokens" in exp_data and isinstance(exp_data["forbidden_tokens"], list)
            if not (has_must_not_include or has_forbidden_tokens):
                errors.append(
                    f"{rel_dir}/{cases_dir_name}/{exp_file.name}: must define 'must_not_include' or 'forbidden_tokens' list"
                )

            # Check schema references if present
            schema_val = exp_data.get("schema_validation")
            if isinstance(schema_val, dict):
                schema_ref = schema_val.get("schema_ref")
                if schema_ref:
                    ref_path = ROOT / schema_ref if not Path(schema_ref).is_absolute() else Path(schema_ref)
                    if not ref_path.is_file() and not (SCHEMAS_DIR / Path(schema_ref).name).is_file():
                        errors.append(
                            f"{rel_dir}/{cases_dir_name}/{exp_file.name}: schema_validation.schema_ref not found: {schema_ref}"
                        )

        except json.JSONDecodeError as exc:
            errors.append(f"{rel_dir}/{cases_dir_name}/{exp_file.name}: invalid JSON: {exc}")

    if case_pairs < 10:
        errors.append(
            f"{rel_dir}: expected at least 10 case pairs, found {case_pairs}"
        )

    return errors, case_pairs


def main() -> int:
    if not GOLDEN_ROOT.is_dir():
        print(f"Error: golden prompts root not found: {GOLDEN_ROOT}", file=sys.stderr)
        return 2

    valid_roles = {p.stem for p in ROLE_ROOT.glob("*.md") if p.name != "README.md"}
    valid_skills = collect_skill_names()

    asset_dirs = sorted([p for p in GOLDEN_ROOT.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))])
    if not asset_dirs:
        print(f"Error: no prompt asset directories found in {GOLDEN_ROOT}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    total_case_pairs = 0

    for asset_dir in asset_dirs:
        errors, count = validate_asset(asset_dir, valid_roles, valid_skills)
        all_errors.extend(errors)
        total_case_pairs += count

    if all_errors:
        for err in all_errors:
            print(f"- {err}", file=sys.stderr)
        print(f"\nGolden prompt evals validation failed with {len(all_errors)} errors.", file=sys.stderr)
        return 1

    print(
        f"Golden prompt evals validation passed: {len(asset_dirs)} assets checked, "
        f"{total_case_pairs} case pairs verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
