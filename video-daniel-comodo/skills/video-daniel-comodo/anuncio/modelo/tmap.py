"""Mapa de tempo de uma edição reaproveitada (mesmo roteiro, narração nova).
Os tempos escritos à mão no build (KIN, sons) e no overlay (kin, mod, P) ficam no tempo da narração ORIGINAL.
M(t_original) -> t desta narração ; N(t desta narração) -> t_original. Sem tmap.json = identidade.
tmap.json = {"cadeia": [ancoras_1, ancoras_2, ...]}: cada reaproveitamento acrescenta um elo (original -> v2 -> v3 ...).
Criado por:  python anuncio.py reaproveitar EDIT_ANTIGO VIDEO_NOVO PASTA_NOVA"""
import json, os, re, bisect, difflib
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, "tmap.json")
CADEIA = json.load(open(P, encoding="utf-8"))["cadeia"] if os.path.exists(P) else []

def _lin(pts, t):
    xs = [p[0] for p in pts]; i = bisect.bisect_right(xs, t) - 1
    if i < 0: return t - pts[0][0] + pts[0][1]
    if i >= len(pts) - 1: return t - pts[-1][0] + pts[-1][1]
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]; return y0 + (t - x0) * (y1 - y0) / (x1 - x0)

def M(t):
    for A in CADEIA: t = _lin(A, t)
    return round(t, 3)

def N(t):
    for A in reversed(CADEIA): t = _lin([(b, a) for a, b in A], t)
    return t

def ancoras(palavras_antigo, palavras_novo):
    """Palavras iguais na mesma ordem viram âncoras (início e fim de cada uma)."""
    nz = lambda x: re.sub(r"[^\wÀ-ÿ]", "", x.lower())
    ler = lambda p: [w for s in json.load(open(p, encoding="utf-8")) for w in s["words"]]
    old, new = ler(palavras_antigo), ler(palavras_novo)
    sm = difflib.SequenceMatcher(None, [nz(w["w"]) for w in old], [nz(w["w"]) for w in new], autojunk=False)
    A = [(0.0, 0.0)]; casadas = 0
    for a, b, n in sm.get_matching_blocks():
        casadas += n
        for k in range(n):
            A += [(old[a + k]["s"], new[b + k]["s"]), (old[a + k]["e"], new[b + k]["e"])]
    A = sorted(set(A)); B = [A[0]]
    for p in A[1:]:
        if p[0] > B[-1][0] + 1e-6 and p[1] > B[-1][1] + 1e-6: B.append(p)
    return B, casadas, len(old), len(new)
