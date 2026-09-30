"""Self-evolution: the tool improves its own knowledge after every run.

Five mechanisms, all logged to knowledge/CHANGELOG.jsonl and reversible via git:
 1. Query selection   — queries are scored by how many *new deals* they bring (EMA); weak ones retire,
                         strong trial queries get promoted.
 2. Query mutation     — new trial queries are spawned from (a) hot companies (watchlist) and
                         (b) rising terms in recent deal headlines.
 3. Rule learning      — verbs / descriptor words are mined from headlines the rules failed on and are
                         adopted only if the golden regression set does not get worse.
 4. Memory             — company→sector associations are learned so later headlines without sector
                         keywords are still classified.
 5. LLM fallback (opt) — unparsed headlines are labelled once by an LLM, cached for reuse, and queued as
                         golden-set candidates for human review.
"""
from __future__ import annotations

import json
import math
import re
import time
from collections import Counter, defaultdict
from datetime import date as Date, timedelta

from . import golden, llm, store
from .analytics import profiles
from .collect import qid
from .config import DATA, TESTS, load_json, log_change, save_json, settings
from .events import build_events, enrich
from .extract import (RE_RUMOR_EN, Rules, _sectors, clean_title, company_key_base, find_money,
                      looks_like_deal)

EN_STOP = set("""today check gmp subscription allotment status band live updates update key things know should buy apply
details date review opens closes day-one issue listing-day premium discount investors retail anchor watch
shares share list lists listing listed rate run debut debuts stock stocks ipo ipos gmp price
priced prices percent pct day days a an the and or of to in on at for with by from as is are was be been its it this that these those
into over after amid via new more than up about nearly its their his her our your says said report reports
raises raise raised raising round funding series seed valuation valued billion million trillion startup startups
company firm ai led backed investors investment talks deal deals worth value week weeks year years month months
first latest record top biggest big largest just now also could may will would than inc co ltd its how why what
who here meet exclusive sources source""".split())


# ---------------------------------------------------------------- 1. query lifecycle
def _lifecycle(evolved: list[dict], stats: dict, s: dict, dry: bool, rep: dict) -> None:
    for q in evolved:
        st = stats.get(qid(q))
        if not st or q.get("status") not in ("trial", "active"):
            continue
        ema, runs = st.get("ema") or 0.0, st.get("runs", 0)
        new_status = None
        if q["status"] == "trial":
            if runs >= s["promote_min_runs"] and ema >= s["promote_yield"]:
                new_status = "active"
            elif runs >= s["retire_min_runs"] and ema < s["promote_yield"]:
                new_status = "retired"
        elif q["status"] == "active" and runs >= s["retire_min_runs"] and ema < s["retire_below_yield"]:
            new_status = "retired"
        if new_status:
            rep["queries_" + ("promoted" if new_status == "active" else "retired")].append(q["q"])
            if not dry:
                q["status"] = new_status
                q["changed"] = time.strftime("%Y-%m-%d")
                log_change("query_" + new_status, {"query": q["q"], "lang": q["lang"], "ema": ema, "runs": runs})


def _add_query(evolved: list[dict], q: str, lang: str, origin: str, dry: bool, rep: dict, why: str) -> bool:
    key = f"{lang}:{q}"
    seeds = {f"{x['lang']}:{x['q']}" for x in (load_json("queries.json", []) or [])}
    if key in seeds or any(f"{x['lang']}:{x['q']}" == key for x in evolved):
        return False
    rep["queries_added"].append(f"{q} ({origin})")
    if not dry:
        evolved.append({"q": q, "lang": lang, "status": "trial", "origin": origin, "added": time.strftime("%Y-%m-%d")})
        log_change("query_added", {"query": q, "lang": lang, "origin": origin, "why": why})
    return True


