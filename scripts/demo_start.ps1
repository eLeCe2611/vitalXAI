# demo_start.ps1 - Arranca servidor + tunel para la demo en vivo
# Uso: powershell -ExecutionPolicy Bypass -File scripts\demo_start.ps1 [-Tunnel cloudflared|ngrok]

param(
    [string]$Tunnel = ""
)

$ErrorActionPreference = "Continue"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

function Get-EnvVar([string]$Name) {
    $envFile = Join-Path $ProjectRoot ".env"
    if (Test-Path $envFile) {
        $line = Get-Content $envFile | Where-Object { $_ -match "^\s*$([regex]::Escape($Name))\s*=" } | Select-Object -First 1
        if ($line) {
            return ($line -split "=", 2)[1].Trim().Trim('"').Trim("'")
        }
    }
    return ""
}

Write-Host ""
Write-Host "=== vitalXAI - Demo en vivo ===" -ForegroundColor Cyan
Write-Host "Directorio de trabajo: $ProjectRoot"

# Limpia una URL publica obsoleta de una ejecucion anterior
if (Test-Path "$ProjectRoot\demo_url.txt") { Remove-Item "$ProjectRoot\demo_url.txt" -Force }

# --- Prechecks ---------------------------------------------------------------
if (Test-Path ".env") {
    Write-Host "[OK] .env encontrado." -ForegroundColor Green
} else {
    Write-Host "[AVISO] No existe .env. Copia .env.example a .env y configuralo." -ForegroundColor Yellow
}

$mysqlUp = Test-NetConnection -ComputerName "localhost" -Port 3306 -InformationLevel Quiet -WarningAction SilentlyContinue
if ($mysqlUp) {
    Write-Host "[OK] MySQL responde en el puerto 3306." -ForegroundColor Green
} else {
    Write-Host "[AVISO] MySQL no responde en 3306. Arranca XAMPP (MySQL en Start) antes de la demo." -ForegroundColor Yellow
}

# --- Proveedor de tunel ------------------------------------------------------
if ($Tunnel -eq "") {
    if ($env:TUNNEL_PROVIDER) {
        $provider = $env:TUNNEL_PROVIDER
    } else {
        $provider = Get-EnvVar "TUNNEL_PROVIDER"
    }
    if ($provider -eq "") { $provider = "cloudflared" }
} else {
    $provider = $Tunnel
}
Write-Host "[OK] Proveedor de tunel: $provider" -ForegroundColor Green

# --- Servidor uvicorn ---------------------------------------------------------
# Fuerza UTF-8 para que main.py imprima emojis sin UnicodeEncodeError al redirigir
$env:PYTHONIOENCODING = "utf-8"
Write-Host "Arrancando uvicorn en 127.0.0.1:8000 (sin reload)..."
$server = Start-Process -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000" `
    -WorkingDirectory $ProjectRoot `
    -RedirectStandardOutput "$ProjectRoot\demo_server.log" `
    -RedirectStandardError "$ProjectRoot\demo_server.err.log" `
    -NoNewWindow -PassThru

Write-Host "Esperando a que el servidor este listo (puede tardar por la carga de TensorFlow)..."
$ready = $false
for ($i = 0; $i -lt 180; $i++) {
    if ($server.HasExited) { break }
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/register" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 500) { $ready = $true; break }
    } catch {
        Start-Sleep -Seconds 1
    }
}
if ($ready) {
    Write-Host "[OK] Servidor listo en http://127.0.0.1:8000" -ForegroundColor Green
} else {
    Write-Host "[AVISO] El servidor no respondio a tiempo. Revisa demo_server.err.log" -ForegroundColor Yellow
}

# --- Tunel -------------------------------------------------------------------
$url = ""
$tunnelProc = $null
if ($provider -eq "ngrok") {
    Write-Host "Arrancando ngrok (http 8000)..."
    $tunnelProc = Start-Process -FilePath "ngrok" -ArgumentList "http", "8000" -WorkingDirectory $ProjectRoot -NoNewWindow -PassThru
    Start-Sleep -Seconds 6
    try {
        $data = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -TimeoutSec 5 -ErrorAction Stop
        $url = ($data.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1).public_url
    } catch {
        Write-Host "[AVISO] No se pudo leer la URL de ngrok. Revisa el dashboard en http://127.0.0.1:4040" -ForegroundColor Yellow
    }
} else {
    Write-Host "Arrancando cloudflared (tunel rapido)..."
    $cloudLog = "$ProjectRoot\demo_tunnel.log"
    $cloudErr = "$ProjectRoot\demo_tunnel.err.log"
    foreach ($f in @($cloudLog, $cloudErr)) { if (Test-Path $f) { Remove-Item $f -Force } }
    $tunnelProc = Start-Process -FilePath "cloudflared" `
        -ArgumentList "tunnel", "--url", "http://localhost:8000" `
        -WorkingDirectory $ProjectRoot `
        -RedirectStandardOutput $cloudLog `
        -RedirectStandardError $cloudErr `
        -NoNewWindow -PassThru
    for ($i = 0; $i -lt 60; $i++) {
        Start-Sleep -Milliseconds 500
        foreach ($f in @($cloudLog, $cloudErr)) {
            if (Test-Path $f) {
                $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
                if ($content -match "https://[a-zA-Z0-9\-]+\.trycloudflare\.com") {
                    $url = $Matches[0]
                    break
                }
            }
        }
        if ($url) { break }
        if ($tunnelProc.HasExited) { break }
    }
}

# --- Resultado ----------------------------------------------------------------
if ($url) {
    Write-Host "Comprobando que la URL publica responde..."
    $reachable = $false
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $resp = Invoke-WebRequest -Uri "$url/register" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
            if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 500) { $reachable = $true; break }
        } catch {
            Start-Sleep -Seconds 2
        }
        if ($tunnelProc.HasExited) { break }
    }
    $url | Out-File -FilePath "$ProjectRoot\demo_url.txt" -Encoding ascii
    Write-Host ""
    Write-Host "==============================================================" -ForegroundColor Cyan
    if ($reachable) {
        Write-Host "  URL PUBLICA DE LA DEMO:" -ForegroundColor Green
        Write-Host "  $url" -ForegroundColor Green
        Write-Host "  (guardada en demo_url.txt - ya responde)" -ForegroundColor DarkGray
    } else {
        Write-Host "  URL DEL TUNEL (sin confirmacion de respuesta):" -ForegroundColor Yellow
        Write-Host "  $url" -ForegroundColor Yellow
        Write-Host "  Si no carga, revisa: servidor local (demo_server.err.log)," -ForegroundColor DarkGray
        Write-Host "  DNS/red y que el tunel siga activo." -ForegroundColor DarkGray
    }
    Write-Host "==============================================================" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "[AVISO] No se pudo obtener la URL publica del tunel." -ForegroundColor Yellow
    Write-Host "La app local sigue en: http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host "Revisa los logs: demo_tunnel.log / demo_tunnel.err.log" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pulsa Enter para detener la demo (se apagaran servidor y tunel)."
Read-Host | Out-Null

# --- Limpieza ----------------------------------------------------------------
if ($tunnelProc -and -not $tunnelProc.HasExited) { Stop-Process -Id $tunnelProc.Id -Force -ErrorAction SilentlyContinue }
if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue }
Write-Host "Demo detenida."
