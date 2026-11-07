#!/usr/bin/env python3
"""Validate discovery manifests and schema conformance.

Validates discovery manifests (such as adapters/antigravity/INDEX_TIER1.json
and /.well-known/agent-skills/index.json) against the normative schema
core/contracts/schemas/agent-skills-discovery.json.

Verifications:
1. Manifest complies with JSON Schema Draft 2020-12 (with pure-Python structural fallback).
2. Every skill's target file exists on disk.
3. Every skill's frontmatter name matches the manifest entry name.
4. Every skill's SHA-256 digest matches LF-normalized file bytes (raw.replace(b"\\r\\n", b"\\n")).
5. Every skill's operational description length is between 20 and 1024 characters.
6. All skill names are unique.
7. All skill entries are sorted alphabetically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

# Ensure core/scripts is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CORE_ROOT, ROOT, parse_frontmatter

try:
    from jsonschema import Draft202012Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

DEFAULT_MANIFEST_PATH = ROOT / "adapters" / "antigravity" / "INDEX_TIER1.json"
WELL_KNOWN_MANIFEST_PATH = ROOT / ".well-known" / "agent-skills" / "index.json"
DEFAULT_SCHEMA_PATH = CORE_ROOT / "contracts" / "schemas" / "agent-skills-discovery.json"


def _structural_fallback_validate(doc: Any, label: str) -> list[str]:
    """Pure-Python structural fallback when jsonschema library is not available."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return [f"{label}: root must be a JSON object"]

    if doc.get("contract_type") is not None and doc.get("contract_type") != "agent-skills-discovery":
        errors.append(f"{label}: contract_type must be 'agent-skills-discovery'")

    if "$schema" not in doc:
        errors.append(f"{label}: missing required property '$schema'")
    elif doc["$schema"] != "https://schemas.agentskills.io/discovery/0.2.0/schema.json":
        errors.append(
            f"{label}: $schema must be 'https://schemas.agentskills.io/discovery/0.2.0/schema.json'"
        )

    if "skills" not in doc:
        errors.append(f"{label}: missing required property 'skills'")
    elif not isinstance(doc["skills"], list):
        errors.append(f"{label}: 'skills' must be an array")
    elif len(doc["skills"]) < 1:
        errors.append(f"{label}: 'skills' array must have at least 1 item")
    else:
        for i, s in enumerate(doc["skills"]):
            if not isinstance(s, dict):
                errors.append(f"{label}: skills[{i}] must be an object")
                continue
            for req in ("name", "type", "description", "url", "digest"):
                if req not in s:
                    errors.append(f"{label}: skills[{i}] missing required property '{req}'")
            if "name" in s:
                if not isinstance(s["name"], str) or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", s["name"]):
                    errors.append(f"{label}: skills[{i}].name '{s.get('name')}' is not a valid kebab-case name")
            if "type" in s:
                if s["type"] not in ("skill-md", "archive"):
                    errors.append(f"{label}: skills[{i}].type '{s.get('type')}' must be 'skill-md' or 'archive'")
            if "description" in s:
                desc = s["description"]
                if not isinstance(desc, str) or len(desc) < 20 or len(desc) > 1024:
                    errors.append(
                        f"{label}: skills[{i}].description length must be between 20 and 1024 characters"
                    )
            if "digest" in s:
                digest = s["digest"]
                if not isinstance(digest, str) or not re.match(r"^sha256:[a-f0-9]{64}$", digest):
                    errors.append(
                        f"{label}: skills[{i}].digest '{digest}' is not a valid sha256 hex digest"
                    )
    return errors


