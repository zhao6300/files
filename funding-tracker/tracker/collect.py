"""Collection step: run every active query, store new mentions, record per-query fitness."""
from __future__ import annotations

import sys
import time

from . import store
from .config import load_json, save_json, settings
from .extract import Rules, extract
from .sources import google_news, rss


def qid(q: dict) -> str:
    return f"{q['lang']}:{q['q']}"


def active_queries() -> list[dict]:
    seeds = [{**q, "origin": "seed", "status": "pinned"} for q in (load_json("queries.json", []) or [])]
    evolved = [q for q in (load_json("queries_evolved.json", []) or []) if q.get("status") in ("trial", "active")]
    seen, out = set(), []
    for q in seeds + evolved:
        if qid(q) not in seen:
            seen.add(qid(q))
            out.append(q)
    return out


def _update_stats(stats: dict, key: str, fetched: int, new: int, deal_new: int, alpha: float) -> None:
    st = stats.setdefault(key, {"runs": 0, "fetched": 0, "new": 0, "deal_new": 0, "ema": None})
    st["runs"] += 1
    st["fetched"] += fetched
    st["new"] += new
    st["deal_new"] += deal_new
    st["ema"] = deal_new if st["ema"] is None else round(alpha * deal_new + (1 - alpha) * st["ema"], 3)
    st["last_run"] = time.strftime("%Y-%m-%d")
    st["last"] = {"fetched": fetched, "new": new, "deal_new": deal_new}


def collect(days: int | None = None, max_queries: int | None = None, include_rss: bool = True,
            log=lambda *a: print(*a, file=sys.stderr)) -> dict:
    s = settings()
    days = days or s["collect_days"]
    rules = Rules()
    existing = store.known_ids()
    stats = load_json("query_stats.json", {}) or {}
    queries = active_queries()[: max_queries or None]
    total_new = total_deal = 0
    for q in queries:
        try:
            items = google_news(q["q"], q["lang"], days)[: s["max_items_per_query"]]
        except Exception as e:  # network errors should not kill the run
            log(f"  ! {qid(q)}: {e}")
            continue
        new = store.add(items, query=q["q"], lang=q["lang"], existing=existing)
        deal_new = sum(1 for m in new if extract(m["title"], rules).deal)
        _update_stats(stats, qid(q), len(items), len(new), deal_new, s["ema_alpha"])
        total_new += len(new)
        total_deal += deal_new
        log(f"  {qid(q)[:60]:60} fetched={len(items):3} new={len(new):3} deals={deal_new:3}")
        time.sleep(s["request_pause_sec"])
    if include_rss:
        for src in load_json("sources.json", []) or []:
            if not src.get("enabled", True):
                continue
            try:
                items = rss(src["url"], src["name"])
            except Exception as e:
                log(f"  ! rss:{src['name']}: {e}")
                continue
            new = store.add(items, query=f"rss:{src['name']}", existing=existing)
            deal_new = sum(1 for m in new if extract(m["title"], rules).deal)
            _update_stats(stats, f"rss:{src['name']}", len(items), len(new), deal_new, s["ema_alpha"])
            total_new += len(new)
            total_deal += deal_new
            log(f"  rss:{src['name']:56} fetched={len(items):3} new={len(new):3} deals={deal_new:3}")
    save_json("query_stats.json", stats)
    return {"queries": len(queries), "new_mentions": total_new, "new_deal_mentions": total_deal}
