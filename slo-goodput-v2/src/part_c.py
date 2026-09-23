# -*- coding: utf-8 -*-
"""Part 5 控制手段 + Part 6 系统级优化 + 结语"""
from deckkit import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 25 五层框架
def framework(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 总框架", "系统上的「旋钮」可以分成五层",
           "这张图也是我们整体优化工作的地图")

    sh = card(s, ML + 2.6, 2.0, CW - 5.2, 0.72, INK, None, radius=0.12)
    box_text(sh, [("目标：在 TTFT / TPOT 约束下，最大化 Goodput", 15.5, True, WHITE)])

    layers = [
        ("架构层", "Architecture", BLUE, ["PD 聚合 / 分离", "Prefill : Decode 配比", "实例规格与数量"]),
        ("调度层", "Scheduling", TEAL, ["队列优先级策略", "批次如何组合", "抢占与让行"]),
        ("执行层", "Execution", VIO, ["Chunk 大小", "Batch 大小", "算子 / 内核效率"]),
        ("显存层", "Memory / KV", AMBER, ["前缀缓存复用", "KV 放在哪一级", "卸载与恢复策略"]),
        ("通信层", "Communication", RED, ["并行切分方式", "All-to-All 与负载均衡", "NVLink / PCIe 路径"]),
    ]
    w = (CW - 4 * 0.2) / 5
    for i, (cn, en, ac, knobs) in enumerate(layers):
        x = ML + i * (w + 0.2)
        arrow(s, x + w / 2, 2.72, x + w / 2, 3.0, FAINT, 1.25, size="sm")
        card(s, x, 3.06, w, 2.5, WHITE, LINE, radius=0.07)
        rect(s, x, 3.06, w, 0.05, ac)
        txt(s, x + 0.22, 3.28, w - 0.44, 0.3, cn, 15, True, INK, line=1.0)
        txt(s, x + 0.22, 3.6, w - 0.44, 0.24, en, 9.5, False, FAINT, line=1.0)
        hline(s, x + 0.22, 3.92, w - 0.44)
        for j, k in enumerate(knobs):
            ty = 4.08 + j * 0.44
            sh2 = card(s, x + 0.22, ty, w - 0.44, 0.36, PANEL, None, radius=0.2)
            box_text(sh2, [(k, 10.5, True, BODY)])
        txt(s, x + 0.22, 5.4, w - 0.44, 0.2, "", 9, False, FAINT, line=1.0)

    takeaway(s, 5.78, "这五层不是并列的备选项，而是同一个延迟预算的五个分配入口——动任何一个，都会影响另一个指标。",
             INK, PANEL, h=0.62)
    txt(s, ML, 6.52, CW, 0.26, "后续几页分别说明每一层在做什么，以及代价是什么。", 11, False, FAINT, line=1.0)
    page_no(s, n)
    return n


