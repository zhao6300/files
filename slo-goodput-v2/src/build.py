# -*- coding: utf-8 -*-
"""生成《大模型推理服务：SLO 与 Goodput》技术分享 PPT"""
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

    def add(fn, *a):
        nonlocal n
        n += 1
        fn(prs, n, *a)

    add(A.cover)
    add(A.summary)
    add(A.roadmap)

    n += 1
    section(prs, "01", "为什么需要 SLO", "推理系统到底在优化什么？\n为什么「跑得快」不等于「服务好」。", n, BLUE, BLUE_L)
    add(A.why_slo)
    add(A.analogy)

    n += 1
    section(prs, "02", "SLO 的核心指标", "TTFT、TPOT、达标率、Goodput\n这四个词说清楚，后面就都好谈了。", n, BLUE, BLUE_L)
    add(A.sla_slo_sli)
    add(A.two_phases)
    add(A.ttft)
    add(A.tpot)
    add(A.tail)
    add(A.goodput)

    n += 1
    section(prs, "03", "TTFT 由什么决定", "为什么用户等了很久才看到第一个字？\n真正的时间花在了哪里。", n, TEAL, TEAL_L)
    add(B.ttft_pipeline)
    add(B.queue_slide)
    add(B.prefill_capacity)
    add(B.kv_ttft)

    n += 1
    section(prs, "04", "TPOT 由什么决定", "为什么生成过程会一顿一顿？\n谁抢走了本该用来出字的时间。", n, AMBER, AMBER_L)
    add(B.tpot_mech)
    add(B.interference)
    add(B.chunked)
    add(B.pd_compare)

    n += 1
    section(prs, "05", "我们有哪些控制手段", "架构、调度、执行、显存、通信\n五层旋钮，以及每一层的代价。", n, VIO, VIO_L)
    add(C.framework)
    add(C.arch_layer)
    add(C.sched_layer)
    add(C.latency_budget)
    add(C.kv_layer)
    add(C.exec_layer)

    n += 1
    section(prs, "06", "从单点优化到系统级优化", "把所有工作收敛到一个目标上：\n在 SLO 约束下最大化 Goodput。", n, BLUE, BLUE_L)
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
