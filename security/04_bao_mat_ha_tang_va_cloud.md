# BẢO MẬT HẠ TẦNG VÀ CLOUD (Infrastructure & Cloud Security)

## 1. Thiết lập & Kiến trúc Hệ thống Mạng (Network Security)

- **Network Segmentation (Phân mảnh mạng)**: Phân tách hệ thống thành các VPC/Subnet độc lập (Public, Private). Database và các service nội bộ tuyệt đối không được expose trực tiếp ra ngoài Internet.
- **Zero Trust Network**: Mọi luồng giao tiếp giữa các service (Service-to-Service communication) đều phải được xác thực. Phương pháp phổ biến nhất là sử dụng mTLS (Mutual TLS). Tuyệt đối không có tư duy "cùng dải IP nội bộ thì tin tưởng nhau".
- **Multi-tenant Isolation (Cô lập đa khách thuê)**: (Rất quan trọng cho các dự án SaaS hoặc HRM Agent Platform).
  - *Logical Isolation*: Gắn `tenant_id` ở mọi luồng query. Áp dụng Row-Level Security (RLS) của database (ví dụ PostgreSQL).
  - *Physical Isolation*: (Dành cho compliance cấp cao), chia database riêng hoặc ít nhất là schema riêng biệt theo tenant.
  - Chú ý rủi ro rò rỉ chéo khi sử dụng Cache chung (Redis) hay Vector DB. Cần namespace/collection tách biệt.
- **Infrastructure as Code (IaC)**: Dùng công cụ Terraform, Pulumi để quản lý hạ tầng bằng code. Phải đưa vào Version Control, require code-review trước khi Apply, hạn chế tối đa việc cấu hình tay trên giao diện web (click-ops) gây sai lệch, khó tracking.
- Áp dụng triệt để Least Privilege cho các IAM Role của dịch vụ. KHÔNG dùng root account hay admin key nạp vào các app.

## 2. Cloud & Container Security

- **Container Image**: Quét lỗ hổng image liên tục (bằng Trivy, Grype). Ưu tiên dùng các Base Image tối giản (Distroless, Alpine) để thu hẹp attack surface. 
- **Kubernetes Security**: 
  - KHÔNG chạy container với quyền `root` bên trong k8s.
  - Sử dụng **NetworkPolicy** để giới hạn luồng traffic giữa các pod với nhau.
  - Tuân thủ Pod Security Standards. 
  - Quản lý Secret an toàn (Sử dụng External Secrets Operator, AWS Secrets Manager...). KHÔNG hardcode secret trong file manifest k8s.
- **Cloud Misconfiguration (Sai sót cấu hình Cloud)**: Là nguyên nhân lớn nhất gây rò rỉ dữ liệu. Các lỗi phổ biến: S3 Bucket để public, Security Group mở toang tất cả các port (`0.0.0.0/0`), IAM Policy cấp quyền dấu sao (`*`).
- **CSPM (Cloud Security Posture Management)**: Sử dụng các công cụ (AWS Config, Wiz, Prisma Cloud) để tự động giám sát, quét và cảnh báo cấu hình sai lệch liên tục trên môi trường Cloud.

## 3. Hệ thống Giám sát & Theo dõi (Monitoring, Logging, Detection)

- **Centralized Logging (Log tập trung)**: (ELK, Loki, Datadog...) Gom toàn bộ log về một nguồn tập trung, không để rải rác ở từng server gây khó khăn cho việc tra cứu khi có sự cố.
- **SIEM (Security Information and Event Management)**: Tổng hợp log và tự động phân tích phát hiện pattern lạ/bất thường (Splunk, Wazuh).
- **Audit Trail**: Hệ thống phải lưu vết chi tiết "Ai - Làm gì - Khi nào - Từ IP/Vị trí nào" đối với các thao tác dữ liệu nhạy cảm.
- **Alerting (Cảnh báo)**: Cấu hình các ngưỡng báo động (Ví dụ: login fail liên tục, lượng traffic tăng đột biến bất thường, truy cập dữ liệu quan trọng ngoài giờ hành chính).
- **Network IDS/IPS**: Hệ thống phát hiện và ngăn chặn xâm nhập (Snort, Suricata).
- **Honeypot / Honeytoken**: Cố tình đặt "bẫy" giả mạo trong hạ tầng để sớm phát hiện dấu vết của kẻ tấn công đang thăm dò bên trong hệ thống.
- **Distributed Tracing (OpenTelemetry)**: Không chỉ dùng để debug lỗi logic mà còn giúp phát hiện các hành vi gọi chuỗi service/agent bất thường.

> *Lưu ý: Đối với yêu cầu lưu log bất biến (Immutable Audit Logging) ở cấp độ cao, vui lòng xem [File 13: Yếu Tố Con Người & Mật Mã Học](13_nhan_thuc_bao_mat_va_mat_ma_hoc.md).*

