import os

STATIC = os.environ.get("STATIC") == "1"
HANDLE = "mohabnamira"

# ---- EDIT THESE (keep each value under ~45 characters) ----
ROWS = [
    ("Now", "what you're working on"),
    ("Prev", "what you did before"),
    ("Stack", "Python, Git, ..."),
    ("Highlights", "something you're proud of"),
]
# -----------------------------------------------------------

W, LINE_H, TOP = 490, 26, 64
H = TOP + (len(ROWS) + 2) * LINE_H + 20

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def row(i, y, inner):
    if STATIC:
        return f'<g transform="translate(0,{y})">{inner}</g>'
    t = round(0.5 + i * 0.35, 2)
    return (
        f'<g opacity="0" transform="translate(0,{y+6})">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{t}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 {y+6}" to="0 {y}" '
        f'begin="{t}s" dur="0.4s" fill="freeze"/></g>'
    )

head = f"{HANDLE}@github"
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="monospace" font-size="14">',
    f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
    f'<path d="M0 8a8 8 0 0 1 8-8h{W-16}a8 8 0 0 1 8 8v24H0z" fill="#161b22"/>',
    '<circle cx="20" cy="16" r="5" fill="#ff5f56"/><circle cx="38" cy="16" r="5" fill="#ffbd2e"/><circle cx="56" cy="16" r="5" fill="#27c93f"/>',
    f'<text x="{W/2}" y="21" text-anchor="middle" fill="#8b949e" font-size="12">neofetch</text>',
]

y = TOP
parts.append(row(0, y, f'<text x="24" y="0" fill="#3fb950" font-weight="bold">{esc(head)}</text>'))
y += LINE_H
parts.append(row(1, y, f'<text x="24" y="0" fill="#484f58">{"-" * len(head)}</text>'))
for i, (k, v) in enumerate(ROWS):
    y += LINE_H
    parts.append(row(i + 2, y, f'<text x="24" y="0" fill="#58a6ff" font-weight="bold">{esc(k)}</text>'
                                f'<text x="130" y="0" fill="#c9d1d9">{esc(v)}</text>'))
parts.append("</svg>")
open("info-card.svg", "w").write("\n".join(parts))
print("wrote info-card.svg")
