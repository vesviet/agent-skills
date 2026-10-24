#!/usr/bin/env python3
"""Deterministic CLI utility for auditing, triaging, and pruning agent persistent memory stores.

Conforms to Draft 2020-12 schema in core/contracts/schemas/memory-audit-report.json.
Provides:
  - Dead path detection against live filesystem
  - Duplicate / redundant instruction detection
  - Line and token budget calculation and enforcement
  - 5-tier triage classification ([active], [stale], [redundant], [resolved], [poisoned])
  - OWASP ASI06 context & memory poisoning defense (secret detection & instruction injection quarantine)
  - Archival offloading
  - Exit codes: 0 = clean/success, 1 = violations in --check mode, 2 = fatal error
"""

from __future__ import annotations

import argparse
import collections
import datetime
import difflib
import json
import math
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any

PATH_EXTENSIONS = {
    ".md", ".ts", ".js", ".php", ".py", ".json", ".yaml", ".yml",
    ".sql", ".sh", ".go", ".rs", ".html", ".css", ".txt", ".toml",
    ".lock", ".template", ".rules", ".conf", ".ini", ".proto",
}

NON_PATH_COMMANDS = {
    "git", "pytest", "curl", "docker", "npm", "node", "python", "python3",
    "bash", "sh", "yarn", "pnpm", "composer", "cargo", "make", "cat",
    "grep", "sed", "awk", "rm", "mv", "cp", "echo", "true", "false",
}

HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}

NEGATION_TOKENS = {
    "not", "never", "no", "without", "except", "prevent", "avoid",
    "neither", "nor", "none", "dont", "don't"
}

PROMPT_INJECTION_REGEX = re.compile(
    r"(?i)(?:<system>|</system>|\b(?:ignore\s+(?:all\s+)?previous\s+(?:instructions|rules)|(?:ai\s+)?system\s+(?:prompt\s+)?override|override\s+(?:ai\s+)?system\s+prompt|ai\s+system\s+prompt|disregard\s+prior\s+(?:instructions|rules))\b|\[poisoned\])"
)

SECRET_PATTERNS = [
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b")),
    ("jwt_token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("api_key_prefix", re.compile(r"\b(?:sk[-_](?:live|ant|proj)?[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9_-]{20,})\b")),
    ("generic_secret", re.compile(r"(?:api[_-]?key|secret|token|password|bearer)\s*[:= ]\s*['\"]?([A-Za-z0-9_\-\.]{20,})['\"]?", re.IGNORECASE)),
]

DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:?\d{2}|Z)?)?)\b")


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="prune-memory.py",
        description="Audit, triage, compact, and prune persistent agent memory files.",
    )
    parser.add_argument(
        "--file", "-f",
        default="MEMORY.md",
        help="Target memory file to audit and prune (default: MEMORY.md)",
    )
    parser.add_argument(
        "--repo-root", "-r",
        default=".",
        help="Root directory for resolving relative file paths (default: cwd)",
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Audit-only mode. Does not mutate files. Exits 1 if violations detected, 0 if clean.",
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Simulate pruning and output preview without writing changes to disk.",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Destination path for pruned markdown (default: in-place overwrite of --file).",
    )
    parser.add_argument(
        "--threshold", "-t",
        type=int,
        default=30,
        help="Staleness threshold in days for unverified entries (default: 30).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: text (human-readable) or json (conforming to memory-audit-report.json).",
    )
    parser.add_argument(
        "--line-budget",
        type=int,
        default=100,
        help="Maximum allowable lines in target memory file (default: 100).",
    )
    parser.add_argument(
        "--token-budget",
        type=int,
        default=1500,
        help="Maximum allowable tokens in target memory file (default: 1500).",
    )
    parser.add_argument(
        "--archive", "-a",
        default=None,
        help="Path to archive file to append pruned stale/resolved entries.",
    )
    parser.add_argument(
        "--ingest-checkpoint",
        default=None,
        help="Path to compact-working-state.json checkpoint to ingest into persistent memory.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable detailed diagnostic logs on stderr.",
    )
    return parser.parse_args(args)


def estimate_tokens(text: str) -> int:
    """Deterministic token estimation (or tiktoken if available)."""
    try:
        import tiktoken  # type: ignore
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        if not text:
            return 0
        words = len(text.split())
        chars = len(text)
        return max(math.ceil(chars / 4), math.ceil(words * 1.33))


