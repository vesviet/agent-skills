# Landing Pages Team Pack (`landing-pages-team`)

> **Version:** `5.0.0` · **Target System:** High-Converting Single-Product Landing Page Engine & SaaS (`landing-builder.example.com` / Carrd for Ads)  
> **Repository:** [`landing-pages`](https://github.com/example-org/landing-pages)  
> **Composition:** `core` + `overlays/go-microservices` + `overlays/ui-design-system` + `overlays/seo-publishing`

---

## 1. Tổng Quan & Sứ Mệnh (Executive Overview & Mission)

Gói năng lực **`landing-pages-team`** chuẩn hóa toàn diện quy trình phát triển, vận hành, tối ưu tỷ lệ chuyển đổi (CRO) và bảo vệ an toàn kiến trúc cho nền tảng tạo Landing Page bán hàng chuyển đổi cao số 1 cho nhà bán hàng chạy Ads Việt Nam (**Carrd for Ads** — [`landing-builder.example.com`](https://landing-builder.example.com)):

* **Tải trang siêu tốc Edge Serverless (TTFB < 25ms)**: Phục vụ 100% bằng Cloudflare Workers SSR, giữ chân tối đa lượt nhấp chuột từ quảng cáo TikTok, Facebook và Google Ads.
* **Chốt đơn 1-chạm COD & Thanh toán số tức thì**: Không bắt người mua đăng ký/đăng nhập giỏ hàng rườm rà. Tích hợp sẵn VietQR Napas 247 tạo mã QR động tự khớp đơn hàng.
* **Bản địa hóa sâu sắc cho thị trường Việt Nam**: Bộ nút nổi liên hệ Zalo & Messenger thu hút khách hàng, Chân trang uy tín minh bạch địa chỉ kho và chính sách bảo hành/đổi trả 1 đổi 1.
* **Bắn đơn tức thì qua Telegram Bot**: Telesale nhận thông báo đơn hàng kèm phân loại chi tiết (`Màu: ... | Size: ...`) trong vòng 5 giây để gọi chốt đơn ngay lập tức.
* **Trợ lý AI rà soát từ ngữ vi phạm**: Tích hợp thuật toán Aho-Corasick rà soát các từ ngữ cấm quảng cáo của TikTok/Facebook (cam kết 100%, trị dứt điểm...) trước khi xuất bản trang.

---

## 2. Kiến Trúc Hệ Thống & Các Ràng Buộc Bất Biến (Architectural Invariants)

Hệ thống được tổ chức theo 3 tầng phân tách rành mạch:

```
                          ┌──────────────────────────────────────┐
                          │     Khách Mua Hàng & Ads Traffic     │
                          └──────────────────┬───────────────────┘
                                             │ HTTPS
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ CLOUDFLARE WORKERS EDGE ENGINE (workers/landing-engine)                                │
│ • Dual Host Routing: landing-builder.example.com vs *.landing-builder.example.com      │
│ • TTFB < 25ms Edge SSR • SITES_KV Invalidation • 0ms Cold Start • Zero Layout Shift   │
│ • 5 CRO Templates: universal-classic, clinical-trust, flash-sale-urgency,              │
│                     luxury-dark, story-provenance                                      │
└──────────────────┬─────────────────────────────────────────────────▲───────────────────┘
                   │ Proxy API Orders / Submits                      │ KV Sync on Publish
                   ▼                                                 │
┌────────────────────────────────────────────────────────┐           │
│ GO KRATOS v2 CLEAN ARCHITECTURE BACKEND (backend/)     │           │
│ • CA-1..CA-9 Architecture Fitness Gates                │           │
│ • ADR-07 Zero-Trust Price Engine (Total re-calc)       ├───────────┘
│ • ADR-09 Aho-Corasick Ad Policy Scanner                │
│ • MySQL 8.4 GORM Persistence & Redis Cache             │
│ • Outbox Pattern Event Publisher                       │
└────────────────────────────────────────────────────────┘
```

### Các Ràng Buộc Kiến Trúc Bắt Buộc (Clean Architecture CA-1..CA-9):
1. **CA-1 (No ORM Leak)**: Tầng `biz` tuyệt đối không được import `gorm.DB` hay bất kỳ ORM framework nào.
2. **CA-2 (Service Isolation)**: Tầng `service` không được gọi trực tiếp tầng `data`, bắt buộc đi qua interface tại `biz`.
3. **CA-3 (Hermetic Boundary)**: E2E test không được import `backend/internal` (opaque-box testing).
4. **CA-4 (Wire Dependency Injection)**: File `wire_gen.go` phải luôn được sinh và commit đồng bộ.
5. **CA-5 (Zero Secrets)**: Tuyệt đối không hardcode API token, database password hay credentials trong mã nguồn.
6. **CA-6 (Zero-Trust Price Engine - ADR-07)**: Giá tiền đơn hàng (`TotalAmount`) bắt buộc phải do server tính toán độc lập dựa trên giá biến thể trong database; cấm tin tưởng giá gửi lên từ client.
7. **CA-7 (Policy Scanner - ADR-09)**: Thuật toán quét từ cấm Aho-Corasick bắt buộc nằm trong tầng `biz`.
8. **CA-8 (Zero Linter Warnings)**: `golangci-lint` phải đạt 0 warning, 0 error.
9. **CA-9 (Dependency Security)**: 100% dependencies quét sạch qua Govulncheck và Trivy.

---

## 3. Các Phân Hệ Tính Năng Cốt Lõi (Core Capabilities)

### 3.1. Ma Trận Biến Thể 2 Chiều (Footwear & Apparel 2D Matrix)
- Hỗ trợ chọn **Màu sắc $\times$ Kích cỡ (Size 35-44+)** độc lập trên cả 5 template.
- Tự động disabled/gạch chéo các size hết hàng theo màu đang chọn.
- Modal Bảng quy đổi kích thước bàn chân (`<dialog id="size-guide-modal">`) chuẩn hóa theo cm.
- Preset 1-chạm trong Dashboard Editor tự động sinh 30 SKU và bảng size 10 dòng chỉ trong 10 giây.

### 3.2. SaaS Marketing Storefront (`landing-builder.example.com` / `www.landing-builder.example.com`)
- Phục vụ trực tiếp qua Cloudflare Edge SSR với TTFB < 25ms.
- Phân luồng Host Routing thông minh: Không ảnh hưởng tới subdomain bán hàng của merchant hay Custom Domain.
- Bộ nhận diện thương hiệu chuẩn mực: Biểu tượng Logo đa giác vát góc kết hợp tia chớp tốc độ và ngôi sao vàng tỏa sáng, bố cục 2 hàng phân cấp tỷ lệ vàng (Hàng 1: `landing-builder.example.com`, Hàng 2: `CARRD FOR ADS`).
- Tích hợp đầy đủ Schema.org JSON-LD (`WebSite`, `SoftwareApplication`, `FAQPage`).

### 3.3. Merchant Dashboard & Onboarding Wizard
- Trình soạn thảo tập trung SplitViewEditor: Chỉnh sửa nội dung kèm xem trước tức thì (Live Preview).
- Quản trị đơn hàng chuyên nghiệp: Tự động che số điện thoại (Paywall Phone Masking `0987.654.xxx`) trên gói Miễn phí từ đơn thứ 51 trở đi, mở khóa 100% khi nâng cấp Pro.
- Xuất đơn hàng linh hoạt sang các đơn vị vận chuyển tại Việt Nam (GHTK, GHN, Viettel Post).

---

## 4. Đội Ngũ Swarm & Phân Công Trách Nhiệm (Multi-Role Swarm Pipeline)

| Vai Trò | Trách Nhiệm Cốt Lõi Trong Pack `landing-pages-team` |
| :--- | :--- |
| **`@solution-architect`** | Thiết kế kiến trúc tổng thể, phân giải routing Cloudflare Edge, đảm bảo tính bất biến CA-1..CA-9. |
| **`@backend-developer`** | Triển khai Go Kratos v2, Wire DI, GORM MySQL, Zero-Trust Price Engine, Outbox Pattern, Telesale Telegram alert. |
| **`@frontend-developer`** | Xây dựng Dashboard React, Zustand store, SplitViewEditor, VariantMatrixSection, tích hợp VietQR và Zalo/Facebook floating widget. |
| **`@cloudflare-engineer`** | Tối ưu Edge SSR, đồng bộ Cloudflare KV, wrangler deployment, TTFB < 25ms, Zero-CLS template rendering. |
| **`@ui-ux-designer`** | Thiết kế nhận diện thương hiệu, Taste-Skill anti-slop, tỷ lệ quang học Logo, 5 CRO templates UX, Size Guide modal. |
| **`@seo-analyst`** | Tối ưu Canonical URLs, thẻ OpenGraph/Twitter Cards cho mạng xã hội, Schema.org JSON-LD, robots.txt và sitemap.xml. |
| **`@qa-engineer`** | Xây dựng và duy trì 100% test pass: Hermetic E2E tests, Vitest component tests, Adversarial stress suites, Paywall masking tests. |
| **`@devops-engineer` / `@sre`** | Vận hành GitHub Actions CI/CD (14 jobs green), Docker GHCR build, ArgoCD GitOps auto-sync, Cloudflare Workers release. |

---

## 5. Quy Trình Vận Hành (Standard Operating Workflows)

Gói năng lực hỗ trợ 3 quy trình vận hành chính:
1. **Tạo & Xuất Bản Trang Đích (Landing Page Creation & Publishing)**: Khởi tạo từ Template $\to$ Tùy biến nội dung & Biến thể $\to$ AI Ad Policy Scan $\to$ Xuất bản tức thì lên Edge KV $\to$ Modal chúc mừng & QR code.
2. **Quản Lý Bán Hàng & Chốt Đơn Telesale (Lead Funnel & Order Lifecycle)**: Khách đặt hàng COD / VietQR $\to$ Zero-Trust Server Price Check $\to$ Ghi nhận database $\to$ Bắn Telegram Telesale $\to$ Xác nhận đơn $\to$ Xuất vận đơn.
3. **Triển Khai CI/CD & Cập Nhật Hệ Thống (Production Deployment)**: Kiểm thử đa tầng (Go unit/data/e2e + Vitest + Fitness functions) $\to$ Build Docker image $\to$ GitOps ArgoCD $\to$ Deploy Cloudflare Workers.

---

## 6. Tiêu Chuẩn Tuân Thủ 2026-2027 (Compliance & Security)

- **EU AI Act Tier**: `minimal_risk` (Công cụ tạo landing page nội bộ và hỗ trợ merchant thương mại điện tử).
- **OWASP ASI Guardrails**:
  - `ASI01 (Goal Hijack)`: Mọi hành động xuất bản và sửa đổi trang đều phải gắn liền với định danh merchant (`merchant_id`).
  - `ASI03 (Zero-Trust Security)`: Cơ chế tính giá tiền server-side bảo vệ merchant khỏi gian lận thay đổi giá từ trình duyệt.
  - `ASI04 (Supply Chain Security)`: 100% Go binaries và npm packages được kiểm tra lỗ hổng bằng Trivy và Govulncheck trước khi xuất bản container.
  - `ASI06 (PII Protection)`: Mã hóa và che giấu thông tin cá nhân (số điện thoại khách mua hàng) theo gói dịch vụ Free/Pro.
