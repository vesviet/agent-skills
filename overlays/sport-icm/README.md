# Sport ICM Overlay

Project-specific conventions for the Sport ICM niche catalog — custom sportswear, athletic uniforms, and performance activewear.

**Depends on:** `overlays/astro-cloudflare`

- **Repo:** `D:\regna\cloudflare\sport-icm`
- **Live:** Cloudflare Pages (sport-icm workers.dev subdomain)

## Specifics

- Niche catalog site built on Astro + Cloudflare Pages
- Product and category data in `src/data/` (TypeScript or JSON)
- Tailwind + sport/athletic theme overrides
- Contact form via Resend API + Turnstile anti-spam
- Static pages with optional dynamic category routes

## Brand

- Niche: Custom sportswear, athletic uniforms, team jersey OEM
- Audience: Sports clubs, schools, corporate teams, tournament organizers
- Tone: Energetic, performance-focused, professional

## Rules

- `rules/sport-project-rules.md` — Catalog structure, brand positioning, deploy conventions

## Relationship to Other ICM Overlays

| Overlay | Brand | Niche |
|---------|-------|-------|
| [icm-main](../icm-main/README.md) | ICM Factory Direct | B2B corporate, master brand |
| [golf-icm](../golf-icm/README.md) | Golf ICM | Golf apparel, resort wear |
| sport-icm | Sport ICM | Sportswear, athletic uniforms |
| [obj-configurator](../obj-configurator/README.md) | OBJ 3D | WebGL product configurator |
