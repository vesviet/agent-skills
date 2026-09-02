# Affiliate Link Automation & Guidelines

This rule outlines the automation standard and placement guidelines for affiliate links in `leaseinvietnam`.

## 1. Automation via Redirects
- **Link Cloaking**: Use a standard markdown link pointing to the `/go/` directory instead of raw affiliate links. 
  Example: `Book your stay on [Agoda](/go/agoda) to get the best rates.`
- **Auto-Tagging**: At build time, the system will convert `[Agoda](/go/agoda)` into `<a href="/go/agoda" target="_blank" rel="sponsored nofollow" data-affiliate="true">Agoda</a>`.

## 2. Adding New Partners
- Add the redirect to `astro.config.ts`.
  ```ts
  redirects: {
    '/go/partnername': 'https://www.partner-affiliate-url.com/?aff_id=XXXXXXX',
  }
  ```

## 3. Placement Guidelines
- **Maximum**: 2 affiliate links per article.
- **Relevance**: Only place in contextually relevant sections.
- **Prohibited**: NEVER place affiliate links in scam or trust-safety articles (to maintain trust integrity).

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/content/optimize-seo/SKILL.md` and the `seo-metadata.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/optimize-seo/SKILL.md` and the `seo-metadata.json` schema.

Last updated: 2026-09-01
