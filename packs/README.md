# Packs

Packs describe how to assemble the portable core with zero or more overlays for a target team. Each pack has a `manifest.yaml` that declares which `core` and `overlays/` to include.

## Available Packs (9)

| Pack | Manifest | Composition |
|------|----------|-------------|
| `global-engineering` | [manifest.yaml](global-engineering/manifest.yaml) | `core` only — no overlays |
| `vesviet-team` | [manifest.yaml](vesviet-team/manifest.yaml) | `core` + `overlays/vesviet-content` |
| `lease-team` | [manifest.yaml](lease-team/manifest.yaml) | `core` + `overlays/lease-content` |
| `mdg-team` | [manifest.yaml](mdg-team/manifest.yaml) | `core` + `overlays/laravel-filament` + `overlays/maydiengiaisaigon` |
| `icm-team` | [manifest.yaml](icm-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/icm-main` |
| `obj-team` | [manifest.yaml](obj-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/obj-configurator` |
| `golf-team` | [manifest.yaml](golf-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/golf-icm` |
| `sport-team` | [manifest.yaml](sport-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/sport-icm` |
| `ecommerce-team` | [manifest.yaml](ecommerce-team/manifest.yaml) | `core` + `overlays/go-microservices` + `overlays/ecommerce-microservices` |

## Manifest Format

Each `manifest.yaml` follows this schema:

```yaml
name: <pack-slug>
description: <one-line description>
includes:
  - core
  - overlays/<overlay-name>   # zero or more
```

## Pack Authoring Rules

- always include `core` as the first entry in `includes`
- list stack overlays before project-specific overlays
- validate after editing: `python3 core/scripts/validate-packs.py`
