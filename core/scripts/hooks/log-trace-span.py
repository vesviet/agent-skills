#!/usr/bin/env python3
"""Cursor/Antigravity hook: append OTel-compatible trace span JSON lines.

2026 upgrades:
- OTel GenAI Semantic Conventions (gen_ai.request.model, gen_ai.usage.*)
- service.name and service.version resource attributes
- span.kind attribute per OTel spec
- W3C Trace Context-compatible trace_id/span_id format
- tool_summary and tool_action attributes for agent observability
"""

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


def _safe_int(val: str | None, default: int = 0) -> int:
    try:
        return int(val or default)
    except (TypeError, ValueError):
        return default


def get_pack_version() -> str:
    env = os.environ.get("AGENT_PACK_VERSION")
    if env:
        return env
    v_file = pack_root() / "VERSION"
    if v_file.is_file():
        return v_file.read_text(encoding="utf-8").strip()
    return "5.0.0"


def main() -> int:
    role = os.environ.get("AGENT_ACTIVE_ROLE", "unknown")
    tool = os.environ.get("CURSOR_TOOL_NAME", os.environ.get("TOOL_NAME", "tool"))
    tool_summary = os.environ.get("CURSOR_TOOL_SUMMARY", os.environ.get("TOOL_SUMMARY", ""))
    tool_action = os.environ.get("CURSOR_TOOL_ACTION", os.environ.get("TOOL_ACTION", ""))

    # OTel GenAI Semantic Convention fields (gen_ai.* namespace)
    model = os.environ.get("AGENT_MODEL", os.environ.get("GEN_AI_MODEL", ""))
    input_tokens = _safe_int(os.environ.get("GEN_AI_USAGE_INPUT_TOKENS"))
    output_tokens = _safe_int(os.environ.get("GEN_AI_USAGE_OUTPUT_TOKENS"))
    reasoning_tokens = _safe_int(os.environ.get("GEN_AI_USAGE_REASONING_TOKENS"))
    cache_read_tokens = _safe_int(os.environ.get("GEN_AI_USAGE_CACHE_READ_TOKENS"))
    cache_creation_tokens = _safe_int(os.environ.get("GEN_AI_USAGE_CACHE_CREATION_TOKENS"))
    finish_reason = os.environ.get("GEN_AI_FINISH_REASON", "stop")

    # W3C Trace Context: trace_id = 32 hex chars, span_id = 16 hex chars
    raw_trace_id = os.environ.get("AGENT_TRACE_ID", str(uuid.uuid4()))
    trace_id = raw_trace_id.replace("-", "")[:32].ljust(32, "0")
    span_id = str(uuid.uuid4()).replace("-", "")[:16]
    parent_span_id = os.environ.get("AGENT_PARENT_SPAN_ID")

    log_dir = pack_root() / "core" / "observability" / "spans"
    log_dir.mkdir(parents=True, exist_ok=True)

    span: dict = {
        # W3C Trace Context
        "trace_id": trace_id,
        "span_id": span_id,
        **({"parent_span_id": parent_span_id} if parent_span_id else {}),
        "span_kind": "INTERNAL",
        # Core attributes
        "role": role,
        "operation": tool,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        # OTel resource attributes
        "resource": {
            "service.name": "agent-skills",
            "service.version": get_pack_version(),
        },
        # OTel span attributes
        "attributes": {
            "hook": "postToolUse",
            "tool.summary": tool_summary,
            "tool.action": tool_action,
            # OTel GenAI Semantic Convention (https://opentelemetry.io/docs/specs/semconv/gen-ai/)
            **({"gen_ai.request.model": model} if model else {}),
            **({"gen_ai.usage.input_tokens": input_tokens} if input_tokens else {}),
            **({"gen_ai.usage.output_tokens": output_tokens} if output_tokens else {}),
            **({"gen_ai.usage.reasoning.output_tokens": reasoning_tokens} if reasoning_tokens else {}),
            **({"gen_ai.usage.cache_read.input_tokens": cache_read_tokens} if cache_read_tokens else {}),
            **({"gen_ai.usage.cache_creation.input_tokens": cache_creation_tokens} if cache_creation_tokens else {}),
            "gen_ai.response.finish_reasons": [finish_reason] if finish_reason else ["stop"],
            "agent.role": role,
        },
    }

    log_file = log_dir / f"{trace_id}.jsonl"
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(span) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
