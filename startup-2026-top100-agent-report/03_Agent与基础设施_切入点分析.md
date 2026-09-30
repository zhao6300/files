# Agent 与基础设施：新创业公司切入点分析

- **数据时间：** 2026年3月–9月30日
- **数据来源：** Google News 聚合的 Reuters、Bloomberg、TechCrunch、The Information、36氪等报道标题。
- **说明：**
  - 标“（估）”的是第三方数据网站的估算值，不是公司披露的数据。
  - “谈判中”表示交易未完成。
  - 本文只是分析，不构成投资建议。

---

## 一、结论

1. **运行层已被巨头拿下，不要正面竞争。** 算力推理、模型网关、沙箱、托管运行时都已被大公司做完或收购：
   - AWS 推出 AgentCore v2，有报道称“云端 Agent 基础设施层已完整”。
   - Anthropic 推出 Claude Managed Agents，据第三方教程标题约 0.08 美元/小时。
   - OpenAI 推出 Dots，Cloudflare 一次发布了20多项 Agent 相关功能。
   - Stripe 收购了 OpenRouter，Nebius 收购了 Tavily。
2. **机会在“信任层”。** 包括身份与权限、运行时安全、审计与认证、保险、支付与风控。原因有三：
   - Agent 事故频发，从报道看已经变成常态。
   - 企业同时用多个模型、多个云，需要一个中立的管控层。
   - 平台方不愿意为 Agent 的行为承担责任。
3. **第二个机会在“供给侧”。** 要让网站、SaaS 和 API 能被 Agent 读懂、调用，并能向 Agent 收费。WebMCP、Shopify 结账、Agent 可读文档都是这类需求。
4. **这个赛道的特点是早期收购多、上市少。** 种子期公司也会被收购，比如 Aegis 成立9个月就被 Upwind 买下。所以一开始就可以把“被谁收购”作为设计目标之一。

---

## 二、关键市场信号

### 1. 风险在爆发，需求被推高

| 事件 | 意义 |
|---|---|
| AI 编程 Agent 把343家公司的1.3万张内部截图传到公开的 GitHub | 数据泄露已经实际发生 |
| Meta Muse 被指在未授权的情况下读取 iPhone 和 Mac 上的敏感数据 | 消费级 Agent 的权限边界失控 |
| OpenAI 披露了几十起 Agent 事故 | 平台方自己也承认问题存在 |
| Unit 42 披露：一个被投毒的工单就能窃取 AWS AgentCore 凭证 | 巨头的平台本身也有漏洞 |
| Nvidia 推出 Agent“紧急停止开关”，OpenAI 没有加入 | 行业开始自救，但标准分裂 |
| 美国 NIST 的 Agent 标准期限将至，但还没有可执行框架；特拉华州在推动“AI 运营公司”相关立法 | 合规需求即将到来 |

### 2. 资金流向

- **Agent 安全与治理：** 有报道称，企业 Agent 相关融资5个月内达到4.35亿美元，其中安全和治理领投。代表案例：
  - AIR 种子轮5000万
  - Reco 5500万
  - Arcade A 轮6000万
  - Baselayer A 轮3500万
  - AIUC A 轮4000万
  - Outerlimit pre-seed 1600万
  - Rig 种子轮1200万
- **高估值案例：**
  - Glow：Agent 安全，估值12亿
  - Irregular：AI 模型安全测试，谈判中，估值15亿
  - Island：企业浏览器，估值64亿
- **数据获取：**
  - Exa 估值22亿
  - Parallel 估值20亿
  - Firecrawl B 轮7500万
  - Keenable 种子轮2600万
- **推理算力（头部集中）：**
  - Baseten：谈判中，估值约260亿
  - Modal：谈判中，估值约157亿
  - Fal：谈判中，估值超150亿
  - Fireworks：谈判中，估值约150亿

### 3. 退出案例

| 收购方 | 标的 | 金额 | 说明 |
|---|---|---|---|
| Stripe | OpenRouter | 约75亿 | 模型网关变成支付公司的资产 |
| Nscale | Anyscale | 16.5亿 | 算力公司补软件栈 |
| Cyera | Oasis Security | 约10亿 | Agent 身份安全 |
| Dynatrace | Arize | 9.15亿 | AI 可观测性被老牌监控公司吸收 |
| Nebius | Tavily | 未披露 | 云厂商补 Agent 搜索能力 |
| Upwind | Aegis | 数千万 | 成立9个月就被收购 |

