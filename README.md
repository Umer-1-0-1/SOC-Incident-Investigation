````markdown
# SOC Log Parser

A **SOC-style authentication log parser** for Linux systems that generates **curated CSV files** and **Markdown incident reports**. Designed for cybersecurity analysts and SOC teams to quickly analyze authentication events.

---

## Features

- Parses Linux authentication logs (`auth.log`) including:
  - `login`, `sudo`, `su`, and `cron` events
- Generates a **curated CSV** of events with:
  - Timestamp  
  - User  
  - Event type (SUCCESSFUL LOGIN, SUCCESSFUL SUDO, FAILED LOGIN/SU, etc.)
- Produces a **Markdown incident report**:
  - Color-coded event table (green for success, red for failure)  
  - Timeline view for quick overview
- Console summary per user for fast analysis
- Dynamic log file path with default fallback

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Umer-1-0-1/SOC-Incident-Investigation.git
cd SOC-Incident-Investigation
````

2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

* **Linux/macOS:**

```bash
source venv/bin/activate
```

* **Windows:**

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** For now, `log_parser.py` uses only Python standard libraries. `requirements.txt` is prepared for future package additions.

---

## Usage

Run the parser:

```bash
python log_parser.py
```

* You will be prompted to enter the path to your log file.
* Press Enter to use the default path: `../logs/auth.log`.

Outputs generated:

* **CSV:** `../logs/auth_curated.csv`
* **Markdown report:** `../reports/incident_report.md`
* Console summary per user

---

## Sample Log Format

Supports Linux PAM-based logs like:

```
2025-12-11T13:59:50.268497+05:00 User login[752]: pam_unix(login:session): session opened for user user1(uid=1000) by user1(uid=0)
2025-12-11T14:01:46.615487+05:00 User sudo: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
2025-12-16T09:00:27.362363+05:00 User su: pam_unix(su:auth): authentication failure; logname= uid=1000 euid=0 tty=/dev/pts/0 ruser=user1 rhost=  user=socuser
```

---

## Python Environment

1. Create and activate a virtual environment (see **Installation**).
2. Keep the `venv/` folder in `.gitignore`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## License

MIT License. Feel free to use and modify for personal or professional SOC projects.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements.

---

## Author

Umar Bin Abdul Aziz | GitHub: [@Umer-1-0-1](https://github.com/Umer-1-0-1)

```
```
