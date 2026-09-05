# TIÊU CHUẨN & NGUYÊN TẮC THIẾT KẾ

Tài liệu này đề cập đến các tiêu chuẩn, framework tham chiếu và những nguyên tắc kiến trúc cốt lõi cần áp dụng trong thiết kế bảo mật.

## 1. Tiêu chuẩn / Framework Tham Chiếu

| Tiêu chuẩn | Phạm vi & Ứng dụng |
|---|---|
| **OWASP Top 10** | Danh sách lỗ hổng ứng dụng web phổ biến nhất — Kiến thức bắt buộc khởi điểm. |
| **OWASP API Security Top 10** | Dành riêng cho rủi ro trên API. |
| **OWASP ASVS** | Application Security Verification Standard — Checklist chi tiết theo từng cấp độ bảo mật. |
| **NIST 800-53 / NIST CSF** | Framework quản trị rủi ro an ninh thông tin của Mỹ, dùng rộng rãi trong doanh nghiệp. |
| **ISO/IEC 27001** | Chuẩn quốc tế về hệ thống quản lý an ninh thông tin (ISMS). |
| **CIS Controls / Benchmarks** | Các checklist cấu hình cứng hóa (hardening) hệ thống, OS, Cloud. |
| **PCI-DSS** | Bắt buộc tuân thủ nếu hệ thống xử lý dữ liệu thẻ thanh toán. |
| **GDPR / Nghị định 13/2023 (VN)** | Yêu cầu pháp lý về bảo vệ dữ liệu cá nhân (đặc biệt quan trọng đối với dữ liệu người dùng). |
| **SOC 2** | Chứng nhận thường yêu cầu khi bán giải pháp B2B / Enterprise (chứng minh hệ thống an toàn). |
| **MITRE ATT&CK** | Ma trận kỹ thuật tấn công thực tế — Dùng để mô hình hóa và đánh giá khả năng phòng thủ của hệ thống. |

## 2. Nguyên Tắc Thiết Kế Cốt Lõi

- **Principle of Least Privilege (Quyền tối thiểu)**: Chỉ cấp quyền hạn thấp nhất, vừa đủ để thực hiện một tác vụ.
- **Defense in Depth (Bảo vệ nhiều lớp)**: Áp dụng nhiều lớp bảo mật độc lập (ví dụ: Firewall → WAF → API Gateway → App-level Auth → DB Permissions).
- **Zero Trust (Không tin tưởng mặc định)**: Không có khái niệm "mạng nội bộ an toàn". Mọi user, thiết bị, và service-to-service communication đều phải được xác thực và ủy quyền liên tục.
- **Fail Securely (Lỗi an toàn)**: Khi có ngoại lệ hoặc hệ thống bị sập, nó phải chuyển về trạng thái từ chối truy cập (deny by default), thay vì mở toang quyền hoặc rò rỉ stack trace.
- **Secure by Default (An toàn mặc định)**: Các cấu hình mặc định (khi vừa cài đặt/triển khai) phải là lựa chọn an toàn nhất, không phải tiện lợi nhất.
- **Separation of Duties (Phân tách nhiệm vụ)**: Không để một cá nhân hoặc một component có toàn quyền sinh-sát hệ thống từ đầu đến cuối.
- **Economy of Mechanism (KISS - Keep It Simple, Stupid)**: Thiết kế và cơ chế bảo mật càng đơn giản càng ít tiềm ẩn lỗ hổng.
- **Complete Mediation (Kiểm soát hoàn toàn)**: Mọi nỗ lực truy cập vào tài nguyên đều phải được kiểm tra qua cơ chế kiểm soát truy cập; không được có đường vòng hay bypass.
- **Don't Trust User Input**: Nguyên tắc tối thượng. Mọi dữ liệu từ bên ngoài (kể cả HTTP headers, API payload, hay files upload) đều là dữ liệu không tin cậy.

## 3. Mẫu Thiết Kế Bảo Mật (Security Design Patterns)

- **Gatekeeper Pattern**: Dùng một service trung gian (như API Gateway) làm điểm kiểm soát tập trung (auth, rate limit, logging) trước khi request đi vào các service lõi.
- **Sidecar Pattern (Service Mesh)**: Tách riêng logic bảo mật (như mTLS, authorization) khỏi business logic bằng cách đặt nó vào một sidecar proxy (VD: Istio, Linkerd) chạy song song với ứng dụng.
- **Circuit Breaker**: Cắt đứt các kết nối lỗi để ngăn tình trạng quá tải hoặc tấn công lan truyền gây sập toàn bộ hệ thống (cascading failure).
- **Bulkhead Pattern**: Phân vùng/cô lập tài nguyên để nếu một module bị tấn công hay cạn kiệt tài nguyên, các module khác vẫn hoạt động bình thường.
- **Token-based Delegation (như OAuth2)**: Các service ủy quyền cho nhau thông qua token sinh ra động thay vì chia sẻ chung một credential cố định/hardcode.
- **Immutable Infrastructure**: Hệ thống máy chủ, container không được can thiệp cấu hình trực tiếp trên production. Mọi thay đổi đều phải thông qua việc build lại image và redeploy mới. (Giảm thiểu backdoor, cấu hình sai lệch).

## 4. Privacy Engineering (Kỹ thuật Quyền riêng tư)

*Đây là tư duy từ khâu thiết kế (Privacy-by-design), khác với bảo vệ dữ liệu (Data Protection) chỉ tập trung mã hóa lúc lưu trữ.*

- **Data Minimization (Tối thiểu hóa dữ liệu)**: Chỉ thu thập những dữ liệu thực sự cần thiết. Dữ liệu không tồn tại thì không thể bị rò rỉ.
- **Purpose Limitation (Giới hạn mục đích)**: Dữ liệu thu thập cho mục đích A không được ngấm ngầm sử dụng cho mục đích B.
- **Right to be Forgotten / Data Retention**: Phải có quy trình xóa dữ liệu sạch sẽ, triệt để (Bao gồm cả trong Backup, Log, Vector DB — điểm dễ bị bỏ sót trong hệ RAG, nơi embedding cũ vẫn giữ thông tin bị xóa).
- *Lưu ý*: Với các dự án như **OmniMer Health**, dữ liệu sức khỏe cực kỳ nhạy cảm. Cần thiết kế privacy ngay từ schema (ví dụ chia nhỏ dữ liệu định danh người dùng khỏi dữ liệu bệnh án).

## 5. Cryptographic Agility (Tính linh hoạt về mã hóa)

- **Không Hardcode thuật toán**: Cấu trúc hệ thống cần cho phép thay đổi thuật toán mã hóa (hoặc đổi Key) nhanh chóng mà không cần phải đập đi viết lại (Versioned encryption scheme).
- **Post-Quantum Readiness**: Tuy chưa khẩn cấp ngay lập tức, nhưng các chuẩn mã hóa mới chống lại máy tính lượng tử (từ NIST) đang hình thành. Nếu hệ thống lưu dữ liệu nhạy cảm có vòng đời 10-20 năm, kiến trúc hiện tại cần có không gian để nâng cấp sau này.
