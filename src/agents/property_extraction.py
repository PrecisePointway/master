import re

def extract_price(text: str):
    clean = text.replace(",", "").replace("£", "").replace("$", "").lower()
    pattern = r"(\d{2,9})(?:\s*[-–]\s*(\d{2,9}))?"
    m = re.search(pattern, clean)
    if not m:
        return None
    low = int(m.group(1))
    high = m.group(2)
    if high:
        high = int(high)
        return min(low, high)
    return low

def detect_defects(text: str):
    defect_keywords = [
        "crack", "cracks", "mold", "mould", "rot", "damp", "damage",
        "broken", "stain", "collapse", "structural", "repair", "modernization", "derelict"
    ]
    t = text.lower()
    return any(kw in t for kw in defect_keywords)

def extract_address(text: str):
    addr_pattern = r"\b\d{1,4}\s+[A-Za-z ]+(?:Road|Street|Avenue|Lane|Drive|Close|Way|Rd|St)\b"
    m = re.search(addr_pattern, text, flags=re.I)
    if not m:
        return None, 0.0
    return m.group(0).strip(), 0.95
