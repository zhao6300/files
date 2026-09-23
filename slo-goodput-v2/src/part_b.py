# -*- coding: utf-8 -*-
"""Part 3 TTFT 成因 + Part 4 TPOT 成因"""
from deckkit import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 15 TTFT 全链路
def ttft_pipeline(prs, n):
    s = blank(prs)
    header(s, "PART 3 · TTFT 成因", "TTFT 是一条完整的链路，任何一环都可能成为瓶颈")

    # 左：链路
    lx, lw = ML, 2.85
    card(s, lx, 2.0, lw, 4.18, PANEL, None, radius=0.07)
    txt(s, lx + 0.26, 2.2, lw - 0.52, 0.28, "一个请求经历的环节", 11.5, True, MUTED, line=1.0)
    steps = [("请求到达", FAINT, WHITE, INK), ("排队等待", BLUE, BLUE_L, BLUE),
             ("调度选中", BLUE, BLUE_L, BLUE), ("读取 KV Cache", VIO, VIO_L, VIO),
             ("Prefill 计算", VIO, VIO_L, VIO), ("数据传输", TEAL, TEAL_L, TEAL),
             ("第一个字", INK, INK, WHITE)]
    y = 2.58
    for i, (t, bc, fill, fc) in enumerate(steps):
        sh = card(s, lx + 0.26, y, lw - 0.52, 0.42, fill, None, radius=0.16)
        box_text(sh, [(t, 12, True, fc)])
        if i < len(steps) - 1:
            arrow(s, lx + lw / 2, y + 0.42, lx + lw / 2, y + 0.54, FAINT, 1.25, size="sm")
        y += 0.54

    # 右：影响因素
    rx = ML + lw + 0.3
    rwd = CW - lw - 0.3
    txt(s, rx, 1.96, rwd, 0.28, "背后的五类影响因素", 13, True, INK, line=1.0)
    factors = [
        ("请求本身", BLUE, ["输入长度", "前缀是否可复用", "KV 命中 / 未命中", "模型规模"]),
        ("调度策略", BLUE, ["队列长度", "批次如何组合", "FCFS / SJF / EDF", "队头阻塞"]),
        ("GPU 执行", VIO, ["Prefill 吞吐", "Batch 大小", "Chunk 大小", "并行切分与内核效率"]),
        ("部署架构", TEAL, ["PD 聚合 / 分离", "Prefill 资源配比", "实例数量", "KV 跨实例传输"]),
        ("显存层级", AMBER, ["HBM 容量", "前缀缓存命中", "DRAM / NVMe 卸载", "KV 恢复延迟"]),
    ]
    cw = (rwd - 0.44) / 3
    ch = 1.92
    for i, (title, ac, items) in enumerate(factors):
        x = rx + (i % 3) * (cw + 0.22)
        yy = 2.3 + (i // 3) * (ch + 0.26)
        card(s, x, yy, cw, ch, WHITE, LINE, radius=0.07)
        rect(s, x, yy, cw, 0.05, ac)
        txt(s, x + 0.24, yy + 0.24, cw - 0.48, 0.3, title, 14, True, INK, line=1.0)
        hline(s, x + 0.24, yy + 0.62, cw - 0.48)
        for j, it in enumerate(items):
            ty = yy + 0.74 + j * 0.28
            rect(s, x + 0.26, ty + 0.08, 0.08, 0.08, ac)
            txt(s, x + 0.44, ty, cw - 0.7, 0.26, it, 11.5, False, BODY, line=1.0)

    # 第六格放结论
    x = rx + 2 * (cw + 0.22)
    yy = 2.3 + ch + 0.26
    card(s, x, yy, cw, ch, BLUE_L, None, radius=0.07)
    txt(s, x + 0.24, yy + 0.3, cw - 0.48, 1.3,
        "TTFT 差，\n往往不是「算得慢」，\n而是「等得久」。",
        16, True, BLUE, line=1.45)

    page_no(s, n)
    return n


# ============================================================ 16 排队
def queue_slide(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因之一", "排队：TTFT 最容易被忽视的杀手",
           "队头阻塞（Head-of-Line Blocking）——一个大请求会拖慢它身后的所有人")

    # 场景 A：FCFS
    card(s, ML, 2.0, CW, 1.5, WHITE, LINE, radius=0.07)
    pill(s, ML + 0.26, 2.2, 2.4, 0.34, "先来先服务（FCFS）", 11, True, RED_L, RED)
    y = 2.78
    xx = ML + 0.26
    rect(s, xx, y, 4.3, 0.46, RED_L)
    txt(s, xx, y + 0.09, 4.3, 0.3, "超长请求（长文档，Prefill 很重）", 11.5, True, RED, "c", line=1.0)
    xx += 4.42
    for i in range(5):
        rect(s, xx, y, 0.76, 0.46, PANEL2)
        txt(s, xx, y + 0.09, 0.76, 0.3, "短请求", 9.5, True, MUTED, "c", line=1.0)
        xx += 0.86
    txt(s, xx + 0.12, y - 0.02, 3.4, 0.52, "→ 后面 5 个请求即使只要 0.2 秒，\n    也得干等前面算完",
        11, True, RED, line=1.25)

    # 场景 B：按优先级
    card(s, ML, 3.66, CW, 1.5, WHITE, LINE, radius=0.07)
    pill(s, ML + 0.26, 3.86, 2.4, 0.34, "按剩余时间预算排序", 11, True, TEAL_L, TEAL)
    y = 4.44
    xx = ML + 0.26
    for i in range(5):
        rect(s, xx, y, 0.76, 0.46, TEAL_L)
        txt(s, xx, y + 0.09, 0.76, 0.3, "短请求", 9.5, True, TEAL, "c", line=1.0)
        xx += 0.86
    rect(s, xx, y, 4.3, 0.46, PANEL2)
    txt(s, xx, y + 0.09, 4.3, 0.3, "超长请求（安排在紧急度更低时）", 11.5, True, MUTED, "c", line=1.0)
    txt(s, xx + 4.42, y - 0.02, 3.4, 0.52, "→ 多数请求 TTFT 显著下降，\n    整体达标率提升", 11, True, TEAL, line=1.25)

    # 负载链
    lx = ML
    txt(s, lx, 5.34, 5.0, 0.28, "负载升高时的连锁反应", 12, True, MUTED, line=1.0)
    chain = [("请求速率上升", BLUE_L, BLUE), ("队列变长", BLUE_L, BLUE),
             ("TTFT 上升", AMBER_L, AMBER), ("SLO 违约增加", RED_L, RED)]
    x = lx
    for i, (t, fill, fc) in enumerate(chain):
        sh = card(s, x, 5.68, 1.62, 0.42, fill, None, radius=0.14)
        box_text(sh, [(t, 11, True, fc)])
        if i < 3:
            arrow(s, x + 1.62, 5.89, x + 1.78, 5.89, FAINT, 1.25, size="sm")
        x += 1.78

    card(s, ML + 7.4, 5.3, CW - 7.4, 0.8, PANEL, None, radius=0.1)
    txt(s, ML + 7.62, 5.42, CW - 7.84, 0.6,
        "请求在真正开始 GPU 计算之前，就已经消耗掉了大量「可用的延迟预算」。",
        12.5, True, INK, line=1.3)

    takeaway(s, 6.3, "TTFT 优化不能只盯着 Prefill 内核 —— 排队与调度往往是更大的那一块。",
             BLUE, BLUE_L, h=0.58)
    page_no(s, n)
    return n


# ============================================================ 17 Prefill 产能
def prefill_capacity(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因之二", "Prefill 产能不足：排队的根源",
           "这也是 PD 分离部署下 TTFT 恶化的主要原因")

    lw = 5.9
    formula(s, ML, 2.0, lw, 0.62, "Prefill 产能  =  每秒能处理的输入 token 数", PANEL, INK, 14)
    card(s, ML, 2.76, lw, 1.5, RED_L, None, radius=0.07)
    txt(s, ML + 0.3, 2.96, lw - 0.6, 0.3, "一旦出现", 11.5, True, RED, line=1.0)
    txt(s, ML + 0.3, 3.28, lw - 0.6, 0.4, "请求到达速率  >  Prefill 产能", 18, True, INK, "c", line=1.1)
    txt(s, ML + 0.3, 3.76, lw - 0.6, 0.3, "队列就会持续堆积，TTFT 随时间不断恶化（而非稳定）",
        11.5, False, BODY, "c", line=1.0)

    card(s, ML, 4.42, lw, 1.62, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.3, 4.62, lw - 0.6, 0.3, "为什么 PD 分离会踩到这个坑", 13, True, INK, line=1.0)
    for i, t in enumerate(["分离后，Prefill 只能用分给它的那部分 GPU；",
                           "一旦 Prefill 侧资源给少了，请求就在 Prefill 前排队；",
                           "此时 TTFT 变差与「算子快不快」几乎无关。"]):
        y = 4.98 + i * 0.32
        rect(s, ML + 0.32, y + 0.09, 0.1, 0.1, RED)
        txt(s, ML + 0.52, y, lw - 0.9, 0.3, t, 12, False, BODY, line=1.0)

    # 右：PD 比例 U 型曲线
    rx = ML + lw + 0.3
    rwd = CW - lw - 0.3
    card(s, rx, 2.0, rwd, 4.04, WHITE, LINE, radius=0.07)
    txt(s, rx + 0.3, 2.22, rwd - 0.6, 0.3, "PD 资源配比 与 TTFT 的关系", 13, True, INK, line=1.0)
    txt(s, rx + 0.3, 2.54, rwd - 0.6, 0.26, "不是单调的：先下降，再上升", 11, False, MUTED, line=1.0)

    ax, ay, aw, ah = rx + 0.85, 5.3, rwd - 1.4, 2.2
    hline(s, ax, ay, aw, FAINT, 1.25)
    vline(s, ax, ay - ah, ah, FAINT, 1.25)
    txt(s, ax - 0.85, ay - ah - 0.06, 0.8, 0.6, "TTFT\n（越低越好）", 9.5, True, MUTED, "r", line=1.2)
    txt(s, ax, ay + 0.12, aw, 0.26, "分给 Decode 的资源比例  →", 9.5, True, MUTED, "c", line=1.0)

    pts = [(0.02, 0.10), (0.16, 0.42), (0.34, 0.68), (0.5, 0.78), (0.66, 0.6), (0.82, 0.26), (0.97, 0.02)]
    xy = [(ax + px * aw, ay - (1 - py) * ah) for px, py in pts]
    for i in range(len(xy) - 1):
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(xy[i][0]), Inches(xy[i][1]),
                                   Inches(xy[i + 1][0]), Inches(xy[i + 1][1]))
        c.line.color.rgb = RGBColor.from_string(BLUE)
        c.line.width = Pt(2.25)
        c.shadow.inherit = False
    bx, by = xy[3]
    sh = shape(s, MSO_SHAPE.OVAL, bx - 0.075, by - 0.075, 0.15, 0.15, WHITE, BLUE, 2.0)
    txt(s, bx - 0.95, by - 0.52, 1.9, 0.28, "最优配比区间", 10.5, True, BLUE, "c", line=1.0)
    txt(s, ax + 0.12, ay - 0.62, 1.7, 0.46, "Prefill 资源不足\n→ 排队，TTFT 高", 9.5, True, RED, line=1.2)
    txt(s, ax + aw - 1.82, ay - 0.62, 1.8, 0.46, "Decode 资源不足\n→ 反压，TTFT 又高", 9.5, True, RED, "r", line=1.2)

    takeaway(s, 6.18, "PD 资源配比本身就是一个 SLO 控制参数：调它不是「调性能」，而是在 TTFT 与 TPOT 之间做分配。",
             TEAL, TEAL_L, h=0.6)
    page_no(s, n)
    return n


