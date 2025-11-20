#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
DC="docker-compose -f ${COMPOSE_FILE}"

echo -e "${GREEN}?? INITIATING SOVEREIGN SYSTEM INTEGRATION TEST${NC}"

need_cmd() { if ! command -v "$1" >/dev/null 2>&1; then echo -e "${RED}? Missing required command: $1${NC}"; exit 1; fi; }
need_cmd docker
need_cmd docker-compose

echo -e "${YELLOW}?? Building Infrastructure...${NC}"
${DC} down --volumes --remove-orphans || true
${DC} build
${DC} up -d

echo "   Waiting for containers to come up..."; sleep 10

echo "   Current containers:"; docker ps --format 'table {{.Names}}\t{{.Status}}'

echo -e "${YELLOW}?? Seeding Jurisdiction Data...${NC}";
mkdir -p Evidence/Inbox Property/Leads
cat > Evidence/Inbox/test_invoice_stable.txt <<EOF
Invoice #101 for Sovereign Services.
Client: Sovereign Systems Ltd.
Total Due: £450.00
EOF
cat > Property/Leads/test_trap_fixer.txt <<EOF
3-bed house at 123 Test Road.
Asking price £350,000.
Notes: Structural cracks visible in foundation and significant damp in rear bedroom.
EOF

echo -e "${YELLOW}??  Running Agents...${NC}";
${DC} run --rm evidence python src/agents/evidence_validator.py || { echo -e "${RED}? Evidence agent failed${NC}"; exit 1; }
${DC} run --rm property python src/agents/property_analyst.py || { echo -e "${RED}? Property agent failed${NC}"; exit 1; }

echo -e "\n${YELLOW}?? VERIFYING JURISDICTIONAL BOUNDARIES...${NC}";
EVIDENCE_OUT="Evidence/Analysis/_verified/test_invoice_stable.json"
PROPERTY_OUT="Property/Scored/_drafts/test_trap_fixer.json"
if [ -f "${EVIDENCE_OUT}" ]; then echo -e "${GREEN}? [EVIDENCE] Routed to _verified (STABLE)${NC}"; else echo -e "${RED}? [EVIDENCE] Missing ${EVIDENCE_OUT}${NC}"; exit 1; fi
if [ -f "${PROPERTY_OUT}" ]; then echo -e "${GREEN}? [PROPERTY] Routed to _drafts (INSIDER)${NC}"; else echo -e "${RED}? [PROPERTY] Missing ${PROPERTY_OUT}${NC}"; exit 1; fi

echo -e "\n${YELLOW}??  VERIFYING LEGISLATIVE ENFORCEMENT...${NC}";
SCORE_LINE=$(grep -o '"condition_score": [0-9]*' "${PROPERTY_OUT}" || true)
SCORE=$(echo "${SCORE_LINE}" | awk -F': ' '{print $2}')
if [ -z "${SCORE:-}" ]; then echo -e "${RED}? Could not read condition_score${NC}"; exit 1; fi
if [ "${SCORE}" -le 5 ]; then echo -e "${GREEN}? Defects trap enforced (condition_score=${SCORE})${NC}"; else echo -e "${RED}? Defects cap violated (condition_score=${SCORE})${NC}"; exit 1; fi
if grep -q '"status": "AUTO_VERIFIED"' "${EVIDENCE_OUT}"; then echo -e "${GREEN}? Governance AUTO_VERIFIED present${NC}"; else echo -e "${YELLOW}?? Governance status missing AUTO_VERIFIED${NC}"; fi

echo -e "\n${YELLOW}?? CHECKING SYSTEM READINESS...${NC}";
${DC} run --rm evidence python scripts/agent_readiness.py || { echo -e "${RED}? Readiness script failed${NC}"; exit 1; }

echo -e "\n${YELLOW}?? RUNNING UNIT TESTS...${NC}";
${DC} run --rm evidence pytest -q tests/test_tracks.py || { echo -e "${RED}? Track tests failed${NC}"; exit 1; }

echo -e "\n${GREEN}?? SOVEREIGN SYSTEM INTEGRATION COMPLETE. ALL SYSTEMS GO.${NC}"