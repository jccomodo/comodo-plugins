"""Tempo de cada palavra de uma narração (Whisper local, nada sobe para a internet).
Uso: python transcrever.py AUDIO.mp3 [--modelo medium]
Serve para achar INICIO/FIM antes de emendar uma frase e para conferir pausas."""
import argparse
from faster_whisper import WhisperModel

p = argparse.ArgumentParser(); p.add_argument("audio"); p.add_argument("--modelo", default="medium")
a = p.parse_args()
m = WhisperModel(a.modelo, device="cpu", compute_type="int8")
segs, _ = m.transcribe(a.audio, language="pt", word_timestamps=True)
for s in segs:
    for w in s.words:
        print(f"{w.start:6.2f} {w.end:6.2f} {w.word.strip()}")
