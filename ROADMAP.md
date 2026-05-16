# 🚀 AutoOSINT Development Roadmap

This document serves as a strategic guide for transitioning from a prototype to a professional-grade OSINT engine.

---

## 🔑 1. Real API Recommendations
Replace the mock data in `modules/` with these industry-standard sources.

### 📧 Email Investigation
*   **HaveIBeenPwned (HIBP)**: The gold standard for data breaches. Requires a low-cost API key.
*   **LeakCheck.io**: Excellent database for raw leak data and passwords.
*   **Hunter.io**: For professional email verification and finding company email patterns.

### 🌐 Domain & IP Recon
*   **Shodan**: "The search engine for things." Essential for seeing what services (ports) are open on a domain's IP.
*   **SecurityTrails**: The best tool for historical DNS data and finding "hidden" subdomains.
*   **WhoisXMLAPI**: For automated WHOIS data (owner names, registration dates).

### 📱 Phone Number Lookup
*   **Twilio Lookup**: Highly accurate for identifying if a number is a "Burner" (VoIP) or a real Mobile line.
*   **Numverify**: Simple, fast, and has a generous free tier for global lookups.
*   **KSA Numberbooks**: For Saudi Arabia, look into integrating with public web-based phonebooks.

### 👤 Username Scanning
*   **Sherlock Project**: Instead of writing your own, consider using the Sherlock site-list (300+ platforms).
*   **Social-Analyzer**: A powerful API-based alternative for deep social media analysis.

---

## 🛠️ 2. Technical Implementation Ideas
Advanced features to build into your core logic.

### ⚡ Parallelism (High Priority)
Currently, the tool scans one module at a time. Using `concurrent.futures.ThreadPoolExecutor` in `core/engine.py` will allow all modules to run at once, making your scans 10x faster.

### 🕵️ Proxy & User-Agent Rotation
To prevent your IP from being banned by sites like Instagram or Twitter:
1.  Add a list of 50+ User-Agents to `utils/http_client.py`.
2.  Integrate a proxy service (like Bright Data or a Tor proxy) to rotate your IP on every request.

### 🧠 Advanced Correlation Rules
Enhance `core/correlator.py` with more complex logic:
*   *Rule*: If a username is found on GitHub AND a domain has an open "Dev" subdomain, alert for "Potential Source Code Leak."
*   *Rule*: If an email is found in a breach AND the phone number is a VoIP line, alert for "High Anonymity/Burner Profile."

---

## 🌟 3. Future Feature Ideas
Big additions to make AutoOSINT a top-tier product.

1.  **Web Dashboard (GUI)**: Use `Streamlit` or `Flask` to create a visual interface where users can see the tables and maps in their browser.
2.  **Database Integration**: Store all scan results in a `SQLite` or `PostgreSQL` database so you can search through past investigations.
3.  **PDF Reporting**: Use a library like `ReportLab` to generate professional investigation reports for clients or law enforcement.
4.  **Graph Visualization**: Use `NetworkX` to create a visual map of how a person's email, phone, and social media are all connected.

---

## ✅ 4. Launch Checklist
*   [ ] Create `.env` file in the root directory.
*   [ ] Add `LEAKCHECK_API_KEY` (Free variant for Email).
*   [ ] Add `SHODAN_API_KEY` (Student/Paid tier for Domains).
*   [ ] Add `SECURITYTRAILS_API_KEY` (SecurityTrails).
*   [ ] Add `NUMVERIFY_API_KEY` (NumVerify).

---

## 🔗 5. Deep Scanning & Pivoting (The "Chain" Feature)
This is the core "Connected OSINT" feature that links findings together automatically.

### ⚙️ How it Works
*   **Pivots**: Modules can now return a `pivots` list (e.g., a username scan finds an email).
*   **Recursive Engine**: When the `-D` or `--deep` flag is used, the engine automatically starts a new scan for every pivot found.
*   **Safety**: The engine tracks "visited" targets to prevent infinite loops (e.g., if target A links to B, and B links back to A).

### 🚀 Expansion Ideas for Pivoting
1.  **Regex Extraction**: Add regex logic to `SocialScanModule` to scrape emails/phones directly from profile bios.
2.  **Domain-to-IP Pivot**: If a domain is scanned, automatically pivot to scan the resulting IP address for open ports (Shodan).
3.  **Depth Control**: Currently, it follows all links. You could add a `--depth` flag to limit how many "hops" the tool takes (e.g., `--depth 2`).

---

## 📝 6. Operational Notes (Important)
*   **Local Testing**: You do NOT need to push to GitHub to test changes. Running `pip install .` inside your local project folder will update the `autoosint` command immediately.
*   **Virtual Environments**: Always use a `venv` to keep your system Python clean. Activate it with `.\venv\Scripts\activate` before testing.
*   **API Security**: Never commit your `.env` file. It is currently in the `.gitignore` for your safety.
*   **Results Location**: All investigation outputs are stored in the `output/results/` directory of the project.