## 4. Resilience & Availability (Khả năng chịu lỗi và tính Sẵn sàng)

- **DDoS Protection**: Có lớp bảo vệ (Cloudflare, AWS Shield) và áp dụng Rate limit ở ngay khu vực rìa (Edge) của hệ thống.
- **Redundancy (Dự phòng)**: Triển khai hạ tầng Multi-AZ (nhiều Availability Zone), thiết lập Failover tự động.
- **Backup & Disaster Recovery (DR)**: 
  - Xác định rõ ràng các chỉ số RTO (thời gian phục hồi tối đa) và RPO (lượng dữ liệu cho phép mất tối đa). 
  - Backup định kỳ là chưa đủ. Phải diễn tập quá trình **Restore thật** để đảm bảo bản backup không bị lỗi khi cần.
- **Chaos Engineering**: (Mức độ nâng cao) - Chủ động tạo ra các sự cố có kiểm soát trong hệ thống (như Chaos Monkey của Netflix) để kiểm thử sức chịu đựng và khả năng tự phục hồi của hạ tầng.

## 5. Bảo mật thiết bị nhân viên (Endpoint Security & Corporate IT)

Đây thường là **điểm yếu nhất** trong thực tế vì hầu hết các cuộc tấn công (phishing, ransomware, đánh cắp credential) bắt đầu từ endpoint của nhân viên chứ không phải hạ tầng cloud.

### 5.1 Quản lý thiết bị (MDM/UEM)
- Triển khai Mobile Device Management / Unified Endpoint Management (Microsoft Intune, Jamf, Google Workspace Endpoint Management) để:
  - Bắt buộc mã hóa ổ đĩa (FileVault/BitLocker).
  - Bắt buộc màn hình khóa tự động sau X phút.
  - Xóa dữ liệu từ xa (remote wipe) khi thiết bị mất/nhân viên nghỉ việc.
  - Kiểm soát cài đặt app ngoài whitelist trên thiết bị công ty.

### 5.2 EDR/XDR thay vì Antivirus truyền thống
- Antivirus truyền thống chỉ dựa vào signature, không phát hiện được kỹ thuật tấn công mới (fileless malware, living-off-the-land).
- EDR (Endpoint Detection & Response) — CrowdStrike, SentinelOne, Microsoft Defender for Endpoint — giám sát hành vi bất thường theo thời gian thực, cho phép cô lập máy bị nhiễm từ xa.
- XDR mở rộng thêm việc tương quan dữ liệu giữa endpoint, network, email, cloud để phát hiện tấn công đa điểm.

### 5.3 VPN / Zero Trust Network Access (ZTNA)
- VPN truyền thống cấp quyền truy cập toàn mạng nội bộ một khi đã kết nối — rủi ro cao nếu credential bị đánh cắp.
- ZTNA (Cloudflare Access, Tailscale, Zscaler Private Access) áp dụng nguyên tắc "never trust, always verify": xác thực từng request theo identity + device posture, chỉ cấp quyền truy cập đúng ứng dụng cần thiết (least privilege), không lộ toàn bộ mạng nội bộ.
- Nên kết hợp MFA bắt buộc cho mọi truy cập VPN/ZTNA.

### 5.4 Bảo mật vật lý (Physical Security)
- **Clean desk policy**: không để tài liệu nhạy cảm, thiết bị lưu trữ, giấy note chứa mật khẩu trên bàn làm việc khi rời đi.
- **Chống Tailgating**: nhân viên không giữ cửa cho người lạ theo sau vào khu vực bảo mật; dùng thẻ từ/vân tay cho từng cá nhân, camera giám sát lối vào.
- **Quản lý thiết bị khách/nhà thầu**: mạng guest tách biệt hoàn toàn khỏi mạng nội bộ; giới hạn thời gian truy cập.
- **Bảo mật phòng server/rack** (nếu có on-premise): kiểm soát ra vào, log truy cập vật lý.

### 5.5 Các điểm bổ sung khác
- **Email security**: DMARC/DKIM/SPF cho domain công ty để chống giả mạo email; anti-phishing gateway; đào tạo nhân viên nhận diện phishing định kỳ (phishing simulation).
- **Patch management**: quy trình cập nhật OS/phần mềm định kỳ, không để endpoint chạy phiên bản lỗi thời có CVE đã biết.
- **USB/removable media control**: hạn chế hoặc chặn cổng USB trên máy chứa dữ liệu nhạy cảm để chống rò rỉ dữ liệu (data exfiltration).
- **Privileged Access Management (PAM)**: tài khoản admin của nhân viên IT phải được quản lý riêng, có ghi log, và dùng just-in-time access thay vì quyền admin thường trực.
