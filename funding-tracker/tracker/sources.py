"""News fetchers: Google News RSS search and generic RSS/Atom feeds. Standard library only."""
from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

UA = "Mozilla/5.0 (compatible; funding-tracker/0.1)"


def http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _date(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip()
    try:
        dt = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")


def _text(el: ET.Element | None) -> str:
    return html.unescape((el.text or "").strip()) if el is not None else ""


def parse_feed(raw: bytes) -> list[dict]:
    """Parse RSS 2.0 or Atom; falls back to regex if XML is malformed."""
    items: list[dict] = []
    try:
        root = ET.fromstring(raw)
        for it in root.iter("item"):
            src = it.find("source")
            items.append({
                "title": _text(it.find("title")),
                "url": _text(it.find("link")),
                "date": _date(_text(it.find("pubDate"))),
                "source": _text(src),
            })
        atom = "{http://www.w3.org/2005/Atom}"
        for it in root.iter(atom + "entry"):
            link = it.find(atom + "link")
            items.append({
                "title": _text(it.find(atom + "title")),
                "url": link.get("href", "") if link is not None else "",
                "date": _date(_text(it.find(atom + "updated")) or _text(it.find(atom + "published"))),
                "source": "",
            })
    except ET.ParseError:
        d = raw.decode("utf-8", "ignore")
        for it in re.findall(r"<item>(.*?)</item>", d, re.S):
            t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
            l = re.search(r"<link>(.*?)</link>", it, re.S)
            p = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
            items.append({
                "title": html.unescape(t.group(1).strip()) if t else "",
                "url": l.group(1).strip() if l else "",
                "date": _date(p.group(1)) if p else None,
                "source": "",
            })
    return [i for i in items if i["title"]]


def split_source(title: str, source: str) -> tuple[str, str]:
    """Google News titles look like 'Headline - Outlet'. Split off the outlet."""
    if source and title.endswith(" - " + source):
        return title[: -len(source) - 3].strip(), source
    if " - " in title:
        head, tail = title.rsplit(" - ", 1)
        if 0 < len(tail) <= 40 and len(head) > 15:
            return head.strip(), source or tail.strip()
    return title.strip(), source


def google_news(query: str, lang: str = "en", days: int | None = 7) -> list[dict]:
    q = query if (days is None or "when:" in query or "after:" in query) else f"{query} when:{days}d"
    params = "hl=zh-CN&gl=CN&ceid=CN:zh-Hans" if lang == "zh" else "hl=en-US&gl=US&ceid=US:en"
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&{params}"
    out = []
    for it in parse_feed(http_get(url)):
        title, source = split_source(it["title"], it["source"])
        out.append({**it, "title": title, "source": source})
    return out


def rss(url: str, name: str) -> list[dict]:
    out = []
    for it in parse_feed(http_get(url)):
        title, source = split_source(it["title"], it["source"] or name)
        out.append({**it, "title": title, "source": source or name})
    return out
