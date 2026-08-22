"""Shared utilities for core pack validators.

2026 additions:
- ValidationResult dataclass for structured validator output
- Python 3.12 type alias syntax (type X = ...)
- collect_workflow_names() helper shared by multiple validators
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = ROOT / "core"
SKILLS_ROOT = CORE_ROOT / "skills"


def strip_fenced_blocks(text: str) -> str:
    """Remove fenced code blocks from markdown text."""
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def section_text(body: str, heading: str, *, level_aware: bool = False) -> str:
    """Extract text between a heading and the next heading of same or higher level."""
    marker = f"{heading}\n"
    start = body.find(marker)
    if start == -1:
        return ""
    start += len(marker)

    if level_aware:
        level = len(heading.split(" ", 1)[0])
        match = re.search(rf"(?m)^#{{2,{level}}} .+", body[start:])
        if match:
            return body[start : start + match.start()]
    else:
        next_heading = body.find("\n## ", start)
        if next_heading != -1:
            return body[start:next_heading]
    return body[start:]


def slug(text: str) -> str:
    """Convert text to a URL-safe slug."""
    value = text.strip().lower().replace("&", "and").replace("/", "-")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    """Parse YAML frontmatter from markdown text."""
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text, ["missing YAML frontmatter"]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, text, ["unterminated YAML frontmatter"]

    metadata: dict[str, str] = {}
    current_key: str | None = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        # Continuation line for YAML block scalar (> or |)
        if current_key and line.startswith(("  ", "\t")):
            metadata[current_key] += " " + line.strip()
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            current_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        # Detect block scalar indicators (> or |) and start accumulation
        if value in (">", "|", ">-", "|-"):
            metadata[key] = ""
            current_key = key
        else:
            metadata[key] = value
            current_key = None

    body = "\n".join(lines[end + 1 :])
    return metadata, body, errors


def collect_skill_names() -> set[str]:
    """Collect all skill names from core and overlay SKILL.md files."""
    names: set[str] = set()
    for path in SKILLS_ROOT.glob("*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name: ([a-z0-9-]+)$", text)
        if match:
            names.add(match.group(1))
    for path in (ROOT / "overlays").glob("*/*/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name: ([a-z0-9-]+)$", text)
        if match:
            names.add(match.group(1))
    return names


def collect_skill_files() -> list[Path]:
    """Collect all SKILL.md file paths from core and overlays."""
    files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    files.extend(sorted((ROOT / "overlays").glob("*/*/*/SKILL.md")))
    return files


def bullet_count(text: str) -> int:
    """Count bullet list items in text."""
    return len(re.findall(r"(?m)^- .+", text))


def collect_workflow_names() -> set[str]:
    """Collect all workflow names (stems) from core/workflows/*.md."""
    return {
        p.stem
        for p in (CORE_ROOT / "workflows").glob("*.md")
        if p.name != "README.md"
    }


# ---------------------------------------------------------------------------
# 2026: Structured validation result (used by validate-all.py and callers)
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Structured result from a single validator run.

    exit_code semantics:
        0 = passed
        1 = failed (rule violations — actionable)
        2 = error  (script crash or missing file)
    """

    name: str
    passed: bool
    exit_code: int
    output: str = ""
    duration_ms: float = 0.0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# 2026: Python 3.12 type alias syntax
type ErrorList = list[str]
type SkillName = str
type RoleName = str
