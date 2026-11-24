"""Medição objetiva de um vídeo SEM HTML (reels montados no ffmpeg, cortes, cenas do clone). Não corrige nada.
Uso: python valida_mp4.py VIDEO.mp4 [--ass legendas.ass] [--lufs -19.5] [--saida PASTA]
Gera em <pasta do vídeo>/val/: relatorio_mp4.md, folha_mp4.jpg (1 quadro a cada 2 s), palavras_final.json.
Mede: resolução/fps/duração, volume integrado (LUFS) e pico, quadro preto, silêncio no começo/fim,
transcrição do vídeo final e, com --ass, a sincronia legenda x fala (cada palavra deve entrar até 0,25 s da fala)."""
import argparse, json, os, re, subprocess, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--ass"); ap.add_argument("--lufs", type=float, default=-19.5)
ap.add_argument("--saida"); a = ap.parse_args()
OUT = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.video)), "val"); os.makedirs(OUT, exist_ok=True)
run = lambda *c: subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace")
achados = []  # (sev, tipo, detalhe)

info = json.loads(run("ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", a.video).stdout)
dur = float(info["format"]["duration"]); vs = [s for s in info["streams"] if s["codec_type"] == "video"][0]
fps = eval(vs["r_frame_rate"]); temaudio = any(s["codec_type"] == "audio" for s in info["streams"])
if (vs["width"], vs["height"]) not in ((1080, 1920), (1920, 1080)): achados.append(("MÉDIO", "FORMATO", f"{vs['width']}x{vs['height']} (esperado 1080x1920 ou 1920x1080)"))
if abs(fps - 30) > 0.5: achados.append(("LEVE", "FPS", f"{fps:.2f} fps (padrão 30)"))
if not temaudio: achados.append(("GRAVE", "AUDIO", "vídeo sem trilha de áudio"))

lufs = pico = None
if temaudio:
    e = run("ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", e); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    lufs = float(m[-1]) if m else None; pico = float(p[-1]) if p else None
    if lufs is not None and abs(lufs - a.lufs) > 1.5: achados.append(("MÉDIO", "VOLUME", f"{lufs:.1f} LUFS (alvo {a.lufs})"))
    if pico is not None and pico > -0.5: achados.append(("MÉDIO", "PICO", f"pico {pico:.1f} dBFS (estoura)"))
    s = run("ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-").stderr
    for st, en in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", s):
        st, en = float(st), float(en)
        if st < 0.05: achados.append(("LEVE", "SILENCIO", f"começa com {en:.2f} s de silêncio"))
        elif en > dur - 0.05: achados.append(("LEVE", "SILENCIO", f"termina com {dur - st:.2f} s de silêncio"))
        elif en - st > 1.2: achados.append(("MÉDIO", "SILENCIO", f"{en - st:.2f} s parado em {st:.2f} s"))
b = run("ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-an", "-vf", "blackdetect=d=0.1:pix_th=0.08", "-f", "null", "-").stderr
for st, en in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", b): achados.append(("GRAVE", "PRETO", f"quadro preto {float(st):.2f}–{float(en):.2f} s"))

n = max(1, int(dur // 2)); cols = 6
run("ffmpeg", "-y", "-v", "error", "-i", a.video, "-vf", f"fps=1/2,scale=270:-2,tile={cols}x{(n + cols - 1) // cols}", "-frames:v", "1", os.path.join(OUT, "folha_mp4.jpg"))

W = []
if temaudio:
    from faster_whisper import WhisperModel
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(a.video, language="pt", word_timestamps=True)
    W = [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for sg in segs for w in sg.words]
    json.dump([{"words": W}], open(os.path.join(OUT, "palavras_final.json"), "w", encoding="utf-8"), ensure_ascii=False)
    if W and W[0]["s"] > 1.0: achados.append(("MÉDIO", "INICIO", f"primeira palavra só em {W[0]['s']:.2f} s"))
    if W and re.search(r"(\.\.\.|[^.!?])$", W[-1]["w"]): achados.append(("MÉDIO", "FINAL", f"termina sem fechar a frase: \"…{' '.join(x['w'] for x in W[-4:])}\""))

sync = ""
if a.ass and W:
    ts = lambda x: sum(float(v) * k for v, k in zip(x.split(":"), (3600, 60, 1)))
    ev = []
    for l in open(a.ass, encoding="utf-8"):
        if not l.startswith("Dialogue:"): continue
        p = l.rstrip("\n").split(",", 9); txt = re.sub(r"\{[^}]*\}", "", p[9]).strip()
        if "\\p1" in p[9]: continue   # desenho da pílula, não é texto
        for tok in txt.split():
            if len(re.sub(r"[^\wÀ-ÿ]", "", tok)) >= 3: ev.append((ts(p[1]), tok))  # palavras curtas casam errado
    nz = lambda t: re.sub(r"[^\wÀ-ÿ]", "", t.lower())
    ev.sort(); un = []; last = {}
    for t, tok in ev:                                   # cada palavra vira vários eventos (entrada animada): fica o 1º
        if nz(tok) in last and t - last[nz(tok)] < 0.6: last[nz(tok)] = t; continue
        last[nz(tok)] = t; un.append((t, tok))
    d = []; usados = set()
    for t, tok in un:                                   # casa com a mesma palavra falada mais próxima no tempo (±1,5 s)
        cands = [k for k in range(len(W)) if k not in usados and nz(W[k]["w"]) == nz(tok) and abs(W[k]["s"] - t) <= 1.5]
        if cands:
            k = min(cands, key=lambda k: abs(W[k]["s"] - t)); usados.add(k); d.append((tok, round(t - W[k]["s"], 2)))
    if d:
        ruins = [x for x in d if x[1] > 0.25 or x[1] < -0.6]
        sync = f"{len(d)} palavras casadas, desvio médio {sum(x[1] for x in d) / len(d):+.2f} s, {len(ruins)} fora de −0,6…+0,25 s"
        for tok, dv in ruins[:10]: achados.append(("MÉDIO", "SINCRONIA", f"\"{tok}\" entra {dv:+.2f} s da fala"))

ordem = {"GRAVE": 0, "MÉDIO": 1, "LEVE": 2}; achados.sort(key=lambda x: ordem[x[0]])
L = [f"# Medição de {os.path.basename(a.video)}", "", f"- {vs['width']}x{vs['height']}, {fps:.2f} fps, {dur:.2f} s",
     f"- Volume: {lufs} LUFS, pico {pico} dBFS" if temaudio else "- Sem áudio", f"- Sincronia: {sync}" if sync else "- Sincronia: (sem --ass)",
     f"- Transcrição do final: {' '.join(x['w'] for x in W)}" if W else "", "", f"## Achados ({len(achados)})", ""]
L += [f"- **{s}** {t}: {d}" for s, t, d in achados] or ["- nenhum"]
L += ["", "Folha de contato: folha_mp4.jpg. Agora faça o passo 2 (checklist visual) nos quadros."]
open(os.path.join(OUT, "relatorio_mp4.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
