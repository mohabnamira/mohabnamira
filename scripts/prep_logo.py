import sys
import numpy as np
from PIL import Image

if len(sys.argv) < 2:
    sys.exit('usage: python scripts/prep_logo.py "<logo.png>"')

a = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)


q = (a // 16).astype(np.int32).reshape(-1, 3)
vals, counts = np.unique(q, axis=0, return_counts=True)
bg = vals[counts.argmax()] * 16 + 8


dist = np.linalg.norm(a - bg, axis=2)
ink = np.clip((dist - 40) / 60, 0, 1)


lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255
intensity = ink * (1 - 0.45 * lum)
gray = (255 * (1 - intensity)).astype(np.uint8)


ys, xs = np.where(ink > 0.5)
pad = 12
y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, gray.shape[0])
x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, gray.shape[1])
Image.fromarray(gray[y0:y1, x0:x1]).save("source-prepped.png")
print("saved source-prepped.png", gray[y0:y1, x0:x1].shape[::-1])