def _validate_single_manifest(
    manifest_path: Path,
    schema: dict[str, Any],
    base_dir: Path | None = None,
) -> list[str]:
    """Validate a single discovery manifest file against schema and disk assets."""
    errors: list[str] = []
    root_dir = base_dir or ROOT

    try:
        rel_label = manifest_path.relative_to(root_dir).as_posix()
    except ValueError:
        rel_label = manifest_path.name

    try:
        raw_text = manifest_path.read_text(encoding="utf-8")
        doc = json.loads(raw_text)
    except Exception as exc:
        return [f"{rel_label}: invalid JSON syntax: {exc}"]

    if not isinstance(doc, dict):
        return [f"{rel_label}: root must be a JSON object"]

    # 1. Schema conformance check (Draft 2020-12 or structural fallback)
    if HAS_JSONSCHEMA:
        validator = Draft202012Validator(schema)
        for err in validator.iter_errors(doc):
            loc = rel_label
            if err.path:
                loc += f" at {list(err.path)}"
            errors.append(f"{loc}: {err.message}")
    else:
        errors.extend(_structural_fallback_validate(doc, rel_label))

    skills = doc.get("skills")
    if not isinstance(skills, list):
        return errors

    # 2. Uniqueness of skill names
    seen_names: set[str] = set()
    duplicate_names: set[str] = set()
    for s in skills:
        if isinstance(s, dict) and "name" in s:
            name = s["name"]
            if name in seen_names:
                duplicate_names.add(name)
            seen_names.add(name)
    for name in sorted(duplicate_names):
        errors.append(f"{rel_label}: duplicate skill name: '{name}'")

    # 3. Alphabetical ordering of skills
    skill_names = [s["name"] for s in skills if isinstance(s, dict) and "name" in s]
    for i in range(1, len(skill_names)):
        if skill_names[i] < skill_names[i - 1]:
            errors.append(
                f"{rel_label}: skills not sorted: '{skill_names[i]}' after '{skill_names[i - 1]}'"
            )
            break

    # 4. Referential and cryptographic checks for each skill
    for s in skills:
        if not isinstance(s, dict):
            continue
        s_name = s.get("name", "<unknown>")

        desc = s.get("description", "")
        if not (isinstance(desc, str) and 20 <= len(desc) <= 1024):
            errors.append(
                f"{rel_label}: skill '{s_name}' description length {len(str(desc))} not between 20 and 1024 chars"
            )

        url = s.get("url")
        if not url or not isinstance(url, str):
            errors.append(f"{rel_label}: skill '{s_name}' missing or invalid url")
            continue

        # Skip remote URLs
        if url.startswith(("http://", "https://")):
            continue

        target_file = root_dir / url
        if not target_file.is_file():
            errors.append(f"{rel_label}: skill '{s_name}' target file not found: {url}")
            continue

        try:
            raw_bytes = target_file.read_bytes()
        except Exception as exc:
            errors.append(f"{rel_label}: skill '{s_name}' failed to read target file {url}: {exc}")
            continue

        # LF normalization before digest computation
        normalized_bytes = raw_bytes.replace(b"\r\n", b"\n")
        computed_digest = f"sha256:{hashlib.sha256(normalized_bytes).hexdigest()}"
        declared_digest = s.get("digest")
        if declared_digest != computed_digest:
            errors.append(
                f"{rel_label}: skill '{s_name}' digest mismatch: declared '{declared_digest}' != computed '{computed_digest}'"
            )

        text = normalized_bytes.decode("utf-8", errors="replace")
        meta, _, _ = parse_frontmatter(text)
        fm_name = meta.get("name")
        if fm_name != s_name:
            errors.append(
                f"{rel_label}: skill '{s_name}' frontmatter name mismatch: declared '{s_name}' != frontmatter '{fm_name}' in {url}"
            )

    return errors


