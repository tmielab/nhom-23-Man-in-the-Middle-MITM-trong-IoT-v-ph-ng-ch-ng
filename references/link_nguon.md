# Danh sách nguồn tài liệu tham khảo - Đề tài 23: MITM trong IoT

Tài liệu này tổng hợp các nguồn học liệu từ hệ sinh thái tài liệu học tập cục bộ và các khuyến nghị quốc tế được sử dụng làm cơ sở thiết kế giải pháp phòng chống Man-in-the-Middle (MITM) trong IoT (đặc biệt là cơ chế Certificate Pinning).

## 1. Tài liệu Ngữ cảnh Cục bộ (Local Resources)
Các file đặc tả kỹ thuật học được từ hệ thống:
- **[V1-IoT_Ecosystem_Requirements.md](../gitmd/V1-IoT_Ecosystem_Requirements.md)**: Định nghĩa các mức độ bảo mật (L1-L3), thiết kế chuỗi cung ứng an toàn, và bảo mật cấu trúc phát triển hệ phần mềm nhúng.
- **[V2-User_Space_Application_Requirements.md](../gitmd/V2-User_Space_Application_Requirements.md)**: Định nghĩa yêu cầu về định danh thiết bị, mã hóa lưu trữ thông tin nhạy cảm và chuyển dịch sang mật mã học hậu lượng tử (Post-Quantum Cryptography).
- **[V4-Communication_Requirements.md](../gitmd/V4-Communication_Requirements.md)**: Quy chuẩn kết nối mạng bảo mật, bắt buộc xác thực mã băm chứng chỉ (Certificate Pinning) tại điều khoản 4.1.5 nhằm chống lại tấn công nghe lén và sửa đổi dữ liệu.
- **[checklist.md](../gitmd/checklist.md)**: Checklist đánh giá bảo mật tổng thể theo chuẩn OWASP IoT Security Testing Guide (ISTG).

## 2. Tiêu chuẩn quốc tế về Phòng chống MITM & Transport Layer
Các nguồn tài liệu tham khảo mở rộng từ các tổ chức bảo mật uy tín:
- **OWASP Transport Layer Protection Cheat Sheet**: Hướng dẫn cấu hình TLS bảo mật và triển khai Pinning.
  - Link: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html
- **OWASP IoT Security Testing Guide (ISTG)**: Cẩm nang kiểm thử bảo mật thiết bị IoT.
  - Link: https://owasp.org/www-project-internet-of-things/
- **IETF RFC 7525 - Recommendations for Secure Use of TLS and DTLS**: Khuyến nghị cấu hình an toàn cho giao thức truyền thông TLS.
  - Link: https://datatracker.ietf.org/doc/html/rfc7525
- **NIST SP800-52r2 - Guidelines for TLS Implementations**: Hướng dẫn của Viện Tiêu chuẩn và Công nghệ Quốc gia Mỹ về cấu hình TLS.
  - Link: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-121r2.pdf
- **Mbed TLS (ARM Cryptography & TLS Library)**: Thư viện mã nguồn mở chuyên dụng cho các hệ thống nhúng (ESP32, STM32).
  - Link: https://github.com/Mbed-TLS/mbedtls
