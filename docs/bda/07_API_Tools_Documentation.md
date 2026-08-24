<!--
name: 07_API_Tools_Documentation.md
description: Comprehensive API Tools Reference & Schema Documentation for Banking CSKH and Debt Collection Voicebot/Chatbot.
-->

# Tài Liệu Đặc Tả API & Công Cụ (API Tools Reference)
## Dành cho AI Voicebot / Chatbot (CSKH Ngân Hàng & Thu Hồi Nợ)

---

## 1. Thông Tin Chung (General Information)

* **Local Base URL:** `http://localhost:3000`
* **Localtunnel / Public Webhook URL:** `https://tiny-cycles-kiss.loca.lt`
* **WebSocket Voice Stream URL:** `ws://localhost:3000/ws/voice-stream` *(hoặc `wss://tiny-cycles-kiss.loca.lt/ws/voice-stream`)*
* **Định dạng dữ liệu:** `application/json`
* **Tiêu chuẩn bảo mật:** Tự động che giấu dữ liệu nhạy cảm theo chuẩn **PCI-DSS** (16 số thẻ, CCCD, CVV, OTP).

---

## 2. Nhóm API Cho Agent 1: Chăm Sóc Khách Hàng (Banking CSKH)

### 2.1. Tool: Khóa Thẻ Khẩn Cấp (`emergency_lock_card`)
* **Mục đích:** Thực hiện định danh nhanh (Fast-track) bằng số điện thoại gọi đến và 4 số cuối CCCD để khóa thẻ tức thì trong vòng 2 giây khi khách hàng báo mất thẻ hoặc nghi ngờ gian lận.
* **Method & Path:** `POST /api/v1/cskh/cards/lock-emergency`
* **Request Body:**
```json
{
  "phoneNumber": "0912345678",
  "nationalIdLast4": "7892",
  "cardId": "CARD_VISA_4568",
  "reason": "LOST_CARD_EMERGENCY"
}
```
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "code": "CARD_LOCKED_SUCCESSFULLY",
  "data": {
    "customerName": "Nguyễn Thị Mai",
    "cardLast4": "4568",
    "lockedAt": "2026-08-21T09:16:23.056Z",
    "spokenMessage": "Dạ thẻ của chị Nguyễn Thị Mai đuôi 4568 đã được khóa thành công an toàn lúc 16:16:23. Mọi giao dịch phát sinh từ thời điểm này đều sẽ bị từ chối an toàn ạ."
  }
}
```
* **cURL mẫu:**
```bash
curl -X POST "https://tiny-cycles-kiss.loca.lt/api/v1/cskh/cards/lock-emergency" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "0912345678", "nationalIdLast4": "7892", "reason": "LOST_CARD_EMERGENCY"}'
```

---

### 2.2. Tool: Định Danh Khách Hàng Chuẩn (`verify_identity`)
* **Mục đích:** Xác thực 3 yếu tố (SĐT, 4 số cuối CCCD, Năm sinh) trước khi tra cứu số dư hoặc lịch sử giao dịch.
* **Method & Path:** `POST /api/v1/cskh/auth/verify`
* **Request Body:**
```json
{
  "phoneNumber": "0987654321",
  "nationalIdLast4": "3456",
  "birthYear": 1988
}
```
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "customerId": "CUST_11203",
    "fullName": "Trần Văn Nam"
  }
}
```

---

### 2.3. Tool: Tra Cứu Số Dư Tài Khoản (`get_account_balance`)
* **Mục đích:** Lấy số dư tài khoản kèm văn bản chuyển đổi sang lời đọc tiếng Việt tự nhiên (`spokenBalance`) cho TTS.
* **Method & Path:** `GET /api/v1/cskh/account/balance?customerId={customerId}`
* **Query Parameters:**
  * `customerId` *(string, bắt buộc)*: Mã khách hàng đã xác thực (ví dụ: `CUST_11203`).
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "accountNumber": "19033445566",
    "balance": 25400000,
    "currency": "VND",
    "spokenBalance": "hai mươi lăm triệu bốn trăm nghìn đồng"
  }
}
```
* **cURL mẫu:**
```bash
curl "https://tiny-cycles-kiss.loca.lt/api/v1/cskh/account/balance?customerId=CUST_11203"
```

---

### 2.4. Tool: Tra Cứu Lịch Sử Giao Dịch (`get_recent_transactions`)
* **Mục đích:** Lấy danh sách 3–5 giao dịch biến động gần nhất.
* **Method & Path:** `GET /api/v1/cskh/account/transactions?customerId={customerId}&limit={limit}`
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "total": 3,
    "transactions": [
      {
        "transactionId": "TXN_001",
        "timestamp": "14:30 21/08/2026",
        "amount": 3000000,
        "type": "CREDIT",
        "description": "Nhận chuyển khoản từ Công ty ABC"
      },
      {
        "transactionId": "TXN_002",
        "timestamp": "10:15 21/08/2026",
        "amount": 500000,
        "type": "DEBIT",
        "description": "Thanh toán tiền điện EVN"
      },
      {
        "transactionId": "TXN_003",
        "timestamp": "18:20 20/08/2026",
        "amount": 120000,
        "type": "DEBIT",
        "description": "Thanh toán GrabFood"
      }
    ]
  }
}
```

---

## 3. Nhóm API Cho Agent 2: Thu Hồi Nợ & Nhắc Phí (Debt Collection)

