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
- every breaking change must include an upgrade path or migration note; breaking changes require a MAJOR SemVer bump — even minor API contract changes
- keep notes accurate — do not imply a fix is complete if it is partial or has known caveats
- commit history must follow Conventional Commits 1.0 (`feat:`, `fix:`, `feat!:`, `BREAKING CHANGE:`) to enable automated changelog generation via `semantic-release`, `changesets`, or `changelogen`
- automated changelogs are drafts only — require human editorial review to remove noisy internal commits before publishing
- deprecations must include exact sunset date in ISO 8601 format and a link to the migration guide (reference RFC 8594 Sunset header)
- dual-audience release communication: user-facing product notes (UX outcomes) must be separated from operator changelogs (env vars, migrations, infra actions)

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
- [ ] commit history follows Conventional Commits 1.0 (lint with Commitlint)
- [ ] SemVer bump is accurate: MAJOR for breaking changes, MINOR for features, PATCH for fixes
- [ ] breaking changes identified and listed first
- [ ] every breaking change has an upgrade path
- [ ] deprecations include ISO 8601 sunset date, alternative, and migration guide link
- [ ] security fixes omit exploit details
- [ ] language is audience-appropriate (no internal jargon or process)
- [ ] partial fixes or known caveats are noted honestly
- [ ] user-facing notes separated from operator/infrastructure notes
- [ ] automated changelog draft reviewed by human before publishing

## Related Skills

- **write-documentation**: Write or update longer-form migration guides, API references, or runbooks
- **commit-code**: Prepare the release commit and tag
- **review-service**: Confirm release readiness before communication goes out
- **write-tech-radar**: Document longer-term technology direction changes



