# -*- coding: utf-8 -*-
"""
ĐỀ TÀI 23: MAN-IN-THE-MIDDLE (MITM) TRONG IOT VÀ PHÒNG CHỐNG
Mô phỏng cơ chế Certificate Pinning (Ghim chứng chỉ) chống lại tấn công MITM.
Mã nguồn này được viết bằng Python chuẩn, không yêu cầu thư viện ngoài.

Liên hệ kiến trúc bảo mật Mbed TLS (thường dùng trong thiết bị IoT như ESP32, ARM Cortex-M):
1. Khởi tạo ngữ cảnh TLS:
   - Python: ssl.create_default_context()
   - Mbed TLS: mbedtls_ssl_config_init(), mbedtls_ssl_config_defaults()
2. Bắt tay TLS & Lấy chứng chỉ của Server:
   - Python: ssl_sock.getpeercert(binary_form=True)
   - Mbed TLS: mbedtls_ssl_handshake(), mbedtls_ssl_get_peer_cert()
3. Tính toán mã băm SHA-256 của chứng chỉ để so khớp (Pinning):
   - Python: hashlib.sha256(der_cert).hexdigest()
   - Mbed TLS: mbedtls_sha256() hoặc kiểm tra khóa công khai thông qua mbedtls_pk_write_pubkey_der()
4. Cấu hình kiểm tra chứng chỉ nghiêm ngặt:
   - Mbed TLS: Cài đặt hàm callback xác thực qua mbedtls_ssl_conf_verify() để từ chối kết nối nếu mã băm không khớp.
"""

import socket
import ssl
import hashlib
import sys

# Cấu hình kết nối tới server demo
TARGET_HOST = "howsmyssl.com"
TARGET_PORT = 443

# Danh sách mã băm SHA-256 ghim sẵn (Pinned Certificate Fingerprints) hợp lệ
# Lưu ý: Mã băm này tương ứng với chứng chỉ thực tế của howsmyssl.com tại thời điểm kiểm tra.
VALID_PINNED_HASH = "b136ce2f59d2e3fffafaafc1ad1980271acad95dc6c9197f3b669a0d222a716f"

# Biến giả lập chế độ tấn công Man-in-the-Middle (MITM)
# - False: Kết nối an toàn thông thường, chứng chỉ khớp với Pin -> KẾT NỐI THÀNH CÔNG
# - True: Giả lập kẻ tấn công đứng giữa can thiệp bằng chứng chỉ giả mạo -> KẾT NỐI BỊ CHẶN
MOCK_MITM_ATTACK = False

