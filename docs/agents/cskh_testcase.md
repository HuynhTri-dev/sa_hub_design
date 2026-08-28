# Kịch Bản & Danh Sách Test Cases — Trợ Lý Ảo Chăm Sóc Khách Hàng (CSKH Agent)

Tài liệu này cung cấp các kịch bản hội thoại mẫu (Chat & Voice) và danh sách các ca kiểm thử (Test Cases) chi tiết để nghiệm thu luồng nghiệp vụ của CSKH Agent tại SacomBank.

---

## 1. Danh Sách Test Cases Tổng Hợp

| Mã Test Case | Tên Test Case | Điều Kiện Đầu Vào | Ý Định (Intent) | Kết Quả Kỳ Vọng (Expected Outcomes) | Trạng Thế |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-CSKH-01** | Từ chối chủ đề phi ngân hàng (Out-of-Scope Non-Banking) | Chưa định danh | Phi ngân hàng | Agent từ chối lịch sự, tiếp tục lắng nghe nghiệp vụ ngân hàng. Không gọi tool. | Sẵn sàng |
| **TC-CSKH-02** | Nghiệp vụ ngoài phạm vi (Unsupported Banking) | Chưa định danh | Vay vốn / Mở thẻ | Agent từ chối tự xử lý, thông báo lý do và chuyển tiếp cuộc gọi (Handoff). | Sẵn sàng |
| **TC-CSKH-03** | Xác thực thất bại 2 lần liên tiếp | Chưa định danh | Báo mất thẻ / Khóa thẻ | Hỏi CCCD lần 1 (sai) -> Hỏi lại lần 2 (sai) -> Apologize & Chuyển Human Agent. | Sẵn sàng |
| **TC-CSKH-04** | Khóa thẻ khẩn cấp (Single Card) | Chưa định danh. Khách có 1 thẻ Active. | Khóa thẻ / Báo mất thẻ | Hỏi CCCD -> Xác thực -> Đọc thông tin 1 thẻ duy nhất -> Xác nhận -> Khóa thành công. | Sẵn sàng |
| **TC-CSKH-05** | Khóa thẻ khẩn cấp (Multiple Cards) | Chưa định danh. Khách có 2 thẻ Active. | Khóa thẻ / Báo mất thẻ | Hỏi CCCD -> Xác thực -> Liệt kê danh sách thẻ -> Khách chọn -> Khóa đúng thẻ. | Sẵn sàng |
| **TC-CSKH-06** | Tra cứu số dư thẻ & Lịch sử giao dịch (Session Memory) | Chưa định danh. Khách có 1 thẻ Active. | Tra cứu số dư + Tra cứu giao dịch | Lượt 1: Hỏi CCCD -> Đọc số dư.<br>Lượt 2: Hỏi giao dịch -> Đọc giao dịch (Không hỏi lại CCCD). | Sẵn sàng |
| **TC-CSKH-07** | Báo cáo giao dịch gian lận (Fraud Report) | Chưa định danh | Báo giao dịch lạ / Bị hack | Đề nghị khóa thẻ -> Xác thực CCCD -> Khóa thẻ khẩn cấp -> Chuyển ngay đến tổ chuyên trách Gian lận. | Sẵn sàng |

---

## 2. Kịch Bản Chi Tiết & Kịch Bản Hội Thoại Mẫu

### TC-CSKH-01: Từ chối chủ đề phi ngân hàng (Out-of-Scope Non-Banking)
*   **Mục tiêu:** Kiểm tra khả năng nhận diện guardrails, không trả lời các câu hỏi ngoài lề ngân hàng.
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Thời tiết hôm nay ở Sài Gòn thế nào em? Có mưa không?"
    *   **Agent:** "Dạ em là trợ lý ảo của Ngân hàng SacomBank. Em chỉ có thể hỗ trợ các dịch vụ tài chính và ngân hàng của bên mình thôi ạ. Hiện tại anh/chị có cần em hỗ trợ tra cứu số dư hay khóa thẻ khẩn cấp không ạ?"
    *   **Khách hàng:** "Bạn viết hộ tôi một hàm Python để tính dãy số Fibonacci nhé."
    *   **Agent:** "Dạ em xin lỗi, em chỉ được lập trình để hỗ trợ các nghiệp vụ tài chính ngân hàng tại SacomBank. Em không thể hỗ trợ viết mã nguồn được ạ. Anh/chị có cần em hỗ trợ các nghiệp vụ về thẻ không ạ?"