# ============================================================ 26 架构层
def arch_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 第一层", "架构层：决定 Prefill 和 Decode 如何共享资源")

    opts = [("PD 聚合", "Aggregation", BLUE,
             "Prefill 与 Decode 共用同一批 GPU",
             ["Prefill 可借用全部算力", "产能高 → TTFT 更容易达标"],
             ["两阶段互相抢占", "TPOT 容易抖动"]),
            ("PD 分离", "Disaggregation", TEAL,
             "Prefill 与 Decode 分池部署",
             ["彻底隔离干扰", "TPOT 稳定，可独立扩缩容"],
             ["Prefill 产能被配比限制", "KV 需要跨实例传输"]),
            ("混合 / 动态", "Hybrid", VIO,
             "不同实例承担不同偏重，再由调度分配请求",
             ["按请求的紧急程度选择落点", "把延迟压力在实例间「搬移」"],
             ["调度复杂度显著上升", "需要准确的预测能力"])]
    w = (CW - 0.44) / 3
    for i, (cn, en, ac, desc, pros, cons) in enumerate(opts):
        x = ML + i * (w + 0.22)
        card(s, x, 2.0, w, 3.96, WHITE, LINE, radius=0.07)
        rect(s, x, 2.0, w, 0.055, ac)
        txt(s, x + 0.3, 2.24, w - 0.6, 0.34, cn, 18, True, INK, line=1.0)
        txt(s, x + 0.3, 2.62, w - 0.6, 0.24, en, 10, False, FAINT, line=1.0)
        txt(s, x + 0.3, 2.94, w - 0.6, 0.5, desc, 12, False, BODY, line=1.3)
        hline(s, x + 0.3, 3.56, w - 0.6)
        txt(s, x + 0.3, 3.7, w - 0.6, 0.26, "换来什么", 11, True, TEAL, line=1.0)
        yy = 4.0
        for p in pros:
            rect(s, x + 0.32, yy + 0.08, 0.1, 0.1, TEAL)
            txt(s, x + 0.52, yy, w - 0.9, 0.42, p, 11.5, False, BODY, line=1.2)
            yy += 0.42
        txt(s, x + 0.3, yy + 0.04, w - 0.6, 0.26, "代价是什么", 11, True, RED, line=1.0)
        yy += 0.34
        for c in cons:
            rect(s, x + 0.32, yy + 0.08, 0.1, 0.1, RED)
            txt(s, x + 0.52, yy, w - 0.9, 0.42, c, 11.5, False, BODY, line=1.2)
            yy += 0.42

    takeaway(s, 6.16, "架构选择要跟着 SLO 走：先明确「哪个指标更不能违约」，再决定部署形态与资源配比。",
             BLUE, BLUE_L)
    page_no(s, n)
    return n


# ============================================================ 27 调度层
def sched_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 第二层", "调度层：同样的算力，谁先算、和谁一起算")

    items = [("FCFS", "先来先服务", FAINT,
              "按到达顺序执行", "实现简单，公平", "队头阻塞：一个大请求拖垮一片"),
             ("SJF", "短作业优先", BLUE,
              "优先执行预计更快的请求", "多数请求延迟明显下降", "长上下文请求可能被长期推迟"),
             ("EDF", "最早截止优先", TEAL,
              "按 SLO 截止时间排序", "直接对齐 SLO 目标", "同截止时间下，无法区分执行代价"),
             ("Latency Budget", "剩余预算优先", VIO,
              "按「还剩多少时间可用」排序", "同时考虑目标与剩余工作量", "依赖对剩余服务时间的预测")]
    w = (CW - 0.66) / 4
    for i, (k, cn, ac, how, pro, con) in enumerate(items):
        x = ML + i * (w + 0.22)
        card(s, x, 2.0, w, 3.2, WHITE, LINE if i else LINE, radius=0.07)
        rect(s, x, 2.0, w, 0.05, ac)
        txt(s, x + 0.26, 2.22, w - 0.52, 0.3, k, 16, True, INK, line=1.0)
        txt(s, x + 0.26, 2.56, w - 0.52, 0.26, cn, 11.5, True, ac, line=1.0)
        hline(s, x + 0.26, 2.9, w - 0.52)
        txt(s, x + 0.26, 3.04, w - 0.52, 0.5, how, 11.5, False, BODY, line=1.25)
        card(s, x + 0.26, 3.62, w - 0.52, 0.66, TEAL_L, None, radius=0.1)
        txt(s, x + 0.4, 3.7, w - 0.8, 0.5, pro, 10.5, True, TEAL, line=1.2)
        card(s, x + 0.26, 4.36, w - 0.52, 0.7, RED_L, None, radius=0.1)
        txt(s, x + 0.4, 4.44, w - 0.8, 0.56, con, 10.5, True, RED, line=1.2)
        if i < 3:
            txt(s, x + w, 2.9, 0.22, 0.3, "›", 16, True, FAINT, "c", line=1.0)

    card(s, ML, 5.36, CW, 0.7, PANEL, None, radius=0.1)
    tb, tf = textbox(s, ML + 0.3, 5.36, CW - 0.6, 0.7, "m")
    rich(tf, [("演进方向：  ", {"bold": True, "color": MUTED, "size": 12}),
              ("从「谁先到」→「谁更短」→「谁更急」→「谁快没时间了」",
               {"bold": True, "color": INK, "size": 14.5})], first=True, line=1.2)

    takeaway(s, 6.2, "调度不创造算力，但它决定延迟预算怎么分配——这是提升达标率成本最低的一层。",
             TEAL, TEAL_L, h=0.6)
    page_no(s, n)
    return n


