# Quy trình / Workflow Thu Hồi Nợ (ElevenLabs)

Workflow này được thiết kế theo cấu trúc Stateful Workflow của ElevenLabs nhằm theo dõi tiến trình thu hồi nợ qua nhiều cuộc gọi.

## 1. Tổng quan các State Variables (Ngữ cảnh cuộc gọi)

Các biến trạng thái sau sẽ được lưu trữ qua các phiên làm việc để Agent biết nên bắt đầu từ đâu, tránh hỏi lại từ đầu nếu cuộc gọi trước bị gián đoạn:
- `confirm` (Boolean): Khách hàng đã xác nhận khoản nợ.
- `reason_late_paid` (String): Lý do quá hạn.
- `proposed_solution` (String): Phương án xử lý (hoặc phản hồi việc phát mãi tài sản bảo đảm - TSBĐ).
- `promised_payment_amount` (Numeric): Số tiền hứa trả.
- `promised_payment_time` (Date/Time): Thời gian hứa trả.

## 2. Thiết kế ElevenLabs Workflow Nodes

Sử dụng tính năng **Agent Workflows** của ElevenLabs, cấu trúc các node như sau:

### Node 1: Start & Greeting (Bắt đầu và Định danh)
- **Hành động:** Agent tự động gọi ra. Chào tên khách hàng và yêu cầu cung cấp số CCCD.
- **Phân nhánh (Edges):**
  - Nhập đúng CCCD -> Chuyển sang **Node 2**
  - Nhập sai CCCD hoặc không phải chính chủ -> Chuyển sang **Node 6 (Kết thúc - Lời nhắn)**

### Node 2: Check Confirmation (Xác nhận nợ)
- **Hành động:** Kiểm tra biến `confirm`. 
  - Nếu chưa có: Đọc chi tiết dư nợ và yêu cầu xác nhận. Khi xác nhận, gọi tool `update_debt_status` (lưu confirm = true).
  - Nếu đã có: Tóm tắt lại khoản nợ khách đã xác nhận lần trước.
- **Phân nhánh (Edges):** Unconditional -> Chuyển sang **Node 3**

### Node 3: Collect Debt Info (Kích hoạt Procedure)
- **Hành động:** Gọi system tool `start_procedure` để chạy **Procedure Thu thập thông tin PTP**. 
  - Procedure này sẽ hoạt động như một "bảng tích" (checklist). Nó sẽ kiểm tra các biến trạng thái (`reason_late_paid`, `proposed_solution`, `promised_payment_amount`, `promised_payment_time`). Nếu biến nào chưa có dữ liệu, Agent sẽ hỏi để thu thập. Nếu đã có, Agent sẽ tự động bỏ qua để tránh hỏi lặp lại.
  - Sau khi Procedure hoàn tất (chốt được cam kết), luồng sẽ tự động chuyển tiếp.
- **Phân nhánh (Edges):** Unconditional -> Chuyển sang **Node 4**

### Node 4 & 5: End Nodes
- **Node 4 (Kết thúc thất bại/Sai người):** Để lại lời nhắn cho chính chủ gọi lại và gọi system tool `end_call`.
- **Node 5 (Kết thúc thành công):** Cảm ơn, dặn dò nộp đúng hạn, ghi nhận lên CRM và gọi system tool `end_call`.
