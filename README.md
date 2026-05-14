# 🛡️ AutoOSINT

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**AutoOSINT** is a professional-grade Open Source Intelligence (OSINT) tool designed for fast, accurate investigations. It automates the process of gathering intelligence on domains, emails, usernames, and phone numbers.

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install the tool globally:
(tip for users who are new to installing tools from github, create a python virtual enviroment)
```bash
git clone https://github.com/yourusername/AutoOSINT.git
cd AutoOSINT
pip install .
```

### 2. Basic Usage
AutoOSINT is designed to be used with explicit flags. No complex subcommands needed!

```bash
# Scan a Domain
autoosint -d google.com

# Scan an Email
autoosint -e admin@example.com

# Scan a Username
autoosint -u "johndoe"

# Scan a Phone Number (Saudi Arabia & Global)
autoosint -p "(966)50XXXXXXX"
```

### 3. Exporting Data
Save your investigation results to professional JSON or CSV formats:
```bash
autoosint -d target.com --export json
```

---

## 🛠️ Features
*   **DNS Reconnaissance**: Real-time lookup of A, MX, and TXT records.
*   **Global Phone Lookup**: Intelligent carrier and location detection (Optimized for KSA).
*   **Social Scanner**: Checks account existence across major platforms.
*   **Breach Engine**: Modular framework for data leak identification.
*   **Data Correlator**: An "AI-lite" layer that finds hidden patterns in your findings.

---

## ⚙️ Configuration
Create a `.env` file in the root directory to add your private API keys:
```bash
HIBP_API_KEY=your_key_here
SHODAN_API_KEY=your_key_here
```

---

## ❓ Troubleshooting (Command Not Found)
If you get an error saying `'autoosint' is not recognized`, your Python Scripts folder is likely not in your **PATH**.

**Windows Fix:**
1. Find your Python Scripts path (usually `C:\Users\YourUser\AppData\Roaming\Python\Python3X\Scripts`).
2. Search Windows for "Edit the system environment variables".
3. Click "Environment Variables" > Select "Path" > "Edit" > "New".
4. Paste the path and restart your terminal.

---

## 🤝 Contributing
Contributions are welcome! Please see [ROADMAP.md](ROADMAP.md) for future expansion ideas.
