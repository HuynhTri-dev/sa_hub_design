# Thiết Kế CSDL Masterclass — Tips & Triết lý Nâng cao

> 💡 **Mục đích:** Tài liệu này dành cho những ai đã nắm vững lý thuyết ERD cơ bản và muốn tiến tới Tư duy Thiết kế Hệ thống (System Design). Nó tập trung giải quyết các cuộc tranh luận kinh điển: SQL vs NoSQL, Chuẩn hóa vs Phản chuẩn hóa, và Khái niệm "Source of Truth".

---

## 🚀 1. Nghệ thuật nhận diện Thực thể (Entity)

Đừng dùng mẹo "Tìm Danh từ trong yêu cầu" vì nó rất dễ sai. (Ví dụ: `Email` là danh từ nhưng thường chỉ là một cột). Hãy dùng 2 công cụ mạnh mẽ sau:

### Công cụ 1: Bộ lọc 6 câu hỏi
Với bất kỳ khái niệm nào đang nghi ngờ, hãy hỏi:
1. Nó có một mã định danh (ID) độc lập không?
2. Nó có vòng đời riêng (Tạo ra -> Thay đổi -> Kết thúc) không?
3. Nó có mang nhiều thuộc tính đi kèm không?
4. Nó có tham gia vào mối quan hệ với đối tượng khác không?
5. Hệ thống có bao giờ cần truy vấn trực tiếp nó không (Ví dụ: "Lấy cho tôi tất cả các Địa chỉ")?
6. Nếu xóa đối tượng cha của nó, nó còn ý nghĩa tồn tại không?

Càng nhiều câu trả lời **CÓ**, đối tượng đó càng chắc chắn là một Entity.

### Công cụ 2: Bài test Động từ (Verb test)
Hệ thống làm gì với nó?
- *Admin đổi TÊN khách hàng* -> Tên là thuộc tính.
- *Admin CẤP QUYỀN, KHÓA, GIA HẠN Tài khoản* -> Tài khoản là một Entity riêng biệt với Khách hàng.

---

## ⚖️ 2. Đừng tôn thờ Chuẩn hóa (Normalization) một cách mù quáng

Trong môi trường học thuật, 3NF luôn là đích đến. Nhưng trong Production: **Chuẩn hóa là một sự Đánh đổi (Trade-off).**

### Khi nào nên Chuẩn hóa chặt chẽ (3NF+)?
- Hệ thống **OLTP (Online Transaction Processing)**: Hệ thống giao dịch cần ghi (Write) rất nhiều và đòi hỏi tính toàn vẹn tuyệt đối (Kế toán, Ngân hàng, Kho).
- Ưu tiên lớn nhất ở đây là: Không bao giờ bị sai lệch dữ liệu khi Update/Delete.

### Khi nào nên Phản chuẩn hóa (Denormalization)?
- Hệ thống **OLAP (Online Analytical Processing)** hoặc Read-heavy (Hệ thống đọc nhiều hơn ghi gấp 100 lần, ví dụ mạng xã hội, dashboard report).
- Thay vì bắt hệ thống phải JOIN 5 bảng với nhau hàng triệu lần mỗi giây, chúng ta **Cố tình** duplicate dữ liệu.
- Lưu ý sinh tử: Phản chuẩn hóa chỉ an toàn khi bạn kiểm soát được **Source of Truth (Nguồn Sự thật)**.

---

## 🌟 3. Nguyên lý tối thượng: "Source of Truth" & Snapshots

Sự khác biệt giữa một Senior và một Junior khi Duplicate dữ liệu nằm ở việc xác định được Source of Truth.

Hãy xem xét 2 ví dụ Duplicate dữ liệu sau:

**Ví dụ A (Thiết kế Tồi):**
- Bảng `Employee` lưu `department_name`.
- Bảng `Department` cũng lưu `department_name`.
- *Tại sao tồi?* Vì nếu phòng ban đổi tên từ "IT" sang "Engineering", bạn phải đi tìm và update hàng nghìn nhân viên. Ở đây, cả 2 bảng đang cố gắng làm Source of Truth cho cùng 1 thông tin.

