---
name: "Bảo mật IoT & Web3"
description: "Các kỹ thuật bảo mật đặc thù cho phần cứng, Internet of Things (IoT) và Blockchain/Smart Contracts."
---

# BẢO MẬT IOT & WEB3 (Hardware & Blockchain Security)

Tài liệu này là phụ lục kỹ thuật mở rộng, áp dụng riêng biệt cho các dự án có dính dáng đến thiết bị phần cứng thông minh (IoT) hoặc công nghệ chuỗi khối (Blockchain/Web3).

## 1. IoT / Hardware Security
- **Secure boot**: đảm bảo thiết bị chỉ chạy firmware đã được ký hợp lệ, chống flash firmware giả mạo.
- **Firmware update an toàn**: cập nhật OTA phải được ký số và mã hóa, tránh bị can thiệp giữa đường truyền.
- **Hardcoded credentials**: lỗi phổ biến nhất ở thiết bị IoT — không được để mật khẩu/API key mặc định giống nhau trên toàn bộ dòng sản phẩm.
- **Giao tiếp mã hóa**: MQTT/CoAP giữa thiết bị và cloud cần TLS, không truyền plaintext.
- **Physical tampering protection**: chip bảo mật (Secure Element/TPM) để lưu khóa, chống đọc trộm qua JTAG/UART debug port.

## 2. Web3 / Blockchain / Smart Contract Security
- **Reentrancy attack**: lỗ hổng kinh điển khi smart contract gọi external call trước khi cập nhật state nội bộ, cho phép kẻ tấn công gọi đệ quy để rút tiền nhiều lần (vụ The DAO là ví dụ nổi tiếng). Khắc phục bằng pattern Checks-Effects-Interactions hoặc dùng `ReentrancyGuard`.
- **Integer overflow/underflow**: cần dùng thư viện an toàn (SafeMath, hoặc Solidity ≥0.8 có built-in check).
- **Access control**: kiểm soát chặt hàm `onlyOwner`, tránh lỗi quên modifier khiến ai cũng gọi được hàm quản trị.
- **Oracle manipulation**: nếu smart contract phụ thuộc vào price feed bên ngoài, cần dùng oracle phi tập trung (Chainlink) thay vì một nguồn duy nhất dễ bị thao túng giá.
- **Audit bắt buộc**: mọi smart contract xử lý tài sản thực nên được audit bởi bên thứ ba (CertiK, Trail of Bits...) và chạy trên testnet trước khi deploy mainnet.
- **Private key management**: dùng multi-sig wallet (Gnosis Safe) cho quỹ/treasury thay vì single private key.
