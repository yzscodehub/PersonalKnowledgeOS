#!/usr/bin/env python3
"""One-time migration to accept Gate A and freeze the bootstrap PR boundary."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ADR = '''---
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
'''

PHASE1_REVIEW = '''---
type: system-review
status: review
review_scope: phase-1
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 1 数学—坐标—相机—投影试点复盘

## 1. 复盘目标

验证当前知识库模型是否真的能够把两本来源转化为：

```text
来源
  ↓
数学基础
  ↓
图形学应用
  ↓
可执行实验
  ↓
MOC / 学习路线 / Manifest
```

本复盘只审核已有试点，不新增光栅化、PBR 或 API 正文。

## 2. 审核范围

### 数学

- 点与向量；
- 向量空间；
- 基与坐标；
- 矩阵作为线性映射；
- 仿射空间与仿射组合；
- 标架与坐标系；
- 齐次坐标。

### 图形学

- 图形学坐标空间总览；
- Object 到 World；
- World 到 View；
- 正交投影；
- 透视投影；
- Clip Space、透视除法与 NDC；
- 深度缓冲、精度与 Reversed-Z。

### 实验

- 矩阵乘法与坐标约定；
- 投影矩阵与 NDC 端点；
- Float32 Forward-Z 与 Reversed-Z 精度。

### 系统对象

- 两本来源笔记；
- 数学和图形学总览；
- 两条学习路线；
- 三个主题 MOC；
- 试点 Manifest；
- 校验和实验 CI。

## 3. 审核清单

### 3.1 符号与数学正确性

- [ ] 列向量、右手观察空间、`-Z` 前向和 `[0,1]` 深度约定在相关文章中一致；
- [ ] Object、World、View、Clip、NDC 的输入输出方向一致；
- [ ] 正交和透视矩阵端点推导与实验一致；
- [ ] 标准深度、Reversed-Z 和线性化公式一致；
- [ ] 主动变换、被动换基、矩阵布局和乘法约定没有混淆。

### 3.2 来源追踪

- [ ] 两本书的相关章节和页码已补充到来源笔记；
- [ ] 文章 `sources` 与正文来源章节一致；
- [ ] 来源笔记能够反向链接全部已提炼文章；
- [ ] `source-checked` 只用于已核对的声明；
- [ ] 超出两本书的工程结论已标明补充证据或待验证。

### 3.3 基础理论与应用边界

- [ ] 数学文章只维护数学本体、推导和性质；
- [ ] 图形学文章只展开坐标约定、渲染应用和工程边界；
- [ ] 没有两篇文章重复同一完整基础解释；
- [ ] Object/View/Projection 等应用文章正确链接数学前置；
- [ ] 后续 UE5、RHI 和 API 内容可以复用当前文章而无需复制。

### 3.4 验证证据

- [ ] 每个 `derived` 都能定位到正文推导；
- [ ] 每个 `experiment-reproduced` 都链接可执行实验；
- [ ] 三个实验输入、断言、结果和局限完整；
- [ ] 实验代码和文章公式使用相同约定；
- [ ] CI 可以从干净环境重复运行。

### 3.5 MOC、路线与 Manifest

- [ ] `map_kind` 与页面职责一致；
- [ ] MOC 只组织主题网络，不复制学习路线；
- [ ] 学习路线的阶段顺序可完整走通；
- [ ] Manifest ID、路径、状态和依赖与实际文件一致；
- [ ] 尚未建设主题没有空 Markdown 文件。

### 3.6 文章原型与维护成本

- [ ] 文章章节没有明显模板化冗余；
- [ ] Frontmatter 字段符合最小模型；
- [ ] 日期同步、验证和附件检查命令可正常使用；
- [ ] 新增一篇同类文章不需要修改总体架构；
- [ ] 每周纯整理成本预计可控制在约 30 分钟内。

## 4. 需要形成的输出

- 矩阵和投影约定审核记录；
- 两本来源的精确章节映射；
- 重复或边界问题清单；
- 验证证据修正清单；
- MOC／Manifest 一致性报告；
- 文章模板精简结论；
- Phase 2 最终范围和非目标。

## 5. 退出条件

全部关键检查完成，且：

- 来源—知识—实验可以双向追踪；
- 至少一条学习路线能从数学走到图形实验；
- 没有阻断性的公式、约定、链接或归属错误；
- 所有 CI 检查通过；
- 本文 `status` 从 `review` 改为 `accepted`；
- PR #1 满足 [[80 系统/60 ADR/ADR-0013-Bootstrap-PR合并边界|ADR-0013]] 的合并条件。

## 6. 当前结论

`review-in-progress`

下一步先执行矩阵、投影和深度约定的逐篇审核，再审核来源定位、知识边界和系统一致性。
'''


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_text(encoding="utf-8") == content:
        return
    target.write_text(content, encoding="utf-8")
    print(path)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("status: review", "status: accepted", 1)
    text = text.replace("version: 3.9", "version: 3.10", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.9", "# 个人知识库总体设计方案 v3.10", 1)
    text = text.replace(
        "当前进入 **总体设计评审期**。",
        "Gate A 总体设计已经通过；当前进入 **Phase 1 试点复盘期**。",
        1,
    )
    text = text.replace(
        "在本方案确认前：",
        "在 Phase 1 复盘和 Bootstrap PR 合并前：",
        1,
    )
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("status: open", "status: accepted", 1)
    text = text.replace("version: 1.8", "version: 2.0", 1)
    text = text.replace("个人知识库总体设计方案 v3.9", "个人知识库总体设计方案 v3.10", 1)
    text = text.replace(
        "结论为“有条件通过”：总体方向正确，但在剩余治理规则冻结前，不进入 Phase 2。",
        "结论为“通过”：Gate A 设计决策已冻结，下一步完成 Phase 1 试点复盘；在 PR #1 合并前不进入 Phase 2。",
        1,
    )
    insertion = '''
## F-10：Bootstrap PR 合并边界已确认

### 决策

PR #1 在 Gate A 通过后继续保持 Draft，用于完成 Phase 1 试点复盘。复盘、清理和全部 CI 通过后，作为 `v0.2.0-design-baseline` 合并到 `main`；Phase 2 使用独立分支和 PR。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0013-Bootstrap-PR合并边界|ADR-0013：Bootstrap PR 合并边界]]。

---

'''
    marker = "# 6. 已通过项"
    if "## F-10：Bootstrap PR" not in text:
        text = text.replace(marker, insertion + marker, 1)
    text = text.replace(
        "23. 顶层编号语义和 70 保留位已冻结。",
        "23. 顶层编号语义和 70 保留位已冻结；\n24. Bootstrap PR 的合并边界已冻结。",
        1,
    )
    text = text.replace(
        "- [ ] 确认当前 PR 合并边界。",
        "- [x] PR #1 将在 Phase 1 复盘后作为 v0.2.0 设计基线合并，并通过 ADR-0013 固化。",
        1,
    )
    text += "\n# 9. Gate A 最终结论\n\n`accepted`\n\n后续只进行 Phase 1 试点复盘和必要修复，不新增 Phase 2 内容。\n"
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("status: review", "status: active", 1)
    text = text.replace("version: 1.1", "version: 1.2", 1)
    text = text.replace("- [ ] 总体设计人工评审；", "- [x] Gate A 总体设计人工评审完成；", 1)
    text = text.replace(
        "- [ ] 明确旧知识库的来源位置和迁移范围；",
        "- [x] 旧库采用 Phase 5 小批次迁移、保留 legacy_id 的范围和原则已确定；",
        1,
    )
    text = text.replace(
        "- [ ] 将设计 PR 调整为可评审状态。",
        "- [x] PR #1 合并边界已确定：完成 Phase 1 复盘后合并。",
        1,
    )
    text = text.replace("`review`\n\n在通过前暂停新增光栅化、PBR 和其他领域正文。", "`completed`\n\nGate A 已通过。当前进入 Phase 1 复盘，继续暂停新增光栅化、PBR 和其他领域正文。", 1)
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    text = text.replace("当前处于 **总体设计评审期**。", "Gate A 已通过，当前处于 **Phase 1 试点复盘期**。", 1)
    text = text.replace(
        "在设计确认前，保留已有数学、坐标、相机、投影和深度试点，但暂停继续扩展光栅化、PBR、API 和其他领域。",
        "当前只审核和修复已有数学、坐标、相机、投影和深度试点；PR #1 合并前暂停扩展光栅化、PBR、API 和其他领域。",
        1,
    )
    adr12 = "- [[80 系统/60 ADR/ADR-0012-顶层编号语义与70保留位|ADR-0012：顶层编号语义]]"
    if "ADR-0013-Bootstrap-PR合并边界" not in text:
        text = text.replace(
            adr12,
            adr12 + "\n- [[80 系统/60 ADR/ADR-0013-Bootstrap-PR合并边界|ADR-0013：PR 合并边界]]\n- [[80 系统/04 Phase 1 试点复盘|Phase 1 试点复盘]]",
            1,
        )
    text = text.replace(
        "- [ ] Draft PR #1 应在哪个边界合并？",
        "- [x] PR #1 在 Phase 1 复盘完成后合并为 v0.2.0 设计基线；",
        1,
    )
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    text = text.replace(
        "当前处于 **总体设计评审期**。已有的数学、坐标、相机、投影和深度试点继续保留，但在总体方案确认前暂停扩展光栅化、PBR、API 和其他领域。",
        "Gate A 总体设计已经通过，当前处于 **Phase 1 试点复盘期**。在试点复盘和 PR #1 合并前，暂停扩展光栅化、PBR、API 和其他领域。",
        1,
    )
    marker = "- 总体评审：[[80 系统/03 总体设计评审记录]]"
    if "Phase 1 复盘" not in text:
        text = text.replace(marker, marker + "\n- Phase 1 复盘：[[80 系统/04 Phase 1 试点复盘]]", 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace("- 个人知识库总体设计方案 v3.9；", "- 个人知识库总体设计方案 v3.10；", 1)
    marker = "- ADR-0012：顶层编号语义与 70 保留位。"
    if "ADR-0013：Bootstrap PR" not in text:
        text = text.replace(marker, marker + "\n- ADR-0013：Bootstrap PR 合并边界。\n- Phase 1 试点复盘文档。", 1)
    changed = "- 顶层编号已明确为语义分区，并保留 70 扩展位。"
    if "Gate A 已通过" not in text:
        text = text.replace(changed, changed + "\n- Gate A 已通过，当前阶段切换到 Phase 1 试点复盘。", 1)
    write(path, text)


def main() -> None:
    write("80 系统/60 ADR/ADR-0013-Bootstrap-PR合并边界.md", ADR)
    write("80 系统/04 Phase 1 试点复盘.md", PHASE1_REVIEW)
    update_design()
    update_review()
    update_roadmap()
    update_home()
    update_readme()
    update_changelog()
    print("Gate A accepted; Phase 1 review initialized.")


if __name__ == "__main__":
    main()
