---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0006：verification 使用多证据列表

## 背景

原模型把 `verification` 设计成单值：

```yaml
verification: experiment-reproduced
```

但同一篇文章可以同时核对来源、完成推导、通过实验，并在生产环境中验证。它们是可累积、互不排斥的证据类型，不是一条只能保留最高值的线性状态。

## 决策

`verification` 改为 YAML 列表：

```yaml
verification:
  - source-checked
  - derived
  - experiment-reproduced
```

允许证据：

- `source-checked`；
- `derived`；
- `experiment-reproduced`；
- `production-validated`。

尚无证据时使用 `verification: []` 或省略字段。`unverified` 不再作为证据值。

`maturity` 和 `lifecycle` 继续使用单值。

## 证据明细

Frontmatter 只表达证据种类。具体依据必须在正文中链接：

- 核对的来源；
- 推导所在章节；
- 可执行实验；
- 生产项目、版本和环境记录。

## 影响

- 现有试点文章迁移为证据列表；
- 模板默认使用空列表，不预先声称已经验证；
- 校验脚本拒绝标量 `verification` 和非法证据；
- Manifest 中的实验验证字段同步使用列表；
- 查询“待验证”时检查该属性为空或不存在。

## 关联文档

- [[80 系统/10 治理规则/Frontmatter规范|Frontmatter 规范]]
- [[80 系统/10 治理规则/成熟度与验证规则|成熟度与验证规则]]
- [[80 系统/03 总体设计评审记录|总体设计评审记录]]
