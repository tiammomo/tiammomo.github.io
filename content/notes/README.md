# Knowledge Topic Data

这里存放写作页图解专题的结构化数据，不存放对外可访问的 Markdown 笔记源文件。

约定：

- `ai-knowledge-topics.json` 是 AI 知识图谱的数据源。
- AI 知识图谱海报由 `python3 scripts/build_knowledge_posters.py` 基于数据源生成。
- 公开站点不链接 `content/notes/*.md`，也不把 Markdown 笔记源文件作为发布资产提交。
- 后续每张图解海报对应的长文应补到正式文章页。
- 图片只保存相对路径引用，不把图片二进制放到 `content/notes/`。
- 对外页面可以从这里摘取摘要、要点和参考图，但不能直接暴露数据源或源文件入口。
- 原创生成图放在 `assets/images/writing/generated/`。
- 高密度知识海报使用 `*-knowledge-map-fantasy.png` 命名。
- 已确认发布的高密度海报不要随意覆盖；生成脚本默认跳过已有图片，只有显式 `--overwrite-posters` 才会重写。
- 截图、草稿和替换素材如果还没确认发布，不放在这里。

当前 AI 知识图谱主题按四条主线维护：

- 大模型应用开发：面向 RAG、Prompt、结构化输出、Agent 工作流、工具调用、运行框架、评测、产品体验与安全边界。
- 大模型 Infra：面向模型网关、协议、安全、向量库、可观测、训练基础设施、模型服务、GPU 运维、评测和 LLMOps。
- 大模型推理：面向模型骨架、推理优化、KV Cache、调度、投机解码、量化压缩和长上下文。
- 大模型算法：面向 Tokenizer、学习范式、训练数据、预训练、微调、偏好对齐和蒸馏。

- 大模型应用开发：RAG、Advanced RAG、Prompt Engineering、Structured Output、Planning、Workflow vs Agent、Context Engineering、AI UX、Multi-Agent、Memory Systems、Tool Calling、Agent Harness、Agent Loop、Tool Use Patterns、Agent Eval Harness、Guardrails / HITL。
- 大模型 Infra：Model Gateway、MCP、LLM Security、Vector Database、Agent Observability、Distributed Training、LLM Serving Architecture、GPU Deployment、LLM Evaluation、LLMOps Lifecycle。
- 大模型推理：Model Architecture、LLM Inference Optimization、KV Cache / PagedAttention、Batching & Scheduling、Speculative Decoding、Quantization / Compression、Long Context / Attention。
- 大模型算法：Tokenizer、Reinforcement Learning、LLM Data Curation、LLM Pretraining Pipeline、SFT / PEFT、Alignment / Preference Optimization、LLM Distillation。
