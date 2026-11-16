# BÁO CÁO NGHIÊN CỨU CHUYÊN SÂU: KHO LƯU TRỮ MATTPOCOCK/SKILLS
## Phân Tích Kiến Trúc, Danh Mục 39 Kỹ Năng, Đánh Giá Đối Chiếu và Lộ Trình Áp Dụng Cho Hệ Thống `agent-skills` & `lotte-dms-agent`

**Mã tài liệu:** `REP-SKILLS-2026-MP01`  
**Phiên bản khảo sát:** `mattpocock/skills` v1.3.2 (Commit `5863806`)  
**Đối chiếu hệ thống:**  
- `agent-skills` v5.9.0 (39 Roles, 184 Skills, 25 Workflows, 63 Schemas, 17 Packs, 21 Overlays, 21 Validation Gates)  
- `lotte-dms-agent` v2.15.0 / A2A v3.1.0 (19 Roles, 35 Skills, 6 Workflows, 65 Schemas, Quy mô 20M+ đơn hàng)  
**Ngày phát hành:** 16 tháng 11 năm 2026  
**Trạng thái:** Hoàn tất nghiên cứu kỹ thuật & Đề xuất hành động (Production-Ready Technical Report)  
**Tác giả:** Đội ngũ Kỹ sư Tác nhân Thông minh (AI Agent Engineering Research Team)

---

## MỤC LỤC CHI TIẾT

