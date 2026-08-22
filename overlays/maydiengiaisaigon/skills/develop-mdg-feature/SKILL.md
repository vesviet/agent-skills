---
name: develop-mdg-feature
description: Develop features for the Máy Điện Giải Sài Gòn Laravel 13 + Filament v4 e-commerce. Use when adding Filament admin resources, Blade pages, Livewire components, or e-commerce logic (cart, checkout, orders) in this specific project.
---

# Develop MDG Feature

Use this skill when building or modifying features in the Máy Điện Giải Sài Gòn e-commerce platform. This extends the generic `develop-laravel-feature` skill with project-specific file map, models, and design constraints.

**Stack (2026):** Laravel 13 + Filament **v4** (Schema API) + Livewire 3 + PHP 8.3+ + Pest v5.

**Prerequisites:** Read `overlays/laravel-filament/rules/laravel-conventions.md` first for generic patterns.

## Project Map

```
D:\myproject\maydiengiaisaigon\
├── app/
│   ├── Actions/                ← Single-action classes (ProcessCheckoutAction)
│   ├── Services/               ← Stateful services (CartService)
│   ├── Filament/Resources/     ← Admin: CategoryResource, ProductResource,
│   │                              OrderResource, ArticleResource
│   ├── Http/
│   │   ├── Controllers/        ← PageController, ProductController,
│   │   │                          ArticleController, CheckoutController
│   │   └── Requests/           ← FormRequest validation
│   ├── Livewire/               ← CartDrawer, AddToCartButton, CartIcon
│   ├── Models/                 ← Category, Product, Order, OrderItem, Article
│   └── Providers/
├── database/migrations/        ← PostgreSQL migrations
├── resources/views/
│   ├── layouts/                ← Base Blade layouts (Elomus Theme)
│   ├── pages/                  ← Static page templates
│   └── livewire/               ← Livewire component views
├── routes/web.php              ← Vietnamese-slug routes
└── tests/                      ← Pest PHP tests
```

## Core Rules

- Follow all rules from `overlays/laravel-filament/rules/laravel-conventions.md` (Thin Controller, DB::transaction, FormRequest, etc.)
- Follow all rules from `overlays/maydiengiaisaigon/rules/mdg-project-rules.md` (Vietnamese slugs, VietQR, deploy targets)
- Apply design tokens from `overlays/maydiengiaisaigon/rules/elomus-design-system.md` (Deep Navy + Teal palette, Outfit font, Elomus interactions)

## Suggested Process

### 1. Identify The Layer

| Task | Layer | Location |
|------|-------|----------|
| Admin CRUD | Filament Resource | `app/Filament/Resources/` |
| New public page | Controller + Blade | `app/Http/Controllers/` + `resources/views/pages/` |
| Interactive widget | Livewire | `app/Livewire/` + `resources/views/livewire/` |
| Business logic | Action / Service | `app/Actions/` or `app/Services/` |
| Schema change | Migration | `database/migrations/` |
| Payment / QR | Service + Config | `app/Services/` |

### 2. Read Existing Patterns

- **Filament**: Read `ProductResource.php` for form/table, media upload, enum selects.
- **Controller**: Read `ProductController.php` for thin-controller pattern.
- **Livewire**: Read `CartDrawer.php` for Alpine.js integration and event dispatching.
- **Model**: Read `Product.php` for casts, relationships, scopes, media conversions.
- **Action**: Read `ProcessCheckoutAction.php` for DB::transaction() pattern.

### 3. Apply Design System

- Deep Navy (`#1B2A4A`) for text, Teal (`#2BA5B5`) for CTAs.
- Outfit font from Google Fonts.
- Product card hover: swap to second image + slide-up "Thêm vào giỏ" button.
- Mobile: Sticky bottom CTA bar on PDP.

### 4. Test Critical Paths

- Cart total calculation and checkout flow (Pest PHP).
- Run: `php artisan test` or `./vendor/bin/pest`.

## Checklist

- [ ] feature placed in the correct architectural layer
- [ ] thin controller pattern followed
- [ ] Livewire used only for interactive islands
- [ ] **Filament v4 `Schema::components()` used** (not deprecated v3 `Form::schema()`)
- [ ] DB::transaction() wraps multi-table writes
- [ ] migrations include indexes on slug, category_id, status columns
- [ ] SoftDeletes on Category and Product
- [ ] Elomus design tokens applied (Deep Navy, Teal, Outfit font)
- [ ] Vietnamese slug routes match web.php conventions
- [ ] FormRequest used for validation
- [ ] media via Spatie with WebP conversion
- [ ] Pest v5 tests written for critical logic (cart, checkout, state transitions)
- [ ] queue used for email, never synchronous

## Related Skills

- **develop-laravel-feature**: generic Laravel + Filament + Livewire patterns (read first)
- **review-code**: review against Laravel and project conventions
- **write-tests**: write Pest PHP tests
- **navigate-service**: understand the codebase before changes
- **commit-code**: commit with proper conventions
