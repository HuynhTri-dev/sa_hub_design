# TỔNG HỢP BẢO MẬT HỆ THỐNG — TỪ CƠ BẢN ĐẾN NÂNG CAO

---

# PHẦN A — TẦNG PHẦN MỀM (Application Layer)

## A1. Authentication & Authorization (Xác thực & Phân quyền)

**Cơ bản:**
- Mật khẩu: hash bằng bcrypt/argon2/scrypt (KHÔNG dùng MD5/SHA1 trần), salt riêng từng user
- MFA/2FA (TOTP, WebAuthn/FIDO2, SMS chỉ nên là backup vì SIM-swap risk)
- Session management: httpOnly + secure + SameSite cookie, timeout hợp lý, invalidate khi logout/đổi mật khẩu
- JWT: có `exp`, ký bằng thuật toán mạnh (RS256 > HS256 khi có nhiều service), không nhét dữ liệu nhạy cảm vào payload (JWT chỉ encode, không encrypt)

**Nâng cao:**
- RBAC (Role-Based) → ABAC (Attribute-Based) → ReBAC (Relationship-Based, kiểu Google Zanzibar) tùy độ phức tạp hệ thống
- Broken Access Control / IDOR: luôn kiểm tra quyền ở **backend**, không tin tưởng dữ liệu từ client (object ID trong URL/body)
- Principle of Least Privilege: mỗi service account, mỗi user chỉ có đúng quyền cần thiết
- Zero Trust: không có "trusted internal network" — mọi request đều phải xác thực/authorize, kể cả nội bộ
- OAuth2/OIDC implementation đúng chuẩn (PKCE bắt buộc cho public client), tránh common misconfigurations (redirect_uri không validate chặt → open redirect/token theft)

## A2. Input Validation & Injection

**Cơ bản:**
- Validate mọi input ở server-side (client-side chỉ là UX, không phải bảo mật)
- Parameterized queries / ORM thay vì string concatenation (chống SQL Injection)
- Escape output theo context (HTML, JS, URL, SQL) — chống XSS
- Whitelist thay vì blacklist khi validate

**Nâng cao:**
- SSRF: validate/whitelist domain khi server tự gọi ra ngoài (webhook, fetch URL từ user), chặn truy cập metadata endpoint nội bộ (169.254.169.254 trên cloud)
- Deserialization: không deserialize dữ liệu không tin cậy (pickle Python, Java serialization) → RCE
- **Prompt Injection & AI/LLM Vulnerabilities** (Cực kỳ quan trọng với hệ AI/RAG/Agent):
  - *Direct injection*: User cố ép LLM bỏ qua system prompt.
  - *Indirect injection via retrieved content*: Mã độc không nằm ở user chat, mà nằm trong một file tài liệu (PDF, Web page) được RAG index. Khi Agent đọc file này để trả lời cho user khác, phiên làm việc của user đó bị chiếm quyền điều khiển.
  - *Tool-argument injection (Từ Model -> Sink)*: Khi LLM gọi Tool, các tham số nó sinh ra có thể chứa mã độc (SQLi, SSRF) và lừa hệ thống thực thi. Output của LLM phải được đối xử như "untrusted input" chứ không được tin tưởng hoàn toàn.
  - *Cross-session / Multi-tenant Context Bleed*: Lỗi bộ nhớ đệm (Prompt cache/Vector DB) hoặc bộ lọc (filter) khiến câu hỏi/dữ liệu của user này lọt vào context prompt của user khác.
  - *Phòng thủ*: Tách rõ system prompt/user input/retrieved content, sandbox tool-calling, output validation trước khi agent thực thi hành động có side-effect (gọi API, ghi DB).
- Template Injection (SSTI) nếu dùng template engine (Jinja2, Handlebars...) với input động
- XXE (XML External Entity) nếu hệ thống xử lý XML

## A3. Data Protection

**Cơ bản:**
- TLS 1.2+ bắt buộc cho mọi kết nối (in-transit)
- Mã hóa dữ liệu nhạy cảm at-rest (AES-256), đặc biệt PII, thông tin sức khỏe (nếu làm OmniMer Health cần chú ý theo chuẩn kiểu HIPAA)
- Không hardcode secret/API key trong code — dùng biến môi trường tối thiểu, tốt hơn là Vault
- Không log dữ liệu nhạy cảm (password, token, PII) ra log file

