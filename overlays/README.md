# Overlays

Overlays extend the portable core with repo-specific, brand-specific, or domain-specific behavior.

Use an overlay when:

- a skill needs absolute content roots or collection paths
- a role needs org-local toolbox extensions
- a workflow assumes one repository family or publishing pipeline
- a pack needs local conventions that do not belong in the global core

## Current Overlays (17)

### Stack Overlays (tech-specific, project-agnostic)

| Overlay | Stack | What it adds |
|---------|-------|--------------|
| [astro-cloudflare](astro-cloudflare/README.md) | Astro v5 + Cloudflare Pages/Workers | Architecture patterns, component conventions, Wrangler deploy rules, ESLint/Prettier config |
| [laravel-filament](laravel-filament/README.md) | Laravel 11 + Filament v3 + Livewire 3 | DB integrity rules, Filament patterns, Pest testing standards, `develop-laravel-feature` skill |
| [go-microservices](go-microservices/README.md) | Go (Golang) | Clean Architecture conventions, gRPC/REST patterns, structured logging, table-driven tests |
| [r3f-stack](r3f-stack/README.md) | React Three Fiber / Three.js (WebGL) | **Stub** — reserved namespace for the R3F cluster migration planned for v4.0.0 |

### Project Overlays (project-specific, depends on a stack overlay)

| Overlay | Project | Depends On |
|---------|---------|------------|
| [maydiengiaisaigon](maydiengiaisaigon/README.md) | Máy Điện Giải Sài Gòn e-commerce (Laravel, ~20 SKUs) | `laravel-filament` |
| [icm-main](icm-main/README.md) | ICM Factory Direct corporate site (Astro/Cloudflare, B2B sportswear) | `astro-cloudflare` |
| [golf-icm](golf-icm/README.md) | Golf ICM niche catalog (Astro/Cloudflare, golf apparel) | `astro-cloudflare` |
| [sport-icm](sport-icm/README.md) | Sport ICM niche catalog (Astro/Cloudflare, sportswear) | `astro-cloudflare` |
| [obj-configurator](obj-configurator/README.md) | OBJ 3D Configurator (Astro + R3F/Three.js, WebGL) | `astro-cloudflare` |
| [ecommerce-microservices](ecommerce-microservices/README.md) | Ecommerce microservices platform | `go-microservices` |
| [donthan-web](donthan-web/README.md) | Donthan.com livestream platform (web-first desktop UX) | standalone (no stack overlay) |

### Content & Domain Overlays (domain-specific, project-agnostic)

| Overlay | Domain | What it adds |
|---------|--------|--------------|
| [vesviet-content](vesviet-content/README.md) | Vesviet / Learn Hugo sites | Brand voice, content schema, `write-vesviet-learn-content` skill, series publishing workflow |
| [lease-content](lease-content/README.md) | Lease in Vietnam / Máy Lạnh Treo Tường (Astro) | Content schema, collections config, `write-leaseinvietnam-maylanhtreotuong-data` skill |
| [seo-publishing](seo-publishing/README.md) | Dual-site SEO sprint | 7-day topic boards, publish logs, cannibalization rules, cadence runbook |
| [ui-design-system](ui-design-system/README.md) | UI design systems | Flow/component handoff conventions |
| [data-analyst-stack](data-analyst-stack/README.md) | DuckDB + Metabase BI | BI metric dashboard templates, stack conventions |
| [data-engineer-rabity](data-engineer-rabity/README.md) | Data engineering learning project | Learning conventions, phase roadmap |

## Overlay Authoring Rules

- keep overlays out of `core/` — portable core must work without any overlay loaded
- an overlay may extend rules, roles, skills, and workflows but must not break core validators
- project overlays should declare their stack overlay dependency in their README
- validate overlays together with core: `python3 core/scripts/validate-skills.py`
