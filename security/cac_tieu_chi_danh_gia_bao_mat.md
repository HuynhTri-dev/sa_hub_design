## 1. Tư duy về Risk, không phải chỉ "chặn hết mọi thứ"

- **Risk = Likelihood × Impact**, không phải mọi lỗ hổng đều đáng đầu tư như nhau. Một hệ thống cố "bảo mật tuyệt đối" mọi thứ thường phá sản hoặc chậm ra sản phẩm.
- **Risk register**: liệt kê rủi ro đã biết, đánh giá, chấp nhận có ý thức (risk acceptance) hoặc chuyển giao (risk transfer — bảo hiểm mạng/cyber insurance), thay vì mặc định "phải fix hết".
- **Threat modeling có framework rõ ràng**: STRIDE (đã nhắc), nhưng còn DREAD (chấm điểm rủi ro), PASTA (gắn với business impact), Attack Trees — bạn nên chọn 1 cái làm chuẩn cho team thay vì làm cảm tính.
- **Exploitability over Theory**: Mọi lỗ hổng phải đi kèm kịch bản khai thác thực tế (concrete attack scenario: ai tấn công, bằng cách nào, gây ra hậu quả gì). Nếu chỉ là "về lý thuyết có thể bị tấn công" thì chưa đủ căn cứ để gọi là một lỗ hổng đáng ưu tiên.
- **Defense-in-depth gaps are not vulnerabilities**: Việc thiếu một lớp bảo vệ (VD: thiếu rate limit ở tầng app) không tự động trở thành lỗ hổng nghiêm trọng nếu hệ thống đã có lớp bảo vệ khác (VD: rate limit ở WAF/CDN) đang hoạt động tốt. Đánh giá rủi ro dựa trên tổng thể thực tế, không phải đánh giá dựa trên việc tick đủ check-list.

## 2. Kinh tế học của bảo mật (Security Economics)

- Chi phí tấn công vs. giá trị tài sản: kẻ tấn công cũng tối ưu ROI — nếu chi phí khai thác > giá trị thu được, họ bỏ qua. Thiết kế sao cho **chi phí tấn công luôn lớn hơn giá trị mục tiêu**.
- **Security debt**: giống technical debt, càng trì hoãn vá càng tích lũy rủi ro — cần track như một loại nợ kỹ thuật thực sự, có owner, có deadline.
- Không phải lúc nào cũng dùng giải pháp đắt nhất — đôi khi WAF + rate limit đã đủ chặn 90% attack, không cần zero-trust full-stack ngay từ ngày đầu với startup 5 người.

## 3. Privacy Engineering (khác Data Protection)

Đây là mảng dễ nhầm với "Data Protection" ở tài liệu trước nhưng thực ra là tư duy khác:
- **Data minimization**: đừng thu thập dữ liệu không cần — thứ không có thì không thể bị đánh cắp
- **Purpose limitation**: dữ liệu thu cho mục đích A không được dùng ngầm cho mục đích B
- **Right to be forgotten / data retention policy**: có quy trình xóa dữ liệu thật sự (kể cả trong backup, log, vector DB — đây là điểm rất dễ bị bỏ sót trong RAG system, embedding cũ vẫn còn "nhớ" dữ liệu đã xóa)
- Đặc biệt quan trọng với **OmniMer Health** — dữ liệu sức khỏe cần tư duy privacy-by-design ngay từ schema, không phải thêm sau.

## 4. Cryptographic Agility & tương lai

- Không hardcode 1 thuật toán mã hóa cố định vĩnh viễn — thiết kế sao cho **thay được thuật toán/key mà không phải viết lại hệ thống** (versioned encryption scheme)
- **Post-quantum readiness**: chưa cấp thiết ngay, nhưng các tổ chức lớn (NIST) đã bắt đầu chuẩn hóa thuật toán chống lượng tử — nếu hệ thống bạn xử lý dữ liệu cần bảo mật 10-20 năm, nên biết xu hướng này tồn tại.

## 5. Red Team / Blue Team / Purple Team

- Bạn có nhắc pentest, nhưng thiếu tư duy **team đối kháng nội bộ liên tục**: Red Team (tấn công), Blue Team (phòng thủ/phát hiện), Purple Team (kết hợp cả hai để cải thiện lẫn nhau) — khác với pentest 1 lần/năm, đây là văn hóa vận hành liên tục ở tổ chức trưởng thành.
- **Tabletop exercise**: diễn tập giả lập incident (không chạm hệ thống thật) để test quy trình phản ứng của con người — rất hay bị bỏ qua dù rẻ và hiệu quả.

## 6. Metrics & đo lường hiệu quả bảo mật

Thiếu hẳn phần này ở bản trước — "bảo mật tốt" cần đo được:
- MTTD (Mean Time To Detect), MTTR (Mean Time To Remediate/Respond)
- % coverage của SAST/DAST trong pipeline
- Số lượng lỗ hổng critical đang mở quá SLA
- Không có số liệu thì không biết đang cải thiện hay tệ đi, và không thuyết phục được leadership đầu tư thêm.

## 7. Security Culture / Security Champions

- Không thể chỉ có 1 team security ôm hết cho cả công ty — mô hình **Security Champion**: mỗi team dev có 1 người được train sâu hơn về bảo mật, làm cầu nối giữa security team và dev team, review sớm từ trong team thay vì đợi audit cuối.
- Bảo mật không phải "rào cản" của security team đặt lên dev — tư duy trưởng thành là biến nó thành trách nhiệm chung, "shift left" cả về văn hóa chứ không chỉ công cụ.

## 8. Vulnerability Disclosure & xử lý khủng hoảng truyền thông

- Có **quy trình công bố lỗ hổng có trách nhiệm** (responsible disclosure policy) — nếu ai đó (nhà nghiên cứu, hacker mũ trắng) báo lỗ hổng cho bạn, cần kênh tiếp nhận rõ ràng, không im lặng hoặc dọa kiện (gây mất uy tín nghiêm trọng)
- Kế hoạch truyền thông khi breach xảy ra thật — ai được nói, nói gì, khi nào phải báo cơ quan quản lý (ở VN có quy định báo cáo sự cố an toàn thông tin trong thời hạn nhất định)

## 9. Supply Chain nâng cao hơn nữa: SLSA Framework

- Bản trước có SBOM, nhưng còn thiếu **SLSA (Supply-chain Levels for Software Artifacts)** — framework phân cấp độ tin cậy của build pipeline (từ level 1 đến 4), Google/OpenSSF đang đẩy mạnh chuẩn này sau vụ SolarWinds.

## 10. AI/Agent-specific — mảng sát nhất với công việc của bạn, nhưng vẫn còn thiếu

Bản trước có nói prompt injection, nhưng còn thiếu:
- **Model/Data poisoning**: nếu hệ thống fine-tune hoặc RAG index cho phép ingest dữ liệu từ nguồn không tin cậy, kẻ tấn công có thể "đầu độc" dữ liệu để thao túng output lâu dài
- **Excessive agency**: agent có quyền hành động (gọi API, ghi DB, gửi email) mà không có human-in-the-loop cho hành động nhạy cảm — đây là rủi ro mới, gần như không tồn tại trong app truyền thống
- **Output validation/guardrails**: đầu ra của LLM cần được validate như bất kỳ input không tin cậy nào khác trước khi dùng để thực thi hành động — nhiều team quên rằng LLM output cũng là "user input" theo một nghĩa nào đó
