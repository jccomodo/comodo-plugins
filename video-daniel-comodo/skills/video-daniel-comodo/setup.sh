#!/bin/bash
# setup.sh — versão Mac/Linux do setup.ps1. Cria ~/Comodo-Videos-Daniel/.env (chaves em branco),
# confere Node, Python e ffmpeg e instala o Whisper local. Nunca sobrescreve um .env que já existe.
DEST="$HOME/Comodo-Videos-Daniel"; mkdir -p "$DEST"; ENVF="$DEST/.env"
if [ ! -f "$ENVF" ]; then
cat > "$ENVF" <<'EOF'
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_A=
ELEVENLABS_MODEL_A=eleven_v4
ELEVENLABS_VOICE_DAN=
ELEVENLABS_SETTINGS_A={"stability":0.1,"similarity_boost":0.88}
HEYGEN_API_KEY=
EOF
fi
FALTA=""
command -v node >/dev/null || FALTA="$FALTA Node.js LTS (nodejs.org);"
command -v python3 >/dev/null || FALTA="$FALTA Python 3 (python.org);"
command -v ffmpeg >/dev/null || FALTA="$FALTA ffmpeg (brew install ffmpeg);"
command -v python3 >/dev/null && python3 -m pip install --quiet --disable-pip-version-check faster-whisper mediapipe playwright pillow numpy && python3 -m playwright install chromium
echo ""; echo "PASTA: $DEST"
[ -n "$FALTA" ] && echo "FALTA INSTALAR:$FALTA"
for k in ELEVENLABS_API_KEY ELEVENLABS_VOICE_A HEYGEN_API_KEY; do
  grep -Eq "^$k=[^[:space:]]{6,}" "$ENVF" || echo "FALTA A CHAVE $k no $ENVF"
done
