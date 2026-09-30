"""Markdown / CSV reports. Each section is a small function so new report types can reuse them."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from .analytics import Profile, new_unicorns, profiles
from .config import KNOW, REPORTS, settings
from .events import Event, in_window


def usd(v: float | None) -> str:
    if not v:
        return "—"
    if v >= 1e12:
        return f"${v / 1e12:.2f}T"
    if v >= 1e9:
        return f"${v / 1e9:.1f}B" if v < 1e11 else f"${v / 1e9:.0f}B"
    if v >= 1e6:
        return f"${v / 1e6:.0f}M"
    return f"${v / 1e3:.0f}K"


def _st(e: Event) -> str:
    return "" if e.status == "closed" else "（谈判/传闻）"


def _src(e: Event) -> str:
    return f"{e.mentions}篇" + (f"·{len(e.sources)}家媒体" if e.sources else "")


def _link(e: Event) -> str:
    title = e.titles[0].replace("|", "/")[:90] if e.titles else ""
    return f"[{title}]({e.urls[0]})" if e.urls else title


def section_funding(evs: list[Event], top: int) -> list[str]:
    rows = sorted([e for e in evs if e.event == "funding" and (e.amount_usd or e.valuation_usd)],
                  key=lambda e: (e.amount_usd or 0, e.valuation_usd or 0), reverse=True)[:top]
    out = ["## 大额融资", "", "| # | 公司 | 金额 | 估值 | 轮次 | 赛道 | 日期 | 报道 | 代表标题 |", "|---|---|---|---|---|---|---|---|---|"]
    for i, e in enumerate(rows, 1):
        out.append(f"| {i} | **{e.company}**{_st(e)} | {usd(e.amount_usd)} | {usd(e.valuation_usd)} | {e.round or '—'} | "
                   f"{'/'.join(e.sectors[:2]) or '—'} | {e.first} | {_src(e)} | {_link(e)} |")
    return out + [""]


def section_growth(profs: dict[str, Profile], top: int) -> list[str]:
    rows = sorted([p for p in profs.values() if p.growth], key=lambda p: p.growth, reverse=True)[:top]
    if not rows:
        return []
    out = ["## 估值跃升", "", "| 公司 | 估值变化 | 倍数 | 间隔 | 赛道 |", "|---|---|---|---|---|"]
    for p in rows:
        first = p.latest_valuation / p.growth
        out.append(f"| **{p.company}** | {usd(first)} → {usd(p.latest_valuation)} | {p.growth:.1f}x | {p.growth_days}天 | "
                   f"{'/'.join(p.sectors) or '—'} |")
    return out + [""]


def section_unicorns(uni: list[Event]) -> list[str]:
    if not uni:
        return []
    out = ["## 新晋独角兽（按本库记录首次估值≥10亿美元）", "", "| 公司 | 估值 | 金额 | 轮次 | 赛道 | 日期 |", "|---|---|---|---|---|---|"]
    for e in sorted(uni, key=lambda e: e.valuation_usd or 0, reverse=True):
        out.append(f"| **{e.company}**{_st(e)} | {usd(e.valuation_usd)} | {usd(e.amount_usd)} | {e.round or '—'} | "
                   f"{'/'.join(e.sectors[:2]) or '—'} | {e.first} |")
    return out + [""]


def section_exits(evs: list[Event]) -> list[str]:
    ipo = sorted([e for e in evs if e.event == "ipo"], key=lambda e: (e.mentions, e.valuation_usd or 0), reverse=True)
    mna = sorted([e for e in evs if e.event == "mna"], key=lambda e: (e.amount_usd or 0, e.mentions), reverse=True)
    out = []
    if ipo:
        out += ["## IPO / 上市", "", "| 公司 | 市值/估值 | 募资 | 日期 | 报道 | 代表标题 |", "|---|---|---|---|---|---|"]
        out += [f"| **{e.company}**{_st(e)} | {usd(e.valuation_usd)} | {usd(e.amount_usd)} | {e.first} | {_src(e)} | {_link(e)} |"
                for e in ipo[:15]] + [""]
    if mna:
        out += ["## 并购", "", "| 标的 | 收购方 | 金额 | 日期 | 报道 | 代表标题 |", "|---|---|---|---|---|---|"]
        out += [f"| **{e.company}**{_st(e)} | {e.acquirer or '—'} | {usd(e.amount_usd)} | {e.first} | {_src(e)} | {_link(e)} |"
                for e in mna[:15]] + [""]
    return out


def section_arr(evs: list[Event]) -> list[str]:
    rows = sorted([e for e in evs if e.arr_usd], key=lambda e: e.arr_usd, reverse=True)[:15]
    if not rows:
        return []
    out = ["## 收入里程碑（年化收入/ARR）", "", "| 公司 | 年化收入 | 日期 | 代表标题 |", "|---|---|---|---|"]
    out += [f"| **{e.company}** | {usd(e.arr_usd)} | {e.first} | {_link(e)} |" for e in rows]
    return out + [""]


def section_sectors(evs: list[Event]) -> list[str]:
    cnt: Counter = Counter()
    amt: dict[str, float] = defaultdict(float)
    for e in evs:
        if e.event != "funding":
            continue
        for s in (e.sectors[:1] or ["未分类"]):
            cnt[s] += 1
            if e.status == "closed":
                amt[s] += e.amount_usd or 0
    if not cnt:
        return []
    out = ["## 赛道分布（融资事件）", "", "| 赛道 | 事件数 | 已完成融资额 |", "|---|---|---|"]
    out += [f"| {s} | {n} | {usd(amt[s])} |" for s, n in cnt.most_common()]
    return out + [""]


def section_heat(profs: dict[str, Profile], top: int) -> list[str]:
    rows = sorted([p for p in profs.values() if p.events], key=lambda p: p.score, reverse=True)[:top]
    out = ["## 综合热度榜", "", "评分 = 估值规模 + 报道热度 + 估值增速 + 退出事件（权重见 `knowledge/settings.json`）", "",
           "| # | 公司 | 评分 | 报道数 | 最高估值 | 增速 | 本期已融 | 退出 | 赛道 |", "|---|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(rows, 1):
        out.append(f"| {i} | **{p.company}** | {p.score:.1f} | {p.mentions} | {usd(p.max_valuation)} | "
                   f"{f'{p.growth:.1f}x' if p.growth else '—'} | {usd(p.raised) if p.raised else '—'} | "
                   f"{'/'.join(p.exits) or '—'} | {'/'.join(p.sectors) or '—'} |")
    return out + [""]


def section_evolution(since: str) -> list[str]:
    p = KNOW / "CHANGELOG.jsonl"
    if not p.exists():
        return []
    rows = [json.loads(l) for l in p.read_text("utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r["ts"][:10] >= since]
    if not rows:
        return []
    c = Counter(r["kind"] for r in rows)
    out = ["## 本期工具进化", "", "| 变更类型 | 次数 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in c.most_common()] + [""]
    out += ["明细见 `knowledge/CHANGELOG.jsonl`。", ""]
    return out


def build(enriched: list[dict], events: list[Event], since: str, until: str, top: int = 20) -> tuple[str, list[Event]]:
    s = settings()
    evs = [e for e in events if in_window(e, since, until)]
    profs = profiles(enriched, events, since, until)
    uni = new_unicorns(events, since, until, s["unicorn_usd"])
    win_mentions = [m for m in enriched if since <= m["date"] <= until]
    closed = [e for e in evs if e.event == "funding" and e.status == "closed"]
    lines = [
        f"# 融资与创业追踪报告：{since} ~ {until}", "",
        f"- 本期收录报道 **{len(win_mentions)}** 条，识别出交易事件 **{len(evs)}** 个"
        f"（融资 {sum(e.event == 'funding' for e in evs)} / IPO {sum(e.event == 'ipo' for e in evs)} / "
        f"并购 {sum(e.event == 'mna' for e in evs)} / 收入 {sum(e.event == 'arr' for e in evs)}）",
        f"- 已完成融资合计 **{usd(sum(e.amount_usd or 0 for e in closed))}**（{len(closed)} 起有金额或估值），"
        f"新晋独角兽 **{len(uni)}** 家",
        "- 数据来自新闻标题的自动抽取，金额按固定汇率折算美元；“谈判/传闻”表示尚未完成。请以原文为准。", "",
    ]
    for sec in (section_heat(profs, top), section_funding(evs, top), section_unicorns(uni), section_growth(profs, 10),
                section_exits(evs), section_arr(evs), section_sectors(evs), section_evolution(since)):
        lines += sec
    return "\n".join(lines), evs


def write(md: str, evs: list[Event], name: str) -> tuple[Path, Path]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    mdp = REPORTS / f"{name}.md"
    mdp.write_text(md + "\n", "utf-8")
    csvp = REPORTS / f"{name}.csv"
    with csvp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["company", "event", "status", "first", "last", "amount_usd", "valuation_usd", "arr_usd", "round",
                    "acquirer", "sectors", "region", "mentions", "sources", "title", "url"])
        for e in evs:
            w.writerow([e.company, e.event, e.status, e.first, e.last, e.amount_usd or "", e.valuation_usd or "",
                        e.arr_usd or "", e.round or "", e.acquirer or "", "/".join(e.sectors), e.region or "",
                        e.mentions, "; ".join(e.sources), e.titles[0] if e.titles else "", e.urls[0] if e.urls else ""])
    return mdp, csvp


def company_timeline(enriched: list[dict], events: list[Event], key: str) -> str:
    evs = sorted([e for e in events if e.key == key], key=lambda e: e.first)
    if not evs:
        return f"没有找到 `{key}` 的交易事件。"
    name = Counter(e.company for e in evs).most_common(1)[0][0]
    lines = [f"# {name}：事件时间线", "", "| 日期 | 事件 | 状态 | 金额 | 估值 | 年化收入 | 轮次 | 报道 | 代表标题 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for e in evs:
        lines.append(f"| {e.first} | {e.event} | {e.status} | {usd(e.amount_usd)} | {usd(e.valuation_usd)} | {usd(e.arr_usd)} | "
                     f"{e.round or '—'} | {e.mentions} | {_link(e)} |")
    return "\n".join(lines)
