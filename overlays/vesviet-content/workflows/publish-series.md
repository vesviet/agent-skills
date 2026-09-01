# Publish Series

End-to-end workflow for producing and publishing a multi-part technical series across the Vesviet and Learn Hugo sites.

## When to Use

Use this workflow when creating a new series or adding parts to an existing series that must be published on both `vesviet` (English) and `learn` (Vietnamese) sites.

## Roles

| Step | Owner |
|------|-------|
| Plan series structure | `task-planner` |
| Draft content (Vietnamese) | `content-writer` |
| Translation Orchestration | `agent-coordinator` (teamwork_preview) |
| Translate to English | `content-writer` |
| Code linting review | `reviewer` |
| AI Governance & Conformance | `reviewer` |
| Commit and push | `content-writer` or `backend-developer` |

## Steps

### Step 1 — Plan Series Structure

1. Define the series topic, target audience, and number of parts.
2. Create a Table of Contents with part titles and one-line descriptions.
3. Identify prerequisite links and cross-references to existing series.
4. Save the plan under `plan/` with a date-based filename.

### Step 2 — Initialize Series Infrastructure

1. Create the series directory under `learn/content/series/<series-slug>/`.
2. Write `_index.md` with `draft: false`, correct frontmatter (see `content-brand.md`), and TOC linking all parts.
3. Verify URL structure matches Hugo config permalinks.

### Step 3 — Draft Parts (Vietnamese — Learn site)

For each part:
1. Clone frontmatter conventions from sibling series (delimiter, keys, ordering).
2. Include: Prerequisite block, numbered sections, code snippets with docstrings, Production Failure story, CTA/Next Step link.
3. Set `draft: true` until review passes.

### Step 4 — Review and Fix (AI Governance)

Role: `reviewer`
1. **AI Governance Gate**: Ensure all content meets Information Gain standards (firsthand experience, real-world failure stories). Reject any raw AI hallucinations or generic filler.
2. Run code linting checks (Python: `py_compile`/`flake8`, Go: `gofmt`/unused imports).
3. Review frontmatter conformance against `content-brand.md` rules.
4. Fix all blocking issues before proceeding.

### Step 5 — Translate to English (Vesviet site)

Role: `agent-coordinator` or `teamwork_preview`
1. Create the same directory structure under `vesviet/content/series/<series-slug>/`.
2. Invoke specialized subagents (`content-writer`) in parallel to translate all parts, maintaining identical code snippets (only translate comments and strings).
3. Update cross-site links to use absolute URLs where needed.

### Step 6 — Final Translation Review

Role: `reviewer`
1. Run `reviewer` role on the English translation for consistency with existing Vesviet series.
2. Verify no unused imports, no placeholder content, no broken internal links, and strict adherence to English terminology.

### Step 7 — Commit and Push

1. Commit the Learn repo: `git add && git commit -m "feat(content): add <series-name> series" && git push`
2. Commit the Vesviet repo: same pattern.
3. Verify both repos show clean `git status`.

### Step 8 — Go Live

1. Toggle `draft: false` on all parts when ready to publish.
2. Commit the draft flag changes separately: `fix(content): publish <series-name> series`.
3. Verify pages render correctly on both live sites.

## Checklist

- [ ] Series plan reviewed and approved
- [ ] `_index.md` created with TOC and `draft: false`
- [ ] All parts drafted with required structure (prerequisite, failure story, CTA)
- [ ] Code snippets pass linting (no unused imports, valid syntax)
- [ ] AI Governance passed (no hallucinations, Information Gain verified)
- [ ] English translation parallelized and completed for Vesviet site
- [ ] Cross-site links use absolute URLs
- [ ] Reviewer approved both Vietnamese and English versions
- [ ] Both repos committed and pushed
- [ ] Draft flags toggled for go-live

### Failure Modes

- **Plan saved without Table of Contents**: a series plan is filed without a numbered part list. **Mitigation:** Step 1 requires a TOC with part titles and one-line descriptions; reject the plan when the TOC is missing.
- **Frontmatter drift across series parts**: a part uses a different frontmatter shape than the sibling parts. **Mitigation:** Step 3 requires cloning the frontmatter from the nearest sibling; reject the part when the shape drifts.
- **AI Governance gate bypassed**: a draft ships without the firsthand experience, real-world failure stories, or Information Gain. **Mitigation:** Step 4 enforces the AI Governance Gate; reject the draft when the gate fails.
- **Code snippet fails linting**: a Python or Go snippet in the draft has unused imports or syntax errors. **Mitigation:** Step 4 requires `py_compile` / `flake8` / `gofmt` to pass; reject the draft when the lint fails.
- **Translation parallelization loses semantic consistency**: parallel subagent translations drift in terminology or formatting. **Mitigation:** Step 6 enforces a reviewer pass for terminology consistency; reject the English translation when the drift is unresolved.
- **Draft flag toggled before review**: a part is set to `draft: false` before the AI Governance gate and the reviewer pass complete. **Mitigation:** Step 8 requires the draft flag to be toggled only after both gates pass; reject the change when the order is reversed.
- **Cross-site link drift**: a Vietnamese URL on Learn does not have the matching English URL on Vesviet. **Mitigation:** Step 5 requires absolute URLs for cross-site links; reject the build when the links are relative.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/content-handoff.json`** (or markdown frontmatter block) from each draft, capturing the part slug, the language, the frontmatter gate verdict, the AI Governance verdict, and the reviewer verdict.
- **`contracts/schemas/coordination-plan.json`** from Step 5, capturing the parallel subagent dispatch and the translation order.
- **`contracts/schemas/release-notes.json`** (or frontmatter block) from Step 7-8, capturing the published series, the languages, and the go-live commit hashes.