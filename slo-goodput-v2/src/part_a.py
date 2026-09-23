# -*- coding: utf-8 -*-
"""封面 + Part 1 为什么需要 SLO + Part 2 核心指标（精简图形版）"""
from deckkit import *
from charts import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 01 封面
def cover(prs, n):
    s = blank(prs)
    rect(s, 0, 0, SW, SH, WHITE)
    rect(s, 8.72, 0, SW - 8.72, SH, PANEL)
    rect(s, 8.72, 0, 0.02, SH, LINE)

    txt(s, ML, 0.9, 6.0, 0.32, "技术分享  ·  推理系统性能优化", 13, True, BLUE, line=1.0)
    rect(s, ML, 2.3, 0.7, 0.06, INK)
    txt(s, ML, 2.66, 7.7, 1.9, "大模型推理服务的\nSLO 与 Goodput", 46, True, INK, line=1.14)
    txt(s, ML, 4.62, 7.4, 0.5, "我们衡量什么，为什么会违约，能动哪些旋钮",
        18, False, MUTED, line=1.3)

    px = ML
    for label, sub, fill, fc in (("TTFT", "首字延迟", BLUE_L, BLUE),
                                 ("TPOT", "每字延迟", TEAL_L, TEAL),
                                 ("Goodput", "有效吞吐", AMBER_L, AMBER)):
        w = 2.28
        sh = card(s, px, 5.42, w, 0.92, fill, None, radius=0.14)
        box_text(sh, [(label, 18, True, fc), (sub, 12.5, False, BODY)])
        px += w + 0.26

    txt(s, ML, 6.74, 7.0, 0.32, "汇报人：＿＿＿      2026 / 09", 13, False, FAINT, line=1.0)

    # 右侧：目标漏斗
    cx0, cw = 9.05, 1.82
    a = card(s, cx0, 1.9, cw, 0.86, WHITE, LINE, radius=0.12)
    box_text(a, [("TTFT", 17, True, BLUE), ("第一个字", 12, False, MUTED)])
    b = card(s, cx0 + cw + 0.2, 1.9, cw, 0.86, WHITE, LINE, radius=0.12)
    box_text(b, [("TPOT", 17, True, TEAL), ("后续每个字", 12, False, MUTED)])
    arrow(s, cx0 + cw / 2, 2.76, cx0 + cw / 2 + 0.42, 3.3, FAINT, 1.5)
    arrow(s, cx0 + cw + 0.2 + cw / 2, 2.76, cx0 + cw + 0.2 + cw / 2 - 0.42, 3.3, FAINT, 1.5)
    c = card(s, cx0, 3.36, cw * 2 + 0.2, 0.86, WHITE, LINE, radius=0.12)
    box_text(c, [("SLO 达标率", 17, True, INK), ("多少请求满足要求", 12, False, MUTED)])
    arrow(s, cx0 + cw + 0.1, 4.22, cx0 + cw + 0.1, 4.7, FAINT, 1.5)
    d = card(s, cx0, 4.76, cw * 2 + 0.2, 1.05, BLUE, None, radius=0.12)
    box_text(d, [("Goodput", 22, True, WHITE), ("达标前提下的产能", 12.5, False, "DCE6FD")])
    txt(s, cx0, 5.98, cw * 2 + 0.2, 0.32, "最终目标", 14, True, MUTED, "c", line=1.0)
    return n


# ============================================================ 02 三个核心观点
def summary(prs, n):
    s = blank(prs)
    header(s, "写在最前面", "只记三句话")
    cards = [
        ("01", "体验只有两件事", BLUE, BLUE_L, [("TTFT", "第一个字等多久"), ("TPOT", "后面出字快不快")]),
        ("02", "看达标率，不看平均", TEAL, TEAL_L, [("p90 / p95", "长尾才是投诉源"), ("分场景", "别饿死长请求")]),
        ("03", "目标是 Goodput", AMBER, AMBER_L, [("达标产能", "能接多少请求"), ("吞吐拉满", "反而可能下降")]),
    ]
    w = (CW - 0.5) / 3
    for i, (num, title, ac, al, pairs) in enumerate(cards):
        x = ML + i * (w + 0.25)
        card(s, x, 2.1, w, 3.5, WHITE, LINE, radius=0.07)
        rect(s, x, 2.1, w, 0.06, ac)
        txt(s, x + 0.36, 2.44, 1.2, 0.6, num, 36, True, al, line=1.0)
        txt(s, x + 0.36, 3.12, w - 0.72, 0.6, title, 21, True, INK, line=1.2)
        hline(s, x + 0.36, 3.92, w - 0.72)
        for j, (k, v) in enumerate(pairs):
            yy = 4.1 + j * 0.66
            rect(s, x + 0.36, yy + 0.06, 0.06, 0.42, ac)
            txt(s, x + 0.54, yy, w - 0.9, 0.3, k, 17, True, ac, line=1.0)
            txt(s, x + 0.54, yy + 0.32, w - 0.9, 0.3, v, 14, False, BODY, line=1.0)
        x += w + 0.25

    takeaway(s, 6.02, "所有底层优化，最终都汇聚成 Goodput 这一个数字", INK, PANEL,
             h=0.72, size=18, icon="一句话")
    page_no(s, n)
    return n


