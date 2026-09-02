# Carga la imagen portable de la demo y la imagen MySQL incluida.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\docker_demo_load.ps1

param(
    [string]$Archive = "vitalxai-demo-1.0.tar"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path -LiteralPath $Archive)) {
    throw "Falta el archivo de imagen: $Archive"
}

& docker load --input $Archive
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo cargar el archivo de imágenes."
}

foreach ($image in @("vitalxai-demo:1.0", "mysql:8.4")) {
    & docker image inspect $image *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "La imagen no está disponible después de cargar el archivo: $image"
    }
}

Write-Host "Imagen de aplicación y MySQL cargadas correctamente." -ForegroundColor Green
