# LLM Inference SLO 技术分享

面向非专业听众的推理系统 SLO 讲解材料，主题：**从延迟指标到 Goodput 优化**。

> **最新版本：** [`slo-goodput-v2/`](slo-goodput-v2/) —— 32 页图表版，一页一图、大字号、附逐页预览图与讲稿备注。下面的根目录文件为早期 20 页版本，保留备查。

## 文件说明

| 文件 | 说明 |
|---|---|
| [`slo-goodput-v2/`](slo-goodput-v2/) | **32 页图表版**：PPT、32 张预览图、生成脚本与讲稿备注 |
| `LLM-Inference-SLO-Goodput.pptx` | 可编辑 PPT，20 页，16:9，浅色风格（英文文件名，便于下载） |
| `LLM_Inference_SLO_Goodput_技术分享.pptx` | 同一份 PPT 的中文文件名副本 |
| `slo-deck.html` | 网页版，浏览器直接打开；可用「打印 → 另存为 PDF」导出 |
| `generate_slo_ppt.py` | PPT 生成脚本，便于批量调整配色与文案 |

## 内容结构

1. **为什么需要 SLO** — 从「机器跑得快」到「用户体验可承诺」
2. **TTFT 与 TPOT** — 一次回答中的两个关键体验时刻
3. **延迟从哪里来** — 队列、调度、KV 获取、Prefill、传输
4. **持续生成** — Decode 节奏、PD 资源干扰、Chunked Prefill 取舍
5. **系统控制面** — 架构、调度、执行、内存、通信五层旋钮
6. **最终目标** — 在 TTFT / TPOT 约束下最大化 Goodput

## 重新生成 PPT

```bash
pip install python-pptx
python generate_slo_ppt.py
```