# ---------------------------------------------------------------- 2a. watchlist queries
def _watchlist(evolved, enriched, events, s, dry, rep, budget: int) -> int:
    until = Date.today().isoformat()
    since = (Date.today() - timedelta(days=30)).isoformat()
    profs = profiles(enriched, events, since, until)
    watched = {x.get("company_key") for x in evolved if x.get("origin") == "watchlist" and x.get("status") != "retired"}
    n_watch = len([x for x in evolved if x.get("origin") == "watchlist" and x.get("status") in ("trial", "active")])
    added = 0
    for p in sorted(profs.values(), key=lambda p: p.score, reverse=True):
        if added >= budget or n_watch >= s["max_watch_queries"]:
            break
        if p.key in watched or not p.events:
            continue
        if not ((p.max_valuation or 0) >= s["unicorn_usd"] or p.growth or p.exits):
            continue
        name = p.company
        zh = bool(re.search(r"[\u4e00-\u9fff]", name))
        q = f"{name} 融资 OR 估值 OR 上市" if zh else f"\"{name}\" valuation OR raises OR IPO"
        why = f"score={p.score:.1f}, max_val={p.max_valuation}, growth={p.growth}"
        if _add_query(evolved, q, "zh" if zh else "en", "watchlist", dry, rep, why):
            if not dry:
                evolved[-1]["company_key"] = p.key
            added += 1
            n_watch += 1
    return added


# ---------------------------------------------------------------- 2b. rising-term queries
def _rising_terms(evolved, enriched, dry, rep, budget: int) -> int:
    today = Date.today()
    recent_since = (today - timedelta(days=14)).isoformat()
    prior_since = (today - timedelta(days=74)).isoformat()
    names = {w for m in enriched for f in ("company", "acquirer") if m["x"].get(f) for w in m["x"][f].lower().split()}
    verbs = Rules().subject_verbs | {"acquires", "acquire", "acquired", "acquisition", "buys", "buy", "led", "lead",
                                     "leads", "backs", "invests", "doubles", "triples", "hits", "tops"}
    rc, pc = Counter(), Counter()
    comps: dict[str, set] = defaultdict(set)
    for m in enriched:
        if m["lang"] != "en" or not m["x"].get("deal") or m["x"].get("event") != "funding":
            continue  # IPO headlines are dominated by listing-day boilerplate
        words = [w for w in re.findall(r"[a-z][a-z\-]+", clean_title(m["title"]).lower())]
        grams = {f"{a} {b}" for a, b in zip(words, words[1:])
                 if a not in EN_STOP and b not in EN_STOP and a not in names and b not in names
                 and a not in verbs and b not in verbs and len(a) > 2 and len(b) > 2}
        if m["date"] >= recent_since:
            rc.update(grams)
            for g in grams:
                comps[g].add(company_key_base(m["x"]["company"]))
        elif m["date"] >= prior_since:
            pc.update(grams)
    scored = []
    for g, r in rc.items():
        if r < 4 or len(comps[g]) < 3:
            continue
        ratio = (r + 1) / (pc[g] * 14 / 60 + 1)
        if ratio >= 3:
            scored.append((ratio * math.log(r + 1), g, r))
    added = 0
    for _, g, r in sorted(scored, reverse=True):
        if added >= budget:
            break
        if _add_query(evolved, f"\"{g}\" startup raises", "en", "rising_term", dry, rep, f"recent={r}, prior={pc[g]}"):
            added += 1
    return added


# ---------------------------------------------------------------- 3. rule learning (gated)
def _unparsed(enriched: list[dict]) -> list[dict]:
    return [m for m in enriched if not m["x"].get("deal") and looks_like_deal(m["title"])]


def _gate(candidate_patterns: dict, unparsed: list[dict]) -> tuple[bool, float, float, int]:
    base_rules = Rules()
    new_rules = Rules(candidate_patterns)
    base_acc = golden.evaluate(base_rules)["accuracy"]
    new_acc = golden.evaluate(new_rules)["accuracy"]
    from .extract import extract
    gain = sum(1 for m in unparsed if extract(m["title"], new_rules).deal)
    return (new_acc >= base_acc and gain >= 2), base_acc, new_acc, gain


