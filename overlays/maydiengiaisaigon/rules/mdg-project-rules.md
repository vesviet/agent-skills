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
