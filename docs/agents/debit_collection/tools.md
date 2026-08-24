# Các Tools & Procedures cho Agent Thu Hồi Nợ

Dưới đây là danh sách các công cụ (Tools) và cấu hình cần thiết trên nền tảng ElevenLabs để hỗ trợ Workflow Thu hồi nợ.

## 1. System Built-in Tools (Công cụ tích hợp sẵn)

Cấu hình trong `conversation_config.agent.prompt.built_in_tools`:

- `end_call`: Sử dụng để ngắt cuộc gọi ngay lập tức khi hoàn tất kịch bản hoặc khi người nhấc máy không phải là chính chủ.
- `voicemail_detection`: Bật tính năng này vì đây là luồng Outbound Calling, giúp Agent phân biệt được người thật hay hộp thư thoại để xử lý cúp máy tránh lãng phí chi phí.

## 2. Webhook Tools (Tích hợp API Ngân Hàng)

Các custom webhook tools được khai báo để Agent kết nối với Core Banking / CRM của Sacombank.

### 2.1 Verify CCCD (`verify_identity`)
- **Mô tả:** Xác thực số CCCD do khách hàng cung cấp.
- **Loại:** `webhook`
- **Schema:**
  - `cccd` (string): Số CCCD người dùng đọc.
- **API Endpoint:** `POST /api/v1/debt-collection/verify`
- **Output:** `{ "is_match": true/false, "customer_name": "Trần Văn Nam" }`
- **Hành vi Agent:** Nếu `is_match` là false, kích hoạt kịch bản từ chối và gọi `end_call`.

### 2.2 Get Debt Information (`get_debt_info`)
- **Mô tả:** Lấy thông tin khoản nợ hiện tại và các biến trạng thái (state variables) của khách hàng để biết tiến độ thu thập.
- **Loại:** `webhook`
- **API Endpoint:** `GET /api/v1/debt-collection/customer/{customer_id}/status`
- **Output:**
  ```json
  {
    "debt_details": {
       "overdue_days": 5,
       "overdue_amount": 2500000,
       "total_debt": 50000000,
       "collateral": "Nhà đất tại 123 Đường ABC",
       "debt_group": 2
    },
    "state": {
       "confirm": true,
       "reason_late_paid": null,
       "proposed_solution": null,
       "promised_payment_amount": null,
       "promised_payment_time": null
    }
  }
  ```
- **Hành vi Agent:** Dựa vào `state`, Agent quyết định bỏ qua bước nào và tiếp tục hỏi câu nào.

### 2.3 Update Debt Status (`update_debt_status`)
- **Mô tả:** Cập nhật thông tin khách hàng cung cấp vào hệ thống CRM (ghi nhận PTP).
- **Loại:** `webhook`
- **Schema:** 
  - Các tham số optional: `confirm` (boolean), `reason` (string), `solution` (string), `promise_amount` (number), `promise_date` (string).
- **API Endpoint:** `PATCH /api/v1/debt-collection/customer/{customer_id}/status`
- **Output:** `{ "success": true }`
- **Hành vi Agent:** Gọi mỗi khi thu thập được thông tin mới để đảm bảo không bị mất dữ liệu nếu rớt mạng/cúp máy giữa chừng.

## 3. Platform Settings (Guardrails)

Để đảm bảo Agent tuân thủ ranh giới hẹp (Scope), cấu hình Guardrails:
- **Prompt Injection:** Bật (`is_enabled: true`) để tránh bị jailbreak (khách hàng cố lừa bot xóa nợ).
- **Custom Guardrail (CSKH & Non-Banking Block):**
  - `name`: No Customer Service or Unrelated Topics
  - `prompt`: Block the agent from answering questions about general banking services (interest rates, opening cards) or non-banking topics.
  - `execution_mode`: blocking
  - `trigger_action`: retry với thông điệp: "Dạ em là trợ lý ảo phụ trách quản lý khoản vay và thu hồi nợ. Để hỗ trợ các dịch vụ khác, anh/chị vui lòng liên hệ tổng đài CSKH ạ."
