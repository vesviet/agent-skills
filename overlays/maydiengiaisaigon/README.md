# Máy Điện Giải Sài Gòn Overlay

Project-specific conventions for the Máy Điện Giải Sài Gòn e-commerce platform — a Laravel 13 monolith selling premium water ionizers (~20 SKUs).

**Depends on:** `overlays/laravel-filament` (generic Laravel 13 + Filament v4 + Livewire 3 rules)

⚠️ **2026 Migration Status**: Upgrading from Laravel 11 → 13 and Filament v3 → v4.
- Laravel 12 bug fix support ended Aug 13, 2026 — Laravel 13 migration required.
- Filament v4 introduces unified `Schema` API — update all Resources.

This overlay adds only what is unique to this project:

- `rules/elomus-design-system.md` — Elomus Theme UI/UX: Deep Navy + Teal palette, Outfit font, product card hover effects, Slide-out Cart, Accordion PDP, VietQR, Mobile Sticky CTA
- `rules/mdg-project-rules.md` — Project-specific conventions: Vietnamese slugs, specific models, cPanel deploy, queue config
- `skills/develop-mdg-feature/` — Feature development skill with this project's exact file map and patterns

Compose with `core` + `overlays/laravel-filament`, not standalone.
