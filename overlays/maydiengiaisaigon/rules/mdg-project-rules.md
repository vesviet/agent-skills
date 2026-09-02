# MDG Project Rules — Máy Điện Giải Sài Gòn

Project-specific conventions extending `overlays/laravel-filament/rules/laravel-conventions.md`.

## 2026 Migration Status

- **Laravel 13** (migrating from 11 → 12 → 13; L12 bug fix support ended Aug 13, 2026)
- **Filament v4** — update all Resources to use `Schema::components()` API
- **PHP 8.3+** required; adopt PHP 8.4 Property Hooks in new model code

## Models & Schema

- **Models:** `Category`, `Product`, `Order`, `OrderItem`, `Article`, `User`
- **Category** uses polymorphic `type` enum (`product`, `article`) for both product and blog categories.
- **Product** has `gallery` as JSONB, `features` as JSONB for specifications table.
- **Order** tracks `status` (pending → confirmed → shipping → completed → cancelled) and `payment_status` (unpaid → paid → refunded).

```php
// PHP 8.4 Property Hooks in new model code
class Product extends Model {
    public string $displayPrice {
        get => 'đ' . number_format($this->price, 0, ',', '.');
    }
    public private(set) string $slug;
}
```

## Routes (Vietnamese Slugs)

All public routes use Vietnamese paths:
- `/` — Trang chủ
- `/san-pham` — Danh sách sản phẩm
- `/san-pham/{slug}` — Chi tiết sản phẩm
- `/tin-tuc` — Blog / Bài viết
- `/tin-tuc/{slug}` — Chi tiết bài viết
- `/gioi-thieu` — Giới thiệu
- `/lien-he` — Liên hệ
- `/thanh-toan` — Checkout
- `/dat-hang-thanh-cong/{orderNumber}` — Order success + VietQR

## Checkout & Payment

- Payment methods: COD (`cod`) and Bank Transfer (`bank_transfer`).
- VietQR API renders QR code on success page with pre-filled amount and order number.
- Fallback: plain-text bank details if VietQR API fails.
- Order confirmation email dispatched via queue to customer + admin notification to BOD.

## Deploy Environments

- **Dev:** SSH Server at `/home/tuananh/laravel/maydiengiaisaigon`
- **Prod:** cPanel Shared Hosting (PHP 8.3+ required — confirm hosting supports PHP 8.3+)
- **Queue (Dev):** Supervisor runs `php artisan queue:work`
- **Queue (Prod):** Cronjob `* * * * * php artisan queue:work --stop-when-empty`
- **Laravel Pulse:** Available at `/pulse` in dev for queue health, slow queries, exceptions

## Media

- Spatie Media Library with WebP auto-conversion.
- Responsive image sizes for product galleries.
- Cloudflare CDN in production for bandwidth savings.

## Filament v4 Resources (Migration Required)

```php
// Update all Resource files from v3 to v4:
use Filament\Schemas\Schema;  // was: use Filament\Forms\Form

public function form(Schema $schema): Schema  // was: form(Form $form): Form
{
    return $schema->components([  // was: ->schema([
        TextInput::make('name')->required(),
    ]);
}
```

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/backend/scaffold-new-service/SKILL.md` and the `implementation-result.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/backend/scaffold-new-service/SKILL.md` and the `implementation-result.json` schema.

Last updated: 2026-09-01
