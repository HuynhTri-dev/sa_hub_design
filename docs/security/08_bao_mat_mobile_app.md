---
name: "Bảo mật ứng dụng di động"
description: "Các kỹ thuật và rủi ro bảo mật đặc thù dành cho ứng dụng di động (iOS/Android)."
---

# BẢO MẬT ỨNG DỤNG DI ĐỘNG (Mobile Application Security)

Tài liệu này tập trung vào các biện pháp bảo vệ chuyên biệt dành cho phần mềm hoạt động trên môi trường di động (iOS, Android).

## 1. Chống Root / Jailbreak Detection
- Kiểm tra dấu hiệu thiết bị bị root/jailbreak trước khi cho phép chạy các tính năng nhạy cảm (thanh toán, xác thực sinh trắc học, lưu trữ token).
- Kỹ thuật: kiểm tra file hệ thống bất thường (`su`, `Cydia`, `Magisk`), kiểm tra quyền ghi vào thư mục hệ thống, kiểm tra chữ ký ứng dụng qua SafetyNet/Play Integrity API (Android) hoặc DeviceCheck/App Attest (iOS).
- Lưu ý: không nên chỉ dựa vào 1 lớp kiểm tra vì có thể bị bypass bằng Magisk Hide/Frida; nên kết hợp nhiều tín hiệu (behavioral + static).

## 2. Lưu trữ an toàn trên thiết bị (Keychain/Keystore)
- **iOS**: dùng Keychain Services để lưu token, mật khẩu, khóa mã hóa — không lưu trong `UserDefaults` hay `plist`.
- **Android**: dùng Android Keystore System để sinh và lưu private key trong phần cứng bảo mật (TEE/StrongBox), không lưu key trong `SharedPreferences` dạng plaintext.
- Token phiên (session token) nên có thời hạn ngắn và cơ chế refresh, tránh lưu refresh token vĩnh viễn không mã hóa.

## 3. Mã hóa cơ sở dữ liệu nội bộ (Local DB Encryption)
- Dùng SQLCipher (mã hóa AES cho SQLite) hoặc Realm Encrypted Database thay vì SQLite thuần.
- Không hardcode encryption key trong source code; key nên được sinh và lưu trong Keychain/Keystore, hoặc dẫn xuất từ passphrase người dùng qua PBKDF2/Argon2.
- Áp dụng cho cache offline, log ứng dụng, và dữ liệu nhạy cảm tạm thời (draft form, lịch sử tìm kiếm).

## 4. Certificate Pinning (chống MITM)
- Pin public key hoặc certificate của server ngay trong app để chặn tấn công man-in-the-middle qua proxy giả mạo (Burp Suite, mitmproxy) hoặc CA giả trong thiết bị bị compromise.
- Nên pin theo **public key hash** (SPKI pinning) thay vì pin nguyên certificate, vì certificate hết hạn/renew mà không cần cập nhật app.
- Cần có cơ chế backup pin (2+ khóa) để tránh app "chết cứng" khi đổi certificate mà quên cập nhật kịp.
- Kết hợp thêm kiểm tra TLS version tối thiểu (TLS 1.2+) và loại bỏ cipher suite yếu.

## 5. Chống dịch ngược (Obfuscation / Anti-Tampering)
- **Android**: dùng ProGuard/R8 để obfuscate code, kết hợp DexGuard hoặc các công cụ thương mại cho tầng bảo vệ cao hơn (native code protection, string encryption).
- **iOS**: hạn chế hơn do App Store review, nhưng vẫn có thể áp dụng symbol stripping, string encryption thủ công cho các hằng số nhạy cảm (API key, endpoint nội bộ).
- Anti-tampering: kiểm tra checksum/chữ ký của APK/IPA lúc runtime để phát hiện app bị sửa đổi và repackage.
- Không bao giờ hardcode API key, secret, hoặc endpoint nội bộ trực tiếp trong code — dùng biến môi trường build-time hoặc lấy về từ backend sau khi xác thực.

## 6. Các điểm bổ sung khác thường bị bỏ sót
- **Deep link / Universal Link validation**: kiểm tra nguồn gọi deep link để tránh bị lợi dụng cho phishing hoặc chiếm quyền điều khiển luồng OAuth.
- **WebView security**: tắt JavaScript nếu không cần thiết, không cho phép `file://` scheme tùy tiện, kiểm soát chặt `addJavascriptInterface` (Android) vì có thể bị khai thác RCE.
- **Clipboard leakage**: tránh copy dữ liệu nhạy cảm (OTP, mật khẩu) vào clipboard hệ thống nếu không cần thiết.
- **Screen recording/screenshot protection** cho màn hình hiển thị dữ liệu nhạy cảm (số thẻ, thông tin y tế).
- **Biometric authentication**: dùng API chuẩn (BiometricPrompt trên Android, LocalAuthentication trên iOS), không tự implement so khớp vân tay/khuôn mặt.
