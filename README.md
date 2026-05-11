# AutoOSINT

A modular CLI-based OSINT automation framework for collecting and correlating public intelligence from usernames, emails, phone numbers, and domains.

## Features

### ✅ Username Enumeration
- Like Sherlock
- Check: GitHub, Reddit, TikTok, Instagram, Twitter/X, Steam, Medium
- Output: `[FOUND] GitHub: github.com/johndoe`

### ✅ Email Intelligence
- Domain extraction
- MX lookup
- Breach exposure APIs
- Gravatar lookup
- Username derivation

### ✅ Phone Intelligence
- Like PhoneInfoga
- Carrier lookup
- Country
- Timezone
- Format validation

### ✅ Domain Recon
- WHOIS
- DNS
- Subdomains
- SSL certificate info

### 🚀 The Correlation Engine (Differentiator)
The Correlation Engine makes the tool intelligent by deriving potential usernames from emails and matching them across different platforms.

## Project Structure

```
AutoOSINT/
│
├── cli.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── engine.py
│   ├── formatter.py
│   └── correlator.py
│
├── modules/
│   ├── __init__.py
│   │
│   ├── email/
│   │   ├── __init__.py
│   │   └── breach_check.py
│   │
│   ├── username/
│   │   ├── __init__.py
│   │   └── social_scan.py
│   │
│   ├── phone/
│   │   ├── __init__.py
│   │   └── carrier_lookup.py
│   │
│   └── domain/
│       ├── __init__.py
│
├── utils/
│   ├── __init__.py
│   ├── http_client.py
│   └── validators.py
│
├── output/
│   ├── results/
│   └── logs/
│
├── tests/
│
└── docs/
    ├── architecture.md
    └── roadmap.md
```

## Setup & Installation

```bash
git clone https://github.com/KJ66KK/AutoOSINT.git
cd AutoOSINT
pip install -r requirements.txt
```

## Usage

```bash
python cli.py email example@gmail.com
python cli.py username johndoe123
python cli.py phone +9665XXXXXXX
python cli.py domain example.com
```

## Recommended Libraries
- **typer**: CLI framework
- **rich**: Beautiful terminal output
- **aiohttp**: Async HTTP requests
- **phonenumbers**: Phone number validation
- **email-validator**: Email validation
