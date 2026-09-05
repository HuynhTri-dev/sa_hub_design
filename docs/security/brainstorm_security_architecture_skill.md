# Brainstorming: SKILL "Xây dựng Security Architecture"

## 1. Phân Tích Bài Toán (Problem Analysis)

**Mục tiêu:** 
Tạo ra một SKILL cho AI Agent đóng vai trò là "Central Hub for Solution Architecture & System Design" (Bộ não của dự án), chuyên biệt về mảng Security Architecture. Agent sẽ tư vấn, đánh giá và thiết kế hệ thống bảo mật ngay từ giai đoạn đầu tiên (Shift Left) của dự án.

**Yêu cầu cốt lõi (Core Requirements):**
1. **Thiết kế & Phân tích sớm:** Phân tích rủi ro, xây dựng kiến trúc và quy trình bảo mật ngay từ ban đầu.
2. **Tư duy kinh tế (Security Economics):** Cân bằng giữa rủi ro và chi phí (ROI). Không "over-engineer" bảo mật. Đảm bảo chi phí tấn công phải lớn hơn giá trị tài sản.
3. **Resource Checklists:** Cung cấp các checklist thực tiễn để đánh giá rủi ro phù hợp với từng ngữ cảnh.
4. **General Security Scanner:** Các script/công cụ quét mã nguồn tĩnh để phát hiện các lỗi cơ bản, điểm bất thường xuyên suốt dự án (không phụ thuộc ngôn ngữ lập trình).

---

## 2. Giải Pháp Đề Xuất (Step-by-step Solution)

### Bước 1: Thiết kế cấu trúc thư mục của SKILL
SKILL sẽ được tổ chức theo chuẩn `SKILL_STRUCTURE.md` của Antigravity, bao gồm:

```text
.agents/skills/security-architecture/
├── SKILL.md                              # [Required] Lõi hướng dẫn Agent
├── resources/                            # Các tài liệu reference & checklist
│   ├── initial_security_questionnaire.md # Bộ câu hỏi thu thập yêu cầu và đánh giá tài nguyên đầu vào
│   ├── risk_assessment_checklist.md      # Checklist phân tích rủi ro tổng thể
│   ├── security_economics_matrix.md      # Ma trận đánh giá chi phí vs rủi ro (ROI)
│   ├── threat_modeling_templates.md      # Template đánh giá rủi ro (STRIDE, DREAD)
│   ├── template_security_architecture.md # Mẫu tài liệu thiết kế Security Architecture
│   └── template_vulnerability_report.md  # Mẫu báo cáo đánh giá lỗ hổng hệ thống
└── scripts/                              # Công cụ hỗ trợ
    └── general_security_scanner.py       # Script quét mã nguồn chung bằng Regex
```

### Bước 2: Thiết kế `SKILL.md` (Agent Instructions)
- **Name**: `security-architecture-blueprint`
- **Triggers**: "security design", "threat modeling", "risk assessment", "review architecture", "security check".
- **Workflow của Agent khi được trigger**:
  1. **Thu thập Ngữ cảnh (Context Gathering)**: Hỏi user về Business Logic, quy mô dự án, và giá trị tài sản cần bảo vệ.
  2. **Security Economics & Threat Modeling**: Áp dụng công thức `Risk = Likelihood × Impact`. Từ chối các giải pháp đắt đỏ nếu rủi ro thấp.
  3. **Risk Assessment**: Sử dụng checklist để rà soát các thành phần: Authentication, Data at Rest/Transit, Cloud Infra, v.v.
  4. **Source Code Review**: Chạy script `general_security_scanner.py` để tìm các lỗ hổng cơ bản và secret bị lộ.

