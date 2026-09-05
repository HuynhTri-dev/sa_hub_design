---
name: "Chi tiết các tiêu chuẩn bảo mật (mở rộng + checklist đánh giá)"
description: "Diễn giải chi tiết 10 tiêu chuẩn/framework bảo mật kèm bảng checklist tự đánh giá cho từng loại."
---

# Chi Tiết Các Tiêu Chuẩn và Framework Bảo Mật (Bản Mở Rộng)

> Mỗi mục giữ nguyên cấu trúc gốc (Tổng quan / Phạm vi / Điểm chính / Giá trị) và bổ sung thêm: (a) phần diễn giải sâu hơn, (b) **bảng checklist đánh giá** để dùng trực tiếp khi audit nội bộ hoặc chuẩn bị cho đánh giá bên ngoài.

---

## 1. OWASP Top 10

**Diễn giải mở rộng:**
OWASP Top 10 không phải là tiêu chuẩn để "đạt chứng chỉ" mà là baseline nhận thức — nếu ứng dụng dính bất kỳ mục nào trong danh sách này, coi như chưa đạt mức an toàn tối thiểu. Danh sách được cập nhật định kỳ (khoảng 3–4 năm/lần) dựa trên dữ liệu thực tế từ hàng trăm tổ chức đóng góp, nên thứ hạng phản ánh đúng xu hướng tấn công hiện tại chứ không cố định mãi mãi (ví dụ SSRF chỉ mới xuất hiện ở bản 2021, trước đó không có).

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Broken Access Control | Mọi endpoint đều kiểm tra quyền ở tầng server (không chỉ ẩn UI); có test case cho IDOR | [ ] |
| 2 | Cryptographic Failures | Dữ liệu nhạy cảm mã hóa at-rest & in-transit; không dùng thuật toán yếu (MD5, SHA-1, DES) | [ ] |
| 3 | Injection | Dùng parameterized query/ORM cho mọi truy vấn; input validation ở tầng server | [ ] |
| 4 | Insecure Design | Có threat modeling ở giai đoạn thiết kế trước khi code | [ ] |
| 5 | Security Misconfiguration | Không còn config mặc định (default password, debug mode bật ở production) | [ ] |
| 6 | Vulnerable/Outdated Components | Có quy trình quét dependency (SCA) và patch định kỳ | [ ] |
| 7 | Identification & Auth Failures | MFA cho tài khoản nhạy cảm; không lộ session ID trong URL | [ ] |
| 8 | Software/Data Integrity Failures | CI/CD pipeline có ký số artifact; kiểm tra checksum khi deploy | [ ] |
| 9 | Security Logging & Monitoring Failures | Log đủ sự kiện bảo mật quan trọng, có alert khi phát hiện bất thường | [ ] |
| 10 | SSRF | Whitelist domain/IP được phép gọi ra từ server, không cho user input tự do control URL đích | [ ] |

---

## 2. OWASP API Security Top 10

**Diễn giải mở rộng:**
Danh sách này ra đời vì OWASP Top 10 (dành cho web truyền thống) không phản ánh đủ các rủi ro đặc thù của kiến trúc API-first hiện đại (microservices, mobile backend, GraphQL). Điểm khác biệt lớn nhất so với OWASP Top 10 là nhóm lỗi liên quan đến **authorization ở nhiều tầng khác nhau** (object level, property level, function level) — vì API thường trả về nguyên payload dữ liệu thay vì render UI có kiểm soát, nên lỗi phân quyền dễ bị khai thác hơn nhiều.

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | BOLA (Broken Object Level Authorization) | Mọi request lấy resource theo ID đều kiểm tra ownership, không chỉ dựa vào ID hợp lệ | [ ] |
| 2 | Broken Authentication | Token có thời hạn ngắn, refresh token được rotate, endpoint auth có rate limit | [ ] |
| 3 | Broken Object Property Level Authorization | API không trả về field nhạy cảm mà role hiện tại không được xem/sửa | [ ] |
| 4 | Unrestricted Resource Consumption | Có rate limiting, giới hạn page size, timeout cho mọi endpoint | [ ] |
| 5 | Broken Function Level Authorization | Endpoint admin được kiểm tra role riêng, không chỉ ẩn trong docs | [ ] |
| 6 | Unrestricted Access to Sensitive Business Flows | Có kiểm soát tần suất cho flow nhạy cảm (đặt hàng, chuyển khoản) chống bot/abuse | [ ] |
| 7 | SSRF | Giống mục OWASP Top 10 #10 | [ ] |
| 8 | Security Misconfiguration | CORS cấu hình đúng, không bật verbose error trả stack trace | [ ] |
| 9 | Improper Inventory Management | Có API inventory đầy đủ, tắt/loại bỏ version API cũ không dùng | [ ] |
| 10 | Unsafe Consumption of APIs | Validate response từ API bên thứ ba trước khi dùng, không tin tưởng mù quáng | [ ] |

