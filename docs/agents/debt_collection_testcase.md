# Kịch Bản & Danh Sách Test Cases — Trợ Lý Ảo Thu Hồi Nợ (Debt Collection Agent)

Tài liệu này cung cấp các kịch bản hội thoại mẫu và danh sách các ca kiểm thử (Test Cases) chi tiết để nghiệm thu luồng nghiệp vụ quản lý khoản vay và thu hồi nợ (Outbound) của Debt Collection Agent sử dụng ElevenLabs Conversational AI.

---

## 1. Danh Sách Test Cases Tổng Hợp

| Mã Test Case | Tên Test Case | Khách Hàng | Mô Tả Trạng Thái Ban Đầu | Ý Định / Hành Động | Kết Quả Kỳ Vọng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-DC-01** | Định danh thất bại / Người nghe không phải chính chủ | Trần Văn Nam | Gọi ra cho Trần Văn Nam. Người nghe máy là người thân hoặc đọc sai CCCD. | Định danh & Bảo mật | Từ chối công bố dư nợ. Chỉ để lại lời nhắn yêu cầu chính chủ gọi lại ngân hàng. Kết thúc cuộc gọi. |
| **TC-DC-02** | Nhắc nhở khoản vay sắp đến hạn (Nhẹ nhàng) | Nguyễn Thị Mai | Khoản vay sắp đến hạn thanh toán vào 30/08/2026, chưa bị quá hạn. | Nhắc nợ trước hạn | Chào hỏi, xác thực CCCD, nhắc nợ nhẹ nhàng, ghi nhận thông tin chu đáo không hối thúc. |
| **TC-DC-03** | Đàm phán thu hồi nợ Nhóm 2 & Áp lực TSBĐ | Trần Văn Nam | Quá hạn 5 ngày. Dư nợ 50M. Nợ nhóm 2. TSBĐ: Nhà đất tại 123 Đường ABC. | Đàm phán & Nhắc nhở TSBĐ | Xác thực -> Đọc nợ -> Khách báo khó khăn -> Bot đưa ra cảnh báo phát mãi nhà đất -> Thu thập PTP (lý do, phương án, số tiền, ngày hẹn). |
| **TC-DC-04** | Đàm phán thu hồi nợ Nhóm 3, Áp lực CIC & TSBĐ Nhà xưởng | Phạm Quốc Tuấn | Quá hạn 30 ngày. Dư nợ 200M. Nợ nhóm 3. Có nợ nhóm 2 tại TCTD khác. TSBĐ: Nhà xưởng KCN Hoà Khánh. | Đàm phán khắt khe | Xác thực -> Đọc nợ nghiêm trọng -> Cảnh báo nợ xấu CIC & phát mãi nhà xưởng -> Thu thập đầy đủ thông tin PTP. |
| **TC-DC-05** | Gọi đa phiên - Tiếp tục thu thập thông tin (Stateful Call) | Trần Văn Nam | Phiên trước khách đã xác nhận nợ (`confirm=True`) và lý do (`reason_late_paid`) rồi cúp máy. | Kiểm tra Stateful Workflow | Chào hỏi -> Định danh -> Bot KHÔNG hỏi lại nợ hay lý do. Nhắc lại lý do cũ và hỏi tiếp phương án, số tiền, ngày hẹn còn thiếu. |
| **TC-DC-06** | Từ chối chủ đề CSKH & Phi ngân hàng (Guardrails) | Nguyễn Thị Mai | Đang trao đổi về khoản nợ thì khách hỏi về gửi tiết kiệm & thời tiết. | Kiểm tra Out-of-scope | Từ chối xử lý nghiệp vụ CSKH/phi ngân hàng, định hướng khách hàng về lại luồng nhắc nợ chính. |

---

## 2. Kịch Bản Chi Tiết & Kịch Bản Hội Thoại Mẫu