### Bước 3: Thiết kế Resource Checklists
1. **Initial Security Questionnaire (Bộ câu hỏi đầu vào)**:
   - *Tài nguyên & Nhân lực*: Đội ngũ có chuyên gia bảo mật không? Ngân sách dự kiến cho bảo mật (công cụ/dịch vụ) là bao nhiêu?
   - *Nghiệp vụ (Business)*: Dự án thuộc lĩnh vực nào (Fintech, Y tế, E-commerce)? Có yêu cầu tuân thủ chuẩn nào (PCI-DSS, HIPAA, GDPR) không?
   - *Quy mô*: Số lượng user dự kiến? Ứng dụng triển khai trên Cloud (AWS/GCP) hay On-premise?
2. **Risk Assessment Checklist**:
   - *Phân quyền*: Đã áp dụng Least Privilege chưa?
   - *Mạng*: Có chia vùng mạng (Network Segmentation), VPC, DMZ không?
   - *Dữ liệu*: Có mã hóa dữ liệu nhạy cảm không? Có cơ chế backup không?
3. **Security Economics Matrix**:
   - So sánh giữa: Tự xây (Build) vs Mua dịch vụ (Buy) vs Dùng mã nguồn mở (OSS).
   - Đánh giá thời gian triển khai và rủi ro bị delay dự án so với việc dùng giải pháp có sẵn (WAF, IAM).

### Bước 4: Thiết kế công cụ quét (General Security Scanner)
Thay vì dùng các công cụ SAST phức tạp (đòi hỏi cài đặt cho từng ngôn ngữ), xây dựng một script Python quét thư mục dự án dựa trên Regex và Heuristics để phát hiện các mẫu (patterns) rủi ro chung:
- **Secrets & Credentials**: AWS Keys, API Tokens, JWT, Private Keys (RSA/EC), Hardcoded passwords (vd: `password = "123456"`).
- **Insecure Configurations**: Bộc lộ IP/Cổng (vd: `0.0.0.0`, `port 80`), Bật Debug mode (vd: `DEBUG = True`, `APP_ENV=local` trên production).
- **Dangerous Functions**: Các lệnh gọi shell trực tiếp (gram) hiện tại**: Mô tả trực quan cách các thành phần (máy chủ ảo, DB, container) đang giao tiếp. Chỉ rõ vị trí Firewall, API Gateway và cơ chế mã hóa.
- **Báo cáo Đánh giá Lỗ hổng (Vulnerability Assessment Report)**: Kết quả quét lỗi tự động hoặc rà soát tĩnh, liệt kê mức độ nghiêm trọng (Critical/High/Medium/Low) của các lỗ hổng cần vá ngay.

---

## 3. Danh sách Rủi ro & Edge-cases (Risks & Considerations)

1. **False Positives (Cảnh báo giả) từ Scanner**:
   - Quét bằng regex rất dễ sinh ra cảnh báo giả (ví dụ: một biến tên là `is_aws_key_valid`).
   - *Mitigation*: Script cần có cơ chế bỏ qua (ignore list) và AI Agent phải có bước "Verification" (đọc lại đoạn code bị cảnh báo) trước khi báo cáo cho user.
2. **Lỗ hổng Logic Nghiệp vụ**:
   - Scanner chung không thể phát hiện các lỗ hổng logic phức tạp (như IDOR, Race Condition).
   - *Mitigation*: Bắt buộc Agent phải tập trung vào bước Threat Modeling và Checklist Assessment để bù đắp giới hạn của code scanner.
3. **Over-engineering (Bảo mật quá mức)**:
   - Agent có xu hướng "nhét" mọi công nghệ bảo mật (Zero-Trust, mTLS) vào dự án nhỏ.
   - *Mitigation*: Áp dụng quy tắc "Security Economics" rất chặt chẽ trong `SKILL.md`. Bắt buộc Agent phải trình bày "Chi phí dự kiến" và "ROI" trước khi đề xuất kiến trúc.
4. **Vấn đề hiệu năng khi quét**:
   - Dự án quá lớn có thể làm script Python chạy chậm.
   - *Mitigation*: Giới hạn độ sâu thư mục hoặc lọc theo các định dạng file phổ biến (`.py`, `.js`, `.ts`, `.go`, `.java`, `.yaml`, `.env`).