def _learn_verbs(unparsed: list[dict], s: dict, dry: bool, rep: dict) -> None:
    rules = Rules()
    skip = {"over", "nearly", "more", "than", "about", "up", "to", "an", "additional", "a", "another", "fresh", "new",
            "record", "around", "almost", "roughly", "at", "for", "of", "in", "with", "and", "the", "its", "by", "from"}
    cnt: Counter = Counter()
    for m in unparsed:
        if m["lang"] != "en":
            continue
        t = clean_title(m["title"])
        money = find_money(t)
        if not money:
            continue
        before = re.findall(r"\S+", t[: money[0].start])
        while before and before[-1].lower().strip(",") in skip:
            before.pop()
        if len(before) < 2:
            continue
        v = before[-1].lower().strip(",:;")
        if re.fullmatch(r"[a-z]{3,}", v) and v not in rules.subject_verbs and v not in EN_STOP and before[-2][:1].isupper():
            cnt[v] += 1
    patterns = load_json("patterns.json", {}) or {}
    for v, n in cnt.most_common(10):
        if n < s["verb_min_support"]:
            break
        cand = json.loads(json.dumps(patterns))
        cand.setdefault("extra_subject_verbs", []).append(v)
        ok, b, a, gain = _gate(cand, unparsed)
        rec = {"verb": v, "support": n, "golden_before": round(b, 4), "golden_after": round(a, 4), "gain": gain}
        if ok:
            rep["verbs_learned"].append(rec)
            if not dry:
                patterns = cand
                save_json("patterns.json", patterns)
                log_change("verb_learned", rec)
        else:
            rep["rejected"].append({"type": "verb", **rec})


def _learn_descriptors(enriched: list[dict], unparsed: list[dict], s: dict, dry: bool, rep: dict) -> None:
    """Words that start the extracted name of many *different* companies are labels, not names."""
    rules = Rules()
    first_tok: dict[str, set] = defaultdict(set)
    lower_use: Counter = Counter()
    for m in enriched:
        if m["lang"] == "en":
            lower_use.update(set(re.findall(r"(?<![A-Za-z])([a-z][a-z\-]{2,})(?![A-Za-z])", m["title"])))
        c = m["x"].get("company")
        if c and m["lang"] == "en" and len(c.split()) >= 2:
            first_tok[c.split()[0].lower()].add(c.split()[1].lower())  # distinct *following* names
    patterns = load_json("patterns.json", {}) or {}
    for w, comps in sorted(first_tok.items(), key=lambda kv: -len(kv[1])):
        if len(comps) < s["descriptor_min_support"]:
            break
        if w in rules.descriptors or not re.fullmatch(r"[a-z\-]{3,}", w) or lower_use[w] < 3:
            continue
        cand = json.loads(json.dumps(patterns))
        cand.setdefault("extra_descriptors", []).append(w)
        base = golden.evaluate(Rules())["accuracy"]
        after = golden.evaluate(Rules(cand))["accuracy"]
        rec = {"descriptor": w, "companies": sorted(comps)[:8], "golden_before": round(base, 4), "golden_after": round(after, 4)}
        if after >= base:
            rep["descriptors_learned"].append(rec)
            if not dry:
                patterns = cand
                save_json("patterns.json", patterns)
                log_change("descriptor_learned", rec)
        else:
            rep["rejected"].append({"type": "descriptor", **rec})


# ---------------------------------------------------------------- 4. sector memory
def _learn_sectors(enriched: list[dict], dry: bool, rep: dict) -> None:
    rules = Rules()
    rules.company_sectors = {}  # count only direct keyword evidence
    votes: dict[str, Counter] = defaultdict(Counter)
    for m in enriched:
        c = m["x"].get("company")
        if not c or not m["x"].get("event"):
            continue
        for sec in _sectors(clean_title(m["title"]), None, rules)[:2]:
            votes[company_key_base(c)][sec] += 1
    mem = load_json("company_sectors.json", {}) or {}
    changed = 0
    for k, cnt in votes.items():
        total = sum(cnt.values())
        top = [sec for sec, n in cnt.most_common(2) if n >= 2 and n / total >= 0.3]
        if top and mem.get(k) != top:
            mem[k] = top
            changed += 1
    rep["sectors_learned"] = changed
    if changed and not dry:
        save_json("company_sectors.json", dict(sorted(mem.items())))
        log_change("sector_memory", {"companies_updated": changed})


