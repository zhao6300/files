# -*- coding: utf-8 -*-
"""生成《大模型推理服务：SLO 与 Goodput》技术分享 PPT（精简图形版）"""
import os
import sys
from deckkit import new_deck, section, BLUE, TEAL, AMBER, VIO, BLUE_L, TEAL_L, AMBER_L, VIO_L
import part_a as A
import part_b as B
import part_c as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "LLM-Inference-SLO-Goodput-v2.pptx")


def main():
    prs = new_deck()
    n = 0

    def add(fn):
        nonlocal n
        n += 1
        fn(prs, n)

    def sec(num, title, desc, ac, al):
        nonlocal n
        n += 1
        section(prs, num, title, desc, n, ac, al)

    add(A.cover)
    add(A.summary)
    add(A.roadmap)

    sec("01", "为什么需要 SLO", "推理系统到底在优化什么", BLUE, BLUE_L)
    add(A.why_slo)
    add(A.analogy)

    sec("02", "核心指标", "TTFT · TPOT · 达标率 · Goodput", BLUE, BLUE_L)
    add(A.two_phases)
    add(A.ttft)
    add(A.tpot)
    add(A.tail)
    add(A.goodput)

    sec("03", "TTFT 由什么决定", "为什么第一个字等很久", TEAL, TEAL_L)
    add(B.ttft_pipeline)
    add(B.queue_slide)
    add(B.prefill_capacity)
    add(B.kv_ttft)

    sec("04", "TPOT 由什么决定", "谁抢走了出字的时间", AMBER, AMBER_L)
    add(B.tpot_mech)
    add(B.interference)
    add(B.chunked)
    add(B.pd_compare)

    sec("05", "五层控制手段", "架构 · 调度 · 执行 · 显存 · 通信", VIO, VIO_L)
    add(C.framework)
    add(C.arch_layer)
    add(C.sched_layer)
    add(C.latency_budget)
    add(C.exec_layer)

    sec("06", "系统级优化", "在 SLO 约束下最大化 Goodput", BLUE, BLUE_L)
    add(C.overview)
    add(C.our_work)
    add(C.closing)

    from notes import NOTES
    for i, sld in enumerate(prs.slides, 1):
        if i in NOTES:
            sld.notes_slide.notes_text_frame.text = NOTES[i]

    prs.save(OUT)
    print("slides:", len(prs.slides.__iter__.__self__._sldIdLst), "->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
