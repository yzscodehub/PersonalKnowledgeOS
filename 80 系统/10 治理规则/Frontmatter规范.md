# Frontmatter 规范

## 目标

Properties 只保存机器需要查询、校验或自动化的稳定结构和动态状态。知识关系、论证和证据明细保留在正文中。

## 最小字段模型

### 正式知识文章

适用于 `concept`、`theory`、`algorithm`、`system`、`api-reference`、`implementation`、`experiment`、`troubleshooting`、`comparison` 和 `principle`：

```yaml
---
id: GFX-PROJ-002
type: theory
domain: graphics
maturity: draft
lifecycle: active
verification:
  - source-checked
  - derived
sources:
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---
```

必填核心字段：

```text
id
type
domain
maturity
lifecycle
```

### 地图类笔记

```yaml
---
type: map
map_kind: moc
domain: graphics
maturity: draft
lifecycle: active
created: 2026-08-04
updated: 2026-08-04
---
```

`id` 仅在地图被 Manifest 稳定引用时按需填写。

### 来源笔记

```yaml
---
type: source-note
source_type: book
status: reading
created: 2026-08-04
updated: 2026-08-04
---
```

来源必填字段：`type`、`source_type`、`status`。

### 项目笔记

```yaml
---
type: project
status: active
area:
  - "[[职业与技术能力]]"
created: 2026-08-04
updated: 2026-08-04
---
```

项目必填字段：`type`、`status`。

## 条件字段

| 条件 | 要求 |
|---|---|
| 存在验证证据 | `verification` 使用列表 |
| 正式知识达到 `draft` 或更高 | `sources` 至少包含一个来源；纯原创推导或实验可以用对应证据替代 |
| `type: map` | 必须填写合法 `map_kind` |
| 版本敏感 | 按需填写 `platforms`、`apis`、`versions`、`version_sensitive` |
| 从旧库迁移 | 填写 `legacy_id` |
| 已被替代 | 填写 `superseded_by` |

## 字段词表

### `type`

```text
concept
theory
algorithm
system
api-reference
implementation
experiment
troubleshooting
comparison
principle
map
source-note
project
area
output
journal
system-design
```

### `domain`

```text
mathematics
physics-engineering
computer-science
graphics
artificial-intelligence
software-engineering
systems-platforms
game-engine
multimedia
embedded-robotics-autonomous-driving
design-content
product-business-career
humanities-social-sciences
knowledge-system
```

### `maturity`

```text
seed
outline
draft
stable
evergreen
```

### `map_kind`

```text
moc
learning-route
index
dashboard
```

### `verification`

```text
source-checked
derived
experiment-reproduced
production-validated
```

尚无证据时使用 `verification: []` 或省略字段。不得使用标量，也不使用 `unverified`。

### `lifecycle`

```text
active
needs-update
deprecated
archived
```

## 日期策略

`created` 和 `updated` 不作为知识语义字段，也不要求人工在每次编辑时维护。

- 模板在创建笔记时写入 `{{date}}`；
- `created` 首次写入后保持不变；
- 提交前运行 `python scripts/sync_note_dates.py --staged`，自动补充空日期并更新暂存区 Markdown 的 `updated`；
- CI 校验已存在日期的格式，但日期字段本身不作为正式知识必填项；
- 需要精确历史时以 Git 记录为最终依据。

## 按需字段

```text
aliases
module
contexts
prerequisites
platforms
apis
versions
version_sensitive
project
legacy_id
superseded_by
```

## 禁止事项

- 不维护与正文重复的庞大 `related` 列表；
- 不把 A/B/C 写成文章的全局绝对优先级；
- 不用标签重复表达目录和知识领域；
- 不把成熟度、生命周期和验证证据混成一条状态链；
- 不把 `verification` 写成单值；
- 不为每篇笔记强制填写所有可选字段；
- 不为了更新时间而进行无意义提交。
