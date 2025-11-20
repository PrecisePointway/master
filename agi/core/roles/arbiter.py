# agi/core/roles/arbiter.py
from __future__ import annotations
from typing import Dict, Any

REFUSAL_PREFIX = "FINAL DECISION: REFUSAL\n"


def run_arbiter(specialist_out: Dict[str, Any], validator_out: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    if not validator_out.get("policy_ok", True):
        final_answer = REFUSAL_PREFIX + validator_out.get("answer", "Refused")
        status = "refused"
    else:
        final_answer = validator_out.get("answer") or specialist_out.get("answer") or ""
        status = "ok"

    return {
        "role": "arbiter",
        "status": status,
        "final_answer": final_answer,
        "violations": validator_out.get("violations", []),
    }
