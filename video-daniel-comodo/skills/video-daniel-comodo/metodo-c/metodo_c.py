"""Método C (tela dividida 1080x1920): animação em cima (0-960), Daniel embaixo (960-1920), pílula laranja na emenda.

Uso (sempre na ordem):
  python metodo_c.py preparar VIDEO_VERTICAL.mp4 PASTA       -> copia o vídeo, os assets e o HTML de exemplo, transcreve,
                                                               gera palavras.json, chunks.js e guia.jpg (quadro para medir o rosto)
  python metodo_c.py daniel PASTA --cabelo Y --rosto-x X [--zoom 1.25]
                                                            -> recorta o Daniel (Y = topo do cabelo e X = centro do rosto,
                                                               em pixels do vídeo 1080x1920; meça no guia.jpg, que está em 1/2)
  (escreva as cenas em PASTA/overlay.html)
  python metodo_c.py teste PASTA 1.0,3.5,8.2                -> quadros soltos t_NN.png (topo) e p_NN.png (pílula) + folha_teste.jpg
  python metodo_c.py quadros PASTA [top,pill]               -> renderiza todos os quadros (30 fps)
  python metodo_c.py sfx PASTA --soft 0,1.5 --tick 3.1 --swish 4.5
  python metodo_c.py montar PASTA SAIDA.mp4                 -> junta tudo, áudio -14 LUFS + sfx, confere sincronia e gera folha_final.jpg
Nada aqui gasta créditos: o vídeo da HeyGen já precisa existir (formato B, Podcast Vertical, 9:16).
"""
import argparse, json, os, re, shutil, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
FPS = 30

def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())

# ---------------- preparar ----------------
def preparar(a):
    os.makedirs(a.pasta, exist_ok=True)
    shutil.copy(a.video, os.path.join(a.pasta, "base.mp4"))
    dst = os.path.join(a.pasta, "assets")
    if not os.path.exists(dst): shutil.copytree(os.path.join(AQUI, "assets"), dst)
    ov = os.path.join(a.pasta, "overlay.html")
    if not os.path.exists(ov): shutil.copy(os.path.join(AQUI, "exemplo_cena.html"), ov)
    base = os.path.join(a.pasta, "base.mp4"); D = dur(base)
    ff("-i", base, "-vn", "-ac", "1", "-ar", "16000", os.path.join(a.pasta, "a16.wav"))
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(os.path.join(a.pasta, "a16.wav"), language="pt", word_timestamps=True)  # sem initial_prompt: ele faz pular o começo
    W = [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]
    json.dump([{"words": W}], open(os.path.join(a.pasta, "palavras.json"), "w", encoding="utf-8"), ensure_ascii=False)
    chunks(a.pasta, D)
    ff("-ss", str(D / 2), "-i", base, "-frames:v", "1", "-vf", "scale=540:960", os.path.join(a.pasta, "guia.jpg"))
    print("ok: %.2f s, %d palavras. Confira palavras.json (corrija grafias e rode 'chunks'), meça o guia.jpg e rode 'daniel'." % (D, len(W)))

def chunks(pasta, D=None):
    """Pílula: 1-3 palavras, até 20 caracteres, quebra em pontuação ou pausa > 0,45 s."""
    D = D or dur(os.path.join(pasta, "base.mp4"))
    W = []
    for s in json.load(open(os.path.join(pasta, "palavras.json"), encoding="utf-8-sig")): W += s["words"]
    clean = lambda t: re.sub(r"[^\wÀ-ÿ]", "", t.lower())
    NOEND = {"a","o","as","os","um","uma","de","da","do","das","dos","em","no","na","nos","nas","por","pra","para","com","que","e","ou","mas","se","ao","à","seu","sua","mais","já","só","é","cada"}
    disp = lambda i: re.sub(r"[.,;:!?]+$", "", W[i]["w"]) + ("?" if W[i]["w"].endswith("?") else "")
    segs, cur = [], []
    for i, w in enumerate(W):
        if cur and (re.search(r"[.?!]$", W[cur[-1]]["w"]) or (re.search(r"[,;:]$", W[cur[-1]]["w"]) and len(cur) >= 2) or w["s"] - W[cur[-1]]["e"] > 0.45):
            segs.append(cur); cur = []
        cur.append(i)
    if cur: segs.append(cur)
    out = []
    for sg in segs:
        n = len(sg); INF = 1e9; best = [INF] * (n + 1); prv = [0] * (n + 1); best[0] = 0
        for q in range(1, n + 1):
            for p in range(max(0, q - 3), q):
                ws = sg[p:q]; txt = " ".join(disp(i) for i in ws)
                if len(txt) > 20: continue
                c = ((len(txt) - 13) ** 2) / 6
                if clean(W[ws[-1]]["w"]) in NOEND and q < n: c += 40
                if q - p == 1 and n > 1: c += 6
                if best[p] + c < best[q]: best[q] = best[p] + c; prv[q] = p
        q = n; parts = []
        while q > 0: parts.append((prv[q], q)); q = prv[q]
        for p, q in reversed(parts):
            ws = sg[p:q]
            out.append(dict(t0=round(max(0, W[ws[0]]["s"] - 0.06), 2), t1=round(W[ws[-1]]["e"] + 0.30, 2),
                            words=[dict(w=disp(i), t=round(max(0, W[i]["s"] - 0.04), 2)) for i in ws]))
    for k in range(len(out) - 1): out[k]["t1"] = min(out[k]["t1"], out[k + 1]["t0"])
    open(os.path.join(pasta, "chunks.js"), "w", encoding="utf-8").write("const DUR=%.3f;\nconst CHUNKS=%s;" % (D, json.dumps(out, ensure_ascii=False)))
    print(len(out), "chunks:", " | ".join("%.2f %s" % (c["t0"], " ".join(w["w"] for w in c["words"])) for c in out))

