
import requests
import json
import time

MITIGATION_TIPS = [
    "Use prepared statements (parameterized queries).",
    "Validate and sanitize all user inputs.",
    "Avoid using dynamic SQL queries.",
    "Use ORM frameworks where possible.",
    "Restrict database permissions for the app user.",
    "Enable error handling to avoid leaking DB errors."
]

ERROR_PATTERNS = [
    "sql syntax", "mysql", "syntax error", "unclosed quotation", "query failed",
    "warning: mysql", "unterminated", "native client", "unexpected token"
]

def load_payloads(file_path="payloads.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def scan_url(url):
    payloads = load_payloads()
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SQLScannerBot/1.0)"}
    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            start_time = time.time()
            response = requests.get(test_url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            content = response.text.lower()
            is_vulnerable = (
                any(error in content for error in ERROR_PATTERNS) or response_time > 4.5
            )
            results.append({
                "payload": payload,
                "vulnerable": is_vulnerable,
                "response_time": round(response_time, 2),
                "tips": MITIGATION_TIPS if is_vulnerable else []
            })
        except Exception as e:
            results.append({
                "payload": payload,
                "vulnerable": False,
                "error": str(e),
                "tips": []
            })
    return results
