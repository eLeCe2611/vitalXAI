# Detiene la demo sin borrar datos.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\docker_demo_down.ps1
# Para borrar también los datos: -RemoveData

param(
    [switch]$RemoveData
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if ($RemoveData) {
    & docker compose --env-file .env.demo down -v
} else {
    & docker compose --env-file .env.demo down
}

if ($LASTEXITCODE -ne 0) {
    throw "No se pudo detener la demo."
}
