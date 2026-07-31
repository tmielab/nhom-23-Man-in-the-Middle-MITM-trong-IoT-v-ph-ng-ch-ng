# DE TAI 23: MAN-IN-THE-MIDDLE (MITM) TRONG IOT VÀ PHÒNG CHỐNG

**Học phần:** BẢO MẬT IoT (INT4410) — TRƯỜNG ĐẠI HỌC VĂN HIẾN  
**Sinh viên thực hiện:** Lương Thị Thanh Thanh (MSSV: 231A010377)  
**Email GitHub:** nissluu@gmail.com / luongthanhthanh14082005@gmail.com  
**Repository Official Link:** [https://github.com/tmielab/nhom-23-Man-in-the-Middle-MITM-trong-IoT-v-ph-ng-ch-ng](https://github.com/tmielab/nhom-23-Man-in-the-Middle-MITM-trong-IoT-v-ph-ng-ch-ng)  

---

## 1. GIỚI THIỆU ĐỀ TÀI & TỔNG QUAN HỆ THỐNG

Tấn công **Man-in-the-Middle (MitM - Kẻ đứng giữa)** là kỹ thuật tấn công phổ biến và nguy hiểm nhất trong môi trường Internet of Things (IoT). Kẻ tấn công lợi dụng điểm yếu không mã hóa của giao thức MQTT truyền thống (cổng 1883) và bản chất thiếu cơ chế xác thực nguồn gốc của giao thức ARP để độc hóa bảng ARP Cache (ARP Poisoning), điều hướng luồng dữ liệu truyền thông đi qua máy tấn công (Kali Linux).

Đề tài triển khai **Mô hình Phòng thủ Nhiều lớp (Defense-in-Depth)** kết hợp giữa an ninh hạ tầng Tầng 2 và mã hóa xác thực hai chiều Tầng Kênh truyền/Ứng dụng:
1. **Lớp Hạ tầng (Layer 2):** Cấu hình tính năng Dynamic ARP Inspection (DAI) & DHCP Snooping trên Cisco Virtual Switch để phát hiện và hủy bỏ (drop) 100% các gói tin ARP Reply giả mạo.
2. **Lớp Kênh truyền & Ứng dụng:** Chuyển dịch sang Mosquitto Broker cổng 8883, mã hóa mTLS toàn trình với chuỗi chứng chỉ X.509 (OpenSSL PKI), bắt buộc xác thực hai chiều (`require_certificate true`) và áp dụng chính sách phân quyền đặc quyền tối thiểu (ACL).

---

## 2. CẤU TRÚC KHO LƯU TRỮ (REPOSITORY TREE)

```text
nhom-23-repo/
├── README.md               # Hướng dẫn chi tiết hệ thống, kịch bản & kết quả thực nghiệm
├── setup_and_push.py       # Script tự động hóa đồng bộ & push lên GitHub
├── generate_demo_images.py # Script sinh 15 hình ảnh demo chuẩn theo mẫu - Copy.docx
├── AnhTest/                # Thư mục chứa toàn bộ 15 hình ảnh demo tên theo hình x.x...
├── certs/                  # Chuỗi chứng chỉ X.509 (ca.crt, server.crt, client.crt, private keys)
├── configs/                # Tệp cấu hình an toàn
│   ├── mosquitto.conf      # Cấu hình Mosquitto Broker hỗ trợ cổng 1883 & 8883 mTLS
│   ├── aclfile.txt         # Phân quyền truy cập Topic MQTT theo nguyên tắc POLP
│   ├── password.txt        # Tệp mật khẩu tài khoản người dùng đã hash
│   └── cisco_switch.cfg    # Cấu hình Layer 2 Security (DAI & DHCP Snooping)
├── data/                   # Dữ liệu mẫu JSON (payload_sample.json)
├── pcap/                   # Tệp vết bắt gói tin Wireshark (.pcap)
├── report/                 # Báo cáo tiểu luận chi tiết (.docx và .pdf)
├── results/                # Kết quả thực nghiệm và log đối chứng
│   ├── logs/               # Tệp nhật ký mqtt_log.txt ghi nhận dữ liệu Subscriber
│   └── screenshots/        # Ảnh chụp minh chứng kịch bản TC-01 đến TC-06
├── references/             # Danh mục tài liệu tham khảo (OWASP, Mbed TLS, Mosquitto)
└── src/                    # Mã nguồn Python thực nghiệm
    ├── code_demo.py        # Script chạy tự động toàn bộ 6 kịch bản kiểm thử (TC-01 -> TC-06)
    ├── mqtt_pub.py         # Client Publisher gửi dữ liệu cảm biến (Hỗ trợ 1883 & 8883 mTLS)
    ├── mqtt_sub.py         # Client Subscriber tiếp nhận dữ liệu & ghi nhật ký mqtt_log.txt
    └── mitm_attack.py      # Script mô phỏng ARP Poisoning & Packet Tampering
```

---

## 3. MA TRẬN 6 KỊCH BẢN KIỂM THỬ (TEST CASES TC-01 -> TC-06)

| ID Kịch bản | Mô tả kịch bản | Đầu vào / Hành vi | Kết quả kỳ vọng | Kết quả thực tế & Đối chiếu |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Luồng kết nối Plaintext Cổng 1883 | Publisher gửi gói tin JSON qua cổng 1883 | **ACCEPT** (Bình thường nhưng không có mã hóa) | **ACCEPT** — 100% gói tin truyền thành công (Plaintext) |
| **TC-02** | Tấn công MitM & Packet Tampering | Kali Linux thực thi arpspoof & Wireshark trace | **ATTACK SUCCESSFUL** (Lọt lộ & sai lệch JSON) | **THÀNH CÔNG** — Đọc lén 100% & sửa nhiệt độ thành 99.9°C |
| **TC-03** | Phòng thủ Layer 2 (DAI & DHCP Snooping) | Kali phát 50 gói ARP Reply giả mạo vào vSwitch | **CHẶN THÀNH CÔNG** (Cisco Switch drop gói ARP) | **CHẶN THÀNH CÔNG** — 0 gói ARP độc hại lọt qua Switch |
| **TC-04** | Phòng thủ mTLS Kết nối hợp lệ Cổng 8883 | Client gửi kèm `client.crt` & `client.key` | **ACCEPT** (Bắt tay mTLS thành công, Encrypted) | **ACCEPT** — Mã hóa TLS 1.3 toàn trình, Độ trễ 18.4 ms |
| **TC-05** | Phòng thủ mTLS Thiếu Certificate | Client kết nối cổng 8883 nhưng thiếu cert | **REJECT** (Broker ngắt kết nối tại Handshake) | **REJECT** — Từ chối kết nối tuyệt đối 100% |
| **TC-06** | Phòng thủ Ứng dụng Phân quyền ACL | Dashboard cố tình Publish lên `iot/sensor/temp` | **REJECT / CHẶN** (Broker từ chối thao tác ghi) | **REJECT** — Mã lỗi 128 Unauthorized, chặn 100% |

---

## 4. HƯỚNG DẪN CHẠY THỰC NGHIỆM VÀ KIỂM THỬ HỆ THỐNG

### 4.1. Khởi chạy toàn bộ 6 Kịch bản Kiểm thử tự động (Auto Test Suite)
```bash
python src/code_demo.py
```

### 4.2. Sinh toàn bộ 15 Hình ảnh minh chứng chuẩn theo file mẫu
```bash
python generate_demo_images.py
```
*Tất cả hình ảnh minh chứng sẽ được tự động lưu vào thư mục `AnhTest/` và `results/screenshots/` theo đúng tên `hình x.x.....` quy định.*

### 4.3. Khởi chạy Publisher & Subscriber thủ công qua Cổng 8883 mTLS
**Terminal 1 — Subscriber (Dashboard Node):**
```bash
python src/mqtt_sub.py --port 8883 --cafile certs/ca.crt --cert certs/client.crt --key certs/client.key
```

**Terminal 2 — Publisher (IoT Sensor Node):**
```bash
python src/mqtt_pub.py --port 8883 --cafile certs/ca.crt --cert certs/client.crt --key certs/client.key
```

---

## 5. DANH MỤC HÌNH ẢNH DEMO TRONG THƯ MỤC ANHTEST

1. **Hình 2.1:** `Hình 2.1. Sơ đồ kiến trúc bối cảnh hệ thống IoT, ranh giới tin cậy và vị trí nguy cơ tấn công Man-in-the-Middle (MitM).png`
2. **Hình 3.1:** `Hình 3.1. Quy trình thực hiện đề tài nghiên cứu tấn công Man-in-the-Middle và giải pháp phòng thủ nhiều lớp cho hệ thống IoT.png`
3. **Hình 3.2:** `Hình 3.2. Mô hình kiến trúc kiểm thử tấn công MitM và hệ thống phòng thủ nhiều lớp cho IoT.png`
4. **Hình 4.1:** `Hình 4.1. Môi trường triển khai Mosquitto Broker hỗ trợ đa cổng (1883 & 8883 mTLS) vận hành trên máy ảo VMware Workstation.png`
5. **Hình 4.2:** `Hình 4.2. Sinh chuỗi chứng chỉ số X.509 mã hóa hai chiều bằng OpenSSL.png`
6. **Hình 4.3:** `Hình 4.3. Nội dung cấu hình kiểm soát an ninh Layer 2 trên Cisco Virtual Switch.png`
7. **Hình 4.4:** `Hình 4.4. Nội dung cấu hình lắng nghe mTLS bảo mật trên tệp mosquitto.conf.png`
8. **Hình 4.5:** `Hình 4.5. Thiết lập chính sách phân quyền tối thiểu (Least Privilege) trong aclfile.txt.png`
9. **Hình 4.6:** `Hình 4.6. Wireshark bắt trọn gói tin MQTT chưa mã hóa chứa nội dung JSON nhạy cảm.png`
10. **Hình 4.7:** `Hình 4.7. Kẻ tấn công thực thi ARP Poisoning và can thiệp làm sai lệch dữ liệu (Packet Tampering).png`
11. **Hình 4.8:** `Hình 4.8. Cisco Switch phát hiện và hủy bỏ gói tin ARP giả mạo ngay tại Layer 2.png`
12. **Hình 4.9:** `Hình 4.9. Publisher kết nối mTLS thành công qua cổng 8883.png`
13. **Hình 4.10:** `Hình 4.10. Wireshark bắt gói tin qua cổng 8883: Toàn bộ dữ liệu bị mã hóa hoàn toàn.png`
14. **Hình 4.11:** `Hình 4.11. Broker từ chối kết nối do Client không cung cấp chứng chỉ mTLS hợp lệ.png`
15. **Hình 4.12:** `Hình 4.12. Subscriber tiếp nhận dữ liệu an toàn và tự động ghi tệp nhật ký mqtt_log.txt.png`

---

## 6. KẾT LUẬN & ĐÁNH GIÁ ĐỊNH LƯỢNG

- **Tính Bảo mật (Confidentiality):** 100% dữ liệu qua cổng 8883 được mã hóa mTLS X.509, giảm tỷ lệ rò rỉ Plaintext về **0%**.
- **Tính Toàn vẹn (Integrity):** Đạt **100%** bảo toàn thông điệp, triệt tiêu hoàn toàn rủi ro Packet Tampering.
- **Tính Khả dụng (Availability) & Hiệu năng:** Độ trễ truyền thông trung bình duy trì ở mức **18.4 ms** (tiêu chuẩn < 100 ms), chênh lệch độ trễ do mTLS và DAI chỉ tăng ~29.5%, đáp ứng tối ưu cho truyền thông IoT.
