<!--
name: procedure.md
description: Reference catalog of customer service procedures designed for the banking CSKH agent.
-->
# Banking CSKH Agent - Procedure Design Catalog

This document defines the structured and free-form procedures for the SacomBank CSKH Agent. These procedures ensure safe, compliant, and deterministic customer service workflows, separating routine inquiries from high-risk transactions.

---

## 1. Summary of Active Procedures

| Procedure ID | Procedure Name | Target Scenario | Security Level | Primary Tool(s) |
| :--- | :--- | :--- | :--- | :--- |
| `proc_emergency_lock` | Báo Mất Thẻ / Khóa Thẻ Khẩn Cấp | Lost/stolen card, immediate lock needed | Medium-High | `verify_customer_id`, `get_customer_cards`, `execute_card_lock` |
| `proc_check_balance` | Tra Cứu Số Dư Tài Khoản / Thẻ | Check current available balance | Medium | `verify_customer_id`, `get_customer_cards`, `get_card_balance` |
| `proc_recent_tx` | Tra Cứu Lịch Sử Giao Dịch | View last 3-5 transactions | Medium | `verify_customer_id`, `get_customer_cards`, `get_recent_transactions` |
| `proc_fraud_report` | Báo Cáo Giao Dịch Gian Lận | Unrecognized transaction or fraud alert | High (Emergency) | `execute_card_lock`, `system_tool_transfer` |
| `proc_unsupported` | Nghiệp Vụ Ngoài Phạm Vi Hỗ Trợ | Handoff OTP, card unlock, card activation, SMS Banking, corporate loans, etc. | Low | `system_tool_transfer` |

> [!IMPORTANT]
> **Các nghiệp vụ dưới đây đã bị chuyển sang Out-of-Scope do thiếu API backend và vi phạm quy tắc bảo mật:**
> - ~~`proc_unlock_card` (Mở khóa thẻ)~~: Yêu cầu OTP — **không được phép** đọc OTP qua Voice/Chat.
> - ~~`proc_activate_card` (Kích hoạt thẻ mới)~~: Yêu cầu OTP — **không được phép** đọc OTP qua Voice/Chat.
> - ~~`proc_sms_banking` (Đăng ký/Hủy SMS Banking)~~: API `toggle_sms_banking` chưa tồn tại ở backend.

---

## 2. Detailed Procedure Workflows

### 1. Procedure: Báo Mất Thẻ / Khóa Thẻ Khẩn Cấp (`proc_emergency_lock`)
*   **Trigger:** User lost their wallet/card, suspects card compromise, or asks to block/lock their card immediately.
*   **Security:** CCCD full number (12 digits) required. Check session memory first.
*   **Steps:**
    1.  **Session Check:** If CCCD is not yet verified in this session, ask for full CCCD number and call `verify_customer_id`.
        *   *On Failure (1st attempt):* Ask the user to repeat carefully.
        *   *On Failure (2nd attempt):* Call `system_tool_transfer` to handoff to a human agent immediately.
    2.  **Card Fetch:** Execute `get_customer_cards` using verified `customerId` from session.
    3.  **Card Selection:**
        *   *If 1 active card:* Read out the card details and ask for confirmation before locking (e.g., "Dạ em thấy anh/chị đang có thẻ Visa đuôi 1234. Anh/chị có muốn khóa thẻ này không ạ?").
        *   *If multiple active cards:* Read out all active cards and ask the user to specify the last 4 digits of the card to lock (e.g., "Dạ, em thấy mình có [N] thẻ: thẻ Visa đuôi 1234 và thẻ Mastercard đuôi 5678. Anh/chị muốn khóa thẻ nào ạ?").
    4.  **Action:** Call `execute_card_lock` with `customerId` (from session) and `card_last_four` (confirmed by user).
    5.  **Output:** Read the `spokenMessage` from the API response directly to the user. Ask if they need further assistance.

---

### 2. Procedure: Tra Cứu Số Dư Tài Khoản / Thẻ (`proc_check_balance`)
*   **Trigger:** "Xem số dư", "Tôi còn bao nhiêu tiền", "Tài khoản có bao nhiêu tiền".
*   **Security:** CCCD full number required (with session memory bypass on subsequent requests).
*   **Steps:**
    1.  **Session Check:** If CCCD is not yet verified, ask for full CCCD number and call `verify_customer_id`.
        *   *On Failure (1st attempt):* Ask the user to repeat carefully.
        *   *On Failure (2nd attempt):* Deny access and ask user to visit a branch.
    2.  **Card Fetch:** Execute `get_customer_cards` using `customerId` from session.
    3.  **Card Selection:**
        *   *If 1 active card:* Proceed directly to fetch balance for that card.
        *   *If multiple active cards:* Read out all active cards and ask which one they want to check.
    4.  **Action:** Call `get_card_balance` with `customerId` (from session) and `card_last_four`.
    5.  **Output:** Read the `spokenBalance` from the API response directly to the user (e.g., "Dạ, số dư khả dụng của thẻ đuôi 1234 là mười lăm triệu đồng ạ"). Do NOT just read the number; use the pre-formatted spoken text.

