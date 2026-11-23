"""Espera um vídeo da HeyGen ficar pronto e baixa o MP4. Só lê status; não gasta créditos.
Uso: python baixar_video.py VIDEO_ID SAIDA.mp4 [--max-min 20]
Rodar em segundo plano depois do create_video_from_avatar."""
import argparse, json, os, re, subprocess, sys, time, urllib.request

p = argparse.ArgumentParser(); p.add_argument("video_id"); p.add_argument("saida"); p.add_argument("--max-min", type=float, default=20)
a = p.parse_args()
home = os.path.expanduser("~")
env_path = next((p for p in [os.environ.get("COMODO_VIDEO_ENV"), os.path.join(home, "Comodo-Videos-Daniel", ".env"),
                             os.path.join(home, "Claude", "podcasts", ".env")] if p and os.path.exists(p)), None)
if not env_path: sys.exit("não achei o .env: rode o setup da skill")
key = None
for l in open(env_path, encoding="utf-8-sig"):
    m = re.match(r"HEYGEN_API_KEY=(.*)", l.strip())
    if m: key = m.group(1).strip().strip('"')
if not key: sys.exit("falta HEYGEN_API_KEY no .env")

fim = time.time() + a.max_min * 60
while True:
    # v1/video_status.get e v2/videos foram aposentados (nov/2026); usar só v3
    req = urllib.request.Request(f"https://api.heygen.com/v3/videos/{a.video_id}", headers={"X-Api-Key": key})
    d = json.load(urllib.request.urlopen(req))["data"]
    st = d.get("status")
    if st == "completed":
        urllib.request.urlretrieve(d["video_url"], a.saida)
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.saida], capture_output=True, text=True).stdout.strip()
        print(f"ok {a.saida} ({dur} s)"); break
    if st == "failed":
        sys.exit(f"falhou: {d.get('failure_message') or d.get('error') or d}")
    if time.time() > fim:
        sys.exit(f"ainda {st} depois de {a.max_min} min; conferir depois com get_video")
    time.sleep(30)
