"""生成 rsi.md 里的两张图表。数据全部来自文中注明的 Anthropic 公开报告。

按 1080px 宽出图；手机上缩到约 343px 显示，所以字号要 ≥12.5pt（≈13px 显示）。

python examples/rsi-assets/make_charts.py   # 需要 matplotlib 和一款中文字体（如 Noto Sans SC）
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import logging  # noqa: E402

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

plt.rcParams["font.family"] = ["Noto Sans SC", "PingFang SC", "Microsoft YaHei", "sans-serif"]
INK, GRAY, LIGHT, SIGNAL = "#0D0D0D", "#8E8EA0", "#E3E3E3", "#F2542D"
OUT = Path(__file__).parent


def bars(fname, title, rows, xmax, source):
    """rows: [(标签, 数值, 数值文字, 是否强调)]"""
    fig, ax = plt.subplots(figsize=(4.8, 1.1 + 0.95 * len(rows)), dpi=225)
    y = [1.35 * i for i in range(len(rows))][::-1]
    for yi, (label, v, text, hi) in zip(y, rows):
        ax.barh(yi, xmax, height=0.46, color="#F5F5F5")
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
    fig.savefig(OUT / fname, facecolor="white")
    plt.close(fig)


bars(
    "speedup.png",
    "同一道题：把训练代码改快，能提速几倍",
    [
        ("熟练的人类研究员，4–8 小时", 4, "约 4 倍", False),
        ("Claude Opus 4，2025 年 5 月", 3, "约 3 倍", False),
        ("Claude Mythos Preview，2026 年 4 月", 52, "约 52 倍", True),
    ],
    52,
    "数据：Anthropic《当 AI 造 AI》，2026 年 6 月",
)
bars(
    "automation.png",
    "Anthropic 内部研发，AI 参与到了哪一步",
    [
        ("AI 至少“协作”的工作", 90, "超过 90%", False),
        ("AI“主导”的工作（2 月还不到 1%）", 26, "26%", True),
        ("AI 完全自主的工作", 0, "0", False),
    ],
    100,
    "数据：Anthropic 研发自动化指数，2026 年 8 月；按员工工时加权",
)
