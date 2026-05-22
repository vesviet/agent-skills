#!/usr/bin/env python3
"""Validate JSON contract schemas under core/contracts/schemas/."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT


SCHEMAS_DIR = CORE_ROOT / "contracts" / "schemas"
REQUIRED_META = ("$schema", "type", "$id", "title")


def validate_schema_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    for key in REQUIRED_META:
        if key not in data:
            errors.append(f"{rel}: missing {key}")

    if data.get("type") != "object" and path.name != "README.md":
        errors.append(f"{rel}: root type should be object")

    props = data.get("properties", {})
    if "required" in data:
        for req in data["required"]:
            if req not in props and "$ref" not in str(data):
                errors.append(f"{rel}: required property missing in properties: {req}")

    return errors


def main() -> int:
    errors: list[str] = []
    schemas = sorted(SCHEMAS_DIR.glob("*.json"))
    if not schemas:
        errors.append("no schemas found")
    for path in schemas:
        errors.extend(validate_schema_file(path))

    if errors:
        print("Contract validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Contract validation passed: {len(schemas)} schemas checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
