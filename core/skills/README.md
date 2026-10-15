# Skills Inventory

This directory contains the **portable core** skill inventory for the global engineering pack.

**Counts:** 153 portable core skills under `core/skills/` + 15 overlay skills under `overlays/*/skills/` = **168 total** (run `validate-skills.py` for the live total, and `validate-indexes.py` to confirm this line matches disk).

## Taxonomy

### Agent (24)

Agent operating discipline, orchestration, and agentic web standards:

- `agent-a2a-protocol`
- `agent-context-management`
- `agent-delegation`
- `agent-graph-orchestration`
- `agent-handoff`
- `agent-memory-compaction`
- `agent-model-routing`
- `agent-observability`
- `agent-panel-meeting`
- `agent-prompt-lifecycle`
- `agent-semantic-memory`
- `agent-tool-orchestration`
- `agent-quality-gate`
- `architect-mcp-server`
- `decompose-agentic-system`
- `manage-agent-identity`

#### Agent Infrastructure & Agentic Web Standards (8)

Configuration and compliance skills for agentic-ready web presence (MCP, RFC 9727, x402, identity provider (WorkOS, Auth0, Okta)):

- `configure-agent-commerce`
- `configure-agent-headers`
- `configure-agent-skills`
- `configure-mcp`
- `configure-oauth-metadata`
- `debug-identity-provider`
- `manage-api-catalog`
- `manage-auth-md`

### AI (1)

High-throughput LLM inference serving, GPU resource allocation, and distributed acceleration:

- `deploy-vllm-inference`

### Foundation (16)

Cross-cutting portable skills:

- `accessibility-review`
- `ai-risk-assessment`
- `combinatorial-testing`
- `conduct-research`
- `create-migration`
- `design-review`
- `design-ux-flow`
- `hostile-component-stress-testing`
- `incident-report`
- `performance-profiling`
- `plan-technical-delivery`
- `playwright-evidence-qa`
- `release-notes`
- `systematic-debugging`
- `write-product-brief`
- `write-tests`

### Meetings And Analysis (3)

- `meeting-review`
- `analyze-business-requirements`
- `analyze-data`

### Repo Ops (5)

- `navigate-service`
- `troubleshoot-service`
- `review-code`
- `review-service`
- `commit-code`

### Content (6)

- `audit-content`
- `design-content-strategy`
- `optimize-seo`
- `repurpose-content`
- `write-article`
- `write-copy`

### SEO (2)

Technical SEO audits, crawl budget diagnostics, and connected Schema.org graph engineering:

- `audit-technical-seo`
- `implement-schema-markup`

### MMO (7)

