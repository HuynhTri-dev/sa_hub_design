# BẢO MẬT TẦNG ỨNG DỤNG (Application Security)

Tài liệu này đi sâu vào các yếu tố bảo mật của phần mềm (mã nguồn, framework, xử lý dữ liệu...).

## 1. Authentication & Authorization (Xác thực & Phân quyền)

**Cơ bản:**
- **Mật khẩu**: Hash bằng bcrypt / argon2 / scrypt (KHÔNG dùng MD5/SHA1 trần), salt riêng biệt từng user.
- **MFA/2FA**: Ưu tiên TOTP, WebAuthn/FIDO2. (SMS tiềm ẩn rủi ro SIM-swap, chỉ nên làm phương án backup).
- **Session management**: Dùng `httpOnly` + `secure` + `SameSite` cookie. Thiết lập timeout hợp lý, phải invalidate phiên bản khi user logout hoặc đổi mật khẩu.
- **JWT**: Phải có thời hạn `exp`, ký bằng thuật toán mạnh (RS256 tốt hơn HS256 nếu có nhiều service). **Lưu ý**: JWT chỉ encode (mã hóa chuẩn) chứ không encrypt (mã hóa bảo mật) nên tuyệt đối KHÔNG nhét dữ liệu nhạy cảm vào payload.

**Nâng cao:**
- **Mô hình phân quyền**: Nâng cấp từ RBAC (Role-Based) → ABAC (Attribute-Based) → ReBAC (Relationship-Based) tùy theo độ phức tạp của hệ thống.
- **Broken Access Control / IDOR**: Luôn kiểm tra quyền truy cập ở **backend**. Không tin tưởng object ID (như user_id, order_id) truyền lên từ frontend (qua URL hoặc body).
- **OAuth2/OIDC**: Cài đặt đúng chuẩn, bắt buộc có PKCE cho các public client. Tránh lỗi cấu hình như `redirect_uri` không validate chặt dẫn đến rủi ro Open Redirect hoặc Token Theft.

> *Lưu ý: Để tìm hiểu sâu về kiến trúc định danh tổng thể (Zero Trust, Identity Lifecycle, M2M), vui lòng tham khảo [File 10: Quản Lý Định Danh và Truy Cập](10_quan_ly_danh_tinh_va_truy_cap.md).*

## 2. Input Validation & Injection (Xử lý dữ liệu đầu vào)

**Cơ bản:**
- Validate mọi dữ liệu ở **server-side** (validate client-side chỉ để tăng UX, hoàn toàn vô dụng về mặt bảo mật).
- Dùng **Parameterized queries / ORM** để chống SQL Injection.
- **Escape output** theo bối cảnh hiển thị (HTML, JS, URL, SQL) để chống XSS.
- Ưu tiên sử dụng **Whitelist** (danh sách trắng cho phép) thay vì Blacklist (danh sách đen chặn) khi validate.

**Nâng cao:**
- **SSRF (Server-Side Request Forgery)**: Nếu server có tính năng tự fetch URL ra ngoài (webhook, image download), cần validate/whitelist domain. Chặn truy cập metadata endpoint nội bộ (vd: `169.254.169.254` trên môi trường cloud).
- **Deserialization**: Tuyệt đối không deserialize các định dạng phức tạp (như Python pickle, Java serialization) từ dữ liệu không an toàn → Dẫn đến lỗ hổng RCE.
- **Template Injection (SSTI)**: Xảy ra nếu dùng template engine (Jinja2, Handlebars) với input động.
- **XXE**: Quản lý rủi ro khi hệ thống xử lý file/dữ liệu XML.

*(Ghi chú: Lỗi về Prompt Injection của AI được tách riêng ở tài liệu **Bảo mật AI & Agent**).*

## 3. Data Protection (Bảo vệ dữ liệu)

**Cơ bản:**
- **TLS 1.2+**: Bắt buộc cho mọi kết nối dữ liệu đang truyền tải (In-transit).
- **Encryption At-rest**: Mã hóa dữ liệu tĩnh lưu trữ (AES-256), đặc biệt các trường thông tin cá nhân (PII, Sức khỏe).
- **Secret Management**: Tuyệt đối không hardcode API key / mật khẩu trong mã nguồn. Dùng biến môi trường (Environment variables) tối thiểu, hoặc tốt nhất là Vault (như HashiCorp Vault, AWS Secrets Manager).
- **Logging**: Không ghi (log) các thông tin nhạy cảm như password, token, PII ra log file.

