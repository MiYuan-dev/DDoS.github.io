💥 YUAN's DDoS Controller

Educational Purpose Only | YUAN WAS HERE - NO SYSTEM IS SAFE

https://img.shields.io/badge/python-3.6%2B-blue
https://img.shields.io/badge/license-Educational-red
https://img.shields.io/github/last-commit/MiYuan-dev/DDoS.github.io

A powerful, educational DDoS attack controller with a web interface. This tool demonstrates various network attack methodologies for learning and authorized testing only. It features a sleek terminal-style UI, multiple attack methods, and real-time attack statistics.

⚠️ IMPORTANT DISCLAIMER: This tool is for EDUCATIONAL PURPOSES ONLY. Unauthorized use of this tool against systems you do not own or have explicit written permission to test is ILLEGAL and UNETHICAL. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---

✨ Features

· 🎯 Multiple Attack Methods: UDP Flood, TCP Flood, HTTP Flood, SYN Flood, ICMP Flood, Slowloris
· 🌐 Web-Based Control: User-friendly terminal-style web interface
· 🔐 Simple Authentication: Basic login to access the control panel
· 📊 Real-Time Statistics: Live updates on packets sent, rate, elapsed time, and progress bar
· 📝 Live Attack Log: Displays real-time events and errors
· 🧵 Multi-Threading: Configurable thread count for attack intensity
· 🖥️ Standalone Server: Built-in Python HTTP server, no external web server needed
· 📱 Termux Compatible: Runs perfectly on Android devices using Termux

---

📁 Project Structure

```
DDoS.github.io/
├── yuan_web_controller.py      # Main Python application (HTTP server + attack engine)
├── ddos.html                   # Frontend HTML/CSS/JavaScript interface
└── README.md                   # This documentation file
```

---

🚀 How to Use (Step-by-Step Guide for Termux/Android)

Prerequisites

· Android device with Termux installed
· Internet connection

Step 1: Install Termux

Download Termux from F-Droid: https://f-droid.org/en/packages/com.termux/

Step 2: Install Python

```bash
pkg update && pkg upgrade -y
pkg install python -y
```

Step 3: Get the Code

```bash
pkg install git -y
git clone https://github.com/MiYuan-dev/DDoS.github.io.git
cd DDoS.github.io
```

Step 4: Run the Controller

```bash
python yuan_web_controller.py
```

Expected output:

```
[✓] Starting web server on port 8080
[!] Open http://localhost:8080 in your browser
[!] Press Ctrl+C to stop
```

Step 5: Access the Web Interface

1. Keep Termux running in the background
2. Open Chrome/Firefox on your Android device
3. Go to: http://localhost:8080

Step 6: Log In

· Username: yuan
· Password: yuan

Step 7: Launch an Attack

1. Enter target (e.g., 192.168.1.1:80) - ⚠️ Only attack systems you own!
2. Select attack method
3. Set threads (50-100 for Termux)
4. Set duration (seconds)
5. Click 🚀 START ATTACK
6. Monitor statistics in real-time
7. Click 🛑 STOP to halt

Step 8: Stop the Server

Press Ctrl+C in Termux

---

📱 Access from Other Devices

1. Find your Android IP: ifconfig or ip addr show
2. From another device: http://<YOUR_IP>:8080

---

⚙️ Configuration

Edit yuan_web_controller.py to change:

```python
WEB_PORT = 8080          # Change if port is busy
MAX_THREADS = 5000       # Reduce for low-end devices
```

---

⚠️ Legal Warning

THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY. Unauthorized DDoS attacks are ILLEGAL and can result in severe penalties. Only use on systems you own or have explicit permission to test.

---

🛠️ Troubleshooting

Problem Solution
ddos.html not found Ensure both files are in same directory
Port 8080 in use Change WEB_PORT in the script
Connection refused Make sure server is running
SYN/ICMP fail Use UDP/TCP/HTTP methods instead (root required for raw sockets)
Termux killed Disable battery optimization for Termux

---

YUAN WAS HERE - NO SYSTEM IS SAFE
