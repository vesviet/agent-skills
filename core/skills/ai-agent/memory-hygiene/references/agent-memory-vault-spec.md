# Agent Memory Vault Specification (`agent.memory.v1`)

## Overview

The Unreviewed Memory Vault provides durable, bounded, file-based memory storage for autonomous agents across multi-turn and cross-session operations. It enforces an explicit anti-poisoning architecture to defend against OWASP ASI06 (Memory & Context Poisoning) and prevent untrusted or hallucinated context from compromising execution integrity.

---

## 1. Architectural Invariants

### Invariant 1: Passive Context Only
Memory documents are strictly passive historical context (e.g. rationale for past choices, discovered API shapes, recorded bugs, completed handoffs). Memories are **NEVER executable instructions, policies, or rules**. When loaded into context, memories must be interpreted as observations, not directives.

### Invariant 2: Mandatory `trust: "unreviewed"`
Every memory document created by an agent carries the mandatory header `trust: "unreviewed"`. The agent runtime provides **no automated promotion** mechanism. An agent cannot declare its own memories to be verified truth. Only human operators or explicit code review workflows may promote verified patterns into governed rules (`.cursorrules`, `AGENTS.md`) or architecture decision records (ADRs).

### Invariant 3: Fail-Closed Isolation
To prevent memory files from leaking into version control, every memory root directory must contain a fail-closed `.gitignore`:
```text
*
!.gitignore
```
This ensures project-specific memories remain local and uncommitted unless explicitly tracked.

### Invariant 4: Zero-Secret Ingestion Preflight
Before writing to disk, memory content is scanned for high-entropy tokens (Shannon entropy $H > 4.5$) and credential patterns (API keys, private keys, authorization tokens). Memory persistence is rejected if a potential credential is discovered.

### Invariant 5: OWASP ASI06 Prompt Injection Defense
Content is scanned for system instruction overrides (e.g. `<system>`, `<|im_start|>`, `IGNORE PREVIOUS RULES`). Injections are blocked from storage, eliminating cross-session poisoning attacks.

---

## 2. Directory Hierarchy

Memory is scoped by project, team, and user boundaries:

```text
.agent/memory/
├── .gitignore                    # Fail-closed git exclusion (*\n!.gitignore\n)
├── project/                      # Project-scoped memory vault
│   ├── .gitignore
│   ├── contexts/                 # Ephemeral environment snapshots
│   ├── decisions/                # Architectural and implementation decisions
│   ├── facts/                    # Empirically verified domain facts
│   ├── handoffs/                 # Session transfer checkpoints
│   ├── lessons/                  # Learned operational takeaways and bugfixes
│   ├── notes/                    # Free-form scratchpad observations
│   └── runbooks/                 # Step-by-step procedures verified on disk
├── team/                         # Team-scoped shared knowledge vault
│   └── ...
└── user/                         # User-specific preferences and workflows
    └── ...
```

---

## 3. Document Format Specification

Memory documents are Markdown files with strict YAML frontmatter conforming to `agent.memory.v1`.

### Frontmatter Schema

```yaml
---
schema: "agent.memory.v1"
id: "mem-<scope>-<timestamp>-<hash>"
kind: "decision" | "fact" | "lesson" | "handoff" | "note" | "runbook" | "context"
title: "Brief descriptive summary of memory"
scope: "project" | "team" | "user"
trust: "unreviewed"               # Mandatory invariant: strictly unreviewed
status: "active" | "superseded" | "deprecated"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
tags:
  - "category-1"
  - "category-2"
---

# Title of Memory Document

Detailed context, findings, evidence, or rationale.
```

### Field Definitions

| Field | Type | Constraint | Description |
|---|---|---|---|
| `schema` | string | Constant: `"agent.memory.v1"` | Memory format specification version. |
| `id` | string | `^mem-(project\|team\|user)-\d{14}-[a-f0-9]{8}$` | Unique identifier generated from scope, timestamp, and content hash. |
| `kind` | string | Enum: `decision`, `fact`, `lesson`, `handoff`, `note`, `runbook`, `context` | Semantic classification of the stored entry. |
| `title` | string | Non-empty, $\le 200$ characters | Single-line human-readable summary. |
| `scope` | string | Enum: `project`, `team`, `user` | Scope boundary of memory retention. |
| `trust` | string | Constant: `"unreviewed"` | Anti-poisoning invariant flag. |
| `status` | string | Enum: `active`, `superseded`, `deprecated` | Lifecycle status of the entry. |
| `created_at`| string | ISO 8601 UTC timestamp | Time of document creation. |
| `tags` | list[str] | List of lowercase alphanumeric tags | Keywords for indexing and bounded retrieval. |

---

## 4. CLI Tooling: `core/scripts/manage-memory-vault.py`

The Python CLI manages the lifecycle of memory documents:

### Commands

1. **Initialize Vault**:
   ```bash
   python3 core/scripts/manage-memory-vault.py init --scope project
   ```
   Creates the directory tree and writes the fail-closed `.gitignore`.

2. **Save Document**:
   ```bash
   python3 core/scripts/manage-memory-vault.py save \
     --title "PostgreSQL 16 Migration Decision" \
     --kind decision \
     --tags "postgres,database" \
     --body "Chose PostgreSQL 16 over MySQL due to JSONB performance requirements."
   ```
   Runs secret scanning and ASI06 prompt injection scanning, generates `agent.memory.v1` frontmatter with `trust: "unreviewed"`, and atomically writes to `.agent/memory/<scope>/decisions/<id>.md`.

3. **Search Vault**:
   ```bash
   python3 core/scripts/manage-memory-vault.py search "postgres"
   ```
   Performs bounded lexical search across document titles, tags, and bodies.

4. **Read Document**:
   ```bash
   python3 core/scripts/manage-memory-vault.py read <document-id>
   ```
   Prints verbatim Markdown document or outputs structured JSON with `--json`.

5. **Audit Vault (`doctor`)**:
   ```bash
   python3 core/scripts/manage-memory-vault.py doctor
   ```
   Audits all documents across the vault. Verifies that `schema == "agent.memory.v1"`, flags any document violating the `trust: "unreviewed"` invariant, and checks that `.gitignore` protections are intact.