### 3.1. Tool: Lấy Chi Tiết Khoản Nợ Outbound (`get_debt_campaign_details`)
* **Mục đích:** Lấy thông tin hợp đồng vay quá hạn theo số điện thoại (tự động kiểm tra và chặn nếu ngoài khung giờ pháp lý 08:00 - 21:00).
* **Method & Path:** `GET /api/v1/debt/campaigns/details?phoneNumber={phoneNumber}`
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "contractId": "LD-8890",
    "debtorName": "Lê Hoàng Long",
    "overdueDays": 5,
    "totalDebtAmount": 2350000,
    "spokenAmount": "hai triệu ba trăm năm mươi nghìn đồng"
  }
}
```
* **Response Ngoài khung giờ gọi (`403 Forbidden`):**
```json
{
  "success": false,
  "code": "OUT_OF_LEGAL_CALLING_HOURS",
  "message": "Hiện tại nằm ngoài khung giờ gọi nhắc nợ theo quy định (08:00 - 21:00)."
}
```

---

### 3.2. Tool: Xác Thực Đúng Người Vay (`verify_debtor`)
* **Mục đích:** Bắt buộc xác nhận người nghe có phải chính chủ hợp đồng không trước khi được phép đọc chi tiết số tiền nợ.
* **Method & Path:** `POST /api/v1/debt/verify-debtor`
* **Request Body (Đúng người vay):**
```json
{
  "phoneNumber": "0901234567",
  "claimedName": "Lê Hoàng Long"
}
```
* **Response:**
```json
{
  "success": true,
  "isPrimaryDebtor": true,
  "action": "PROCEED_TO_DEBT_DISCLOSURE"
}
```
* **Request Body (Người nghe hộ / Người thân):**
```json
{
  "phoneNumber": "0901234567",
  "claimedName": "Trần Thị Hoa (vợ)"
}
```
* **Response (Tuyệt đối không đọc số tiền nợ):**
```json
{
  "success": true,
  "isPrimaryDebtor": false,
  "action": "DO_NOT_DISCLOSE_DEBT",
  "spokenGuidance": "Dạ em cảm ơn anh/chị. Nhờ anh/chị chuyển lời giúp chủ hợp đồng vui lòng liên hệ lại tổng đài Ngân hàng SacomBank sớm nhất giúp em nhé ạ."
}
```

---

### 3.3. Tool: Ghi Nhận Hẹn Thanh Toán PTP (`commit_promise_to_pay`)
* **Mục đích:** Chốt ngày hẹn thanh toán (Promise to Pay - PTP), cập nhật CRM và tự động kích hoạt gửi SMS/Zalo ZNS hướng dẫn thanh toán tức thì.
* **Method & Path:** `POST /api/v1/debt/ptp/commit`
* **Request Body:**
```json
{
  "contractId": "LD-8890",
  "ptpDate": "2026-08-25",
  "ptpAmount": 2350000,
  "paymentChannel": "CHUYEN_KHOAN"
}
```
* **Response Thành công (`200 OK`):**
```json
{
  "success": true,
  "code": "PTP_RECORDED_SUCCESSFULLY",
  "data": {
    "contractId": "LD-8890",
    "disposition": "PTP",
    "spokenConfirmation": "Dạ em đã ghi nhận lịch hẹn thanh toán của anh/chị là ngày 2026-08-25 với số tiền là hai triệu ba trăm năm mươi nghìn đồng. Tin nhắn SMS xác nhận và số tài khoản nộp tiền đã được gửi ngay đến máy của anh/chị rồi ạ."
  }
}
```

---

### 3.4. Tool: Cập Nhật Trạng Thái CRM (`update_crm_disposition`)
* **Mục đích:** Ghi nhận mã phân loại kết quả cuộc gọi vào CRM sau khi kết thúc đàm thoại.
* **Method & Path:** `POST /api/v1/debt/disposition/update`
* **Request Body:**
```json
{
  "contractId": "LD-8890",
  "status": "DISPUTE_PAYMENT",
  "notes": "Khách hàng báo đã nộp tiền tại cây ATM tuần trước, khiếu nại chưa được gạch nợ."
}
```
* **Các giá trị `status` hợp lệ:**
  * `PTP`: Đã chốt hẹn thanh toán thành công.
  * `NO_ANSWER`: Không nhấc máy / Thuê bao bận.
  * `WRONG_PERSON`: Người nghe không phải chủ nợ.
  * `DISPUTE_PAYMENT`: Khách hàng khiếu nại / tranh chấp số dư.
  * `REFUSAL`: Khách hàng từ chối hợp tác / từ chối trả nợ.

---

## 4. Bảng Dữ Liệu Test Mẫu (Test Data Cheatsheet)

| Nghiệp vụ | Số điện thoại | 4 số cuối CCCD | Tên khách hàng | Mã hợp đồng / Mã KH | Trạng thái mẫu |
|---|---|---|---|---|---|
| **CSKH Khẩn cấp (Mất thẻ)** | `0912345678` | `7892` | Nguyễn Thị Mai | Thẻ `CARD_VISA_4568` | Đang hoạt động $\rightarrow$ Khóa thành công |
| **CSKH Tra cứu số dư** | `0987654321` | `3456` | Trần Văn Nam | `CUST_11203` | Số dư: 25.400.000 VNĐ |
| **Thu hồi nợ (PTP)** | `0901234567` | `1109` | Lê Hoàng Long | `LD-8890` | Quá hạn 5 ngày (2.350.000 VNĐ) |
| **Thu hồi nợ (Tranh chấp)** | `0933445566` | `5567` | Phạm Quốc Tuấn | `CC-4421` | Quá hạn 14 ngày (10.200.000 VNĐ) |
