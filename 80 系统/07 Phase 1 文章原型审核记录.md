---
type: system-review
status: accepted
review_scope: phase-1-note-prototypes
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 1 文章原型审核记录

## 发现

原知识文章模板同时固定要求定义、机制、推导、直觉、实现、性能等所有章节，容易让简单概念文章出现空章节，也会让作者为了“填模板”重复内容。

## 决策

模板只固定以下主干：

- 问题与范围；
- 定义与约定；
- 核心内容；
- 边界、误区与失败条件；
- 验证证据；
- 知识关系；
- 来源。

推导、算法、数据流、实现、调试和性能按文章类型选择，不要求全部出现。

新文章默认 `maturity: seed`，避免空模板一创建就声称达到 `draft`。达到 `draft` 后必须具有来源或原创推导／实验／生产证据。

## 原型结论

| 类型 | 试点结果 |
|---|---|
| theory | 适合数学定义、推导和边界 |
| concept | 适合坐标空间等稳定概念总览 |
| implementation | 适合 Object 到 World 等工程映射 |
| experiment | 适合问题、输入、断言、结果和局限 |
| map | 通过 `map_kind` 区分 MOC、路线和索引 |
| source-note | 适合章节定位、权利和反向映射 |

## 维护成本判断

- Frontmatter 已缩减为最小字段；
- 日期可由脚本同步；
- MOC、学习路线和 Manifest 不再重复职责；
- 一篇同类文章不需要修改总体架构；
- 当前模板可以进入 Phase 2 使用。

## 结论

`accepted`
