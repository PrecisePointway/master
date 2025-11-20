#!/usr/bin/env bash
set -euo pipefail

BACKUP=${1:-}
LEDGER_DIR=Governance/Logs
STAMP=$(date +%Y%m%d_%H%M%S)

perform_backup() {
  echo "?? Triggering Backup to Drives E & F..."
  if [ -f "sovereign-backup.ps1" ]; then
    powershell.exe -ExecutionPolicy Bypass -File "./sovereign-backup.ps1" || echo "?? Backup script failed"
  else
    echo "?? sovereign-backup.ps1 not found; skipping external drive mirror"
  fi
}

echo "?? Sovereign shutdown initiated..."

# Flush: nothing to do explicitly, but we can snapshot ledgers
mkdir -p backups
if [ "$BACKUP" = "--backup" ]; then
  tar czf backups/ledger_${STAMP}.tar.gz ${LEDGER_DIR} || true
  echo "???  Ledger snapshot: backups/ledger_${STAMP}.tar.gz"
  perform_backup
fi

docker-compose down

echo "? Shutdown complete."