# ============================================================ 18 KV Cache 对 TTFT
def kv_ttft(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因之三", "KV Cache 命中，不一定意味着 TTFT 更低",
           "这是一个非常反直觉、但对我们工作非常关键的结论")

    # 左：层级
    lw = 4.5
    card(s, ML, 2.0, lw, 3.42, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.3, 2.2, lw - 0.6, 0.3, "前缀 KV 可能存在的位置", 13, True, INK, line=1.0)
    tiers = [("HBM（显存）", "直接可用，几乎零成本", TEAL, 0.0),
             ("DRAM（内存）", "需要搬运到显存", BLUE, 0.16),
             ("NVMe（硬盘）", "读取 + 多级搬运，很慢", AMBER, 0.32),
             ("未命中", "只能重新做一遍 Prefill", RED, 0.48)]
    y = 2.6
    for i, (t, d, ac, ind) in enumerate(tiers):
        sh = card(s, ML + 0.3 + ind, y, lw - 0.6 - ind, 0.54, WHITE, ac, 1.25, radius=0.1)
        tf = sh.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        rich(tf, [(t + "    ", {"bold": True, "color": ac, "size": 12.5}),
                  (d, {"color": BODY, "size": 10.5})], first=True, align="l", line=1.1)
        if i < 3:
            arrow(s, ML + 0.45 + ind, y + 0.54, ML + 0.45 + ind + 0.16, y + 0.63, FAINT, 1.25, size="sm")
        y += 0.63
    txt(s, ML + 0.3, 5.1, lw - 0.6, 0.28, "越往下：省下的计算越多，但搬运代价越大", 11, True, MUTED, line=1.0)

    # 右：对比表 + 警示
    rx = ML + lw + 0.3
    rwd = CW - lw - 0.3
    rows = [("KV 所在层级", "省下的 Prefill 计算", "额外搬运开销", "对 TTFT 的净效果"),
            ("HBM 命中", "全部", "几乎没有", "大幅下降 ✓"),
            ("DRAM 命中", "全部", "中等", "通常下降 ✓"),
            ("NVMe 命中", "全部", "较高", "可能反而上升 ×"),
            ("未命中", "无", "无", "取决于 Prefill 产能")]
    grid_table(s, rx, 2.0, rwd, [1.5, 1.4, 1.2, 1.6], rows, row_h=0.46, head_h=0.5,
               align=["l", "c", "c", "c"], size=11)

    card(s, rx, 4.6, rwd, 0.82, AMBER_L, None, radius=0.08)
    tb, tf = textbox(s, rx + 0.28, 4.6, rwd - 0.56, 0.82, "m")
    rich(tf, [("典型案例：  ", {"bold": True, "color": AMBER, "size": 12}),
              ("64K 长上下文请求，KV 命中在 NVMe 上。虽然省掉了大量 Prefill 计算，但 NVMe → 内存 → 显存的恢复延迟，"
               "足以让 TTFT 直接违约。", {"color": INK, "size": 12})], first=True, line=1.3)

    takeaway(s, 5.82, "KV Cache 优化的目标不是把命中率做到最高，而是降低「让请求达标」的总成本——命中也要算上搬运账。",
             AMBER, AMBER_L, h=0.62, icon="对我们的含义")
    page_no(s, n)
    return n


