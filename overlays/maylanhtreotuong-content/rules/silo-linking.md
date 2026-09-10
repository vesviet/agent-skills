# Silo Link Topology & Internal Linking Standards

This rule governs the internal linking architecture of `maylanhtreotuong`, ensuring structured topical authority, crawl depth optimization, and seamless conversion funneling from technical articles to commercial product pages.

## 1. Silo Architecture Structure

```
[Category Hub / Root Page]
       ▲
       ├──► [Cluster Guides / Educational Articles] (7 Categories)
       │         ▲                ▲
       │         ▼                ▼
       │    [Model Reviews] ◄──► [Comparisons]
       │         │
       │         ▼ (Commercial Contextual CTA)
       └──► [Product Landing Pages] (72 SKUs under /san-pham/* or root model slug)
```

## 2. Linking Quotas Per Article

Every post in `src/data/post/` must maintain:
- **Minimum Internal Links**: At least **4-6 contextual internal links** total.
- **Cluster Peer Links**: At least **3 links** pointing to articles within the same or closely related category (e.g., `so-sanh` linking to `review` and `kien-thuc`).
- **Product Landing Page Link**: At least **1 contextual link** pointing to the exact product model page (e.g., `[Daikin FTKB25WVMV 1HP](/daikin-ftkb25wvmv-1hp)`).
- **External Authority Citation**: At least **1 link** to an official standard, manufacturer catalog, or government authority (e.g., TCVN, ASHRAE, MOIT Energy Label, Daikin Technical Portal).

## 3. Anchor Text Best Practices

- **Descriptive & Intent-Focused**: Use explicit model names or engineering terms (e.g., "bảng thông số Daikin FTKB35WVMV 1.5HP" or "nguyên lý làm lạnh của màng lọc Streamer").
- **Avoid Generic Anchors**: Strictly forbid anchors such as "tại đây", "xem thêm", "ở link này".
- **Anchor Variance**: Rotate anchor text across different articles targeting the same destination page to avoid over-optimization penalties.

## 4. Commercial CTA Integration

For buying guides, price breakdowns, and teardown reviews, insert the interactive commercial call-to-action:
```astro
import PostCallToAction from '~/components/blog/PostCallToAction.astro';

<PostCallToAction />
```
Place this component before the concluding FAQ section or immediately after the pricing & recommendation table.

---

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
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

Last updated: 2026-09-10
