import os
from pathlib import Path

def check_readiness():
    evidence_verified = Path("/data/evidence/Analysis/_verified")
    property_drafts = Path("/data/property/Scored/_drafts")
    if not evidence_verified.exists():
        evidence_verified = Path("Evidence/Analysis/_verified")
    if not property_drafts.exists():
        property_drafts = Path("Property/Scored/_drafts")

    ev_files = list(evidence_verified.iterdir()) if evidence_verified.exists() else []
    prop_files = list(property_drafts.iterdir()) if property_drafts.exists() else []

    ev_status = "LIVE" if ev_files else "WAITING"
    prop_status = "CALIBRATING" if prop_files else "IDLE"

    print(f"EVIDENCE STATUS: {ev_status} ({len(ev_files)} files)")
    print(f"PROPERTY STATUS: {prop_status} ({len(prop_files)} drafts)")

if __name__ == "__main__":
    check_readiness()
