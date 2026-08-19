import re

KEYWORD_MAP = {
    # Execution
    "powershell": "T1059.001",
    "command injection": "T1059",
    "malicious php": "T1059",

    # Initial Access
    "spearphishing attachment": "T1566.001",
    "phishing": "T1566",
    "exploit public-facing application": "T1190",
    "rce": "T1190",
    "remote code execution": "T1190",

    # Persistence
    "scheduled task": "T1053.005",

    # Credential Access
    "credential dumping": "T1003",
    "steal credentials": "T1552",
    "steal browser credentials": "T1555.003",

    # Lateral Movement
    "move across networks": "T1021",
    "socks5 proxies": "T1090",

    # Exfiltration
    "exfiltrate data": "T1041",
    "data theft": "T1041",

    # Impact
    "ransomware": "T1486",
}

def extract_ttp_ids(text):
    ids = set(re.findall(r"T1\d{3}(?:\.\d{3})?", text))
    for kw, tid in KEYWORD_MAP.items():
        if kw in text.lower():
            ids.add(tid)
    return list(ids)
