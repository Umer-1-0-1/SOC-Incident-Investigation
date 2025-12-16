# log_parser.py
# SOC-style parser that generates CSV and Markdown incident report

import os
import csv
import re
from collections import defaultdict

# Dynamic log file path
current_dir = os.path.dirname(__file__)
LOG_FILE_DEFAULT = os.path.join(current_dir, "../logs/auth.log")
CSV_OUTPUT = os.path.join(current_dir, "../logs/auth_curated.csv")
MD_OUTPUT = os.path.join(current_dir, "../reports/incident_report.md")


def parse_log(file_path):
    events = []
    summary = defaultdict(lambda: defaultdict(int))  # nested dict: summary[user][event] = count

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 1)
            timestamp = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            event_type = None
            user = "unknown"

            # Failed login via su
            if "authentication failure" in rest.lower():
                event_type = "FAILED LOGIN/SU"
                match = re.search(r'user=(\w+)', rest)
                if match:
                    user = match.group(1)

            # Successful login session
            elif "session opened" in rest.lower():
                if "sudo" in rest.lower():
                    event_type = "SUCCESSFUL SUDO"
                    match = re.search(r'for user (\w+)', rest)
                    if match:
                        user = match.group(1)
                    else:
                        match2 = re.search(r'for user (\w+)\(uid=', rest)
                        if match2:
                            user = match2.group(1)
                elif "cron" in rest.lower():
                    event_type = "SUCCESSFUL CRON"
                    match = re.search(r'for user (\w+)', rest)
                    if match:
                        user = match.group(1)
                    else:
                        user = "root"
                else:
                    event_type = "SUCCESSFUL LOGIN"
                    match = re.search(r'for user (\w+)', rest)
                    if match:
                        user = match.group(1)
                    else:
                        match2 = re.search(r'for user (\w+)\(uid=', rest)
                        if match2:
                            user = match2.group(1)

            # Successful su
            elif "session opened for user" in rest.lower() and "su[" in rest.lower():
                event_type = "SUCCESSFUL SU"
                match = re.search(r'for user (\w+)', rest)
                if match:
                    user = match.group(1)

            # Add to events list and summary
            if event_type:
                # Color-code for Markdown table
                if "SUCCESS" in event_type:
                    ev_display = f"<span style='color:green'>{event_type}</span>"
                else:
                    ev_display = f"<span style='color:red'>{event_type}</span>"

                events.append([timestamp, user, ev_display])
                summary[user][event_type] += 1

    return events, summary


def write_csv(events, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "User", "Event"])
        for ts, user, ev_display in events:
            # Remove HTML for CSV
            clean_ev = ev_display.replace("<span style='color:green'>", "") \
                                 .replace("<span style='color:red'>", "") \
                                 .replace("</span>", "")
            writer.writerow([ts, user, clean_ev])
    print(f"CSV generated: {output_file}")


def print_summary(summary):
    print("\n=== SOC Summary ===")
    for user, events in summary.items():
        print(f"User: {user}")
        for event, count in events.items():
            print(f"  {event}: {count}")
        print("-" * 30)


def write_markdown(events, summary, md_file):
    os.makedirs(os.path.dirname(md_file), exist_ok=True)
    with open(md_file, "w", encoding="utf-8") as md:
        md.write("# SOC Incident Report\n\n")

        # Table version with color coding
        md.write("## Event Table\n\n")
        md.write("| Timestamp | User | Event |\n")
        md.write("|-----------|------|-------|\n")
        for ts, user, ev_display in events:
            md.write(f"| {ts} | {user} | {ev_display} |\n")

        md.write("\n## Timeline\n\n")
        # Bullet timeline version (ASCII safe)
        for ts, user, ev_display in events:
            clean_ev = ev_display.replace("<span style='color:green'>", "") \
                                 .replace("<span style='color:red'>", "") \
                                 .replace("</span>", "")
            md.write(f"- {ts} | {user} | {clean_ev}\n")


if __name__ == "__main__":
    file_path = input(f"Enter path to log file (press Enter for default '{LOG_FILE_DEFAULT}'): ").strip()
    if not file_path:
        file_path = LOG_FILE_DEFAULT

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
    else:
        events, summary = parse_log(file_path)
        write_csv(events, CSV_OUTPUT)
        print_summary(summary)
        write_markdown(events, summary, MD_OUTPUT)
        print(f"Markdown report generated: {MD_OUTPUT}")
