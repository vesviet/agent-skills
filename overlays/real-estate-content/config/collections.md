# Lease Content Collections

Astro `src/data` collection trees, schemas, and corpus inventory for the Lease
in Vietnam and HVAC Portal sites. Snapshot: 2026-10-24. Canonical
corpus indexes: `real-estate/plan/CONTENT_INDEX.md` (posts), `real-estate/plan/LAW_CONTENT_INDEX_AND_AUDIT_2026.md` (204 law-related posts), and
`real-estate/plan/PROPERTY_INDEX.md` (61 luxury properties) — regenerate after every
batch, then refresh the counts here.

## Site Roots

| Site | Data path (workspace-relative) | Collections | Loader |
|------|-------------------------------|-------------|--------|
| Real Estate Portal | `real-estate/src/data` | `post` (482 MDX), `property` (61 MD) | `glob('**/*.{md,mdx}')` |
| HVAC Portal | `hvac-portal/src/data` | `post`, `product` | same glob loader |

## Post Layout Convention

- Posts live in **category folders**, not dated folders:
  `src/data/post/<category>/<slug>.mdx`
- 12 categories: `guides` (113), `neighborhood` (70), `living` (50),
  `trust-safety` (43), `property-review` (36), `legal` (36), `market-radar` (27),
  `market-data` (25), `travel` (24), `scam` (22), `neighborhood-comparison` (21),
  `comparisons` (15)
- Use `.mdx` — the `<AnswerFirst>` component and layout imports require it.

## Post Schema (Zod, `src/content/config.ts`)

Required: `title`. Optional: `publishDate`, `updateDate`, `draft`, `excerpt`,
`image`, `category`, `tags`, `author`, `metadata` (canonical/robots/OpenGraph),
`anti_slop_gate` (boolean or `{ gate_passed, slop_sections_flagged,
boilerplate_removed, substance_elements_added }`), `postLayout` enum
(`GuideLayout` | `MarketRadarLayout` | `ScamAlertLayout` | `NeighborhoodLayout`
| `responsive`). The schema uses `.passthrough()` — layout-specific keys are
allowed; copy them from sibling posts using the same layout.

Editorial-gate fields (not schema-enforced but workflow-enforced):
`unique_angle`, `serp_title`, `faq` (frontmatter array), `substance_requirements`.

## Property Schema (Lease)

`title`, `price` (number, `currency` default VND), `bedrooms`, `bathrooms`,
`area`, `location`, `propertyType`, `agentId`, `coordinates {lat,lng}`, `gallery`,
`amenities`, `status`, `floorPlan`, `videoTour`, `tags`, `metadata`.
Houzez-extended fields supported via passthrough.
Enforced via `scripts/tools/validate_property_listings.py`: title <= 60, desc <= 160,
integer VND price, management fee breakdown, EVN 6-tier rates, water tariffs, and soundproofing decibel rating.

## 2026 Gate Coverage (real-estate)

| Gate | Coverage |
|---|---|
| `<AnswerFirst>` component | 482/482 (100%) |
| `author` + `publishDate` | 482/482 (100%) |
| `faq` block | 482/482 (100%) |
| `anti_slop_gate` | 482/482 (100%) |
| `unique_angle` | 482/482 (100%) |
| Property cross-links | 482/482 posts link `/property/*` |
| Property Listings Quality Gate | 61/61 properties (0 defects) |

## Author Registry

`src/data/authors.ts` — 17 E-E-A-T persona slugs (133 aliases) with verifiable credentials
(lawyers, CPA, MEP engineer, architect, MD). Frontmatter `author:` must
reference one of these slugs.