def validate_discovery_manifests(
    manifest_path: Path | str | None = None,
    schema_path: Path | str | None = None,
    base_dir: Path | str | None = None,
) -> list[str]:
    """Validate discovery manifest(s) against schema and asset integrity contracts.

    Parameters:
        manifest_path: Path to a specific manifest file to validate.
                       If None, validates adapters/antigravity/INDEX_TIER1.json
                       and /.well-known/agent-skills/index.json (if present).
        schema_path: Path to agent-skills-discovery.json schema.
                     If None, defaults to core/contracts/schemas/agent-skills-discovery.json.
        base_dir: Base repository root directory for resolving relative URLs.
                  If None, defaults to the repository root.

    Returns:
        List of validation error strings. Empty list indicates 100% pass.
    """
    root_dir = Path(base_dir) if base_dir is not None else ROOT
    resolved_schema = Path(schema_path) if schema_path is not None else DEFAULT_SCHEMA_PATH
    if not resolved_schema.is_file():
        return [f"Discovery schema not found: {resolved_schema}"]

    try:
        schema_data = json.loads(resolved_schema.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Failed to load discovery schema {resolved_schema}: {exc}"]

    manifests_to_validate: list[Path] = []
    if manifest_path is not None:
        manifests_to_validate.append(Path(manifest_path))
    else:
        manifests_to_validate.append(DEFAULT_MANIFEST_PATH)
        if WELL_KNOWN_MANIFEST_PATH.is_file():
            manifests_to_validate.append(WELL_KNOWN_MANIFEST_PATH)

    errors: list[str] = []
    for mf in manifests_to_validate:
        if not mf.is_file():
            errors.append(f"Discovery manifest not found: {mf}")
            continue

        errors.extend(_validate_single_manifest(mf, schema_data, base_dir=root_dir))

    return errors


def run_self_tests() -> int:
    """Run internal test suite with synthetic valid and invalid manifests."""
    print("Running validate-discovery-manifests self-test suite...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_root = Path(tmpdir)
        skill_dir = tmp_root / "skills" / "my-skill"
        skill_dir.mkdir(parents=True)
        skill_file = skill_dir / "SKILL.md"
        skill_content = "---\nname: my-skill\ndescription: A valid test skill description for testing purposes.\n---\n# My Skill\n"
        skill_file.write_text(skill_content, encoding="utf-8")

        raw = skill_file.read_bytes().replace(b"\r\n", b"\n")
        digest = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        # 1. Valid manifest
        valid_doc = {
            "contract_type": "agent-skills-discovery",
            "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
            "skills": [
                {
                    "name": "my-skill",
                    "type": "skill-md",
                    "description": "A valid test skill description for testing purposes.",
                    "url": "skills/my-skill/SKILL.md",
                    "digest": digest,
                }
            ],
        }
        manifest_path = tmp_root / "manifest.json"
        manifest_path.write_text(json.dumps(valid_doc, indent=2), encoding="utf-8")

        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert not errs, f"Expected valid manifest to pass, got: {errs}"

        # 2. Tampered digest
        tampered_doc = dict(valid_doc)
        tampered_doc["skills"] = [
            {
                "name": "my-skill",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/my-skill/SKILL.md",
                "digest": "sha256:" + "0" * 64,
            }
        ]
        manifest_path.write_text(json.dumps(tampered_doc, indent=2), encoding="utf-8")
        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert any("digest mismatch" in e for e in errs), f"Expected digest mismatch, got: {errs}"

        # 3. Missing target file
        missing_doc = dict(valid_doc)
        missing_doc["skills"] = [
            {
                "name": "my-skill",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/nonexistent/SKILL.md",
                "digest": digest,
            }
        ]
        manifest_path.write_text(json.dumps(missing_doc, indent=2), encoding="utf-8")
        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert any("target file not found" in e for e in errs), f"Expected target file not found, got: {errs}"

        # 4. Frontmatter name mismatch
        fm_mismatch_doc = dict(valid_doc)
        fm_mismatch_doc["skills"] = [
            {
                "name": "other-skill-name",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/my-skill/SKILL.md",
                "digest": digest,
            }
        ]
        manifest_path.write_text(json.dumps(fm_mismatch_doc, indent=2), encoding="utf-8")
        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert any("frontmatter name mismatch" in e for e in errs), f"Expected frontmatter mismatch, got: {errs}"

        # 5. Unsorted skills
        skill_dir_b = tmp_root / "skills" / "a-skill"
        skill_dir_b.mkdir(parents=True)
        (skill_dir_b / "SKILL.md").write_text(
            "---\nname: a-skill\ndescription: Another valid test skill description for testing.\n---\n# A Skill\n",
            encoding="utf-8",
        )
        raw_b = (skill_dir_b / "SKILL.md").read_bytes().replace(b"\r\n", b"\n")
        digest_b = f"sha256:{hashlib.sha256(raw_b).hexdigest()}"

        unsorted_doc = dict(valid_doc)
        unsorted_doc["skills"] = [
            {
                "name": "my-skill",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/my-skill/SKILL.md",
                "digest": digest,
            },
            {
                "name": "a-skill",
                "type": "skill-md",
                "description": "Another valid test skill description for testing.",
                "url": "skills/a-skill/SKILL.md",
                "digest": digest_b,
            },
        ]
        manifest_path.write_text(json.dumps(unsorted_doc, indent=2), encoding="utf-8")
        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert any("skills not sorted" in e for e in errs), f"Expected skills not sorted, got: {errs}"

        # 6. Duplicate skills
        duplicate_doc = dict(valid_doc)
        duplicate_doc["skills"] = [
            {
                "name": "my-skill",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/my-skill/SKILL.md",
                "digest": digest,
            },
            {
                "name": "my-skill",
                "type": "skill-md",
                "description": "A valid test skill description for testing purposes.",
                "url": "skills/my-skill/SKILL.md",
                "digest": digest,
            },
        ]
        manifest_path.write_text(json.dumps(duplicate_doc, indent=2), encoding="utf-8")
        errs = validate_discovery_manifests(
            manifest_path=manifest_path,
            schema_path=DEFAULT_SCHEMA_PATH,
            base_dir=tmp_root,
        )
        assert any("duplicate skill name" in e for e in errs), f"Expected duplicate skill name, got: {errs}"

    print("All self-test vectors PASSED (6/6).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate discovery manifest (INDEX_TIER1.json) and schema conformance."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to discovery manifest to validate (default: adapters/antigravity/INDEX_TIER1.json)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=None,
        help="Path to agent-skills-discovery.json schema",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run internal self-tests with synthetic manifests",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_tests()

    errors = validate_discovery_manifests(manifest_path=args.manifest, schema_path=args.schema)
    if errors:
        print(f"Discovery manifest validation failed ({len(errors)} errors):", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    target = args.manifest or DEFAULT_MANIFEST_PATH
    try:
        rel = target.relative_to(ROOT).as_posix()
    except ValueError:
        rel = str(target)

    count = 0
    try:
        doc = json.loads(target.read_text(encoding="utf-8"))
        count = len(doc.get("skills", []))
    except Exception:
        pass

    print(f"Discovery manifest validation passed: {rel} ({count} skills checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
