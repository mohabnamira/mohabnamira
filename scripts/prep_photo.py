import sys
import numpy as np
import cv2
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("usage: python scripts/prep_photo.py <photo>")

img = Image.open(sys.argv[1]).convert("RGB")

try:
    from rembg import remove
    cut = remove(img).convert("RGBA")
    alpha = np.array(cut)[:, :, 3].astype(np.float32) / 255.0
    rgb = np.array(cut)[:, :, :3]
except (Exception, SystemExit) as e:
    print("Background removal skipped:", e)
    rgb = np.array(img)
    alpha = np.ones(rgb.shape[:2], dtype=np.float32)

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
out = (gray * alpha + 255 * (1 - alpha)).clip(0, 255).astype(np.uint8)
Image.fromarray(out).save("source-prepped.png")
print("saved source-prepped.png")