**Nâng cao:**
- Key management: rotate key định kỳ, tách biệt key mã hóa dữ liệu (DEK) và key mã hóa key (KEK) — envelope encryption
- Data masking/tokenization cho dữ liệu hiển thị (che số thẻ, số CCCD)
- Field-level encryption cho dữ liệu cực nhạy cảm (không chỉ mã hóa cả DB mà từng field)
- Data residency/sovereignty nếu có yêu cầu pháp lý (dữ liệu người dùng VN phải lưu ở VN theo Nghị định 53/2022)
- Backup: mã hóa, test restore định kỳ, tách quyền truy cập backup khỏi hệ thống chính (chống ransomware xóa cả backup)

## A4. API Security

**Cơ bản:**
- Rate limiting/throttling theo user, theo IP
- Input schema validation (OpenAPI schema, Pydantic...) — chặn payload dị dạng/quá lớn
- CORS cấu hình đúng (không dùng `*` khi có credential)
- Versioning rõ ràng, deprecate an toàn

**Nâng cao:**
- API Gateway làm điểm kiểm soát tập trung: auth, rate limit, logging, WAF rule
- GraphQL-specific risks: query depth limiting (chống DoS qua nested query), disable introspection ở production
- Mass assignment: không bind trực tiếp toàn bộ request body vào model (user có thể tự set field `role: admin`)
- Broken Object Level Authorization (BOLA) — lỗi phổ biến nhất trong OWASP API Security Top 10

## A5. Dependency & Supply Chain

**Cơ bản:**
- Quét lỗ hổng dependency định kỳ: `npm audit`, `pip-audit`, Snyk, Dependabot, Trivy
- Pin version, dùng lock file (`package-lock.json`, `poetry.lock`)
- Review license và nguồn gốc package trước khi thêm

**Nâng cao:**
- SBOM (Software Bill of Materials) — biết chính xác mọi thành phần trong hệ thống (chuẩn CycloneDX/SPDX)
- Chống typosquatting: kiểm tra kỹ tên package trước khi cài
- Sigstore/cosign: ký số artifact/container image để đảm bảo tính toàn vẹn
- CI/CD pipeline security: secret không lộ trong build log, branch protection, require review trước merge, không cho pipeline có quyền ghi vượt mức cần thiết

## A6. Business Logic Security (Lỗ hổng Logic Nghiệp Vụ & Lợi dụng tính năng)

- **Race condition**: Ví dụ double-submit trong thanh toán/đặt chỗ → dùng lock, idempotency key. Chú ý các lỗ hổng xảy ra giữa lúc check và lúc thao tác (Time-of-check to time-of-use - TOCTOU).
- **State machine violations**: Client bỏ qua bước xác thực OTP bằng cách gọi thẳng API bước sau. Luôn enforce state machine ở backend. Chú ý: Có thể nhảy cóc các bước không? Trạng thái khi rollback một nửa (partial failure) sẽ ra sao?
- **Feature Abuse (Lợi dụng tính năng hợp lệ)**:
  - *Export/Import Abuse*: Dùng tính năng Export để trộm data nháp/data bị xóa; dùng Import để ghi đè dữ liệu mà không qua hàm validate thông thường.
  - *Search/Filter as an Oracle*: Dùng tính năng tìm kiếm/lọc để "đoán" xem một dữ liệu (mà user không có quyền xem) có tồn tại hay không thông qua response time hoặc cách dữ liệu được sắp xếp (ordering).
  - *Preview/Draft Leakage*: Tính năng xem trước (preview) hoặc dữ liệu nháp có vô tình bị lộ qua API listing hay cache không?
- Rate limit riêng cho các action nhạy cảm (login, reset password, OTP) để chống brute-force.
- Đảm bảo mọi luồng nghiệp vụ có audit log (ai làm gì, khi nào).

## A7. Cấu trúc code & Secure SDLC

- **Secure by Design**: threat modeling ngay từ giai đoạn thiết kế (không phải "code xong mới nghĩ đến bảo mật")
- Code review bắt buộc, đặc biệt các module auth/payment/data access
- Static Analysis (SAST) tích hợp CI: SonarQube, Semgrep, Bandit (Python), ESLint security plugin
- Dependency Injection/interface tách biệt rõ layer (không để business logic dính chặt vào raw SQL/HTTP)
- Fail securely: khi lỗi xảy ra, hệ thống phải fail về trạng thái an toàn (deny by default), không lộ stack trace chi tiết ra ngoài production
- Separation of concerns: tách rõ authentication service, business logic, data access — giảm blast radius khi 1 phần bị compromise