# ============================================================ 03 内容框架
def roadmap(prs, n):
    s = blank(prs)
    header(s, "内容框架", "六个部分，一条主线")
    items = [("1", "为什么需要 SLO", BLUE), ("2", "核心指标", BLUE),
             ("3", "TTFT 由什么决定", TEAL), ("4", "TPOT 由什么决定", TEAL),
             ("5", "五层控制手段", AMBER), ("6", "系统级优化", AMBER)]
    w = (CW - 0.5) / 3
    for i, (num, title, ac) in enumerate(items):
        x = ML + (i % 3) * (w + 0.25)
        y = 2.24 + (i // 3) * 1.96
        card(s, x, y, w, 1.6, WHITE, LINE, radius=0.07)
        rect(s, x, y, 0.06, 1.6, ac)
        sh = shape(s, MSO_SHAPE.OVAL, x + 0.34, y + 0.34, 0.52, 0.52, ac, None)
        box_text(sh, [(num, 17, True, WHITE)])
        txt(s, x + 1.02, y + 0.42, w - 1.3, 0.48, title, 20, True, INK, line=1.15)

    txt(s, ML, 6.26, CW, 0.4, "指标 → 成因 → 手段 → 权衡", 17, True, MUTED, "c", line=1.0)
    page_no(s, n)
    return n


# ============================================================ 05 从性能到 SLO
def why_slo(prs, n):
    s = blank(prs)
    header(s, "PART 1", "换个视角看指标")

    lw = 3.95
    card(s, ML, 2.1, lw, 2.9, PANEL, None, radius=0.07)
    txt(s, ML + 0.34, 2.36, lw - 0.68, 0.34, "机器视角", 18, True, MUTED, line=1.0)
    for i, t in enumerate(["吞吐", "延迟", "GPU 利用率", "Tokens / s"]):
        yy = 2.9 + i * 0.5
        rect(s, ML + 0.36, yy + 0.12, 0.14, 0.14, FAINT)
        txt(s, ML + 0.62, yy, lw - 1.0, 0.36, t, 17, False, BODY, line=1.0)

    arrow(s, ML + lw + 0.22, 3.55, ML + lw + 1.1, 3.55, BLUE, 2.5, size="lg")
    txt(s, ML + lw + 0.1, 3.05, 1.2, 0.3, "换视角", 14, True, BLUE, "c", line=1.0)

    rx = ML + lw + 1.32
    rwd = CW - lw - 1.32
    card(s, rx, 2.1, rwd, 2.9, WHITE, BLUE, 1.5, radius=0.07)
    rect(s, rx, 2.1, rwd, 0.06, BLUE)
    txt(s, rx + 0.4, 2.36, rwd - 0.8, 0.34, "用户视角", 18, True, INK, line=1.0)
    txt(s, rx + 0.4, 2.82, rwd - 0.8, 1.16,
        "体验不被破坏的前提下，\n最多能承载多少请求？", 24, True, BLUE, line=1.35)
    hline(s, rx + 0.4, 4.08, rwd - 0.8)
    trio = [("SLA", "对外承诺"), ("SLO", "内部目标"), ("SLI", "实测数值")]
    cw2 = (rwd - 0.8 - 0.4) / 3
    for i, (k, v) in enumerate(trio):
        x = rx + 0.4 + i * (cw2 + 0.2)
        sh = card(s, x, 4.24, cw2, 0.6, PANEL, None, radius=0.1)
        tf = sh.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        rich(tf, [(k + "  ", {"bold": True, "color": INK, "size": 15}),
                  (v, {"color": BODY, "size": 13})], first=True, align="c", line=1.0)

    takeaway(s, 5.54, "吞吐再高，用户等不起就不算产能", BLUE, BLUE_L, h=0.78, size=20)
    page_no(s, n)
    return n


# ============================================================ 06 餐厅类比
def analogy(prs, n):
    s = blank(prs)
    header(s, "PART 1", "把推理服务想成一家餐厅")
    steps = [("排队等位", "请求排队", "Queue", BLUE),
             ("看菜单点单", "读完提问", "Prefill", VIO),
             ("第一道菜上桌", "第一个字", "TTFT", TEAL),
             ("后续菜陆续上", "逐字生成", "TPOT", AMBER),
             ("满意客人数", "达标请求数", "Goodput", INK)]
    w = (CW - 4 * 0.28) / 5
    for i, (top, bottom, tagname, ac) in enumerate(steps):
        x = ML + i * (w + 0.28)
        card(s, x, 2.2, w, 1.5, WHITE, LINE, radius=0.08)
        rect(s, x, 2.2, w, 0.06, ac)
        txt(s, x + 0.16, 2.6, w - 0.32, 0.8, top, 19, True, INK, "c", line=1.25)
        tri_down(s, x + w / 2, 3.86, 0.26, 0.18, FAINT)
        card(s, x, 4.2, w, 1.42, PANEL, None, radius=0.08)
        txt(s, x + 0.16, 4.44, w - 0.32, 0.4, bottom, 18, True, BODY, "c", line=1.1)
        pill(s, x + (w - 1.5) / 2, 4.98, 1.5, 0.4, tagname, 12.5, True, WHITE, ac, ac, 1.25)
        if i < 4:
            arrow(s, x + w + 0.04, 2.95, x + w + 0.26, 2.95, FAINT, 1.5, size="sm")

    takeaway(s, 5.9, "「等第一道菜」和「后面上菜快不快」是两个问题", TEAL, TEAL_L, h=0.78, size=20)
    page_no(s, n)
    return n


# ============================================================ 08 两个阶段
def two_phases(prs, n):
    s = blank(prs)
    header(s, "PART 2", "一次请求，两个阶段")

    card(s, ML, 2.2, 4.75, 2.45, WHITE, VIO, 1.5, radius=0.07)
    rect(s, ML, 2.2, 4.75, 0.06, VIO)
    txt(s, ML + 0.34, 2.5, 4.1, 0.44, "Prefill  读题", 24, True, INK, line=1.0)
    for i, t in enumerate(["一次读完整段输入", "吃算力（计算密集）", "产生 KV Cache"]):
        yy = 3.16 + i * 0.44
        rect(s, ML + 0.36, yy + 0.13, 0.14, 0.14, VIO)
        txt(s, ML + 0.62, yy, 4.0, 0.36, t, 16.5, False, BODY, line=1.0)

    sh = card(s, ML + 5.05, 3.0, 1.62, 1.0, INK, None, radius=0.12)
    box_text(sh, [("第一个字", 16, True, WHITE)])
    arrow(s, ML + 4.82, 3.5, ML + 5.0, 3.5, INK, 2.0)
    arrow(s, ML + 6.72, 3.5, ML + 6.9, 3.5, INK, 2.0)

    dx = ML + 6.95
    dw = CW - 6.95
    card(s, dx, 2.2, dw, 2.45, WHITE, AMBER, 1.5, radius=0.07)
    rect(s, dx, 2.2, dw, 0.06, AMBER)
    txt(s, dx + 0.34, 2.5, dw - 0.6, 0.44, "Decode  写答案", 24, True, INK, line=1.0)
    for i, t in enumerate(["一个字一个字生成", "吃显存带宽", "步数多，怕被打断"]):
        yy = 3.16 + i * 0.44
        rect(s, dx + 0.36, yy + 0.13, 0.14, 0.14, AMBER)
        txt(s, dx + 0.62, yy, dw - 1.0, 0.36, t, 16.5, False, BODY, line=1.0)

    sh = card(s, ML, 4.86, 4.75, 0.82, VIO_L, None, radius=0.1)
    box_text(sh, [("TTFT", 26, True, VIO)])
    sh = card(s, dx, 4.86, dw, 0.82, AMBER_L, None, radius=0.1)
    box_text(sh, [("TPOT", 26, True, AMBER)])

    takeaway(s, 5.92, "瓶颈不同：优化 TTFT 的手段，常常伤害 TPOT", TEAL, TEAL_L, h=0.78, size=20)
    page_no(s, n)
    return n


# ============================================================ 09 TTFT 构成（堆叠条形图）
def ttft(prs, n):
    s = blank(prs)
    header(s, "PART 2 · TTFT", "TTFT 不等于 Prefill 时间")

    band(s, ML, 2.08, CW, 3.42)
    tag(s, ML + 0.34, 2.26, "示意图（非实测数据）", 12.5, FAINT)
    legend(s, ML + 0.34, 2.72, [("排队", BLUE), ("KV 读取", VIO), ("Prefill 计算", TEAL),
                                ("其他", FAINT)], size=15)
    rows = [("负载低", [(0.4, BLUE), (0.25, VIO), (1.0, TEAL, "Prefill"), (0.15, FAINT)],
             "1.8 s   达标", TEAL),
            ("负载高", [(3.3, BLUE, "排队"), (0.25, VIO), (1.0, TEAL, "Prefill"), (0.15, FAINT)],
             "4.7 s   违约", RED)]
    bx, bw, _ = hbar_stacked(s, ML + 0.34, 3.36, CW - 0.68, rows, maxv=5.4,
                             row_h=0.88, gap=0.44, lab_w=1.5, lab_size=19,
                             seg_size=14, total_size=17)
    # SLO 红线（标签放在两行之间的空隙，避免压住条形）
    sx = bx + bw * 2.4 / 5.4
    vline(s, sx, 3.2, 2.2, RED, 2.0)
    txt(s, sx + 0.16, 4.34, 2.2, 0.32, "SLO 红线", 15, True, RED, line=1.0)

    takeaway(s, 5.82, "只优化 Prefill 内核，救不了 TTFT", BLUE, BLUE_L, h=0.86, size=22)
    page_no(s, n)
    return n


# ============================================================ 10 TPOT（柱状图）
def tpot(prs, n):
    s = blank(prs)
    header(s, "PART 2 · TPOT", "TPOT：生成时每个字的间隔")

    band(s, ML, 2.1, 6.9, 3.5)
    txt(s, ML + 0.4, 2.34, 6.1, 0.34, "用户能感觉到的差别", 16, True, MUTED, line=1.0)
    vbar_chart(s, ML + 0.9, 2.86, 5.5, 1.85,
               [("50 ms", 20, TEAL, "20 字/秒", "流畅"),
                ("100 ms", 10, BLUE, "10 字/秒", "可接受"),
                ("300 ms", 3, RED, "3 字/秒", "明显卡顿")],
               maxv=24, val_size=20, lab_size=18, sub_size=15)

    rx = ML + 7.2
    rwd = CW - 7.2
    card(s, rx, 2.1, rwd, 1.6, WHITE, LINE, radius=0.07)
    rect(s, rx, 2.1, 0.06, 1.6, AMBER)
    txt(s, rx + 0.36, 2.4, rwd - 0.7, 0.34, "怎么算", 16, True, MUTED, line=1.0)
    txt(s, rx + 0.36, 2.8, rwd - 0.7, 0.84, "Decode 总时间\n÷ 输出字数", 18.5, True, INK, line=1.35)

    card(s, rx, 3.86, rwd, 1.74, AMBER_L, None, radius=0.07)
    txt(s, rx + 0.36, 4.12, rwd - 0.7, 0.34, "它不是什么", 16, True, AMBER, line=1.0)
    txt(s, rx + 0.36, 4.54, rwd - 0.7, 0.92, "不是首次响应速度，\n而是持续输出速度",
        18, True, INK, line=1.35)

    # 时间轴
    y0 = 6.06
    rect(s, ML, y0 - 0.26, 3.0, 0.52, BLUE_L)
    txt(s, ML, y0 - 0.19, 3.0, 0.38, "TTFT", 17, True, BLUE, "c", line=1.0)
    x = ML + 3.1
    for i in range(9):
        rect(s, x + i * 1.0, y0 - 0.2, 0.8, 0.4, AMBER_L)
        txt(s, x + i * 1.0, y0 - 0.13, 0.8, 0.3, "字", 15, True, AMBER, "c", line=1.0)
    txt(s, x + 0.9, y0 + 0.3, 3.0, 0.3, "间隔 = TPOT", 15, True, AMBER, line=1.0)
    page_no(s, n)
    return n


# ============================================================ 11 长尾
def tail(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 统计口径", "平均值会骗人")

    band(s, ML, 2.1, 7.5, 3.9)
    base = 5.42
    heights = [0.3, 0.68, 1.15, 1.55, 1.3, 0.94, 0.66, 0.46, 0.33, 0.24, 0.18, 0.13, 0.1, 0.08]
    bw = 0.47
    for i, hh in enumerate(heights):
        x = ML + 0.55 + i * bw
        rect(s, x, base - hh, bw - 0.09, hh, BLUE_L if i < 9 else RED_L)
    hline(s, ML + 0.45, base, 6.9, FAINT, 1.5)
    slo_x = ML + 0.55 + 9 * bw
    vline(s, slo_x, 2.72, 2.7, RED, 2.0)
    txt(s, slo_x - 1.5, 2.36, 3.0, 0.34, "SLO 红线", 16, True, RED, "c", line=1.0)
    txt(s, slo_x + 0.16, 4.5, 2.2, 0.8, "越线 =\n违约", 18, True, RED, line=1.25)
    for lb, xx in (("p50", 3), ("p90", 7), ("p95", 9), ("p99", 12)):
        x = ML + 0.55 + xx * bw
        txt(s, x - 0.45, base + 0.14, 1.0, 0.3, lb, 14, True, MUTED, "c", line=1.0)

    rx = ML + 7.8
    rwd = CW - 7.8
    card(s, rx, 2.1, rwd, 1.9, RED_L, None, radius=0.07)
    txt(s, rx + 0.34, 2.44, rwd - 0.68, 1.3,
        "平均达标，\n不代表没人受影响", 21, True, INK, line=1.4)
    card(s, rx, 4.16, rwd, 1.84, WHITE, LINE, radius=0.07)
    txt(s, rx + 0.34, 4.44, rwd - 0.68, 0.34, "要看", 16, True, MUTED, line=1.0)
    for i, t in enumerate(["p90 / p95", "SLO 达标率", "按上下文长度分桶"]):
        yy = 4.86 + i * 0.4
        rect(s, rx + 0.36, yy + 0.12, 0.12, 0.12, BLUE)
        txt(s, rx + 0.58, yy, rwd - 0.95, 0.34, t, 16, False, BODY, line=1.0)

    takeaway(s, 6.16, "关键不是平均值，而是越线的人有多少", RED, RED_L, h=0.74, size=20)
    page_no(s, n)
    return n


# ============================================================ 12 Goodput（双曲线）
def goodput(prs, n):
    s = blank(prs)
    header(s, "PART 2 · 系统级指标", "吞吐最高，Goodput 未必最高")

    band(s, ML, 2.08, 8.4, 4.0)
    ax, ay, aw, ah = ML + 1.15, 2.6, 6.7, 2.7
    axes(s, ax, ay, aw, ah, "指标值", "系统负载  →", FAINT, 1.5, 15, 15)

    # 先铺底色区（保证曲线画在上层）
    px = ax + 0.5 * aw
    py = ay + ah - 0.7 * ah
    rect(s, px, ay, aw - (px - ax), ah, "FBF1F1")
    txt(s, px + 0.28, ay + ah - 1.15, aw - (px - ax) - 0.5, 0.8,
        "吞吐还在涨\n达标率已在掉", 17, True, RED, line=1.3)

    # 吞吐：单调上升并饱和
    curve(s, ax, ay, aw, ah, [(0, 0.05), (0.2, 0.36), (0.4, 0.6), (0.6, 0.76),
                              (0.8, 0.85), (1.0, 0.88)], BLUE, 3.0)
    # Goodput：先升后降
    curve(s, ax, ay, aw, ah, [(0, 0.05), (0.18, 0.34), (0.36, 0.6), (0.5, 0.7),
                              (0.66, 0.55), (0.83, 0.3), (1.0, 0.12)], TEAL, 3.0)
    legend(s, ax + 0.15, ay - 0.5, [("吞吐", BLUE), ("Goodput", TEAL)], size=16)

    vline(s, px, py, ay + ah - py, FAINT, 1.5)
    dot(s, px, py, 0.1, WHITE, TEAL, 2.5)
    txt(s, px - 2.95, py - 0.46, 2.8, 0.32, "最佳工作点", 15, True, TEAL, "r", line=1.0)

    rx = ML + 8.7
    rwd = CW - 8.7
    card(s, rx, 2.08, rwd, 1.9, WHITE, TEAL, 1.5, radius=0.07)
    rect(s, rx, 2.08, rwd, 0.06, TEAL)
    txt(s, rx + 0.34, 2.38, rwd - 0.68, 1.52,
        "Goodput\n=\n吞吐 × 达标率", 20, True, INK, line=1.45)
    card(s, rx, 4.14, rwd, 1.94, PANEL, None, radius=0.07)
    txt(s, rx + 0.34, 4.44, rwd - 0.68, 1.3,
        "只有两个指标\n都达标的请求，\n才算真实产能", 18, True, BODY, line=1.45)

    takeaway(s, 6.28, "后面所有取舍，都围绕这条曲线", TEAL, TEAL_L, h=0.7, size=19)
    page_no(s, n)
    return n