# ============================================================ 28 Latency Budget
def latency_budget(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 核心概念", "延迟预算：把「还能等多久」变成可计算的量",
           "它能把排队、KV 搬运、抢占这些看似无关的操作放到同一把尺子上比较")

    formula(s, ML, 1.98, CW, 0.66,
            "剩余延迟预算  =  SLO 目标  −  预计还需要的服务时间", PANEL, INK, 16)

    txt(s, ML, 2.84, 6.6, 0.28, "举个例子：TTFT 目标 = 5 秒", 12.5, True, MUTED, line=1.0)
    cases = [("请求 A", "预计还需 1 秒", 1.0, 4.0, TEAL, "预算充裕"),
             ("请求 B", "预计还需 4.5 秒", 4.5, 0.5, RED, "预算紧张")]
    y = 3.2
    for name, need, used, left, ac, tag in cases:
        card(s, ML, y, 6.6, 1.0, WHITE, LINE, radius=0.07)
        txt(s, ML + 0.26, y + 0.12, 1.1, 0.28, name, 14, True, INK, line=1.0)
        tb, tf = textbox(s, ML + 0.26, y + 0.42, 1.78, 0.36)
        rich(tf, [(need + "  ", {"color": MUTED, "size": 10.5}),
                  ("剩余 %.1f s" % left, {"bold": True, "color": ac, "size": 11.5})],
             first=True, line=1.0)
        bx, bw_ = ML + 2.1, 3.1
        rect(s, bx, y + 0.24, bw_, 0.34, PANEL2)
        rect(s, bx, y + 0.24, bw_ * used / 5.0, 0.34, FAINT)
        txt(s, bx, y + 0.28, bw_ * used / 5.0, 0.26, "已占用", 9.5, True, WHITE, "c", line=1.0)
        rect(s, bx + bw_ * used / 5.0, y + 0.24, bw_ * left / 5.0, 0.34, ac)
        txt(s, bx, y + 0.64, bw_, 0.24, "←   SLO 目标 5 秒   →", 9, False, FAINT, "c", line=1.0)
        pill(s, bx + bw_ + 0.22, y + 0.22, 1.1, 0.38, tag, 10.5, True, WHITE, ac, ac, 1.0)
        y += 1.12

    card(s, ML, 5.46, 6.6, 0.84, AMBER_L, None, radius=0.08)
    txt(s, ML + 0.26, 5.56, 6.1, 0.68,
        "现在要做一次耗时 300ms 的 KV 搬运：对 A 完全可以接受；对 B 就可能直接导致违约。",
        12.5, True, INK, line=1.3)

    # 右侧：预算的消耗者
    rx = ML + 6.9
    rwd = CW - 6.9
    txt(s, rx, 2.84, rwd, 0.28, "谁在消耗这份预算", 12.5, True, INK, line=1.0)
    sh = card(s, rx, 3.2, rwd, 0.58, VIO, None, radius=0.12)
    box_text(sh, [("请求的剩余延迟预算", 13.5, True, WHITE)])
    consumers = [("排队等待", BLUE), ("KV 搬运 / 恢复", AMBER), ("被抢占与重算", RED)]
    cw2 = (rwd - 0.3) / 3
    for i, (t, ac) in enumerate(consumers):
        x = rx + i * (cw2 + 0.15)
        arrow(s, x + cw2 / 2, 3.78, x + cw2 / 2, 3.98, FAINT, 1.25, size="sm")
        sh2 = card(s, x, 4.04, cw2, 0.62, WHITE, ac, 1.25, radius=0.1)
        box_text(sh2, [(t, 11, True, ac)])
    for i in range(3):
        x = rx + i * (cw2 + 0.15)
        arrow(s, x + cw2 / 2, 4.66, rx + rwd / 2, 4.9, FAINT, 1.0, size="sm")
    sh = card(s, rx, 4.96, rwd, 0.58, PANEL, None, radius=0.12)
    box_text(sh, [("预算耗尽 → SLO 违约", 13, True, INK)])
    arrow(s, rx + rwd / 2, 5.54, rx + rwd / 2, 5.74, FAINT, 1.25, size="sm")
    sh = card(s, rx, 5.8, rwd, 0.5, INK, None, radius=0.12)
    box_text(sh, [("Goodput 下降", 12.5, True, WHITE)])

    takeaway(s, 6.4, "同一个系统动作，对不同请求的价值完全不同——这是从「优化平均」走向「优化达标」的关键转变。",
             VIO, VIO_L, h=0.5, size=13)
    page_no(s, n)
    return n