---

## 3. OWASP ASVS (Application Security Verification Standard)

**Diễn giải mở rộng:**
ASVS khác OWASP Top 10 ở chỗ nó là **checklist có thể đo lường được** (hàng trăm yêu cầu cụ thể, đánh số rõ ràng theo từng chương: V1 Architecture, V2 Authentication, V3 Session Management...). Một tổ chức có thể tuyên bố "đạt ASVS Level 2" như một tiêu chí hợp đồng với đối tác/khách hàng, tương tự cách dùng ISO 27001 nhưng ở tầng ứng dụng thay vì tầng tổ chức.

**Checklist đánh giá (theo cấp độ, không liệt kê hết hàng trăm mục — dùng làm khung xác định level phù hợp):**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Xác định Level phù hợp | Đã phân loại ứng dụng theo mức độ nhạy cảm dữ liệu để chọn Level 1/2/3 | [ ] |
| 2 | V1 Architecture | Có tài liệu kiến trúc bảo mật, threat model được review | [ ] |
| 3 | V2 Authentication | Chính sách mật khẩu, MFA, khóa tài khoản sau N lần sai đạt theo level đã chọn | [ ] |
| 4 | V3 Session Management | Session timeout, invalidate session khi logout/đổi mật khẩu | [ ] |
| 5 | V4 Access Control | RBAC/ABAC được implement và test | [ ] |
| 6 | V5 Validation/Sanitization | Input validation nhất quán ở mọi tầng | [ ] |
| 7 | V7 Error Handling & Logging | Không lộ thông tin nhạy cảm qua error message | [ ] |
| 8 | V9 Communications | TLS 1.2+ bắt buộc, cert pinning nếu cần | [ ] |
| 9 | V14 Configuration | Hardening cấu hình server/framework theo checklist | [ ] |
| 10 | Đánh giá định kỳ | Có lịch review lại checklist ASVS mỗi release lớn | [ ] |

---

## 4. NIST 800-53 / NIST CSF

**Diễn giải mở rộng:**
NIST CSF phù hợp để trình bày cho ban lãnh đạo (5 chức năng dễ hiểu, không quá kỹ thuật), trong khi NIST 800-53 là tài liệu chi tiết dành cho đội kỹ thuật triển khai từng control cụ thể (có hơn 1000 control chia theo họ — Access Control, Audit, Incident Response...). Hai tài liệu này thường dùng **song song**: CSF làm khung báo cáo, 800-53 làm checklist triển khai.

**Checklist đánh giá (theo 5 chức năng CSF):**
| # | Chức năng | Hạng mục kiểm tra | Trạng thái |
|---|---|---|---|
| 1 | Identify | Có asset inventory đầy đủ, đã xác định rủi ro theo từng asset | [ ] |
| 2 | Identify | Có risk assessment định kỳ | [ ] |
| 3 | Protect | Access control, encryption, security training đã triển khai | [ ] |
| 4 | Protect | Có quy trình quản lý thay đổi (change management) | [ ] |
| 5 | Detect | Có hệ thống giám sát liên tục (SIEM/log monitoring) | [ ] |
| 6 | Detect | Có quy trình phát hiện bất thường (anomaly detection) | [ ] |
| 7 | Respond | Có Incident Response Plan đã được test | [ ] |
| 8 | Respond | Có quy trình truyền thông khi xảy ra sự cố | [ ] |
| 9 | Recover | Có DR/BCP plan và đã diễn tập | [ ] |
| 10 | Recover | Có quy trình rút kinh nghiệm (post-incident review) sau mỗi sự cố | [ ] |

---

## 5. ISO/IEC 27001

