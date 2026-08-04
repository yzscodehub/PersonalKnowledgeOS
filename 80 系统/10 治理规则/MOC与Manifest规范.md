# MOC 与 Manifest 规范

## 职责分离

### MOC

MOC 面向人阅读，负责：

- 解释领域边界；
- 给出学习顺序；
- 组织已存在的文章；
- 展示前置、应用、对比和实验路径；
- 为同一批文章提供不同视角。

MOC 只链接已经存在、值得回访的正式笔记。尚未建设的主题使用普通文本或链接到 Manifest，避免制造大量失效链接。

### Manifest

Manifest 面向规划和自动化，负责：

- 主题稳定 ID；
- 唯一主归属；
- 文章类型；
- 建设状态；
- 学习路线中的 A/B/C；
- 前置依赖；
- 目标文件路径；
- 来源与验证要求。

尚未开始的主题只登记在 Manifest，不创建空 Markdown 文件。

## 建设状态

```text
planned
seed
outline
draft
stable
evergreen
```

状态与知识文章的 `maturity` 对齐，但 Manifest 可以在文件尚未创建时使用 `planned`。

## 优先级

A/B/C 属于具体课程、路线或建设批次，而不是文章的全局属性。

```yaml
priority:
  graphics-foundation: A
  interview-review: A
  ai-foundation: C
```

简单试点允许使用单值 `priority: A`，正式扩展时改为上下文化映射。

## 路径变化

移动文章时：

1. 更新 Manifest 的 `path`；
2. 依赖 Obsidian 自动更新内部链接；
3. 运行校验脚本；
4. 保留稳定 `id`；
5. 从旧知识库迁移时保留 `legacy_id`。

## 一致性检查

自动化应逐步检查：

- Manifest 中 `draft` 及以上主题是否存在文件；
- 已登记文件的 Frontmatter `id` 是否匹配；
- ID 是否重复；
- 依赖 ID 是否存在；
- 文件路径是否唯一；
- MOC 是否出现失效链接。