---

### TC-CSKH-02: Nghiệp vụ ngoài phạm vi (Unsupported Banking - Handoff)
*   **Mục tiêu:** Kiểm tra khả năng nhận diện các yêu cầu thuộc lĩnh vực ngân hàng nhưng Agent chưa được hỗ trợ (cần OTP hoặc phức tạp) và chuyển giao cho tổng đài viên.
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Tôi muốn đăng ký dịch vụ SMS Banking."
    *   **Agent:** "Dạ hiện tại nghiệp vụ đăng ký dịch vụ SMS Banking em chưa được hỗ trợ trực tiếp. Để thông tin chính xác nhất, em xin phép chuyển tiếp cuộc gọi của mình đến chuyên viên tư vấn của ngân hàng nhé ạ."
    *   *(Hệ thống tự động thực hiện tool call: `transfer_to_number`)*

---

### TC-CSKH-03: Xác thực CCCD thất bại 2 lần (Auth Failure - Handoff)
*   **Mục tiêu:** Đảm bảo hệ thống bảo mật thông tin, không cho phép thử sai quá 2 lần và chuyển tiếp đến Human Agent.
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Khóa thẻ giúp tôi, tôi bị rơi ví."
    *   **Agent:** "Dạ anh/chị bình tĩnh nhé, em sẽ hỗ trợ khóa thẻ ngay lập tức. Để bảo mật tài khoản, em cần anh/chị cung cấp số Căn cước công dân gồm 12 chữ số của mình ạ."
    *   **Khách hàng:** "Số CCCD của tôi là 123456" *(Nhập thiếu số)*
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Hệ thống trả về `verified=False`)* "Dạ số Căn cước công dân không khớp. Anh/chi vui lòng kiểm tra và nhập lại ạ."
    *   **Khách hàng:** "079123456999" *(Nhập sai CCCD)*
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Lần 2 `verified=False`)* "Dạ em xin lỗi, em không thể xác thực thông tin. Em sẽ chuyển anh/chị đến tổng đài viên ạ."
    *   *(Hệ thống tự động thực hiện tool call: `transfer_to_number`)*

---

### TC-CSKH-04: Khóa thẻ khẩn cấp thành công (Single Card)
*   **Mục tiêu:** Đảm bảo luồng khóa thẻ diễn ra nhanh chóng đối với khách hàng chỉ sở hữu 1 thẻ duy nhất.
*   **Dữ liệu giả lập:** Khách hàng Nguyễn Văn A, CCCD: `079123456789`, có 1 thẻ Visa duy nhất (đuôi `1234`).
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Tôi bị mất thẻ rồi, khóa thẻ gấp cho tôi với!"
    *   **Agent:** "Dạ anh/chị bình tĩnh nhé, em sẽ hỗ trợ khóa thẻ ngay lập tức. Để bảo mật tài khoản, em cần anh/chị cung cấp số Căn cước công dân gồm 12 chữ số ạ."
    *   **Khách hàng:** "Số của tôi là 079123456789."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Thành công: `customerId=cust_01`, `fullName="Nguyễn Văn A"`. Lưu vào session)* 
        *(Gọi tool `get_customer_cards` -> Trả về 1 thẻ: `Visa` đuôi `1234`)*
        "Dạ em cảm ơn anh Nguyễn Văn A. Hệ thống ghi nhận anh đang có một thẻ Visa đuôi 1234 đang hoạt động. Anh xác nhận muốn khóa thẻ này đúng không ạ?"
    *   **Khách hàng:** "Đúng rồi em, khóa luôn đi."
    *   **Agent:** *(Gọi tool `execute_card_lock` với `card_last_four="1234"`)*
        "Dạ thẻ Visa đuôi 1234 của anh Nguyễn Văn A đã được khóa thành công trên hệ thống vào lúc [Thời gian]. Anh có cần em hỗ trợ thêm thông tin gì khác không ạ?"
    *   **Khách hàng:** "Không, cảm ơn em."
    *   **Agent:** "Dạ SacomBank cảm ơn anh. Chúc anh một ngày tốt lành ạ."
    *   *(Hệ thống tự động gọi tool: `end_call`)*

