"""Anúncio do clone do Daniel (HeyGen 9:16) — ADS REELS simples (pílula vermelha + zooms + CTA).
Base: CMD221 (legenda de ADS em pílula vermelha + escurecimento + bloco "clique no / botão / aqui embaixo").
Acrescenta os dois zooms do padrão (×1,166 em torno do ponto fixo 0,53/0,46), trocando no início de frase."""
import json, re, os, sys, wave
import numpy as np
W = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, W)
import legendas_designer as LD

# =====================================================================================================
# MODELO da skill video-daniel (anuncio/modelo). Exemplo pronto = anúncio "Visita Marcada 1".
# Por anúncio, só mexa nos blocos marcados  >>> DO ANÚNCIO <<<  (KIN, sons). Tempos escritos à mão
# passam por M(): numa edição reaproveitada (voz nova) o tmap.json converte o tempo antigo no novo.
# Censura: censura.json (gerado por "anuncio.py censura") troca a legenda e põe pi + tarja.
# =====================================================================================================
LD.CX = 540
FMT = "REELS"; OUT_H = 1920; FONTS = os.path.join(W, "fonts")
SRC = os.path.join(W, "src.mp4")
PILL_FULL = 1066; CAP_EM = 56; PH = 92
TXT = r"&H00FFFFFF&"; SH = r"ord0\shad0"; FN = r"nPoppins SemiBold0"; FN_B = r"nPoppins1"; FN_K = r"nPoppins Black0"
PILL_C = r"&H2B32E5&"
ZOOM_T = 1.166; CXF, CYF = 0.53, 0.46; FLIP_MIN, FLIP_FORCE = 2.4, 7.5
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return "%d:%02d:%05.2f" % (h, m, s)

# ---------- palavras (com correções) ----------
words = []
for si, s in enumerate(json.load(open(os.path.join(W, "palavras.json"), encoding="utf-8"))):
    words += [dict(w, seg=si) for w in s["words"]]
FIX = {"comodo,": "Cômodo,", "comodo": "Cômodo"}          # grafias que o Whisper erra (minúsculas, com pontuação)
CENS = json.load(open(os.path.join(W, "censura.json"), encoding="utf-8")) if os.path.exists(os.path.join(W, "censura.json")) else None
out = []
for w in words:
    k = w["w"].strip().lower()
    if k in FIX: w = dict(w, w=FIX[k])
    if CENS and re.sub(r"[^\wÀ-ÿ]", "", k) == CENS["palavra"] and abs(w["s"] - CENS["s"]) < 0.3:   # legenda censurada: m***a
        p_ = re.match(r"^(\W*)(\w)(.*?)(\w)(\W*)$", w["w"].strip()); w = dict(w, w=p_.group(1) + p_.group(2) + "***" + p_.group(4) + p_.group(5))
    out.append(w)
words = out
LAST = words[-1]["e"]; DUR = round(LAST + 1.0, 2)                # 1 s de cauda (tpad) para a CTA respirar
def norm(t): return re.sub(r"[^\wÀ-ÿ%-]", "", t.lower())
clean = [norm(w["w"]) for w in words]
def disp(i):
    t = re.sub(r"[.,;:!]+$", "", words[i]["w"].strip())
    if words[i]["w"].strip().endswith("?") and not t.endswith("?"): t += "?"
    return t

# ---------- CTA ----------
ic = max(i for i, c in enumerate(clean) if c == "clica")
CTA_T = {"clica": words[ic]["s"] - 0.05, "botão": words[ic + 2]["s"] - 0.05, "aqui": words[ic + 3]["s"] - 0.05}
CTA_DARK = words[ic]["s"] - 0.25
KIN = [(words[ic]["s"] - 0.06, 999)]

# ---------- legenda de ADS (pílula) — igual ao CMD221 ----------
NOEND = {"te","não","a","o","as","os","um","uma","uns","umas","de","da","do","das","dos","em","no","na","nos","nas","por","pra","para","com","que","e","ou","mas","se","ao","à","pelo","pela","como","quando","porque","seu","sua","meu","minha","mais","muito","nem","já","só","é","tá","esse","essa","está","menos","pro","enquanto","todo","quem"}
PREFER = {"que","e","ou","mas","como","porque","quando","para","pra","com","por"}
MAXC, MAXW, IDEAL = 27, 5, 18
NUM = {"dois","três","quatro","cinco"}
def hard_break(i, j, seg_len):
    w = words[i]["w"].strip()
    if clean[i] in NUM and clean[j] in NUM | {"cinco"}: return False      # "dois, três, quatro, cinco mil" fica junto
    return re.search(r"[.?!]$", w) is not None or (re.search(r"[,;:]$", w) is not None and seg_len >= 2) or (words[j]["s"] - words[i]["e"]) > 0.40