# ============================================================ 29 KV / 显存层
def kv_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 第四层", "显存与 KV 层：省计算，但别把时间省到搬运上去")

    pillars = [("命中与复用", AMBER, ["前缀缓存（多轮对话 / 系统提示）",
                                  "相同前缀的请求共享 KV",
                                  "命中率是手段，不是目的"]),
               ("放在哪一级", BLUE, ["HBM：最快，但容量最贵",
                                 "DRAM：容量大，搬运可接受",
                                 "NVMe：容量最大，恢复最慢"]),
               ("怎么搬过来", TEAL, ["搬运路径与带宽（NVLink / PCIe）",
                                 "是否能与计算重叠",
                                 "什么时候「重算」比「搬运」更划算"])]
    w = (CW - 0.44) / 3
    for i, (title, ac, items) in enumerate(pillars):
        x = ML + i * (w + 0.22)
        card(s, x, 2.0, w, 2.3, WHITE, LINE, radius=0.07)
        rect(s, x, 2.0, w, 0.05, ac)
        sh = shape(s, MSO_SHAPE.OVAL, x + 0.3, 2.26, 0.34, 0.34, ac, None)
        box_text(sh, [(str(i + 1), 12, True, WHITE)])
        txt(s, x + 0.76, 2.3, w - 1.0, 0.3, title, 15, True, INK, line=1.0)
        hline(s, x + 0.3, 2.78, w - 0.6)
        for j, it in enumerate(items):
            ty = 2.94 + j * 0.42
            rect(s, x + 0.32, ty + 0.1, 0.1, 0.1, ac)
            txt(s, x + 0.52, ty, w - 0.9, 0.4, it, 11.5, False, BODY, line=1.2)

    card(s, ML, 4.5, CW, 1.5, WHITE, AMBER, 1.25, radius=0.07)
    txt(s, ML + 0.34, 4.7, CW - 0.68, 0.3, "一个容易走偏的优化目标", 12, True, AMBER, line=1.0)
    lw = (CW - 1.4) / 2
    card(s, ML + 0.34, 5.06, lw, 0.76, RED_L, None, radius=0.1)
    txt(s, ML + 0.5, 5.14, lw - 0.32, 0.6, "× 只看：缓存命中率提升了多少", 13, True, RED, line=1.25)
    arrow(s, ML + 0.34 + lw + 0.1, 5.44, ML + 0.34 + lw + 0.6, 5.44, FAINT, 1.5)
    card(s, ML + 0.34 + lw + 0.72, 5.06, lw, 0.76, TEAL_L, None, radius=0.1)
    txt(s, ML + 0.5 + lw + 0.72, 5.14, lw - 0.32, 0.6, "√ 要看：达标请求数是否真的增加",
        13, True, TEAL, line=1.25)

    takeaway(s, 6.16, "命中率 ≠ 更低的 TTFT。KV 优化要连搬运代价一起算，必要时「重算」才是更优解。",
             AMBER, AMBER_L)
    page_no(s, n)
    return n


