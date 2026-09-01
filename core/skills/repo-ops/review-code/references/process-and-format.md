# Review Code — Process, Inputs, and Output Format (Reference)

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