**Diễn giải mở rộng:**
Điểm khác biệt cốt lõi của ISO 27001 so với các framework kỹ thuật khác: nó là hệ thống **quản lý** (ISMS), nghĩa là đánh giá không chỉ dừng ở "có kiểm soát kỹ thuật hay không" mà còn "có quy trình duy trì, cải tiến liên tục hay không". Một tổ chức có thể có công nghệ tốt nhưng vẫn trượt audit ISO 27001 nếu thiếu tài liệu hóa quy trình, thiếu bằng chứng review định kỳ, hoặc thiếu cam kết từ ban lãnh đạo.

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Phạm vi ISMS | Đã xác định rõ scope (hệ thống/phòng ban nào thuộc phạm vi chứng nhận) | [ ] |
| 2 | Risk Assessment | Có quy trình đánh giá rủi ro định kỳ, có risk register | [ ] |
| 3 | Statement of Applicability (SoA) | Đã map đầy đủ Annex A controls áp dụng/không áp dụng kèm lý do | [ ] |
| 4 | Quản lý tài sản | Có asset owner rõ ràng cho từng loại tài sản thông tin | [ ] |
| 5 | An toàn nhân sự | Có quy trình background check, NDA, training khi onboard/offboard | [ ] |
| 6 | An toàn vật lý | Kiểm soát ra vào, camera, clean desk policy | [ ] |
| 7 | Quản lý sự cố | Có quy trình ghi nhận, xử lý, rút kinh nghiệm sự cố | [ ] |
| 8 | Internal Audit | Có lịch audit nội bộ định kỳ trước khi audit chứng nhận | [ ] |
| 9 | Management Review | Ban lãnh đạo có review ISMS định kỳ (thường 6–12 tháng) | [ ] |
| 10 | PDCA | Có bằng chứng cải tiến liên tục (Corrective Action) từ các đợt review trước | [ ] |

---

## 6. CIS Controls / Benchmarks

**Diễn giải mở rộng:**
CIS Controls được sắp xếp theo thứ tự ưu tiên (Implementation Group 1/2/3 — IG1 dành cho tổ chức nhỏ với nguồn lực hạn chế, IG3 cho tổ chức lớn có đội bảo mật chuyên trách), giúp tổ chức biết nên làm gì trước nếu chưa đủ nguồn lực làm hết. CIS Benchmarks thì cụ thể đến từng dòng config (ví dụ: "phải set `PermitRootLogin no` trong `sshd_config`"), rất phù hợp để tự động hóa dưới dạng compliance-as-code (dùng công cụ như OpenSCAP, InSpec để scan tự động).

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Inventory & Control of Assets | Có danh sách đầy đủ thiết bị/phần mềm được phép dùng | [ ] |
| 2 | Data Protection | Dữ liệu nhạy cảm được mã hóa và phân loại | [ ] |
| 3 | Secure Configuration | Hệ điều hành/server đã hardening theo CIS Benchmark tương ứng | [ ] |
| 4 | Account Management | Không còn tài khoản mặc định/dùng chung; có quy trình thu hồi quyền | [ ] |
| 5 | Access Control Management | Least privilege đã áp dụng cho toàn bộ hệ thống | [ ] |
| 6 | Vulnerability Management | Có lịch scan lỗ hổng định kỳ và SLA vá lỗi theo mức độ nghiêm trọng | [ ] |
| 7 | Audit Log Management | Log được bật đầy đủ và lưu trữ đủ thời gian yêu cầu | [ ] |
| 8 | Malware Defense | EDR/antivirus đã triển khai trên toàn bộ endpoint | [ ] |
| 9 | Incident Response | Có quy trình IR phù hợp với Implementation Group đã chọn | [ ] |
| 10 | Compliance as Code | Có tự động hóa kiểm tra config (OpenSCAP/InSpec) thay vì check thủ công | [ ] |

---

## 7. PCI-DSS

**Diễn giải mở rộng:**
Mức độ tuân thủ PCI-DSS phụ thuộc vào **số lượng giao dịch thẻ xử lý mỗi năm** (chia thành 4 Merchant Level, Level 1 là cao nhất — trên 6 triệu giao dịch/năm, yêu cầu audit bởi QSA — Qualified Security Assessor bên ngoài). Chiến lược phổ biến nhất để giảm chi phí tuân thủ là **thu hẹp phạm vi (scope reduction)**: dùng payment gateway/tokenization của bên thứ ba đã đạt PCI-DSS để không bao giờ để dữ liệu thẻ thật chạm vào hệ thống của mình (outsource toàn bộ CDE — Cardholder Data Environment).

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Firewall Configuration | Firewall được cấu hình đúng, không dùng rule mặc định | [ ] |
| 2 | Default Password | Không còn password mặc định trên bất kỳ thiết bị/hệ thống nào | [ ] |
| 3 | Cardholder Data Protection | Không lưu CVV; PAN nếu lưu phải mã hóa mạnh + tokenization | [ ] |
| 4 | Encryption in Transit | Toàn bộ truyền dữ liệu thẻ qua TLS, không có kênh plaintext | [ ] |
| 5 | Vulnerability Management | Antivirus/EDR cập nhật, patch định kỳ cho hệ thống trong CDE | [ ] |
| 6 | Access Control | Truy cập dữ liệu thẻ giới hạn theo need-to-know | [ ] |
| 7 | Network Monitoring | Log và giám sát toàn bộ truy cập vào CDE | [ ] |
| 8 | Regular Testing | Có pentest định kỳ (tối thiểu hàng năm) cho hệ thống trong scope | [ ] |
| 9 | Security Policy | Có chính sách bảo mật thông tin bằng văn bản, được phổ biến cho nhân viên | [ ] |
| 10 | Scope Reduction | Đã đánh giá khả năng outsource xử lý thẻ để giảm phạm vi tuân thủ | [ ] |

