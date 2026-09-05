# TỔNG QUAN & TƯ DUY BẢO MẬT

Tài liệu này tổng hợp các tư duy nền tảng xuyên suốt cần có trước khi bắt tay vào thiết kế hay viết mã cho bất kỳ hệ thống nào. 

## 1. Tư duy xuyên suốt (Core Mindsets)

- **Assume breach**: Luôn giả định hệ thống sẽ hoặc đã bị xâm nhập một phần. Hãy thiết kế để giảm thiểu thiệt hại (blast radius) khi sự cố xảy ra chứ không chỉ cố gắng ngăn chặn 100%.
- **Shift left**: Đưa bảo mật vào càng sớm càng tốt trong vòng đời phát triển (SDLC), ngay từ lúc thu thập yêu cầu và thiết kế kiến trúc, không phải để đến bước cuối cùng trước khi release mới kiểm tra.
- **Bảo mật là quy trình liên tục**: Không phải là trạng thái đạt được một lần rồi xong. Cần review, patch, test định kỳ.
- **Sự cân bằng**: Cân bằng giữa mức độ bảo mật với chi phí (tiền bạc, thời gian) và trải nghiệm người dùng. Không phải hệ thống nào cũng cần mức độ bảo mật như hàng không vũ trụ. Quan trọng là đánh giá đúng risk phù hợp với dữ liệu và nghiệp vụ.

## 2. Tư duy về Risk (Rủi ro)

- **Risk = Likelihood × Impact**: Không phải mọi lỗ hổng đều đáng đầu tư xử lý như nhau. Một hệ thống cố gắng "bảo mật tuyệt đối" mọi thứ thường phá sản hoặc rất chậm ra mắt sản phẩm.
- **Risk Register**: Liệt kê rủi ro đã biết, đánh giá, chấp nhận có ý thức (risk acceptance) hoặc chuyển giao rủi ro (risk transfer — ví dụ mua bảo hiểm mạng/cyber insurance), thay vì mặc định "phải fix hết".
- **Threat modeling có framework rõ ràng**: Nên chọn 1 framework làm chuẩn cho team thay vì đánh giá cảm tính. Ví dụ:
  - **STRIDE**: Đánh giá các mối đe dọa (Spoofing, Tampering, Repudiation, Info Disclosure, Denial of Service, Elevation of Privilege).
  - **DREAD**: Chấm điểm rủi ro.
  - **PASTA**: Gắn kết bảo mật với business impact.
  - **Attack Trees**: Mô hình hóa đường đi của kẻ tấn công.
- **Exploitability over Theory**: Mọi lỗ hổng phải đi kèm kịch bản khai thác thực tế (concrete attack scenario: ai tấn công, bằng cách nào, gây ra hậu quả gì). Nếu chỉ là "về lý thuyết có thể bị tấn công" thì chưa đủ căn cứ để gọi là lỗ hổng đáng ưu tiên.
- **Defense-in-depth gaps are not vulnerabilities**: Việc thiếu một lớp bảo vệ (VD: thiếu rate limit ở tầng app) không tự động trở thành lỗ hổng nghiêm trọng nếu hệ thống đã có lớp bảo vệ khác (VD: rate limit ở WAF/CDN) đang hoạt động tốt. Phải đánh giá rủi ro dựa trên tổng thể thực tế.

## 3. Kinh tế học của bảo mật (Security Economics)

- **Chi phí tấn công vs. Giá trị tài sản**: Kẻ tấn công cũng tối ưu ROI — nếu chi phí để khai thác > giá trị thu được, họ sẽ bỏ qua. Do đó, hãy thiết kế sao cho **chi phí tấn công luôn lớn hơn rất nhiều so với giá trị mục tiêu**.
- **Security debt (Nợ bảo mật)**: Giống như technical debt (nợ kỹ thuật), càng trì hoãn vá lỗ hổng thì hệ thống càng tích lũy rủi ro. Cần track nợ bảo mật như một loại nợ kỹ thuật thực sự: có owner (người chịu trách nhiệm) và có deadline.
- Không phải lúc nào cũng dùng giải pháp đắt nhất. Đôi khi WAF + rate limit đã đủ chặn 90% attack, không cần phải áp dụng zero-trust full-stack đắt đỏ ngay từ ngày đầu với một startup quy mô 5 người.

## 4. Văn hóa bảo mật (Security Culture) & Security Champions

- Không thể chỉ có 1 team security ôm hết mọi thứ cho cả công ty. 
- **Mô hình Security Champion**: Mỗi team dev nên có 1 người được training sâu hơn về bảo mật. Người này làm cầu nối giữa security team và dev team, chịu trách nhiệm review sớm từ trong team thay vì đợi audit ở cuối kỳ.
- Bảo mật không phải là "rào cản" do security team đặt lên dev. Tư duy trưởng thành là biến nó thành trách nhiệm chung. "Shift left" không chỉ là áp dụng công cụ sớm, mà phải là "shift left" cả về văn hóa.
