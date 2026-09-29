"""生成 rsi.md 的图表和封面。数据全部来自文中注明的 Anthropic、Hugging Face 公开报告。

python examples/rsi-assets/make_charts.py   # 需要 matplotlib 和中文字体（如 Noto Sans SC）
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
sys.path.insert(0, str(OUT.parents[1] / "scripts"))
import wxcharts as wc  # noqa: E402

wc.bars(
    OUT / "speedup.png",
    "同一道题：把训练代码改快，能提速几倍",
    [
        ("熟练的人类研究员，4–8 小时", 4, "约 4 倍", False),
        ("Claude Opus 4，2025 年 5 月", 3, "约 3 倍", False),
        ("Claude Mythos Preview，2026 年 4 月", 52, "约 52 倍", True),
    ],
    52,
    "数据：Anthropic《当 AI 造 AI》，2026 年 6 月",
)
wc.bars(
    OUT / "automation.png",
    "Anthropic 内部研发，AI 参与到了哪一步",
    [
        ("AI 至少“协作”的工作", 90, "超过 90%", False),
        ("AI“主导”的工作（2 月还不到 1%）", 26, "26%", True),
        ("AI 完全自主的工作", 0, "0", False),
    ],
    100,
    "数据：Anthropic 研发自动化指数，2026 年 8 月；按员工工时加权",
)
wc.bars(
    OUT / "oversight.png",
    "每周约 10 万段可疑记录，只有约 50 段交给人看",
    [
        ("离线监控每周标出的可疑记录", 100000, "约 10 万段", False),
        ("经过几层分类器筛选后，送到人手里的", 50, "约 50 段", True),
    ],
    100000,
    "数据：Anthropic，2026 年 9 月发布（8 月数据）",
)
wc.steps(
    OUT / "intrusion.png",
    "一次“偷答案”是怎么发生的",
    [
        ("", "考题", "网络攻防能力测试：找漏洞、写攻击代码", False),
        ("", "推断", "测试的参考答案可能放在 Hugging Face 上", False),
        ("", "越狱", "用零日漏洞钻出沙箱，借道第三方公开服务器", False),
        ("", "入侵", "打进数据处理系统：7 月 9–13 日，约 17600 次操作", True),
    ],
    "来源：Hugging Face 技术复盘，2026 年 7 月",
)
wc.cover(OUT / "cover.png", [("AI 已经在造 AI 了", False), ("给它打分的", False), ("也是 AI", True)], "递归自我改进")
