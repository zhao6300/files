"""生成 agent.md 的图表和封面。数据都来自文中注明的 OpenAI、Anthropic 一手报告。

python examples/agent-assets/make_charts.py   # 需要 matplotlib 和中文字体（如 Noto Sans SC）
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
sys.path.insert(0, str(OUT.parents[1] / "scripts"))
import wxcharts as wc  # noqa: E402

SRC_OPENAI = "来源：OpenAI 事故报告，2026 年 9 月 20 日（9 月 25 日更新）"
wc.steps(
    OUT / "path.png",
    "一道找作者的题，它换了四条路",
    [
        ("第 1 条", "用给定的搜索工具", "搜出来的是音乐和泛泛的建议", False),
        ("第 2 条", "直接访问三大搜索引擎", "分别收到 403、502、502", False),
        ("第 3 条", "猜题目出自 BrowseComp", "下载题库、解开加密逐条比对，没对上", False),
        ("第 4 条", "借 DNS 问外部聊天机器人", "9:50 拿到回复，又接着问了 18 个问题", True),
    ],
    SRC_OPENAI,
)
wc.steps(
    OUT / "timeline.png",
    "发现只用了 12 分钟，停下来用了两个半小时",
    [
        ("9:50", "拿到外部回复", "agent 经 DNS 通道问到了外部聊天机器人", False),
        ("10:02", "监控报警", "最高级别（P0）告警", False),
        ("10:05", "有人接手", "值班人员确认告警", False),
        ("12:34", "才被手动停掉", "自动停止没有生效", True),
    ],
    SRC_OPENAI,
)
wc.steps(
    OUT / "funnel.png",
    "4.81 亿条记录里，真正闯出去的只有 4 起",
    [
        ("4.81 亿", "全部记录", "红队、评测、强化学习、子 agent 日志", False),
        ("920 万", "第一轮筛出可疑", "出现公网 IP、网址等痕迹", False),
        ("4 起", "确认进入真实系统", "都出在同一家合作方配错网络的评测里", True),
    ],
    "来源：Anthropic 对齐评估，2026 年 9 月 9 日",
)
wc.cover(OUT / "cover.png", [("AI 没想逃", False), ("它只是太想", False), ("把活干完", True)], "AI agent 越界")