## A8. Chained & Second-order Attacks (Chuỗi Tấn Công)

- **Chained attacks (Tấn công kết hợp)**: Các hành vi/lỗ hổng rủi ro thấp khi kết hợp lại tạo thành rủi ro cao. Ví dụ: Info disclosure (lộ resource ID) + IDOR (không check quyền) + Thiếu Rate limit = Brute-force toàn bộ dữ liệu. Open redirect + OAuth callback = Token theft.
- **Cross-component trust gaps (Khoảng trống tin cậy giữa các thành phần)**: Component A validate dữ liệu và truyền cho Component B. B có tin tưởng tuyệt đối A không? Việc validate của A có khớp với nhu cầu của B không? (VD: A cho phép 255 ký tự nhưng B cắt gọt đi còn 128, tạo ra một chuỗi hoàn toàn khác có thể chứa mã độc).
- **Second-order attacks (Tấn công gián tiếp)**: Dữ liệu an toàn lúc lưu trữ nhưng nguy hiểm khi lấy ra dùng ở bối cảnh khác. Ví dụ: một tên biến hợp lệ trong SQL nhưng lại trở thành mã độc khi đưa vào JSON path; một slug hợp lệ trong URL lại trở thành mã độc khi nối vào file path ở hệ thống backup.

---

# PHẦN B — TẦNG HẠ TẦNG (Infrastructure Layer)

## B1. Thiết lập & Kiến trúc hệ thống

- **Network segmentation**: tách VPC/subnet public-private, database không expose internet trực tiếp
- **Zero Trust Network**: mọi service-to-service communication đều phải xác thực (mTLS), không tin theo IP nội bộ
- **Defense in Depth**: nhiều lớp bảo vệ độc lập (firewall → WAF → API Gateway → app-level auth → DB permission)
- Multi-tenant isolation (rất liên quan tới HRM Agent Platform của bạn):
  - Logical isolation: tenant_id ở mọi query, row-level security (PostgreSQL RLS)
  - Physical isolation (khi cần compliance cao): schema riêng hoặc DB riêng theo tenant
  - Tránh cross-tenant data leak qua cache/vector DB chung (Qdrant/Neo4j namespace theo tenant)
- IaC (Infrastructure as Code — Terraform, Pulumi): version control hạ tầng, review trước khi apply, tránh click-ops gây cấu hình sai
- Least privilege cho IAM role — mỗi service chỉ có quyền cần thiết, không dùng root/admin key cho ứng dụng

## B2. Cloud & Container Security

- Container image: scan lỗ hổng (Trivy, Grype), dùng base image tối giản (distroless/alpine), không chạy container với quyền root
- Kubernetes: NetworkPolicy giới hạn traffic giữa pod, Pod Security Standards, secrets qua K8s Secrets/External Secrets Operator (không hardcode trong manifest)
- Cloud misconfiguration là nguyên nhân hàng đầu gây rò rỉ dữ liệu: S3 bucket public, security group mở toàn bộ port, IAM policy quá rộng
- Sử dụng CSPM (Cloud Security Posture Management) tool để tự động phát hiện misconfiguration: AWS Config, Wiz, Prisma Cloud

## B3. Hệ thống theo dõi (Monitoring, Logging, Detection)

- **Centralized logging**: ELK/Loki/Datadog — log tập trung, không nằm rải rác từng server
- **SIEM** (Security Information and Event Management): tổng hợp log, phát hiện pattern bất thường (Splunk, Elastic Security, Wazuh)
- Audit trail đầy đủ: ai truy cập gì, khi nào, từ đâu — đặc biệt với dữ liệu nhạy cảm
- Alerting: cấu hình ngưỡng cảnh báo (spike traffic lạ, login fail liên tục, truy cập ngoài giờ hành chính)
- **IDS/IPS** (Intrusion Detection/Prevention System): Snort, Suricata — phát hiện traffic bất thường ở tầng network
- Honeypot/honeytoken: đặt "bẫy" để phát hiện sớm kẻ tấn công đã xâm nhập
- Distributed tracing (OpenTelemetry) giúp vừa debug vừa phát hiện hành vi bất thường trong luồng gọi giữa các service/agent

## B4. Resilience & Availability