# ---------------- Daniel embaixo ----------------
def daniel(a):
    """Amplia o vídeo vertical e recorta 1080x960 com o topo do cabelo ~66 px abaixo da emenda e o rosto no centro."""
    z = a.zoom; W, H = round(1080 * z), round(1920 * z)
    x = int(min(max(a.rosto_x * z - 540, 0), W - 1080)); y = int(min(max(a.cabelo * z - 66, 0), H - 960))
    ff("-i", os.path.join(a.pasta, "base.mp4"), "-an", "-vf", f"scale={W}:{H}:flags=lanczos,crop=1080:960:{x}:{y},fps={FPS}",
       "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", os.path.join(a.pasta, "daniel.mp4"))
    ff("-ss", "3", "-i", os.path.join(a.pasta, "daniel.mp4"), "-frames:v", "1", os.path.join(a.pasta, "daniel_quadro.jpg"))
    print("ok daniel.mp4 (zoom %.2f, crop x=%d y=%d). Confira daniel_quadro.jpg: cabelo logo abaixo do topo, rosto centralizado." % (z, x, y))

# ---------------- render (Playwright) ----------------
def _browser(pw):
    try: return pw.chromium.launch(args=["--disable-gpu", "--allow-file-access-from-files"])
    except Exception:
        exe = [os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser(os.path.join("~", ".cache", "puppeteer"))) for f in fs if f in ("chrome.exe", "chrome")]
        return pw.chromium.launch(executable_path=exe[0], args=["--disable-gpu", "--allow-file-access-from-files"])

def _page(br, pasta, layer):
    pg = br.new_page(viewport={"width": 1080, "height": 1920})
    pg.on("pageerror", lambda e: print("ERRO no HTML:", e))
    pg.goto("file:///" + os.path.abspath(os.path.join(pasta, "overlay.html")).replace("\\", "/") + "?layer=" + layer)
    pg.wait_for_function("window.READY===1", timeout=30000); return pg

