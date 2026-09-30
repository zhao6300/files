"""生成 selfevo.md 开头的首页图 hero.png（1080×760）。数据来自 SAGE（arXiv 2609.36043）和 SelfSearch（arXiv 2609.37968）摘要。"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
for base in (OUT.parents[1] / "scripts", OUT.parents[1] / "wechat-article-skill" / "scripts"):
    sys.path.insert(0, str(base))
import wxcharts as wc  # noqa: E402

plt = wc.plt
plt.rcParams["font.family"] = ["Noto Sans CJK SC", "Noto Sans SC", "sans-serif"]

W, H = 1080, 760
fig = plt.figure(figsize=(W / 225, H / 225), dpi=225)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
L = 64  # 左边距

# 栏目行
ax.add_patch(plt.Rectangle((L, 682), 16, 16, color=wc.SIGNAL, lw=0))
ax.text(L + 30, 690, "17 篇自我进化 Agent 论文 · arXiv 2026.9.30", fontsize=11.5, color=wc.GRAY, va="center")

# 核心判断，两行
ax.text(L, 600, "Agent 改好自己，只要 4 美元", fontsize=20.5, fontweight="bold", color=wc.INK, va="center")
ax.text(L, 510, "难的是判断，这次改动该不该留", fontsize=20.5, fontweight="bold", color=wc.SIGNAL, va="center")

# 下半部分：两种验收方式的对比
ax.add_patch(plt.Rectangle((L, 96), W - 2 * L, 330, color=wc.TRACK, lw=0))
ax.plot([W / 2, W / 2], [150, 340], color="#DDDDDD", lw=1.5)
ax.text(L + 36, 388, "被接受的改动，把已经做对的题改错了", fontsize=12, color=wc.BODY, va="center")

cols = [
    (L + 36, "按平均分放行", "36.5%", wc.SIGNAL),
    (W / 2 + 36, "逐题比较（SAGE）", "0%", wc.INK),
]
for x, label, num, color in cols:
    ax.text(x, 316, label, fontsize=12.5, fontweight="bold", color=wc.INK, va="center")
    ax.text(x - 4, 222, num, fontsize=36, fontweight="bold", color=color, va="center")

ax.text(L + 36, 128, "LiveMath 基准，DeepSeek-V4",
        fontsize=10, color=wc.GRAY, va="center")

ax.text(L, 48, "数据：SAGE、SelfSearch（arXiv 2609.36043 / 2609.37968）",
        fontsize=9.5, color=wc.GRAY, va="center")

fig.savefig(OUT / "hero.png", facecolor="white")
plt.close(fig)
