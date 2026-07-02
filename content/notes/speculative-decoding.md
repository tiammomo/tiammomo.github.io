# Speculative Decoding 投机解码地图：用小模型加速大模型

> 投机解码让 draft model 先生成候选 token，再由 target model 并行验证，以较小质量代价提升生成速度。

![Speculative Decoding 投机解码高密度幻想风知识地图](../../assets/images/writing/generated/speculative-decoding-knowledge-map-fantasy.png)

## 一句话

投机解码像让小模型先探路，大模型再批量验票；接受率越高，加速收益越明显。

## 标准流程

1. 输入上下文
2. 小模型草拟
3. 生成候选
4. 大模型验证
5. 接受前缀
6. 回退重采
7. 继续生成
8. 评估加速

## 知识拆解

### 核心定义

- Speculative Decoding 是一种生成加速方法
- 小模型先草拟多个 token
- 大模型并行验证候选 token 是否可接受
- 目标是在保持质量下减少大模型串行步骤

### Draft Model

- Draft model 通常更小、更快、更便宜
- 需要和 target model 语言分布相近
- 可用蒸馏模型或同家族小模型
- 过弱会降低接受率，抵消加速收益

### Target Model

- Target model 负责最终质量和分布校验
- 一次验证多个候选 token
- 拒绝后从目标分布重新采样
- 输出仍以 target model 为准

### 候选生成

- 每轮生成若干 draft token
- 候选长度越长，理论并行收益越大
- 但候选越长越容易被拒绝
- 需要按任务和模型调候选长度

### 验证接受

- 大模型计算候选序列概率
- 按接受规则保留最长可接受前缀
- 被拒绝位置由大模型重新生成
- 接受率是核心性能指标

### 加速收益

- 减少 target model 的串行 decode 次数
- 适合输出较长、分布稳定的任务
- 显著受 draft 速度和接受率影响
- 小模型开销不能超过节省的大模型开销

### 质量风险

- 实现不当可能偏离目标模型分布
- 高温、多样性任务接受率下降
- 复杂推理可能被弱 draft 引导得更差
- 需要和普通解码做回归对比

### 适用场景

- 摘要、改写、客服回复等长文本生成
- 固定领域、风格稳定的输出
- 大模型 decode 成本明显的服务
- 不适合极短输出或强随机创作场景

### 工程落地

- 选择合适 draft/target 组合
- 监控接受率、TTFT、TPOT 和质量指标
- 按模型和任务开启灰度
- 低接受率时自动关闭或改候选参数

## 实践检查清单

- Draft model 要便宜且预测分布接近 target model
- 加速收益取决于候选长度和接受率
- 验证逻辑必须保持目标模型分布尽量一致
- 复杂推理和高温采样可能降低接受率
- 上线前同时评估质量、延迟和成本

## 维护说明

本文由 `content/notes/ai-knowledge-topics.json` 的结构化内容生成。
如果需要调整正文或海报文字，请先修改数据源，再运行 `python3 scripts/build_knowledge_posters.py`。
如果只想更新单个主题，可以在命令后追加 slug，例如 `python3 scripts/build_knowledge_posters.py agent-harness`。
脚本默认不会覆盖已存在的海报；如需生成程序化草稿图，请显式追加 `--overwrite-posters`。