---

## 8. GDPR / Nghị định 13/2023/NĐ-CP (VN)

**Diễn giải mở rộng:**
Khác biệt quan trọng giữa hai quy định: GDPR áp dụng **ngoài lãnh thổ** (extraterritorial — công ty Việt Nam xử lý dữ liệu công dân EU vẫn phải tuân thủ), trong khi NĐ 13/2023 tập trung vào dữ liệu cá nhân trong lãnh thổ Việt Nam nhưng có thêm yêu cầu đặc thù như phải lập **Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân (DPIA)** và trong một số trường hợp phải gửi cho Bộ Công an trước khi xử lý dữ liệu nhạy cảm quy mô lớn — đây là điểm GDPR không yêu cầu nộp hồ sơ cho cơ quan quản lý trước (chỉ cần lưu nội bộ, trừ khi được yêu cầu).

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Privacy by Design | Đánh giá privacy risk từ giai đoạn thiết kế tính năng mới | [ ] |
| 2 | Consent Management | Có cơ chế xin/ghi log/thu hồi sự đồng ý rõ ràng | [ ] |
| 3 | Data Mapping | Biết rõ dữ liệu cá nhân nằm ở đâu trong toàn hệ thống (kể cả backup, log) | [ ] |
| 4 | DSAR Process | Có quy trình xử lý yêu cầu truy cập/xóa/xuất dữ liệu trong thời hạn luật định | [ ] |
| 5 | DPIA/PIA | Đã lập đánh giá tác động cho các tính năng xử lý dữ liệu nhạy cảm | [ ] |
| 6 | Breach Notification | Có quy trình thông báo vi phạm trong 72h (GDPR) | [ ] |
| 7 | Data Processing Agreement | Có DPA với mọi vendor/bên thứ ba xử lý dữ liệu thay mặt tổ chức | [ ] |
| 8 | Data Residency (nếu áp dụng) | Dữ liệu được lưu đúng khu vực pháp lý yêu cầu | [ ] |
| 9 | DPO/Người phụ trách | Đã chỉ định người/bộ phận chịu trách nhiệm về bảo vệ dữ liệu | [ ] |
| 10 | Thông báo cơ quan quản lý (NĐ13) | Đã đánh giá nghĩa vụ thông báo Bộ Công an nếu xử lý dữ liệu nhạy cảm quy mô lớn | [ ] |

---

## 9. SOC 2

**Diễn giải mở rộng:**
SOC 2 có 2 loại báo cáo: **Type I** (đánh giá thiết kế control tại một thời điểm) và **Type II** (đánh giá hiệu quả vận hành của control trong một khoảng thời gian, thường 6–12 tháng) — Type II có giá trị cao hơn nhiều với khách hàng enterprise vì chứng minh control thực sự hoạt động chứ không chỉ tồn tại trên giấy. Không phải mọi tổ chức đều cần cả 5 Trust Services Criteria — có thể chọn scope chỉ gồm Security (bắt buộc, không thể bỏ) + Availability nếu chưa cần Privacy/Confidentiality.

