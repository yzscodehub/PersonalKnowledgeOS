---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0013：Bootstrap PR 在 Phase 1 复盘后合并

## 背景

PR #1 同时包含总体架构、治理规则、自动化和第一批数学—图形学试点。严格拆分会要求重写已完成的提交历史，但过早合并又会把尚未复盘的文章原型直接作为稳定基线。

## 决策

PR #1 作为一次性 Bootstrap 例外，合并边界确定为：

1. Gate A 总体设计评审完成并标记 `accepted`；
2. Phase 1 数学—坐标—相机—投影试点完成正式复盘；
3. 来源、知识、实验、MOC 和 Manifest 双向追踪通过；
4. 所有临时迁移脚本和一次性工作流清理完成；
5. 知识库校验、公共附件检查和实验全部通过；
6. PR 描述、README、CHANGELOG 和路线图同步；
7. PR 从 Draft 改为 Ready 后进行最终人工检查。

满足以上条件后，PR #1 以 `v0.2.0-design-baseline` 为合并基线进入 `main`。建议使用 Squash Merge，使 `main` 保留一条清晰的 Bootstrap 基线提交，详细过程仍可在 PR 历史中查看。

## 不在本 PR 中继续的内容

以下内容使用独立分支和 PR：

- Phase 2 实时光栅化管线；
- Phase 3 纹理、光照与 PBR；
- API 和渲染器架构；
- 旧知识库迁移；
- AI、音视频、UE5 等多领域扩展。

## 当前状态

Gate A 已通过，但 PR #1 继续保持 Draft，直到 Phase 1 复盘完成。Phase 2 不得提前开始。

## 关联文档

- [[80 系统/03 总体设计评审记录|Gate A 总体设计评审记录]]
- [[80 系统/02 实施路线图|实施路线图]]
- [[80 系统/04 Phase 1 试点复盘|Phase 1 试点复盘]]
