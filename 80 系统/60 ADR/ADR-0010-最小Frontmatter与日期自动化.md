---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0010：采用最小 Frontmatter 与日期自动化

## 背景

Frontmatter 过重会增加捕捉和维护成本，而字段过少又无法支持查询、校验和迁移。`created`、`updated` 尤其容易成为高频手工负担。

## 决策

正式知识文章的核心必填字段为：

```text
id
type
domain
maturity
lifecycle
```

地图类笔记使用 `type`、`map_kind`、`domain`、`maturity`、`lifecycle`；来源和项目使用各自最小状态字段。

`verification`、`sources`、平台版本和迁移字段按条件填写。

日期策略：

- 模板创建时写入日期；
- `created` 首次写入后保持不变；
- `updated` 由 `scripts/sync_note_dates.py` 对暂存区笔记自动更新；
- 日期不作为知识正文必填字段，Git 历史是最终依据。

## 校验

- 正式知识类型必须具有核心字段；
- 地图类笔记必须具有 `map_kind` 和 `lifecycle`；
- `draft` 以上文章必须具有来源或推导、实验、生产证据；
- 已填写的日期必须符合 `YYYY-MM-DD`；
- 模板和系统说明不因空占位符触发正式知识校验。

## 影响

- 现有地图笔记补充 `lifecycle: active`；
- 模板统一使用 `{{date}}`；
- 校验脚本改为按笔记类型检查字段；
- 提交流程增加日期同步命令；
- 不再要求人工维护所有可选属性。

## 关联文档

- [[80 系统/10 治理规则/Frontmatter规范|Frontmatter 规范]]
- [[80 系统/70 Obsidian与Git/Git工作流|Git 工作流]]
- [[80 系统/03 总体设计评审记录|总体设计评审记录]]
