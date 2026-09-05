# Design & Content



#### `ux-flow-spec.json`

**UX Flow Specification**  
Structured multi-screen flow handoff from UI/UX Designer to Frontend, QA, and Backend.

Required fields: `contract_type`, `flow_id`, `flow_name`, `user_goal`, `screens`, `component_spec_refs`  
Size: 5,782 bytes  
✅ Has example

#### `ui-component-spec.json`

**UI Component Specification**  
Structured component spec for handoff between UI/UX Designer and Frontend Developer.

Required fields: `component_name`, `type`, `states`  
Size: 4,683 bytes  
✅ Has example

#### `content-handoff.json`

**Content Handoff**
Structured handoff from Content Writer to SEO Analyst, Reviewer, or publisher upon completing an article. Includes typed information gain gate (`information_gain.type` enum with 6 categories), GEO/AEO execution evidence (`geo_aeo_fields_applied`: answer-first, fan-out coverage, answer formats, fact density), E-E-A-T signal audit (`eeat_signals`: experience proof type, YMYL flag), and source credibility tracking aligned with research-report.json source hierarchy. Pairs with seo-metadata.json for final publication metadata.

Required fields: `contract_type`, `content_path`, `status`
Size: 12,064 bytes
✅ Has example

#### `content-audit-report.json`

**Content Audit Report**
Structured deliverable emitted by Content Manager using audit-content skill. Records portfolio-wide or URL-level content audit results, ROT classifications, AI semantic flaw scores, information gain ratings, and refresh actions.

Required fields: `contract_type`, `audit_id`, `created_at`, `site`, `audit_scope`, `audited_items`, `portfolio_summary`, `handoff`
✅ Has example

#### `documentation-handoff.json`

**Documentation Handoff**  
Structured documentation deliverable from Technical Writer.

Required fields: `contract_type`, `topic`, `audience`, `doc_paths`, `doc_type`, `status`  
Size: 2,973 bytes  
✅ Has example

#### `learning-handoff.json`

**Learning Handoff**  
Structured handoff for MOET-aligned middle-school learning plans, exercises, and evaluations.

Required fields: `contract_type`, `subject`, `grade`, `topic`, `artifact_type`, `goals`, `next_steps`  
Size: 2,792 bytes  
✅ Has example

#### `research-report.json`

**Research Report Specification**  
Structured output for iterative research synthesis with deep (10+ rounds) or scoped depth.

Required fields: `contract_type`, `objective`, `execution_metrics`, `synthesis`, `raw_data_references`, `recommended_next_roles`  
Size: 6,782 bytes  
✅ Has example

#### `data-analysis-report.json`

**Data Analysis Report**  
Structured analyst deliverable for metrics, findings, and recommendations.

Required fields: `contract_type`, `business_question`, `metrics`, `sources`, `findings`, `confidence`  
Size: 3,347 bytes  
✅ Has example

#### `schema-migration.json`

**Schema Migration Plan**  
Structured output for a database migration plan.

Required fields: `contract_type`, `migration_name`, `database`, `changes`, `is_destructive`, `requires_downtime`, `up_script`, `down_script`  
Size: 2,118 bytes  
✅ Has example
