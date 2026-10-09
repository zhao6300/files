# 开源大模型分类榜单汇总

> 整理时间：2026-10-09
>
> 本文按照 **Text、Image、Video、Audio、Retrieval、Decision** 六类模型整理开源模型榜单。除特别说明外，“开源”采用 Artificial Analysis 的 **Open Weights** 口径：模型权重可以下载，或可以通过供应商提供的推理运行时自行部署。这一口径不一定等同于 OSI 法律意义上的开源许可证。

## 一、口径说明

| 类别 | 采用榜单 | 主要指标 |
|---|---|---|
| Text | Artificial Analysis LLM Leaderboard | Intelligence Index |
| Image | Artificial Analysis Text-to-Image Open Weights Leaderboard | Arena Elo |
| Video | Artificial Analysis Text-to-Video / Image-to-Video Open Weights Leaderboard | Arena Elo |
| Audio | Artificial Analysis Text-to-Speech Open Weights Leaderboard | Arena Elo |
| Retrieval | MTEB RTEB(beta) 榜单 | 检索任务综合排名 |
| Decision | Benchmark Heaven JevBench v1.6.1 | Capability Score |

不同榜单的评分不可直接横向比较。例如，Text 的 Intelligence 分数、Image/Video/Audio 的 Elo、Retrieval 的检索分数，以及 Decision 的 Capability Score 都属于不同评价体系。

## 二、Text：开源文本模型 Top 10

来源：[Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models?weights=open)。榜单将同一模型的不同推理强度配置作为独立条目。

| 排名 | 模型 | Intelligence |
|---:|---|---:|
| 1 | MiMo-V2.6-Pro | 46 |
| 2 | GLM-5.3（max） | 45 |
| 3 | Kimi K3（max） | 44 |
| 4 | GLM-5.3-Flash | 42 |
| 5 | Qwen3.8 2.4T A95B | 40 |
| 6 | Qwen3.8-Flash-Next | 40 |
| 7 | DeepSeek V4.1 Flash（max） | 39 |
| 8 | MiMo-V2.6-Flash | 38 |
| 9 | DeepSeek V4 Pro 0813（max） | 36 |
| 10 | GLM-5.3（low） | 34 |

**简要观察：** MiMo、GLM、Kimi、Qwen 和 DeepSeek 构成当前开源文本模型的主要前列阵营。若按模型家族去重，GLM-5.3、MiMo-V2.6、Qwen3.8 和 DeepSeek V4 系列最突出。

## 三、Image：开源图像模型 Top 10

来源：[AA-Image-T2I v2.0 Open Weights Leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image/open-weights)。该榜单评估文生图质量。

| 排名 | 模型 | Elo |
|---:|---|---:|
| 1 | Qwen-Image-2.1 | 1035 |
| 2 | Ideogram 4.0（Quality） | 1012 |
| 3 | Ideogram 4.0 | 1004 |
| 4 | FLUX.2 [dev] | 1000 |
| 5 | Qwen Image Max 2512 | 999 |
| 6 | FLUX.2 [dev] Turbo | 998 |
| 7 | Ming-Image-0.1-Design | 997 |
| 8 | HunyuanImage 3.0 Instruct | 996 |
| 9 | Cosmos3-Super-Text2Image（agentic） | 994 |
| 10 | FLUX.2 [dev] Flash | 987 |

**简要观察：** Qwen-Image-2.1 暂列第一；Ideogram、FLUX、HunyuanImage 和 Cosmos 系列也进入前十。榜单中的不同推理/速度版本仍分别计名次。

## 四、Video：开源视频模型

### 4.1 文生视频