**Checklist đánh giá:**
| # | Hạng mục kiểm tra | Mô tả cần đạt | Trạng thái |
|---|---|---|---|
| 1 | Xác định Trust Services Criteria | Đã chọn đúng scope (Security bắt buộc + các mục còn lại theo nhu cầu khách hàng) | [ ] |
| 2 | Security | Access control, MFA, encryption đã triển khai và có bằng chứng | [ ] |
| 3 | Availability | Có SLA uptime, monitoring, DR plan | [ ] |
| 4 | Processing Integrity | Có kiểm soát đảm bảo dữ liệu xử lý chính xác, đầy đủ, kịp thời | [ ] |
| 5 | Confidentiality | Dữ liệu bảo mật (không phải PII) được kiểm soát truy cập đúng | [ ] |
| 6 | Privacy | Nếu trong scope: tuân thủ nguyên tắc xử lý PII tương tự GDPR | [ ] |
| 7 | Chọn loại báo cáo | Đã xác định cần Type I hay Type II theo yêu cầu khách hàng | [ ] |
| 8 | Bằng chứng vận hành | Có log/evidence chứng minh control hoạt động liên tục (cho Type II) | [ ] |
| 9 | Vendor Management | Đánh giá SOC 2 của các vendor quan trọng mà mình phụ thuộc | [ ] |
| 10 | Audit Readiness | Đã làm việc với auditor độc lập (CPA firm) được công nhận | [ ] |

---

## 10. MITRE ATT&CK

**Diễn giải mở rộng:**
Khác với các framework compliance ở trên, MITRE ATT&CK không phải là "checklist để đạt chuẩn" mà là **bản đồ tri thức về hành vi tấn công thực tế**, dùng để đo mức độ bao phủ phòng thủ (defense coverage) — ví dụ: công cụ EDR hiện tại phát hiện được bao nhiêu % kỹ thuật trong ma trận. Có 3 ma trận chính: **Enterprise** (IT truyền thống), **Mobile**, và **ICS** (hệ thống công nghiệp) — cần chọn đúng ma trận theo loại hạ tầng đang đánh giá.

**Checklist đánh giá (theo các giai đoạn tấn công chính):**
| # | Giai đoạn (Tactic) | Hạng mục kiểm tra | Trạng thái |
|---|---|---|---|
| 1 | Initial Access | Có kiểm soát phishing, giới hạn exposed service ra internet | [ ] |
| 2 | Execution | Có application whitelisting/EDR chặn thực thi mã lạ | [ ] |
| 3 | Persistence | Giám sát thay đổi scheduled task, registry, service khởi động cùng hệ thống | [ ] |
| 4 | Privilege Escalation | Có giám sát hành vi leo quyền bất thường | [ ] |
| 5 | Defense Evasion | Có giám sát việc tắt log/antivirus trên endpoint | [ ] |
| 6 | Credential Access | Giám sát hành vi dump credential (Mimikatz-like behavior) | [ ] |
| 7 | Lateral Movement | Có network segmentation hạn chế di chuyển ngang | [ ] |
| 8 | Collection/Exfiltration | Có DLP giám sát luồng dữ liệu ra ngoài bất thường | [ ] |
| 9 | Command & Control | Có giám sát traffic C2 bất thường (DNS tunneling, beaconing) | [ ] |
| 10 | Coverage Mapping | Đã map công cụ phòng thủ hiện có (SIEM/EDR) lên ma trận để biết vùng còn thiếu | [ ] |

---

## Bảng tổng hợp mức độ ưu tiên áp dụng theo loại tổ chức

| Tiêu chuẩn | Startup/SME | Enterprise thường | Tài chính/Y tế/Chính phủ |
|---|---|---|---|
| OWASP Top 10 | Bắt buộc | Bắt buộc | Bắt buộc |
| OWASP API Top 10 | Nếu có API public | Bắt buộc | Bắt buộc |
| ASVS | Khuyến khích (Level 1) | Khuyến khích (Level 2) | Bắt buộc (Level 2/3) |
| NIST CSF/800-53 | Không bắt buộc | Khuyến khích | Bắt buộc (đặc biệt nếu làm việc với chính phủ Mỹ) |
| ISO 27001 | Không bắt buộc | Khuyến khích/theo yêu cầu khách hàng | Thường bắt buộc |
| CIS Controls | Khuyến khích (IG1) | Khuyến khích (IG2) | Khuyến khích (IG3) |
| PCI-DSS | Chỉ nếu xử lý thẻ | Bắt buộc nếu xử lý thẻ | Bắt buộc nếu xử lý thẻ |
| GDPR/NĐ13 | Bắt buộc nếu có PII | Bắt buộc | Bắt buộc |
| SOC 2 | Không cần | Thường yêu cầu bởi khách hàng B2B | Thường bắt buộc |
| MITRE ATT&CK | Tham khảo | Khuyến khích cho SOC/Red-Blue team | Bắt buộc cho đội SOC |
