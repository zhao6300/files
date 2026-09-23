# -*- coding: utf-8 -*-
"""封面 + Part 1 为什么需要 SLO + Part 2 核心指标"""
from deckkit import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 01 封面
def cover(prs, n):
    s = blank(prs)
    rect(s, 0, 0, SW, SH, WHITE)
    rect(s, 8.72, 0, SW - 8.72, SH, PANEL)
    rect(s, 8.72, 0, 0.02, SH, LINE)

    # 左侧
    txt(s, ML, 0.86, 5.0, 0.26, "技术分享  ·  推理系统性能优化", 11.5, True, BLUE, line=1.0)
    rect(s, ML, 2.18, 0.62, 0.05, INK)
    txt(s, ML, 2.52, 7.6, 1.8, "大模型推理服务的\nSLO 与 Goodput", 42, True, INK, line=1.12)
    txt(s, ML, 4.32, 7.3, 0.9,
        "从「跑得更快」到「稳定达标」\n我们衡量什么、为什么会违约、我们有哪些控制手段",
        15, False, MUTED, line=1.5)

    px = ML
    for label, sub, fill, fc in (("TTFT", "首字延迟", BLUE_L, BLUE),
                                 ("TPOT", "每字延迟", TEAL_L, TEAL),
                                 ("Goodput", "有效吞吐", AMBER_L, AMBER)):
        w = 2.05
        sh = card(s, px, 5.55, w, 0.78, fill, None, radius=0.14)
        box_text(sh, [(label, 15, True, fc), (sub, 10.5, False, BODY)])
        px += w + 0.22

    txt(s, ML, 6.72, 7.0, 0.3, "汇报人：＿＿＿      日期：2026 / 09", 11, False, FAINT, line=1.0)

    # 右侧小图：两个延迟指标 → 达标率 → Goodput
    cx0, cw = 9.05, 1.82
    a = card(s, cx0, 1.62, cw, 0.72, WHITE, LINE, radius=0.12)
    box_text(a, [("TTFT", 13, True, BLUE), ("第一个字多久出来", 9, False, MUTED)])
    b = card(s, cx0 + cw + 0.2, 1.62, cw, 0.72, WHITE, LINE, radius=0.12)
    box_text(b, [("TPOT", 13, True, TEAL), ("后续每个字多快", 9, False, MUTED)])

    arrow(s, cx0 + cw / 2, 2.34, cx0 + cw / 2 + 0.45, 2.92, FAINT, 1.25)
    arrow(s, cx0 + cw + 0.2 + cw / 2, 2.34, cx0 + cw + 0.2 + cw / 2 - 0.45, 2.92, FAINT, 1.25)

    c = card(s, cx0, 2.98, cw * 2 + 0.2, 0.72, WHITE, LINE, radius=0.12)
    box_text(c, [("SLO 达标率", 13, True, INK), ("多少比例的请求满足体验要求", 9, False, MUTED)])
    arrow(s, cx0 + cw + 0.1, 3.7, cx0 + cw + 0.1, 4.18, FAINT, 1.25)

    d = card(s, cx0, 4.24, cw * 2 + 0.2, 0.92, BLUE, None, radius=0.12)
    box_text(d, [("Goodput", 17, True, WHITE), ("达标前提下能承载的请求量", 9.5, False, "DCE6FD")])
    txt(s, cx0, 5.32, cw * 2 + 0.2, 0.3, "系统优化的最终目标", 10.5, True, MUTED, "c", line=1.0)
    return n


