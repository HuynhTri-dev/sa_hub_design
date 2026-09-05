# QUẢN LÝ CHUỖI CUNG ỨNG (Supply Chain Security)

Phần mềm hiện đại không được viết lại từ số không, mà được lắp ghép từ hàng nghìn thư viện mã nguồn mở. Việc bảo mật chuỗi cung ứng (Supply Chain) hiện nay là một yêu cầu sống còn.

## 1. Quản lý Lỗ hổng Dependency (Thư viện phụ thuộc)

- **Quét lỗ hổng liên tục**: Thực hiện quét định kỳ các thư viện mà dự án đang sử dụng thông qua các công cụ chuyên dụng (`npm audit`, `pip-audit`, Snyk, Dependabot, Trivy, OWASP Dependency-Check).
- **Version Pinning & Lock Files**: Luôn ghim cố định phiên bản, phải commit các lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`) lên repository để đảm bảo môi trường build production hoàn toàn giống với dev và staging, ngăn ngừa việc thư viện tự động update mang theo mã độc mới.
- **Review License và Nguồn gốc**: Luôn kiểm tra kỹ license có phù hợp với phần mềm thương mại hay không và nguồn gốc repo có đáng tin cậy không trước khi cài thêm một package mới.
- **Chống Typosquatting**: Cảnh giác và kiểm tra chính xác từng ký tự tên của package. Kẻ tấn công hay tạo ra các package giả mạo sai 1 chữ cái (VD: thay vì `requests`, chúng tạo `requets`) chứa mã độc để lừa những lập trình viên gõ vội vàng.

## 2. SBOM (Software Bill of Materials)

- SBOM là một danh sách chi tiết (như bảng thành phần nguyên liệu) liệt kê toàn bộ các thư viện, phiên bản, giấy phép, và thành phần tạo nên phần mềm.
- **Lợi ích**: Khi có một lỗ hổng chấn động thế giới (như vụ log4j), tổ chức có SBOM sẽ biết ngay lập tức mình có bị ảnh hưởng ở component nào không để phản ứng ngay, thay vì phải đi bới code từng dự án.
- Có thể dùng các chuẩn định dạng tiêu chuẩn như **CycloneDX** hoặc **SPDX**.

## 3. SLSA Framework (Supply-chain Levels for Software Artifacts)

- Một bộ quy chuẩn bảo mật cao cấp (phát triển bởi Google / OpenSSF) dùng để đánh giá và đảm bảo tính tin cậy của toàn bộ quá trình đóng gói phần mềm, chia thành 4 level từ thấp đến cao.
- Framework này giúp ngăn chặn các cuộc tấn công tinh vi (như vụ SolarWinds) nơi mà mã độc được hacker cấy trực tiếp vào pipeline Build CI/CD, biến phần mềm hợp pháp thành mã độc.
- **Sigstore / Cosign**: Ký số (Digital signature) các bản build (Artifacts/Container images) ngay trong quá trình CI/CD. Đảm bảo image chạy trên production chính là image đã đi qua quá trình kiểm thử, không bị đánh tráo giữa chừng.

## 4. Bảo mật Pipeline CI/CD

Pipeline CI/CD chính là "chìa khóa kho báu". Nếu bị chiếm quyền, kẻ tấn công có thể làm mọi thứ.
- **Bảo mật Secrets**: Không để rò rỉ token/secret vào logs của quá trình build. Khuyến khích che (mask) logs cẩn thận.
- **Branch Protection**: Bắt buộc phải có Code Review (ít nhất 1-2 Approve) trước khi Merge vào các branch chính. Không ai được quyền push đè trực tiếp (force push) lên main branch.
- **Pipeline Least Privilege**: Pipeline không được có quyền "Vô hạn" trên Cloud. Cấp quyền deploy giới hạn mức tối thiểu đủ dùng (VD: chỉ cấp quyền update ECR, update ECS, không cấp quyền xóa bảng Database).
