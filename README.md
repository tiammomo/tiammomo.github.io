# Tiammomo GitHub Pages Portfolio

Tiammomo 的个人 GitHub Pages 首页，用来对外介绍 AI 产品工程方向的开源实践：LLM 应用、Agent 工作流、数据工具、工程基础设施和全栈产品原型。

这是一个零构建依赖的静态站点，根目录的 `index.html` 会直接作为 `https://tiammomo.github.io/` 的首页发布。

## 本地预览

直接打开 `index.html` 即可预览。也可以启动本地静态服务：

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

- 项目卡片在 `index.html` 的 `#work` 区域维护。
- 项目筛选通过卡片上的 `data-category` 和筛选按钮的 `data-filter` 对应。
- 状态灯通过 `data-status` 控制：`active`、`wip`、`archived`。
- 视觉和响应式样式集中在 `styles.css`。
- 复制按钮和导航交互集中在 `script.js`。
- `.nojekyll` 已放在根目录，GitHub Pages 会按普通静态文件发布。
