#!/usr/bin/env bash
# setup.sh — prepara o Mac para editar os vídeos da Cômodo. Só na 1ª vez.
falta=()
command -v python3 >/dev/null || falta+=("Python 3 (python.org)")
command -v ffmpeg >/dev/null || falta+=("ffmpeg (brew install ffmpeg)")
if command -v python3 >/dev/null; then
  python3 -m pip install --quiet --disable-pip-version-check faster-whisper mediapipe opencv-python numpy pillow playwright && python3 -m playwright install chromium
fi
command -v auto-editor >/dev/null || [ -x "$HOME/Claude/tools/auto-editor/auto-editor" ] || falta+=("auto-editor 31.8+ (só para a decupagem): github.com/WyattBlue/auto-editor/releases")
mkdir -p "$HOME/Claude/ENTREGAS"
echo
if [ ${#falta[@]} -gt 0 ]; then echo "FALTA INSTALAR: ${falta[*]}"; else echo "OK: tudo pronto para editar."; fi
