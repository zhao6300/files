"""Rule-based extraction of deal facts from news headlines (English + Chinese).

Every word list here is a *baseline*; knowledge/patterns.json can extend it. The evolve step
adds entries there (e.g. new funding verbs, new descriptor words) only after they pass the
golden regression test, so extraction quality can grow without code changes.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .config import load_json

# ---------------------------------------------------------------- money
FX = {"USD": 1.0, "EUR": 1.1, "GBP": 1.3, "CNY": 0.14, "CAD": 0.73, "AUD": 0.66, "JPY": 0.0067,
      "INR": 0.012, "KRW": 0.00073, "HKD": 0.128, "SGD": 0.78, "CHF": 1.15, "SEK": 0.1}
UNIT_EN = {"trillion": 1e12, "tn": 1e12, "t": 1e12, "billion": 1e9, "bn": 1e9, "b": 1e9,
           "million": 1e6, "mn": 1e6, "mln": 1e6, "m": 1e6, "thousand": 1e3, "k": 1e3,
           "crore": 1e7, "cr": 1e7, "lakh": 1e5}
CUR_SYM = {"us$": "USD", "usd": "USD", "$": "USD", "c$": "CAD", "ca$": "CAD", "a$": "AUD", "au$": "AUD",
           "hk$": "HKD", "s$": "SGD", "€": "EUR", "eur": "EUR", "£": "GBP", "gbp": "GBP", "¥": "JPY",
           "₹": "INR", "rs": "INR", "rs.": "INR", "inr": "INR", "cny": "CNY", "rmb": "CNY"}
CUR_WORD = {"yuan": "CNY", "renminbi": "CNY", "rmb": "CNY", "euro": "EUR", "euros": "EUR",
            "dollars": "USD", "rupees": "INR", "won": "KRW", "yen": "JPY", "pounds": "GBP"}
UNIT_ZH = {"万亿": 1e12, "千亿": 1e11, "百亿": 1e10, "亿": 1e8, "千万": 1e7, "百万": 1e6, "万": 1e4}
CUR_ZH = {"美元": "USD", "美金": "USD", "元人民币": "CNY", "人民币": "CNY", "元": "CNY", "欧元": "EUR",
          "英镑": "GBP", "港元": "HKD", "港币": "HKD", "日元": "JPY"}

_NUM = r"(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
MONEY_PREFIX = re.compile(
    r"(?P<cur>(?i:US\$|USD|CA\$|C\$|AU\$|A\$|HK\$|S\$|EUR|GBP|CNY|RMB|INR|Rs\.?)|\$|€|£|¥|₹)\s?" + _NUM +
    r"[\s-]?(?P<unit>(?i:trillion|billion|million|thousand|crore|lakh|mln|bn|mn|tn|cr)|[TBMKkm])(?![A-Za-z])")
MONEY_SUFFIX = re.compile(
    _NUM + r"\s?(?P<unit>(?i:trillion|billion|million|bn|mn))\s+(?P<curw>(?i:yuan|renminbi|rmb|euros?|dollars|rupees|won|yen|pounds))\b")
MONEY_ZH = re.compile(
    r"(?:(?P<num>\d+(?:\.\d+)?)\s*)?(?P<unit>万亿|千亿|百亿|亿|千万|百万|万)?\s*(?P<cur>美元|美金|元人民币|人民币|欧元|英镑|港元|港币|日元|元)?")

VAL_AFTER = re.compile(r"^\s*(?:(?i:post-money|pre-money)\s+)?(?:(?i:valuation|value\b|valued)|(?:的|投后|投前)?(?:估值|市值))")
VAL_BEFORE_ZH = re.compile(r"(?:估值|市值)(?:(?!融资|筹资|募资|完成|获|的)[\u4e00-\u9fff]){0,6}?(?:达|至|为|超过|超|破|突破|升至|到|达到)?\s*(?:约|近|超|逾)?\s*$")
VAL_BEFORE = re.compile(
    r"(?i:valuation|valued|value|valuing|worth|market\s+cap(?:italization)?|market\s+value|估值|市值)"
    r"\s*(?i:of|at|to|hits|reaches|reaching|soars\s+to|surges\s+to|jumps\s+to|climbs\s+to|rises\s+to|tops|surpasses|"
    r"exceeds|exceeding|surpassing|topping|nearing|near|of\s+more\s+than|of\s+over|exceeds|nears|could\s+hit|hitting|at\s+up\s+to|of\s+up\s+to|up\s+to|above|over|达|至|超过|超|为|约|破|突破|升至|"
    r"飙升至|或达|近|翻倍至|倍增至|涨至|料倍增至|料达)?\s*(?i:about|around|nearly|roughly|over|more\s+than|at\s+least|"
    r"a|an|~|up\s+to)?\s*$")
VAL_BEFORE_LOOSE = re.compile(
    r"(?i:valuation|valued|market\s+cap|估值|市值)(?:\s+[A-Za-z\-]+){1,3}?\s+(?i:to|at|of|hits?|reaches|tops|surpasses|past)"
    r"\s*(?i:about|around|nearly|roughly|over|more\s+than|at\s+least|a|an|~|up\s+to)?\s*$")
VAL_AT = re.compile(r"(?i)\b(?:raise|raises|raised|raising|round|funds|funding|financing|investment|invest)\b[^$€£¥₹\d]{0,25}"
                    r"\bat\s+(?:a\s+|an\s+)?(?:over|about|around|nearly|up\s+to|more\s+than|roughly|least|at\s+least)?\s*$")
ARR_AFTER = re.compile(
    r"^\s*(?i:in\s+)?(?i:ARR|annual(?:ized)?\s+(?:recurring\s+)?revenue|(?:gross\s+)?(?:revenue\s+)?run[- ]rate|"
    r"(?:annual\s+|annualized\s+)?revenue|年化收入|年化营收|营收|收入)")
ARR_BEFORE_ZH = re.compile(r"(?:年化收入|年化营收|营收|收入|ARR)[\u4e00-\u9fff]{0,4}?(?:达|突破|超过|超|达到|至)?\s*(?:约|近|超|逾)?\s*$")
ARR_BEFORE = re.compile(
    r"(?i:ARR|revenue|run[- ]rate|sales|年化收入|年化营收|营收|收入)\s*(?i:of|hits|hit|reaches|reaching|reached|"
    r"crosses|crossed|tops|surpasses|exceeds|nears|to|达|突破|超过|超|达到)?\s*(?i:about|nearly|over|more\s+than|"
    r"a|an|roughly)?\s*$")


NOT_DEAL_AFTER = re.compile(r"^\s*(?:(?i:net|operating|annual)\s+)?(?i:loss|losses|deficit|in losses|wiped|lost|write-?down|"
                            r"fine|penalty|lawsuit|settlement)|^\s*(?:的)?(?:亏损|净亏损|损失|罚款)")


@dataclass
class Money:
    usd: float
    start: int
    end: int
    role: str = "amount"  # amount | valuation | arr


def _num(s: str) -> float:
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", s):
        return float(s.replace(",", ""))
    return float(s.replace(",", "."))


def find_money(text: str) -> list[Money]:
    if re.search(r"[\u4e00-\u9fff]", text):
        text = re.sub(r"(\d+)万(\d{1,4})亿", lambda mm: f"{int(mm.group(1)) + int(mm.group(2)) / 10000:g}万亿", text)
    found: list[Money] = []
    for m in MONEY_PREFIX.finditer(text):
        cur = CUR_SYM.get(m.group("cur").lower().strip(), "USD")
        unit = m.group("unit")
        mult = UNIT_EN.get(unit.lower() if len(unit) > 1 else unit.lower())
        if mult is None:
            continue
        found.append(Money(_num(m.group("num")) * mult * FX[cur], m.start(), m.end()))
    for m in MONEY_SUFFIX.finditer(text):
        cur = CUR_WORD.get(m.group("curw").lower(), "USD")
        found.append(Money(_num(m.group("num")) * UNIT_EN[m.group("unit").lower()] * FX[cur], m.start(), m.end()))
    if re.search(r"[\u4e00-\u9fff]", text):
        # "1万4000亿" -> "1.4万亿" (same length is not required: positions are only used locally)
        text = re.sub(r"(\d+)万(\d{1,4})亿", lambda mm: f"{int(mm.group(1)) + int(mm.group(2)) / 10000:g}万亿", text)
        for m in MONEY_ZH.finditer(text):
            num, unit, cur = m.group("num"), m.group("unit"), m.group("cur")
            if not (num or unit):
                continue
            if num is None and unit not in ("千亿", "百亿", "万亿"):
                continue
            if cur is None:
                # bare "估值100亿" is common in Chinese headlines: only accept after 估值/市值
                if not (unit and re.search(r"(?:估值|市值)[^\d]{0,4}$", text[: m.start()])):
                    continue
                cur = "元"
            if unit is None and num is not None and cur is not None and float(num) < 1e5:
                continue
            v = float(num or 1) * UNIT_ZH.get(unit or "", 1) * FX[CUR_ZH[cur]]
            found.append(Money(v, m.start(), m.end()))
    # drop overlaps (keep the earliest/longest), sort by position
    found.sort(key=lambda x: (x.start, -(x.end - x.start)))
    out: list[Money] = []
    for f in found:
        if out and f.start < out[-1].end:
            continue
        if f.usd < 1e5:
            continue
        out.append(f)
    out = [f for f in out if not NOT_DEAL_AFTER.search(text[f.end: f.end + 25])]
    for f in out:
        before, after = text[max(0, f.start - 45): f.start], text[f.end: f.end + 40]
        if (VAL_AFTER.search(after) or VAL_BEFORE.search(before) or VAL_BEFORE_LOOSE.search(before) or VAL_AT.search(before)
                or VAL_BEFORE_ZH.search(before)):
            f.role = "valuation"
        elif ARR_AFTER.search(after) or ARR_BEFORE.search(before) or ARR_BEFORE_ZH.search(before):
            f.role = "arr"
    return out


# ---------------------------------------------------------------- event/status/round
RE_MNA_EN = re.compile(r"(?i)\b(acqui\w*|to buy|buys|bought|buying|agrees? to buy|merger|merge|takeover|snaps up|sold to)\b")
RE_IPO_EN = re.compile(r"(?i)(?<![A-Za-z])I\.P\.O\.|\b(IPO|goes public|go public|going public|public debut|trading debut|market debut|"
                       r"stock market debut|debuts?|listing|lists on|files (?:confidentially )?(?:for|to go)|prospectus|"
                       r"nasdaq|nyse)\b")
RE_PREIPO_EN = re.compile(r"(?i)\b(pre-ipo|ahead of (?:its |an |a )?(?:planned )?ipo|before (?:its |an )?ipo)\b")
RE_FUND_EN = re.compile(r"(?i)\b(rais\w*|funding|financing|round|series [a-k]\b|seed|secures|secured|lands|closes|bags|nabs|"
                        r"valuation|valued|investment|invests?|backs|backed by|unicorn)\b")
RE_ARR_EN = re.compile(r"(?i)\b(ARR|annual(?:ized)? (?:recurring )?revenue|run[- ]rate|revenue)\b")
RE_MNA_ZH = re.compile(r"(收购|并购|被.{0,12}收购|合并)")
RE_IPO_ZH = re.compile(r"(上市|IPO|递表|招股|挂牌|登陆(?:港交所|港股|科创板|纳斯达克|纽交所|创业板|北交所|A股)|首日|破发)")
RE_PREIPO_ZH = re.compile(r"(Pre-IPO|pre-IPO|上市前融资)")
RE_FUND_ZH = re.compile(r"(融资|轮|估值|领投|注资|增资|获投|投资)")
RE_ARR_ZH = re.compile(r"(年化收入|年化营收|ARR|营收)")

RE_RUMOR_EN = re.compile(
    r"(?i)\b(in talks|talks|seeks?|seeking|eyes|eyeing|targets?|targeting|nears?|nearing|weighs?|weighing|considers?|"
    r"considering|reportedly|reports?|reported|sources|source:|could|may|might|plans?|planning|looking to|aims?|"
    r"in discussions|poised|set to|preparing|explores?|exploring|chasing|expected to|would|rumou?red|mulls?)\b")
RE_RUMOR_ZH = re.compile(r"(洽谈|拟|传|据悉|消息称|或将|计划|筹备|寻求|有望|据报|料|接近|即将|正以|谈判|或达|或)")

RE_ROUND_EN = re.compile(r"(?i)\b(pre-seed|seed|series\s+[a-k](?:-\d)?\+?(?:\s+extension)?|pre-ipo|growth round|strategic round)\b")
RE_ROUND_ZH = re.compile(r"(天使\+?轮|种子轮|Pre-?[A-G]\+?轮|[A-G]\+{0,2}轮|[A-G]-\d轮|战略融资|战略投资|Pre-IPO轮?|首轮)")

# ---------------------------------------------------------------- company extraction (EN)
SUBJECT_VERBS = {
    "raises", "raised", "raise", "raising", "secures", "secured", "lands", "landed", "closes", "closed", "bags", "nabs",
    "gets", "receives", "attracts", "hits", "hit", "reaches", "nears", "tops", "crosses", "surpasses", "doubles",
    "triples", "quadruples", "soars", "surges", "jumps", "climbs", "valued", "seeks", "eyes", "targets", "weighs",
    "files", "prices", "debuts", "pops", "lists", "delays", "postpones", "announces", "says", "becomes", "sets",
    "snags", "scores", "pulls", "hauls", "rakes", "wins", "draws", "expands", "extends", "confirms", "unveils", "joins",
    "plans", "passes", "overtakes", "leapfrogs", "vaults", "rockets", "notches", "banks", "boosts",
    "soar", "surge", "jump", "climb", "pop", "rally", "rallies", "plunge", "plunges", "tumble", "tumbles", "slides",
    "slips", "falls", "drops", "debut", "goes", "prepares", "picks", "taps", "hires",
    "closing", "nearing", "raising", "seeking", "eyeing", "targeting", "weighing", "securing", "landing",
}
# verbs that only anchor if followed by money/valuation words (avoid 'X unveils product')
WEAK_VERBS = {"announces", "says", "confirms", "unveils", "joins", "plans", "expands", "extends", "sets", "boosts"}
AUX = {"is", "has", "was", "are", "will", "could", "may", "set", "now", "in", "to"}
AUX_NEXT = {"raising", "in", "reportedly", "valued", "seeking", "eyeing", "said", "closing", "nearing", "poised",
            "planning", "preparing", "looking", "targeting", "weighing", "considering", "gearing", "talks",
            "discussions", "final", "raise", "set", "about", "said", "go", "file", "list"}
MODALS = {"could", "would", "should", "might", "may", "will", "can", "must", "set", "aim", "aims", "looks", "looking",
          "poised", "ready", "plans", "planning", "is", "was", "has", "now", "to", "said"}
LEAD_NOISE = {"watch", "video", "podcast", "breaking", "exclusive", "report", "opinion", "analysis", "update", "scoop",
              "listen", "live"}
ADVERBS = {"reportedly", "now", "officially", "quietly", "just", "also", "finally", "nearly", "again", "newly",
           "formally", "successfully", "reported", "already", "then", "still", "almost"}
MNA_PHRASES = [
    "agrees to acquire", "agrees to buy", "in talks to acquire", "in talks to buy", "completes acquisition of",
    "completes its acquisition of", "closes acquisition of", "announces acquisition of", "plans to acquire",
    "set to acquire", "is acquiring", "is buying", "to acquire", "to buy", "acquires", "acquired", "acquiring",
    "buys", "bought", "snaps up", "scoops up", "nears deal to buy", "nears deal to acquire", "officially closes its",
]
PASSIVE_MNA = ["to be acquired by", "is being acquired by", "acquired by", "sold to", "bought by"]
INVEST_PHRASES = ["in talks to lead", "to invest in", "invests in", "invest in", "investment in", "stake in", "bets on", "to back",
                  "backs", "back", "leads round in", "leads funding in"]
DESCRIPTORS = {
    "ai", "a.i.", "start-up", "startup", "startups", "chip", "chipmaker", "firm", "company", "co", "maker", "developer",
    "provider", "platform", "unicorn", "lab", "giant", "rival", "challenger", "upstart", "specialist", "player",
    "pioneer", "operator", "creator", "leader", "outfit", "business", "israeli", "french", "german", "british",
    "uk", "us", "u.s.", "chinese", "indian", "japanese", "korean", "european", "american", "swedish", "australian",
    "canadian", "cyber", "cybersecurity", "security", "software", "fintech", "robotics", "robot", "humanoid",
    "defense", "defence", "drone", "data", "cloud", "legal", "health", "healthcare", "the", "its", "coding", "agent",
    "agentic", "model", "gateway", "infrastructure", "identity", "observability", "computing", "physical",
    "generative", "genai", "voice", "video", "search", "analytics", "inference", "semiconductor", "space", "fusion",
    "battery", "energy", "insurtech", "proptech", "healthtech", "edtech", "biotech", "medical", "enterprise",
    "e-commerce", "commerce", "payments", "crypto", "stablecoin", "viral", "stealth", "secretive", "hot", "buzzy",
    "new", "young", "rising", "military", "satellite", "autonomous", "self-driving", "consumer", "app", "tech",
    "hardware", "networking", "web", "browser", "assistant", "personal", "photonics", "quantum", "gpu", "llm",
    "open-source", "frontier", "research", "native", "vibe", "vibe-coding", "neocloud", "rocket", "ev", "smart",
    "ring", "wearable", "logistics", "hr", "accounting", "marketing", "sales", "customer", "service", "support",
    "prediction", "market", "markets", "exchange", "neobank", "lender", "insurer", "retailer", "marketplace",
}
ROLE_NOUNS = {"startup", "start-up", "startups", "firm", "company", "maker", "developer", "provider", "unicorn", "giant",
              "rival", "upstart", "player", "operator", "outfit", "business", "chipmaker", "specialist", "pioneer",
              "creator", "leader", "challenger", "lab", "platform", "co"}
BAD_NAMES = {"ai", "ipo", "series", "seed", "sec", "ceo", "report", "nasdaq", "nyse", "wall street", "big tech", "vc",
             "vcs", "us", "uk", "eu", "the", "this", "that", "why", "how", "what", "who", "here", "meet", "inside",
             "watch", "sources", "exclusive", "startup", "startups", "investors", "funding", "tech", "its", "a", "an",
             "after", "before", "as", "with", "new", "top", "best", "biggest", "major", "latest", "former", "ex",
             "billionaire", "china", "india", "europe", "israel", "france", "germany", "japan", "korea", "america",
             "global", "world", "week", "weekly", "today", "breaking", "update", "opinion", "analysis", "q1", "q2",
             "q3", "q4", "h1", "h2", "it", "he", "she", "they", "we", "you", "i", "is", "one", "two", "three", "one-person",
             "ai startup", "ai startups", "start-up", "valuation", "valuations", "revenue", "ipo", "funding round",
             "unicorn", "unicorns", "shares", "stocks", "markets", "deal", "deals", "vcs", "hong kong", "singapore",
             "silicon valley", "asia", "london", "new york", "san francisco", "beijing", "shanghai", "shenzhen",
             "tokyo", "paris", "berlin", "dubai", "saudi", "uae", "texas", "california", "company", "firm", "founders", "founder", "stock", "shares"}
STOP_TITLE = {"ipo", "listing", "debut", "makes", "shares", "stock", "gmp", "subscription", "allotment",
              "for", "in", "at", "to", "as", "with", "from", "after", "amid", "on", "and", "deal", "worth", "valued",
              "valuation", "reportedly", "series", "seed", "funding", "round", "raises", "raise", "hits", "the", "by",
              "founded", "led", "backed", "via", "over", "of", "into", "is", "that", "which", "who", "a", "an", "its"}
POSSESSIVE_NEXT = {"valuation", "value", "annualized", "annual", "revenue", "arr", "ipo", "shares", "stock",
                   "market", "run-rate", "funding", "latest", "new", "series"}
CONNECT = {"&", "AI", "ai", "Labs", "de", "von"}

_UNIT_WORDS = {"billion", "million", "trillion", "thousand", "yuan", "euros", "dollars", "bn", "mn", "crore",
               "post-money", "pre-money"}
_TRAIL = re.compile(r"[,;:!?\"“”)\]’']+$")
_LEAD = re.compile(r"^[\"“‘(\[']+")


def _clean_tok(t: str) -> str:
    t = _LEAD.sub("", _TRAIL.sub("", t))
    if t.endswith(".") and not re.fullmatch(r"(?:[A-Za-z]\.){2,}", t):
        t = t[:-1]
    return t


def _is_possessive(raw: str) -> bool:
    return bool(re.search(r"['’]s[,:]?$", raw))


def _is_cap(t: str) -> bool:
    if not t or re.match(r"^[$€£¥₹]", t) or re.fullmatch(r"\d+(?:\.\d+)?[BMKbmk%x]?", t):
        return False
    if re.search(r"[\u4e00-\u9fff]", t):
        return False
    if t.lower() in _UNIT_WORDS:
        return False
    if t[0].isupper():
        return True
    return bool(re.fullmatch(r"\d+[A-Za-z][\w.\-]*", t))


@dataclass
class Extraction:
    company: str | None = None
    event: str | None = None  # funding | ipo | mna | arr
    status: str = "closed"  # closed | rumored
    amount_usd: float | None = None
    valuation_usd: float | None = None
    arr_usd: float | None = None
    round: str | None = None
    acquirer: str | None = None
    sectors: list[str] = field(default_factory=list)
    region: str | None = None
    lang: str = "en"
    method: str = "rules"
    deal: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class Rules:
    """Baseline word lists merged with learned additions from knowledge/patterns.json."""

    def __init__(self, patterns: dict | None = None):
        p = patterns if patterns is not None else (load_json("patterns.json", {}) or {})
        self.subject_verbs = SUBJECT_VERBS | set(p.get("extra_subject_verbs", []))
        self.descriptors = DESCRIPTORS | set(p.get("extra_descriptors", []))
        self.bad_names = BAD_NAMES | set(p.get("extra_bad_names", []))
        self.sectors: dict[str, list[str]] = load_json("sectors.json", {}) or {}
        self.company_sectors: dict[str, list[str]] = load_json("company_sectors.json", {}) or {}
        self.regions: dict[str, list[str]] = load_json("regions.json", {}) or {}
        self.aliases: dict[str, str] = {company_key_base(k): v for k, v in (load_json("aliases.json", {}) or {}).items()}
        known = set(load_json("known_companies.json", []) or []) | set(self.aliases.values())
        blocked = {company_key_base(x) for x in (load_json("not_startups.json", []) or [])}
        self.blocked = blocked
        # longest first so "Modal Labs" wins over "Modal"
        self.known = sorted((k for k in known if company_key_base(k) not in blocked and len(k) >= 3
                             and (re.search(r"[\u4e00-\u9fff]", k) or _valid(k, self))), key=len, reverse=True)
        self.alias_surface = sorted(((k, v) for k, v in (load_json("aliases.json", {}) or {}).items()
                                     if re.search(r"[\u4e00-\u9fff]", k) and len(k) >= 2), key=lambda kv: -len(kv[0]))


def company_key_base(name: str) -> str:
    k = name.strip().lower()
    k = re.sub(r"[’'`\"“”,()]", "", k)
    k = k.replace(".", "")
    k = re.sub(r"\s+", " ", k).strip()
    k = re.sub(r"\s+(?:inc|corp|corporation|ltd|co|technologies|technology|systems|holdings|group)$", "", k)
    k = re.sub(r"\s+ai$", "", k)
    return k.strip()


def normalize_company(name: str, rules: Rules) -> tuple[str, str]:
    """Return (display_name, key) after alias resolution."""
    base = company_key_base(name)
    canon = rules.aliases.get(base)
    if canon:
        return canon, company_key_base(canon)
    return name.strip(), base


def clean_title(t: str) -> str:
    t = t.strip()
    t = re.sub(r"^【[^】]{1,20}】", "", t)
    t = re.sub(r"^[^\w$€£¥₹\u4e00-\u9fff]+", "", t)
    for _ in range(2):
        t = re.sub(r"^(?i:icymi|recap|exclusive|scoop|sources?|breaking|report|reports|media|update|watch|market chatter|analysis|opinion|"
                   r"explainer|video|podcast|快讯|独家|重磅|突发)\s*(?:-|:|\||–|—|：|丨)\s*", "", t)
    parts = re.split(r"\s*[｜|丨]\s*", t)
    if len(parts) > 1 and len(parts[0]) >= 12:
        t = parts[0]
    return t.strip()


def _run_back(toks: list[str], raws: list[str], i: int, rules: Rules) -> str | None:
    """Collect a capitalized name run ending just before index i (walking backwards)."""
    j = i - 1
    while j >= 0 and (toks[j].lower() in ADVERBS or toks[j].lower() in MODALS):
        j -= 1
    if j >= 0 and toks[j] in ("&", "and", "And"):
        return None  # "X strikes deal with Y & raises ..." — subject is ambiguous
    run: list[str] = []
    while j >= 0 and len(run) < 5:
        t, raw = toks[j], raws[j]
        if raw.endswith(",") or raw.endswith(":") or raw.endswith("：") or _is_possessive(raw):
            break
        if re.search(r"-(?i:led|backed|owned|founded|based|funded|linked|born|made)$", t):
            break
        low = t.lower()
        if low in STOP_TITLE and low not in ("the",):
            break
        if low in ROLE_NOUNS and not (j == 0 and not run):
            break
        if low in rules.descriptors and t not in CONNECT:
            # A capitalized descriptor directly after a real name is part of the name
            # ("Unitree Robotics", "Oasis Security", "Mistral AI"); otherwise it is a label.
            prev_ok = (j - 1 >= 0 and _is_cap(toks[j - 1]) and toks[j - 1].lower() not in rules.descriptors
                       and not raws[j - 1].endswith((",", ":", "：")) and not _is_possessive(raws[j - 1])
                       and not re.search(r"-(?i:led|backed|owned|founded|based|funded)$", toks[j - 1]))
            title_start = (j == 0 and not run and _is_cap(t))
            if not (_is_cap(t) and (prev_ok or title_start)):
                break
            run.insert(0, t)
            j -= 1
            continue
        if _is_cap(t) or t in CONNECT:
            run.insert(0, t)
            j -= 1
            continue
        break
    while len(run) > 1 and (run[0].lower() in rules.descriptors or run[0] in ("&",) or run[0].lower() in LEAD_NOISE):
        run.pop(0)
    return _valid(" ".join(run), rules)


def _run_fwd(toks: list[str], i: int, rules: Rules, raws: list[str] | None = None) -> str | None:
    """Collect a capitalized name run starting at index i, skipping leading descriptors."""
    j = i
    if raws and j < len(raws) and raws[j][:1] in "'‘\"“":
        while j < len(raws) and not re.search(r"['’\"”][,:]?$", raws[j]):
            j += 1
        j += 1  # skip 'Godmother Of AI'
        if j >= len(toks):
            return None
    while j < len(toks) and (toks[j].lower() in rules.descriptors or not _is_cap(toks[j])) and j < i + 7:
        if toks[j].lower() in STOP_TITLE and toks[j].lower() not in ("the", "its", "a", "an"):
            return None
        if re.search(r"['’]s$", toks[j]):
            return None  # "acquire AI pioneer's San Francisco startup" — target unnamed
        j += 1
    run: list[str] = []
    while j < len(toks) and len(run) < 5:
        t = toks[j]
        if re.search(r"['’]s$", t):
            if not run and _is_cap(t):
                return _valid(re.sub(r"['’]s$", "", t), rules)  # "invest in Kalshi's new fundraise"
            return None  # "... backs Ex-DeepMind Researcher's New AI Startup" — target is unnamed
        if t.lower() in STOP_TITLE:
            if not run:
                return None  # "Buys AI Startup For $8.2B" — target unnamed
            break
        if _is_cap(t) or (run and t in CONNECT):
            run.append(t)
            j += 1
            continue
        break
    return _valid(" ".join(run), rules)


PEOPLE = {"leaders", "founders", "founder", "researchers", "researcher", "alumni", "veterans", "staffers", "executives",
          "engineers", "investors", "backers", "employees", "ceo", "cto", "billionaire", "dropouts", "scientists"}


FUNDS = {"fund", "capital", "ventures", "partners", "investments", "vc"}


def _valid(name: str, rules: Rules) -> str | None:
    name = re.sub(r"['’]s$", "", name.strip())
    name = re.sub(r"(?:\s+(?:IPO|GMP|Stock|Shares|Listing))+$", "", name)
    if not name or len(name) < 2:
        return None
    last = name.split()[-1].lower()
    if last in PEOPLE or last in FUNDS or (last in ROLE_NOUNS and len(name.split()) > 1):
        return None
    if name.lower() in rules.bad_names:
        return None
    first = name.split()[0].lower()
    if first in rules.bad_names and len(name.split()) == 1:
        return None
    if first in ("the", "this", "why", "how", "what", "who", "here", "meet", "inside", "these", "those", "one", "two",
                 "three", "four", "five", "six", "seven", "eight", "nine", "ten", "several", "many", "some", "all"):
        return None
    return name


def _find_phrase(low_toks: list[str], phrases: list[str]) -> tuple[int, int] | None:
    best = None
    for ph in phrases:
        pt = ph.split()
        n = len(pt)
        for i in range(len(low_toks) - n + 1):
            if low_toks[i:i + n] == pt:
                if best is None or i < best[0] or (i == best[0] and n > best[1] - best[0]):
                    best = (i, i + n)
                break
    return best


def _company_en(title: str, event: str | None, rules: Rules) -> tuple[str | None, str | None]:
    """Return (company, acquirer)."""
    raws = title.split()
    toks = [_clean_tok(t) for t in raws]
    low = [t.lower() for t in toks]

    # "Company: $150 Million Series D ..." (Pulse 2.0 style)
    m = re.match(r"^([^:：]{2,45})[:：]\s", title)
    if m and event in ("funding", "arr", "ipo"):
        cand = m.group(1).strip()
        if len(cand.split()) <= 4 and all(_is_cap(_clean_tok(w)) or w in CONNECT for w in cand.split()):
            v = _valid(cand, rules)
            if v:
                return v, None

    if event == "mna":
        hit = _find_phrase(low, PASSIVE_MNA)
        if hit:
            return _run_back(toks, raws, hit[0], rules), _run_fwd(toks, hit[1], rules)
        hit = _find_phrase(low, MNA_PHRASES)
        if hit:
            return _run_fwd(toks, hit[1], rules, raws), _run_back(toks, raws, hit[0], rules)

    if event == "funding":
        hit = _find_phrase(low, INVEST_PHRASES)
        if hit:
            tgt = _run_fwd(toks, hit[1], rules)
            if tgt:
                return tgt, None

    # possessive: "Anthropic's valuation surges"; noun-adjunct: "SpaceX stock closes", "Cerebras shares soar"
    for i, raw in enumerate(raws[:-1]):
        if i > 3:
            break
        if _is_possessive(raw) and low[i + 1] in POSSESSIVE_NEXT:
            fixed = raws[:i] + [re.sub(r"['’]s[,:]?$", "", raw)]
            cand = _run_back([_clean_tok(x) for x in fixed] + [""], fixed + [""], i + 1, rules)
            if cand:
                return cand, None
        if low[i + 1] in ("stock", "shares") and _is_cap(toks[i]) and not _is_possessive(raw) \
                and low[i] not in rules.descriptors and i + 2 <= len(low):
            cand = _run_back(toks, raws, i + 1, rules)
            if cand:
                return cand, None

    for i, t in enumerate(low):
        anchor = False
        if t in rules.subject_verbs:
            anchor = True
            if t in WEAK_VERBS:
                rest = " ".join(low[i + 1:i + 6])
                anchor = bool(re.search(r"[$€£¥₹]|\d|series|seed|funding|raise|round|ipo|valuation|revenue|arr|unicorn", rest))
        elif t in AUX and i + 1 < len(low) and (low[i + 1] in AUX_NEXT or low[i + 1] in rules.subject_verbs):
            if t == "to" and low[i + 1] not in ("raise", "go", "file", "list"):
                anchor = False
            elif t == "in" and low[i + 1] not in ("talks", "discussions", "final"):
                anchor = False
            else:
                anchor = True
        if anchor and i > 0:
            cand = _run_back(toks, raws, i, rules)
            if cand:
                return cand, None
    return None, None


# ---------------------------------------------------------------- company extraction (ZH)
ZH_VERB = re.compile(
    r"(?:宣布|官宣)?(?:即将完成|将完成|已完成|完成|获得|再获|又获|斩获|拿下|获投|获|启动|拟|洽谈|寻求|正以|首轮融资|新一轮融资|"
    r"新轮融资|融资|估值|上市|IPO|登陆|递表|挂牌|冲刺|赴港|被)")
ZH_DESC = ["服务商", "供应商", "运营商", "提供商", "制造商", "开发商", "独角兽", "初创公司", "初创企业", "创业公司", "创企", "初创", "公司", "企业", "厂商", "明星", "黑马", "新锐", "龙头",
           "巨头", "平台", "旗下"]
ZH_LEAD = re.compile(r"^(?:意大利|德国|法国|英国|日本|韩国|印度|以色列|欧洲|新加坡|加拿大|澳大利亚|瑞典|瑞士|荷兰|西班牙|的|在|让|由|将|与|和|从|为|对|据|投融资动态|消息称|据悉|据报道|据报|传|曝|快讯|独家|重磅|官宣|又一|国内|全球|首家|中国|美国|硅谷|英伟达投资的|"
                     r"腾讯投资的|阿里投资的|红杉投资的|投资界|最新|刚刚)+")
ZH_TRAIL = re.compile(r"(?:获超|获|拿下|斩获|二度|二次|再度|三度|首次|港股|A股|美股|科创板|创业板|北交所|最新|再次|本轮|此前|目前|日前|近期|即将|正式|已经|已|再|又|拟|或将|宣布|刚刚|成功|将|今日|今天|近日|日前|本周|首日|正|也|再度|终于)+$")
ZH_JUNK = re.compile(r"(产业链|领域|日报|周报|月报|希望|成立|完成|首轮|领投|跟投|基金|投资方|以|按|计划|目标|冲刺|个月|月底|最新|发布|式$|前$|后$|年$|天$|周$|日$|起$|并$|"
                     r"^[一二三四五六七八九十\d]+|\d{4}年|年度|股票|发行|之$|^又|^再|^新|实习生|创业|新公司|投资人|创始人|们|什么|如何|为何|为什么|谁|这|那|"
                     r"的$|了$|吗|呢|！|？|\?|!|“|”|《|》)")
ZH_BAD = {"赴港", "赴美", "集体", "三巨头", "巨头", "目标", "计划", "消息", "报道", "据报道", "市场", "行业", "赛道", "资本", "投资", "洽谈", "融资", "估值", "上市", "完成", "获得", "收购", "IPO", "公司", "企业", "AI", "独角兽", "机器人", "大模型", "智能体", "短剧", "港股", "A股", "美股", "新股", "该公司"}


ZH_MONEY_TAIL = re.compile(r"(?:以|按|将以|拟以|计划以)\s*[\d.,万千百]+\s*(?:万亿|千亿|百亿|亿|千万|百万|万)?\s*(?:美元|美金|元|人民币|欧元|港元)?.*$|"
                           r"[\d.,万千百]+\s*(?:万亿|千亿|百亿|亿|千万|百万|万)?\s*(?:美元|美金|元|人民币|欧元|港元)?\s*$")
ZH_VERBISH = re.compile(r"(发布|计划|推出|宣布|启动|寻求|完成|获得|获|以|按|在|将|拟|正在|已|与|和|并)")


ZH_GENERIC = re.compile(r"^(?:AI|人工智能)?[\u4e00-\u9fff]{0,4}(?:音乐|视频|编程|芯片|机器人|医疗|金融|安全|大模型|智能体|具身|自动驾驶|"
                        r"航天|能源|电池|数据|算力|短剧|漫剧|教育|游戏|电商|物流|汽车|制药|药企)$")


def _zh_clean(cand: str) -> str | None:
    cand = ZH_MONEY_TAIL.sub("", cand)
    cand = re.sub(r"(?:以|按|将|拟|计划|正在|已)+$", "", cand)
    head = re.match(r"^([A-Za-z][A-Za-z0-9.\-]*[A-Za-z0-9])(?=[\u4e00-\u9fff])", cand)
    if head and ZH_VERBISH.search(cand[len(head.group(1)):]):
        cand = head.group(1)  # "Instinct以100亿美元" / "OpenAI发布AI助手Dots并" -> Latin head
    for d in ZH_DESC:  # "合肥产投集团旗下中科离子公司" -> "中科离子公司"
        if d in cand[:-len(d)]:
            cand = cand.split(d)[-1] or cand
    for d in ZH_DESC:  # "中科离子公司" -> "中科离子"; "AI音乐独角兽" -> "AI音乐" (generic -> None)
        if cand.endswith(d) and len(cand) > len(d):
            cand = cand[: -len(d)]
            if ZH_GENERIC.match(cand) or re.fullmatch(r"(?:AI|人工智能)?[\u4e00-\u9fff]{0,2}", cand):
                return None
            break
    cand = ZH_TRAIL.sub("", ZH_LEAD.sub("", cand))
    cand = re.sub(r"(?:天使\+?|种子|Pre-?[A-G]\+{0,2}|[A-G]\+{0,2})轮$", "", cand)  # "同泰怡A轮" -> "同泰怡"
    cand = cand.strip("·.-+ ")
    lead = re.fullmatch(r"(?:[A-Z]{0,3})[\u4e00-\u9fff]{2,}([A-Z][A-Za-z0-9.\-]{2,}(?: [A-Z][A-Za-z0-9.\-]+)*)", cand)
    if lead:
        cand = lead.group(1)
    mixed = re.fullmatch(r"([A-Za-z][A-Za-z0-9.\-]+)([\u4e00-\u9fff]{1,4})", cand)
    if mixed and not re.search(r"(科技|智能|机器人|数据|医疗|汽车|资本|集团|动力|生物|半导体|芯|云)$", mixed.group(2)):
        cand = mixed.group(1)  # "OpenAI推迟" -> "OpenAI"
    if len(cand) < 2 or len(cand) > 20 or cand in ZH_BAD or cand.isdigit():
        return None
    cjk = len(re.findall(r"[\u4e00-\u9fff]", cand))
    if cjk > 10 or ZH_JUNK.search(cand):
        return None
    if re.fullmatch(r"[\d.%+]+", cand):
        return None
    return cand


def _company_zh(title: str, event: str | None) -> tuple[str | None, str | None]:
    if event == "mna":
        m = re.search(r"被([^，,。；\s]{0,15}?)收购", title)
        if m:
            tail = re.search(r"([A-Za-z0-9\u4e00-\u9fff·.\-]+)$", title[: m.start()])
            tgt = _zh_clean(tail.group(1)) if tail else None
            acq = _zh_clean(m.group(1)) if m.group(1) else None
            if tgt:
                return tgt, acq
        m = re.search(r"收购", title)
        if m:
            prefix = re.sub(r"(?:拟以|将以|以)[^以]*$", "", title[: m.start()])
            prefix = re.sub(r"(?:拟|将|宣布|正式|已|计划)+$", "", prefix)
            tail = re.search(r"([A-Za-z0-9\u4e00-\u9fff·.\-]+)$", prefix)
            acq = _zh_clean(tail.group(1)) if tail else None
            after = re.split(r"[，,。；|｜：:（(]", title[m.end():])[0]
            latins = [mm for mm in re.finditer(r"([A-Z][A-Za-z0-9.\-]+(?: [A-Z][A-Za-z0-9.\-]+)*)", after)
                      if mm.group(1).lower() not in DESCRIPTORS and mm.group(1) not in ("AI", "IPO")]
            if latins and re.search(r"[\u4e00-\u9fff]", after[: latins[-1].start()]):
                return latins[-1].group(1), acq
            if re.search(r"(创业公司|初创公司|创企|的公司|公司)\s*$", after):
                return None, acq  # "收购李飞飞AI 创业公司" — target unnamed
            if "的" in after:
                after = after.split("的")[-1]
            after = re.sub(r"^(?:[A-Za-z]{0,4}(?:芯片|机器人|软件|科技)?(?:初创公司|初创企业|公司|创企|独角兽|企业|平台))", "", after)
            after = re.sub(r"(?:股权|多数股权|全部股权|控股权).*$", "", after).strip()
            m2 = re.match(r"([A-Za-z][A-Za-z0-9.\- ]{1,30}|[\u4e00-\u9fff·A-Za-z0-9]{2,15})", after)
            tgt = _zh_clean(m2.group(1).strip()) if m2 else None
            if tgt:
                return tgt, acq
    for m in ZH_VERB.finditer(title):
        prefix = title[: m.start()].rstrip()
        if re.search(r"[A-Za-z\u4e00-\u9fff]\s*(?:和|与|、|及)\s*[A-Za-z\u4e00-\u9fff]+$", prefix) and not re.search(r"[，,：:]", prefix[-12:]):
            return "", None  # "A 和 B 洽谈融资" names two companies: ambiguous, leave to LLM
        tail = re.search(r"((?:[A-Za-z][A-Za-z0-9.\-]* )*[A-Za-z0-9\u4e00-\u9fff·.\-+&]+)$", prefix)
        if not tail:
            continue
        cand = _zh_clean(tail.group(1))
        if cand:
            return cand, None
    return None, None


# ---------------------------------------------------------------- main entry
def _event(title: str, zh: bool, has_money: bool, money_roles: set[str]) -> str | None:
    if zh:
        if re.search(r"(递表|招股|上市首日|挂牌|登陆(?:港交所|科创板|纳斯达克|纽交所|创业板|北交所))", title):
            return "ipo"
        if RE_MNA_ZH.search(title):
            return "mna"
        if RE_IPO_ZH.search(title) and not RE_PREIPO_ZH.search(title):
            return "ipo"
        if RE_FUND_ZH.search(title):
            return "funding"
        if RE_ARR_ZH.search(title) and "arr" in money_roles:
            return "arr"
    if RE_MNA_EN.search(title) and not re.search(r"(?i)\bacquisition (?:of )?(?:customers|talent|users)\b", title):
        return "mna"
    if (RE_IPO_EN.search(title) and not RE_PREIPO_EN.search(title)
            and not re.search(r"(?i)\b(rais\w*|series|seed)\b.*\bvaluation\b", title)
            and not re.search(r"(?i)\b(series [a-k]|seed round|seed funding|funding round)\b", title)):
        return "ipo"
    if RE_FUND_EN.search(title) or "valuation" in money_roles:
        return "funding"
    if RE_ARR_EN.search(title) and ("arr" in money_roles or not has_money):
        return "arr"
    return None


def _round(title: str) -> str | None:
    m = RE_ROUND_EN.search(title)
    if m:
        r = m.group(1)
        low = r.lower()
        if low == "seed":
            return "Seed"
        if low == "pre-seed":
            return "Pre-Seed"
        if low == "pre-ipo":
            return "Pre-IPO"
        if low.startswith("series"):
            return "Series " + r.split(None, 1)[1].upper()
        return r.title()
    m = RE_ROUND_ZH.search(title)
    if not m:
        return None
    r = m.group(1)
    zh_map = {"天使轮": "Angel", "天使+轮": "Angel+", "种子轮": "Seed", "战略融资": "Strategic", "战略投资": "Strategic",
              "首轮": "First Round", "Pre-IPO": "Pre-IPO", "Pre-IPO轮": "Pre-IPO"}
    if r in zh_map:
        return zh_map[r]
    mm = re.fullmatch(r"Pre-?([A-G]\+?)轮", r)
    if mm:
        return f"Pre-{mm.group(1)}"
    mm = re.fullmatch(r"([A-G](?:\+{1,2}|-\d)?)轮", r)
    return f"Series {mm.group(1)}" if mm else r


def _sectors(title: str, company_key: str | None, rules: Rules) -> list[str]:
    low = title.lower()
    out = []
    for sector, kws in rules.sectors.items():
        for kw in kws:
            kwl = kw.lower()
            if re.search(r"[\u4e00-\u9fff]", kwl):
                hit = kwl in low
            else:
                hit = re.search(r"(?<![a-z])" + re.escape(kwl) + r"(?![a-z])", low) is not None
            if hit:
                out.append(sector)
                break
    if not out and company_key and company_key in rules.company_sectors:
        out = list(rules.company_sectors[company_key])
    return out


def _region(title: str, rules: Rules) -> str | None:
    low = title.lower()
    for region, kws in rules.regions.items():
        for kw in kws:
            kwl = kw.lower()
            if re.search(r"[\u4e00-\u9fff]", kwl):
                if kwl in low:
                    return region
            elif re.search(r"(?<![a-z])" + re.escape(kwl) + r"(?![a-z])", low):
                return region
    return None


def extract(title: str, rules: Rules | None = None) -> Extraction:
    rules = rules or Rules()
    t = clean_title(title)
    zh = bool(re.search(r"[\u4e00-\u9fff]{2,}", t))
    money = find_money(t)
    roles = {m.role for m in money}
    ex = Extraction(lang="zh" if zh else "en")
    ex.event = _event(t, zh, bool(money), roles)
    ex.status = "rumored" if (RE_RUMOR_ZH.search(t) if zh else RE_RUMOR_EN.search(t)) else "closed"
    for m in money:
        if m.role == "valuation" and ex.valuation_usd is None:
            ex.valuation_usd = m.usd
        elif m.role == "arr" and ex.arr_usd is None:
            ex.arr_usd = m.usd
        elif m.role == "amount" and ex.amount_usd is None:
            ex.amount_usd = m.usd
    ex.round = _round(t)
    if zh and RE_DIGEST_ZH.search(t):
        ex.amount_usd = ex.valuation_usd = ex.arr_usd = None  # multi-story digest: money may belong to another item
    company, acquirer = (_company_zh(t, ex.event) if zh else (None, None))
    if company is None:
        company, acquirer = _company_en(t, ex.event, rules)
    if company is None and ex.event:
        company = _known_at_start(t, zh, rules)
    company = company or None
    if company:
        ex.company, key = normalize_company(company, rules)
    else:
        key = None
    if acquirer:
        ex.acquirer = normalize_company(acquirer, rules)[0]
    if key:
        for mo in money:
            owner = re.search(r"([A-Z][\w.&\-]+)['’]s\s+(?:[a-z\-]+\s+){0,2}$", t[: mo.start])
            if zh and not owner:
                for surf, canon in rules.alias_surface:  # "在英伟达130亿美元交易前" -> money belongs to Nvidia
                    if t[: mo.start].rstrip().endswith(surf):
                        owner = re.match(r"(.+)", canon)
                        break
            if owner and company_key_base(owner.group(1)) != key and company_key_base(owner.group(1)) not in key:
                for f in ("amount_usd", "valuation_usd", "arr_usd"):
                    if getattr(ex, f) == mo.usd:
                        setattr(ex, f, None)
    ex.sectors = _sectors(t, key, rules)
    ex.region = _region(t, rules)
    ex.deal = (is_deal(ex) and not (ex.event == "funding" and RE_DEBT.search(t) and not ex.valuation_usd and not ex.round)
               and key not in rules.blocked and not RE_NOT_DEAL.search(t))
    return ex


RE_DIGEST_ZH = re.compile(r"(头条|早报|晚报|早知道|速递|一览|汇总|8点1氪|早参|快报|日报|周报)")
RE_NOT_DEAL = re.compile(r"(?i)\b(seed cap|investment limit|investment ceiling|cheque size|check size|new fund|fund size|"
                         r"closes (?:its )?(?:\w+ )?fund|raises (?:a )?(?:new )?(?:\$[\d.]+\w* )?(?:venture )?fund|fund (?:i|ii|iii|iv|v|vi)\b)")
RE_DEBT = re.compile(r"(?i)\b(bonds?|notes offering|loan|credit facility|credit line|convertible notes|high-yield)\b|债券|贷款|授信")


def is_deal(ex: Extraction) -> bool:
    """A mention counts toward events only if it carries hard facts, not just keywords."""
    if not ex.company or not ex.event:
        return False
    if ex.event == "funding":
        return bool(ex.amount_usd or ex.valuation_usd or ex.round)
    if ex.event == "arr":
        return bool(ex.arr_usd)
    return True


def _known_at_start(t: str, zh: bool, rules: Rules) -> str | None:
    """Memory fallback: a company seen in earlier deals that opens the headline is the subject."""
    head = t[:14] if zh else t[:60]
    for surf, canon in rules.alias_surface:
        if head.startswith(surf):
            return canon
    for name in rules.known:
        if zh:
            if head.startswith(name):
                return name
        elif re.match(re.escape(name) + r"(?:['’]s)?(?![A-Za-z0-9])", t):
            return name
    return None


def looks_like_deal(title: str) -> bool:
    """Heuristic used to collect *unparsed* candidates for the evolve step."""
    t = clean_title(title)
    if not find_money(t):
        return False
    return bool(RE_FUND_EN.search(t) or RE_MNA_EN.search(t) or RE_IPO_EN.search(t) or RE_FUND_ZH.search(t)
                or RE_MNA_ZH.search(t) or RE_IPO_ZH.search(t))
