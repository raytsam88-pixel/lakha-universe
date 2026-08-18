#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import ssl
import ipaddress
import subprocess
import shutil
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import HTTPConnection, HTTPSConnection

# ============================================================
# LAKHA UNIVERSE TEST - Termux Multi Tool
# Mobile-friendly UI (designed for narrow phone terminals)
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;205m"
TEAL = "\033[38;5;51m"

DEFAULT_FILE = "/sdcard/A1LAKHA/ULI.txt"
OUT_DIR = "/sdcard/A1LAKHA"

C_TITLE = PINK
C_MENU = CYAN
C_SCAN = TEAL
C_CODE = GREEN
C_SERVER = MAGENTA
C_PORT = YELLOW
C_IP = BLUE
C_HOST = WHITE
C_INFO = CYAN
C_OK = GREEN
C_WARN = YELLOW
C_ERR = RED
C_FILE = ORANGE


def clear():
    os.system("clear")


def banner():
    clear()
    print(PINK + BOLD + "        LAKHA UNIVERSE TEST" + RESET)
    print(TEAL + BOLD + "          TERMUX MULTI TOOL" + RESET)
    print(DIM + "----------------------------------------------" + RESET)


def pause():
    input(YELLOW + "\nPress ENTER to continue..." + RESET)


def section(title, color):
    print()
    print(color + BOLD + f"[ {title} ]" + RESET)
    print(DIM + "-" * 46 + RESET)


def clean_host(value):
    value = value.strip()
    if not value or value.startswith("#"):
        return ""
    if "://" in value:
        value = urlparse(value).hostname or value
    value = value.strip().split("/")[0]
    if value.count(":") == 1:
        left, right = value.rsplit(":", 1)
        if right.isdigit():
            value = left
    return value.strip()


def read_hosts(path):
    out = []
    seen = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            host = clean_host(line)
            if host and host not in seen:
                seen.add(host)
                out.append(host)
    return out


def short(text, width):
    text = str(text or "-")
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[:width - 3] + "..."


def color_code(code):
    if 200 <= code < 300:
        return GREEN
    if 300 <= code < 400:
        return YELLOW
    if 400 <= code < 500:
        return ORANGE
    if code >= 500:
        return RED
    return WHITE


def http_check(host, port, method="GET", timeout=3):
    try:
        ip = socket.gethostbyname(host)
        if port in (443, 8443, 9443):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            conn = HTTPSConnection(host, port, timeout=timeout, context=ctx)
        else:
            conn = HTTPConnection(host, port, timeout=timeout)

        conn.request(method, "/", headers={
            "Host": host,
            "User-Agent": "LAKHA-UNIVERSE-TEST/1.0",
            "Connection": "close",
        })
        response = conn.getresponse()
        headers = {k.lower(): v for k, v in response.getheaders()}
        result = {
            "host": host,
            "ip": ip,
            "port": port,
            "method": method,
            "code": response.status,
            "server": headers.get("server", "-"),
        }
        conn.close()
        return result
    except Exception:
        return None


def print_table_row(r):
    method = short(r["method"], 6).ljust(6)
    code = str(r["code"]).rjust(3)
    server = short(r["server"], 14).ljust(14)
    port = str(r["port"]).rjust(4)
    ip = short(r["ip"], 15).ljust(15)
    host = short(r["host"], 25)

    print(
        C_SCAN + method + RESET + "  "
        + color_code(r["code"]) + code + RESET + "  "
        + C_SERVER + server + RESET + "  "
        + C_PORT + port + RESET + "  "
        + C_IP + ip + RESET + "  "
        + C_HOST + host + RESET
    )


