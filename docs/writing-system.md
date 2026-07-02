# Writing System

这个项目把写作内容、公开页面和生成图片分开管理，避免后续笔记越来越多后混在 HTML 里。

## 目录约定

```text
content/notes/
  README.md
  ai-knowledge-topics.json
  rag.md
  reinforcement-learning.md
  planning.md
  model-architecture.md
  workflow-vs-agent.md
  context-engineering.md
  multi-agent.md
  memory-systems.md
  tool-calling.md
  mcp.md
  agent-harness.md
  agent-loop.md
  tool-use-patterns.md
  agent-eval-harness.md
  agent-observability.md
  guardrails-hitl.md
  llm-pretraining-pipeline.md
  llm-sft-peft.md
  llm-alignment-preference.md
  llm-inference-optimization.md
  llm-serving-architecture.md
  llm-gpu-deployment.md
  llm-data-curation.md
  llm-distributed-training.md
  llm-quantization-compression.md
  llm-long-context-attention.md
  llm-evaluation-benchmarks.md
  llmops-lifecycle.md

assets/images/writing/generated/
  *-knowledge-map-fantasy.png
  fantasy-scenes/

scripts/
  build_knowledge_posters.py

docs/
  writing-system.md
```

## 职责边界

- `content/notes/ai-knowledge-topics.json`：AI 知识图谱的数据源，包含标题、摘要、流程、章节、检查清单和图片引用。
- `content/notes/*.md`：由数据源生成的笔记正文，便于直接阅读和外部引用。
- `assets/images/writing/generated/`：已经确认要在站点展示的原创生成图和高密度知识海报。
- `assets/images/writing/generated/fantasy-scenes/`：原创幻想风主题视觉素材，用作知识海报的氛围层。
- `scripts/build_knowledge_posters.py`：从 JSON 数据源生成高密度海报和 Markdown 笔记。
- `docs/writing-system.md`：写作系统、内容目录和维护规则。
- `writing.html`：公开入口页，只放适合外部读者快速浏览的摘要、专题入口和文章索引。
- `writing/*.html`：图解笔记专题页，按大模型应用开发、Infra、推理、算法四条线承载完整海报卡片。
- 临时草稿、未确认图片、参考原图不放进正式目录。

## 图片规则

- 不直接使用外部原图或聊天里提供的参考图。
- 需要图解时，基于主题重新生成原创图。
- 可以使用原创清冷幻想风讲解角色、魔法书、旅途笔记、古典图书馆等视觉元素，但不要复刻已有 IP 角色、服装、构图或标识。
- 主题视觉可以由生成模型产出，但海报正文必须由结构化数据源排版生成，避免小字不可控。
- 高密度海报使用稳定语义命名，例如 `rag-knowledge-map-fantasy.png`。
- 如果后续替换主题视觉，优先替换 `fantasy-scenes/` 中的语义文件，再重新运行生成脚本。

## 生成流程

修改知识图谱内容时：

```bash
python3 scripts/build_knowledge_posters.py
```

这个脚本会同时更新：

- `content/notes/*.md`

如果目标海报不存在，脚本会生成一张程序化草稿海报到 `assets/images/writing/generated/*-knowledge-map-fantasy.png`。
如果目标海报已经存在，脚本默认跳过图片，避免覆盖已经人工确认或由 gpt-image2 生成的正式图。

`writing.html` 和 `writing/*.html` 只维护卡片摘要和入口链接，不作为长正文事实源。

只新增或重生成部分主题时，可以传入 slug，避免覆盖已经人工确认过的海报：

```bash
python3 scripts/build_knowledge_posters.py agent-harness agent-loop
```

如果确实要用程序化模板覆盖已有海报，再显式追加：

```bash
python3 scripts/build_knowledge_posters.py agent-harness --overwrite-posters
```

## 笔记规则

每篇笔记建议包含：

- 标题
- 一段核心解释
- 主图
- 基本流程或概念拆解
- 适用场景
- 项目视角或工程视角

写作页首页只展示摘要，不把长正文塞进卡片里。

## 页面组织

图解笔记区按四条主线组织，后续新增主题先归入主线，再补卡片、Markdown 和数据源：

- 大模型应用开发：RAG、Advanced RAG、Prompt Engineering、Structured Output、Planning、Workflow vs Agent、Context Engineering、AI UX、Multi-Agent、Memory、Tool Calling、Agent Harness、Agent Loop、Tool Use Patterns、Agent Eval Harness、Guardrails。
- 大模型 Infra：Model Gateway、MCP、LLM Security、Vector Database、Agent Observability、Distributed Training、LLM Serving、GPU Deployment、LLM Evaluation、LLMOps。
- 大模型推理：Model Architecture、LLM Inference、KV Cache / PagedAttention、Batching & Scheduling、Speculative Decoding、Quantization、Long Context。
- 大模型算法：Tokenizer、Reinforcement Learning、Data Curation、LLM Pretraining、SFT / PEFT、Alignment、Distillation。

如果某个方向会持续扩展，例如 RAG 系列、Agent 系列、Infra 系列或算法系列，优先在现有主线下形成连续主题；只有当主题数量和读者心智都足够独立时，再新增主线。

## 当前知识图谱主题

- 大模型应用开发：RAG、Advanced RAG、Prompt Engineering、Structured Output、Planning、Workflow vs Agent、Context Engineering、AI UX、Multi-Agent、Memory、Tool Calling、Agent Harness、Agent Loop、Tool Use Patterns、Agent Eval Harness、Guardrails / HITL。
- 大模型 Infra：Model Gateway、MCP、LLM Security、Vector Database、Agent Observability、Distributed Training、LLM Serving、GPU Deployment、LLM Evaluation、LLMOps。
- 大模型推理：Model Architecture、LLM Inference、KV Cache / PagedAttention、Batching & Scheduling、Speculative Decoding、Quantization、Long Context。
- 大模型算法：Tokenizer、Reinforcement Learning、Data Curation、LLM Pretraining、SFT / PEFT、Alignment、Distillation。
