# MILES 强化学习完整流程

> 本文基于 `radixark/miles` 源码整理，重点解释从 prompt 采样、SGLang rollout、reward 计算、训练数据转换、advantage/loss 计算，到 Actor 权重同步回推理引擎的完整链路。
>
> 参考仓库：[radixark/miles](https://github.com/radixark/miles)

## 1. 整体架构

MILES 是面向大规模 LLM/VLM post-training 的分布式 RL 框架。它将推理 rollout 与训练 backend 解耦：SGLang 负责高吞吐生成，Megatron/FSDP 负责 Actor/Critic 训练，Ray 负责组件编排和数据引用传输。

```text
Prompt Dataset
      │
      ▼
SGLang Rollout Engines
      │  response + rollout logprob
      ▼
Reward Model / Agent Environment
      │ reward
      ▼
Rollout Data Conversion
      │ tokens / rewards / masks / logprobs
      ▼
Megatron / FSDP Actor Training
      │ optimizer.step()
      ▼
Actor 新权重
      │
      ▼
同步回 SGLang
```

MILES 的几个核心对象：

| 对象 | 作用 |
|---|---|
| Prompt dataset | 提供问题、标签、工具调用信息和多模态输入 |
| Rollout engine | 使用 SGLang 生成回答或 agent trajectory |
| Reward model | 将 `(prompt, response, label)` 转成 reward |
| Actor | 被 RL 更新的策略模型 |
| Critic | PPO 中估计 value，可选 |
| Reference | 冻结的参考策略，用于 KL 约束 |

对应官方概念文档：[docs/user-guide/concepts.md](https://github.com/radixark/miles/blob/main/docs/user-guide/concepts.md)。

## 2. 启动流程

通常用户通过 `scripts/run_*.py` 启动。Launch script 主要组装模型、checkpoint、rollout、reward、GRPO/PPO 和 Ray 参数，真正的训练入口是：

- [train.py](https://github.com/radixark/miles/blob/main/train.py)：同步 RL；
- [train_async.py](https://github.com/radixark/miles/blob/main/train_async.py)：普通 async 和 fully async RL。

同步入口的初始化顺序是：

```text
parse_args()
    │
    ▼
init_orchestration_script()
    │
    ▼
create_rollout_components()
    ├── InferenceController
    └── RolloutExecutor
    │
    ▼
create_training_models()
    ├── Actor
    └── Critic（PPO 可选）
    │
    ▼
Actor → SGLang 初始权重同步
```

### InferenceController

`InferenceController` 管理 SGLang engine 的生命周期，负责：

- 启动或发现 SGLang servers；
- 等待 engine ready；
- 准备 rollout 和 evaluation；
- 暂停/恢复 generation；
- offload/onload 权重和 KV cache；
- 为权重同步返回可更新的 engine 集合。

源码：[miles/ray/rollout/inference_controller.py](https://github.com/radixark/miles/blob/main/miles/ray/rollout/inference_controller.py)。

### RolloutExecutor

`RolloutExecutor` 是 rollout 侧的总入口，负责：

1. 初始化 DataSource；
2. 加载 rollout function；
3. 执行生成；
4. 执行 reward；
5. 过滤和整理 Sample；
6. 转成训练数据；
7. 按 DP rank 切 shard；
8. 将 shard 放入 object store。

源码：[miles/ray/rollout/rollout_executor.py](https://github.com/radixark/miles/blob/main/miles/ray/rollout/rollout_executor.py)。

## 3. Prompt 到 Sample

默认数据源位于 [miles/rollout/data_source.py](https://github.com/radixark/miles/blob/main/miles/rollout/data_source.py)。它会加载 JSONL 或用户指定的数据源，并使用 tokenizer/processor 处理：

```python
Dataset(
    args.prompt_data,
    tokenizer=tokenizer,
    processor=processor,
    prompt_key=args.input_key,
    label_key=args.label_key,
    metadata_key=args.metadata_key,
    tool_key=args.tool_key,
)
```

每条数据会变成一个 `Sample`。它包含：

```python
Sample(
    prompt=...,
    tokens=...,
    response=...,
    response_length=...,
    label=...,
    reward=...,
    loss_mask=...,
    rollout_log_probs=...,
    group_index=...,
    index=...,
    weight_versions=...,
)
```

如果：

```text
rollout_batch_size = 64
n_samples_per_prompt = 8
```

那么一轮会读取 64 个 prompt，并为每个 prompt 生成 8 个 response：

```text
64 个 prompt × 8 个 response = 512 个 Sample
```

内部首先保持 group 结构：

```text
[
  [sample_0_0, ..., sample_0_7],
  [sample_1_0, ..., sample_1_7],
  ...
]
```

同一个 prompt 产生的 sibling sample 拥有相同的 `group_index`，这是 GRPO 进行组内 reward 对比的基础。

## 4. Rollout 生成

默认 class-based rollout function 是：

```text
miles.rollout.inference_rollout.inference_rollout_common.InferenceRolloutFn
```

调用链如下：

```text
RolloutExecutor.get()
    │
    ▼
InferenceRolloutFn
    │
    ▼
generate_rollout_async()
    │
    ▼
generate_and_rm_group()
    │
    ▼
SGLang /generate
```

相关源码：

- [inference_rollout_common.py](https://github.com/radixark/miles/blob/main/miles/rollout/inference_rollout/inference_rollout_common.py)；
- [inference_rollout_train.py](https://github.com/radixark/miles/blob/main/miles/rollout/inference_rollout/inference_rollout_train.py)。

`generate_rollout_async()` 会反复执行：

```text
从 DataSource 取 prompt group
        │
        ▼
提交异步 generation task
        │
        ▼
等待 task 完成
        │
        ▼
执行 dynamic filter
        │
        ▼
直到收集够 rollout_batch_size 个 group
```

如果部分 group 被 dynamic filter 丢弃，系统会继续采样，因此通常还需要：

```text
over_sampling_batch_size >= rollout_batch_size
```

### 单条 SGLang 请求

默认生成函数位于 [single_turn.py](https://github.com/radixark/miles/blob/main/miles/rollout/generate_hub/single_turn.py)。

流程是：

```text
Sample.prompt
    │
    ▼
tokenizer / processor
    │
    ▼
prompt token ids
    │
    ▼
构造 SGLang /generate 请求
    │
    ▼
SGLang Router
    │
    ▼
SGLang engine
```

请求通常包含：

```python
{
    "input_ids": input_ids,
    "sampling_params": {
        "temperature": ...,
        "top_p": ...,
        "top_k": ...,
        "max_new_tokens": ...,
    },
    "return_logprob": True,
}
```

根据配置，还可以返回：

- sampling support mask；
- MoE routed experts；
- indexer top-k；
- rollout top-k logprobs；
- 每个 token 的 weight version。

SGLang 返回后，MILES 直接将生成 token 和 logprob 写入 `Sample`：

```python
sample.tokens += new_response_tokens
sample.response_length += len(new_response_tokens)
sample.response += output["text"]
sample.rollout_log_probs += new_response_log_probs
```

这样避免：

```text
token ids → detokenize 成字符串 → 再重新 tokenize
```

从而降低 rollout token 与训练 token 不一致的风险。

## 5. Reward 计算

生成完成后，MILES 会调用 `generate_and_rm()` 或 `generate_and_rm_group()`。

源码：[inference_rollout_common.py](https://github.com/radixark/miles/blob/main/miles/rollout/inference_rollout/inference_rollout_common.py)。

如果 Sample 在 agent 环境中没有提前设置 reward，则调用：

```python
sample.reward = await async_rm(args, sample)
```

如果启用 group reward：

```text
--group-rm
```

则等一个 prompt 的所有 sibling 生成完成后，再批量调用 reward function。

Reward hub 位于：[miles/rollout/rm_hub](https://github.com/radixark/miles/tree/main/miles/rollout/rm_hub)。

内置 reward 类型包括：

```text
remote_rm
math
dapo
deepscaler
gemma_math
f1
gpqa
ifbench
random
deterministic_random
```

也可以通过 `--custom-rm-path` 注入自定义 reward model。自定义 reward 可以接收单条 Sample，也可以接收整个 group。

Agentic rollout 中，reward 还可以在工具调用和环境交互期间直接写入 `sample.reward`。如果 reward 已存在，MILES 不会重复计算。

## 6. Agent / Environment Rollout

MILES 的 rollout function 不局限于单轮问答，也支持 coding agent、computer-use、工具调用和多轮环境交互。

一个 agent trajectory 可能是：

```text
用户问题
   │
   ▼
模型生成工具调用
   │
   ▼
环境执行工具
   │
   ▼
返回 observation
   │
   ▼
模型继续生成
   │
   ▼
最终完成 trajectory
```

自定义 generate function 接收 `GenerateFnInput`，可以修改：

```python
sample.response
sample.tokens
sample.loss_mask
sample.reward
sample.metadata
sample.rollout_id
```

其中：

```text
loss_mask = 1：该 token 参与 loss
loss_mask = 0：该 token 不参与 loss
```

因此工具 observation 可以保留在上下文中，但不参与策略梯度。

## 7. Rollout 数据转换

生成得到的 Sample 会被 `RolloutExecutor.get()` 转成训练数据：

```python
convert_samples_to_train_data(...)
```

实现：[train_data_conversion.py](https://github.com/radixark/miles/blob/main/miles/ray/rollout/train_data_conversion.py)。

核心字段大致为：

```python
{
    "tokens": ...,
    "response_lengths": ...,
    "rewards": ...,
    "raw_reward": ...,
    "loss_masks": ...,
    "sample_indices": ...,
    "rollout_ids": ...,
    "rollout_log_probs": ...,
    "weight_versions": ...,
}
```

### Loss mask

没有显式 mask 时，默认只训练 response：

```python
sample.loss_mask = [1] * sample.response_length
```

prompt token 用作上下文，但默认不参与 loss。如果 `sample.remove_sample=True`，则整条 response 的 mask 会被置零。

### Reward normalization

GRPO 通常在同一个 prompt 的 sibling response 之间做归一化：

```text
r_i' = r_i - mean(r_group)
```

如果启用标准差归一化，则进一步计算：

```text
r_i' = (r_i - mean(r_group)) / (std(r_group) + ε)
```

同一个 rollout 的 sibling sample 必须共享一个 reward。MILES 会检查这一点。

### DP 分片

随后根据 Actor 的并行配置将训练数据切分到 DP rank：

```text
global rollout data
        │
        ▼
DP rank 0 shard
DP rank 1 shard
DP rank 2 shard
...
```

每个 shard 会放入 object store，训练 Actor 只读取自己对应的 shard。

## 8. 四个 batch 参数

MILES 有一个重要约束：

```text
rollout_batch_size × n_samples_per_prompt
  = global_batch_size × num_steps_per_rollout
```

例如：

```text
rollout_batch_size = 64
n_samples_per_prompt = 8
global_batch_size = 128
```

则：

```text
总 Sample 数 = 64 × 8 = 512
num_steps_per_rollout = 512 / 128 = 4
```

一次 rollout 会被训练成 4 个 optimizer step。

注意：

- `rollout_batch_size` 是 prompt group 数量；
- `global_batch_size` 是 Sample 数量，不是 prompt 数量；
- `micro_batch_size` 只负责拆分显存中的 micro-batch；
- dynamic batch 会按照 token 数量重新构造 micro-batch schedule。

约束校验位于 [miles/utils/arguments.py](https://github.com/radixark/miles/blob/main/miles/utils/arguments.py)。

## 9. 训练侧加载数据

训练 Actor 通过 `get_rollout_data()` 从 object store 获取数据：

```text
Object Store
    │
    ▼
CPU rollout data
    │
    ▼
GPU tokens / masks
    │
    ▼
Context Parallel 切分
    │
    ▼
micro-batch iterator
```

实现：[training_utils/data/rollout.py](https://github.com/radixark/miles/blob/main/miles/backends/training_utils/data/rollout.py)。

训练侧会处理：

- tokens 搬到 GPU；
- loss mask 对齐；
- THD/BSHD 数据布局；
- Context Parallel 切片；
- multimodal inputs；
- rollout logprob 的 CP 对齐；
- dynamic micro-batch schedule。

训练过程中 prompt token 仍然参与模型 forward，但通过 loss mask 排除在最终 policy loss 之外。

## 10. Reference、Old Actor 和 Critic

### Reference model

如果启用了 KL 约束，训练需要计算：

```text
log πθ(y|x)
log πref(y|x)
```

其中 `πref` 是冻结参考模型。Megatron backend 使用 model tag/backup 在 `actor`、`ref`、`old_actor`、`teacher` 之间切换。

### Old actor / behavior policy

PPO 需要 old policy 的 logprob。它可以来自：

1. 训练前重新计算的 Actor logprob；
2. SGLang 在 rollout 时记录的 `rollout_log_probs`；
3. async PPO 中保存的 `old_actor`。

异步训练中，生成时的策略和训练时的策略可能不同，因此不能默认完全 on-policy。

### Critic

PPO 的 critic 会先训练：

```text
critic forward
    │
    ▼
value predictions
    │
    ▼
GAE advantages / returns
    │
    ▼
critic value loss + optimizer.step()
```

然后把 values 通过 object store 传给 Actor。同步训练中，顺序是：

```text
Rollout → Critic → Actor
```

GRPO 通常不需要 Critic。

## 11. Advantage 和 Return

入口函数：

```python
compute_advantages_and_returns(args, rollout_data)
```

实现：[objective.py](https://github.com/radixark/miles/blob/main/miles/backends/training_utils/loss/objective.py)。

它会：

1. 取得 Actor logprob；
2. 取得 Reference logprob；
3. 计算 KL；
4. 选择 advantage estimator；
5. 计算 advantages 和 returns；
6. 可选执行 distributed whitening；
7. 写回 `rollout_data`。

### GRPO

GRPO 将每条 response 的 scalar reward 广播到该 response 的有效 token：

```text
advantage[token] = normalized_group_reward
```

因此 GRPO 不需要 critic，组内 reward 差异本身就充当 baseline。

### GSPO

GSPO 在 sequence 级别计算 old/current logprob 差异和 KL，再将 sequence-level 信号广播回 token。因此可以概括为：

```text
GRPO：token-level policy ratio
GSPO：sequence-level policy ratio
```

### PPO

PPO 将 reward 分成两部分：

```text
token_reward[t] = -kl_coef × KL[t]
terminal_reward[last_token] += environment_reward
```

然后用 critic value 计算 GAE：

```text
δ_t = r_t + γ V(s_{t+1}) - V(s_t)
A_t = δ_t + γλ A_{t+1}
return_t = A_t + V(s_t)
```

### REINFORCE++

REINFORCE++ 不依赖 critic，而是从 response 末尾反向累积 discounted return，同时将 KL penalty 合并进 token reward。

实现入口：[advantages.py](https://github.com/radixark/miles/blob/main/miles/backends/training_utils/loss/hub/advantages.py)。

## 12. Policy Loss

核心实现：[losses.py](https://github.com/radixark/miles/blob/main/miles/backends/training_utils/loss/hub/losses.py)。

训练 Actor 对同一批 token 做 forward，得到当前策略 logprob：

```text
log πθ
```

然后与 old policy 比较：

```text
ppo_kl = log πold - log πθ
ratio = exp(log πθ - log πold)
       = exp(-ppo_kl)
```

PPO-style clipped objective 为：

```text
pg_loss_1 = -ratio × advantage
pg_loss_2 = -clip(ratio, 1 - ε_low, 1 + ε_high) × advantage
pg_loss   = max(pg_loss_1, pg_loss_2)
```

最终 loss 可能还包含：

```text
policy gradient loss
- entropy_coef × entropy
+ kl_loss_coef × reference KL loss
```

MILES 会记录：

```text
pg_loss
entropy_loss
pg_clipfrac
ppo_kl
kl_loss
ess_ratio
tis / ois
```

如果启用 TIS，则使用 rollout logprob 和训练 logprob 计算截断 importance sampling weight：

```text
w = exp(log πtrain - log πrollout)
w = clamp(w, tis_clip_low, tis_clip)
```

## 13. Actor optimizer step

Megatron Actor 的训练入口是：

```python
actor_model.train(rollout_id, rollout_data_pack)
```

核心顺序：

```text
1. 读取 rollout data
2. 创建 data iterator
3. Reference forward（如果需要）
4. Actor/old Actor logprob forward
5. 读取 Critic values（PPO）
6. 计算 advantages / returns
7. 构造 micro-batch
8. forward
9. policy/value loss
10. backward
11. gradient synchronization
12. optimizer.step()
```

Megatron backend 将底层计算交给 Megatron pipeline。TorchNative/FSDP backend 通过 `StepRunner.forward_backward_step()` 和 `apply_step()` 执行相同的 RL objective。

因此不同 backend 共享：

```text
rollout data
advantage / return
policy loss
KL / clipping 逻辑
```

差异主要在：

```text
模型分片、并行执行、checkpoint、权重迭代器
```

## 14. 同步训练完整流程

`train.py` 的核心循环可以概括为：

```python
for rollout_id in range(start_rollout_id, num_rollout):
    await inference_controller.prepare_rollout(rollout_id)

    rollout_data_pack = await rollout_executor.get(rollout_id)

    if args.use_critic:
        values = await critic_model.train(rollout_id, rollout_data_pack)
        await actor_model.train(
            rollout_id,
            rollout_data_pack,
            external_data=values,
        )
    else:
        await actor_model.train(rollout_id, rollout_data_pack)

    save / eval
    await update_weights(...)
```

对应的时序是：

```text
第 N 轮：

Actor 当前权重
      │
      ▼
SGLang 生成 rollout
      │
      ▼
Reward model / environment 打分
      │
      ▼
转换为训练 batch
      │
      ▼
Critic 更新（PPO 可选）
      │
      ▼
Actor 计算 advantage 和 loss
      │
      ▼
optimizer.step()
      │
      ▼
Actor 新权重同步回 SGLang
      │
      ▼
第 N+1 轮
```

## 15. 普通 Async RL

`train_async.py` 会提前启动下一轮 generation：

```python
rollout_data_next_future = await eager_create_task(
    prepare_and_generate(start_rollout_id)
)
```

训练第 N 批时，第 N+1 批已经在生成：

```text
当前 batch rollout ───────┐
                          ├── 当前 batch training
下一 batch rollout ───────┘
```

其目标是将单轮耗时从：

```text
rollout_time + train_time
```

降低到接近：

```text
max(rollout_time, train_time)
```

当到达 `update_weights_interval` 时，普通 async 会先等待正在进行的 generation 完成，再同步新权重，避免一次 generation 中途更换模型。

## 16. Fully Async RL

Fully async 的实现位于：

- [fully_async_rollout.py](https://github.com/radixark/miles/blob/main/miles/rollout/fully_async_rollout.py)；
- [fully_async_data_buffer.py](https://github.com/radixark/miles/blob/main/miles/rollout/fully_async_data_buffer.py)。

它使用长期运行的 producer：

```text
Producer：
  取 prompt → SGLang 生成 → reward → DataBuffer.put()

Consumer：
  DataBuffer.get() → Actor training
```

DataBuffer 在 `put` 时过滤：

- aborted group；
- 缺少 reward 的 group；
- dynamic filter 拒绝的 group。

在 `get` 时过滤：

- 超过 `max_weight_staleness` 的 group；
- 版本过旧的 rollout 数据。

未使用的 group 可以：

```text
drop：直接丢弃
retry：放回 data source 重新生成
```

Fully async 的主要风险是 off-policy：

```text
生成时权重版本 ≠ 训练时权重版本
```

因此需要结合：

```text
weight_version
max_weight_staleness
use_rollout_logprobs
use_tis
keep_old_actor
```

进行过滤或重要性采样修正。

## 17. Rollout logprob 与训练 logprob

这是阅读 MILES 时最容易混淆的地方。

### `rollout_log_probs`

由 SGLang 在真实生成过程中记录，表示 behavior policy 对已采样 token 的 logprob。

### `log_probs`

由训练 Actor 对相同 token 重新 forward 得到的 logprob。

默认情况下，MILES 可以重新使用训练 Actor 计算 old policy logprob。如果启用：

```text
--use-rollout-logprobs
```

则 policy loss 的 old-policy denominator 使用 SGLang 记录的 rollout logprob，更适合 async 或 train/inference 存在差异的场景。

## 18. 权重同步

训练完成后，MILES 通过 `update_weights()` 将 Actor 新权重传回 SGLang：

```text
1. inference_controller.start_update_weights()
2. 暂停 SGLang generation / health monitoring
3. actor_model.update_weights()
4. WeightUpdater 读取 Actor 权重
5. 按 bucket 发送权重
6. SGLang reload 权重
7. 设置新的 weight_version
8. 恢复 generation
9. RolloutExecutor 记录新版本
```

相关源码：

- [placement_group.py](https://github.com/radixark/miles/blob/main/miles/ray/placement_group.py)；
- [megatron_utils/actor.py](https://github.com/radixark/miles/blob/main/miles/backends/megatron_utils/actor.py)；
- [weight_update/updater.py](https://github.com/radixark/miles/blob/main/miles/backends/training_utils/weight_update/updater.py)；
- [sglang_api_client.py](https://github.com/radixark/miles/blob/main/miles/backends/sglang_utils/sglang_api_client.py)。

根据配置，权重传输可以使用 tensor、distributed、P2P/RDMA 或 disk 路径。LoRA 场景还可以只更新 adapter，不重新发送整个 base model。

## 19. 最重要的代码阅读顺序

```text
train.py
train_async.py
miles/rollout/data_source.py
miles/rollout/inference_rollout/inference_rollout_common.py
miles/rollout/inference_rollout/inference_rollout_train.py
miles/ray/rollout/rollout_executor.py
miles/ray/rollout/train_data_conversion.py
miles/backends/training_utils/loss/objective.py
miles/backends/training_utils/loss/hub/advantages.py
miles/backends/training_utils/loss/hub/losses.py
miles/backends/megatron_utils/actor.py
miles/backends/training_utils/weight_update/updater.py
miles/rollout/fully_async_rollout.py
```

## 20. 总结

MILES 每个 RL iteration 的核心就是：

```text
使用当前 Actor 在 SGLang 中采样 response
→ 使用 reward model 或 environment 打分
→ 将 response token、reward、logprob、mask 转成训练 batch
→ 根据 GRPO/PPO/GSPO/REINFORCE++ 计算 advantage
→ 在 Megatron/FSDP 中执行 policy/value loss 和 optimizer step
→ 将 Actor 新权重同步回 SGLang
→ 进入下一轮采样
```

MILES 相比简单 RLHF 脚本更复杂的地方主要是：

1. rollout 与 training 分布式解耦；
2. SGLang 与 Megatron/FSDP 之间的高速权重同步；
3. 支持多轮 agent/environment trajectory；
4. 支持 GRPO、GSPO、PPO、REINFORCE++；
5. 支持 DP、TP、PP、CP、EP 等并行方式；
6. 支持同步、普通 async 和 fully async；
7. 对 train-inference mismatch、weight version、MoE routing replay 做额外处理；
8. 通过 object store 在 rollout worker 和 trainer worker 之间传递训练数据。