# ============================================================ 02 一分钟摘要
def summary(prs, n):
    s = blank(prs)
    header(s, "写在最前面", "一页话讲清这次分享的三个观点",
           "如果只记住三句话，就记这三句")
    cards = [
        ("01", "用户体验是可以被量化的", BLUE, BLUE_L,
         "用户对「快」的感受只有两件事：\n第一个字等多久（TTFT）、\n后面的字出得稳不稳（TPOT）。",
         "→ 它们对应两个完全不同的计算阶段，优化手段也完全不同。"),
        ("02", "平均值不重要，达标率才重要", TEAL, TEAL_L,
         "平均延迟好看，不代表用户不投诉。\n真正要看的是：有多少比例的\n请求越过了红线。",
         "→ 我们关注 p90 / p95 长尾，以及分场景的达标率。"),
        ("03", "最终目标是 Goodput", AMBER, AMBER_L,
         "在「体验达标」的前提下，\n同样的 GPU 最多能接多少请求，\n这才是真实产能。",
         "→ 吞吐做到最高，Goodput 反而可能下降。"),
    ]
    x = ML
    w = (CW - 0.44) / 3
    for num, title, ac, al, body, foot in cards:
        card(s, x, 2.0, w, 3.9, WHITE, LINE, radius=0.06)
        rect(s, x, 2.0, w, 0.055, ac)
        txt(s, x + 0.34, 2.32, 1.0, 0.44, num, 26, True, al, line=1.0)
        txt(s, x + 0.34, 2.92, w - 0.68, 0.5, title, 16, True, INK, line=1.2)
        hline(s, x + 0.34, 3.58, w - 0.68)
        txt(s, x + 0.34, 3.76, w - 0.68, 1.3, body, 12.5, False, BODY, line=1.6)
        card(s, x + 0.34, 5.1, w - 0.68, 0.62, al, None, radius=0.1)
        txt(s, x + 0.5, 5.18, w - 1.0, 0.5, foot, 11, True, ac, line=1.3)
        x += w + 0.22

    takeaway(s, 6.16,
             "我们做的每一项底层优化（PD 部署、Chunk 大小、KV Cache、通信），最终都会汇聚成这一个数字。",
             INK, PANEL, icon="一句话")
    page_no(s, n)
    return n


