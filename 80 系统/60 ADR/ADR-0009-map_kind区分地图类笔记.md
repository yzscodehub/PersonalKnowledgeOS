---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0009：使用 map_kind 区分地图类笔记

## 背景

MOC、学习路线、索引和仪表盘都承担导航功能，但目标不同。只使用 `type: map` 会让查询和模板无法区分“主题结构”“学习顺序”“查找入口”和“动态状态”。

## 决策

地图类笔记使用统一模型：

```yaml
type: map
map_kind: moc
```

允许：

- `moc`；
- `learning-route`；
- `index`；
- `dashboard`。

`type: map` 必须填写 `map_kind`。系统仪表盘也迁移为 `type: map`、`map_kind: dashboard`。

## 边界

- MOC：主题网络；
- 学习路线：目标驱动的有序路径；
- 索引：简洁查找入口；
- 仪表盘：当前行动与动态状态；
- Manifest：建设计划，不属于地图类笔记。

## 影响

- 现有总览、MOC、学习路线、索引和仪表盘补充 `map_kind`；
- MOC 模板不再混入完整学习路线结构；
- 校验脚本要求 `type: map` 具有合法 `map_kind`；
- Obsidian Bases 可以按 `map_kind` 建立导航视图。

## 关联文档

- [[80 系统/10 治理规则/MOC与Manifest规范|MOC、学习路线、索引与 Manifest 规范]]
- [[80 系统/40 索引定义/索引体系|索引体系]]
- [[80 系统/03 总体设计评审记录|总体设计评审记录]]
