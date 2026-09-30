#!/usr/bin/env python3
"""Query Google News RSS and print dated headlines. Usage: gn.py "query" [max] [lang]"""
import sys, urllib.request, urllib.parse, re, html
from email.utils import parsedate_to_datetime

q = sys.argv[1]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 25
lang = sys.argv[3] if len(sys.argv) > 3 else "en"
if lang == "zh":
    params = "hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
else:
    params = "hl=en-US&gl=US&ceid=US:en"
url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&{params}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
d = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
items = re.findall(r"<item>(.*?)</item>", d, re.S)
rows = []
for it in items:
    t = html.unescape(re.search(r"<title>(.*?)</title>", it, re.S).group(1))
    p = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
    dt = parsedate_to_datetime(p.group(1)) if p else None
    rows.append((dt, t))
rows.sort(key=lambda r: r[0].timestamp() if r[0] else 0, reverse=True)
print(f"### {q}")
seen = []
n = 0
for dt, t in rows:
    base = t.rsplit(" - ", 1)[0]
    w = set(re.findall(r"\w+", base.lower()))
    if any(len(w & s) / max(1, len(w | s)) > 0.35 for s in seen):
        continue
    seen.append(w)
    print((dt.strftime("%Y-%m-%d") if dt else "????"), "|", base)
    n += 1
    if n >= mx:
        break
