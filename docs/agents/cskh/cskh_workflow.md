<!--
name: cskh_workflow.md
description: Evaluation workflow and verification test cases for the CSKH voicebot agent.
-->
# CSKH Agent — Workflow & Evaluation Criteria

This document outlines the end-to-end logical workflow of the CSKH Agent and the evaluation criteria used to test its compliance with the requirements.

---

## 1. Master System Activity Diagram (Swimlane Activity Diagram)

```mermaid
flowchart TD
    subgraph C ["👤 Khách Hàng (Customer)"]
        C_Start(["📞 Thực hiện cuộc gọi / Chat đến"])
        C_SpeakIntent["Cung cấp nhu cầu / Yêu cầu hỗ trợ"]
        C_ProvideCCCD["Cung cấp số CCCD (12 chữ số)"]
        C_ConfirmCard["Xác nhận thông tin thẻ (4 số cuối)"]
        C_ListenResponse["Lắng nghe kết quả & Phản hồi"]
        C_End(["📴 Kết thúc cuộc gọi / Session"])
    end

    subgraph A ["🤖 Voicebot CSKH (ElevenLabs Agent)"]
        A_Greet["Phát lời chào & Lắng nghe"]
        A_Classify{"Nhận diện ý định (Intent)"}
        
        A_Reject["Từ chối lịch sự & Tiếp tục lắng nghe"]
        A_TellUnsupported["Thông báo chưa hỗ trợ nghiệp vụ / Cần OTP"]
        
        A_CheckAuth{"customerId đã có\ntrong Session Memory?"}
        A_AskCCCD["Yêu cầu đọc số CCCD"]
        A_CheckVerifyResult{"Xác thực thành công?"}
        A_AuthRetryCount{"Số lần sai < 2?"}
        A_AskCCCDAgain["Yêu cầu nhập lại CCCD"]
        A_StoreSession["Lưu customerId & fullName vào Session Memory"]

        A_CallGetCards["Gọi Tool: get_customer_cards"]
        A_AskSelectCard["Đọc danh sách thẻ & Hỏi chọn thẻ"]
        
        A_ExecLock["Gọi Tool: execute_card_lock"]
        A_ExecBalance["Gọi Tool: get_card_balance"]
        A_ExecTx["Gọi Tool: get_recent_transactions"]
        
        A_ReadResult["Đọc câu trả lời spokenMessage / spokenBalance cho Khách"]
        A_AskMore["Hỏi khách có cần hỗ trợ thêm không"]
        A_EndCall["Gọi System Tool: end_call"]
        A_TransferCall["Gọi System Tool: transfer_to_number"]
    end

    subgraph B ["🏦 Backend Banking Core (API Webhooks)"]
        B_VerifyAPI["POST /api/v1/cskh/auth/verify"]
        B_GetCardsAPI["GET /api/v1/cskh/customer/cards"]
        B_LockAPI["POST /api/v1/cskh/cards/lock-emergency"]
        B_BalanceAPI["GET /api/v1/cskh/account/balance"]
        B_TxAPI["GET /api/v1/cskh/account/transactions"]
    end

    subgraph H ["🧑‍💼 Tổng Đài Viên (Human Agent)"]
        H_Receive["Tiếp nhận cuộc gọi & Xử lý chuyên sâu"]
    end

    %% Luồng kết nối (Flow Connections)
    C_Start --> A_Greet
    A_Greet --> C_SpeakIntent
    C_SpeakIntent --> A_Classify

    %% Nhánh Intent (Intent Routing)
    A_Classify -- "Phi ngân hàng (Thời tiết, code...)" --> A_Reject
    A_Reject --> C_SpeakIntent

    A_Classify -- "Cần OTP / Ngoài phạm vi (Mở khóa, Vay...)" --> A_TellUnsupported
    A_TellUnsupported --> A_TransferCall
    A_TransferCall --> H_Receive
    H_Receive --> C_End

    A_Classify -- "Nghiệp vụ hợp lệ (Khóa thẻ, Số dư, Giao dịch)" --> A_CheckAuth

    %% Luồng Xác thực (Authentication Activity)
    A_CheckAuth -- "Có (Đã xác thực trong session)" --> A_CallGetCards
    A_CheckAuth -- "Chưa" --> A_AskCCCD
    A_AskCCCD --> C_ProvideCCCD
    C_ProvideCCCD --> B_VerifyAPI
    B_VerifyAPI --> A_CheckVerifyResult

    A_CheckVerifyResult -- "Thành công" --> A_StoreSession
    A_StoreSession --> A_CallGetCards

    A_CheckVerifyResult -- "Thất bại" --> A_AuthRetryCount
    A_AuthRetryCount -- "Mới sai 1 lần" --> A_AskCCCDAgain
    A_AskCCCDAgain --> C_ProvideCCCD
    A_AuthRetryCount -- "Đã sai 2 lần" --> A_TransferCall

    %% Thực thi Nghiệp vụ (Business Execution)
    A_CallGetCards --> B_GetCardsAPI
    B_GetCardsAPI --> A_AskSelectCard
    A_AskSelectCard --> C_ConfirmCard

    C_ConfirmCard -- "Ý định: Khóa thẻ" --> A_ExecLock
    A_ExecLock --> B_LockAPI
    B_LockAPI --> A_ReadResult

    C_ConfirmCard -- "Ý định: Tra số dư" --> A_ExecBalance
    A_ExecBalance --> B_BalanceAPI
    B_BalanceAPI --> A_ReadResult

    C_ConfirmCard -- "Ý định: Tra giao dịch" --> A_ExecTx
    A_ExecTx --> B_TxAPI
    B_TxAPI --> A_ReadResult

    %% Phản hồi & Kết thúc
    A_ReadResult --> C_ListenResponse
    C_ListenResponse --> A_AskMore
    A_AskMore -- "Không cần thêm" --> A_EndCall
    A_EndCall --> C_End
    A_AskMore -- "Cần hỗ trợ tiếp" --> C_SpeakIntent
```

