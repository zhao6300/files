"""Append-only, git-friendly mention store: data/mentions/YYYY-MM.jsonl.

Only raw facts (headline, outlet, date, url, query) are stored. Extraction is recomputed on
read, so every rule improvement is applied retroactively to the full history.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from collections import defaultdict
from typing import Iterable

from .config import DATA, MENTIONS
from .sources import split_source


def mention_id(title: str) -> str:
    norm = re.sub(r"\s+", " ", title.strip().lower())
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def load_all() -> list[dict]:
    out: list[dict] = []
    if not MENTIONS.exists():
        return out
    for p in sorted(MENTIONS.glob("*.jsonl")):
        for line in p.read_text("utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def known_ids() -> set[str]:
    return {m["id"] for m in load_all()}


def add(items: Iterable[dict], query: str | None = None, lang: str | None = None,
        existing: set[str] | None = None) -> list[dict]:
    """Persist items not seen before; returns the newly added mentions."""
    existing = existing if existing is not None else known_ids()
    fetched = time.strftime("%Y-%m-%d")
    by_month: dict[str, list[dict]] = defaultdict(list)
    new: list[dict] = []
    for it in items:
        title = (it.get("title") or "").strip()
        if len(title) < 8:
            continue
        mid = mention_id(title)
        if mid in existing:
            continue
        date = it.get("date") or fetched
        m = {"id": mid, "title": title, "source": it.get("source") or "", "url": it.get("url") or "",
             "date": date, "lang": lang or it.get("lang") or ("zh" if re.search(r"[\u4e00-\u9fff]", title) else "en"),
             "query": query or it.get("query") or "", "fetched": fetched}
        existing.add(mid)
        new.append(m)
        by_month[date[:7]].append(m)
    MENTIONS.mkdir(parents=True, exist_ok=True)
    for month, rows in by_month.items():
        with (MENTIONS / f"{month}.jsonl").open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return new


def import_txt(path) -> list[dict]:
    """Import 'YYYY-MM-DD | headline' lines (the format of earlier research snapshots)."""
    items = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*$", line)
        if m:
            title, source = split_source(m.group(2), "")
            items.append({"date": m.group(1), "title": title, "source": source, "query": f"import:{path.name}"})
    return add(items)


# ---------------------------------------------------------------- LLM extraction cache
LLM_CACHE = DATA / "llm_extractions.jsonl"


def load_llm_cache() -> dict[str, dict]:
    if not LLM_CACHE.exists():
        return {}
    out = {}
    for line in LLM_CACHE.read_text("utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r["extraction"]
    return out


def save_llm_results(rows: list[dict]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with LLM_CACHE.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