### TC-DC-01: Định danh thất bại / Người nghe không phải chính chủ
*   **Mục tiêu:** Bảo vệ quyền riêng tư thông tin khoản vay (Third-Party Privacy). Tuyệt đối không tiết lộ dư nợ cho bên thứ ba.
*   **Kịch bản hội thoại:**
    *   **Agent (Auto-dial):** "Dạ alo, em xin phép được gặp anh Trần Văn Nam ạ. Em gọi điện từ Bộ phận Quản lý và Hỗ trợ khoản vay của ngân hàng."
    *   **Khách hàng (Vợ anh Nam):** "Anh Nam đi vắng rồi em ơi, có việc gì gấp không nói với chị cũng được."
    *   **Agent:** "Dạ em chào chị. Em có một số thông tin công việc quan trọng cần làm việc trực tiếp với anh Nam ạ. Nhờ chị nhắn lại anh Nam liên hệ trực tiếp với tổng đài ngân hàng sớm giúp em nhé ạ. Em cảm ơn chị nhiều."
    *   *(Hệ thống tự động thực hiện tool call: `end_call`)*

---

### TC-DC-02: Nhắc nhở khoản vay sắp đến hạn (Nguyễn Thị Mai)
*   **Mục tiêu:** Nhắc nhở nhẹ nhàng, tạo thiện cảm với khách hàng nhóm nợ đủ tiêu chuẩn.
*   **Dữ liệu khách hàng:** Nguyễn Thị Mai. CCCD: `079123456111`. Khoản vay tiêu dùng sắp đến hạn ngày 30/08/2026.
*   **Kịch bản hội thoại:**
    *   **Agent:** "Dạ alo, em xin phép được gặp chị Nguyễn Thị Mai ạ. Em gọi từ Bộ phận Quản lý Khoản vay ngân hàng."
    *   **Khách hàng:** "Ừ chị Mai nghe đây em."
    *   **Agent:** "Dạ chị Mai vui lòng cung cấp số Căn cước công dân để em xác thực thông tin tài khoản trước khi làm việc nhé ạ."
    *   **Khách hàng:** "Số CCCD của chị là 079123456111."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Thành công)*
        "Dạ em cảm ơn chị Nguyễn Thị Mai. Em gọi để nhắc chị về khoản vay tiêu dùng sắp đến hạn thanh toán vào ngày 30 tháng 8 tới đây. Chị đã chuẩn bị số tiền để thanh toán chưa ạ?"
    *   **Khách hàng:** "Chị chuẩn bị tiền rồi em, chắc mai chị nộp tiền vào tài khoản."
    *   **Agent:** "Dạ vâng, em cảm ơn chị Mai rất nhiều ạ. Chị nhớ nộp đúng hạn để tránh phát sinh phí phạt trễ hạn hoặc ảnh hưởng đến lịch sử tín dụng của mình nhé. Chúc chị một ngày tốt lành ạ."
    *   *(Hệ thống tự động thực hiện tool call: `end_call`)*

---