---

### 3. Procedure: Tra Cứu Lịch Sử Giao Dịch (`proc_recent_tx`)
*   **Trigger:** "Xem lịch sử giao dịch", "Tôi mới chuyển khoản/nhận tiền được chưa", "Tra cứu giao dịch gần đây", "Tại sao số dư bị trừ".
*   **Security:** CCCD full number required (with session memory bypass).
*   **Steps:**
    1.  **Session Check:** Verify CCCD if not already authenticated in this session.
    2.  **Card/Account Fetch:** Execute `get_customer_cards` using `customerId` from session.
    3.  **Card Selection:** If multiple active cards exist, ask user to select which card's history to view.
    4.  **Action:** Call `get_recent_transactions` with `customerId` and `limit=3` (default). Returns last 3 transactions with date, amount, type, and description.
    5.  **Output:** Read out each transaction clearly, converting timestamps to natural Vietnamese (e.g., "Dạ, giao dịch gần nhất là vào ngày 22 tháng 8, rút năm mươi nghìn đồng tại ATM ạ..."). For negative amounts, say "trừ [amount]"; for positive, say "cộng [amount]".

---

### 4. Procedure: Báo Cáo Giao Dịch Gian Lận (`proc_fraud_report`)
*   **Trigger:** "Tôi bị trừ tiền lạ", "Giao dịch không phải tôi làm", "Ai đó hack tài khoản tôi", "Tôi không thực hiện giao dịch này".
*   **Security:** Emergency Flow — minimize time-to-lock.
*   **Steps:**
    1.  **Immediate Offer:** Offer to lock the card immediately to prevent further fraudulent transactions. Do not ask for lengthy verification first.
    2.  **Session Check:** If CCCD is not verified, ask for full CCCD number and call `verify_customer_id`. If authentication fails once, still proceed with `system_tool_transfer` to escalate immediately.
    3.  **Card Fetch & Lock:** Execute `get_customer_cards`. If the user identifies the affected card (by last 4 digits), call `execute_card_lock` immediately.
    4.  **Transfer:** After locking (or if authentication fails), immediately initiate human handoff via `system_tool_transfer` to the Fraud/Risk Management team. Inform the user:
        > "Dạ em đã ghi nhận và khóa thẻ để bảo vệ tài sản của anh/chị. Em đang chuyển anh/chị đến bộ phận xử lý khiếu nại giao dịch để hỗ trợ thêm ạ."

---

### 5. Procedure: Nghiệp Vụ Ngoài Phạm Vi Hỗ Trợ (`proc_unsupported`)
*   **Trigger:** Any request the agent is not trained to handle, including:
    *   **Mở khóa thẻ / Kích hoạt thẻ mới** (requires OTP — out-of-scope for voice agent)
    *   **Đăng ký / Hủy SMS Banking** (API not yet available)
    *   **Tư vấn vay vốn, vay mua nhà, vay doanh nghiệp**
    *   **Mở tài khoản, khiếu nại phức tạp, thương lượng lãi suất**
*   **Content:**
    Tell the user: *"Dạ đối với yêu cầu này, em chưa được cấp quyền hỗ trợ trực tiếp. Để được hỗ trợ chính xác nhất, em xin phép chuyển tiếp cuộc trò chuyện của anh/chị đến chuyên viên tư vấn của ngân hàng ạ."*
    Then execute `[system_tool id="transfer_call"]`.

---

## 3. Human Handoff (Fallback) Standards

For any of the following scenarios, the agent must immediately route to a human agent:

1.  **Double Authentication Failure:** User fails CCCD check twice in a row.
2.  **Out-of-Scope Requests:** OTP verification, card unlock, card activation, SMS Banking registration, corporate accounts, loan applications, complex disputes.
3.  **Sentiment Trigger:** User becomes extremely angry, uses profanity, explicitly insists on talking to a human, or expresses distress.
4.  **Fraud Report:** Always escalate to a human after locking the card in a fraud scenario.

> [!CAUTION]
> **Safety Rules (Non-Negotiable):**
> - **Never** ask the user to read out OTP, CVV/CVC, card expiration date, or passwords under any circumstance.
> - **Never** attempt to handle card unlock or card activation via the voice/chat channel.
> - **Never** repeat the CCCD number back verbatim to the user.