**规律：** 收购方大多是支付、安全、监控、云这几类老牌公司，它们用收购来补 Agent 能力。

---

## 三、Agent 技术栈分层与机会评级

★越多，新公司的机会越大。

| 层 | 代表公司 / 动态 | 竞争格局 | 评级 |
|---|---|---|---|
| **推理算力** | Baseten、Modal、Fal、Fireworks、Together | 每轮融资十亿级，头部集中 | ★ |
| **模型网关 / 路由** | OpenRouter 被 Stripe 收购 | 已被整合 | ★ |
| **运行时 / 沙箱 / 持久执行** | E2B、Daytona、Vercel Sandbox、Temporal（125.5亿）、Restate（A 轮2000万）、AWS AgentCore、Claude Managed Agents、Cloudflare | 巨头已经把托管运行时做成标配 | ★★ |
| **记忆 / 上下文** | Mem0、Letta、HydraDB（650万）；Genspark 在推“上下文” | 平台都在内置，很难单独收费 | ★★ |
| **开源框架** | LangChain（第三方估算 ARR 约1600万，估值约13亿） | 用户多但不好变现 | ★ |
| **网页 / 数据获取** | Exa、Parallel、Firecrawl、Browserbase（估算 ARR 约440万）、Tavily 被 Nebius 收购 | 通用搜索已有头部；垂直数据源和授权内容还有空间 | ★★★ |
| **工具连接 / MCP / 执行层** | Arcade、Composio、Runlayer（和 Rippling 打官司）、AgentCore Gateway；Bird 融资4.5亿做 Agent 通信 | 协议还在变，MCP 已改为无状态 | ★★★ |
| **身份 / 权限 / 了解你的 Agent（KYA）** | Baselayer、Keycard、Oasis 被 Cyera 收购、Outerlimit、Rig；国内有亿格云 | 刚起步，还没有标准 | ★★★★★ |
| **运行时安全 / 防火墙** | AIR、Reco、Glow、Eve、Irregular、Aegis 被 Upwind 收购、Nvidia 停止开关 | 热，但已有报道说“开始拥挤”，并购整合会很快 | ★★★★ |
| **可观测 / 评测 / 自动修复** | Arize 被 Dynatrace 收购、Braintrust（曾发生数据泄露）、Autoheal（790万）、Sazabi（800万） | 更可能被老牌监控公司收购 | ★★★ |
| **支付 / 商务** | Stripe ACP、Google AP2、x402（Coinbase、Block、Cloudflare 钱包）、Visa、Mastercard、Natural（A 轮3000万）、Creem | 协议碎片化：有文章说“5套结账标准，采用率约3%” | ★★★★ |
| **认证 / 保险 / 责任** | AIUC（与 Lloyd's 合作）、Humanos（320万）；法律 AI 公司 Crosby 在为自己的 Agent 找保险 | 全新品类 | ★★★★ |
| **人机协作界面** | Ando（2000万，“人和 Agent 共用的 Slack”） | 平台（Slack、Teams、飞书）自己也会做 | ★★★ |

---

## 四、平台方会做什么、不会做什么

| 平台方会做（别碰） | 平台方不愿或做不好（机会） |
|---|---|
| 模型、推理、托管运行时、沙箱 | **跨模型、跨云的中立治理**：企业同时用 Claude、GPT、Gemini、开源模型，而 OpenAI 连 Nvidia 的安全联盟都没加入 |
| 在自己生态里用的记忆、工具、连接器 | **为 Agent 行为承担责任**：认证、保险、赔付 |
| 通用搜索、浏览器 Agent | **垂直行业的合规**：金融、医疗、政务场景的审计留痕和私有化部署 |
| 自家的支付协议 | **跨协议聚合和风控**：同一个商家要同时接 ACP、AP2、x402、Visa |
| 通用个人助理（Meta Muse、OpenAI Dots、腾讯元宝） | **供给侧改造**：把存量网站、ERP、老旧系统变成 Agent 能调用的形式 |