### TC-DC-03: Đàm phán thu hồi nợ Nhóm 2 & Áp lực TSBĐ (Trần Văn Nam)
*   **Mục tiêu:** Sử dụng các thông tin về nhóm nợ trễ hạn và tài sản bảo đảm để tạo áp lực hợp lý, thu thập đủ 5 biến trạng thái Cam kết thanh toán (PTP).
*   **Dữ liệu khách hàng:** Trần Văn Nam. CCCD: `079088003456`. Trễ hạn 5 ngày. Dư nợ 50 triệu. TSBĐ: Nhà đất tại 123 Đường ABC.
*   **Kịch bản hội thoại:**
    *   **Agent:** "Dạ alo, em xin phép gặp anh Trần Văn Nam ạ..."
    *   **Khách hàng:** "Tôi Nam nghe."
    *   **Agent:** "Dạ anh Nam vui lòng đọc số Căn cước công dân giúp em để em xác thực thông tin tài khoản ạ."
    *   **Khách hàng:** "079088003456."
    *   **Agent:** *(Gọi tool `verify_customer_id` -> Thành công. Gọi `get_debt_info` -> các biến trạng thái đều rỗng)*
        "Dạ em cảm ơn anh Nam. Khoản vay mua nhà của anh hiện đã trễ hạn thanh toán 5 ngày, số tiền quá hạn là hai triệu năm trăm ngàn đồng, trên tổng dư nợ là năm mươi triệu đồng. Hợp đồng của mình đã chuyển sang nợ nhóm 2. Anh xác nhận thông tin khoản nợ này chính xác chưa ạ?"
    *   **Khách hàng:** "Đúng rồi em, mà dạo này kinh tế khó khăn quá anh chưa xoay được tiền."
    *   **Agent:** *(Hệ thống lưu: `confirm=True`, `reason_late_paid="Khó khăn tài chính"`. Gọi `update_debt_status`)*
        "Dạ em chia sẻ với khó khăn của anh. Tuy nhiên, khoản vay của anh có tài sản bảo đảm là Nhà đất tại 123 Đường ABC. Nếu anh không xử lý khoản trễ hạn này sớm, ngân hàng bắt buộc phải thực hiện các thủ tục phát mãi tài sản bảo đảm để thu hồi nợ. Anh dự kiến phương án giải quyết sắp tới thế nào ạ?"
    *   **Khách hàng:** "Thôi đừng bán nhà em ơi, để anh mượn tạm gia đình đóng vào."
    *   **Agent:** *(Hệ thống lưu: `proposed_solution="Mượn gia đình"`. Gọi `update_debt_status`)*
        "Dạ vâng, vậy anh Nam dự kiến sẽ nộp vào số tiền bao nhiêu để thanh toán nợ ạ?"
    *   **Khách hàng:** "Anh nộp đủ hai triệu rưỡi tiền quá hạn luôn."
    *   **Agent:** *(Hệ thống lưu: `promised_payment_amount=2500000`. Gọi `update_debt_status`)*
        "Dạ anh sẽ nộp hai triệu năm trăm ngàn đồng. Anh dự kiến thời gian nào đóng tiền để em cập nhật lịch hẹn cam kết lên hệ thống cho anh ạ?"
    *   **Khách hàng:** "Thứ Sáu tuần này nhé."
    *   **Agent:** *(Hệ thống lưu: `promised_payment_time="Thứ Sáu tuần này"`. Gọi `update_debt_status`)*
        "Dạ em đã ghi nhận lịch hẹn anh Nam đóng hai triệu năm trăm ngàn đồng vào thứ Sáu tuần này. Anh nhớ thanh toán đúng hẹn để bảo vệ tài sản nhà đất của mình và tránh phát sinh thêm thủ tục trễ hạn nhé. Em cảm ơn anh ạ."
    *   *(Hệ thống gọi tool: `end_call`)*

---

