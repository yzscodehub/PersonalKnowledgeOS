# Contributing

本仓库以个人长期维护为主，所有变更仍按可审阅、可回滚的方式提交。

## 工作流

1. 先确定信息角色和唯一主归属；
2. 为正式知识写出唯一主问题；
3. 按 [[80 系统/20 模板/文章原型选择指南|文章原型选择指南]] 选择 `type`；
4. 检查是否已有主解释、应用文章或待合并版本；
5. 需要规划的主题在 Manifest 中登记 ID、依赖、路径和路线优先级；
6. 更新知识正文，并同步来源、MOC、学习路线、索引或仪表盘中真正需要维护的视图；
7. 暂存后运行 `python scripts/sync_note_dates.py --staged`，重新暂存；
8. 运行知识库校验、公共附件检查和相关实验；
9. 创建 Pull Request，说明范围、主归属、来源、验证方式和遗留问题。

## 分支命名

```text
design/<topic>
content/<domain>-<topic>
migration/<scope>
fix/<problem>
automation/<tool>
```

当前 Bootstrap 完整设计工作继续使用 `design/knowledge-base-v3`，直到 D1～D10 完成。

## Commit 类型

```text
feat: 新增知识、结构或能力
docs: 修改说明、规则或来源笔记
refactor: 调整结构但不改变知识结论
fix: 修复链接、元数据或事实错误
test: 增加实验或校验
chore: 工具、配置和维护工作
```

## 新建知识文章前

- 用一句话写出“本文主要回答什么”；
- 确认类型是 `concept`、`theory`、`algorithm`、`system`、`implementation`、`api-reference`、`experiment`、`troubleshooting` 或 `comparison`；
- 检查是否已有相同抽象层的主版本；
- 区分通用基础解释和具体领域／平台应用；
- 分配或复用稳定 ID；
- 在需要建设规划时登记 Manifest；
- 不为尚未开始的主题创建空 Markdown 文件。

## 拆分和合并

拆分前确认子文章可以独立回答不同问题。合并时选择主归属正确、ID 更稳定、证据更完整的主版本。

已有稳定引用的旧文章使用：

```yaml
lifecycle: deprecated
superseded_by:
  - "[[替代文章]]"
```

无稳定引用的 `seed`／`outline` 重复草稿可以直接合并并删除。

## 命名和移动

- 标题、文件名和路径变化时保留稳定 ID；
- 旧标题有搜索价值时加入 `aliases`；
- 从旧库迁入使用 `legacy_ids` 列表；
- 移动后更新 Manifest 路径并运行链接校验；
- 不在旧目录保留重复正文。

## 完成标准

所有正式知识文章至少具有：

- 明确的主问题、范围和非目标；
- 与 `type` 匹配的核心结构；
- 边界、失败条件、反例或适用条件；
- 可靠来源或原创推导／实验／生产证据；
- 需要解释的前置、应用、实现、实验和替代关系；
- 与成熟度和验证状态一致的正文内容。

类型专用标准见 [[80 系统/10 治理规则/知识对象类型与文章原型规则|知识对象类型与文章原型规则]]。

## 提交前检查

```bash
python scripts/sync_note_dates.py --staged
git add .
python scripts/validate_kb.py
python scripts/check_public_assets.py
python scripts/check_pilot_consistency.py
```

修改相关实验时同时运行对应实验脚本。
