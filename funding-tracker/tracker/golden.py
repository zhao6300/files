"""Golden regression set: the safety gate that every automatic rule change must pass."""
from __future__ import annotations

import json
from typing import Any

from .config import TESTS
from .extract import Rules, company_key_base, extract

FIELDS = ["company", "event", "status", "amount_usd", "valuation_usd", "arr_usd", "round", "acquirer"]


def load(path=None) -> list[dict]:
    p = path or (TESTS / "golden.jsonl")
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text("utf-8").splitlines() if l.strip()]


def _match(field: str, got: Any, want: Any) -> bool:
    if field.endswith("_usd"):
        if want is None or got is None:
            return want is None and got is None
        return abs(got - want) <= 0.03 * abs(want)
    if field in ("company", "acquirer"):
        if want is None or got is None:
            return want is None and got is None
        return company_key_base(got) == company_key_base(want)
    return got == want


def evaluate(rules: Rules | None = None, cases: list[dict] | None = None) -> dict:
    rules = rules or Rules()
    cases = cases if cases is not None else load()
    total = correct = 0
    per_field: dict[str, list[int]] = {f: [0, 0] for f in FIELDS}
    failures = []
    for c in cases:
        ex = extract(c["title"], rules).as_dict()
        bad = {}
        for f, want in c["expect"].items():
            ok = _match(f, ex.get(f), want)
            per_field[f][0] += int(ok)
            per_field[f][1] += 1
            total += 1
            correct += int(ok)
            if not ok:
                bad[f] = {"want": want, "got": ex.get(f)}
        if bad:
            failures.append({"title": c["title"], "diff": bad})
    return {
        "accuracy": correct / total if total else 1.0,
        "cases": len(cases),
        "checks": total,
        "per_field": {f: (v[0] / v[1] if v[1] else None) for f, v in per_field.items()},
        "failures": failures,
    }
