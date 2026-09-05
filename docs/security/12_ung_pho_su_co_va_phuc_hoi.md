# 12. Ứng Phó Sự Cố và Phục Hồi (Incident Response & Disaster Recovery)

*(Cấp độ Enterprise/Chính phủ: Sẵn sàng ứng phó với tấn công APT, Ransomware và duy trì tính liên tục của hệ thống)*

## 12.1 Playbook ứng phó theo từng loại sự cố
Mỗi loại sự cố cần một playbook riêng vì hành động đầu tiên khác nhau hoàn toàn:

**Ransomware:**
1. Cô lập ngay các máy nghi nhiễm khỏi mạng (không tắt máy — có thể mất bằng chứng forensic trong RAM).
2. Xác định chủng ransomware, kiểm tra có decryption tool công khai không (No More Ransom project).
3. Không vội trả tiền chuộc — đánh giá qua pháp lý/bảo hiểm trước.
4. Khôi phục từ backup **offline/immutable** (backup online cùng mạng cũng có thể bị mã hóa theo).

**Data Breach:**
1. Xác định phạm vi dữ liệu bị lộ (loại dữ liệu, số lượng user ảnh hưởng).
2. Vá lỗ hổng gốc trước khi công bố (tránh bị khai thác tiếp trong lúc xử lý).
3. Thông báo cơ quan quản lý trong 72h (GDPR) và người dùng bị ảnh hưởng theo luật áp dụng.
4. Chuẩn bị bộ phận truyền thông/pháp lý song song với đội kỹ thuật.

**DDoS:**
1. Kích hoạt DDoS mitigation (Cloudflare, AWS Shield) — nên có sẵn từ trước, không đợi tấn công mới đăng ký.
2. Phân biệt DDoS thật với traffic spike hợp lệ (flash sale, viral content) để tránh block nhầm user thật.
3. Rate limiting + WAF rule tạm thời cho endpoint bị nhắm tới cụ thể.

## 12.2 BCP (Business Continuity Plan)
- Xác định **RTO** (Recovery Time Objective — thời gian tối đa được phép ngừng hoạt động) và **RPO** (Recovery Point Objective — lượng dữ liệu tối đa được phép mất, tính theo thời gian kể từ backup gần nhất) cho từng hệ thống theo mức độ quan trọng.
- Xác định **quy trình vận hành thủ công tạm thời** khi hệ thống chính down (ví dụ: quy trình xử lý đơn hàng bằng tay khi hệ thống order-management sập).

## 12.3 DR (Disaster Recovery)
- Chiến lược theo mức độ ưu tiên/ngân sách: **Backup & Restore** (rẻ, RTO/RPO cao) → **Pilot Light** → **Warm Standby** → **Multi-site Active-Active** (đắt nhất, RTO/RPO gần bằng 0).
- **Diễn tập DR định kỳ** (DR drill) — kế hoạch không có giá trị nếu chưa từng thử nghiệm thực tế; nhiều tổ chức chỉ phát hiện backup bị lỗi/không restore được khi đã quá muộn.
- Backup phải tuân theo nguyên tắc **3-2-1**: 3 bản sao, 2 loại phương tiện lưu trữ khác nhau, 1 bản off-site (và nên có ít nhất 1 bản **immutable/air-gapped** để chống ransomware mã hóa luôn cả backup).
