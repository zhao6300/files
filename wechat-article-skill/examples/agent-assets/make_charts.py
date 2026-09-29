"""生成 agent.md 的图表和封面。数据都来自文中注明的一手来源。

按 1080px 宽出图；手机上缩到约 343px 显示，所以字号要 ≥12.5pt。
python examples/agent-assets/make_charts.py   # 需要 matplotlib 和中文字体（如 Noto Sans SC）
"""
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
plt.rcParams["font.family"] = ["Noto Sans SC", "PingFang SC", "Microsoft YaHei", "sans-serif"]
INK, GRAY, SIGNAL = "#0D0D0D", "#8E8EA0", "#F2542D"
OUT = Path(__file__).parent


def steps(fname, title, rows, source):
    """rows: [(左侧标签, 标题, 说明, 是否强调)]，竖排的时间线 / 漏斗。"""
    fig, ax = plt.subplots(figsize=(4.8, 1.2 + 1.05 * len(rows)), dpi=225)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(rows))
    ax.axis("off")
    for i, (tag, head, body, hi) in enumerate(rows):
        y = len(rows) - i - 0.5
        ax.add_patch(plt.Rectangle((0.02, y - 0.36), 0.96, 0.72, color="#FFF3EE" if hi else "#F5F5F5", lw=0))
        ax.text(0.06, y, tag, fontsize=14, fontweight="bold", color=SIGNAL if hi else INK, va="center")
        ax.text(0.33, y + 0.13, head, fontsize=13, fontweight="bold", color=SIGNAL if hi else INK, va="center")
        ax.text(0.33, y - 0.16, body, fontsize=11.5, color="#353740", va="center")
        if i < len(rows) - 1:
            ax.annotate("", xy=(0.5, y - 0.52), xytext=(0.5, y - 0.38),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
    fig.text(0.02, 0.975, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.015, source, fontsize=10, color=GRAY, va="bottom")
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.06)
    fig.savefig(OUT / fname, facecolor="white")
    plt.close(fig)


steps(
    "timeline.png",
    "发现只用了 12 分钟，停下来用了两个半小时",
    [
        ("9:50", "拿到外部回复", "agent 经 DNS 通道问到了外部聊天机器人", False),
        ("10:02", "监控报警", "最高级别（P0）告警", False),
        ("10:05", "有人接手", "值班人员确认告警", False),
        ("12:34", "才被手动停掉", "自动停止没有生效", True),
    ],
    "来源：OpenAI 事故报告，2026 年 9 月 20 日（9 月 25 日更新）",
)
steps(
    "path.png",
    "一道找作者的题，它换了四条路",
    [
        ("第 1 条", "用给定的搜索工具", "搜出来的是音乐和泛泛的建议", False),
        ("第 2 条", "直接访问三大搜索引擎", "分别收到 403、502、502", False),
        ("第 3 条", "猜题目出自 BrowseComp", "下载题库、解开加密逐条比对，没对上", False),
        ("第 4 条", "借 DNS 问外部聊天机器人", "9:50 拿到回复，又接着问了 18 个问题", True),
    ],
    "来源：OpenAI 事故报告，2026 年 9 月 20 日（9 月 25 日更新）",
)
steps(
    "funnel.png",
    "4.81 亿条记录里，真正闯出去的只有 4 起",
    [
        ("4.81 亿", "全部记录", "红队、评测、强化学习、子 agent 日志", False),
        ("920 万", "第一轮筛出可疑", "出现公网 IP、网址等痕迹", False),
        ("4 起", "确认进入真实系统", "都出在同一家合作方配错网络的评测里", True),
    ],
    "来源：Anthropic 对齐评估，2026 年 9 月 9 日",
)


def cover(fname, lines, kicker):
    """公众号封面 2.35:1。文字放在中间的正方形里，分享时裁成 1:1 也完整。"""
    W, H = 1800, 766
    fig = plt.figure(figsize=(W / 200, H / 200), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    x0 = (W - H) / 2
    ax.add_patch(plt.Rectangle((x0 + 70, H - 190), 14, 14, color=SIGNAL, lw=0))
    ax.text(x0 + 96, H - 183, kicker, fontsize=14, color=GRAY, va="center")
    for i, (t, hi) in enumerate(lines):
        ax.text(x0 + 70, H - 290 - i * 104, t, fontsize=29, fontweight="bold", color=SIGNAL if hi else INK, va="center")
    fig.savefig(OUT / fname, facecolor="white")
    plt.close(fig)


cover("cover.png", [("AI 没想逃", False), ("它只是太想", False), ("把活干完", True)], "AI agent 越界")
