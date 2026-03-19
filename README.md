# 💥 YUAN's DDoS Controller

**Educational Purpose Only | YUAN WAS HERE - NO SYSTEM IS SAFE**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Educational-red)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/MiYuan-dev/DDoS.github.io)](https://github.com/MiYuan-dev/DDoS.github.io/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/MiYuan-dev/DDoS.github.io?style=social)](https://github.com/MiYuan-dev/DDoS.github.io/stargazers)

A powerful, educational DDoS attack controller with a web interface and command-line support. This tool demonstrates various network attack methodologies for **learning and authorized testing only**. It features a sleek BlackArch Linux-style terminal UI, multiple attack methods, real-time statistics, and full command-line argument support.

**⚠️ IMPORTANT DISCLAIMER:** This tool is for **EDUCATIONAL PURPOSES ONLY**. Unauthorized use of this tool against systems you do not own or have explicit written permission to test is ILLEGAL and UNETHICAL. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---

## 📸 **Screenshot Preview**
![Screenshot_2026-03-18-13-56-21-557_com termux-edit](https://github.com/user-attachments/assets/379181b5-8583-425b-917d-586cbeb22f2b)
## 🌐 **Web Interface**
![Screenshot_2026-03-19-16-19-17-514_com android chrome-edit](https://github.com/user-attachments/assets/22b886ce-1337-43b9-9f63-cb08163eb18c)
![Screenshot_2026-03-19-16-19-50-202_com android chrome-edit](https://github.com/user-attachments/assets/dbc51321-e522-4d34-83c2-aa640191c114)


---

## ✨ **Features**

- 🎯 **Multiple Attack Methods**: UDP Flood, TCP Flood, HTTP Flood, SYN Flood, ICMP Flood, Slowloris
- 🌐 **Web-Based Control**: User-friendly terminal-style web interface (`ddos.html`)
- 🖥️ **Command-Line Interface**: Full argument support (`--port`, `--help`, `--version`)
- 🔐 **Simple Authentication**: Basic login to access the control panel
- 📊 **Real-Time Statistics**: Live updates on packets sent, rate, elapsed time, and progress bar
- 📝 **Live Attack Log**: Displays real-time events and errors
- 🧵 **Multi-Threading**: Configurable thread count for attack intensity
- 🖥️ **Standalone Server**: Built-in Python HTTP server, no external dependencies
- 📱 **Termux Compatible**: Runs perfectly on Android devices
- ☁️ **Cloudflared Support**: Auto-detects and provides tunnel instructions
- 🌍 **Auto IP Detection**: Automatically displays local and public IP addresses
- 🎨 **BlackArch Theme**: Authentic BlackArch Linux styling

---

## 📁 **Project Structure**
```

DDoS.github.io/
├── yuan_web_controller.py      # Main Python application with CLI support
├── ddos.html                   # Frontend HTML/CSS/JavaScript interface
├── usage.txt                   # Complete command guide
└── README.md                   # This documentation

```


---

## 🚀 **Quick Start Guide**

### Prerequisites

- Python 3.6 or higher
- Git (optional)
- Cloudflared (optional, for public tunnels)

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/MiYuan-dev/DDoS.github.io.git
cd DDoS.github.io

# No pip install needed! Uses only Python standard library
```

Basic Usage

```bash
# Run on default port 8080
python yuan_web_controller.py

# Run on custom port
python yuan_web_controller.py --port 9090
python yuan_web_controller.py -p 8080  # Short form

# Show help
python yuan_web_controller.py --help

# Show version
python yuan_web_controller.py --version
```

Expected Output

```
[✓] Attack Engine: Ready
[✓] Local URL:     http://localhost:8080
[✓] Network URL:   http://192.168.1.100:8080
[✓] Public IP:     210.23.162.152
[✓] API Endpoint:  http://192.168.1.100:8080/api
```

Access the Web Interface

1. Open your browser
2. Navigate to http://localhost:8080 (or your custom port)
3. Login with credentials:
   · Username: yuan
   · Password: yuan

---

📱 Termux (Android) Instructions

```bash
# Install Termux from F-Droid
pkg update && pkg upgrade -y
pkg install python git -y

# Clone and run
git clone https://github.com/MiYuan-dev/DDoS.github.io.git
cd DDoS.github.io
python yuan_web_controller.py --port 8080
```

Access from browser: http://localhost:8080

---

🌐 Network Access & Tunneling

Local Network Access

```bash
# After starting, the tool shows your local IP
# Share with others on same network:
http://192.168.1.100:8080
```

Cloudflared Tunnel (Public Internet)

```bash
# Install cloudflared first
# Termux: pkg install cloudflared
# Linux:  sudo apt install cloudflared
# Mac:    brew install cloudflared

# Create tunnel
cloudflared tunnel --url http://localhost:8080
# You'll get a public URL like: https://random-name.trycloudflare.com
```

---

🎯 Command-Line Arguments

Argument Description Example
--port, -p Set custom port python yuan_web_controller.py --port 9090
--help, -h Show help menu python yuan_web_controller.py --help
--version, -v Show version python yuan_web_controller.py --version

---

📡 API Endpoints

Once the server is running, you can interact with these API endpoints:

Endpoint Method Description
/api/status GET Get current attack status
/api/network GET Get network information
/api/login POST Authenticate (username/password)
/api/start POST Start an attack
/api/stop POST Stop current attack

Example API Usage

```bash
# Check status
curl http://localhost:8080/api/status

# Get network info
curl http://localhost:8080/api/network

# Start UDP flood
curl -X POST http://localhost:8080/api/start \
  -H "Content-Type: application/json" \
  -d '{"target":"192.168.1.1:80","method":"UDP","threads":100,"seconds":30}'

# Stop attack
curl -X POST http://localhost:8080/api/stop
```

---

⚙️ Configuration

Edit yuan_web_controller.py to modify default settings:

```python
DEFAULT_PORT = 8080        # Default web interface port
MAX_THREADS = 5000         # Maximum attack threads
YUAN_MESSAGES = [...]      # Customize victory messages
```

---

📚 Complete Command Guide

See usage.txt for a comprehensive list of all commands and examples:

```bash
cat usage.txt
```

---

🛠️ Troubleshooting

Issue Solution
ddos.html not found Ensure file is in same directory as script
Port already in use Use --port to specify different port
Connection refused Verify server is running with `ps aux
SYN/ICMP fails Requires root privileges on Linux
No stats updating Check API at http://localhost:PORT/api/status
Termux killed Disable battery optimization for Termux
Cloudflared not found Install using package manager (see instructions)

---

⚠️ Legal & Ethical Warning

THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY.

· ❌ Do NOT use against systems you don't own
· ❌ Do NOT use without explicit written permission
· ❌ Unauthorized DDoS attacks are ILLEGAL
· ⚠️ Violators face severe legal consequences including:
  · 5-10 years imprisonment
  · $500,000+ fines
  · Permanent criminal record

By using this software, you agree to take full responsibility for your actions.

---

🤝 Contributing

Contributions for educational improvements are welcome:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

Note: Malicious modifications will be rejected.

---

📜 License

Educational use only. Not for commercial or malicious purposes.

---

📞 Support

· GitHub Issues: https://github.com/MiYuan-dev/DDoS.github.io/issues
· Include: Device info, Python version, error messages, and steps to reproduce

---

🙏 Acknowledgments

· Built with Python standard library (no external dependencies)
· BlackArch Linux for design inspiration
· Educational security community

---

📊 Stats

https://img.shields.io/github/repo-size/MiYuan-dev/DDoS.github.io
https://img.shields.io/github/languages/code-size/MiYuan-dev/DDoS.github.io
https://img.shields.io/github/languages/count/MiYuan-dev/DDoS.github.io
https://img.shields.io/github/languages/top/MiYuan-dev/DDoS.github.io

---

YUAN WAS HERE - NO SYSTEM IS SAFE

With great power comes great responsibility. Use ethically.

---

Last updated: March 2026

```


---

## 🚀 **How to Update on GitHub**

### **Method 1: Direct on GitHub Website**

1. Go to your repository: `https://github.com/MiYuan-dev/DDoS.github.io`
2. Click on `README.md`
3. Click the pencil icon (Edit)
4. **Delete all existing content**
5. **Paste the entire updated README above**
6. Scroll down and add commit message: `Updated README with new features and CLI docs`
7. Click **"Commit changes"**

### **Method 2: Using Git Commands**

```bash
# Navigate to your local repo
cd /storage/emulated/0/Download/Telegram/CyberSecurityTools/YUANCYBER/WebControl/DDoS.github.io

# Update README.md (paste the new content)
nano README.md

# Add to git
git add README.md

# Commit
git commit -m "Updated README with command-line arguments and BlackArch styling"

# Push to GitHub
git push origin main
```

---

✅ What's New in README

Section Added
Screenshot Preview ASCII banner preview
Command-Line Interface New CLI features documented
API Endpoints Complete API reference
Usage Examples All new commands explained
Troubleshooting Port conflict solutions
Stats Badges Repository statistics

Your README is now fully updated with all the new features! 🎉