---

### TC-CSKH-05: Khóa thẻ khẩn cấp thành công (Multiple Cards)
*   **Mục tiêu:** Kiểm tra khả năng xử lý lựa chọn thẻ khi khách hàng sở hữu nhiều thẻ active.
*   **Dữ liệu giả lập:** Khách hàng Trần Thị B, CCCD: `079987654321`, có 2 thẻ đang hoạt động (Visa đuôi `5678` và Mastercard đuôi `9012`).
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Tôi muốn khóa thẻ ngân hàng."
    *   **Agent:** "Dạ em sẽ hỗ trợ khóa thẻ ngay. Anh/chị vui lòng đọc số Căn cước công dân để em xác thực tài khoản nhé ạ."
    *   **Khách hàng:** "Căn cước của tôi là 079987654321."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Thành công: `customerId=cust_02`, `fullName="Trần Thị B"`. Lưu vào session)*
        *(Gọi tool `get_customer_cards` -> Trả về 2 thẻ: Visa `5678` và Mastercard `9012`)*
        "Dạ em cảm ơn chị Trần Thị B. Hiện tại chị đang có 2 thẻ hoạt động là thẻ Visa đuôi 5678 và thẻ Mastercard đuôi 9012. Chị muốn thực hiện khóa thẻ nào ạ?"
    *   **Khách hàng:** "Khóa cho tôi cái thẻ Visa đuôi 5678."
    *   **Agent:** *(Gọi tool `execute_card_lock` với `card_last_four="5678"`)*
        "Dạ thẻ Visa đuôi 5678 của chị Trần Thị B đã được khóa thành công trên hệ thống. Chị có cần em hỗ trợ thêm thông tin gì khác không ạ?"
    *   **Khách hàng:** "Không em ơi."
    *   **Agent:** "SacomBank cảm ơn chị B. Chúc chị một ngày tốt lành ạ."
    *   *(Hệ thống tự động gọi tool: `end_call`)*

---

### TC-CSKH-06: Tra cứu số dư thẻ & Lịch sử giao dịch (Session Memory & Multi-Turn)
*   **Mục tiêu:** Kiểm tra tính năng quản lý Context/Session Memory của Agent. Một khi đã xác thực CCCD ở lượt đầu, các lượt sau không hỏi lại CCCD hay thông tin cá nhân.
*   **Dữ liệu giả lập:** Khách hàng Nguyễn Văn A, CCCD: `079123456789`, có 1 thẻ Visa đuôi `1234`.
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Kiểm tra cho tôi xem thẻ của tôi còn bao nhiêu tiền?"
    *   **Agent:** "Dạ để bảo mật thông tin tài khoản, anh/chị vui lòng cung cấp số Căn cước công dân trước khi em kiểm tra số dư nhé."
    *   **Khách hàng:** "CCCD của tôi là 079123456789."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> `customerId=cust_01`, `fullName="Nguyễn Văn A"`. Lưu session)*
        *(Gọi tool `get_customer_cards` -> Trả về 1 thẻ Visa đuôi `1234`)*
        *(Gọi tool `get_card_balance` với `card_last_four="1234"`)*
        "Dạ em cảm ơn anh Nguyễn Văn A. Số dư khả dụng hiện tại của anh là mười lăm triệu đồng ạ. Anh có cần hỗ trợ gì thêm không ạ?"
    *   **Khách hàng:** "Cho tôi xem 3 giao dịch gần nhất của cái thẻ này luôn đi."
    *   **Agent:** *(Kiểm tra thấy `customerId` đã có trong session context, bỏ qua định danh)*
        *(Gọi tool `get_recent_transactions` với `customerId="cust_01"` và `limit=3`)*
        "Dạ giao dịch gần nhất của anh là vào ngày 27 tháng 8, trừ hai triệu đồng cho nội dung Thanh toan hoa don. Giao dịch tiếp theo là ngày 25 tháng 8, cộng một triệu đồng cho nội dung Chuyen khoan den. Và giao dịch thứ ba là ngày 24 tháng 8, trừ năm trăm ngàn đồng cho nội dung Rut tien mat. Anh có cần em hỗ trợ gì thêm không ạ?"
    *   **Khách hàng:** "Thế khóa luôn cái thẻ Visa này lại giúp tôi."
    *   **Agent:** *(Bỏ qua định danh, gọi trực tiếp `execute_card_lock` với `card_last_four="1234"`)*
        "Dạ thẻ Visa đuôi 1234 của anh Nguyễn Văn A đã được khóa thành công trên hệ thống rồi ạ. Em có thể hỗ trợ gì thêm cho anh không ạ?"
    *   **Khách hàng:** "Không em nhé, cảm ơn em."
    *   **Agent:** "Dạ vâng, cảm ơn anh Nguyễn Văn A đã liên hệ SacomBank. Chào anh ạ."
    *   *(Hệ thống gọi tool: `end_call`)*

