# Máy Lạnh Treo Tường Content Collection Schema

This rule enforces schema specifications and frontmatter integrity for the Astro v5 Content Collections in `maylanhtreotuong` (`post` and `product`).

## 1. Post Collection (`src/data/post/<category>/<slug>.mdx`)

All articles must be stored in one of the 7 authorized category folders:
- `gia-ca` (Giá cả & biến động thị trường)
- `huong-dan` (Hướng dẫn chọn công suất, lắp đặt, bảo dưỡng)
- `kien-thuc` (Nguyên lý nhiệt động học, Inverter, gas lạnh)
- `kinh-nghiem` (Kinh nghiệm vận hành, xử lý sự cố)
- `mua-sam` (Tư vấn mua sắm theo nhu cầu và không gian)
- `review` (Đánh giá chi tiết model sản phẩm)
- `so-sanh` (So sánh trực tiếp model hoặc công nghệ)

### Required Frontmatter Schema

```yaml
---
publishDate: 2026-08-23T08:00:00.000Z
updateDate: 2026-08-23T08:00:00.000Z
title: "Primary H1 Title (strictly <= 60 chars, clear intent)"
image: ~/assets/images/content/your-featured-image.webp
excerpt: "Concise summary (120-160 chars) highlighting verifiable engineering specs."
category: review # must match parent category folder exactly
tags:
  - daikin
  - inverter
  - 1hp
author: "Kỹ sư Điện lạnh Nguyễn Văn Hùng" # must reference registered persona
draft: false
unique_angle: "Specific, non-generic empirical information gain statement."
substance_requirement: "Verifiable technical data (e.g., CSPF 6.22, 19 dB(A), 0.72 kWh/night)."
anti_slop_gate:
  gate_passed: true
  verified_by: "Content Manager"
metadata:
  title: "SEO SERP Title (strictly <= 60 chars)"
  description: "Meta description (120-155 chars) containing target keywords and value prop."
---
```

### Markdown / MDX Structure Rules
- **Answer-First BLUF (MANDATORY)**: Immediately follow the frontmatter imports with an Answer-First block:
  ```markdown
  > **Answer-first:** [Direct, quantitative summary <= 60 words addressing user intent directly].
  ```
- **Call-to-Action Integration**: Include the commercial CTA component at strategic decision points:
  ```astro
  import PostCallToAction from '~/components/blog/PostCallToAction.astro';

  <PostCallToAction />
  ```
- **Silo Navigation**: Minimum 3 internal links to peer cluster articles + 1 link to a commercial product landing page under `src/data/product/`.

---

## 2. Product Collection (`src/data/product/<brand-model-hp>.md`)

Specification files for individual AC units must provide complete technical and pricing attributes:

```yaml
---
publishDate: 2026-05-15T08:00:00.000Z
updateDate: 2026-08-10T08:00:00.000Z
title: "Daikin FTKB25WVMV 1 HP Inverter"
brand: "Daikin"
model: "FTKB25WVMV"
hp: 1.0
btu: 8500
price: 10490000
currency: "VND"
priceCheckedDate: 2026-08-10T08:00:00.000Z
dataSources:
  - "Daikin Vietnam Official Catalog 2026"
  - "Quatest 3 Energy Efficiency Report"
installCostEstimate: "800.000 - 1.200.000 VND"
warrantySummary: "1 năm thân máy, 5 năm máy nén"
bestFor:
  - "Phòng ngủ 10-15m2"
  - "Gia đình cần máy vận hành êm 19 dB(A)"
notFor:
  - "Phòng khách hướng tây bị nắng chiếu trực tiếp"
inverter: true
gasType: "R32"
energyRating: 5
noiseLevel: 19
offers:
  - label: "Điện Máy Xanh"
    href: "https://example.com/partner/dmx"
    price: 10490000
    partner: "DMX"
draft: false
tags:
  - daikin
  - 1hp
  - inverter
metadata:
  title: "Máy Lạnh Daikin 1HP FTKB25WVMV - Giá & Đánh Giá 2026"
  description: "Thông số, giá bán và đánh giá thực nghiệm máy lạnh Daikin 1HP FTKB25WVMV Inverter."
---
```

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
