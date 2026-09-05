# QUY TRÌNH & VẬN HÀNH (Quy trình làm việc & Yếu tố con người)

Công cụ và kỹ thuật chỉ bảo vệ được một nửa hệ thống. Một nửa còn lại nằm ở văn hóa, con người, và quy trình vận hành liên tục.

## 1. Quy trình Phát triển An toàn (Secure SDLC)

Bảo mật phải được nhúng vào tất cả các khâu từ thu thập yêu cầu tới Deploy:
1. **Thiết kế**: Threat Modeling sớm (dùng mô hình STRIDE). Xác định các luồng dữ liệu, nơi dữ liệu đi qua biên giới hệ thống (Trust boundaries).
2. **Code**: Team phải có Secure Coding Guideline nội bộ để tuân thủ.
3. **Review**: Code Review là bắt buộc. Đặc biệt với các module Auth, Payment, hoặc Data Access.
4. **Test & Build**: SAST / DAST / SCA chạy tự động ở CI/CD pipeline để cản code lỗi trước khi merge.
5. **Release & Audit**: Pentest định kỳ (Bởi team nội bộ độc lập hoặc thuê ngoài) ít nhất 1-2 lần mỗi năm hoặc trước các bản release tính năng cực kỳ lớn.

## 2. Quản lý Vận hành & Thay đổi (Operations & Change Management)

- **Access Review**: Rà soát định kỳ xem ai đang có quyền gì trong hệ thống. Tuyệt đối thu hồi quyền ngay lập tức khi nhân viên nghỉ việc hoặc thay đổi phòng ban (Offboarding process).
- **Change Management**: Bất kỳ thay đổi hạ tầng hay cấu hình production nào cũng phải được review kịch bản, và luôn luôn có kế hoạch Rollback.
- **Patch Management**: Quy trình vá các lỗi đã được công bố. 
  - Phải có SLA rõ ràng theo điểm rủi ro (CVSS Score). 
  - VD: Lỗ hổng Critical phải vá trong vòng 24-48h, Lỗ hổng Low có thể vá trong sprint kế tiếp.

## 3. Quy trình Báo cáo Lỗ hổng (Vulnerability Disclosure Policy)

- **Vulnerability Disclosure Policy**: Cần có một quy trình công bố lỗ hổng có trách nhiệm. Nếu có nhà nghiên cứu độc lập hoặc hacker mũ trắng báo lỗi cho công ty, cần có kênh tiếp nhận thân thiện thay vì im lặng hoặc dọa kiện (việc này sẽ gây khủng hoảng truyền thông cực lớn).
- *Lưu ý: Đối với quy trình Xử lý Sự cố (Incident Response Plan), Playbook chống hack và Kế hoạch Truyền thông, vui lòng xem chi tiết tại [File 12: Ứng phó sự cố và Phục hồi](12_ung_pho_su_co_va_phuc_hoi.md).*

## 4. Xây dựng Đội ngũ Đối kháng (Red / Blue / Purple Team)

Trong một tổ chức trưởng thành, bảo mật là quá trình đối kháng nội bộ diễn ra liên tục:
- **Red Team**: Nhóm chuyên trách việc mô phỏng tấn công (như một nhóm Hacker thật sự), liên tục tìm cách chọc thủng hệ thống mà không báo trước để kiểm tra khả năng phòng ngự.
- **Blue Team**: Nhóm phòng thủ, quản lý giám sát (SIEM, Alert) có nhiệm vụ phát hiện ra Red Team và ngăn chặn.
- **Purple Team**: Sự kết hợp và hợp tác giữa Red và Blue để cùng nhau thảo luận, review và cải thiện hệ thống bảo mật tổng thể nhanh hơn.
- **Tabletop Exercise**: Các buổi diễn tập giả định sự cố mạng (không thao tác trên server thật mà ngồi họp bàn). Mục đích để test phản ứng của ban lãnh đạo và quy trình vận hành. Rẻ, cực kỳ hiệu quả mà thường bị bỏ quên.

## 5. Metrics: Đo lường Hiệu quả Bảo mật

Không có số liệu thì không biết bảo mật đang tốt lên hay tệ đi. Các chỉ số cần track:
- **MTTD (Mean Time To Detect)**: Thời gian trung bình từ lúc mã độc/kẻ tấn công xâm nhập đến lúc Blue Team phát hiện ra.
- **MTTR (Mean Time To Remediate/Respond)**: Thời gian trung bình để xử lý và vá xong lỗ hổng kể từ lúc phát hiện.
- **Tỉ lệ Coverage của SAST/DAST** trong toàn bộ hệ thống pipeline.
- Số lượng lỗ hổng Critical / High đang ở trạng thái Open quá thời hạn SLA cho phép.

## 6. Yếu tố Con người (Human Factor)

> Nội dung chi tiết về chống Phishing, Đào tạo Nhận thức Bảo mật, và Quản trị rủi ro Nội gián (Insider Threat) đã được quy chuẩn hóa ở cấp độ tổ chức.
> 
> *Vui lòng xem chi tiết tại [File 13: Yếu Tố Con Người & Mật Mã Học](13_nhan_thuc_bao_mat_va_mat_ma_hoc.md).*

## 7. Vận hành tuân thủ quyền riêng tư (Privacy Operations)

> Toàn bộ quy trình vận hành DSAR, PIA/DPIA, Data Retention, và tuân thủ pháp lý (GDPR/NĐ13) đã được tách thành một bộ tài liệu chuyên sâu.
> 
> *Vui lòng xem chi tiết tại [File 11: Quyền Riêng Tư Dữ Liệu và Tuân Thủ](11_quyen_rieng_tu_va_tuan_thu_phap_ly.md).*