# ============================================================ 20 TPOT 机制
def tpot_mech(prs, n):
    s = blank(prs)
    header(s, "PART 4 · TPOT 成因", "TPOT 由每一次 Decode 步的耗时累积而成")

    # 中间：一次 decode step
    cxs = ML
    txt(s, ML, 1.96, 5.6, 0.28, "一次 Decode 步做了什么", 13, True, INK, line=1.0)
    parts = [("注意力计算", "反复读取 KV Cache → 吃显存带宽", AMBER),
             ("线性层 / MoE 计算", "参数读取与矩阵运算", VIO),
             ("跨卡通信", "张量并行 / 专家并行的数据交换", BLUE),
             ("调度与批次组装", "这一步和谁拼在一个 batch 里", TEAL)]
    y = 2.32
    for t, d, ac in parts:
        card(s, ML, y, 5.6, 0.68, WHITE, LINE, radius=0.08)
        rect(s, ML, y, 0.05, 0.68, ac)
        txt(s, ML + 0.26, y + 0.1, 3.0, 0.28, t, 13, True, INK, line=1.0)
        txt(s, ML + 0.26, y + 0.38, 5.1, 0.26, d, 11, False, BODY, line=1.0)
        y += 0.78
    arrow(s, ML + 2.8, y, ML + 2.8, y + 0.22, FAINT, 1.5)
    sh = card(s, ML + 1.4, y + 0.28, 2.8, 0.5, INK, None, radius=0.14)
    box_text(sh, [("下一个字输出", 12.5, True, WHITE)])

    # 右：敏感因素
    rx = ML + 5.9
    rwd = CW - 5.9
    txt(s, rx, 1.96, rwd, 0.28, "TPOT 对什么最敏感", 13, True, INK, line=1.0)
    groups = [("显存与缓存", AMBER, ["显存带宽（最根本的上限）", "KV Cache 容量与访问效率",
                                "Decode 批次大小与注意力内核效率"]),
              ("干扰与调度", BLUE, ["同一张卡上是否同时在跑 Prefill", "批次里请求的混合方式",
                                "抢占 / 重算带来的抖动"]),
              ("通信（工程扩展维度）", VIO, ["张量并行 / 专家并行的通信量",
                                      "MoE 的 All-to-All 与专家负载均衡",
                                      "NVLink / PCIe 带宽差异"])]
    y = 2.32
    for title, ac, items in groups:
        h = 1.32
        card(s, rx, y, rwd, h, WHITE, LINE, radius=0.07)
        rect(s, rx, y, rwd, 0.05, ac)
        txt(s, rx + 0.26, y + 0.16, rwd - 0.52, 0.28, title, 13, True, INK, line=1.0)
        for j, it in enumerate(items):
            ty = y + 0.5 + j * 0.27
            rect(s, rx + 0.28, ty + 0.08, 0.08, 0.08, ac)
            txt(s, rx + 0.46, ty, rwd - 0.74, 0.26, it, 11.5, False, BODY, line=1.0)
        y += h + 0.15

    txt(s, rx, y + 0.04, rwd, 0.3,
        "注：MoE / PCIe 相关结论来自我们自己的工程观测，不属于论文结论。",
        10.5, True, VIO, line=1.2)

    page_no(s, n)
    return n