# ---------------------------------------------------------------- 4a. company memory
def _learn_known(enriched: list[dict], dry: bool, rep: dict) -> None:
    """Remember companies confirmed by >=2 independent deal headlines; used as a fallback when a new
    headline's grammar defeats the rules ("DeepSeek年化营收突破10亿美元，计划…融资")."""
    rules = Rules()
    cnt: dict[str, Counter] = defaultdict(Counter)
    srcs: dict[str, set] = defaultdict(set)
    for m in enriched:
        x = m["x"]
        if x.get("deal") and x.get("company"):
            k = company_key_base(x["company"])
            cnt[k][x["company"]] += 1
            srcs[k].add(m.get("source") or m["id"])
    known = set(load_json("known_companies.json", []) or [])
    add = []
    for k, c in cnt.items():
        name = c.most_common(1)[0][0]
        if len(srcs[k]) >= 2 and name not in known and k not in rules.blocked and len(name) >= 3:
            add.append(name)
    if not add:
        return
    base = golden.evaluate(Rules())["accuracy"]
    save_json("known_companies.json", sorted(known | set(add)))
    after = golden.evaluate(Rules())["accuracy"]
    rec = {"added": len(add), "sample": sorted(add)[:10], "golden_before": round(base, 4), "golden_after": round(after, 4)}
    if after >= base and not dry:
        rep["known_learned"] = len(add)
        log_change("company_memory", rec)
    else:
        save_json("known_companies.json", sorted(known))
        (rep.setdefault("rejected", [])).append({"type": "company_memory", **rec}) if after < base else None
        rep["known_learned"] = len(add) if dry else 0


# ---------------------------------------------------------------- 4b. alias learning
def _learn_aliases(enriched: list[dict], events, dry: bool, rep: dict) -> None:
    """'Colossal Biosciences' / 'Colossal', 'Prediction Market Kalshi' / 'Kalshi': if a longer name contains a
    shorter known name and both report the same deal terms within 30 days, merge them under the shorter name."""
    names: dict[str, Counter] = defaultdict(Counter)
    lower_use: Counter = Counter()
    for m in enriched:
        lower_use.update(set(re.findall(r"(?<![A-Za-z])([a-z][a-z\-]{2,})(?![A-Za-z])", m["title"])))
        c = m["x"].get("company")
        if c and m["x"].get("deal"):
            names[company_key_base(c)][c] += 1
    rules = Rules()
    by_key = defaultdict(list)
    for e in events:
        by_key[e.key].append(e)

    def same_deal(ea, eb) -> bool:
        if abs((Date.fromisoformat(ea.first) - Date.fromisoformat(eb.first)).days) > 30:
            return False
        v = ea.valuation_usd and eb.valuation_usd and abs(ea.valuation_usd - eb.valuation_usd) <= 0.1 * max(ea.valuation_usd, eb.valuation_usd)
        a = ea.amount_usd and eb.amount_usd and abs(ea.amount_usd - eb.amount_usd) <= 0.05 * max(ea.amount_usd, eb.amount_usd)
        return bool(v or a)

    aliases = load_json("aliases.json", {}) or {}
    alias_keys = {company_key_base(k) for k in aliases}
    proposals = []
    for kb in names:
        bt = kb.split()
        if len(bt) < 2 or kb in alias_keys:
            continue
        for n in range(1, len(bt)):
            prefix, suffix = " ".join(bt[:n]), " ".join(bt[-n:])
            # suffix match only when the dropped words are labels ("Prediction Market Kalshi")
            cands = [prefix] + ([suffix] if all(w in rules.descriptors for w in bt[:-n]) else [])
            for ka in cands:
                if len(ka.split()) == 1 and lower_use[ka] >= 2:
                    continue  # never collapse onto a common word ("network", "world")
                if ka in names and ka != kb and any(same_deal(x, y) for x in by_key[ka] for y in by_key[kb]):
                    proposals.append((kb, names[ka].most_common(1)[0][0], names[kb].most_common(1)[0][0]))
                    break
            else:
                continue
            break
    for kb, canon, longer in proposals:
        cand = dict(aliases)
        cand[kb] = canon
        base = golden.evaluate(Rules())["accuracy"]
        save_json("aliases.json", cand)  # Rules() reads aliases from disk
        after = golden.evaluate(Rules())["accuracy"]
        rec = {"alias": longer, "canonical": canon, "golden_before": round(base, 4), "golden_after": round(after, 4)}
        if after >= base and not dry:
            aliases = cand
            rep["aliases_learned"].append(rec)
            log_change("alias_learned", rec)
        else:
            save_json("aliases.json", aliases)
            (rep["aliases_learned"] if dry and after >= base else rep["rejected"]).append(rec)


