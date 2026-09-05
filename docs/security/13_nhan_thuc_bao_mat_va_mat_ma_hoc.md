# 13. Yếu Tố Con Người & Mật Mã Học (Human Factor & Cryptography)

*(Cấp độ Enterprise/Chính phủ: Chống lại Insider Threat và chuẩn bị cho kỷ nguyên Post-Quantum)*

## 13.1 Con người — Phishing, Social Engineering, Insider Threat
- **Phishing simulation định kỳ**: gửi email giả lập để đo tỷ lệ nhân viên click/nhập credential, dùng làm chỉ số đào tạo (không dùng để trừng phạt cá nhân — mục tiêu là cải thiện nhận thức, không phải "bẫy" nhân viên).
- **Social Engineering** không chỉ qua email: vishing (giả danh qua điện thoại), pretexting (giả danh IT support xin cấp lại mật khẩu) — cần quy trình xác minh danh tính chuẩn trước khi thực hiện các thao tác nhạy cảm (reset password, cấp quyền).
- **Insider Threat**: rủi ro từ chính nhân viên (cố ý hoặc vô ý). Giảm thiểu bằng: least privilege, tách biệt nhiệm vụ (segregation of duties — người phê duyệt không phải người thực thi), giám sát hành vi bất thường (UEBA — User & Entity Behavior Analytics).
- **Security Awareness Training**: nên định kỳ (không chỉ 1 lần lúc onboard), có nội dung cập nhật theo xu hướng tấn công mới (ví dụ: deepfake voice trong social engineering hiện đang gia tăng).

## 13.2 Cryptography — Key Management
- **KMS (Key Management Service)**: quản lý vòng đời khóa mã hóa tập trung (tạo, xoay vòng, thu hồi), tách biệt khóa khỏi dữ liệu được mã hóa.
- **HSM (Hardware Security Module) — góc độ code:**
  - Với hệ thống yêu cầu bảo mật cực cao (ngân hàng, chính phủ), private key **không bao giờ** được tạo ra hoặc tồn tại dạng plaintext trong bộ nhớ ứng dụng.
  - Mọi thao tác ký số/giải mã phải gọi qua API của HSM chuyên dụng (thiết bị phần cứng hoặc cloud HSM như AWS CloudHSM) — HSM thực hiện phép toán mật mã nội bộ và chỉ trả về kết quả, key không bao giờ rời khỏi thiết bị.
- **Vòng đời chứng chỉ TLS/SSL**: tự động hóa renew (Let's Encrypt/ACME) để tránh hết hạn gây downtime; giám sát certificate transparency log để phát hiện chứng chỉ giả mạo domain của mình.
- **Thuật toán được phép dùng**: có whitelist rõ ràng (AES-256, RSA-2048+ hoặc ECC, SHA-256+) và **blacklist** thuật toán cũ (MD5, SHA-1, DES, RC4) — nên có static analysis/linter chặn việc dùng thuật toán yếu ngay trong CI/CD.

## 13.3 Immutable Audit Logging
- Mọi hành động của user, đặc biệt admin/DBA, phải được ghi log **không thể sửa đổi**:
  - Log được hash theo chuỗi (mỗi entry chứa hash của entry trước — tương tự blockchain) hoặc ký điện tử (cryptographic signing) để phát hiện nếu log bị chỉnh sửa.
  - Lưu log ở hệ thống tách biệt quyền truy cập với hệ thống chính — kể cả DBA có quyền cao nhất trên DB chính cũng không có quyền sửa log ở kho log riêng.
  - Mục tiêu: đảm bảo tính **non-repudiation** — không ai (kể cả admin) có thể chối bỏ hành động đã thực hiện hoặc phi tang bằng chứng.

## 13.4 Chuẩn bị cho Post-Quantum Cryptography (PQC)
- Máy tính lượng tử trong tương lai có thể phá vỡ các thuật toán bất đối xứng hiện tại (RSA, ECC) qua thuật toán Shor.
- Hướng chuẩn bị hiện tại (không cần làm ngay, nhưng nên thiết kế để không bị khóa cứng):
  - Chọn thuật toán đã được NIST chuẩn hóa cho PQC (CRYSTALS-Kyber cho key exchange, CRYSTALS-Dilithium cho chữ ký số).
  - Thiết kế hệ thống theo hướng **crypto-agility**: key length và signature size có thể thay đổi được (PQC signature thường lớn hơn nhiều so với ECC hiện tại) mà không phải sửa lại toàn bộ schema database/API contract.
  - Áp dụng **hybrid approach** trong giai đoạn chuyển tiếp: kết hợp thuật toán cổ điển + PQC song song để vừa an toàn với công nghệ hiện tại vừa chuẩn bị cho tương lai.