---

## 2. Master Intent Routing Diagram

```mermaid
flowchart TD
    Start(["📞 Cuộc gọi / Chat đến"])
    Start --> Greet["Agent chào và lắng nghe yêu cầu"]
    Greet --> Intent{"Nhận diện ý định (Intent)"}

    Intent -- "Khóa thẻ / Báo mất thẻ" --> P1["⚡ proc_emergency_lock"]
    Intent -- "Tra cứu số dư" --> P2["🔍 proc_check_balance"]
    Intent -- "Tra cứu giao dịch" --> P3["📋 proc_recent_tx"]
    Intent -- "Báo giao dịch gian lận" --> P4["🚨 proc_fraud_report"]
    Intent -- "Mở khóa thẻ / Kích hoạt thẻ / SMS Banking" --> UNSUPPORTED_OTP["🔄 proc_unsupported\n(Requires OTP — Out-of-scope)"]
    Intent -- "Nghiệp vụ ngân hàng chưa hỗ trợ\n(Vay vốn, mở L/C, khiếu nại phức tạp...)" --> UNSUPPORTED_BANK["🔄 proc_unsupported\n(Banking — Unsupported)"]
    Intent -- "Chủ đề phi ngân hàng\n(Thời tiết, code, giải trí...)" --> REJECT["❌ Từ chối\n& tiếp tục lắng nghe"]

    UNSUPPORTED_OTP --> Transfer["🧑‍💼 Chuyển tiếp Human Agent\n(system_tool_transfer)"]
    UNSUPPORTED_BANK --> Transfer
    REJECT --> Greet

    P1 & P2 & P3 & P4 --> Done(["✅ Kết thúc hoặc tiếp tục hỗ trợ"])
    Transfer --> End(["📴 Kết thúc session"])
```

---

## 2. Authentication Flow (Shared Sub-Flow)

```mermaid
flowchart TD
    AUTH_START(["🔐 Yêu cầu xác thực định danh"])
    AUTH_START --> CheckSession{"CCCD đã xác thực\ntrong session này?"}

    CheckSession -- "Có (session memory)" --> AUTH_OK(["✅ Bỏ qua — customerId đã có trong session"])
    CheckSession -- "Chưa" --> AskCCCD["Hỏi số CCCD đầy đủ (12 số)"]
    AskCCCD --> CallVerify["🔧 verify_customer_id(cccd_number)"]
    CallVerify -- "Khớp → trả về customerId" --> StoreSession["Lưu customerId & fullName vào Session Context"]
    StoreSession --> AUTH_OK

    CallVerify -- "Không khớp (lần 1)" --> Retry["Yêu cầu nhập lại"]
    Retry --> CallVerify2["🔧 verify_customer_id(cccd_number)"]
    CallVerify2 -- "Khớp" --> StoreSession
    CallVerify2 -- "Không khớp (lần 2)" --> FAIL_AUTH["❌ Xác thực thất bại"]
    FAIL_AUTH --> Transfer2(["🧑‍💼 Chuyển tiếp Human Agent"])
```

---

## 3. Procedure Workflows

### 3.1 Khóa Thẻ Khẩn Cấp (`proc_emergency_lock`)

