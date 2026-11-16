#!/usr/bin/env python3
"""Strategic Compact Suggester Hook (PreToolUse).

Monitors cumulative tool call invocations and context pressure across agent
sessions, advising proactive, strategic compaction at natural phase transitions
rather than arbitrary mid-task truncation.

Key Behaviors:
  - Tracks tool call invocations per session in `/tmp/agent_compact_state_<session_id>.json`.
  - Emits a non-blocking stderr advisory at 50 tool invocations (COMPACT_THRESHOLD),
    and at every 25 invocations thereafter (COMPACT_INTERVAL).
  - Advises state persistence to `compact-working-state.json` and compaction at
    phase transitions (Research -> Planning, Planning -> Implementation, etc.).
  - Always exits with code 0 (non-blocking contract).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_THRESHOLD = 50
DEFAULT_INTERVAL = 25
DEFAULT_TTL_DAYS = 14
STATE_FILE_PREFIX = "agent_compact_state_"


def sanitize_session_id(raw_id: str) -> str:
    """Sanitize session identifier to prevent directory traversal or invalid filenames."""
    if not raw_id:
        return "default"
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", raw_id.strip())
    return cleaned or "default"


def resolve_session_id(cli_id: Optional[str] = None) -> str:
    """Resolve active session ID from CLI flag, environment variables, or default."""
    if cli_id:
        return sanitize_session_id(cli_id)
    env_id = (
        os.environ.get("AGENT_SESSION_ID")
        or os.environ.get("CLAUDE_SESSION_ID")
        or os.environ.get("CURSOR_SESSION_ID")
        or ""
    )
    return sanitize_session_id(env_id)


def get_state_file_path(session_id: str) -> Path:
    """Return path to the session state file in temp directory."""
    custom_path = os.environ.get("AGENT_COMPACT_STATE_PATH")
    if custom_path:
        return Path(custom_path)
    temp_dir = Path(tempfile.gettempdir())
    return temp_dir / f"{STATE_FILE_PREFIX}{session_id}.json"


def sweep_stale_state_files(temp_dir: Path, ttl_days: int, current_file: Path) -> None:
    """Remove session state files older than ttl_days, ignoring current session."""
    try:
        cutoff = time.time() - (ttl_days * 86400)
        for item in temp_dir.glob(f"{STATE_FILE_PREFIX}*.json"):
            if item.resolve() == current_file.resolve():
                continue
            try:
                if item.stat().st_mtime < cutoff:
                    item.unlink(missing_ok=True)
            except Exception:
                pass
    except Exception:
        pass


def load_state(path: Path) -> Dict[str, Any]:
    """Read session state file or return fresh default state."""
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {
        "session_id": path.stem.removeprefix(STATE_FILE_PREFIX),
        "tool_calls": 0,
        "first_seen": int(time.time()),
        "last_updated": int(time.time()),
        "last_advised_count": 0,
    }


def save_state_atomic(path: Path, state: Dict[str, Any]) -> None:
    """Write session state atomically via temporary file replacement."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f".tmp.{os.getpid()}")
        tmp_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        tmp_path.replace(path)
    except Exception as exc:
        print(f"[STRATEGIC-COMPACT] WARN: failed to persist state: {exc}", file=sys.stderr)


def check_and_increment(
    session_id: str,
    threshold: int = DEFAULT_THRESHOLD,
    interval: int = DEFAULT_INTERVAL,
) -> tuple[int, Optional[str]]:
    """Increment tool call count and return (count, advisory_message)."""
    state_file = get_state_file_path(session_id)
    sweep_stale_state_files(state_file.parent, DEFAULT_TTL_DAYS, state_file)

    state = load_state(state_file)
    count = int(state.get("tool_calls", 0)) + 1
    state["tool_calls"] = count
    state["last_updated"] = int(time.time())

    advisory: Optional[str] = None
    if threshold > 0 and count == threshold:
        advisory = (
            f"[STRATEGIC-COMPACT] {threshold} tool invocations recorded.\n"
            "Phase transition check recommended: save state to compact-working-state.json and run /compact."
        )
        state["last_advised_count"] = count
    elif count > threshold and interval > 0 and (count - threshold) % interval == 0:
        advisory = (
            f"[STRATEGIC-COMPACT] {count} tool invocations recorded.\n"
            "Context checkpoint recommended: save state to compact-working-state.json and run /compact if transitioning phases."
        )
        state["last_advised_count"] = count

    # Context pressure signal check if AGENT_CONTEXT_TOKENS is set
    ctx_tokens_str = os.environ.get("AGENT_CONTEXT_TOKENS")
    if ctx_tokens_str and not advisory:
        try:
            tokens = int(ctx_tokens_str)
            token_threshold = int(os.environ.get("COMPACT_CONTEXT_THRESHOLD", "160000"))
            if tokens >= token_threshold:
                advisory = (
                    f"[STRATEGIC-COMPACT] Context pressure ~{tokens // 1000}k tokens reached.\n"
                    "Consider persisting working state to compact-working-state.json and running /compact."
                )
        except ValueError:
            pass

    save_state_atomic(state_file, state)
    return count, advisory


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Strategic Compact Suggester: monitors tool calls and context pressure."
    )
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Session identifier (defaults to AGENT_SESSION_ID or 'default').",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=int(os.environ.get("COMPACT_THRESHOLD", DEFAULT_THRESHOLD)),
        help=f"First suggestion threshold (default: {DEFAULT_THRESHOLD}).",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.environ.get("COMPACT_INTERVAL", DEFAULT_INTERVAL)),
        help=f"Subsequent suggestion interval (default: {DEFAULT_INTERVAL}).",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display current session tool count without incrementing.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset session counter to 0.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON on stdout.",
    )
    args = parser.parse_args()

    session_id = resolve_session_id(args.session_id)
    state_file = get_state_file_path(session_id)

    if args.reset:
        if state_file.is_file():
            try:
                state_file.unlink()
            except Exception:
                pass
        if args.json:
            print(json.dumps({"session_id": session_id, "tool_calls": 0, "status": "reset"}))
        else:
            print(f"[STRATEGIC-COMPACT] Session '{session_id}' state reset.")
        return 0

    if args.status:
        state = load_state(state_file)
        if args.json:
            print(json.dumps(state))
        else:
            print(f"[STRATEGIC-COMPACT] Session: {session_id}, Tool calls: {state.get('tool_calls', 0)}")
        return 0

    count, advisory = check_and_increment(session_id, args.threshold, args.interval)

    if advisory:
        print(advisory, file=sys.stderr)

    if args.json:
        print(
            json.dumps(
                {
                    "session_id": session_id,
                    "tool_calls": count,
                    "advisory": advisory is not None,
                    "message": advisory or "",
                }
            )
        )

    # Always exit 0 for PreToolUse non-blocking hook contract
    return 0


if __name__ == "__main__":
    sys.exit(main())
