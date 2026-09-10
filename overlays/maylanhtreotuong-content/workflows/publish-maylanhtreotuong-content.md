---
name: publish-maylanhtreotuong-content
description: End-to-end 6-step content production workflow enforcing HVAC engineering rigor, TCVN standards, and Silo link topology for maylanhtreotuong.
version: 1.0.0
roles:
  - content-writer
  - seo-analyst
  - content-manager
---

# Publish Maylanhtreotuong Content Workflow

This workflow governs the end-to-end authoring, review, and publishing lifecycle for air conditioning articles and product pages on `maylanhtreotuong`.

## 7-Day Content Mix Guardrails

Before launching a weekly publishing cycle, the `Task Planner` and `SEO Analyst` must verify:
- **Category Balance**: Distribution across buying guides (`huong-dan`, `mua-sam`), technical explanations (`kien-thuc`), empirical reviews (`review`), and pricing (`gia-ca`).
- **Brand Diversity**: No more than 2 consecutive articles focused on the same manufacturer brand (Daikin, Panasonic, Casper, LG, Mitsubishi).
- **Commercial Cross-Linking**: Every published article must connect to at least one corresponding product landing page in `src/data/product/`.
- **Anti-Cannibalization**: Verify target keywords against existing posts to prevent SERP cannibalization within clusters.

---

## 6-Step Production Workflow

### Step 1: Technical SEO Briefing (`seo-analyst`)
- Conduct keyword intent analysis and competitor gap analysis.
- Define primary keyword, secondary keywords, search volume, and search intent.
- Specify technical data requirements (e.g., CSPF target, noise level dB(A), room sizing formula).
- Emit structured brief using `contracts/schemas/seo-content-brief.json`.

### Step 2: Empirical Research & OEM Manual Inspection (`content-writer`)
- Extract official technical parameters from manufacturer Service Manuals and Quatest test reports.
- Gather power consumption measurement logs (Hioki meter data in kWh/night) and acoustic readings.
- Define the article's `unique_angle` and `substance_requirement`.

### Step 3: Drafting & Content Formatting (`content-writer`)
- Draft article in `.mdx` under the proper category folder in `src/data/post/<category>/`.
- Craft a concise Answer-First summary (`> **Answer-first:**`) under 60 words.
- Structure content with clear H2/H3 headings, data comparison tables, and FAQ block.
- Embed `<PostCallToAction />` at high-intent decision junctures.

### Step 4: Silo Linking & Commercial Integration (`content-writer`)
- Insert 3-4 contextual internal links to peer cluster articles.
- Insert at least 1 contextual link to the specific product model page in `src/data/product/`.
- Verify all links resolve to valid 200 OK endpoints without redirects.

### Step 5: Technical Quality & Anti-Slop Audit (`content-manager` / `reviewer`)
- Verify frontmatter schema compliance (`title`, `excerpt`, `author`, `anti_slop_gate`).
- Audit against `governance/quality_gates_antislop.md` (zero generic AI tropes or fluff).
- Verify energy calculations against TCVN 7830:2021.
- Sign off `anti_slop_gate: { gate_passed: true, verified_by: "Content Manager" }`.
- Emit structured handoff artifact using `contracts/schemas/content-handoff.json`.

### Step 6: Build Verification & Cloudflare Deployment (`cloudflare-engineer`)
- Execute Astro build verification locally:
  ```bash
  npm run build
  ```
- Verify zero TypeScript or collection schema errors.
- Commit changes and deploy via Cloudflare Pages.
- Update tracking logs in `plan/baiviet/`.

---

## Failure Modes

- **Technical claim inaccuracies**: an article quotes an outdated CSPF formula or incorrect gas type. **Mitigation:** Step 2 requires manufacturer service manual cross-referencing.
- **Missing commercial conversion link**: an article does not link to any product model page. **Mitigation:** Step 4 enforces a mandatory product landing page link.
- **Unverified anti-slop gate**: an article is published without the gate sign-off. **Mitigation:** Step 5 blocks publishing until `anti_slop_gate.gate_passed` is verified.
- **Build failure on Cloudflare**: MDX syntax error breaks Astro build. **Mitigation:** Step 6 requires a clean exit code 0 from `npm run build` prior to deployment.

## Output Contracts

When completing this workflow, emit:
- **`contracts/schemas/seo-content-brief.json`** at the completion of Step 1.
- **`contracts/schemas/content-handoff.json`** at the completion of Step 5.

---

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-10
