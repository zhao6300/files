# -*- coding: utf-8 -*-
"""Part 3 TTFT 成因 + Part 4 TPOT 成因（精简图形版）"""
from deckkit import *
from charts import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 14 TTFT 五类因素
def ttft_pipeline(prs, n):
    s = blank(prs)
    header(s, "PART 3 · TTFT", "五类因素决定 TTFT")
    factors = [("请求本身", BLUE, ["输入长度", "前缀可否复用", "KV 命中"]),
               ("调度策略", BLUE, ["队列长度", "批次组合", "队头阻塞"]),
               ("GPU 执行", VIO, ["Prefill 产能", "Chunk 大小", "内核效率"]),
               ("部署架构", TEAL, ["PD 形态", "资源配比", "KV 传输"]),
               ("显存层级", AMBER, ["HBM 容量", "前缀缓存", "卸载与恢复"])]
    w = (CW - 4 * 0.24) / 5
    for i, (title, ac, items) in enumerate(factors):
        x = ML + i * (w + 0.24)
        card(s, x, 2.18, w, 2.9, WHITE, LINE, radius=0.07)
        rect(s, x, 2.18, w, 0.06, ac)
        txt(s, x + 0.24, 2.5, w - 0.48, 0.38, title, 19, True, INK, line=1.0)
        hline(s, x + 0.24, 3.02, w - 0.48)
        for j, it in enumerate(items):
            ty = 3.2 + j * 0.54
            rect(s, x + 0.26, ty + 0.14, 0.12, 0.12, ac)
            txt(s, x + 0.48, ty, w - 0.76, 0.52, it, 15.5, False, BODY, line=1.15)

    card(s, ML, 5.28, CW, 0.9, BLUE_L, None, radius=0.1)
    txt(s, ML, 5.42, CW, 0.5, "TTFT 差，通常不是「算得慢」，而是「等得久」", 24, True, BLUE, "c", line=1.0)
    page_no(s, n)
    return n


