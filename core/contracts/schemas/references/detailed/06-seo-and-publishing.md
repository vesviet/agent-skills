# SEO & Publishing



#### `seo-content-brief.json`

**SEO Content Brief**  
Pre-draft handoff from SEO Analyst to Content Writer. Produced by the optimize-seo skill. Validates against seo-analyst.md Output Template and Review Checklist.

Required fields: `brief_id`, `created_at`, `site`, `context`, `topical_authority`, `keywords`, `geo_aeo`, `on_page_plan`, `eeat_gates`, `schema_requirements`, `internal_links`, `handoff`  
Size: 25,539 bytes  
✅ Has example

#### `seo-audit-report.json`

**SEO Audit Report**  
Pre/post-publish audit produced by SEO Analyst using optimize-seo skill. Covers traditional SEO issues, AI extractability, metadata compliance, and technical escalation items. Validates against seo-analyst.md Review Checklist.

Required fields: `audit_id`, `created_at`, `site`, `audited_url_or_path`, `audit_type`, `traditional_seo`, `ai_extractability`, `metadata_audit`, `cannibalization_check`, `handoff`  
Size: 20,547 bytes  
✅ Has example

#### `seo-metadata.json`

**SEO Metadata**  
Publisher-ready metadata produced by SEO Analyst. Used at publish time to set title, meta description, slug, and social metadata. Does not include full article content — that is in content-handoff.json. Validates against seo-analyst.md Outputs Produced section and overlay slug/frontmatter rules.

Required fields: `metadata_id`, `created_at`, `site`, `url_or_path`, `title`, `meta_description`, `slug`, `primary_keyword`, `secondary_keywords`, `schema_types`, `status`  
Size: 8,838 bytes  
✅ Has example

#### `seo-weekly-board.json`

**SEO Weekly Board**  
7-day dual-site topic board for machine handoff between Task Planner, SEO Analyst, and Content Writer. Produced by the optimize-seo skill under the seo-publishing overlay. Mirrors the markdown plan/baiviet/plan-YYYY-MM-DD.md board in structured JSON. Validates against overlays/seo-publishing/rules/topic-board-template.md and site-mix-and-cannibalization.md.

Required fields: `board_id`, `created_at`, `week_start`, `week_end`, `timezone`, `sites`, `entries`, `guardrails_check`, `handoff`  
Size: 22,945 bytes  
✅ Has example

#### `series-article.json`

**Series Article**  
Schema for a series article output, validating required frontmatter fields and body structure before publishing.

Required fields: `frontmatter`, `body`  
Size: 3,422 bytes  
✅ Has example