# ---------------------------------------------------------------- 5. LLM fallback
def _llm(unparsed: list[dict], dry: bool, rep: dict, limit: int = 40) -> None:
    if not llm.available():
        rep["llm"] = "skipped (set FT_LLM_API_KEY to enable)"
        return
    cache = store.load_llm_cache()
    todo = [m for m in unparsed if m["id"] not in cache][:limit]
    rows, cands = [], []
    for i in range(0, len(todo), 20):
        batch = todo[i:i + 20]
        try:
            res = llm.extract_batch([m["title"] for m in batch])
        except Exception as e:
            rep["llm"] = f"error: {e}"
            break
        for m, x in zip(batch, res):
            if x is None:
                continue
            rows.append({"id": m["id"], "title": m["title"], "extraction": x, "ts": time.strftime("%Y-%m-%d")})
            if x.get("event") and x.get("company"):
                cands.append({"title": m["title"], "expect": {k: v for k, v in x.items() if v is not None}, "origin": "llm"})
    rep["llm_labeled"] = len(rows)
    if rows and not dry:
        store.save_llm_results(rows)
        with (TESTS / "golden_candidates.jsonl").open("a", encoding="utf-8") as f:
            for c in cands:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        log_change("llm_labeled", {"count": len(rows), "golden_candidates": len(cands)})


# ---------------------------------------------------------------- entry
def evolve(dry_run: bool = False, use_llm: bool = False) -> dict:
    s = settings()
    rep: dict = {"queries_added": [], "queries_retired": [], "queries_promoted": [], "verbs_learned": [],
                 "descriptors_learned": [], "aliases_learned": [], "sectors_learned": 0, "llm_labeled": 0, "rejected": []}
    enriched = enrich(store.load_all())
    events = build_events(enriched)
    evolved = load_json("queries_evolved.json", []) or []
    stats = load_json("query_stats.json", {}) or {}

    _lifecycle(evolved, stats, s, dry_run, rep)
    budget = s["max_new_queries_per_evolve"]
    budget -= _watchlist(evolved, enriched, events, s, dry_run, rep, min(4, budget))
    _rising_terms(evolved, enriched, dry_run, rep, max(0, min(2, budget)))
    if not dry_run:
        save_json("queries_evolved.json", evolved)

    unparsed = _unparsed(enriched)
    rep["unparsed"] = len(unparsed)
    _learn_verbs(unparsed, s, dry_run, rep)
    _learn_descriptors(enriched, unparsed, s, dry_run, rep)
    _learn_sectors(enriched, dry_run, rep)
    _learn_aliases(enriched, events, dry_run, rep)
    _learn_known(enriched, dry_run, rep)
    if use_llm:
        _llm(unparsed, dry_run, rep)

    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / "unparsed_latest.jsonl").open("w", encoding="utf-8") as f:
        for m in sorted(unparsed, key=lambda m: m["date"], reverse=True)[:200]:
            f.write(json.dumps({"date": m["date"], "title": m["title"], "x": m["x"]}, ensure_ascii=False) + "\n")
    rep["golden_accuracy"] = round(golden.evaluate()["accuracy"], 4)
    return rep
