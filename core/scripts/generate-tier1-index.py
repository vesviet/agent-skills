#!/usr/bin/env python3
"""Generate Tier 1 discovery manifest (INDEX_TIER1.json) for agentskills.io.

Scans all portable core skills (core/skills/*/*/SKILL.md) and overlay skills
(overlays/*/skills/*/SKILL.md), computes canonical SHA-256 digests (normalizing
CRLF to LF), sanitizes operational descriptions to maintain a compact footprint,
and emits adapters/antigravity/INDEX_TIER1.json conforming to
core/contracts/schemas/agent-skills-discovery.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure core/scripts is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CORE_ROOT, ROOT, SKILLS_ROOT, parse_frontmatter

SCHEMA_PATH = CORE_ROOT / "contracts" / "schemas" / "agent-skills-discovery.json"
TIER1_INDEX_PATH = ROOT / "adapters" / "antigravity" / "INDEX_TIER1.json"


def sanitize_description(desc: str, max_len: int = 100) -> str:
    """Clean linebreaks and sanitize description to maintain compact token footprint.

    Enforces single whitespace, strips boundaries, and truncates to <= max_len
    while preserving trailing ellipsis.
    """
    cleaned = re.sub(r"\s+", " ", str(desc)).strip()
    if len(cleaned) <= max_len:
        return cleaned
    truncated = cleaned[: max_len - 3].rstrip()
    return truncated + "..."


def compute_canonical_digest(raw_bytes: bytes) -> str:
    """Compute canonical SHA-256 digest normalizing line endings to LF."""
    normalized = raw_bytes.replace(b"\r\n", b"\n")
    return f"sha256:{hashlib.sha256(normalized).hexdigest()}"


def collect_skills() -> list[dict[str, str]]:
    """Scan all 183 unique skills across core and overlays.

    Overlay skills override core skills on name collision.
    Returns skills sorted alphabetically by name.
    """
    skills_dict: dict[str, dict[str, str]] = {}

    # 1. Portable core skills (169 files)
    for s_file in sorted(SKILLS_ROOT.glob("*/*/SKILL.md")):
        raw = s_file.read_bytes()
        digest = compute_canonical_digest(raw)
        normalized_text = raw.replace(b"\r\n", b"\n").decode("utf-8")
        meta, _, _ = parse_frontmatter(normalized_text)
        name = meta.get("name") or s_file.parent.name
        desc_raw = meta.get("description", "")
        if isinstance(desc_raw, list):
            desc_raw = " ".join(desc_raw)
        desc = sanitize_description(desc_raw)
        rel_path = s_file.relative_to(ROOT).as_posix()
        skills_dict[name] = {
            "name": name,
            "type": "skill-md",
            "description": desc,
            "url": rel_path,
            "digest": digest,
        }

    # 2. Overlay skills (14 files) - overlays override core entries
    for s_file in sorted(ROOT.glob("overlays/*/skills/*/SKILL.md")):
        raw = s_file.read_bytes()
        digest = compute_canonical_digest(raw)
        normalized_text = raw.replace(b"\r\n", b"\n").decode("utf-8")
        meta, _, _ = parse_frontmatter(normalized_text)
        name = meta.get("name") or s_file.parent.name
        desc_raw = meta.get("description", "")
        if isinstance(desc_raw, list):
            desc_raw = " ".join(desc_raw)
        desc = sanitize_description(desc_raw)
        rel_path = s_file.relative_to(ROOT).as_posix()
        skills_dict[name] = {
            "name": name,
            "type": "skill-md",
            "description": desc,
            "url": rel_path,
            "digest": digest,
        }

    return [skills_dict[k] for k in sorted(skills_dict.keys())]


def build_tier1_doc() -> dict[str, Any]:
    """Build root Tier 1 discovery document conforming to schema."""
    skills = collect_skills()
    return {
        "contract_type": "agent-skills-discovery",
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": skills,
    }


def validate_tier1_doc(doc: dict[str, Any]) -> None:
    """Validate generated document against agent-skills-discovery schema."""
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Missing discovery schema: {SCHEMA_PATH}")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema

        jsonschema.validate(instance=doc, schema=schema)
    except ImportError:
        # Fallback structural validation
        assert doc.get("contract_type") == "agent-skills-discovery"
        assert doc.get("$schema") == "https://schemas.agentskills.io/discovery/0.2.0/schema.json"
        skills = doc.get("skills", [])
        assert isinstance(skills, list) and len(skills) > 0
        for s in skills:
            for req in ("name", "type", "description", "url", "digest"):
                assert req in s, f"Missing key '{req}' in {s}"
            assert s["type"] in ("skill-md", "archive")
            assert 20 <= len(s["description"]) <= 1024
            assert re.match(r"^sha256:[a-f0-9]{64}$", s["digest"])


def generate_payload() -> str:
    """Generate and validate formatted Tier 1 index JSON string."""
    doc = build_tier1_doc()
    validate_tier1_doc(doc)
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify Tier 1 discovery manifest (INDEX_TIER1.json)."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify adapters/antigravity/INDEX_TIER1.json is up to date without writing; exit 1 if stale/missing",
    )
    args = parser.parse_args()

    expected_payload = generate_payload()

    if args.check:
        if not TIER1_INDEX_PATH.is_file():
            print(
                f"Missing Tier 1 discovery index: {TIER1_INDEX_PATH.relative_to(ROOT)}. "
                f"Run: python core/scripts/generate-tier1-index.py"
            )
            return 1

        actual_payload = TIER1_INDEX_PATH.read_text(encoding="utf-8")
        if actual_payload != expected_payload:
            print(
                f"Stale Tier 1 discovery index: {TIER1_INDEX_PATH.relative_to(ROOT)} is out of date. "
                f"Run: python core/scripts/generate-tier1-index.py"
            )
            return 1

        print("Tier 1 discovery index is up to date.")
        return 0

    TIER1_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    TIER1_INDEX_PATH.write_text(expected_payload, encoding="utf-8", newline="\n")
    doc = json.loads(expected_payload)
    count = len(doc.get("skills", []))
    print(
        f"Generated {TIER1_INDEX_PATH.relative_to(ROOT)} ({count} skills, {len(expected_payload.encode('utf-8'))} bytes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
