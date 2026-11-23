import sys, os, json, glob, subprocess
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "modelos")
video, fps, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
tmp = out + "_frames"
os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.jpg"):
    os.remove(f)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf", f"fps={fps},scale=540:-1", "-q:v", "3", tmp + "/f%05d.jpg"], check=True)

opts = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=os.path.join(M, "face_landmarker.task")),
                                    running_mode=vision.RunningMode.IMAGE, num_faces=1)
det = vision.FaceLandmarker.create_from_options(opts)
rows = []
for i, p in enumerate(sorted(glob.glob(tmp + "/*.jpg"))):
    img = mp.Image.create_from_file(p)
    r = det.detect(img)
    t = i / fps
    if not r.face_landmarks:
        rows.append({"t": round(t, 2), "ok": False}); continue
    lm = r.face_landmarks[0]
    nose = lm[1]
    w = abs(lm[454].x - lm[234].x)
    top = lm[10].y; chin = lm[152].y
    rows.append({"t": round(t, 2), "ok": True, "nx": round(nose.x, 4), "ny": round(nose.y, 4),
                 "fw": round(w, 4), "top": round(top, 4), "chin": round(chin, 4)})
json.dump(rows, open(out, "w"))
ok = [r for r in rows if r["ok"]]
print(video, "quadros:", len(rows), "com rosto:", len(ok))