**Nâng cao:**
- **Key management**: Rotate (xoay vòng) key định kỳ. Sử dụng Envelope Encryption: tách biệt key mã hóa dữ liệu (DEK) và key mã hóa key (KEK).
- **Data masking/tokenization**: Che khuất dữ liệu khi hiển thị (vd: số thẻ tín dụng `**** **** **** 1234`).
- **Field-level encryption**: Không chỉ mã hóa full DB, mà mã hóa cấp độ field cho những dữ liệu cực kỳ nhạy cảm.
- **Data residency**: Tuân thủ luật pháp (VD: Dữ liệu người dùng VN phải lưu ở VN theo Nghị định 53/2022).
- **Backup an toàn**: Mã hóa backup, tách quyền truy cập backup khỏi hệ thống chính (chống ransomware xóa toàn bộ hệ thống lẫn backup), và phải test quá trình restore định kỳ.

## 4. API Security (Bảo mật giao tiếp API)

**Cơ bản:**
- Rate limiting / Throttling theo User và theo IP.
- Validation Input Schema bằng thư viện (Pydantic, Joi, OpenAPI Schema) để chặn payload dị dạng, quá tải lớn.
- **CORS**: Cấu hình đúng nguồn gốc (Origin), KHÔNG dùng `*` nếu API có liên kết với credentials (cookies, tokens).
- Versioning rõ ràng để dễ quản lý nâng cấp/hủy API cũ an toàn.

**Nâng cao:**
- Sử dụng **API Gateway** làm lá chắn tập trung: Quản lý Auth, Rate limit, Logging, WAF rule...
- **GraphQL-specific risks**: Giới hạn Query Depth (tránh DoS qua nested query), Disable Introspection ở môi trường Production.
- **Mass Assignment**: Không gán trực tiếp toàn bộ dữ liệu body request vào Object Model (VD: Kẻ tấn công cố tình truyền thêm trường `role: admin` để leo thang đặc quyền).

## 5. Business Logic Security (Bảo vệ luồng nghiệp vụ)

Đây là các lỗ hổng không phải do lỗi code (syntax) mà do sai sót trong việc thiết kế luồng quy trình:
- **Race condition**: (VD: ấn nút thanh toán nhiều lần cùng lúc). Giải quyết: Dùng DB Lock, Idempotency key. Chú ý các lỗi sinh ra do thời gian lệch (TOCTOU - Time-of-check to time-of-use).
- **State machine violations**: Kẻ tấn công nhảy cóc quy trình, ví dụ bỏ qua OTP mà gọi thẳng API tạo lệnh chuyển tiền. Luôn phải check trạng thái hợp lệ (state machine) ở Backend.
- **Feature Abuse (Lợi dụng tính năng)**:
  - Dùng tính năng *Export* để ăn cắp dữ liệu, hoặc *Import* để chèn dữ liệu không qua validate.
  - *Search/Filter làm Oracle*: Kẻ tấn công dùng chức năng lọc để đoán xem dữ liệu (mà họ không có quyền xem) có tồn tại hay không thông qua response time.
  - Lộ lọt dữ liệu qua *Preview / Draft*.
- Cần có Audit log chặt chẽ (Ai làm gì, khi nào) cho mọi hành động thay đổi trạng thái của luồng nghiệp vụ nhạy cảm.

## 6. Cấu trúc Code & Chained Attacks

- **Separation of Concerns**: Phân chia ứng dụng thành nhiều tầng rõ ràng (Authentication, Business logic, Data access). Giảm thiểu thiệt hại (blast radius) khi một tầng bị thủng.
- **Dependency Injection**: Không để logic dính chặt vào raw SQL hay HTTP. Dễ dàng thay thế mock và unit test.
- **Chained attacks (Tấn công chuỗi)**: Lỗi nghiêm trọng thường bắt đầu từ chuỗi các lỗi nhỏ liên kết lại (Info Disclosure + Thiếu IDOR check + Thiếu Rate Limit = Lộ dữ liệu toàn hệ thống).
- **Second-order attacks**: Dữ liệu được đưa vào DB rất an toàn, nhưng khi lấy từ DB ra và render ở một module khác lại trở thành XSS/SSTI. Dữ liệu tin cậy ở module này chưa chắc đã an toàn cho ngữ cảnh của module khác.
