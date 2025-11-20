ORG := PrecisePointway
ROOT := C:/Users/andyj
REPOS := source/repos/PrecisePointway/master source/repos/Blade2AI

.PHONY: all discovery solutions clone bootstrap health audit

all: discovery solutions clone bootstrap health audit

discovery:
	powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Discovery-RepoRemotes.ps1 -Root "$(ROOT)" -Repos $(REPOS)

solutions:
	powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Discovery-Solutions.ps1 -Root "$(ROOT)"

clone:
	powershell -NoProfile -ExecutionPolicy Bypass -Command "foreach($r in '$(REPOS)'.Split(' ')){ $dest = Join-Path '$(ROOT)' $r; if(!(Test-Path $dest)){ $leaf = Split-Path $r -Leaf; git clone https://github.com/$(ORG)/$leaf.git $dest } else { Write-Host '[SKIP] '+$r } }"

bootstrap:
	powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Bootstrap-All.ps1 -Root "$(ROOT)" -Repos $(REPOS) -Org $(ORG)

health:
	powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Healthcheck.ps1

audit:
	powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Ledger-Audit.ps1
