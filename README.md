# 🌌 LAKHA UNIVERSE TEST

<p align="center">
  <b>⚡ TERMUX MULTI TOOL ⚡</b>
</p>

<p align="center">
  A Termux-based network scanning, server analysis and utility toolkit.
</p>

---

## 📌 About

**LAKHA UNIVERSE TEST** is a Termux Multi Tool designed for network testing, host/domain analysis, server checking and useful Termux utilities.

The tool provides multiple utilities through a simple menu-based interface.

---

## 🛠️ FEATURES

```text
LAKHA UNIVERSE TEST
       TERMUX MULTI TOOL
----------------------------------------------
[01] 🔍 HOST / HTTP SCANNER
[02] ⚡ ULTRA SERVER SCANNER
[03] 🌐 SUBDOMAIN FINDER
[04] 🚪 PORT CHECKER
[05] 🧮 CIDR RANGE GENERATOR
[06] ☁️  CDN / HTTP HEADERS
[07] 📡 RESPONSE MONITOR (SIM)
[08] 🔗 VLESS CONFIG CHECKER
[09] 🖥️  LOCAL VPS / SSH SERVER
[10] 📣 SOCIALS & CHANNELS
[11] 📚 HELP & DOCUMENTATION
[00] ❌ EXIT
----------------------------------------------


---

📥 INSTALLATION

1️⃣ Install Termux packages

Open Termux and run:

pkg update -y
pkg install python git curl -y


---

2️⃣ Install LAKHA UNIVERSE

Run this single command:

curl -fsSL "https://raw.githubusercontent.com/raytsam88-pixel/lakha-universe/main/install.sh" | bash

The installer will automatically download and install the tool.


---

🚀 RUN THE TOOL

After installation, simply type:

lakha

That's it! 🔥

The LAKHA UNIVERSE menu will appear.


---

🔍 HOST / HTTP SCANNER

The Host / HTTP Scanner reads domains or hosts from a TXT file and checks their HTTP/HTTPS responses.

Input file

Place your TXT file here:

/sdcard/A1LAKHA/ULI.txt

After scanning, the tool will ask:

Do you want to save results to SD Card? (y/n)

If you select:

Y

the results will be saved to:

/sdcard/A1LAKHA/lakha_scan_results.txt

If you select:

N

the results will not be saved.


---

⚡ ULTRA SERVER SCANNER

The Ultra Server Scanner can perform fast connectivity checks on IP addresses or CIDR ranges.

It can be useful for authorized network testing and server troubleshooting.


---

🌐 SUBDOMAIN FINDER

The Subdomain Finder checks common subdomains for a given domain.

Example:

example.com

It can help identify commonly used subdomains during authorized testing.


---

🚪 PORT CHECKER

The Port Checker checks specified ports on a host and reports their availability.

Example:

80
443
8080

Use this only on systems you own or have permission to test.


---

🧮 CIDR RANGE GENERATOR

The CIDR Range Generator helps generate IP addresses from a CIDR network range.

Example:

192.168.1.0/24


---

☁️ CDN / HTTP HEADERS

This utility checks HTTP response headers and displays useful HTTP/CDN-related information.

It can be useful for basic server and website troubleshooting.


---

📡 RESPONSE MONITOR

The Response Monitor can be used to monitor network/HTTP responses and connectivity behaviour.


---

🔗 VLESS CONFIG CHECKER

The VLESS Config Checker provides basic checking functionality for VLESS configurations.

Use configurations only on servers and networks you are authorized to access.


---

🖥️ LOCAL VPS / SSH SERVER

This option provides utilities for setting up and running a local SSH/server environment inside Termux.


---

📂 FILE LOCATION

LAKHA UNIVERSE uses the following directory:

/sdcard/A1LAKHA/

Main scanner input:

/sdcard/A1LAKHA/ULI.txt

Scanner output:

/sdcard/A1LAKHA/lakha_scan_results.txt


---

📱 TERMUX STORAGE PERMISSION

If Termux cannot access your phone storage, run:

termux-setup-storage

Allow the storage permission when Android asks.


---

🔄 UPDATE

To update the tool, reinstall the latest version using:

curl -fsSL "https://raw.githubusercontent.com/raytsam88-pixel/lakha-universe/main/install.sh" | bash

Then run:

lakha


---

❌ UNINSTALL

To remove the lakha command:

rm -f "$PREFIX/bin/lakha"


---

📢 TELEGRAM CHANNEL

🇮🇳 Jamnagar Parivar

Get updates, announcements and other projects here:

👉 https://t.me/tm_jam_nagar


---

👨‍💻 DEVELOPER

LAKHA UNIVERSE

Made for Termux users and network/utility testing.


---

⚠️ DISCLAIMER

LAKHA UNIVERSE TEST is intended for:

Educational purposes

Authorized security testing

Network troubleshooting

Server administration

Testing systems that you own or have permission to test


Do not use this tool to scan, access, attack, or interfere with systems, servers, networks, or services without authorization.

The developer is not responsible for misuse of this tool.


---

⭐ SUPPORT

If you find this project useful, consider giving the repository a ⭐ on GitHub.

LAKHA UNIVERSE TEST — Termux Multi Tool
