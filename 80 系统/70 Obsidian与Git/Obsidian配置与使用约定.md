# Obsidian 配置与使用约定

## 仓库内配置

当前提交以下可共享配置：

- `.obsidian/app.json`：附件目录、新文件入口和自动更新链接；
- `.obsidian/templates.json`：模板目录；
- `.obsidian/daily-notes.json`：每日笔记目录和模板。

工作区布局、缓存和设备特有状态通过 `.gitignore` 排除。

## 推荐核心能力

- Files、Search、Quick Switcher；
- Backlinks、Outgoing Links、Outline；
- Templates、Daily Notes；
- Properties、Bases；
- Bookmarks、File Recovery。

知识库核心工作流不依赖社区插件。社区插件只能增强体验，不能成为正文可读性和基础结构的前提。

## 链接约定

- 使用 Wikilink；
- 重命名文件时保持自动更新链接开启；
- 优先链接稳定概念文章；
- 标题和块链接用于精确引用；
- 不把标签作为主要知识关系。

## 附件

所有附件默认进入 `_assets`。大型原始资料不直接提交到仓库，来源笔记中记录合法存储位置和书目信息。
