# Reúne todos los artefactos necesarios para transportar la demo.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\docker_demo_package.ps1

param(
    [string]$Archive = "vitalxai-demo-1.0.tar",
    [string]$Output = "vitalXAI-demo-package"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$validator = Join-Path $PSScriptRoot "docker_demo_validate.ps1"
& $validator -RequireArchive -Archive $Archive

$requiredPaths = @(
    $Archive,
    ".env.demo",
    "compose.yaml",
    "README-DEFENSA.md",
    "demo-models",
    "demo-data",
    "demo-cache\keras"
)

foreach ($requiredPath in $requiredPaths) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Falta el recurso requerido: $requiredPath"
    }
}

if (Test-Path -LiteralPath $Output) {
    throw "La carpeta de salida ya existe: $Output. Elimínala o usa otro nombre."
}

New-Item -ItemType Directory -Path $Output | Out-Null
Copy-Item -LiteralPath $Archive -Destination $Output
Copy-Item -LiteralPath ".env.demo" -Destination $Output
Copy-Item -LiteralPath "compose.yaml" -Destination $Output
Copy-Item -LiteralPath "Dockerfile" -Destination $Output
Copy-Item -LiteralPath ".dockerignore" -Destination $Output
Copy-Item -LiteralPath ".env.demo.example" -Destination $Output
Copy-Item -LiteralPath "README-DEFENSA.md" -Destination $Output
Copy-Item -LiteralPath "demo-models" -Destination $Output -Recurse
Copy-Item -LiteralPath "demo-data" -Destination $Output -Recurse
Copy-Item -LiteralPath "demo-cache" -Destination $Output -Recurse

$scriptsOutput = Join-Path $Output "scripts"
New-Item -ItemType Directory -Path $scriptsOutput | Out-Null
Copy-Item -LiteralPath "scripts\docker_demo_build.ps1" -Destination $scriptsOutput
Copy-Item -LiteralPath "scripts\docker_demo_up.ps1" -Destination $scriptsOutput
Copy-Item -LiteralPath "scripts\docker_demo_down.ps1" -Destination $scriptsOutput
Copy-Item -LiteralPath "scripts\docker_demo_load.ps1" -Destination $scriptsOutput
Copy-Item -LiteralPath "scripts\docker_demo_validate.ps1" -Destination $scriptsOutput

if (Test-Path -LiteralPath "database-demo.sql") {
    Copy-Item -LiteralPath "database-demo.sql" -Destination $Output
}

Write-Host "Paquete creado en: $(Join-Path $ProjectRoot $Output)" -ForegroundColor Green
Write-Host "Copia esta carpeta completa al ordenador de la defensa." -ForegroundColor Green