- DDoS protection: Cloudflare/AWS Shield, rate limit ở edge
- Redundancy: multi-AZ, failover tự động
- Backup & Disaster Recovery: RTO/RPO xác định rõ, test DR định kỳ (không chỉ backup mà phải test restore thật)
- Chaos Engineering (nâng cao): chủ động gây lỗi có kiểm soát để kiểm tra khả năng chống chịu (Netflix Chaos Monkey)

---

# PHẦN C — CON NGƯỜI & QUY TRÌNH VẬN HÀNH

## C1. Quy trình phát triển an toàn (Secure SDLC)

1. **Threat Modeling** ở giai đoạn thiết kế (STRIDE, PASTA framework)
2. **Secure coding guideline** cho team, training định kỳ
3. **Code review** bắt buộc trước merge, đặc biệt phần auth/payment
4. **SAST/DAST/SCA** tích hợp CI/CD pipeline
5. **Pentest** định kỳ (nội bộ hoặc thuê ngoài) — ít nhất 1-2 lần/năm hoặc trước mỗi release lớn
6. **Bug bounty program** nếu sản phẩm đủ lớn (HackerOne, Bugcrowd)

## C2. Quản lý vận hành

- **Incident Response Plan**: quy trình rõ ràng khi phát hiện breach — ai làm gì, thông báo ai, trong bao lâu
- **Patch management**: quy trình vá lỗ hổng theo mức độ nghiêm trọng (CVSS score), SLA vá (Critical: 24-48h)
- **Access review** định kỳ: rà soát ai đang có quyền gì, thu hồi quyền khi nhân viên nghỉ việc/đổi vai trò ngay lập tức
- **Change management**: mọi thay đổi hạ tầng/production phải qua review, có rollback plan

## C3. Con người

- Training nhận thức bảo mật (security awareness) cho toàn bộ nhân viên — phishing là vector tấn công phổ biến nhất
- Insider threat: nguyên tắc need-to-know, two-person rule cho hành động cực nhạy cảm
- Onboarding/offboarding checklist rõ ràng cho việc cấp/thu hồi quyền truy cập
- Background check với vị trí truy cập dữ liệu nhạy cảm (tùy ngành)

---

# PHẦN D — TIÊU CHUẨN & NGUYÊN TẮC THIẾT KẾ

## D1. Tiêu chuẩn/Framework tham chiếu

| Tiêu chuẩn | Phạm vi |
|---|---|
| **OWASP Top 10** | Lỗ hổng web phổ biến nhất — điểm khởi đầu bắt buộc phải biết |
| **OWASP API Security Top 10** | Riêng cho API |
| **OWASP ASVS** | Application Security Verification Standard — checklist chi tiết theo từng level |
| **NIST 800-53 / NIST CSF** | Framework quản trị an ninh thông tin (Mỹ, dùng rộng rãi) |
| **ISO/IEC 27001** | Chuẩn quốc tế về hệ thống quản lý an ninh thông tin (ISMS) |
| **CIS Controls / CIS Benchmarks** | Checklist cấu hình cứng hóa (hardening) hệ thống, cloud |
| **PCI-DSS** | Bắt buộc nếu xử lý thẻ thanh toán |
| **GDPR / Nghị định 13/2023 (VN)** | Bảo vệ dữ liệu cá nhân |
| **SOC 2** | Chứng nhận thường yêu cầu khi bán B2B/enterprise |
| **MITRE ATT&CK** | Ma trận kỹ thuật tấn công thực tế — dùng để đánh giá khả năng phòng thủ |

## D2. Nguyên tắc thiết kế cốt lõi

- **Principle of Least Privilege** — chỉ cấp quyền tối thiểu cần thiết
- **Defense in Depth** — nhiều lớp bảo vệ độc lập
- **Zero Trust** — không tin bất kỳ ai/thứ gì theo mặc định, xác thực mọi lúc
- **Fail Securely** — lỗi phải fail về trạng thái an toàn, không mở toang
- **Secure by Default** — cấu hình mặc định phải là an toàn nhất, không phải tiện nhất
- **Separation of Duties** — không để 1 người/1 component có toàn quyền
- **Economy of Mechanism (KISS)** — hệ thống bảo mật càng đơn giản càng ít lỗi
- **Complete Mediation** — mọi truy cập đều phải qua kiểm tra, không có "đường tắt"
- **Don't trust user input** — nguyên tắc số 1 trong secure coding

## D3. Mẫu thiết kế bảo mật (Security Design Patterns)

