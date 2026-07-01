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
- `writing.html`：公开入口页，只放适合外部读者快速浏览的摘要和卡片。
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

- `assets/images/writing/generated/*-knowledge-map-fantasy.png`
- `content/notes/*.md`

`writing.html` 只维护卡片摘要和入口链接，不作为长正文事实源。

## 笔记规则

每篇笔记建议包含：

- 标题
- 一段核心解释
- 主图
- 基本流程或概念拆解
- 适用场景
- 项目视角或工程视角

写作页首页只展示摘要，不把长正文塞进卡片里。

## 当前知识图谱主题

- RAG：检索增强生成
- Reinforcement Learning：强化学习
- Planning：规划能力
- Model Architecture：模型架构
- Workflow vs Agent：流程与智能体边界
- Context Engineering：上下文工程
- Multi-Agent：多智能体协作
- Memory：记忆系统
- Tool Calling：工具调用
- MCP：模型上下文协议
