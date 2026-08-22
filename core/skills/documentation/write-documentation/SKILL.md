---
name: write-documentation
description: Draft or update technical documentation by following the repo's existing doc structure, audience needs, and source-of-truth boundaries. Use for README updates, service docs, runbooks, integration notes, or change explanations.
---

# Write Documentation

Use this skill when a change needs clear technical documentation or when existing docs are outdated or incomplete.

**Role routing:** Long-form **articles, blogs, guides, and SEO posts** → **Content Writer** role with `write-article`. **README, runbooks, API docs, setup guides** → **Technical Writer** role. Content Writer may use this skill for structure and clarity patterns only—not as a substitute for `write-article` on publishable posts.

## When to Use

- README updates or service docs
- runbooks or integration notes
- explaining a change
- following repo doc structure + source-of-truth

## Core Rules

- write for the intended audience, not for the author; open every page with the core definition or solution in the first paragraph — do not bury the answer
- keep docs aligned with the actual source of truth; do not duplicate content that already lives in an authoritative location — link to it instead
- prefer concrete steps and exact examples over vague explanation; code samples must have language tags, valid syntax, and complete imports
- **Diátaxis quadrant isolation**: every documentation file belongs to exactly ONE quadrant — Tutorial (learning-oriented), How-to (problem-oriented), Reference (information-oriented), or Explanation (understanding-oriented); never mix architectural philosophy with step-by-step beginner guides in a single file
- **Dual-audience authoring**: structure every document for both human engineers and AI agents — consistent Markdown headings, unambiguous terminology, and semantic YAML frontmatter (`title`, `description`, `category: tutorial|howto|reference|explanation`, `last_verified_version`) enable LLM and RAG retrieval without hallucination
- **Reference docs must be auto-generated**: API reference documentation is generated directly from OpenAPI / AsyncAPI / protobuf specs using Redocly, Scalar, or Mintlify — hand-typed endpoint definitions are rejected as they drift from the source of truth
- **Docs-as-code CI gate**: documentation PRs must pass `markdownlint`, Vale prose style, broken-link checker, and frontmatter schema validation before merge; Cloudflare Pages or Netlify deploy previews are mandatory for reviewer sign-off
- avoid internal workflow wording in user-visible docs unless the repo explicitly expects it

## Suggested Process

### 1. Identify The Documentation Need

Clarify:

- who will read it
- what problem it should solve
- whether it is setup, architecture, operations, usage, or release-oriented documentation

### 2. Inspect Existing Documentation Patterns

Look for:

- local doc location and naming conventions
- section structure
- voice and depth
- whether docs are colocated with code or live elsewhere

### 3. Gather The Minimum Correct Facts

Collect:

- commands or workflows that actually work
- key architecture or integration points
- configuration requirements
- known limitations or risks worth noting

### 4. Draft For Fast Usefulness

Prefer:

- short purpose statement
- prerequisites
- exact steps or examples
- troubleshooting notes when relevant
- links to deeper references instead of repeating them

### 5. Verify The Documentation

Check:

- examples match the code or repo structure
- commands are plausible for the target environment
- ownership and source-of-truth references are clear
- stale or conflicting guidance is removed

### 2026: Modern Documentation Standards

To align with modern AI-assisted engineering and automated API publishing:

- **AI-Readable Formats**: Maintain `/llms.txt` at the repository root and `/llms-full.txt` in markdown format to serve as clean, high-context inputs for LLMs and AI coding assistants.
- **Diataxis Framework**: Categorize documentation into four distinct forms:
  - **Tutorials**: Learning-oriented guides to help newcomers get started.
  - **How-to Guides**: Goal-oriented recipes showing how to solve specific problems.
  - **Reference**: Information-oriented technical descriptions (APIs, schemas, commands).
  - **Explanation**: Understanding-oriented concept overviews and architectural rationale.
- **OpenAPI Reference Docs**: Auto-generate API reference documentation using Redocly, Scalar, or Mintlify, ensuring the OpenAPI specification remains the single source of truth.
- **Docs-as-Code Pipeline**: Implement continuous integration checks for markdown links and formatting, with automated pull request previews deployed to Cloudflare Pages or Netlify for team reviews.

## Checklist

- [ ] audience and doc purpose identified
- [ ] local doc pattern reviewed
- [ ] facts gathered from current source of truth
- [ ] examples and steps written clearly
- [ ] stale or conflicting guidance removed
- [ ] `/llms.txt` and `/llms-full.txt` standards updated for AI readability
- [ ] Diataxis structure followed (Tutorials, How-to, Reference, Explanation)
- [ ] OpenAPI spec verified and auto-generation configured (Redocly, Scalar, Mintlify)
- [ ] Docs-as-code pipeline checked (CI linting and Cloudflare Pages/Netlify previews working)

## Related Skills

- **write-article**: Narrative and blog drafting under Content Writer
- **navigate-service**: Gather context before documenting a service
- **review-service**: Capture readiness or release notes after review
- **troubleshoot-service**: Turn learned recovery steps into runbook updates
- **write-tech-radar**: Draft higher-level technology assessments
- **commit-code**: Prepare doc updates for delivery

## Output Contracts

- `contracts/schemas/documentation-handoff.json`

