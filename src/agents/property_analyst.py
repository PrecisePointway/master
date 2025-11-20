import sys, os, json
from pathlib import Path

sys.path.append(os.getcwd())
from src.core.router import SovereignRouter
from src.agents.property_extraction import extract_price, detect_defects, extract_address

def run_analyst():
    try:
        router = SovereignRouter("property")
    except Exception as e:
        print(f"? FATAL: Router Init Failed: {e}")
        return
    print(f"???  Property Analyst Online | Mode: {router.track.upper()}")

    data_root = Path(os.getenv("DATA_DIR", ".")) / "property"
    leads_dir = data_root / "Leads"
    if not leads_dir.exists():
        leads_dir = Path("Property/Leads")  # local fallback

    if not leads_dir.exists():
        print(f"?? No Leads Directory found at {leads_dir}")
        return

    files = [f for f in leads_dir.iterdir() if f.is_file()]
    print(f"   Found {len(files)} leads...")

    for file_path in files:
        print(f"   Analyzing: {file_path.name}")
        try:
            text_content = file_path.read_text(encoding="utf-8")
        except Exception:
            text_content = "Error reading file"

        price = extract_price(text_content)
        defects = detect_defects(text_content)
        address, addr_conf = extract_address(text_content)

        # Legislative constraints
        condition_score = 5 if defects else 7
        if "modernization" in text_content.lower() and condition_score > 5:
            condition_score = 5
        if address is None:
            addr_flag = "ADDRESS_UNKNOWN"
        else:
            addr_flag = "NONE"

        result = {
            "address": address,
            "asking_price": price,
            "condition_score": condition_score,
            "risk_flags": [flag for flag in ["STRUCTURAL_RISK" if defects else "NONE", addr_flag] if flag != "NONE"],
            "confidence": 0.75 if defects else 0.85,
            "notes": text_content[:120].replace("\n", " ")
        }

        router.save_result(f"{file_path.stem}.json", result)

if __name__ == "__main__":
    run_analyst()
