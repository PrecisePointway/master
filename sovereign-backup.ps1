# SOVEREIGN MIRROR PROTOCOL (PC4)
# Target: Drives E and F

param(
  [string]$Source = "C:\Users\andyj\AI_Agent_Research",
  [string]$DestPrimary = "E:\Sovereign_Backups",
  [string]$DestSecondary = "F:\Sovereign_Backups"
)

$Options = @("/MIR", "/FFT", "/R:3", "/W:5", "/XD", ".git", ".venv", "__pycache__")

Write-Host "?? INITIATING SOVEREIGN BACKUP..." -ForegroundColor Cyan

if (Test-Path "E:\") {
    Write-Host "?? MIRRORING TO DRIVE E..." -ForegroundColor Yellow
    robocopy $Source $DestPrimary $Options
} else {
    Write-Host "? DRIVE E NOT FOUND!" -ForegroundColor Red
}

if (Test-Path "F:\") {
    Write-Host "?? MIRRORING TO DRIVE F..." -ForegroundColor Yellow
    robocopy $Source $DestSecondary $Options
} else {
    Write-Host "? DRIVE F NOT FOUND!" -ForegroundColor Red
}

Write-Host "? SOVEREIGNTY SECURED." -ForegroundColor Green
