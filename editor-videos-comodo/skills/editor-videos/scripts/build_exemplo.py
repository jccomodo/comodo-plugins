"""CMD-novo1 - montador no padrão CMD124 (skill editor-videos). Todos os valores de MEDIDO vêm do CMD124.
Editorial deste vídeo: bloco 'EDITORIAL' no meio do arquivo."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legendas_designer as LD
STACK_IV = []; PENDING = []
import numpy as np
from PIL import ImageFont

W = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(W, "fonts")

# ================= MEDIDO no CMD124 =================
SPEED = 1.10
GAP, PAD_B, PAD_A = 0.50, 0.12, 0.15
FACE_W_WIDE, ZOOM_RATIO = 0.408, 1.166
ANCHOR = (0.53, 0.46)
NOSE_WIDE = (0.506, 0.497)
GAIN = (0.885, 0.875, 0.88)
LUFS_TARGET = -19.5
K = 1.78
BASE_CAP, CAP_EM = 1482, 59
MAX_CHARS, MAX_WORDS = 16, 4
TXT = r"&H00F3F3F3&"
LUT = "filtro_dan.cube"
FLIP_MIN, FLIP_FORCE = 2.4, 7.5          # troca de zoom: início de frase, >=2,4 s desde a última; força se >7,5 s

# ================= EDITORIAL (deste vídeo) =================
DROP_AFTER = 113.0                        # alucinação do Whisper no silêncio final
DISP_FIX = {"tá": "está", "comodo": "Cômodo", "whatsapp": "WhatsApp", "crm": "CRM", "google": "Google"}
EM_SMALL, EM_NORM, W_BIG, EM_BIGMAX = 84, 84, 680, 148
R_EDGE, EM_ORD, EM_SIDE, PITCH_SIDE = 870, 540, 84, 84
STACK_BASE, PITCH_CTX = 1476, 119
BIG = [
 ("stack", "você sabe de qual anúncio", [("Você sabe de qual", 4, "small"), ("anúncio", 1, "big")]),
 ("stack", "você abriu um restaurante", [("você abriu um", 3, "small"), ("restaurante", 1, "big")]),
 ("stack", "distribuindo panfleto", [("distribuindo", 1, "small"), ("panfleto", 1, "big")]),
 ("stack", "só que ninguém perguntou", [("só que", 2, "small"), ("ninguém perguntou", 2, "big")]),
 ("stack", "você não sabe qual panfleteiro", [("você não sabe qual", 4, "small"), ("panfleteiro", 1, "big")]),
 ("stack", "trocar o panfleto por anúncio", [("trocar o panfleto por", 4, "small"), ("anúncio", 1, "big")]),
 ("stack", "o restaurante pela sua loja", [("o restaurante pela", 3, "small"), ("sua loja", 2, "big")]),
 ("stack", "onde chega o lead", [("onde chega o", 3, "small"), ("lead", 1, "big")]),
 ("stack", "numa planilha", [("numa", 1, "small"), ("planilha", 1, "big")]),
 ("stack", "no whatsapp", [("no", 1, "small"), ("WhatsApp", 1, "big")]),
 ("stack", "chegar com uma etiqueta", [("chegar com uma", 3, "small"), ("etiqueta", 1, "big")], {"align": "left"}),
 ("stack", "desse canal dessa campanha e desse anúncio", [("desse canal", 2, "big"), ("dessa campanha", 2, "big"), ("desse anúncio", 3, "big")]),
 ("stack", "fica na ficha dele", [("fica na", 2, "small"), ("ficha dele", 2, "big")]),
 ("stack", "o nome disso é rastreamento", [("o nome disso é", 4, "small"), ("rastreamento", 1, "big")]),
 ("stack", "dentro de um crm", [("dentro de um", 3, "small"), ("CRM", 1, "big")]),
 ("stack", "colocar mais dinheiro", [("colocar mais", 2, "small"), ("dinheiro", 1, "big")]),
 ("stack", "dividir verba no chute", [("dividir verba", 2, "small"), ("no chute", 2, "big")]),
 ("stack", "a parte que quase ninguém conta", [("a parte que", 3, "small"), ("quase ninguém conta", 3, "big")]),
 ("stack", "dá para devolver essa informação", [("dá para devolver", 3, "small"), ("essa informação", 2, "big")]),
 ("stack", "pro meta e pro google", [("pro Meta", 2, "big"), ("e pro Google", 3, "big")]),
 ("stack", "onde chega o lead da sua loja hoje", [("onde chega o", 3, "small"), ("lead da sua loja", 4, "big")]),
 ("stack", "planilha", [("planilha", 1, "big")]),
 ("stack", "whatsapp", [("WhatsApp", 1, "big")]),
 ("stack", "ou crm", [("ou CRM", 2, "big")]),
 ("stack", "comenta aqui embaixo", [("comenta", 1, "small"), ("aqui embaixo", 2, "big")]),
]
QUOTES = ["esse anúncio que eu trouxe o cliente e esse anúncio que fez com que a pessoa comprasse"]
# (arquivo, palavras faladas, centro y, largura px)  - texto de imagem precisa ser LEGÍVEL: imagens com texto ficam acima da cabeça e mais largas
BANNERS = [("imagens/banner_crm_corte.png", "dentro de um crm", 270, 1000)]
DL = os.environ.get("STOCK_DIR", ".") + "/"  # pasta dos vídeos de banco usados neste exemplo
# (tipo, cena|arquivo, a partir de..., até..., [início no clipe])  -- ilustra cada EXEMPLO do roteiro, sincronizado com a fala
ILLUS = [
 ("scene", "pergunta", "você sabe de qual anúncio", "último cliente"),
 ("scene", "restaurante", "imagina aqui comigo", "bairro diferente"),
 ("scene", "salao", "no fim do mês", "chegou até ali"),
 ("scene", "panfleteiro", "resultado você não sabe", "compensa mais"),
 ("scene", "troca", "agora vamos trocar", "pela sua loja"),
 ("scene", "lead", "onde chega o lead que a sua agência traz", "no whatsapp"),
 ("stock", DL + "4857328_Tablet_Teamwork_3840x2160.mp4", "você sabe que chegou gente", "essa pessoa veio", 0.0),
 ("scene", "etiqueta", "a saída é cada cliente", "desse anúncio"),
 ("scene", "ficha", "essa informação fica na ficha dele", "final da venda desse cliente"),
 ("stock", DL + "4960692_Red_Arrow_Animation_1920x1080.mp4", "com isso você descobre em qual campanha", "colocar mais dinheiro", 0.5),
 ("scene", "verba", "e que tipo de anúncio", "no chute"),
 ("scene", "devolve", "quando você sabe de onde vem", "pro meta e pro google"),
 ("stock", DL + "0_Animation_Graphs_3840x2160.mp4", "com isso eles aprendem", "já fechou com você", 2.0),
 ("scene", "final", "onde chega o lead da sua loja hoje", "ou crm"),
]
CARD_AT = "segue o perfil da comodo"

# ================= transcrição + correções editoriais =================
words = []
for s in json.load(open(os.path.join(W, "palavras.json"), encoding="utf-8")):
    words += s["words"]
words = [w for w in words if w["s"] < DROP_AFTER]
fixed, i = [], 0
while i < len(words):
    w = words[i]
    low = re.sub(r"[^\wÀ-ÿ-]", "", w["w"].lower())
    nxt = re.sub(r"[^\wÀ-ÿ-]", "", words[i + 1]["w"].lower()) if i + 1 < len(words) else ""
    if low == "li" and nxt == "de":
        fixed.append({"w": "lead", "s": w["s"], "e": words[i + 1]["e"]}); i += 2; continue
    if low == "imóveis" and i + 1 < len(words) and "planejados" in words[i + 1]["w"].lower():
        w = dict(w, w="móveis")
    fixed.append(w); i += 1
words = fixed
def norm(t): return re.sub(r"[^\wÀ-ÿ%-]", "", t.lower())
clean = [norm(w["w"]) for w in words]
def disp(i):
    t = re.sub(r"[.,;:!]+$", "", words[i]["w"].strip())
    return DISP_FIX.get(t.lower(), t)
def find_seq(seq, start=0):
    n = len(seq)
    for i in range(start, len(clean) - n + 1):
        if clean[i:i + n] == seq: return i
    raise SystemExit("não achei no roteiro: " + " ".join(seq))

# ================= cortes de pausa =================
segs = []
cs, pe = words[0]["s"], words[0]["e"]
for w in words[1:]:
    if w["s"] - pe >= GAP:
        segs.append([max(0, cs - PAD_B), pe + PAD_A]); cs = w["s"]
    pe = w["e"]
segs.append([max(0, cs - PAD_B), pe + PAD_A])

# ================= trocas de zoom: início de frase (regra da skill) =================
starts = [i for i in range(1, len(words)) if re.search(r"[.?!]$", words[i - 1]["w"].strip())]
flips = []; last = words[0]["s"]
NUMERAL_STEPS = {"primeiro", "segundo", "terceiro", "quarto"}
for i in starts:
    ts_ = words[i]["s"]
    # elapsed medido na linha do tempo final aproximada: só tempo de fala (pausas cortadas contam pouco)
    el = ts_ - last
    if el >= FLIP_MIN or (el >= 1.4 and clean[i] in NUMERAL_STEPS):
        flips.append(max(0, ts_ - 0.09)); last = ts_
# força troca se o trecho passar de FLIP_FORCE: no próximo início de frase
fl2 = []; last = words[0]["s"]
for i in starts:
    ts_ = words[i]["s"]
    if (max(0, ts_ - 0.09)) in flips:
        fl2.append(max(0, ts_ - 0.09)); last = ts_
    elif ts_ - last > FLIP_FORCE:
        fl2.append(max(0, ts_ - 0.09)); last = ts_
flips = sorted(set(fl2))
zsegs = []
for a, b in [(s[0], s[1]) for s in segs]:
    pts = [a] + [f for f in flips if a + 0.15 < f < b - 0.25] + [b]
    for k in range(len(pts) - 1):
        n_flips = sum(1 for f in flips if f <= pts[k] + 0.15)
        zsegs.append([pts[k], pts[k + 1], n_flips % 2])
t = 0.0
for s in zsegs:
    s.append(t); t += s[1] - s[0]
TOTAL_PRE = t; TOTAL = t / SPEED
def remap_pre(x):
    for a, b, st, o in zsegs:
        if a - 0.2 <= x <= b + 0.05: return o + min(max(x, a), b) - a
    for a, b, st, o in zsegs:
        if x < a: return o
    return TOTAL_PRE
def remap(x): return remap_pre(x) / SPEED

# ================= câmera estática =================
FACE = [r for r in json.load(open(os.path.join(W, "face_src.json"))) if r["ok"]]
NX_G = float(np.median([r["nx"] for r in FACE])); NY_G = float(np.median([r["ny"] for r in FACE]))
FACE_W_SRC = float(np.median([r["fw"] for r in FACE]))
Z_W = round(FACE_W_WIDE / FACE_W_SRC, 3); Z_T = round(Z_W * ZOOM_RATIO, 3)
Xw = NX_G * 1080 * Z_W - NOSE_WIDE[0] * 1080; Yw = NY_G * 1920 * Z_W - NOSE_WIDE[1] * 1920
Cx, Cy = ANCHOR[0] * 1080, ANCHOR[1] * 1920
Sx, Sy = (Xw + Cx) / Z_W, (Yw + Cy) / Z_W
Xt, Yt = Sx * Z_T - Cx, Sy * Z_T - Cy
CAM = {0: (Z_W, int(round(Xw)), int(round(Yw))), 1: (Z_T, int(round(Xt)), int(round(Yt)))}
for z, x, y in CAM.values():
    assert 0 <= x <= 1080 * z - 1080 and 0 <= y <= 1920 * z - 1920, ("recorte fora da imagem", z, x, y)

# ================= medição de texto =================
FILES = {"sb": "Poppins-SemiBold.ttf", "b": "Poppins-Bold.ttf", "k": "Poppins-Black.ttf"}
_c = {}
def font(kind, em):
    k = (kind, round(em, 1))
    if k not in _c: _c[k] = ImageFont.truetype(os.path.join(FONTS, FILES[kind]), em)
    return _c[k]
def adv(text, kind, em): return font(kind, 1000).getlength(text) * em / 1000.0
FN = {"sb": r"\fnPoppins SemiBold\b0", "b": r"\fnPoppins\b1", "k": r"\fnPoppins Black\b0"}
def fs(em): return int(round(em * K))
def ms(x): return int(round(x * 1000))
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return "%d:%02d:%05.2f" % (h, m, s)

ev = []; overlays = []; used = set(); cursor = 0; HOLD = 0.30
SH = r"\bord0\xshad2\yshad4\4c&H00000000&\4a&H30&"

def reveal(text, t0, dur_ms=90):
    t0 = max(0.0, t0)
    return r"{\alpha&HFF&\t(%d,%d,\alpha&H00&)}%s" % (ms(t0), ms(t0) + dur_ms, text)
def line_style(txt, st):
    if st == "small": return EM_SMALL, "b"
    if st == "norm": return EM_NORM, "b"
    return int(min(EM_BIGMAX, 1000.0 * W_BIG / adv(txt, "b", 1000))), "b"
def big_motion(posy, big, x=540):
    if big:
        return r"\move(%d,%d,%d,%d,0,170)\fad(100,140)\blur9\t(0,160,0.6,\blur0)" % (x, posy + 24, x, posy)
    return r"\move(%d,%d,%d,%d,0,170)\fad(100,140)" % (x, posy + 18, x, posy)

def numeral_event(num, tn, t_end, em_n, base_n, alpha=""):
    fN = fs(em_n)
    ev.append((tn, t_end, 0, r"{\an7\pos(%d,%d)%s\fs%d\c%s%s%s\fad(120,160)\fscx80\fscy92\t(0,220,0.5,\fscx86\fscy100)}%s" % (120, base_n - 0.642 * fN, FN["k"], fN, TXT, SH, alpha, num)))

for item in BIG:
    kind = item[0]
    if kind == "stack":
        seq = [norm(x) for x in item[1].split()]
        a = find_seq(seq, cursor); lines = item[2]
        pos = a; spans = []
        for (txt, n, st) in lines:
            spans.append((pos, pos + n - 1)); pos += n
        first, last_ = spans[0][0], spans[-1][1]; cursor = last_ + 1; used.update(range(first, last_ + 1))
        t_end = remap(words[last_]["e"]) + HOLD
        # linhas -> [(palavra, instante da fala)]; texto exibido vem do DSL (ex.: "27 de novembro"), tempo de cada palavra da frase
        L = []
        for (txt, n, st), (sa, sb) in zip(lines, spans):
            ws = txt.split(); idx = list(range(sa, sb + 1))
            L.append([(w, remap(words[idx[min(j, len(idx) - 1)]]["s"])) for j, w in enumerate(ws)])
        caps = [84 if st == "small" else None for (txt, n, st) in lines]
        PENDING.append((L, t_end, caps))
    elif kind == "ghost":
        _, num, phr = item
        seq = [norm(x) for x in phr.split()]
        a = find_seq(seq, cursor); last_ = a + len(seq) - 1; used.update(range(a, last_ + 1)); cursor = last_ + 1
        numeral_event(num, remap(words[a]["s"]) - 0.04, remap(words[last_]["e"]) + 0.15, EM_ORD, 1480, alpha=r"\1a&H90&")

# blocos grandes: cada um sai SECO quando o próximo começa (nunca dois blocos juntos na tela)
PENDING.sort(key=lambda p: p[0][0][0][1])
for i_, (L, t_end, caps) in enumerate(PENDING):
    if i_ + 1 < len(PENDING):
        nxt = PENDING[i_ + 1][0][0][0][1] - 0.10 - 0.04          # início do bloco seguinte (1ª palavra - pré-roll) - folga
        t_end = max(L[0][0][1] + 0.5, min(t_end, nxt))
    evs = LD.justified_stack(FONTS, L, t_end, TXT, SH, FN["b"], layer=3, caps=caps)
    ev += evs; STACK_IV.append((evs[0][0], t_end))
# imagens, ilustrações animadas, stock e cartão (tempos ANTES da aceleração)
def window(frm, to):
    sa = [norm(x) for x in frm.split()]; sb_ = [norm(x) for x in to.split()]
    a = find_seq(sa, 0); b = find_seq(sb_, a) + len(sb_) - 1
    return remap_pre(words[a]["s"]) - 0.10, remap_pre(words[b]["e"]) + 0.25
for path, phrase, cy, bw in BANNERS:
    seq = [norm(x) for x in phrase.split()]
    a = find_seq(seq, 0); b = a + len(seq) - 1
    overlays.append(dict(kind="banner", src=path, p0=remap_pre(words[a]["s"]) - 0.06, p1=remap_pre(words[b]["e"]) + 0.12, cy=cy, bw=bw))
anim_jobs = []
for n, it in enumerate(ILLUS):
    kind, name, frm, to = it[:4]
    p0, p1 = window(frm, to)
    if kind == "scene":
        out = "frames/%s_%d" % (name, n)
        anim_jobs.append({"scene": name, "dur": round(p1 - p0, 3), "out": out})
        overlays.append(dict(kind="anim", src="motion/%s/%%04d.png" % out, p0=p0, p1=p1, cy=270, bw=900))
    else:
        overlays.append(dict(kind="stock", src=name, p0=p0, p1=p1, cy=270, bw=900, tin=it[4]))
json.dump(anim_jobs, open(os.path.join(W, "motion", "anims.json"), "w"), indent=1)
ca = find_seq([norm(x) for x in CARD_AT.split()], 0)
cs0 = remap_pre(words[ca]["s"]) - 0.35
overlays.append(dict(kind="card", src="imagens/card_seguir.png", p0=cs0, p1=cs0 + 1.7, cy=1343, bw=630))
overlays.append(dict(kind="card", src="imagens/card_seguindo.png", p0=cs0 + 1.7, p1=cs0 + 3.6, cy=1343, bw=630))

# ================= legendas corridas =================
qpre, qsuf = {}, {}
for q in QUOTES:
    seq = [norm(x) for x in q.split()]; a = find_seq(seq, 0)
    qpre[a] = "“"; qsuf[a + len(seq) - 1] = "”"
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
        txt = qpre.get(k, "") + disp(k) + qsuf.get(k, "")
        if words[k]["w"].strip().endswith("?") and not txt.endswith("?”") and not txt.endswith("?"): txt += "?"
        toks.append((txt, remap(words[k]["s"])))
    runs.append([toks[0][1] - 0.03, remap(words[grp[-1]]["e"]) + 0.25, toks])
for k in range(len(runs) - 1):
    if runs[k + 1][0] - runs[k][1] < 0.40 or runs[k][1] > runs[k + 1][0]:
        runs[k][1] = runs[k + 1][0]
bigstarts = sorted(s for s, _ in STACK_IV) + sorted(e[0] for e in ev if e[2] != 3 and e[2] != 4)
for r in runs:
    for bs in bigstarts:
        if r[0] < bs - 0.02 < r[1]: r[1] = bs - 0.02; break
big_iv = sorted(STACK_IV + [(e[0], e[1]) for e in ev if e[2] not in (3, 4)])
pos_y = BASE_CAP - 0.627 * fs(CAP_EM)
for s0, s1, toks in runs:
    for bs, be in big_iv:                      # legenda não invade o bloco grande: espera ele sair
        if bs - 0.02 <= s0 < be: s0 = be
    if s1 <= s0 + 0.12: continue
    s1 = max(s1, s0 + 0.2)
    wl = [(txt, max(ts_, s0 + 0.05)) for txt, ts_ in toks]
    ev += LD.small_caption(FONTS, wl, s1, TXT, SH, FN["sb"], em=CAP_EM, base_y=BASE_CAP, layer=4)

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
    for s, e, layer, txt in ev:
        f.write("Dialogue: %d,%s,%s,Default,,0,0,0,,%s\n" % (layer, ts(s), ts(e), txt))

# ================= filtro: câmera estática por trecho =================
vparts, mparts, vl, ml = [], [], "", ""
for n, (a, b, st, o) in enumerate(zsegs):
    z, x, y = CAM[st]
    sc = "scale=w=%d:h=%d:flags=lanczos" % (2 * int(1080 * z / 2), 2 * int(1920 * z / 2))
    vparts.append("[0:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS,%s,crop=1080:1920:%d:%d,setsar=1[v%d]" % (a, b, sc, x, y, n))
    vparts.append("[0:a]atrim=start=%.3f:end=%.3f,asetpts=PTS-STARTPTS[a%d]" % (a, b, n))
    mparts.append("[1:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS,scale=1080:1920:flags=bicubic,format=gray,%s,crop=1080:1920:%d:%d,setsar=1[m%d]" % (a, b, sc.replace("lanczos", "bicubic"), x, y, n))
    vl += "[v%d][a%d]" % (n, n); ml += "[m%d]" % n
g = vparts + mparts
g.append("%sconcat=n=%d:v=1:a=1[vc0][ac0]" % (vl, len(zsegs)))
g.append("%sconcat=n=%d:v=1:a=0[mc0]" % (ml, len(zsegs)))
g.append("[vc0]lut3d=file=%s:interp=tetrahedral,lutrgb=r='val*%.3f':g='val*%.3f':b='val*%.3f'[vc]" % (LUT, *GAIN))
g.append("[vc]split[vbase][vtop]")
chain = "[vbase]"; inputs = []; head_windows = []
def add_input(args):
    inputs.append(args); return len(inputs) + 1          # 0 = bruto, 1 = matte
for k, ov in enumerate(overlays):
    kind, p0, p1, cy, bw = ov["kind"], ov["p0"], ov["p1"], ov["cy"], ov["bw"]; d = p1 - p0
    if kind == "banner":
        idx = add_input(["-loop", "1", "-framerate", "30", "-t", "150", "-i", ov["src"]])
        pop = "(0.86+0.14*(1-pow(1-clip(t/0.22,0,1),3)))"
        g.append("[%d:v]format=rgba,scale=w='trunc(%d*%s/2)*2':h=-1:eval=frame:flags=lanczos,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st=%.3f:d=0.10:alpha=1,setpts=PTS+%.3f/TB[o%d]" % (idx, bw, pop, max(0.1, d - 0.10), p0, k))
        head_windows.append((p0, p1))
    elif kind == "card":
        idx = add_input(["-loop", "1", "-framerate", "30", "-t", "150", "-i", ov["src"]])
        pop = "(0.8+0.2*(1-pow(1-clip(t/0.25,0,1),3)))"
        g.append("[%d:v]format=rgba,scale=w='trunc(%d*%s/2)*2':h=-1:eval=frame:flags=lanczos,fade=t=in:st=0:d=0.14:alpha=1,fade=t=out:st=%.3f:d=0.14:alpha=1,setpts=PTS+%.3f/TB[o%d]" % (idx, bw, pop, max(0.15, d - 0.14), p0, k))
    elif kind == "anim":
        idx = add_input(["-framerate", "30", "-i", ov["src"]])
        pop = "(0.94+0.06*(1-pow(1-clip(t/0.2,0,1),3)))"
        g.append("[%d:v]format=rgba,scale=w='trunc(%d*%s/2)*2':h=-1:eval=frame:flags=lanczos,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st=%.3f:d=0.12:alpha=1,setpts=PTS+%.3f/TB[o%d]" % (idx, bw, pop, max(0.15, d - 0.12), p0, k))
        head_windows.append((p0, p1))
    else:   # stock: recorte 900x420, cantos arredondados, entra/sai com fade
        idx = add_input(["-i", ov["src"]]); im = add_input(["-loop", "1", "-framerate", "30", "-t", "%.2f" % (d + 1), "-i", "motion/mask.png"])
        tin = ov["tin"]
        g.append("[%d:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=2,scale=900:-2:flags=lanczos,crop=900:420,format=rgba[sc%d]" % (idx, tin, tin + d, k))
        g.append("[%d:v]format=gray[mk%d]" % (im, k))
        g.append("[sc%d][mk%d]alphamerge,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st=%.3f:d=0.12:alpha=1,setpts=PTS+%.3f/TB[o%d]" % (k, k, max(0.15, d - 0.12), p0, k))
        head_windows.append((p0, p1))
    g.append("%s[o%d]overlay=x='(W-w)/2':y='%d-h/2':enable='between(t,%.3f,%.3f)':format=auto[c%d]" % (chain, k, cy, p0, p1, k))
    chain = "[c%d]" % k
en = "+".join("between(t,%.3f,%.3f)" % w for w in head_windows)
g.append("[mc0]gblur=sigma=1.4[mc]")
g.append("[vtop][mc]alphamerge[person]")
g.append("%s[person]overlay=enable='gt(%s,0)':format=auto[comp]" % (chain, en))
g.append("[comp]setpts=PTS/%.4f,ass=legendas.ass:fontsdir=fonts[v]" % SPEED)
g.append("[ac0]atempo=%.4f,loudnorm=I=%.1f:TP=-0.3:LRA=7[a]" % (SPEED, LUFS_TARGET))
open(os.path.join(W, "filtro.txt"), "w", encoding="utf-8").write(";\n".join(g))
json.dump({"inputs": inputs, "velocidade": SPEED, "duracao_final": round(TOTAL, 2), "z_largo": Z_W, "z_fechado": Z_T, "camera": {str(k): v for k, v in CAM.items()},
           "trechos": len(zsegs), "flips_src": [round(f, 2) for f in flips], "overlays": [{k: v for k, v in o.items()} for o in overlays], "eventos": len(ev)},
          open(os.path.join(W, "cortes.json"), "w"), indent=1, default=float)
print("trechos:", len(zsegs), "| trocas de zoom:", len(flips), "| final: %.1fs" % TOTAL, "| z %.3f/%.3f" % (Z_W, Z_T), "| camera", CAM, "| eventos:", len(ev), "| blocos:", len(runs))