MMO/growth-ops skills with compliance notices; each maps to `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role:

- `generate-mmo-content`
- `analyze-campaign-roi`
- `deploy-mmo-infrastructure`
- `deploy-proxyware-fleet`
- `create-automation-script`
- `manage-mmo-assets`
- `setup-tracking-system`

### Backend (8)

- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `build-mcp-server`
- `implement-auth`
- `implement-structured-outputs`
- `optimize-postgres`
- `scaffold-new-service`

### Frontend (13)

- `add-page-route`
- `add-ui-component`
- `anti-ui-slop-finish-gate`
- `component-composition`
- `design-system-engineering`
- `frontend-micro-polish`
- `frontend-testing`
- `implement-view-transitions`
- `implement-webmcp`
- `integrate-api-client`
- `interactive-component-workbench`
- `setup-design-system`
- `setup-visual-regression`

### Game Development (20)

Real-time gameplay engineering, ECS architecture, game feel tuning, physics & camera systems, game AI, procedural generation, shaders, technical art, dynamic audio, performance profiling, and multi-platform publishing across 5 pillars:

- `integrate-game-engine` — Cross-engine lifecycle integration, deterministic asset imports, export presets, and headless CI test runners
- `develop-gameplay-systems` — Deterministic fixed-timestep gameplay loops, kinematic character controllers, hierarchical state machines, and combat mechanics
- `architect-ecs-systems` — Data-oriented Entity Component System (ECS) architecture, cache-friendly SoA memory layouts, archetypes, and parallel job systems
- `manage-scene-lifecycle` — Asynchronous scene streaming, additive level loading, deterministic object pooling, and leak-free memory/VRAM lifecycle management
- `implement-save-persistence` — Versioned save/load serialization, schema migration pipelines, cryptographic integrity checks, and cloud-sync conflict resolution
- `tune-game-feel` — Tactile game feel ("juice"), coyote time, input buffering, hit-stop micro-freezes, trauma-based screen shake, and accessibility toggles
- `configure-physics-collision` — Physics engine configuration, collision layer/mask matrices, Continuous Collision Detection (CCD), and non-allocating spatial queries
- `abstract-input-actions` — Cross-device input action abstraction, runtime control remapping, input chord/buffer queues, and controller haptics
- `direct-camera-systems` — Virtual camera orchestration, Cinemachine/PhantomCamera blending, dead-zone framing, spring-damper smoothing, and occlusion avoidance
- `author-game-ai` — Game AI architecture across Behavior Trees, Utility AI, GOAP, NavMesh pathfinding, steering behaviors, and time-sliced perception
- `design-procedural-generation` — Seeded deterministic procedural generation using Wave Function Collapse (WFC), BSP dungeons, cellular automata, and noise fields
- `build-game-ui-ux` — Resolution-independent HUDs, diegetic/spatial UI, focus-driven gamepad navigation, safe-area scaling, and rich-text localization
- `integrate-dialogue-narrative` — Branching narrative and dialogue trees (Ink, Yarn Spinner, Dialogic), quest state trackers, and localized voiceover lip-sync triggers
- `program-game-shaders` — Real-time HLSL/GLSL/Godot shader programming, PBR material pipelines, compute shaders, and full-screen post-processing passes
- `inspect-blender-rigs-motion` — DCC-to-engine skeletal rig validation, bone weight normalization, root motion extraction, retargeting, and glTF/FBX export hygiene
- `render-webgl-threejs` — WebGL2/WebGPU and Three.js browser rendering, instanced draw calls, KTX2/Draco compression, and GPU resource disposal
- `generate-game-assets-pipeline` — Automated 2D/3D asset conditioning, LOD chain generation, texture atlas packing, and provenance-gated AI asset pipelines
- `mix-dynamic-game-audio` — Interactive audio bus routing (FMOD, Wwise, native mixers), adaptive music stems, 3D spatial attenuation, voice stealing, and sidechain ducking
- `profile-game-performance` — CPU/GPU frame-time profiling, draw-call batching, memory allocation tracking, thermal throttling triage, and `performance-audit.json` emission
- `automate-game-publishing` — Reproducible multi-platform build automation, Steamworks Pipe/SDK integration, console/mobile store compliance, and crash symbol upload

> R3F/Three.js cluster (`debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets`) migrated to `overlays/r3f-stack/skills/` in v4.0.0 per the stack-overlay naming rules.

> Note: `create-automation-script` is classified under MMO (`core/skills/mmo/`) — its stealth/CDP automation scripts serve growth-ops workflows, even though the underlying techniques are platform-level. See Domain Cluster Notes below.

### Mobile (2)

React Native, Expo, mobile performance, and store delivery:

- `deploy-mobile-app`
- `develop-mobile-app`

### Platform (18)

Delivery, runtime, Cloudflare-specific, cloud, and system infrastructure skills:

- `aws-infrastructure`
- `deploy-aws-eks-workloads`
- `setup-deployment`
- `setup-gpu-finops`
- `setup-llm-gateway`
- `orchestrate-chaos-experiment`
- `supply-chain-security`
- `system-design`
- `wrangler`
- `debug-workers-edge`
- `debug-runtime-platform`
- `add-telemetry-instrumentation`
- `cloudflare-email-service`
- `durable-objects`
- `sandbox-sdk`
- `turnstile-spin`
- `web-perf`
- `workers-best-practices`

### Business (3)

Requirements elicitation, use case engineering, and traceability analysis:

- `elicit-requirements`
- `trace-requirements-impact`
- `write-use-cases`

### Product (4)

Product strategy, quantitative roadmap prioritization, SaaS unit economics, and user story mapping:

- `build-story-map`
- `define-product-strategy`
- `model-saas-metrics`
- `prioritize-roadmap`

### Commerce (4)

E-commerce catalog, checkout, payment, and fulfillment:

- `integrate-payment-gateway`
- `handle-checkout-flow`
- `manage-product-catalog`
- `manage-order-fulfillment`

### Security And Data (8)

- `manage-secrets`
- `database-maintenance`
- `manage-vietnam-accounting`
- `security-audit`
- `build-data-pipeline`
- `optimize-olap-database`
- `query-analytical-engine`
- `skill-preflight-ast-check`

### Documentation (3)

- `configure-llms-txt`
- `write-documentation`
- `write-tech-radar`

### Education (3)

Teaching and curriculum:

- `design-learning-plan`
- `create-exercises`
- `grade-and-review`

### Legal Compliance (3)

Vietnam legal ecosystem governance, contract review, AI Law 134/2025 compliance, and legal opinion drafting:

- `manage-vietnam-legal`
- `audit-ai-compliance`
- `draft-legal-opinion`

Overlay-specific skills (site stacks, ICM, content data, R3F) live under `overlays/*/skills/` and are validated together with core.

## Skill Boundaries (quick reference)

| Topic | Primary skill | Escalate to |
| ----- | ------------- | ----------- |
| Deep discovery | `conduct-research` | Researcher role |
| Ad-hoc analysis / dashboards | `analyze-data` | Data Analyst role |
| Pipelines / ETL / warehouse | `build-data-pipeline` | Data Engineer role; analysis-only → `analyze-data` |
| UX flows and specs | `design-ux-flow` | UI/UX Designer |
| Visual / IA critique (no code) | `design-review` | UI/UX or Reviewer |
| a11y conformance | `accessibility-review` | QA + Frontend |
| Generic CI/CD deploy | `setup-deployment` | DevOps Engineer |
| System topology & capacity | `system-design` | System Engineer |
| Cloudflare Workers/Pages | `wrangler` | Cloudflare Engineer |
| MCP server configuration | `configure-mcp` | Cloudflare Engineer |
| Agentic commerce flows | `configure-agent-commerce` | Backend Developer |
| Vietnam accounting controls, reconciliations, or close evidence | `manage-vietnam-accounting` | Vietnam Accounting Specialist; tax position/legal interpretation -> qualified human reviewer |
| Vietnam legal compliance, contract vetting, or Decree 13 DPIA | `manage-vietnam-legal` | Vietnam Legal Counsel role; litigation/court representation -> qualified human legal counsel |
| Vietnam AI Law 134/2025 compliance audit, risk classification, or conformity assessment | `audit-ai-compliance` | Vietnam Legal Counsel role; regulatory filings -> qualified human legal counsel |
| Vietnam formal legal opinion drafting, statutory analysis, or non-litigation caveats | `draft-legal-opinion` | Vietnam Legal Counsel role; external representation/issuance -> qualified human legal counsel |
| Agent-ready web discovery | `configure-agent-headers` + `manage-api-catalog` | Agent Discovery Engineer |
| Root-cause analysis & defect reproduction | `systematic-debugging` | QA Engineer |
| Combinatorial test matrix reduction | `combinatorial-testing` | QA Engineer |
| Modern auth, OAuth2 PKCE, session revocation, or tenant isolation | `implement-auth` | Backend Developer |
| PostgreSQL query optimization, connection pooling, or RLS policies | `optimize-postgres` | Backend Developer |
| Advanced component composition, slot delegation, headless decomposition | `component-composition` | Frontend Developer |
| Native CSS View Transitions, shared element morphing, route transitions | `implement-view-transitions` | Frontend Developer |
| React Native / Expo New Architecture, Hermes, FlashList recycling, offline sync | `develop-mobile-app` | Mobile Engineer |
| Mobile EAS Build, signing credentials, OTA updates, App Store compliance | `deploy-mobile-app` | Mobile Engineer |
| Direct-response copywriting, conversion copy, behavioral psychology | `write-copy` | Content Writer |
| Content strategy, pillar-cluster taxonomy, funnel mapping, decay triage | `design-content-strategy` | Content Manager |
| Technical SEO audit, crawl budgets, AI bot governance | `audit-technical-seo` | SEO Analyst role |
| Connected Schema.org @graph JSON-LD, E-E-A-T credentials | `implement-schema-markup` | SEO Analyst role |
| Enterprise MCP server architecture, tool contract design, stateless HTTP transport | `architect-mcp-server` | Technical Architect |
| Recursive system & task decomposition, DAG dependencies, disk-backed persistent planning | `decompose-agentic-system` | Technical Architect |
| Columnar database architecture, sparse indexing, ClickHouse / DuckDB tuning | `optimize-olap-database` | Data Engineer role |
| In-process embedded analytical SQL (chDB, DuckDB), cross-source joins | `query-analytical-engine` | Data Analyst role |
| Controlled chaos engineering, steady-state verification, game day drills | `orchestrate-chaos-experiment` | SRE role |
| High-throughput LLM serving, vLLM v1 PagedAttention, DRA GPU scheduling | `deploy-vllm-inference` | AI Systems Engineer role |
| Concentric border radius, OKLCH lightness delta steps, APCA contrast math | `design-system-engineering` | UI/UX Designer role |
| 100% state coverage & optical finish gate criteria | `anti-ui-slop-finish-gate` | UI/UX Designer role |
| 2px optical button padding offsets, play centroid shift, iOS zoom guard | `frontend-micro-polish` | Frontend Developer role |
| URL search param switchers (?__state=, ?__variant=) for component previews | `interactive-component-workbench` | Frontend Developer role |
| 6-axis hostile scenario resilience testing (break-axes) | `hostile-component-stress-testing` | QA Engineer role |
| Tripartite evidence triage (screenshot + DOM snapshot + console/telemetry) | `playwright-evidence-qa` | QA Engineer role |
| Zero-execution static AST security analysis for third-party skills | `skill-preflight-ast-check` | Security Engineer role |

## Backlog (not yet skills)

### Priority 2

- `3d-material-pipeline` (not yet created)
- `product-discovery` (not yet created)

### Priority 3

- `frontend-state-management` (not yet created)

## Naming Rules

- prefer generic names over stack-specific names
- categorize skills under their respective taxonomy folders (agent, foundation, backend, frontend, platform, security-data, documentation, education)
- move stack-specific or org-specific variants into overlays when they are not portable

## Skill Authoring Standard

Every SKILL.md is an [Agent Skills](https://agentskills.io/specification) manifest (the open standard indexed by skills.sh): YAML frontmatter with required `name` and `description`, then a markdown body. The pack layers these baseline sections on top:

1. YAML frontmatter with `name` and `description`.
2. H1 title matching the skill name in title case.
3. One short "Use this skill..." paragraph.
4. `## Core Rules` for non-negotiable constraints.
5. `## Suggested Process` for the normal execution path.
6. `## Checklist` for completion checks.
7. `## Related Skills` with one-line descriptions.

Optional spec fields (`license`, `compatibility`, `metadata`, `allowed-tools`) may be added when they carry real information; do not add per-skill versions — the pack `VERSION` governs all core skills.

Optional body sections such as `## Output Format`, `## When to Use`, `## Deliverable Decision`, or domain-specific guidance are fine when they improve execution; contract-emission guidance must use the canonical `## Output Contracts` heading.

Descriptions should include both what the skill does and when to use it, with specific trigger keywords — agents match requests against this field at startup. Keep skills repo-agnostic by default; put stack-specific assumptions in adapters or overlays.

### References Subdirectory Policy

A skill may add a `references/` subdirectory when the SKILL.md body alone would exceed ~150 lines. Use `references/` for:

- long external-spec excerpts (e.g., `agent-a2a-protocol/references/a2a-spec.md`)
- framework or stack variant guides (e.g., `turnstile-spin/references/{astro,hugo,nextjs-app,nextjs-pages,sveltekit,vanilla-html}.md`)
- deep rules/checklists that the SKILL.md body summarizes (e.g., `durable-objects/references/{rules,testing,workers}.md`)

When you add a `references/` subdirectory:

- keep SKILL.md focused on the trigger conditions, core rules, suggested process, and checklist
- link from SKILL.md to each reference doc by relative path the first time the topic appears (e.g., `See references/rules.md for the full checklist`)
- do not duplicate content between SKILL.md and `references/`
- references are loaded on demand — do not rely on them being read for the skill to start

The validator does not check `references/` content; the structural contract only applies to the SKILL.md file itself.

### Size Guidance

- Aim for SKILL.md between 80 and 200 lines.
- Below ~70 lines is acceptable for tight, scope-narrow skills (e.g., compliance-locked MMO skills) provided all baseline sections are present.
- Above ~200 lines signals a candidate for `references/` extraction; above 500 lines is rejected by the validator.

### Domain Cluster Notes (2026)

- The **MMO cluster** spans multiple taxonomies by design (foundation for content/ROI, platform for infra/automation, security-data for assets/tracking). Their pre-2025.4 drift has been retired; current skills carry Legal & Compliance Notices that map to `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role.
- The **R3F/3D cluster** migrated from `core/skills/frontend/` to `overlays/r3f-stack/skills/` in v4.0.0. The `3d-graphics-engineer` role toolbox resolves via overlay. See `overlays/r3f-stack/README.md` for the migration notes.

## Validation Gate

Run this before treating core skill changes as complete:

```bash
python3 core/scripts/validate-skills.py
```

The validator checks:

- every skill has valid `name` and `description` frontmatter
- Agent Skills spec compliance: hyphen placement in names, no XML tags, no reserved words
- descriptions include both capability and trigger language
- skill names match directory names
- every skill has the baseline sections
- checklists contain enough actionable completion checks
- related skill references point to existing skills
- role and workflow skill references resolve

Skill changes are not done until this check passes.

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

Last updated: 2026-09-02
