#!/usr/bin/env python3
"""Verification suite for P0 post-compaction survival, skill-size gate, and discipline tables."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_SKILLS_PATH = REPO_ROOT / "core" / "scripts" / "validate-skills.py"
SESSION_START_HOOK = REPO_ROOT / "core" / "scripts" / "hooks" / "session-start.py"
CLAUDE_SETTINGS = REPO_ROOT / "adapters" / "claude" / "settings.template.json"
CURSOR_HOOKS = REPO_ROOT / "adapters" / "cursor" / "hooks.template.json"
AGY_TOOLS_MD = REPO_ROOT / "adapters" / "antigravity" / "antigravity-tools.md"
AGY_ADAPTER_MD = REPO_ROOT / "adapters" / "antigravity" / "ANTIGRAVITY.md"

DISCIPLINE_SKILLS = [
    REPO_ROOT / "core" / "skills" / "foundation" / "systematic-debugging" / "SKILL.md",
    REPO_ROOT / "core" / "skills" / "foundation" / "write-tests" / "SKILL.md",
    REPO_ROOT / "core" / "skills" / "agent" / "agent-quality-gate" / "SKILL.md",
    REPO_ROOT / "core" / "skills" / "agent" / "agent-memory-compaction" / "SKILL.md",
    REPO_ROOT / "core" / "skills" / "repo-ops" / "review-code" / "SKILL.md",
]


def load_validate_skills_module():
    scripts_dir = str(VALIDATE_SKILLS_PATH.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("validate_skills_mod", str(VALIDATE_SKILLS_PATH))
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class TestP0PostCompactionAndDiscipline(unittest.TestCase):
    """Tests for <20KB skill-size cap, SessionStart hook, tool mapping, and Red Flags tables."""

    def test_01_all_skills_under_20kb_compaction_cap(self) -> None:
        skill_files = sorted(
            list((REPO_ROOT / "core" / "skills").rglob("SKILL.md"))
            + list((REPO_ROOT / "overlays").rglob("SKILL.md"))
        )
        self.assertGreaterEqual(len(skill_files), 184)
        oversized = []
        for path in skill_files:
            size = path.stat().st_size
            if size >= 20_000:
                oversized.append(f"{path.relative_to(REPO_ROOT).as_posix()} ({size} bytes)")
        self.assertEqual(oversized, [], f"Skills exceed 20,000 byte compaction cap: {oversized}")

    def test_02_validate_skills_rejects_oversized_skill_adversarial(self) -> None:
        mod = load_validate_skills_module()
        self.assertEqual(mod.MAX_SKILL_BYTES, 20_000)
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "oversized-sample"
            skill_dir.mkdir(parents=True)
            skill_file = skill_dir / "SKILL.md"
            filler = "A" * 500
            lines = [
                "---",
                "name: oversized-sample",
                "description: Sample oversized skill. Use when verifying byte cap.",
                "allowed-tools: [read_file]",
                "---",
                "",
                "# Oversized Sample",
                "",
                "## Core Rules",
            ] + [f"- {filler}" for _ in range(42)] + [
                "",
                "## Suggested Process",
                "1. Step one.",
                "",
                "## Checklist",
                "- [ ] item 1",
                "- [ ] item 2",
                "- [ ] item 3",
                "- [ ] item 4",
                "- [ ] item 5",
                "",
                "## Related Skills",
                "- **write-tests**: test helper",
            ]
            skill_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            self.assertGreaterEqual(skill_file.stat().st_size, 20_000)
            errors = mod.validate_skill(skill_file, {"oversized-sample", "write-tests"})
            self.assertTrue(
                any("20000 bytes" in err for err in errors),
                f"Expected byte-cap error, got: {errors}",
            )

    def test_03_session_start_hook_json_and_compact_event(self) -> None:
        self.assertTrue(SESSION_START_HOOK.is_file())
        proc = subprocess.run(
            [sys.executable, str(SESSION_START_HOOK), "--format", "json"],
            input=json.dumps({"source": "compact"}),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        hook_out = payload.get("hookSpecificOutput", {})
        self.assertEqual(hook_out.get("hookEventName"), "SessionStart")
        ctx = hook_out.get("additionalContext", "")
        self.assertIn("compact", ctx)
        self.assertIn("core/rules/code.md", ctx)
        self.assertIn("INDEX_TIER1.json", ctx)
        self.assertIn("Verification-Before-Completion", ctx)
        self.assertLessEqual(len(ctx.encode("utf-8")), 2_500)

    def test_04_session_start_hook_text_strict_and_disabled(self) -> None:
        env = dict(os.environ)
        env["AGENT_HOOK_PROFILE"] = "strict"
        env["AGENT_DISABLED_HOOKS"] = ""
        proc = subprocess.run(
            [sys.executable, str(SESSION_START_HOOK), "--format", "text", "--source", "clear"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("profile=strict", proc.stdout)
        self.assertIn("Strict mode:", proc.stdout)

        env["AGENT_DISABLED_HOOKS"] = "session-start"
        disabled_proc = subprocess.run(
            [sys.executable, str(SESSION_START_HOOK), "--format", "json"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        self.assertEqual(disabled_proc.returncode, 0)
        self.assertEqual(disabled_proc.stdout.strip(), "")

    def test_05_claude_and_cursor_adapters_wire_session_start_hook(self) -> None:
        claude_cfg = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8"))
        session_hooks = claude_cfg.get("hooks", {}).get("SessionStart", [])
        self.assertTrue(session_hooks, "Claude settings.template.json must define SessionStart hook")
        matchers = [entry.get("matcher", "") for entry in session_hooks]
        self.assertTrue(any("compact" in m and "startup" in m for m in matchers))
        commands = [h.get("command", "") for entry in session_hooks for h in entry.get("hooks", [])]
        self.assertTrue(any("session-start.py" in cmd for cmd in commands))

        cursor_cfg = json.loads(CURSOR_HOOKS.read_text(encoding="utf-8"))
        cursor_start = cursor_cfg.get("hooks", {}).get("sessionStart", [])
        self.assertTrue(any("session-start.py" in entry.get("command", "") for entry in cursor_start))

    def test_06_antigravity_tool_mapping_and_reference(self) -> None:
        self.assertTrue(AGY_TOOLS_MD.is_file())
        content = AGY_TOOLS_MD.read_text(encoding="utf-8")
        for tool in ("read_file", "write_file", "edit_file", "run_command", "invoke_subagent", "swarm", "manage_task"):
            self.assertIn(f"`{tool}`", content)
        self.assertIn("antigravity-tools.md", AGY_ADAPTER_MD.read_text(encoding="utf-8"))

    def test_07_core_discipline_skills_have_red_flags_tables(self) -> None:
        for path in DISCIPLINE_SKILLS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Red Flags", text, f"Missing '## Red Flags' table in {path.name}")
            self.assertIn("Rationalization Thought", text, f"Missing rationalization table header in {path.name}")
            self.assertIn("Positive Corrective Action", text, f"Missing positive corrective column in {path.name}")
            self.assertLess(len(text.splitlines()), 200, f"{path} exceeds 200 lines")
            self.assertLess(path.stat().st_size, 20_000, f"{path} exceeds 20,000 bytes")


if __name__ == "__main__":
    unittest.main()
