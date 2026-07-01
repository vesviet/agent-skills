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
