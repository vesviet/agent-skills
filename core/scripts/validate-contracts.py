#!/usr/bin/env python3
"""Validate JSON contract schemas and their bundled examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT


try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCHEMAS_DIR = CORE_ROOT / "contracts" / "schemas"
REQUIRED_META = ("$schema", "type", "$id", "title")


def build_schema_registry(schemas: list[Path]) -> Registry | None:
    if not HAS_JSONSCHEMA:
        return None
    resources = {}
    for p in schemas:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            res = Resource.from_contents(data)
            resources[p.name] = res
            if "$id" in data:
                resources[data["$id"]] = res
        except Exception:
            continue
    return Registry().with_resources(resources.items())


def validate_example(example: object, schema: dict, location: str) -> list[str]:
    if not isinstance(example, dict):
        return [f"{location}: example must be an object"]

    errors: list[str] = []
    for required in schema.get("required", []):
        if required not in example:
            errors.append(f"{location}: missing required property {required}")
    for key, definition in schema.get("properties", {}).items():
        if key not in example or not isinstance(definition, dict):
            continue
        if "const" in definition and example[key] != definition["const"]:
            errors.append(
                f"{location}.{key}: expected const {definition['const']!r}"
            )
        if "enum" in definition and example[key] not in definition["enum"]:
            errors.append(f"{location}.{key}: value is not in enum")
    return errors


def validate_schema_file(path: Path, registry: Registry | None = None) -> list[str]:
    rel = path.relative_to(ROOT)
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    for key in REQUIRED_META:
        if key not in data:
            errors.append(f"{rel}: missing {key}")
    if data.get("type") != "object":
        errors.append(f"{rel}: root type should be object")

    props = data.get("properties", {})
    for required in data.get("required", []):
        if required not in props:
            errors.append(f"{rel}: required property missing in properties: {required}")

    examples = data.get("examples", [])
    if examples and not isinstance(examples, list):
        errors.append(f"{rel}: examples must be an array")
    for index, example in enumerate(examples if isinstance(examples, list) else []):
        errors.extend(
            f"{rel}: example[{index}]: {error}"
            for error in validate_example(example, data, "$")
        )

    if HAS_JSONSCHEMA and registry is not None:
        try:
            Draft202012Validator.check_schema(data)
        except Exception as exc:
            errors.append(f"{rel}: schema definition failed Draft 2020-12 meta-schema: {exc}")

        validator = Draft202012Validator(data, registry=registry)
        for index, example in enumerate(examples if isinstance(examples, list) else []):
            for err in validator.iter_errors(example):
                if err.validator == "required" and not err.path:
                    continue
                loc = f"{rel}: example[{index}]"
                if err.path:
                    loc += f" at {list(err.path)}"
                errors.append(f"{loc}: {err.message}")

    return errors


def main() -> int:
    schemas = sorted(SCHEMAS_DIR.glob("*.json"))
    registry = build_schema_registry(schemas)
    errors = [error for path in schemas for error in validate_schema_file(path, registry=registry)]
    if not schemas:
        errors.append("no schemas found")
    if errors:
        print("Contract validation failed:")
        print(*(f"- {error}" for error in errors), sep="\n")
        return 1
    print(f"Contract validation passed: {len(schemas)} schemas checked; bundled examples checked for required fields and discriminators.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