1. [Executive Summary (Tóm Tắt Điều Hành & Mục Tiêu Chiến Lược)](#1-executive-summary)
2. [Tổng Quan Kho Lưu Trữ mattpocock/skills](#2-tổng-quan-kho-lưu-trữ-mattpocockskills)
   - 2.1 Xuất xứ, Tác giả & Định vị Triết lý
   - 2.2 Cấu trúc Cây Thư mục & Phân Vùng 4 Buckets
   - 2.3 Mô hình Phân phối Đa Nền tảng & Cơ chế Đồng bộ Harness
   - 2.4 Mô hình Kích hoạt Lưỡng tính (User vs Model Invocation)
3. [Danh Mục Toàn Diện 39 Kỹ Năng (Comprehensive Master Index)](#3-danh-mục-toàn-diện-39-kỹ-năng)
   - 3.1 Bảng Chỉ Mục Tổng Thể (Master Index Table)
   - 3.2 Phân Bố Công Cụ & Thống Kê Tần Suất Kích Hoạt
4. [Phân Tích Chuyên Sâu Các Pattern & Kỹ Thuật Nổi Bật](#4-phân-tích-chuyên-sâu-các-pattern--kỹ-thuật-nổi-bật)
   - 4.1 Kiến trúc Deep Modules (Ousterhout), Seams & The Deletion Test
   - 4.2 Đánh giá Mã nguồn Hai Trục Độc lập (Two-Axis Code Review)
   - 4.3 Vòng lặp Chẩn đoán Lỗi 6 Giai đoạn Kỷ luật Cao (Disciplined 6-Phase Debugging Loop)
   - 4.4 Lập trình Hướng Kiểm thử theo Seam (Seam-Based TDD & Anti-Tautological Testing)
   - 4.5 Đa luồng Concurrency theo Đồ thị Tác vụ & Git Worktree (`implement-spec`)
   - 4.6 Báo cáo Chẩn đoán Kiến trúc Trực quan HTML Độc lập (Tailwind & Mermaid CDN)
   - 4.7 Tự động hóa Thủ tục Có Người Can thiệp (Interactive Bash Wizard)
   - 4.8 Kỷ luật Soạn thảo Cho Tác nhân (`writing-for-agents` & Prompt Mechanics)
5. [Phân Tích Đối Chiếu Với Hệ Thống `agent-skills` (v5.9.0)](#5-phân-tích-đối-chiếu-với-hệ-thống-agent-skills-v590)
   - 5.1 Quản trị Hình thức, Kiểm định Tự động & 21 Validation Gates
   - 5.2 Hợp đồng Dữ liệu JSON Schema (Draft 2020-12) vs Free-form Markdown
   - 5.3 Phân định Trách nhiệm Role & Skill Ownership vs Flat Developer Persona
   - 5.4 Cân bằng Chiến lược: Formal Rigor vs Developer Ergonomics
6. [Phân Tích Đối Chiếu Với Hệ Thống `lotte-dms-agent` (v2.15.0 / A2A v3.1.0)](#6-phân-tích-đối-chiếu-với-hệ-thống-lotte-dms-agent-v2150--a2a-v310)
   - 6.1 Đặc thù Miền Nghiệp vụ Bán lẻ / Kho vận Quy mô 20M+ Đơn hàng
   - 6.2 Cổng Kiểm soát 9 Chiều (9-Dimension Review Gate) & Socratic Cognitive Guardrails
   - 6.3 Kiểm soát Cơ sở Dữ liệu Quy mô Khủng: Zero-Downtime DDL (`gh-ost`), Outbox & Financial Invariants
   - 6.4 Policy-as-Code Hooks (`check-policy.py`, SARIF/OCSF) vs Client-side Claude Hooks
7. [Đánh Giá Ưu Điểm, Nhược Điểm và Anti-Patterns Cần Né Tránh](#7-đánh-giá-ưu-điểm-nhược-điểm-và-anti-patterns-cần-né-tránh)
   - 7.1 Điểm Mạnh Vượt Trội Đáng Tiếp Thu
   - 7.2 Lỗ Hổng Kiến Trúc, Anti-Patterns & Rủi Ro Vận Hành Thực Tế
8. [Đề Xuất Giải Pháp Áp Dụng Cụ Thể Cho `agent-skills`](#8-đề-xuất-giải-pháp-áp-dụng-cụ-thể-cho-agent-skills)
   - 8.1 Surface 1: Bổ sung Heuristics vào Core Skills Hiện hành
   - 8.2 Surface 2: Phát triển Core Skills Mới (`design-deep-modules`, `scaffold-hitl-wizard`, `socratic-design-interview`)
   - 8.3 Surface 3: Xây dựng Gói Chuyên Biệt `packs/typescript-craft-team` & `overlays/typescript-craft`
   - 8.4 Quy trình Chuẩn Hóa Chuyển Đổi 6 Bước (Adaptation Pipeline)
9. [Đề Xuất Giải Pháp Áp Dụng Cụ Thể Cho `lotte-dms-agent`](#9-đề-xuất-giải-pháp-áp-dụng-cụ-thể-cho-lotte-dms-agent)
   - 9.1 Tích hợp Kỷ luật Debugging Loop First & Falsifiable Hypotheses vào `workflows/debug.md`
   - 9.2 Chuẩn hóa Từ vựng Deep Module cho Kiến trúc sư (`ta.md`) và Tech Lead (`tech-lead.md`)
   - 9.3 Ứng dụng Kỹ thuật Socratic Grilling cho Phân tích Nghiệp vụ (`ba.md`, `pm.md`)
   - 9.4 Danh mục Các Pattern Bắt buộc Từ Chối (Rejected Patterns)
10. [Lộ Trình Triển Khai Chi Tiết (Implementation Roadmap)](#10-lộ-trình-triển-khai-chi-tiết)
    - 10.1 Kế hoạch Phân kỳ 4 Giai đoạn (Phases 1 - 4)
    - 10.2 Tiêu chí Nghiệm thu (DoD), Gate Validation & Kế hoạch Rollback
11. [Hướng Dẫn Tái Hiện & Kiểm Chứng Độc Lập (Verification & Audit Commands)](#11-hướng-dẫn-tái-hiện--kiểm-chứng-độc-lập)

---

## 1. EXECUTIVE SUMMARY

### 1.1 Bối Cảnh Cuộc Cách Mạng Kỹ Sư Tác Nhân (2025 – 2027)
Giai đoạn 2025–2027 đánh dấu sự chuyển dịch căn bản từ kỷ nguyên *AI Coding Assistant* (hỗ trợ gợi ý code dòng đơn lẻ, tab completion) sang kỷ nguyên **Autonomous Engineering Agents** (tác nhân kỹ thuật tự chủ, có khả năng tiếp nhận yêu cầu cấp cao, lập kế hoạch kiến trúc, phân rã công việc, viết mã, kiểm thử và rà soát chất lượng độc lập). Tuy nhiên, một vấn đề trầm trọng nhanh chóng bộc lộ trong cộng đồng phát triển phần mềm toàn cầu: hiện tượng **"Vibe Coding"** — tình trạng lập trình phụ thuộc vào cảm tính, thiếu kiểm chứng thực nghiệm, tạo ra mã nguồn bề ngoài có vẻ hoạt động nhưng bên trong tích tụ nợ kỹ thuật khổng lồ, phá vỡ cấu trúc mô-đun và suy thoái tính chịu lỗi khi mở rộng quy mô.

Trước thực trạng đó, các phương pháp luận và kiến trúc kỹ thuật tác nhân phân hóa thành hai trường phái rõ nét:
1. **Trường phái Formal Governance & Multi-Agent Orchestration (Hành chính Hình thức & Đa Tác nhân Có Cổng Kiểm soát)**: Đại diện tiêu biểu là `agent-skills` (v5.9.0) và `lotte-dms-agent` (v2.15.0). Mô hình này tập trung vào tính tiền định (determinism), hợp đồng giao tiếp máy đọc được (JSON Schemas Draft 2020-12), phân định vai trò nghiêm ngặt (39 roles, 19 roles), quản lý ranh giới quyền hạn (Policy-as-Code, OWASP ASI01-10, AST01-10, Lethal Trifecta Scanner) và kiểm thử hồi quy tự động ở cấp độ nền tảng (21 validation gates).
2. **Trường phái Craftsmanship & Developer Ergonomics (Kỷ luật Kỹ thuật Thủ công & Công thái học Lập trình)**: Tiêu biểu nhất trong hệ sinh thái Claude Code và OpenAI Codex hiện nay là kho lưu trữ `https://github.com/mattpocock/skills` của Matt Pocock (nhà sáng lập Total TypeScript). Triết lý của Matt Pocock bác bỏ các framework quản lý tác nhân cồng kềnh ("GSD, BMAD, Spec-Kit...") vốn cố chiếm quyền kiểm soát quy trình và che giấu lỗi; thay vào đó, ông cung cấp một tập hợp các kỹ năng nhỏ, sắc bén, độc lập, tập trung vào việc áp dụng các nguyên lý kỹ thuật phần mềm cốt lõi (Ousterhout Deep Modules, Seam-Based TDD, Hypotheses-Driven Debugging, Task-Graph Concurrency) vào tương tác với mô hình ngôn ngữ lớn (LLM).

### 1.2 Mục Tiêu Chiến Lược Của Nghiên Cứu
Nghiên cứu này được tiến hành nhằm thực hiện một cuộc phẫu thuật giải phẫu kỹ thuật (technical dissection) toàn diện trên kho lưu trữ `mattpocock/skills` (phiên bản v1.3.2, commit `5863806`). Mục tiêu chiến lược bao gồm:
1. **Lập danh mục toàn diện và tường minh (Exhaustive Indexing)**: Phân loại, giải mã cơ chế hoạt động, công cụ sử dụng và đầu ra của toàn bộ 39 kỹ năng hiện có trong `mattpocock/skills`.
2. **Khai thác tinh hoa nhận thức và phương pháp luận (Pattern Extraction)**: Trích xuất các khuôn mẫu nhận thức vượt trội (mental models) như kỹ thuật gọt dũa giả thuyết trong gỡ lỗi, kiểm thử theo seam, thiết kế mô-đun sâu, phỏng vấn Socrate gắt gao (grilling) và báo cáo chẩn đoán trực quan độc lập.
3. **Phân tích đối chiếu đa chiều (Comparative Analysis)**: So sánh khách quan giữa `mattpocock/skills`, `agent-skills` và `lotte-dms-agent` trên các trục: Quản trị hình thức, Hợp đồng dữ liệu, Bảo mật tác nhân, và Công thái học lập trình.
4. **Xây dựng đề xuất tích hợp thực dụng (Actionable Adoption Roadmap)**: Đề xuất giải pháp bổ sung các heuristics hay vào `agent-skills` và `lotte-dms-agent`, đồng thời thiết lập rào chắn ngăn ngừa các anti-patterns (lỗi cú pháp YAML, mã nguồn rác tại `/tmp`, thiếu hợp đồng kiểm soát). Toàn bộ quá trình nghiên cứu tuân thủ nghiêm ngặt nguyên tắc **bảo toàn tuyệt đối mã nguồn** (không can thiệp, không commit, không push).

### 1.3 Bảng So Sánh Chỉ Số Cốt Lõi Của 3 Hệ Thống

| Tiêu Chí So Sánh | `mattpocock/skills` (v1.3.2) | `agent-skills` (v5.9.0) | `lotte-dms-agent` (v2.15.0) |
| :--- | :--- | :--- | :--- |
| **Bản chất Kiến trúc** | Prompt-driven skills pack cho cá nhân kỹ sư | Enterprise Autonomous Agent Operating System | Domain-specific Multi-Agent Logistics Engine |
| **Quy mô Danh mục** | 39 kỹ năng (4 buckets) + 1 archived | 184 kỹ năng (170 core + 14 overlays) | 35 kỹ năng (chuyên biệt hóa cho 15 microservices) |
| **Phân định Vai trò (Roles)** | Không có role (Flat persona "Developer") | 39 roles (18 sections, 12-24 locks/role) | 19 roles (Standards-2027, 19 locks/role) |
| **Hợp đồng Dữ liệu (Schemas)** | Không có (Free-form Markdown text) | 63 JSON Schemas (Draft 2020-12) | 65 JSON Schemas (Draft 2020-12/Draft-07) |
| **Cổng Kiểm định Tự động** | 0 gates (Chỉ dùng `@changesets/cli`) | 21 validation gates (`validate-all.py`, 946 pytest) | 4 native gates (`validate-all.py`, 129 passed pytest) |
| **Bảo mật Tác nhân (Security)** | Redaction nhắc nhở bằng văn bản | AST Security Scanner, OWASP ASI/AST, Lethal Trifecta | Policy-as-Code (`check-policy.py`), SARIF/OCSF, 19 Locks |
| **Phương Thức Thực Thi** | Interactive Claude Code / Codex | Dual: Tương tác người dùng & Graph A2A tự trị | Tương tác & Pipeline CI/CD, Docker-First |
| **Điểm Mạnh Vượt Trội** | Công thái học xuất sắc, triết lý phần mềm sâu | Quản trị chuẩn mực, an toàn tuyệt đối, mở rộng cao | Chuyên sâu logistics, 20M+ scale, Zero-Downtime DDL |
| **Rủi Ro / Hạn Chế** | Thiếu test, dễ lỗi cú pháp (YAML bug), unguided | Chi phí thủ tục lớn (Formal Tax), dốc học tập cao | Bị trói chặt vào domain bán lẻ/kho vận DMS |

---

## 2. TỔNG QUAN KHO LƯU TRỮ MATTPOCOCK/SKILLS

### 2.1 Xuất Xứ, Tác Giả & Định Vị Triết Lý
Kho lưu trữ `mattpocock/skills` được tạo lập và duy trì bởi Matt Pocock — một trong những chuyên gia hàng đầu thế giới về TypeScript, tác giả của nền tảng đào tạo *Total TypeScript* và chuyên gia tư vấn kỹ thuật phần mềm cao cấp. 

Khác với các kho lưu trữ tổng hợp kỹ năng mang tính chắp vá, `mattpocock/skills` được định hình như một bộ công cụ "chiến đấu hàng ngày" phục vụ kỹ sư phần mềm thực thụ. Tuyên ngôn của dự án được ghi nhận nguyên văn tại `README.md:15-19`:
> *"My agent skills that I use every day to do real engineering - not vibe coding. Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve. These skills are designed to be small, easy to adapt, and composable."*

Kho lưu trữ tập trung xử lý dứt điểm 4 thất bại kinh điển trong tương tác giữa lập trình viên và AI:
1. **Lệch pha nhận thức (Misalignment)**: Tác nhân không làm đúng ý con người $\rightarrow$ Giải quyết bằng kỹ thuật phỏng vấn đào sâu không ngừng (`grilling`).
2. **Bội thực thuật ngữ rườm rà (Jargon Disconnect)**: Tác nhân lan man, dùng sai khái niệm miền nghiệp vụ $\rightarrow$ Giải quyết bằng ngôn ngữ chung (Ubiquitous Language) qua `domain-modeling` và `GLOSSARY.md`.
3. **Mã nguồn vỡ vụn (Broken Implementations)**: Mã sinh ra không chạy được hoặc lỗi tiềm ẩn $\rightarrow$ Giải quyết bằng vòng lặp phản hồi siêu chặt (`diagnosing-bugs`) và TDD theo seam (`tdd`).
4. **Suy thoái cấu trúc (Architectural Degradation)**: Ứng dụng biến thành đống bùn lầy (Big Ball of Mud) $\rightarrow$ Giải quyết bằng nguyên lý mô-đun sâu (`codebase-design`, `improve-codebase-architecture`, `setup-ts-deep-modules`).

### 2.2 Cấu Trúc Cây Thư Mục & Phân Vùng 4 Buckets
Tại phiên bản khảo sát v1.3.2, toàn bộ 39 kỹ năng được tổ chức vật lý thành 4 phân vùng (buckets) tại thư mục `skills/`:

```
mattpocock-skills/
├── .agents/                          # Kiến trúc quyết định (ADR) và quy tắc nội bộ
│   ├── adr/
│   │   ├── 0001-explicit-setup-pointer-only-for-hard-dependencies.md
│   │   └── 0002-ship-as-a-claude-code-plugin.md
│   ├── install-block.md             # Tài liệu phân phối chuẩn tắc
│   ├── invocation.md                # Đặc tả mô hình kích hoạt (User vs Model)
│   └── writing-docs.md              # Quy chuẩn viết docs hướng dẫn
├── .changeset/                       # Hệ thống quản lý phiên bản Changesets
├── .claude-plugin/                   # Plugin manifest cho Claude Code
│   ├── marketplace.json
│   └── plugin.json                  # Định nghĩa 27 kỹ năng chính thức (Promoted)
├── .out-of-scope/                    # Cơ sở tri thức lưu trữ các yêu cầu bị từ chối vĩnh viễn
│   ├── frozen-misc-skills.md
│   ├── harness-name-collisions.md
│   ├── lazy-load-writing-for-agents.md
│   ├── mainstream-issue-trackers-only.md
│   ├── native-question-tool.md
│   ├── new-skills.md
│   ├── question-limits.md
│   ├── setup-skill-verify-mode.md
│   └── subagent-recursion.md
├── docs/                             # Tài liệu người dùng hướng dẫn sử dụng
│   ├── engineering/                 # 20 tài liệu kỹ thuật + 1 tài liệu lưu trữ
│   └── productivity/                # 7 tài liệu năng suất
├── skills/                           # Thư mục chứa 39 kỹ năng thực thi
│   ├── engineering/                 # 20 kỹ năng kỹ thuật cốt lõi (Promoted)
│   ├── productivity/                # 7 kỹ năng năng suất & tư duy (Promoted)
│   ├── in-progress/                 # 8 kỹ năng thử nghiệm / beta (Unpromoted)
│   ├── misc/                        # 4 kỹ năng tiện ích đóng băng (Frozen)
│   └── deprecated/                  # Phân vùng rỗng (xóa hoàn toàn khi bỏ)
├── CLAUDE.md / AGENTS.md             # File điều hướng trung tâm (Steering File)
├── GLOSSARY.md                      # Bảng từ điển thuật ngữ toàn cục của repo
├── package.json                     # Quản lý phát hành npm v1.3.2
└── SCOPE.md                         # Tiêu chí nghiêm ngặt lọc issue và pull request
```

Đặc điểm phân bổ 4 phân vùng:
- **`skills/engineering/` (20 skills)**: Bao quát toàn bộ vòng đời phát triển phần mềm: từ tiếp nhận spec, rã ticket, TDD, thiết kế mô-đun sâu, review mã 2 trục, tạo PR, đến cải tiến cấu trúc và hồi tưởng (retro). Tất cả 20 skills này đều được đưa vào Claude Code Plugin chính thức (`plugin.json`).
- **`skills/productivity/` (7 skills)**: Các mẫu tư duy tổng quát: phỏng vấn đào sâu (`grilling`), bàn giao ngữ cảnh (`handoff`), sư phạm nhận thức (`teach`), điều tra câu hỏi và cẩm nang viết tài liệu cho AI (`writing-for-agents`). Cả 7 skills đều nằm trong Plugin chính thức.
- **`skills/in-progress/` (8 skills)**: Các kỹ năng đang trong giai đoạn ấp ủ (Chief of Staff điều phối, Software Factory ontology, pipeline viết bài explore-exploit, kiểm tra deep modules). Các kỹ năng này **không** được đưa vào `plugin.json` để tránh gây nhiễu cho người dùng cuối.
- **`skills/misc/` (4 skills)**: Các script tiện ích đặc thù, đã bị đóng băng phát triển (Git guardrails hook, thiết lập pre-commit Husky, bài tập mẫu TypeScript, chuyển đổi shoehorn test). Không nằm trong plugin.
- *(Lưu trữ đặc biệt)*: Kỹ năng `resolving-merge-conflicts` đã chính thức bị gỡ bỏ từ phiên bản v1.3.0 và chuyển thành tài liệu lưu trữ tại `docs/engineering/resolving-merge-conflicts.md` do tính năng native của các tác nhân hiện đại đã xử lý tốt conflict cơ bản.

### 2.3 Mô Hình Phân Phối Đa Nền Tảng & Cơ Chế Đồng Bộ Harness
Kho lưu trữ của Matt Pocock thiết lập một kiến trúc phân phối linh hoạt, hỗ trợ 5 môi trường tác nhân phổ biến nhất hiện nay:
1. **Claude Code Plugin**: Kênh phân phối hạng nhất (First-class citizen). Cài đặt qua lệnh:
   ```bash
   claude plugin install mattpocock-skills@claude-plugins-official
   ```
   Plugin tự động cập nhật phiên bản mới nhất, quản lý qua `.claude-plugin/plugin.json` và đồng bộ phiên bản từ `package.json` bằng script `scripts/sync-plugin-version.mjs`.
2. **OpenAI Codex Marketplace**: Tích hợp thông qua marketplace registry:
   ```bash
   codex plugin marketplace add mattpocock/skills && codex plugin add mattpocock-skills@mattpocock
   ```
3. **GitHub Copilot CLI & VS Code**: Đăng ký qua cấu hình `~/.copilot/settings.json`.
4. **Google Gemini CLI**: Hỗ trợ cài đặt trực tiếp theo đường dẫn bucket:
   ```bash
   gemini skills install https://github.com/mattpocock/skills.git --path skills/engineering
   ```
5. **Universal Fallback Runner**: Cài đặt thông qua npx:
   ```bash
   npx skills@latest add mattpocock/skills -a <agent-name>
   ```

**Cơ chế Harness Parity (`SKILL.md` song hành `agents/openai.yaml`)**:  
Theo quyết định kiến trúc tại `.agents/invocation.md`, mỗi kỹ năng được thiết kế để hoạt động song song trên cả Claude Code lẫn OpenAI Codex. Mỗi thư mục kỹ năng chứa một file `SKILL.md` và một file bổ trợ `agents/openai.yaml`. Tuy nhiên, như sẽ được chỉ ra trong phần đánh giá nhược điểm, cơ chế này gặp lỗi không đồng nhất tại kỹ năng `software-factory` do thiếu vắng kiểm thử tự động.

### 2.4 Mô Hình Kích Hoạt Lưỡng Tính (User vs Model Invocation)
Matt Pocock thiết lập sự phân biệt dứt khoát giữa hai chế độ kích hoạt tác nhân:
- **Kỹ năng do Người dùng kích hoạt (User-Invoked Skills - 23 skills)**:
  - Khai báo frontmatter: `disable-model-invocation: true` trong `SKILL.md` và `policy.allow_implicit_invocation: false` trong `openai.yaml`.
  - Mục đích: Dành cho các tác vụ lớn, mang tính chỉ đạo chiến lược hoặc thay đổi trạng thái repo mà người dùng muốn toàn quyền kiểm soát thời điểm chạy (ví dụ: `/implement-spec`, `/to-spec`, `/triage`, `/improve-codebase-architecture`, `/wayfinder`, `/handoff`).
  - Đặc điểm prompt: Phần mô tả (`description`) được viết hướng tới người dùng ngắn gọn; mô hình AI **không được phép** tự ý kích hoạt kỹ năng này ngầm định, và các kỹ năng khác cũng không thể gọi nó qua công cụ.
- **Kỹ năng do Mô hình kích hoạt (Model-Invoked / Autonomous Skills - 16 skills)**:
  - Khai báo: Mặc định bỏ qua thuộc tính `disable-model-invocation`.
  - Mục đích: Dành cho các kỹ thuật chuyên môn sâu mà tác nhân cần tự động viện dẫn khi gặp tình huống tương ứng trong quá trình làm việc (ví dụ: tự động áp dụng `diagnosing-bugs` khi người dùng kêu lỗi, tự động dùng `tdd` khi viết code, tự động kích hoạt `codebase-design` khi thiết kế interface, tự dùng `writing-for-agents` khi soạn docs).
  - Đặc điểm prompt: Phần mô tả chứa các từ khóa kích hoạt mạnh mẽ (*"Use when the user says 'diagnose'...", "Use when designing module interfaces..."*).

**Kỹ thuật liên kết kỹ năng qua `Skill` tool**:  
Các kỹ năng trong kho lưu trữ không bao giờ dùng đường dẫn file tương đối kiểu `../other-skill/SKILL.md` để gọi nhau trong chỉ dẫn vận hành. Thay vào đó, chúng ra lệnh cho mô hình sử dụng công cụ chuẩn:
```markdown
Call the Skill tool with "grilling"
Call the Skill tool twice, for "grilling" and "domain-modeling"
```
Quy ước này giúp các kỹ năng hoàn toàn trung lập với harness (không bị phụ thuộc vào ký tự gạch chéo `/` của Claude hay cú pháp gọi hàm của Codex/Gemini). Nhờ đó, kỹ năng `grill-with-docs` chỉ cần đúng 7 dòng prompt để kết hợp hoàn hảo hai kỹ năng phức tạp là `grilling` và `domain-modeling`.

---

## 3. DANH MỤC TOÀN DIỆN 39 KỸ NĂNG (COMPREHENSIVE MASTER INDEX)

### 3.1 Bảng Chỉ Mục Tổng Thể (Master Index Table)
Dưới đây là bảng danh mục giải phẫu toàn diện 39 kỹ năng đang hoạt động trong `mattpocock/skills` v1.3.2 (kèm 1 kỹ năng lưu trữ):

| # | Ký Hiệu Kỹ Năng (Identifier) | Phân Vùng (Bucket) | Chế Độ (Mode) | Dòng | Công Cụ & Môi Trường | Mục Đích Chính & Phạm Vi Nghiệp Vụ | Dữ Liệu Đầu Vào (Inputs) | Sản Phẩm Đầu Ra (Outputs) | Đặc Trưng Prompt & Heuristics | Tập Tin Phụ Trợ (Auxiliary) |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | `ask-matt` | `engineering` | **User** | 97 | Markdown viewer | Điều hướng trung tâm toàn bộ kho kỹ năng; hướng dẫn lộ trình làm việc, điểm bắt đầu và phân định ranh giới pha. | Yêu cầu tổng quan từ kỹ sư | Lộ trình kỹ năng đề xuất | Mapping 3 luồng chính, on-ramps, health checks | `PHASE-BOUNDARIES.md` |
| 02 | `code-review` | `engineering` | **Model** | 89 | `git` | Rà soát mã nguồn 2 trục độc lập (Standards vs Spec) bằng 2 subagent chạy song song, tránh ô nhiễm ngữ cảnh. | Fixed point (`HEAD~1`, commit, branch), Spec nguồn | Báo cáo review 2 cột độc lập (mỗi trục $\le 400$ từ) | Bộ 12 Fowler Code Smells, phân biệt hard breach vs judgement call | Không |
| 03 | `codebase-design` | `engineering` | **Model** | 114 | None | Bộ từ vựng và nguyên lý thiết kế mô-đun sâu (Ousterhout): module, interface, depth, seam, adapter, leverage, locality. | Ý định thiết kế mã nguồn | Đặc tả interface mô-đun sâu & kế hoạch tái cấu trúc | The Deletion Test, Interface là Test surface, 1 adapter = giả định, 2 adapters = seam thật | `DEEPENING.md`, `DESIGN-IT-TWICE.md` |
| 04 | `diagnosing-bugs` | `engineering` | **Model** | 138 | `git`, `bash`, `curl` | Quy trình chẩn đoán lỗi 6 giai đoạn nghiêm ngặt: tạo feedback loop đỏ, tái hiện & cô lập tối thiểu, lập giả thuyết, gắn log có tag, sửa và dọn dẹp. | Báo cáo lỗi, triệu chứng vỡ hạt | Lệnh test đỏ chặt chẽ, bản tái hiện tối thiểu, regression test | "This is the skill", xếp hạng 10 loại feedback loop, 3-5 falsifiable hypotheses, tag `[DEBUG-...]` | `scripts/hitl-loop.template.sh` |
| 05 | `domain-modeling` | `engineering` | **Model** | 74 | Markdown editor | Thiết lập ngôn ngữ chung (Ubiquitous Language), chất vấn khái niệm mập mờ, duy trì `GLOSSARY.md` và ADR siêu tinh gọn. | Khái niệm miền nghiệp vụ | File `GLOSSARY.md` cập nhật, bản ghi ADR trong `docs/adr/` | Quy tắc 3 điều kiện tạo ADR, từ chối từ đồng nghĩa, `GLOSSARY-MAP.md` cho monorepo | `GLOSSARY-FORMAT.md`, `ADR-FORMAT.md` |
| 06 | `grill-with-docs` | `engineering` | **User** | 7 | Skill tool | Kỹ năng kết hợp (composite): gọi đồng thời `grilling` và `domain-modeling` để vừa làm sắc nét kế hoạch vừa cập nhật từ điển domain. | Kế hoạch hoặc spec thô | Kế hoạch đã thẩm định + `GLOSSARY.md` & ADRs | Tái sử dụng qua `Skill` tool, chỉ 7 dòng prompt | Không |
| 07 | `implement-spec` | `engineering` | **User** | 42 | `git worktree`, subagents | Điều phối thực thi toàn bộ spec trên nhánh tích hợp (integration branch) sử dụng đồ thị tác vụ (DAG) và subagent chạy song song trên worktree riêng. | Spec và danh sách tickets | Các commit tích hợp, tickets được đóng, draft PR sẵn sàng | Task graph frontier, exploration agent lưu file ngoài repo, merger agent gom code | Không |
| 08 | `implement` | `engineering` | **User** | 17 | `git`, test runner | Thực thi một vertical slice đơn lẻ theo quy trình TDD tại seam đã thống nhất, kết thúc bằng rà soát mã nguồn. | 1 ticket hoặc lát cắt spec | Commit mã nguồn hoàn chỉnh, test xanh, đã qua review | Lát cắt dọc tracer bullet, cấm horizontal slicing | Không |
| 09 | `improve-codebase-architecture` | `engineering` | **User** | 71 | `git`, Tailwind/Mermaid | Quét toàn bộ codebase tìm cơ hội làm sâu mô-đun, xuất báo cáo chẩn đoán HTML tương tác độc lập trong `/tmp`, sau đó phỏng vấn đào sâu ứng viên được chọn. | Cây thư mục dự án | File HTML chẩn đoán tự chứa (`<tmpdir>/architecture-review-*.html`) | CDN Tailwind/Mermaid, biểu đồ trực quan before/after, badge màu đánh giá độ ưu tiên | `HTML-REPORT.md` |
| 10 | `pr` | `engineering` | **Model** | 170 | `git` | Định dạng nội dung Pull Request chuẩn tắc: tóm tắt trực quan ngắn gọn, bằng chứng before/after, cảnh báo rủi ro 1-way door vs 2-way door. | Diff git và lịch sử commit | Mô tả PR hoàn chỉnh, sắc nét | Cấu trúc visual summary, phân định cửa 1 chiều vs 2 chiều, ghi nhận đóng góp | `CREDITS.md` |
| 11 | `prototype` | `engineering` | **Model** | 26 | Browser, dev server | Xây dựng mã thử nghiệm vứt đi (throwaway) để trả lời câu hỏi thiết kế: logic thuần túy (1 file HTML) hoặc UI (route đa biến thể toggle). | Câu hỏi thiết kế cần giải đáp | File demo HTML độc lập hoặc route thử nghiệm tạm thời | Throwaway code, tách biệt logic và UI, gắn cờ thử nghiệm | `UI.md`, `LOGIC.md` |
| 12 | `research` | `engineering` | **Model** | 12 | Web/file tools, subagent | Điều tra câu hỏi kỹ thuật chuyên sâu bằng cách cử subagent chạy ngầm tra cứu nguồn dữ liệu gốc có độ tin cậy cao. | Câu hỏi kỹ thuật | File Markdown đúc kết kết quả nghiên cứu kèm trích dẫn | Fresh context window cho subagent, trích dẫn tài liệu gốc | Không |
| 13 | `retro` | `engineering` | **User** | 44 | CI/Linter inspector | Tổ chức phiên hồi tưởng (retrospective) sau phiên làm việc nhằm tìm cách cải thiện môi trường tác nhân (linter, script, docs). | Lịch sử phiên làm việc | Danh sách đề xuất cải tiến môi trường phát triển được xếp hạng | Tập trung vào cải tiến tooling, CI, conventions thay vì đổ lỗi cho AI | Không |
| 14 | `setup-matt-pocock-skills` | `engineering` | **User** | 120 | `git`, `gh`, `glab` | Thiết lập cấu hình lần đầu cho dự án: chọn trình quản lý issue (GitHub/GitLab/Local), nhãn triage, cấu trúc docs; cập nhật `CLAUDE.md`. | Lựa chọn môi trường của repo | Bộ tài liệu điều hướng trong `docs/agents/` | Thiết lập tracker backend, triage labels, cấu trúc domain docs | `issue-tracker-github.md`, `issue-tracker-gitlab.md`, `issue-tracker-local.md`, `triage-labels.md`, `domain.md` |
| 15 | `tdd` | `engineering` | **Model** | 38 | Test runner (`vitest`, `jest`, `pytest`) | Vòng lặp Red-Green-Refactor tập trung tại seam của interface công khai; nghiêm cấm test trùng lặp (tautological) và móc nối implementation. | Yêu cầu hành vi mới | Test đỏ $\rightarrow$ Code xanh $\rightarrow$ Mã tái cấu trúc | Cấm sửa test khi refactor, test interface thay vì private, cấm mock quá sâu | `mocking.md`, `tests.md` |
| 16 | `to-spec` | `engineering` | **User** | 75 | Issue tracker CLI | Tổng hợp cuộc trò chuyện thành bản đặc tả kỹ thuật hoàn chỉnh: user stories, quyết định, testing seams, ranh giới ngoài phạm vi. | Lịch sử thảo luận | Issue đặc tả kỹ thuật gắn nhãn `ready-for-agent` | Không phỏng vấn lại, tổng hợp trực tiếp, định nghĩa rõ out-of-scope | Không |
| 17 | `to-tickets` | `engineering` | **User** | 105 | Issue tracker CLI | Phân rã đặc tả kỹ thuật thành các ticket dạng lát cắt dọc tracer-bullet; thiết lập cạnh chặn phụ thuộc (DAG); hỗ trợ kỹ thuật expand-contract. | Bản đặc tả kỹ thuật | Tập hợp issue tickets có liên kết phụ thuộc `Blocked by` | Tracer bullets, expand-contract cho refactoring diện rộng, sizing vừa 1 context | Không |
| 18 | `triage` | `engineering` | **User** | 112 | Issue tracker CLI | Máy trạng thái phân loại issues và external PRs thành 2 nhóm và 5 trạng thái; sinh brief cho agent hoặc chuyển vào `.out-of-scope/`. | Issues / PRs mới | Cập nhật nhãn, comment agent brief, hoặc bản ghi từ chối trong `.out-of-scope/` | State machine rõ ràng, tạo agent brief cô đọng, dứt khoát đẩy việc không hợp lệ vào out-of-scope | `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md` |
| 19 | `wayfinder` | `engineering` | **User** | 128 | Issue tracker CLI | Lập bản đồ cho các dự án khổng lồ, mù sương (foggy) kéo dài nhiều phiên; quản lý bản đồ quyết định (`wayfinder:map`) và gỡ sương mù từng bước. | Dự án phức tạp, mơ hồ | Issue bản đồ `wayfinder:map` + các ticket quyết định con | Khái niệm "Fog of War", chỉ số Decisions-so-far, chuyển sương mù thành ticket cụ thể | Không |
| 20 | `wizard` | `engineering` | **Model** | 44 | `bash`, `gh`, `.env` | Tự động tạo script bash tương tác từng bước cho các thủ tục thủ công bắt buộc con người can thiệp (lấy API key, cấp quyền OAuth, cutover DB). | Thủ tục thủ công cần thực hiện | Script bash tương tác thực thi được dựa trên `template.sh` | Phân đoạn stage rõ ràng, tự lưu `.env`, đẩy secret lên `gh secret`, hỗ trợ Ctrl-C tiếp tục lại | `template.sh` |
| 21 | `chief-of-staff` | `in-progress` | **User** | 75 | Subagents, background | Đóng vai trò Trưởng ban Điều phối (DRI) theo đuổi các mục tiêu dài hạn; điều phối subagents và duy trì trang wiki lịch sử liên kết. | Mục tiêu chiến lược dự án | Bộ tài liệu wiki lịch sử (`index.md`, các tuyên bố gắn mã SHA commit) | Vai trò DRI, duy trì wiki lịch sử với git SHA đối chiếu, fresh subagents | Không |
| 22 | `claude-handoff` | `in-progress` | **User** | 18 | `claude --bg` | Ghi tóm tắt bàn giao ngữ cảnh ra file markdown trong `/tmp` và tự động khởi tạo ngay một background agent nạp ngữ cảnh đó. | Ngữ cảnh phiên hiện tại | File handoff tại `$TMPDIR` + background agent được kích hoạt | Tự động hóa tiếp sức không gián đoạn bằng tiến trình nền | Không |
| 23 | `loop-me` | `in-progress` | **User** | 32 | Markdown editor | Phiên phỏng vấn biến các vòng lặp công việc/cuộc sống lặp đi lặp lại thành đặc tả quy trình có thể tự động hóa trong `workflows/*.md`. | Mô tả vòng lặp thường nhật | Bản đặc tả quy trình `workflows/<slug>.md` và `NOTES.md` | Phỏng vấn tìm điểm nghẽn, tự động hóa vòng lặp lặp lại | Không |
| 24 | `setup-ts-deep-modules` | `in-progress` | **User** | 102 | `npm`, `dependency-cruiser` | Cài đặt và cấu hình `dependency-cruiser` trong dự án TypeScript để rào cứng kiến trúc mô-đun sâu (chỉ cho phép import entry point root). | Dự án TypeScript | File cấu hình `.dependency-cruiser.cjs` & script `check:deps` | Rào chặn barrel file vô tội vạ, bảo vệ thư mục con private, kiểm thử chỉ gọi interface | `dependency-cruiser.config.cjs` |
| 25 | `software-factory` | `in-progress` | **User** | 98 | CI / git / ticket tools | Hệ thống từ vựng và kiến trúc thiết kế "nhà máy phần mềm tự động bằng AI" (Task, Trigger, Run, Runner, 3 Phanh an toàn). | Nhu cầu tự động hóa quy trình phần mềm | Bản thiết kế kiến trúc nhà máy phần mềm & phân rã tasks | 3 Brakes (kiểm tra tự động, auto-review, phê duyệt con người), runner mapping | `RUNNERS.md`, `EXAMPLE-TASKS.md`, `TICKET-TRACKERS.md`, `OBSERVABILITY-PLATFORMS.md`, `GIT-HOSTS.md` |
| 26 | `writing-beats` | `in-progress` | **User** | 67 | Markdown editor | Giai đoạn Exploit bài viết: ghép các mảnh tư liệu thô thành hành trình từng nhịp nối tiếp, neo chắc khái niệm trước khi sử dụng. | Mảnh tư liệu từ `writing-fragments` | Bài viết nối tiếp các nhịp tư duy (beats) | Chọn lựa hành trình người đọc, làm chỗ dựa vững chắc cho khái niệm mới | Không |
| 27 | `writing-fragments` | `in-progress` | **User** | 79 | Markdown editor | Giai đoạn Explore bài viết: khai thác triệt để suy nghĩ phi cấu trúc, câu đắt giá, hoạt cảnh thực tế và từ khóa dẫn dắt. | Ý tưởng thô, quan sát | File tư liệu thô (`# Working title` + các mẩu vụn) | Không vội tạo cấu trúc, thu thập tối đa mảnh ghép tư duy sắc sảo | Không |
| 28 | `writing-shape` | `in-progress` | **User** | 79 | Markdown editor | Giai đoạn hoàn thiện bài viết: gọt dũa tư liệu thành bài luận hoàn chỉnh từng đoạn văn, biện luận cho cấu trúc lựa chọn. | Bài viết dạng nhịp hoặc tư liệu thô | Bài viết hoàn chỉnh có cấu trúc chặt chẽ | Biện luận định dạng, làm chủ nhịp điệu đọc và hiểu | Không |
| 29 | `git-guardrails-claude-code` | `misc` | **Model** | 95 | `bash`, `jq`, Claude hooks | Hook `PreToolUse` can thiệp chặn đứng các lệnh git nguy hiểm (`push`, `reset --hard`, `clean -fd`, `branch -D`) trước khi Claude chạy. | Lệnh git từ Claude Code | Script hook `.claude/hooks/block-dangerous-git.sh` & cài đặt | Chặn đứng thao tác phá hoại repo tại tầng client, cảnh báo người dùng xác nhận | `scripts/block-dangerous-git.sh` |
| 30 | `migrate-to-shoehorn` | `misc` | **Model** | 118 | `npm` | Chuyển đổi mã kiểm thử TypeScript từ ép kiểu không an toàn `as any` / `as Type` sang fixture an toàn kiểu `@total-typescript/shoehorn`. | File kiểm thử có ép kiểu | Mã kiểm thử sạch mùi ép kiểu, an toàn với `fromPartial()` | Loại bỏ code smell, tạo mock data tối thiểu nhưng an toàn kiểu dữ liệu | Không |
| 31 | `scaffold-exercises` | `misc` | **Model** | 106 | `git`, course CLI | Tự động sinh cấu trúc thư mục bài tập đào tạo (`problem/`, `solution/`, `explainer/`) kèm file hướng dẫn `readme.md` chuẩn linter. | Danh sách bài tập cần tạo | Cấu trúc thư mục bài tập chuẩn hóa vượt qua bộ kiểm tra linter | Phục vụ nền tảng giáo dục lập trình, đồng bộ cấu trúc bài giảng | Không |
| 32 | `setup-pre-commit` | `misc` | **Model** | 91 | `npm`, `husky`, `prettier` | Thiết lập Husky pre-commit hook chạy lint-staged (Prettier), kiểm tra kiểu (`tsc`), và chạy unit test trên các file được staged. | Dự án Node/TypeScript | File cấu hình `.husky/pre-commit`, `.lintstagedrc.json`, `.prettierrc` | Ngăn chặn code bẩn lọt vào git history, kiểm tra nhanh trước khi commit | Không |
| 33 | `grill-me` | `productivity` | **User** | 7 | Skill tool | Phiên phỏng vấn Socratic nhanh, không phụ thuộc repo, đào sâu vào bất kỳ kế hoạch, ý tưởng hoặc tài liệu thiết kế nào. | Kế hoạch, ý tưởng từ người dùng | Cây quyết định được làm sáng tỏ trong cuộc trò chuyện | Triệu hồi lõi `grilling` nhanh chóng chỉ với 7 dòng prompt | Không |
| 34 | `grilling` | `productivity` | **Model** | 30 | None | Lõi phỏng vấn Socratic nền tảng: mô hình hóa quyết định thành cây thiết kế, tính toán ranh giới (frontier), hỏi từng đợt có gợi ý đáp án. | Vấn đề mơ hồ, đa phương án | Cây quyết định được chốt và thống nhất hiểu biết chung | Tính toán frontier quyết định, hỏi có đánh số kèm khuyến nghị, ép subagent tra cứu | Không |
| 35 | `handoff` | `productivity` | **User** | 16 | Markdown editor | Nén toàn bộ ngữ cảnh cuộc trò chuyện thành file bàn giao markdown trong thư mục tạm hệ thống (`$TMPDIR`), dùng con trỏ ngữ cảnh. | Phiên làm việc sắp đầy token | File tài liệu bàn giao tại `$TMPDIR` | Giải phóng ngữ cảnh, chỉ lưu con trỏ trỏ tới tài nguyên thay vì nhồi nhét text | Không |
| 36 | `teach` | `productivity` | **User** | 140 | Browser, Markdown editor | Khung sư phạm tương tác dựa trên khoa học nhận thức: Vùng phát triển gần nhất (ZPD), thực hành gợi nhớ, lưu giữ kiến thức, bài học HTML. | Chủ đề cần học tập | File `MISSION.md`, `RESOURCES.md`, `./learning-records/`, `./lessons/*.html` | ZPD, retrieval practice, storage strength, bài học tương tác HTML | `GLOSSARY-FORMAT.md`, `RESOURCES-FORMAT.md`, `MISSION-FORMAT.md`, `LEARNING-RECORD-FORMAT.md` |
| 37 | `to-questionnaire` | `productivity` | **User** | 54 | Markdown editor | Chuyển đổi các quyết định không thể tự giải quyết trong repo thành bảng câu hỏi khảo sát ngắn gọn gửi cho stakeholder bên ngoài. | Các quyết định bế tắc | File bảng câu hỏi markdown (`to-questionnaire-<slug>.md`) | "Grill the send, not the subject", tối ưu hóa thời gian của chuyên gia bên ngoài | Không |
| 38 | `wait-what` | `productivity` | **User** | 7 | None | Cầu dao ngắt khẩn cấp khi tác nhân nói chuyện khó hiểu: buộc tác nhân diễn giải lại bằng tiếng Anh kỹ thuật đơn giản và từ vựng GLOSSARY. | Lời giải thích lộn xộn của AI | Lời giải thích rõ ràng, giản dị, đúng trọng tâm | Simplified Technical English, bám sát GLOSSARY, xóa bỏ sự hoa mỹ sáo rỗng | Không |
| 39 | `writing-for-agents` | `productivity` | **Model** | 81 | None | Cẩm nang tối thượng về kỹ thuật soạn thảo tài liệu cho tác nhân: con trỏ ngữ cảnh, 2 loại tải, phân cấp thông tin, từ dẫn dắt, tiêu chí hoàn tất. | Tài liệu hoặc prompt cần viết | Tài liệu kỹ thuật, kỹ năng hoặc file chỉ đạo tối ưu cho LLM | The Two Loads (Context vs Cognitive), Progressive Disclosure, Leading Words, Negation Prevention, Demand & Clarity | `SKILL-MECHANICS.md` |
| *(40)* | `resolving-merge-conflicts` *(Archived)* | `engineering` | *(Model)* | *(53)* | `git` | *(Lưu trữ v1.3.0)*: Giải quyết xung đột git merge/rebase dựa trên tài liệu gốc (commit logs, PRs, issues) thay vì máy móc chọn `--ours`/`--theirs`. | Git conflict hiện hữu | Commit merge hoàn tất, vượt qua các kiểm tra tự động | Đọc lịch sử commit gốc để hiểu ý đồ tác giả thay vì đoán mò | Lưu trữ tại `docs/engineering/resolving-merge-conflicts.md` |

### 3.2 Phân Bố Công Cụ & Thống Kê Tần Suất Kích Hoạt
Từ việc phân tích tổng hợp 39 kỹ năng:
- **Tỷ lệ Chế độ Kích hoạt**:
  - **User-Invoked**: 23 skills (chiếm 59.0%). Phản ánh rõ nét triết lý: trao quyền làm chủ tiến trình cho lập trình viên, ngăn chặn AI tự biên tự diễn các bước trọng yếu.
  - **Model-Invoked**: 16 skills (chiếm 41.0%). Tập trung vào các heuristics chuyên sâu và quy chuẩn thực thi khi viết mã, kiểm thử hoặc gỡ lỗi.
- **Phân Bố Công Cụ Phổ Biến**:
  - Công cụ quản lý mã nguồn (`git`, worktree): Xuất hiện trong 14 skills.
  - Trình duyệt và Dev Server: Xuất hiện trong 4 skills (`prototype`, `teach`, `improve-codebase-architecture`).
  - Lệnh Shell & Bash Script: Xuất hiện trong 6 skills (`diagnosing-bugs`, `wizard`, `git-guardrails-claude-code`, v.v.).
  - Trình quản lý Issue CLI (`gh`, `glab`): Xuất hiện trong 5 skills (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `setup-matt-pocock-skills`).
  - Trình phân tích kiểm thử & Linter (`vitest`, `dependency-cruiser`, `husky`): Xuất hiện trong 5 skills.
  - Hoàn toàn không dùng công cụ bên ngoài (Pure Prompt Heuristics): Chiếm 11 skills (như `codebase-design`, `grilling`, `writing-for-agents`, `domain-modeling`).

---

## 4. PHÂN TÍCH CHUYÊN SÂU CÁC PATTERN & KỸ THUẬT NỔI BẬT

### 4.1 Kiến Trúc Deep Modules (Ousterhout), Seams & The Deletion Test
Một trong những đóng góp học thuật và thực tiễn giá trị nhất trong `mattpocock/skills` là việc chuẩn hóa các nguyên lý từ cuốn sách kinh điển *A Philosophy of Software Design* của Giáo sư John Ousterhout (`codebase-design/SKILL.md` và `DEEPENING.md`):

1. **Định nghĩa Mô-đun Sâu (Deep Module) vs Mô-đun Nông (Shallow Module)**:
   - **Mô-đun Sâu**: Sở hữu một giao diện (Interface) cực kỳ nhỏ gọn, đơn giản, nhưng che giấu bên trong một khối lượng hành vi triển khai (Implementation) phức tạp và đồ sộ. Mang lại **đòn bẩy (Leverage)** tối đa cho người gọi (ít thứ phải học nhưng làm được nhiều việc) và tính **cục bộ (Locality)** cho người bảo trì (sửa một chỗ là sửa toàn bộ hệ thống).
   - **Mô-đun Nông**: Giao diện phức tạp gần bằng phần thân triển khai, chủ yếu chỉ làm nhiệm vụ chuyển tiếp (pass-through) hoặc bọc lại sơ sài. Đây là mầm mống gây ô nhiễm ngữ cảnh tác nhân và gia tăng số lượng file cần đọc hiểu.

```
MÔ-ĐUN SÂU (DEEP MODULE)             MÔ-ĐUN NÔNG (SHALLOW MODULE - CẦN TRÁNH)
┌───────────────────────────┐         ┌─────────────────────────────────────────┐
│     Small Interface       │         │             Large Interface             │
│   (Ít hàm, tham số gọn)   │         │       (Nhiều hàm, tham số phức tạp)     │
├───────────────────────────┤         ├─────────────────────────────────────────┤
│                           │         │ Thin Implementation (Chỉ chuyển tiếp)   │
│    Deep Implementation    │         └─────────────────────────────────────────┘
│   (Ẩn giấu logic phức tạp)│
│                           │
└───────────────────────────┘
```

2. **Khái niệm Seam (Michael Feathers) & Adapter**:
   - **Seam**: Vị trí mà tại đó bạn có thể thay đổi hành vi của chương trình mà không cần phải chỉnh sửa trực tiếp mã nguồn tại vị trí đó; đây chính là nơi mà Interface của mô-đun ngự trị.
   - **Adapter**: Đối tượng cụ thể đáp ứng giao diện tại một seam.
   - **Quy tắc Vàng**: *"Một adapter chỉ chứng minh một seam giả định. Phải có từ hai adapters trở lên mới chứng minh được sự tồn tại hợp lý của một seam."* Điều này ngăn chặn triệt để thói quen over-engineering của các AI khi tự ý tạo ra hàng loạt interface trừu tượng rỗng mà chỉ có duy nhất một class triển khai.

3. **Phép Thử Xóa Bỏ (The Deletion Test)**:
   - Một tiêu chí kiểm định kiến trúc sắc bén: Hãy tưởng tượng xóa bỏ mô-đun đó đi. Nếu toàn bộ sự phức tạp biến mất mà không ảnh hưởng gì, mô-đun đó chỉ là một lớp bọc vô dụng (pass-through). Nhưng nếu sự phức tạp đó lập tức vỡ vụn và tái xuất hiện trên $N$ vị trí gọi khác nhau, thì mô-đun đó hoàn toàn xứng đáng tồn tại và đang làm tròn bổn phận bảo vệ hệ thống.

4. **Interface Chính Là Bề Mặt Kiểm Thử (The Interface Is The Test Surface)**:
   - Cả mã gọi nghiệp vụ và mã kiểm thử đều phải đi qua cùng một seam giao diện. Nếu một bài test cố tìm cách chui qua interface để soi mói các biến hoặc hàm private bên trong, đó là dấu hiệu không thể chối cãi rằng mô-đun đang bị thiết kế sai hình thái.

### 4.2 Đánh Giá Mã Nguồn Hai Trục Độc Lập (Two-Axis Code Review)
Trong kỹ năng `code-review`, Matt Pocock giải quyết triệt để vấn đề "thiên kiến rà soát" (review bias) khi một tác nhân cố gắng đánh giá toàn bộ khía cạnh của một pull request trong cùng một cửa sổ ngữ cảnh:

```
                          ┌───────────────────────┐
                          │  Diff & Git Commits   │
                          └───────────┬───────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
   ┌───────────────────────────┐             ┌───────────────────────────┐
   │    Standards Sub-Agent    │             │      Spec Sub-Agent       │
   │  (Fresh Context Window)   │             │  (Fresh Context Window)   │
   │  - Documented repo rules  │             │  - Spec / Issue tickets   │
   │  - 12 Fowler Code Smells  │             │  - Scope creep detection  │
   │  - Output: <= 400 words   │             │  - Output: <= 400 words   │
   └─────────────┬─────────────┘             └─────────────┬─────────────┘
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      ▼
                          ┌───────────────────────┐
                          │ Two-Column Aggregator │
                          │ (Không trộn lẫn điểm) │
                          └───────────────────────┘
```

- **Tách Biệt Hai Trục**:
  1. **Trục Tiêu Chuẩn (Standards Axis)**: Kiểm tra mã nguồn có tuân thủ quy chuẩn dự án (`CONTRIBUTING.md`, `CODING_STANDARDS.md`) và bảng 12 mùi mã nguồn kinh điển của Martin Fowler (*Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest*).
  2. **Trục Đặc Tả (Spec Axis)**: Đối chiếu từng dòng diff với yêu cầu nghiệp vụ gốc trong spec/issue. Phát hiện: thiếu yêu cầu, làm sai yêu cầu, hoặc tự ý thêm tính năng ngoài phạm vi (scope creep).
- **Subagent Độc Lập Tránh Ô Nhiễm Chéo**:
  Cả hai subagent được khởi động song song trên các context window hoàn toàn tươi mới (fresh context). Nhờ đó:
  - Một thay đổi tuân thủ 100% chuẩn coding nhưng làm sai nghiệp vụ sẽ bị bắt ngay tại Spec Axis mà không bị vẻ đẹp của cú pháp che mắt (`Standards PASS, Spec FAIL`).
  - Một thay đổi đáp ứng đúng yêu cầu nghiệp vụ nhưng vi phạm nghiêm trọng kiến trúc sẽ bị bắt tại Standards Axis (`Spec PASS, Standards FAIL`).
  - Báo cáo cuối cùng giữ nguyên hai cột riêng biệt, từ chối việc xếp hạng chung một lỗi duy nhất để tránh làm lu mờ khiếm khuyết.

### 4.3 Vòng Lặp Chẩn Đoán Lỗi 6 Giai Đoạn Kỷ Luật Cao (Disciplined 6-Phase Debugging Loop)
Kỹ năng `diagnosing-bugs` được xây dựng như một pháo đài ngăn chặn thói quen "đoán mò và sửa thử" (trial-and-error vibe coding) của các mô hình AI:

- **Châm Ngôn Cốt Lõi**: *"Phase 1: Build a feedback loop. This is the skill. Everything else is mechanical."* (Xây dựng vòng lặp phản hồi. Đây chính là toàn bộ kỹ năng. Mọi thứ còn lại chỉ là cơ học).
- **Quy Trình 6 Giai Đoạn**:
  1. **Giai đoạn 1: Xây dựng vòng lặp phản hồi chặt chẽ (Build a feedback loop)**:
     - Bắt buộc phải thiết lập được **một câu lệnh duy nhất** (a single command) có khả năng kích hoạt đúng đoạn mã lỗi và **chắc chắn trả về kết quả đỏ (red-capable)**.
     - Xếp hạng ưu tiên 10 loại feedback loop: (1) Unit/Integration test lỗi $\rightarrow$ (2) Curl/HTTP script $\rightarrow$ (3) Lệnh CLI diff stdout với snapshot chuẩn $\rightarrow$ (4) Headless Playwright script $\rightarrow$ (5) Replay trace payload từ đĩa $\rightarrow$ (6) Throwaway harness tối thiểu $\rightarrow$ (7) Fuzz loop 1000 lần $\rightarrow$ (8) Git bisect automation harness $\rightarrow$ (9) Differential loop chạy 2 phiên bản $\rightarrow$ (10) HITL bash script qua template.
     - Tiêu chuẩn hoàn tất (Completion Criterion): Lệnh phải thỏa mãn 4 tiêu chí: **Red-capable** (bắt đúng triệu chứng người dùng), **Deterministic** (tiền định, tỷ lệ tái hiện cao), **Fast** (vài giây, không quá vài phút), **Agent-runnable** (tác nhân tự chạy không cần can thiệp).
     - **Cấm kỵ tuyệt đối**: Nếu tác nhân bắt đầu đọc code để suy đoán giả thuyết khi chưa có lệnh test đỏ, quy trình coi như vi phạm kỷ luật.
  2. **Giai đoạn 2: Tái hiện & Thu nhỏ tối thiểu (Reproduce + minimise)**:
     - Chạy vòng lặp và quan sát trạng thái đỏ thực sự xuất hiện.
     - **Thu nhỏ tối thiểu (Minimise)**: Cắt giảm đầu vào, cấu hình, dữ liệu từng bước một cho đến khi đạt được bản tái hiện nhỏ nhất mà vẫn đỏ. Bản tái hiện tối thiểu này sẽ biến thành bài regression test sạch sẽ tại Giai đoạn 5.
  3. **Giai đoạn 3: Lập 3–5 giả thuyết có thể bác bỏ (Hypothesise)**:
     - Bắt buộc liệt kê **từ 3 đến 5 giả thuyết được xếp hạng** trước khi tiến hành thử nghiệm bất kỳ giả thuyết nào, nhằm tránh hiện tượng "neo nhận thức" (anchoring bias) vào ý tưởng đầu tiên nảy ra.
     - Định dạng chuẩn bắt buộc: `"If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."` (Nếu X là nguyên nhân, thì việc thay đổi Y sẽ làm lỗi biến mất / thay đổi Z sẽ làm lỗi trầm trọng hơn). Nếu không viết được cấu trúc này, giả thuyết chỉ là cảm tính và bị loại bỏ.
  4. **Giai đoạn 4: Gắn thiết bị đo kiểm (Instrument)**:
     - Thử nghiệm từng giả thuyết bằng cách thay đổi duy nhất một biến số tại một thời điểm.
     - Ưu tiên công cụ: Debugger/REPL $\rightarrow$ Log có chủ đích.
     - Quy chuẩn tag: Mọi dòng log chẩn đoán bắt buộc phải mang một tiền tố duy nhất, ví dụ `[DEBUG-a4f2]`. Nhờ đó, việc dọn dẹp ở cuối quy trình chỉ cần một lệnh `grep` là sạch bóng, loại bỏ hoàn toàn nguy cơ rò rỉ log debug lên môi trường production.
  5. **Giai đoạn 5: Sửa lỗi & Viết Regression Test (Fix + regression test)**:
     - Viết bài regression test tại đúng seam trước khi sửa mã nguồn. Nếu không tìm được seam phù hợp, phải ghi nhận sự thiếu hụt kiến trúc này.
     - Áp dụng bản sửa đổi $\rightarrow$ quan sát test chuyển từ đỏ sang xanh $\rightarrow$ chạy lại feedback loop ban đầu trên kịch bản đầy đủ.
  6. **Giai đoạn 6: Dọn dẹp sạch sẽ (Cleanup)**:
     - Xóa bỏ 100% các dòng log mang prefix `[DEBUG-...]`, xóa file tạm và ghi rõ giả thuyết đúng vào commit message.

### 4.4 Lập Trình Hướng Kiểm Thử Theo Seam (Seam-Based TDD & Anti-Tautological Testing)
Kỹ năng `tdd` và tài liệu đi kèm (`tests.md`, `mocking.md`) thiết lập các nguyên tắc phòng ngự nghiêm ngặt chống lại các tệ nạn phổ biến của mã kiểm thử do AI sinh ra:
1. **Chống Kiểm Thử Trùng Lặp Tautological (Anti-Tautological Tests)**:
   - Hiện tượng AI viết test kiểu "lặp lại chính xác logic vừa viết" (ví dụ: mock function A trả về X, gọi B, assert B nhận được X). Bài test này luôn xanh nhưng không mang lại bất kỳ giá trị kiểm chứng thực tế nào.
   - Nguyên tắc: Test phải xác minh sự chuyển đổi trạng thái hoặc kết quả đầu ra quan sát được từ phía người gọi qua giao diện công khai, độc lập hoàn toàn với cách thức triển khai bên trong.
2. **Cấm Sửa Test Khi Tái Cấu Trúc (The Refactoring Invariant)**:
   - Trong chu trình Red-Green-Refactor, giai đoạn Refactor nghiêm cấm chạm vào file test. Nếu việc sửa mã nội bộ bắt buộc phải sửa test, điều đó chứng minh bài test đã bị móc nối chặt chẽ (tightly coupled) vào chi tiết triển khai thay vì gắn vào seam giao diện.
3. **Phát Triển Theo Lát Cắt Dọc Tracer Bullets (Vertical Slicing)**:
   - Thay vì kiểm thử theo lớp ngang (viết toàn bộ schema $\rightarrow$ viết toàn bộ repo $\rightarrow$ viết toàn bộ service), TDD áp dụng lát cắt dọc siêu mỏng xuyên suốt từ đầu vào đến đầu ra, chứng minh tính thông suốt của luồng dữ liệu trước khi mở rộng.

### 4.5 Đa Luồng Concurrency Theo Đồ Thị Tác Vụ & Git Worktree (`implement-spec`)
Kỹ năng `implement-spec` phác thảo một mô hình điều phối đa tác nhân (Swarm Orchestration) ở đẳng cấp cao:
- **Đồ Thị Tác Vụ (DAG) & Ranh Giới (Frontier)**:
  Các ticket được rã từ spec không phải là một danh sách tuần tự tuyến tính mà tạo thành một đồ thị có hướng không chu trình (DAG) với các liên kết phụ thuộc rõ ràng (`Blocked by: #ticket_id`). Tập hợp các ticket không bị chặn bởi bất kỳ ticket nào khác tạo thành **Ranh giới khả thi (Frontier)**.
- **Git Worktree Isolation**:
  Mỗi ticket trong Frontier được phân bổ cho một **Implementer Subagent** riêng biệt. Mỗi subagent làm việc trong một thư mục `git worktree` hoàn toàn độc lập trên một nhánh git riêng, dựa trên nhánh tích hợp (`integration-branch`). Điều này triệt tiêu hoàn toàn nguy cơ tranh chấp file hoặc xung đột lock giữa các tiến trình chạy song song.
- **Tác Nhân Thám Hiểm Lưu Trữ Ngoài Repo (Exploration Agent)**:
  Tác nhân thám hiểm ban đầu thu thập tri thức và lưu trữ các ghi chú markdown ra một thư mục nằm **bên ngoài repository**. Nhờ đó, tất cả các implementer subagents đều có thể đọc được tài liệu này mà không làm bẩn git index hay gây nhiễu ngữ cảnh của nhánh tích hợp.
- **Merger Subagent & Đẩy Ranh Giới**:
  Khi một implementer subagent hoàn tất kiểm thử TDD, một **Merger Subagent** sẽ gộp nhánh đó vào `integration-branch`. Việc gộp thành công sẽ lập tức giải phóng các ticket phụ thuộc tiếp theo, mở rộng Frontier và kích hoạt làn sóng subagents mới chạy ngầm. Kết thúc quy trình, toàn bộ worktree được dọn dẹp sạch sẽ và một phiên `code-review` hai trục được kích hoạt trên toàn bộ nhánh tích hợp.

```
       [Spec] ──> [to-tickets] ──> [Task Graph (DAG)]
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼ (Ticket A - Ready)                  ▼ (Ticket B - Ready)
                 FRONTIER: TICKET A                    FRONTIER: TICKET B
              ┌─────────────────────┐               ┌─────────────────────┐
              │ Implementer Agent 1 │               │ Implementer Agent 2 │
              │ in Git Worktree A   │               │ in Git Worktree B   │
              │ (TDD at seam)       │               │ (TDD at seam)       │
              └──────────┬──────────┘               └──────────┬──────────┘
                         │                                     │
                         ▼                                     ▼
                  [Merger Agent] ──────────────────────> [Merger Agent]
                         │                                     │
                         ▼                                     ▼
            Integration Branch Commit 1           Integration Branch Commit 2
                         │                                     │
                         └──────────────────┬──────────────────┘
                                            ▼ (Ticket C Unblocked!)
                                      FRONTIER ADVANCES
                                     FRONTIER: TICKET C
```

### 4.6 Báo Cáo Chẩn Đoán Kiến Trúc Trực Quan HTML Độc Lập (Tailwind & Mermaid CDN)
Trong kỹ năng `improve-codebase-architecture`, Matt Pocock giới thiệu một mẫu báo cáo trực quan hóa kiến trúc cực kỳ sáng tạo:
- Thay vì xuất ra những file markdown dài dòng khiến lập trình viên ngán ngẩm, tác nhân tự động tổng hợp toàn bộ các cơ hội làm sâu mô-đun (deepening opportunities) thành một file HTML duy nhất đặt tại thư mục tạm của hệ điều hành (`$TMPDIR/architecture-review-*.html`).
- **Tự Chứa & Không Phụ Thuộc Build Tools (Self-contained via CDNs)**:
  File HTML nhúng trực tiếp CDN của **Tailwind CSS** và module **Mermaid.js v11**.
- **Mẫu Thiết Kế Candidate Card Trực Quan**:
  Mỗi ứng viên tái cấu trúc được gói gọn trong một thẻ `<article>` với:
  - Badge độ ưu tiên trực quan (Màu ngọc lục bảo `Strong`, màu hổ phách `Worth exploring`, màu xám đá `Speculative`).
  - Biểu đồ **Before vs After** đặt cạnh nhau bằng Mermaid và các div CSS tùy biến: biểu diễn rõ đường nét đứt (seam), mũi tên đỏ (leakage) và khối sẫm màu (deep module).
  - Định dạng văn bản cực kỳ cô đọng: 1 câu mô tả vấn đề ("What hurts"), 1 câu mô tả giải pháp ("What changes"), và các gạch đầu dòng lợi ích $\le 6$ từ ("Delete 4 shallow wrappers", "Tests hit one interface").
  - Nếu cần một đoạn văn dài để giải thích biểu đồ, quy tắc yêu cầu: *"Vẽ lại biểu đồ, không viết thêm văn bản."*

### 4.7 Tự Động Hóa Thủ Tục Có Người Can Thiệp (Interactive Bash Wizard)
Trong thực tế phát triển phần mềm, luôn tồn tại những bước công việc mà tác nhân AI **không thể và không được phép** tự động thực thi vì lý do bảo mật hoặc hạn chế môi trường (ví dụ: đăng nhập trang quản trị AWS/Stripe để lấy API key bí mật, cấp quyền OAuth qua trình duyệt, gõ mật khẩu root, hoặc bấm nút cutover cơ sở dữ liệu production).

Kỹ năng `wizard` giải quyết bài toán hóc búa này bằng cách sinh ra một script bash tương tác dựa trên mẫu chuẩn `template.sh`:
- **Giao Diện Terminal Thân Thiện & Đẹp Mắt**:
  Sử dụng mã màu ANSI chuẩn, hàm `_clear` làm sạch màn hình sau mỗi bước để người dùng chỉ tập trung vào đúng chỉ dẫn hiện tại.
- **Chia Giai Đoạn Rõ Ràng (Stages)**:
  Hiển thị thanh tiến trình `▸ Stage X/Y · <Tên bước>`, đưa ra chỉ dẫn rõ ràng cho con người ("Mở URL này trên trình duyệt, copy giá trị API secret dán vào đây").
- **Tự Động Lưu Trữ Idempotent & Bảo Vệ Secret**:
  Nhận giá trị người dùng nhập vào, tự động ghi vào `.env` cục bộ hoặc đẩy thẳng lên kho bí mật GitHub qua lệnh `gh secret set <NAME>`, hoàn toàn không để lộ secret trong lịch sử trò chuyện của AI.
- **Hỗ Trợ Ngắt & Tiếp Tục (Resumable via Ctrl-C)**:
  Người dùng có thể bấm `Ctrl-C` bất cứ lúc nào để tạm dừng và chạy lại sau; script tự động kiểm tra các giá trị đã lưu trước đó để bỏ qua các bước đã hoàn tất mà không bắt người dùng nhập lại từ đầu.

### 4.8 Kỷ Luật Soạn Thảo Cho Tác Nhân (`writing-for-agents` & Prompt Mechanics)
Kỹ năng `writing-for-agents` được đúc kết từ hàng ngàn giờ quan sát hành vi của LLM trong thực tế kỹ thuật:

1. **Hai Loại Tải Trọng (The Two Loads)**:
   - **Tải Ngữ Cảnh (Context Load)**: Chi phí token của các tài liệu luôn luôn được nạp sẵn trong cửa sổ ngữ cảnh (như `AGENTS.md`, `CLAUDE.md`, phần mô tả của các kỹ năng). Tải này tiêu tốn token và làm suy giảm sự chú ý (attention) của mô hình ở mọi lượt trò chuyện dù nó có được dùng hay không. Cần cắt gọt tối đa.
   - **Tải Nhận Thức (Cognitive Load)**: Chi phí ghi nhớ của con người về việc tài liệu nào tồn tại và khi nào nên gọi chúng. Đây là cái giá của quyền tự chủ của con người (human agency); chỉ nên chi trả ở nơi mà phán đoán của con người thực sự tạo ra giá trị, và loại bỏ ở những nơi tác nhân có thể tự suy luận.

2. **Tiết Lộ Tịnh Tiến (Progressive Disclosure) & Thang Bậc Thông Tin**:
   - Phân cấp thông tin 3 tầng bậc:
     * *Tầng 1 (In-file Steps)*: Quy trình tuần tự các bước tác nhân phải làm.
     * *Tầng 2 (In-file Reference)*: Các quy tắc bình đẳng được tra cứu khi cần.
     * *Tầng 3 (Disclosed Reference)*: Đẩy toàn bộ chi tiết cồng kềnh ra các file phụ trợ phía sau một **con trỏ ngữ cảnh (context pointer)**.
   - Thử nghiệm rẽ nhánh (The Branching Test): Chỉ giữ lại ở file chính những gì mọi nhánh thực thi đều cần; đẩy ra sau con trỏ những gì chỉ một số nhánh chạm tới.

3. **Từ Khóa Dẫn Dắt (Leading Words)**:
   - Thay vì diễn giải dài dòng một khái niệm qua nhiều câu văn, hãy chọn lựa các từ đơn lẻ giàu năng lượng ngữ nghĩa đã có sẵn trong dữ liệu tiền huấn luyện của mô hình (*tight, red, seam, depth, tracer bullet, relentless, fog of war*).
   - Ví dụ: Thay vì nhắc *"Hãy tạo vòng lặp chạy nhanh, không bị flake, chi phí thấp"*, chỉ cần dùng từ `tight`. Thay vì viết *"Hãy đảm bảo bài test bắt đúng lỗi và thất bại rõ ràng"*, chỉ cần dùng từ `red`. Từ dẫn dắt neo giữ hành vi phức tạp trong một token duy nhất mà không tốn token định nghĩa.

4. **Phòng Ngừa Phủ Định (Negation Prevention)**:
   - Hiện tượng *"Đừng nghĩ về con voi"*: Khi bạn ra lệnh cấm cho LLM ("Không được viết hàm quá 50 dòng"), từ phủ định là một modifier yếu ớt bị khái niệm được kích hoạt mạnh mẽ đè bẹp; lệnh cấm vô tình kéo hành vi bị cấm vào ngữ cảnh.
   - Nguyên tắc: **Luôn chỉ đạo bằng hành vi khẳng định tích cực** ("Viết các hàm ngắn dưới 30 dòng, tập trung duy nhất một trách nhiệm"). Chỉ dùng lệnh cấm như một bức tường bảo vệ cứng khi không thể diễn đạt bằng câu khẳng định, và ngay cả khi đó, phải lập tức ghép đôi với mục tiêu tích cực.

5. **Tiêu Chí Hoàn Tất: Độ Rõ Ràng vs Độ Đòi Hỏi (Completion Criteria: Clarity vs Demand)**:
   - **Độ Rõ Ràng (Clarity)**: Tác nhân có thể phân biệt dứt khoát giữa "đã xong" và "chưa xong" hay không? Nếu tiêu chí mập mờ, tác nhân sẽ bị cám dỗ kết thúc sớm (premature completion) vì sức hút của các bước tiếp theo.
   - **Độ Đòi Hỏi (Demand)**: Mức độ khắt khe của tiêu chí. Ví dụ: *"Tất cả các model bị sửa đổi đều phải có test tương ứng"* đòi hỏi sự đào sâu (legwork) lớn hơn nhiều so với câu *"Hãy liệt kê các thay đổi"*.

---

## 5. PHÂN TÍCH ĐỐI CHIẾU VỚI HỆ THỐNG `AGENT-SKILLS` (v5.9.0)

### 5.1 Quản Trị Hình Thức, Kiểm Định Tự Động & 21 Validation Gates
Sự đối lập rõ rệt nhất giữa hai kho lưu trữ nằm ở cấp độ quản trị hình thức (formal governance):

```
HỆ THỐNG agent-skills (v5.9.0)              KHO LƯU TRỮ mattpocock/skills (v1.3.2)
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│  21 Validation Gates                 │     │  Changesets Release Only             │
│  - 946 pytest passed in 56s          │     │  - npm run version                   │
│  - validate-skills.py (184 skills)   │     │  - 0 unit tests                      │
│  - validate-roles.py (39 roles)      │     │  - 0 schema validators               │
│  - validate-contracts.py (63 schemas)│     │  - 0 AST security checks             │
│  - AST Security & Lethal Trifecta    │     │  - Silent YAML syntax bug in repo    │
└──────────────────────────────────────┘     └──────────────────────────────────────┘
```

Trong khi `mattpocock/skills` hoàn toàn không có bất kỳ bộ kiểm thử tự động nào trong `package.json` (chỉ có `@changesets/cli` để bump version), thì `agent-skills` được thiết kế như một hệ điều hành tác nhân chuẩn mực với **21 Cổng kiểm soát (Validation Gates)** chạy qua `python3 core/scripts/validate-all.py` và bộ 946 unit tests pytest:
1. `validate-rules.py`: Quét quy tắc lõi và kiểm tra tính đồng bộ 9 nhóm chẵn trên 7 tệp adapter mirrors.
2. `validate-skills.py`: Kiểm định định dạng frontmatter, chiều dài ($\le 200$ dòng) và công cụ hợp lệ cho 184 kỹ năng.
3. `validate-roles.py`: Kiểm soát 18 phần bắt buộc và 12-24 khóa bảo vệ (LOCKs) cho 39 vai trò.
4. `validate-workflows.py`: Kiểm định thứ tự tuần tự và liên kết vai trò của 25 quy trình.
5. `validate-packs.py`: Xác thực tính toàn vẹn của 17 gói chuyên đề.
6. `validate-overlays.py`: Xác thực 21 overlays bổ trợ.
7. `validate-compliance-2026.py`: Kiểm tra tuân thủ Đạo luật AI của EU (EU AI Act Article 50).
8. `validate-contracts.py`: Kiểm tra 63 JSON Schemas bằng `Draft202012Validator` với các ví dụ mẫu bundled.
9. `validate-a2a.py`: Kiểm định sự tuân thủ chuẩn giao tiếp Agent-to-Agent (A2A 1.0).
10. `validate-agent-cards.py`: Xác thực thẻ tác nhân đại diện cho 39 vai trò.
11. `validate-standardization.py`: Đánh giá điểm chuẩn hóa (đạt 100%).
12. `validate-version-sync.py`: Đồng bộ phiên bản 5.9.0 trên toàn bộ registry và tài liệu.
13. `validate-indexes.py`: Rà soát tính toàn vẹn của `INDEX.md`.
14. `validate-policy-consistency.py`: Kiểm tra ranh giới hành vi không thể đảo ngược (Irreversible Actions).
15. `validate-skill-ownership.py`: Đảm bảo 100% (170/170) core skills đều có Primary owner.
16. `validate-skill-sections.py`: Bắt buộc 7 phần cấu trúc chuẩn trong toàn bộ kỹ năng.
17. `validate-contract-coverage.py`: Đảm bảo mọi vai trò đều có hợp đồng đầu ra rõ ràng.
18. `validate-golden-evals.py`: Xác thực 17 tài sản và 178 cặp kiểm thử vàng.
19. `validate-thirdparty-skills.py`: Quét tiền kiểm duyệt mã nguồn tác nhân bên thứ ba.
20. `validate-skill-security.py`: **AST Skill Security & Lethal Trifecta Scanner**: Quét AST tĩnh không thực thi, ngăn chặn triệt để mã độc, cấm `eval()`, `exec()`, `curl | bash`, và kiểm soát bất biến bộ ba hủy diệt ($T_{lethal} = D_{priv} \land C_{untrusted} \land E_{net} \land \neg S_{box}$).
21. `validate-discovery-manifest.py`: Kiểm định `INDEX_TIER1.json` kèm mã băm SHA-256 bảo vệ toàn vẹn byte.

### 5.2 Hợp Đồng Dữ Liệu JSON Schema (Draft 2020-12) vs Free-form Markdown
- **`agent-skills`**: Mọi giao tiếp giữa các tác nhân và bàn giao kết quả đều phải thông qua các hợp đồng dữ liệu chuẩn hóa bằng **JSON Schema Draft 2020-12** (63 schemas như `feature-ticket.json`, `technical-delivery-plan.json`, `implementation-result.json`, `test-report.json`, `code-review-finding.json`). Dữ liệu xuất ra có cấu trúc định lượng, trường định danh (`contract_type`), có thể tự động parse bởi script và tích hợp vào pipeline CI/CD mà không phụ thuộc vào cảm xúc của mô hình.
- **`mattpocock/skills`**: Hoàn toàn không có hợp đồng schema. Đầu ra của các kỹ năng (`code-review`, `to-spec`, `handoff`) là văn bản Markdown tự do. Mặc dù phong cách Markdown này rất thân thiện với lập trình viên khi đọc bằng mắt, nhưng nó hoàn toàn bất lực trong việc bảo đảm tính tiền định khi các tác nhân tự động bắt tay nhau (Agent-to-Agent handover) trong các swarm quy mô lớn.

### 5.3 Phân Định Trách Nhiệm Role & Skill Ownership vs Flat Developer Persona
- **`agent-skills`**: Áp dụng mô hình **Phân chia Trách nhiệm Chuyên môn hóa (Separation of Concerns)** với 39 vai trò phân định rõ ràng (`software-architect`, `frontend-developer`, `backend-developer`, `qa-engineer`, `security-engineer`, `task-planner`, `seo-analyst`, v.v.). Mỗi vai trò sở hữu hộp công cụ riêng (`Primary Skills` tự chạy trực tiếp, `Supporting Skills` phải cộng tác). Mọi kỹ năng bắt buộc phải có chủ sở hữu (`validate-skill-ownership.py`). Điều này ngăn ngừa tình trạng một tác nhân lập trình tự ý can thiệp vào bảo mật hoặc hạ tầng mà không có sự kiểm tra chéo.
- **`mattpocock/skills`**: Sử dụng một **Nhân cách Lập trình viên Đồng nhất (Flat Developer Persona)**. Cả 39 kỹ năng đều giả định người ngồi trước máy là một "Fullstack Senior Developer" sử dụng Claude Code qua các lệnh gạch chéo (`/`). Mô hình này rất gọn gàng cho cá nhân làm việc độc lập, nhưng không thể mở rộng cho các tổ chức doanh nghiệp nơi mà kỹ sư QA, kiến trúc sư và chuyên viên bảo mật có những ranh giới quyền hạn và trách nhiệm pháp lý riêng biệt.

### 5.4 Cân Bằng Chiến Lược: Formal Rigor vs Developer Ergonomics
- **"Thuế Hình Thức" (Formal Tax) của `agent-skills`**: Để tạo ra một kỹ năng mới trong `agent-skills`, kỹ sư phải viết đúng 18 mục của vai trò, 7 mục bắt buộc của kỹ năng, giới hạn dưới 200 dòng, khai báo allowed-tools từ policy map, viết JSON schema đầu ra, và chạy qua 21 cổng kiểm thử. Quy trình này đảm bảo an toàn tuyệt đối nhưng tạo ra ma sát nhận thức lớn (high cognitive friction) khi cần thử nghiệm nhanh các heuristics linh hoạt.
- **"Sự Thanh Thoát Thực Dụng" (Ergonomics) của `mattpocock/skills`**: Kỹ năng được viết tự nhiên, súc tích, giải quyết trúng tim đen các nỗi đau hàng ngày của lập trình viên (debug lỗi khó, bẻ khóa interface sâu, viết test không bị nhảm).  
$\rightarrow$ **Kết luận Chiến lược**: Tinh hoa của `mattpocock/skills` nằm ở các **Heuristics & Mental Models**, trong khi sức mạnh của `agent-skills` nằm ở **Nền tảng Quản trị & Hạ tầng Bảo mật**. Sự kết hợp lý tưởng là đóng gói các heuristics của Matt Pocock vào đúng các khuôn mẫu hình thức của `agent-skills`.

---

## 6. PHÂN TÍCH ĐỐI CHIẾU VỚI HỆ THỐNG `LOTTE-DMS-AGENT` (v2.15.0 / A2A v3.1.0)

### 6.1 Đặc Thù Miền Nghiệp Vụ Bán Lẻ / Kho Vận Quy Mô 20M+ Đơn Hàng
Hệ thống `lotte-dms-agent` đại diện cho một môi trường vận hành công nghiệp khắc nghiệt với mức độ rủi ro tài chính trực tiếp:
- **Quy mô Giao dịch**: Xử lý hơn **20 triệu đơn hàng**, 15 dịch vụ vi mô (microservices: `orders-service`, `settlement-service`, `delivery-services`, `auto-assign`, v.v.), 5 cơ sở dữ liệu MySQL liên kết federated (`martonline_oms`, `martonline_dms`, `martonline_usts`, `dosiin_lotte`, `martonline_chat`).
- **Máy Trạng Thái Nghiêm Ngặt**: 30 trạng thái OMS và 29 trạng thái DMS. Quá trình chuyển dịch trạng thái được kiểm soát tuyệt đối qua `app/StateTransitions` trong `orders-service` (BF-09/BF-15). Nghiêm cấm mọi hành vi cập nhật trạng thái trực tiếp vào DB. Các trạng thái cuối (`220: COMPLETE`, `210: CANCELLED`) là bất biến.
- **Tác Động Tài Chính Thực Tế**: Dòng tiền thu hộ COD đối soát trên 4 cơ sở dữ liệu, tự động sinh chứng từ kế toán MISA AMIS (tài khoản TK 1381 / TK 3381). Một sai sót nhỏ của AI trong tính toán GrandTotal hoặc cấn trừ tiền hàng có thể dẫn đến thất thoát hàng tỷ đồng.

### 6.2 Cổng Kiểm Soát 9 Chiều (9-Dimension Review Gate) & Socratic Cognitive Guardrails
Trong khi `mattpocock/skills` chỉ rà soát mã nguồn trên 2 trục (Standards vs Spec), `lotte-dms-agent` bắt buộc mọi thay đổi mã nguồn phải bước qua **Cổng kiểm soát 9 chiều toàn diện** (`rules/code-change-review.md`):
1. *Chiều 1: Kiến trúc Backend (Clean Architecture, Ports & Adapters, Service Boundaries)*.
2. *Chiều 2: Quy mô & Tải 20M+ Đơn hàng (Cấm `leftJoinSub` gây sập 504, cấm `LIKE '%...'`, bắt buộc chỉ mục bao phủ covering index)*.
3. *Chiều 3: Toàn vẹn Dữ liệu & Schema (Bảo vệ Migration, Khóa ngoại, Transaction isolation)*.
4. *Chiều 4: Quy tắc Nghiệp vụ & State Machines (Kiểm soát 30 OMS / 29 DMS transitions)*.
5. *Chiều 5: Bảo mật & Đa khách thuê (Multi-Tenancy Store Isolation, Phân quyền dữ liệu)*.
6. *Chiều 6: Tương thích Frontend & Mobile Apps (Đồng bộ hợp đồng API với Picker App và Driver App)*.
7. *Chiều 7: Kiểm chứng Thực nghiệm (Bắt buộc chạy Docker-First test, không chấp nhận khẳng định suông)*.
8. *Chiều 8: Ranh giới Quyền hạn Tác nhân (Tuân thủ `action-boundaries-dms.yaml`)*.
9. *Chiều 9: Độ Sạch Bộ nhớ & Trôi Ngữ cảnh (Tuân thủ ngân sách bộ nhớ Tier 1 $\le 65$ dòng)*.

Đặc biệt, hệ thống tích hợp sẵn các **Rào chắn Nhận thức Socrate (Socratic Cognitive Guardrails)** chuyên sâu cho kho vận:
- *Bất biến Cân bằng Tồn kho*: $\text{AvailableStock} = \text{PhysicalStock} - \text{ReservedStock} - \text{DamagedStock}$.
- *Bất biến Trạng thái Xe đẩy (Trolley Lifecycle - LMO-5415)*: Xe đẩy chỉ được gán độc quyền cho một người nhặt hàng tại một thời điểm, chuyển đổi đơn điệu, giải phóng ngay khi hoàn tất đợt nhặt để tránh xe đẩy bị kẹt ở trạng thái `'in_use'`.
- *Bất biến Sổ cái COD*: Tổng tiền mặt thu từ tài xế bắt buộc phải khớp tuyệt đối với biên bản bàn giao và chứng từ kế toán MISA AMIS.

### 6.3 Kiểm Soát Cơ Sở Dữ Liệu Quy Mô Khủng: Zero-Downtime DDL (`gh-ost`), Outbox & Financial Invariants
- **Thay Đổi Cấu Trúc Bảng Không Gián Đoạn (Zero-Downtime DDL via OSC)**:
  Tại quy mô bảng dữ liệu hàng chục triệu dòng trong DMS, một lệnh `ALTER TABLE` trực tiếp sẽ khóa bảng (table lock) gây sập toàn bộ hệ sinh thái đặt hàng. `lotte-dms-agent` bắt buộc mọi migration trên bảng nóng (>1M dòng) phải sử dụng công cụ **`gh-ost` (GitHub's Online Schema Migration)** với kế hoạch rollback hai chiều (`up()` và `down()`), thời gian chờ khóa tối đa 5 giây và chạy thử nghiệm khô (dry-run). Kỹ thuật này nằm ngoài phạm vi cân nhắc của `mattpocock/skills`.
- **Mô Hình Transactional Outbox**:
  Mọi sự kiện hàng đợi (Queue Events) hoặc tích hợp vận chuyển bên ngoài (3PL Grab, Ahamove) bắt buộc phải tuân thủ mẫu:
  `DB::afterCommit(fn () => dispatch(...))` để ngăn chặn triệt để hiện tượng race condition khi event bắn đi nhưng transaction cơ sở dữ liệu bị rollback.
- **Bất Biến Môi Trường Staging Đọc-Ghi (Staging Read-Only Invariant)**:
  Tác nhân bị cấm tuyệt đối việc ghi, sửa đổi bảng hoặc chạy thử nghiệm trực tiếp trên DB Staging. Mọi hành động xác minh bắt buộc phải thực thi bên trong mạng Docker cục bộ (`orders-php`, `dms-mysql`).

### 6.4 Policy-as-Code Hooks (`check-policy.py`) vs Client-side Claude Hooks
- **`mattpocock/skills`**: Sử dụng script bash `.claude/hooks/block-dangerous-git.sh` kết nối qua tính năng `PreToolUse` của riêng Claude Code để chặn các lệnh `git push` hay `git reset`. Giải pháp này mang tính chất cục bộ trên máy của một lập trình viên dùng Claude Code; nếu chuyển sang Cursor, Codex hay chạy CI/CD tự động thì rào chắn này hoàn toàn vô hiệu.
- **`lotte-dms-agent`**: Sở hữu kiến trúc bảo mật cấp doanh nghiệp với bộ tiền kiểm soát **`scripts/hooks/check-policy.py`**. Hook này chạy độc lập với mọi IDE, đối chiếu hành vi của tác nhân với ma trận quyền hạn `policies/action-boundaries-dms.yaml`, phân loại rủi ro 3 cấp độ (`allowed`, `requires_approval`, `denied`), và xuất ra nhật ký kiểm toán chuẩn quốc tế **SARIF 2.1.0** cùng chuẩn bảo mật **OCSF 99001 (Security Findings)**.

---

## 7. ĐÁNH GIÁ ƯU ĐIỂM, NHƯỢC ĐIỂM VÀ ANTI-PATTERNS CẦN NÉ TRÁNH

### 7.1 Điểm Mạnh Vượt Trội Đáng Tiếp Thu
1. **Khung Nhận Thức Kỹ Thuật Đỉnh Cao (World-Class Software Mental Models)**:
   - Các nguyên lý Ousterhout Deep Modules (`codebase-design`), kiểm thử theo seam (`tdd`), và gọt dũa giả thuyết khoa học (`diagnosing-bugs`) là vũ khí tối thượng để dập tắt thói quen "vibe coding".
2. **Kỹ Thuật Chẩn Đoán Trực Quan Độc Lập (Self-Contained Visual Diagnostics)**:
   - Khả năng tự sinh báo cáo HTML trực quan với CDN Tailwind/Mermaid trong `/tmp` giúp con người nắm bắt kiến trúc trong vài giây mà không làm bẩn git workspace.
3. **Giải Pháp Cầu Nối Con Người An Toàn (Safe HITL Automation)**:
   - Mẫu script `wizard/template.sh` là lời giải xuất sắc cho bài toán thiết lập biến môi trường, secret và các thao tác thủ công nhạy cảm mà không bao giờ để lộ bí mật vào prompt.
4. **Vệ Sinh Cửa Sổ Ngữ Cảnh Tối Tối (Aggressive Context Window Hygiene)**:
   - Nguyên tắc luôn khởi tạo fresh context window cho subagents, lưu tài liệu thám hiểm ngoài repo, và chỉ truyền con trỏ ngữ cảnh (context pointers) thay vì nhồi nhét dữ liệu giúp tác nhân duy trì sự tập trung tối đa.

### 7.2 Lỗ Hổng Kiến Trúc, Anti-Patterns & Rủi Ro Vận Hành Thực Tế
Mặc dù sở hữu những prompt heuristics tuyệt vời, `mattpocock/skills` bộc lộ những khiếm khuyết chết người mang tính cấu trúc mà một hệ thống doanh nghiệp bắt buộc phải loại trừ:

```
                            NHỮNG LỖ HỔNG & ANTI-PATTERNS CỦA mattpocock/skills
                                            │
         ┌──────────────────────────────────┼──────────────────────────────────┐
         ▼                                  ▼                                  ▼
┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│ LỖI CÚ PHÁP THỰC │              │ HOÀN TOÀN THIẾU  │              │ VI PHẠM HARNESS  │
│ TẾ TRONG REPO    │              │ TEST VÀ SCHEMAS  │              │ PARITY TỰ ĐẶT RA │
│ - software-factory│             │ - 0 JSON schemas │              │ - software-factory│
│   SKILL.md lỗi   │              │ - 0 automated    │              │   thiếu hoàn toàn │
│   YAML scanner   │              │   test gates     │              │   openai.yaml    │
│   do thiếu nháy  │              │ - Rủi ro trôi dạt│              │ - Router nói dối │
│   ở dấu hai chấm │              │   không kiểm soát│              │   (ask-matt sync)│
└──────────────────┘              └──────────────────┘              └──────────────────┘
```

1. **Lỗi Cú Pháp YAML Thực Tế Đang Tồn Tại Trong Bản Shipped (Real-World Syntax Error)**:
   - Tại dòng 3 tệp `skills/in-progress/software-factory/SKILL.md`:
     ```yaml
     ---
     name: software-factory
     description: Shared language for designing a software factory: the tasks it runs and the services it plugs into.
     ---
     ```
   - Giá trị của thuộc tính `description` chứa dấu hai chấm (`: `) ngay sau chữ *software factory* nhưng không được bọc trong dấu ngoặc kép. Khi phân tích cú pháp bằng bất kỳ thư viện chuẩn nào (như `PyYAML` trong Python), hệ thống sẽ lập tức ném ra ngoại lệ nghiêm trọng:
     `yaml.scanner.ScannerError: mapping values are not allowed here`.
   - *Hệ quả*: Tác nhân hoặc harness nào cố gắng nạp kỹ năng này sẽ bị crash ngay lập tức. Đây là bằng chứng không thể chối cãi của việc thiếu vắng các validation gates tự động.

2. **Vi Phạm Tính Song Hành Harness Parity (Broken Harness Parity)**:
   - Kho lưu trữ đặt ra nguyên tắc bất di bất dịch tại `CLAUDE.md:10` và `.agents/invocation.md:10`: *"Every skill also carries an agents/openai.yaml beside its SKILL.md"*.
   - Tuy nhiên, kỹ năng `software-factory` hoàn toàn không có thư mục `agents/` hay tệp `openai.yaml`. Sự bất nhất này chứng minh rằng việc duy trì quy chuẩn bằng tài liệu văn bản mà không có script kiểm tra tự động sẽ luôn dẫn đến suy thoái.

3. **Hoàn Toàn Thiếu Vắng Hợp Đồng Dữ Liệu (Zero Schema Contracts)**:
   - Các kỹ năng giao tiếp hoàn toàn bằng văn bản tự do. Trong một hệ sinh thái đa tác nhân, việc một tác nhân xuất ra markdown tự do khiến tác nhân tiếp theo phải đoán cấu trúc, làm tăng tỷ lệ ảo giác (hallucination) và phá vỡ tính tự động hóa của chuỗi quy trình.

4. **Rủi Ro "Bộ Điều Hướng Nói Dối" (Routers That Lie)**:
   - Kỹ năng điều hướng `ask-matt` phải được bảo trì và cập nhật hoàn toàn bằng tay mỗi khi một kỹ năng mới được thêm vào hoặc đổi tên (`CLAUDE.md:21-22`). Khi kho lưu trữ phình to, việc đồng bộ bằng tay này chắc chắn sẽ bị bỏ quên, biến `ask-matt` thành một chiếc la bàn chỉ sai hướng. Trong `agent-skills`, việc này được tự động hóa 100% qua script `core/scripts/generate-index.py`.

5. **Xả File Rác Bừa Bãi Ra Thư Mục Tạm Hệ Điều Hành (`$TMPDIR`)**:
   - Kỹ năng `handoff` và `claude-handoff` tự tiện xả các file markdown không được định danh cấu trúc ra `/tmp` của máy host. Trong môi trường doanh nghiệp có nhiều người dùng hoặc nhiều container chạy chung, điều này vi phạm ranh giới bảo mật (OWASP ASI06 - Context Poisoning), làm rò rỉ thông tin nhạy cảm và không có cơ chế thu hồi dọn dẹp.

6. **Anti-Pattern "Software Factory Không Người Lái" (Unattended Loops Without Brakes)**:
   - Ý tưởng của `software-factory` và `loop-me` hướng tới việc cho tác nhân chạy vòng lặp vô tận, tự đọc issue và tự tạo PR mà không có sự phê duyệt của con người ở các chốt chặn then chốt. Trong các hệ thống bán lẻ và tài chính như DMS, điều này vi phạm nghiêm trọng **Nguyên tắc Tối thiểu Quyền lực (Least-Agency Principle)** và quy tắc phê duyệt hành động không thể đảo ngược.

---

## 8. ĐỀ XUẤT GIẢI PHÁP ÁP DỤNG CỤ THỂ CHO `AGENT-SKILLS`

Để hấp thu trọn vẹn những giá trị tinh hoa của `mattpocock/skills` mà vẫn bảo toàn 100% sự nghiêm ngặt của 21 Validation Gates và 946 bài test trong `agent-skills`, chúng tôi đề xuất chiến lược tích hợp 3 tầng (3-Tier Integration Strategy):

### 8.1 Surface 1: Bổ Sung Heuristics Vào Core Skills Hiện Hành (Zero Overhead)
Đây là phương án có giá trị cao nhất và độ rủi ro bằng 0, không làm tăng số lượng kỹ năng, không tạo thêm gánh nặng cho bảng phân quyền role:
1. **Làm Giàu `core/skills/foundation/systematic-debugging` Bằng Kỷ Luật Của `diagnosing-bugs`**:
   - Bổ sung quy tắc: **Bắt buộc thiết lập tight red-capable feedback loop** trước khi cho phép tác nhân đọc code để đoán nguyên nhân.
   - Bổ sung bảng xếp hạng 10 loại feedback loop vào phần `## Suggested Process`.
   - Bổ sung kỹ thuật **Thu nhỏ tối thiểu (Minimise)** bản tái hiện lỗi.
   - Chuẩn hóa định dạng giả thuyết: Yêu cầu bắt buộc tạo **3–5 giả thuyết có thể bác bỏ** theo mẫu `"If X is cause, then changing Y will eliminate bug"`.
   - Chuẩn hóa tiền tố gắn log: Bắt buộc dùng `[DEBUG-...]` và grep dọn sạch trước khi đóng task.
2. **Làm Giàu `core/skills/foundation/plan-technical-delivery` & `core/skills/product/build-story-map` Bằng Kỹ Thuật Tracer-Bullets Của `to-tickets`**:
   - Bổ sung quy chuẩn rã ticket theo lát cắt dọc (Vertical tracer-bullet slicing): mỗi ticket phải đi xuyên suốt schema, API, UI, test và vừa vặn một context window đơn lẻ.
   - Bổ sung kỹ thuật **Expand-Contract (Mở rộng - Thu hẹp)** cho các đợt refactoring lớn.
   - Bắt buộc khai báo đồ thị phụ thuộc (`Blocked by: ...`) để tác nhân điều phối có thể tính toán Ranh giới (Frontier) thực thi song song.
3. **Làm Giàu Vai Trò `@reviewer` Trong `core/skills/repo-ops/review-code`**:
   - Tích hợp mô hình **Two-Axis Review**: Tách biệt rõ ràng trục Tiêu chuẩn (Standards) và trục Nghiệp vụ (Spec), nhúng bảng 12 mùi mã nguồn của Martin Fowler làm heuristic tham chiếu mặc định.

### 8.2 Surface 2: Phát Triển Các Core Skills Mới (Được Chuẩn Hóa Theo Chuẩn 184 Skills)
Xây dựng 3 kỹ năng cốt lõi mới, đặt tại các phân vùng phù hợp, tuân thủ tuyệt đối cấu trúc chuẩn (dưới 200 dòng, đầy đủ 7 sections bắt buộc, có JSON schema output, đăng ký Primary Owner):

#### 1. `core/skills/foundation/design-deep-modules/SKILL.md` (Chuyển giao từ `codebase-design`)
- **Primary Owner**: `technical-architect` (Supporting: `solution-architect`, `backend-developer`). Lý do: `technical-architect.md` trực tiếp sở hữu và phát hành `adr-spec.json` cùng `architecture-options.json` (trong khi `solution-architect` sở hữu `solution-brief.json` và theo phân định ranh giới tại `solution-architect.md:300` thì explicitly không sở hữu `adr-spec.json`).
- **Allowed Tools**: `[read_file, search_code, execute_command]`.
- **Mục tiêu**: Hướng dẫn thiết kế mô-đun sâu theo John Ousterhout, xác định vị trí Seam, áp dụng Deletion Test, và triển khai kỹ thuật "Design It Twice".
- **Hợp đồng Đầu ra**: `contracts/schemas/architecture-options.json` hoặc `contracts/schemas/adr-spec.json`.
- **Bảo mật**: Tuân thủ khóa kiến trúc và OWASP ASI05.

#### 2. `core/skills/foundation/scaffold-hitl-wizard/SKILL.md` (Chuyển giao từ `wizard`)
- **Primary Owner**: `devops-engineer` (Supporting: `system-engineer`, `agent-coordinator`).
- **Allowed Tools**: `[read_file, write_file, edit_file, execute_command]`.
- **Mục tiêu**: Tự động sinh script bash tương tác có giao diện trực quan (`scripts/setup-wizard.sh`) cho các thủ tục bắt buộc con người can thiệp (lấy secret, OAuth, DB cutover) dựa trên thư viện chuẩn hóa `wizard/template.sh`.
- **Hợp đồng Đầu ra**: File script thực thi tại `scripts/` và bản ghi kế hoạch triển khai `contracts/schemas/deployment-plan.json` (tuân thủ quy định tại `devops-engineer.md:383`: vai trò DevOps bàn giao deployment-plan, không bao giờ bàn giao `implementation-result.json` vốn thuộc sở hữu của developer).
- **Bảo mật**: AST Security Scanner kiểm duyệt không có lệnh phá hoại, cấm lưu secret dạng plain text trong prompt.

#### 3. `core/skills/agent/socratic-design-interview/SKILL.md` (Chuyển giao từ `grilling`)
- **Primary Owner**: `business-analyst` (Supporting: `agent-coordinator`, `task-planner`).
- **Allowed Tools**: `[read_file, search_code]`. Giới hạn tối giản (Minimal Footprint), loại bỏ `execute_command` nhằm tránh kích hoạt các rào kiểm duyệt `requires_approval` không cần thiết trong quá trình phỏng vấn làm rõ yêu cầu nghiệp vụ.
- **Mục tiêu**: Kỹ thuật phỏng vấn Socrate gọt dũa yêu cầu; xây dựng cây quyết định thiết kế; tính toán ranh giới câu hỏi đã giải quyết vs chưa giải quyết; hỏi theo từng đợt có đánh số kèm khuyến nghị lựa chọn; cấm hỏi những gì có thể tự tra cứu trong repo.
- **Hợp đồng Đầu ra**: `contracts/schemas/feature-ticket.json` và `contracts/schemas/assumptions-ledger.json` (loại bỏ `solution-brief.json` vốn thuộc sở hữu độc quyền của `solution-architect`; tuân thủ phân định ranh giới tại `business-analyst.md:155,185`).

### 8.3 Surface 3: Thiết Kế Gói Chuyên Biệt `packs/typescript-craft-team` & `overlays/typescript-craft`
Dành riêng cho các dự án phát triển TypeScript cao cấp (như các dự án Astro, Next.js, Cloudflare Workers trong workspace):
- **Overlay `overlays/typescript-craft/`**:
  - *Quy tắc*: `overlays/typescript-craft/rules/typescript-architecture.md` (cấm barrel files bừa bãi, rào chặn kiến trúc thư mục).
  - *Kỹ năng đặc thù*:
    * `setup-ts-deep-modules`: Tự động cài đặt và cấu hình `dependency-cruiser` bảo vệ ranh giới mô-đun sâu.
    * `migrate-to-shoehorn`: Dọn sạch code smell ép kiểu bẩn bằng `@total-typescript/shoehorn`.
    * `setup-pre-commit`: Cấu hình Husky, lint-staged và Prettier.
- **Pack `packs/typescript-craft-team/manifest.yaml`**:
  - Đóng gói toàn bộ các vai trò và overlay trên thành một gói hoàn chỉnh sẵn sàng kích hoạt.

### 8.4 Quy Trình Chuẩn Hóa Chuyển Đổi 6 Bước (Adaptation Pipeline)
Mọi kỹ năng tiếp thu từ bên ngoài bắt buộc phải đi qua đường ống chuẩn hóa nghiêm ngặt:

```markdown
1. Chuẩn Hóa Frontmatter (YAML Sanitization):
   - [ ] name: viết thường, nối bằng dấu gạch ngang, <= 64 ký tự, trùng tên thư mục cha.
   - [ ] description: <= 1024 ký tự, bắt đầu bằng "Use when ...", ngôi thứ ba, bọc nháy kép toàn bộ nếu có dấu hai chấm.
   - [ ] allowed-tools: danh sách tường minh không rỗng, khớp chính xác với core/policies/mcp-tool-map.yaml.
2. Tái Cấu Trúc Văn Bản & Tiêu Đề:
   - [ ] Tổng số dòng trong SKILL.md phải nghiêm ngặt < 200 dòng (chuyển cẩm nang dài vào references/).
   - [ ] Tiêu đề H1 duy nhất khớp chính xác slug name (không có chữ " Skill" ở cuối).
   - [ ] Đầy đủ 7 phần bắt buộc: When to Use, Core Rules, Suggested Process, Checklist (>= 5 checkboxes), Failure Modes, Output Contracts, Security Guardrails, Related Skills.
   - [ ] Dòng cuối cùng: Đúng một dòng duy nhất "Last updated: YYYY-MM-DD".
3. Kiểm Tra Quét AST Security & Lethal Trifecta:
   - [ ] Không chứa builtins bị cấm (eval, exec, compile).
   - [ ] Không chứa mẫu shell nguy hiểm (curl | bash, /dev/tcp, fork bombs).
   - [ ] Vượt qua kiểm tra Lethal Trifecta Scanner.
4. Gán Quyền Sở Hữu Role (Ownership Wiring):
   - [ ] Khai báo là Primary Skill trong ít nhất một file core/roles/*.md.
   - [ ] Kiểm tra Decision Boundaries và Role Boundaries của role không phủ nhận hành động của skill.
5. Tái Sinh Toàn Bộ Registry & Index:
   - [ ] Chạy python3 core/scripts/generate-a2a-registry.py
   - [ ] Chạy python3 core/scripts/generate-index.py
   - [ ] Chạy python3 core/scripts/generate-tier1-index.py (cập nhật SHA-256 digests)
6. Kiểm Tra Toàn Bộ 21 Cổng:
   - [ ] Chạy python3 core/scripts/validate-all.py (đạt 21/21 gates PASS).
   - [ ] Chạy pytest -q (đạt 100% passed).
```

---

## 9. ĐỀ XUẤT GIẢI PHÁP ÁP DỤNG CỤ THỂ CHO `LOTTE-DMS-AGENT`

### 9.1 Nâng Cấp Quy Trình Debug Vi Dịch Vụ Với Kỷ Luật Feedback-Loop-First
Hệ thống `lotte-dms-agent` hiện có sẵn quy trình `workflows/debug.md` và 16 kỹ năng debug vi dịch vụ chuyên sâu (`orders-service-debug`, `settlement-service-debug`, v.v.). Tuy nhiên, quy trình hiện tại mới chỉ dừng lại ở chỉ dẫn chung: *"§0.5 Điều tra $\rightarrow$ Báo cáo $\rightarrow$ Review $\rightarrow$ Sửa mã"*.

**Đề xuất nâng cấp thực tiễn**:
1. **Phân Định Rõ Ràng Ranh Giới Vai Trò (Role Boundaries) & Kỷ Luật Docker Test Đỏ**:
   - **Ranh giới vai trò**: Giai đoạn Triage / Điều tra sơ bộ / Phân tích nguyên nhân gốc (RCA) thuộc quyền sở hữu của các vai trò điều tra: `trace-data` và `incident`. Tuy nhiên, theo bảng phân quyền `policies/action-boundaries-dms.yaml:82-85` và `workflows/debug.md:99`, `incident` là vai trò điều phối sự cố / RCA mà hành động `code_change` bắt buộc phải qua phê duyệt (`requires_approval`). Do đó, giai đoạn Xây dựng kịch bản tái hiện (Reproduction) và Sửa mã nguồn (Code Remediation) thuộc quyền sở hữu độc quyền của kỹ sư chuyên trách: `developer-be` (hoặc `developer-fe` / `data` tùy thuộc vào vi dịch vụ). Tác nhân `incident` tuyệt đối không được phép trực tiếp sửa mã.
   - **Kỷ luật Docker-First test đỏ**: Trước khi bất kỳ dòng code nào trong `orders-service` hay `settlement-service` được sửa, kỹ sư tác nhân (`developer-be`) **bắt buộc phải trình ra một lệnh Docker-First test đỏ**:
     ```bash
     docker compose exec -T orders-php php artisan test --filter OrderCancellationTest
     ```
   - Lệnh này phải tái hiện chính xác triệu chứng lỗi được người dùng báo cáo. Nếu không có lệnh test đỏ này, tác nhân bị cấm tuyệt đối bước sang giai đoạn sửa mã.
2. **Bắt Buộc Cô Lập Giao Dịch Cơ Sở Dữ Liệu (Database Transaction Isolation)**:
   - Trong môi trường Docker vi dịch vụ của DMS, container `orders-php` kết nối trực tiếp đến cơ sở dữ liệu MySQL dùng chung cho môi trường phát triển (`martonline_oms`, `martonline_dms`). Việc chạy kiểm thử tạo đơn hàng hoặc biến đổi dữ liệu trực tiếp mà không cô lập sẽ làm nhiễm bẩn dữ liệu dùng chung (state pollution), gây ra lỗi giả cho các test chạy sau và kích hoạt sai lệch các worker ngầm hoặc sự kiện RabbitMQ/Kafka.
   - Do đó, mọi test tái hiện Docker-first bắt buộc phải sử dụng trait `DatabaseTransactions` của Laravel/Lumen hoặc cơ chế rollback giao dịch tự động trong `tearDown()` để bảo đảm khôi phục hoàn toàn trạng thái cơ sở dữ liệu, ngăn ngừa tuyệt đối rủi ro biến đổi dữ liệu dùng chung.
3. **Cơ Chế Hook Alignment Cho Công Cụ Kiểm Tra Chính Sách (`check-policy.py` & `mcp-tool-map.yaml`)**:
   - Khi chạy lệnh kiểm thử Docker-first (`docker compose exec -T orders-php php artisan test ...`), nếu công cụ `execute_command` chỉ được ánh xạ chung trong `mcp-tool-map.yaml` thành `run_build`, chính sách `check-policy.py` sẽ phân giải hành động là `run_build` và kích hoạt rào cản phê duyệt (`POLICY APPROVAL REQUIRED: role 'developer-be' needs approval for 'run_build'`).
   - Để hỗ trợ chu trình phản hồi tự động nhanh chóng (tight feedback loop) mà không bị nghẽn bởi các rào phê duyệt giả (false approval blocks), `mcp-tool-map.yaml` phải được cấu hình mở rộng nhằm nhận diện các mẫu lệnh `docker compose exec ... test` hoặc `php artisan test` và ánh xạ chuẩn xác về hành động `local_verify` (vốn là hành động được phép tự động thực thi `allowed` đối với `developer-be` theo `action-boundaries-dms.yaml`).
4. **Yêu cầu 3–5 Giả thuyết Có Thể Bác Bỏ trong Báo cáo Chẩn đoán**:
   - Nâng cấp mẫu báo cáo `incident-report.json` và `contracts/schemas/debug-finding.json` với trường bắt buộc: `falsifiable_hypotheses` (danh sách các giả thuyết theo cú pháp: "Nếu X là nguyên nhân, thì sửa Y sẽ hết lỗi / sửa Z sẽ nặng hơn").
5. **Chuẩn Hóa Tag Debug Log trong Container PHP**:
   - Yêu cầu mọi log chẩn đoán tạm thời trong Laravel/Lumen phải dùng tiền tố `\Log::debug('[DEBUG-DMS-xxxx] ...');` và có bước kiểm tra tự động trước khi tạo Merge Request để đảm bảo không một dòng log nào bị sót lại.

### 9.2 Chuẩn Hóa Từ Vựng Deep Module Cho Kiến Trúc Sư Và Tech Lead
Hệ sinh thái DMS gồm 15 microservices đang đối mặt với sự phân mảnh kiến trúc (chẳng hạn: các controller quá béo trong `orders-service`, các closure xử lý đơn hàng phức tạp đan xen trực tiếp vào DB queries).
- **Tích hợp Từ vựng Deep Module vào `role/ta.md` (Technical Architect) & `role/tech-lead.md`**:
  - Đưa bộ từ vựng chuẩn tắc (Module, Interface, Implementation, Seam, Adapter, Depth, Leverage, Locality) vào tài liệu vai trò và checklist của Kiến trúc sư.
  - Áp dụng nguyên lý: *"Giao diện của microservice là ranh giới bất biến; ẩn giấu toàn bộ logic tính toán tồn kho, chiết khấu và đối soát COD vào sâu bên trong thân dịch vụ."*
- **Quy Tắc "Hai Adapter Mới Chứng Minh Một Seam" Cho Các Tích Hợp 3PL**:
  - Khi tích hợp các đối tác vận chuyển bên ngoài (`dms-3pl-grab-express`, Ahamove, Lalamove), áp dụng triệt để nguyên lý: Chỉ tạo interface trừu tượng vận chuyển khi có từ 2 hãng vận chuyển trở lên cùng chia sẻ một seam tích hợp; tránh việc tạo các lớp trung gian giả tạo (Middle Man code smell) cho các dịch vụ độc quyền.

### 9.3 Ứng Dụng Kỹ Thuật Socratic Grilling Cho Phân Tích Nghiệp Vụ (`ba.md`, `pm.md`)
Các bài toán nghiệp vụ trong DMS có độ phức tạp thuật toán và rủi ro vận hành cực lớn:
- **Thuật Toán Wave Planning (Phần 3 Task 9)**: Gom đơn hàng theo đợt sóng dựa trên khung giờ giao hàng, khu vực địa lý và sức chứa của kho.
- **Smart Picking (Task 10)**: Tối ưu hóa lộ trình di chuyển của người nhặt hàng trong kho siêu thị.
- **Cấn Trừ Sổ Cái Tiền Mặt COD (BF-12)**: Đối soát hàng triệu dòng tiền mặt giữa tài xế, bưu tá và ngân hàng.

**Giải pháp ứng dụng**:
- Trang bị kỹ năng `socratic-design-interview` (chuyển giao từ `grilling`) cho vai trò `@ba` và `@pm`.
- Trước khi chốt tài liệu đặc tả nghiệp vụ (`feature-ticket.json`), BA tác nhân phải chủ động vẽ ra cây quyết định, tính toán các ranh giới còn mù mờ và tiến hành phỏng vấn chuyên gia phân tích nghiệp vụ của Lotte Mart theo các đợt câu hỏi có khuyến nghị rõ ràng:
  > *"Đối với đơn hàng có hàng tươi sống cần cân lại trọng lượng (CatchWeightDelta), nếu khách hủy đơn tại thời điểm tài xế đã lấy hàng, trạng thái chuyển về 210 (CANCELLED) hay đưa vào nhánh xử lý ngoại lệ hoàn hàng trả tiền? Khuyến nghị: Chọn phương án B theo chuẩn BF-15 để bảo toàn sổ cái COD."*

### 9.4 Danh Mục Các Pattern Bắt Buộc Từ Chối (Rejected Patterns)
Để bảo vệ an toàn tuyệt đối cho hệ sinh thái bán lẻ DMS, các pattern sau đây từ `mattpocock/skills` **bị nghiêm cấm tích hợp**:
1. ❌ **Từ chối "Software Factory Không Người Lái" (`software-factory`, `loop-me`)**:
   - Nghiêm cấm mọi cơ chế cho phép AI tự động đọc issue và tự merge code vào các nhánh chính. Mọi thay đổi mã nguồn trong DMS bắt buộc phải qua sự phê duyệt của con người theo đúng `IRREVERSIBLE-ACTION-LOCK`.
2. ❌ **Từ chối Bàn Giao File Tự Do Ra Thư Mục `/tmp` (`handoff`, `claude-handoff`)**:
   - DMS đã có cơ chế quản lý bộ nhớ Tier 1 (`.agents/memory.md` $\le 65$ dòng) và phân vùng hội thoại an toàn (`.agents/conversations/<id>/`). Nghiêm cấm việc xuất dữ liệu nghiệp vụ ra thư mục tạm `/tmp` của host vì nguy cơ lộ lọt dữ liệu khách hàng và vi phạm ranh giới bảo mật.
3. ❌ **Từ chối PreToolUse Git Hooks Cục Bộ Của Claude Code (`git-guardrails-claude-code`)**:
   - DMS đã có hệ thống kiểm soát quyền hạn tập trung `scripts/hooks/check-policy.py` hỗ trợ SARIF 2.1.0 và OCSF 99001. Việc cài đặt các hook bash lẻ tẻ của Claude Code gây xung đột môi trường và tạo ra cảm giác an toàn giả tạo.
4. ❌ **Từ chối Ràng Buộc Kiểm Tra Dependency-Cruiser Của Node.js Cho Toàn Bộ Repo**:
   - Hệ thống backend DMS sử dụng 85% là PHP (Laravel/Lumen). Việc áp dụng `dependency-cruiser` chỉ có ý nghĩa trên frontend Vue 3 (`dms-web`). Đối với backend PHP, phải sử dụng các công cụ kiến trúc bản địa của PHP (như Deptrac hoặc PHPStan Architecture Rules).

---

## 10. LỘ TRÌNH TRIỂN KHAI CHI TIẾT (IMPLEMENTATION ROADMAP)

Để đưa các đề xuất trên vào thực tế một cách an toàn, có kiểm soát và không gây gián đoạn hệ thống, chúng tôi xây dựng lộ trình triển khai phân kỳ 4 giai đoạn trong vòng 8 tuần:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   LỘ TRÌNH TRIỂN KHAI 4 GIAI ĐOẠN (8 TUẦN)                       │
├────────────────────┬────────────────────┬───────────────────┬────────────────────┤
│ GIAI ĐOẠN 1        │ GIAI ĐOẠN 2        │ GIAI ĐOẠN 3       │ GIAI ĐOẠN 4        │
│ (Tuần 1 - 2)       │ (Tuần 3 - 4)       │ (Tuần 5 - 6)      │ (Tuần 7 - 8)       │
├────────────────────┼────────────────────┼───────────────────┼────────────────────┤
│ Quick Wins &       │ Core Skills &      │ DMS Workflow      │ Automation Tooling │
│ Heuristic Infusion │ TypeScript Overlay │ Adaptation        │ & Visual Engine    │
│                    │                    │                   │                    │
│ - systematic-debug │ - design-deep-mod  │ - workflows/debug │ - HTML Report CLI  │
│   feedback-loop    │ - scaffold-wizard  │ - BA/PM Socratic  │ - Interactive Bash │
│ - plan-delivery    │ - socratic-grill   │   Grilling        │   Wizard Library   │
│   tracer-bullets   │ - overlay TS Craft │ - PHP Deptrac     │ - CI/CD SARIF Auto │
│ - @reviewer 2-axis │ - 21 Gates pass    │ - 4 Gates pass    │   Reporting        │
└────────────────────┴────────────────────┴───────────────────┴────────────────────┘
```

### 10.1 Kế Hoạch Phân Kỳ 4 Giai Đoạn (Phases 1 – 4)

#### Giai Đoạn 1: Quick Wins & Bơm Heuristics Vào Hệ Thống Hiện Hữu (Tuần 1 – Tuần 2)
- **Mục tiêu**: Nâng cấp tư duy kỹ thuật của các core skills hiện có mà không làm thay đổi cấu trúc bảng registry hay tạo file mới.
- **Nội dung công việc**:
  1. Cập nhật `core/skills/foundation/systematic-debugging/SKILL.md` trong `agent-skills`: Nhúng kỷ luật tight feedback-loop-first, thu nhỏ tối thiểu repro, và chuẩn hóa 3–5 giả thuyết falsifiable.
  2. Cập nhật `core/skills/foundation/plan-technical-delivery/SKILL.md`: Nhúng kỹ thuật tracer-bullet vertical slicing và expand-contract refactoring.
  3. Cập nhật tài liệu hướng dẫn của vai trò `@reviewer`: Bổ sung hướng dẫn rà soát mã 2 trục độc lập và bảng 12 mùi mã nguồn Fowler.
- **Tiêu chuẩn nghiệm thu (DoD)**:
  - 100% các file chỉnh sửa giữ nguyên chiều dài $\le 200$ dòng.
  - Chạy `python3 core/scripts/validate-all.py` đạt 21/21 gates PASS.
  - Chạy `pytest -q` đạt 946 passed.

#### Giai Đoạn 2: Xây Dựng Core Skills Mới & TypeScript Overlay (Tuần 3 – Tuần 4)
- **Mục tiêu**: Hiện thực hóa 3 kỹ năng cốt lõi mới và đóng gói gói chuyên đề TypeScript Craft cho `agent-skills`.
- **Nội dung công việc**:
  1. Soạn thảo 3 core skills mới: `core/skills/foundation/design-deep-modules/`, `core/skills/foundation/scaffold-hitl-wizard/`, và `core/skills/agent/socratic-design-interview/`.
  2. Gán quyền sở hữu Primary Owner cho `technical-architect` (cho `design-deep-modules`), `devops-engineer` (cho `scaffold-hitl-wizard`), và `business-analyst` (cho `socratic-design-interview`) trong `core/roles/`.
  3. Xây dựng overlay `overlays/typescript-craft/` và pack `packs/typescript-craft-team/`.
  4. Tái sinh toàn bộ index và registry (`generate-a2a-registry.py`, `generate-index.py`, `generate-tier1-index.py`).
- **Tiêu chuẩn nghiệm thu (DoD)**:
  - Cả 3 kỹ năng mới đều có schema hợp đồng đầu ra rõ ràng, vượt qua AST Security Scanner.
  - Số lượng kỹ năng tăng từ 184 lên 187; số gói tăng từ 17 lên 18; số overlay tăng từ 21 lên 22.
  - Toàn bộ 21 gates của `validate-all.py` vượt qua 100%.

#### Giai Đoạn 3: Chuyển Giao Quy Trình Vào `lotte-dms-agent` (Tuần 5 – Tuần 6)
- **Mục tiêu**: Nâng cấp năng lực chẩn đoán vi dịch vụ và phân tích nghiệp vụ cho hệ thống logistics DMS.
- **Nội dung công việc**:
  1. Cập nhật `workflows/debug.md` và `skills/senior-engineering/SKILL.md` trong DMS: Tách bạch rõ ranh giới Triage/RCA (`trace-data`, `incident`) và Sửa mã (`developer-be`); bắt buộc câu lệnh Docker test đỏ trước khi viết code kèm trait `DatabaseTransactions` để cô lập dữ liệu trên DB dùng chung (`martonline_oms`, `martonline_dms`).
  2. Cấu hình Hook Alignment trong `mcp-tool-map.yaml`: Ánh xạ các lệnh `docker compose exec ... test` hoặc `php artisan test` thành hành động `local_verify` cho `developer-be`, giải phóng false approval gates từ `check-policy.py`.
  3. Tích hợp từ vựng Deep Module vào `role/ta.md` và `role/tech-lead.md`.
  4. Tích hợp Socratic Grilling vào `role/ba.md` và `role/pm.md` cho các bài toán Wave Planning và COD Settlement.
  5. Thử nghiệm công cụ kiểm tra kiến trúc PHP (Deptrac) trên `orders-service`.
- **Tiêu chuẩn nghiệm thu (DoD)**:
  - Chạy `python3 scripts/validate-all.py` trong DMS đạt 4/4 suites PASS (`validate-dms`, `check-policy`, `validate-links`, `validate-agent-cards`).
  - Không phá vỡ bất kỳ quy tắc nào trong 9 chiều của Review Gate.

#### Giai Đoạn 4: Hoàn Thiện Tooling Tự Động Hóa & Báo Cáo Trực Quan (Tuần 7 – Tuần 8)
- **Mục tiêu**: Xây dựng các công cụ hỗ trợ tự động hóa trải nghiệm lập trình viên.
- **Nội dung công việc**:
  1. Xây dựng script tiện ích sinh báo cáo kiến trúc HTML độc lập (Tailwind/Mermaid) cho các đợt audit kiến trúc định kỳ trong workspace.
  2. Chuẩn hóa thư viện `wizard-library.sh` dùng chung cho toàn bộ các script devops và release trong `agent-skills`.
  3. Thiết lập dashboard theo dõi chỉ số chất lượng mã nguồn và sự tuân thủ hợp đồng A2A.
- **Tiêu chuẩn nghiệm thu (DoD)**:
  - Báo cáo HTML tự sinh trong thư mục tạm, mở được trên mọi trình duyệt ngoại tuyến, hiển thị trực quan sơ đồ Seams và Modules.
  - Hệ thống vận hành ổn định, sẵn sàng chuyển giao tài liệu hướng dẫn cho toàn bộ kỹ sư tác nhân.

### 10.2 Kế Hoạch Quản Lý Rủi Ro & Tiêu Chí Rollback
- **Điều Kiện Kích Hoạt Rollback Khẩn Cấp (Rollback Triggers)**:
  1. Bất kỳ cổng nào trong 21 Validation Gates của `agent-skills` bị đỏ sau khi tích hợp.
  2. Bất kỳ sự cố nào làm suy giảm hiệu năng xử lý hoặc gây timeout (504) trên các truy vấn đơn hàng của DMS.
  3. Xuất hiện vi phạm Lethal Trifecta hoặc cảnh báo bảo mật từ `check-policy.py`.
- **Quy Trình Rollback**:
  - Đối với `agent-skills`: Do toàn bộ các thay đổi được kiểm soát chặt chẽ qua git nhánh tính năng, việc rollback được thực hiện bằng cách revert commit trên nhánh tính năng và chạy lại lệnh tái sinh index:
    `python3 core/scripts/generate-index.py && python3 core/scripts/validate-all.py`.
  - Đối với `lotte-dms-agent`: Mọi migration đều có phương thức `down()` được kiểm tra trước, và mã nguồn vi dịch vụ được khôi phục qua git tag phát hành gần nhất đã được kiểm chứng.

---

## 11. HƯỚNG DẪN TÁI HIỆN & KIỂM CHỨNG ĐỘC LẬP (VERIFICATION & AUDIT COMMANDS)

Để một kiểm toán viên độc lập (Independent Forensic Auditor) có thể xác minh tính chân thực của toàn bộ các quan sát, dữ liệu thống kê và kết luận trong báo cáo này, vui lòng thực thi tuần tự các tập lệnh sau trên môi trường Linux:

### 11.1 Xác Minh Kho Lưu Trữ Mục Tiêu `mattpocock/skills`
```bash
# 1. Chuyển vào thư mục clone của mattpocock/skills
cd /home/user/personalized/tmp/mattpocock-skills

# 2. Xác minh Git commit SHA và phiên bản package.json
git log -1 --oneline
# Kết quả mong đợi: 5863806 Merge pull request #1416 from mattpocock/software-factory-task-wording
node -p 'require("./package.json").version'
# Kết quả mong đợi: "1.3.2"

# 3. Xác minh tổng số lượng 39 kỹ năng và phân bổ 4 phân vùng
find skills -name SKILL.md | wc -l
# Kết quả mong đợi: 39

python3 -c '
import glob
skills = glob.glob("skills/**/SKILL.md", recursive=True)
buckets = [s.split("/")[1] for s in skills]
from collections import Counter
print(dict(Counter(buckets)))
'
# Kết quả mong đợi: {'engineering': 20, 'in-progress': 8, 'productivity': 7, 'misc': 4}

# 4. Xác minh lỗi cú pháp YAML thực tế trong software-factory/SKILL.md
python3 -c '
import yaml
with open("skills/in-progress/software-factory/SKILL.md") as f:
    parts = f.read().split("---")
    try:
        yaml.safe_load(parts[1])
        print("YAML Valid")
    except Exception as e:
        print("YAML Scanner Error Confirmed:", type(e).__name__)
'
# Kết quả mong đợi: YAML Scanner Error Confirmed: ScannerError

# 5. Xác minh sự thiếu hụt openai.yaml trong software-factory
ls skills/in-progress/software-factory/agents/openai.yaml 2>&1
# Kết quả mong đợi: No such file or directory (exit code 2)
```

### 11.2 Xác Minh Hệ Thống Đường Cơ Sở `agent-skills`
```bash
# 1. Chuyển vào thư mục agent-skills
cd /home/user/personalized/agent-skills

# 2. Chạy toàn bộ 21 Validation Gates
python3 core/scripts/validate-all.py
# Kết quả mong đợi:
# - Rules validation passed
# - Skill validation passed: 184 skills checked
# - Role validation passed: 39 roles checked
# - Workflow validation passed: 25 workflows checked
# - Pack validation passed: 17 packs checked
# - Overlay validation passed: 21 overlays checked
# - Contract validation passed: 63 schemas checked
# - AST Skill Security & Lethal Trifecta Scanner: 170 skills clean, 0 lethal violations
# - All core validators passed (Exit code: 0)

# 3. Chạy kiểm tra bộ unit test pytest
pytest -q
# Kết quả mong đợi: 946 passed, 9 skipped in ~55s (Exit code: 0)
```

### 11.3 Xác Minh Hệ Thống Đường Cơ Sở `lotte-dms-agent`
```bash
# 1. Chuyển vào thư mục lotte-dms-agent
cd /home/user/ldcc-mart/DMS/.agents

# 2. Xác minh phiên bản và cấu trúc
cat VERSION
# Kết quả mong đợi: 2.15.0

# 3. Chạy 4 cổng kiểm định tự động native của DMS
python3 scripts/validate-all.py
# Kết quả mong đợi:
# === Suite: dms ===
#   [PASS] validate-dms
#   [PASS] check-policy
#   [PASS] validate-links
#   [PASS] validate-agent-cards
# Summary: 4/4 passed (Exit code: 0)
```

### 11.4 Xác Minh Tính Bất Biến Của Mã Nguồn (Zero Modification Invariant)
```bash
# Xác nhận không có commit, tag hay push nào được tạo
cd /home/user/personalized/agent-skills && git status --short
cd /home/user/ldcc-mart/DMS/.agents && git status --short
# Kết quả mong đợi: Không có commit hoặc file source code nghiệp vụ nào bị sửa đổi bởi báo cáo này.
```

---
*Báo cáo nghiên cứu được biên soạn công phu, chuẩn mực và bảo đảm tính toàn vẹn kỹ thuật cao nhất.*  
*Được lưu trữ chính thức tại:* `agent-skills/reports/mattpocock-skills-research.md`  
*Bản quyền phân tích kỹ thuật © 2026 AI Agent Engineering Team.*
