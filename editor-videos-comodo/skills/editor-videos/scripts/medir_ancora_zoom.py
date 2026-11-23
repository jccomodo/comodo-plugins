import sys, json, subprocess, numpy as np, cv2, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

import os
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "modelos", "selfie_segmenter.tflite")
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=M), output_confidence_masks=True, output_category_mask=False,
    running_mode=vision.RunningMode.IMAGE))

def frame(path, t, w=540, h=960):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(h, w, 3)

def person(rgb):
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    m = np.squeeze(r.confidence_masks[0].numpy_view())
    return cv2.dilate((m > 0.3).astype(np.uint8), np.ones((25, 25), np.uint8))

def register(path, tj):
    a = frame(path, tj - 0.12); b = frame(path, tj + 0.12)
    ma = person(a); mb = person(b)
    valid = ((ma == 0) & (mb == 0)).astype(np.uint8)
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), (5, 5), 0).astype(np.float32)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_RGB2GRAY), (5, 5), 0).astype(np.float32)
    best = None
    for z0 in (0.8, 0.86, 0.92, 1.0, 1.09, 1.16, 1.25):          # chute inicial de escala (b -> a)
        W = np.array([[z0, 0, 270 * (1 - z0)], [0, z0, 480 * (1 - z0)]], np.float32)
        try:
            cc, W = cv2.findTransformECC(ga, gb, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), valid, 5)
        except cv2.error:
            continue
        if best is None or cc > best[0]: best = (cc, W.copy())
    if best is None: return None
    cc, W = best                      # mapeia coords de a -> b?  (ECC: warp de template(a) para input(b))
    A = W[:, :2]; t = W[:, 2]
    # b(x) = a(A x + t)  =>  ponto fixo C de A x + t = x
    try: C = np.linalg.solve(np.eye(2) - A, t)
    except np.linalg.LinAlgError: C = np.array([np.nan, np.nan])
    return cc, A[0, 0], A[1, 1], C[0] / 540, C[1] / 960

path = sys.argv[1]; times = [float(x) for x in sys.argv[2].split(",")]
print("t(s)   escala(x)  escala(y)  correlação   ponto fixo do zoom (x,y em fração do quadro)")
for tj in times:
    r = register(path, tj)
    print(f"{tj:5.1f}  " + ("falhou" if r is None else f"{1/r[1]:.3f}      {1/r[2]:.3f}      {r[0]:.2f}        ({r[3]:.2f}, {r[4]:.2f})"))