CTA_WORDS = set(i for i, w in enumerate(words) if any(a_ <= w["s"] < b_ for a_, b_ in KIN))
segments, cur_ = [], []
for i in range(len(words)):
    if i in CTA_WORDS:
        if cur_: segments.append(cur_); cur_ = []
        continue
    if cur_ and hard_break(cur_[-1], i, len(cur_)): segments.append(cur_); cur_ = []
    cur_.append(i)
if cur_: segments.append(cur_)
def chunk_cost(seg, p, q):
    ws = seg[p:q]; c = sum(len(disp(i)) for i in ws) + len(ws) - 1
    if c > MAXC or len(ws) > MAXW: return None
    pen = ((c - IDEAL) ** 2) / 4.0
    dur_ = words[ws[-1]]["e"] - words[ws[0]]["s"]
    if dur_ < 0.8 and len(seg) > len(ws): pen += 160 * (0.8 - dur_)
    if len(ws) == 1 and len(seg) > 1: pen += 70
    if (clean[ws[-1]] in NOEND or re.search(r"\d", clean[ws[-1]])) and q < len(seg): pen += 400
    if clean[ws[0]] in PREFER and p > 0: pen -= 12
    return pen
chunks = []
for seg in segments:
    n = len(seg); INF = 1e18; best = [INF] * (n + 1); prev = [0] * (n + 1); best[0] = 0
    for q in range(1, n + 1):
        for p in range(q):
            c = chunk_cost(seg, p, q)
            if c is None or best[p] >= INF: continue
            if best[p] + c < best[q]: best[q] = best[p] + c; prev[q] = p
    parts = []; q = n
    while q > 0: parts.append((prev[q], q)); q = prev[q]
    parts.reverse()
    for p, q in parts: chunks.append(seg[p:q])

def rrect(w, h, r):
    return "m %.0f 0 l %.0f 0 b %.0f 0 %.0f 0 %.0f %.0f l %.0f %.0f b %.0f %.0f %.0f %.0f %.0f %.0f l %.0f %.0f b 0 %.0f 0 %.0f 0 %.0f l 0 %.0f b 0 0 0 0 %.0f 0" % (
        r, w - r, w, w, w, r, w, h - r, w, h, w, h, w - r, h, r, h, h, h, h - r, r, r)
runs = []
for grp in chunks:
    s0 = words[grp[0]]["s"] - 0.04; s1 = max(words[grp[-1]]["e"] + 0.30, s0 + 0.8)
    runs.append([s0, s1, grp])
for k in range(len(runs) - 1):
    if runs[k + 1][0] - runs[k][1] < 0.30 or runs[k][1] > runs[k + 1][0]: runs[k][1] = runs[k + 1][0]
if runs and runs[-1][1] > KIN[0][0]: runs[-1][1] = KIN[0][0]
ev = []; fs = int(round(CAP_EM * LD.K))
for s0, s1, grp in runs:
    toks = [disp(k) for k in grp]; text = " ".join(toks); l, r_, _ = LD.ink(FONTS, text, "sb")
    pw = (r_ - l) * CAP_EM + 64; yb = PILL_FULL
    x_origin = LD.CX - ((r_ - l) * CAP_EM) / 2.0 - l * CAP_EM; pos = 0
    x_left = int(LD.CX - pw / 2); tstart = [max(words[k]["s"], s0 + 0.04) - 0.05 for k in grp]
    for j in range(len(grp)):
        pre = " ".join(toks[:j + 1]); lp, rp, _ = LD.ink(FONTS, pre, "sb"); wj = (rp - lp) * CAP_EM + 64
        a0 = (s0 - 0.02) if j == 0 else tstart[j] - 0.02; a1 = s1 if j == len(grp) - 1 else tstart[j + 1] - 0.02
        ev.append((a0, a1, 2, r"{\an7\pos(%d,%d)\p1\bord0\shad0\1c%s%s}%s" % (x_left, yb, PILL_C, r"\fad(60,0)" if j == 0 else "", rrect(wj, PH, 22))))
    for k, tk in zip(grp, toks):
        prefix = text[:pos]; x = x_origin + (LD.ink(FONTS, prefix, "sb")[2] * CAP_EM if prefix else 0); pos += len(tk) + 1
        ev += LD._entry_events(max(words[k]["s"], s0 + 0.04) - 0.05, s1, int(round(x)), yb + PH / 2 + 0.36 * CAP_EM, fs, "sb", tk, rise=12, blur0=4, dur=0.22, color=TXT, shadow=SH, fn=FN, fade_out=0, layer=4)

