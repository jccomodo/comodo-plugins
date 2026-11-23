"""Gera o recorte (matte) da pessoa para todo o vídeo: gray8 540x960 -> matte.mkv (mesma linha do tempo do bruto)."""
import sys, subprocess, numpy as np, mediapipe as mp, os
from mediapipe.tasks.python import vision, BaseOptions

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 540, 960, 30
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "modelos", "selfie_segmenter.tflite")
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=M), output_confidence_masks=True,
    output_category_mask=False, running_mode=vision.RunningMode.IMAGE))

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-qp", "8", "-pix_fmt", "gray", OUT], stdin=subprocess.PIPE)
n = 0
prev = None
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    m = np.squeeze(r.confidence_masks[0].numpy_view())
    m = np.clip((m - 0.35) / 0.4, 0, 1)            # endurece a borda: cabelo/ombro mais firmes
    if prev is not None:
        m = 0.6 * m + 0.4 * prev                    # suaviza tremida entre quadros
    prev = m
    enc.stdin.write((m * 255).astype(np.uint8).tobytes())
    n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("quadros:", n)
