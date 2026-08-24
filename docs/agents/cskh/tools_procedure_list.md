<!--
name: tools_procedure_list.md
description: Requirements for server-side webhook tools and deterministic agent procedures for banking CSKH.
-->
# Tools & Procedures Requirements

Based on the agent requirements, the Agent needs a mix of Server-side Tools to integrate with the core banking system (CBS) and Procedures to enforce deterministic workflows.

> [!NOTE]
> **Scope decision (2026-08-22):** OTP-based tools (`send_otp`, `verify_otp`) and `toggle_sms_banking` are **removed from scope**. Procedures requiring them (`proc_unlock_card`, `proc_activate_card`, `proc_sms_banking`) are now classified as **Unsupported In-Scope (Handoff)** — Agent will transfer to a human operator when triggered.

---

## 1. Server-side Webhook Tools (Active)

These tools are configured in the ElevenLabs dashboard to hit the backend API endpoints.

| Tool ID | Tool Name | Maps to API | Description | Inputs |
| :--- | :--- | :--- | :--- | :--- |
| `tool_verify_cccd` | `verify_customer_id` | `POST /api/v1/cskh/customer/verify` | Verifies the full CCCD (12 digits) provided by the user. Returns `customerId` and `fullName` to store in session. | `cccd_number` (string) |
| `tool_get_cards` | `get_customer_cards` | `GET /api/v1/cskh/customer/cards?customerId=` | Retrieves the list of cards (type, last 4 digits, status) for an authenticated customer. | `customerId` (string) |
| `tool_lock_card` | `execute_card_lock` | `POST /api/v1/cskh/customer/lock-card` | Locks a specific card of the user. Requires authenticated `customerId`. | `customerId` (string), `card_last_four` (string) |
| `tool_get_balance` | `get_card_balance` | `GET /api/v1/cskh/customer/balance` | Retrieves available balance for a specific card. Returns numeric balance and pre-formatted Vietnamese speech text (`spokenBalance`). | `customerId` (string), `card_last_four` (string) |
| `tool_get_transactions` | `get_recent_transactions` | `GET /api/v1/cskh/account/transactions` | Retrieves the last N recent transactions for a card. Default limit=3. | `customerId` (string), `limit` (number, optional) |
| `sys_transfer` | `system_tool_transfer` | Built-in ElevenLabs | Routes the call/chat session to a human operator. | N/A |
| `sys_end_call` | `system_tool_end` | Built-in ElevenLabs | Terminates the call/chat session. | N/A |

---

## 2. Deprecated / Out-of-Scope Tools (Do NOT configure)

The following tools are intentionally **not configured** and must not be added to the ElevenLabs agent toolset:

| Tool Name | Reason for Exclusion |
| :--- | :--- |
| `send_otp` | Reading OTP over Voice/Chat is prohibited (Social Engineering risk). API not yet available. |
| `verify_otp` | Same as above. Procedures requiring OTP verification are routed to human handoff. |
| `toggle_sms_banking` | API endpoint does not exist in the current backend. Feature is planned for future sprint. |
| `execute_card_unlock` | Depends on OTP verification — out-of-scope for agent. |
| `execute_card_activation` | Depends on OTP verification — out-of-scope for agent. |

---

## 3. Procedures Design (Active)

### Procedure 1: Báo Mất Thẻ / Khóa Thẻ Khẩn Cấp (`proc_emergency_lock`)
*   **Type:** Structured Procedure (Deterministic)
*   **Trigger:** "When the user says they lost their wallet, lost their card, or asks to lock/block their card immediately."
*   **Steps:**
    1.  **Ask:** "Ask the user to provide their full CCCD number (12 digits) to authenticate (if not already authenticated in this session)."
    2.  **Tool:** `verify_customer_id`.
        *   *On 1st Failure:* Ask the user to try again carefully.
        *   *On 2nd Failure (Fallback):* Call `system_tool_transfer` immediately.
    3.  **Tool:** `get_customer_cards` (pass `customerId` from session — NOT the raw CCCD).
    4.  **Identify Card to Lock:**
        *   *If 1 active card:* Ask for confirmation before locking.
        *   *If multiple active cards:* List them and ask which card (by last 4 digits) to lock.
    5.  **Tool:** `execute_card_lock` (pass `customerId` from session + `card_last_four` confirmed by user).
    6.  **Say:** Read the `spokenMessage` from the API response directly.
    7.  **System Tool:** Ask if they need further assistance, then `system_tool_end` or remain available.

### Procedure 2: Tra Cứu Số Dư Tài Khoản / Thẻ (`proc_check_balance`)
*   **Type:** Structured Procedure (Deterministic)
*   **Trigger:** "When the user asks to check their account balance, how much money is left, or their card/account balance."
*   **Steps:**
    1.  **Ask:** "Ask the user for their full CCCD number to authenticate (if not already authenticated in this session)."
    2.  **Tool:** `verify_customer_id`.
        *   *On 1st Failure:* Ask the user to try again.
        *   *On 2nd Failure:* Deny request, ask user to contact a branch.
    3.  **Tool:** `get_customer_cards` (pass `customerId` from session).
    4.  **Identify Card:**
        *   *If 1 active card:* Proceed directly.
        *   *If multiple active cards:* Ask user to specify which card (by last 4 digits).
    5.  **Tool:** `get_card_balance` (pass `customerId` from session + `card_last_four`).
    6.  **Say:** Read the `spokenBalance` from the API response.

### Procedure 3: Tra Cứu Lịch Sử Giao Dịch (`proc_recent_tx`)
*   **Type:** Structured Procedure (Deterministic)
*   **Trigger:** "When the user asks about recent transactions, why their balance changed, or whether a transfer went through."
*   **Steps:**
    1.  **Ask:** Authenticate via CCCD if not already done this session.
    2.  **Tool:** `get_customer_cards` (pass `customerId` from session).
    3.  **Identify Card:** Ask user to select card if multiple active cards exist.
    4.  **Tool:** `get_recent_transactions` (pass `customerId` + `limit=3`).
    5.  **Say:** Read each transaction clearly in natural Vietnamese, including date, amount, and description.

### Procedure 4: Nghiệp Vụ Ngoài Phạm Vi (`proc_unsupported`)
*   **Type:** Free-form Procedure
*   **Trigger:** "When the user requests any of the following: card unlock, card activation, OTP-related services, SMS Banking registration/cancellation, corporate loans, opening letters of credit, or any banking service the agent is not trained to handle."
*   **Content:**
    ```markdown
    Tell the user: "Dạ đối với yêu cầu này, em chưa được cấp quyền hỗ trợ trực tiếp. Để được hỗ trợ chính xác nhất, em xin phép chuyển tiếp cuộc trò chuyện của anh/chị đến chuyên viên tư vấn của ngân hàng ạ."
    Then execute [system_tool id="transfer_call"].
    ```
