# -*- coding: utf-8 -*-
"""
Script tự động hóa thiết lập cấu trúc Repository và quản lý Git.
Đặt tại: D:\\IoT\\gitmd\\git\\setup_and_push.py
Thực hiện các nhiệm vụ:
1. Tạo cây thư mục trống theo quy chuẩn giảng viên.
2. Di chuyển/đảm bảo code_demo.py nằm đúng vị trí trong src/.
3. Sinh file references/link_nguon.md liệt kê các nguồn tài liệu.
4. Chạy Git init, add, commit và push lên remote repo.
"""

import os
import shutil
import subprocess
import sys

# Đảm bảo đầu ra console hỗ trợ UTF-8 cho tiếng Việt trên Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Đường dẫn thư mục làm việc hiện tại của Repository
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run_command(args, cwd=REPO_DIR):
    """Hàm bổ trợ để chạy lệnh hệ thống và trả về kết quả."""
    try:
        # Dùng shell=True trên Windows để tránh lỗi phân giải đường dẫn phần mềm trong PATH
        use_shell = sys.platform.startswith('win')
        result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=use_shell)
        return result.stdout.strip(), None
    except FileNotFoundError:
        return "", "Không tìm thấy chương trình thực thi. Vui lòng cài đặt Git và cấu hình biến môi trường PATH."
    except subprocess.CalledProcessError as e:
        return e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else f"Lỗi thực thi với mã thoát: {e.returncode}"

def create_directory_structure():
    print("[*] Bước 1: Khởi tạo cấu trúc thư mục quy chuẩn...")
    
    # Định nghĩa cấu trúc cây thư mục cần tạo
    dirs_to_create = [
        "report",
        "slides",
        "src",
        "configs",
        "data",
        os.path.join("results", "screenshots"),
        os.path.join("results", "logs"),
        "references"
    ]
    
    for d in dirs_to_create:
        path = os.path.join(REPO_DIR, d)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"  [+] Đã tạo thư mục: {d}")
        else:
            print(f"  [.] Thư mục đã tồn tại: {d}")
    print("[✓] Hoàn thành khởi tạo thư mục.\n")

def manage_code_demo():
    print("[*] Bước 2: Kiểm tra và di chuyển code_demo.py vào thư mục src/...")
    src_file = os.path.join(REPO_DIR, "code_demo.py")
    dest_file = os.path.join(REPO_DIR, "src", "code_demo.py")
    
    # Trường hợp file nằm ngoài thư mục gốc, di chuyển vào src/
    if os.path.exists(src_file) and not os.path.exists(dest_file):
        shutil.move(src_file, dest_file)
        print("  [+] Đã di chuyển code_demo.py vào src/code_demo.py")
    elif os.path.exists(dest_file):
        print("  [.] File code_demo.py đã nằm đúng vị trí trong src/")
    else:
        print("  [!] Không tìm thấy code_demo.py ở thư mục gốc hay src/. Vui lòng tạo lại file.")
    print("[✓] Hoàn thành quản lý file nguồn.\n")

