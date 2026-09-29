#!/usr/bin/env python3
"""
md2wechat — 把 Markdown 转成可直接粘贴进微信公众号编辑器的 HTML。

特点
  * 零依赖：只用 Python 3.8+ 标准库。
  * 全内联样式：公众号会剥离 <style>、class、id、<script>，所以每个元素都自带 style。
  * 移动端优先：15px 正文 / 1.85 行高 / 0.5px 字距 / 两端对齐，按 375pt 手机屏幕调校。
  * 六套主题：陶土 clay（默认）、素白 mono、墨印 ink、青瓷 celadon、琥珀 amber、石墨 graphite。
  * 扩展组件：导读、金句、提示卡、卡片、结尾区块、==高亮==。
  * 外链自动转脚注（公众号正文不允许外链；mp.weixin.qq.com 链接保留）。
  * 中英文之间自动加空格（盘古之白），中文语境直引号转弯引号。
  * --check 可读性检查：段落过长、小标题过长、连续大段无视觉锚点等。
  * 文风检查：套话、AI 腔、模糊信源（“有研究表明”）、空标题、感叹号过多；
    人味检查：书面腔 / 拔高腔 / 收尾腔、设问自答、排比三连、高频句式、破折号、句长节奏
    （--no-style 或 front matter lint: layout 关闭）。
  * <!-- 注释 --> 不进入正文，可用来写论点卡和写作备注。

用法
  python md2wechat.py article.md                 # 输出 article.html（带手机预览 + 一键复制）
  python md2wechat.py article.md --theme mono
  python md2wechat.py article.md --fragment -o out.html   # 仅输出可粘贴的 HTML 片段
  python md2wechat.py article.md --check         # 只做可读性检查
  python md2wechat.py --list-themes
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

FONT = "-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Helvetica Neue',Arial,sans-serif"
SERIF = "Georgia,'Times New Roman','Songti SC',serif"
# 中文衬线标题：iOS 宋体 / 安卓思源宋体 / Windows 宋体，均为系统字体，无需加载
SERIF_CN = "'Songti SC','Noto Serif SC','Source Han Serif SC','Noto Serif CJK SC',STSong,SimSun,Georgia,serif"
MONO = "Menlo,Monaco,Consolas,'Courier New',monospace"

# ──────────────────────────────────────────────────────────────────────────────
# 主题
# 每个主题 = 颜色 + 一组“结构开关”。未声明的开关取 DEFAULTS。
# ──────────────────────────────────────────────────────────────────────────────
DEFAULTS: dict = {
    "head_font": None,      # 标题字体；None = 继承正文无衬线
    "h2": "editorial",      # seal | numeral | editorial | index | big
    "h2_size": "19px",
    "h2_ls": "1px",
    "h2_rule": False,       # index 样式：章节上方是否加细线
    "h2_marker": False,     # index 样式：序号前是否加信号色方块
    "h3": "bar",            # bar | square | plain
    "h3_size": "16px",
    "hr": "· · ·",
    "hr_style": "glyph",    # glyph | line
    "quote": "center",      # center | serif | display
    "lead": "box",          # box | dek
    "lead_color": None,     # 导读正文颜色；None = muted
    "callout": "bar",       # bar（左竖线）| soft（圆角色块）
    "radius": "4px",
    "bullet": "dot",        # dot | square
    "ol_font": SERIF,
    "ol_color": None,       # None = accent
    "ol_fmt": "{n}.",
    "table": "tint",        # tint（表头色底）| rule（黑色细线）
    "mark": None,           # ==高亮== 底色；None = mid
    "link": None,           # 链接文字色；None = accent
    "link_line": None,      # 链接下划线；None = mid
    "code_color": None,     # 行内代码色；None = accent
    "signal": None,         # 信号色（脚注号、强调下划线、标记）；None = accent
    "rule": "#EEEEEE",      # 细线颜色
    "quote_line": None,     # 引用左线；None = mid
    "warn": "#B0413E",
    "warn_bg": "#FBF0EF",
    "end": "— END —",
    "paper": "#FAF8F3",     # front matter `paper: true` 时的纸张底色
}

THEMES: dict[str, dict] = {
    "clay": {
        "label": "陶土",
        "desc": "灵感来自 Claude：燕麦纸色、陶土橙、宋体标题、章节序号。温暖知性，适合观点、人文、AI 与科技随笔。",
        "accent": "#C2603E",
        "soft": "#F4F0E8",
        "mid": "#E4D9C8",
        "text": "#3D3A34",
        "heading": "#1C1B18",
        "muted": "#8B857A",
        "code_bg": "#F4F0E8",
        "head_font": SERIF_CN,
        "h2": "index",
        "h2_size": "20px",
        "h2_ls": "0.5px",
        "h3": "plain",
        "h3_size": "17px",
        "hr": "· · ·",
        "quote": "serif",
        "lead": "box",
        "lead_color": "#5A554C",
        "callout": "soft",
        "radius": "12px",
        "mark": "#F2DDD0",
        "link_line": "#E3B8A4",
        "code_color": "#A34E30",
        "rule": "#ECE6DB",
        "end": "— 完 —",
        "paper": "#FAF8F3",
    },
    "mono": {
        "label": "素白",
        "desc": "灵感来自 OpenAI：黑白灰、细线分隔、大号无衬线金句，外加一点信号橙。理性锐利，适合技术、产品、AI、研究解读。",
        "accent": "#0D0D0D",
        "soft": "#F5F5F5",
        "mid": "#E3E3E3",
        "text": "#353740",
        "heading": "#0D0D0D",
        "muted": "#8E8EA0",
        "code_bg": "#F7F7F8",
        "signal": "#F2542D",
        "h2": "index",
        "h2_size": "21px",
        "h2_ls": "0",
        "h2_rule": True,
        "h2_marker": True,
        "h3": "plain",
        "h3_size": "16.5px",
        "hr_style": "line",
        "quote": "display",
        "lead": "dek",
        "lead_color": "#353740",
        "callout": "soft",
        "radius": "12px",
        "bullet": "square",
        "ol_font": MONO,
        "ol_color": "#8E8EA0",
        "ol_fmt": "{n}.",
        "table": "rule",
        "mark": "#FFE3D9",
        "link": "#0D0D0D",
        "link_line": "#F2542D",
        "code_color": "#0D0D0D",
        "rule": "#E8E8E8",
        "quote_line": "#D0D0D6",
        "warn": "#F2542D",
        "warn_bg": "#FFF3EE",
        "end": "END",
        "paper": "#FAFAFA",
    },
    "ink": {
        "label": "墨印",
        "desc": "宣纸白 + 朱砂印章红。东方留白，适合人文、随笔、观点、品牌故事。",
        "accent": "#B5462F",
        "soft": "#F8F1EE",
        "mid": "#E5C8BE",
        "text": "#3F3F3F",
        "heading": "#1F1F1F",
        "muted": "#8C8C8C",
        "code_bg": "#F7F5F2",
        "h2": "seal",
        "h3": "square",
        "hr": "◆",
    },
    "celadon": {
        "label": "青瓷",
        "desc": "青绿釉色 + 细衬线数字。安静克制，适合生活方式、读书、健康、教育。",
        "accent": "#3D7A70",
        "soft": "#EEF4F2",
        "mid": "#C3D9D3",
        "text": "#3A4240",
        "heading": "#1E2A28",
        "muted": "#8A9693",
        "code_bg": "#F3F6F5",
        "h2": "numeral",
        "h3": "bar",
    },
    "amber": {
        "label": "琥珀",
        "desc": "暖琥珀 + 杂志式小序号。有温度的深度长文、商业分析、人物稿。",
        "accent": "#A8651E",
        "soft": "#FAF4EB",
        "mid": "#EAD4B6",
        "text": "#403A33",
        "heading": "#221C15",
        "muted": "#958B7F",
        "code_bg": "#F8F5F0",
        "h2": "editorial",
        "h3": "bar",
        "hr": "◇ ◇ ◇",
    },
    "graphite": {
        "label": "石墨",
        "desc": "石墨灰 + 钢蓝。理性清晰，适合技术、产品、数据、教程。",
        "accent": "#2E5E8C",
        "soft": "#EFF3F8",
        "mid": "#C8D5E4",
        "text": "#3B3F45",
        "heading": "#1B1F24",
        "muted": "#8A9099",
        "code_bg": "#F5F7FA",
        "h2": "editorial",
        "h3": "square",
        "hr": "/ / /",
    },
}
DEFAULT_THEME = "clay"

CN_NUM = "零壹贰叁肆伍陆柒捌玖"

# 可读性阈值（按 375pt 屏宽、15px 字号 ≈ 每行 21~22 个汉字 估算）
MAX_PARA_CHARS = 150      # ≈ 7 行；头部账号段落中位数 76–123 字，90 分位 118–192 字（benchmarks.md）
MAX_H2_CHARS = 20        # 观点句式小标题（晚点式）可到两行；短语式建议 6–12 字
MAX_H3_CHARS = 20
MAX_RUN_PARAS = 6         # 连续纯文字段落数
MAX_TITLE_CHARS = 26      # 订阅号消息列表两行内
MAX_SUMMARY_CHARS = 120   # 公众号摘要上限
MAX_CODE_LINE = 40        # 12.5px 等宽字体在手机上一行约 40 字符，超过会横向滚动
READ_SPEED = 400          # 字/分钟

CJK = (
    r"\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f"
    r"\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
)
RE_CJK = re.compile(f"[{CJK}]")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$")
IMG_ONLY_RE = re.compile(r'^!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+"([^"]*)")?\s*\)$')
CODE_PH = "\x02"   # 行内代码占位符（盘古空格把它当作拉丁字符）
PH = "\x00"        # 其它行内占位符


def resolve_theme(name: str) -> dict:
    t = {**DEFAULTS, **THEMES[name]}
    for key, fallback in (("mark", "mid"), ("link", "accent"), ("link_line", "mid"), ("code_color", "accent"),
                          ("signal", "accent"), ("quote_line", "mid"), ("lead_color", "muted"), ("ol_color", "accent")):
        if t[key] is None:
            t[key] = t[fallback]
    return t


def count_chars(text: str) -> int:
    """汉字按 1 计，连续的英文单词/数字按 1 计。"""
    return len(RE_CJK.findall(text)) + len(re.findall(r"[A-Za-z0-9]+", text))


def pangu(text: str) -> str:
    alnum = f"A-Za-z0-9{CODE_PH}"
    text = re.sub(f"([{CJK}])([{alnum}@#$&])", r"\1 \2", text)
    text = re.sub(f"([{alnum}%])([{CJK}])", r"\1 \2", text)
    return text


def smart_quotes(text: str) -> str:
    """中文语境下把直引号 "…" 换成弯引号 “…”（内容含汉字才替换，英文原样保留）。"""
    return re.sub(r'"([^"\n]+?)"', lambda m: f"“{m.group(1)}”" if RE_CJK.search(m.group(1)) else m.group(0), text)


def style(**kw) -> str:
    # 行高一律写成 em（公众号编辑器自带的写法）。不带单位的“1.85”会被公众号的排版检查
    # 判成“行高小于字体大小”；em 在元素上算成 px 再继承，子元素字号更小时也不会重叠。
    lh = kw.get("line_height")
    if lh is not None and re.fullmatch(r"\d+(?:\.\d+)?", str(lh)) and float(lh) > 0:
        kw["line_height"] = f"{lh}em"
    return ";".join(f"{k.replace('_', '-')}:{v}" for k, v in kw.items() if v is not None)


def square(color: str, size: int = 6, gap: str = "8px") -> str:
    return (
        f'<span style="{style(display="inline-block", width=f"{size}px", height=f"{size}px", background_color=color, margin_right=gap, vertical_align="middle")}"></span>'
    )


# ──────────────────────────────────────────────────────────────────────────────
# 渲染器
# ──────────────────────────────────────────────────────────────────────────────
class Renderer:
    def __init__(self, theme: dict, meta: dict):
        self.t = theme
        self.meta = meta
        # 章节序号默认关闭（晚点、少数派都不编号，见 benchmarks.md）；front matter 写 numbered: true 才显示
        self.numbered = str(meta.get("numbered", "false")).lower() == "true"
        self.use_pangu = str(meta.get("pangu", "true")).lower() != "false"
        # 正文字号：15（默认，精致）或 16（大字，适合中老年读者 / 访谈长文）
        self.fs, self.lh = ("16px", "1.8") if str(meta.get("size", "15")).strip() == "16" else ("15px", "1.85")
        # bold: accent → 加粗句用主题色（刘润 / 晚点式“金句着色”）
        self.strong = theme["signal"] if str(meta.get("bold", "")).lower() == "accent" else theme["heading"]
        self.footnotes: list[tuple[str, str]] = []
        self.h2_index = 0
        self.warnings: list[str] = []
        self.chars = 0
        self.images = 0
        self.run = 0          # 连续段落计数
        self.run_start = 0
        # 段落样式覆盖栈（容器内部字号/颜色不同）；以 _ 开头的键是行为开关，不进 style
        self.p_stack: list[dict] = [{}]

    # ── 基础样式 ───────────────────────────────────────────────────────────
    def p_style(self, **extra) -> str:
        base = dict(
            margin="0 0 20px",
            font_size=self.fs,
            line_height=self.lh,
            letter_spacing="0.5px",
            color=self.t["text"],
            text_align="justify",
            word_wrap="break-word",
        )
        base.update({k: v for k, v in self.p_stack[-1].items() if not k.startswith("_")})
        base.update(extra)
        return style(**base)

    def warn(self, line: int, msg: str) -> None:
        self.warnings.append(f"  L{line:<4} {msg}")

    def anchor(self) -> None:
        """遇到小标题/图片/金句等视觉锚点，重置连续段落计数。"""
        self.run = 0

    # ── 行内 ───────────────────────────────────────────────────────────────
    def inline(self, text: str) -> str:
        t = self.t
        ph: list[str] = []
        code_ph: list[str] = []

        def keep(h: str) -> str:
            ph.append(h)
            return f"{PH}{len(ph) - 1}{PH}"

        def keep_code(h: str) -> str:
            code_ph.append(h)
            return f"{CODE_PH}{len(code_ph) - 1}{CODE_PH}"

        # 行内代码
        text = re.sub(
            r"(`+)(.+?)\1",
            lambda m: keep_code(
                f'<code style="{style(font_family=MONO, font_size="13px", color=t["code_color"], background_color=t["soft"], padding="2px 5px", margin="0 2px", border_radius="4px", word_break="break-all")}">'
                f"{html.escape(m.group(2).strip())}</code>"
            ),
            text,
        )
        # 行内图片
        text = re.sub(
            r'!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+"[^"]*")?\s*\)',
            lambda m: keep(
                f'<img src="{html.escape(m.group(2))}" alt="{html.escape(m.group(1))}" '
                f'style="{style(display="inline-block", max_width="100%", height="auto", vertical_align="middle")}"/>'
            ),
            text,
        )
        # 链接
        text = re.sub(
            r'\[([^\]]+)\]\(\s*([^)\s]+)(?:\s+"[^"]*")?\s*\)',
            lambda m: keep(self.link(m.group(1), m.group(2))),
            text,
        )
        # 自动链接 <https://...>
        text = re.sub(r"<(https?://[^>\s]+)>", lambda m: keep(self.link(m.group(1), m.group(1))), text)

        text = html.escape(text, quote=False)
        text = smart_quotes(text)
        if self.use_pangu:
            text = pangu(text)

        text = re.sub(
            r"\*\*(.+?)\*\*|__(.+?)__",
            lambda m: f'<strong style="{style(font_weight="bold", color=self.strong)}">{m.group(1) or m.group(2)}</strong>',
            text,
        )
        text = re.sub(
            r"==(.+?)==",
            lambda m: f'<span style="{style(background_color=t["mark"], color=t["heading"], padding="1px 3px", border_radius="2px")}">{m.group(1)}</span>',
            text,
        )
        text = re.sub(
            r"~~(.+?)~~",
            lambda m: f'<span style="{style(text_decoration="line-through", color=t["muted"])}">{m.group(1)}</span>',
            text,
        )
        # 中文不适合斜体：*强调* 渲染为主题色 + 虚线下划线
        text = re.sub(
            r"(?<![*A-Za-z0-9])\*(?![\s*])(.+?)(?<![\s*])\*(?![*A-Za-z0-9])",
            lambda m: f'<span style="{style(color=t["accent"], border_bottom="1px dashed " + t["signal"], padding_bottom="1px")}">{m.group(1)}</span>',
            text,
        )
        text = text.replace("\x01", "<br/>")

        text = re.sub(f"{CODE_PH}(\\d+){CODE_PH}", lambda m: code_ph[int(m.group(1))], text)
        text = re.sub(f"{PH}(\\d+){PH}", lambda m: ph[int(m.group(1))], text)
        return text

    def link(self, label: str, url: str) -> str:
        t = self.t
        label_html = self.inline(label) if label != url else html.escape(url)
        if "mp.weixin.qq.com" in url:
            return (
                f'<a href="{html.escape(url)}" style="{style(color=t["link"], text_decoration="none", border_bottom="1px solid " + t["link_line"])}">'
                f"{label_html}</a>"
            )
        urls = [u for _, u in self.footnotes]
        if url in urls:
            n = urls.index(url) + 1
        else:
            self.footnotes.append((label, url))
            n = len(self.footnotes)
        sup = f'<sup style="{style(font_size="10px", color=t["signal"], line_height="1", margin_left="1px")}">[{n}]</sup>'
        if label == url:  # 裸链接只保留脚注编号
            return sup
        # 书名号、引号放到下划线外面：包在 span 里时，浏览器不在“《”前换行，整段书名被挤到下一行，上一行两端对齐后字距拉得很开
        m = re.match(r"^([《「『“（]?)(.+?)([》」』”）]?)$", label, re.S)
        pre, core, post = m.groups() if m else ("", label, "")
        core_html = self.inline(core) if (pre or post) else label_html
        return f'{pre}<span style="{style(color=t["link"], border_bottom="1px solid " + t["link_line"])}">{core_html}</span>{post}{sup}'

    # ── 块级 ───────────────────────────────────────────────────────────────
    def is_block_start(self, line: str, nxt: str | None) -> bool:
        s = line.strip()
        return bool(
            not s
            or re.match(r"^(```|~~~)", s)
            or re.match(r"^:::", s)
            or re.match(r"^#{1,6}\s", s)
            or re.match(r"^([-*_])(\s*\1){2,}$", s)
            or s.startswith(">")
            or LIST_RE.match(line)
            or IMG_ONLY_RE.match(s)
            or ("|" in s and nxt is not None and TABLE_SEP_RE.match(nxt.strip()))
        )

    def blocks(self, lines: list[str], base: int = 1) -> str:
        out: list[str] = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            s = line.strip()
            ln = base + i
            if not s:
                i += 1
                continue

            # 围栏代码
            m = re.match(r"^(```+|~~~+)\s*([\w+#.-]*)", s)
            if m:
                fence, lang = m.group(1), m.group(2)
                j, buf = i + 1, []
                while j < n and not lines[j].strip().startswith(fence):
                    buf.append(lines[j])
                    j += 1
                out.append(self.code_block(buf, lang, ln))
                i = j + 1
                continue

            # ::: 容器
            m = re.match(r"^:::\s*([\w-]+)\s*(.*)$", s)
            if m:
                typ, arg = m.group(1).lower(), m.group(2).strip()
                j, depth, buf = i + 1, 1, []
                while j < n:
                    sj = lines[j].strip()
                    if re.match(r"^:::\s*[\w-]+", sj):
                        depth += 1
                    elif sj == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    buf.append(lines[j])
                    j += 1
                out.append(self.container(typ, arg, buf, ln + 1))
                i = j + 1
                continue

            # 标题
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", s)
            if m:
                out.append(self.heading(len(m.group(1)), m.group(2), ln))
                i += 1
                continue

            # 分隔线
            if re.match(r"^([-*_])(\s*\1){2,}$", s):
                out.append(self.hr())
                i += 1
                continue

            # 引用
            if s.startswith(">"):
                j, buf = i, []
                while j < n and lines[j].strip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[j]))
                    j += 1
                out.append(self.blockquote(buf, ln))
                i = j
                continue

            # 表格
            if "|" in s and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1].strip()):
                j, rows = i + 2, []
                while j < n and "|" in lines[j] and lines[j].strip():
                    rows.append(lines[j])
                    j += 1
                out.append(self.table(lines[i], lines[i + 1], rows, ln))
                i = j
                continue

            # 列表
            if LIST_RE.match(line):
                j, buf = i, []
                while j < n:
                    lj = lines[j]
                    if not lj.strip():
                        k = j + 1
                        while k < n and not lines[k].strip():
                            k += 1
                        if k < n and LIST_RE.match(lines[k]):
                            j = k
                            continue
                        break
                    if LIST_RE.match(lj) or (buf and lj[:1] in (" ", "\t")):
                        buf.append(lj)
                        j += 1
                        continue
                    break
                out.append(self.list_block(buf, ln))
                i = j
                continue

            # 独立图片
            m = IMG_ONLY_RE.match(s)
            if m:
                out.append(self.figure(m.group(2), m.group(3) or m.group(1)))
                i += 1
                continue

            # 段落
            j, buf = i, []
            while j < n:
                nxt = lines[j + 1] if j + 1 < n else None
                if buf and self.is_block_start(lines[j], nxt):
                    break
                if not lines[j].strip():
                    break
                buf.append(lines[j])
                j += 1
            out.append(self.paragraph(buf, ln))
            i = j
        return "\n".join(out)

    def join_lines(self, buf: list[str]) -> str:
        text = ""
        keep_breaks = bool(self.p_stack[-1].get("_breaks"))
        for raw in buf:
            hard = keep_breaks or raw.endswith("  ") or raw.rstrip().endswith("\\")
            piece = raw.strip().rstrip("\\").rstrip()
            if text and not text.endswith("\x01"):
                if not (RE_CJK.match(text[-1]) or (piece and RE_CJK.match(piece[0]))):
                    text += " "
            text += piece + ("\x01" if hard else "")
        return text.rstrip("\x01")

    def paragraph(self, buf: list[str], ln: int) -> str:
        text = self.join_lines(buf)
        c = count_chars(re.sub(r"\]\([^)]*\)", "]", text))
        self.chars += c
        if len(self.p_stack) == 1:
            if c > MAX_PARA_CHARS:
                self.warn(ln, f"段落约 {c} 字（手机上 ≈{c // 21 + 1} 行），按意思拆开（多数段落 60–110 字即可）")
            if self.run == 0:
                self.run_start = ln
            self.run += 1
            if self.run == MAX_RUN_PARAS + 1:
                self.warn(self.run_start, f"从此处起连续 {self.run}+ 段纯文字，优先插入配图或图表；不要为此把正文改成列表")
        qa = self.p_stack[-1].get("_qa")
        if qa:
            m = re.match(r"^(?:\*\*)?([^：:*\s]{1,12})(?:\*\*)?[：:]\s*(.*)$", text, re.S)
            if m:
                who, rest = m.groups()
                t = self.t
                if who == qa or who in ("问", "Q"):
                    chip = (
                        f'<span style="{style(display="inline-block", padding="0 6px", margin_right="8px", background_color=t["signal"], color="#FFFFFF", font_size="13px", line_height="1.7", border_radius="3px", letter_spacing="1px", vertical_align="1px")}">{html.escape(who)}</span>'
                    )
                    return f'<p style="{self.p_style(margin="32px 0 14px", font_weight="bold", color=t["heading"])}">{chip}{self.inline(rest)}</p>'
                return (
                    f'<p style="{self.p_style()}"><strong style="{style(font_weight="bold", color=t["heading"])}">{html.escape(who)}：</strong>{self.inline(rest)}</p>'
                )
        return f'<p style="{self.p_style()}">{self.inline(text)}</p>'

    # ── 标题 ───────────────────────────────────────────────────────────────
    def heading(self, level: int, text: str, ln: int) -> str:
        t = self.t
        self.anchor()
        c = count_chars(text)
        self.chars += c
        body = self.inline(text)
        if level == 1:
            return (
                f'<p style="{style(margin="8px 0 32px", font_family=t["head_font"], font_size="22px", font_weight="bold", line_height="1.5", letter_spacing="1px", color=t["heading"], text_align="center")}">{body}</p>'
            )
        if level == 2:
            if c > MAX_H2_CHARS:
                self.warn(ln, f"二级标题 {c} 字，建议 ≤{MAX_H2_CHARS} 字（手机上最好一行）")
            self.h2_index += 1
            return self.h2(body, self.h2_index)
        if level == 3:
            if c > MAX_H3_CHARS:
                self.warn(ln, f"三级标题 {c} 字，建议 ≤{MAX_H3_CHARS} 字")
            mark = ""
            if t["h3"] == "square":
                mark = square(t["accent"], 7, "10px")
            elif t["h3"] == "bar":
                mark = f'<span style="{style(display="inline-block", width="3px", height="15px", background_color=t["accent"], margin_right="10px", vertical_align="-2px", border_radius="2px")}"></span>'
            top = "34px" if t["h3"] == "plain" else "36px"
            return (
                f'<p style="{style(margin=f"{top} 0 12px", font_family=t["head_font"], font_size=t["h3_size"], font_weight="bold", line_height="1.6", letter_spacing="0.5px" if t["h3"] == "plain" else "1px", color=t["heading"], text_align="left")}">{mark}{body}</p>'
            )
        return (
            f'<p style="{style(margin="28px 0 10px", font_size="15px", font_weight="bold", line_height="1.6", letter_spacing="1px", color=t["accent"] if t["accent"] != t["heading"] else t["heading"], text_align="left")}">{body}</p>'
        )

    def h2(self, body: str, idx: int) -> str:
        t = self.t
        variant = t["h2"]
        title_style = style(
            margin="0", font_family=t["head_font"], font_size=t["h2_size"], font_weight="bold", line_height="1.5",
            letter_spacing=t["h2_ls"], color=t["heading"], text_align="left",
        )
        if variant == "big":
            # 大号序号（远川 / 刘润式）：40px 数字压在标题上方，左对齐
            num = ""
            if self.numbered:
                num_font = SERIF if t["head_font"] else FONT
                num = (
                    f'<p style="{style(margin="0 0 8px", font_family=num_font, font_size="40px", font_weight="bold" if not t["head_font"] else None, line_height="1", letter_spacing="1px", color=t["signal"], text_align="left")}">{idx:02d}</p>'
                )
            return f'<section style="{style(margin="52px 0 22px")}">{num}<p style="{title_style}">{body}</p></section>'
        if variant == "index":
            # 只写序号，不加“/ 总数”“PART”这类标签（头部账号实测均不使用，见 benchmarks.md）
            kicker = ""
            if self.numbered:
                marker = square(t["signal"]) if t["h2_marker"] else ""
                num_color = t["heading"] if t["h2_marker"] else t["accent"]
                kicker = (
                    f'<p style="{style(margin="0 0 10px", font_family=MONO, font_size="12px", line_height="1.4", letter_spacing="1px", color=t["muted"], text_align="left")}">'
                    f'{marker}<span style="{style(color=num_color, font_weight="bold")}">{idx:02d}</span></p>'
                )
            sec = style(margin="52px 0 22px", padding_top="20px" if t["h2_rule"] else None,
                        border_top=f"1px solid {t['rule']}" if t["h2_rule"] else None)
            return f'<section style="{sec}">{kicker}<p style="{title_style}">{body}</p></section>'
        center_title = title_style.replace("text-align:left", "text-align:center").replace(
            f"font-size:{t['h2_size']}", "font-size:18px").replace(f"letter-spacing:{t['h2_ls']}", "letter-spacing:2px")
        if variant == "seal":
            num = ""
            if self.numbered:
                label = CN_NUM[idx] if idx < 10 else ("拾" + (CN_NUM[idx - 10] if idx > 10 else ""))
                num = (
                    f'<p style="{style(margin="0 0 14px", line_height="1", text_align="center")}">'
                    f'<span style="{style(display="inline-block", width="30px", height="30px", line_height="30px", background_color=t["accent"], color="#FFFFFF", font_family=SERIF, font_size="16px", text_align="center", border_radius="3px", letter_spacing="0")}">{label}</span></p>'
                )
            dots = "".join(
                f'<span style="{style(display="inline-block", width="4px", height="4px", background_color=c, margin="0 3px", border_radius="50%")}"></span>'
                for c in (t["mid"], t["accent"], t["mid"])
            )
            return (
                f'<section style="{style(margin="56px 0 28px", text_align="center")}">{num}<p style="{center_title}">{body}</p>'
                f'<p style="{style(margin="10px 0 0", line_height="1", font_size="0", text_align="center")}">{dots}</p></section>'
            )
        if variant == "numeral":
            num = ""
            if self.numbered:
                num = (
                    f'<p style="{style(margin="0 0 6px", font_family=SERIF, font_size="34px", font_style="italic", line_height="1.1", color=t["accent"], letter_spacing="2px", text_align="center", opacity="0.9")}">{idx:02d}</p>'
                )
            return (
                f'<section style="{style(margin="56px 0 28px", text_align="center")}">{num}<p style="{center_title}">{body}</p>'
                f'<p style="{style(margin="12px 0 0", line_height="1", font_size="0", text_align="center")}">'
                f'<span style="{style(display="inline-block", width="28px", height="2px", background_color=t["accent"])}"></span></p></section>'
            )
        # editorial
        kicker = ""
        if self.numbered:
            kicker = (
                f'<p style="{style(margin="0 0 6px", font_family=SERIF, font_size="12px", font_weight="bold", line_height="1.4", letter_spacing="3px", color=t["accent"], text_align="left")}">{idx:02d}</p>'
            )
        return (
            f'<section style="{style(margin="52px 0 24px", padding="0 0 12px", border_bottom="1px solid " + t["mid"])}">{kicker}'
            f'<p style="{title_style}">{body}</p></section>'
        )

    # ── 其它块 ─────────────────────────────────────────────────────────────
    def hr(self) -> str:
        self.anchor()
        t = self.t
        if t["hr_style"] == "line":
            return f'<hr style="{style(margin="40px 0", height="0", border="0", border_top="1px solid " + t["rule"])}"/>'
        return (
            f'<p style="{style(margin="40px 0", font_size="12px", line_height="1", letter_spacing="6px", color=t["accent"], text_align="center", opacity="0.75")}">{html.escape(t["hr"])}</p>'
        )

    def blockquote(self, buf: list[str], ln: int) -> str:
        t = self.t
        self.anchor()
        self.p_stack.append(dict(font_size="14px", color=t["muted"], margin="0 0 8px", line_height="1.85"))
        inner = self.blocks(buf, ln)
        self.p_stack.pop()
        return (
            f'<section style="{style(margin="24px 0", padding="4px 0 4px 16px", border_left="3px solid " + t["quote_line"])}">{inner}</section>'
        )

    def figure(self, src: str, caption: str) -> str:
        t = self.t
        self.anchor()
        self.images += 1
        cap = ""
        if caption:
            cap = (
                f'<p style="{style(margin="10px 0 0", font_size="12px", line_height="1.6", letter_spacing="1px", color=t["muted"], text_align="center")}">{self.inline(caption)}</p>'
            )
        radius = "8px" if t["radius"] == "12px" else "4px"
        return (
            f'<section style="{style(margin="28px 0", text_align="center")}">'
            f'<img src="{html.escape(src)}" alt="{html.escape(caption)}" style="{style(display="block", width="100%", height="auto", margin="0 auto", border_radius=radius)}"/>'
            f"{cap}</section>"
        )

    def code_block(self, buf: list[str], lang: str, ln: int) -> str:
        t = self.t
        self.anchor()
        rendered = []
        for k, raw in enumerate(buf):
            raw = raw.replace("\t", "    ")
            if len(raw) > MAX_CODE_LINE:
                self.warn(ln + 1 + k, f"代码行 {len(raw)} 字符，手机上需横向滑动，建议 ≤{MAX_CODE_LINE}")
            esc = html.escape(raw).replace(" ", "&nbsp;")
            rendered.append(esc or "&nbsp;")
        label = ""
        if lang:
            label = (
                f'<p style="{style(margin="0", padding="12px 16px 0", font_family=MONO, font_size="11px", line_height="1.4", letter_spacing="1px", color=t["muted"], text_align="left")}">{html.escape(lang.lower())}</p>'
            )
        return (
            f'<section style="{style(margin="24px 0", background_color=t["code_bg"], border_radius=t["radius"], border="1px solid " + t["soft"])}">{label}'
            f'<pre style="{style(margin="0", padding="10px 16px 16px" if lang else "16px", overflow_x="auto", background="transparent")}">'
            f'<code style="{style(display="block", font_family=MONO, font_size="12.5px", line_height="1.75", color="#3A3F47", white_space="nowrap", background="transparent")}">'
            + "<br/>".join(rendered)
            + "</code></pre></section>"
        )

    def list_block(self, buf: list[str], ln: int) -> str:
        t = self.t
        items: list[list] = []  # [level, ordered, text_lines]
        base_indent = None
        for raw in buf:
            raw = raw.replace("\t", "    ")
            m = LIST_RE.match(raw)
            if m:
                indent = len(m.group(1))
                if base_indent is None:
                    base_indent = indent
                level = max(0, (indent - base_indent) // 2)
                items.append([min(level, 2), m.group(2)[0].isdigit(), [m.group(3)]])
            elif items:
                items[-1][2].append(raw.strip())

        counters = [0, 0, 0]
        ps = self.p_stack[-1]
        out = []
        w = "1.5em"
        for level, ordered, lines in items:
            counters[level] += 1
            for deeper in range(level + 1, 3):
                counters[deeper] = 0
            text = self.join_lines(lines)
            self.chars += count_chars(text)
            box = style(display="inline-block", width=w, text_indent="0", vertical_align="middle", line_height="1")
            if ordered:
                marker = (
                    f'<span style="{style(display="inline-block", width=w, text_indent="0", font_family=t["ol_font"], font_size="13px" if t["ol_font"] == MONO else None, line_height="1", font_weight="bold", color=t["ol_color"])}">'
                    f'{t["ol_fmt"].format(n=counters[level])}</span>'
                )
            elif level == 0:
                radius = "0" if t["bullet"] == "square" else "50%"
                marker = (
                    f'<span style="{box}"><span style="{style(display="inline-block", width="5px" if t["bullet"] == "square" else "6px", height="5px" if t["bullet"] == "square" else "6px", border_radius=radius, background_color=t["accent"], vertical_align="middle")}"></span></span>'
                )
            else:
                marker = (
                    f'<span style="{box}"><span style="{style(display="inline-block", width="5px", height="5px", border_radius="0" if t["bullet"] == "square" else "50%", border="1px solid " + t["accent"], vertical_align="middle")}"></span></span>'
                )
            pad = f"{1.5 + level * 1.5}em"
            p = self.p_style(margin="0 0 10px", padding_left=pad, text_indent=f"-{w}")
            out.append(f'<p style="{p}">{marker}{self.inline(text)}</p>')
        self.anchor()
        bottom = ps.get("margin", "0 0 20px").split()[-1] if ps else "20px"
        return f'<section style="{style(margin=f"4px 0 {bottom}")}">' + "".join(out) + "</section>"

    def table(self, head: str, sep: str, rows: list[str], ln: int) -> str:
        t = self.t
        self.anchor()

        def cells(r: str) -> list[str]:
            r = r.strip()
            if r.startswith("|"):
                r = r[1:]
            if r.endswith("|"):
                r = r[:-1]
            return [c.strip() for c in r.split("|")]

        heads = cells(head)
        aligns = []
        for c in cells(sep):
            if c.startswith(":") and c.endswith(":"):
                aligns.append("center")
            elif c.endswith(":"):
                aligns.append("right")
            else:
                aligns.append("left")
        if len(heads) > 3:
            self.warn(ln, f"表格 {len(heads)} 列，手机上会拥挤，建议 ≤3 列或改成列表")
        tint = t["table"] == "tint"
        th = "".join(
            f'<th style="{style(padding="9px 10px", background_color=t["soft"] if tint else None, color=t["heading"], font_weight="bold", text_align=aligns[k] if k < len(aligns) else "left", border_bottom="1px solid " + (t["mid"] if tint else t["heading"]), white_space="nowrap")}">{self.inline(h)}</th>'
            for k, h in enumerate(heads)
        )
        trs = []
        for r in rows:
            cs = cells(r)
            tds = "".join(
                f'<td style="{style(padding="9px 10px", color=t["text"], text_align=aligns[k] if k < len(aligns) else "left", border_bottom="1px solid " + t["rule"])}">{self.inline(c)}</td>'
                for k, c in enumerate(cs)
            )
            trs.append(f"<tr>{tds}</tr>")
        return (
            f'<section style="{style(margin="24px 0", overflow_x="auto")}">'
            f'<table style="{style(width="100%", border_collapse="collapse", font_size="13px", line_height="1.7", letter_spacing="0.3px")}">'
            f"<thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></section>"
        )

    # ── 扩展容器 ───────────────────────────────────────────────────────────
    def label(self, text: str, color: str, marker: str | None = None) -> str:
        m = square(marker, 6, "8px") if marker else ""
        return (
            f'<p style="{style(margin="0 0 8px", font_size="12px", font_weight="bold", line_height="1.4", letter_spacing="2px", color=color, text_align="left")}">{m}{html.escape(text)}</p>'
        )

    def container(self, typ: str, arg: str, buf: list[str], ln: int) -> str:
        t = self.t
        self.anchor()
        # 信号色主题（mono）的标签：黑字 + 橙色小方块；其它主题：主题色字
        sig = t["signal"] if t["signal"] != t["accent"] else None

        def inner(**ps) -> str:
            self.p_stack.append(ps)
            h = self.blocks(buf, ln)
            self.p_stack.pop()
            return h

        if typ == "lead":
            if t["lead"] == "dek":
                body = inner(font_size="16px", color=t["lead_color"], margin="0 0 8px", line_height="1.85", letter_spacing="0.3px")
                lab = self.label(arg, t["heading"], sig) if arg else ""
                return (
                    f'<section style="{style(margin="4px 0 36px", padding="0 0 24px", border_bottom="1px solid " + t["rule"])}">{lab}{body}</section>'
                )
            body = inner(font_size="14px", color=t["lead_color"], margin="0 0 6px", line_height="1.85")
            return (
                f'<section style="{style(margin="4px 0 36px", padding="18px 20px 12px", background_color=t["soft"], border_radius=t["radius"])}">'
                f"{self.label(arg, t['accent'], sig) if arg else ''}{body}</section>"
            )

        if typ == "quote":
            if t["quote"] == "serif":
                body = inner(font_family=t["head_font"], font_size="18px", color=t["heading"], margin="0 0 6px", line_height="1.75", letter_spacing="0.5px", text_align="left")
                author = ""
                if arg:
                    author = f'<p style="{style(margin="14px 0 0", font_size="13px", line_height="1.5", letter_spacing="1px", color=t["muted"], text_align="left")}">— {self.inline(arg)}</p>'
                bar = f'<hr style="{style(width="22px", margin="0 0 16px", height="0", border="0", border_top="2px solid " + t["accent"])}"/>'
                return f'<section style="{style(margin="44px 4px")}">{bar}{body}{author}</section>'
            if t["quote"] == "display":
                body = inner(font_size="20px", font_weight="bold", color=t["heading"], margin="0 0 6px", line_height="1.55", letter_spacing="0", text_align="left")
                author = ""
                if arg:
                    author = f'<p style="{style(margin="14px 0 0", font_size="13px", line_height="1.5", letter_spacing="0.5px", color=t["muted"], text_align="left")}">{square(t["signal"])}{self.inline(arg)}</p>'
                return (
                    f'<section style="{style(margin="44px 0", padding="2px 0 2px 18px", border_left="3px solid " + t["signal"])}">{body}{author}</section>'
                )
            body = inner(font_size="17px", color=t["heading"], margin="0 0 6px", line_height="1.8", letter_spacing="1px", text_align="center", font_weight="bold")
            author = ""
            if arg:
                author = f'<p style="{style(margin="12px 0 0", font_size="13px", line_height="1.5", letter_spacing="1px", color=t["muted"], text_align="center")}">—— {self.inline(arg)}</p>'
            return (
                f'<section style="{style(margin="44px 12px", text_align="center")}">'
                f'<p style="{style(margin="0 0 -10px", font_family=SERIF, font_size="44px", line_height="1", color=t["accent"], text_align="center", opacity="0.85")}">&ldquo;</p>'
                f"{body}{author}</section>"
            )

        if typ in ("tip", "note", "info", "warn", "warning", "danger"):
            is_warn = typ in ("warn", "warning", "danger")
            default = {"tip": "提示", "note": "要点", "info": "说明"}.get(typ, "注意")
            body = inner(font_size="14px", color=t["text"], margin="0 0 6px", line_height="1.85")
            if t["callout"] == "soft":
                bg = t["warn_bg"] if is_warn else t["soft"]
                color = t["warn"] if is_warn else (t["heading"] if sig else t["accent"])
                marker = (t["warn"] if is_warn else sig) if sig else None
                return (
                    f'<section style="{style(margin="24px 0", padding="16px 18px 10px", background_color=bg, border_radius=t["radius"])}">'
                    f"{self.label(arg or default, color, marker)}{body}</section>"
                )
            color = t["warn"] if is_warn else t["accent"]
            bg = t["warn_bg"] if is_warn else t["soft"]
            return (
                f'<section style="{style(margin="24px 0", padding="14px 16px 8px", background_color=bg, border_left="3px solid " + color, border_radius="0 4px 4px 0")}">'
                f"{self.label(arg or default, color)}{body}</section>"
            )

        if typ == "card":
            title = ""
            if arg:
                title = f'<p style="{style(margin="0 0 10px", font_family=t["head_font"], font_size="16px", font_weight="bold", line_height="1.6", color=t["heading"], letter_spacing="0.5px")}">{self.inline(arg)}</p>'
            body = inner(font_size="14px", margin="0 0 8px", line_height="1.85")
            border = t["rule"] if t["callout"] == "soft" else t["mid"]
            return (
                f'<section style="{style(margin="28px 0", padding="20px 20px 12px", border="1px solid " + border, border_radius=t["radius"])}">{title}{body}</section>'
            )
        if typ in ("qa", "interview"):
            # 访谈体：以“提问方：”开头的段落渲染为问题（色块标签 + 粗体），“某某：”开头的段落名字加粗
            return inner(_qa=arg or "问")
        if typ == "center":
            return inner(text_align="center", _breaks=True)
        if typ == "footer":
            body = inner(font_size="13px", color=t["muted"], text_align="center", margin="0 0 6px", line_height="1.8", _breaks=True)
            return (
                f'<section style="{style(margin="36px 0 0", padding="20px 0 0", border_top="1px solid " + t["rule"], text_align="center")}">{body}</section>'
            )
        # 未知容器：原样渲染内部
        return inner()

    # ── 收尾 ───────────────────────────────────────────────────────────────
    def end_matter(self) -> str:
        t = self.t
        out = []
        if str(self.meta.get("end", "true")).lower() != "false":
            out.append(
                f'<p style="{style(margin="56px 0 8px", font_size="12px", line_height="1", letter_spacing="6px", color=t["muted"], text_align="center")}">{html.escape(t["end"])}</p>'
            )
        if self.footnotes:
            items = "".join(
                f'<p style="{style(margin="0 0 6px", font_size="12px", line_height="1.7", color=t["muted"], text_align="left", word_break="break-all")}">'
                f'<span style="{style(color=t["signal"])}">[{k}]</span> '
                + ("" if label == url else f"{html.escape(label)}<br/>")
                + f'<span style="{style(color="#A0A0A0")}">{html.escape(url)}</span></p>'
                for k, (label, url) in enumerate(self.footnotes, 1)
            )
            out.append(
                f'<section style="{style(margin="32px 0 0", padding="16px 0 0", border_top="1px solid " + t["rule"])}">'
                f'<p style="{style(margin="0 0 10px", font_size="12px", font_weight="bold", letter_spacing="3px", color=t["muted"])}">参考资料</p>{items}</section>'
            )
        return "".join(out)


# ──────────────────────────────────────────────────────────────────────────────
# 入口
# ──────────────────────────────────────────────────────────────────────────────
def parse_front_matter(src: str) -> tuple[dict, str, int]:
    meta: dict = {}
    if src.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", src, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                        v = v[1:-1]
                    meta[k.strip().lower()] = v
            return meta, src[m.end():], m.group(0).count("\n") + 1
    return meta, src, 1


def strip_comments(body: str) -> str:
    """删掉 <!-- 注释 -->（论点卡、写作备注），保留换行，行号不变。"""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), body, flags=re.S)


# ──────────────────────────────────────────────────────────────────────────────
# 文风检查：套话 / AI 腔 / 模糊信源 / 感叹号（只查表面，观点质量靠 content-craft.md 自评）
# ──────────────────────────────────────────────────────────────────────────────
STYLE_RULES: list[tuple[str, str, str]] = [
    # (类别, 正则, 建议)
    ("空洞开头", r"随着.{1,16}的(?:发展|进步|普及|到来)|在当今(?:社会|时代|世界)?|众所周知|在这个.{1,12}的时代", "直接写事实或场景"),
    ("套话总结", r"总而言之|综上所述|总的来说|总之", "删掉，直接写结论"),
    ("虚假强调", r"值得(?:注意|一提|关注)的是|需要(?:指出|强调|注意)的是|不可否认|毋庸置疑|不言而喻", "删掉；重要的话不需要预告"),
    ("模糊对冲", r"(?:某种|一定)程度上|可以说|从某种意义上", "给出具体条件，或删掉"),
    ("空洞形容", r"(?:非常|极其|极为|十分)(?:重要|关键|显著|巨大)|意义(?:深远|重大)|至关重要", "换成数字或例子"),
    ("行话黑话", r"赋能|抓手|闭环|打通|底层逻辑|颗粒度|组合拳", "换成具体的动作或对象"),
    ("AI 腔", r"让我们(?:一起)?|不仅(?:仅)?是.{1,20}(?:更|而且)是|这不仅.{1,20}更|一场.{1,10}的(?:革命|变革)|开启.{1,8}新篇章|深刻(?:改变|影响)|无疑", "改成直接陈述"),
    ("排比凑数", r"首先.{0,200}其次|其次.{0,200}再次", "改成列表，或只保留真正并列的项"),
    ("模糊信源", r"有(?:研究|调查|数据|报告|统计)(?:表明|显示|发现|指出)|据统计|据悉|据了解|(?:有|一些|很多)?专家(?:认为|表示|指出)|业内人士|有关人士|有人(?:说|认为)", "写出具体的机构、人名、时间"),
    # 以下来自 references/human-voice.md：出现一次就值得改
    ("书面腔", r"悄然|彰显|诠释|璀璨|绽放|熠熠生辉|砥砺前行|扬帆起航", "换成口语里会说的词"),
    ("亲切腔", r"你是否也曾|你有没有过这样的(?:体验|经历|感觉)|相信(?:很多|不少|大家)|在这个快节奏|信息爆炸的时代", "换成一个真实、具体的场景"),
    ("拔高腔", r"值得[^，。！？]{0,8}深思|引人深思|发人深省|这也提醒(?:了)?我们|何尝不是|这或许就是.{1,10}的意义", "停在事实上，把判断留给读者"),
    ("收尾腔", r"希望(?:这篇|本文|以上).{0,8}(?:帮助|启发)|让我们拭目以待|未来可期|一起加油", "结尾停在具体画面、未解问题或下一步信号上"),
    ("设问自答", r"[？?]\s*(?:答案|原因|其实|很简单|因为|这是因为)", "直接说答案，删掉设问"),
    ("冒号揭晓", r"(?:真相|答案|关键|秘密|原因|本质)(?:只有一个|很简单|就是|在于)?[：:]", "删掉预告词，直接写内容"),
]
STYLE_RES = [(cat, re.compile(p), tip) for cat, p, tip in STYLE_RULES]
# 频率类：单用无妨，AI 的问题是每段都用。超过上限才提示
DENSITY_RULES: list[tuple[str, str, int]] = [
    ("“不是……而是……”句式", r"不是[^。！？\n]{1,24}[，,]\s*(?:而|就|更)?是", 2),
    ("揭晓词（本质 / 归根结底 / 说白了 / 换句话说 / 说到底）", r"本质上?|归根结底|说白了|换句话说|说到底", 2),
    ("“真正的”", r"真正的", 2),
    ("“更重要的是”", r"更重要的是", 1),
    ("“意味着”", r"意味着", 3),
]
DENSITY_RES = [(name, re.compile(p), n) for name, p, n in DENSITY_RULES]
MAX_DASH_PER_K = 3          # 每千字破折号上限
MIN_RHYTHM_SENTENCES = 20   # 句子数够多才判断节奏
MIN_RHYTHM_CV = 0.4         # 句长变异系数低于此值 = 句子长短过于均匀
EMPTY_HEADINGS = {"背景", "总结", "结语", "前言", "引言", "概述", "小结", "介绍", "简介", "结论"}
MAX_EXCLAIM = 2


def lint_style(body: str, offset: int, r: Renderer) -> None:
    fence = None
    hits: list[str] = []
    exclaim: list[int] = []
    density: dict[str, list[int]] = {}
    dashes: list[int] = []
    sent_lens: list[int] = []
    for i, line in enumerate(body.split("\n")):
        s = line.strip()
        m = re.match(r"^(```+|~~~+)", s)
        if m:
            fence = None if fence and s.startswith(fence) else (fence or m.group(1))
            continue
        if fence or not s or s.startswith(":::"):
            continue
        ln = offset + i
        text = re.sub(r"`[^`]*`|\]\([^)]*\)", "", s)
        h = re.match(r"^#{2,3}\s+(.*)$", text)
        if h and h.group(1).strip(" *#") in EMPTY_HEADINGS:
            hits.append(f"  L{ln:<4} [空标题] “{h.group(1).strip()}”没有信息量，写成短语或观点句")
        found: dict[str, list[str]] = {}
        for cat, rx, tip in STYLE_RES:
            for mm in rx.finditer(text):
                found.setdefault(f"{cat}|{tip}", []).append(mm.group(0) if len(mm.group(0)) <= 12 else mm.group(0)[:10] + "…")
        for key, words in found.items():
            cat, tip = key.split("|")
            hits.append(f"  L{ln:<4} [{cat}] “{'”“'.join(dict.fromkeys(words))}”→ {tip}")
        exclaim.extend([ln] * len(re.findall(r"[！!](?![\[(])", text)))
        if h:
            continue
        for name, rx, _ in DENSITY_RES:
            density.setdefault(name, []).extend([ln] * len(rx.findall(text)))
        dashes.extend([ln] * text.count("——"))
        prose = not (LIST_RE.match(text) or text.startswith(("|", ">", "!["))) and RE_CJK.search(text)
        if prose:
            plain = re.sub(r"[*=_~]", "", text)
            # 排比三连：连续 3 个分句用同样的两个字开头（“它是……，它是……，它是……”）
            clauses = [c.strip("“”\"' ") for c in re.split(r"[，。；！？、,;]", plain)]
            clauses = [c for c in clauses if count_chars(c) >= 4]
            for k in range(len(clauses) - 2):
                a = clauses[k][:2]
                if RE_CJK.match(a[:1]) and clauses[k + 1].startswith(a) and clauses[k + 2].startswith(a):
                    hits.append(f"  L{ln:<4} [排比三连] 连续以“{a}”开头 → 挑最有力的一项，其余删掉")
                    break
            for s in re.split(r"[。！？!?]+", plain):
                c = count_chars(s)
                if c >= 2:
                    sent_lens.append(c)
    if len(exclaim) > MAX_EXCLAIM:
        hits.append(f"  L{exclaim[0]:<4} [感叹号] 全文 {len(exclaim)} 处（L{', L'.join(map(str, dict.fromkeys(exclaim)))}），建议 ≤{MAX_EXCLAIM}，让事实本身有力量")
    for name, rx, limit in DENSITY_RES:
        lines = density.get(name, [])
        if len(lines) > limit:
            hits.append(f"  L{lines[0]:<4} [AI 味·频率] {name} 全文 {len(lines)} 次（L{', L'.join(map(str, dict.fromkeys(lines)))}），建议 ≤{limit}")
    total = max(1, sum(sent_lens))
    if len(dashes) * 1000 / total > MAX_DASH_PER_K and len(dashes) > 2:
        hits.append(f"  L{dashes[0]:<4} [破折号] 全文 {len(dashes)} 处，约每千字 {len(dashes) * 1000 // total} 处，建议 ≤{MAX_DASH_PER_K}")
    if len(sent_lens) >= MIN_RHYTHM_SENTENCES:
        mean = sum(sent_lens) / len(sent_lens)
        cv = (sum((x - mean) ** 2 for x in sent_lens) / len(sent_lens)) ** 0.5 / mean
        short = sum(1 for x in sent_lens if x <= 8)
        if cv < MIN_RHYTHM_CV:
            hits.append(f"  META  [节奏] {len(sent_lens)} 句平均 {mean:.0f} 字，长短差异很小（变异系数 {cv:.2f}，建议 ≥{MIN_RHYTHM_CV}）→ 穿插几个短句，让重要的地方停一下")
        elif short == 0:
            hits.append(f"  META  [节奏] 全文没有 ≤8 字的短句 → 在需要停顿的地方用一两个短句")
    r.warnings.extend(hits)




def render(src: str, theme_name: str | None = None) -> tuple[str, Renderer, dict]:
    meta, body, offset = parse_front_matter(src.replace("\r\n", "\n"))
    body = strip_comments(body)
    name = theme_name or meta.get("theme") or DEFAULT_THEME
    if name not in THEMES:
        raise SystemExit(f"未知主题 {name!r}，可选：{', '.join(THEMES)}")
    t = resolve_theme(name)
    if meta.get("h2") in ("index", "big", "seal", "numeral", "editorial"):
        t["h2"] = meta["h2"]   # 单篇文章覆盖章节样式
    r = Renderer(t, meta)
    inner = r.blocks(body.split("\n"), offset)
    inner += r.end_matter()
    if meta.get("byline"):
        # 署名：文丨某某　编辑丨某某（晚点 / 人物 / 三联的惯例，放在正文最上方）
        by = re.sub(r"\s*[|｜]\s*", "丨", meta["byline"])
        by = re.sub(r"\s{2,}|　", "\x03", by)
        cells = "".join(
            f'<span style="{style(display="inline-block", margin_right="16px")}">{r.inline(c.strip())}</span>'
            for c in by.split("\x03") if c.strip()
        )
        inner = (
            f'<p style="{style(margin="0 0 28px", font_size="13px", line_height="1.8", letter_spacing="1px", color=t["muted"], text_align="left")}">{cells}</p>'
            + inner
        )
    paper = str(meta.get("paper", "false")).lower() == "true"
    root = style(
        margin="0",
        padding="28px 18px" if paper else "0 4px",
        background_color=t["paper"] if paper else None,
        border_radius="12px" if paper else None,
        font_family=FONT,
        font_size=r.fs,
        color=t["text"],
        line_height=r.lh,
        letter_spacing="0.5px",
        word_wrap="break-word",
        text_align="justify",
    )
    return f'<section style="{root}">{inner}</section>', r, meta


def lint_output(frag: str, r: Renderer) -> None:
    """自检生成的 HTML：行高不能小于字号，否则公众号粘贴时报“行高异常 / 文字重叠”。"""
    bad = 0
    for st in re.findall(r'style="([^"]*)"', frag):
        lh = re.search(r"(?:^|;)line-height:([\d.]+)(em|px)?", st)
        if not lh:
            continue
        fs = re.search(r"(?:^|;)font-size:([\d.]+)px", st)
        v, unit = float(lh.group(1)), lh.group(2)
        size = float(fs.group(1)) if fs else None
        if size == 0:
            continue
        px = v if unit == "px" else (v * size if size else None)
        if v == 0 or unit is None or (px is not None and size and px < size):
            bad += 1
    if bad:
        r.warnings.append(f"  HTML  {bad} 处行高小于字号或未写单位，粘贴进公众号会报“行高异常”（脚本问题，请修 md2wechat.py）")


def lint_meta(meta: dict, r: Renderer) -> None:
    title = meta.get("title", "")
    # 栏目前缀（“晚点对话丨”“APPSO 独家｜”）不计入主体长度，但整体仍不宜超过 40 字
    main = re.split(r"[丨｜|]", title, maxsplit=1)[-1] if re.search(r"[丨｜|]", title) else title
    if title and count_chars(main) > MAX_TITLE_CHARS:
        r.warnings.insert(0, f"  META  标题主体 {count_chars(main)} 字，订阅号列表会被截断，建议 ≤{MAX_TITLE_CHARS} 字")
    elif title and count_chars(title) > 40:
        r.warnings.insert(0, f"  META  标题含栏目前缀共 {count_chars(title)} 字，建议 ≤40 字")
    summary = meta.get("summary", "")
    if not summary:
        r.warnings.insert(0, "  META  缺少 summary（摘要），分享卡片会自动截取正文开头")
    elif len(summary) > MAX_SUMMARY_CHARS:
        r.warnings.insert(0, f"  META  摘要 {len(summary)} 字，超过公众号 {MAX_SUMMARY_CHARS} 字上限")


PREVIEW_TMPL = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 公众号预览</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;background:#E9E7E3;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333}
  .bar{position:sticky;top:0;z-index:9;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;padding:10px 12px;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid #ddd;font-size:13px}
  .bar button{border:1px solid #ccc;background:#fff;border-radius:16px;padding:5px 14px;font-size:13px;cursor:pointer}
  .bar button.on{border-color:var(--c);color:#fff;background:var(--c)}
  .bar .copy{background:#07C160;border-color:#07C160;color:#fff;font-weight:600}
  .bar .stat{color:#888}
  .phone{width:390px;max-width:100%;margin:24px auto 60px;background:#fff;border-radius:28px;box-shadow:0 12px 40px rgba(0,0,0,.12);overflow:hidden}
  @media (max-width:430px){.phone{margin:0;border-radius:0;box-shadow:none}}
  .head{padding:28px 20px 0}
  .head h1{margin:0 0 14px;font-size:22px;line-height:1.4;font-weight:700;color:#191919;letter-spacing:.5px}
  .head .by{font-size:15px;color:#576B95;margin-bottom:22px}
  .head .by span{color:#999;margin-left:10px}
  .body{padding:0 16px 40px}
  .wx-article{display:none}.wx-article.on{display:block}
  .toast{position:fixed;left:50%;top:40%;transform:translate(-50%,-50%);background:rgba(0,0,0,.78);color:#fff;padding:12px 22px;border-radius:8px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none}
  .toast.show{opacity:1}
  .warn{max-width:390px;margin:-40px auto 60px;font-size:12px;color:#8a6d3b;background:#fcf8e3;border:1px solid #faebcc;border-radius:8px;padding:10px 14px;white-space:pre-wrap;line-height:1.7}
</style></head>
<body>
<div class="bar">__BUTTONS__<button class="copy" onclick="copyArticle()">复制到公众号</button><span class="stat">__STAT__</span></div>
<div class="phone"><div class="head"><h1>__TITLE__</h1><div class="by">__AUTHOR__<span>__DATE__</span></div></div>
<div class="body">__ARTICLES__</div></div>
__WARN__
<div class="toast" id="toast">已复制，去公众号编辑器粘贴即可</div>
<script>
function pick(name){document.querySelectorAll('.wx-article').forEach(e=>e.classList.toggle('on',e.dataset.theme===name));
document.querySelectorAll('.bar button[data-theme]').forEach(b=>b.classList.toggle('on',b.dataset.theme===name));}
async function copyArticle(){
  const el=document.querySelector('.wx-article.on'); const html=el.innerHTML;
  try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([html],{type:'text/html'}),'text/plain':new Blob([el.innerText],{type:'text/plain'})})]);}
  catch(e){const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy');s.removeAllRanges();}
  const t=document.getElementById('toast');t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1600);
}
pick('__DEFAULT__');
</script>
</body></html>
"""


