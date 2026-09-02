# Construye y exporta la imagen portable para la defensa.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\docker_demo_build.ps1

param(
    [string]$Tag = "vitalxai-demo:1.0",
    [string]$Platform = "linux/amd64"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if ($Platform -ne "linux/amd64") {
    throw "Esta configuración de demo se valida y transporta como linux/amd64."
}

& "$PSScriptRoot\docker_demo_validate.ps1"

foreach ($requiredPath in @(
        "Dockerfile",
        "compose.yaml",
        "demo-models\DenseNet121\best_fold1.keras",
        "demo-models\EfficientNetB0\best_fold1.keras",
        "demo-data\NORMAL",
        "demo-data\PNEUMONIA",
        "demo-cache\keras\models\mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5",
        "demo-cache\keras\models\densenet121_weights_tf_dim_ordering_tf_kernels_notop.h5",
        "demo-cache\keras\models\efficientnetb0_notop.h5"
    )) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Falta el recurso requerido: $requiredPath"
    }
}

Write-Host "Validando Compose..." -ForegroundColor Cyan
& docker compose --env-file .env.demo config --quiet
if ($LASTEXITCODE -ne 0) {
    throw "La configuración Compose no es válida."
}

Write-Host "Construyendo $Tag para $Platform..." -ForegroundColor Cyan
& docker buildx build --platform $Platform --tag $Tag --tag "vitalxai-demo:1.0" --load .
if ($LASTEXITCODE -ne 0) {
    throw "La construcción de la imagen ha fallado."
}

$safeTag = $Tag.Replace(":", "-").Replace("/", "-")
$archive = Join-Path $ProjectRoot "$safeTag.tar"
& docker image inspect "mysql:8.4" *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Descargando la imagen MySQL para incluirla en el paquete..." -ForegroundColor Cyan
    & docker pull "mysql:8.4"
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo obtener la imagen mysql:8.4."
    }
}
Write-Host "Exportando imagen a $archive..." -ForegroundColor Cyan
& docker save --output $archive "vitalxai-demo:1.0" "mysql:8.4"
if ($LASTEXITCODE -ne 0) {
    throw "La exportación de la imagen ha fallado."
}

Write-Host "Imagen preparada: $archive" -ForegroundColor Green
