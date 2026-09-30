"""Optional LLM extraction for headlines the rules cannot parse.

Works with any OpenAI-compatible chat-completions API (OpenAI, DeepSeek, Qwen, Kimi, local vLLM...):
  FT_LLM_API_KEY   required to enable
  FT_LLM_BASE_URL  default https://api.openai.com/v1
  FT_LLM_MODEL     default gpt-4o-mini
Results are cached in data/llm_extractions.jsonl so each headline is paid for only once.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request

PROMPT = """You extract startup deal facts from news headlines (English or Chinese).
Return JSON: {"items": [ ... one object per headline, same order ... ]}. Each object:
{"company": string|null (the startup the deal is about; for M&A the TARGET),
 "event": "funding"|"ipo"|"mna"|"arr"|null (null if not a concrete deal/IPO/M&A/revenue milestone),
 "status": "closed"|"rumored" (rumored if in talks / reportedly / seeks / plans / 洽谈 / 拟),
 "amount_usd": number|null (money raised, IPO proceeds or M&A price, converted to USD),
 "valuation_usd": number|null, "arr_usd": number|null,
 "round": string|null (e.g. "Seed", "Series B", "A+轮"),
 "acquirer": string|null}
Use plain numbers (1.5 billion -> 1500000000). EUR=1.1 USD, GBP=1.3, CNY=0.14. Do not guess missing facts."""


def available() -> bool:
    return bool(os.environ.get("FT_LLM_API_KEY"))


def extract_batch(titles: list[str], timeout: int = 90) -> list[dict | None]:
    base = (os.environ.get("FT_LLM_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("FT_LLM_MODEL") or "gpt-4o-mini"
    body = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": "\n".join(f"{i + 1}. {t}" for i, t in enumerate(titles))},
        ],
    }
    req = urllib.request.Request(
        base + "/chat/completions", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.environ['FT_LLM_API_KEY']}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", content, re.S)
    items = json.loads(m.group(0)).get("items", []) if m else []
    out: list[dict | None] = []
    for i in range(len(titles)):
        it = items[i] if i < len(items) and isinstance(items[i], dict) else None
        if it is not None:
            it = {k: it.get(k) for k in ("company", "event", "status", "amount_usd", "valuation_usd", "arr_usd",
                                         "round", "acquirer")}
            it["status"] = it.get("status") or "closed"
            if it.get("event") not in ("funding", "ipo", "mna", "arr"):
                it["event"] = None
            for k in ("amount_usd", "valuation_usd", "arr_usd"):
                try:
                    it[k] = float(it[k]) if it[k] not in (None, "", 0) else None
                except (TypeError, ValueError):
                    it[k] = None
        out.append(it)
    return out