# ============================================================ 21 干扰
def interference(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 主因之一", "PD 聚合部署：Prefill 会「插队」打断 Decode",
           "两个阶段抢同一份算力，受伤的通常是 TPOT")

    # 时间轴示意
    card(s, ML, 2.0, CW, 2.16, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.3, 2.2, 6.0, 0.28, "同一张 GPU 上的时间片", 13, True, INK, line=1.0)
    y = 2.66
    txt(s, ML + 0.3, y + 0.06, 1.1, 0.28, "理想情况", 11, True, MUTED, line=1.0)
    x = ML + 1.5
    for i in range(12):
        rect(s, x + i * 0.72, y, 0.6, 0.38, TEAL_L)
        txt(s, x + i * 0.72, y + 0.05, 0.6, 0.28, "字", 10, True, TEAL, "c", line=1.0)
    txt(s, ML + 1.5, y + 0.42, 8.8, 0.24, "每个字之间的间隔均匀 → TPOT 稳定", 10.5, False, MUTED, line=1.0)

    y = 3.4
    txt(s, ML + 0.3, y + 0.06, 1.1, 0.28, "实际情况", 11, True, RED, line=1.0)
    x = ML + 1.5
    seq = ["d", "d", "d", "P", "d", "d", "d", "P", "d", "d"]
    px = x
    for t in seq:
        if t == "d":
            rect(s, px, y, 0.6, 0.38, TEAL_L)
            txt(s, px, y + 0.05, 0.6, 0.28, "字", 10, True, TEAL, "c", line=1.0)
            px += 0.72
        else:
            rect(s, px, y, 1.5, 0.38, VIO_L)
            txt(s, px, y + 0.05, 1.5, 0.28, "Prefill 占用", 10, True, VIO, "c", line=1.0)
            px += 1.62
    txt(s, ML + 1.5, y + 0.42, 9.5, 0.24,
        "Prefill 一次要吃掉很长一段算力 → 出字出现空档 → 用户看到「卡顿」，TPOT 被拉高",
        10.5, False, RED, line=1.0)

    # 干扰强度
    lw = (CW - 0.28) / 2
    card(s, ML, 4.36, lw, 1.56, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.3, 4.54, lw - 0.6, 0.28, "如何量化这种干扰", 12.5, True, INK, line=1.0)
    formula(s, ML + 0.3, 4.9, lw - 0.6, 0.6,
            "干扰强度  =  Decode 期间插入的 Prefill token 数  ÷  输出长度",
            PANEL, INK, 12.5)
    txt(s, ML + 0.3, 5.58, lw - 0.6, 0.26, "直观理解：写答案的时候被打断了多少次、每次多久",
        11, False, MUTED, line=1.0)

    rx = ML + lw + 0.28
    card(s, rx, 4.36, lw, 1.56, BLUE_L, None, radius=0.07)
    txt(s, rx + 0.3, 4.54, lw - 0.6, 0.28, "实验观测", 12.5, True, BLUE, line=1.0)
    txt(s, rx + 0.3, 4.88, lw - 0.6, 0.66,
        "TPOT 与干扰强度呈很强的线性关系（实验中 R² = 0.99）",
        14.5, True, INK, line=1.35)
    txt(s, rx + 0.3, 5.58, lw - 0.6, 0.26, "意味着 TPOT 是可预测、可控的，而不是随机抖动",
        11, True, BLUE, line=1.0)

    takeaway(s, 6.12, "TPOT 变差常常不是 Decode 本身慢了，而是被 Prefill 抢走了时间片。",
             AMBER, AMBER_L, h=0.6)
    page_no(s, n)
    return n