# ============================================================ 30 执行与通信层
def exec_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 第三 / 第五层", "执行与通信层：底层优化最终也要翻译成 SLO 语言")

    groups = [("Prefill 侧", VIO, ["矩阵运算效率（GEMM）", "FlashAttention 等注意力实现",
                                "Chunk 大小 / Batch 大小", "张量并行切分"], "主要影响 TTFT"),
              ("Decode 侧", AMBER, ["显存带宽利用率", "KV Cache 访问模式",
                                  "注意力内核效率", "批次调度与组合"], "主要影响 TPOT"),
              ("MoE 与通信", RED, ["专家并行（EP）与 All-to-All", "token 分发与专家负载均衡",
                                "NCCL 通信效率", "NVLink / PCIe 带宽差异"], "主要影响 TPOT")]
    w = (CW - 0.44) / 3
    for i, (title, ac, items, tag) in enumerate(groups):
        x = ML + i * (w + 0.22)
        card(s, x, 2.0, w, 2.66, WHITE, LINE, radius=0.07)
        rect(s, x, 2.0, w, 0.05, ac)
        txt(s, x + 0.3, 2.24, w - 0.6, 0.32, title, 15.5, True, INK, line=1.0)
        pill(s, x + 0.3, 2.62, 1.75, 0.34, tag, 10, True, WHITE, ac, ac, 1.0)
        hline(s, x + 0.3, 3.1, w - 0.6)
        for j, it in enumerate(items):
            ty = 3.26 + j * 0.32
            rect(s, x + 0.32, ty + 0.1, 0.1, 0.1, ac)
            txt(s, x + 0.52, ty, w - 0.9, 0.3, it, 11.5, False, BODY, line=1.0)

    txt(s, ML, 4.86, CW, 0.28, "以通信为例：底层指标是如何传导到业务结果的", 12.5, True, MUTED, line=1.0)
    chain = [("跨卡通信变慢", RED_L, RED), ("单步 Decode 时间变长", AMBER_L, AMBER),
             ("TPOT 上升", AMBER_L, AMBER), ("SLO 达标率下降", RED_L, RED),
             ("Goodput 下降", INK, WHITE)]
    w2 = (CW - 4 * 0.28) / 5
    for i, (t, fill, fc) in enumerate(chain):
        x = ML + i * (w2 + 0.28)
        sh = card(s, x, 5.22, w2, 0.56, fill, None, radius=0.14)
        box_text(sh, [(t, 12, True, fc)])
        if i < 4:
            arrow(s, x + w2 + 0.03, 5.5, x + w2 + 0.25, 5.5, FAINT, 1.25, size="sm")

    takeaway(s, 6.02, "任何底层优化，都要能回答一句话：它把哪个指标的延迟预算省下来了？",
             VIO, VIO_L, h=0.62)
    txt(s, ML, 6.72, CW, 0.24, "注：MoE / PCIe 相关内容属于我们的工程扩展维度，不是论文已验证的结论。",
        10, False, FAINT, line=1.0)
    page_no(s, n)
    return n


