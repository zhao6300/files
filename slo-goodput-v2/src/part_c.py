# -*- coding: utf-8 -*-
"""Part 5 控制手段 + Part 6 系统级优化（精简图形版）"""
from deckkit import *
from charts import *
from pptx.enum.shapes import MSO_SHAPE


# ============================================================ 24 五层框架
def framework(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 总框架", "五层旋钮")

    sh = card(s, ML + 2.9, 2.1, CW - 5.8, 0.82, INK, None, radius=0.12)
    box_text(sh, [("在 SLO 约束下最大化 Goodput", 20, True, WHITE)])

    layers = [("架构层", BLUE, ["PD 聚合 / 分离", "资源配比"]),
              ("调度层", TEAL, ["优先级策略", "批次组合"]),
              ("执行层", VIO, ["Chunk 大小", "内核效率"]),
              ("显存层", AMBER, ["前缀缓存", "KV 放置"]),
              ("通信层", RED, ["并行方式", "NVLink / PCIe"])]
    w = (CW - 4 * 0.24) / 5
    for i, (cn, ac, knobs) in enumerate(layers):
        x = ML + i * (w + 0.24)
        arrow(s, x + w / 2, 2.92, x + w / 2, 3.22, FAINT, 1.5, size="sm")
        card(s, x, 3.28, w, 2.1, WHITE, LINE, radius=0.07)
        rect(s, x, 3.28, w, 0.06, ac)
        txt(s, x + 0.2, 3.6, w - 0.4, 0.4, cn, 21, True, INK, "c", line=1.0)
        for j, k in enumerate(knobs):
            sh2 = card(s, x + 0.2, 4.18 + j * 0.56, w - 0.4, 0.46, PANEL, None, radius=0.2)
            box_text(sh2, [(k, 14.5, True, BODY)])

    takeaway(s, 5.68, "同一份延迟预算的五个分配入口，动一处必看另一处",
             INK, PANEL, h=0.8, size=19)
    page_no(s, n)
    return n


# ============================================================ 25 架构层
def arch_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 架构层", "Prefill 与 Decode 怎么共享资源")

    opts = [("PD 聚合", BLUE, "共用同一批 GPU", "Prefill 产能高", "两阶段互相抢占"),
            ("PD 分离", TEAL, "分池独立部署", "隔离干扰，TPOT 稳", "产能受配比限制"),
            ("混合 / 动态", VIO, "按紧急程度分配落点", "在实例间搬移压力", "调度复杂度高")]
    w = (CW - 0.5) / 3
    for i, (cn, ac, desc, pro, con) in enumerate(opts):
        x = ML + i * (w + 0.25)
        card(s, x, 2.18, w, 3.4, WHITE, LINE, radius=0.07)
        rect(s, x, 2.18, w, 0.06, ac)
        txt(s, x + 0.34, 2.5, w - 0.68, 0.44, cn, 24, True, INK, line=1.0)
        txt(s, x + 0.34, 3.04, w - 0.68, 0.36, desc, 15.5, False, MUTED, line=1.0)
        hline(s, x + 0.34, 3.56, w - 0.68)
        card(s, x + 0.34, 3.74, w - 0.68, 0.74, TEAL_L, None, radius=0.1)
        txt(s, x + 0.5, 3.82, w - 1.0, 0.58, pro, 16.5, True, TEAL, line=1.2)
        card(s, x + 0.34, 4.6, w - 0.68, 0.74, RED_L, None, radius=0.1)
        txt(s, x + 0.5, 4.68, w - 1.0, 0.58, con, 16.5, True, RED, line=1.2)

    takeaway(s, 5.86, "架构跟着 SLO 走，不跟着跑分走", BLUE, BLUE_L, h=0.78, size=20)
    page_no(s, n)
    return n


# ============================================================ 26 调度层
def sched_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 调度层", "谁先算：从「谁先到」到「谁快没时间了」")

    items = [("FCFS", "先来先服务", FAINT, "队头阻塞"),
             ("SJF", "短作业优先", BLUE, "长请求被推迟"),
             ("EDF", "最早截止优先", TEAL, "看不出执行代价"),
             ("剩余预算", "还能等多久", VIO, "依赖预测能力")]
    w = (CW - 3 * 0.3) / 4
    for i, (k, cn, ac, con) in enumerate(items):
        x = ML + i * (w + 0.3)
        card(s, x, 2.2, w, 2.7, WHITE, LINE, radius=0.07)
        rect(s, x, 2.2, w, 0.06, ac)
        txt(s, x + 0.26, 2.52, w - 0.52, 0.44, k, 23, True, INK, line=1.0)
        txt(s, x + 0.26, 3.06, w - 0.52, 0.36, cn, 16, True, ac if i else MUTED, line=1.0)
        hline(s, x + 0.26, 3.56, w - 0.52)
        txt(s, x + 0.26, 3.72, w - 0.52, 0.3, "问题", 14, True, MUTED, line=1.0)
        txt(s, x + 0.26, 4.06, w - 0.52, 0.6, con, 16, False, BODY, line=1.2)
        if i < 3:
            arrow(s, x + w + 0.04, 3.5, x + w + 0.26, 3.5, FAINT, 1.75, size="sm")

    takeaway(s, 5.34, "调度不创造算力，但是提升达标率最便宜的一层", TEAL, TEAL_L, h=0.8, size=20)
    page_no(s, n)
    return n


# ============================================================ 27 延迟预算
def latency_budget(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 核心概念", "延迟预算：还能等多久")

    formula(s, ML, 2.1, CW, 0.82, "剩余预算  =  SLO 目标  −  预计还需时间", PANEL, INK, 24)

    txt(s, ML, 3.12, 6.6, 0.34, "TTFT 目标 = 5 秒", 17, True, MUTED, line=1.0)
    cases = [("请求 A", 1.0, 4.0, TEAL), ("请求 B", 4.5, 0.5, RED)]
    y = 3.56
    for name, used, left, ac in cases:
        card(s, ML, y, 7.4, 1.06, WHITE, LINE, radius=0.07)
        txt(s, ML + 0.3, y + 0.32, 1.3, 0.4, name, 19, True, INK, line=1.0)
        bx, bw_ = ML + 1.7, 3.6
        rect(s, bx, y + 0.3, bw_, 0.46, PANEL2)
        rect(s, bx, y + 0.3, bw_ * used / 5.0, 0.46, FAINT)
        txt(s, bx, y + 0.38, bw_ * used / 5.0, 0.32, "已占用", 13.5, True, WHITE, "c", line=1.0)
        rect(s, bx + bw_ * used / 5.0, y + 0.3, bw_ * left / 5.0, 0.46, ac)
        txt(s, bx + bw_ + 0.3, y + 0.28, 1.75, 0.48, "剩 %.1f s" % left, 20, True, ac, line=1.0)
        y += 1.2

    card(s, ML, 5.96, 7.4, 0.86, AMBER_L, None, radius=0.08)
    txt(s, ML + 0.3, 6.1, 6.8, 0.6, "同样一次 300ms 的 KV 搬运：A 无所谓，B 直接违约",
        19, True, INK, line=1.2)

    # 右侧：预算消耗者
    rx = ML + 7.7
    rwd = CW - 7.7
    sh = card(s, rx, 3.12, rwd, 0.7, VIO, None, radius=0.12)
    box_text(sh, [("剩余预算", 18, True, WHITE)])
    consumers = [("排队", BLUE), ("KV 搬运", AMBER), ("抢占重算", RED)]
    cw2 = (rwd - 0.3) / 3
    for i, (t, ac) in enumerate(consumers):
        x = rx + i * (cw2 + 0.15)
        arrow(s, x + cw2 / 2, 3.82, x + cw2 / 2, 4.06, FAINT, 1.5, size="sm")
        sh2 = card(s, x, 4.12, cw2, 0.72, WHITE, ac, 1.5, radius=0.1)
        box_text(sh2, [(t, 14.5, True, ac)])
    for i in range(3):
        x = rx + i * (cw2 + 0.15)
        arrow(s, x + cw2 / 2, 4.84, rx + rwd / 2, 5.14, FAINT, 1.25, size="sm")
    sh = card(s, rx, 5.2, rwd, 0.7, PANEL, None, radius=0.12)
    box_text(sh, [("预算耗尽 = 违约", 16.5, True, INK)])
    arrow(s, rx + rwd / 2, 5.9, rx + rwd / 2, 6.14, FAINT, 1.5, size="sm")
    sh = card(s, rx, 6.2, rwd, 0.62, INK, None, radius=0.12)
    box_text(sh, [("Goodput ↓", 17, True, WHITE)])
    page_no(s, n)
    return n


# ============================================================ 28 执行 / 显存 / 通信
def exec_layer(prs, n):
    s = blank(prs)
    header(s, "PART 5 · 执行 · 显存 · 通信", "底层优化要翻译成 SLO 语言")

    groups = [("执行层", VIO, ["算子与注意力实现", "Chunk / Batch"], "主要影响 TTFT"),
              ("显存层", AMBER, ["前缀缓存复用", "KV 放置与卸载"], "两者都影响"),
              ("通信层", RED, ["TP / EP 通信量", "NVLink / PCIe"], "主要影响 TPOT")]
    w = (CW - 0.5) / 3
    for i, (title, ac, items, tagt) in enumerate(groups):
        x = ML + i * (w + 0.25)
        card(s, x, 2.18, w, 2.5, WHITE, LINE, radius=0.07)
        rect(s, x, 2.18, w, 0.06, ac)
        txt(s, x + 0.34, 2.5, w - 0.68, 0.44, title, 23, True, INK, line=1.0)
        pill(s, x + 0.34, 3.04, 2.3, 0.42, tagt, 13.5, True, WHITE, ac, ac, 1.25)
        hline(s, x + 0.34, 3.64, w - 0.68)
        for j, it in enumerate(items):
            ty = 3.8 + j * 0.44
            rect(s, x + 0.36, ty + 0.13, 0.12, 0.12, ac)
            txt(s, x + 0.58, ty, w - 0.96, 0.38, it, 16, False, BODY, line=1.0)

    txt(s, ML, 4.94, CW, 0.34, "以通信为例，看它怎么传导到业务结果", 16, True, MUTED, line=1.0)
    chain = [("通信变慢", RED_L, RED), ("单步变长", AMBER_L, AMBER), ("TPOT ↑", AMBER_L, AMBER),
             ("达标率 ↓", RED_L, RED), ("Goodput ↓", INK, WHITE)]
    w2 = (CW - 4 * 0.3) / 5
    for i, (t, fill, fc) in enumerate(chain):
        x = ML + i * (w2 + 0.3)
        sh = card(s, x, 5.36, w2, 0.72, fill, None, radius=0.14)
        box_text(sh, [(t, 17, True, fc)])
        if i < 4:
            arrow(s, x + w2 + 0.04, 5.72, x + w2 + 0.26, 5.72, FAINT, 1.75, size="sm")

    takeaway(s, 6.3, "任何优化都要回答：省下了哪个指标的预算", VIO, VIO_L, h=0.68, size=19)
    page_no(s, n)
    return n


# ============================================================ 30 全景图
def overview(prs, n):
    s = blank(prs)
    header(s, "PART 6 · 全景", "从负载到产能")

    fx, fw = ML, 7.3
    sh = card(s, fx + 1.4, 2.1, fw - 2.8, 0.62, PANEL, None, radius=0.12)
    box_text(sh, [("业务负载", 17, True, INK)])
    cw2 = (fw - 0.4) / 2
    arrow(s, fx + fw / 2 - 1.2, 2.72, fx + cw2 / 2, 2.94, FAINT, 1.5, size="sm")
    arrow(s, fx + fw / 2 + 1.2, 2.72, fx + cw2 + 0.4 + cw2 / 2, 2.94, FAINT, 1.5, size="sm")

    rows = [(("Prefill", VIO_L, VIO), ("Decode", AMBER_L, AMBER)),
            (("TTFT", VIO, WHITE), ("TPOT", AMBER, WHITE))]
    y = 3.0
    for r, row in enumerate(rows):
        for i, (t, fill, fc) in enumerate(row):
            x = fx + i * (cw2 + 0.4)
            sh = card(s, x, y, cw2, 0.68, fill, None, radius=0.12)
            box_text(sh, [(t, 20 if r else 18, True, fc)])
            arrow(s, x + cw2 / 2, y + 0.68, x + cw2 / 2, y + 0.9, FAINT, 1.5, size="sm")
        y += 0.9

    txt(s, fx, 4.86, cw2, 0.3, "排队 · KV · 计算", 14, True, VIO, "c", line=1.0)
    txt(s, fx + cw2 + 0.4, 4.86, cw2, 0.3, "带宽 · 干扰 · 通信", 14, True, AMBER, "c", line=1.0)
    arrow(s, fx + cw2 / 2, 5.2, fx + fw / 2 - 1.2, 5.42, FAINT, 1.5, size="sm")
    arrow(s, fx + cw2 + 0.4 + cw2 / 2, 5.2, fx + fw / 2 + 1.2, 5.42, FAINT, 1.5, size="sm")
    sh = card(s, fx + 1.0, 5.48, fw - 2.0, 0.66, PANEL2, None, radius=0.12)
    box_text(sh, [("SLO 达标率", 18, True, INK)])
    arrow(s, fx + fw / 2, 6.14, fx + fw / 2, 6.34, FAINT, 1.75)
    sh = card(s, fx + 1.7, 6.4, fw - 3.4, 0.72, INK, None, radius=0.12)
    box_text(sh, [("Goodput", 22, True, WHITE)])

    rx = ML + fw + 0.4
    rwd = CW - fw - 0.4
    card(s, rx, 2.1, rwd, 5.02, PANEL, None, radius=0.07)
    txt(s, rx + 0.32, 2.36, rwd - 0.64, 0.34, "我们能动的五层", 17, True, INK, line=1.0)
    knobs = [("架构层", BLUE), ("调度层", TEAL), ("执行层", VIO), ("显存层", AMBER), ("通信层", RED)]
    y = 2.88
    for t, ac in knobs:
        card(s, rx + 0.32, y, rwd - 0.64, 0.66, WHITE, LINE, radius=0.1)
        rect(s, rx + 0.32, y, 0.06, 0.66, ac)
        txt(s, rx + 0.56, y + 0.16, rwd - 1.0, 0.34, t, 18, True, INK, line=1.0)
        y += 0.78
    arrow(s, rx + 0.12, 4.4, ML + fw + 0.14, 4.4, FAINT, 1.5, dash=True, size="sm")
    txt(s, rx + 0.32, 6.76, rwd - 0.64, 0.3, "动一处，看另一处", 14, True, MUTED, "c", line=1.0)
    page_no(s, n)
    return n


# ============================================================ 31 工作映射
def our_work(prs, n):
    s = blank(prs)
    header(s, "PART 6 · 落地", "我们的工作在图上的位置")

    rows = [("我们的工作", "层", "改善", "风险"),
            ("PD 分离 / 配比", "架构", "TPOT 稳定", "Prefill 产能不足"),
            ("Chunked Prefill", "执行", "两者的平衡点", "块太小伤产能"),
            ("KV 卸载 / LMCache", "显存", "长上下文成本", "恢复延迟拖高 TTFT"),
            ("调度与批次", "调度", "达标率、长尾", "长请求被饿死"),
            ("TP / EP 通信", "通信", "单步时间", "通信抖动"),
            ("GPU 利用率", "执行", "吞吐与成本", "利用率拉满反降 Goodput")]
    grid_table(s, ML, 2.05, CW, [3.1, 1.0, 2.5, 3.4], rows, row_h=0.55, head_h=0.56,
               align=["l", "c", "l", "l"], size=16, head_size=15)

    takeaway(s, 6.14, "不说「内核快了 X%」，而说「同样 SLO 下多接 Y% 请求」",
             INK, PANEL, h=0.78, size=19, icon="汇报口径")
    page_no(s, n)
    return n


# ============================================================ 32 结语
def closing(prs, n):
    s = blank(prs)
    rect(s, 0, 0, SW, SH, WHITE)
    rect(s, 0, 0, SW, 0.18, INK)
    txt(s, ML, 1.2, CW, 0.34, "小结", 14, True, BLUE, line=1.0)
    txt(s, ML, 1.72, CW, 0.7, "不是让某个内核更快，", 34, True, INK, line=1.25)
    txt(s, ML, 2.56, CW, 1.5, "而是在给定 TTFT / TPOT 下，\n让系统承载更多请求。",
        34, True, BLUE, line=1.3)

    formula(s, ML, 4.36, CW, 1.05,
            "最大化 Goodput      s.t.   TTFT ≤ 目标   且   TPOT ≤ 目标", PANEL, INK, 24)

    items = [("统一语言", "TTFT / TPOT / 达标率", BLUE),
             ("统一判据", "达标请求变多了吗", TEAL),
             ("统一地图", "五层旋钮互相牵制", AMBER)]
    w = (CW - 0.5) / 3
    for i, (t, d, ac) in enumerate(items):
        x = ML + i * (w + 0.25)
        card(s, x, 5.66, w, 1.06, WHITE, LINE, radius=0.07)
        rect(s, x, 5.66, 0.06, 1.06, ac)
        txt(s, x + 0.3, 5.84, w - 0.56, 0.36, t, 18, True, INK, line=1.0)
        txt(s, x + 0.3, 6.24, w - 0.56, 0.34, d, 15, False, BODY, line=1.0)

    txt(s, ML, 6.94, CW, 0.34, "谢谢  ·  欢迎讨论", 15, True, MUTED, line=1.0)
    return n