来源：[AA-Video-T2V v2.0 Open Weights Leaderboard](https://artificialanalysis.ai/video/leaderboard/text-to-video/open-weights)。该榜单目前只有 5 个开源权重模型，因此不使用闭源模型补足到 10 个。

| 排名 | 模型 | Elo |
|---:|---|---:|
| 1 | MiniMax H3（768p） | 1137 |
| 2 | LTX-2.5 Fast | 946 |
| 3 | LTX-2.5 Pro | 943 |
| 4 | LTX-2.3 Pro | 892 |
| 5 | LTX-2.3 Fast | 855 |

### 4.2 图生视频补充

为补充视频类别的覆盖，增加 Artificial Analysis 图生视频开源榜的 3 个模型。由于任务不同，下面的 Elo **不能与文生视频分数直接比较**。

来源：[AA-Video-I2V v1.0 Open Weights Leaderboard](https://artificialanalysis.ai/video/leaderboard/image-to-video/open-weights)。

| 来源 | 模型 | Elo |
|---|---|---:|
| 图生视频 | MAGI-2 Preview | 1093 |
| 图生视频 | LTX-2 Fast | 923 |
| 图生视频 | LTX-2 Pro | 863 |

**简要观察：** 开源视频模型的公开可比样本明显少于图像和语音模型。MAGI-2 Preview 在榜单中标记为 Coming soon，使用时需要确认实际 API 或权重可用性。

## 五、Audio：开源语音生成模型 Top 10

本文 Audio 采用 TTS（Text-to-Speech）口径，即文本转语音质量，不代表 ASR（语音识别）能力。

来源：[Artificial Analysis Text-to-Speech Open Weights Leaderboard](https://artificialanalysis.ai/text-to-speech/leaderboard/provider-voice/open-weights)。

| 排名 | 模型 | Elo |
|---:|---|---:|
| 1 | Breeze TTS 2 | 1222 |
| 2 | Fish Audio S2 Pro | 1116 |
| 3 | Step Audio EditX（Mar 2026） | 1097 |
| 4 | Voxtral TTS | 1085 |
| 5 | Magpie-Multilingual 357M | 1065 |
| 6 | Kokoro 82M v1.0 | 1065 |
| 7 | Maya 1 | 1048 |
| 8 | OpenAudio S1 Mini | 1045 |
| 9 | Higgs Audio V3 TTS | 1038 |
| 10 | Chatterbox | 1028 |

**简要观察：** Breeze TTS 2 暂列开源 TTS 榜首；Fish Audio、Step Audio、Voxtral、Kokoro 和 Chatterbox 适合重点关注。若目标是语音识别，应另看 ASR 榜单，不能用 TTS 排名替代。

## 六、Retrieval：开源 Embedding 模型 Top 10

Artificial Analysis 的 Search API 榜单评估的是 Perplexity、Exa、Brave、OpenAI Web Search 等搜索服务，并不是可下载部署的 Retrieval 模型。因此本节改用 **MTEB RTEB(beta)**，它更专注于检索质量。

数据来源：[MTEB Leaderboard API](https://mteb-leaderboard-backend.hf.space)。筛选规则为榜单自带的 `openWeights=true`，并剔除同一模型的 INT8 量化重复版本。

| 开源排名 | 模型 | 参数规模 | 许可证 | RTEB 总榜位置 |
|---:|---|---:|---|---:|
| 1 | nvidia/Nemotron-3-Embed-8B-BF16 | 8.0B | OpenMDW-1.1 | 2 |
| 2 | Octen/Octen-Embedding-8B | 7.6B | Apache-2.0 | 3 |
| 3 | Octen/Octen-Embedding-4B | 4.0B | Apache-2.0 | 7 |
| 4 | bflhc/MoD-Embedding | 4.0B | Apache-2.0 | 9 |
| 5 | nvidia/Nemotron-3-Embed-1B-BF16 | 1.1B | OpenMDW-1.1 | 14 |
| 6 | Qwen/Qwen3-Embedding-8B | 7.6B | Apache-2.0 | 15 |
| 7 | codefuse-ai/F2LLM-v2-14B | 14B | Apache-2.0 | 16 |
| 8 | codefuse-ai/F2LLM-v2-8B | 7.6B | Apache-2.0 | 17 |
| 9 | Octen/Octen-Embedding-0.6B | 0.6B | Apache-2.0 | 21 |
| 10 | codefuse-ai/F2LLM-v2-4B | 4.0B | Apache-2.0 | 23 |

**注意事项：**

- RTEB 榜单的前列包含闭源 Voyage 模型，因此开源排名与总榜排名不同。
- 本表按 embedding 模型统计，不包含 reranker。
- Nemotron 3 Embed 8B 和 1B 的公开发布信息还可参考 [NVIDIA 论坛公告](https://forums.developer.nvidia.com/t/nvidia-nemotron-3-embed-is-out-and-the-8b-model-is-1-on-rteb/377089)。
- 不同检索任务、语言、向量维度和数据域可能导致实际排序变化，生产部署前应使用自己的 query-document 标注集验证。

## 七、Decision：Jev 类开源决策模型 Top 10

这里不再使用 GDPval-AA。GDPval 测量的是复杂知识工作和文档生成，不属于 Jev 类判别式决策模型。

本节采用 [Benchmark Heaven JevBench v1.6.1](https://benchmarkheaven.com/jev-models)。JevBench 的输入是状态和有界规则，输出是类型化答案及概率；主榜只排名开源权重模型。榜单的 Capability Score 由 Intelligence 与 Calibration 平均得到。

| 排名 | 模型 | 底座 | Capability | Intelligence | Calibration |
|---:|---|---|---:|---:|---:|
| 1 | Quyet-1.0-Large | Gemma-4-31B | 81.7 | 73.4 | 90.0 |
| 2 | decisio v0.8.0 on gemma-4-31B-it | Gemma-4-31B | 79.6 | 70.4 | 88.7 |
| 3 | deck-31B | Gemma-4-31B | 77.6 | 73.0 | 82.2 |
| 4 | René-1 31B FP8 | Gemma-4-31B | 76.0 | 61.7 | 90.2 |
| 5 | H2O-Lightning-4B v1.1 | 4B | 75.0 | 60.0 | 90.0 |
| 6 | Bobcat Flash 1.2 | – | 73.5 | 65.8 | 81.2 |
| 7 | Surogate Rune 26B-A4B v3 | – | 73.5 | 56.1 | 90.9 |
| 8 | decider-12b v2 | Gemma-4-12B | 72.5 | 63.0 | 82.0 |
| 9 | Xor 26B-A4B | – | 72.4 | 58.7 | 86.1 |
| 10 | decider-12b v1 | Gemma-4-12B | 72.2 | 60.6 | 83.8 |
| — | **Laya** | — | **未公开** | — | — |

> Laya 是重要的 Jev-like 开源决策模型候选，但当前快照没有公开可直接映射到 JevBench Capability Score 的成绩，因此作为未排名候选加入，不参与前十排序。

**补充说明：**

- TypeSafe Jev 1.13.0 是闭源 API，在 JevBench 中只作为参考，不参与开源模型排名。
- JevBench 还提供考虑成本和延迟的综合排序；如果生产场景更关注低延迟和低成本，应同时查看 Cost 和 Latency。
- `autotrust/JEV-9B` 与 `autotrust/JEV-27B` 是接近 Jev 行为的开源模型，但在本次榜单快照中还没有进入 JevBench 主榜，因此没有擅自插入排名。
- Laya 在另一项 `decision-models-under-pressure` 独立评测中报告为 Jev 准确率的 90%；该结果与 JevBench Capability Score 不同，不能直接混排。

## 八、最终结论

| 类别 | 当前开源榜首 | 采用指标 |
|---|---|---|
| Text | MiMo-V2.6-Pro | Intelligence 46 |
| Image | Qwen-Image-2.1 | Elo 1035 |
| Video（文生） | MiniMax H3（768p） | Elo 1137 |
| Audio（TTS） | Breeze TTS 2 | Elo 1222 |
| Retrieval（Embedding） | Nemotron-3-Embed-8B-BF16 | RTEB 开源排名第 1 |
| Decision（Jev 类） | Quyet-1.0-Large | Capability 81.7 |

### 选型方向

- **通用文本生成：** 优先比较 MiMo、GLM、Kimi、Qwen 和 DeepSeek；部署时重点核对显存、上下文长度和许可证。
- **图像生成：** Qwen-Image、FLUX、HunyuanImage 是开源权重阵营的主要选择。
- **视频生成：** MiniMax H3 和 LTX 系列是当前榜单中的主要开源候选，但显存和推理速度要求较高。
- **语音生成：** Breeze TTS 2 适合作为榜首候选，Fish Audio、Kokoro 和 Chatterbox 可作为轻量或备选方案。
- **检索：** Nemotron 3 Embed 8B 追求质量，Nemotron 1B 和 Octen 0.6B/4B 更适合控制部署成本；Qwen3-Embedding-8B 是 Apache-2.0 生态中的重要选择。
- **结构化决策：** 不要用通用 LLM 的 Intelligence Index 替代 JevBench；Quyet、decisio、deck、H2O-Lightning 和 decider 系列更符合“状态输入、结构化决策输出”的模型定义。

## 九、数据限制

1. 所有排名都是指定榜单和快照时间下的结果，模型发布和榜单更新会改变名次。
2. Elo、Intelligence、RTEB 和 Capability Score 不可横向比较。
3. “开源”在不同榜单中主要表示 Open Weights；商业使用前仍需逐个核对许可证。
4. Video 的开源候选目前不足 10 个，因此本文没有用闭源模型填充。
5. Retrieval 本文使用 embedding 榜；如果实际系统需要 reranking，应单独评估 reranker。
6. Decision 本文使用 JevBench；如果目标是安全审核、意图路由或工具选择，应使用与具体业务更匹配的测试集重新评估。

本文内容是对各榜单信息的整理和改写，模型名称、排名及分数以原始榜单的最新版本为准。
