# 10. Quản Lý Định Danh và Truy Cập (IAM — Identity & Access Management)

*(Cấp độ Enterprise/Chính phủ: Tập trung vào Zero Trust và quản trị danh tính tập trung)*

## 10.1 Zero Trust Architecture (ZTA)
Nguyên tắc cốt lõi: **không tin tưởng ngầm định**, dù request đến từ bên trong hay bên ngoài mạng — mọi truy cập đều phải được xác thực và đánh giá lại liên tục.

**Zero Trust Policy Engine (góc độ code):**
- Không chỉ kiểm tra token một lần lúc login rồi tin cậy trong suốt phiên làm việc. Mỗi API call/function quan trọng nên đánh giá lại ngữ cảnh (**continuous authorization**):
  - Thiết bị gọi request có nằm trong danh sách thiết bị đã đăng ký/đạt chuẩn bảo mật (device posture) không?
  - IP/địa lý có bất thường so với hành vi thường ngày của user không (impossible travel)?
  - Token có bị revoke, hoặc risk score của phiên đăng nhập có tăng đột biến không?
- Kiến trúc gợi ý: tách riêng một **Policy Decision Point (PDP)** — thường dùng mô hình **ABAC** với engine như Open Policy Agent (OPA)/Rego — để mọi service gọi vào hỏi "request này có được phép không?" thay vì mỗi service tự viết logic phân quyền rời rạc.

## 10.2 RBAC vs ABAC
- **RBAC (Role-Based)**: gán quyền theo vai trò (Admin, Editor, Viewer) — đơn giản, dễ audit, nhưng cứng nhắc khi cần điều kiện phức tạp.
- **ABAC (Attribute-Based)**: quyết định quyền dựa trên nhiều thuộc tính (role + department + time-of-day + resource sensitivity + device trust) — linh hoạt hơn, phù hợp cho hệ thống lớn/multi-tenant, nhưng phức tạp hơn khi audit và debug.
- Thực tế enterprise thường dùng **kết hợp**: RBAC làm khung chính, ABAC cho các rule đặc biệt (ví dụ: chỉ cho truy cập dữ liệu y tế nếu user đang trong ca trực).

## 10.3 SSO, MFA, OAuth2/OIDC
- **SSO** (Single Sign-On) qua SAML hoặc OIDC để nhân viên dùng một danh tính cho toàn bộ hệ thống nội bộ — giảm số lượng mật khẩu rời rạc dễ bị lộ.
- **MFA** bắt buộc cho mọi tài khoản có quyền truy cập dữ liệu nhạy cảm, ưu tiên phương thức chống phishing (FIDO2/WebAuthn, security key) hơn SMS OTP (SMS dễ bị SIM-swap).
- **OAuth2/OIDC**: phân biệt rõ *Authentication* (OIDC — "bạn là ai") và *Authorization* (OAuth2 — "bạn được làm gì"). Lỗi phổ biến: dùng access token của OAuth2 để xác thực danh tính thay vì dùng ID token của OIDC.

## 10.4 Identity Lifecycle Management
- **Provisioning**: cấp quyền tự động theo template khi nhân viên/user mới được tạo (tránh cấp quyền thủ công dễ sai sót hoặc quá rộng).
- **De-provisioning**: đây là khâu hay bị bỏ sót nhất — khi nhân viên nghỉ việc/đổi phòng ban, quyền truy cập phải bị thu hồi **ngay lập tức**, không chỉ ở hệ thống chính mà cả các dịch vụ SaaS bên thứ ba đã cấp quyền.
- **Access Review định kỳ** (quarterly access certification): quản lý phải xác nhận lại định kỳ xem nhân viên có còn cần quyền đang có hay không — chống "quyền tích lũy" (privilege creep) theo thời gian.

## 10.5 Machine-to-Machine (M2M) Authentication
- Service-to-service không nên dùng static API key dài hạn. Ưu tiên:
  - **mTLS** (mutual TLS) giữa các service trong mesh (Istio, Linkerd).
  - **Short-lived JWT/token** cấp qua service account với thời hạn ngắn, tự động xoay vòng (rotation).
- Không hardcode credential M2M trong code/config — dùng secret manager (Vault, AWS Secrets Manager) với cơ chế inject runtime.
