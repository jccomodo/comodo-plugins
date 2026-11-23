"""Decupagem automática de um vídeo falado (local, sem internet).

Uso:
  python decupar.py VIDEO [--modelo medium|large-v3] [--saida PASTA]

Gera na pasta de saída (padrão: <video>_decupagem):
  palavras.json   palavra por palavra com início/fim (s)
  frases.json     frases com início/fim, pausa antes e marcas
  decupagem.md    tabela legível: tempo, frase, marcas, decisão sugerida
  cortes.txt      trechos a CORTAR, já no formato do auto-editor: "12.40sec,15.10sec 40.02sec,41.80sec" (uma linha)

Marcas:
  PAUSA     pausa >= 0,5 s antes da frase (o auto-editor corta sozinho)
  RETAKE    frase repetida/recomeçada: a anterior parecida vira CORTAR (fica a última tomada)
  MULETA    "né", "tipo", "éé", "hum" soltos (só aviso; cortar no meio da frase costuma pular)
  FALSO     frase curta abandonada (< 4 palavras seguida de recomeço)
  INCOMPLETA última frase sem pontuação final (gravação parou no meio): sugerida para cortar
"""
import argparse, json, os, re, sys, difflib, warnings
warnings.filterwarnings("ignore")

MULETAS = {"né", "tipo", "éé", "é...", "hum", "humm", "ahn", "ah", "eh", "ãh", "então,"}


def norm(t):
    t = t.lower()
    t = re.sub(r"[^\wà-ú ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def transcrever(video, modelo):
    from faster_whisper import WhisperModel
    try:
        m = WhisperModel(modelo, device="cuda", compute_type="float16")
        segs, _ = m.transcribe(video, language="pt", word_timestamps=True, vad_filter=True)
        segs = list(segs)
    except Exception:
        m = WhisperModel(modelo, device="cpu", compute_type="int8")
        segs, _ = m.transcribe(video, language="pt", word_timestamps=True, vad_filter=True)
        segs = list(segs)
    palavras = []
    for s in segs:
        for w in (s.words or []):
            palavras.append({"t": w.word.strip(), "ini": round(w.start, 3), "fim": round(w.end, 3)})
    return palavras


def frases_de(palavras):
    """Quebra em frases por pontuação final ou pausa >= 0,6 s."""
    frases, atual = [], []
    for i, w in enumerate(palavras):
        atual.append(w)
        prox = palavras[i + 1] if i + 1 < len(palavras) else None
        pausa = (prox["ini"] - w["fim"]) if prox else 99
        if re.search(r"[.!?]$", w["t"]) or pausa >= 0.6:
            frases.append(atual)
            atual = []
    if atual:
        frases.append(atual)
    out = []
    for k, f in enumerate(frases):
        texto = " ".join(w["t"] for w in f)
        pausa_antes = round(f[0]["ini"] - frases[k - 1][-1]["fim"], 2) if k else round(f[0]["ini"], 2)
        out.append({"n": k + 1, "ini": f[0]["ini"], "fim": f[-1]["fim"], "texto": texto,
                    "pausa_antes": pausa_antes, "marcas": [], "decisao": "manter"})
    return out


def marcar(frases):
    for k, f in enumerate(frases):
        if f["pausa_antes"] >= 0.5 and k:
            f["marcas"].append("PAUSA")
        toks = norm(f["texto"]).split()
        if any(t in MULETAS for t in toks):
            f["marcas"].append("MULETA")
        # retake: a frase seguinte (até 2 adiante) começa igual ou é muito parecida
        for j in (k + 1, k + 2):
            if j >= len(frases):
                break
            a, b = norm(f["texto"]), norm(frases[j]["texto"])
            if not a or not b:
                continue
            sim = difflib.SequenceMatcher(None, a, b).ratio()
            inicio_igual = a.split()[:3] == b.split()[:3] and len(a.split()) >= 3
            curta = len(a.split()) < 4 and b.startswith(a.split()[0])
            if sim >= 0.72 or inicio_igual:
                f["marcas"].append(f"RETAKE (repetida na frase {frases[j]['n']})")
                f["decisao"] = "CORTAR"
                break
            if curta:
                f["marcas"].append(f"FALSO (recomeça na frase {frases[j]['n']})")
                f["decisao"] = "CORTAR"
                break
    # última frase sem ponto final e curta = gravação parou no meio ("O que faz...")
    if frases:
        u = frases[-1]
        tx = u["texto"].strip()
        if (not re.search(r"[.!?]$", tx) or tx.endswith("...")) and len(norm(tx).split()) < 8 and u["decisao"] != "CORTAR":
            u["marcas"].append("INCOMPLETA (revisar)")
            u["decisao"] = "CORTAR"
    return frases


def fmt(s):
    return f"{int(s // 60)}:{s % 60:05.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--modelo", default="medium")
    ap.add_argument("--saida")
    a = ap.parse_args()
    saida = a.saida or os.path.splitext(a.video)[0] + "_decupagem"
    os.makedirs(saida, exist_ok=True)

    palavras = transcrever(a.video, a.modelo)
    frases = marcar(frases_de(palavras))

    json.dump(palavras, open(os.path.join(saida, "palavras.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    json.dump(frases, open(os.path.join(saida, "frases.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)

    cortes = []
    for f in frases:
        if f["decisao"] == "CORTAR":
            # corta da frase descartada até o começo da próxima fala (sem comer a palavra seguinte)
            cortes.append((max(0, f["ini"] - 0.05), f["fim"] + 0.05))
    with open(os.path.join(saida, "cortes.txt"), "w", encoding="utf8") as fh:
        fh.write(" ".join(f"{i:.2f}sec,{fi:.2f}sec" for i, fi in cortes) + "\n")  # cola direto depois de --cut

    linhas = ["# Decupagem: " + os.path.basename(a.video), "",
              f"{len(palavras)} palavras, {len(frases)} frases, {len(cortes)} trechos sugeridos para cortar.", "",
              "| # | Tempo | Pausa antes | Frase | Marcas | Decisão |", "|---|---|---|---|---|---|"]
    for f in frases:
        linhas.append(f"| {f['n']} | {fmt(f['ini'])} a {fmt(f['fim'])} | {f['pausa_antes']:.2f} s | {f['texto']} | "
                      f"{', '.join(f['marcas'])} | {f['decisao']} |")
    open(os.path.join(saida, "decupagem.md"), "w", encoding="utf8").write("\n".join(linhas) + "\n")
    print(f"ok: {saida}  ({len(frases)} frases, {len(cortes)} cortes sugeridos)")


if __name__ == "__main__":
    main()
