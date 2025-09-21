import requests
import time
import sys
import os
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# ANSI colors cầu vồng (dùng colorama để chắc chắn hiển thị mọi terminal)
RAINBOW = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.WHITE,
]

CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
RESET = Style.RESET_ALL

endpoint = "https://api.tqxmg.dpdns.org/buffviewtik"

# Banner tool
print(f"""{CYAN}
==============================
 🚀 TOOL BUFF VIEW TIKTOK
 🔰 Powered by TQXMG
==============================
{RESET}""")

# Hàm mở link rút gọn vt.tiktok.com
def expand_vt_link(url):
    if "vt.tiktok.com" in url:
        try:
            resp = requests.get(url, timeout=5)
            return resp.url
        except Exception:
            return url
    return url

# Hàm lưu số giây còn lại vào file
def save_remaining_seconds(seconds):
    expire_time = datetime.now() + timedelta(hours=6)
    with open("remain.txt", "w") as f:
        f.write(f"{seconds}\n{expire_time.timestamp()}")
    print(f"{YELLOW}⏳ Số giây còn lại đã lưu vào remain.txt, sẽ tự động xóa sau 6 giờ.{RESET}")

# Hàm load số giây còn lại từ file
def load_remaining_seconds():
    if os.path.exists("remain.txt"):
        with open("remain.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 2:
                seconds = int(lines[0])
                expire_timestamp = float(lines[1])
                if datetime.now().timestamp() <= expire_timestamp:
                    return seconds
                else:
                    os.remove("remain.txt")
    return 0

# Hàm xóa file nếu quá 6 giờ
def cleanup_file():
    if os.path.exists("remain.txt"):
        with open("remain.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 2:
                expire_timestamp = float(lines[1])
                if datetime.now().timestamp() > expire_timestamp:
                    os.remove("remain.txt")
                    print(f"{CYAN}🗑️ File remain.txt đã hết hạn và đã xóa.{RESET}")

# Progress bar cầu vồng sống động
def rainbow_progress_bar(seconds):
    bar_length = 30
    for i in range(seconds, 0, -1):
        done = seconds - i
        filled = int(bar_length * done / seconds)
        bar = ""
        for j in range(bar_length):
            color = RAINBOW[(j + int(time.time()*10)) % len(RAINBOW)]
            bar += color + ("█" if j < filled else "-") + RESET
        sys.stdout.write(f"\r[{bar}] {i}s còn lại")
        sys.stdout.flush()
        time.sleep(1)
    print()  # xuống dòng

# Kiểm tra file cũ
cleanup_file()

# Nhập link
url = input("🔗 Nhập URL TikTok: ").strip()
url = expand_vt_link(url)

MAX_PER_SEND = 100
MAX_TOTAL = 2000
total_sent = 0

# Tự động load số giây còn lại nếu có
remaining_from_file = load_remaining_seconds()
if remaining_from_file > 0:
    print(f"{CYAN}⏳ Bạn còn {remaining_from_file} giây chưa gửi từ lần trước.{RESET}")
    while True:
        cont = input("🔄 Bạn có muốn tiếp tục buff phần còn lại không? (y/n): ").strip().lower()
        if cont in ("y", "yes"):
            total_sent = MAX_TOTAL - remaining_from_file
            print(f"{CYAN}🚀 Tiếp tục buff {remaining_from_file} giây...{RESET}")
            break
        elif cont in ("n", "no"):
            remaining_from_file = 0
            break
        else:
            print(f"{YELLOW}⚠️  Vui lòng nhập y (có) hoặc n (không).{RESET}")

while total_sent < MAX_TOTAL:
    remain = MAX_TOTAL - total_sent
    print(f"\nTổng thời gian còn lại có thể gửi: {remain} giây")
    
    # Nhập TIME
    while True:
        try:
            time_delay = int(input(f"⏱️  Nhập TIME cho lần gửi (≤ {MAX_PER_SEND} giây): ").strip())
            if 1 <= time_delay <= MAX_PER_SEND:
                if time_delay > remain:
                    print(f"{YELLOW}⚠️  Chỉ còn {remain} giây có thể gửi, vui lòng nhập nhỏ hơn hoặc bằng {remain}.{RESET}")
                    continue
                break
            else:
                print(f"{YELLOW}⚠️  Chỉ được nhập từ 1 đến {MAX_PER_SEND} giây mỗi lần.{RESET}")
        except:
            print(f"{YELLOW}⚠️  Nhập số nguyên hợp lệ nhé.{RESET}")
    
    total_sent += time_delay
    print(f"{CYAN}🚀 Gửi API với {time_delay} giây...{RESET}")
    params = {"url": url, "time": time_delay}
    try:
        requests.get(endpoint, params=params, timeout=4)
    except:
        pass

    rainbow_progress_bar(time_delay)
    
    print(f"{GREEN}✅ Hoàn thành lần gửi!{RESET}")

    if total_sent >= MAX_TOTAL:
        print(f"\n{CYAN}🎉 Đã đạt tổng thời gian tối đa 1000 giây, không thể gửi thêm.{RESET}")
        break

    # Hỏi có tiếp tục buff không
    while True:
        cont = input("🔄 Bạn có muốn buff thêm không? (y/n): ").strip().lower()
        if cont in ("y", "yes"):
            break
        elif cont in ("n", "no"):
            remain = MAX_TOTAL - total_sent
            if remain > 0:
                save_remaining_seconds(remain)
            total_sent = MAX_TOTAL  # dừng vòng lặp
            break
        else:
            print(f"{YELLOW}⚠️  Vui lòng nhập y (có) hoặc n (không).{RESET}")

# Pháo hoa ASCII cầu vồng
fireworks = [
    "      *       ",
    "     ***      ",
    "    *****     ",
    "   *******    ",
    "    *****     ",
    "     ***      ",
    "      *       ",
]
for line in fireworks:
    color = RAINBOW[int(time.time()*10) % len(RAINBOW)]
    print(f"{color}{line}{RESET}")
    time.sleep(0.1)

print(f"\n{CYAN}🎉 Cảm ơn đã sử dụng TOOL TQXMG!{RESET}")
