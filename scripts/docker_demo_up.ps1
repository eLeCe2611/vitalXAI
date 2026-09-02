# Arranca la demo Docker usando siempre el entorno de demo.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\docker_demo_up.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

& "$PSScriptRoot\docker_demo_validate.ps1"

foreach ($image in @("vitalxai-demo:1.0", "mysql:8.4")) {
    & docker image inspect $image *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Falta la imagen $image. Ejecuta docker_demo_build.ps1 o docker_demo_load.ps1."
    }
}

& docker compose --env-file .env.demo up -d
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo arrancar la demo."
}

$appId = (& docker compose --env-file .env.demo ps -q app).Trim()
$healthy = $false
for ($i = 0; $i -lt 90; $i++) {
    $health = (& docker inspect --format '{{.State.Health.Status}}' $appId 2>$null).Trim()
    if ($health -eq "healthy") {
        $healthy = $true
        break
    }
    if ($health -eq "unhealthy") {
        & docker compose --env-file .env.demo logs --tail=100 app
        throw "La aplicación quedó unhealthy."
    }
    Start-Sleep -Seconds 2
}

& docker compose --env-file .env.demo ps
if (-not $healthy) {
    & docker compose --env-file .env.demo logs --tail=100 app
    throw "La aplicación no alcanzó el estado healthy en 180 segundos."
}

Write-Host "Demo disponible en http://localhost:8000" -ForegroundColor Green
Write-Host "Logs: docker compose --env-file .env.demo logs -f app" -ForegroundColor DarkGray