- **Gatekeeper pattern**: một service trung gian kiểm soát mọi truy cập vào hệ thống lõi
- **Sidecar pattern (service mesh)**: tách logic bảo mật (mTLS, auth) ra khỏi business logic — Istio/Linkerd
- **Circuit breaker**: ngăn lỗi/tấn công lan truyền giữa các service
- **Bulkhead pattern**: cô lập tài nguyên giữa các module để 1 phần bị tấn công không kéo sập toàn hệ thống
- **Token-based delegation (OAuth2)**: không share credential trực tiếp giữa service
- **Immutable infrastructure**: server không được sửa trực tiếp, mọi thay đổi qua rebuild/redeploy — giảm khả năng bị cài backdoor âm thầm

---

# PHẦN E — KỸ THUẬT & CÔNG CỤ TÌM KIẾM, KHAI THÁC LỖ HỔNG (để fix)

> Mục tiêu: hiểu góc nhìn tấn công để phòng thủ tốt hơn (offensive security tư duy, áp dụng có đạo đức trên hệ thống của mình/được ủy quyền).

## E1. Reconnaissance & Scanning

- **Nmap** — quét port, service, OS fingerprinting
- **Amass / Subfinder** — dò subdomain, mở rộng attack surface
- **Shodan / Censys** — tìm thiết bị/service expose ra internet

## E2. Web Application Testing

- **Burp Suite / OWASP ZAP** — proxy chặn/sửa request, quét lỗ hổng web tự động và thủ công
- **sqlmap** — tự động phát hiện/khai thác SQL Injection (dùng để TEST hệ thống của mình)
- **Nikto** — quét lỗ hổng cấu hình web server cơ bản

## E3. Dependency & Static Analysis

- **Semgrep / CodeQL** — SAST, tìm pattern code không an toàn
- **Trivy / Grype** — quét lỗ hổng container image, filesystem
- **Snyk / Dependabot / OWASP Dependency-Check** — quét lỗ hổng dependency

## E4. Dynamic/Runtime Testing

- **DAST tools** (OWASP ZAP, Burp) chạy tự động trong CI/CD trước khi deploy
- **Fuzzing**: AFL, libFuzzer — gửi input ngẫu nhiên/bất thường để tìm crash/lỗ hổng, đặc biệt hiệu quả với parser, file format
- **Postman/Newman + security test collection** cho API testing tự động

## E5. Infrastructure & Cloud

- **ScoutSuite / Prowler** — audit cấu hình cloud (AWS/GCP/Azure)
- **kube-hunter / kube-bench** — kiểm tra bảo mật Kubernetes cluster

## E6. Quy trình xử lý sau khi tìm ra lỗ hổng

1. Xác định mức độ nghiêm trọng (CVSS score)
2. Ưu tiên vá theo risk (khả năng khai thác × mức độ ảnh hưởng)
3. Vá → test lại → deploy qua quy trình review bình thường (không patch nóng production khi không cần thiết, trừ khi zero-day đang bị khai thác)
4. Ghi nhận vào tracking (Jira/GitHub Security Advisory) và rút kinh nghiệm (post-mortem) nếu đã bị khai thác thật

## E7. Lộ trình học (nếu muốn đi sâu offensive security)

1. Nắm chắc OWASP Top 10 + thực hành trên **PortSwigger Web Security Academy** (miễn phí, chất lượng rất cao)
2. Thực hành trên **HackTheBox / TryHackMe** (môi trường hợp pháp để luyện tập)
3. Học CTF (Capture The Flag) — rèn tư duy tìm lỗ hổng
4. Chứng chỉ tham khảo nếu muốn theo hướng chuyên: **OSCP** (offensive), **CISSP** (quản trị), **CEH** (tổng quan)

---

# TÓM TẮT: TƯ DUY XUYÊN SUỐT

1. **Assume breach** — luôn giả định hệ thống sẽ/đã bị xâm nhập một phần, thiết kế để giảm thiểu thiệt hại (blast radius) chứ không chỉ cố ngăn 100%
2. **Shift left** — đưa bảo mật vào càng sớm càng tốt trong vòng đời phát triển, không phải bước cuối trước khi release
3. **Bảo mật là quy trình liên tục**, không phải trạng thái đạt được một lần rồi xong — cần review, patch, test định kỳ
4. **Cân bằng** giữa mức độ bảo mật và chi phí/trải nghiệm người dùng — không phải hệ thống nào cũng cần mức độ như hàng không vũ trụ, quan trọng là đánh giá đúng risk phù hợp với dữ liệu/nghiệp vụ đang bảo vệ
