# 2026年创业公司调研：Top 100 与 Agent 基础设施切入点

- **调研时间：** 2026-09-30
- **覆盖范围：** 2026年4月–9月
- **数据来源：** Google News 聚合的 Reuters、Bloomberg、CNBC、TechCrunch、WSJ、The Information、Crunchbase News、36氪等媒体的报道标题，以及 CNBC 2026 Disruptor 50 榜单页面。

## 使用前请注意

- 数据是标题层面的信息，没有逐篇核对原文，正式引用前请先查看原文。
- 标“谈判中”或“据报道”的交易尚未完成。
- 标“估”的数字是第三方数据网站的估算值。
- 文中分析不构成投资建议。

## 文件说明

| 文件 | 内容 |
|---|---|
| `01_2026年4-9月_创业公司Top100.md` | 100家高增长、高关注度公司，分10类，每家附这半年的关键事件，最后总结趋势 |
| `02_新创业公司切入点.md` | 根据这100家公司，分析哪些方向不宜进入、值得切入的8个方向、中国市场的机会和判断框架 |
| `03_Agent与基础设施_切入点分析.md` | Agent 技术栈分层与机会评级、5个重点方向、中国市场机会、要避开的坑、90天验证清单、融资和并购速查表 |
| `04_一人公司OPC切入点.md` | 适合一人公司的7个切入点：平台插件、Agent 化改造、AI 服务公司、爆款小工具、专业数据、开源安全工具、国内政策，附技术栈、自检问题和按背景选择的建议 |
| `05_OPC三方向详细展开.md` | 三个方向的落地方案：Agent 化改造、个人版 FDE（企业微信、飞书、钉钉）、AI 短剧和内容超级个体。每个方向包括市场信号、客户、服务套餐和报价、交付流程、技术栈、合规、获客、收入测算、风险；另有组合打法和90天计划 |
| `tools/gn.py` | 新闻检索脚本：按关键词和日期查询 Google News RSS，输出按时间排序、去重后的标题 |
| `data/*.txt` | 检索原始结果快照（日期和标题），用于追溯报告中的数据 |

## 检索工具用法

只需要 Python 3 标准库，不用安装依赖。

```bash
# 用法：python3 tools/gn.py "关键词" [返回条数，默认25] [en|zh，默认en]
python3 tools/gn.py "raises billion valuation after:2026-09-01 before:2026-09-30" 60
python3 tools/gn.py "人形机器人 融资 估值 after:2026-05-01" 30 zh
```

**常用查询语法**（Google News 支持）：

| 语法 | 作用 |
|---|---|
| `after:YYYY-MM-DD` / `before:YYYY-MM-DD` | 限定日期范围 |
| `when:30d` | 只看最近30天 |
| 引号 `"..."` | 精确匹配 |

**按月更新榜单时可以用的查询：**

```bash
for m in 2026-10 2026-11; do
  python3 tools/gn.py "raises billion valuation after:${m}-01 before:${m}-31" 60
done
python3 tools/gn.py "IPO debut shares soar startup after:2026-10-01" 40
python3 tools/gn.py "acquires startup for billion after:2026-10-01" 40
python3 tools/gn.py "annualized revenue ARR fastest growing startup after:2026-10-01" 40
```

**限制：**
- 每次查询最多返回约100条结果。
- 结果只有标题和日期，没有正文。
- Crunchbase News 的 RSS 被 Cloudflare 拦截，无法直接抓取，所以改用 Google News 聚合。

## 持续追踪

本目录是一次性的调研结果。持续更新请使用产品化后的工具 [`../funding-tracker`](../funding-tracker/README.md)：每周自动采集新闻、抽取交易事件、生成报告，并在运行中自我改进。