def host_scanner():
    banner()
    section("01  HOST / HTTP SCANNER", C_SCAN)

    print(C_INFO + f"TXT file path [ENTER={DEFAULT_FILE}]: " + RESET, end="")
    path = input().strip() or DEFAULT_FILE

    if not os.path.isfile(path):
        print(C_ERR + f"File not found: {path}" + RESET)
        pause()
        return

    try:
        hosts = read_hosts(path)
    except Exception as e:
        print(C_ERR + f"Read error: {e}" + RESET)
        pause()
        return

    total_domains = len(hosts)
    if not total_domains:
        print(C_ERR + "No domains found in TXT." + RESET)
        pause()
        return

    ports_text = input(C_PORT + "Ports [ENTER=80,443]: " + RESET).strip()
    if not ports_text:
        ports = [80, 443]
    else:
        try:
            ports = [int(x.strip()) for x in ports_text.split(",") if 1 <= int(x.strip()) <= 65535]
        except ValueError:
            print(C_ERR + "Invalid ports." + RESET)
            pause()
            return

    method = input(C_SCAN + "HTTP method [GET]: " + RESET).strip().upper() or "GET"
    timeout = max(1.0, min(float(input(C_SCAN + "Timeout seconds [3]: " + RESET).strip() or "3"), 15.0))
    workers = max(1, min(int(input(C_SCAN + "Threads [10]: " + RESET).strip() or "10"), 30))

    jobs = [(h, p) for h in hosts for p in ports]
    total = len(jobs)

    print(C_INFO + f"\nTargets: {total_domains} | Jobs: {total}" + RESET)
    input(GREEN + "Press ENTER to START..." + RESET)

    scanned = 0
    shown = 0
    all_http = 0
    results = []

    print()
    print(C_SCAN + "Method" + RESET + "  " + C_CODE + "Cd" + RESET + "  " + C_SERVER + "Server" + RESET + "          " + C_PORT + "Port" + RESET + "  " + C_IP + "IP" + RESET + "          " + C_HOST + "Host" + RESET)
    print(DIM + "------  --  --------------  ----  ---------------  -------------------------" + RESET)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(http_check, h, p, method, timeout): (h, p) for h, p in jobs}

        for future in as_completed(futures):
            scanned += 1
            try:
                r = future.result()
            except Exception:
                r = None

            if r is not None:
                all_http += 1
                if r["code"] != 302:
                    results.append(r)
                    shown += 1
                    print_table_row(r)

            percent = (scanned * 100) / total if total > 0 else 100
            bar_len = 22
            filled_len = int(bar_len * scanned // total) if total > 0 else bar_len
            bar_filled = PINK + "█" * filled_len + RESET
            bar_empty = DIM + "─" * (bar_len - filled_len) + RESET
            print(f"\r{CYAN}Progress: [{bar_filled}{bar_empty}] {percent:.1f}% ({scanned}/{total}){RESET}", end="", flush=True)

    print("\n")
    print(C_OK + f"Scan Done! Total Scanned: {scanned}/{total} | Successful: {all_http} | Displayed: {shown}" + RESET)

    # Save prompt Y/N
    save_choice = input(YELLOW + "Do you want to save results to SD Card? (y/n) [y]: " + RESET).strip().lower()
    if save_choice != 'n':
        default_out = os.path.join(OUT_DIR, "lakha_scan_results.txt")
        os.makedirs(os.path.dirname(default_out), exist_ok=True)
        try:
            with open(default_out, "w", encoding="utf-8") as f:
                f.write("LAKHA UNIVERSE TEST - HOST SCANNER RESULTS\n" + "="*45 + "\n")
                for r in results:
                    f.write(f"Method: {r['method']} | Code: {r['code']} | Server: {r['server']} | Port: {r['port']} | IP: {r['ip']} | Host: {r['host']}\n")
            print(C_FILE + f"✓ Successfully saved at: {default_out}" + RESET)
        except Exception as e:
            print(C_ERR + f"Save error: {e}" + RESET)
    else:
        print(C_WARN + "Result saving skipped by user." + RESET)

    pause()


def ultra_server_scanner():
    banner()
    section("⚡ ULTRA SERVER SCANNER", TEAL)
    print(C_MENU + "[1] CIDR Scan" + RESET)
    print(C_MENU + "[2] IP File" + RESET)
    print(C_MENU + "[3] Back to Menu" + RESET)
    
    choice = input(CYAN + "Select > " + RESET).strip()
    
    if choice == "1":
        ports_text = input(C_PORT + "Ports (default 80,443) > " + RESET).strip()
        ports = [int(p.strip()) for p in ports_text.split(",")] if ports_text else [80, 443]
        
        threads = int(input(C_SCAN + "TCP Threads (500): " + RESET).strip() or 500)
        timeout = float(input(C_SCAN + "TCP Timeout (2): " + RESET).strip() or 2.0)
        cidr_input = input(C_FILE + "CIDR > " + RESET).strip()
        
        try:
            net = ipaddress.ip_network(cidr_input, strict=False)
            ips = [str(ip) for ip in net.hosts()]
            total_ips = net.num_addresses
        except ValueError as e:
            print(C_ERR + f"Invalid CIDR: {e}" + RESET)
            pause()
            return
            
    elif choice == "2":
        path = input(C_FILE + f"IP File path [ENTER={DEFAULT_FILE}] > " + RESET).strip() or DEFAULT_FILE
        if not os.path.isfile(path):
            print(C_ERR + f"File not found: {path}" + RESET)
            pause()
            return
        ips = read_hosts(path)
        total_ips = len(ips)
        ports_text = input(C_PORT + "Ports (default 80,443) > " + RESET).strip()
        ports = [int(p.strip()) for p in ports_text.split(",")] if ports_text else [80, 443]
        threads = int(input(C_SCAN + "TCP Threads (500): " + RESET).strip() or 500)
        timeout = float(input(C_SCAN + "TCP Timeout (2): " + RESET).strip() or 2.0)
    else:
        return

    jobs = [(ip, p) for ip in ips for p in ports]
    total = len(jobs)
    
    print(C_INFO + f"Total Targets: {total}" + RESET)
    input(GREEN + "Press ENTER to START Scan..." + RESET)
    print()

    scanned = 0
    results = []

    def check_target(ip, port):
        try:
            if port in (443, 8443, 9443):
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                conn = HTTPSConnection(ip, port, timeout=timeout, context=ctx)
            else:
                conn = HTTPConnection(ip, port, timeout=timeout)

            conn.request("GET", "/", headers={
                "Host": ip,
                "User-Agent": "Mozilla/5.0",
                "Connection": "close"
            })
            resp = conn.getresponse()
            server_header = resp.getheader("Server", "Unknown")
            status_code = resp.status
            conn.close()
            return ip, port, status_code, server_header
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_target, ip, p): (ip, p) for ip, p in jobs}
        
        for future in as_completed(futures):
            scanned += 1
            res = future.result()
            if res:
                ip_addr, port_num, code, srv = res
                if code != 302:
                    results.append((ip_addr, port_num, code, srv))
                    print(GREEN + f"✓ {ip_addr}:{port_num} [{code}] {srv}" + RESET)

            percent = (scanned * 100) / total if total > 0 else 100
            bar_len = 22
            filled_len = int(bar_len * scanned // total) if total > 0 else bar_len
            bar_filled = PINK + "█" * filled_len + RESET
            bar_empty = DIM + "─" * (bar_len - filled_len) + RESET
            print(f"\r{CYAN}Progress: [{bar_filled}{bar_empty}] {percent:.1f}% ({scanned}/{total}){RESET}", end="", flush=True)

    print(C_OK + f"\n\nScan completed successfully!" + RESET)
    
    save_choice = input(YELLOW + "Do you want to save Ultra Server scan results? (y/n) [y]: " + RESET).strip().lower()
    if save_choice != 'n':
        default_out = os.path.join(OUT_DIR, "lakha_server_results.txt")
        os.makedirs(os.path.dirname(default_out), exist_ok=True)
        try:
            with open(default_out, "w", encoding="utf-8") as f:
                f.write("LAKHA UNIVERSE TEST - ULTRA SERVER SCANNER\n" + "="*45 + "\n")
                for ip_addr, port_num, code, srv in results:
                    f.write(f"IP: {ip_addr} | Port: {port_num} | Code: {code} | Server: {srv}\n")
            print(C_FILE + f"✓ Saved to: {default_out}" + RESET)
        except Exception as e:
            print(C_ERR + f"Save error: {e}" + RESET)

    pause()


def subdomain_finder():
    banner()
    section("SUBDOMAIN FINDER", GREEN)
    domain = clean_host(input("Domain: "))
    if not domain:
        print(C_ERR + "Domain required." + RESET)
        pause()
        return

    names = ["www", "api", "app", "mail", "cdn", "static", "media", "blog", "shop", "portal", "login", "dev", "test"]
    found = []
    for n in names:
        host = f"{n}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            found.append((host, ip))
            print(GREEN + f"✓ {host} -> {ip}" + RESET)
        except socket.gaierror:
            pass
    print(GREEN + f"\nFound: {len(found)}" + RESET)
    pause()


def port_checker():
    banner()
    section("PORT CHECKER", RED)
    host = clean_host(input("Domain/IP: "))
    if not host:
        print(C_ERR + "Host required." + RESET)
        pause()
        return
    text = input("Ports [80,443,8080,8443]: ").strip()
    ports = [int(x.strip()) for x in (text or "80,443,8080,8443").split(",") if x.strip().isdigit()]
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(C_ERR + "DNS resolution failed." + RESET)
        pause()
        return
    print(BLUE + f"IP: {ip}" + RESET)
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        ok = s.connect_ex((ip, p)) == 0
        s.close()
        print((GREEN + "OPEN " if ok else RED + "CLOSED ") + str(p))
    pause()


def cidr_generator():
    banner()
    section("CIDR RANGE GENERATOR", MAGENTA)
    cidr = input("CIDR (example 1.0.0.0/24): ").strip()
    out_file = input("Output filename [cidr_ips.txt]: ").strip() or "cidr_ips.txt"
    out = os.path.join(OUT_DIR, out_file)
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            for ip in net.hosts():
                f.write(str(ip) + "\n")
        print(GREEN + f"✓ {net.num_addresses} addresses saved to {out}" + RESET)
    except Exception as e:
        print(C_ERR + f"Error: {e}" + RESET)
    pause()


def cdn_checker():
    banner()
    section("CDN / HTTP HEADERS", CYAN)
    host = clean_host(input("Domain: "))
    if not host:
        print(C_ERR + "Domain required." + RESET)
        pause()
        return

    for port in (443, 80):
        r = http_check(host, port, "HEAD", 4)
        if r:
            print(CYAN + f"Port: {port} | Code: {r['code']} | Server: {r['server']} | IP: {r['ip']}" + RESET)
            server = r["server"].lower()
            hints = []
            if "cloudflare" in server: hints.append("Cloudflare")
            if "vercel" in server: hints.append("Vercel")
            if "nginx" in server: hints.append("nginx")
            if "apache" in server: hints.append("Apache")
            print(MAGENTA + "Detected: " + RESET + (", ".join(hints) if hints else "No obvious CDN header"))
            break
    else:
        print(RED + "No HTTP(S) response." + RESET)
    pause()


def local_ssh_server():
    banner()
    section("LOCAL VPS / SSH SERVER", GREEN)
    print(C_INFO + "Configures and runs local Dropbear/OpenSSH server on Termux." + RESET)
    port = input("Local SSH port [8022]: ").strip() or "8022"
    
    if input("Initialize keys and start sshd now? (y/n): ").strip().lower() == "y":
        # Check if host keys exist, generate if not
        if not os.path.exists(os.path.expanduser("~/.ssh/ssh_host_rsa_key")):
            print(YELLOW + "Generating SSH host keys..." + RESET)
            os.system("ssh-keygen -A")
        
        # Kill existing sshd if running and start new
        os.system("pkill sshd 2>/dev/null")
        result = os.system(f"sshd -p {port}")
        if result == 0:
            print(GREEN + f"✓ SSH server successfully started on port {port}!" + RESET)
            print(CYAN + f"Connect using: ssh localhost -p {port}" + RESET)
        else:
            print(RED + "✗ Failed to start SSH server. Try running 'pkg install openssh' first." + RESET)
    pause()


def telegram_channels():
    banner()
    section("COMMUNITY & SOCIALS", PINK)
    
    links = [
        ("𝐉𝐚𝐦𝐧𝐚𝐠𝐚𝐫 𝐏𝐚𝐫𝐢𝐯𝐚𝐫", "https://t.me/tm_jam_nagar"),
        ("𝐁𝐀𝐂𝐊 +99 𝐂𝐎𝐌𝐌𝐔𝐍𝐈𝐓𝐘", "https://t.me/lakharathod444"),
        ("𝑰𝒏𝒔𝒊𝒅𝒆 𝑫𝒘𝒂𝒓𝒌𝒂", "https://t.me/lakha53"),
        ("𝙇𝘼𝙆𝙃𝘼 𝙍𝘼𝙏𝙃𝙊𝘿", "https://t.me/lakha_991"),
        ("Back+99❤️", "https://t.me/back_P9"),
        ("Gujarat tiger TM", "https://t.me/b_99v2"),
        ("Gujarati Dost 🇮🇳 (WhatsApp)", "https://whatsapp.com/channel/0029VbAPatSLY6cxmGbrP636"),
        ("LAKHA RATHOD INSTA", "https://www.instagram.com/nobita_boy_50k?igsh=NWxlZ2xnZTdubzQy&igsi=NWxlZ2xnZTdubzQy")
    ]
    
    for i, (name, url) in enumerate(links, 1):
        print(f"[{i}] {PINK}{BOLD}{name}{RESET}")
        print(f"    {CYAN}{url}{RESET}")
    
    print("\n" + YELLOW + "Kisi bhi link ko open karne ke liye uska number dalein (Ya 0 dabayein wapas jane ke liye):" + RESET)
    choice = input(CYAN + "Choice > " + RESET).strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(links):
            target_url = links[idx][1]
            print(GREEN + f"Opening: {target_url}" + RESET)
            if shutil.which("termux-open-url"):
                os.system(f"termux-open-url '{target_url}'")
            else:
                print(YELLOW + "Termux-tools missing. Link copy kar le bhai ya browser me khole." + RESET)
            pause()


def packet_capture_sim():
    banner()
    section("RESPONSE MONITOR (SIMULATION)", TEAL)
    print(CYAN + "Local activity simulator running..." + RESET)
    try:
        for n in range(1, 11):
            time.sleep(0.3)
            print(TEAL + f"[{n:02}] response-event local-check-{n}.example" + RESET)
    except KeyboardInterrupt:
        pass
    pause()


def vless_validator():
    banner()
    section("VLESS CONFIG CHECKER", MAGENTA)
    link = input("\nVLESS link: ").strip()
    try:
        p = urlparse(link)
        if p.scheme.lower() == "vless":
            print(GREEN + f"✓ Valid VLESS Host: {p.hostname} | Port: {p.port}" + RESET)
        else:
            print(RED + "✗ Not a valid VLESS link." + RESET)
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
    pause()


def help_docs():
    banner()
    section("📚 HELP & DOCUMENTATION", YELLOW)
    print(CYAN + BOLD + "Welcome to LAKHA UNIVERSE TEST - Termux Multi Tool!\n" + RESET)
    print(WHITE + "Yeh tool network scanning, server analysis, aur automation ke liye design kiya gaya hai.\n" + RESET)
    
    print(GREEN + BOLD + "[How to use - Guide]:" + RESET)
    print(WHITE + "1. **Host / HTTP Scanner ([01])**: Yeh option aapke TXT file se domains/hosts read karta hai.")
    print(f"   - Default input file yahan honi chahiye: {ORANGE}{DEFAULT_FILE}{WHITE}")
    print(f"   - Scan ke baad aapko prompt milega: '{YELLOW}Do you want to save results to SD Card? (y/n){WHITE}'")
    print(f"   - Agar aap {GREEN}Y{WHITE} select karoge, toh file yahan save hogi:")
    print(f"     {ORANGE}/sdcard/A1LAKHA/lakha_scan_results.txt{WHITE}")
    print(f"   - Agar {RED}N{WHITE} karoge toh save skip ho jayegi.\n")
    
    print(GREEN + BOLD + "[Other Features]:" + RESET)
    print(WHITE + "- **Ultra Server Scanner ([02])**: CIDR ya IP file par fast TCP/HTTP check chalata hai.")
    print(WHITE + "- **Subdomain Finder ([03])**: Kisi bhi domain ke common subdomains find karta hai.")
    print(WHITE + "- **Port Checker ([04])**: Specific host ke open/closed ports check karta hai.")
    print(WHITE + "- **Local VPS / SSH ([09])**: Termux par local SSH server setup aur run karta hai.")
    print(CYAN + "\nSabhi files /sdcard/A1LAKHA/ folder ke andar store hoti hain." + RESET)
    pause()


def menu():
    while True:
        banner()
        print(CYAN + BOLD + "[01] 🔍 HOST / HTTP SCANNER" + RESET)
        print(TEAL + BOLD + "[02] ⚡ ULTRA SERVER SCANNER" + RESET)
        print(GREEN + BOLD + "[03] 🌐 SUBDOMAIN FINDER" + RESET)
        print(RED + BOLD + "[04] 🚪 PORT CHECKER" + RESET)
        print(MAGENTA + BOLD + "[05] 🧮 CIDR RANGE GENERATOR" + RESET)
        print(CYAN + BOLD + "[06] ☁️  CDN / HTTP HEADERS" + RESET)
        print(YELLOW + BOLD + "[07] 📡 RESPONSE MONITOR (SIM)" + RESET)
        print(PINK + BOLD + "[08] 🔗 VLESS CONFIG CHECKER" + RESET)
        print(GREEN + BOLD + "[09] 🖥️  LOCAL VPS / SSH SERVER" + RESET)
        print(PINK + BOLD + "[10] 📣 SOCIALS & CHANNELS" + RESET)
        print(ORANGE + BOLD + "[11] 📚 HELP & DOCUMENTATION" + RESET)
        print(RED + BOLD + "[00] ❌ EXIT" + RESET)

        choice = input(CYAN + "\nSelect option: " + RESET).strip().lower()

        if choice in ("1", "01"):
            host_scanner()
        elif choice in ("2", "02"):
            ultra_server_scanner()
        elif choice in ("3", "03"):
            subdomain_finder()
        elif choice in ("4", "04"):
            port_checker()
        elif choice in ("5", "05"):
            cidr_generator()
        elif choice in ("6", "06"):
            cdn_checker()
        elif choice in ("7", "07"):
            packet_capture_sim()
        elif choice in ("8", "08"):
            vless_validator()
        elif choice in ("9", "09"):
            local_ssh_server()
        elif choice in ("10",):
            telegram_channels()
        elif choice in ("11",):
            help_docs()
        elif choice in ("0", "00", "q", "quit", "exit"):
            print(GREEN + "Bye bhai 👋" + RESET)
            break
        else:
            print(RED + "Invalid option." + RESET)
            time.sleep(0.7)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n" + YELLOW + "Stopped by user." + RESET)
    except Exception as e:
        print("\n" + RED + f"Unexpected error: {e}" + RESET)
