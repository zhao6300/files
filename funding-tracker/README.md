# funding-tracker：会自我进化的融资与创业追踪工具

把手工做的“半年创业公司 Top100”调研变成一条可重复运行的流水线：每周自动采集新闻，抽取出融资、IPO、并购、收入等结构化事件，输出排行榜和报告。**每跑一次，工具都会根据结果改进自己**，包括检索词、抽取规则、公司记忆和赛道归类。

- 纯 Python 标准库，Python ≥ 3.9，不需要装任何依赖
- 所有知识都放在 `knowledge/*.json` 里，不用改代码；所有自动修改都记在 `knowledge/CHANGELOG.jsonl`，可以用 git 回滚
- 原始数据按月追加写入 `data/mentions/`；抽取结果在读取时实时计算，所以**规则一升级，全部历史数据自动按新规则重新抽取**

## 快速开始

```bash
cd funding-tracker
python3 ft.py run --days 7          # 每周任务：采集 → 进化 → 报告（约30秒）
python3 ft.py top --days 30         # 终端查看近30天的综合热度榜
python3 ft.py company "Cognition"   # 单家公司的事件时间线
python3 ft.py test                  # 标准答案集回归测试
```

生成的文件在 `reports/`：`YYYY-MM-DD_weekly.md`（报告）和 `.csv`（明细，可直接用 Excel 打开）。

## 命令

| 命令 | 作用 |
|---|---|
| `run [--days 7] [--llm]` | 一键执行采集、进化和报告 |
| `collect [--days N] [--no-rss]` | 运行所有启用中的检索词和 RSS 源，只保存新出现的报道 |
| `report [--days N \| --since D --until D] [--top 20] [--name X]` | 生成 Markdown 和 CSV 报告 |
| `top [--days 30] [--n 30]` | 在终端输出综合热度榜 |
| `company NAME` | 查看某家公司的融资、IPO、并购时间线 |
| `evolve [--dry-run] [--llm]` | 自我进化；加 `--dry-run` 只预览、不写入 |
| `test [--min 0.9]` | 回归测试；准确率低于阈值时退出码为1，可用作 CI 门禁 |
| `golden review \| accept [ids\|all]` | 审核大模型标注的候选用例，合格的并入标准答案集 |
| `stats` | 查看每个检索词的适应度（EMA，指数移动平均）和状态 |
| `import-txt FILE...` | 导入 `YYYY-MM-DD \| 标题` 格式的历史快照 |
| `extract "标题"` | 调试单条标题的抽取结果 |

## 流水线

```
 queries.json(种子) + queries_evolved.json(进化出的)     sources.json(RSS)
                 │                                          │
                 ▼                                          ▼
          ┌─────────────── collect ───────────────┐  记录每个检索词带来的新交易数
          │  Google News RSS / RSS → data/mentions │ ─────────────► query_stats.json
          └───────────────────┬───────────────────┘
                              ▼
   extract（中英文规则 + patterns/aliases/known_companies/company_sectors + LLM缓存）
                              ▼
   events（同一公司、同一类事件、条款相近的报道合并为一个事件；数周后重复报道同一轮也能合并）
                              ▼
   analytics（最高估值、估值增速、报道热度、退出事件 → 综合评分）──► report（.md / .csv）
                              ▼
   evolve ──► 修改 knowledge/*.json（每项修改都要先通过标准答案集回归测试）
```

## 进化机制

| # | 机制 | 做什么 | 安全门 |
|---|---|---|---|
| 1 | **检索词选择** | 按每个检索词带来的“新交易”数计算 EMA。试用期的词表现好就转正，表现差就退役 | 种子检索词固定不退役 |
| 2 | **检索词变异** | 从热度榜里的公司自动生成监控检索词；从近期融资标题里找增长快的词组，生成新检索词 | 新词先试用，通过考核才转正 |
| 3 | **规则学习** | 从抽取失败的标题里挖新的动词（如 snags、pockets）；从多个公司名的首词里发现描述词（如 Healthcare Xxx） | 标准答案集准确率不下降，且确实能多解析出交易 |
| 4 | **别名学习** | 同一轮融资被写成 `Colossal Biosciences` 和 `Colossal` 时，自动合并成一家公司 | 回归测试；不会合并到常见英文单词上 |
| 5 | **公司记忆** | 被至少2家媒体确认过的公司名会记住，以后语法复杂的标题也能识别出来 | 回归测试；`not_startups.json` 黑名单 |
| 6 | **赛道记忆** | 学会公司和赛道的对应关系，标题里没有赛道关键词时也能归类 | — |
| 7 | **大模型兜底（可选）** | 规则解析不了的标题交给大模型标注一次，结果缓存复用；同时放入 `tests/golden_candidates.jsonl` 等人工审核 | 人工 `golden accept` 之后才并入标准答案集 |

