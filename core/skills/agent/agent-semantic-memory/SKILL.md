---
name: agent-semantic-memory
description: Read from and write to persistent memory stores so agents retain codebase patterns, past fixes, and architectural facts across conversations. Use when starting work in a known repo, after fixing a non-obvious bug, after discovering a codebase convention, or when the same mistake has occurred more than once.
---

# Agent Semantic Memory

Use this skill when the agent needs to persist or retrieve knowledge that outlives a single conversation.

## When to Use

- starting work in a known repo
- after fixing a non-obvious bug
- after discovering a codebase convention
- the same mistake has occurred more than once

## Core Rules

- write to memory only when the knowledge is reusable across future tasks
- always include repo context (repo name, language, framework) in memory entries
- verify retrieved memories are still current before acting on them
- prefer specific, actionable entries over vague summaries
- never store secrets, credentials, or sensitive data in memory
- tag entries by type so retrieval can be filtered

## Memory Tiers

### Working Memory (Ephemeral)

The current conversation context. Managed by `agent-context-management` and `agent-memory-compaction`. Dies when the conversation ends.

### Episodic Memory (Experiential)

Past actions and their outcomes. Answers questions like:

- "How did I fix the Postgres JSON operator error last time?"
- "What happened when we ran the migration on the maydiengiaisaigon repo?"
- "Which approach worked better for the 3D texture optimization?"

Storage format: timestamped entries with tags.

### Semantic Memory (Structural)

Long-term facts about codebases, architectures, and team conventions. Answers questions like:

- "What ORM does the maydiengiaisaigon repo use?"
- "What is the deployment target for the vesviet site?"
- "Which columns in the pages table are JSON (translatable)?"

Storage format: key-value facts with repo and domain tags.

## Suggested Process

### 1. Read Before Starting

Before beginning work in a known repo:

- query semantic memory for repo architecture facts
- query episodic memory for recent fixes and known gotchas
- inject relevant memories into the working context

### 2. Write After Learning

After completing work that produced reusable knowledge:

- identify what was learned (a pattern, a fix, a convention)
- classify it as episodic (action + outcome) or semantic (fact)
- write a concise, tagged entry

### 3. Validate Before Trusting

Retrieved memories may be stale:

- check timestamps — older entries need verification against current code
- cross-reference with the actual codebase before acting
- flag contradictions between memory and current state

### 4. Prune Periodically

- mark entries as deprecated when the underlying code changes
- merge duplicate entries covering the same knowledge
- remove entries that have never been retrieved

## Entry Format

### Episodic Entry

```yaml
type: episodic
repo: maydiengiaisaigon
date: 2026-05-09
tags: [postgres, json, i18n, spatie-translatable]
summary: "Postgres JSON columns cannot use = operator directly. Fixed slug queries by using arrow syntax: where('slug->' . app()->getLocale(), $value)"
outcome: success
```

### Semantic Entry

```yaml
type: semantic
repo: maydiengiaisaigon
tags: [architecture, stack, i18n]
facts:
  - "Uses Laravel + Filament + Spatie Translatable"
  - "Database: PostgreSQL with JSON columns for translatable fields"
  - "Translatable columns: name, title, slug, description, content, meta_title, meta_description"
  - "All slug queries must use JSON arrow syntax with locale"
last_verified: 2026-05-09
```

## Checklist

- [ ] relevant memories retrieved before starting work
- [ ] retrieved memories verified against current codebase
- [ ] stale memories flagged or updated
- [ ] new reusable knowledge identified after task completion
- [ ] entries classified as episodic or semantic
- [ ] entries tagged with repo, language, and domain
- [ ] no secrets or sensitive data stored
- [ ] entry is specific and actionable (not vague summary)

## Related Skills

- **agent-context-management**: Manage working memory and decide when to pull from long-term stores
- **agent-memory-compaction**: Identify knowledge worth promoting from working to long-term memory
- **agent-tool-orchestration**: Use memory retrieval tools (vector search, graph query) as part of task setup
- **agent-prompt-lifecycle**: Version prompt changes that were informed by memory-driven insights