# ============================================================ 22 Chunked Prefill
def chunked(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 关键旋钮", "Chunked Prefill：把长输入切块，块多大是一个权衡",
           "它不是「越大越好」或「越小越好」，而是在 TTFT 与 TPOT 之间移动")

    lw = (CW - 1.2) / 2
    # 大 chunk
    card(s, ML, 2.0, lw, 3.3, WHITE, BLUE, 1.25, radius=0.07)
    rect(s, ML, 2.0, lw, 0.055, BLUE)
    txt(s, ML + 0.3, 2.24, lw - 0.6, 0.32, "块切得大", 17, True, INK, line=1.0)
    for i in range(3):
        rect(s, ML + 0.3 + i * 1.72, 2.7, 1.6, 0.36, BLUE_L)
    txt(s, ML + 0.3, 3.16, lw - 0.6, 0.24, "一次喂给 GPU 很长的输入", 10.5, False, MUTED, line=1.0)
    hline(s, ML + 0.3, 3.5, lw - 0.6)
    for i, (t, ac, good) in enumerate([("Prefill 产能更高，排队更少", TEAL, True),
                                       ("TTFT 下降 ↓", TEAL, True),
                                       ("对 Decode 的打断更严重", RED, False),
                                       ("TPOT 上升 ↑", RED, False)]):
        y = 3.66 + i * 0.36
        rect(s, ML + 0.32, y + 0.1, 0.1, 0.1, ac)
        txt(s, ML + 0.52, y, lw - 0.9, 0.3, t, 12.5, i in (1, 3), ac if i in (1, 3) else BODY, line=1.0)

    txt(s, ML + lw + 0.1, 3.4, 1.0, 0.5, "反向\n权衡", 11.5, True, MUTED, "c", line=1.25)
    arrow(s, ML + lw + 0.18, 3.0, ML + lw + 1.02, 3.0, FAINT, 1.5)
    arrow(s, ML + lw + 1.02, 4.2, ML + lw + 0.18, 4.2, FAINT, 1.5)

    # 小 chunk
    rx = ML + lw + 1.2
    card(s, rx, 2.0, lw, 3.3, WHITE, AMBER, 1.25, radius=0.07)
    rect(s, rx, 2.0, lw, 0.055, AMBER)
    txt(s, rx + 0.3, 2.24, lw - 0.6, 0.32, "块切得小", 17, True, INK, line=1.0)
    for i in range(10):
        rect(s, rx + 0.3 + i * 0.52, 2.7, 0.4, 0.36, AMBER_L)
    txt(s, rx + 0.3, 3.16, lw - 0.6, 0.24, "分很多次，每次只喂一小段", 10.5, False, MUTED, line=1.0)
    hline(s, rx + 0.3, 3.5, lw - 0.6)
    for i, (t, ac) in enumerate([("对 Decode 的打断更小", TEAL),
                                 ("TPOT 下降 ↓", TEAL),
                                 ("Prefill 产能降低，队列变长", RED),
                                 ("TTFT 上升 ↑", RED)]):
        y = 3.66 + i * 0.36
        rect(s, rx + 0.32, y + 0.1, 0.1, 0.1, ac)
        txt(s, rx + 0.52, y, lw - 0.9, 0.3, t, 12.5, i in (1, 3), ac if i in (1, 3) else BODY, line=1.0)

    formula(s, ML, 5.5, CW, 0.62,
            "Chunk 增大  →  TTFT ↓ ，TPOT ↑          Chunk 减小  →  TTFT ↑ ，TPOT ↓",
            PANEL, INK, 15)

    takeaway(s, 6.3, "Chunk 大小不是性能参数，而是 SLO 分配参数：把延迟预算从一个指标挪给另一个。",
             VIO, VIO_L, h=0.58)
    page_no(s, n)
    return n


