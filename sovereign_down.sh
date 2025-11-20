#!/usr/bin/env bash
set -euo pipefail

BACKUP=${1:-}
LEDGER_DIR=Governance/Logs
STAMP=$(date +%Y%m%d_%H%M%S)

echo "?? Sovereign shutdown initiated..."

# Flush: nothing to do explicitly, but we can snapshot ledgers
mkdir -p backups
if [ "$BACKUP" = "--backup" ]; then
  tar czf backups/ledger_${STAMP}.tar.gz ${LEDGER_DIR} || true
  echo "???  Ledger snapshot: backups/ledger_${STAMP}.tar.gz"
fi

docker-compose down

echo "? Shutdown complete."
