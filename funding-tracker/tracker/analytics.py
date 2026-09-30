"""Company profiles and rankings on top of events."""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date as Date, timedelta

from .config import settings
from .events import Event, in_window
from .extract import company_key_base


@dataclass
class Profile:
    key: str
    company: str
    mentions: int = 0
    sources: int = 0
    max_valuation: float | None = None
    latest_valuation: float | None = None
    growth: float | None = None  # latest / earliest valuation within lookback
    growth_days: int | None = None
    raised: float = 0.0
    exits: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)
    region: str | None = None
    events: list[Event] = field(default_factory=list)
    score: float = 0.0


def window(days: int | None = None, since: str | None = None, until: str | None = None) -> tuple[str, str]:
    until_d = Date.fromisoformat(until) if until else Date.today()
    if since:
        return since, until_d.isoformat()
    return (until_d - timedelta(days=(days or 7) - 1)).isoformat(), until_d.isoformat()


def profiles(enriched: list[dict], events: list[Event], since: str, until: str,
             lookback_days: int = 365) -> dict[str, Profile]:
    s = settings()
    w = s["weights"]
    lb = (Date.fromisoformat(until) - timedelta(days=lookback_days)).isoformat()
    out: dict[str, Profile] = {}

    names: dict[str, Counter] = defaultdict(Counter)
    srcs: dict[str, set] = defaultdict(set)
    for m in enriched:
        x = m["x"]
        if not x.get("company") or not x.get("event"):
            continue
        k = company_key_base(x["company"])
        names[k][x["company"]] += 1
        if since <= m["date"] <= until:
            p = out.setdefault(k, Profile(key=k, company=x["company"]))
            p.mentions += 1
            if m.get("source"):
                srcs[k].add(m["source"])

    by_key: dict[str, list[Event]] = defaultdict(list)
    for e in events:
        by_key[e.key].append(e)

    for k, evs in by_key.items():
        win = [e for e in evs if in_window(e, since, until)]
        if not win:
            continue
        p = out.setdefault(k, Profile(key=k, company=win[0].company))
        p.company = names[k].most_common(1)[0][0] if names[k] else win[0].company
        p.events = win
        p.sources = len(srcs[k])
        vals = [(e.last, e.valuation_usd) for e in evs if e.valuation_usd and lb <= e.last <= until]
        vals.sort()
        if vals:
            p.max_valuation = max(v for _, v in vals)
            p.latest_valuation = vals[-1][1]
            first_d, first_v = vals[0]
            if len(vals) >= 2 and first_v and vals[-1][1] > first_v * 1.05:
                p.growth = vals[-1][1] / first_v
                p.growth_days = (Date.fromisoformat(vals[-1][0]) - Date.fromisoformat(first_d)).days
        p.raised = sum(e.amount_usd or 0 for e in win if e.event == "funding" and e.status == "closed")
        p.exits = sorted({e.event for e in win if e.event in ("ipo", "mna")})
        p.sectors = [s for s, _ in Counter(s for e in evs for s in e.sectors).most_common(2)]
        p.region = Counter(e.region for e in evs if e.region).most_common(1)[0][0] if any(e.region for e in evs) else None

    for p in out.values():
        val = math.log10((p.max_valuation or 0) / 1e8 + 1)
        heat = math.log2(p.mentions + 1)
        growth = math.log2(p.growth) if p.growth and p.growth > 1 else 0.0
        p.score = w["valuation"] * val + w["heat"] * heat + w["growth"] * growth + w["exit"] * len(p.exits)
    return out


def new_unicorns(events: list[Event], since: str, until: str, threshold: float) -> list[Event]:
    before: set[str] = {e.key for e in events if e.valuation_usd and e.valuation_usd >= threshold and e.last < since}
    seen: set[str] = set()
    out = []
    for e in sorted(events, key=lambda e: e.first):
        if (in_window(e, since, until) and e.valuation_usd and e.valuation_usd >= threshold
                and e.key not in before and e.key not in seen and e.event == "funding"):
            seen.add(e.key)
            out.append(e)
    return out
