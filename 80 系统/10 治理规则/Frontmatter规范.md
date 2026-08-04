# Frontmatter 规范

## 目标

Properties 只保存机器查询、校验和自动化真正需要的稳定身份、对象类型和动态状态。知识关系、论证、证据明细和阅读顺序保留在正文、MOC、学习路线和 Manifest 中。

## 正式知识文章

允许类型：

```text
concept
theory
algorithm
system
implementation
api-reference
experiment
troubleshooting
comparison
```

`principle` 不再作为独立正式类型。

标准示例：

```yaml
---
id: GFX-PROJ-002
type: theory
domain: graphics
maturity: draft
lifecycle: active
aliases:
  - Perspective Projection
verification:
  - source-checked
  - derived
sources:
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---
```

### 核心必填字段

```text
id
type
domain
maturity
lifecycle
```

### 条件字段

| 条件 | 要求 |
|---|---|
| 存在验证证据 | `verification` 使用 YAML 列表 |
| 达到 `draft` 或更高 | 具有 `sources`，或 `derived`／`experiment-reproduced`／`production-validated` 之一 |
| 存在稳定别名 | `aliases` 使用列表 |
| 版本敏感 | 按需填写 `platforms`、`apis`、`versions`、`version_sensitive` |
| 从旧库迁入 | 使用 `legacy_ids` 列表 |
| 被其他文章替代 | 使用 `superseded_by` 列表 |
| `type: api-reference` | `version_sensitive: true`，达到 `draft` 后记录版本和官方来源 |
| `type: experiment` 达到 `stable` | `verification` 包含 `experiment-reproduced` |

## 地图类笔记

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

`map_kind` 允许：

```text
moc
learning-route
index
dashboard
```

地图只有在 Manifest、发布系统或外部工具需要稳定引用时才按需分配 `id`。

## 来源笔记

```yaml
---
type: source-note
source_type: book
status: reading
created: 2026-08-04
updated: 2026-08-04
---
```

必填：`type`、`source_type`、`status`。

状态：

```text
unread
reading
processed
reference
abandoned
```

## 项目笔记

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

项目状态：

```text
planned
active
waiting
paused
completed
cancelled
```

## 其他对象类型

```text
inbox
area
output
journal
map
source-note
project
system-design
system-review
roadmap
governance
adr
home
```

这些对象不使用正式知识文章的完整字段模型，按各自模板和 D1 角色规则维护。

## 字段词表

### `id`

正式知识稳定身份：

```text
<DOMAIN>-<MODULE>-<NNN>
<DOMAIN>-<CATEGORY>-<MODULE>-<NNN>
```

示例：

```text
MATH-LA-001
GFX-PROJ-002
GFX-EXP-TRANSFORM-001
```

要求：

- 大写字母、数字和连字符；
- 总段数 3～5；
- 最后一段为三位数字；
- 仓库内唯一；
- 不随标题、文件名、路径和成熟度变化。

详细规则见 [[80 系统/10 治理规则/稳定ID别名与重命名规则|稳定 ID、别名与重命名规则]]。

### `type`

正式知识：

```text
concept
theory
algorithm
system
implementation
api-reference
experiment
troubleshooting
comparison
```

地图和其他角色类型见上文。

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

`planned` 只存在于 Manifest，不写入已实例化文章。

### `verification`

```text
source-checked
derived
experiment-reproduced
production-validated
```

标准写法：

```yaml
verification:
  - source-checked
  - derived
```

尚无证据时使用 `verification: []` 或省略。验证不是单选等级。

### `lifecycle`

```text
active
needs-update
deprecated
archived
```

`deprecated` 原则上需要：

```yaml
superseded_by:
  - "[[替代文章]]"
```

确实没有替代文章时，正文必须说明弃用原因、历史价值和仍适用范围。

### `aliases`

```yaml
aliases:
  - Perspective Divide
  - 透视除法
```

只收录稳定中英文术语、通用缩写和有搜索价值的旧标题。不得重复当前标题或堆积关键词。

### `legacy_ids`

```yaml
legacy_ids:
  - OLD-GFX-102
  - graphics/math/matrix-note
```

一个文章可映射多个旧 ID；同一旧 ID 不得被多个新文章重复声明。`legacy_id` 单值为旧写法，后续迁移统一转换。

### `superseded_by`

必须使用列表：

```yaml
superseded_by:
  - "[[新主文章]]"
```

### `platforms`、`apis`、`versions`

均使用列表，只有版本敏感文章按需填写。

## 日期策略

`created` 和 `updated` 不属于知识语义，不要求人工每次维护。

- 模板创建时写入 `{{date}}`；
- `created` 首次写入后保持不变；
- 提交前运行 `python scripts/sync_note_dates.py --staged`；
- CI 校验已填写日期格式；
- 精确历史以 Git 为准。

## 属性与正文边界

Properties 负责：

```text
稳定身份
对象类型
主领域
成熟度
验证证据类别
生命周期
版本和平台查询
迁移和替代关系
```

正文负责：

```text
定义和推导
具体证据定位
前置和应用关系
边界和失败条件
实现、实验和决策解释
```

不维护与正文重复的庞大 `related`、`links` 或 `topics` 列表。

## 禁止事项

- 不使用 `principle` 创建新正式知识；
- 不把 A/B/C 写成文章的全局优先级；
- 不用标签重复领域、类型、状态、平台和 API；
- 不把成熟度、生命周期和验证证据混成一条状态链；
- 不把列表字段写成标量；
- 不为每篇文章强制填写所有可选字段；
- 不为了更新时间进行无意义提交；
- 不因移动文件而修改稳定 ID。

## 关联规则

- [[80 系统/12 D2 知识对象与导航模型|D2 知识对象与导航模型]]
- [[80 系统/10 治理规则/知识对象类型与文章原型规则|知识对象类型与文章原型规则]]
- [[80 系统/10 治理规则/标签属性目录与链接职责规则|标签、属性、目录与链接职责规则]]