这里的“进化”不是黑箱：每条自动修改都写在 `knowledge/CHANGELOG.jsonl` 里，记录内容包括时间、类型、证据，以及修改前后的回归测试准确率。开发过程中发现过几条学偏的修改，已经修复并记为 `manual_revert`，可以作为参考。

### 开启大模型兜底

支持任何兼容 OpenAI 接口的服务，比如 OpenAI、DeepSeek、通义、Kimi，或者本地部署的 vLLM：

```bash
export FT_LLM_API_KEY=...
export FT_LLM_BASE_URL=https://api.deepseek.com/v1   # 可选，默认是 OpenAI
export FT_LLM_MODEL=deepseek-chat                    # 可选
python3 ft.py run --llm
python3 ft.py golden review && python3 ft.py golden accept all   # 审核通过后并入回归集
```

## 知识文件（`knowledge/`）

| 文件 | 内容 | 维护方式 |
|---|---|---|
| `queries.json` | 种子检索词（中文和英文） | 手动 |
| `queries_evolved.json` / `query_stats.json` | 进化出的检索词及其适应度 | 自动 |
| `sources.json` | RSS 源（TechCrunch、36氪、Sifted） | 手动 |
| `sectors.json` / `regions.json` | 赛道和地区关键词 | 手动 |
| `aliases.json` | 公司别名，比如 `深度求索 → DeepSeek`、`Anysphere → Cursor` | 手动加自动 |
| `known_companies.json` / `company_sectors.json` | 公司记忆和赛道记忆 | 自动（可以人工修正） |
| `patterns.json` | 学到的动词、描述词、无效名称 | 自动（经过回归测试） |
| `not_startups.json` | 大公司、投资机构、交易所等非创业公司黑名单 | 手动 |
| `settings.json` | 评分权重、进化阈值等，会覆盖 `tracker/config.py` 里的默认值 | 手动 |

## 质量与局限

- **标准答案集：** `tests/golden.jsonl` 里有122条中英文标题，覆盖388项检查，当前全部通过。它同时也是开发时调规则用的数据，所以不能代表对新数据的真实准确率。
- **新数据抽查：** 从本周实时采集的数据里随机抽了50条没参与调规则的交易，公司、事件、金额三项全对的约占90%。常见错误有：一条标题里写了多条新闻、从句里提到的其他公司金额被错算、非创业公司（交易所、上市公司）的 IPO。
- 只根据标题抽取，不读正文；金额按固定汇率折算成美元（见 `tracker/extract.py` 里的 `FX`）。
- “新晋独角兽”是按**本库记录**判断的，也就是本库里第一次出现估值≥10亿美元。库里数据越多，结果越准。
- Google News RSS 每次查询最多返回约100条；Crunchbase 有 Cloudflare 拦截，所以没有直接接入。

## 自动运行（GitHub Actions）

仓库根目录的 `.github/workflows/funding-tracker.yml` 每周一 01:00 UTC 运行，流程是：回归测试 → `ft.py run` → 再次回归测试 → 提交 `data/`、`knowledge/`、`reports/` 的变更。

- GitHub 的定时任务**只在默认分支上触发**，需要合并到 `main` 后才会生效；在此之前可以在 Actions 页面手动触发（workflow_dispatch）。
- 在仓库 Secrets 里配置 `FT_LLM_API_KEY`（可选再配 `FT_LLM_BASE_URL`、`FT_LLM_MODEL`），就会自动开启大模型兜底。

## 代码结构

```
ft.py                 命令行入口
tracker/sources.py    Google News / RSS 采集
tracker/extract.py    规则抽取：金额、估值、年化收入、轮次、公司、收购方、状态、赛道、地区
tracker/store.py      按月追加写入的数据存储，以及大模型结果缓存
tracker/events.py     报道合并为事件
tracker/analytics.py  公司画像、增速、综合评分、新晋独角兽
tracker/report.py     报告的各个章节（可复用）
tracker/evolve.py     自我进化
tracker/golden.py     回归评测
tracker/llm.py        兼容 OpenAI 接口的大模型客户端
tests/                标准答案集和单元测试（python3 -m unittest discover -s tests）
```