# ============================================================ 23 PD 聚合 vs 分离
def pd_compare(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 架构权衡", "PD 聚合 与 PD 分离：没有普遍更优，只有更适配")

    rows = [("对比维度", "PD 聚合（放在一起）", "PD 分离（拆开部署）"),
            ("Prefill / Decode 资源", "共用同一批 GPU", "各自独立的 GPU 池"),
            ("Prefill 产能", "高（可借用全部算力）", "受分配比例限制"),
            ("TTFT 表现", "通常较低（更好）", "容易因排队而恶化"),
            ("两阶段相互干扰", "存在，且明显", "基本消除"),
            ("TPOT 表现", "容易被 Prefill 拖累", "通常更稳定"),
            ("资源独立扩缩容", "较弱", "较强"),
            ("KV 跨实例传输", "不需要", "需要，且有成本"),
            ("主要风险点", "TPOT 违约", "TTFT 违约")]
    grid_table(s, ML, 1.92, CW, [2.1, 2.6, 2.6], rows, row_h=0.4, head_h=0.44,
               align=["l", "c", "c"], size=11.5)

    txt(s, ML, 5.66, CW, 0.28, "在不同 SLO 要求下，实验结论完全反转", 12.5, True, MUTED, line=1.0)
    cases = [("TTFT 要求宽松 + TPOT 要求严格", "PD 分离胜出", "达标率约 98%", TEAL),
             ("TTFT 要求严格 + TPOT 要求宽松", "PD 聚合胜出", "达标率约 97%", BLUE),
             ("两个指标都要求严格", "两者都明显下降", "需要更精细的手段", RED)]
    w = (CW - 0.4) / 3
    for i, (cond, who, num, ac) in enumerate(cases):
        x = ML + i * (w + 0.2)
        card(s, x, 5.96, w, 0.8, WHITE, LINE, radius=0.08)
        rect(s, x, 5.96, 0.05, 0.8, ac)
        txt(s, x + 0.22, 6.04, w - 0.44, 0.24, cond, 10.5, False, MUTED, line=1.0)
        txt(s, x + 0.22, 6.3, w - 0.44, 0.26, who, 13, True, ac, line=1.0)
        txt(s, x + 0.22, 6.56, w - 0.44, 0.22, num, 10, False, BODY, line=1.0)
    page_no(s, n)
    return n
