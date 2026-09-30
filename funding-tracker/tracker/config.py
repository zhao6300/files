"""Paths and JSON knowledge-base helpers. All tunable knowledge lives in knowledge/*.json."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
KNOW = ROOT / "knowledge"
DATA = ROOT / "data"
MENTIONS = DATA / "mentions"
REPORTS = ROOT / "reports"
TESTS = ROOT / "tests"

DEFAULT_SETTINGS: dict[str, Any] = {
    "collect_days": 7,
    "request_pause_sec": 0.6,
    "max_items_per_query": 100,
    # score weights for the composite "heat" ranking
    "weights": {"valuation": 1.0, "heat": 1.0, "growth": 1.5, "exit": 1.0},
    # evolution
    "ema_alpha": 0.5,
    "retire_min_runs": 3,
    "retire_below_yield": 1.0,
    "promote_min_runs": 2,
    "promote_yield": 2.0,
    "max_new_queries_per_evolve": 6,
    "max_watch_queries": 30,
    "verb_min_support": 3,
    "descriptor_min_support": 3,
    "event_merge_days": 21,
    "unicorn_usd": 1e9,
}


def load_json(name: str, default: Any = None) -> Any:
    p = KNOW / name
    if not p.exists():
        return default
    return json.loads(p.read_text("utf-8"))


def save_json(name: str, obj: Any) -> None:
    KNOW.mkdir(parents=True, exist_ok=True)
    (KNOW / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", "utf-8")


def settings() -> dict[str, Any]:
    s = dict(DEFAULT_SETTINGS)
    s.update(load_json("settings.json", {}) or {})
    return s


def log_change(kind: str, detail: dict[str, Any]) -> None:
    """Append an auditable record of every automatic knowledge change."""
    KNOW.mkdir(parents=True, exist_ok=True)
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "kind": kind, **detail}
    with (KNOW / "CHANGELOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
