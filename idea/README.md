### 1. ☁️ DevOps & SRE (Site Reliability Engineering)
Nhóm này cực kỳ quan trọng để tự động hóa và duy trì hệ thống sống.
*   **Mục tiêu:** Quản lý hạ tầng, tự động hóa 배포 (deploy), và đảm bảo độ tin cậy.
*   **Đầu ra (Outputs):** Scripts Dockerfile/docker-compose, Kubernetes manifests, Terraform/Pulumi (Infrastructure as Code), CI/CD pipelines (GitHub Actions, GitLab CI), và cấu hình Monitor/Alerting (Prometheus, Grafana).
*   **Lý do cần:** Tránh tình trạng "code chạy tốt trên máy dev nhưng tịt trên production". Agent đóng vai trò kỹ sư DevOps sẽ setup toàn bộ luồng deploy chuẩn chỉnh.

### 2. 🗄️ Database & Data Engineering (Thiết kế & Tối ưu Dữ liệu)
Dù nhóm "Code Architecture" có nhắc đến hệ thống, nhưng việc thiết kế Schema CSDL là một mảng rất sâu.
*   **Mục tiêu:** Thiết kế cấu trúc lưu trữ, tối ưu hóa truy vấn và quản lý luồng dữ liệu.
*   **Đầu ra:** ERD (Entity-Relationship Diagrams), SQL Migration scripts, chiến lược Đánh chỉ mục (Indexing), thiết kế Caching (Redis/Memcached), và Data pipelines.
*   **Lý do cần:** Dữ liệu là cốt lõi. Một Agent chuyên trách về Data sẽ giúp bạn tránh các lỗi như N+1 query, khóa chéo (deadlock), hoặc thiết kế bảng không thể scale khi dữ liệu phình to.

### 3. 🚀 Performance & Load Testing (Tối ưu Hiệu năng)
Nhóm QA/QC hiện tại của bạn đang nghiêng về kiểm thử chức năng (Functional) và chất lượng test script.
*   **Mục tiêu:** Đảm bảo hệ thống chịu tải được khi có nhiều người dùng.
*   **Đầu ra:** Kịch bản test chịu tải (K6, JMeter), báo cáo phân tích thắt cổ chai (bottlenecks), phát hiện rò rỉ bộ nhớ (memory leaks).
*   **Lý do cần:** Tránh việc hệ thống sập ngay khi vừa launch. Kỹ năng này hướng dẫn Agent cách stress-test mã nguồn thay vì chỉ pass Unit Test.

### 4. 🔌 API Design & Integration (Thiết kế Cổng giao tiếp)
Đặc biệt quan trọng nếu dự án của bạn là Microservices hoặc có app Mobile/Web tách biệt.
*   **Mục tiêu:** Chuẩn hóa giao thức giao tiếp giữa các services và với bên thứ 3.
*   **Đầu ra:** OpenAPI/Swagger Specs, GraphQL schemas, gRPC protobufs, và chiến lược kết nối 3rd-party (Payment, SMS, Email).
*   **Lý do cần:** Giúp Frontend và Backend làm việc hoàn toàn độc lập thông qua "hợp đồng API" (API Contract), không bị chồng chéo code.

### 5. 📚 Technical Writing (Tài liệu hóa Kỹ thuật)
Dành cho giai đoạn cuối (Bàn giao).
*   **Mục tiêu:** Viết tài liệu cho User và cho Developer thế hệ sau.
*   **Đầu ra:** README chuẩn mực, API Documentation, Release Notes, và User Manuals.
*   **Lý do cần:** Dự án dù code tốt đến đâu mà không có tài liệu thì cũng bằng không. Agent Tech Writer sẽ chuyên làm nhiệm vụ đọc hiểu code và dịch nó ra ngôn ngữ dễ hiểu.

---

**Tóm lại:** Nếu bạn muốn bộ repo này trở thành "công ty phần mềm thu nhỏ" hoàn hảo, tôi đề xuất ưu tiên thêm 2 nhóm là **DevOps** (để tự động hóa đưa code lên server) và **Database Design** (để tối ưu nền tảng dữ liệu) trước! Bạn có muốn tôi tạo cấu trúc cho 1 trong các nhóm này không?