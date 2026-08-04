# Contributing

本仓库以个人长期维护为主，所有变更仍按可审阅、可回滚的方式提交。

## 工作流

1. 从 `main` 创建功能分支；
2. 先确定信息角色和唯一主归属；
3. 更新或新增知识正文；
4. 同步更新 MOC、来源笔记和 Manifest；
5. 运行 `python scripts/validate_kb.py`；
6. 创建 Pull Request，说明范围、来源、验证方式和遗留问题。

## 分支命名

```text
design/<topic>
content/<domain>-<topic>
migration/<scope>
fix/<problem>
automation/<tool>
```

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

- 确认它解决的核心问题；
- 检查是否已有权威基础解释；
- 确定它是基础理论、领域应用、实现、实验还是故障案例；
- 在 Manifest 中登记 ID、主归属、依赖和建设优先级；
- 不为尚未开始的主题创建空 Markdown 文件。

## 完成标准

正式知识文章至少应具有：

- 明确的问题和边界；
- 定义、机制、推导或数据流；
- 常见误区或失败条件；
- 可靠来源；
- 前置知识和上层应用链接；
- 与文章类型匹配的验证方式。

API 和工程文章还需要记录平台、版本、生命周期、调试和性能影响。