# ---------- CTA final ("clique no / botão / aqui embaixo") ----------
END = DUR; CTA_CY = 780; BW = 800; XL = 540 - BW / 2
lb, rb, _ = LD.ink(FONTS, "botão", "k"); em_b = BW / (rb - lb); bbase = int(CTA_CY + 0.30 * em_b - 4)
def line_ev(text, kind, em, x, base, t0, fn, color):
    l, r_, _ = LD.ink(FONTS, text, kind); return LD._entry_events(t0, END, int(round(x - l * em)), base, int(round(em * LD.K)), kind, text, rise=40, blur0=10 if kind == "k" else 6, dur=0.4, color=color, shadow=SH, fn=fn, fade_out=0, layer=5)
l3, r3, _ = LD.ink(FONTS, "aqui embaixo", "b")
ev += line_ev("clica no", "b", 66, XL, bbase - 0.82 * em_b, CTA_T["clica"], FN_B, TXT)
ev += line_ev("botão", "k", em_b, XL, bbase, CTA_T["botão"], FN_K, r"&H2B32E5&")
ev += line_ev("aqui embaixo", "b", 62, XL + BW - (r3 - l3) * 62, bbase + 0.22 * em_b + 40, CTA_T["aqui"], FN_B, TXT)
ev.sort(key=lambda e: (e[0], e[2]))
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: %d
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Poppins SemiBold,114,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
with open(os.path.join(W, "legendas_%s.ass" % FMT), "w", encoding="utf-8") as f:
    f.write(hdr % OUT_H)
    for s, e, layer, t in ev: f.write("Dialogue: %d,%s,%s,Default,,0,0,0,,%s\n" % (layer, ts(max(0, s)), ts(max(e, s + 0.05)), t))
with open(os.path.join(W, "chunks.txt"), "w", encoding="utf-8") as f:
    for s0, s1, grp in runs: f.write("%5.2f-%5.2f  %s\n" % (s0, s1, " ".join(disp(k) for k in grp)))

# ---------- trocas de zoom: início de frase ----------
starts = [0] + [i for i in range(1, len(words)) if re.search(r"[.?!]$", words[i - 1]["w"].strip())]
commas = [i for i in range(1, len(words)) if re.search(r"[,;:]$", words[i - 1]["w"].strip())]
flips = []; last = 0.0
for i in range(1, len(words)):
    t = words[i]["s"] - 0.09
    if t >= KIN[0][0] - 0.3: break
    if (i in starts and t - last >= FLIP_MIN) or (i in commas and t - last > FLIP_FORCE):
        flips.append(round(t, 2)); last = t
bounds = [0.0] + flips + [DUR]
# a CTA fica no enquadramento largo (mais ar para o bloco)
SW, SHH = 2 * round(1080 * ZOOM_T / 2), 2 * round(1920 * ZOOM_T / 2)
XC, YC = round(CXF * 1080 * (ZOOM_T - 1)), round(CYF * 1920 * (ZOOM_T - 1))

# ---------- sfx ----------
SR = 44100; sfx = np.zeros(int(SR * (DUR + 1)), np.float32); rng = np.random.default_rng(21)
def add(tt, y, gn=1.0):
    i = int(max(tt, 0) * SR); y = (y * gn).astype(np.float32); n = min(len(y), len(sfx) - i)
    if n > 0: sfx[i:i + n] += y[:n]
def whoosh(d=0.5):
    n = int(SR * d); x = rng.standard_normal(n); env = np.sin(np.linspace(0, np.pi, n)) ** 2; k = np.linspace(0.02, 0.35, n); y = np.zeros(n); lp = 0
    for j in range(n): lp += k[j] * (x[j] - lp); y[j] = lp
    return y * env * 1.6
def thud(d=.28):
    n = int(SR * d); tt = np.arange(n) / SR; f = 95 * np.exp(-tt * 7) + 38; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 11)