---

## 五、五个重点切入方向

### A. Agent 身份与权限（首选）

**做什么：**
- 给每个 Agent 发身份，实现“了解你的 Agent”（KYA）
- 最小权限和临时凭证：Agent 不直接拿密钥，由代理层代为执行
- 高风险操作需要人工审批
- 把 Agent 的行为关联到委托它的具体用户

**为什么是现在：** 凭证被盗（AgentCore 漏洞）、越权访问（Muse 事件）已经实际发生。另外，Oasis 被以10亿收购，说明收购方愿意付钱。

**客户：** 大企业的 CISO、身份访问管理团队、开放 API 的 SaaS 公司。

**风险：** Okta、Microsoft Entra、CrowdStrike 会往下延伸做同样的事。应对方法是在 Agent 专用的场景上做得比它们更深，并把被它们收购当作退出路径。

### B. 行为治理、审计与认证，并和保险挂钩

**做什么：**
- 记录并回放 Agent 的每一步决策和操作
- 按行业规则做策略检查
- 生成可以交给审计和监管的报告
- 用这些数据帮保险公司给 Agent 风险定价（参考 AIUC 与 Lloyd's 的模式）

**切入口：** 先从一个有明确监管要求的行业做起，比如金融、医疗或法律。可以同时给这个行业的 Agent 创业公司提供“可投保”的认证。

**护城河：** 积累的 Agent 事故和行为数据，会成为风险定价的基础。

### C. 跨协议的 Agent 支付与风控

**做什么：**
- 商家接入一次，就能同时支持 ACP、AP2、x402、Visa 和 Mastercard 的 Agent 支付
- 识别 Agent 欺诈。OpenRouter 创始人称，Token 欺诈即将“海啸级”爆发。
- 支持 Agent 之间的小额计量计费

**为什么是现在：** 协议碎片化，采用率又低，正是需要“聚合层”的时候。Checkout.com 同时支持3套协议，说明大玩家也在观望。

**风险：** Stripe 这类公司一旦统一标准，聚合层的价值会被压缩。所以风控和争议处理要做成核心能力，而不只是做接口聚合。

### D. 供给侧：让网站和系统能被 Agent 调用（Agent-ready）

**做什么：**
- 把现有网站、ERP、老旧系统一键转成可被 Agent 调用的接口（MCP 或 WebMCP）
- 自动生成 Agent 能读懂的文档
- 按次收费的内容授权，让网站能向 Agent 的抓取收费
- 面向 AI 搜索的优化（GEO），参考 Profound 估值18亿

**为什么是现在：** Shopify 已经在结账环节支持 WebMCP；Amazon 向 Agent 开放了卖家后台；Stripe 称读文档的 Agent 很快会比人还多。

**客户：** 中小 SaaS、电商、媒体和内容网站。这个方向可以走产品自然增长（PLG），不需要靠大企业销售。

### E. Agent 的训练、评测环境与可靠性

**做什么：**
- 给企业搭建“私有强化学习环境”：把企业自己的系统做成可以训练和测试 Agent 的沙箱（参考 Arga Labs）
- 回归测试：模型每次升级后，自动验证 Agent 是否还按预期工作
- 自动修复：Agent 出错后，由另一个 Agent 接手（参考 Autoheal，号称单任务成本最多降低30%）

**依据：** DeepSeek 公开了 Agent 训练沙箱 DSec，说明“训练环境”本身就是护城河。另外，数据和环境类公司（AfterQuery、Snorkel）的估值涨得很快。

**风险：** 客户集中在大模型公司和大企业，销售周期长。

---

## 六、中国市场的特殊机会

1. **私有化部署的企业 Agent 治理：** 国内大企业偏好本地部署，还要适配国产算力，海外的 SaaS 很难进来。参考亿格云近亿元 B+ 轮，做企业 AI 治理基础设施。
2. **FDE 模式做垂直 Agent：** FDE 指派工程师驻场交付。参考词元无限：字节系团队，数亿元天使轮，靠 FDE 拿下数十家大客户。这种模式在国内比纯 SaaS 更容易打开市场。
3. **超级 App 生态内的 Agent 支付和调用：** 支付宝、微信、飞书、钉钉都在开放能力。可以做商家侧的 Agent 接入、风控和对账工具。
4. **数据智能体：** 帮企业把业务数据接给 Agent 用。参考数巅智能再获数亿元融资。
5. **Agent 出海的基础设施：** 国内团队做面向海外开发者的开源工具加云服务。PPIO 这类公司在讨论“下一代云基础设施重构”。