def calculate_shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    counts = collections.Counter(data)
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def extract_candidate_paths(text: str) -> list[str]:
    candidates: list[str] = []
    # 1. Backtick strings: `...`
    for match in re.findall(r"`([^`]+)`", text):
        cleaned = match.strip()
        if not cleaned:
            continue
        if cleaned.startswith("-") or cleaned.startswith("?"):
            continue
        first_word = cleaned.split()[0] if cleaned.split() else ""
        if first_word.upper() in HTTP_METHODS or first_word in NON_PATH_COMMANDS:
            continue
        if re.match(r"^\d+/\d+$", cleaned):
            continue
        if re.search(r"/\*$", cleaned) or re.match(r"^/(?:api|v\d+|product|channel|webhook|internal)/", cleaned):
            continue
        if " " in cleaned:
            suffix = Path(cleaned).suffix.lower()
            if suffix not in PATH_EXTENSIONS or any(w.startswith("-") for w in cleaned.split()):
                continue
        cleaned = re.sub(r"#[^/]*$", "", cleaned)
        candidates.append(cleaned)

    # 2. Markdown links: [text](path)
    for match in re.findall(r"\[([^\]]+)\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
        cleaned = match[1].strip()
        if not cleaned or cleaned.startswith(("http://", "https://", "mailto:", "ftp://")):
            continue
        candidates.append(cleaned)

    valid_candidates: list[str] = []
    for c in candidates:
        p = c.strip(" ,;:)'\"[]*")
        if not p:
            continue
        if p.startswith("http://") or p.startswith("https://") or p.startswith("mailto:") or p.startswith("ftp://"):
            continue
        if p in NON_PATH_COMMANDS:
            continue
        if re.match(r"^\d+(\.\d+)*$", p) or re.match(r"^\d{4}-\d{2}-\d{2}", p):
            continue
        if re.match(r"^\d+/\d+$", p):
            continue
        has_slash = "/" in p
        suffix = Path(p).suffix.lower()
        has_ext = suffix in PATH_EXTENSIONS
        ends_with_slash = c.strip().endswith("/") or p.endswith("/")

        if has_slash and not has_ext and not ends_with_slash:
            if not (p.startswith("./") or p.startswith("../") or p.startswith(".agents/") or p.startswith(".")):
                parts = p.split("/")
                if len(parts) == 2 and (
                    re.match(r"^[A-Z]{2,5}/[A-Z]{2,5}$", p)
                    or p.lower() in ("and/or", "true/false", "read/write", "in/out", "yes/no", "on/off")
                    or re.match(r"^[A-Za-z0-9_]+/[A-Z0-9_]+$", p)
                ):
                    continue

        if has_ext or ends_with_slash or has_slash:
            if p.endswith("/*"):
                p = p[:-2]
            elif p.endswith("*"):
                p = p[:-1]
            if p and p not in valid_candidates:
                valid_candidates.append(p)

    return valid_candidates


def is_dead_path(candidate: str, repo_root: Path, file_dir: Path) -> bool:
    candidate = re.sub(r"#[^/]*$", "", candidate)
    p = Path(candidate)
    if p.is_absolute():
        return not p.exists()
    if (repo_root / candidate).exists():
        return False
    if (file_dir / candidate).exists():
        return False
    return True


def normalize_instruction(text: str) -> str:
    s = re.sub(r"^\s*[-*+]\s*(\[[ xX]\]\s*)?", "", text)
    s = re.sub(r"^\s*\d+\.\s*", "", s)
    s = re.sub(r"[*_`]", "", s)
    s = s.replace("|", " ")
    s = re.sub(r"[^\w\s]", "", s).lower().strip()
    return " ".join(s.split())


class MemoryEntry:
    def __init__(
        self,
        line_idx: int,
        raw_line: str,
        entry_id: str,
        topic: str,
        content: str,
        is_table_row: bool = False,
    ):
        self.line_idx = line_idx
        self.raw_line = raw_line
        self.entry_id = entry_id
        self.topic = topic
        self.content = content
        self.is_table_row = is_table_row
        self.classification = "active"  # active, stale, redundant, resolved, poisoned
        self.reason = "Active operational memory entry"
        self.referenced_paths: list[str] = []
        self.dead_paths: list[str] = []
        self.action_taken = "retained"  # retained, updated, compacted, archived, quarantined, deleted


def parse_memory_file(content: str) -> tuple[list[str], list[MemoryEntry]]:
    lines = content.splitlines()
    entries: list[MemoryEntry] = []
    current_section = "General"
    entry_counter = 1
    in_code_block = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Section headings
        if stripped.startswith("#"):
            current_section = stripped.lstrip("#").strip()
            continue

        # Skip separators and empty lines
        if not stripped or stripped.startswith("---") or stripped.startswith(">"):
            continue

        # Table rows
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Skip separator rows like |---|---|
            if any(set(c).issubset({"-", " ", ":"}) for c in cells if c):
                continue
            # Skip table headers (like Field / Value, ID / Topic)
            if any(c.lower() in ("field", "id", "session topic", "topic", "status") for c in cells):
                continue

            # This is a data row
            first_cell = re.sub(r"[*_`]", "", cells[0]).strip()
            topic = current_section
            entry_id = f"M-{entry_counter:02d}"

            if len(cells) >= 3 and (first_cell.startswith("M-") or first_cell.startswith("C-") or re.match(r"^[A-Z0-9\-\.]+$", first_cell)):
                entry_id = first_cell
                topic = re.sub(r"[*_`]", "", cells[1]).strip() or current_section
                content_text = " | ".join(cells[2:])
            elif len(cells) >= 2:
                topic = first_cell or current_section
                content_text = cells[1]
                entry_id = f"T-{entry_counter:02d}"
            else:
                content_text = stripped

            entry_counter += 1
            entries.append(
                MemoryEntry(
                    line_idx=idx,
                    raw_line=line,
                    entry_id=entry_id,
                    topic=topic,
                    content=content_text,
                    is_table_row=True,
                )
            )
            continue

        # Bullet list items
        if re.match(r"^\s*[-*+]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            cleaned = re.sub(r"^\s*[-*+]\s*(\[[ xX]\]\s*)?", "", line)
            cleaned = re.sub(r"^\s*\d+\.\s*", "", cleaned)
            # Check if there is bold topic prefix like - **Topic:** ...
            topic = current_section
            topic_match = re.match(r"^\*\*([^*]+)\*\*[:\s]*(.*)", cleaned)
            if topic_match:
                topic = topic_match.group(1).strip()
                content_text = topic_match.group(2).strip()
            else:
                content_text = cleaned

            entry_id = f"L-{entry_counter:02d}"
            entry_counter += 1
            entries.append(
                MemoryEntry(
                    line_idx=idx,
                    raw_line=line,
                    entry_id=entry_id,
                    topic=topic,
                    content=content_text,
                    is_table_row=False,
                )
            )
            continue

        # Normal text line that might be an instruction/rule
        if len(stripped) > 5 and not stripped.startswith("<!--"):
            entry_id = f"P-{entry_counter:02d}"
            entry_counter += 1
            entries.append(
                MemoryEntry(
                    line_idx=idx,
                    raw_line=line,
                    entry_id=entry_id,
                    topic=current_section,
                    content=stripped,
                    is_table_row=False,
                )
            )

    return lines, entries


def prune_and_audit(
    file_path: Path,
    repo_root: Path,
    check_mode: bool = False,
    dry_run: bool = False,
    output_path: Path | None = None,
    threshold_days: int = 30,
    line_budget: int = 100,
    token_budget: int = 1500,
    archive_path: Path | None = None,
    verbose: bool = False,
) -> tuple[dict[str, Any], str, list[str]]:
    """Execute audit, classification, triage, pruning, and return structured audit payload."""
    raw_content = file_path.read_text(encoding="utf-8")
    lines_before = len(raw_content.splitlines())
    tokens_before = estimate_tokens(raw_content)

    file_dir = file_path.resolve().parent
    repo_root = repo_root.resolve()

    original_lines, entries = parse_memory_file(raw_content)

    now = datetime.datetime.now(datetime.timezone.utc)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    sanitized_items: list[dict[str, str]] = []
    secrets_detected = 0
    poisoned_quarantined = 0

    seen_instructions: list[tuple[str, MemoryEntry]] = []
    findings: list[dict[str, Any]] = []

    lines_to_remove: set[int] = set()
    archived_lines: list[str] = []

    finding_idx = 1

    for entry in entries:
        finding_id = f"F-{finding_idx:02d}"
        line = entry.raw_line
        clean_line = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", line)

        # 1. OWASP ASI06 Prompt Injection Check
        if PROMPT_INJECTION_REGEX.search(clean_line):
            entry.classification = "poisoned"
            entry.reason = "OWASP ASI06: Adversarial prompt injection instruction detected"
            entry.action_taken = "quarantined"
            poisoned_quarantined += 1
            sanitized_items.append({
                "finding_id": finding_id,
                "threat_type": "hidden_instruction",
                "action": "quarantined",
                "details": f"Quarantined prompt injection in entry '{entry.topic}': '{line.strip()[:60]}...'",
            })
            lines_to_remove.add(entry.line_idx)
            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "action_taken": entry.action_taken,
            })
            continue

        # 2. OWASP ASI06 Secret & Entropy Detection
        has_secret = False
        for secret_name, pat in SECRET_PATTERNS:
            if pat.search(line):
                has_secret = True
                break
        if not has_secret:
            # Check continuous tokens for Shannon entropy > 4.5 or long hex tokens
            for token in re.findall(r"\b[A-Za-z0-9_\-\.]{20,}\b", line):
                h = calculate_shannon_entropy(token)
                if h > 4.5 or (len(token) >= 32 and h > 3.5 and all(c in "0123456789abcdefABCDEF-_" for c in token)):
                    has_secret = True
                    break

        if has_secret:
            secrets_detected += 1
            sanitized_items.append({
                "finding_id": finding_id,
                "threat_type": "credential_leak",
                "action": "masked",
                "details": f"Detected high-entropy credential or secret pattern in '{entry.topic}'.",
            })
            # Also quarantine or mask secret
            entry.classification = "poisoned"
            entry.reason = "OWASP ASI06: High-entropy secret / credential leak detected"
            entry.action_taken = "quarantined"
            poisoned_quarantined += 1
            lines_to_remove.add(entry.line_idx)
            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "action_taken": entry.action_taken,
            })
            continue

        # 3. Path Extraction & Live Filesystem Probing
        candidate_paths = extract_candidate_paths(line)
        entry.referenced_paths = candidate_paths
        entry.dead_paths = [p for p in candidate_paths if is_dead_path(p, repo_root, file_dir)]

        if entry.dead_paths:
            entry.classification = "stale"
            entry.reason = f"Referenced dead path(s): {', '.join(entry.dead_paths)}"
            lines_to_remove.add(entry.line_idx)
            if archive_path:
                entry.action_taken = "archived"
                archived_lines.append(line)
            else:
                entry.action_taken = "deleted"

            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "referenced_paths": entry.referenced_paths,
                "dead_paths": entry.dead_paths,
                "action_taken": entry.action_taken,
            })
            continue

        # 4. Explicit Status Tags
        line_lower = line.lower()
        if "[stale]" in line_lower:
            entry.classification = "stale"
            entry.reason = "Explicit [stale] tag"
            lines_to_remove.add(entry.line_idx)
            if archive_path:
                entry.action_taken = "archived"
                archived_lines.append(line)
            else:
                entry.action_taken = "deleted"
            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "action_taken": entry.action_taken,
            })
            continue

        if "[redundant]" in line_lower:
            entry.classification = "redundant"
            entry.reason = "Explicit [redundant] tag"
            entry.action_taken = "deleted"
            lines_to_remove.add(entry.line_idx)
            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "action_taken": entry.action_taken,
            })
            continue

        if "[resolved]" in line_lower or "| resolved |" in line_lower or "status: resolved" in line_lower:
            entry.classification = "resolved"
            entry.reason = "Resolved historical milestone"
            if archive_path:
                entry.action_taken = "archived"
                lines_to_remove.add(entry.line_idx)
                archived_lines.append(line)
            else:
                entry.action_taken = "retained"
            finding_idx += 1
            findings.append({
                "finding_id": finding_id,
                "entry_id": entry.entry_id,
                "classification": entry.classification,
                "topic": entry.topic,
                "raw_content": line.strip(),
                "reason": entry.reason,
                "action_taken": entry.action_taken,
            })
            continue

        # 5. Temporal Staleness
        date_match = DATE_PATTERN.search(line)
        if date_match:
            date_str = date_match.group(1)[:10]
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
                age_days = (now - entry_date).days
                if age_days > threshold_days:
                    entry.classification = "stale"
                    entry.reason = f"Entry date ({date_str}) exceeds staleness threshold ({age_days} > {threshold_days} days)"
                    lines_to_remove.add(entry.line_idx)
                    if archive_path:
                        entry.action_taken = "archived"
                        archived_lines.append(line)
                    else:
                        entry.action_taken = "deleted"
                    finding_idx += 1
                    findings.append({
                        "finding_id": finding_id,
                        "entry_id": entry.entry_id,
                        "classification": entry.classification,
                        "topic": entry.topic,
                        "raw_content": line.strip(),
                        "reason": entry.reason,
                        "action_taken": entry.action_taken,
                    })
                    continue
            except Exception:
                pass

        # 6. Duplicate / Redundant Instruction Detection
        norm = normalize_instruction(entry.content or line)
        if norm and len(norm) > 10:
            duplicate_found = False
            words_curr = set(norm.split())
            neg_curr = words_curr & NEGATION_TOKENS
            for prev_norm, prev_entry in seen_instructions:
                words_prev = set(prev_norm.split())
                neg_prev = words_prev & NEGATION_TOKENS
                if neg_curr != neg_prev:
                    continue
                if norm == prev_norm or difflib.SequenceMatcher(None, norm, prev_norm).ratio() >= 0.85:
                    duplicate_found = True
                    entry.classification = "redundant"
                    entry.reason = f"Duplicate or redundant with '{prev_entry.topic or prev_entry.entry_id}'"
                    entry.action_taken = "deleted"
                    lines_to_remove.add(entry.line_idx)
                    finding_idx += 1
                    findings.append({
                        "finding_id": finding_id,
                        "entry_id": entry.entry_id,
                        "classification": entry.classification,
                        "topic": entry.topic,
                        "raw_content": line.strip(),
                        "reason": entry.reason,
                        "action_taken": entry.action_taken,
                    })
                    break

            if duplicate_found:
                continue

            seen_instructions.append((norm, entry))

        # 7. Otherwise Clean / Active Entry
        entry.classification = "active"
        entry.action_taken = "retained"
        entry.reason = "Active operational entry verified against disk truth"

    # Construct Pruned Content
    pruned_lines: list[str] = []
    for idx, line in enumerate(original_lines):
        if idx in lines_to_remove:
            continue
        # Update Last cleaned header timestamp if present
        if re.search(r"Last cleaned:", line):
            line = re.sub(
                r"(Last cleaned:\s*\*?\*?)[^|*\n]+",
                rf"\g<1>{now_iso} ",
                line,
            )
        pruned_lines.append(line)

    pruned_content = "\n".join(pruned_lines)
    if pruned_lines and not pruned_content.endswith("\n"):
        pruned_content += "\n"

    lines_after = len(pruned_lines) if not check_mode else lines_before
    tokens_after = estimate_tokens(pruned_content) if not check_mode else tokens_before
    token_delta = tokens_before - tokens_after
    token_reduction_pct = round((token_delta / tokens_before * 100), 1) if tokens_before > 0 else 0.0
    if token_reduction_pct < 0:
        token_reduction_pct = 0.0

    # Triage summary counts
    active_count = sum(1 for e in entries if e.classification == "active")
    stale_count = sum(1 for e in entries if e.classification == "stale")
    redundant_count = sum(1 for e in entries if e.classification == "redundant")
    resolved_count = sum(1 for e in entries if e.classification == "resolved")
    poisoned_count = sum(1 for e in entries if e.classification == "poisoned")
    total_entries = len(entries)

    # Determine runtime mode
    if check_mode:
        runtime_mode = "check"
    elif dry_run:
        runtime_mode = "dry-run"
    elif archive_path and not output_path:
        runtime_mode = "in-place"
    else:
        runtime_mode = "in-place"

    # Target file relative path
    try:
        rel_target = str(file_path.relative_to(repo_root))
    except Exception:
        rel_target = str(file_path)

    # Budget checks
    target_lines = lines_before if check_mode else lines_after
    target_tokens = tokens_before if check_mode else tokens_after
    line_budget_exceeded = target_lines > line_budget
    budget_exceeded = target_tokens > token_budget

    audit_payload: dict[str, Any] = {
        "contract_type": "memory-audit-report",
        "audit_id": f"MEM-AUDIT-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
        "target_file": rel_target,
        "audited_at": now_iso,
        "auditor": {
            "role": "prompt-engineer",
            "tool": "prune-memory.py",
            "runtime_mode": runtime_mode,
        },
        "lifecycle_phase": "triage" if (check_mode or dry_run) else ("archival" if archive_path else "compaction"),
        "token_metrics": {
            "tokens_before": tokens_before,
            "tokens_after": tokens_after,
            "token_delta": token_delta,
            "token_reduction_pct": token_reduction_pct,
            "budget_token_cap": token_budget,
            "budget_exceeded": budget_exceeded,
        },
        "line_metrics": {
            "lines_before": lines_before,
            "lines_after": lines_after,
            "line_budget_cap": line_budget,
            "line_budget_exceeded": line_budget_exceeded,
        },
        "entry_triage_summary": {
            "active_count": active_count,
            "stale_count": stale_count,
            "redundant_count": redundant_count,
            "resolved_count": resolved_count,
            "poisoned_count": poisoned_count,
            "total_entries": total_entries,
        },
        "findings": findings,
        "security_sanitization": {
            "owasp_asi06_checked": True,
            "secrets_detected": secrets_detected,
            "poisoned_entries_quarantined": poisoned_quarantined,
            "sanitized_items": sanitized_items,
        },
    }

    if archive_path:
        audit_payload["archival_target"] = str(archive_path)

    return audit_payload, pruned_content, archived_lines


