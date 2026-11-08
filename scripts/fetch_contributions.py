import json, os, re, sys
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER", "mohabnamira")
r = requests.get(f"https://github.com/users/{USER}/contributions",
                 headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day"):
    d = td.get("data-date")
    if not d:
        continue
    m = re.match(r"(\d+)\s+contribution", tips.get(td.get("id"), ""))
    days.append({"date": d, "count": int(m.group(1)) if m else 0,
                 "level": int(td.get("data-level", 0))})

if not days:
    sys.exit("No contribution cells found - GitHub's HTML may have changed.")
days.sort(key=lambda x: x["date"])

total = sum(d["count"] for d in days)
best = max(days, key=lambda d: d["count"])

longest = run = 0
for d in days:
    run = run + 1 if d["count"] > 0 else 0
    longest = max(longest, run)

current = 0
for d in reversed(days):
    if d["count"] > 0:
        current += 1
    elif d is days[-1]:
        continue          # today may not have contributions yet
    else:
        break

monthly = {}
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

os.makedirs("data", exist_ok=True)
json.dump({"user": USER, "total": total, "current_streak": current,
           "longest_streak": longest, "best_day": best, "monthly": monthly,
           "days": days}, open("data/contributions.json", "w"), indent=1)
print(f"{total} contributions, {len(days)} days saved")