def simulate_iot_client():
    print("=" * 70)
    print("MÔ PHỎNG THIẾT BỊ IoT XÁC THỰC CERTIFICATE PINNING (MBED TLS PRINCIPLE)")
    print("=" * 70)
    print(f"[*] Đang chuẩn bị kết nối tới: {TARGET_HOST}:{TARGET_PORT}")
    print(f"[*] Trạng thái giả lập tấn công MITM: {'KÍCH HOẠT (MITM Active)' if MOCK_MITM_ATTACK else 'TẮT (Normal)'}")
    print(f"[*] Mã băm chứng chỉ đã ghim (Pinned Hash): {VALID_PINNED_HASH}\n")

    # 1. Khởi tạo ngữ cảnh SSL/TLS
    # Tương đương: mbedtls_ssl_config_defaults() với cấu hình MBEDTLS_SSL_IS_CLIENT
    context = ssl.create_default_context()
    
    # Thiết lập kiểm tra chuỗi chứng chỉ thông thường từ các CA hệ thống
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True

    try:
        # 2. Tạo kết nối TCP Socket thông thường tới Server
        # Tương đương: mbedtls_net_connect()
        raw_socket = socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=10)
        print("[+] Bước 1: Thiết lập kết nối TCP thành công.")

        # 3. Thực hiện quá trình bắt tay TLS (TLS Handshake)
        # Tương đương: mbedtls_ssl_setup() & mbedtls_ssl_handshake()
        ssl_socket = context.wrap_socket(raw_socket, server_hostname=TARGET_HOST)
        print("[+] Bước 2: Bắt tay TLS thành công. Đường truyền đã được mã hóa.")

        # 4. Lấy chứng chỉ X.509 dạng nhị phân DER từ đối tác (Server)
        # Tương đương: mbedtls_ssl_get_peer_cert() trong Mbed TLS
        der_cert = ssl_socket.getpeercert(binary_form=True)
        print(f"[+] Bước 3: Đã tải xuống chứng chỉ X.509 từ Server ({len(der_cert)} bytes).")

        # 5. Tính toán mã băm SHA-256 của chứng chỉ nhận được
        # Tương đương việc sử dụng thư viện Crypto của Mbed TLS: mbedtls_sha256()
        received_cert_hash = hashlib.sha256(der_cert).hexdigest()
        print(f"[+] Bước 4: Mã băm SHA-256 chứng chỉ thực tế: {received_cert_hash}")

        # 6. Thực hiện so khớp ghim chứng chỉ (Certificate Pinning Verification)
        # Trong Mbed TLS, logic này được thực thi trong hàm callback đăng ký bởi mbedtls_ssl_conf_verify()
        print("[*] Bước 5: Tiến hành đối chiếu mã băm chứng chỉ (Pinning Check)...")
        
        # Nếu đang bật chế độ giả lập tấn công MITM, ta thay đổi mã băm của server hoặc ghim sai
        expected_pin = VALID_PINNED_HASH
        if MOCK_MITM_ATTACK:
            # Giả lập kẻ tấn công đưa ra chứng chỉ giả mạo có mã băm hoàn toàn khác
            print("[!] CẢNH BÁO: Đang giả lập MITM. Kẻ tấn công trình chứng chỉ giả!")
            expected_pin = "0000000000000000000000000000000000000000000000000000000000000000" # mã băm giả lập của attacker

        if received_cert_hash == expected_pin:
            print("[OK] XÁC THỰC THÀNH CÔNG: Mã băm chứng chỉ trùng khớp hoàn toàn!")
            print("[✓] Thiết bị IoT xác nhận Server này là tin cậy và chính chủ.")
            print("[*] Gửi dữ liệu telemetry an toàn...")
            
            # Gửi yêu cầu HTTP đơn giản để kiểm tra kết nối hoạt động
            ssl_socket.sendall(b"GET / HTTP/1.1\r\nHost: howsmyssl.com\r\nConnection: close\r\n\r\n")
            response = ssl_socket.recv(1024)
            print(f"[+] Server phản hồi thành công (đọc được {len(response)} bytes).")
        else:
            # Ngắt kết nối lập tức nếu phát hiện mã băm không khớp
            # Tương đương trong Mbed TLS trả về mã lỗi: MBEDTLS_ERR_X509_CERT_VERIFY_FAILED
            print("[X] LỖI CỰC KỲ NGUY HIỂM: Mã băm chứng chỉ KHÔNG TRÙNG KHỚP với Pin đã ghim!")
            print("    [!] Cảnh báo tấn công Man-in-the-Middle (MITM) hoặc DNS Spoofing!")
            raise ssl.SSLError("VerificationAlert: Certificate Pinning Mismatch! Access Denied.")

    except ssl.SSLError as ssl_err:
        print(f"\n[!] LỖI BẢO MẬT SSL/TLS: {ssl_err}")
        print("[X] Kết nối đã bị ngắt lập tức để bảo vệ dữ liệu thiết bị IoT.")
    except Exception as e:
        print(f"\n[!] Lỗi kết nối mạng: {e}")
    finally:
        try:
            ssl_socket.close()
            print("[*] Đã đóng socket an toàn.")
        except NameError:
            pass
        print("=" * 70 + "\n")

if __name__ == "__main__":
    # Cấu hình hỗ trợ tiếng Việt trên Console Windows
    if sys.platform.startswith('win'):
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # Chạy lần 1: Kết nối thông thường (Normal)
    simulate_iot_client()
    
    # Chạy lần 2: Giả lập tấn công MITM để xem phản ứng ngăn chặn
    MOCK_MITM_ATTACK = True
    simulate_iot_client()