def build_preview(src: str, default_theme: str, meta: dict, r: Renderer) -> str:
    articles, buttons = [], []
    for name, th in THEMES.items():
        frag, _, _ = render(src, name)
        articles.append(f'<div class="wx-article" data-theme="{name}">{frag}</div>')
        dot = (
            f'<span style="display:inline-block;width:6px;height:6px;background:{th["signal"]};margin-left:6px;vertical-align:middle"></span>'
            if th.get("signal") else ""
        )
        buttons.append(
            f'<button data-theme="{name}" style="--c:{th["accent"]}" onclick="pick(\'{name}\')">{th["label"]}{dot}</button>'
        )
    minutes = max(1, round(r.chars / READ_SPEED))
    warn = ""
    if r.warnings:
        warn = '<div class="warn">可读性提示（不会进入正文）：\n' + html.escape("\n".join(r.warnings)) + "</div>"
    return (
        PREVIEW_TMPL.replace("__TITLE__", smart_quotes(html.escape(meta.get("title", "未命名文章"), quote=False)))
        .replace("__AUTHOR__", html.escape(meta.get("author", "作者")))
        .replace("__DATE__", html.escape(meta.get("date", "")))
        .replace("__BUTTONS__", "".join(buttons))
        .replace("__STAT__", f"约 {r.chars} 字 · {minutes} 分钟 · {r.images} 图")
        .replace("__ARTICLES__", "".join(articles))
        .replace("__WARN__", warn)
        .replace("__DEFAULT__", default_theme)
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Markdown → 微信公众号排版 HTML（移动端优先）")
    ap.add_argument("input", nargs="?", help="Markdown 文件")
    ap.add_argument("-o", "--output", help="输出路径，默认与输入同名 .html")
    ap.add_argument("-t", "--theme", choices=list(THEMES), help="主题（覆盖 front matter）")
    ap.add_argument("--fragment", action="store_true", help="只输出可粘贴的 HTML 片段，不含预览外壳")
    ap.add_argument("--check", action="store_true", help="只做可读性检查，不写文件")
    ap.add_argument("--no-style", action="store_true", help="跳过文风检查（套话 / 模糊信源 / 感叹号），只查排版")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出统计与警告")
    ap.add_argument("--list-themes", action="store_true", help="列出主题")
    a = ap.parse_args(argv)

    if a.list_themes:
        for k, v in THEMES.items():
            mark = " (默认)" if k == DEFAULT_THEME else ""
            print(f"{k:<9} {v['label']}{mark}  {v.get('signal') or v['accent']}  {v['desc']}")
        return 0
    if not a.input:
        ap.error("需要输入 Markdown 文件")

    src = Path(a.input).read_text(encoding="utf-8")
    frag, r, meta = render(src, a.theme)
    lint_meta(meta, r)
    lint_output(frag, r)
    if str(meta.get("lint", "true")).lower() != "layout" and not a.no_style:
        _, body, offset = parse_front_matter(src.replace("\r\n", "\n"))
        lint_style(strip_comments(body), offset, r)
    theme = a.theme or meta.get("theme") or DEFAULT_THEME
    minutes = max(1, round(r.chars / READ_SPEED))

    if a.json:
        print(json.dumps({"theme": theme, "chars": r.chars, "minutes": minutes, "images": r.images,
                          "sections": r.h2_index, "footnotes": len(r.footnotes), "warnings": r.warnings},
                         ensure_ascii=False, indent=2))
    else:
        print(f"✓ 主题 {theme}（{THEMES[theme]['label']}） · 约 {r.chars} 字 · 阅读 {minutes} 分钟 · "
              f"{r.h2_index} 个章节 · {r.images} 张图 · {len(r.footnotes)} 条脚注", file=sys.stderr)
        if r.warnings:
            print(f"⚠ 可读性提示 {len(r.warnings)} 条：", file=sys.stderr)
            print("\n".join(r.warnings), file=sys.stderr)
        else:
            print("✓ 可读性检查通过", file=sys.stderr)

    if a.check:
        return 0
    out = Path(a.output) if a.output else Path(a.input).with_suffix(".html")
    content = frag if a.fragment else build_preview(src, theme, meta, r)
    out.write_text(content, encoding="utf-8")
    print(f"→ {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
