#!/usr/bin/env python3
"""funding-tracker CLI.

  python3 ft.py run [--days 7]              collect → evolve → report (the weekly job)
  python3 ft.py collect [--days 7]          fetch news for all active queries + RSS
  python3 ft.py report [--days 7 | --since D --until D] [--top 20] [--name NAME]
  python3 ft.py top [--days 30] [--n 30]    composite heat ranking in the terminal
  python3 ft.py company NAME                timeline of one company
  python3 ft.py evolve [--dry-run] [--llm]  self-improvement step
  python3 ft.py test [--min 0.9]            golden regression (exit 1 if below --min)
  python3 ft.py golden review|accept        review / promote LLM-labelled golden candidates
  python3 ft.py stats                       query fitness table
  python3 ft.py import-txt FILE...          import 'YYYY-MM-DD | headline' snapshots
  python3 ft.py extract "headline"          debug a single headline
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracker import golden, store  # noqa: E402
from tracker.analytics import profiles, window  # noqa: E402
from tracker.collect import active_queries, collect, qid  # noqa: E402
from tracker.config import TESTS, load_json  # noqa: E402
from tracker.events import build_events, enrich  # noqa: E402
from tracker.evolve import evolve  # noqa: E402
from tracker.extract import company_key_base, extract  # noqa: E402
from tracker.report import build, company_timeline, usd, write  # noqa: E402


def _load():
    enriched = enrich(store.load_all())
    return enriched, build_events(enriched)


def cmd_collect(a):
    r = collect(days=a.days, max_queries=a.max_queries, include_rss=not a.no_rss)
    print(json.dumps(r, ensure_ascii=False))


def cmd_report(a):
    since, until = window(a.days, a.since, a.until)
    enriched, events = _load()
    md, evs = build(enriched, events, since, until, a.top)
    name = a.name or f"{until}_{'weekly' if (a.days or 7) == 7 and not a.since else 'report'}"
    mdp, csvp = write(md, evs, name)
    print(f"report: {mdp}\ncsv:    {csvp}\nevents in window: {len(evs)}")


def cmd_top(a):
    since, until = window(a.days, a.since, a.until)
    enriched, events = _load()
    profs = sorted([p for p in profiles(enriched, events, since, until).values() if p.events],
                   key=lambda p: p.score, reverse=True)[: a.n]
    print(f"{since} ~ {until}")
    for i, p in enumerate(profs, 1):
        g = f"{p.growth:.1f}x" if p.growth else "-"
        print(f"{i:3}. {p.company[:28]:28} score={p.score:5.1f} mentions={p.mentions:3} maxval={usd(p.max_valuation):>8} "
              f"growth={g:>5} exits={','.join(p.exits) or '-'} {'/'.join(p.sectors)}")


def cmd_company(a):
    enriched, events = _load()
    print(company_timeline(enriched, events, company_key_base(a.name)))


def cmd_evolve(a):
    print(json.dumps(evolve(dry_run=a.dry_run, use_llm=a.llm), ensure_ascii=False, indent=2))


def cmd_test(a):
    r = golden.evaluate()
    print(f"golden accuracy: {r['accuracy']:.3f} ({r['checks']} checks / {r['cases']} cases)")
    print("per field:", {k: (round(v, 3) if v is not None else None) for k, v in r["per_field"].items()})
    for f in r["failures"][: a.show]:
        print("  ✗", f["title"][:100], json.dumps(f["diff"], ensure_ascii=False))
    sys.exit(0 if r["accuracy"] >= a.min else 1)


def cmd_golden(a):
    cand_p = TESTS / "golden_candidates.jsonl"
    cands = [json.loads(l) for l in cand_p.read_text("utf-8").splitlines() if l.strip()] if cand_p.exists() else []
    if a.action == "review":
        for i, c in enumerate(cands):
            print(i, c["title"][:100], json.dumps(c["expect"], ensure_ascii=False))
        print(f"{len(cands)} candidates")
        return
    idx = set(range(len(cands))) if a.ids in (None, "all") else {int(x) for x in a.ids.split(",")}
    keep, take = [], []
    for i, c in enumerate(cands):
        (take if i in idx else keep).append(c)
    with (TESTS / "golden.jsonl").open("a", encoding="utf-8") as f:
        for c in take:
            f.write(json.dumps({"title": c["title"], "expect": c["expect"]}, ensure_ascii=False) + "\n")
    cand_p.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in keep), "utf-8")
    print(f"accepted {len(take)}, remaining {len(keep)}")


def cmd_stats(a):
    stats = load_json("query_stats.json", {}) or {}
    act = {qid(q): q for q in active_queries()}
    evolved = {f"{q['lang']}:{q['q']}": q for q in (load_json("queries_evolved.json", []) or [])}
    rows = []
    for k, st in stats.items():
        q = act.get(k) or evolved.get(k) or {}
        rows.append((st.get("ema") or 0, k, st, q.get("status", "rss" if k.startswith("rss:") else "retired"), q.get("origin", "")))
    for ema, k, st, status, origin in sorted(rows, reverse=True):
        print(f"{ema:6.2f}  runs={st['runs']:2}  deals={st['deal_new']:4}  {status:8} {origin:11} {k[:70]}")


def cmd_import(a):
    for f in a.files:
        print(f, len(store.import_txt(Path(f))))


def cmd_extract(a):
    print(json.dumps(extract(a.title).as_dict(), ensure_ascii=False, indent=2))


def cmd_run(a):
    print("== collect", file=sys.stderr)
    print(json.dumps(collect(days=a.days, include_rss=not a.no_rss), ensure_ascii=False))
    print("== evolve", file=sys.stderr)
    rep = evolve(use_llm=a.llm)
    print(json.dumps({k: v for k, v in rep.items() if k != "rejected"}, ensure_ascii=False))
    print("== report", file=sys.stderr)
    a.since = a.until = a.name = None
    a.top = 20
    cmd_report(a)


def main():
    p = argparse.ArgumentParser(description="Self-evolving startup funding tracker")
    sub = p.add_subparsers(dest="cmd", required=True)

    def win(sp, days=7):
        sp.add_argument("--days", type=int, default=days)
        sp.add_argument("--since")
        sp.add_argument("--until")

    sp = sub.add_parser("collect"); sp.add_argument("--days", type=int); sp.add_argument("--max-queries", type=int)
    sp.add_argument("--no-rss", action="store_true"); sp.set_defaults(f=cmd_collect)
    sp = sub.add_parser("report"); win(sp); sp.add_argument("--top", type=int, default=20); sp.add_argument("--name")
    sp.set_defaults(f=cmd_report)
    sp = sub.add_parser("top"); win(sp, 30); sp.add_argument("--n", type=int, default=30); sp.set_defaults(f=cmd_top)
    sp = sub.add_parser("company"); sp.add_argument("name"); sp.set_defaults(f=cmd_company)
    sp = sub.add_parser("evolve"); sp.add_argument("--dry-run", action="store_true"); sp.add_argument("--llm", action="store_true")
    sp.set_defaults(f=cmd_evolve)
    sp = sub.add_parser("test"); sp.add_argument("--min", type=float, default=0.9); sp.add_argument("--show", type=int, default=30)
    sp.set_defaults(f=cmd_test)
    sp = sub.add_parser("golden"); sp.add_argument("action", choices=["review", "accept"]); sp.add_argument("ids", nargs="?")
    sp.set_defaults(f=cmd_golden)
    sp = sub.add_parser("stats"); sp.set_defaults(f=cmd_stats)
    sp = sub.add_parser("import-txt"); sp.add_argument("files", nargs="+"); sp.set_defaults(f=cmd_import)
    sp = sub.add_parser("extract"); sp.add_argument("title"); sp.set_defaults(f=cmd_extract)
    sp = sub.add_parser("run"); sp.add_argument("--days", type=int, default=7); sp.add_argument("--no-rss", action="store_true")
    sp.add_argument("--llm", action="store_true"); sp.set_defaults(f=cmd_run)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