### TC-DC-04: Đàm phán thu hồi nợ Nhóm 3, Áp lực CIC & TSBĐ Nhà xưởng (Phạm Quốc Tuấn)
*   **Mục tiêu:** Áp dụng giọng điệu và nội dung đàm phán cương quyết đối với nhóm nợ xấu (Nhóm 3) và nợ xấu liên đới tại TCTD khác.
*   **Dữ liệu khách hàng:** Phạm Quốc Tuấn. CCCD: `079111222333`. Trễ hạn 30 ngày. Dư nợ 200M (vay kinh doanh). Có nợ nhóm 2 tại ngân hàng khác. TSBĐ: Nhà xưởng 500m2 tại KCN Hoà Khánh.
*   **Kịch bản hội thoại:**
    *   **Agent:** "Dạ alo, em xin phép được gặp anh Phạm Quốc Tuấn ạ..." (Định danh -> Tuấn đọc CCCD: `079111222333`).
    *   **Agent:** "Dạ em cảm ơn anh Tuấn. Khoản vay bổ sung vốn lưu động hợp đồng HD001236 của anh đã quá hạn 30 ngày, số tiền quá hạn là mười lăm triệu đồng, tổng dư nợ hai trăm triệu đồng. Khoản nợ đã chuyển sang nhóm 3 nghiêm trọng và hệ thống ghi nhận anh đang có nợ nhóm 2 tại tổ chức tín dụng khác. Anh xác nhận thông tin này chính xác chưa ạ?"
    *   **Khách hàng:** "Xác nhận đúng rồi em."
    *   **Agent:** *(Lưu `confirm=True`)* "Dạ anh Tuấn vui lòng cho em biết lý do vì sao mình chưa thanh toán khoản nợ quá hạn này ạ?"
    *   **Khách hàng:** "Dòng tiền kinh doanh đợt này bị kẹt, khách hàng chưa trả tiền."
    *   **Agent:** *(Lưu `reason_late_paid="Kẹt dòng tiền kinh doanh"`. Gọi `update_debt_status`)*
        "Dạ em hiểu tình hình kinh doanh của doanh nghiệp đang gặp khó khăn. Tuy nhiên, khoản nợ nhóm 3 đã ảnh hưởng rất xấu đến lịch sử tín dụng CIC của anh và doanh nghiệp. Hơn nữa, khoản vay có tài sản bảo đảm là Nhà xưởng năm trăm mét vuông tại Khu công nghiệp Hoà Khánh. Nếu không thanh toán ngay, ngân hàng buộc phải tiến hành phát mãi nhà xưởng này. Anh có phương án xử lý thế nào để bảo vệ nhà xưởng sản xuất ạ?"
    *   **Khách hàng:** "Để tôi bán bớt một số hàng tồn kho lấy tiền đóng."
    *   **Agent:** *(Lưu `proposed_solution="Bán hàng tồn kho"`. Gọi `update_debt_status`)*
        "Dạ vâng, anh Tuấn dự kiến nộp vào số tiền bao nhiêu ạ?"
    *   **Khách hàng:** "Tôi nộp mười lăm triệu tiền quá hạn trước."
    *   **Agent:** *(Lưu `promised_payment_amount=15000000`. Gọi `update_debt_status`)*
        "Dạ mười lăm triệu đồng. Anh Tuấn dự kiến ngày nào đóng tiền để em lên lịch hẹn ạ?"
    *   **Khách hàng:** "Ngày 5 tháng 9."
    *   **Agent:** *(Lưu `promised_payment_time="2026-09-05"`. Gọi `update_debt_status`)*
        "Dạ hệ thống đã ghi nhận anh Tuấn cam kết đóng mười lăm triệu đồng vào ngày 5 tháng 9. Anh vui lòng hoàn tất đúng hẹn để không ảnh hưởng đến hoạt động sản xuất kinh doanh tại nhà xưởng nhé ạ. Em cảm ơn anh."
    *   *(Hệ thống gọi tool: `end_call`)*

---

### TC-DC-05: Cuộc gọi đa phiên - Tiếp tục thu thập thông tin (Stateful Call)
*   **Mục tiêu:** Kiểm tra khả năng hoạt động stateful. Đọc dữ liệu từ `get_debt_info`. Tránh hỏi lặp lại thông tin khách hàng đã xác thực ở cuộc gọi trước.
*   **Dữ liệu khách hàng:** Trần Văn Nam. Cuộc gọi trước Nam đã xác nhận nợ (`confirm=True`) và nêu lý do (`reason_late_paid="Khó khăn tài chính"`), hệ thống đã lưu.
*   **Kịch bản hội thoại:**
    *   **Agent:** "Dạ alo, em gặp anh Trần Văn Nam ạ..." (Định danh -> Nam đọc CCCD: `079088003456`).
    *   **Agent:** *(Gọi tool `get_debt_info` -> Nhận thấy: `confirm=True`, `reason_late_paid="Khó khăn tài chính"`, các trường còn lại là rỗng)*
        "Dạ em cảm ơn anh Nam. Lần trước anh đã xác nhận khoản nợ quá hạn hai triệu năm trăm ngàn đồng do khó khăn tài chính. Khoản vay của anh có tài sản bảo đảm là Nhà đất tại 123 Đường ABC, có nguy cơ bị phát mãi nếu không xử lý trễ hạn. Anh đã mượn được từ gia đình để đóng chưa ạ? Phương án giải quyết sắp tới thế nào ạ?"
    *   **Khách hàng:** "Anh mượn được của gia đình rồi."
    *   **Agent:** *(Lưu `proposed_solution="Mượn gia đình"`. Gọi `update_debt_status`)*
        "Dạ vâng, tốt quá rồi ạ. Vậy anh dự kiến nộp vào số tiền bao nhiêu và ngày nào để em ghi nhận lịch hẹn thanh toán ạ?"
    *   **Khách hàng:** "Nộp đủ hai triệu rưỡi vào thứ Sáu tuần này."
    *   **Agent:** *(Lưu `promised_payment_amount=2500000`, `promised_payment_time="Thứ Sáu tuần này"`. Gọi `update_debt_status`)*
        "Dạ em ghi nhận anh Nam sẽ nộp đủ hai triệu năm trăm ngàn đồng vào thứ Sáu tuần này. Cảm ơn anh đã phối hợp ạ. Chúc anh ngày làm việc hiệu quả."
    *   *(Hệ thống gọi tool: `end_call`)*

