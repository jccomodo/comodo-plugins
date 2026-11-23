"""CMD128 - base = montagem do usuário (cortes/zooms/cor prontos). Acrescenta legendas de designer, motions, matte e áudio."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legendas_designer as LD

W = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(W, "fonts")
K = 1.78; BASE_CAP, CAP_EM = 1482, 59; MAX_CHARS, MAX_WORDS = 16, 4
TXT = r"&H00F3F3F3&"; HOLD = 0.30; DUR = 49.5
SH = r"\bord0\xshad2\yshad4\4c&H00000000&\4a&H30&"
FN = {"sb": r"\fnPoppins SemiBold\b0", "b": r"\fnPoppins\b1"}
DISP_FIX = {"tá": "está", "comodo": "Cômodo"}

words = []
for s in json.load(open(os.path.join(W, "palavras.json"), encoding="utf-8-sig")):
    words += [w for w in s["words"] if w["s"] < DUR - 0.1]
def norm(t): return re.sub(r"[^\wÀ-ÿ%-]", "", t.lower())
clean = [norm(w["w"]) for w in words]
def disp(i):
    t = re.sub(r"[.,;:!]+$", "", words[i]["w"].strip()); return DISP_FIX.get(t.lower(), t)
def find_seq(seq, start=0):
    n = len(seq)
    for i in range(start, len(clean) - n + 1):
        if clean[i:i + n] == seq: return i
    raise SystemExit("não achei: " + " ".join(seq))
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return "%d:%02d:%05.2f" % (h, m, s)

# ---------- EDITORIAL: blocos grandes SÓ em frases-chave com dado ----------
# (frase para localizar, [(texto exibido, n tokens, estilo, mapa palavra->token)])
BIG = [
 ("quanto custa um lead",                [("Quanto custa", 2, "norm", None), ("um lead", 2, "norm", None)]),
 ("mais de 400 operações de planejados", [("mais de 400", 3, "norm", None), ("operações", 1, "norm", None), ("de planejados", 2, "norm", None)]),
 ("de 6 70 até 150 200 reais",           [("de R$ 6,70", 3, "norm", [0, 1, 2]), ("até R$ 150, R$ 200", 4, "norm", [0, 1, 1, 2, 2])]),
 ("isso não é achismo",                  [("Isso não é", 3, "norm", None), ("achismo", 1, "norm", None)]),
 ("cerca de 400 lojas de planejados",    [("cerca de 400", 3, "norm", None), ("lojas de planejados", 3, "norm", None)]),
 ("é só comentar comparar",              [("é só comentar", 3, "norm", None), ("Comparar", 1, "norm", None)]),
]
ev = []; used = set(); cursor = 0; PENDING = []; STACK_IV = []
for phrase, lines in BIG:
    a = find_seq([norm(x) for x in phrase.split()], cursor)
    pos = a; spans = []
    for (txt, n, st, mp) in lines: spans.append((pos, pos + n - 1)); pos += n
    first, last_ = spans[0][0], spans[-1][1]; cursor = last_ + 1; used.update(range(first, last_ + 1))
    t_end = words[last_]["e"] + HOLD
    L = []
    for (txt, n, st, mp), (sa, sb) in zip(lines, spans):
        ws = txt.split(); idx = list(range(sa, sb + 1)); mp = mp or [min(j, len(idx) - 1) for j in range(len(ws))]
        L.append([(w, words[idx[mp[j]]]["s"]) for j, w in enumerate(ws)])
    PENDING.append((L, t_end, [84 if st == "small" else None for (_, _, st, _) in lines]))
PENDING.sort(key=lambda p: p[0][0][0][1])
for i_, (L, t_end, caps) in enumerate(PENDING):
    if i_ + 1 < len(PENDING):
        t_end = max(L[0][0][1] + 0.5, min(t_end, PENDING[i_ + 1][0][0][0][1] - 0.14))
    evs = LD.justified_stack(FONTS, L, t_end, TXT, SH, FN["b"], layer=3, caps=caps)
    ev += evs; STACK_IV.append((evs[0][0], t_end))

# ---------- legendas corridas ----------
BREAK_BEFORE = {"que", "ou", "mas", "se", "para", "pra", "com", "como"}
chunks, i = [], 0
while i < len(words):
    if i in used: i += 1; continue
    grp = [i]; chars = len(disp(i))
    while True:
        j = grp[-1] + 1
        if j >= len(words) or j in used: break
        endp = re.search(r"[.?!,;:]$", words[grp[-1]]["w"].strip()) is not None
        gap = words[j]["s"] - words[grp[-1]]["e"]
        if endp or gap > 0.25: break
        if len(grp) >= MAX_WORDS or chars + 1 + len(disp(j)) > MAX_CHARS: break
        if len(grp) >= 2 and clean[j] in BREAK_BEFORE: break
        grp.append(j); chars += 1 + len(disp(j))
    chunks.append(grp); i = grp[-1] + 1
runs = []
for grp in chunks:
    toks = []
    for k in grp:
        txt = disp(k)
        if words[k]["w"].strip().endswith("?") and not txt.endswith("?"): txt += "?"
        toks.append((txt, words[k]["s"]))
    runs.append([toks[0][1] - 0.03, words[grp[-1]]["e"] + 0.25, toks])
for k in range(len(runs) - 1):
    if runs[k + 1][0] - runs[k][1] < 0.40 or runs[k][1] > runs[k + 1][0]: runs[k][1] = runs[k + 1][0]
bigstarts = sorted(s for s, _ in STACK_IV)
for r in runs:
    for bs in bigstarts:
        if r[0] < bs - 0.02 < r[1]: r[1] = bs - 0.02; break
for s0, s1, toks in runs:
    for bs, be in STACK_IV:
        if bs - 0.02 <= s0 < be: s0 = be
    if s1 <= s0 + 0.12: continue
    s1 = max(s1, s0 + 0.2)
    ev += LD.small_caption(FONTS, [(t, max(ts_, s0 + 0.05)) for t, ts_ in toks], s1, TXT, SH, FN["sb"], em=CAP_EM, base_y=BASE_CAP, layer=4)
ev.sort(key=lambda e: (e[0], e[2]))
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Poppins SemiBold,114,&H00F3F3F3,&H00F3F3F3,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,3,7,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
with open(os.path.join(W, "legendas.ass"), "w", encoding="utf-8") as f:
    f.write(hdr)
    for s, e, layer, txt in ev: f.write("Dialogue: %d,%s,%s,Default,,0,0,0,,%s\n" % (layer, ts(s), ts(e), txt))

# ---------- motions (timing.json) ----------
tm = json.load(open(os.path.join(W, "motion", "timing.json"), encoding="utf-8-sig"))
CARD_W, CARD_Y = 930, 30
inputs = []; g = ["[0:v]split[vb][vt]", "[1:v]scale=1080:1920:flags=bicubic,format=gray,gblur=sigma=1.4[mk]", "[vt][mk]alphamerge[person]"]
chain = "[vb]"; wins = []
for k, t in enumerate(tm):
    inputs += ["-framerate", "30", "-i", "motion/frames/%02d_%s/%%04d.png" % (t["n"], t["scene"])]
    p0 = "%.3f" % t["inicio_s"]; p1 = "%.3f" % t["fim_s"]
    g.append("[%d:v]format=rgba,scale=%d:-1:flags=lanczos,setpts=PTS+%s/TB[o%d]" % (k + 2, CARD_W, p0, k))
    g.append("%s[o%d]overlay=x='(W-w)/2':y='%d':enable='between(t,%s,%s)':format=auto[c%d]" % (chain, k, CARD_Y, p0, p1, k))
    chain = "[c%d]" % k; wins.append("between(t,%s,%s)" % (p0, p1))
g.append("%s[person]overlay=enable='gt(%s,0)':format=auto[comp]" % (chain, "+".join(wins)))
g.append("[comp]ass=legendas.ass:fontsdir=fonts[v]")
open(os.path.join(W, "filtro.txt"), "w", encoding="utf-8").write(";\n".join(g))
json.dump({"inputs": inputs}, open(os.path.join(W, "cortes.json"), "w"))
print("eventos:", len(ev), "| blocos grandes:", len(PENDING), "| legendas:", len(runs), "| motions:", len(tm))
