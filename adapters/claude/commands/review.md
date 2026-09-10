---
description: "Review staged code changes against core/rules/code.md, unit test coverage, and security boundaries."
---

# Code Review Command

Use this command to audit pending changes prior to asking for commit approval:

1. Assume the role of `reviewer` (`core/roles/reviewer.md`).
2. Inspect `git status` and `git diff` for staged and unstaged changes.
3. Check against `core/rules/code.md`:
   - Verify NO `.env`, `.dev.vars`, or secret tokens are present.
   - Verify all comments are implementation-focused and <= 3 lines.
   - Verify NO AI process metadata or severity labels (`P0`/`P1`/`P2`) are exposed.
4. Run project-specific linters and test suites.
5. If issues are identified, emit `contracts/schemas/code-review-finding.json`.
6. Once clean, request explicit user confirmation before creating any commit.
