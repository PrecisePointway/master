#!/bin/bash
set -euo pipefail

# COLORS
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}?? INITIATING SOVEREIGN SYSTEM INTEGRATION TEST${NC}"

# --- STEP 0: CLEAN & BUILD ---
echo "?? Building Infrastructure..."
docker-compose down --volumes --remove-orphans || true
docker-compose build
docker-compose up -d

echo "   Waiting for container health..."
sleep 10

# --- STEP 1: SEED TEST DATA ---
echo "?? Seeding Jurisdiction Data..."
mkdir -p Evidence/Inbox Property/Leads

echo "Invoice #101 for Sovereign Services" > Evidence/Inbox/test_invoice_stable.txt
echo "3 Bed House. 123 Test Rd. Asking £350k. Warning: Structural cracks visible in foundation." > Property/Leads/test_trap_fixer.txt

# --- STEP 2: EXECUTE AGENTS ---
echo "??  Running Agents..."
docker-compose run --rm evidence python src/agents/evidence_validator.py
docker-compose run --rm property python src/agents/property_analyst.py

# --- STEP 3: VERIFY JURISDICTIONS ---
echo -e "\n?? VERIFYING JURISDICTIONAL BOUNDARIES..."
if ls Evidence/Analysis/_verified/test_invoice_stable.json 1> /dev/null 2>&1; then
  echo -e "${GREEN}? [EVIDENCE] Correctly routed to _verified (STABLE)${NC}"
else
  echo -e "${RED}? [EVIDENCE] Failed to reach _verified${NC}"; exit 1
fi
if ls Property/Scored/_drafts/test_trap_fixer.json 1> /dev/null 2>&1; then
  echo -e "${GREEN}? [PROPERTY] Correctly routed to _drafts (INSIDER)${NC}"
else
  echo -e "${RED}? [PROPERTY] Failed to reach _drafts${NC}"; exit 1
fi

# --- STEP 4: VERIFY LEGISLATIVE LOGIC ---
echo -e "\n??  VERIFYING LEGISLATIVE ENFORCEMENT..."
SCORE=$(grep -o '"condition_score": [0-9]*' Property/Scored/_drafts/test_trap_fixer.json | awk -F': ' '{print $2}')
if [ -z "${SCORE}" ]; then echo -e "${RED}? Could not read condition_score${NC}"; exit 1; fi
if [ "${SCORE}" -le 5 ]; then
  echo -e "${GREEN}? [LEGISLATION] Defects Trap Caught! Score capped at ${SCORE} (<= 5)${NC}";
else
  echo -e "${RED}? [LEGISLATION] FAILED. Score is ${SCORE} (>5).${NC}"; exit 1;
fi

# --- STEP 5: READINESS & TESTS ---
echo -e "\n?? CHECKING SYSTEM READINESS..."
docker-compose run --rm evidence python scripts/agent_readiness.py || { echo -e "${RED}? Readiness script failed${NC}"; exit 1; }

echo -e "\n?? RUNNING UNIT TESTS..."
docker-compose run --rm evidence pytest tests/test_tracks.py || { echo -e "${RED}? Track tests failed${NC}"; exit 1; }

echo -e "\n${GREEN}?? SOVEREIGN SYSTEM INTEGRATION COMPLETE. ALL SYSTEMS GO.${NC}"