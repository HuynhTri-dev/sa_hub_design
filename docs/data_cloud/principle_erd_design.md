# ERD Design Principles — Nguyên tắc Thiết kế Dữ liệu Cốt lõi

> 💡 **Mục đích:** Tài liệu này tổng hợp 24 nguyên tắc "xương máu" khi thiết kế ERD (Entity-Relationship Diagram). Thay vì chỉ liệt kê lý thuyết, mỗi nguyên tắc sẽ đi kèm với ví dụ Thực tế (Before/After) để bạn dễ dàng áp dụng vào dự án thực.

---

## 📌 Nhóm 1: Khởi tạo ý tưởng và Nhận diện Thực thể

### Nguyên tắc 1: Bắt đầu từ nghiệp vụ, không bắt đầu từ database
Khi nhận yêu cầu, đừng nghĩ ngay đến bảng (table). Hãy nghĩ đến các **Thực thể (Entity)** trong thế giới thực.
- ❌ **Sai:** Suy nghĩ tạo `customer_tbl`, `order_tbl`, `product_tbl`.
- ✅ **Đúng:** Hỏi "Hệ thống này quản lý những đối tượng nào?" -> Khách hàng, Đơn hàng, Sản phẩm. Model business trước, model database sau.

### Nguyên tắc 2: Nhận diện Entity bằng Identity và Lifecycle
Một đối tượng nên trở thành Entity khi nó có:
1. Identifier (Khóa định danh riêng)
2. Lifecycle (Vòng đời: Được tạo ra, thay đổi, xóa đi)
3. Thuộc tính (Attribute) riêng.

> **Ví dụ:** `Customer` là Entity vì có ID riêng, được tạo tài khoản, bị khóa tài khoản. Nhưng `Customer.name` chỉ là một thuộc tính vì nó không thể tự tồn tại nếu không có Customer.

### Nguyên tắc 3: Mỗi Entity phải có một Primary Key (PK) mạnh
- Ưu tiên dùng **Surrogate Key** (Khóa nhân tạo như UUID, Auto-increment ID).
- Tránh dùng **Natural Key** (Khóa tự nhiên như Email, Số CMND) làm PK vì business rule có thể thay đổi (khách hàng muốn đổi email).
- Khóa tự nhiên nên được set là `UNIQUE` constraint, không phải PK.

```sql
-- ❌ THIẾT KẾ SAI (Dùng Natural Key làm PK)
CREATE TABLE Customer (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);

-- ✅ THIẾT KẾ ĐÚNG (Dùng Surrogate Key làm PK)
CREATE TABLE Customer (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255)
);
```

---

## 🔗 Nhóm 2: Xác định Mối quan hệ (Relationship)

### Nguyên tắc 4: Đọc mối quan hệ thành "Câu hoàn chỉnh"
Đừng chỉ vẽ một đường nối giữa 2 Entity. Hãy đọc nó thành câu theo cả 2 chiều:
- *"Một Khách hàng có thể có nhiều Đơn hàng."*
- *"Một Đơn hàng bắt buộc phải thuộc về đúng một Khách hàng."*
Điều này giúp bạn xác định rõ ràng Cardinality (1:N) và Optionality (Bắt buộc/Không bắt buộc).

### Nguyên tắc 5: Xử lý triệt để quan hệ N:N (Many-to-Many)
Trong cơ sở dữ liệu quan hệ, bạn không thể code trực tiếp quan hệ N:N. Bắt buộc phải sinh ra một **Associative Entity (Bảng trung gian)**.

```mermaid
erDiagram
    %% ❌ SAI: Trực tiếp nối N:N
    %% STUDENT }o--o{ COURSE : enrolls

    %% ✅ ĐÚNG: Dùng bảng trung gian
    STUDENT ||--o{ ENROLLMENT : has
    COURSE ||--o{ ENROLLMENT : includes
    
    ENROLLMENT {
        uuid student_id FK
        uuid course_id FK
        date enrolled_at
        float grade
    }
```
**Luật vàng:** Nếu một mối quan hệ tự nó mang theo thuộc tính (như `enrolled_at`, `grade`), bản thân mối quan hệ đó chính là một Entity.

### Nguyên tắc 6: Foreign Key (FK) luôn nằm ở phe "Nhiều" (Many)
Trong quan hệ 1:N (Một Khách hàng - Nhiều Đơn hàng), FK luôn phải đặt ở bảng Đơn hàng.
- ❌ **Sai:** Bảng `Customer` chứa cột `order_ids` (mảng/chuỗi ID).
- ✅ **Đúng:** Bảng `Order` chứa cột `customer_id`.

---

## 🧹 Nhóm 3: Chuẩn hóa Dữ liệu (Normalization)

Chuẩn hóa giúp loại bỏ sự dư thừa dữ liệu (redundancy) và đảm bảo tính nhất quán.

### Nguyên tắc 7: 1NF - Thuộc tính phải Nguyên tử (Atomic)
Không một ô (cell) nào được chứa nhiều hơn 1 giá trị.
- ❌ **Sai:** Cột `phone_numbers` chứa `"0901, 0902, 0903"`.
- ✅ **Đúng:** Tách ra bảng `CustomerPhone` chứa từng số điện thoại trên một dòng riêng biệt.

