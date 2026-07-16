---
name: release-notes
description: Draft, structure, and review release notes for a software change so that users, operators, and downstream consumers understand what changed, what broke compatibility, and what action they must take. Use when shipping a feature, fix, or breaking change that requires external communication.
---

# Release Notes

Use this skill when a release, deployment, or version bump requires communication to users, operators, or downstream teams.

## When To Use

- a new version, feature, or fix is shipping to production
- a breaking change, deprecation, or migration step affects consumers
- a changelog or release communication needs to be written and reviewed
- internal teams need a structured summary of what changed for handoff or support

## When to Use

- shipping a feature, fix, or breaking change
- external communication of what changed
- calling out compatibility breaks and required actions
- structuring user/operator-facing notes

## Core Rules

- write for the audience, not for the implementation team — use user-facing language, not internal jargon
- separate breaking changes clearly from new features and bug fixes
- do not mention internal process, agent names, ticket IDs, or team structure unless the audience needs them
- do not include secrets, credentials, configuration values, or PII
- distinguish **user-facing changes** from **operator or infrastructure changes**
- every breaking change must include an upgrade path or migration note
- keep notes accurate — do not imply a fix is complete if it is partial or has known caveats

## Suggested Process

### 1. Collect The Changes

Gather:

- merged pull requests or commits since the last release
- closed tickets or issues that changed user-facing behavior
- schema or API contract changes
- dependency upgrades with behavioral impact
- configuration changes that operators must act on

Discard internal refactors, test-only changes, and dependency bumps with no behavioral impact unless they affect upgradeability.

### 2. Classify By Type And Audience

Sort changes into:

| Type | When to use |
|------|-------------|
| **Breaking Change** | Removes or incompatibly changes an existing behavior, API, or contract |
| **New Feature** | Adds net-new capability users can opt into |
| **Improvement** | Enhances existing behavior without removing anything |
| **Bug Fix** | Corrects unintended behavior |
| **Deprecation** | Marks something for future removal with a timeline |
| **Security** | Addresses a vulnerability — use minimal exploit detail |
| **Upgrade / Operator Note** | Requires action from operators, admins, or platform teams |

Label each by audience when needed:
- `[User]` — visible to end users
- `[API]` — affects API consumers or integrators
- `[Operator]` — requires infrastructure or config action
- `[Internal]` — relevant to developers integrating the service

### 3. Draft Notes For Each Change

For each entry:

- **What changed** — one clear sentence from the user's perspective
- **Why it matters** — optional; include when the benefit is not obvious
- **Action required** — required for breaking changes and deprecations

Breaking changes must include:
- what breaks
- what the migration path is
- a deadline or timeline if the old behavior will be fully removed

### 4. Review Gate

Before publishing, verify:

- breaking changes are listed first and clearly labeled
- every breaking change has an upgrade path
- security fixes do not expose exploit details
- language is audience-appropriate (no internal process references)
- notes are accurate and do not over-claim completeness of a partial fix
- links to migration guides, changelogs, or docs are valid

## Output Format

```markdown
# Release Notes — <Service or Product> v<version> (<date>)

## ⚠️ Breaking Changes

- **[API]** <What changed and what breaks>. Upgrade path: <what consumers must do>.
- **[Operator]** <Config or infra change required>. See [migration guide](<link>).

## ✨ New Features

- **[User]** <What users can now do>.
- **[API]** <New endpoint or capability>.

## 🛠️ Improvements

- <What improved and why it matters to users>.

## 🐛 Defect Fixes

- <What was broken and what correct behavior looks like now>.

## 🔒 Security

- <Minimal description of the vulnerability class fixed>. Update recommended.

## ⚠️ Deprecations

- **<Feature or endpoint>** is deprecated and will be removed in <version or date>. Use <alternative> instead.

## 📋 Operator Notes

- <Config change, migration step, or infra action required>.

## 📦 Upgrade Notes

<Consolidated upgrade path when multiple changes require coordinated action.>
```

## Checklist

- [ ] changes collected from source of truth (commits, PRs, tickets)
- [ ] breaking changes identified and listed first
- [ ] every breaking change has an upgrade path
- [ ] deprecations include timeline and alternative
- [ ] security fixes omit exploit details
- [ ] language is audience-appropriate (no internal jargon or process)
- [ ] partial fixes or known caveats are noted honestly
- [ ] operator notes separated from user notes where relevant

## Related Skills

- **write-documentation**: Write or update longer-form migration guides, API references, or runbooks
- **commit-code**: Prepare the release commit and tag
- **review-service**: Confirm release readiness before communication goes out
- **write-tech-radar**: Document longer-term technology direction changes
\n### 2026: Release Automation

- **GitHub Releases automation:** Generate release notes from Conventional Commits via `gh release create --generate-notes` or the GitHub Releases API. Customize the note template in `.github/release.yml` to categorize commits by type (Features, Fixes, Breaking Changes). This avoids hand-writing notes for every release.
- **Semantic versioning decision rules:** MAJOR bump when a breaking change is introduced (even minor API contract changes). MINOR bump for backward-compatible features. PATCH bump for fixes. Provide a decision table in the checklist to prevent incorrect version bumping.
- **Deprecation calendar in release notes:** Every release note for a deprecated feature must include the exact sunset date in ISO 8601 format and a link to the migration guide. Consider referencing the RFC 8594 Sunset header specification.\n