"""Turn raw mentions into deduplicated deal events and per-company profiles."""
from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date as Date
from typing import Any

from .config import settings
from .extract import Extraction, Rules, company_key_base, extract, normalize_company
from .store import load_llm_cache


def _d(s: str) -> Date:
    return Date.fromisoformat(s[:10])


def enrich(mentions: list[dict], rules: Rules | None = None) -> list[dict]:
    """Attach an extraction to every mention (LLM cache wins over rules when present)."""
    rules = rules or Rules()
    cache = load_llm_cache()
    out = []
    for m in mentions:
        if m["id"] in cache:
            e = Extraction(**{k: v for k, v in cache[m["id"]].items() if k in Extraction.__dataclass_fields__})
            e.method = "llm"
            if e.company:
                e.company = normalize_company(e.company, rules)[0]
            from .extract import is_deal
            e.deal = is_deal(e)
            ex = e
        else:
            ex = extract(m["title"], rules)
        out.append({**m, "x": ex.as_dict()})
    return out


@dataclass
class Event:
    company: str
    key: str
    event: str
    status: str
    first: str
    last: str
    amount_usd: float | None
    valuation_usd: float | None
    arr_usd: float | None
    round: str | None
    acquirer: str | None
    sectors: list[str]
    region: str | None
    mentions: int
    sources: list[str]
    titles: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def _mode(vals: list):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return Counter(vals).most_common(1)[0][0]


def _money_mode(vals: list[float | None]) -> float | None:
    vals = [v for v in vals if v]
    if not vals:
        return None
    buckets = Counter(round(v, -int(len(str(int(v)))) + 2) for v in vals)  # 2 significant digits
    top = buckets.most_common(1)[0][0]
    close = [v for v in vals if abs(v - top) <= 0.1 * top]
    return statistics.median(close) if close else top


def _compatible(a: float | None, b: float | None, tol: float = 0.25) -> bool:
    if not a or not b:
        return True
    return abs(a - b) <= tol * max(a, b)


def build_events(enriched: list[dict]) -> list[Event]:
    s = settings()
    merge_days = s["event_merge_days"]
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for m in enriched:
        x = m["x"]
        if not x.get("deal"):
            continue
        groups[(company_key_base(x["company"]), x["event"])].append(m)

    events: list[Event] = []
    for (key, etype), ms in groups.items():
        ms.sort(key=lambda m: m["date"])
        clusters: list[list[dict]] = []
        for m in ms:
            x = m["x"]
            placed = False
            for c in reversed(clusters[-4:]):
                last = c[-1]
                cv = _money_mode([y["x"]["valuation_usd"] for y in c])
                ca = _money_mode([y["x"]["amount_usd"] for y in c])
                cr = _mode([y["x"]["round"] for y in c])
                gap = (_d(m["date"]) - _d(last["date"])).days
                # the same round is often re-reported weeks later ("... after raising $122B at $852B")
                same_terms = (ca and x["amount_usd"] and _compatible(ca, x["amount_usd"], 0.05)
                              and cv and x["valuation_usd"] and _compatible(cv, x["valuation_usd"], 0.10))
                if gap > merge_days and not (same_terms and gap <= 180):
                    continue
                if not _compatible(cv, x["valuation_usd"]) or not _compatible(ca, x["amount_usd"], 0.4):
                    continue
                if cr and x["round"] and cr != x["round"]:
                    continue
                c.append(m)
                placed = True
                break
            if not placed:
                clusters.append([m])
        for c in clusters:
            xs = [y["x"] for y in c]
            events.append(Event(
                company=_mode([x["company"] for x in xs]),
                key=key,
                event=etype,
                status="closed" if any(x["status"] == "closed" for x in xs) and
                       sum(x["status"] == "closed" for x in xs) >= max(1, len(xs) // 3) else "rumored",
                first=c[0]["date"], last=c[-1]["date"],
                amount_usd=_money_mode([x["amount_usd"] for x in xs]),
                valuation_usd=_money_mode([x["valuation_usd"] for x in xs]),
                arr_usd=_money_mode([x["arr_usd"] for x in xs]),
                round=_mode([x["round"] for x in xs]),
                acquirer=_mode([x["acquirer"] for x in xs]),
                sectors=[k for k, _ in Counter(s for x in xs for s in x["sectors"]).most_common(3)],
                region=_mode([x["region"] for x in xs]),
                mentions=len(c),
                sources=sorted({y["source"] for y in c if y.get("source")}),
                titles=[y["title"] for y in c[:5]],
                urls=[y["url"] for y in c[:3] if y.get("url")],
            ))
    events.sort(key=lambda e: e.first)
    return events


def in_window(e: Event, since: str, until: str) -> bool:
    return not (e.last < since or e.first > until)
