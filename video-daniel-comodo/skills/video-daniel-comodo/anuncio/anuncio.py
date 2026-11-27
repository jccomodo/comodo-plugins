"""Edição de ANÚNCIO (ADS) do clone do Daniel — vídeo B vertical da HeyGen -> REELS simples ou STORY estilo B.
Nada aqui gasta crédito. Comandos (PASTA = pasta de edição do anúncio, ex.: <anuncio>/edit):

  novo VIDEO_B.mp4 PASTA                 copia o modelo, transcreve (palavras.json) e monta o overlay de exemplo
  reaproveitar EDIT_ANTIGO VIDEO.mp4 PASTA
                                         mesma edição sobre narração nova (outra voz/take): copia builds e overlay,
                                         transcreve e grava tmap.json (tempos antigos -> novos)
  overlay PASTA                          remonta overlay.html (overlay_head + overlay_mods.js + overlay_tail)
  frames PASTA                           renderiza o overlay do STORY (frames2_content / frames2_mask), 6 processos
  render PASTA story|reels               gera legendas/sons/filtro e o MP4 (saida_STORY.mp4 / saida_REELS.mp4)
  censura PASTA --palavra merda [--formato story|reels] [--a T --b T]
                                         acha a palavra, mede o pi pelo volume da voz e a boca no vídeo JÁ renderizado,
                                         grava censura.json. Depois rode o render de novo.
"""
import argparse, glob, json, math, os, re, shutil, subprocess, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__)); MOD = os.path.join(AQUI, "modelo")
PY = sys.executable
nz = lambda x: re.sub(r"[^\wÀ-ÿ]", "", x.lower())
ARQS = ["build_story_b.py", "build_reels.py", "legendas_designer.py", "rpB.py", "tmap.py", "overlay_head.html", "overlay_tail.html"]

