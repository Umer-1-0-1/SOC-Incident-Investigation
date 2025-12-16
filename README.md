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
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
