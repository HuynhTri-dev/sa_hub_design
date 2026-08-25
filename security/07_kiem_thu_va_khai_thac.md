# KỸ THUẬT & CÔNG CỤ KIỂM THỬ KHAI THÁC LỖ HỔNG (Offensive Security)

> *Mục tiêu của tài liệu này là cung cấp góc nhìn của kẻ tấn công để phòng thủ tốt hơn. Tư duy "Offensive Security" phải luôn đi kèm với đạo đức nghề nghiệp, và chỉ áp dụng trên hệ thống của chính bạn hoặc các hệ thống đã cấp quyền ủy quyền.*

## 1. Trinh sát & Quét mạng (Reconnaissance & Scanning)

Bước đầu tiên để tấn công là thu thập thông tin về bề mặt tấn công (Attack Surface).
- **Nmap**: Công cụ kinh điển để quét các port đang mở, các service đang chạy, và fingerprinting phiên bản Hệ điều hành / Phần mềm.
- **Amass / Subfinder**: Dò tìm các Subdomain ẩn, mở rộng Attack Surface (Ví dụ: `dev.company.com`, `api-old.company.com`).
- **Shodan / Censys**: Các "công cụ tìm kiếm" dành cho thiết bị IoT, Server, và các dịch vụ cấu hình lỏng lẻo bị expose trực tiếp ra ngoài Internet.

## 2. Kiểm thử Ứng dụng Web (Web Application Testing)

- **Burp Suite / OWASP ZAP**: Hai bộ công cụ chặn, sửa request (Proxy) và quét lỗ hổng ứng dụng web mạnh mẽ nhất. Được dùng từ quét tự động tới phân tích manual.
- **sqlmap**: Công cụ tự động hóa việc phát hiện và khai thác cực sâu lỗi SQL Injection.
- **Nikto**: Quét các lỗi cấu hình cơ bản của Web Server (Lộ file `.git`, lộ file config tĩnh, phiên bản webserver cũ kỹ).

## 3. Phân tích Tĩnh và Dependency (Static & Dependency Analysis)

- **SAST (Static Application Security Testing)**: 
  - **Semgrep / CodeQL**: Phân tích mã nguồn tĩnh, tìm kiếm các đoạn code lỗi, pattern code không an toàn mà không cần phải chạy (execute) phần mềm.
- **SCA (Software Composition Analysis)**:
  - **Trivy / Grype**: Quét lỗ hổng container image, hệ thống file.
  - **Snyk / Dependabot / OWASP Dependency-Check**: Quét lỗ hổng đến từ các thư viện, package phụ thuộc của dự án.

## 4. Kiểm thử Động (Dynamic/Runtime Testing)

- **DAST (Dynamic Application Security Testing)**: 
  - Có thể dùng bản command-line của OWASP ZAP hoặc Burp Suite tích hợp thẳng vào CI/CD. Chạy ứng dụng lên và bắn request giả lập tấn công để test.
- **Fuzzing (Kỹ thuật ném dữ liệu hỗn loạn)**:
  - **AFL, libFuzzer**: Liên tục nhồi/gửi các chuỗi input ngẫu nhiên, bất thường hoặc cực lớn để tìm ra các vị trí làm phần mềm bị Crash hoặc Memory leak. Đặc biệt hiệu quả với các parser xử lý file format (XML, PDF, JSON).
- **Postman/Newman + Security Test Collection**: Có thể dùng để viết các script test tự động chạy check phân quyền API.

## 5. Đánh giá Cấu hình Hạ tầng & Cloud

- **ScoutSuite / Prowler**: Công cụ Audit tự động, quét hàng ngàn rule kiểm tra lỗi cấu hình (Misconfiguration) trên môi trường Cloud (AWS, GCP, Azure).
- **kube-hunter / kube-bench**: Công cụ chuyên biệt để kiểm tra bảo mật cấu hình của Kubernetes cluster và các Nodes.

## 6. Lộ trình Học hỏi thêm (Offensive Security)