def transcrever(video, pasta):
    from faster_whisper import WhisperModel
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(video, language="pt", word_timestamps=True)
    out = [{"words": [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for w in s.words]} for s in segs]
    json.dump(out, open(os.path.join(pasta, "palavras.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(" ".join(f"{w['w']}@{w['s']}" for s in out for w in s["words"]))
    return out

def overlay(pasta):
    mods = os.path.join(pasta, "overlay_mods.js")
    html = "".join(open(os.path.join(pasta, f), encoding="utf-8-sig").read() for f in ("overlay_head.html", "overlay_mods.js", "overlay_tail.html"))
    open(os.path.join(pasta, "overlay.html"), "w", encoding="utf-8").write(html); print("overlay.html ok")

def copiar_base(pasta, video, de=None):
    os.makedirs(pasta, exist_ok=True)
    for f in ARQS: shutil.copy(os.path.join(MOD, f), pasta)               # motor sempre da versão atual da skill
    if os.path.isdir(os.path.join(pasta, "fonts")): shutil.rmtree(os.path.join(pasta, "fonts"))
    shutil.copytree(os.path.join(MOD, "fonts"), os.path.join(pasta, "fonts"))
    shutil.copy(video, os.path.join(pasta, "src.mp4"))

def cmd_novo(a):
    copiar_base(a.pasta, a.video)
    shutil.copy(os.path.join(MOD, "overlay_mods.js"), a.pasta)
    transcrever(os.path.join(a.pasta, "src.mp4"), a.pasta); overlay(a.pasta)
    print("\nPróximo: corrigir grafias no palavras.json; REELS -> render reels. STORY -> escrever overlay_mods.js (exemplo = Visita Marcada),"
          " ajustar KIN e sons no build_story_b.py, overlay, frames, render story.")

def cmd_reaproveitar(a):
    old = a.antigo
    copiar_base(a.pasta, a.video)
    for f in ("build_story_b.py", "build_reels.py", "overlay_mods.js"):     # o que é do anúncio vem da edição antiga
        if os.path.exists(os.path.join(old, f)): shutil.copy(os.path.join(old, f), a.pasta)
    sys.path.insert(0, a.pasta); import tmap
    transcrever(os.path.join(a.pasta, "src.mp4"), a.pasta)
    A, cas, no, nn = tmap.ancoras(os.path.join(old, "palavras.json"), os.path.join(a.pasta, "palavras.json"))
    cad = json.load(open(os.path.join(old, "tmap.json"), encoding="utf-8"))["cadeia"] if os.path.exists(os.path.join(old, "tmap.json")) else []
    json.dump({"cadeia": cad + [A]}, open(os.path.join(a.pasta, "tmap.json"), "w", encoding="utf-8"))
    overlay(a.pasta)
    print(f"\ntmap.json: {cas} palavras casadas (antiga {no} / nova {nn}). Abaixo de ~90% = roteiro mudou: confira os tempos à mão.")
    if os.path.exists(os.path.join(old, "censura.json")):
        print("A edição antiga tinha censura de", json.load(open(os.path.join(old, "censura.json"), encoding="utf-8"))["palavra"], "-> rode render, censura e render de novo.")

def cmd_overlay(a): overlay(a.pasta)

def duracao(pasta):
    W = [w for s in json.load(open(os.path.join(pasta, "palavras.json"), encoding="utf-8")) for w in s["words"]]
    return W[-1]["e"] + 1.0

def cmd_frames(a):
    if not os.path.exists(os.path.join(a.pasta, "overlay.html")): overlay(a.pasta)
    n = math.ceil(duracao(a.pasta) * 30) + 15; parte = math.ceil(n / 3); ps = []
    for k in ("content", "mask"):
        d = os.path.join(a.pasta, "frames2_" + k)
        if os.path.isdir(d): shutil.rmtree(d)
        for i in range(3):
            ps.append(subprocess.Popen([PY, "rpB.py", "frames", k, str(i * parte), str(min(n, (i + 1) * parte))], cwd=a.pasta,
                                       stdout=open(os.path.join(a.pasta, f"rB_{k}_{i}.log"), "w"), stderr=subprocess.STDOUT))
    falhou = [p.args for p in ps if p.wait() != 0]
    print("quadros:", len(os.listdir(os.path.join(a.pasta, "frames2_content"))), "de", n, "| erros:", falhou or "nenhum (veja rB_*.log)")

def cmd_render(a):
    b = "build_story_b.py" if a.formato == "story" else "build_reels.py"
    if a.formato == "story" and not os.path.isdir(os.path.join(a.pasta, "frames2_content")): sys.exit("rode 'frames' antes do render story")
    subprocess.run([PY, b], cwd=a.pasta, check=True)
    args = json.load(open(os.path.join(a.pasta, "args_%s.json" % ("STORY" if a.formato == "story" else "REELS"))))
    r = subprocess.run(["ffmpeg"] + args, cwd=a.pasta, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: sys.exit(r.stderr[-2000:])
    print("ok:", os.path.join(a.pasta, args[-1]))

def cmd_censura(a):
    import numpy as np
    W = [w for s in json.load(open(os.path.join(a.pasta, "palavras.json"), encoding="utf-8")) for w in s["words"]]
    alvo = nz(a.palavra); idx = [i for i, w in enumerate(W) if nz(w["w"]) == alvo]
    if not idx: sys.exit(f"'{a.palavra}' não está no palavras.json")
    if len(idx) > 1: print("aparece", len(idx), "vezes; censurando a 1ª (use --ocorrencia N)")
    i = idx[min(a.ocorrencia, len(idx)) - 1]; w = W[i]
    SR = 16000; t0 = max(0, w["s"] - 0.6)
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{w['e'] - t0 + 1.0:.3f}", "-i", os.path.join(a.pasta, "src.mp4"),
                                      "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float)
    F = int(SR * 0.01); rms = np.array([np.sqrt((x[k:k + F] ** 2).mean() + 1e-9) for k in range(0, len(x) - F, F)]); tt = t0 + np.arange(len(rms)) * 0.01
    # início: vale de volume logo antes da palavra (fim da palavra anterior); fim: volume cai e fica baixo
    j0 = [k for k in range(len(tt)) if w["s"] - 0.15 <= tt[k] <= w["s"] + 0.08]
    A = a.a if a.a is not None else round(float(tt[min(j0, key=lambda k: rms[k])]) - 0.01, 3)
    pico = rms[[k for k in range(len(tt)) if A <= tt[k] <= w["e"]]].max(); B = None
    for k in range(len(tt)):
        if tt[k] > A + 0.25 and all(rms[k:k + 4] < 0.08 * pico): B = round(float(tt[k]) + 0.03, 3); break
    B = a.b if a.b is not None else (B or round(w["e"] + 0.05, 3))
    print(f"palavra {w['w']} {w['s']}–{w['e']}  ->  pi {A}–{B}")
    for k in range(0, len(tt), 2):
        if A - 0.3 <= tt[k] <= B + 0.3: print("%6.2f %s %s" % (tt[k], "PI" if A <= tt[k] <= B else "  ", "#" * int(rms[k] / pico * 30)))
    # boca: medida no vídeo já montado (o zoom muda a posição)
    saida = os.path.join(a.pasta, "saida_%s.mp4" % a.formato.upper()); boca = []; T0 = round(A - 0.2, 3)
    if os.path.exists(saida):
        import mediapipe as mp
        from mediapipe.tasks.python import vision, BaseOptions
        from PIL import Image
        q = os.path.join(a.pasta, "censura_quadros"); shutil.rmtree(q, ignore_errors=True); os.makedirs(q)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{T0:.3f}", "-i", saida, "-t", f"{B - T0 + 0.3:.3f}", "-vf", "fps=30", os.path.join(q, "f_%03d.png")], check=True)
        lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=os.path.join(MOD, "face_landmarker.task")), num_faces=1))
        LIPS = [61, 291, 0, 17, 13, 14, 78, 308, 40, 270, 91, 321, 181, 405]
        for f in sorted(glob.glob(os.path.join(q, "f_*.png"))):
            im = np.array(Image.open(f).convert("RGB")); r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=im))
            if not r.face_landmarks: boca.append(None); continue
            p = r.face_landmarks[0]; xs = [p[k].x * im.shape[1] for k in LIPS]; ys = [p[k].y * im.shape[0] for k in LIPS]
            boca.append([round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))])
        print("boca em", sum(1 for b in boca if b), "de", len(boca), "quadros")
    else:
        print(f"sem {os.path.basename(saida)}: rode o render {a.formato} antes para medir a boca (senão sai só o pi)")
    json.dump({"palavra": alvo, "s": w["s"], "a": A, "b": B, "t0": T0, "boca": boca}, open(os.path.join(a.pasta, "censura.json"), "w", encoding="utf-8"))
    print("censura.json ok -> rode o render de novo e confira o trecho (folha de quadros + ouvir).")

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest="cmd", required=True)
x = sp.add_parser("novo"); x.add_argument("video"); x.add_argument("pasta"); x.set_defaults(f=cmd_novo)
x = sp.add_parser("reaproveitar"); x.add_argument("antigo"); x.add_argument("video"); x.add_argument("pasta"); x.set_defaults(f=cmd_reaproveitar)
x = sp.add_parser("overlay"); x.add_argument("pasta"); x.set_defaults(f=cmd_overlay)
x = sp.add_parser("frames"); x.add_argument("pasta"); x.set_defaults(f=cmd_frames)
x = sp.add_parser("render"); x.add_argument("pasta"); x.add_argument("formato", choices=["story", "reels"]); x.set_defaults(f=cmd_render)
x = sp.add_parser("censura"); x.add_argument("pasta"); x.add_argument("--palavra", required=True); x.add_argument("--formato", default="story", choices=["story", "reels"])
x.add_argument("--a", type=float); x.add_argument("--b", type=float); x.add_argument("--ocorrencia", type=int, default=1); x.set_defaults(f=cmd_censura)
a = ap.parse_args(); a.pasta = os.path.abspath(a.pasta); a.f(a)
