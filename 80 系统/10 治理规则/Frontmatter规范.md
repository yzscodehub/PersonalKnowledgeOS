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
verification:
  - source-checked
  - derived
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

`verification` 是可多选的证据列表，不是单选成熟度，也不存在“最高验证状态”。允许值：

```text
source-checked
derived
experiment-reproduced
production-validated
```

实际 YAML 不应包含上面代码块中的额外缩进；标准写法：

```yaml
verification:
  - source-checked
  - derived
  - experiment-reproduced
```

尚无证据时使用：

```yaml
verification: []
```

也可以省略该字段。不得把 `unverified` 与其他证据并列，因为“未验证”是空证据状态，不是一种正向证据。

具体来源、推导章节、实验文章或生产记录应在正文的“验证证据”部分链接，不只依赖属性标签。

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
created: 2026-08-04
updated: 2026-08-04
---
```

来源状态：`unread`、`reading`、`processed`、`reference`、`abandoned`。

来源不使用单一 `authority` 字段进行跨类型全局排序。来源能支持哪些声明，应在正文的“可支持的声明类型”中说明。

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
- 不用标签重复表达目录和知识领域；
- 不把成熟度、生命周期和验证证据混成一条状态链；
- 不把 `verification` 写成单值；
- 不为每篇笔记强制填写所有可选字段。