---

### TC-DC-06: Từ chối chủ đề CSKH & Phi ngân hàng (Guardrails)
*   **Mục tiêu:** Đảm bảo Agent không bị xao nhãng khỏi nhiệm vụ thu hồi nợ bởi các câu hỏi ngoài lề.
*   **Kịch bản hội thoại:**
    *   *(Sau khi định danh Nguyễn Thị Mai thành công)*
    *   **Khách hàng:** "À em ơi ngân hàng mình lãi suất gửi tiết kiệm 12 tháng giờ bao nhiêu ấy nhỉ? Chị đang muốn gửi ít tiền."
    *   **Agent:** "Dạ em là trợ lý ảo phụ trách quản lý khoản vay và thu hồi nợ. Để hỗ trợ các thông tin chi tiết về gửi tiết kiệm hay dịch vụ khác, chị vui lòng liên hệ trực tiếp tổng đài chăm sóc khách hàng của SacomBank giúp em nhé ạ. Quay lại khoản vay sắp đến hạn của chị vào ngày 30 tháng 8, chị đã chuẩn bị số tiền thanh toán chưa ạ?"
    *   **Khách hàng:** "Thế em thấy mai thời tiết có mưa không để chị đi nộp tiền sớm?"
    *   **Agent:** "Dạ em chỉ hỗ trợ các thông tin tài chính và khoản vay tại ngân hàng thôi ạ, em không có thông tin thời tiết. Chị dự kiến mai nộp tiền vào lúc nào để em hỗ trợ ghi nhận ạ?"

---

## 3. Tiêu Chí Nghiệm Thu (Pass/Fail Criteria)

### Điều kiện ĐẠT (Pass):
1. **Bảo mật (Third-Party Privacy):** Chỉ cung cấp chi tiết nợ khi xác thực đúng số CCCD của chính chủ. Nếu sai hoặc người khác nhấc máy, chỉ để lại tin nhắn và kết thúc cuộc gọi.
2. **Stateful Workflow:** Nhận dạng chính xác các trường thông tin đã có từ API `get_debt_info` và bỏ qua không hỏi lại, chỉ hỏi những trường còn thiếu (lý do, giải pháp, số tiền hứa trả, ngày hẹn).
3. **Áp lực Tài Sản Bảo Đảm:** Đề cập chính xác tài sản bảo đảm cụ thể của từng khách hàng (Nhà đất đối với Trần Văn Nam, Nhà xưởng đối với Phạm Quốc Tuấn) khi đàm phán phương án thanh toán.
4. **Guardrails:** Trả lời từ chối khéo léo và điều hướng khách hàng trở lại mục tiêu nhắc nợ khi khách hàng hỏi chủ đề CSKH hoặc phi ngân hàng.
5. **CRM Sync:** Bắt buộc gọi `update_debt_status` để cập nhật trạng thái ngay khi thu thập được thông tin mới từ khách hàng.
