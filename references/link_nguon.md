# Danh sách nguồn tài liệu tham khảo - Đề tài 23: MITM trong IoT

Tài liệu này tổng hợp 3 nguồn GitHub bắt buộc do Giảng viên phân công và các tiêu chuẩn bảo mật quốc tế cho Đề tài 23 (Man-in-the-Middle trong IoT và phòng chống - Hướng D).

## 1. Ba (03) Nguồn GitHub Bắt Buộc Theo Hướng Dẫn Đề Tài 23
1. **OWASP IoT Security Verification Standard (ISVS)**
   - Link Repo: https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS
   - Mục đích: Bộ tiêu chuẩn xác minh bảo mật IoT, làm cơ sở kiểm tra tính an toàn kênh truyền và xác thực thiết bị.
2. **Mbed TLS (ARM Cryptography & TLS Library)**
   - Link Repo: https://github.com/Mbed-TLS/mbedtls
   - Mục đích: Thư viện mã hóa TLS/DTLS siêu nhẹ dành cho thiết bị vi điều khiển IoT (ESP32, ARM Cortex-M), cung cấp hàm xác thực chứng chỉ `mbedtls_ssl_conf_verify()` và mã băm `mbedtls_sha256()`.
3. **OWASP IoT Security Testing Guide (ISTG)**
   - Link Repo: https://github.com/OWASP/owasp-istg
   - Mục đích: Hướng dẫn chi tiết kiểm thử an toàn thông tin cho thiết bị và hệ sinh thái IoT, quy định checklist đánh giá nguy cơ nghe lén/MITM.

## 2. Tiêu chuẩn quốc tế bổ trợ về Transport Layer & Phòng chống MITM
- **OWASP Transport Layer Protection Cheat Sheet**:
  - Link: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html
- **IETF RFC 7525 - Recommendations for Secure Use of TLS and DTLS**:
  - Link: https://datatracker.ietf.org/doc/html/rfc7525
- **IETF RFC 7252 - The Constrained Application Protocol (CoAP)**:
  - Link: https://datatracker.ietf.org/doc/html/rfc7252
- **NIST SP800-52r2 - Guidelines for TLS Implementations**:
  - Link: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf
