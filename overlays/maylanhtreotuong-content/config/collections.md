# Máy Lạnh Treo Tường Content Collections

Astro v5 `src/data` collection trees, schemas, and corpus inventory for `maylanhtreotuong`. Snapshot: 2026-09-10.

## Site Roots & Content Loaders

| Collection | Data Path (workspace-relative) | Total Items | Loader Type |
| :--- | :--- | :--- | :--- |
| `post` | `maylanhtreotuong/src/data/post` | 300 MDX articles | `glob({ pattern: '**/*.{md,mdx}', base: './src/data/post' })` |
| `product` | `maylanhtreotuong/src/data/product` | 72 MD specs | `glob({ pattern: '**/*.{md,mdx}', base: './src/data/product' })` |

## Post Category Taxonomy (300 Articles)

All posts are organized strictly into 7 category subdirectories:
- `gia-ca/` (25 articles): Price lists, market movements, price-per-BTU comparisons.
- `huong-dan/` (63 articles): Sizing calculations ($V = S \times H$), installation guidelines, maintenance steps.
- `kien-thuc/` (71 articles): Thermodynamic principles, inverter algorithms, refrigerant properties (R32 vs R410A).
- `kinh-nghiem/` (30 articles): Practical troubleshooting, compressor error code diagnosis, usage tips.
- `mua-sam/` (33 articles): Space-specific recommendations (bedroom, living room, rental apartment).
- `review/` (33 articles): Individual model teardowns, component inspections, real-world noise/power testing.
- `so-sanh/` (45 articles): Side-by-side brand and model comparisons (e.g., Daikin FTKY vs Panasonic XU).

## Product Specifications (72 Models)

Comprehensive database of popular wall-mounted split AC units across Vietnam:
- Brands: Daikin, Panasonic, Mitsubishi Heavy, Mitsubishi Electric, LG, Casper, Toshiba, Gree, Aqua, Sharp, Funiki, Samsung, Beko, Midea, TCL, Nagakawa.
- Capacities: 1.0 HP (9,000 BTU), 1.5 HP (12,000 BTU), 2.0 HP (18,000 BTU), 2.5 HP (24,000 BTU).
- Attributes: `brand`, `model`, `hp`, `btu`, `price`, `currency`, `priceCheckedDate`, `dataSources`, `installCostEstimate`, `warrantySummary`, `bestFor`, `notFor`, `inverter`, `gasType`, `energyRating`, `noiseLevel`, `offers`.

## 2026 Gate Coverage

| Quality Gate | Current Coverage | Status |
| :--- | :--- | :--- |
| `<AnswerFirst>` BLUF block | 300 / 300 posts (100%) | Verified |
| Author & Publish Date | 300 / 300 posts (100%) | Verified |
| `unique_angle` Frontmatter | 300 / 300 posts (100%) | Verified |
| `substance_requirement` | 300 / 300 posts (100%) | Verified |
| `anti_slop_gate` Verification | 300 / 300 posts (100%) | Verified |
| Product Cross-Links | 300 / 300 posts (100%) | Verified |

## Author Registry

Authors are registered HVAC professionals and engineers:
- `Kỹ sư Điện lạnh Nguyễn Văn Hùng`: Chuyên gia kiểm định hiệu suất năng lượng và chu trình lạnh.
- `Kỹ thuật viên Trịnh Quốc Bảo`: Chuyên gia cơ điện lạnh và giải pháp lắp đặt thực địa.
- `Ban Biên Tập Maylanhtreotuong.com`: Tổ hợp biên soạn thị trường và giá cả thiết bị.

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