# ============================================================ 15 排队
def queue_slide(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因一", "队头阻塞：一个大请求拖慢一片")

    # FCFS
    card(s, ML, 2.15, CW, 1.72, WHITE, LINE, radius=0.07)
    pill(s, ML + 0.3, 2.38, 1.5, 0.44, "FCFS", 15, True, RED_L, RED)
    y = 3.0
    xx = ML + 0.3
    rect(s, xx, y, 4.6, 0.6, RED_L)
    txt(s, xx, y + 0.14, 4.6, 0.36, "超长请求", 17, True, RED, "c", line=1.0)
    xx += 4.75
    for i in range(5):
        rect(s, xx, y, 0.9, 0.6, PANEL2)
        txt(s, xx, y + 0.14, 0.9, 0.36, "短", 15, True, MUTED, "c", line=1.0)
        xx += 1.0
    txt(s, xx + 0.2, y + 0.06, 1.5, 0.5, "全部干等", 18, True, RED, line=1.2)

    # 按预算排序
    card(s, ML, 4.03, CW, 1.72, WHITE, LINE, radius=0.07)
    pill(s, ML + 0.3, 4.26, 2.6, 0.44, "按剩余预算排序", 15, True, TEAL_L, TEAL)
    y = 4.88
    xx = ML + 0.3
    for i in range(5):
        rect(s, xx, y, 0.9, 0.6, TEAL_L)
        txt(s, xx, y + 0.14, 0.9, 0.36, "短", 15, True, TEAL, "c", line=1.0)
        xx += 1.0
    rect(s, xx, y, 4.6, 0.6, PANEL2)
    txt(s, xx, y + 0.14, 4.6, 0.36, "超长请求", 17, True, MUTED, "c", line=1.0)
    txt(s, xx + 4.8, y + 0.06, 1.5, 0.5, "多数变快", 18, True, TEAL, line=1.2)

    takeaway(s, 5.94, "排队与调度，常常比 Prefill 内核更值得优化", BLUE, BLUE_L, h=0.78, size=20)
    page_no(s, n)
    return n


# ============================================================ 16 Prefill 产能 / PD 配比
def prefill_capacity(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因二", "PD 资源配比：存在最优区间")

    lw = 3.5
    card(s, ML, 2.15, lw, 1.7, RED_L, None, radius=0.07)
    txt(s, ML + 0.32, 2.38, lw - 0.64, 1.4,
        "到达速率\n>\nPrefill 产能", 20, True, INK, "c", line=1.35)
    tri_down(s, ML + lw / 2, 3.94, 0.3, 0.2, FAINT)
    card(s, ML, 4.22, lw, 1.7, WHITE, LINE, radius=0.07)
    txt(s, ML + 0.32, 4.46, lw - 0.64, 1.38,
        "队列持续堆积\n↓\nTTFT 不断恶化", 19, True, RED, "c", line=1.35)

    # U 型曲线
    rx = ML + lw + 0.35
    rwd = CW - lw - 0.35
    band(s, rx, 2.15, rwd, 3.77)
    ax, ay, aw, ah = rx + 1.65, 2.75, rwd - 2.35, 2.35
    axes(s, ax, ay, aw, ah, "TTFT\n越低越好", "分给 Decode 的资源比例  →", FAINT, 1.5, 15, 15)
    pts = curve(s, ax, ay, aw, ah,
                [(0.02, 0.9), (0.16, 0.58), (0.34, 0.32), (0.5, 0.22),
                 (0.66, 0.4), (0.82, 0.74), (0.97, 0.98)], BLUE, 3.0)
    bx, by = pts[3]
    dot(s, bx, by, 0.1, WHITE, BLUE, 2.5)
    txt(s, bx - 1.5, by + 0.16, 3.0, 0.34, "最优区间", 16, True, BLUE, "c", line=1.0)
    txt(s, ax + 0.18, ay + ah - 1.02, 2.1, 0.62, "Prefill\n资源不足", 15.5, True, RED, line=1.2)
    txt(s, ax + aw - 2.28, ay + ah - 1.02, 2.1, 0.62, "Decode\n资源不足", 15.5, True, RED, "r", line=1.2)

    takeaway(s, 6.04, "PD 配比不是性能参数，而是 SLO 分配参数", TEAL, TEAL_L, h=0.74, size=20)
    page_no(s, n)
    return n


# ============================================================ 17 KV Cache（堆叠条形图）
def kv_ttft(prs, n):
    s = blank(prs)
    header(s, "PART 3 · 主因三", "KV 命中，不一定更快")

    band(s, ML, 2.1, CW, 3.86)
    legend(s, ML + 0.4, 2.36, [("Prefill 计算", TEAL), ("搬运 / 恢复", AMBER)], size=15)
    tag(s, ML + CW - 3.2, 2.38, "示意图（非实测数据）", 12.5, FAINT)
    rows = [("HBM 命中", [(0.15, TEAL), (0.1, AMBER)], "最快", TEAL),
            ("DRAM 命中", [(0.15, TEAL), (0.7, AMBER)], "仍然更快", TEAL),
            ("NVMe 命中", [(0.15, TEAL), (3.6, AMBER, "搬运")], "反而违约", RED),
            ("未命中", [(2.2, TEAL, "重新 Prefill"), (0, AMBER)], "看产能", MUTED)]
    bx, bw, _ = hbar_stacked(s, ML + 0.4, 3.02, CW - 0.8, rows, maxv=4.4,
                             row_h=0.6, gap=0.2, lab_w=2.0, lab_size=18,
                             seg_size=14, total_size=16)
    sx = bx + bw * 2.9 / 4.4
    txt(s, sx - 1.5, 2.56, 3.0, 0.32, "TTFT 红线", 15, True, RED, "c", line=1.0)
    vline(s, sx, 2.92, 3.0, RED, 2.0)

    takeaway(s, 6.14, "省下的计算，可能被搬运延迟全部吃掉", AMBER, AMBER_L, h=0.76,
             size=20, icon="对我们的含义")
    page_no(s, n)
    return n


# ============================================================ 19 TPOT 机制
def tpot_mech(prs, n):
    s = blank(prs)
    header(s, "PART 4 · TPOT", "每一步 Decode 都可能被拖慢")

    steps = [("注意力", "读 KV Cache", AMBER), ("线性层 / MoE", "读参数", VIO),
             ("跨卡通信", "TP / EP", BLUE), ("调度组批", "和谁一起算", TEAL)]
    w = (CW - 3 * 0.24 - 2.3) / 4
    for i, (t, d, ac) in enumerate(steps):
        x = ML + i * (w + 0.24)
        card(s, x, 2.2, w, 1.2, WHITE, LINE, radius=0.08)
        rect(s, x, 2.2, w, 0.06, ac)
        txt(s, x + 0.16, 2.5, w - 0.32, 0.36, t, 18, True, INK, "c", line=1.0)
        txt(s, x + 0.16, 2.9, w - 0.32, 0.32, d, 14, False, MUTED, "c", line=1.0)
        if i < 3:
            txt(s, x + w, 2.62, 0.24, 0.36, "+", 20, True, FAINT, "c", line=1.0)
    sh = card(s, ML + 4 * (w + 0.24), 2.2, 2.06, 1.2, INK, None, radius=0.12)
    box_text(sh, [("下一个字", 17, True, WHITE)])

    groups = [("显存带宽", AMBER, "最根本的上限"),
              ("Prefill 干扰", BLUE, "被抢走时间片"),
              ("通信开销", VIO, "MoE / PCIe")]
    w2 = (CW - 0.5) / 3
    for i, (t, ac, d) in enumerate(groups):
        x = ML + i * (w2 + 0.25)
        card(s, x, 3.68, w2, 1.85, WHITE, LINE, radius=0.07)
        rect(s, x, 3.68, 0.06, 1.85, ac)
        sh = shape(s, MSO_SHAPE.OVAL, x + 0.34, 3.98, 0.44, 0.44, ac, None)
        box_text(sh, [(str(i + 1), 15, True, WHITE)])
        txt(s, x + 0.34, 4.6, w2 - 0.68, 0.4, t, 21, True, INK, line=1.0)
        txt(s, x + 0.34, 5.06, w2 - 0.68, 0.34, d, 15, False, BODY, line=1.0)

    txt(s, ML, 5.68, CW, 0.32, "注：MoE / PCIe 为我们的工程观测，非论文结论", 13, False, FAINT, line=1.0)
    takeaway(s, 6.08, "TPOT 慢，往常不是 Decode 本身慢", AMBER, AMBER_L, h=0.76, size=20)
    page_no(s, n)
    return n


# ============================================================ 20 干扰（时间轴 + 散点）
def interference(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 主因一", "Prefill 插队，打断出字节奏")

    # 时间轴
    card(s, ML, 2.15, CW, 1.92, WHITE, LINE, radius=0.07)
    y = 2.46
    txt(s, ML + 0.3, y + 0.1, 1.3, 0.36, "理想", 17, True, MUTED, line=1.0)
    x = ML + 1.75
    for i in range(11):
        rect(s, x + i * 0.88, y, 0.74, 0.44, TEAL_L)
        txt(s, x + i * 0.88, y + 0.08, 0.74, 0.3, "字", 14, True, TEAL, "c", line=1.0)
    y = 3.28
    txt(s, ML + 0.3, y + 0.1, 1.3, 0.36, "实际", 17, True, RED, line=1.0)
    px = ML + 1.75
    for t in ["d", "d", "d", "P", "d", "d", "d", "P", "d"]:
        if t == "d":
            rect(s, px, y, 0.74, 0.44, TEAL_L)
            txt(s, px, y + 0.08, 0.74, 0.3, "字", 14, True, TEAL, "c", line=1.0)
            px += 0.88
        else:
            rect(s, px, y, 1.8, 0.44, VIO_L)
            txt(s, px, y + 0.08, 1.8, 0.3, "Prefill 占用", 14, True, VIO, "c", line=1.0)
            px += 1.94

    # 散点图
    band(s, ML, 4.24, 6.6, 2.0)
    ax, ay, aw, ah = ML + 1.6, 4.5, 4.6, 1.15
    axes(s, ax, ay, aw, ah, "TPOT", "干扰强度  →", FAINT, 1.5, 15, 14)
    pts01 = [(0.06, 0.1), (0.2, 0.22), (0.3, 0.34), (0.44, 0.44),
             (0.58, 0.6), (0.7, 0.66), (0.84, 0.82), (0.96, 0.92)]
    curve(s, ax, ay, aw, ah, [(0.02, 0.06), (0.98, 0.95)], BLUE, 2.25, dash=True)
    for fx, fy in pts01:
        dot(s, ax + fx * aw, ay + ah - fy * ah, 0.075, AMBER, WHITE, 1.25)
    txt(s, ax + 0.18, ay + 0.02, 2.1, 0.34, "R² = 0.99", 17, True, BLUE, line=1.0)

    rx = ML + 6.9
    rwd = CW - 6.9
    card(s, rx, 4.24, rwd, 2.0, PANEL, None, radius=0.07)
    txt(s, rx + 0.34, 4.5, rwd - 0.68, 0.34, "干扰强度（Decode 期间）", 15, True, MUTED, line=1.0)
    txt(s, rx + 0.34, 4.94, rwd - 0.68, 0.84,
        "插入的 Prefill token 数\n÷ 输出长度", 17, True, INK, line=1.4)
    txt(s, rx + 0.34, 5.84, rwd - 0.68, 0.32, "→ 可预测、可控", 16, True, BLUE, line=1.0)
    page_no(s, n)
    return n


# ============================================================ 21 Chunked Prefill（交叉曲线）
def chunked(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 关键旋钮", "Chunk 大小：在两个指标之间移动")

    band(s, ML, 2.12, 8.1, 3.95)
    ax, ay, aw, ah = ML + 1.5, 2.72, 6.2, 2.5
    axes(s, ax, ay, aw, ah, "延迟", "Chunk 大小  →", FAINT, 1.5, 15, 16)
    curve(s, ax, ay, aw, ah, [(0.02, 0.92), (0.25, 0.62), (0.5, 0.45),
                              (0.75, 0.34), (0.98, 0.28)], BLUE, 3.0)
    curve(s, ax, ay, aw, ah, [(0.02, 0.2), (0.25, 0.3), (0.5, 0.45),
                              (0.75, 0.68), (0.98, 0.92)], AMBER, 3.0)
    legend(s, ax + 0.15, ay - 0.46, [("TTFT", BLUE), ("TPOT", AMBER)], size=16)
    cx, cy = ax + 0.5 * aw, ay + ah - 0.45 * ah
    dot(s, cx, cy, 0.1, WHITE, INK, 2.5)
    txt(s, cx - 1.3, cy - 0.5, 2.6, 0.32, "平衡点", 16, True, INK, "c", line=1.0)

    rx = ML + 8.4
    rwd = CW - 8.4
    card(s, rx, 2.12, rwd, 1.85, WHITE, LINE, radius=0.07)
    rect(s, rx, 2.12, rwd, 0.06, AMBER)
    txt(s, rx + 0.32, 2.42, rwd - 0.64, 0.4, "块大", 21, True, INK, line=1.0)
    txt(s, rx + 0.32, 2.94, rwd - 0.64, 0.8, "产能高 → TTFT ↓\n打断重 → TPOT ↑",
        16, True, BODY, line=1.45)
    card(s, rx, 4.22, rwd, 1.85, WHITE, LINE, radius=0.07)
    rect(s, rx, 4.22, rwd, 0.06, BLUE)
    txt(s, rx + 0.32, 4.52, rwd - 0.64, 0.4, "块小", 21, True, INK, line=1.0)
    txt(s, rx + 0.32, 5.04, rwd - 0.64, 0.8, "打断轻 → TPOT ↓\n产能低 → TTFT ↑",
        16, True, BODY, line=1.45)

    takeaway(s, 6.2, "不是越大越好，而是把预算从一个指标挪给另一个", VIO, VIO_L, h=0.72, size=19)
    page_no(s, n)
    return n


# ============================================================ 22 PD 聚合 vs 分离（矩阵）
def pd_compare(prs, n):
    s = blank(prs)
    header(s, "PART 4 · 架构权衡", "没有普遍更优，只有更适配")

    cols = ["TTFT 松\nTPOT 紧", "TTFT 紧\nTPOT 松", "两者都紧"]
    rows = ["PD 聚合", "PD 分离"]
    cells = [[("↓", "达标率下降", PANEL2, MUTED), ("97%", "胜出", BLUE_L, BLUE),
              ("↓", "明显下降", RED_L, RED)],
             [("98%", "胜出", TEAL_L, TEAL), ("↓", "达标率下降", PANEL2, MUTED),
              ("↓", "明显下降", RED_L, RED)]]
    band(s, ML, 2.12, 7.6, 3.6)
    matrix(s, ML + 0.35, 2.4, 7.0, 3.06, cols, rows, cells,
           col_size=15.5, row_size=20, cell_size=26, sub_size=13, head_h=0.86, lab_w=1.9)

    rx = ML + 7.9
    rwd = CW - 7.9
    items = [("聚合的风险", "TPOT 被干扰", RED), ("分离的风险", "TTFT 被排队", RED),
             ("聚合的长处", "Prefill 产能高", TEAL), ("分离的长处", "可独立扩缩容", TEAL)]
    for i, (k, v, ac) in enumerate(items):
        yy = 2.12 + i * 0.94
        card(s, rx, yy, rwd, 0.76, WHITE, LINE, radius=0.08)
        rect(s, rx, yy, 0.06, 0.76, ac)
        txt(s, rx + 0.26, yy + 0.1, rwd - 0.5, 0.3, k, 14.5, False, MUTED, line=1.0)
        txt(s, rx + 0.26, yy + 0.38, rwd - 0.5, 0.32, v, 18, True, INK, line=1.0)

    takeaway(s, 5.94, "先定「哪个指标不能违约」，再选架构", BLUE, BLUE_L, h=0.82, size=21)
    page_no(s, n)
    return n
