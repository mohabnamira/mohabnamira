import os
from xml.sax.saxutils import escape
from PIL import Image
import numpy as np

RAMP = " .`:-=+*cs#%@"   # bright/sparse -> dark/dense
COLS = int(os.environ.get("COLS", 100))
CW, LH, FONT = 6.0, 11.0, 10
COLOR = "#c9d1d9"

img = Image.open("source-prepped.png").convert("L")
w, h = img.size
rows = max(1, round(COLS * h / w * (CW / LH)))
px = np.array(img.resize((COLS, rows), Image.LANCZOS))

lines = ["".join(RAMP[int((255 - int(v)) / 255 * (len(RAMP) - 1))] for v in row) for row in px]

W, H = COLS * CW, rows * LH + 6
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', "<defs>"]
for i in range(rows):
    t = round(i * 0.06, 2)
    out.append(
        f'<clipPath id="c{i}"><rect x="0" y="{i*LH}" width="0" height="{LH}">'
        f'<animate attributeName="width" from="0" to="{W}" begin="{t}s" dur="0.5s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
out.append("</defs>")

for i, line in enumerate(lines):
    t = round(i * 0.06, 2)
    if line.strip():
        out.append(
            f'<text x="0" y="{(i+1)*LH-2}" font-family="monospace" font-size="{FONT}" '
            f'fill="{COLOR}" xml:space="preserve" textLength="{W}" lengthAdjust="spacing" '
            f'clip-path="url(#c{i})">{escape(line)}</text>'
        )
    out.append(
        f'<rect x="0" y="{i*LH}" width="{CW}" height="{LH}" fill="{COLOR}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{t}s"/>'
        f'<animate attributeName="x" from="0" to="{W}" begin="{t}s" dur="0.5s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0" begin="{round(t+0.5,2)}s"/></rect>'
    )
out.append("</svg>")
open("ascii-portrait.svg", "w").write("\n".join(out))
print("wrote ascii-portrait.svg")
