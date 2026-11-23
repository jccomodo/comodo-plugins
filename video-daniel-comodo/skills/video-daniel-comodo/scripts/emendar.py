"""Troca uma frase dentro de uma narração pronta, sem regravar o resto.

Uso:
  python emendar.py BASE.mp3 TRECHO.mp3 INICIO FIM SAIDA.mp3 [--antes 0.25] [--depois 0.25]

- INICIO / FIM: segundos do trecho a substituir em BASE (pegue com transcrever.py; corte um pouco
  antes da primeira palavra e um pouco depois da última, dentro do silêncio).
- TRECHO: a frase nova (gerada com narrar.js --frase, com --antes/--depois de contexto).
  O silêncio do começo e do fim do trecho é removido automaticamente.
- --antes / --depois: silêncio (s) colocado antes e depois da frase nova.
- O volume da frase nova é igualado ao do trecho original (LUFS), com fades curtos nas emendas.
"""
import argparse, os, re, subprocess, tempfile

p = argparse.ArgumentParser()
p.add_argument("base"); p.add_argument("trecho"); p.add_argument("inicio", type=float); p.add_argument("fim", type=float)
p.add_argument("saida"); p.add_argument("--antes", type=float, default=0.25); p.add_argument("--depois", type=float, default=0.25)
a = p.parse_args()

def lufs(args):
    r = subprocess.run(["ffmpeg", "-v", "info", *args, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1])

tmp = tempfile.mkdtemp()
limpo = os.path.join(tmp, "limpo.wav")
# tira silêncio do começo e do fim da frase nova
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.trecho, "-af",
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse",
                "-ar", "44100", "-ac", "1", limpo], check=True)
ganho = lufs(["-ss", str(a.inicio), "-t", str(a.fim - a.inicio), "-i", a.base]) - lufs(["-i", limpo])
fc = ("[0:a]aformat=sample_rates=44100:channel_layouts=mono,asplit=2[a][b];"
      f"[a]atrim=0:{a.inicio},asetpts=N/SR/TB,afade=t=out:st={max(a.inicio - 0.03, 0)}:d=0.03[p1];"
      f"[b]atrim={a.fim},asetpts=N/SR/TB,afade=t=in:d=0.03[p3];"
      f"[1:a]volume={ganho:.2f}dB,afade=t=in:d=0.01,areverse,afade=t=in:d=0.03,areverse[mid];"
      "[p1][2:a][mid][3:a][p3]concat=n=5:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.base, "-i", limpo,
                "-f", "lavfi", "-t", str(a.antes), "-i", "anullsrc=r=44100:cl=mono",
                "-f", "lavfi", "-t", str(a.depois), "-i", "anullsrc=r=44100:cl=mono",
                "-filter_complex", fc, "-map", "[o]", "-b:a", "192k", a.saida], check=True)
print(f"ok {a.saida} (ganho {ganho:+.1f} dB)")
