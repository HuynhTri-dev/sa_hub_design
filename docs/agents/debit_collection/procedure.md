# Procedure: Thu Thập & Thỏa Thuận Thanh Toán (Promise To Pay)

Procedure này được thiết kế theo dạng **Free Form** (Kịch bản mở dựa trên Checklist). Nhiệm vụ của nó là hoạt động như một "bảng kiểm" để thu thập thông tin còn thiếu từ khách hàng.

## 1. Cấu hình chung

- **Tên Procedure:** `Thu Thập Thông Tin PTP (Bảng Tích)`
- **Loại:** `free_form`
- **Trigger:** "Khách hàng đã xác nhận đúng thông tin khoản nợ và đồng ý trao đổi tiếp."

## 2. Kịch bản (Prompt)

```markdown
Bạn có nhiệm vụ thu thập thông tin Cam kết thanh toán (PTP) từ khách hàng. Hãy hoạt động như một "bảng kiểm" (checklist) để thu thập thông tin còn thiếu.

BƯỚC 1: KHỞI TẠO THÔNG TIN
- Ngay khi bắt đầu, BẮT BUỘC gọi tool `get_debt_info` để lấy thông tin khoản nợ và các biến trạng thái (dynamic variables) hiện có của khách hàng.
- Đọc và set các biến: `confirm`, `reason_late_paid`, `proposed_solution`, `promised_payment_amount`, `promised_payment_time` từ kết quả trả về của tool.

BƯỚC 2: THU THẬP THÔNG TIN (BẢNG TÍCH)
LUÔN kiểm tra các biến vừa nhận được. NẾU DỮ LIỆU ĐÃ CÓ (khác rỗng hoặc null), KHÔNG ĐƯỢC HỎI LẠI. CHỈ HỎI NHỮNG GÌ CÒN THIẾU (dữ liệu rỗng hoặc null).

1. **Lý do quá hạn (reason):**
   - Nếu `reason_late_paid` rỗng hoặc null: Hỏi "Dạ anh/chị cho em hỏi hiện tại mình đang gặp khó khăn gì mà chưa thể thanh toán khoản nợ này đúng hạn ạ?"
2. **Phương án xử lý (solution):**
   - Nếu `proposed_solution` rỗng hoặc null: Đàm phán phương án. Nhấn mạnh: "Nếu không thanh toán, ngân hàng sẽ buộc phải phát mãi tài sản bảo đảm. Vậy anh/chị dự định phương án giải quyết sắp tới như thế nào ạ?"
3. **Số tiền cam kết nộp (promise_amount):**
   - Nếu `promised_payment_amount` rỗng hoặc null: Hỏi "Dạ vậy anh/chị có thể nộp vào số tiền bao nhiêu để em ghi nhận lên hệ thống ạ?"
4. **Ngày giờ cam kết nộp (promise_date):**
   - Nếu `promised_payment_time` rỗng hoặc null: Hỏi "Dạ anh/chị dự kiến sẽ nộp số tiền này vào thời gian nào (ngày nào) để em tạo lịch hẹn ạ?"

BƯỚC 3: KẾT THÚC
- Sau khi đã thu thập ĐỦ 4 thông tin trên (hoặc nếu tất cả đều đã có sẵn), BẮT BUỘC gọi tool `update_debt_status` để đẩy các dữ liệu vừa lấy được về hệ thống.
- Cuối cùng, cảm ơn và dặn dò khách hàng thanh toán đúng hạn.
```
