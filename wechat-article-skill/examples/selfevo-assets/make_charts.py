"""生成 selfevo.md 的图表和封面。数据来自文中各论文摘要。"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
for base in (OUT.parents[1] / "scripts", OUT.parents[1] / "wechat-article-skill" / "scripts"):
    sys.path.insert(0, str(base))
import wxcharts as wc  # noqa: E402

wc.plt.rcParams["font.family"] = ["Noto Sans CJK SC", "Noto Sans SC", "sans-serif"]

wc.steps(
    OUT / "layers.png",
    "自我进化 Agent：改哪一层",
    [
        ("外层", "harness：上下文、工具、流程", "模型不动，改动好回滚", False),
        ("中层", "技能库、动作空间", "经验存成可增删改的条目", False),
        ("内层", "模型参数", "沉淀最深，也最难审计", False),
        ("验收", "这次改动该不该留下", "三层都绕不开的一道门", True),
    ],
    "整理：据 arXiv cs.AI 2026 年 9 月 30 日公告中 11 篇论文",
)
wc.bars(
    OUT / "regression.png",
    "被接受的改动，把已做对的题改错了多少",
    [
        ("LiveMath · 按平均分放行", 36.5, "36.5%", True),
        ("LiveMath · SAGE", 0, "0%", False),
        ("OfficeQA · 按平均分放行", 42.8, "42.8%", True),
        ("OfficeQA · SAGE", 0, "0%", False),
    ],
    42.8,
    "数据：SAGE（arXiv 2609.36043），DeepSeek-V4，2026 年 9 月",
)
wc.cover(
    OUT / "cover.png",
    [("Agent 改自己", False), ("只要 4 美元", False), ("难在该不该改", True)],
    "17 篇自我进化 Agent 论文",
)
