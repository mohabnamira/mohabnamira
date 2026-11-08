import json
from datetime import date, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
data = json.load(open("data/contributions.json"))
days = data["days"]

first = date.fromisoformat(days[0]["date"])
start = first - timedelta(days=(first.weekday() + 1) % 7)   # back to Sunday
weeks = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1

CELL, GAP = 12, 3
STEP = CELL + GAP
LEFT, TOP = 34, 30
W = 860
H = TOP + 7 * STEP + 50

STYLE = """<style>
.c{opacity:0;animation:pop .45s ease-out forwards}
@keyframes pop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
text{font-family:monospace;fill:#8b949e;font-size:10px}
</style>"""

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         STYLE, f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117"/>']

for w in range(weeks):
    s = start + timedelta(days=7 * w)
    if s.day <= 7:
        parts.append(f'<text x="{LEFT + w*STEP}" y="{TOP-8}">{s.strftime("%b")}</text>')
for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    parts.append(f'<text x="4" y="{TOP + row*STEP + 10}">{name}</text>')

mx = max(d["count"] for d in days) or 1
for d in days:
    idx = (date.fromisoformat(d["date"]) - start).days
    w, dow = divmod(idx, 7)
    lvl = min(d["level"], 4)
    if lvl == 4 and d["count"] >= 0.75 * mx:
        lvl = 5
    delay = round((w + dow) * 0.018, 3)
    parts.append(
        f'<rect class="c" x="{LEFT + w*STEP}" y="{TOP + dow*STEP}" width="{CELL}" height="{CELL}" '
        f'rx="2" fill="{PALETTE[lvl]}" style="animation-delay:{delay}s">'
        f'<title>{d["count"]} contributions on {d["date"]}</title></rect>')

fy = TOP + 7 * STEP + 24
parts.append(f'<text x="{LEFT}" y="{fy}">{data["total"]:,} contributions in the last year'
             f' · longest streak {data["longest_streak"]} days · current streak {data["current_streak"]}</text>')
lx = W - 190
parts.append(f'<text x="{lx}" y="{fy}">Less</text>')
for i, c in enumerate(PALETTE):
    parts.append(f'<rect x="{lx + 30 + i*15}" y="{fy-10}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
parts.append(f'<text x="{lx + 30 + len(PALETTE)*15 + 4}" y="{fy}">More</text>')
parts.append("</svg>")

open("contrib-heatmap.svg", "w").write("\n".join(parts))
print("wrote contrib-heatmap.svg")
