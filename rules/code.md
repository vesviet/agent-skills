---
trigger: always_on
glob: "**"
description: "Minimal global rules for commit and publish approval, user-visible wording, and code comment hygiene."
---

# Rules

- **META-RULE**: Before finalizing any response or executing a command, you MUST explicitly state in your thought process: 'I have verified this action against rules/code.md'. If any step violates a rule, you MUST automatically halt and ask the user for permission.
- Do not create a commit unless the user explicitly confirms that specific commit action.
- Do not push commits, create tags, or publish releases unless the user explicitly confirms that specific action.
- Repo-local rules override these defaults when they are explicitly present.
- Ensure all code changes pass local linters, unit tests, and build checks before creating a commit.
- Prefer repo-local standards, templates, and workflows when they exist.
- Do not invent repository conventions, paths, branching models, or release rules that are not present in the active codebase.
- Do not mention agents, AI workflow, review labels, severity labels, task trackers, or other internal process metadata in commit messages, changelog text, release notes, or other user-visible change notes.
- Do not expose secrets, credentials, tokens, private keys, or sensitive internal values in commits, comments, changelogs, release notes, or other user-visible artifacts.
- Prefer no comment over comments that merely restate the code.
- Keep code comments implementation-focused and useful.
- Do not mention agents, review labels, severity labels, or task trackers in code comments.
- Keep each code comment within 3 lines unless a longer comment is required for doc comments, file headers, or tooling directives.