def generate_references_file():
    print("[*] Bước 3: Đang tự động tạo file references/link_nguon.md...")
    ref_path = os.path.join(REPO_DIR, "references", "link_nguon.md")
    
    content = """# Danh sách nguồn tài liệu tham khảo - Đề tài 23: MITM trong IoT

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
"""
    try:
        with open(ref_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [+] Đã tạo file thành công tại references/link_nguon.md")
    except Exception as e:
        print(f"  [X] Lỗi khi tạo file: {e}")
    print("[✓] Hoàn thành sinh tài liệu tham khảo.\n")

def automate_git():
    print("[*] Bước 4: Tự động hóa quy trình Git...")
    
    # Kiểm tra xem Git có được cài đặt và cấu hình PATH hay không
    stdout, stderr = run_command(["git", "--version"])
    if stderr or not stdout:
        print("\n[!] CẢNH BÁO BẢO TRÌ: Không tìm thấy lệnh 'git' trong hệ thống.")
        print("    - Vui lòng cài đặt Git từ trang chủ: https://git-scm.com/")
        print("    - Đảm bảo đã tích chọn 'Add Git to PATH' trong quá trình cài đặt trên Windows.")
        print("    - Bạn cần khởi động lại Terminal hoặc VS Code sau khi cài đặt để cập nhật biến môi trường.")
        print("    - Cấu trúc thư mục và tài liệu tham khảo đã được tạo hoàn thành cục bộ.\n")
        return

    print(f"  [.] Tìm thấy: {stdout}")

    # 1. Kiểm tra Git repo
    git_dir = os.path.join(REPO_DIR, ".git")
    if not os.path.exists(git_dir):
        print("  [*] Khởi tạo Git repository mới...")
        stdout, stderr = run_command(["git", "init"])
        if stderr:
            print(f"  [X] Lỗi khởi tạo Git: {stderr}")
            return
        print("  [+] Đã khởi tạo Git repository.")
    else:
        print("  [.] Đã là một Git repository tồn tại.")

    # 2. Thực hiện git add
    print("  [*] Đang chạy 'git add .'...")
    stdout, stderr = run_command(["git", "add", "."])
    if stderr:
        print(f"  [!] Cảnh báo khi git add: {stderr}")
    else:
        print("  [+] Đã thêm toàn bộ file vào Staging Area.")

    # 3. Thực hiện git commit
    print("  [*] Đang thực hiện commit...")
    commit_msg = "Feat: Initialize required repo structure and code_demo for 25% progress"
    stdout, stderr = run_command(["git", "commit", "-m", commit_msg])
    if stderr and "nothing to commit" in stdout.lower():
        print("  [.] Repo không có thay đổi nào mới để commit.")
    elif stderr:
        # Nếu git config chưa được thiết lập (thiếu user.email, user.name), git commit sẽ báo lỗi
        if "user.email" in stderr or "user.name" in stderr:
            print("\n[!] LỖI CẤU HÌNH GIT: Bạn chưa cấu hình thông tin định danh Git (Name/Email).")
            print("    Vui lòng chạy các lệnh sau trong terminal để thiết lập:")
            print("      git config --global user.email \"email_cua_ban@example.com\"")
            print("      git config --global user.name \"Ten Cua Ban\"")
            print("    Sau đó chạy lại script này.\n")
            return
        print(f"  [!] Cảnh báo/Lỗi commit: {stderr}")
    else:
        print(f"  [+] Đã commit thành công với thông điệp:\n      \"{commit_msg}\"")

    # 4. Đẩy code lên Remote Repository
    print("  [*] Đang kiểm tra cấu hình Remote...")
    remotes_out, stderr = run_command(["git", "remote", "-v"])
    
    if not remotes_out:
        print("  [!] Chưa tìm thấy Remote Repository (origin) nào được cấu hình.")
        print("  >>> Vui lòng nhập URL Remote Repository trên GitHub của bạn.")
        print("  >>> Ví dụ: https://github.com/username/ten-repo.git")
        print("  >>> (Nhấn Enter để bỏ qua nếu bạn chưa muốn đẩy code lên lúc này)")
        
        try:
            remote_url = input("URL Remote Repository: ").strip()
        except (KeyboardInterrupt, EOFError):
            remote_url = ""
            print()
            
        if remote_url:
            stdout, stderr = run_command(["git", "remote", "add", "origin", remote_url])
            if stderr:
                print(f"  [X] Lỗi khi thêm remote: {stderr}")
                return
            print(f"  [+] Đã thiết lập remote 'origin' hướng tới: {remote_url}")
        else:
            print("  [.] Bỏ qua thiết lập remote. Quá trình tự động hóa Git hoàn tất cục bộ.")
            return
    else:
        print(f"  [.] Tìm thấy remote được cấu hình:\n{remotes_out}")

    # Lấy tên branch hiện tại
    branch_name, stderr = run_command(["git", "branch", "--show-current"])
    if not branch_name or stderr:
        branch_name = "main" # default fallback
    
    print(f"  [*] Đang đẩy code lên remote '{branch_name}'...")
    stdout, stderr = run_command(["git", "push", "-u", "origin", branch_name])
    if stderr and "error" in stderr.lower():
        print(f"  [X] Lỗi khi đẩy code lên remote: {stderr}")
        print("  [!] Gợi ý: Hãy kiểm tra quyền truy cập GitHub SSH/HTTPS hoặc kiểm tra xem repo remote đã có commit khác chưa.")
    else:
        print(f"  [✓] Đã đẩy code thành công lên GitHub nhánh '{branch_name}'!")
        if stdout:
            print(f"      Chi tiết: {stdout}")

if __name__ == "__main__":
    print("======================================================================")
    print(" BẮT ĐẦU TỰ ĐỘNG HÓA THIẾT LẬP REPO & ĐẨY CODE (TIẾN ĐỘ 25%)")
    print("======================================================================\n")
    
    create_directory_structure()
    manage_code_demo()
    generate_references_file()
    automate_git()
    
    print("======================================================================")
    print(" HOÀN THÀNH QUY TRÌNH TỰ ĐỘNG HÓA.")
    print("======================================================================")