def teste(a):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    ts = [float(x) for x in a.tempos.split(",")]
    with sync_playwright() as pw:
        br = _browser(pw); pt = _page(br, a.pasta, "top"); pp = _page(br, a.pasta, "pill")
        for i, t in enumerate(ts):
            pt.evaluate("t=>window.render(t)", t); pt.screenshot(path=os.path.join(a.pasta, "t_%02d.png" % i), clip={"x": 0, "y": 0, "width": 1080, "height": 960})
            pp.evaluate("t=>window.render(t)", t); pp.screenshot(path=os.path.join(a.pasta, "p_%02d.png" % i), omit_background=True)
        br.close()
    n = len(ts); cols = min(5, n); rows = (n + cols - 1) // cols
    sh = Image.new("RGB", (360 * cols, 373 * rows), "white")
    for i in range(n):
        im = Image.open(os.path.join(a.pasta, "t_%02d.png" % i)).convert("RGB").resize((360, 320))
        p = Image.open(os.path.join(a.pasta, "p_%02d.png" % i)).crop((0, 880, 1080, 1040)).resize((360, 53))
        sh.paste(im, ((i % cols) * 360, (i // cols) * 373)); sh.paste(p, ((i % cols) * 360, (i // cols) * 373 + 320), p)
    sh.save(os.path.join(a.pasta, "folha_teste.jpg")); print("ok folha_teste.jpg")

def quadros(a):
    from playwright.sync_api import sync_playwright
    D = dur(os.path.join(a.pasta, "base.mp4"))
    with sync_playwright() as pw:
        br = _browser(pw)
        for layer in a.camadas.split(","):
            out = os.path.join(a.pasta, "fr_" + layer); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
            pg = _page(br, a.pasta, layer)
            for i in range(int(round(D * FPS))):
                pg.evaluate("t=>window.render(t)", i / FPS)
                clip = {"x": 0, "y": 0, "width": 1080, "height": 960} if layer == "top" else {"x": 0, "y": 900, "width": 1080, "height": 120}
                pg.screenshot(path=os.path.join(out, "%05d.png" % (i + 1)), clip=clip, omit_background=(layer == "pill"))
            pg.close(); print("ok", layer)
        br.close()

# ---------------- efeitos sonoros ----------------
def sfx(a):
    import numpy as np, wave
    SR = 44100; D = dur(os.path.join(a.pasta, "base.mp4")) + .3; s = np.zeros(int(SR * D), np.float32); rng = np.random.default_rng(3)
    def add(t, y, g):
        i = int(t * SR); y = (y * g).astype(np.float32); n = min(len(y), len(s) - i)
        if i >= 0 and n > 0: s[i:i + n] += y[:n]
    def soft(d=.13, f0=560):
        n = int(SR * d); t = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 22) + 240) / SR) * np.exp(-t * 24)
    def swish(d=.3):
        n = int(SR * d); x = rng.standard_normal(n); env = np.sin(np.linspace(0, np.pi, n)) ** 2; k = np.linspace(.03, .28, n); y = np.zeros(n); lp = 0
        for j in range(n): lp += k[j] * (x[j] - lp); y[j] = lp
        return y * env * 1.3
    def tick(d=.05):
        n = int(SR * d); t = np.arange(n) / SR; return (np.sin(2 * np.pi * 1900 * t) * .5 + rng.standard_normal(n) * .2) * np.exp(-t * 110)
    lst = lambda v: [float(x) for x in v.split(",")] if v else []
    for t in lst(a.soft): add(t, soft(), .28)
    for t in lst(a.tick): add(t, tick(), .45)
    for t in lst(a.swish): add(t, swish(), .30)
    with wave.open(os.path.join(a.pasta, "sfx.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(s, -1, 1) * 32767).astype(np.int16).tobytes())
    print("ok sfx.wav")

# ---------------- montar ----------------
def montar(a):
    import numpy as np
    P = lambda f: os.path.join(a.pasta, f); D = dur(P("base.mp4"))
    # vídeo e áudio em comandos separados (filtro pesado no mesmo comando já derrubou áudio)
    ff("-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}:d={D}", "-i", P("daniel.mp4"),
       "-framerate", str(FPS), "-i", P("fr_top/%05d.png"), "-framerate", str(FPS), "-i", P("fr_pill/%05d.png"),
       "-filter_complex", "[0:v][1:v]overlay=0:960:shortest=1[b1];[b1][2:v]overlay=0:0[b2];[b2][3:v]overlay=0:900:format=auto,format=yuv420p[v]",
       "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-t", str(D), P("v.mp4"))
    if os.path.exists(P("sfx.wav")):
        ff("-i", P("base.mp4"), "-i", P("sfx.wav"), "-filter_complex",
           "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a0];[1:a]aresample=48000,volume=0.9[a1];[a0][a1]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]",
           "-map", "[a]", "-c:a", "aac", "-b:a", "192k", P("a.m4a"))
    else:
        ff("-i", P("base.mp4"), "-vn", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", P("a.m4a"))
    ff("-i", P("v.mp4"), "-i", P("a.m4a"), "-c", "copy", "-shortest", a.saida)
    def env(f):
        b = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout
        x = np.abs(np.frombuffer(b, np.float32)); return np.array([x[i:i + 80].mean() for i in range(0, len(x) - 80, 80)])
    x = env(P("base.mp4")); y = env(a.saida); n = min(len(x), len(y)); x = x[:n] - x[:n].mean(); y = y[:n] - y[:n].mean()
    k = max(range(-50, 51), key=lambda k: np.dot(x[max(0, k):n + min(0, k)], y[max(0, -k):n - max(0, k)]))
    N = int(D * FPS); sel = "+".join("eq(n\\,%d)" % int(N * (i + .5) / 8) for i in range(8))
    ff("-i", a.saida, "-vf", f"select='{sel}',scale=270:480,tile=4x2", "-frames:v", "1", P("folha_final.jpg"))
    print("ok %s (%.2f s). Deslocamento do áudio: %.2f s (tem que ser 0,00). Veja folha_final.jpg." % (a.saida, dur(a.saida), k * 0.01))

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest="cmd", required=True)
p = sp.add_parser("preparar"); p.add_argument("video"); p.add_argument("pasta"); p.set_defaults(f=preparar)
p = sp.add_parser("chunks"); p.add_argument("pasta"); p.set_defaults(f=lambda a: chunks(a.pasta))
p = sp.add_parser("daniel"); p.add_argument("pasta"); p.add_argument("--cabelo", type=float, required=True); p.add_argument("--rosto-x", type=float, required=True); p.add_argument("--zoom", type=float, default=1.25); p.set_defaults(f=daniel)
p = sp.add_parser("teste"); p.add_argument("pasta"); p.add_argument("tempos"); p.set_defaults(f=teste)
p = sp.add_parser("quadros"); p.add_argument("pasta"); p.add_argument("camadas", nargs="?", default="top,pill"); p.set_defaults(f=quadros)
p = sp.add_parser("sfx"); p.add_argument("pasta"); p.add_argument("--soft"); p.add_argument("--tick"); p.add_argument("--swish"); p.set_defaults(f=sfx)
p = sp.add_parser("montar"); p.add_argument("pasta"); p.add_argument("saida"); p.set_defaults(f=montar)
a = ap.parse_args(); a.f(a)
