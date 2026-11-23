# setup.ps1 — prepara o computador para os vídeos do clone do Daniel (Windows).
# Uso: powershell -ExecutionPolicy Bypass -File setup.ps1
# Cria %USERPROFILE%\Comodo-Videos-Daniel com o .env (chaves em branco), confere Node, Python e ffmpeg
# e instala o Whisper local (faster-whisper). Nunca sobrescreve um .env que já existe.
$ErrorActionPreference = "Continue"
$dest = Join-Path $env:USERPROFILE "Comodo-Videos-Daniel"
New-Item -ItemType Directory -Force $dest | Out-Null
$envFile = Join-Path $dest ".env"
if (-not (Test-Path $envFile)) {
  @'
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_A=
ELEVENLABS_MODEL_A=eleven_v4
ELEVENLABS_SETTINGS_A={"stability":0.1,"similarity_boost":0.88}
HEYGEN_API_KEY=
'@ | Out-File -Encoding utf8 $envFile
}
$falta = @()
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { $falta += "Node.js LTS (nodejs.org)" }
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { $falta += "Python 3.12 (python.org, marcar 'Add to PATH')" }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { $falta += "ffmpeg (winget install Gyan.FFmpeg)" }
if ($py) { & $py.Source -m pip install --quiet --disable-pip-version-check faster-whisper playwright pillow numpy; & $py.Source -m playwright install chromium }
Write-Output ""
Write-Output "PASTA: $dest"
if ($falta.Count) { Write-Output ("FALTA INSTALAR: " + ($falta -join "; ")) }
$txt = Get-Content $envFile -Raw
foreach ($k in "ELEVENLABS_API_KEY","ELEVENLABS_VOICE_A","HEYGEN_API_KEY") {
  if ($txt -notmatch "(?m)^$k=\S{6,}") { Write-Output "FALTA A CHAVE $k no $envFile" }
}
