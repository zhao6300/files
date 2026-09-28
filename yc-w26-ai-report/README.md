# YC Winter 2026（W26）批次：公司分类与 AI 创业趋势报告

> **数据来源说明**：你上传的附件表格在传输中损坏，读不出来。本报告改用 YC 官方公司目录的公开镜像数据 [yc-oss/api](https://yc-oss.github.io/api/batches/winter-2026.json)（Winter 2026 批次，共 **199 家公司**，数据抓取于 2026-09-28）。字段包括公司名、one-liner、描述、地点、团队规模等。分类和中文简介由我根据公司自述人工标注。如果你的原表和这份数据有差异，请重新提供 CSV，我会按原表重跑。

## 一、核心结论（TL;DR）

1. **几乎全是 AI 公司**：199 家中有 159 家（约 80%）在描述里明确提到 AI、LLM、Agent 或模型。剩下的也大多是 AI 时代的配套，比如能源、芯片、支付。
2. **Agent 是默认的产品形态**：73 家（36.7%）的描述提到 Agent，38 家直接把 “Agent” 写进一句话介绍。产品形态从 “AI Copilot” 变成了 “AI 员工 / AI 队友”，“Copilot” 一词只出现了 3 次。
3. **“卖铲子”仍是最大板块**：AI 基础设施、Agent 基础设施和开发者工具合计 52 家（26.1%）。其中 Agent 专用的支付、护栏、可观测、控制平面、Agent-first API 是这一批的新热点。
4. **垂直行业纵深**：金融、法律、医疗、生命科学和传统产业运营合计 74 家（37.2%），是占比最高的一类。选的行业多是规则重、流程重、文档重的“不性感”行业。
5. **从卖软件到卖结果**：出现了一批 **AI 原生服务公司**，包括 AI 律所、AI 会计、AI 医疗账单、AI 保险经纪。它们直接交付服务，按结果收费（Service-as-Software）。另有 FDE（前线部署工程师）模式的公司。
6. **Physical AI 起势**：机器人与具身智能 14 家，航天、国防、能源与硬科技 14 家，合计 14.1%。机器人赛道的重心放在**数据、评测和世界模型**这些瓶颈环节。
7. **消费端依然偏冷**：消费应用、游戏、AI 硬件和内容创作合计 12 家（6.0%），超过 9 成公司做 B2B。
8. **团队极小、极度集中在湾区**：团队规模中位数是 **3 人**，约 40%（79 家）是 2 人团队。65.8% 位于旧金山，80.4% 位于美国。

## 二、分类方法与分布

每家公司按主营方向归入 14 个类别之一（单选）：

| 代码 | 分类 | 公司数 | 占比 | 分布 |
|---|---|---:|---:|---|
| C4 | 企业职能AI Agent（销售/营销/客服/HR/运营） | 26 | 13.1% | █████████ |
| C5 | 金融科技、会计与保险 | 26 | 13.1% | █████████ |
| C1 | AI基础设施与模型层 | 23 | 11.6% | ████████ |
| C11 | 垂直产业运营（建筑/物流/制造/酒店等） | 16 | 8.0% | █████ |
| C2 | Agent基础设施与AI治理 | 15 | 7.5% | █████ |
| C10 | 航天、国防、能源与硬科技 | 14 | 7.0% | █████ |
| C9 | 机器人与具身智能（Physical AI） | 14 | 7.0% | █████ |
| C3 | 开发者与工程设计工具 | 14 | 7.0% | █████ |
| C7 | 医疗健康服务 | 12 | 6.0% | ████ |
| C6 | 法律、合规与政府事务 | 10 | 5.0% | ███ |
| C8 | 生命科学与AI for Science | 10 | 5.0% | ███ |
| C13 | 消费应用、游戏与AI硬件 | 7 | 3.5% | ██ |
| C12 | 网络安全与身份 | 7 | 3.5% | ██ |
| C14 | AI内容创作与媒体 | 5 | 2.5% | ██ |

按大板块汇总：

| 大板块 | 包含分类 | 公司数 | 占比 |
|---|---|---:|---:|
| 垂直行业 AI | 金融 / 法律 / 医疗 / 生命科学 / 产业运营 | 74 | 37.2% |
| AI 与 Agent 基础设施（卖铲子） | 模型层 / Agent 基础设施 / 开发者工具 | 52 | 26.1% |
| 企业通用职能 Agent | 销售、营销、客服、HR、运营 | 26 | 13.1% |
| Physical AI 与硬科技 | 机器人 / 航天、国防、能源 | 28 | 14.1% |
| 安全 | 网络安全与身份 | 7 | 3.5% |
| 消费与内容 | 消费应用 / 内容创作 | 12 | 6.0% |

### 各分类公司一览

- **企业职能AI Agent（销售/营销/客服/HR/运营）（26）**：BaseFrame、Booko、Bubble Lab、Cardinal、Caretta、Cofia、Corvera、EigenPal、Fixture、Jinba、Khotan (formerly Pollinate)、Laurence、Menza、Perfectly、Pollen、RamAIn、Samora AI、Signals、Sila、Sitefire、Skillsync、Terminal Use、Turnstone、Unisson、Vela、Veriad
- **金融科技、会计与保险（26）**：Alt-X、Axis、Balance、Copperlane、End Close、Fenrock AI、Forum、FullSeam、Grade、Instinct、InventoryQuant、Kita、Maywood、MouseCat、o11、Palus Finance、Panta、Proximitty、Q2Q、Sequence Markets、SpotPay、Unifold、Valence、Valgo、Verdex、ZeroSettle
- **AI基础设施与模型层（23）**：Anchorhead、ARC Prize Foundation、Ashr、Autumn AI、Byteport、Cascade、Chamber、Compresr、Cumulus Labs、Envariant、Luel、Mantis、Ndea、Overshoot、Piris Labs、Polymath、Rubric AI、RunAnywhere、Shofo、Talking Computers、The Token Company、Traverse、Velum Labs
- **垂直产业运营（建筑/物流/制造/酒店等）（16）**：AutoSitu、Avoice、Bidflow、Burt、Chasi、Foreman、Haladir、Inviscid AI、Lance、Ossus、Reframe、Revion、Robby、Travo、Ventura、Zymbly
- **Agent基础设施与AI治理（15）**：Agentic Fabriq、Canary、Captain、Carrot Labs、Klaus AI、Maven、Moda、Orthogonal、Oximy、Ressl AI、Salus、Sentrial、Sponge、VOYGR、Zatanna
- **航天、国防、能源与硬科技（14）**：AxionOrbital Space、Beyond Reach Labs、Condor Energy、Constellation Space、DAIVIN!、Galactic Resource Utilization Space, Inc. (GRU Space)、Kyten Technologies、Milliray、Seeing Systems、Squid、Terranox AI、Visibl Semiconductors、Voltair、Voxel Energy
- **机器人与具身智能（Physical AI）（14）**：Asimov、Brumby (Formerly GrazeMate)、Congruent、Fern、General Astronautics、Hlabs、Human Archive、Mirabelle、OctaPulse、One Robot、Origami Robotics、Remy AI、RoboDock、Servo7
- **开发者与工程设计工具（14）**：/dev/fast、21st、Aemon、Approxima、Aurorin CAD、Corelayer、Emdash、IncidentFox、Lucent、Mendral、OpenSpec、Quotient Labs、REV1、Sparkles
- **医疗健康服务（12）**：Beacon Health、ClaimGlide、Eos AI、Mango Medical、MochaCare、Opalite Health、Overdrive Health、Patientdesk.ai、Prana、Ruma Care、Scheduling Wizard、Tepali
- **法律、合规与政府事务（10）**：Docura Health、Fed10、General Legal、LegalOS、Moritz、Oxus、Payna、Stilta、Vector Legal、Wayco
- **生命科学与AI for Science（10）**：10x Science、Cajal、CellType、Confluence Labs、Ditto Biosciences、Origin、Rhizome AI、Ritivel、Strand AI、Synthetic Sciences
- **消费应用、游戏与AI硬件（7）**：Button Computer、CatchBack Cards、CodeWisp、Doomersion、Fort、Pax Historia、Pocket
- **网络安全与身份（7）**：BeeSafe AI、Crosslayer Labs、Didit、Lexius、Parameter、Polymorph、Protent
- **AI内容创作与媒体（5）**：Cardboard、Martini、Remix、shortkit、Wideframe

## 三、十大创业趋势

### 趋势 1：Agent 从功能变成产品本身，定位是“AI 员工”
- 一句话介绍里的高频表述是 “AI agents that…”、“AI teammates”、“AI employees”、“AI workforce”、“AI operator”，例如 Beacon Health（基层医疗 AI 员工）、Burt（物流 AI 队友）、Ventura（制造与分销 AI 劳动力）、Lance（运营酒店的 AI Agent）。
- 定价逻辑随之变化：对标的是**人力预算**，而不是 IT/SaaS 预算。

### 趋势 2：Agent 经济的配套基础设施成型
Agent 大规模上线后，需要和人类员工一样的一整套配套：
- **身份、权限与控制平面**：Agentic Fabriq、Oximy（影子 AI 治理）
- **护栏、红队与可靠性**：Salus（执行前校验）、Canary（对抗测试）、Sentrial（Agent 版 Datadog）、Moda（Harness 工程）
- **Agent 支付与金融**：Orthogonal（API 按次付费）、Sponge（Agent 经济金融基础设施）、Maven（对话式 Agent 支付）
- **Agent-first 的数据与工具**：Zatanna（把软件变成 Agent API）、VOYGR（给 Agent 的地图 API）、Captain（Agent 文件检索）、21st（Agent 互联网 UI 组件）
- **成本管理**：Carrot Labs（跨供应商 AI 成本归因）、Quotient Labs（Claude Code 成本降 47%）

### 趋势 3：模型层的机会转向“后训练 + 数据 + 评测”
预训练基本被巨头垄断，创业公司集中在下面几个环节：
- **后训练、蒸馏、持续学习**：Cascade、Ashr、Confluence Labs
- **训练数据供给**：Luel（版权合规的多模态数据）、Shofo（视频库）、Human Archive（物理世界数据，团队 100 人，本批最大）
- **评测与 RL 环境**：Polymath（长程 Agent 仿真环境）、Anchorhead（研究 Agent 评测）、ARC Prize Foundation、Traverse（不可验证任务）、Rubric AI（验证）
- **推理效率**：RunAnywhere、Cumulus Labs、Compresr 与 The Token Company（上下文 / Token 压缩）、Piris Labs（AI 网络互连硬件）

### 趋势 4：AI 编程外溢，“Claude Code for X”成为新句式
- 编程工具本身：OpenSpec（规格驱动，GitHub 2 万多星）、Emdash（开源 Agentic 开发环境）、/dev/fast（AI 原生代码托管）
- 编程能力外溢到工程设计：REV1、Aurorin CAD（两家都自称“机械工程师的 Claude Code”）
- 从写代码延伸到**运维代码**：IncidentFox（AI SRE）、Mendral（AI DevOps）、Corelayer（受监管行业 AI 生产工程师）、Chamber（ML 团队 AIOps）

### 趋势 5：AI 原生服务公司（Service-as-Software）
这类公司不卖工具，而是自己成为服务商，用 AI 做到更低成本、更快交付：
- **AI 律所**：Vector Legal、LegalOS（移民）、Moritz（当天交付）、General Legal（25 人，本批第二大团队）、Docura Health（医疗-法律）
- **其他服务**：Overdrive Health（医疗账单）、Panta（商业保险经纪）、Balance（全栈 AI 会计）、MochaCare（照护机构管理）
- **FDE / 转型服务**：Terminal Use、Khotan、Aemon，用“前线部署工程师 + 平台”帮企业重建流程

### 趋势 6：深耕“不性感”的垂直行业
金融（26 家）是最大的单一垂直行业，其次是产业运营（16）、医疗（12）、法律（10）、生命科学（10）。切入点通常很细，例如：
- 电气算量（Bidflow）、医美病历（Tepali）、牙科前台（Patientdesk.ai）、输液诊所（Ruma Care）、家政服务增收（Robby）、设备经销（Chasi）、图书馆（Ossus）、航空运营决策（Zymbly）、渔场质检（OctaPulse）、放牧（Brumby）
- 共同点是：流程重、文档和合规负担大、IT 化程度低，AI Agent 可以直接替代大量人工环节。

### 趋势 7：Physical AI 的瓶颈在数据和评测
- 本体与应用：Origami Robotics（通用操作）、Servo7（集装箱卸货）、Remy AI（仓库灵巧操作）、RoboDock（自动驾驶车队场站）、Mirabelle（家用机器人厨师）
- **数据、仿真与评测**：Asimov（人形机器人动作数据）、Human Archive、Fern（机器人 RL 环境）、One Robot（机器人世界模型）
- **供应链与保险**：Hlabs（美国本土机器人零部件）、Valgo（Physical AI 保险）

### 趋势 8：国防、航天和 AI 能源成为硬科技主线
- **无人机与反无人机**：Seeing Systems（国防无人机）、Milliray（小型无人机探测）、Voltair（对地观测无人机）
- **太空**：GRU Space（月球酒店）、Beyond Reach Labs（太空太阳能阵列）、AxionOrbital（对地观测基础模型）、Constellation Space（卫星网络 OS）
- **AI 算力背后的能源**：Voxel Energy（能源自给数据中心）、Inviscid AI（数据中心物理仿真）、Squid（电网规划 Agent）、Terranox AI（AI 铀矿勘探）

### 趋势 9：金融科技向链上资产和预测市场延伸
- 稳定币、链上资产与预测市场：SpotPay（稳定币全球账户）、Unifold（多链支付）、Sequence Markets（跨加密 / 预测 / 代币化资产执行）、Valence（统一预测市场）、Forum（注意力交易所）
- 传统金融机构的 AI 化：Fenrock（银行 Agent）、Maywood（金融合规主动式 AI）、Copperlane（Agent 化房贷）、Proximitty（商业贷款 OS）、End Close（AI 对账）

### 趋势 10：“AI 攻防”成为安全新主题
- 用 AI 做攻击性安全：Parameter（7×24 AI 渗透测试）
- 防御 AI 驱动的新型攻击：BeeSafe AI（社会工程防御）、Crosslayer Labs（仿冒攻击监测）、Didit（身份与反欺诈）
- 保护 AI 系统本身：Canary、Salus、Agentic Fabriq（见趋势 2）

## 四、其他观察

- **高频措辞**：“AI-native”（24 家）、“Operating System / OS for X”（12 家）、“Agentic”（15 家）。“Copilot”（3 家）明显退潮。
- **消费端的亮点不多**，但方向有特点：AI 录音硬件（Pocket，15 人）、语音 AI 专用硬件（Button Computer）、力量训练可穿戴（Fort）、AI 游戏创作（CodeWisp、Pax Historia）、刷短视频学外语（Doomersion）。
- **地理分布**：旧金山 131 家、纽约 20 家、伦敦 8 家、西雅图 4 家；班加罗尔和多伦多各 3 家；巴黎和悉尼各 2 家。美国以外（已披露地点）共 24 家，约占 12%。
- **团队规模**：中位数 3 人，均值约 4 人；团队最大的是 Human Archive（100 人）和 General Legal（25 人）。
- **状态**：数据中有 3 家已标记为 Inactive（Kyten Technologies、Q2Q、Mendral）。

## 五、对创业者和投资人的启示

1. **单纯的“AI 功能”已经不构成差异化**。能打动 YC 的，要么是在某个垂直行业里吃透一个完整流程，要么是 Agent 规模化之后必须存在的基础设施。
2. **按结果定价、对标人力预算**是 Agent 公司的主流商业模式。AI 原生服务公司把这一点推到极致。
3. **数据和评测是 Physical AI 与前沿模型的共同瓶颈**，也是创业公司相对大厂有机会的环节。
4. **硬科技回潮**：国防、航天、能源等方向在 YC 中的比重上升，AI 算力对能源的需求成为新的叙事。

## 附录：完整公司列表（199 家，按分类排序）

完整数据另见同目录的 `YC-W26-Companies-Classified.csv` / `.xlsx`，包含官网链接、YC 行业标签和状态字段。

| # | 公司 | 分类 | 中文简介 | One-liner（原文） | 地点 | 团队 |
|---:|---|---|---|---|---|---:|
| 1 | [BaseFrame](https://www.ycombinator.com/companies/baseframe) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 识别团队中可被AI自动化的工作 | Detect what AI can automate for your team | San Francisco, CA, USA | 2 |
| 2 | [Booko](https://www.ycombinator.com/companies/booko) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 按时段售卖业务的动态定价 | Dynamically pricing the whole economy. | San Francisco, CA, USA | 2 |
| 3 | [Bubble Lab](https://www.ycombinator.com/companies/bubble-lab) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 活动与社群人脉匹配 | Turn gatherings into lasting relationships. | San Francisco, CA, USA | 2 |
| 4 | [Cardinal](https://www.ycombinator.com/companies/trycardinal-ai) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 面向GTM团队的营收Agent | Revenue Agents for GTM teams | San Francisco, CA, USA | 0 |
| 5 | [Caretta](https://www.ycombinator.com/companies/caretta) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 销售通话实时AI | Realtime AI for Sales Calls | San Francisco, CA, USA | 4 |
| 6 | [Cofia](https://www.ycombinator.com/companies/cofia) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 自动发现并落地内部运营自动化 | AI automations that implement themselves | New York City, NY, USA | 3 |
| 7 | [Corvera](https://www.ycombinator.com/companies/corvera) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 消费品（CPG）品牌AI销售引擎 | The AI sales engine for CPG brands | San Francisco, CA, USA | 4 |
| 8 | [EigenPal](https://www.ycombinator.com/companies/eigenpal) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 企业AI文档工作流 | AI Document Workflows for Enterprises | San Francisco, CA, USA |  |
| 9 | [Fixture](https://www.ycombinator.com/companies/fixture) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 为初创公司打造的AI优先CRM | An AI-first CRM built for Startups | 未披露 | 5 |
| 10 | [Jinba](https://www.ycombinator.com/companies/jinba) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 通过聊天自动化企业工作流 | Automate enterprise workflows through chat | 未披露 | 11 |
| 11 | [Khotan (formerly Pollinate)](https://www.ycombinator.com/companies/khotan) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 前线部署工程师（FDE）平台，把运营重建为软件 | FDE as a platform for rebuilding critical operations in software. | San Francisco, CA, USA | 2 |
| 12 | [Laurence](https://www.ycombinator.com/companies/laurence) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 以量化方法驱动电商广告增长 | Quantitative research for autonomous e-commerce growth | New York City, NY, USA | 2 |
| 13 | [Menza](https://www.ycombinator.com/companies/menza) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 面向消费品牌的AI数据分析师，7×24挖掘增收机会与成本漏洞 | The AI data analyst for consumer brands | London, England, United Kingdom | 3 |
| 14 | [Perfectly](https://www.ycombinator.com/companies/perfectly) | 企业职能AI Agent（销售/营销/客服/HR/运营） | AI原生招聘操作系统 | The AI-native Recruiting OS | San Francisco, CA, USA | 4 |
| 15 | [Pollen](https://www.ycombinator.com/companies/pollen) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 自动化客户成功工作的AI Agent | AI agents that automate customer success | San Francisco, CA, USA | 3 |
| 16 | [RamAIn](https://www.ycombinator.com/companies/ramain) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 用自然语言自动化任意UI任务 | Automate any UI task with natural language | San Francisco, CA, USA | 4 |
| 17 | [Samora AI](https://www.ycombinator.com/companies/samora-ai) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 多语言语音Agent | Multilingual voice agents that outperform humans | 未披露 | 8 |
| 18 | [Signals](https://www.ycombinator.com/companies/signals) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 面向DTC品牌的iMessage复购营收渠道 | iMessage revenue channel for DTC brands that brings customers back | San Francisco, CA, USA | 2 |
| 19 | [Sila](https://www.ycombinator.com/companies/sila) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 人与Agent协作的WhatsApp式通讯 | Agentic Whatsapp | 未披露 | 2 |
| 20 | [Sitefire](https://www.ycombinator.com/companies/sitefire) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 面向Agent化网络的营销套件（GEO） | Marketing suite for the agentic web | BY, Germany | 2 |
| 21 | [Skillsync](https://www.ycombinator.com/companies/skillsync) | 企业职能AI Agent（销售/营销/客服/HR/运营） | AI对话的知识管理（AI聊天版Notion） | Notion for AI chats | San Francisco, CA, USA | 2 |
| 22 | [Terminal Use](https://www.ycombinator.com/companies/terminal-use) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 为运营密集型企业做AI原生流程重塑 | AI-native transformation for operations-heavy companies | San Francisco, CA, USA | 4 |
| 23 | [Turnstone](https://www.ycombinator.com/companies/turnstone) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 懂你的Agent工作空间（第二大脑） | Work with agents that already know you | San Francisco, CA, USA | 3 |
| 24 | [Unisson](https://www.ycombinator.com/companies/unisson) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 自动化B2B软件实施的AI Agent | AI agents that automate B2B software implementation | San Francisco, CA, USA | 2 |
| 25 | [Vela](https://www.ycombinator.com/companies/vela) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 高管猎头AI招聘协调员 | AI Recruiting Coordinator for Executive Search | San Francisco, CA, USA | 2 |
| 26 | [Veriad](https://www.ycombinator.com/companies/veriad) | 企业职能AI Agent（销售/营销/客服/HR/运营） | 广告AI操作系统 | AI operating system for advertising | London, England, United Kingdom | 2 |
| 27 | [Alt-X](https://www.ycombinator.com/companies/alt-x) | 金融科技、会计与保险 | AI原生私募市场流动性交易平台 | Building the best venue for private markets exposure. | Los Angeles, CA, USA | 2 |
| 28 | [Axis](https://www.ycombinator.com/companies/axis-2) | 金融科技、会计与保险 | 交易台AI Copilot | An AI Copilot for Trading Desks | New York City, NY, USA | 2 |
| 29 | [Balance](https://www.ycombinator.com/companies/getbalance) | 金融科技、会计与保险 | 全栈AI会计 | Full-Stack AI Accounting | London, England, United Kingdom | 4 |
| 30 | [Copperlane](https://www.ycombinator.com/companies/copperlane) | 金融科技、会计与保险 | Agent化房贷发放 | Agentic Mortgage Origination | San Francisco, CA, USA | 3 |
| 31 | [End Close](https://www.ycombinator.com/companies/end-close) | 金融科技、会计与保险 | 高交易量支付公司的AI对账 | AI powered reconciliation for high-volume payments companies | 未披露 | 2 |
| 32 | [Fenrock AI](https://www.ycombinator.com/companies/fenrock-ai) | 金融科技、会计与保险 | 银行AI Agent | AI agents for banks | San Francisco, CA, USA | 2 |
| 33 | [Forum](https://www.ycombinator.com/companies/forum) | 金融科技、会计与保险 | 交易注意力的交易所 | The first exchange to trade on attention. | New York City, NY, USA | 2 |
| 34 | [FullSeam](https://www.ycombinator.com/companies/fullseam) | 金融科技、会计与保险 | 企业财务会计团队AI Agent | AI agents for corporate accounting teams | 未披露 | 3 |
| 35 | [Grade](https://www.ycombinator.com/companies/grade) | 金融科技、会计与保险 | 绩效薪酬发放API | API for performance-based payroll | San Francisco, CA, USA | 2 |
| 36 | [Instinct](https://www.ycombinator.com/companies/instinct-xyz) | 金融科技、会计与保险 | AI辅助交易（含加密资产） | Trade with superhuman instinct | San Francisco, CA, USA | 5 |
| 37 | [InventoryQuant](https://www.ycombinator.com/companies/inventoryquant) | 金融科技、会计与保险 | 保险理赔库存清点自动化 | We automate the inventory process in insurance | San Francisco, CA, USA | 1 |
| 38 | [Kita](https://www.ycombinator.com/companies/kita) | 金融科技、会计与保险 | 全球借款人分钟级信贷审核 | Underwrite borrowers around the world in minutes | San Francisco, CA, USA | 3 |
| 39 | [Maywood](https://www.ycombinator.com/companies/maywood) | 金融科技、会计与保险 | 金融合规的7×24主动式AI | The first finance-compliant proactive AI that runs 24/7 | New York City, NY, USA | 5 |
| 40 | [MouseCat](https://www.ycombinator.com/companies/mousecat) | 金融科技、会计与保险 | 打击金融犯罪的AI（反洗钱/合规） | AI to fight financial crime | New York City, NY, USA | 6 |
| 41 | [o11](https://www.ycombinator.com/companies/o11) | 金融科技、会计与保险 | 金融机构的AI数据仓库 | The AI Data Warehouse For Financial Firms | New York City, NY, USA | 2 |
| 42 | [Palus Finance](https://www.ycombinator.com/companies/palus-finance) | 金融科技、会计与保险 | 初创公司财务顾问 | Your startup's financial advisor | 未披露 | 2 |
| 43 | [Panta](https://www.ycombinator.com/companies/panta) | 金融科技、会计与保险 | AI原生商业保险经纪 | AI Native Commercial Insurance Brokerage | San Francisco, CA, USA | 3 |
| 44 | [Proximitty](https://www.ycombinator.com/companies/proximitty) | 金融科技、会计与保险 | 商业贷款AI操作系统 | AI operating system for commercial loans | San Francisco, CA, USA | 2 |
| 45 | [Q2Q](https://www.ycombinator.com/companies/q2q) | 金融科技、会计与保险 | 帮助私募股权团队快速找到收购标的 | We help private equity teams find acquisition targets faster | San Francisco, CA, USA | 2 |
| 46 | [Sequence Markets](https://www.ycombinator.com/companies/sequence-markets) | 金融科技、会计与保险 | 跨加密、预测市场与代币化资产的低延迟执行 | Low-latency execution across crypto, prediction, and tokenized assets | Toronto, ON, Canada | 5 |
| 47 | [SpotPay](https://www.ycombinator.com/companies/spotpay) | 金融科技、会计与保险 | 稳定币全球银行账户 | Stablecoin Global Bank Account | San Francisco, CA, USA | 2 |
| 48 | [Unifold](https://www.ycombinator.com/companies/unifold) | 金融科技、会计与保险 | 多链充值与支付基础设施 | Multi-chain deposit and payment infrastructure | New York City, NY, USA | 3 |
| 49 | [Valence](https://www.ycombinator.com/companies/valence) | 金融科技、会计与保险 | 统一预测市场交易平台 | Unified prediction markets trading platform | San Francisco, CA, USA | 3 |
| 50 | [Valgo](https://www.ycombinator.com/companies/valgo) | 金融科技、会计与保险 | 具身/物理AI的保险风险层 | Insurance risk layer for physical AI | San Francisco, CA, USA | 3 |
| 51 | [Verdex](https://www.ycombinator.com/companies/verdex) | 金融科技、会计与保险 | 保险AI核验 | AI Verification for Insurance | San Francisco, CA, USA | 2 |
| 52 | [ZeroSettle](https://www.ycombinator.com/companies/zerosettle) | 金融科技、会计与保险 | App内购直付账单SDK | Drop-in Direct Billing SDK for In-App Purchases | San Diego, CA, USA | 2 |
| 53 | [Anchorhead](https://www.ycombinator.com/companies/anchorhead) | AI基础设施与模型层 | 前沿研究Agent的评测 | Evals for frontier research agents | San Francisco, CA, USA | 1 |
| 54 | [ARC Prize Foundation](https://www.ycombinator.com/companies/arc-prize-foundation) | AI基础设施与模型层 | 衡量通用智能的AI基准（ARC-AGI）基金会 | AI benchmarks that measure general intelligence and inspire new ideas | San Francisco, CA, USA; Remote | 4 |
| 55 | [Ashr](https://www.ycombinator.com/companies/ashr) | AI基础设施与模型层 | 企业级后训练、监控与持续学习平台 | Enterprise post-training, monitoring, and continual learning platform | San Francisco, CA, USA | 2 |
| 56 | [Autumn AI](https://www.ycombinator.com/companies/autumn-ai) | AI基础设施与模型层 | 全网人物与公司信息索引/实体解析 | Everything on anyone. | San Francisco, CA, USA | 2 |
| 57 | [Byteport](https://www.ycombinator.com/companies/byteport) | AI基础设施与模型层 | 1GB–100TB文件全球上传加速网络 | Global upload acceleration for 1GB-100TB files. | San Francisco, CA, USA | 4 |
| 58 | [Cascade](https://www.ycombinator.com/companies/cascade) | AI基础设施与模型层 | 用专有数据蒸馏/对齐模型 | Distilling Proprietary Intelligence | San Francisco, CA, USA | 2 |
| 59 | [Chamber](https://www.ycombinator.com/companies/chamber) | AI基础设施与模型层 | 面向ML团队的AIOps Agent | The AIOps Agent for ML Teams | Seattle, WA, USA | 4 |
| 60 | [Compresr](https://www.ycombinator.com/companies/compresr) | AI基础设施与模型层 | LLM上下文压缩以提升准确率 | LLM context compression for better accuracy | San Francisco, CA, USA | 3 |
| 61 | [Cumulus Labs](https://www.ycombinator.com/companies/cumulus-labs) | AI基础设施与模型层 | 高速多模态推理操作系统 | The Fastest Multimodal Inference OS | San Francisco, CA, USA | 2 |
| 62 | [Envariant](https://www.ycombinator.com/companies/envariant) | AI基础设施与模型层 | 基础模型可解释性与推理基础设施 | Interpretability and reasoning infra for foundation models. | San Francisco, CA, USA | 1 |
| 63 | [Luel](https://www.ycombinator.com/companies/luel) | AI基础设施与模型层 | 版权合规的多模态训练数据采购与授权 | Turning everyday words and actions into usable training data. | San Francisco, CA, USA | 12 |
| 64 | [Mantis](https://www.ycombinator.com/companies/mantis) | AI基础设施与模型层 | LLM+物理仿真的人类数字孪生，预测人类行为 | Digital Twins of humans | New York City, NY, USA | 3 |
| 65 | [Ndea](https://www.ycombinator.com/companies/ndea-com) | AI基础设施与模型层 | 构建具备创新能力的AGI研究实验室 | Building AGI that can innovate. | Remote | 15 |
| 66 | [Overshoot](https://www.ycombinator.com/companies/overshoot) | AI基础设施与模型层 | 实时视觉应用AI基础设施 | AI Infra for real-time vision applications | San Francisco, CA, USA | 5 |
| 67 | [Piris Labs](https://www.ycombinator.com/companies/pirislabs) | AI基础设施与模型层 | AI集群的网络互连层（硬件） | The Networking Layer of AI | San Francisco, CA, USA | 8 |
| 68 | [Polymath](https://www.ycombinator.com/companies/polymath) | AI基础设施与模型层 | 训练与评测长程Agent的仿真环境 | Simulation environments to train & evaluate long-horizon AI agents | San Francisco, CA, USA | 6 |
| 69 | [Rubric AI](https://www.ycombinator.com/companies/rubric-ai) | AI基础设施与模型层 | AI推理与验证基础设施 | Reasoning and verification infra for AI | New York City, NY, USA | 1 |
| 70 | [RunAnywhere](https://www.ycombinator.com/companies/runanywhere) | AI基础设施与模型层 | 开源模型本地/托管/端侧的高速推理 | Fastest inference anywhere: open models on-prem, hosted or on-device | San Francisco, CA, USA | 5 |
| 71 | [Shofo](https://www.ycombinator.com/companies/shofo) | AI基础设施与模型层 | 全球最大视频库（训练数据） | The World's Largest Video Library | San Francisco, CA, USA | 4 |
| 72 | [Talking Computers](https://www.ycombinator.com/companies/talking-computers) | AI基础设施与模型层 | 语音Agent实时交互模型 | Real-time interaction models for voice agents | Toronto, ON, Canada | 2 |
| 73 | [The Token Company](https://www.ycombinator.com/companies/the-token-company) | AI基础设施与模型层 | 提升LLM输出的压缩中间件 | Compression middleware that improves LLM outputs | San Francisco, CA, USA | 2 |
| 74 | [Traverse](https://www.ycombinator.com/companies/traverse) | AI基础设施与模型层 | 解决不可验证任务的研究实验室（RL） | Research lab solving non-verifiable work | San Francisco, CA, USA | 1 |
| 75 | [Velum Labs](https://www.ycombinator.com/companies/velum-labs) | AI基础设施与模型层 | 跨数据栈的数据质量操作系统 | The OS for data quality across any stack | San Francisco, CA, USA | 2 |
| 76 | [AutoSitu](https://www.ycombinator.com/companies/autositu) | 垂直产业运营（建筑/物流/制造/酒店等） | 建成环境（房地产/建筑）AI操作系统 | The AI operating system for the built world | 未披露 | 2 |
| 77 | [Avoice](https://www.ycombinator.com/companies/avoice) | 垂直产业运营（建筑/物流/制造/酒店等） | 建筑/工程/施工（AEC）AI原生工作空间 | AI-native workspace for AEC | San Francisco, CA, USA | 7 |
| 78 | [Bidflow](https://www.ycombinator.com/companies/bidflow) | 垂直产业运营（建筑/物流/制造/酒店等） | 电气工程AI算量（Takeoff），自动识别图纸估算材料 | AI Takeoffs for Electrical | New York City, NY, USA | 2 |
| 79 | [Burt](https://www.ycombinator.com/companies/burt) | 垂直产业运营（建筑/物流/制造/酒店等） | 物流行业AI队友 | AI teammates for logistics | San Francisco, CA, USA | 2 |
| 80 | [Chasi](https://www.ycombinator.com/companies/chasi) | 垂直产业运营（建筑/物流/制造/酒店等） | 设备行业AI营收引擎 | AI Revenue Engine for the Equipment Industry | San Francisco, CA, USA | 2 |
| 81 | [Foreman](https://www.ycombinator.com/companies/foreman) | 垂直产业运营（建筑/物流/制造/酒店等） | 让承包商少坐办公室的施工AI | Keeping contractors on the job site, not behind a desk. | San Francisco, CA, USA | 2 |
| 82 | [Haladir](https://www.ycombinator.com/companies/haladir) | 垂直产业运营（建筑/物流/制造/酒店等） | 全球物流的运营超级智能 | Operational Superintelligence for Global Logistics | San Francisco, CA, USA | 4 |
| 83 | [Inviscid AI](https://www.ycombinator.com/companies/inviscid-ai) | 垂直产业运营（建筑/物流/制造/酒店等） | 工业设施与数据中心实时物理仿真 | Real-time Physics Simulations for Industrial Facilities & Data Centers | Singapore, Singapore; Remote | 2 |
| 84 | [Lance](https://www.ycombinator.com/companies/lance) | 垂直产业运营（建筑/物流/制造/酒店等） | 运营酒店的AI Agent | AI Agents That Run Hotel Operations. | San Francisco, CA, USA | 10 |
| 85 | [Ossus](https://www.ycombinator.com/companies/ossus) | 垂直产业运营（建筑/物流/制造/酒店等） | 文化机构（图书馆）AI操作系统 | Intelligence for cultural institutions | San Francisco, CA, USA | 3 |
| 86 | [Reframe](https://www.ycombinator.com/companies/usereframe) | 垂直产业运营（建筑/物流/制造/酒店等） | AI原生硬件零部件采购市场 | AI-native, hardware procurement marketplace | San Francisco, CA, USA | 1 |
| 87 | [Revion](https://www.ycombinator.com/companies/revion) | 垂直产业运营（建筑/物流/制造/酒店等） | 汽车经销/运营智能 | Intelligence for Automotive Operations | New York City, NY, USA | 10 |
| 88 | [Robby](https://www.ycombinator.com/companies/robby) | 垂直产业运营（建筑/物流/制造/酒店等） | 为家政/家庭服务企业增收的AI Agent | AI agents that grow revenue for home services businesses | New York City, NY, USA | 3 |
| 89 | [Travo](https://www.ycombinator.com/companies/travo) | 垂直产业运营（建筑/物流/制造/酒店等） | 房地产与建筑领域（官方未披露详情） | . | San Francisco, CA, USA | 4 |
| 90 | [Ventura](https://www.ycombinator.com/companies/ventura) | 垂直产业运营（建筑/物流/制造/酒店等） | 分销商与制造商的AI劳动力 | AI Workforce for Distributors and Manufacturers | San Francisco, CA, USA | 2 |
| 91 | [Zymbly](https://www.ycombinator.com/companies/zymbly) | 垂直产业运营（建筑/物流/制造/酒店等） | 航空运营团队决策支持 | The decision-support layer for aviation ops teams to know what to do… | London, England, United Kingdom | 0 |
| 92 | [Agentic Fabriq](https://www.ycombinator.com/companies/agentic-fabriq) | Agent基础设施与AI治理 | AI Agent的控制平面（身份、权限、安全） | The control plane for AI agents. | San Francisco, CA, USA | 2 |
| 93 | [Canary](https://www.ycombinator.com/companies/canary) | Agent基础设施与AI治理 | 攻击你AI系统的对抗式AI（红队） | Adversarial AI that breaks your AI | San Francisco, CA, USA | 2 |
| 94 | [Captain](https://www.ycombinator.com/companies/captain) | Agent基础设施与AI治理 | 为AI Agent提供自调优的文件检索 | Self-tuning file search for AI agents | San Francisco, CA, USA | 2 |
| 95 | [Carrot Labs](https://www.ycombinator.com/companies/carrot-labs) | Agent基础设施与AI治理 | 跨供应商的AI成本追踪与归因 | AI Cost Management: Track and attribute AI spend across every provider | San Francisco, CA, USA | 2 |
| 96 | [Klaus AI](https://www.ycombinator.com/companies/klaus-ai) | Agent基础设施与AI治理 | 云端托管的安全OpenClaw个人Agent实例 | Fast and Safe OpenClaw on the cloud | San Francisco, CA, USA | 2 |
| 97 | [Maven](https://www.ycombinator.com/companies/maven) | Agent基础设施与AI治理 | 对话式Agent支付基础设施 | Payments Infrastructure for Conversational Agents | San Francisco, CA, USA | 2 |
| 98 | [Moda](https://www.ycombinator.com/companies/moda) | Agent基础设施与AI治理 | Agent Harness工程基础设施 | Harness Engineering Infrastructure that developers love. | San Francisco, CA, USA | 6 |
| 99 | [Orthogonal](https://www.ycombinator.com/companies/orthogonal) | Agent基础设施与AI治理 | 面向API的Agent支付 | Agentic Payments for APIs | San Francisco, CA, USA | 2 |
| 100 | [Oximy](https://www.ycombinator.com/companies/oximy) | Agent基础设施与AI治理 | 管理企业内已在使用的AI（影子AI治理） | Take command of the AI your company already runs on. | San Francisco, CA, USA | 8 |
| 101 | [Ressl AI](https://www.ycombinator.com/companies/ressl-ai) | Agent基础设施与AI治理 | 训练、评测与构建自主Agent | Train, eval and build autonomous agents | Bengaluru, KA, India | 3 |
| 102 | [Salus](https://www.ycombinator.com/companies/salus) | Agent基础设施与AI治理 | Agent动作执行前的校验护栏 | Guardrails to validate your agent's actions before they execute | San Francisco, CA, USA | 2 |
| 103 | [Sentrial](https://www.ycombinator.com/companies/sentrial) | Agent基础设施与AI治理 | Agent可靠性监控（Agent版Datadog） | Datadog for Agent Reliability | San Francisco, CA, USA | 2 |
| 104 | [Sponge](https://www.ycombinator.com/companies/sponge) | Agent基础设施与AI治理 | Agent经济的金融基础设施 | Financial infrastructure for the agent economy | San Francisco, CA, USA | 3 |
| 105 | [VOYGR](https://www.ycombinator.com/companies/voygr) | Agent基础设施与AI治理 | 面向AI应用与Agent的实时地点情报API | Real-world place intelligence for AI apps and agents | San Francisco, CA, USA |  |
| 106 | [Zatanna](https://www.ycombinator.com/companies/zatanna) | Agent基础设施与AI治理 | 把所有软件变成Agent优先的API | Turning all software into agent-first APIs | San Francisco, CA, USA | 2 |
| 107 | [AxionOrbital Space](https://www.ycombinator.com/companies/axionorbital-space) | 航天、国防、能源与硬科技 | 7×24对地观测基础模型 | Foundation models for 24/7 Earth Observation | San Francisco, CA, USA | 2 |
| 108 | [Beyond Reach Labs](https://www.ycombinator.com/companies/beyond-reach-labs) | 航天、国防、能源与硬科技 | 在轨展开至足球场大小的太空太阳能阵列 | Space solar arrays that grow to the size of a football field in orbit | New York City, NY, USA | 8 |
| 109 | [Condor Energy](https://www.ycombinator.com/companies/condor-energy) | 航天、国防、能源与硬科技 | 企业能源采购软件 | Software for enterprise energy procurement. | Paris, Île-de-France, France | 3 |
| 110 | [Constellation Space](https://www.ycombinator.com/companies/constellation-space) | 航天、国防、能源与硬科技 | 超大规模卫星网络AI操作系统 | AI operating system for mega-scale satellite networks. | Seattle, WA, USA | 4 |
| 111 | [DAIVIN!](https://www.ycombinator.com/companies/daivin) | 航天、国防、能源与硬科技 | 无气瓶潜水装备（海陆空呼吸自主） | Tankless Dive Gear - Breath Autonomy at Sea, Land & Space | San Francisco, CA, USA | 1 |
| 112 | [Galactic Resource Utilization Space, Inc. (GRU Space)](https://www.ycombinator.com/companies/galactic-resource-utilization-space-inc-gru-space) | 航天、国防、能源与硬科技 | 月球酒店与地外建设公司 | Moon Hotel -> The Intergalactic Construction Company of Earth | Los Angeles, CA, USA | 5 |
| 113 | [Kyten Technologies](https://www.ycombinator.com/companies/kyten-technologies) | 航天、国防、能源与硬科技 | 定制航空级电池包 | Custom Aerospace-Grade Battery Packs | Seattle, WA, USA | 2 |
| 114 | [Milliray](https://www.ycombinator.com/companies/milliray) | 航天、国防、能源与硬科技 | 小型无人机探测与追踪 | Technology to detect and track small drones | London, England, United Kingdom | 3 |
| 115 | [Seeing Systems](https://www.ycombinator.com/companies/seeing-systems) | 航天、国防、能源与硬科技 | 模块化AI指挥的国防无人机 | Modular AI-Commanded Drones for Defence | London, England, United Kingdom | 7 |
| 116 | [Squid](https://www.ycombinator.com/companies/squid) | 航天、国防、能源与硬科技 | 电网规划AI Agent | AI agents for power grid planning  🦑 | London, England, United Kingdom | 3 |
| 117 | [Terranox AI](https://www.ycombinator.com/companies/terranox-ai) | 航天、国防、能源与硬科技 | AI驱动的铀矿勘探 | The first AI-powered uranium discovery company | San Francisco, CA, USA | 2 |
| 118 | [Visibl Semiconductors](https://www.ycombinator.com/companies/visibl-semiconductors) | 航天、国防、能源与硬科技 | 电力电子定制芯片 | Custom silicon for power electronics | San Francisco, CA, USA | 3 |
| 119 | [Voltair](https://www.ycombinator.com/companies/voltair) | 航天、国防、能源与硬科技 | 对地观测自主无人机 | Autonomous Drones for Earth Observation | San Francisco, CA, USA | 5 |
| 120 | [Voxel Energy](https://www.ycombinator.com/companies/voxel-energy) | 航天、国防、能源与硬科技 | 太阳能+退役电池的能源自给数据中心 | Energy independent data centers with solar and repurposed batteries. | 未披露 | 3 |
| 121 | [Asimov](https://www.ycombinator.com/companies/asimov) | 机器人与具身智能（Physical AI） | 为人形机器人采集真实人类动作数据 | Real-world human movement data for humanoid robots | San Francisco, CA, USA; Remote | 3 |
| 122 | [Brumby (Formerly GrazeMate)](https://www.ycombinator.com/companies/brumby) | 机器人与具身智能（Physical AI） | 用AI无人机放牧的“机器人牛仔” | Robot Cowboys that Herd Cattle with AI Drones | Sydney, NSW, Australia | 3 |
| 123 | [Congruent](https://www.ycombinator.com/companies/congruent) | 机器人与具身智能（Physical AI） | 自动驾驶汽车AI原生雷达 | AI native radars for self-driving cars | San Francisco, CA, USA | 2 |
| 124 | [Fern](https://www.ycombinator.com/companies/fern-bot) | 机器人与具身智能（Physical AI） | 为机器人公司提供强化学习环境 | RL environments for robotics companies | 未披露 | 2 |
| 125 | [General Astronautics](https://www.ycombinator.com/companies/generalastro) | 机器人与具身智能（Physical AI） | 面向太空研发的机器人 | Robotics for Space R&D | San Francisco, CA, USA | 2 |
| 126 | [Hlabs](https://www.ycombinator.com/companies/hlabs) | 机器人与具身智能（Physical AI） | 美国本土制造的机器人零部件 | US-Made Parts for Robots | Austin, TX, USA | 1 |
| 127 | [Human Archive](https://www.ycombinator.com/companies/human-archive) | 机器人与具身智能（Physical AI） | 物理AI数据实验室（传感器采集与模型） | Physical AI data lab | San Francisco, CA, USA | 100 |
| 128 | [Mirabelle](https://www.ycombinator.com/companies/mirabelle) | 机器人与具身智能（Physical AI） | 家用机器人厨师 | Your robot chef | Paris, Île-de-France, France | 2 |
| 129 | [OctaPulse](https://www.ycombinator.com/companies/octapulse) | 机器人与具身智能（Physical AI） | 渔场质检的视觉+机器人自动化 | CV and robotics to automate quality inspection in fish farms | 未披露 | 2 |
| 130 | [One Robot](https://www.ycombinator.com/companies/one-robot) | 机器人与具身智能（Physical AI） | 用于机器人评测与训练的世界模型 | World models for robot evals and training. | San Francisco, CA, USA | 2 |
| 131 | [Origami Robotics](https://www.ycombinator.com/companies/origami-robotics) | 机器人与具身智能（Physical AI） | 可操作任意物体的机器人 | Manipulate Anything Robot | San Francisco, CA, USA | 5 |
| 132 | [Remy AI](https://www.ycombinator.com/companies/remy-ai) | 机器人与具身智能（Physical AI） | 仓库灵巧操作AI机器人 | Automating dexterous tasks in warehouses with AI-powered robots | San Francisco, CA, USA | 2 |
| 133 | [RoboDock](https://www.ycombinator.com/companies/robodock) | 机器人与具身智能（Physical AI） | 为自动驾驶车队运营自动化场站的机器人 | Robots that run autonomous depots for autonomous fleets. | San Francisco, CA, USA | 4 |
| 134 | [Servo7](https://www.ycombinator.com/companies/servo7) | 机器人与具身智能（Physical AI） | 仓库集装箱卸货机器人 | Container unloading robots for warehouses | Amsterdam, NH, Netherlands | 3 |
| 135 | [/dev/fast](https://www.ycombinator.com/companies/devfast) | 开发者与工程设计工具 | AI原生代码托管与协作平台 | /dev/fast is the AI-native code forge | San Francisco, CA, USA | 4 |
| 136 | [21st](https://www.ycombinator.com/companies/21st) | 开发者与工程设计工具 | 面向Agent互联网的UI组件 | UI building blocks for the agentic internet | San Francisco, CA, USA | 3 |
| 137 | [Aemon](https://www.ycombinator.com/companies/aemon) | 开发者与工程设计工具 | 前线部署的AI研究工程师，自动演化最优解 | The Forward-Deployed AI Research Engineer | San Francisco, CA, USA | 3 |
| 138 | [Approxima](https://www.ycombinator.com/companies/approxima) | 开发者与工程设计工具 | 自我构建的软件 | Your software should build itself. | Toronto, ON, Canada | 2 |
| 139 | [Aurorin CAD](https://www.ycombinator.com/companies/aurorin-cad) | 开发者与工程设计工具 | 面向机械工程师的“Claude Code”（CAD） | Claude code for Mechanical Engineers | San Francisco, CA, USA | 1 |
| 140 | [Corelayer](https://www.ycombinator.com/companies/corelayer) | 开发者与工程设计工具 | 受监管行业的AI生产工程师 | AI production engineer for regulated industries | San Francisco, CA, USA | 3 |
| 141 | [Emdash](https://www.ycombinator.com/companies/emdash) | 开发者与工程设计工具 | 开源Agentic开发环境 | Open-source Agentic Development Environment | San Francisco, CA, USA | 2 |
| 142 | [IncidentFox](https://www.ycombinator.com/companies/brownie) | 开发者与工程设计工具 | 分诊、协调并修复线上事故的AI SRE Agent | AI SRE agent that triages, coordinates, and fixes production incidents | San Francisco, CA, USA | 2 |
| 143 | [Lucent](https://www.ycombinator.com/companies/lucent) | 开发者与工程设计工具 | 根据用户行为自动改进产品的AI产品经理 | AI that automatically improves products from user behavior | San Francisco, CA, USA | 2 |
| 144 | [Mendral](https://www.ycombinator.com/companies/mendral) | 开发者与工程设计工具 | AI DevOps工程师 | AI DevOps Engineer | San Francisco, CA, USA | 2 |
| 145 | [OpenSpec](https://www.ycombinator.com/companies/openspec) | 开发者与工程设计工具 | 面向编码Agent的规格驱动开发框架（开源） | Plan mode for complex features | Sydney, NSW, Australia |  |
| 146 | [Quotient Labs](https://www.ycombinator.com/companies/quotient-labs) | 开发者与工程设计工具 | 一行安装让Claude Code成本降低47% | Use Claude Code at 47% less cost in one line of installation. | San Francisco, CA, USA | 2 |
| 147 | [REV1](https://www.ycombinator.com/companies/rev1) | 开发者与工程设计工具 | 面向机械工程师的“Claude Code” | Claude Code for Mechanical Engineers | San Francisco, CA, USA | 2 |
| 148 | [Sparkles](https://www.ycombinator.com/companies/sparkles) | 开发者与工程设计工具 | 让团队每个人都能当工程师 | Make everyone on your team an engineer | London, England, United Kingdom | 1 |
| 149 | [Beacon Health](https://www.ycombinator.com/companies/beacon-health) | 医疗健康服务 | 基层医疗的AI员工 | AI Employees for Primary Care | San Francisco, CA, USA | 2 |
| 150 | [ClaimGlide](https://www.ycombinator.com/companies/claimglide) | 医疗健康服务 | 为私人诊所自动完成医保预授权 | AI automated prior-auths for private medical practices | Seattle, WA, USA | 1 |
| 151 | [Eos AI](https://www.ycombinator.com/companies/eos-ai) | 医疗健康服务 | 医疗机构自治运营系统 | Autonomous OS for healthcare | San Francisco, CA, USA | 2 |
| 152 | [Mango Medical](https://www.ycombinator.com/companies/mango-medical-inc) | 医疗健康服务 | 骨科手术规划基础模型 | Foundation models for planning orthopedic surgery | 未披露 | 3 |
| 153 | [MochaCare](https://www.ycombinator.com/companies/mochacare) | 医疗健康服务 | 照护机构Agent化管理服务 | Agentic Management Service for Care Organizations | San Francisco, CA, USA | 2 |
| 154 | [Opalite Health](https://www.ycombinator.com/companies/opalite-health) | 医疗健康服务 | 帮助医疗机构跨语言沟通 | Helping Healthcare Providers Speak Any Language | San Francisco, CA, USA | 3 |
| 155 | [Overdrive Health](https://www.ycombinator.com/companies/overdrive-health) | 医疗健康服务 | AI原生医疗账单代理服务 | AI-Native Medical Billing Services | New York City, NY, USA | 1 |
| 156 | [Patientdesk.ai](https://www.ycombinator.com/companies/patientdeskai) | 医疗健康服务 | 牙科诊所前后台AI Agent | AI front & back office agent for dental practices | 未披露 | 5 |
| 157 | [Prana](https://www.ycombinator.com/companies/prana-health) | 医疗健康服务 | 口袋里的AI全科医生 | An AI primary care doctor in your pocket | San Francisco, CA, USA | 4 |
| 158 | [Ruma Care](https://www.ycombinator.com/companies/ruma-care) | 医疗健康服务 | 生物制剂输液诊所运营系统 | The operations stack for biologic infusion clinics | San Francisco, CA, USA | 5 |
| 159 | [Scheduling Wizard](https://www.ycombinator.com/companies/scheduling-wizard) | 医疗健康服务 | 医疗运营排班与调度基础设施 | Logistics infrastructure to modernize healthcare operations | Washington, DC, USA | 3 |
| 160 | [Tepali](https://www.ycombinator.com/companies/tepali) | 医疗健康服务 | 医美与健康诊所AI电子病历 | AI EMR for medspas & wellness clinics | New York City, NY, USA | 2 |
| 161 | [Docura Health](https://www.ycombinator.com/companies/docura-health) | 法律、合规与政府事务 | AI原生医疗-法律（Med-Legal）事务所 | AI-Native Med-Legal Firm | San Francisco, CA, USA | 3 |
| 162 | [Fed10](https://www.ycombinator.com/companies/fed10) | 法律、合规与政府事务 | 政府事务AI Agent | AI Agents for Government Affairs | San Francisco, CA, USA | 3 |
| 163 | [General Legal](https://www.ycombinator.com/companies/general-legal) | 法律、合规与政府事务 | 面向高增长公司的精英AI律所 | Elite AI law firm for high growth companies | 未披露 | 25 |
| 164 | [LegalOS](https://www.ycombinator.com/companies/legalos) | 法律、合规与政府事务 | AI原生移民律所 | The AI-Native Immigration Law Firm | San Francisco, CA, USA; Remote | 3 |
| 165 | [Moritz](https://www.ycombinator.com/companies/moritz) | 法律、合规与政府事务 | 全球AI原生律所，当天交付法律工作 | Global AI-native law firm handling legal work with same-day turnaround | Oslo, Oslo, Norway | 10 |
| 166 | [Oxus](https://www.ycombinator.com/companies/oxus) | 法律、合规与政府事务 | 内部审计流程AI自动化 | AI-powered automation for internal audit workflows | San Francisco, CA, USA | 3 |
| 167 | [Payna](https://www.ycombinator.com/companies/payna) | 法律、合规与政府事务 | 受监管行业的AI牌照申请Agent | AI Licensing Agent for Regulated Industries | San Francisco, CA, USA | 2 |
| 168 | [Stilta](https://www.ycombinator.com/companies/stilta) | 法律、合规与政府事务 | 知识产权领域Agentic AI | Agentic AI for intellectual property | Stockholm, Stockholm County, Sweden | 4 |
| 169 | [Vector Legal](https://www.ycombinator.com/companies/vector-legal) | 法律、合规与政府事务 | 面向初创公司的AI原生律所与法律操作系统 | A premier AI-native law firm & legal operating system for Startups. | San Francisco, CA, USA | 7 |
| 170 | [Wayco](https://www.ycombinator.com/companies/wayco) | 法律、合规与政府事务 | 医疗-法律案件AI操作员 | AI operator for medlegal cases | New York City, NY, USA | 5 |
| 171 | [10x Science](https://www.ycombinator.com/companies/10x-science) | 生命科学与AI for Science | AI原生蛋白质表征平台 | The AI-native platform for next-generation protein characterization. | San Francisco, CA, USA | 5 |
| 172 | [Cajal](https://www.ycombinator.com/companies/cajal-technologies) | 生命科学与AI for Science | 规模化形式化验证加速科学发现 | Scaling formal verification to accelerate scientific discovery | San Francisco, CA, USA | 2 |
| 173 | [CellType](https://www.ycombinator.com/companies/celltype) | 生命科学与AI for Science | 模拟人体生物学的Agent化药企 | The agentic drug company. We simulate human biology. | New York City, NY, USA | 5 |
| 174 | [Confluence Labs](https://www.ycombinator.com/companies/confluence-labs) | 生命科学与AI for Science | 从经验中学习的AI模型（数据稀缺的科学领域） | AI models that learn from experience | San Francisco, CA, USA | 2 |
| 175 | [Ditto Biosciences](https://www.ycombinator.com/companies/ditto-biosciences) | 生命科学与AI for Science | 自身免疫病的进化智能药物发现 | Evolutionary intelligence for autoimmune disease | San Francisco, CA, USA | 3 |
| 176 | [Origin](https://www.ycombinator.com/companies/origin-bio) | 生命科学与AI for Science | 癌症疗法的AI与数据平台 | AI and Data for Cancer Therapeutics | San Francisco, CA, USA | 4 |
| 177 | [Rhizome AI](https://www.ycombinator.com/companies/rhizome-ai) | 生命科学与AI for Science | 生命科学Agent平台 | Agent Platform for Life Sciences | New York City, NY, USA; Remote | 1 |
| 178 | [Ritivel](https://www.ycombinator.com/companies/ritivel) | 生命科学与AI for Science | 生命科学文档AI原生平台 | AI-native platform for Life-Sciences Documentation | Bengaluru, KA, India | 3 |
| 179 | [Strand AI](https://www.ycombinator.com/companies/strand-ai) | 生命科学与AI for Science | 多模态基础模型预测未采集的患者生物学数据 | Multimodal foundation models to predict uncollected patient biology | San Francisco, CA, USA | 2 |
| 180 | [Synthetic Sciences](https://www.ycombinator.com/companies/synthetic-sciences) | 生命科学与AI for Science | 自主科学（Autonomous Science）基础设施 | Infrastructure for Autonomous Science | San Francisco, CA, USA | 2 |
| 181 | [Button Computer](https://www.ycombinator.com/companies/button-computer) | 消费应用、游戏与AI硬件 | 为语音AI打造的微型计算机硬件 | The tiny computer built for voice AI. | San Francisco, CA, USA | 1 |
| 182 | [CatchBack Cards](https://www.ycombinator.com/companies/catchback-cards) | 消费应用、游戏与AI硬件 | 数字收藏卡包开包游戏 | The most thrilling way to create and rip digital collectible packs | San Francisco, CA, USA | 7 |
| 183 | [CodeWisp](https://www.ycombinator.com/companies/codewisp) | 消费应用、游戏与AI硬件 | 人人都能用AI做游戏 | Anyone can create real games with AI | San Francisco, CA, USA | 3 |
| 184 | [Doomersion](https://www.ycombinator.com/companies/doomersion) | 消费应用、游戏与AI硬件 | 刷短视频学外语 | Doomscroll to learn languages | San Francisco, CA, USA; Remote | 4 |
| 185 | [Fort](https://www.ycombinator.com/companies/fort) | 消费应用、游戏与AI硬件 | 力量训练可穿戴设备 | Strength Tracking Wearable | San Francisco, CA, USA | 4 |
| 186 | [Pax Historia](https://www.ycombinator.com/companies/pax-historia) | 消费应用、游戏与AI硬件 | AI世界构建与游戏平台 | The first AI-powered worldbuilding and gameplay platform | San Francisco, CA, USA | 6 |
| 187 | [Pocket](https://www.ycombinator.com/companies/pocket) | 消费应用、游戏与AI硬件 | AI录音笔硬件（现实世界记笔记） | Take Notes in the Real World | San Francisco, CA, USA | 15 |
| 188 | [BeeSafe AI](https://www.ycombinator.com/companies/beesafe-ai) | 网络安全与身份 | 防御社会工程攻击的前沿AI | Frontier AI Defenses for Social Engineering Attacks | San Francisco, CA, USA | 3 |
| 189 | [Crosslayer Labs](https://www.ycombinator.com/companies/crosslayer-labs) | 网络安全与身份 | 从外部监测并防御网站/API仿冒攻击 | Protect, monitor and defend your Internet presence | New York City, NY, USA | 3 |
| 190 | [Didit](https://www.ycombinator.com/companies/didit) | 网络安全与身份 | 身份认证与反欺诈基础设施 | Infrastructure for identity and fraud. | San Francisco, CA, USA | 16 |
| 191 | [Lexius](https://www.ycombinator.com/companies/lexius) | 网络安全与身份 | 企业安防摄像头AI | AI for Corporate Security Cameras | San Francisco, CA, USA | 3 |
| 192 | [Parameter](https://www.ycombinator.com/companies/parameter) | 网络安全与身份 | 持续渗透测试的AI安全Agent | Security builds trust. Strengthen both, all on one platform. | San Francisco, CA, USA | 14 |
| 193 | [Polymorph](https://www.ycombinator.com/companies/polymorph) | 网络安全与身份 | 构建安全的多态应用 | Building secure polymorphic apps | San Francisco, CA, USA | 4 |
| 194 | [Protent](https://www.ycombinator.com/companies/protent) | 网络安全与身份 | 面向执法与安保团队的实时情报 | Real time intelligence for law enforcement & security teams. | San Francisco, CA, USA | 2 |
| 195 | [Cardboard](https://www.ycombinator.com/companies/cardboard) | AI内容创作与媒体 | Agent化视频编辑器 | Agentic video editor | Bengaluru, KA, India | 8 |
| 196 | [Martini](https://www.ycombinator.com/companies/martini) | AI内容创作与媒体 | 专业AI视频制作 | AI Video Production for Professionals | San Francisco, CA, USA | 2 |
| 197 | [Remix](https://www.ycombinator.com/companies/remix-3) | AI内容创作与媒体 | 用已有素材自动生成社交媒体内容 | Social media content auto-generated with your existing data | San Francisco, CA, USA | 0 |
| 198 | [shortkit](https://www.ycombinator.com/companies/shortkit) | AI内容创作与媒体 | 为消费App提供短视频媒体基础设施 | Media infra for consumer apps | 未披露 | 2 |
| 199 | [Wideframe](https://www.ycombinator.com/companies/wideframe) | AI内容创作与媒体 | 视频剪辑师的AI同事 | AI coworker for video editors to ship more video faster | San Francisco, CA, USA | 2 |
