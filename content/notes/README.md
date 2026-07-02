# Notes Content

这里存放写作页的笔记正文源文件。

约定：

- `ai-knowledge-topics.json` 是 AI 知识图谱的数据源。
- 每篇笔记一个 Markdown 文件，文件名使用短横线命名。
- AI 知识图谱类笔记由 `python3 scripts/build_knowledge_posters.py` 生成。
- 图片只保存相对路径引用，不把图片二进制放到 `content/notes/`。
- 对外页面可以从这里摘取摘要、要点和参考图，但这里是内容事实源。
- 原创生成图放在 `assets/images/writing/generated/`。
- 高密度知识海报使用 `*-knowledge-map-fantasy.png` 命名。
- 已确认发布的高密度海报不要随意覆盖；生成脚本默认跳过已有图片，只有显式 `--overwrite-posters` 才会重写。
- 截图、草稿和替换素材如果还没确认发布，不放在这里。

当前 AI 知识图谱主题：

- RAG
- Reinforcement Learning
- Planning
- Model Architecture
- Workflow vs Agent
- Context Engineering
- Multi-Agent
- Memory Systems
- Tool Calling
- MCP
- Agent Harness
- Agent Loop
- Tool Use Patterns
- Agent Eval Harness
- Agent Observability
- Guardrails / HITL