# ============================================================ 32 总览图
def overview(prs, n):
    s = blank(prs)
    header(s, "PART 6 · 全景", "一张图看懂：从负载特征到最终产能")

    fx, fw = ML, 7.5
    # Workload
    sh = card(s, fx + 1.5, 1.94, fw - 3.0, 0.5, PANEL, None, radius=0.12)
    box_text(sh, [("业务负载（输入有多长、输出有多长）", 12.5, True, INK)])
    cw2 = (fw - 0.3) / 2
    arrow(s, fx + fw / 2 - 1.2, 2.44, fx + cw2 / 2, 2.62, FAINT, 1.25, size="sm")
    arrow(s, fx + fw / 2 + 1.2, 2.44, fx + cw2 + 0.3 + cw2 / 2, 2.62, FAINT, 1.25, size="sm")

    pairs = [(("Prefill 阶段", VIO_L, VIO), ("Decode 阶段", AMBER_L, AMBER)),
             (("TTFT", VIO, WHITE), ("TPOT", AMBER, WHITE))]
    y = 2.68
    for row in pairs:
        for i, (t, fill, fc) in enumerate(row):
            x = fx + i * (cw2 + 0.3)
            sh = card(s, x, y, cw2, 0.56, fill, None, radius=0.12)
            box_text(sh, [(t, 14 if y > 3 else 12.5, True, fc)])
            arrow(s, x + cw2 / 2, y + 0.56, x + cw2 / 2, y + 0.74, FAINT, 1.25, size="sm")
        y += 0.74

    # 影响因素小字
    txt(s, fx, 4.16, cw2, 0.26, "排队 · KV 读取 · 计算 · 传输", 10.5, True, VIO, "c", line=1.0)
    txt(s, fx + cw2 + 0.3, 4.16, cw2, 0.26, "带宽 · 干扰 · 通信 · 调度", 10.5, True, AMBER, "c", line=1.0)

    arrow(s, fx + cw2 / 2, 4.44, fx + fw / 2 - 1.2, 4.62, FAINT, 1.25, size="sm")
    arrow(s, fx + cw2 + 0.3 + cw2 / 2, 4.44, fx + fw / 2 + 1.2, 4.62, FAINT, 1.25, size="sm")
    sh = card(s, fx + 1.2, 4.68, fw - 2.4, 0.56, PANEL2, None, radius=0.12)
    box_text(sh, [("SLO 达标率（两个指标都满足的比例）", 12.5, True, INK)])
    arrow(s, fx + fw / 2, 5.24, fx + fw / 2, 5.42, FAINT, 1.5)
    sh = card(s, fx + 1.8, 5.48, fw - 3.6, 0.72, INK, None, radius=0.12)
    box_text(sh, [("Goodput", 18, True, WHITE)])
    txt(s, fx, 6.28, fw, 0.26, "= 达标前提下的真实产能", 11, True, MUTED, "c", line=1.0)

    # 右侧：手段
    rx = ML + fw + 0.4
    rwd = CW - fw - 0.4
    card(s, rx, 1.94, rwd, 4.52, PANEL, None, radius=0.07)
    txt(s, rx + 0.28, 2.14, rwd - 0.56, 0.28, "我们能动的五层旋钮", 13, True, INK, line=1.0)
    knobs = [("架构层", "PD 形态与资源配比", BLUE), ("调度层", "优先级 · 批次 · 抢占", TEAL),
             ("执行层", "Chunk · Batch · 内核", VIO), ("显存层", "前缀缓存 · KV 放置与卸载", AMBER),
             ("通信层", "并行方式 · NVLink / PCIe", RED)]
    y = 2.5
    for t, d, ac in knobs:
        card(s, rx + 0.28, y, rwd - 0.56, 0.62, WHITE, LINE, radius=0.1)
        rect(s, rx + 0.28, y, 0.05, 0.62, ac)
        txt(s, rx + 0.48, y + 0.06, rwd - 0.9, 0.26, t, 12.5, True, INK, line=1.0)
        txt(s, rx + 0.48, y + 0.33, rwd - 0.9, 0.24, d, 10.5, False, BODY, line=1.0)
        y += 0.7
    arrow(s, rx + 0.1, 4.2, ML + fw + 0.12, 4.2, FAINT, 1.25, dash=True, size="sm")
    txt(s, rx + 0.28, 6.04, rwd - 0.56, 0.34, "每一次调整，都是在两个指标之间重新分配预算",
        10.5, True, MUTED, line=1.2)
    page_no(s, n)
    return n


