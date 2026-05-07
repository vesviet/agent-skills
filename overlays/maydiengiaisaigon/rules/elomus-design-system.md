# Elomus Design System — Máy Điện Giải Sài Gòn

UI/UX design constraints based on the Elomus Theme reference for premium water ionizer presentation.

## Color Palette

- **Primary text / headings:** Deep Navy (`#1B2A4A`) — never use pure black `#000000`.
- **CTA / accent:** Teal (`#2BA5B5`) or Soft Aqua (`#5EC4D4`) — evokes "clean water technology".
- **Background:** Clean White (`#FFFFFF`) with generous whitespace.
- **Subtle backgrounds:** Light Gray (`#F8F9FA`) for alternating sections.
- **Danger / Sale:** Coral (`#E84C3D`).

## Typography

- **Primary font:** `Outfit` or `Plus Jakarta Sans` from Google Fonts — never browser defaults.
- **Headings:** 600–700 weight, generous letter-spacing.
- **Body:** 400 weight, line-height 1.7 for readability.
- **Price display:** Tabular nums, bold, with VND formatting via `number_format()`.

## Layout Principles

- Wide layouts with ample whitespace — premium feel.
- Sticky Header: transparent on top, solid background on scroll.
- Hero Banner: full-width, high-quality imagery with overlay text.
- Product Grid: 3–4 columns on desktop, 2 on tablet, 1 on mobile.

## Product Card Interactions

- Hover: swap to second gallery image.
- Hover: "Thêm vào giỏ" button slides up from bottom.
- Price shows original (strikethrough) and sale price side-by-side.

## Product Detail Page (PDP)

- Accordion tabs: Mô tả chung, Thông số kỹ thuật, Chính sách bảo hành.
- Mobile: Sticky bottom CTA bar with "Thêm vào giỏ" button.
- Trust Badges below CTA: Bảo hành 5 năm, Miễn phí lắp đặt, Chứng nhận y tế.

## Cart (Slide-out Drawer)

- Opens from right edge via Livewire + Alpine.js.
- Shows item thumbnail, name, quantity controls, line total.
- Overlay backdrop on desktop, full-screen on mobile.

## Checkout UX

- VietQR integration: auto-render QR code with amount and order number.
- Fallback: plain-text bank account details if API fails.
- Payment methods: COD and Bank Transfer only.

## Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px–1024px
- Desktop: > 1024px
- Max content width: 1280px