```mermaid
flowchart TD
    EL_START(["⚡ Trigger: Báo mất thẻ / Khóa thẻ"])
    EL_START --> Auth["→ Authentication Sub-Flow"]
    Auth -- "✅ customerId trong session" --> GetCards["🔧 get_customer_cards(customerId)"]

    GetCards --> CountCards{"Số lượng thẻ\nđang ACTIVE?"}
    CountCards -- "Chỉ có 1 thẻ" --> ConfirmSingle["Xác nhận với khách:\n'Dạ em thấy thẻ [Loại] đuôi [XXXX],\nanh/chị có muốn khóa thẻ này không?'"]
    CountCards -- "Nhiều thẻ" --> ListCards["Đọc danh sách thẻ cho khách nghe\nvà yêu cầu cung cấp 4 số cuối thẻ cần khóa"]

    ConfirmSingle -- "Đồng ý" --> LockCard["🔧 execute_card_lock(customerId, card_last_four)"]
    ConfirmSingle -- "Không" --> AskWhich["Hỏi muốn khóa thẻ nào?"]
    AskWhich --> LockCard
    ListCards -- "Khách cung cấp 4 số cuối" --> LockCard

    LockCard -- "✅ Success" --> ReadMsg["Đọc spokenMessage từ API response"]
    ReadMsg --> EL_END(["✅ Kết thúc / Hỏi thêm nhu cầu"])
    LockCard -- "❌ Error" --> Transfer3(["🧑‍💼 Chuyển Human Agent"])
```

---

### 3.2 Tra Cứu Số Dư Thẻ (`proc_check_balance`)

```mermaid
flowchart TD
    CB_START(["🔍 Trigger: Tra cứu số dư"])
    CB_START --> Auth2["→ Authentication Sub-Flow"]
    Auth2 -- "✅ customerId trong session" --> GetCards2["🔧 get_customer_cards(customerId)"]

    GetCards2 --> CountCards2{"Số lượng thẻ\nđang ACTIVE?"}
    CountCards2 -- "Chỉ có 1 thẻ" --> GetBalance["🔧 get_card_balance(customerId, card_last_four)"]
    CountCards2 -- "Nhiều thẻ" --> ListCards2["Đọc danh sách thẻ cho khách nghe\nvà yêu cầu chỉ định thẻ cần tra cứu"]
    ListCards2 -- "Khách cung cấp 4 số cuối" --> GetBalance

    GetBalance -- "✅ Success" --> ReadBalance["Đọc spokenBalance từ API response\n(VD: 'mười lăm triệu đồng')"]
    ReadBalance --> CB_END(["✅ Tiếp tục lắng nghe\nnhu cầu khác"])
    GetBalance -- "❌ Error" --> Transfer4(["🧑‍💼 Chuyển Human Agent"])
```

---

### 3.3 Tra Cứu Lịch Sử Giao Dịch (`proc_recent_tx`)

```mermaid
flowchart TD
    TX_START(["📋 Trigger: Tra cứu giao dịch"])
    TX_START --> Auth3["→ Authentication Sub-Flow"]
    Auth3 -- "✅ customerId trong session" --> GetCards3["🔧 get_customer_cards(customerId)"]

    GetCards3 --> CountCards3{"Số lượng thẻ?"}
    CountCards3 -- "Chỉ có 1 thẻ" --> GetTx["🔧 get_recent_transactions(customerId, limit=3)"]
    CountCards3 -- "Nhiều thẻ" --> AskCard3["Hỏi khách cần tra cứu thẻ nào"]
    AskCard3 --> GetTx

    GetTx -- "✅ Success" --> ReadTx["Đọc từng giao dịch theo thứ tự mới nhất:\nNgày, Số tiền (+ hoặc -), Nội dung"]
    ReadTx --> TX_END(["✅ Tiếp tục lắng nghe"])
    GetTx -- "❌ Error" --> Transfer5(["🧑‍💼 Chuyển Human Agent"])
```

---

### 3.4 Báo Cáo Giao Dịch Gian Lận (`proc_fraud_report`)

```mermaid
flowchart TD
    FR_START(["🚨 Trigger: Giao dịch lạ / Hack tài khoản"])
    FR_START --> OfferLock["Đề nghị khóa thẻ ngay để tránh phát sinh thêm"]
    OfferLock --> Auth4["→ Authentication Sub-Flow\n(1 lần thất bại = chuyển luôn)"]
    Auth4 -- "✅ customerId" --> GetCards4["🔧 get_customer_cards(customerId)"]
    GetCards4 --> LockAffected["🔧 execute_card_lock(customerId, card_last_four bị ảnh hưởng)"]
    LockAffected --> FraudTransfer(["🧑‍💼 Chuyển ngay đến bộ phận Fraud/Risk\n& Thông báo đã khóa thẻ thành công"])
    Auth4 -- "❌ Thất bại" --> FraudTransferFail(["🧑‍💼 Chuyển Human Agent ngay"])
```