**Ví dụ B (Thiết kế Xuất sắc):**
- Bảng `Customer` lưu `name = "Nguyễn Văn A"`. (Đây là **Source of Truth** - có thể thay đổi).
- Bảng `Order` lưu `customer_name_at_checkout = "Nguyễn Văn A"`. (Đây là **Snapshot**).
- *Tại sao xuất sắc?* Vì 5 năm sau, khách hàng có thể đổi tên thành "Nguyễn Văn B", nhưng Hóa đơn đỏ xuất ra cách đây 5 năm bắt buộc phải giữ nguyên tên cũ.

> **Triết lý:** Duplicate dữ liệu là thảm họa nếu bạn không biết ai là Source of Truth. Ngược lại, nó là một Pattern kinh điển (Snapshot Pattern) nếu được dùng có chủ đích.

---

## 🗂️ 4. Cuộc chiến SQL vs NoSQL (Relational vs Document)

Đừng chọn MongoDB chỉ vì "nó dễ dùng và không cần khai báo schema". Hãy chọn dựa trên **Access Pattern (Mô hình truy cập dữ liệu)**.

### SQL (PostgreSQL, MySQL) hỏi:
> "Mối quan hệ giữa các dữ liệu là gì?"
Mọi thứ được tách thành các bảng nhỏ gọn, tránh lặp lại. Khi cần, ta dùng lệnh `JOIN` để gom chúng lại.

### NoSQL (MongoDB, DynamoDB) hỏi câu thứ hai quan trọng hơn:
> "Application ĐỌC dữ liệu này cùng nhau hay riêng lẻ?"

**Nguyên tắc "Đọc cùng nhau -> Nằm cùng nhau" (Data that is read together, is stored together):**

Nếu mỗi lần mở một Đơn hàng (`Order`), ứng dụng LUÔN LUÔN phải hiển thị danh sách các món hàng (`OrderItems`), thì tại sao phải tách ra 2 bảng rồi tốn công JOIN?
Trong MongoDB, ta thiết kế **Embed (Nhúng)**:
```json
{
  "_id": "ORDER_123",
  "customer_id": "CUST_999",
  "total": 500,
  "items": [
    { "product_id": "P1", "quantity": 2 },
    { "product_id": "P2", "quantity": 1 }
  ]
}
```
*Chỉ 1 thao tác đọc đĩa (1 I/O operation), bạn lấy được toàn bộ thông tin.*

**Nguyên tắc "Cập nhật độc lập -> Tách ra" (Reference):**
Nhưng đừng nhúng mọi thứ. Trong ví dụ trên, chúng ta **Không nhúng** chi tiết Khách hàng (Customer) vào thẳng trong mảng items. Vì thông tin Khách hàng được dùng chung bởi hàng trăm Đơn hàng khác. Nếu khách hàng đổi địa chỉ, ta không thể đi cập nhật hàng trăm Document được. Do đó, ta chỉ lưu `customer_id` (Reference).

---

## 🧠 5. Workflow Tư duy 3 Tầng (3-Layer Mental Model)

Khi thiết kế bất kỳ hệ thống dữ liệu nào, hãy rèn luyện việc tách não bạn ra làm 3 tầng:

1. **Tầng Business (Nghiệp vụ):** Khách hàng đặt mua một Sản phẩm. (Chỉ tập trung vào quy trình thực tế).
2. **Tầng Logical (Logic ERD):** Khách hàng (1) --- (N) Đơn Hàng (1) --- (N) Chi tiết Đơn hàng (N) --- (1) Sản phẩm. Ở tầng này, ta áp dụng các chuẩn 1NF, 2NF, 3NF để đảm bảo tính đúng đắn.
3. **Tầng Physical (Vật lý):** Quyết định chọn PostgreSQL (dùng JOIN) hay Redis (dùng Key-Value) hay MongoDB (dùng Embedded Document) để **tối ưu hóa tốc độ**.

> Một ERD đạt chuẩn 3NF ở tầng Logical, nhưng lại được triển khai dưới dạng JSON lồng nhau ở tầng Physical của MongoDB là một thiết kế **hoàn toàn hợp lý và không hề mâu thuẫn.**
