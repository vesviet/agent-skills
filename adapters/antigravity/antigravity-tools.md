# Antigravity Tool Mapping (`agy` / Antigravity IDE)

Skills in `agent-skills` use harness-neutral action names (`read_file`, `delegate_task`, `execute_command`, `run_tests`, etc.). When operating inside **Google Antigravity**, resolve each logical action to the exact native tool below.

| Logical Skill Action | Antigravity Native Tool | Operational Notes |
|---|---|---|
| Read file / image / PDF / media | `read_file` | Bounded (`<= 800` lines / `46 KB` per call); always pass absolute paths and `StartLine`/`EndLine` for targeted reads. |
| Create file or write artifact | `write_file` | Pass `ArtifactMetadata` **only** for artifact files under `<appDataDir>/brain/<conversation-id>/`; omit for workspace files. |
| Surgical file edit | `edit_file` | Single contiguous block per call; exact whitespace match required. |
| Shell / tests / lint / build / git | `run_command` | On Windows PowerShell, chain with `; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }` (never `&&`). Background long jobs via `WaitMsBeforeAsync`; set `IsDaemon: true` only for non-terminating servers. |
| Manage background commands | `manage_task` | Controls background `run_command` / `schedule` tasks (`list`, `status`, `send_input`, `kill`). **Not** a todo checklist tool. |
| Dispatch a specialist subagent | `invoke_subagent` | Use named pack subagent (`TypeName`, e.g., `backend-developer`, `reviewer`, `qa-engineer`) or `self` / `research` / `browser`. Set `Workspace: "share"` or `"branch"` for parallel authors. |
| Resume or guide a running subagent | `send_message` | Communicate by subagent `conversationId`; never use `send_message` to address the user. |
| Inspect or terminate subagents | `manage_subagents` | `list`, `kill`, or `kill_all`. Land/merge diffs before killing branched workspaces. |
| Parallel multi-agent swarm | `swarm` | Actions: `add`, `status`, `models`, `model`, `kill`, `title`. Workers inherit coordinator model by default; recover quota errors via `swarm{action:"model"}`, never `kill`+`add`. |
| Clarify design / requirements | `ask_question` | Use for structured multiple-choice disambiguation; ask simple yes/no questions in plain prose. |
| Web research / live docs | `search_web` | Prefer `search_web` for static docs/references; delegate interactive/JS-rendered sites to the `browser` subagent (`Model: "flash"`). |
| External MCP server tools | `call_mcp_tool` | Read `<appDataDir>/mcp/<serverName>/<toolName>.json` schema before calling lazy MCP tools. |
| Deferred timer / recurring check | `schedule` | Never use shell `sleep` as a timer; use `schedule` (`DurationSeconds` or `CronExpression`) and cancel via `manage_task`. |

## Post-Compaction Survival Rules

1. Every `SKILL.md` in `agent-skills` is enforced strictly `< 200` lines and `< 20,000` bytes so harness re-attachment after `/compact` never silently truncates skill rules.
2. When resuming after context compaction, re-anchor against `core/rules/code.md`, the active role file, and the 10-slot checkpoint (`core/scripts/compact-context.py --validate`) before running any mutating tool.
3. For Claude Code / Cursor companion sessions sharing this repository, wire `core/scripts/hooks/session-start.py` to `SessionStart` (`startup|clear|compact`) so the same bootstrap invariants survive compaction across harnesses.
