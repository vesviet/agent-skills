# MDG Project Rules — Máy Điện Giải Sài Gòn

Project-specific conventions that extend `overlays/laravel-filament/rules/laravel-conventions.md`.

## Models & Schema

- **Models:** `Category`, `Product`, `Order`, `OrderItem`, `Article`, `User`
- **Category** uses polymorphic `type` enum (`product`, `article`) for both product and blog categories.
- **Product** has `gallery` as JSONB, `features` as JSONB for specifications table.
- **Order** tracks `status` (pending → confirmed → shipping → completed → cancelled) and `payment_status` (unpaid → paid → refunded).

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

- **Dev:** SSH Server (`192.168.1.114`) at `/home/tuananh/laravel/maydiengiaisaigon`.
- **Prod:** cPanel Shared Hosting.
- **Queue (Dev):** Supervisor runs `php artisan queue:work`.
- **Queue (Prod):** Cronjob `* * * * * php artisan queue:work --stop-when-empty`.

## Media

- Spatie Media Library with WebP auto-conversion.
- Responsive image sizes for product galleries.
- Cloudflare CDN in production for bandwidth savings.
