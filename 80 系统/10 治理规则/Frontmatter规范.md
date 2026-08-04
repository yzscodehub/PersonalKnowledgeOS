# Frontmatter 规范

## 目标

Properties 用于表达机器可查询的结构化信息和动态状态，不重复正文中的知识关系。

## 通用字段

| 字段 | 说明 | 规则 |
|---|---|---|
| `type` | 笔记类型 | 正式笔记必填 |
| `created` | 创建日期 | `YYYY-MM-DD` |
| `updated` | 最近重要修改日期 | 内容发生实质变化时更新 |
| `id` | Manifest 主题 ID | 已登记的核心知识文章必填 |
| `aliases` | 常用别名 | 按需使用 |
| `legacy_id` | 旧知识库 ID | 迁移文章按需使用 |

## 知识文章字段

```yaml
---
id: MATH-LA-001
type: theory
domain: mathematics
maturity: draft
verification: source-checked
lifecycle: active
sources:
  - "[[Steven J. Gortler - Foundations of 3D Computer Graphics]]"
created: 2026-08-04
updated: 2026-08-04
---
```

### `type`

允许的核心类型：

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
dashboard
system-design
```

### `domain`

当前领域标识：

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

### `verification`

```text
unverified
source-checked
derived
experiment-reproduced
production-validated
```

### `lifecycle`

```text
active
needs-update
deprecated
archived
```

## 项目字段

```yaml
---
type: project
status: active
area:
  - "[[职业与技术能力]]"
created: 2026-08-04
due:
---
```

项目状态：`planned`、`active`、`waiting`、`paused`、`completed`、`cancelled`。

## 来源字段

```yaml
---
type: source-note
source_type: book
status: reading
authority: authoritative-secondary
created: 2026-08-04
updated: 2026-08-04
---
```

来源状态：`unread`、`reading`、`processed`、`reference`、`abandoned`。

## 按需字段

```text
module
contexts
prerequisites
platforms
apis
versions
version_sensitive
project
superseded_by
```

## 禁止事项

- 不维护与正文重复的庞大 `related` 列表；
- 不把 A/B/C 写成文章的全局绝对优先级；
- 不用标签重复表达目录和领域；
- 不把 `reviewed`、`verified` 和内容成熟度混成一条状态链；
- 不为每篇笔记强制填写所有可选字段。
