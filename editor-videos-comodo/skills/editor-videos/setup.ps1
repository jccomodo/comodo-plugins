# setup.ps1 — prepara o computador para editar os vídeos da Cômodo (Windows). Só na 1ª vez.
# Uso: powershell -ExecutionPolicy Bypass -File setup.ps1
# Confere Python e ffmpeg, instala as bibliotecas (Whisper local, MediaPipe, OpenCV, Playwright) e confere o auto-editor.
$ErrorActionPreference = "Continue"
$falta = @()
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { $falta += "Python 3.12 (python.org, marcar 'Add to PATH')" }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { $falta += "ffmpeg (winget install Gyan.FFmpeg)" }
if ($py) {
  & $py.Source -m pip install --quiet --disable-pip-version-check faster-whisper mediapipe opencv-python numpy pillow playwright
  & $py.Source -m playwright install chromium
}
$ae = Join-Path $env:USERPROFILE "Claude\tools\auto-editor\auto-editor.exe"
if (-not (Test-Path $ae)) { $falta += "auto-editor 31.8+ (só para a decupagem): baixe a versão Windows em github.com/WyattBlue/auto-editor/releases e salve como $ae" }
New-Item -ItemType Directory -Force (Join-Path $env:USERPROFILE "Claude\ENTREGAS") | Out-Null
Write-Output ""
if ($falta.Count) { Write-Output ("FALTA INSTALAR: " + ($falta -join "; ")) } else { Write-Output "OK: tudo pronto para editar." }
Write-Output "Fontes: a pasta assets\fonts desta skill tem a Poppins; copie para fonts\ de cada projeto de vídeo."