# ============================================================ 33 工作映射
def our_work(prs, n):
    s = blank(prs)
    header(s, "PART 6 · 落地", "我们已有的工作，在这张地图上的位置",
           "同一个框架下，这些工作不再是零散的优化点")

    rows = [("我们的工作", "属于哪一层", "主要改善", "需要同时盯住的风险"),
            ("PD 分离 / 资源配比调整", "架构层", "TPOT 稳定性", "Prefill 产能不足导致 TTFT 恶化"),
            ("Chunked Prefill 调优", "执行层", "TTFT 与 TPOT 的平衡点", "块太小会牺牲 Prefill 产能"),
            ("KV Cache 分析与卸载（LMCache）", "显存层", "长上下文的 Prefill 成本", "深层恢复延迟反而拖高 TTFT"),
            ("调度与批次策略", "调度层", "整体达标率、长尾", "长请求被饿死、公平性"),
            ("TP / EP 与 MoE 通信优化", "通信层", "单步 Decode 时间", "通信与负载不均带来的抖动"),
            ("GPU 利用率提升", "执行层", "吞吐与成本", "利用率拉满可能反而降低 Goodput")]
    grid_table(s, ML, 2.0, CW, [3.4, 1.4, 2.4, 3.4], rows, row_h=0.52, head_h=0.5,
               align=["l", "c", "l", "l"], size=11.5)

    card(s, ML, 5.94, CW, 0.72, PANEL, None, radius=0.1)
    tb, tf = textbox(s, ML + 0.3, 5.94, CW - 0.6, 0.72, "m")
    rich(tf, [("建议的汇报口径  ｜  ", {"bold": True, "color": MUTED, "size": 12}),
              ("不说「我们把某个内核优化了 X%」，而说「在同样的 SLO 下，这套系统能多承载 Y% 的请求」。",
               {"bold": True, "color": INK, "size": 13.5})], first=True, line=1.25)
    page_no(s, n)
    return n


# ============================================================ 34 结语
def closing(prs, n):
    s = blank(prs)
    rect(s, 0, 0, SW, SH, WHITE)
    rect(s, 0, 0, SW, 0.16, INK)
    txt(s, ML, 1.1, CW, 0.28, "小结", 11.5, True, BLUE, line=1.0)
    txt(s, ML, 1.5, CW, 1.4,
        "推理系统优化的最终目标，\n不是让某一个内核更快，",
        28, True, INK, line=1.32)
    txt(s, ML, 2.86, CW, 0.72,
        "而是在给定的 TTFT / TPOT 要求下，让系统承载更多请求。",
        28, True, BLUE, line=1.32)

    formula(s, ML, 3.9, CW, 1.0,
            "最大化  Goodput      约束条件：TTFT ≤ 目标值    且    TPOT ≤ 目标值",
            PANEL, INK, 20)

    items = [("统一语言", "用 TTFT / TPOT / 达标率 / Goodput 对话，而不是各说各的指标", BLUE),
             ("统一判据", "任何优化都要回答：它让达标请求变多了吗", TEAL),
             ("统一地图", "五层旋钮，动一处就要看另一处的代价", AMBER)]
    w = (CW - 0.44) / 3
    for i, (t, d, ac) in enumerate(items):
        x = ML + i * (w + 0.22)
        card(s, x, 5.2, w, 1.12, WHITE, LINE, radius=0.07)
        rect(s, x, 5.2, 0.05, 1.12, ac)
        txt(s, x + 0.26, 5.36, w - 0.5, 0.3, t, 14, True, INK, line=1.0)
        txt(s, x + 0.26, 5.7, w - 0.52, 0.5, d, 11.5, False, BODY, line=1.25)

    txt(s, ML, 6.56, CW, 0.3, "谢谢  ·  欢迎讨论与指正", 13, True, MUTED, line=1.0)
    page_no(s, n)
    return n
