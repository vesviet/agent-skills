---
name: review-code
description: Review a diff since a fixed point along two separate axes — Standards (does the code follow this repo's documented standards plus a fixed smell baseline?) and Spec (does it faithfully implement the originating issue or spec?). Runs both axes as parallel sub-agents and reports them side by side without reranking. Use for PR reviews, "review since X", local change reviews, and pre-merge audits.
---

# Review Code

Use this skill to review concrete changes, not to explain architecture in the abstract.

The review runs on **two deliberate axes**:

- **Standards**: does the code conform to this repo's documented coding standards, plus a fixed code-smell baseline?
- **Spec**: does the code faithfully implement the originating issue / spec?

A change can pass one axis and fail the other — code that follows every standard but implements the wrong thing is a Standards pass with a Spec fail. Reporting the axes separately stops one from masking the other; never merge or cross-rank their findings.

If the user asks for a full service audit or release readiness pass, hand off to `review-service`.

## When to Use

- PR reviews, local change reviews, or pre-merge audits
- "review since `<fixed point>`" requests against a commit, branch, tag, or merge-base
- checking correctness, security, contracts, data handling, and test coverage
- verifying a change actually implements what its originating issue asked for

## Core Rules

- review the actual changed behavior, not only style or formatting
- prioritize bugs, regressions, security risk, and missing validation
- **keep the axes separate**: report Standards and Spec findings side by side; do not merge or rerank across axes
- **the repo overrides the baseline**: a documented repo standard always wins over the smell baseline; suppress a smell where the repo endorses the pattern
- **smells are always judgement calls**: label each one ("possible Feature Envy"), never report it as a hard violation; documented-standard breaches can be hard violations
- skip anything tooling already enforces (linters, type checkers)
- cite exact files and code paths for every finding
- adapt framework-specific checks to the active repository
- do not invent platform, protocol, or shared-library concerns that are absent from the repo
- apply zero-trust validation for AI-generated code (1.7× higher defect rate), executing full boundary-level checks
- require independent human verification on critical paths when AI reviews AI-generated code
- conduct full dependency-graph blast radius reviews rather than diff-only reviews for AI changes
- **AI-REVIEW-TOOLS**: CodeRabbit, Qodo Merge, and similar AI-powered PR review tools provide useful first-pass annotations — use them as advisory signals, not as substitutes for human review; AI-generated review comments MUST be verified against the actual code before acting on them
- **PRE-COMMIT-HOOKS**: Use Lefthook (or Husky for Node.js projects) to enforce local pre-commit quality gates (lint, format, secret scan, type check) — failing gates must block the commit, not warn-only

## Inputs To Gather

- the fixed point the user names (commit SHA, branch, tag, `main`, `HEAD~5`)
- purpose of the change and its originating issue or spec, when one exists
- affected services, libraries, APIs, events, or migrations
- local repo standards under `docs/standards/`, `CONTRIBUTING.md`, or equivalent

If the repo does not have standards docs, the smell baseline below still applies on its own.

## Suggested Process

Review in this order.

### 1. Pin The Diff Fixed Point

Whatever the user named is the fixed point; if they did not specify one, ask before proceeding.

- capture the diff once: `git diff <fixed-point>...HEAD` — three-dot, so the comparison runs against the merge-base
- list the commits via `git log <fixed-point>..HEAD --oneline`
- fail fast here: confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty — a bad ref or empty diff must fail now, not inside parallel sub-agents

### 2. Resolve The Spec Source

Look for the originating spec, in this order:

1. issue references in the commit messages (`#123`, `Closes #45`) fetched via the repo's issue-tracker workflow
2. a spec path the user passed as an argument
3. a spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature
4. nothing found → ask the user where the spec is; if they say there isn't one, run the Spec axis anyway and report "no spec available"

### 3. Gather Standards Sources And Baseline

Collect every file documenting how code should be written. On top of repo docs, the Standards axis always carries the **Fowler smell baseline** (12 smells from _Refactoring_ ch.3) — see [references/two-axis-review.md](references/two-axis-review.md) for the full table and paste-ready sub-agent briefs. The baseline binds by two rules: the repo overrides it, and each hit is a labelled judgement call.

### 4. Run Both Axes In Parallel

Spawn the Standards and Spec reviews as **parallel sub-agents** so neither pollutes the other's context. Each sub-agent prompt must be self-contained:

- the full diff command and commit list
- Standards agent: the standards-source file list plus the smell baseline pasted in full (the sub-agent has no other access to it)
- Spec agent: the path or fetched contents of the spec
- each brief asks for findings under 400 words, quoting the violated standard or spec line per finding

If the spec is missing, skip the Spec sub-agent and note that in the final report. While agents run, apply the domain checks in step 5 yourself to the same diff.

### 5. Domain Checks (Standards depth)

- preserve layer boundaries such as handler -> biz -> data; keep business logic out of transport layers
- validate requests close to the boundary; keep REST/gRPC naming consistent; check backward compatibility of public methods, payloads, and enums; confirm error mapping suits callers
- wrap multi-step writes in transactions; avoid N+1 queries; use parameterized queries; paginate list endpoints that can grow; verify migrations are reversible or rollout-safe; prefer expand/migrate/contract over destructive schema changes
- propagate `context.Context`; avoid unmanaged goroutines; respect timeouts and cancellation; clean up connections, files, and streams; make retries and idempotency explicit on critical paths
- no hardcoded secrets; enforce authn/authz where needed; avoid leaking credentials or PII in logs; validate user-controlled input; call out trust-boundary changes clearly
- verify config added in code exists in config or manifests; check health probes and rollout assumptions when deployment files changed; verify event consumers survive the change; verify shared-library version bumps are intentional
- check meaningful coverage around changed business logic; ensure error paths and boundary cases are tested; call out fragile naming, duplication, or unclear ownership

### 6. Aggregate Without Reranking

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. End with a one-line summary: total findings per axis and the worst issue within each axis — never pick a single winner across axes, because that is exactly the reranking the separation prevents.

## Output Format

Findings come first. Keep summaries brief. When the Spec axis ran, group under the two axis headings; otherwise use the flat layout.

```markdown
## Standards

### Blocking
1. [path/to/file:123] Violates <documented standard>: description

### Important
1. [path/to/file:45] Possible <Smell Name> (judgement call): description

### Follow-Up
1. [path/to/file:78] Maintainability gap

## Spec

- missing: requirement from spec line "<quote>" not implemented
- scope creep: behaviour in diff not asked for
- suspect: implemented but likely wrong because <reason>

## Open Questions

- Assumption or repo-specific detail that needs confirmation

## Summary

Standards: N findings (worst: ...). Spec: M findings (worst: ...).

## Notes

- brief positive observations
- remaining validation gaps
```

If there are no findings, say so explicitly and mention residual risk such as unrun tests, unreviewed deployment config, or missing integration coverage.

## Checklist

- [ ] fixed point resolves and diff is non-empty (fail-fast passed)
- [ ] changed files and intent understood
- [ ] spec source resolved (or "no spec available" recorded)
- [ ] standards sources gathered and smell baseline applied as judgement calls
- [ ] both axes ran separately and are reported side by side without cross-reranking
- [ ] correctness and architecture checked
- [ ] API, event, or public contract safety checked
- [ ] data and state changes checked
- [ ] concurrency and reliability checked when relevant
- [ ] security and sensitive data handling checked
- [ ] platform and operations impact checked
- [ ] test coverage and maintainability checked
- [ ] AI-generated code trust tier verified (zero-trust boundary review for 1.7× defect rate)
- [ ] independent human reviewer requirement satisfied on critical paths
- [ ] full dependency-graph impact checked for AI changes (blast radius mapped)

## Output Contracts

When completing a structured code review or pull request audit, emit:

- **`contracts/schemas/code-review-finding.json`** — Emitted to provide machine-readable review findings across code quality domains, documenting severity levels, blast radius assessments, file locations, and merge recommendations.

Skip emission for informal exploratory walkthroughs where no formal review gate is active.

## Repo-Specific Adapters

Adapt these references to the active repository:

- standards docs: `docs/standards/...`
- infrastructure docs: `docs/infrastructure/...`
- deployment manifests: `gitops/`, `deploy/`, `k8s/`, or equivalent
- shared library: `common/` or your internal platform module

Skip any category the repo genuinely does not use. Do not invent GitOps, protobuf, or shared-library findings when those concepts are absent.

## Related Skills

- **review-service**: Expand a narrow code review into release readiness
- **security-audit**: Deepen security-specific findings
- **write-tests**: Add or improve coverage for reviewed behavior
- **troubleshoot-service**: Investigate a suspected bug before reviewing the fix
- **commit-code**: Prepare reviewed changes for delivery
