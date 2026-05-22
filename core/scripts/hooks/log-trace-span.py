#!/usr/bin/env python3
"""Cursor hook: append lightweight trace span JSON lines for observability."""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def pack_root() -> Path:
    env = os.environ.get("AGENT_SKILLS_ROOT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3]


def main() -> int:
    role = os.environ.get("AGENT_ACTIVE_ROLE", "unknown")
    tool = os.environ.get("CURSOR_TOOL_NAME", os.environ.get("TOOL_NAME", "tool"))
    log_dir = pack_root() / "core" / "observability" / "spans"
    log_dir.mkdir(parents=True, exist_ok=True)
    span = {
        "trace_id": os.environ.get("AGENT_TRACE_ID", str(uuid.uuid4())),
        "span_id": str(uuid.uuid4())[:16],
        "role": role,
        "operation": tool,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "attributes": {"hook": "postToolUse"},
    }
    log_file = log_dir / f"{span['trace_id']}.jsonl"
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(span) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
