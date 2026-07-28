#!/usr/bin/env python3
"""Validate generated Agent Cards against agent-card.json and registry integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT


REGISTRY_DIR = CORE_ROOT / "a2a" / "registry"
WELL_KNOWN = CORE_ROOT / "a2a" / ".well-known" / "agent-registry.json"
CARD_SCHEMA = CORE_ROOT / "contracts" / "schemas" / "agent-card.json"
ROLE_ROOT = CORE_ROOT / "roles"

REQUIRED_CARD_KEYS = (
    "name",
    "description",
    "url",
    "version",
    "protocol_version",
    "capabilities",
    "skills",
    "role_file",
    "policy_profile",
)


def validate_card_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    errors: list[str] = []
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    for key in REQUIRED_CARD_KEYS:
        if key not in card:
            errors.append(f"{rel}: missing key: {key}")

    if card.get("protocol_version") != "1.0":
        errors.append(f"{rel}: protocol_version must be 1.0")

    caps = card.get("capabilities", {})
    if not caps.get("streaming"):
        errors.append(f"{rel}: capabilities.streaming should be true")
    if not caps.get("stateTransitionHistory"):
        errors.append(f"{rel}: capabilities.stateTransitionHistory should be true")

    if not card.get("skills"):
        errors.append(f"{rel}: skills array must not be empty")

    stem = path.stem.replace(".agent-card", "")
    if card.get("name") != stem:
        errors.append(f"{rel}: name {card.get('name')} != expected {stem}")
    if card.get("policy_profile") != stem:
        errors.append(f"{rel}: policy_profile mismatch")

    role_path = ROOT / card.get("role_file", "")
    if not role_path.is_file():
        errors.append(f"{rel}: role_file does not exist: {card.get('role_file')}")

    return errors


def validate_registry(cards: list[Path]) -> list[str]:
    errors: list[str] = []
    if not WELL_KNOWN.is_file():
        return ["missing registry — run generate-a2a-registry.py"]

    reg = json.loads(WELL_KNOWN.read_text(encoding="utf-8"))
    agents = reg.get("agents", [])
    reg_roles = {a["role"] for a in agents}
    card_roles = {p.stem.replace(".agent-card", "") for p in cards}

    missing = card_roles - reg_roles
    extra = reg_roles - card_roles
    for r in sorted(missing):
        errors.append(f"registry missing entry for role: {r}")
    for r in sorted(extra):
        errors.append(f"registry unknown role: {r}")

    roles_on_disk = {
        p.stem
        for p in ROLE_ROOT.glob("*.md")
        if p.name not in {"README.md", "role-standard.md"}
    }
    if card_roles != roles_on_disk:
        errors.append(
            f"card count {len(card_roles)} != role count {len(roles_on_disk)}"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    if not CARD_SCHEMA.is_file():
        errors.append("missing agent-card.json schema")
    cards = sorted(REGISTRY_DIR.glob("*.agent-card.json"))
    if not cards:
        errors.append("no agent cards — run: python3 core/scripts/generate-a2a-registry.py")

    for path in cards:
        errors.extend(validate_card_file(path))
    errors.extend(validate_registry(cards))

    if errors:
        print("Agent card validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Agent card validation passed: {len(cards)} cards checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
