param(
  [string]$Root = "C:\Users\andyj",
  [string[]]$Repos = @('source/repos/PrecisePointway/master','source/repos/Blade2AI'),
  [switch]$SkipClone,
  [string]$Org = 'PrecisePointway'
)
$ErrorActionPreference='Continue'
Write-Host "=== Sovereign IDE Bootstrap ===" -ForegroundColor Cyan
if(-not $SkipClone){
  Write-Host "[Phase] Cloning Repos" -ForegroundColor Magenta
  foreach($r in $Repos){
    $dest = Join-Path $Root $r
    if(Test-Path $dest){ Write-Host "[SKIP] $r exists" -ForegroundColor DarkYellow; continue }
    $leaf = Split-Path $r -Leaf
    $url = "https://github.com/$Org/$leaf.git"
    Write-Host "Cloning $url -> $dest" -ForegroundColor Gray
    git clone $url $dest
  }
}
Write-Host "[Phase] Discover Solutions" -ForegroundColor Magenta
$solutions = Get-ChildItem -Path $Root -Recurse -Filter *.sln -ErrorAction SilentlyContinue
if(-not $solutions){ Write-Warning "No .sln files found under $Root" } else { $solutions | ForEach-Object { Write-Host "Found: $($_.FullName)" } }
Write-Host "[Phase] Launch Solutions" -ForegroundColor Magenta
foreach($s in $solutions){ Start-Process $s.FullName }
Write-Host "[Phase] Healthcheck (placeholder)" -ForegroundColor Magenta
if(Test-Path "scripts/Healthcheck.ps1"){ & scripts/Healthcheck.ps1 } else { Write-Host "No Healthcheck.ps1 present" -ForegroundColor Yellow }
Write-Host "[Phase] Ledger Audit (placeholder)" -ForegroundColor Magenta
if(Test-Path "scripts/Ledger-Audit.ps1"){ & scripts/Ledger-Audit.ps1 } else { Write-Host "No Ledger-Audit.ps1 present" -ForegroundColor Yellow }
Write-Host "Bootstrap complete." -ForegroundColor Green