def format_text_report(payload: dict[str, Any], preview_text: str | None = None) -> str:
    lines = [
        "=" * 72,
        f"Memory Audit & Hygiene Report: {payload['target_file']}",
        f"Audit ID: {payload['audit_id']} | Audited At: {payload['audited_at']}",
        f"Auditor: {payload['auditor']['role']} via {payload['auditor']['tool']} ({payload['auditor']['runtime_mode']})",
        "=" * 72,
        "",
        "--- Metrics & Budget ---",
        f"Tokens: {payload['token_metrics']['tokens_before']} -> {payload['token_metrics']['tokens_after']} (Delta: -{payload['token_metrics']['token_delta']}, -{payload['token_metrics']['token_reduction_pct']}%) [Cap: {payload['token_metrics']['budget_token_cap']}] - Exceeded: {payload['token_metrics']['budget_exceeded']}",
        f"Lines:  {payload['line_metrics']['lines_before']} -> {payload['line_metrics']['lines_after']} [Cap: {payload['line_metrics']['line_budget_cap']}] - Exceeded: {payload['line_metrics']['line_budget_exceeded']}",
        "",
        "--- Entry Triage Summary ---",
        f"Active:    {payload['entry_triage_summary']['active_count']}",
        f"Stale:     {payload['entry_triage_summary']['stale_count']}",
        f"Redundant: {payload['entry_triage_summary']['redundant_count']}",
        f"Resolved:  {payload['entry_triage_summary']['resolved_count']}",
        f"Poisoned:  {payload['entry_triage_summary']['poisoned_count']}",
        f"Total:     {payload['entry_triage_summary']['total_entries']}",
        "",
        "--- Security Sanitization (OWASP ASI06) ---",
        f"OWASP ASI06 Checked: {payload['security_sanitization']['owasp_asi06_checked']}",
        f"Secrets Detected:     {payload['security_sanitization']['secrets_detected']}",
        f"Poisoned Quarantined: {payload['security_sanitization']['poisoned_entries_quarantined']}",
    ]

    if payload["security_sanitization"]["sanitized_items"]:
        lines.append("Sanitized Items:")
        for item in payload["security_sanitization"]["sanitized_items"]:
            lines.append(f"  - [{item['threat_type']}] {item['finding_id']}: {item['details']} ({item['action']})")

    if payload["findings"]:
        lines.append("")
        lines.append("--- Findings ---")
        for f in payload["findings"]:
            paths_info = ""
            if "dead_paths" in f and f["dead_paths"]:
                paths_info = f" [Dead: {', '.join(f['dead_paths'])}]"
            lines.append(f"  * {f['finding_id']} [{f['classification'].upper()}] {f['topic']}: {f['reason']}{paths_info} -> {f['action_taken']}")

    if preview_text is not None:
        lines.append("")
        lines.append("--- Pruned Content Preview ---")
        lines.append(preview_text.strip())

    lines.append("=" * 72)
    return "\n".join(lines)


