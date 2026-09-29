"""公众号配图小工具：条形图、步骤 / 时间线图、封面。可选依赖 matplotlib + 一款中文字体（如 Noto Sans SC）。

规格（见 references/writing-guide.md）：
  * 按 1080px 宽出图；手机上缩到约 343px 显示，所以最小字号 ≥12.5pt（显示约 13px）。
  * 图内写标题和“数据：某某，某年某月”，正文里用 ![](图.png)，不再加图注。
  * 封面 2.35:1，文字放在中间的正方形里，分享时裁成 1:1 也完整。

用法：
  import sys; sys.path.insert(0, "<skill>/scripts"); import wxcharts as wc
  wc.bars(out / "a.png", "标题", [("标签", 数值, "数值文字", 是否强调), ...], 最大值, "数据：……")
  wc.steps(out / "b.png", "标题", [("左侧标签", "小标题", "说明", 是否强调), ...], "来源：……")
  wc.cover(out / "cover.png", [("第一行", False), ("强调行", True)], "栏目 / 话题")
"""
from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
plt.rcParams["font.family"] = ["Noto Sans SC", "PingFang SC", "Microsoft YaHei", "sans-serif"]

# 素白 mono 主题配色；换主题时改这里
INK, GRAY, SIGNAL, TRACK, HIGHLIGHT, BODY = "#0D0D0D", "#8E8EA0", "#F2542D", "#F5F5F5", "#FFF3EE", "#353740"


def bars(path: Path, title: str, rows: list[tuple], xmax: float, source: str) -> None:
    """横向条形图。rows: [(标签, 数值, 数值文字, 是否强调)]"""
    fig, ax = plt.subplots(figsize=(4.8, 1.1 + 0.95 * len(rows)), dpi=225)
    y = [1.35 * i for i in range(len(rows))][::-1]
    for yi, (label, v, text, hi) in zip(y, rows):
        ax.barh(yi, xmax, height=0.46, color=TRACK)
        ax.barh(yi, max(v, xmax * 0.004), height=0.46, color=SIGNAL if hi else INK)
        ax.text(0, yi + 0.33, label, fontsize=12.5, color=INK, va="bottom")
        ax.text(min(v, xmax) + xmax * 0.015, yi, text, fontsize=14, fontweight="bold",
                color=SIGNAL if hi else INK, va="center")
    ax.set_xlim(0, xmax * 1.3)
    ax.set_ylim(-0.5, 1.35 * (len(rows) - 1) + 0.9)
    ax.axis("off")
    fig.text(0.02, 0.97, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.02, source, fontsize=10, color=GRAY, va="bottom")
    fig.subplots_adjust(left=0.03, right=0.97, top=0.84, bottom=0.12)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def steps(path: Path, title: str, rows: list[tuple], source: str) -> None:
    """竖排步骤 / 时间线 / 漏斗。rows: [(左侧标签, 小标题, 说明, 是否强调)]；左侧标签为空时标题左对齐。"""
    fig, ax = plt.subplots(figsize=(4.8, 1.2 + 1.05 * len(rows)), dpi=225)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(rows))
    ax.axis("off")
    for i, (tag, head, body, hi) in enumerate(rows):
        y = len(rows) - i - 0.5
        x = 0.33 if tag else 0.06
        ax.add_patch(plt.Rectangle((0.02, y - 0.36), 0.96, 0.72, color=HIGHLIGHT if hi else TRACK, lw=0))
        if tag:
            ax.text(0.06, y, tag, fontsize=14, fontweight="bold", color=SIGNAL if hi else INK, va="center")
        ax.text(x, y + (0.13 if tag else 0.12), head, fontsize=13, fontweight="bold", color=SIGNAL if hi else INK, va="center")
        ax.text(x, y - 0.16, body, fontsize=11.5, color=BODY, va="center")
        if i < len(rows) - 1:
            ax.annotate("", xy=(0.5, y - 0.52), xytext=(0.5, y - 0.38),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
    fig.text(0.02, 0.975, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.015, source, fontsize=10, color=GRAY, va="bottom")
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.06)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def cover(path: Path, lines: list[tuple], kicker: str) -> None:
    """封面 1800×766（2.35:1），最多 3 行。字号会按最长一行自动缩小，裁成 1:1 时不会出界。"""
    W, H = 1800, 766
    fig = plt.figure(figsize=(W / 200, H / 200), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    x0 = (W - H) / 2  # 中间正方形左边界
    ax.add_patch(plt.Rectangle((x0 + 70, H - 190), 14, 14, color=SIGNAL, lw=0))
    ax.text(x0 + 96, H - 183, kicker, fontsize=14, color=GRAY, va="center")
    # 字号按最长一行自动缩小，保证裁成 1:1 时左右各留 70px（R15：两次封面出界）
    size, room = 29.0, H - 140
    texts = [ax.text(x0 + 70, H - 290 - i * 104, t, fontsize=size, fontweight="bold", color=SIGNAL if hi else INK, va="center")
             for i, (t, hi) in enumerate(lines)]
    renderer = fig.canvas.get_renderer()
    widest = max(tx.get_window_extent(renderer).width for tx in texts)
    if widest > room:
        for tx in texts:
            tx.set_fontsize(size * room / widest)
    fig.savefig(path, facecolor="white")
    plt.close(fig)