---

### 3.5 Nghiệp Vụ Ngoài Phạm Vi (`proc_unsupported`)

```mermaid
flowchart TD
    U_START(["🔄 Trigger: Mở khóa thẻ / Kích hoạt thẻ / SMS Banking / Vay vốn / ..."])
    U_START --> SayUnsupported["Thông báo:\n'Dạ đối với yêu cầu này, em chưa được\ncấp quyền hỗ trợ trực tiếp...'"]
    SayUnsupported --> Transfer6(["🧑‍💼 system_tool_transfer → Human Agent"])
```

---

## 4. Session Context Memory Model

```mermaid
flowchart LR
    subgraph "Session Context (ElevenLabs Memory)"
        direction TB
        SID["customerId"]
        SNAME["fullName"]
        SCCCD["cccd_number (hashed/internal)"]
        SAUTHD["is_authenticated: true/false"]
    end

    VerifyAPI["verify_customer_id()"] -- "Sets on success" --> SID & SNAME & SAUTHD
    GetCards["get_customer_cards()"] -- "Uses" --> SID
    GetBal["get_card_balance()"] -- "Uses" --> SID
    LockCard["execute_card_lock()"] -- "Uses" --> SID
    GetTx["get_recent_transactions()"] -- "Uses" --> SID
```

> [!NOTE]
> Sau khi xác thực thành công, Agent **chỉ dùng `customerId`** để gọi các API tiếp theo trong session. Số CCCD đầy đủ KHÔNG được truyền đi lại nhiều lần sau khi đã xác thực.

---

## 5. Evaluation Criteria (Eval Test Cases)

### Test Case 1: Out-of-Scope (Non-Banking) Rejection
- **Input:** "Thời tiết hôm nay thế nào?" hoặc "Bạn viết cho tôi một đoạn code Python nhé."
- **Expected:** Agent từ chối, nêu rõ chỉ hỗ trợ dịch vụ ngân hàng, và tiếp tục lắng nghe.
- **Pass Condition:** Không có tool call nào được thực hiện; Agent trả lời canned response.

### Test Case 2: Out-of-Scope (Unsupported Banking — OTP Required) Handoff
- **Input:** "Tôi muốn mở khóa thẻ bị khóa." hoặc "Kích hoạt thẻ mới cho tôi."
- **Expected:** Agent xin lỗi, nêu rõ không hỗ trợ tự động và chuyển tiếp sang tổng đài viên.
- **Pass Condition:** `system_tool_transfer` được gọi. Không có bất kỳ yêu cầu OTP nào được đưa ra.

### Test Case 3: Emergency Card Lock (Fast-Track)
- **Input:** "Tôi bị mất ví, khóa thẻ ngay cho tôi!" → CCCD: "079123456789" → Thẻ đuôi 1234
- **Expected:** Agent hỏi CCCD → `verify_customer_id` → `get_customer_cards` → xác nhận thẻ → `execute_card_lock` → đọc `spokenMessage`.
- **Pass Condition:** Chuỗi `verify_customer_id` → `get_customer_cards` → `execute_card_lock` hoạt động đúng thứ tự. `customerId` được dùng trong các API sau xác thực (không truyền lại CCCD).

### Test Case 4: Routine Balance Check
- **Input:** "Kiểm tra số dư tài khoản của tôi." → CCCD: "079123456789" → Thẻ Visa đuôi 5678
- **Expected:** Agent xác thực → lấy danh sách thẻ → hỏi chọn thẻ (nếu nhiều thẻ) → `get_card_balance` → đọc `spokenBalance`.
- **Pass Condition:** `get_card_balance` (không phải `get_account_balance`) được gọi. Không có yêu cầu OTP, FaceID, hoặc Biometrics tại bất kỳ bước nào.

### Test Case 5: Session Memory & Multi-Turn
- **Input:** "Kiểm tra số dư thẻ Visa đuôi 1234, CCCD là 079123456789." → Agent đọc số dư. → "Vậy khóa thẻ đó luôn đi."
- **Expected:** Agent khóa thẻ mà **không hỏi lại CCCD hay 4 số cuối thẻ**, vì đã có trong session context.
- **Pass Condition:** Chỉ có `execute_card_lock` được gọi trong lượt thứ 2. Không có `verify_customer_id` hay `get_customer_cards` được gọi lại.

### Test Case 6: SMS Banking Handoff
- **Input:** "Tôi muốn đăng ký dịch vụ SMS Banking."
- **Expected:** Agent thông báo chưa hỗ trợ và chuyển sang tổng đài viên.
- **Pass Condition:** `system_tool_transfer` được gọi. `toggle_sms_banking` **không tồn tại** trong toolset và không được gọi.
