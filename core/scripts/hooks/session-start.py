#!/usr/bin/env python3
"""SessionStart bootstrap hook for agent-skills (startup|clear|compact).

Re-injects mandatory pack routing, post-compaction discipline, and
verification-before-completion tripwires across Claude Code, Cursor, and CLI
harnesses without shell sub-process forks or PATH dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
VERSION_FILE = REPO_ROOT / "VERSION"
MAX_BOOTSTRAP_BYTES = 2_500


def read_pack_version() -> str:
    if VERSION_FILE.is_file():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return "5.10.0"


def is_disabled() -> bool:
    raw = os.environ.get("AGENT_DISABLED_HOOKS", "")
    disabled = {item.strip().lower() for item in raw.split(",") if item.strip()}
    return "session-start" in disabled or "all" in disabled


def build_bootstrap_context(event_source: str = "startup", profile: str = "standard") -> str:
    version = read_pack_version()
    lines = [
        f"agent-skills v{version} active ({event_source}, profile={profile}).",
        "Mandatory pre-action protocol (re-anchored after startup/clear/compact):",
        "1. Read core/rules/code.md and the assigned role (core/roles/role-standard.md -> core/roles/<role>.md) before editing files or running state-changing commands.",
        "2. Use Two-Tier JIT skill discovery: check adapters/antigravity/INDEX_TIER1.json first, then load only the needed SKILL.md (verified < 20 KB) before acting.",
        "3. Apply Verification-Before-Completion (IDENTIFY -> RUN -> READ -> VERIFY -> REPORT): never claim fixed/passed without fresh exit-code-0 output.",
        "4. Never commit, push, tag, or publish without explicit user confirmation; never expose .env or secrets.",
        "5. Red-Flags tripwire: if you think 'this is too simple to check a skill/test', 'it passed earlier', or 'I remember the file', STOP and verify live disk/command evidence first.",
    ]
    if profile == "strict":
        lines.append(
            "6. Strict mode: require explicit contract emission (core/contracts/schemas/) and policy check before any mutating tool call."
        )
    text = "\n".join(lines)
    if len(text.encode("utf-8")) > MAX_BOOTSTRAP_BYTES:
        text = text[: MAX_BOOTSTRAP_BYTES - 1]
    return text


def detect_event_source() -> str:
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            if raw:
                payload = json.loads(raw)
                source = payload.get("source") or payload.get("hook_event_name")
                if isinstance(source, str) and source.strip():
                    return source.strip()
        except Exception:
            pass
    return os.environ.get("AGENT_SESSION_SOURCE", "startup")


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit post-compaction survival bootstrap context.")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--source", default="", help="Override event source (startup|clear|compact)")
    args = parser.parse_args()

    if is_disabled():
        return 0

    profile = os.environ.get("AGENT_HOOK_PROFILE", "standard").strip().lower() or "standard"
    source = args.source.strip() or detect_event_source()
    context = build_bootstrap_context(event_source=source, profile=profile)

    if args.format == "text":
        sys.stdout.write(context + "\n")
    else:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
