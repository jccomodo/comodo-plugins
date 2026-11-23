﻿# setup.ps1 — prepara o computador para editar os vídeos da Cômodo (Windows). Só na 1ª vez.
# Uso: powershell -ExecutionPolicy Bypass -File setup.ps1
# Confere Python e ffmpeg (7 ou mais novo), instala as bibliotecas, baixa o Whisper medium (≈1,5 GB) e confere o auto-editor.
$ErrorActionPreference = "Continue"
$falta = @()
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { $falta += "Python 3.12 (python.org, marcar 'Add to PATH')" }
$ff = (Get-Command ffmpeg -ErrorAction SilentlyContinue)
if (-not $ff) { $falta += "ffmpeg 7 ou mais novo (winget install Gyan.FFmpeg)" }
else {
  $v = (& ffmpeg -hide_banner -version | Select-Object -First 1)
  if ($v -match "version (n)?(\d+)\." -and [int]$Matches[2] -lt 7) { $falta += "ffmpeg 7 ou mais novo (o seu: $v). Atualize: winget upgrade Gyan.FFmpeg" }
}
if ($py) {
  Write-Output "Instalando bibliotecas (pode levar alguns minutos)..."
  & $py.Source -m pip install --disable-pip-version-check -q faster-whisper mediapipe opencv-python numpy pillow playwright
  if ($LASTEXITCODE -ne 0) { $falta += "bibliotecas do Python: o pip deu erro (veja as mensagens acima)" }
  & $py.Source -m playwright install chromium
  Write-Output "Baixando o modelo de transcrição Whisper medium (≈1,5 GB, só na 1ª vez)..."
  & $py.Source -c "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu', compute_type='int8'); print('Whisper medium pronto')"
  if ($LASTEXITCODE -ne 0) { $falta += "modelo Whisper medium (sem internet? rode o setup de novo)" }
}
$ae = Join-Path $env:USERPROFILE "Claude\tools\auto-editor\auto-editor.exe"
if (-not (Test-Path $ae)) { $falta += "auto-editor 31.8+ (só para a decupagem): baixe a versão Windows em github.com/WyattBlue/auto-editor/releases e salve como $ae" }
New-Item -ItemType Directory -Force (Join-Path $env:USERPROFILE "Claude\ENTREGAS") | Out-Null
Write-Output ""
if ($falta.Count) { Write-Output ("FALTA INSTALAR: " + ($falta -join "; ")) } else { Write-Output "OK: tudo pronto para editar." }
Write-Output "Fontes: a pasta assets\fonts desta skill tem a Poppins; copie para fonts\ de cada projeto de vídeo."
