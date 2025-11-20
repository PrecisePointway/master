#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
DC = ["docker-compose"]
REPORT_DIR = ROOT / "Governance"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_PATH = REPORT_DIR / "integration_report.json"

EVIDENCE_INBOX = ROOT / "Evidence" / "Inbox"
PROPERTY_LEADS = ROOT / "Property" / "Leads"
EVIDENCE_VERIFIED = ROOT / "Evidence" / "Analysis" / "_verified"
PROPERTY_DRAFTS = ROOT / "Property" / "Scored" / "_drafts"


def run(cmd: list[str], check=True) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.returncode, (p.stdout + p.stderr)


def need_cmd(name: str):
    rc, _ = run(["which" if os.name != "nt" else "where", name], check=False)
    if rc != 0:
        raise RuntimeError(f"Missing required command: {name}")


def seed_files():
    EVIDENCE_INBOX.mkdir(parents=True, exist_ok=True)
    PROPERTY_LEADS.mkdir(parents=True, exist_ok=True)

    (EVIDENCE_INBOX / "test_invoice_stable.txt").write_text(
        "Invoice #101 for Sovereign Services.\nClient: Sovereign Systems Ltd.\nTotal Due: £450.00\n",
        encoding="utf-8",
    )
    (PROPERTY_LEADS / "test_trap_fixer.txt").write_text(
        "3 Bed House. 123 Test Rd. Asking £350k. Warning: Structural cracks visible in foundation.",
        encoding="utf-8",
    )


def compose(*args: str):
    return run(DC + list(args))


def boot_sequence(report: dict):
    # Clean and build
    compose("down", "--volumes", "--remove-orphans")
    compose("build")

    # Boardroom first, then agents
    compose("up", "-d", "boardroom")
    time.sleep(3)
    compose("up", "-d", "evidence")
    compose("up", "-d", "property")

    # Wait for containers to stabilize
    time.sleep(10)
    rc, ps = run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"], check=False)
    report["containers"] = ps.strip()


def verify_tracks(report: dict):
    env_path = ROOT / ".env"
    env_data = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env_data[k.strip()] = v.strip()
    report["tracks"] = {
        "TRACK": env_data.get("TRACK", ""),
        "EVIDENCE_TRACK": env_data.get("EVIDENCE_TRACK", ""),
        "PROPERTY_TRACK": env_data.get("PROPERTY_TRACK", ""),
    }


def run_agents(report: dict):
    # Seed data
    seed_files()

    # Execute agents inside containers
    ev_rc, ev_out = compose("run", "--rm", "evidence", "python", "src/agents/evidence_validator.py")
    pr_rc, pr_out = compose("run", "--rm", "property", "python", "src/agents/property_analyst.py")
    report["agent_runs"] = {"evidence": ev_out, "property": pr_out}


def verify_outputs(report: dict):
    ok = True
    details = {}

    ev_out = EVIDENCE_VERIFIED / "test_invoice_stable.json"
    pr_out = PROPERTY_DRAFTS / "test_trap_fixer.json"

    details["evidence_verified_path"] = str(ev_out)
    details["property_drafts_path"] = str(pr_out)

    if not ev_out.exists():
        ok = False
        details["evidence"] = "Missing expected verified output"
    else:
        details["evidence"] = "OK"

    if not pr_out.exists():
        ok = False
        details["property"] = "Missing expected drafts output"
    else:
        # Verify legislative trap: condition_score <= 5
        try:
            import re
            txt = pr_out.read_text(encoding="utf-8")
            m = re.search(r'"condition_score"\s*:\s*(\d+)', txt)
            if not m:
                ok = False
                details["property_legislation"] = "condition_score not found"
            else:
                score = int(m.group(1))
                if score <= 5:
                    details["property_legislation"] = f"OK (score={score})"
                else:
                    ok = False
                    details["property_legislation"] = f"Violation (score={score})"
        except Exception as e:
            ok = False
            details["property_legislation_error"] = str(e)

    report["verification"] = details
    report["verified"] = ok


def verify_ledger(report: dict):
    # Try running the existing ledger verifier if present
    script = ROOT / "scripts" / "verify_ledger.py"
    info = {"ran": False, "result": "skipped"}
    if script.exists():
        rc, out = run([sys.executable, str(script)], check=False)
        info = {"ran": True, "rc": rc, "output": out.strip()[:2000]}
    report["ledger_audit"] = info


def main():
    report: dict = {"status": "INIT"}
    try:
        need_cmd("docker")
        need_cmd("docker-compose")
        report["status"] = "BOOTING"
        boot_sequence(report)
        verify_tracks(report)
        run_agents(report)
        verify_outputs(report)
        verify_ledger(report)
        report["status"] = "GREEN" if report.get("verified") else "RED"
    except Exception as e:
        report["status"] = "RED"
        report["error"] = str(e)
    finally:
        REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"status": report.get("status"), "report": str(REPORT_PATH)}, indent=2))
        if report.get("status") != "GREEN":
            sys.exit(1)


if __name__ == "__main__":
    main()
