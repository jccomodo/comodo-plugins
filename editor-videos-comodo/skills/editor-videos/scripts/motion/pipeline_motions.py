"""Gera cues (palavras do CMD125) -> anims.json + timing.json.  Frases e gatilhos por cena."""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
words = []
for s in json.load(open(os.path.join(ROOT, "ref125", "words.json"), encoding="utf-8-sig")):
    for w in s["words"]:
        words.append({"w": w["w"].strip(), "s": w["s"], "e": w["e"]})
def nz(t): return re.sub(r"[^\wà-ÿ]", "", t.lower())
norm = [nz(w["w"]) for w in words]

# cena, janela (de, até), gatilhos (alternativas separadas por |)
SCENES = [
 ("pergunta",    "você sabe de qual",        "com a sua loja",       ["anúncio", "último", "fechou"]),
 ("restaurante", "imagina aqui comigo",      "bairro diferente",     ["restaurante", "três", "distribuindo", "bairro"]),
 ("salao",       "no fim do mês",            "chegou até ali",       ["salão", "ninguém", "chegou"]),
 ("panfleteiro", "você não sabe qual",       "compensa mais",        ["não", "panfleteiro", "bairro", "compensa"]),
 ("troca",       "agora vamos trocar",       "sua loja",             ["panfleto", "anúncio", "restaurante", "loja"]),
 ("lead",        "onde chega o",             "mesmo problema",       ["agência", "planilha", "whatsapp", "mesmo"]),
 ("etiqueta",    "a saída é",                "desse anúncio",        ["cliente", "etiqueta", "canal", "campanha", "anúncio"]),
 ("ficha",       "essa informação fica",     "venda desse cliente",  ["ficha", "acompanha", "venda"]),
 ("verba",       "com isso você descobre",   "no chute",             ["campanha", "dinheiro", "repetir", "dividir", "chute"]),
 ("devolve",     "quando você sabe de onde", "fechou com você",      ["fecha", "devolver", "meta", "google", "anúncio", "anúncio", "aprendem", "parecida"]),
 ("final",       "onde chega",               "comenta aqui embaixo", ["loja", "tuanilha|planilha", "whatsapp", "crm"]),
]
FIX = {"lide": "lead", "tuanilha": "Planilha", "comodo": "Cômodo"}
PRE, POST = 0.06, 0.30

def find_seq(seq, start):
    n = len(seq)
    for i in range(start, len(norm) - n + 1):
        if norm[i:i + n] == seq: return i
    raise SystemExit("não achei: " + " ".join(seq))

jobs, timing = [], []
cur = 0
for k, (name, frm, to, cues) in enumerate(SCENES, 1):
    a = find_seq([nz(x) for x in frm.split()], cur)
    tseq = [nz(x) for x in to.split()]
    b = find_seq(tseq, a) + len(tseq) - 1
    cur = b + 1
    t0 = max(0.0, words[a]["s"] - PRE); t1 = words[b]["e"] + POST
    cue_t = []; pos = a
    for c in cues:
        alts = c.split("|"); hit = None
        for i in range(pos, b + 1):
            if norm[i] in [nz(x) for x in alts]: hit = i; break
        if hit is None: raise SystemExit("gatilho não achado em %s: %s" % (name, c))
        cue_t.append(round(words[hit]["s"] - t0, 3)); pos = hit + 1
    phrase = " ".join(FIX.get(nz(w["w"]), w["w"]) for w in words[a:b + 1])
    phrase = re.sub(r"[:*\"<>|/\\]", "", phrase.replace("?", ",")).strip().rstrip(".,")
    phrase = phrase[0].upper() + phrase[1:]
    dur = round(t1 - t0, 3)
    out = "frames/%02d_%s" % (k, name)
    jobs.append({"scene": name, "cues": cue_t, "dur": dur, "out": out, "scale": 1.5})
    timing.append({"n": k, "scene": name, "frase": phrase, "inicio_s": round(t0, 2), "fim_s": round(t0 + dur, 2), "duracao_s": dur, "gatilhos_s": [round(t0 + c, 2) for c in cue_t],
                   "arquivo": "%02d - %s.mov" % (k, phrase)})
# um motion termina quando o próximo começa (sem sobreposição)
for i in range(len(timing) - 1):
    if timing[i]["fim_s"] > timing[i + 1]["inicio_s"]:
        nf = timing[i + 1]["inicio_s"]
        timing[i]["fim_s"] = nf; timing[i]["duracao_s"] = round(nf - timing[i]["inicio_s"], 3)
        jobs[i]["dur"] = timing[i]["duracao_s"]
json.dump(jobs, open(os.path.join(HERE, "anims2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(timing, open(os.path.join(HERE, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t in timing: print("%02d %-12s %5.1f-%5.1f (%4.1fs) gatilhos %s | %s" % (t["n"], t["scene"], t["inicio_s"], t["fim_s"], t["duracao_s"], t["gatilhos_s"], t["frase"][:60]))

