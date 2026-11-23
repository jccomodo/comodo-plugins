#!/usr/bin/env bash
# setup.sh — prepara o Mac para editar os vídeos da Cômodo. Só na 1ª vez.
falta=()
command -v python3 >/dev/null || falta+=("Python 3 (python.org)")
command -v ffmpeg >/dev/null || falta+=("ffmpeg 7+ (brew install ffmpeg)")
if command -v ffmpeg >/dev/null; then fv=$(ffmpeg -version | head -1 | grep -oE 'version n?[0-9]+' | grep -oE '[0-9]+'); [ "${fv:-0}" -ge 7 ] 2>/dev/null || falta+=("ffmpeg 7+ (o seu é $fv)"); fi
if command -v python3 >/dev/null; then
  python3 -m pip install -q --disable-pip-version-check faster-whisper mediapipe opencv-python numpy pillow playwright || falta+=("bibliotecas do Python (pip deu erro)")
  python3 -m playwright install chromium
  echo "Baixando o Whisper medium (~1,5 GB, só na 1ª vez)..."
  python3 -c "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu', compute_type='int8')" || falta+=("modelo Whisper medium")
fi
command -v auto-editor >/dev/null || [ -x "$HOME/Claude/tools/auto-editor/auto-editor" ] || falta+=("auto-editor 31.8+ (só para a decupagem): github.com/WyattBlue/auto-editor/releases")
mkdir -p "$HOME/Claude/ENTREGAS"
echo
if [ ${#falta[@]} -gt 0 ]; then echo "FALTA INSTALAR: ${falta[*]}"; else echo "OK: tudo pronto para editar."; fi