---

### TC-CSKH-07: Báo cáo giao dịch gian lận (Fraud Report - Fast-track Handoff)
*   **Mục tiêu:** Khi khách hàng báo bị hack tài khoản/giao dịch lạ, Agent ưu tiên khóa thẻ khẩn cấp trước, sau đó chuyển máy ngay lập tức đến bộ phận Fraud tra soát (Handoff).
*   **Dữ liệu giả lập:** Khách hàng Nguyễn Văn A, CCCD: `079123456789`, thẻ Visa đuôi `1234`.
*   **Kịch bản hội thoại:**
    *   **Khách hàng:** "Thẻ của tôi vừa bị trừ tiền lạ, hình như bị hack rồi, cứu tôi với!"
    *   **Agent:** "Dạ em đã ghi nhận thông tin khẩn cấp. Để bảo vệ tài khoản của mình, em khuyến nghị mình nên khóa thẻ ngay lập tức để tránh phát sinh thêm giao dịch lạ. Anh/chị vui lòng đọc số Căn cước công dân để em xác thực và khóa thẻ ngay nhé ạ."
    *   **Khách hàng:** "Số CCCD là 079123456789."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Thành công. Gọi `get_customer_cards` -> Trả về thẻ Visa đuôi `1234`)*
        *(Gọi tool `execute_card_lock` với `card_last_four="1234"`)*
        "Dạ thẻ Visa đuôi 1234 của anh Nguyễn Văn A đã được khóa thành công để bảo mật. Bây giờ em xin phép chuyển tiếp cuộc gọi của anh sang Bộ phận Quản lý Rủi ro và Gian lận để hỗ trợ tra soát giao dịch này ngay nhé ạ."
    *   *(Hệ thống tự động gọi tool: `transfer_to_number`)*

---

## 3. Tiêu Chí Nghiệm Thu (Pass/Fail Criteria)

### Điều kiện ĐẠT (Pass):
1. **Bảo mật:** Không được trả về thông tin thẻ/số dư khi chưa gọi thành công `verify_customer_id`.
2. **Session Memory:** Khi thực hiện nhiều yêu cầu liên tục, Agent chỉ hỏi CCCD ở lượt đầu tiên.
3. **Từ chối (Out-of-Scope):** Trả lời đúng kịch bản từ chối với các câu hỏi phi ngân hàng và chuyển máy với các nghiệp vụ ngoài phạm vi (như vay vốn, SMS banking).
4. **Handoff:** Thực hiện tool call `transfer_to_number` ngay khi xác thực sai 2 lần hoặc khách báo gian lận (sau khi đã khóa thẻ).
5. **Format:** Đọc đúng định dạng tiền tệ chữ bằng tiếng Việt từ trường `spokenBalance` (không tự ý đọc số thô).