# ============================================================ 03 路线图
def roadmap(prs, n):
    s = blank(prs)
    header(s, "内容框架", "这份材料的六个部分", "沿着一条主线：从目标 → 指标 → 成因 → 手段 → 系统级权衡")
    items = [
        ("1", "为什么需要 SLO", "推理系统到底在优化什么？", BLUE),
        ("2", "核心指标", "TTFT / TPOT / Goodput 怎么定义？", BLUE),
        ("3", "TTFT 由什么决定", "为什么第一个字会等很久？", TEAL),
        ("4", "TPOT 由什么决定", "为什么生成会卡顿？", TEAL),
        ("5", "有哪些控制手段", "系统上有哪些「旋钮」？", AMBER),
        ("6", "系统级优化", "为什么最终要优化 Goodput？", AMBER),
    ]
    w = (CW - 0.44) / 3
    h = 1.72
    for i, (num, title, q, ac) in enumerate(items):
        x = ML + (i % 3) * (w + 0.22)
        y = 2.1 + (i // 3) * (h + 0.3)
        card(s, x, y, w, h, WHITE, LINE, radius=0.07)
        rect(s, x, y, 0.05, h, ac)
        sh = shape(s, MSO_SHAPE.OVAL, x + 0.3, y + 0.3, 0.42, 0.42, ac, None)
        box_text(sh, [(num, 13, True, WHITE)])
        txt(s, x + 0.88, y + 0.34, w - 1.2, 0.36, title, 15.5, True, INK, line=1.1)
        txt(s, x + 0.3, y + 1.02, w - 0.6, 0.5, q, 12, False, MUTED, line=1.35)

    takeaway(s, 6.12, "前 4 部分建立共识：指标是什么、问题从哪来；后 2 部分说明：我们在做什么、为什么这样做。",
             BLUE, BLUE_L, icon="阅读方式")
    page_no(s, n)
    return n


# ============================================================ 05 从性能到 SLO
def why_slo(prs, n):
    s = blank(prs)
    header(s, "PART 1 · 为什么需要 SLO", "指标的视角，要从「机器」换到「用户」")
    lw = (CW - 1.1) / 2

    card(s, ML, 2.0, lw, 3.5, PANEL, None, radius=0.06)
    txt(s, ML + 0.34, 2.28, lw - 0.68, 0.3, "过去常看的「性能指标」", 15, True, MUTED, line=1.0)
    hline(s, ML + 0.34, 2.7, lw - 0.68, FAINT)
    for i, (k, v) in enumerate([("吞吐 Throughput", "每秒能处理多少 token"),
                                ("延迟 Latency", "平均响应多快"),
                                ("GPU 利用率", "卡有没有闲着"),
                                ("Tokens / s", "峰值跑分能到多少")]):
        y = 2.9 + i * 0.6
        rect(s, ML + 0.34, y + 0.1, 0.16, 0.16, FAINT)
        txt(s, ML + 0.62, y + 0.02, lw - 1.0, 0.3, k, 13.5, True, BODY, line=1.0)
        txt(s, ML + 0.62, y + 0.28, lw - 1.0, 0.26, v, 11, False, MUTED, line=1.0)
    txt(s, ML + 0.34, 5.08, lw - 0.68, 0.3, "特点：描述机器有多强", 11.5, True, MUTED, line=1.0)

    mx = ML + lw + 0.12
    arrow(s, mx + 0.1, 3.7, mx + 0.78, 3.7, BLUE, 2.0, size="lg")
    txt(s, mx - 0.06, 3.22, 1.0, 0.3, "换视角", 11, True, BLUE, "c", line=1.0)

    rx = ML + lw + 1.1
    card(s, rx, 2.0, lw, 3.5, WHITE, BLUE, 1.25, radius=0.06)
    rect(s, rx, 2.0, lw, 0.055, BLUE)
    txt(s, rx + 0.34, 2.28, lw - 0.68, 0.3, "线上服务真正关心的问题", 15, True, INK, line=1.0)
    hline(s, rx + 0.34, 2.7, lw - 0.68, LINE)
    txt(s, rx + 0.34, 2.9, lw - 0.68, 0.8,
        "在用户体验不被破坏的前提下，\n这套系统最多能承载多少请求？",
        16, True, BLUE, line=1.45)
    hline(s, rx + 0.34, 3.88, lw - 0.68, LINE)
    for i, (k, v) in enumerate([("SLO", "把体验写成可检查的目标（如首字 ≤ 2 秒）"),
                                ("SLO 达标率", "实际有多少比例的请求达到了目标"),
                                ("Goodput", "达标请求的吞吐，也就是真实产能")]):
        y = 3.98 + i * 0.44
        txt(s, rx + 0.34, y, 1.3, 0.28, k, 12.5, True, INK, line=1.0)
        txt(s, rx + 1.5, y, lw - 1.9, 0.28, v, 11.5, False, BODY, line=1.0)
    txt(s, rx + 0.34, 5.14, lw - 0.68, 0.3, "特点：描述用户是否满意", 11.5, True, BLUE, line=1.0)

    takeaway(s, 5.86, "吞吐再高，如果用户等不起，就不能算作有效产能；所以优化目标要从 Performance 转向 SLO。",
             BLUE, BLUE_L)
    page_no(s, n)
    return n


# ============================================================ 06 餐厅比喻
def analogy(prs, n):
    s = blank(prs)
    header(s, "PART 1 · 建立直觉", "用一家餐厅来理解推理服务",
           "后面所有术语，都可以对应到这张图上的某个环节")
    steps = [
        ("客人进门排队", "请求排队等待", "Queue", BLUE),
        ("服务员看菜单点单", "读取并理解整个提问", "Prefill", VIO),
        ("第一道菜上桌", "第一个字出现 → TTFT", "TTFT", TEAL),
        ("后面的菜陆续上", "逐字生成 → TPOT", "Decode", AMBER),
        ("今天接待了多少满意客人", "达标的请求数\n→ Goodput", "Goodput", INK),
    ]
    w = (CW - 4 * 0.26) / 5
    for i, (top, bottom, tag, ac) in enumerate(steps):
        x = ML + i * (w + 0.26)
        card(s, x, 2.08, w, 1.36, WHITE, LINE, radius=0.08)
        rect(s, x, 2.08, w, 0.05, ac)
        txt(s, x + 0.18, 2.36, w - 0.36, 0.3, "第 %d 步" % (i + 1), 10, True, FAINT, line=1.0)
        txt(s, x + 0.18, 2.66, w - 0.36, 0.6, top, 13.5, True, INK, line=1.3)
        tri_down(s, x + w / 2, 3.56, 0.22, 0.15, FAINT)
        card(s, x, 3.82, w, 1.3, PANEL, None, radius=0.08)
        txt(s, x + 0.18, 4.0, w - 0.36, 0.56, bottom, 12.5, True, BODY, line=1.3)
        pill(s, x + 0.18, 4.62, min(w - 0.36, 1.35), 0.32, tag, 10, True, WHITE, ac, ac, 1.0)
        if i < 4:
            arrow(s, x + w + 0.03, 2.76, x + w + 0.23, 2.76, FAINT, 1.25, size="sm")

    card(s, ML, 5.34, CW, 0.66, PANEL, None, radius=0.1)
    tb, tf = textbox(s, ML + 0.3, 5.34, CW - 0.6, 0.66, "m")
    rich(tf, [("关键区别  ｜  ", {"bold": True, "color": MUTED, "size": 12}),
              ("「等第一道菜」和「后面上菜快不快」", {"bold": True, "color": INK, "size": 13.5}),
              ("  是两种完全不同的体验问题，餐厅里的解法也不同（增加点单人手 / 增加后厨出菜速度）。",
               {"color": BODY, "size": 13})], first=True, line=1.25)

    takeaway(s, 6.16, "推理系统之所以有两个指标，是因为一次请求里真的存在两个性质完全不同的阶段。",
             TEAL, TEAL_L)
    page_no(s, n)
    return n


# ============================================================ 08 SLA / SLO / SLI
def sla_slo_sli(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 术语对齐", "SLA / SLO / SLI：先把话说到同一个频道上")
    defs = [
        ("SLA", "Service Level Agreement", "服务等级协议", "对外承诺：做不到要负责", BLUE),
        ("SLO", "Service Level Objective", "服务等级目标", "对内目标：系统要达到的数值", TEAL),
        ("SLI", "Service Level Indicator", "服务等级指标", "实际测量：现在到底是多少", AMBER),
    ]
    w = (CW - 0.44) / 3
    for i, (k, en, cn, desc, ac) in enumerate(defs):
        x = ML + i * (w + 0.22)
        card(s, x, 2.0, w, 1.72, WHITE, LINE, radius=0.07)
        rect(s, x, 2.0, 0.05, 1.72, ac)
        txt(s, x + 0.3, 2.22, w - 0.6, 0.4, k, 22, True, ac, line=1.0)
        txt(s, x + 0.3, 2.68, w - 0.6, 0.26, en, 10, False, FAINT, line=1.0)
        txt(s, x + 0.3, 3.0, w - 0.6, 0.3, cn, 14, True, INK, line=1.0)
        txt(s, x + 0.3, 3.32, w - 0.6, 0.28, desc, 11.5, False, BODY, line=1.0)
        if i < 2:
            arrow(s, x + w + 0.03, 2.86, x + w + 0.19, 2.86, FAINT, 1.25, size="sm")

    txt(s, ML, 4.0, CW, 0.3, "一个具体例子", 13, True, MUTED, line=1.0)
    hline(s, ML, 4.34, CW)
    rows = [
        ("层级", "内容", "谁来看"),
        ("SLA", "99% 的请求必须在承诺的响应时间内完成", "客户 / 业务方"),
        ("SLO", "TTFT ≤ 2s（首字）；TPOT ≤ 100ms（后续每字）", "我们自己定的工程目标"),
        ("SLI", "实测 TTFT / TPOT 的 p50、p90、p95，以及 SLO 达标率", "监控与优化的依据"),
    ]
    grid_table(s, ML, 4.5, CW, [0.9, 5.4, 3.0], rows, row_h=0.5, head_h=0.46,
               align=["c", "l", "l"])

    takeaway(s, 6.36, "SLA 是承诺，SLO 是目标，SLI 是事实；我们的工作是让 SLI 稳定落在 SLO 之内。",
             BLUE, BLUE_L, h=0.58)
    page_no(s, n)
    return n


# ============================================================ 09 两个阶段
def two_phases(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 机制", "一次请求天然分成两段，所以天然有两个 SLO")

    # Prefill 阶段
    card(s, ML, 2.05, 4.55, 2.5, WHITE, VIO, 1.25, radius=0.07)
    rect(s, ML, 2.05, 4.55, 0.055, VIO)
    pill(s, ML + 0.3, 2.28, 1.5, 0.34, "Prefill 阶段", 11, True, VIO_L, VIO)
    txt(s, ML + 0.3, 2.78, 3.95, 0.34, "把整段提问一次性读完", 16, True, INK, line=1.1)
    for i, t in enumerate(["一次处理全部输入内容，计算量集中",
                           "吃 GPU 算力（计算密集型）",
                           "过程中产生 KV Cache（后续生成要用的记忆）",
                           "目标：尽快吐出第一个字"]):
        y = 3.26 + i * 0.3
        rect(s, ML + 0.32, y + 0.08, 0.1, 0.1, VIO)
        txt(s, ML + 0.54, y, 3.75, 0.28, t, 11.5, False, BODY, line=1.0)

    # 中间：首 token
    arrow(s, ML + 4.6, 3.3, ML + 5.32, 3.3, INK, 1.75)
    sh = card(s, ML + 5.4, 2.82, 1.55, 0.95, INK, None, radius=0.12)
    box_text(sh, [("第一个字", 13, True, WHITE), ("First Token", 9, False, "B9C2D6")])
    arrow(s, ML + 7.03, 3.3, ML + 7.75, 3.3, INK, 1.75)

    # Decode 阶段
    dx = ML + 7.83
    card(s, dx, 2.05, CW - 7.83, 2.5, WHITE, AMBER, 1.25, radius=0.07)
    rect(s, dx, 2.05, CW - 7.83, 0.055, AMBER)
    pill(s, dx + 0.3, 2.28, 1.5, 0.34, "Decode 阶段", 11, True, AMBER_L, AMBER)
    txt(s, dx + 0.3, 2.78, 3.9, 0.34, "一个字一个字往外写", 16, True, INK, line=1.1)
    for i, t in enumerate(["自回归：每一步只生成一个 token",
                           "反复读取 KV Cache（吃显存带宽）",
                           "单步计算量小，但步数多",
                           "目标：稳定、连续地出字"]):
        y = 3.26 + i * 0.3
        rect(s, dx + 0.32, y + 0.08, 0.1, 0.1, AMBER)
        txt(s, dx + 0.54, y, CW - 8.5, 0.28, t, 11.5, False, BODY, line=1.0)

    # 指标归属
    card(s, ML, 4.76, 4.55, 0.72, VIO_L, None, radius=0.1)
    tb, tf = textbox(s, ML + 0.3, 4.76, 4.0, 0.72, "m")
    rich(tf, [("对应指标：", {"color": BODY, "size": 12}),
              ("TTFT", {"bold": True, "color": VIO, "size": 16}),
              ("（首字延迟）", {"color": BODY, "size": 12})], first=True, line=1.1)
    card(s, dx, 4.76, CW - 7.83, 0.72, AMBER_L, None, radius=0.1)
    tb, tf = textbox(s, dx + 0.3, 4.76, 4.0, 0.72, "m")
    rich(tf, [("对应指标：", {"color": BODY, "size": 12}),
              ("TPOT", {"bold": True, "color": AMBER, "size": 16}),
              ("（每字延迟）", {"color": BODY, "size": 12})], first=True, line=1.1)

    card(s, ML, 5.66, CW, 0.56, PANEL, None, radius=0.1)
    txt(s, ML + 0.3, 5.66, CW - 0.6, 0.56,
        "白话版：Prefill 像「读题」，算力越强读得越快；Decode 像「手写答案」，写得快不快更取决于翻阅笔记（显存带宽）的速度。",
        12.5, False, BODY, line=1.1)
    tb = s.shapes[-1]

    takeaway(s, 6.34, "两个阶段的瓶颈不同（算力 vs 带宽），所以优化 TTFT 的手段，往往会伤害 TPOT。",
             TEAL, TEAL_L, h=0.58)
    page_no(s, n)
    return n


# ============================================================ 10 TTFT
def ttft(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 指标定义", "TTFT：用户从提问到看到第一个字的等待时间",
           "Time To First Token —— 决定「这个系统反应快不快」的第一印象")

    stages = [("排队等待", "Queue", "前面还有别的请求", BLUE),
              ("调度决策", "Schedule", "什么时候被挑中执行", BLUE),
              ("读取 KV", "KV Retrieval", "命中的缓存要搬进显存", VIO),
              ("Prefill 计算", "Prefill", "真正的模型计算", VIO),
              ("结果传输", "Transfer", "跨实例/跨卡的数据搬运", TEAL)]
    w = (CW - 4 * 0.2) / 5
    for i, (cn, en, desc, ac) in enumerate(stages):
        x = ML + i * (w + 0.2)
        card(s, x, 2.18, w, 1.28, WHITE, LINE, radius=0.08)
        rect(s, x, 2.18, w, 0.05, ac)
        txt(s, x + 0.16, 2.42, w - 0.32, 0.3, cn, 14, True, INK, line=1.0)
        txt(s, x + 0.16, 2.74, w - 0.32, 0.24, en, 9.5, False, FAINT, line=1.0)
        txt(s, x + 0.16, 3.02, w - 0.32, 0.36, desc, 11, False, BODY, line=1.15)
        if i < 4:
            txt(s, x + w, 2.62, 0.2, 0.3, "+", 15, True, FAINT, "c", line=1.0)

    txt(s, ML, 1.9, 3.0, 0.24, "请求到达", 10, True, FAINT, line=1.0)
    txt(s, SW - ML - 3.0, 1.9, 3.0, 0.24, "第一个字出现", 10, True, FAINT, "r", line=1.0)

    formula(s, ML, 3.66, CW, 0.66,
            "TTFT  =  排队  +  调度  +  KV 读取  +  Prefill 计算  +  数据传输",
            PANEL, INK, 16)

    lw = (CW - 0.26) / 2
    card(s, ML, 4.54, lw, 1.4, RED_L, None, radius=0.08)
    txt(s, ML + 0.3, 4.76, lw - 0.6, 0.34, "最容易误解的一点", 12, True, RED, line=1.0)
    txt(s, ML + 0.3, 5.14, lw - 0.6, 0.6, "TTFT  ≠  Prefill 计算时间",
        20, True, INK, line=1.1)

    card(s, ML + lw + 0.26, 4.54, lw, 1.4, WHITE, LINE, radius=0.08)
    txt(s, ML + lw + 0.56, 4.76, lw - 0.6, 0.34, "这意味着", 12, True, MUTED, line=1.0)
    for i, t in enumerate(["把 Prefill 的算子优化到极限，TTFT 也可能很差；",
                           "因为大量时间可能消耗在排队、等调度、搬 KV 上。"]):
        txt(s, ML + lw + 0.56, 5.1 + i * 0.36, lw - 0.86, 0.34, t, 12.5, False, BODY, line=1.2)

    takeaway(s, 6.16, "优化 TTFT 不能只盯着 Prefill 内核，要看它在整条链路上真正把时间花在了哪里。",
             BLUE, BLUE_L)
    page_no(s, n)
    return n


# ============================================================ 11 TPOT
def tpot(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 指标定义", "TPOT：生成过程中平均每个字的间隔时间",
           "Time Per Output Token —— 决定「读起来是否顺畅、会不会卡顿」")

    lw = 6.1
    card(s, ML, 2.05, lw, 2.35, WHITE, LINE, radius=0.07)
    rect(s, ML, 2.05, 0.05, 2.35, AMBER)
    txt(s, ML + 0.34, 2.3, lw - 0.68, 0.3, "定义", 12, True, MUTED, line=1.0)
    txt(s, ML + 0.34, 2.62, lw - 0.68, 0.6,
        "Decode 阶段平均生成一个输出 token 所需的时间", 15.5, True, INK, line=1.3)
    formula(s, ML + 0.34, 3.36, lw - 0.68, 0.56,
            "TPOT  ≈  Decode 总时间  /  （输出字数 − 1）", PANEL, INK, 14)
    txt(s, ML + 0.34, 4.02, lw - 0.68, 0.3,
        "它刻画的是「持续输出速度」，而不是首次响应速度。", 12, False, BODY, line=1.0)

    rx = ML + lw + 0.26
    rwd = CW - lw - 0.26
    card(s, rx, 2.05, rwd, 2.35, PANEL, None, radius=0.07)
    txt(s, rx + 0.34, 2.3, rwd - 0.68, 0.3, "用户侧的感受", 12, True, MUTED, line=1.0)
    for i, (v, d, ac) in enumerate([("50 ms / 字", "约 20 字/秒，明显快于阅读速度，体验流畅", TEAL),
                                    ("100 ms / 字", "约 10 字/秒，接近正常阅读速度，可接受", BLUE),
                                    ("300 ms / 字", "约 3 字/秒，肉眼可见地「一顿一顿」", RED)]):
        y = 2.68 + i * 0.56
        rect(s, rx + 0.34, y + 0.06, 0.055, 0.34, ac)
        txt(s, rx + 0.5, y, 1.5, 0.3, v, 14, True, ac, line=1.0)
        txt(s, rx + 2.0, y + 0.02, rwd - 2.4, 0.48, d, 11.5, False, BODY, line=1.15)

    # 时间轴示意
    txt(s, ML, 4.62, CW, 0.26, "两个指标在时间轴上的位置", 12, True, MUTED, line=1.0)
    y0 = 5.28
    hline(s, ML, y0, CW, FAINT, 1.25)
    # TTFT 段
    rect(s, ML, y0 - 0.2, 3.1, 0.4, BLUE_L)
    txt(s, ML, y0 - 0.15, 3.1, 0.3, "TTFT（含排队与 Prefill）", 11, True, BLUE, "c", line=1.0)
    x = ML + 3.1
    for i in range(9):
        rect(s, x + i * 0.94, y0 - 0.14, 0.78, 0.28, AMBER_L)
        txt(s, x + i * 0.94, y0 - 0.1, 0.78, 0.24, "字", 10, True, AMBER, "c", line=1.0)
        if i < 8:
            txt(s, x + i * 0.94 + 0.78, y0 - 0.1, 0.16, 0.24, "·", 10, True, FAINT, "c", line=1.0)
    txt(s, x, y0 + 0.24, CW - 3.1, 0.3, "← 每两个字之间的平均间隔 = TPOT →", 11, True, AMBER, "c", line=1.0)

    takeaway(s, 6.24, "TTFT 决定「愿不愿意等」，TPOT 决定「看得顺不顺」；两者都达标，用户才算满意。",
             AMBER, AMBER_L, h=0.6)
    page_no(s, n)
    return n


# ============================================================ 12 长尾
def tail(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 统计口径", "平均值会骗人：SLO 本质上是长尾问题")

    # 分布示意
    card(s, ML, 2.0, 6.5, 3.4, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.34, 2.24, 5.8, 0.3, "延迟分布：大多数请求很快，少数请求很慢（横轴为百分位）", 13, True, INK, line=1.0)
    base = 4.92
    heights = [0.28, 0.62, 1.05, 1.42, 1.2, 0.86, 0.6, 0.42, 0.3, 0.22, 0.16, 0.12, 0.09, 0.07]
    bw = 0.39
    for i, hh in enumerate(heights):
        x = ML + 0.42 + i * bw
        c = BLUE_L if i < 9 else RED_L
        rect(s, x, base - hh, bw - 0.07, hh, c)
    hline(s, ML + 0.34, base, 5.85, FAINT, 1.25)
    # SLO 红线
    slo_x = ML + 0.42 + 9 * bw
    vline(s, slo_x, 2.72, 2.4, RED, 1.5)
    txt(s, slo_x - 1.0, 2.46, 2.0, 0.26, "SLO 红线", 11, True, RED, "c", line=1.0)
    txt(s, slo_x + 0.1, 4.44, 1.9, 0.44, "越线的请求\n= SLO 违约", 10.5, True, RED, line=1.2)
    for lb, xx in (("p50", 3), ("p90", 7), ("p95", 9), ("p99", 12)):
        x = ML + 0.42 + xx * bw
        txt(s, x - 0.3, base + 0.08, 0.8, 0.24, lb, 10, True, MUTED, "c", line=1.0)

    rx = ML + 6.76
    rwd = CW - 6.76
    card(s, rx, 2.0, rwd, 1.6, RED_L, None, radius=0.07)
    txt(s, rx + 0.3, 2.22, rwd - 0.6, 0.3, "问题", 11.5, True, RED, line=1.0)
    txt(s, rx + 0.3, 2.54, rwd - 0.6, 0.9,
        "平均延迟达标，不代表没有用户受影响。真正重要的是：有多少请求越过了红线。",
        14, True, INK, line=1.4)

    card(s, rx, 3.76, rwd, 1.64, WHITE, LINE, radius=0.07)
    txt(s, rx + 0.3, 3.96, rwd - 0.6, 0.3, "所以我们至少要同时看", 11.5, True, MUTED, line=1.0)
    for i, t in enumerate(["TTFT 的 p50 / p90 / p95",
                           "TPOT 的 p50 / p90 / p95",
                           "SLO 达标率 = 达标请求数 ÷ 总请求数"]):
        y = 4.3 + i * 0.36
        rect(s, rx + 0.32, y + 0.09, 0.1, 0.1, BLUE)
        txt(s, rx + 0.52, y, rwd - 0.9, 0.3, t, 12, False, BODY, line=1.0)

    card(s, ML, 5.58, CW, 0.62, AMBER_L, None, radius=0.1)
    tb, tf = textbox(s, ML + 0.3, 5.58, CW - 0.6, 0.62, "m")
    rich(tf, [("还要注意  ｜  ", {"bold": True, "color": AMBER, "size": 12}),
              ("只看整体达标率，可能掩盖「长上下文请求被长期饿死」的问题", {"bold": True, "color": INK, "size": 13}),
              ("——建议按业务场景 / 上下文长度分桶统计。", {"color": BODY, "size": 12.5})],
         first=True, line=1.2)

    takeaway(s, 6.34, "不追求平均值好看，而追求「越线的人足够少」，并且没有一类用户被系统性牺牲。",
             RED, RED_L, h=0.58)
    page_no(s, n)
    return n


# ============================================================ 13 Goodput
def goodput(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 系统级指标", "Goodput：把「达标」和「产能」合成一个数字")

    card(s, ML, 2.0, 6.1, 1.5, WHITE, TEAL, 1.25, radius=0.07)
    rect(s, ML, 2.0, 6.1, 0.055, TEAL)
    txt(s, ML + 0.34, 2.24, 5.5, 0.3, "定义", 12, True, MUTED, line=1.0)
    txt(s, ML + 0.34, 2.56, 5.5, 0.7,
        "在同时满足 TTFT 与 TPOT 目标的前提下，\n系统能够持续承载的最大请求速率",
        15, True, INK, line=1.35)

    formula(s, ML, 3.66, 6.1, 0.62, "Goodput  =  Throughput  ×  SLO 达标率", PANEL, INK, 15)
    txt(s, ML, 4.42, 6.1, 0.3, "更严格地说：", 11.5, True, MUTED, line=1.0)
    formula(s, ML, 4.74, 6.1, 0.78,
            "Goodput  =  单位时间内「TTFT 达标 且 TPOT 达标」的请求数",
            WHITE, INK, 13.5, LINE, True)

    # 右侧因果链
    rx = ML + 6.4
    rwd = CW - 6.4
    txt(s, rx, 1.96, rwd, 0.3, "为什么「吞吐拉满」反而会掉 Goodput", 13, True, INK, line=1.0)
    chain = [("把吞吐压到最高", BLUE_L, BLUE),
             ("GPU 利用率上升、批次变大", BLUE_L, BLUE),
             ("排队变长 · 相互干扰变强", AMBER_L, AMBER),
             ("长尾延迟恶化", RED_L, RED),
             ("SLO 达标率下降", RED_L, RED),
             ("Goodput 下降", RED, WHITE)]
    y = 2.4
    for i, (t, fill, fc) in enumerate(chain):
        sh = card(s, rx, y, rwd, 0.5, fill, None, radius=0.14)
        box_text(sh, [(t, 12.5, True, fc)])
        if i < len(chain) - 1:
            arrow(s, rx + rwd / 2, y + 0.5, rx + rwd / 2, y + 0.66, FAINT, 1.25, size="sm")
        y += 0.68

    takeaway(s, 6.28, "吞吐最高 ≠ Goodput 最高。后面所有的取舍，都是围绕这一句话展开的。",
             TEAL, TEAL_L, h=0.58)
    page_no(s, n)
    return n
