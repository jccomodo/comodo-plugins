"""Legendas no padrão do designer (medido no CMD126 aprovado).

REGRAS MEDIDAS
- Bloco "justificado": TODAS as linhas do bloco têm a mesma largura de tinta (~670 px), centradas em x=540.
  Linha curta ("de 2026") fica enorme (em ~172); linha longa ("Black Friday") fica menor (em ~106). Isso cria hierarquia sem precisar de "tamanho de destaque".
- Linhas coladas: topo (ascendente) da linha seguinte = baseline da anterior + ~0,255·em da anterior.
- Base da última linha em y=1480; o bloco cresce para CIMA.
- Cada palavra entra no instante da fala (-0,10 s), SUBINDO ~50 px com desfoque 10→0 e fade-in, ease-out cúbico em ~0,4 s.
- O bloco inteiro sai seco quando começa a próxima frase (fade de 70 ms).
- Legenda pequena (Poppins SemiBold 59, base 1482) usa a mesma entrada, só mais suave (sobe 16 px, desfoque 6).
"""
import os, re
from PIL import ImageFont

K = 1.78                       # \fs do libass = em × 1,78 (medido em frases 60–420 px; 1,93 era erro de letras soltas)
BLOCK_W, EM_MIN, EM_MAX = 670, 44, 185
BASE_Y = 1480
GAP_K, TOP_K = 0.255, 0.76     # folga entre linhas (× em da linha de cima) e altura da ascendente (× em)

_cache = {}
def font(fonts_dir, kind, em):
    file = {"sb": "Poppins-SemiBold.ttf", "b": "Poppins-Bold.ttf", "k": "Poppins-Black.ttf"}[kind]
    k = (fonts_dir, file)
    if k not in _cache: _cache[k] = ImageFont.truetype(os.path.join(fonts_dir, file), 1000)
    return _cache[k]

def ink(fonts_dir, text, kind):
    f = font(fonts_dir, kind, 1000); bb = f.getbbox(text, anchor="ls")
    return bb[0] / 1000.0, bb[2] / 1000.0, f.getlength(text) / 1000.0          # (esq, dir, avanço) por 1 em

def fit_em(fonts_dir, text, kind="b", width=BLOCK_W):
    l, r, _ = ink(fonts_dir, text, kind)
    return max(EM_MIN, min(EM_MAX, width / (r - l)))

def top_off(fs):               # \an7: linha de base = pos_y + off·fs (medido 0,627 em 59–78 e 0,642 em 520)
    return 0.627 + max(0, min(1, (fs - 78) / 442.0)) * 0.015

def ass_ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return "%d:%02d:%05.2f" % (h, m, s)

def _entry_events(t0, t1, x, y_base, fs, kind, text, rise, blur0, dur, color, shadow, fn, fade_out=0.07, layer=0):
    """Uma palavra: entra subindo (ease-out cúbico em 4 trechos lineares) com desfoque e fade-in; depois fica parada até t1."""
    ev = []
    top = y_base - top_off(fs) * fs
    segs = 4; d = dur / segs
    prog = [1 - (1 - i / float(segs)) ** 3 for i in range(segs + 1)]          # 0 .58 .875 .98 1
    for i in range(segs):
        a = t0 + i * d; b = t0 + (i + 1) * d
        if a >= t1: break
        b = min(b, t1)
        y0 = top + rise * (1 - prog[i]); y1 = top + rise * (1 - prog[i + 1])
        bl0 = blur0 * (1 - prog[i]); bl1 = blur0 * (1 - prog[i + 1])
        al = r"\alpha&HFF&\t(0,%d,\alpha&H00&)" % int(min(dur, 0.18) * 1000) if i == 0 else r"\alpha&H00&"
        ev.append((a, b, layer, r"{\an7\move(%d,%.1f,%d,%.1f,0,%d)%s%s\fs%d\blur%.1f\t(0,%d,\blur%.1f)\c%s%s}%s" % (
            x, y0, x, y1, int((b - a) * 1000), fn, "", fs, bl0, int((b - a) * 1000), bl1, color, shadow + al, text)))
    if t1 > t0 + dur:
        ev.append((t0 + dur, t1, layer, r"{\an7\pos(%d,%.1f)%s\fs%d\c%s%s%s}%s" % (
            x, top, fn, fs, color, shadow, (r"\fad(0,%d)" % int(fade_out * 1000)) if fade_out else "", text)))
    return ev

def justified_stack(fonts_dir, lines, t_end, color, shadow, fn_bold, base_y=BASE_Y, width=BLOCK_W, layer=0, kind="b", caps=None):
    """lines = [ [(palavra, t_inicio_fala), ...], ... ]  (de cima para baixo). Retorna eventos ASS (start, end, layer, texto)."""
    ems, texts = [], []
    for i, ln in enumerate(lines):
        t = " ".join(w for w, _ in ln); texts.append(t); e = fit_em(fonts_dir, t, kind, width)
        if caps and caps[i]: e = min(e, caps[i])          # linha de CONTEXTO (ex.: 'só que'): corpo limitado, não vira destaque
        ems.append(e)
    bases = [0] * len(lines); bases[-1] = base_y
    for k in range(len(lines) - 2, -1, -1):
        top_next = bases[k + 1] - TOP_K * ems[k + 1]
        bases[k] = top_next - GAP_K * ems[k]
    ev = []
    for k, ln in enumerate(lines):
        em = ems[k]; fs = int(round(em * K)); l, r, adv = ink(fonts_dir, texts[k], kind)
        x_origin = 540 - ((r - l) * em) / 2.0 - l * em
        pos = 0
        for (w, ts_) in ln:
            prefix = texts[k][:pos]; x = x_origin + ink(fonts_dir, prefix, kind)[2] * em if prefix else x_origin
            pos += len(w) + 1
            ev += _entry_events(ts_ - 0.10, t_end, int(round(x)), bases[k], fs, kind, w, rise=50, blur0=10, dur=0.40,
                                color=color, shadow=shadow, fn=fn_bold, layer=layer)
    return ev

def small_caption(fonts_dir, words, t_end, color, shadow, fn_semibold, em=59, base_y=1482, layer=0):
    """Legenda corrida: 1–4 palavras numa linha centrada; cada palavra entra no instante da fala (sobe 16 px, desfoque 6)."""
    text = " ".join(w for w, _ in words); l, r, adv = ink(fonts_dir, text, "sb")
    fs = int(round(em * K)); x_origin = 540 - ((r - l) * em) / 2.0 - l * em; pos = 0; ev = []
    for (w, ts_) in words:
        prefix = text[:pos]; x = x_origin + (ink(fonts_dir, prefix, "sb")[2] * em if prefix else 0); pos += len(w) + 1
        ev += _entry_events(ts_ - 0.05, t_end, int(round(x)), base_y, fs, "sb", w, rise=16, blur0=6, dur=0.26,
                            color=color, shadow=shadow, fn=fn_semibold, fade_out=0, layer=layer)
    return ev


