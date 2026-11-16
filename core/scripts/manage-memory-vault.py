#!/usr/bin/env python3
"""Unreviewed Memory Vault Manager & Anti-Poisoning Architecture.

Standalone CLI tool to initialize, write, search, read, and audit project/team/user
memory vaults under `.agent/memory/`.

Core Anti-Poisoning Invariant:
  All memory documents are strictly passive context (historical facts/decisions),
  NEVER executable instructions, policies, or rules. Every memory document is
  mandatorily tagged with `trust: "unreviewed"`.

Features:
  - `init`: creates directory structure with fail-closed `.gitignore` (`*\\n!.gitignore\\n`).
  - `save`: atomically writes markdown with strict YAML frontmatter (`agent.memory.v1`),
    scanning for secrets and OWASP ASI06 prompt injection patterns before persistence.
  - `search`: bounded lexical search across vault documents.
  - `read`: retrieves a memory document by ID.
  - `doctor`: audits vault integrity, schema conformance, and flags any non-unreviewed trust.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = "agent.memory.v1"
MANDATORY_TRUST = "unreviewed"
VALID_KINDS = {
    "decision",
    "fact",
    "lesson",
    "handoff",
    "note",
    "runbook",
    "context",
}
VALID_STATUSES = {"active", "superseded", "deprecated"}
VALID_SCOPES = {"project", "team", "user"}
MEMORY_SUBDIRS = [
    "contexts",
    "decisions",
    "facts",
    "handoffs",
    "lessons",
    "notes",
    "runbooks",
]

FAIL_CLOSED_GITIGNORE = "*\n!.gitignore\n"

# OWASP ASI06 Prompt Injection & Instruction Hijacking Signatures
INJECTION_PATTERNS = [
    re.compile(r"<\s*system\s*>", re.IGNORECASE),
    re.compile(r"<\s*/\s*system\s*>", re.IGNORECASE),
    re.compile(r"<\s*\|\s*im_start\s*\|>", re.IGNORECASE),
    re.compile(r"<\s*\|\s*im_end\s*\|>", re.IGNORECASE),
    re.compile(r"IGNORE\s+(ALL\s+)?PREVIOUS\s+(INSTRUCTIONS|PROMPTS|RULES)", re.IGNORECASE),
    re.compile(r"DISREGARD\s+(ALL\s+)?PRIOR\s+RULES", re.IGNORECASE),
    re.compile(r"YOU\s+ARE\s+NOW\s+(A\s+|AN\s+)?", re.IGNORECASE),
    re.compile(r"SYSTEM\s+PROMPT\s+OVERRIDE", re.IGNORECASE),
    re.compile(r"NEW\s+ROLE\s+ASSIGNMENT", re.IGNORECASE),
    re.compile(r"BYPASS\s+SAFETY\s+GUARDRAIL", re.IGNORECASE),
]

# Secret Detection Signatures
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key ID
    re.compile(r"ghp_[0-9a-zA-Z]{36}"),  # GitHub Personal Access Token
    re.compile(r"github_pat_[0-9a-zA-Z_]{82}"),  # Fine-grained GitHub Token
    re.compile(r"-----BEGIN\s+([A-Z\s]+)?PRIVATE\s+KEY-----"),  # PEM Private Key
    re.compile(r"\b(?:sk|rk)[-_]live[-_][0-9a-zA-Z]{16,}\b", re.IGNORECASE),  # Stripe/live provider secret key
    re.compile(r"\bsk[-_](?:live|test|proj|ant)?[a-zA-Z0-9_\-]{16,}\b", re.IGNORECASE),  # API keys (OpenAI, Stripe, Anthropic)
    re.compile(r"\bBearer\s+[a-zA-Z0-9_\-\.]{20,}\b", re.IGNORECASE),  # Bearer authentication token
    re.compile(
        r"(?:api_key|apikey|client_secret|secret_key|api_token|auth_token|bearer)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
        re.IGNORECASE,
    ),
]


def shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    counts: Dict[str, int] = {}
    for char in data:
        counts[char] = counts.get(char, 0) + 1
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def scan_for_secrets(content: str) -> List[str]:
    """Scan content for credentials, tokens, or high-entropy tokens (including hex secrets)."""
    violations: List[str] = []
    for pattern in SECRET_PATTERNS:
        match = pattern.search(content)
        if match:
            violations.append(f"Credential pattern detected: {match.group(0)[:12]}...")

    # High-entropy token scan:
    # 1. Hexadecimal secrets: min length 32, charset [0-9a-fA-F], theoretical max H=4.0;
    #    threshold H > 3.0 effectively catches random/crypto hex secrets while avoiding false positives.
    # 2. General base64/alphanumeric tokens: min length 24, threshold H > 4.5.
    for token in re.findall(r"[A-Za-z0-9+/=_-]{24,}", content):
        h = shannon_entropy(token)
        is_hex = bool(re.fullmatch(r"[0-9a-fA-F]+", token))
        if is_hex and len(token) >= 32 and h > 3.0:
            violations.append(f"High-entropy hex secret detected ({token[:8]}..., H={h:.2f})")
            break
        elif not is_hex and h > 4.5:
            violations.append(f"High-entropy token detected ({token[:8]}..., H={h:.2f})")
            break

    return violations


def scan_for_injections(content: str) -> List[str]:
    """Scan content for OWASP ASI06 prompt injection and instruction hijack patterns."""
    violations: List[str] = []
    for pattern in INJECTION_PATTERNS:
        match = pattern.search(content)
        if match:
            violations.append(f"Prompt injection pattern detected: '{match.group(0)}'")
    return violations


def resolve_vault_root(cli_root: Optional[str] = None) -> Path:
    """Resolve base directory for the memory vault."""
    if cli_root:
        return Path(cli_root).resolve()
    env_root = os.environ.get("AGENT_MEMORY_VAULT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    # Default to .agent/memory in current working directory
    return Path(".agent/memory").resolve()


def resolve_scope_dir(vault_root: Path, scope: str) -> Path:
    """Return path for a specific memory scope."""
    if scope not in VALID_SCOPES:
        raise ValueError(f"Invalid scope '{scope}'. Allowed: {sorted(VALID_SCOPES)}")
    return vault_root / scope


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown content."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}, text

    fm_raw = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])

    def _yaml_unescape(val: str) -> str:
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            try:
                return json.loads(val)
            except Exception:
                return val[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        return val

    # Simple YAML key-value parser for agent.memory.v1
    fm: Dict[str, Any] = {}
    current_key: Optional[str] = None
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- ") and current_key:
            val = _yaml_unescape(line[2:])
            if isinstance(fm.get(current_key), list):
                fm[current_key].append(val)
            else:
                fm[current_key] = [val]
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = _yaml_unescape(val)
            current_key = key
            if val == "":
                fm[key] = []
            else:
                fm[key] = val

    return fm, body


def yaml_escape(val: Any) -> str:
    """Sanitize and escape string value for standard YAML double-quoted scalar."""
    clean = re.sub(r"[\r\n]+", " ", str(val)).strip()
    return json.dumps(clean)


def serialize_document(fm: Dict[str, Any], body: str) -> str:
    """Serialize frontmatter dict and body into standard markdown safely."""
    lines = ["---"]
    for k in ["schema", "id", "kind", "title", "scope", "trust", "status", "created_at"]:
        if k in fm:
            lines.append(f"{k}: {yaml_escape(fm[k])}")
    if "tags" in fm and isinstance(fm["tags"], list):
        lines.append("tags:")
        for t in fm["tags"]:
            lines.append(f"  - {yaml_escape(t)}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


# CLI Commands


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize memory vault directory structure and fail-closed gitignore."""
    vault_root = resolve_vault_root(args.vault_root)
    scopes = [args.scope] if args.scope != "all" else list(VALID_SCOPES)

    for scope in scopes:
        scope_dir = resolve_scope_dir(vault_root, scope)
        scope_dir.mkdir(parents=True, exist_ok=True)

        for sub in MEMORY_SUBDIRS:
            (scope_dir / sub).mkdir(parents=True, exist_ok=True)

        # Write fail-closed .gitignore
        gitignore_path = scope_dir / ".gitignore"
        gitignore_path.write_text(FAIL_CLOSED_GITIGNORE, encoding="utf-8")

    # Also place fail-closed .gitignore at vault root
    vault_root.mkdir(parents=True, exist_ok=True)
    (vault_root / ".gitignore").write_text(FAIL_CLOSED_GITIGNORE, encoding="utf-8")

    print(f"[MEMORY-VAULT] Initialized memory vault at: {vault_root}")
    for scope in scopes:
        print(f"  - Scope: {scope} ({resolve_scope_dir(vault_root, scope)})")
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    """Atomically write memory document with strict YAML frontmatter."""
    title = re.sub(r"[\r\n]+", " ", args.title or "").strip()
    if not title:
        print("ERROR: --title is required and cannot be empty.", file=sys.stderr)
        return 1

    kind = (args.kind or "").strip().lower()
    if kind not in VALID_KINDS:
        print(f"ERROR: Invalid kind '{kind}'. Must be one of {sorted(VALID_KINDS)}", file=sys.stderr)
        return 1

    scope = (args.scope or "project").strip().lower()
    if scope not in VALID_SCOPES:
        print(f"ERROR: Invalid scope '{scope}'. Must be one of {sorted(VALID_SCOPES)}", file=sys.stderr)
        return 1

    # Sanitize tags: split by comma, collapse internal newlines in each tag, strip whitespace
    raw_tags = [
        re.sub(r"[\r\n]+", " ", t).strip()
        for t in (args.tags or "").split(",")
        if t.strip()
    ]
    raw_tags = [t for t in raw_tags if t]

    # Read body from args or stdin
    body = args.body or ""
    if args.stdin or not body:
        if not sys.stdin.isatty():
            body = sys.stdin.read()
    body = body.strip()

    if not body:
        print("ERROR: Memory body cannot be empty.", file=sys.stderr)
        return 1

    # Prepare complete ingress content (title + tags + body) for guardrail scans
    tags_scan_str = " ".join(raw_tags)
    content_to_scan = f"{title}\n{tags_scan_str}\n{body}"

    # Secret Scanning Guardrail (audits title, tags, and body)
    secret_issues = scan_for_secrets(content_to_scan)
    if secret_issues:
        print("ERROR: Memory persistence rejected by secret scanner:", file=sys.stderr)
        for issue in secret_issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    # OWASP ASI06 Prompt Injection Guardrail (audits title, tags, and body)
    injection_issues = scan_for_injections(content_to_scan)
    if injection_issues:
        print("ERROR: Memory persistence rejected by OWASP ASI06 prompt injection scanner:", file=sys.stderr)
        for issue in injection_issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    # Generate document ID and metadata
    now = datetime.datetime.now(datetime.timezone.utc)
    ts_str = now.strftime("%Y%m%d%H%M%S")
    iso_time = now.isoformat()
    h = hashlib.sha256(f"{title}:{ts_str}:{body}".encode("utf-8")).hexdigest()[:8]
    doc_id = f"mem-{scope}-{ts_str}-{h}"

    fm: Dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "id": doc_id,
        "kind": kind,
        "title": title,
        "scope": scope,
        "trust": MANDATORY_TRUST,  # Invariant: hardcoded unreviewed
        "status": "active",
        "created_at": iso_time,
        "tags": raw_tags,
    }

    doc_text = serialize_document(fm, body)

    # Destination directory based on kind plural
    vault_root = resolve_vault_root(args.vault_root)
    scope_dir = resolve_scope_dir(vault_root, scope)
    kind_dir = scope_dir / (f"{kind}s" if not kind.endswith("s") else kind)
    kind_dir.mkdir(parents=True, exist_ok=True)

    dest_file = kind_dir / f"{doc_id}.md"

    # Atomic write via temp file
    tmp_file = kind_dir / f".tmp_{doc_id}_{os.getpid()}.md"
    try:
        tmp_file.write_text(doc_text, encoding="utf-8")
        tmp_file.replace(dest_file)
    except Exception as exc:
        print(f"ERROR writing memory file: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"id": doc_id, "path": str(dest_file), "kind": kind, "title": title, "trust": MANDATORY_TRUST}))
    else:
        print(f"[MEMORY-VAULT] Saved memory: {doc_id}")
        print(f"  Kind:  {kind}")
        print(f"  Title: {title}")
        print(f"  Trust: {MANDATORY_TRUST} (unreviewed invariant)")
        print(f"  File:  {dest_file}")

    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Bounded lexical search across memory documents."""
    query = (args.query or "").strip().lower()
    if not query:
        print("ERROR: Search query cannot be empty.", file=sys.stderr)
        return 1

    vault_root = resolve_vault_root(args.vault_root)
    scopes = [args.scope] if args.scope != "all" else list(VALID_SCOPES)
    limit = args.limit or 20

    results: List[Dict[str, Any]] = []

    for scope in scopes:
        scope_dir = resolve_scope_dir(vault_root, scope)
        if not scope_dir.is_dir():
            continue
        for md_file in scope_dir.glob("*/*.md"):
            if md_file.name.startswith("."):
                continue
            try:
                text = md_file.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(text)
                title = str(fm.get("title", "")).lower()
                tags = [str(t).lower() for t in fm.get("tags", [])]
                body_lower = body.lower()

                if query in title or any(query in t for t in tags) or query in body_lower:
                    # Extract snippet
                    idx = body_lower.find(query)
                    start = max(0, idx - 40)
                    end = min(len(body), idx + len(query) + 40)
                    snippet = body[start:end].replace("\n", " ").strip()
                    results.append(
                        {
                            "id": fm.get("id", md_file.stem),
                            "kind": fm.get("kind", md_file.parent.name),
                            "title": fm.get("title", ""),
                            "scope": scope,
                            "trust": fm.get("trust", "unknown"),
                            "created_at": fm.get("created_at", ""),
                            "tags": fm.get("tags", []),
                            "snippet": f"...{snippet}..." if idx != -1 else "",
                            "path": str(md_file),
                        }
                    )
            except Exception:
                continue

    # Sort results newest first
    results.sort(key=lambda r: str(r.get("created_at", "")), reverse=True)
    results = results[:limit]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"[MEMORY-VAULT] Search results for '{query}' ({len(results)} matches, limit {limit}):")
        if not results:
            print("  (no matches found)")
        for r in results:
            print(f"  [{r['id']}] ({r['kind']}, trust={r['trust']}) {r['title']}")
            if r["snippet"]:
                print(f"    Snippet: {r['snippet']}")

    return 0


def cmd_read(args: argparse.Namespace) -> int:
    """Read a memory document by ID."""
    doc_id = (args.id or "").strip()
    if not doc_id:
        print("ERROR: Memory document ID is required.", file=sys.stderr)
        return 1

    vault_root = resolve_vault_root(args.vault_root)
    scopes = [args.scope] if args.scope != "all" else list(VALID_SCOPES)

    target_file: Optional[Path] = None
    for scope in scopes:
        scope_dir = resolve_scope_dir(vault_root, scope)
        if not scope_dir.is_dir():
            continue
        # Direct check
        for md_file in scope_dir.glob(f"*/*{doc_id}*.md"):
            if md_file.name.startswith("."):
                continue
            target_file = md_file
            break
        if target_file:
            break

    if not target_file or not target_file.is_file():
        print(f"ERROR: Memory document '{doc_id}' not found.", file=sys.stderr)
        return 1

    text = target_file.read_text(encoding="utf-8")
    if args.json:
        fm, body = parse_frontmatter(text)
        print(json.dumps({"metadata": fm, "body": body, "path": str(target_file)}, indent=2))
    else:
        print(text)

    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Audit vault integrity, schema conformance, and anti-poisoning invariants."""
    vault_root = resolve_vault_root(args.vault_root)
    scopes = [args.scope] if args.scope != "all" else list(VALID_SCOPES)

    errors: List[str] = []
    warnings: List[str] = []
    scanned_count = 0

    if not vault_root.is_dir():
        errors.append(f"Vault root does not exist: {vault_root}")
        print("Doctor Audit FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    # Check root gitignore
    root_gitignore = vault_root / ".gitignore"
    if not root_gitignore.is_file() or FAIL_CLOSED_GITIGNORE.strip() not in root_gitignore.read_text(encoding="utf-8"):
        warnings.append(f"Root .gitignore missing or incomplete at {root_gitignore}")

    for scope in scopes:
        scope_dir = resolve_scope_dir(vault_root, scope)
        if not scope_dir.is_dir():
            continue

        scope_gitignore = scope_dir / ".gitignore"
        if not scope_gitignore.is_file() or FAIL_CLOSED_GITIGNORE.strip() not in scope_gitignore.read_text(encoding="utf-8"):
            warnings.append(f"Fail-closed .gitignore missing in scope: {scope_dir}")

        for md_file in scope_dir.glob("*/*.md"):
            if md_file.name.startswith("."):
                continue
            scanned_count += 1
            rel_path = md_file.relative_to(vault_root)
            try:
                text = md_file.read_text(encoding="utf-8")
            except Exception as exc:
                errors.append(f"{rel_path}: unreadable file: {exc}")
                continue

            fm, body = parse_frontmatter(text)
            if not fm:
                errors.append(f"{rel_path}: missing or invalid YAML frontmatter")
                continue

            # Invariant: schema check
            if fm.get("schema") != SCHEMA_VERSION:
                errors.append(f"{rel_path}: invalid schema '{fm.get('schema')}', expected '{SCHEMA_VERSION}'")

            # CRITICAL Anti-poisoning Invariant: trust MUST be "unreviewed"
            trust = fm.get("trust")
            if trust != MANDATORY_TRUST:
                errors.append(
                    f"{rel_path}: SECURITY INVARIANT VIOLATION: trust is '{trust}', "
                    f"must be strictly '{MANDATORY_TRUST}'"
                )

            # Kind check
            kind = fm.get("kind")
            if kind not in VALID_KINDS:
                errors.append(f"{rel_path}: unknown kind '{kind}'")

            # Status check
            status = fm.get("status")
            if status not in VALID_STATUSES:
                errors.append(f"{rel_path}: invalid status '{status}'")

            # Secret / credential check on existing file
            secrets = scan_for_secrets(text)
            if secrets:
                errors.append(f"{rel_path}: secret/credential detected: {secrets[0]}")

            # Injection check on existing file
            injections = scan_for_injections(text)
            if injections:
                errors.append(f"{rel_path}: prompt injection signature detected: {injections[0]}")

    print(f"[MEMORY-VAULT DOCTOR] Scanned {scanned_count} document(s) across {len(scopes)} scope(s).")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
        return 1

    print("Status: HEALTHY. Anti-poisoning invariant verified (all memories passive & unreviewed).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unreviewed Memory Vault Manager: passive context storage with anti-poisoning architecture."
    )
    parser.add_argument(
        "--vault-root",
        type=str,
        default=None,
        help="Vault root directory (default: .agent/memory).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialize memory vault directory structure.")
    p_init.add_argument(
        "--scope",
        choices=["project", "team", "user", "all"],
        default="project",
        help="Scope to initialize (default: project).",
    )

    # save
    p_save = subparsers.add_parser("save", help="Atomically save a memory document with unreviewed trust.")
    p_save.add_argument("--title", required=True, help="Memory document title.")
    p_save.add_argument(
        "--kind",
        choices=sorted(VALID_KINDS),
        required=True,
        help="Memory kind classification.",
    )
    p_save.add_argument("--tags", default="", help="Comma-separated tags.")
    p_save.add_argument("--body", default=None, help="Document markdown body.")
    p_save.add_argument(
        "--scope",
        choices=["project", "team", "user"],
        default="project",
        help="Scope (default: project).",
    )
    p_save.add_argument("--stdin", action="store_true", help="Read body from stdin.")
    p_save.add_argument("--json", action="store_true", help="Output result as JSON.")

    # search
    p_search = subparsers.add_parser("search", help="Search memory documents by keyword.")
    p_search.add_argument("query", help="Lexical search query string.")
    p_search.add_argument(
        "--scope",
        choices=["project", "team", "user", "all"],
        default="all",
        help="Scope to search in (default: all).",
    )
    p_search.add_argument("--limit", type=int, default=20, help="Max results (default: 20).")
    p_search.add_argument("--json", action="store_true", help="Output results as JSON.")

    # read
    p_read = subparsers.add_parser("read", help="Read a memory document by ID.")
    p_read.add_argument("id", help="Memory document ID.")
    p_read.add_argument(
        "--scope",
        choices=["project", "team", "user", "all"],
        default="all",
        help="Scope to search in (default: all).",
    )
    p_read.add_argument("--json", action="store_true", help="Output as JSON.")

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Audit memory vault integrity and anti-poisoning invariants.")
    p_doctor.add_argument(
        "--scope",
        choices=["project", "team", "user", "all"],
        default="all",
        help="Scope to audit (default: all).",
    )

    args = parser.parse_args()

    cmd_map = {
        "init": cmd_init,
        "save": cmd_save,
        "search": cmd_search,
        "read": cmd_read,
        "doctor": cmd_doctor,
    }

    return cmd_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
