# Tiammomo GitHub Pages Portfolio

Tiammomo 的个人 GitHub Pages 首页，用来对外介绍 AI 产品工程方向的开源实践：LLM 应用、Agent 工作流、数据工具、工程基础设施和全栈产品原型。

页面采用原创奇幻动漫视觉系统：月夜工作台、精灵系魔法工程师、魔法书与 AI 浮动面板，用来强化“AI 工作站”的个人记忆点，同时避免直接使用任何现成动漫 IP 角色。

这是一个零构建依赖的静态站点，根目录的 `index.html` 会直接作为 `https://tiammomo.github.io/` 的首页发布。

## 本地预览

推荐启动本地静态服务预览，确保 `data/projects.json` 和 `data/profile-stats.json` 能被页面正常读取：

```bash
python3 -m http.server 4173
```

然后访问：

```text
http://127.0.0.1:4173/
```

## 同步到 GitHub Pages

这个站点应推送到用户主页仓库：

```text
git@github.com:tiammomo/tiammomo.github.io.git
```

首次同步：

```bash
git init
git add .
git commit -m "Create Tiammomo GitHub Pages portfolio"
git branch -M main
git remote add origin git@github.com:tiammomo/tiammomo.github.io.git
git push -u origin main
```

如果 `origin` 已存在：

```bash
git remote set-url origin git@github.com:tiammomo/tiammomo.github.io.git
git push -u origin main
```

后续更新：

```bash
git add .
git commit -m "Update portfolio"
git push
```

## 线上访问

推送成功后，访问：

```text
https://tiammomo.github.io/
```

如果出现 GitHub Pages 404，优先检查：

- 仓库是否是公开仓库 `tiammomo/tiammomo.github.io`。
- `index.html` 是否在仓库根目录。
- 默认分支是否是 `main`。
- `Settings -> Pages` 是否已经启用，从 `main` 分支的 `/root` 发布。
- `Actions` 或 `Settings -> Pages` 中是否有构建或部署错误。

## 内容维护

- 首页在 `index.html` / `en.html`，保持精炼定位、精选项目和分流入口。
- 首页统计区由 `data/profile-stats.json` 和 `data/projects.json` 渲染，HTML 内的数字只作为无 JavaScript 兜底。
- 项目中心在 `projects/index.html`，项目数据源在 `data/projects.json`，精选项目卡片和项目索引都从这里渲染。
- 写作中心在 `writing.html`，用于承载项目复盘、图解专题和工程札记入口；完整图解按专题放在 `writing/*.html`。
- AI 知识图谱的数据源放在 `content/notes/ai-knowledge-topics.json`。
- 高密度知识海报和 Markdown 笔记通过 `python3 scripts/build_knowledge_posters.py` 生成。
- 写作正文源文件放在 `content/notes/`，写作系统规范在 `docs/writing-system.md`。
- 写作页原创生成图放在 `assets/images/writing/generated/`，不要直接使用外部原图或聊天参考图；已发布海报使用 `*-knowledge-map-fantasy.png` 命名。
- 关于页在 `about.html`，用于展示能力矩阵、竞赛背景和合作方向。
- 重点案例页放在 `projects/` 目录，目前包含 ModelPort、Temu Price Studio、QuantPilot、RoutePilot、Mamoji 和 SellerHarbor。
- 项目筛选通过卡片上的 `data-category` 和筛选按钮的 `data-filter` 对应。
- 新增项目时优先维护 `data/projects.json`：数组顺序就是展示顺序；`categories` 决定筛选；`index.direction` 和 `index.proof` 决定项目索引文案。
- 状态灯通过 `data-status` 控制：`active`、`wip`、`archived`。
- 动漫风格图片资产放在 `assets/images/generated/`，页面优先加载 `webp`，并保留 `png` 作为社交分享和兼容 fallback。
- 项目图替换源文件放在 `assets/images/replacements/`。该目录下的源图默认不提交到 git，处理后的站点资产会输出到 `assets/images/generated/`。
- 视觉和响应式样式集中在 `styles.css`。
- 复制按钮和导航交互集中在 `script.js`。
- `.nojekyll` 已放在根目录，GitHub Pages 会按普通静态文件发布。

## 更新首页统计

首页的公开仓库数、累计 Stars 和公开 PR 数来自 GitHub API 快照；精选项目数来自 `data/projects.json`。更新时运行：

```bash
python3 scripts/update_profile_stats.py
python3 scripts/validate_site.py
```

如果遇到 GitHub API 限流，可以带上个人访问令牌：

```bash
GITHUB_TOKEN=ghp_xxx python3 scripts/update_profile_stats.py
```

## 替换项目图

准备好项目图后，把源图放到：

```text
assets/images/replacements/
```

推荐文件名：

```text
modelport.png
quantpilot.png
routepilot.png
mamoji.png
sellerharbor.png
temu-price-studio.png
portfolio-og.png
```

然后运行：

```bash
python scripts/build_project_images.py
```

如果本机没有 Pillow，可以使用临时虚拟环境，不会影响项目零构建发布：

```bash
python3 -m venv /tmp/portfolio-image-tools
/tmp/portfolio-image-tools/bin/python -m pip install pillow
/tmp/portfolio-image-tools/bin/python scripts/build_project_images.py
```

脚本会自动裁切到 `16:9`，并生成站点需要的 `png`、`webp` 和缩略 `webp` 文件。生成完成后运行：

```bash
python scripts/validate_site.py
```

## 站点文件

- `404.html`：自定义 GitHub Pages 404 页面。
- `sitemap.xml`：搜索引擎站点地图。
- `site.webmanifest`：基础 PWA/安装元数据。
- `assets/favicon.svg`：站点图标。

## 质量校验

仓库包含 GitHub Actions 工作流：

```text
.github/workflows/validate-site.yml
```

它会在 push 和 pull request 时运行：

```bash
python scripts/validate_site.py
```

校验内容包括 HTML 内部引用、CSS 图片引用、JSON-LD、`site.webmanifest` 和 `sitemap.xml`。
