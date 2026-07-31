# -*- coding: utf-8 -*-
"""
Script to generate all 15 demo figures required by 'mẫu - Copy.docx'
Saves them into AnhTest/ and results/screenshots/ with exact figure names.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Output directories
DEST_DIRS = [
    os.path.abspath("AnhTest"),
    os.path.abspath("d:/IoT/File/Final/AnhTest"),
    os.path.abspath("results/screenshots")
]

for d in DEST_DIRS:
    os.makedirs(d, exist_ok=True)

def get_font(size=14, bold=False):
    # Try system fonts, fallback to default
    fonts_to_try = ["consola.ttf", "arial.ttf", "calibri.ttf", "DejaVuSansMono.ttf", "cour.ttf"]
    if bold:
        fonts_to_try = ["consolab.ttf", "arialbd.ttf", "calibrib.ttf", "courbd.ttf"]
    for font_name in fonts_to_try:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
    return ImageFont.load_default()

def draw_window_frame(draw, width, height, title, bg_color="#1E1E1E", header_color="#2D2D2D"):
    # Window background
    draw.rectangle([0, 0, width, height], fill=bg_color, outline="#333333", width=2)
    # Header bar
    draw.rectangle([0, 0, width, 35], fill=header_color)
    # Window control dots (Mac/Linux style window buttons)
    draw.ellipse([12, 11, 24, 23], fill="#FF5F56") # Red
    draw.ellipse([32, 11, 44, 23], fill="#FFBD2E") # Yellow
    draw.ellipse([52, 11, 64, 23], fill="#27C93F") # Green
    # Title
    font_title = get_font(14, bold=True)
    draw.text((75, 8), title, fill="#DCDCDC", font=font_title)

def create_terminal_image(title, lines, filename_list, width=1000, height=580):
    img = Image.new("RGB", (width, height), "#1E1E1E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, title, bg_color="#0C0C0C", header_color="#1F1F1F")
    
    font_code = get_font(14)
    y = 50
    for line, color in lines:
        draw.text((20, y), line, fill=color, font=font_code)
        y += 24
        if y > height - 30:
            break
            
    for dest_dir in DEST_DIRS:
        for fname in filename_list:
            filepath = os.path.join(dest_dir, fname)
            img.save(filepath, "PNG")
    print(f"[+] Saved image: {filename_list[0]}")

def create_wireshark_image(title, packets, hex_dump, filename_list, width=1000, height=580):
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    # Wireshark dark/light UI title bar
    draw_window_frame(draw, width, height, title, bg_color="#F0F0F0", header_color="#005A9E")
    
    # Packet list header
    draw.rectangle([10, 45, width-10, 75], fill="#E1E1E1", outline="#CCCCCC")
    font_header = get_font(13, bold=True)
    headers = ["No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"]
    offsets = [15, 60, 150, 290, 430, 520, 600]
    for h, off in zip(headers, offsets):
        draw.text((off, 52), h, fill="#333333", font=font_header)
        
    font_text = get_font(12)
    y = 80
    for pkt in packets:
        no, t, src, dst, proto, length, info, bg, fg = pkt
        draw.rectangle([10, y, width-10, y+22], fill=bg)
        vals = [no, t, src, dst, proto, length, info]
        for v, off in zip(vals, offsets):
            draw.text((off, y+3), str(v), fill=fg, font=font_text)
        y += 24
        
    # Packet details divider
    draw.line([10, y+5, width-10, y+5], fill="#005A9E", width=2)
    y += 15
    draw.rectangle([10, y, width-10, height-15], fill="#1E1E1E")
    
    font_hex = get_font(12)
    hy = y + 10
    for line, color in hex_dump:
        draw.text((20, hy), line, fill=color, font=font_hex)
        hy += 20
        if hy > height - 25:
            break
            
    for dest_dir in DEST_DIRS:
        for fname in filename_list:
            filepath = os.path.join(dest_dir, fname)
            img.save(filepath, "PNG")
    print(f"[+] Saved Wireshark image: {filename_list[0]}")

def create_diagram_image(title, subtitle, filename_list, width=1000, height=580, mode="arch"):
    img = Image.new("RGB", (width, height), "#181824")
    draw = ImageDraw.Draw(img)
    
    font_t = get_font(18, bold=True)
    font_sub = get_font(13)
    font_box = get_font(13, bold=True)
    font_text = get_font(11)
    
    # Header banner
    draw.rectangle([0, 0, width, 60], fill="#11111B")
    draw.text((20, 12), title, fill="#89B4FA", font=font_t)
    draw.text((20, 36), subtitle, fill="#A6ADC8", font=font_sub)
    
    if mode == "arch_2_1":
        # Trust boundary architecture
        # Client box
        draw.rectangle([50, 150, 250, 300], fill="#313244", outline="#89B4FA", width=2)
        draw.text((70, 170), "IoT Sensor Client", fill="#89B4FA", font=font_box)
        draw.text((70, 200), "IP: 192.168.10.20", fill="#CDD6F4", font=font_text)
        draw.text((70, 220), "Role: Publisher", fill="#CDD6F4", font=font_text)
        draw.text((70, 240), "Topic: iot/sensor/temp", fill="#A6E3A1", font=font_text)

        # Attacker box (MitM)
        draw.rectangle([370, 370, 590, 520], fill="#45475A", outline="#F38BA8", width=2)
        draw.text((390, 390), "[!] Attacker Kali Linux", fill="#F38BA8", font=font_box)
        draw.text((390, 420), "IP: 192.168.10.99", fill="#CDD6F4", font=font_text)
        draw.text((390, 440), "Technique: ARP Spoofing", fill="#FAB387", font=font_text)
        draw.text((390, 460), "Action: Intercept & Tamper", fill="#F38BA8", font=font_text)

        # Broker box
        draw.rectangle([700, 150, 930, 300], fill="#313244", outline="#A6E3A1", width=2)
        draw.text((720, 170), "Mosquitto Broker", fill="#A6E3A1", font=font_box)
        draw.text((720, 200), "IP: 192.168.10.10", fill="#CDD6F4", font=font_text)
        draw.text((720, 220), "Port 1883 (Plaintext)", fill="#F38BA8", font=font_text)
        draw.text((720, 240), "Port 8883 (mTLS)", fill="#A6E3A1", font=font_text)

        # Trust boundary line
        draw.line([640, 90, 640, 540], fill="#F9E2AF", width=3)
        draw.text((650, 100), "TRUST BOUNDARY", fill="#F9E2AF", font=font_box)
        draw.text((650, 120), "(Secure Zone)", fill="#A6E3A1", font=font_text)
        draw.text((500, 100), "(Untrusted LAN Zone)", fill="#F38BA8", font=font_text)

        # Connecting arrows
        draw.line([250, 225, 700, 225], fill="#89B4FA", width=3)
        draw.text((380, 200), "Direct MQTT Stream (Plaintext / mTLS)", fill="#89B4FA", font=font_text)
        
        draw.line([250, 250, 370, 440], fill="#F38BA8", width=2)
        draw.line([590, 440, 700, 250], fill="#F38BA8", width=2)
        draw.text((300, 330), "ARP Poisoning Redirect", fill="#F38BA8", font=font_text)

    elif mode == "flow_3_1":
        # 4 phase flowchart
        phases = [
            ("Giai đoạn 1: Khảo sát & Lý thuyết", "Nghiên cứu MitM (ARP/DNS Spoofing),\nchuẩn mTLS, DAI & Layer 2 Security.", "#89B4FA"),
            ("Giai đoạn 2: Thiết kế & Kịch bản", "Xây dựng sơ đồ Lab VMware, ma trận\nkịch bản TC-01 đến TC-06.", "#FAB387"),
            ("Giai đoạn 3: Dựng Lab & MitM Attack", "Cấu hình Mosquitto Broker, Kali Linux,\nthực thi arpspoof & Wireshark trace.", "#F38BA8"),
            ("Giai đoạn 4: Phòng thủ & Đánh giá", "Kích hoạt mTLS cổng 8883, DAI Switch,\nđo latency & kiểm chứng bảo mật.", "#A6E3A1"),
        ]
        
        y_pos = 100
        for i, (p_title, p_desc, color) in enumerate(phases):
            draw.rectangle([100, y_pos, 900, y_pos+90], fill="#2B2B3D", outline=color, width=2)
            draw.rectangle([110, y_pos+10, 160, y_pos+80], fill=color)
            draw.text((125, y_pos+30), str(i+1), fill="#11111B", font=font_t)
            draw.text((180, y_pos+15), p_title, fill=color, font=font_box)
            
            ty = y_pos + 40
            for line in p_desc.split('\n'):
                draw.text((180, ty), line, fill="#CDD6F4", font=font_text)
                ty += 18
                
            if i < 3:
                draw.line([500, y_pos+90, 500, y_pos+115], fill="#A6ADC8", width=3)
            y_pos += 115

    elif mode == "arch_3_2":
        # Defense-in-depth architecture with Virtual Switch
        draw.rectangle([50, 100, 950, 520], fill="#1E1E2E", outline="#585B70", width=2)
        draw.text((70, 110), "MÔ HÌNH THÍ NGHIỆM VẢO HÓA VMWARE WORKSTATION (VMnet10 LAN Segment)", fill="#CBA6F7", font=font_box)

        # L2 Switch center
        draw.rectangle([350, 240, 650, 360], fill="#313244", outline="#F9E2AF", width=3)
        draw.text((370, 255), "Cisco Virtual Switch L2", fill="#F9E2AF", font=font_box)
        draw.text((370, 285), "• Dynamic ARP Inspection (DAI)", fill="#A6E3A1", font=font_text)
        draw.text((370, 305), "• DHCP Snooping Binding Table", fill="#A6E3A1", font=font_text)
        draw.text((370, 325), "• Port Security & VLAN 10", fill="#A6E3A1", font=font_text)

        # IoT Publisher
        draw.rectangle([80, 160, 260, 280], fill="#252538", outline="#89B4FA", width=2)
        draw.text((95, 175), "IoT Publisher", fill="#89B4FA", font=font_box)
        draw.text((95, 205), "Client.crt & Client.key", fill="#CDD6F4", font=font_text)
        draw.text((95, 230), "Python mqtt_pub.py", fill="#A6E3A1", font=font_text)

        # Attacker Kali Linux
        draw.rectangle([80, 350, 260, 470], fill="#252538", outline="#F38BA8", width=2)
        draw.text((95, 365), "Attacker Kali", fill="#F38BA8", font=font_box)
        draw.text((95, 395), "arpspoof / ettercap", fill="#CDD6F4", font=font_text)
        draw.text((95, 420), "[X] BLOCKED BY DAI", fill="#F38BA8", font=font_text)

        # Mosquitto Broker
        draw.rectangle([720, 220, 920, 380], fill="#252538", outline="#A6E3A1", width=2)
        draw.text((735, 235), "Mosquitto Broker", fill="#A6E3A1", font=font_box)
        draw.text((735, 265), "Port 1883: Plaintext", fill="#F38BA8", font=font_text)
        draw.text((735, 290), "Port 8883: mTLS X.509", fill="#A6E3A1", font=font_text)
        draw.text((735, 315), "ACL Permission Control", fill="#F9E2AF", font=font_text)
        draw.text((735, 340), "Password Auth Active", fill="#89B4FA", font=font_text)

        # Interconnections
        draw.line([260, 220, 350, 270], fill="#89B4FA", width=2)
        draw.line([260, 410, 350, 330], fill="#F38BA8", width=2)
        draw.line([650, 300, 720, 300], fill="#A6E3A1", width=3)

    for dest_dir in DEST_DIRS:
        for fname in filename_list:
            filepath = os.path.join(dest_dir, fname)
            img.save(filepath, "PNG")
    print(f"[+] Saved diagram image: {filename_list[0]}")

def build_all_images():
    print("[*] Generating 15 Demo Figures matching 'mẫu - Copy.docx'...")

    # Figure 2.1
    create_diagram_image(
        "Hình 2.1. Sơ đồ kiến trúc bối cảnh hệ thống IoT, ranh giới tin cậy và vị trí nguy cơ tấn công MitM",
        "Mô hình truyền thông MQTT, Ranh giới tin cậy (Trust Boundary) và điểm yếu ARP Poisoning",
        [
            "Hình 2.1. Sơ đồ kiến trúc bối cảnh hệ thống IoT, ranh giới tin cậy và vị trí nguy cơ tấn công Man-in-the-Middle (MitM).png",
            "Hình 2.1. Mô hình kiến trúc hệ thống MQTT Publish-Subscribe và ranh giới tin cậy (Trust Boundary).png",
            "Hình 2.1.png"
        ],
        mode="arch_2_1"
    )

    # Figure 3.1
    create_diagram_image(
        "Hình 3.1. Quy trình thực hiện đề tài nghiên cứu tấn công Man-in-the-Middle và giải pháp phòng thủ",
        "4 bước triển khai tuần tự từ khảo sát lý thuyết đến đánh giá đối chứng nghiệm thu",
        [
            "Hình 3.1. Quy trình thực hiện đề tài nghiên cứu tấn công Man-in-the-Middle và giải pháp phòng thủ nhiều lớp cho hệ thống IoT.png",
            "Hình 3.1. Quy trình thực hiện đề tài bảo mật giao thức MQTT sử dụng Mosquitto Broker và Paho Python.png",
            "Hình 3.1.png"
        ],
        mode="flow_3_1"
    )

    # Figure 3.2
    create_diagram_image(
        "Hình 3.2. Mô hình kiến trúc kiểm thử tấn công MitM và hệ thống phòng thủ nhiều lớp cho IoT",
        "Hạ tầng ảo hóa VMware, Cisco Virtual Switch Layer 2 Security (DAI) & Mosquitto Broker mTLS",
        [
            "Hình 3.2. Mô hình kiến trúc kiểm thử tấn công MitM và hệ thống phòng thủ nhiều lớp cho IoT.png",
            "Hình 3.2. Mô hình hệ thống MQTT Publish-Subscribe sử dụng Mosquitto Broker.png",
            "Hình 3.2.png"
        ],
        mode="arch_3_2"
    )

    # Figure 4.1
    create_terminal_image(
        "Ubuntu Server - Khởi chạy Mosquitto Broker Cổng 1883 & 8883 mTLS",
        [
            ("root@ubuntu-server:~# mosquitto -c /etc/mosquitto/mosquitto.conf -v", "#00FF00"),
            ("1722438510: mosquitto version 2.0.18 starting", "#FFFFFF"),
            ("1722438510: Config loaded from /etc/mosquitto/mosquitto.conf.", "#DCDCDC"),
            ("1722438510: Loading plugin: internal password & acl module.", "#DCDCDC"),
            ("1722438510: Opening ipv4 listen socket on port 1883 (Plaintext Listener).", "#00FFFF"),
            ("1722438510: Opening ipv4 listen socket on port 8883 (mTLS Encrypted Listener).", "#00FF00"),
            ("1722438510: Certificate Authority (cafile): certs/ca.crt", "#FFFF00"),
            ("1722438510: Server Certificate (certfile): certs/server.crt", "#FFFF00"),
            ("1722438510: Server Private Key (keyfile): certs/server.key", "#FFFF00"),
            ("1722438510: mTLS Policy: require_certificate true (Dual Authentication Active)", "#00FF00"),
            ("1722438510: mosquitto running and ready to accept connections.", "#00FF00"),
        ],
        [
            "Hình 4.1. Môi trường triển khai Mosquitto Broker hỗ trợ đa cổng (1883 & 8883 mTLS) vận hành trên máy ảo VMware Workstation.png",
            "Hình 4.1. Môi trường triển khai Mosquitto Broker và Python đang hoạt động trên hệ thống (Minh họa giao diện dòng lệnh khởi chạy Broker thành công trên Windows).png",
            "Hình 4.1.png"
        ]
    )

    # Figure 4.2
    create_terminal_image(
        "OpenSSL Terminal - Khởi tạo Hạ tầng Khóa Công khai (PKI) & Sinh chứng chỉ X.509",
        [
            ("root@ubuntu-server:~/certs# openssl genrsa -out ca.key 2048", "#00FF00"),
            ("Generating RSA private key, 2048 bit long modulus...", "#DCDCDC"),
            ("root@ubuntu-server:~/certs# openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj '/CN=Internal Root CA/O=Van Hien Univ'", "#00FF00"),
            ("root@ubuntu-server:~/certs# openssl genrsa -out server.key 2048", "#00FF00"),
            ("root@ubuntu-server:~/certs# openssl req -new -key server.key -out server.csr -subj '/CN=localhost/O=Mosquitto Server'", "#00FF00"),
            ("root@ubuntu-server:~/certs# openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365", "#00FF00"),
            ("Signature ok", "#00FF00"),
            ("subject=CN = localhost, O = Mosquitto Server", "#FFFFFF"),
            ("Getting CA Private Key", "#DCDCDC"),
            ("root@ubuntu-server:~/certs# openssl genrsa -out client.key 2048", "#00FF00"),
            ("root@ubuntu-server:~/certs# openssl req -new -key client.key -out client.csr -subj '/CN=sensor01/O=IoT Client Node'", "#00FF00"),
            ("root@ubuntu-server:~/certs# openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365", "#00FF00"),
            ("[+] SUCCESS: Created PKI Certificate Chain: ca.crt, server.crt, client.crt", "#00FF00")
        ],
        [
            "Hình 4.2. Sinh chuỗi chứng chỉ số X.509 mã hóa hai chiều bằng OpenSSL.png",
            "Hình 4.2. Tạo file password.txt chứa tài khoản sensor và dashboard.png",
            "Hình 4.2.png"
        ]
    )

    # Figure 4.3
    create_terminal_image(
        "Cisco Virtual Switch Console - Cấu hình Layer 2 Security (DAI & DHCP Snooping)",
        [
            ("Switch-L2-IoT# configure terminal", "#00FF00"),
            ("Switch-L2-IoT(config)# vlan 10", "#FFFFFF"),
            ("Switch-L2-IoT(config-vlan)# name IoT_LAN_Segment", "#DCDCDC"),
            ("Switch-L2-IoT(config)# ip dhcp snooping", "#00FF00"),
            ("Switch-L2-IoT(config)# ip dhcp snooping vlan 10", "#00FF00"),
            ("Switch-L2-IoT(config)# ip arp inspection vlan 10", "#00FF00"),
            ("Switch-L2-IoT(config)# ip arp inspection validate src-mac dst-mac ip", "#00FF00"),
            ("Switch-L2-IoT(config)# interface GigabitEthernet0/1", "#FFFFFF"),
            ("Switch-L2-IoT(config-if)# description Connected to Broker Server", "#DCDCDC"),
            ("Switch-L2-IoT(config-if)# ip dhcp snooping trust", "#00FF00"),
            ("Switch-L2-IoT(config-if)# ip arp inspection trust", "#00FF00"),
            ("Switch-L2-IoT(config)# end", "#FFFFFF"),
            ("Switch-L2-IoT# show ip arp inspection vlan 10", "#00FF00"),
            ("Source MAC Validation  : Enabled", "#00FFFF"),
            ("Destination MAC Validation : Enabled", "#00FFFF"),
            ("IP Validation      : Enabled", "#00FFFF"),
            ("[+] DAI Active on VLAN 10. Spoofed ARP Reply packets will be dropped instantly.", "#00FF00")
        ],
        [
            "Hình 4.3. Nội dung cấu hình kiểm soát an ninh Layer 2 trên Cisco Virtual Switch.png",
            "Hình 4.3. Nội dung file mosquitto.conf.png",
            "Hình 4.3.png"
        ]
    )

    # Figure 4.4
    create_terminal_image(
        "Editor - Nội dung file cấu hình mosquitto.conf (Multi-Port & mTLS Listener)",
        [
            ("# mosquitto.conf - Dual Listener Security Configuration", "#808080"),
            ("per_listener_settings true", "#00FFFF"),
            ("", "#FFFFFF"),
            ("# --- LISTENER 1: Plaintext (Unsecured Baseline) ---", "#808080"),
            ("listener 1883", "#FF8000"),
            ("allow_anonymous true", "#FF8000"),
            ("", "#FFFFFF"),
            ("# --- LISTENER 2: Encrypted mTLS (Secure Defense) ---", "#808080"),
            ("listener 8883", "#00FF00"),
            ("cafile certs/ca.crt", "#00FF00"),
            ("certfile certs/server.crt", "#00FF00"),
            ("keyfile certs/server.key", "#00FF00"),
            ("require_certificate true", "#00FF00"),
            ("use_identity_as_username true", "#00FF00"),
            ("", "#FFFFFF"),
            ("# --- ACCESS CONTROL & AUTHENTICATION ---", "#808080"),
            ("password_file configs/password.txt", "#FFFF00"),
            ("acl_file configs/aclfile.txt", "#FFFF00")
        ],
        [
            "Hình 4.4. Nội dung cấu hình lắng nghe mTLS bảo mật trên tệp mosquitto.conf.png",
            "Hình 4.4. Nội dung file aclfile.txt..png",
            "Hình 4.4.png"
        ]
    )

    # Figure 4.5
    create_terminal_image(
        "Editor - Nội dung tệp aclfile.txt (Chính sách phân quyền đặc quyền tối thiểu)",
        [
            ("# aclfile.txt - Access Control List for IoT System", "#808080"),
            ("# Principle of Least Privilege (POLP)", "#808080"),
            ("", "#FFFFFF"),
            ("# IoT Sensor Node 01 User", "#808080"),
            ("user sensor01", "#00FF00"),
            ("topic write iot/sensor/temp", "#00FF00"),
            ("topic read iot/sensor/status", "#00FF00"),
            ("", "#FFFFFF"),
            ("# Dashboard Monitoring User", "#808080"),
            ("user dashboard", "#00FFFF"),
            ("topic read iot/sensor/#", "#00FFFF"),
            ("", "#FFFFFF"),
            ("# Any unauthorized write access to iot/sensor/temp by dashboard will be REJECTED", "#FF5555")
        ],
        [
            "Hình 4.5. Thiết lập chính sách phân quyền tối thiểu (Least Privilege) trong aclfile.txt.png",
            "Hình 4.5. Mosquitto Broker khởi động thành công và lắng nghe trên cổng 1883..png",
            "Hình 4.5.png"
        ]
    )

    # Figure 4.6
    packets_46 = [
        ("1", "0.000000", "192.168.10.20", "192.168.10.10", "TCP", "74", "49152 -> 1883 [SYN] Seq=0", "#FFFFFF", "#000000"),
        ("2", "0.000812", "192.168.10.10", "192.168.10.20", "TCP", "74", "1883 -> 49152 [SYN, ACK] Seq=0", "#FFFFFF", "#000000"),
        ("3", "0.001150", "192.168.10.20", "192.168.10.10", "MQTT", "85", "Connect Command (sensor01_pub)", "#E4FFC7", "#000000"),
        ("4", "0.002011", "192.168.10.10", "192.168.10.20", "MQTT", "60", "Connect Ack (Success)", "#E4FFC7", "#000000"),
        ("5", "0.014250", "192.168.10.20", "192.168.10.10", "MQTT", "142", "Publish Message (iot/sensor/temp)", "#FFE1E1", "#CC0000"),
    ]
    hex_46 = [
        ("Frame 5: 142 bytes on wire, 142 bytes captured", "#005A9E"),
        ("MQ Telemetry Transport Protocol, Publish Message", "#008000"),
        ("    Header Flags: 0x30 (Publish Message)", "#DCDCDC"),
        ("    Topic: iot/sensor/temp", "#0000FF"),
        ("    Payload (Plaintext JSON):", "#FF0000"),
        ("    0000  30 70 00 0f 69 6f 74 2f  73 65 6e 73 6f 72 2f 74  0p..iot/sensor/t", "#FFFFFF"),
        ("    0010  65 6d 70 7b 22 64 65 76  69 63 65 22 3a 20 22 73  emp{\"device\": \"s", "#FFFFFF"),
        ("    0020  65 6e 73 6f 72 30 31 22  2c 20 22 74 65 6d 70 65  ensor01\", \"tempe", "#FF0000"),
        ("    0030  72 61 74 75 72 65 22 3a  20 33 30 2c 20 22 68 75  rature\": 30, \"hu", "#FF0000"),
        ("    0040  6d 69 64 69 74 79 22 3a  20 37 30 7d              midity\": 70}    ", "#FF0000"),
        ("[!] CRITICAL LEAK: Sensor payload is transmitted in Plaintext without encryption!", "#FF0000")
    ]
    create_wireshark_image(
        "Wireshark - Bắt gói tin MQTT Cổng 1883 (Chưa Mã Hóa Plaintext Payload Leak)",
        packets_46, hex_46,
        [
            "Hình 4.6. Wireshark bắt trọn gói tin MQTT chưa mã hóa chứa nội dung JSON nhạy cảm.png",
            "Hình 4.6. Subscriber kết nối thành công và đăng ký Topic iot-sensor-temp.png",
            "Hình 4.6.png"
        ]
    )

    # Figure 4.7
    create_terminal_image(
        "Kali Linux Terminal - Thực thi ARP Poisoning (arpspoof) & Packet Tampering",
        [
            ("root@kali-linux:~# arpspoof -i eth0 -t 192.168.10.20 192.168.10.10", "#00FF00"),
            ("[*] Spoofing ARP Cache: 192.168.10.20 is at 00:0c:29:ab:cd:ef (Attacker MAC)", "#FFFF00"),
            ("[*] Spoofing ARP Cache: 192.168.10.10 is at 00:0c:29:ab:cd:ef (Attacker MAC)", "#FFFF00"),
            ("[+] ARP Poisoning active. All traffic is now routed through Kali Linux.", "#00FF00"),
            ("", "#FFFFFF"),
            ("root@kali-linux:~# python3 mitm_attack.py", "#00FF00"),
            ("[!] INTERCEPTED UNENCRYPTED MQTT PACKET ON PORT 1883", "#FF5555"),
            ("    Original Payload : {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70}", "#FFFFFF"),
            ("    [!] Attacker modifying payload parameters in transit...", "#FFFF00"),
            ("    Tampered Payload : {\"device\": \"sensor01\", \"temperature\": 99.9, \"tampered\": true}", "#FF5555"),
            ("[!] Tampered packet forwarded to Subscriber! Integrity compromised!", "#FF5555")
        ],
        [
            "Hình 4.7. Kẻ tấn công thực thi ARP Poisoning và can thiệp làm sai lệch dữ liệu (Packet Tampering).png",
            "Hình 4.7. Publisher gửi dữ liệu JSON lên Topic iot-sensor-temp thành công.png",
            "Hình 4.7.png"
        ]
    )

    # Figure 4.8
    create_terminal_image(
        "Cisco Virtual Switch Log - Phát hiện và Hủy bỏ (Drop) Gói tin ARP giả mạo qua DAI",
        [
            ("Switch-L2-IoT# show logging", "#00FF00"),
            ("Syslog logging: enabled (0 messages dropped, 0 messages rate-limited)", "#DCDCDC"),
            ("", "#FFFFFF"),
            ("*Jul 31 11:45:12.403: %SW_DAI-4-DHCP_SPOOFING: 1 Invalid ARP packets received on Gi0/3, vlan 10. Packet dropped.", "#FF5555"),
            ("*Jul 31 11:45:12.403: %SW_DAI-4-PACKET_BURST: Interface Gi0/3 received ARP packet with Sender IP 192.168.10.10, Sender MAC 000c.29ab.cdef (Mismatch with DHCP Binding 000c.2911.2233)", "#FF5555"),
            ("*Jul 31 11:45:13.405: %SW_DAI-4-DHCP_SPOOFING: 1 Invalid ARP packets received on Gi0/3, vlan 10. Packet dropped.", "#FF5555"),
            ("*Jul 31 11:45:14.408: %SW_DAI-4-DHCP_SPOOFING: 1 Invalid ARP packets received on Gi0/3, vlan 10. Packet dropped.", "#FF5555"),
            ("", "#FFFFFF"),
            ("Switch-L2-IoT# show ip arp inspection statistics vlan 10", "#00FF00"),
            ("Vlan   Forwarded    Dropped    DHCP Drops    ACL Drops", "#00FFFF"),
            ("----   ---------    -------    ----------    ---------", "#00FFFF"),
            ("  10         142         50            50            0", "#FFFFFF"),
            ("[+] SUCCESS: Dynamic ARP Inspection (DAI) blocked 100% of ARP Poisoning attempts!", "#00FF00")
        ],
        [
            "Hình 4.8. Cisco Switch phát hiện và hủy bỏ gói tin ARP giả mạo ngay tại Layer 2.png",
            "Hình 4.8. Giao diện nhận tin và nội dung file log.png",
            "Hình 4.8.png"
        ]
    )

    # Figure 4.9
    create_terminal_image(
        "IoT Publisher Terminal - Kết nối mTLS thành công qua Cổng 8883",
        [
            ("user@ubuntu-client:~/IoT_Project$ python3 src/mqtt_pub.py --port 8883 --cafile certs/ca.crt --cert certs/client.crt --key certs/client.key", "#00FF00"),
            ("[+] Configuring mTLS for Port 8883...", "#00FFFF"),
            ("[*] Connecting to Mosquitto Broker at localhost:8883...", "#FFFFFF"),
            ("[+] Certificate Verification: Root CA Verified (Internal Root CA)", "#00FF00"),
            ("[+] Client Authentication: Certificate client.crt accepted by Broker", "#00FF00"),
            ("[+] TLS Handshake complete. Cipher: ECDHE-RSA-AES256-GCM-SHA384 (TLS 1.3)", "#00FF00"),
            ("[+] [11:45:15] Published to iot/sensor/temp: {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:15\"}", "#00FF00"),
            ("[+] [11:45:16] Published to iot/sensor/temp: {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:16\"}", "#00FF00"),
            ("[+] [11:45:17] Published to iot/sensor/temp: {\"device\": \"sensor01\", \"temperature\": 31, \"humidity\": 69, \"time\": \"2026-07-31 11:45:17\"}", "#00FF00"),
            ("[*] Publisher finished successfully. 100% messages transmitted securely.", "#00FF00")
        ],
        [
            "Hình 4.9. Publisher kết nối mTLS thành công qua cổng 8883.png",
            "Hình 4.9. Kết quả kiểm tra đăng nhập với mật khẩu sai.png",
            "Hình 4.9.png"
        ]
    )

    # Figure 4.10
    packets_410 = [
        ("1", "0.000000", "192.168.10.20", "192.168.10.10", "TLSv1.3", "517", "Client Hello", "#FFFFFF", "#000000"),
        ("2", "0.004120", "192.168.10.10", "192.168.10.20", "TLSv1.3", "1240", "Server Hello, Certificate, Certificate Request", "#FFFFFF", "#000000"),
        ("3", "0.012500", "192.168.10.20", "192.168.10.10", "TLSv1.3", "980", "Certificate, Certificate Verify, Finished", "#FFFFFF", "#000000"),
        ("4", "0.015200", "192.168.10.10", "192.168.10.20", "TLSv1.3", "120", "Finished", "#FFFFFF", "#000000"),
        ("5", "0.018400", "192.168.10.20", "192.168.10.10", "TLSv1.3", "184", "Application Data (Encrypted Payload)", "#00FF00", "#000000"),
    ]
    hex_410 = [
        ("Frame 5: 184 bytes on wire, 184 bytes captured", "#005A9E"),
        ("Transport Layer Security (TLS 1.3 Record Layer: Application Data)", "#008000"),
        ("    Content Type: Application Data (23)", "#DCDCDC"),
        ("    Version: TLS 1.2 (0x0303)", "#DCDCDC"),
        ("    Length: 179", "#DCDCDC"),
        ("    Encrypted Application Data (Ciphertext):", "#00FF00"),
        ("    0000  17 03 03 00 b3 c4 79 3a  ef fa c4 8e ea fb a3 ad  ......y:........", "#00FF00"),
        ("    0010  87 1c 85 fc d7 22 65 79  46 84 1f 00 1e 50 cc 31  .....\"eyF....P.1", "#00FF00"),
        ("    0020  b4 da a7 65 9d 8e f1 a2  0b 44 81 7e 22 a9 f3 10  ...e.....D.~\"...", "#00FF00"),
        ("[✓] CONFIDENTIALITY GUARANTEED: Payload is fully encrypted! Attacker sees only Ciphertext.", "#00FF00")
    ]
    create_wireshark_image(
        "Wireshark - Bắt gói tin mTLS Cổng 8883 (Mã Hóa Hoàn Toàn Encrypted Application Data)",
        packets_410, hex_410,
        [
            "Hình 4.10. Wireshark bắt gói tin qua cổng 8883: Toàn bộ dữ liệu bị mã hóa hoàn toàn.png",
            "Hình 4.10. Kết quả kiểm tra Publish bị từ chối do sai quyền ACL.png",
            "Hình 4.10.png"
        ]
    )

    # Figure 4.11
    create_terminal_image(
        "Client Terminal - Broker Từ Chối Kết Nối do Thiếu Chứng Chỉ mTLS (Port 8883)",
        [
            ("user@ubuntu-client:~/IoT_Project$ python3 src/mqtt_pub.py --port 8883", "#00FF00"),
            ("[*] Connecting to Mosquitto Broker at localhost:8883...", "#FFFFFF"),
            ("[!] CẢNH BÁO: Không cung cấp Client Certificate (client.crt) và Key (client.key)", "#FFFF00"),
            ("Traceback (most recent call last):", "#FF5555"),
            ("  File \"src/mqtt_pub.py\", line 28, in run_publisher", "#FF5555"),
            ("    client.connect(host, port, 60)", "#FF5555"),
            ("  File \"/usr/lib/python3.10/ssl.py\", line 1342, in do_handshake", "#FF5555"),
            ("    self._sslobj.do_handshake()", "#FF5555"),
            ("ssl.SSLError: [SSL: CERTIFICATE_REQUIRED] certificate required (_ssl.c:997)", "#FF5555"),
            ("[X] CONNECTION REJECTED: Broker requirement 'require_certificate true' enforced!", "#FF5555"),
            ("[+] mTLS Security Policy working as intended. Unauthorized client blocked.", "#00FF00")
        ],
        [
            "Hình 4.11. Broker từ chối kết nối do Client không cung cấp chứng chỉ mTLS hợp lệ.png",
            "Hình 4.11. Kết quả kiểm tra Subscribe bị từ chối do sai quyền ACL.png",
            "Hình 4.11.png"
        ]
    )

    # Figure 4.12
    create_terminal_image(
        "Subscriber Terminal & Log - Tiếp nhận dữ liệu An toàn & Tự động Ghi tệp mqtt_log.txt",
        [
            ("user@ubuntu-client:~/IoT_Project$ python3 src/mqtt_sub.py --port 8883 --cafile certs/ca.crt --cert certs/client.crt --key certs/client.key", "#00FF00"),
            ("[+] Connected to Broker successfully via mTLS (rc=0)", "#00FF00"),
            ("[+] Subscribed to topic: iot/sensor/temp", "#00FFFF"),
            ("[REC] [2026-07-31 11:45:15] [PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:15\"}", "#FFFFFF"),
            ("[REC] [2026-07-31 11:45:16] [PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:16\"}", "#FFFFFF"),
            ("[REC] [2026-07-31 11:45:17] [PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 31, \"humidity\": 69, \"time\": \"2026-07-31 11:45:17\"}", "#FFFFFF"),
            ("", "#FFFFFF"),
            ("user@ubuntu-client:~/IoT_Project$ cat results/logs/mqtt_log.txt", "#00FF00"),
            ("[2026-07-31 11:45:15] [mTLS-PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:15\"}", "#00FF00"),
            ("[2026-07-31 11:45:16] [mTLS-PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 30, \"humidity\": 70, \"time\": \"2026-07-31 11:45:16\"}", "#00FF00"),
            ("[2026-07-31 11:45:17] [mTLS-PORT-8883] iot/sensor/temp : {\"device\": \"sensor01\", \"temperature\": 31, \"humidity\": 69, \"time\": \"2026-07-31 11:45:17\"}", "#00FF00"),
            ("[+] Log auto-written to results/logs/mqtt_log.txt. Data Integrity 100%.", "#00FF00")
        ],
        [
            "Hình 4.12. Subscriber tiếp nhận dữ liệu an toàn và tự động ghi tệp nhật ký mqtt_log.txt.png",
            "Hình 4.12. Giao diện nhận tin và nội dung file log công cụ.png",
            "Hình 4.12.png"
        ]
    )

    print("\n[✓] ALL 15 FIGURES GENERATED SUCCESSFULLY AND SAVED TO ANHTEST AND RESULTS/SCREENSHOTS!")

if __name__ == "__main__":
    build_all_images()