Nếu muốn đi sâu vào con đường tìm lỗ hổng:
1. **Nền tảng**: Hiểu cực sâu bộ OWASP Top 10.
2. **Thực hành miễn phí**: **PortSwigger Web Security Academy** (Tài liệu và Lab miễn phí chất lượng cao nhất hiện nay, tạo bởi chính công ty làm ra Burp Suite).
3. **Môi trường diễn tập**: Luyện tập tấn công hợp pháp trên **HackTheBox** hoặc **TryHackMe**.
4. **CTF (Capture The Flag)**: Chơi các giải CTF để rèn luyện tư duy tìm lỗ hổng và sáng tạo kỹ thuật mới.
5. **Chứng chỉ tham khảo**:
   - **OSCP** (Rất thực chiến, thi thực hành hack server).
   - **CEH** (Cung cấp góc nhìn bao quát, thiên về lý thuyết).
   - **CISSP** (Chuyên gia quản trị bảo mật cấp cao).

## 7. Khai thác & Tấn công Mạng Nội bộ (Internal Network/LAN)

Mạng nội bộ (LAN/WLAN) tự nó không an toàn mặc định. Dưới đây là các vector tấn công thuần kỹ thuật khi kẻ tấn công đã có được vị trí (foothold) bên trong mạng:

**1. Tấn công tầng mạng (Layer 2/3)**
- **ARP Spoofing/Poisoning**: giả mạo địa chỉ MAC để chen vào giữa 2 máy trong LAN, nghe lén hoặc sửa traffic (MITM nội bộ) mà không cần lừa người dùng làm gì cả.
- **VLAN Hopping**: khai thác cấu hình switch sai (trunk port để mặc định) để nhảy từ VLAN này sang VLAN khác vốn phải bị cô lập.
- **DHCP Starvation / Rogue DHCP**: dựng DHCP server giả để cấp gateway/DNS giả cho máy trong mạng, từ đó redirect traffic.
- **DNS Spoofing nội bộ**: đầu độc DNS cache trong mạng LAN để điều hướng người dùng đến server giả.

**2. Thiết bị kết nối vào mạng (không phải máy nhân viên)**
- Máy in, camera IP, smart TV phòng họp, IoT thiết bị văn phòng — thường chạy firmware cũ, có lỗ hổng đã biết (CVE), và ít khi được patch. Đây là điểm chân bám (foothold) rất phổ biến để hacker lọt vào rồi di chuyển ngang (**lateral movement**) sang máy chủ quan trọng hơn.
- **Rogue device**: ai đó (không hẳn ác ý) cắm một Raspberry Pi hoặc router cá nhân vào mạng công ty tạo lỗ hổng không kiểm soát.

**3. Wi-Fi nội bộ**
- **Evil Twin AP**: dựng access point giả mạo trùng tên SSID công ty để hứng traffic.
- **WPA2/WPA3 cracking** nếu passphrase yếu hoặc dùng PSK chung cho cả công ty (không có 802.1X/RADIUS riêng từng nhân viên).
- **Deauth attack** để ép thiết bị kết nối lại vào AP giả.

**4. Thiếu network segmentation (phân vùng mạng)**
- Đây là lỗi kiến trúc lớn nhất: nếu mạng "phẳng" (flat network), một máy bị nhiễm malware ở phòng kế toán có thể touch trực tiếp tới server production. Nguyên tắc đúng là segment theo mức độ tin cậy (dev/staging/prod, phòng ban, IoT riêng VLAN) + firewall rule giữa các segment (micro-segmentation).

**5. Lỗ hổng phần mềm nội bộ chưa patch**
- Service nội bộ (file server SMB cũ, Jenkins, GitLab tự host, database quản trị) thường ít được vá kịp vì nghĩ "ở trong mạng nội bộ nên an toàn" — đây chính là tư duy sai lầm mà mô hình **Zero Trust** ra đời để khắc phục: giả định mạng nội bộ *đã* bị xâm nhập, không tin tưởng ngầm định chỉ vì "ở trong LAN".

**6. Supply chain qua thiết bị/phần mềm thứ ba**
- Update giả mạo từ phần mềm quản lý nội bộ (như vụ SolarWinds) — kẻ tấn công không cần vào tận nơi, chỉ cần compromise một phần mềm mà cả mạng tin tưởng cài đặt.
