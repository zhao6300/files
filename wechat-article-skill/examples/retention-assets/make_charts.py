"""生成 retention.md 的图表和封面。数据均来自文中注明的来源。

python examples/retention-assets/make_charts.py   # 需要 matplotlib 和中文字体（Noto Sans CJK SC）
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
sys.path.insert(0, str(OUT.parents[1] / "scripts"))
import wxcharts as wc  # noqa: E402

wc.plt.rcParams["font.family"] = ["Noto Sans CJK SC", "Noto Sans SC", "sans-serif"]

wc.bars(
    OUT / "funnel.png",
    "AI 应用：进门的人多，留下的人少",
    [
        ("试用转付费 · AI 应用", 8.5, "8.5%", True),
        ("试用转付费 · 非 AI 应用", 5.6, "5.6%", False),
        ("年度订阅一年后续费 · AI 应用", 21.1, "21.1%", True),
        ("年度订阅一年后续费 · 非 AI 应用", 30.7, "30.7%", False),
    ],
    30.7,
    "数据：RevenueCat《2026 订阅应用报告》，中位数，2026 年 3 月",
)
wc.bars(
    OUT / "spread.png",
    "3519 个 AI 应用，一年后还在付费的订阅",
    [
        ("留存高分组（前 30%）", 13.9, "13.9%", True),
        ("中间组（中间 40%）", 5.3, "5.3%", False),
        ("留存低分组（后 30%）", 1.4, "1.4%", False),
    ],
    13.9,
    "数据：RevenueCat，2024.7–2025.6 开始的付费订阅，中位数，2026 年 9 月",
)
wc.bars(
    OUT / "renewal.png",
    "月度订阅：第一次续费就拉开了差距",
    [
        ("高分组 · 第一次续费", 57.9, "57.9%", True),
        ("低分组 · 第一次续费", 30.2, "30.2%", False),
        ("高分组 · 第三次续费", 79.5, "79.5%", False),
        ("低分组 · 第三次续费", 68.5, "68.5%", False),
    ],
    100,
    "数据：RevenueCat，3519 个 AI 应用，2026 年 9 月",
)
wc.cover(
    OUT / "cover.png",
    [("同是 AI 应用", False), ("一年后留存", False), ("差了 10 倍", True)],
    "AI 时代如何造出更复用的产品",
)
