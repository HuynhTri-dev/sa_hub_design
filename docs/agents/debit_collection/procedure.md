# Procedure: Thu Thập & Thỏa Thuận Thanh Toán (Promise To Pay)

Procedure này được thiết kế theo dạng **Deterministic** (Các bước thực hiện tuần tự). Nhiệm vụ của nó là hoạt động như một "bảng kiểm" (checklist) để thu thập thông tin còn thiếu từ khách hàng dựa trên các `state variables`.

## 1. Cấu hình chung

- **Tên Procedure:** `collect_ptp_info`
- **Loại:** `deterministic`
- **Trigger:** "Khách hàng đã xác nhận đúng thông tin khoản nợ và đồng ý trao đổi tiếp."

## 2. Kịch bản đánh giá "Bảng tích" (Condition Logic)

Nhờ việc dữ liệu trạng thái đã được kéo về (thông qua webhook `get_debt_info`), Agent sẽ biết trường nào bị trống (`null`). Tại mỗi bước, Agent ngầm kiểm tra:
- **Nếu đã có dữ liệu:** Bỏ qua không hỏi (hoặc chỉ xác nhận lại một câu ngắn gọn nếu cần thiết).
- **Nếu chưa có dữ liệu:** Đặt câu hỏi theo kịch bản để thu thập và lưu vào biến.

## 3. Các bước (Steps) của Procedure

### Step 1: Hỏi lý do quá hạn (`reason_late_paid`)
- **Điều kiện:** `if (state.reason_late_paid == null)`
- **Hành động (Action):** `question`
- **Kịch bản (Prompt):** "Dạ anh/chị cho em hỏi hiện tại mình đang gặp khó khăn gì mà chưa thể thanh toán khoản nợ này đúng hạn ạ?"
- **Expected Variable:** `reason` (Lưu ý: Agent lắng nghe và trích xuất lý do thành text ngắn gọn).

### Step 2: Thỏa thuận phương án xử lý (`proposed_solution`)
- **Điều kiện:** `if (state.proposed_solution == null)`
- **Hành động (Action):** `question`
- **Kịch bản (Prompt):** 
  - Đàm phán phương án thanh toán. 
  - *Context-aware:* Nếu khoản nợ thuộc nhóm nguy hiểm và có Tài sản bảo đảm (TSBĐ), Agent sẽ sử dụng thông tin TSBĐ để cảnh báo rủi ro phát mãi/bán tài sản nếu khách hàng không hợp tác đưa ra phương án. "Dạ khoản vay của mình đang được đảm bảo bằng {collateral}, nếu không thanh toán, ngân hàng sẽ buộc phải phát mãi tài sản này. Vậy anh/chị dự định phương án giải quyết sắp tới như thế nào ạ?"
- **Expected Variable:** `solution`

### Step 3: Chốt số tiền cam kết (`promised_payment_amount`)
- **Điều kiện:** `if (state.promised_payment_amount == null)`
- **Hành động (Action):** `question`
- **Kịch bản (Prompt):** "Dạ vậy anh/chị có thể nộp vào số tiền bao nhiêu để em ghi nhận lên hệ thống ạ?"
- **Expected Variable:** `promise_amount`

### Step 4: Chốt thời gian cam kết (`promised_payment_time`)
- **Điều kiện:** `if (state.promised_payment_time == null)`
- **Hành động (Action):** `question`
- **Kịch bản (Prompt):** "Dạ anh/chị dự kiến sẽ nộp số tiền này vào thời gian nào (ngày nào) để em tạo lịch hẹn ạ?"
- **Expected Variable:** `promise_date`

### Step 5: Cập nhật hệ thống (Webhook Tool)
- **Hành động (Action):** `tool_call`
- **Tool ID:** `update_debt_status`
- **Logic:** Gọi webhook để đẩy tất cả các biến đã thu thập (`reason`, `solution`, `promise_amount`, `promise_date`) về hệ thống CRM của Sacombank. Sau khi gọi thành công, Procedure kết thúc, trả quyền điều khiển về Workflow chính (để chuyển sang Node kết thúc).