add(CTA_DARK - 0.3, whoosh(0.4), 0.4); add(CTA_T["botão"] - 0.1, thud(), 0.7)
with wave.open(os.path.join(W, "sfx.wav"), "wb") as w_: w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())

def tarja_filtro():   # tarja preta seguindo a boca (censura.json["boca"]: caixa dos lábios por quadro, medida no vídeo já montado)
    if not CENS or not CENS.get("boca"): return "null"
    cb = []
    for i, b in enumerate(CENS["boca"]):
        t = CENS["t0"] + i / 30
        if b and CENS["a"] - 0.05 <= t <= CENS["b"] + 0.04: cb.append((t, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    f = []
    for k, (t, x, y) in enumerate(cb):
        viz = cb[max(0, k - 1):k + 2]; x = sum(q[1] for q in viz) / len(viz); y = sum(q[2] for q in viz) / len(viz)
        f.append("drawbox=x=%d:y=%d:w=210:h=104:color=black@1:t=fill:enable='between(t,%.3f,%.3f)'" % (x - 105, y - 52, t - 0.001, t + 1 / 30 - 0.001))
    return ",".join(f) or "null"

# ---------- filtro ----------
g = ["[0:v]fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1.2,split=%d%s" % (len(bounds) - 1, "".join("[s%d]" % k for k in range(len(bounds) - 1)))]
for k in range(len(bounds) - 1):
    a, b = bounds[k], bounds[k + 1]; tight = (k % 2 == 1) and b <= KIN[0][0] + 0.5
    z = ",scale=%d:%d:flags=lanczos,crop=1080:1920:%d:%d" % (SW, SHH, XC, YC) if tight else ""
    g.append("[s%d]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS%s,setsar=1[z%d]" % (k, a, b, z, k))
g.append("%sconcat=n=%d:v=1:a=0,format=yuv420p[vz]" % ("".join("[z%d]" % k for k in range(len(bounds) - 1)), len(bounds) - 1))
g.append("color=c=black:s=1080x1920:r=30:d=%d,format=rgba,colorchannelmixer=aa=0.62,fade=t=in:st=%.2f:d=0.35:alpha=1[dk2]" % (DUR + 5, CTA_DARK))
g.append("[vz]%s[vc]" % tarja_filtro())
g.append("[vc][dk2]overlay=0:0:format=auto[m3]")
g.append("[m3]format=yuv420p,ass=legendas_REELS.ass:fontsdir=fonts[v]")
if CENS:   # censura de TV: voz zerada + pi de 1 kHz no mesmo volume da fala
    g.append("[0:a]volume=0:enable='between(t,%.3f,%.3f)',apad=pad_dur=1.2,loudnorm=I=-19.5:TP=-1.5:LRA=7[voz]" % (CENS["a"], CENS["b"]))
    g.append("[1:a]volume=0.10[fx]")
    g.append("sine=frequency=1000:sample_rate=48000:duration=%.3f,volume=1.3,afade=t=in:d=0.01,afade=t=out:st=%.3f:d=0.01,adelay=%d:all=1[pi]" % (CENS["b"] - CENS["a"], CENS["b"] - CENS["a"] - 0.01, round(CENS["a"] * 1000)))
    g.append("[voz][fx][pi]amix=inputs=3:duration=first:weights=1 1 1:normalize=0,alimiter=limit=0.89:level=false[a]")
else:
    g.append("[0:a]apad=pad_dur=1.2,loudnorm=I=-19.5:TP=-1.5:LRA=7[voz]")
    g.append("[1:a]volume=0.10[fx]")
    g.append("[voz][fx]amix=inputs=2:duration=first:weights=1 1:normalize=0,alimiter=limit=0.89:level=false[a]")
open(os.path.join(W, "filtro_REELS.txt"), "w", encoding="utf-8").write(";\n".join(g))
args = ["-y", "-v", "error", "-i", SRC, "-i", "sfx.wav", "-/filter_complex", "filtro_REELS.txt", "-map", "[v]", "-map", "[a]", "-t", "%.3f" % DUR,
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "saida_REELS.mp4"]
json.dump(args, open(os.path.join(W, "args_REELS.json"), "w"))
print("dur", DUR, "| legendas:", len(runs), "| eventos:", len(ev), "| trocas de zoom:", flips, "| CTA", CTA_T)
