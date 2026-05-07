# Máy Điện Giải Sài Gòn Overlay

Project-specific conventions for the Máy Điện Giải Sài Gòn e-commerce platform — a Laravel 11 monolith selling premium water ionizers (~20 SKUs).

**Depends on:** `overlays/laravel-filament` (generic Laravel + Filament + Livewire rules)

This overlay adds only what is unique to this project:

- `rules/elomus-design-system.md` — Elomus Theme UI/UX: Deep Navy + Teal palette, Outfit font, product card hover effects, Slide-out Cart, Accordion PDP, VietQR, Mobile Sticky CTA
- `rules/mdg-project-rules.md` — Project-specific conventions: Vietnamese slugs, specific models, cPanel deploy, queue config
- `skills/develop-mdg-feature/` — Feature development skill with this project's exact file map and patterns

This overlay should be composed with `core` + `overlays/laravel-filament`, not used standalone.
