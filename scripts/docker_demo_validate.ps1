# Valida los artefactos y secretos locales antes de construir, arrancar o empaquetar.

param(
    [switch]$RequireArchive,
    [string]$Archive = "vitalxai-demo-1.0.tar"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

function Get-DemoEnvValue([string]$Name) {
    foreach ($line in Get-Content -LiteralPath ".env.demo") {
        if ($line -match "^\s*$([regex]::Escape($Name))\s*=") {
            return ($line -split "=", 2)[1].Trim().Trim('"').Trim("'")
        }
    }
    return ""
}

if (-not (Test-Path -LiteralPath ".env.demo")) {
    throw "Falta .env.demo. Copia .env.demo.example y configura sus valores."
}

foreach ($name in @("DB_ROOT_PASSWORD", "DB_USER", "DB_PASSWORD", "JWT_SECRET_KEY")) {
    $value = Get-DemoEnvValue $name
    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "$name debe estar configurada en .env.demo."
    }
    if ($value -match "change-this|tu_api_key|genera_una_clave") {
        throw "$name todavía contiene un valor de ejemplo. Cámbialo antes de la demo."
    }
}

if ((Get-DemoEnvValue "DB_USER") -eq "root") {
    throw "DB_USER no debe ser root; usa el usuario de aplicación definido por Compose."
}

$jwtSecret = Get-DemoEnvValue "JWT_SECRET_KEY"
if ($jwtSecret.Length -lt 32) {
    throw "JWT_SECRET_KEY debe tener al menos 32 caracteres."
}

foreach ($path in @(
        "compose.yaml",
        "Dockerfile",
        "demo-models\DenseNet121\best_fold1.keras",
        "demo-models\EfficientNetB0\best_fold1.keras",
        "demo-data\NORMAL",
        "demo-data\PNEUMONIA",
        "demo-cache\keras\models\mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5",
        "demo-cache\keras\models\densenet121_weights_tf_dim_ordering_tf_kernels_notop.h5",
        "demo-cache\keras\models\efficientnetb0_notop.h5"
    )) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Falta el recurso requerido: $path"
    }
}

$normalCount = @(Get-ChildItem -LiteralPath "demo-data\NORMAL" -File | Where-Object { $_.Extension -in @(".jpg", ".jpeg", ".png") }).Count
$pneumoniaCount = @(Get-ChildItem -LiteralPath "demo-data\PNEUMONIA" -File | Where-Object { $_.Extension -in @(".jpg", ".jpeg", ".png") }).Count
if ($normalCount -eq 0 -or $pneumoniaCount -eq 0) {
    throw "demo-data debe contener imágenes en NORMAL y PNEUMONIA."
}

if ($RequireArchive -and -not (Test-Path -LiteralPath $Archive)) {
    throw "Falta el archivo de imagen exportada: $Archive"
}

Write-Host "Artefactos y configuración de demo válidos." -ForegroundColor Green
