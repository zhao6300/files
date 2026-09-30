"""生成 reuse.md 的图表和封面。数据来自文中注明的来源。

python examples/reuse-assets/make_charts.py   # 需要 matplotlib 和中文字体（如 Noto Sans SC）
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
sys.path.insert(0, str(OUT.parents[1] / "scripts"))
import wxcharts as wc  # noqa: E402

wc.bars(
    OUT / "growth.png",
    "官方 MCP 注册表：每月新上架的服务器",
    [
        ("2025 年 9 月（上线）", 407, "407", False),
        ("2026 年 2 月", 1081, "1081", False),
        ("2026 年 4 月", 2387, "2387", False),
        ("2026 年 6 月", 3662, "3662", False),
        ("2026 年 8 月", 6265, "6265", True),
    ],
    6265,
    "数据：DevToolHub 统计官方注册表 API，截至 2026 年 9 月 10 日",
)
wc.bars(
    OUT / "stale.png",
    "3 万多个服务器里，大多数上架后没人再管",
    [
        ("只发过一个版本，之后再没更新", 62, "62%", True),
        ("最新版本号还停在第一版", 40.8, "40.8%", False),
        ("3 个月以上没动过（含无时间戳）", 36, "约 36%", False),
        ("远程服务器里，不给源码仓库的", 37, "37%", False),
    ],
    100,
    "数据：DevToolHub，官方 MCP 注册表 30375 个服务器，2026 年 9 月 10 日",
)
wc.bars(
    OUT / "miro.png",
    "8 月，agent 调用 Miro 是去读还是去写",
    [
        ("读白板，再照着去干活（如写代码）", 57, "57%", True),
        ("把生成的内容写回白板", 41, "41%", False),
    ],
    100,
    "数据：Miro 新闻稿，2026 年 9 月 29 日",
)
wc.cover(OUT / "cover.png", [("Miro 被 AI", False), ("调用了 1600 万次", False), ("复用的主角换了", True)], "AI 时代如何让产品更复用")
