"""
file_io.py — Three file I/O projects in one:
  1. CSV Analyser   — reads sales data, computes stats, writes a report
  2. Log Parser     — scans a log file, extracts errors and warnings
  3. Word Counter   — counts word frequencies and writes a ranked list

Run:  python3 file_io.py
"""

import csv
import os
import re
from collections import Counter
from datetime import datetime

TEMP_DIR = os.path.join(os.path.dirname(__file__), "_temp")
os.makedirs(TEMP_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# 1. CSV ANALYSER
# ══════════════════════════════════════════════════════════════════════════════

SALES_CSV = os.path.join(TEMP_DIR, "sales.csv")
REPORT_TXT = os.path.join(TEMP_DIR, "sales_report.txt")

SALES_DATA = [
    ["date",       "product",   "region",  "units", "price"],
    ["2024-01-05", "Widget A",  "North",   "120",   "9.99"],
    ["2024-01-05", "Widget B",  "South",   "85",    "14.99"],
    ["2024-01-12", "Widget A",  "South",   "200",   "9.99"],
    ["2024-01-12", "Gadget X",  "North",   "30",    "49.99"],
    ["2024-01-19", "Gadget X",  "East",    "45",    "49.99"],
    ["2024-01-19", "Widget B",  "North",   "110",   "14.99"],
    ["2024-02-02", "Widget A",  "East",    "175",   "9.99"],
    ["2024-02-02", "Gadget X",  "South",   "60",    "49.99"],
    ["2024-02-09", "Widget B",  "East",    "95",    "14.99"],
    ["2024-02-09", "Widget A",  "North",   "140",   "9.99"],
    ["2024-02-16", "Gadget Y",  "North",   "25",    "79.99"],
    ["2024-02-16", "Gadget Y",  "South",   "18",    "79.99"],
]


def write_sales_csv():
    with open(SALES_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(SALES_DATA)
    print(f"  ✓ Written: {SALES_CSV}")


def analyse_sales():
    """Read CSV, compute stats, write a formatted report."""
    rows = []
    with open(SALES_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "date":    row["date"],
                "product": row["product"],
                "region":  row["region"],
                "units":   int(row["units"]),
                "price":   float(row["price"]),
                "revenue": int(row["units"]) * float(row["price"]),
            })

    # Compute stats
    total_revenue = sum(r["revenue"] for r in rows)
    total_units   = sum(r["units"]   for r in rows)

    by_product = {}
    for r in rows:
        p = r["product"]
        by_product.setdefault(p, {"units": 0, "revenue": 0.0})
        by_product[p]["units"]   += r["units"]
        by_product[p]["revenue"] += r["revenue"]

    by_region = {}
    for r in rows:
        rg = r["region"]
        by_region.setdefault(rg, {"units": 0, "revenue": 0.0})
        by_region[rg]["units"]   += r["units"]
        by_region[rg]["revenue"] += r["revenue"]

    best_product = max(by_product, key=lambda p: by_product[p]["revenue"])
    best_region  = max(by_region,  key=lambda rg: by_region[rg]["revenue"])

    # Write report
    lines = [
        "=" * 50,
        "  SALES REPORT",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 50,
        f"  Total revenue:   £{total_revenue:,.2f}",
        f"  Total units:     {total_units:,}",
        f"  Transactions:    {len(rows)}",
        "",
        "  By product:",
    ]
    for prod, stats in sorted(by_product.items(), key=lambda x: -x[1]["revenue"]):
        lines.append(f"    {prod:<12}  £{stats['revenue']:>8,.2f}  "
                     f"({stats['units']} units)")
    lines += ["", "  By region:"]
    for reg, stats in sorted(by_region.items(), key=lambda x: -x[1]["revenue"]):
        lines.append(f"    {reg:<10}  £{stats['revenue']:>8,.2f}  "
                     f"({stats['units']} units)")
    lines += [
        "",
        f"  Best-selling product: {best_product}",
        f"  Top region:           {best_region}",
        "=" * 50,
    ]

    with open(REPORT_TXT, "w") as f:
        f.write("\n".join(lines))

    print(f"  ✓ Report written: {REPORT_TXT}")
    print("\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════════
# 2. LOG PARSER
# ══════════════════════════════════════════════════════════════════════════════

LOG_FILE     = os.path.join(TEMP_DIR, "app.log")
ERRORS_FILE  = os.path.join(TEMP_DIR, "errors.log")

SAMPLE_LOG = """2024-03-01 08:00:01 INFO  Application started
2024-03-01 08:00:05 INFO  Database connected
2024-03-01 08:01:12 INFO  User 'alice' logged in
2024-03-01 08:03:45 WARNING  High memory usage: 87%
2024-03-01 08:05:00 ERROR  Failed to write to disk: /var/log/app — Permission denied
2024-03-01 08:05:01 INFO  Retrying disk write
2024-03-01 08:05:03 ERROR  Disk write failed again: timeout after 2000ms
2024-03-01 08:06:22 INFO  User 'bob' logged in
2024-03-01 08:07:55 WARNING  Slow query detected: 3400ms (threshold: 1000ms)
2024-03-01 08:09:00 INFO  Cache cleared
2024-03-01 08:10:15 ERROR  Unhandled exception in worker thread: NullPointerException
2024-03-01 08:10:16 INFO  Worker thread restarted
2024-03-01 08:12:00 INFO  Scheduled backup started
2024-03-01 08:14:33 WARNING  Backup size exceeds quota: 4.2GB / 4.0GB
2024-03-01 08:15:00 INFO  Application shutdown initiated
"""

LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(INFO|WARNING|ERROR)\s+(.*)"
)


def write_log():
    with open(LOG_FILE, "w") as f:
        f.write(SAMPLE_LOG)
    print(f"  ✓ Written: {LOG_FILE}")


def parse_log():
    """Read log, count levels, extract errors & warnings, write error file."""
    counts  = Counter()
    errors  = []
    warnings = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            m = LOG_PATTERN.match(line.strip())
            if m:
                ts, level, msg = m.groups()
                counts[level] += 1
                if level == "ERROR":
                    errors.append((ts, msg))
                elif level == "WARNING":
                    warnings.append((ts, msg))

    print(f"\n  Log summary:")
    for level in ("INFO", "WARNING", "ERROR"):
        print(f"    {level:<8}: {counts[level]}")

    print(f"\n  Errors ({len(errors)}):")
    for ts, msg in errors:
        print(f"    [{ts}] {msg}")

    print(f"\n  Warnings ({len(warnings)}):")
    for ts, msg in warnings:
        print(f"    [{ts}] {msg}")

    with open(ERRORS_FILE, "w") as f:
        f.write(f"Error report — {datetime.now()}\n")
        f.write("=" * 50 + "\n")
        for ts, msg in errors:
            f.write(f"[{ts}] ERROR: {msg}\n")
        f.write("\nWarnings:\n")
        for ts, msg in warnings:
            f.write(f"[{ts}] WARNING: {msg}\n")

    print(f"\n  ✓ Error report written: {ERRORS_FILE}")


# ══════════════════════════════════════════════════════════════════════════════
# 3. WORD COUNTER
# ══════════════════════════════════════════════════════════════════════════════

TEXT_FILE   = os.path.join(TEMP_DIR, "sample_text.txt")
WORD_REPORT = os.path.join(TEMP_DIR, "word_frequencies.txt")

SAMPLE_TEXT = """
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub.
"""

STOP_WORDS = {"the", "a", "an", "to", "and", "or", "of", "in", "is",
              "be", "by", "no", "tis", "s", "that", "there"}


def write_text():
    with open(TEXT_FILE, "w") as f:
        f.write(SAMPLE_TEXT)
    print(f"  ✓ Written: {TEXT_FILE}")


def count_words():
    """Read text file, count word frequencies, write ranked report."""
    with open(TEXT_FILE, "r") as f:
        raw = f.read()

    words = re.findall(r"[a-zA-Z']+", raw.lower())
    words = [w.strip("'") for w in words if w.strip("'") not in STOP_WORDS]

    freq = Counter(words)
    total = sum(freq.values())

    print(f"\n  Word frequencies (top 10):")
    print(f"  {'Word':<20} {'Count':>6}  {'%':>6}  Bar")
    print("  " + "─" * 50)
    for word, count in freq.most_common(10):
        pct = count / total * 100
        bar = "█" * count
        print(f"  {word:<20} {count:>6}  {pct:>5.1f}%  {bar}")

    with open(WORD_REPORT, "w") as f:
        f.write(f"Word frequency report\nTotal words: {total}\n\n")
        for word, count in freq.most_common():
            f.write(f"{count:>4}  {word}\n")

    print(f"\n  ✓ Frequency report written: {WORD_REPORT}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║           File I/O Projects              ║")
    print("╚══════════════════════════════════════════╝")

    print("\n── 1. CSV Analyser ──────────────────────────")
    write_sales_csv()
    analyse_sales()

    print("\n── 2. Log Parser ────────────────────────────")
    write_log()
    parse_log()

    print("\n── 3. Word Counter ──────────────────────────")
    write_text()
    count_words()