---

## 七、要避开的坑

- **通用框架、通用沙箱、通用记忆、通用浏览器：** 用户可以很多，但平台会把这些做成免费标配。LangChain 约13亿估值对应的估算 ARR 仅约1600万。
- **押注单一协议：** MCP 已改为无状态，结账标准有5套还在打架。产品要做到协议无关。
- **自身的安全和法律风险：**
  - Braintrust 发生数据泄露，所有客户都要轮换密钥。
  - Runlayer 和 Rippling 互相起诉。
  - 做安全和基础设施的公司，自己一旦出事就可能毁掉口碑。
- **赛道太挤：** Agent 安全已被媒体称为“开始拥挤”。晚进场要找更窄的切口，比如语音 Agent 的合规（参考 Modulate），或者编程 Agent 的数据防泄漏。

---

## 八、90天验证清单

1. **找20个目标客户做访谈**（企业 CISO、平台工程负责人、垂直 Agent 创业公司），问三个问题：
   - 你们现在有多少个 Agent 在生产环境运行？
   - 出过什么事？
   - 谁为这些事负责？
2. **做一个最小可用的“拦截点”：** 比如一个 MCP 网关，或者一个凭证代理，先接入1到2个客户的真实 Agent 流量。
3. **选一个付费触发点：** 合规审计、保险要求，或者一次真实事故之后。“效率提升”作为付费理由不够强。
4. **提前画好退出路径：** 列出潜在收购方，比如 Cyera、CrowdStrike、Okta、Datadog、Dynatrace、Stripe、云厂商，并了解它们的产品缺口。

---

### 附：2026年3–9月 Agent 基础设施融资和并购速查

| 公司 | 领域 | 事件 |
|---|---|---|
| Glow | Agent 安全 | 1.8亿，估值12亿 |
| Irregular | 模型安全测试 | 谈判中，估值15亿 |
| AIR | Agent 防火墙、插件审查 | 种子轮5000万 |
| Reco | 企业 Agent 安全 | 5500万，AT&T 参投 |
| Arcade | Agent 安全执行层 | A 轮6000万 |
| Baselayer | Agent 身份（KYA） | A 轮3500万 |
| AIUC | Agent 认证与保险 | A 轮4000万 |
| Outerlimit | Agent 零信任安全 | pre-seed 1600万 |
| Rig Security | Agent 安全 | 种子轮1200万（创始人来自 Wiz） |
| Eve Security | 运行时 Agent 管控 | 450万 |
| Natural | Agent 支付 | A 轮3000万 |
| Creem | AI 原生公司计费 | 500万欧元 |
| Restate | Agent 持久执行 | A 轮2000万 |
| Temporal | 持久执行 | 5.5亿，估值125.5亿 |
| Firecrawl | 网页数据 | B 轮7500万 |
| Keenable | 搜索 | 种子轮2600万 |
| Exa | 面向 AI 的搜索 | 2.5亿，估值22亿 |
| Parallel | 面向 Agent 的网页基础设施 | 1亿，估值20亿 |
| Bird | Agent 通信基础设施 | 4.5亿 |
| Autoheal | Agent 自动修复 | 790万 |
| Sazabi | AI 原生可观测性 | 种子轮800万 |
| Ando | 人与 Agent 协作 | 2000万 |
| Ema | 企业“AI 员工” | 7700万 |
| Modulate | 语音 Agent 合规、深度伪造检测 | 2500万 |
| Arize | AI 可观测性 | 被 Dynatrace 以9.15亿收购 |
| Tavily | Agent 搜索 | 被 Nebius 收购 |
| Aegis | AI 安全 | 被 Upwind 收购（成立9个月） |
| Oasis | Agent 身份 | 被 Cyera 以约10亿收购 |
| OpenRouter | 模型网关 | 被 Stripe 以约75亿收购 |
