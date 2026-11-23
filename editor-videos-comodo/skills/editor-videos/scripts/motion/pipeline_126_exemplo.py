"""cues das cenas do CMD126 a partir do transcrito do PRÓPRIO CMD126 (linha do tempo final)."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
words = []
for s in json.load(open(os.path.join(ROOT, "palavras.json"), encoding="utf-8-sig")):
    for w in s["words"]:
        if w["s"] < 59.7: words.append({"w": w["w"].strip(), "s": w["s"], "e": w["e"]})
def nz(t): return re.sub(r"[^\wà-ÿ]", "", t.lower())
norm = [nz(w["w"]) for w in words]
SCENES = [
 ("bf",          "a black friday",            "cinco semanas",            ["black", "27", "novembro", "cinco"]),
 ("oito",        "segundo uma pesquisa",      "realmente mais baixos",    ["pesquisa", "8", "compram", "preços"]),
 ("vago",        "em móveis",                 "não convencendo",          ["móveis", "compara", "desconto", "convencendo"]),
 ("oferta",      "então o primeiro",          "qual que é a condição",    ["oferta", "incluso", "dia", "condição"]),
 ("condicao",    "em vez de descontão",       "até o dia x",              ["descontão", "condição", "dia"]),
 ("comecar",     "o segundo é",               "da black friday",          ["segundo", "varejo", "novembro", "planejado", "ciclo", "agora", "fecha"]),
 ("atendimento", "o terceiro passo",          "primeira resposta",        ["atendimento", "oferta", "horas", "resposta"]),
 ("final2",      "sua loja vai participar",   "e o porquê",               ["loja", "participar", "sim", "não", "porquê"]),
]
PRE, POST = 0.06, 0.30
def find_seq(seq, start):
    n = len(seq)
    for i in range(start, len(norm) - n + 1):
        if norm[i:i + n] == seq: return i
    raise SystemExit("não achei: " + " ".join(seq))
jobs, timing = [], []; cur = 0
for k, (name, frm, to, cues) in enumerate(SCENES, 1):
    a = find_seq([nz(x) for x in frm.split()], cur)
    tseq = [nz(x) for x in to.split()]; b = find_seq(tseq, a) + len(tseq) - 1; cur = b + 1
    t0 = max(0.0, words[a]["s"] - PRE); t1 = words[b]["e"] + POST
    cue_t = []; pos = a
    for c in cues:
        hit = None
        for i in range(pos, b + 1):
            if norm[i] == nz(c): hit = i; break
        if hit is None: raise SystemExit("gatilho não achado em %s: %s" % (name, c))
        cue_t.append(round(words[hit]["s"] - t0, 3)); pos = hit + 1
    # o próprio fim: deixa a cena viva até 0,3 s após a última palavra
    jobs.append({"scene": name, "cues": cue_t, "dur": round(t1 - t0, 3), "out": "frames/%02d_%s" % (k, name), "scale": 1.5})
    timing.append({"n": k, "scene": name, "inicio_s": round(t0, 2), "fim_s": round(t1, 2), "gatilhos_s": [round(t0 + c, 2) for c in cue_t],
                   "frase": " ".join(w["w"] for w in words[a:b + 1])})
for i in range(len(timing) - 1):
    if timing[i]["fim_s"] > timing[i + 1]["inicio_s"]:
        nf = timing[i + 1]["inicio_s"]; timing[i]["fim_s"] = nf; jobs[i]["dur"] = round(nf - timing[i]["inicio_s"], 3)
json.dump(jobs, open(os.path.join(HERE, "anims2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(timing, open(os.path.join(HERE, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t in timing: print("%d %-12s %5.1f-%5.1f cues %s" % (t["n"], t["scene"], t["inicio_s"], t["fim_s"], t["gatilhos_s"]))
