# 11. Quyền Riêng Tư Dữ Liệu và Tuân Thủ (Data Privacy & Compliance)

*(Cấp độ Enterprise/Chính phủ: Đảm bảo chủ quyền dữ liệu và tuân thủ các khung pháp lý nghiêm ngặt)*

## 11.1 Phân loại dữ liệu (Data Classification)
Nền tảng cho mọi chính sách bảo mật dữ liệu — không thể bảo vệ dữ liệu nếu không biết dữ liệu nào quan trọng đến đâu:

| Mức | Ví dụ | Yêu cầu xử lý |
|---|---|---|
| Public | Nội dung marketing | Không cần kiểm soát đặc biệt |
| Internal | Tài liệu nội bộ | Giới hạn trong tổ chức |
| Confidential | Hợp đồng, lương | Mã hóa, giới hạn truy cập theo vai trò |
| Restricted/PII | CMND, sức khỏe, thẻ thanh toán | Mã hóa bắt buộc, log truy cập, giới hạn tối đa |

## 11.2 Xử lý PII (Personally Identifiable Information)
- Áp dụng nguyên tắc **Data Minimization**: chỉ thu thập dữ liệu thực sự cần thiết cho mục đích đã khai báo.
- **Pseudonymization** (giả danh hóa) vs **Anonymization** (ẩn danh hóa hoàn toàn): pseudonymization vẫn có thể truy ngược (dùng cho phân tích nội bộ có kiểm soát), anonymization thì không thể truy ngược được nữa (dùng khi chia sẻ dữ liệu ra ngoài, ví dụ cho nghiên cứu).

## 11.3 Data Masking/Redaction — góc độ code
Code phải "hiểu" mức độ nhạy cảm của field và tự động che dữ liệu dựa trên clearance level của người gọi API:
- **Static masking**: che dữ liệu trong môi trường non-production (dev/staging dùng bản dữ liệu đã mask thay vì copy nguyên dữ liệu thật từ production).
- **Dynamic masking**: che tại thời điểm trả response — ví dụ trả về `***-***-1234` cho số điện thoại nếu user gọi API không có quyền xem đầy đủ.
- Triển khai thực tế: đặt logic masking ở tầng serialization/response layer (DTO/Presenter), không rải rác trong business logic — dễ audit và tránh sót field khi thêm field mới vào model.

## 11.4 Data Retention & Data Residency/Localization
- **Data Retention**: định nghĩa rõ thời gian lưu từng loại dữ liệu, có job tự động xóa/anonymize khi hết hạn (đã nêu ở phần Privacy Operations trước, nhắc lại vì đây là yêu cầu bắt buộc theo luật ở hầu hết các domain compliance).
- **Data Residency (góc độ kiến trúc)**: với hệ thống multi-region, dữ liệu công dân của quốc gia nào phải được lưu và xử lý tại server/region hợp pháp của quốc gia đó (ví dụ: dữ liệu công dân EU phải ở trong khu vực EU theo GDPR; Việt Nam có yêu cầu tương tự với một số loại dữ liệu theo NĐ 13/2023).
  - Kiến trúc microservices cần có **routing layer** nhận diện region của user/dữ liệu và điều hướng traffic/storage về đúng cụm hạ tầng hợp pháp, tránh trường hợp dữ liệu vô tình được replicate sang region sai.

## 11.5 Chuẩn tuân thủ theo ngành
- **PCI-DSS** (thẻ thanh toán): không được lưu CVV; số thẻ đầy đủ (PAN) nếu phải lưu thì bắt buộc mã hóa mạnh + tokenization; khuyến nghị dùng payment gateway bên thứ ba đã đạt PCI-DSS thay vì tự xử lý thẻ trực tiếp để giảm phạm vi tuân thủ (scope reduction).
- **HIPAA** (y tế — nếu làm việc với đối tác Mỹ): yêu cầu Business Associate Agreement (BAA) với mọi vendor xử lý dữ liệu y tế (PHI), audit log truy cập bắt buộc, mã hóa dữ liệu at-rest và in-transit.
- **PDPA/NĐ 13/2023** (Việt Nam): yêu cầu có văn bản đánh giá tác động xử lý dữ liệu cá nhân (tương tự DPIA), thông báo cho Bộ Công an trong một số trường hợp xử lý dữ liệu nhạy cảm quy mô lớn.
