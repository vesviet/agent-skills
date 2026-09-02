# Donthan Web UX Conventions

Áp dụng cho mọi UI/UX Designer và Frontend Developer khi làm việc với dự án Donthan.com (Web-first).

## 1. Web-First Layout Architecture
- **Tuyệt đối không dùng Bottom Navigation Bar cho giao diện Desktop.**
- **Sidebar Layout:** Sử dụng Left-Sidebar (Menu dọc cố định bên trái) cho việc điều hướng chính (Trang chủ Live, Khám phá, Tin nhắn, Cá nhân) tương tự Twitch hoặc Discord.
- **Split-Pane Livestream:** Màn hình phòng Live trên Desktop phải tận dụng chiều ngang:
  - Cột Trái (Left Pane): Thu gọn danh sách menu.
  - Cột Giữa (Center Pane): Luồng Video Livestream chính giữa.
  - Cột Phải (Right Pane): Text Chat và Khung Tặng Quà (Virtual Gifts) ghim cố định, không che lấp Video.

## 2. Responsive Degradation (Thích ứng di động)
- Thiết kế cho Desktop/Tablet trước. Khi co màn hình về kích thước Mobile (width < 768px), Left-Sidebar sẽ biến mất và chuyển thành Bottom Tab Bar tạm thời (PWA style).
- Khung Chat ở màn hình Mobile sẽ hiển thị dạng Overlay (mờ) đè lên nửa dưới của luồng Video.

## 3. Dark Mode Tối ưu (Livestream Focus)
- Giao diện mặc định là Dark Mode (Gradient Indigo/Deep Purple) để tối ưu hoá việc xem Video thời gian dài trên màn hình lớn. Tuyệt đối không dùng nền trắng tinh cho các trang có luồng video để tránh mỏi mắt.

## 4. AI Tarot Web UX
- Trên Desktop, kết quả AI Tarot được hiển thị bằng Popup Modal hoặc Side-panel trượt từ mép phải ra. Tuyệt đối không chuyển hẳn sang trang mới (Full page reload) để tránh ngắt quãng tiếng/hình của luồng xem Live.
- Luôn có Tag `🔮 AI Generated` và dùng Tooltip (khi di chuột vào tag) để hiển thị chi tiết Độ Tự Tin (Confidence Level).

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
  See `See `core/skills/frontend/setup-design-system/SKILL.md` and the `implementation-result.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/frontend/setup-design-system/SKILL.md` and the `implementation-result.json` schema.

Last updated: 2026-09-01