def ingest_checkpoint_and_audit(
    checkpoint_path: Path,
    target_file: Path,
    repo_root: Path,
    check_mode: bool = False,
    dry_run: bool = False,
    output_path: Path | None = None,
    line_budget: int = 100,
    token_budget: int = 1500,
    archive_path: Path | None = None,
    verbose: bool = False,
) -> tuple[dict[str, Any], str, list[str]]:
    """Ingest a compact-working-state.json checkpoint into persistent memory."""
    now = datetime.datetime.now(datetime.timezone.utc)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    raw_checkpoint = checkpoint_path.read_text(encoding="utf-8")
    ckpt = json.loads(raw_checkpoint)

    existing_content = target_file.read_text(encoding="utf-8") if target_file.exists() else ""
    lines_before = len(existing_content.splitlines()) if existing_content else 0
    tokens_before = estimate_tokens(existing_content) if existing_content else 0

    findings: list[dict[str, Any]] = []
    sanitized_items: list[dict[str, Any]] = []
    secrets_detected = 0
    poisoned_quarantined = 0

    def sanitize_field(val: str, field_name: str) -> str:
        nonlocal secrets_detected, poisoned_quarantined
        if not val or not isinstance(val, str):
            return ""

        if PROMPT_INJECTION_REGEX.search(val):
            poisoned_quarantined += 1
            f_id = f"SEC-{len(sanitized_items)+1:02d}"
            sanitized_items.append({
                "finding_id": f_id,
                "threat_type": "hidden_instruction",
                "action": "quarantined",
                "details": f"Prompt injection pattern detected in {field_name}",
            })
            findings.append({
                "finding_id": f_id,
                "entry_id": f"INJ-{len(findings)+1:02d}",
                "classification": "poisoned",
                "topic": field_name,
                "raw_content": val[:80],
                "reason": f"OWASP ASI06: Prompt injection pattern detected in {field_name}",
                "referenced_paths": [],
                "dead_paths": [],
                "action_taken": "quarantined",
            })
            return "[QUARANTINED_INJECTION]"

        for sec_name, pattern in SECRET_PATTERNS:
            if pattern.search(val):
                secrets_detected += 1
                f_id = f"SEC-{len(sanitized_items)+1:02d}"
                sanitized_items.append({
                    "finding_id": f_id,
                    "threat_type": "credential_leak",
                    "action": "redacted",
                    "details": f"Secret pattern ({sec_name}) detected in {field_name}",
                })
                findings.append({
                    "finding_id": f_id,
                    "entry_id": f"SEC-{len(findings)+1:02d}",
                    "classification": "poisoned",
                    "topic": field_name,
                    "raw_content": "[REDACTED SECRET]",
                    "reason": f"OWASP ASI06: Credential leak detected ({sec_name}) in {field_name}",
                    "referenced_paths": [],
                    "dead_paths": [],
                    "action_taken": "compacted",
                })
                val = pattern.sub("[REDACTED_SECRET]", val)

        for token in re.findall(r"\b[A-Za-z0-9_\-\.]{20,}\b", val):
            h = calculate_shannon_entropy(token)
            if h > 4.5 or (len(token) >= 32 and h > 3.5 and all(c in "0123456789abcdefABCDEF-_" for c in token)):
                secrets_detected += 1
                f_id = f"SEC-{len(sanitized_items)+1:02d}"
                sanitized_items.append({
                    "finding_id": f_id,
                    "threat_type": "credential_leak",
                    "action": "redacted",
                    "details": f"High-entropy string (H > {h:.2f}) detected in {field_name}",
                })
                findings.append({
                    "finding_id": f_id,
                    "entry_id": f"SEC-{len(findings)+1:02d}",
                    "classification": "poisoned",
                    "topic": field_name,
                    "raw_content": "[REDACTED HIGH_ENTROPY]",
                    "reason": f"OWASP ASI06: High-entropy string detected in {field_name}",
                    "referenced_paths": [],
                    "dead_paths": [],
                    "action_taken": "compacted",
                })
                val = val.replace(token, "[REDACTED_HIGH_ENTROPY]")

        return val

    file_dir = target_file.parent
    files_obj = ckpt.get("files_modified_and_inspected", {})
    modified_paths = files_obj.get("modified", [])
    inspected_paths = files_obj.get("inspected", [])

    valid_modified: list[str] = []
    dead_modified: list[str] = []
    for p in modified_paths:
        if is_dead_path(p, repo_root, file_dir):
            dead_modified.append(p)
            f_id = f"F-{len(findings)+1:02d}"
            findings.append({
                "finding_id": f_id,
                "entry_id": f"MOD-{len(findings)+1:02d}",
                "classification": "stale",
                "topic": "Files Modified",
                "raw_content": p,
                "reason": f"Modified file path does not exist on live disk: {p}",
                "referenced_paths": [p],
                "dead_paths": [p],
                "action_taken": "updated",
            })
            sanitized_items.append({
                "finding_id": f_id,
                "threat_type": "hallucinated_path",
                "action": "updated",
                "details": f"Modified file path not found on live disk: {p}",
            })
        else:
            valid_modified.append(p)

    valid_inspected: list[str] = []
    for p in inspected_paths:
        if is_dead_path(p, repo_root, file_dir):
            f_id = f"F-{len(findings)+1:02d}"
            findings.append({
                "finding_id": f_id,
                "entry_id": f"INSP-{len(findings)+1:02d}",
                "classification": "stale",
                "topic": "Files Inspected",
                "raw_content": p,
                "reason": f"Inspected file path does not exist on live disk: {p}",
                "referenced_paths": [p],
                "dead_paths": [p],
                "action_taken": "updated",
            })
            sanitized_items.append({
                "finding_id": f_id,
                "threat_type": "hallucinated_path",
                "action": "updated",
                "details": f"Inspected file path not found on live disk: {p}",
            })
        else:
            valid_inspected.append(p)

    goal = sanitize_field(ckpt.get("current_goal", ""), "current_goal")
    next_action = sanitize_field(ckpt.get("next_single_safe_action", ""), "next_single_safe_action")
    raw_constraints = ckpt.get("active_constraints", [])
    constraints = [sanitize_field(c, "active_constraints") for c in raw_constraints if isinstance(c, str)]
    raw_invariants = ckpt.get("preserved_invariants", [])
    invariants = [sanitize_field(inv, "preserved_invariants") for inv in raw_invariants if isinstance(inv, str)]
    raw_decisions = ckpt.get("decisions_and_tradeoffs", [])

    mem_lines: list[str] = [
        "# Persistent Agent Memory",
        "",
        f"**Last cleaned:** {now_iso} | **Budget:** <= {line_budget} lines, <= {token_budget} tokens",
        "",
        "## Active Goal",
        f"- {goal if goal else 'None'}",
        "",
        "## Active Constraints & Invariants",
    ]
    for c in constraints:
        if c:
            mem_lines.append(f"- [constraint] {c}")
    for inv in invariants:
        if inv:
            mem_lines.append(f"- [invariant] {inv}")
    if not constraints and not invariants:
        mem_lines.append("- None")

    mem_lines.append("")
    mem_lines.append("## Tracked Files")
    mod_strs = [f"`{p}`" for p in valid_modified]
    insp_strs = [f"`{p}`" for p in valid_inspected]
    mem_lines.append(f"- Modified: [{', '.join(mod_strs) if mod_strs else 'None'}]")
    mem_lines.append(f"- Inspected: [{', '.join(insp_strs) if insp_strs else 'None'}]")

    mem_lines.append("")
    mem_lines.append("## Key Decisions")
    if raw_decisions:
        for d in raw_decisions:
            if isinstance(d, dict):
                dec = sanitize_field(d.get("decision", ""), "decisions_and_tradeoffs")
                rat = sanitize_field(d.get("rationale", ""), "decisions_and_tradeoffs")
                mem_lines.append(f"- Decision: {dec} (Rationale: {rat})")
    else:
        mem_lines.append("- None")

    mem_lines.append("")
    mem_lines.append("## Next Safe Action")
    mem_lines.append(f"- {next_action if next_action else 'None'}")
    mem_lines.append("")

    updated_content = "\n".join(mem_lines)

    archived_lines: list[str] = []
    raw_ckpt_id = ckpt.get("checkpoint_id", f"CHK-{now.strftime('%Y%m%d-%H%M%S')}")
    ckpt_id = sanitize_field(str(raw_ckpt_id), "checkpoint_id")
    pc = ckpt.get("phase_control", {})
    if isinstance(pc, dict):
        p_name = sanitize_field(str(pc.get("phase_name", "N/A")), "phase_control.phase_name")
        p_curr = sanitize_field(str(pc.get("current_phase", "N/A")), "phase_control.current_phase")
        p_stat = sanitize_field(str(pc.get("status", "completed")), "phase_control.status")
        archived_lines.append(f"- **Checkpoint {ckpt_id}** ({now_iso}) | Phase: {p_name} (`{p_curr}`) | Status: `{p_stat}`")
        if goal:
            archived_lines.append(f"  - Goal: {goal}")

    failed_attempts = ckpt.get("failed_attempts_and_antipatterns", [])
    if failed_attempts:
        archived_lines.append("  - Failed Attempts & Anti-Patterns:")
        for fa in failed_attempts:
            if isinstance(fa, dict):
                att = sanitize_field(fa.get("attempt", ""), "failed_attempts")
                reas = sanitize_field(fa.get("failure_reason", ""), "failed_attempts")
                rule = sanitize_field(fa.get("preventive_rule", ""), "failed_attempts")
                rule_str = f" -> Preventive Rule: {rule}" if rule else ""
                archived_lines.append(f"    - Attempt: {att} (Failed: {reas}){rule_str}")

    lines_after = len(updated_content.splitlines())
    tokens_after = estimate_tokens(updated_content)
    token_delta = tokens_before - tokens_after
    token_reduction_pct = round((token_delta / tokens_before * 100), 1) if tokens_before > 0 else 0.0
    if token_reduction_pct < 0:
        token_reduction_pct = 0.0

    line_budget_exceeded = lines_after > line_budget
    budget_exceeded = tokens_after > token_budget

    stale_count = len(dead_modified) + (len(inspected_paths) - len(valid_inspected))
    active_count = len(valid_modified) + len(constraints) + len(invariants)
    resolved_count = len(archived_lines)
    total_entries = active_count + stale_count + poisoned_quarantined + resolved_count

    try:
        rel_target = str(target_file.relative_to(repo_root))
    except Exception:
        rel_target = str(target_file)

    audit_payload = {
        "contract_type": "memory-audit-report",
        "audit_id": f"MEM-AUDIT-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
        "target_file": rel_target,
        "audited_at": now_iso,
        "auditor": {
            "role": "prompt-engineer",
            "tool": "prune-memory.py",
            "runtime_mode": "check" if check_mode else ("dry-run" if dry_run else "in-place"),
        },
        "lifecycle_phase": "compaction",
        "token_metrics": {
            "tokens_before": tokens_before,
            "tokens_after": tokens_after,
            "token_delta": token_delta,
            "token_reduction_pct": token_reduction_pct,
            "budget_token_cap": token_budget,
            "budget_exceeded": budget_exceeded,
        },
        "line_metrics": {
            "lines_before": lines_before,
            "lines_after": lines_after,
            "line_budget_cap": line_budget,
            "line_budget_exceeded": line_budget_exceeded,
        },
        "entry_triage_summary": {
            "active_count": active_count,
            "stale_count": stale_count,
            "redundant_count": 0,
            "resolved_count": resolved_count,
            "poisoned_count": poisoned_quarantined,
            "total_entries": total_entries,
        },
        "findings": findings,
        "security_sanitization": {
            "owasp_asi06_checked": True,
            "secrets_detected": secrets_detected,
            "poisoned_entries_quarantined": poisoned_quarantined,
            "sanitized_items": sanitized_items,
        },
    }

    if archive_path:
        audit_payload["archival_target"] = str(archive_path)

    return audit_payload, updated_content, archived_lines


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    target_file = Path(args.file)
    if not args.ingest_checkpoint and not target_file.exists():
        sys.stderr.write(f"Error: Target memory file does not exist: {target_file}\n")
        return 2

    repo_root = Path(args.repo_root)
    if not repo_root.exists():
        sys.stderr.write(f"Error: Repo root directory does not exist: {repo_root}\n")
        return 2

    output_path = Path(args.output) if args.output else None
    archive_path = Path(args.archive) if args.archive else None

    if args.ingest_checkpoint:
        checkpoint_path = Path(args.ingest_checkpoint)
        if not checkpoint_path.exists():
            sys.stderr.write(f"Error: Checkpoint file does not exist: {checkpoint_path}\n")
            return 2
        try:
            payload, pruned_content, archived_lines = ingest_checkpoint_and_audit(
                checkpoint_path=checkpoint_path,
                target_file=target_file,
                repo_root=repo_root,
                check_mode=args.check,
                dry_run=args.dry_run,
                output_path=output_path,
                line_budget=args.line_budget,
                token_budget=args.token_budget,
                archive_path=archive_path,
                verbose=args.verbose,
            )
        except Exception as exc:
            sys.stderr.write(f"Fatal error during checkpoint ingestion: {exc}\n")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 2
    else:
        try:
            payload, pruned_content, archived_lines = prune_and_audit(
                file_path=target_file,
                repo_root=repo_root,
                check_mode=args.check,
                dry_run=args.dry_run,
                output_path=output_path,
                threshold_days=args.threshold,
                line_budget=args.line_budget,
                token_budget=args.token_budget,
                archive_path=archive_path,
                verbose=args.verbose,
            )
        except Exception as exc:
            sys.stderr.write(f"Fatal error during pruning: {exc}\n")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 2

    # Write archive if specified and not in check or dry-run mode
    if archive_path and archived_lines and not args.check and not args.dry_run:
        archive_content = ""
        now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if not archive_path.exists():
            archive_content = "# Memory Archive\n\nPruned and archived historical entries from persistent memory stores.\n"
        archive_content += f"\n## Archived Entries - {now_iso}\n\n"
        archive_content += "\n".join(archived_lines) + "\n"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        with open(archive_path, "a", encoding="utf-8") as f:
            f.write(archive_content)

    # Write pruned file if not check and not dry-run
    if not args.check and not args.dry_run:
        dest = output_path if output_path else target_file
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(pruned_content, encoding="utf-8")

    # Output formatting
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        preview = pruned_content if args.dry_run else None
        print(format_text_report(payload, preview))

    # Exit code determination
    if args.check:
        has_violations = (
            payload["token_metrics"]["budget_exceeded"]
            or payload["line_metrics"]["line_budget_exceeded"]
            or payload["entry_triage_summary"]["stale_count"] > 0
            or payload["entry_triage_summary"]["poisoned_count"] > 0
            or payload["entry_triage_summary"]["redundant_count"] > 0
        )
        return 1 if has_violations else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