### Nguyên tắc 8: 2NF - Xóa bỏ Phụ thuộc một phần (Partial Dependency)
(Chỉ áp dụng khi dùng Composite Primary Key - Khóa chính kép).
- ❌ **Sai:** Bảng `OrderItem(order_id, product_id, product_name)`. Ở đây `product_name` chỉ phụ thuộc vào `product_id`, không phụ thuộc vào `order_id`. Nếu đổi tên sản phẩm, bạn phải đi update hàng triệu dòng OrderItem.
- ✅ **Đúng:** Tách `product_name` về bảng `Product`.

### Nguyên tắc 9: 3NF - Xóa bỏ Phụ thuộc bắc cầu (Transitive Dependency)
- ❌ **Sai:** `Employee(id, name, department_id, department_name)`. Ở đây `id -> department_id -> department_name`. 
- ✅ **Đúng:** Tách thành 2 bảng `Employee` và `Department`.

### Nguyên tắc 10: Đừng chuẩn hóa thái quá (Over-normalization)
Nếu một thuộc tính chỉ đơn thuần là text/mô tả và không bao giờ được dùng để query/group by, đừng tách nó ra thành bảng riêng.
- ❌ **Sai (Thái quá):** `Product` có thuộc tính `Color`, tách ra bảng `ColorTable`, bảng `ColorTranslation`, bảng `ColorGroup`.
- ✅ **Đúng:** Giữ nguyên cột `color VARCHAR(50)` trong bảng `Product` nếu hệ thống không có nhu cầu quản lý màu sắc phức tạp.

---

## 🛡️ Nhóm 4: Bào vệ Toàn vẹn Dữ liệu (Integrity)

### Nguyên tắc 11: Chuyển hóa Business Rule thành Database Constraint
Đừng chỉ trông cậy vào Code Backend để validate dữ liệu. Hãy dùng Constraint của Database làm chốt chặn cuối cùng.
- Quy tắc: "Mỗi User chỉ có 1 Profile" -> Dùng `UNIQUE(user_id)` trong bảng Profile.
- Quy tắc: "Số lượng mua phải lớn hơn 0" -> Dùng `CHECK (quantity > 0)`.
- Quy tắc: "Đơn hàng phải có Khách hàng" -> Dùng `NOT NULL` cho `customer_id`.

### Nguyên tắc 12: Xác định rõ Cascade Behavior (Hành vi xóa)
Hỏi: *"Nếu tôi xóa Entity A, Entity B có còn ý nghĩa tồn tại không?"*
- Nếu KHÔNG (ví dụ: Xóa Order thì OrderItem vô nghĩa): Dùng `ON DELETE CASCADE`.
- Nếu CÓ (ví dụ: Xóa Customer, nhưng Order cũ vẫn phải giữ lại để kế toán kiểm tra): Dùng `ON DELETE RESTRICT` hoặc `SET NULL`.

---

## ⏳ Nhóm 5: Dữ liệu Lịch sử (Temporal Data)

### Nguyên tắc 13: Trạng thái Hiện tại vs Lịch sử
Nếu hệ thống chỉ có `status = SHIPPED` trong bảng `Order`, bạn chỉ biết hiện tại, nhưng bị mù về quá khứ.
Nếu business cần theo dõi (Audit/Tracking):
> "Đơn hàng này được Confirm lúc nào? Ai là người Pack hàng?"
-> Bạn bắt buộc phải tạo bảng Lịch sử: `OrderStatusHistory(order_id, status, changed_at, changed_by)`.

### Nguyên tắc 14: Giá trị thay đổi theo thời gian
Thuộc tính cực kỳ nhạy cảm: **Giá tiền (Price)**.
- ❌ **Sai:** Lưu `price` ở bảng `Product`. Khi khách mua hàng, lưu mã sản phẩm ở `OrderItem`. Vài tháng sau `Product` tăng giá -> Lịch sử hóa đơn của khách tự động bị đội giá lên (LỖI NGHIÊM TRỌNG).
- ✅ **Đúng:** Trong bảng `OrderItem`, bắt buộc phải copy giá tại thời điểm mua: `unit_price_at_order_time`. Đây KHÔNG PHẢI là duplicate data, đây là Snapshot dữ liệu.

---

## ✅ Checklist Kiểm tra nhanh ERD (Trước khi code)

Dùng 5 câu hỏi sinh tử này để review ERD của bạn:
1. Mọi bảng đã có Khóa chính (PK) là Surrogate Key chưa?
2. Có bảng nào đang chứa chuỗi "ngăn cách bởi dấu phẩy" không? (Vi phạm 1NF).
3. Có cột nào có thể được tính toán (Derived) từ các cột khác mà vẫn bị lưu cứng xuống DB không? (VD: cột `total_amount` trong khi đã có các dòng `OrderItem`).
4. Quan hệ N:N đã được hóa giải bằng bảng trung gian chưa?
5. Ràng buộc `ON DELETE` đã được review cẩn thận chưa, hay đang để mặc định?
