# 💥 YUAN's DDoS Controller

**Educational Purpose Only | YUAN WAS HERE - NO SYSTEM IS SAFE**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Educational-red)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/MiYuan-dev/DDoS.github.io)](https://github.com/MiYuan-dev/DDoS.github.io/commits/main)

A powerful, educational DDoS attack controller with a web interface. This tool demonstrates various network attack methodologies for **learning and authorized testing only**. It features a sleek terminal-style UI, multiple attack methods, and real-time attack statistics.

**⚠️ IMPORTANT DISCLAIMER:** This tool is for **EDUCATIONAL PURPOSES ONLY**. Unauthorized use of this tool against systems you do not own or have explicit written permission to test is ILLEGAL and UNETHICAL. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---

## ✨ Features

- 🎯 **Multiple Attack Methods**: UDP Flood, TCP Flood, HTTP Flood, SYN Flood, ICMP Flood, Slowloris
- 🌐 **Web-Based Control**: User-friendly terminal-style web interface
- 🔐 **Simple Authentication**: Basic login to access the control panel
- 📊 **Real-Time Statistics**: Live updates on packets sent, rate, elapsed time, and progress bar
- 📝 **Live Attack Log**: Displays real-time events and errors
- 🧵 **Multi-Threading**: Configurable thread count for attack intensity
- 🖥️ **Standalone Server**: Built-in Python HTTP server, no external web server needed

---

## 📁 Project Structure

```
DDoS.github.io/
├── yuan_web_controller.py      # Main Python application (HTTP server + attack engine)
├── ddos.html                   # Frontend HTML/CSS/JavaScript interface
└── README.md                   # Documentation
```

---

🚀 Quick Start Guide

Prerequisites

· Python 3.6 or higher
· Git (optional)

Installation & Setup

```bash
# Clone the repository
git clone https://github.com/MiYuan-dev/DDoS.github.io.git
cd DDoS.github.io

# Run the controller
python yuan_web_controller.py
```

Expected Output

```
╔═══════════════════════════════════════════════════════════════════════╗
║              YUAN'S WEB DDOS CONTROLLER - v3.0                        ║
║              Control attacks from web interface                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                    ⚠️  EDUCATIONAL PURPOSE ONLY  ⚠️                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Web Interface: http://localhost:8080                                 ║
║  API Endpoint:  http://localhost:8080/api                             ║
╚═══════════════════════════════════════════════════════════════════════╝

[✓] Starting web server on port 8080
[!] Open http://localhost:8080 in your browser
[!] Press Ctrl+C to stop
```

Access the Interface

1. Open your browser
2. Navigate to http://localhost:8080
3. Login with credentials:
   · Username: yuan
   · Password: yuan

Launch an Attack

1. Enter target (e.g., 192.168.1.1:80)
2. Select attack method
3. Configure threads and duration
4. Click 🚀 START ATTACK
5. Monitor real-time statistics
6. Click 🛑 STOP to halt

---

📱 Termux (Android) Instructions

Install Termux

Download from F-Droid: https://f-droid.org/en/packages/com.termux/

Setup Commands

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/MiYuan-dev/DDoS.github.io.git
cd DDoS.github.io
python yuan_web_controller.py
```

Access from Browser

· Local: http://localhost:8080
· Network: http://<YOUR_IP>:8080 (find IP with ifconfig)

---

🌐 Network Access

To access from other devices on the same network:

```bash
# Find your IP address
ip addr show  # Linux/Termux
ifconfig      # macOS/Linux
ipconfig      # Windows
```

Then from another device: http://<YOUR_IP>:8080

---

⚙️ Configuration

Edit yuan_web_controller.py to modify:

```python
WEB_PORT = 8080          # Web interface port
MAX_THREADS = 5000       # Maximum attack threads
YUAN_MESSAGES = [...]    # Customize messages
```

---

🔧 Advanced Usage

Custom Port

```bash
# Edit the port in script
sed -i 's/WEB_PORT = 8080/WEB_PORT = 9090/' yuan_web_controller.py
python yuan_web_controller.py
```

Run in Background

```bash
nohup python yuan_web_controller.py > server.log 2>&1 &
tail -f server.log
```

Multiple Instances

```bash
cp yuan_web_controller.py instance2.py
# Edit port in instance2.py
python instance2.py
```

---

⚠️ Legal & Ethical Warning

THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY.

· ❌ Do NOT use against systems you don't own
· ❌ Do NOT use without explicit written permission
· ❌ Unauthorized DDoS attacks are ILLEGAL
· ⚠️ Violators face severe legal consequences

By using this software, you agree to take full responsibility for your actions.

---

🛠️ Troubleshooting

Issue Solution
ddos.html not found Ensure file is in same directory as script
Port 8080 in use Change WEB_PORT in script
Connection refused Verify server is running
SYN/ICMP fails Requires root privileges
No stats updating Check API at http://localhost:8080/api/status
Termux killed Disable battery optimization

---

📜 License

Educational use only. Not for commercial or malicious purposes.

---

🤝 Contributing

Contributions for educational improvements are welcome. Malicious modifications will be rejected.

1. Fork the repository
2. Create feature branch
3. Submit pull request

---

📞 Support

· GitHub Issues: https://github.com/MiYuan-dev/DDoS.github.io/issues
· Include device info and error details

---

🙏 Acknowledgments

· Built with Python standard library
· Terminal-style UI design
· Educational security community

---

YUAN WAS HERE - NO SYSTEM IS SAFE

With great power comes great responsibility. Use ethically.

---

Last updated: March 2026
