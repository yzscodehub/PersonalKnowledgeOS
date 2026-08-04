#!/usr/bin/env python3
"""Switch the design branch from merge-ready to complete-design convergence."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    if target.read_text(encoding="utf-8") == content:
        return
    target.write_text(content, encoding="utf-8")
    print(path)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("status: accepted", "status: active", 1)
    text = text.replace("version: 3.10", "version: 3.11", 1)
    text = text.replace(
        "# 个人知识库总体设计方案 v3.10",
        "# 个人知识库总体设计方案 v3.11",
        1,
    )

    pattern = re.compile(r"## 0\. 当前决策状态\n[\s\S]*?\n---\n\n# 1\. 系统定位")
    replacement = '''## 0. 当前决策状态

Gate A 架构评审和 Phase 1 数学—图形学试点已经通过，但总体设计尚未完成全部详细设计工作。

当前进入 **完整设计收敛阶段**，PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。

在 [[80 系统/09 完整设计收敛计划|完整设计收敛计划]] 通过前：

- 保留并修复已经完成的数学、坐标、相机、投影和深度试点；
- 继续建设顶层信息角色、工作流、领域蓝图、Obsidian 体验、自动化、迁移、备份、发布和长期治理设计；
- 允许为验证设计建立最小模板、脚本、仪表盘和示例；
- 暂停 Phase 2 光栅化、PBR、API、UE5、AI 等大规模正文建设；
- 不进行旧知识库全量迁移；
- 不提前创建大批目录和空文章。

完整设计完成后，再依据 [[80 系统/60 ADR/ADR-0014-完整设计后合并Bootstrap分支|ADR-0014]] 进行最终评审和合并。

---

# 1. 系统定位'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace current decision state in design document")
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("version: 1.3", "version: 1.4", 1)
    text = text.replace(
        "1. 先确认总体设计，再继续扩展正文；",
        "1. 先完成总体架构和详细设计，再继续扩展正文；",
        1,
    )
    text = text.replace(
        "Phase 1  数学—坐标—相机—投影试点\n   ↓\nPhase 2  实时光栅化管线试点",
        "Phase 1  数学—坐标—相机—投影试点\n   ↓\nDesign D  完整设计收敛与冻结\n   ↓\nPhase 2  实时光栅化管线试点",
        1,
    )
    text = text.replace(
        "- [x] PR #1 合并边界已确定：完成 Phase 1 复盘后合并。",
        "- [x] PR #1 合并边界已更新：完整设计收敛完成后再合并。",
        1,
    )
    text = text.replace(
        "Gate A 已通过。当前进入 Phase 1 复盘，继续暂停新增光栅化、PBR 和其他领域正文。",
        "Gate A 已通过。Phase 1 也已完成；当前进入完整设计收敛阶段，继续暂停新增光栅化、PBR 和其他领域正文。",
        1,
    )
    text = text.replace(
        "Phase 1 复盘已通过；等待 PR #1 最终人工检查和合并。",
        "Phase 1 复盘已通过；其结论作为完整设计的验证样本保留，但不再触发 PR #1 合并。",
        1,
    )

    marker = "# 5. Phase 2：实时光栅化管线试点"
    section = '''# 4.5 Design D：完整设计收敛与冻结

## 目标

在不扩大知识正文范围的前提下，完成 Personal Knowledge Base v3 的全部详细设计，使合并后的 `main` 可以直接作为长期运行基线。

## 详细范围

完整工作包见 [[80 系统/09 完整设计收敛计划|完整设计收敛计划]]：

```text
D1  顶层信息角色详细设计
D2  知识对象与导航模型
D3  端到端工作流设计
D4  全知识领域蓝图
D5  Obsidian 使用体验设计
D6  自动化与质量门禁
D7  Git、版本、备份与发布
D8  旧知识库迁移与回滚
D9  长期维护与治理
D10 完整设计演练、评审与冻结
```

## 非目标

- 不建设 Phase 2 光栅化正文；
- 不进入纹理、PBR、API、UE5 和 AI 的大规模内容生产；
- 不进行旧库全量迁移；
- 不以创建空目录和空文章代表设计完成。

## 退出条件

- D1～D10 全部完成；
- 所有顶层角色和端到端工作流有明确设计；
- 13 个知识领域具有一级模块蓝图；
- Obsidian、自动化、Git、备份、发布、迁移和运维设计闭环；
- 至少完成一轮端到端演练和完整设计复盘；
- 所有 ADR、规则、模板、脚本和导航入口一致；
- 所有 CI 通过，临时迁移文件已清理；
- PR #1 根据 ADR-0014 完成最终人工评审。

## 当前状态

`active`

下一步：D1 顶层信息角色详细设计。

---

'''
    if section.strip() not in text:
        if marker not in text:
            raise RuntimeError("Could not locate Phase 2 marker")
        text = text.replace(marker, section + marker, 1)
    write(path, text)


def update_phase1_review() -> None:
    path = "80 系统/04 Phase 1 试点复盘.md"
    text = read(path)
    text = text.replace("version: 2.0", "version: 2.1", 1)
    text = text.replace(
        "- PR #1 满足 [[80 系统/60 ADR/ADR-0013-Bootstrap-PR合并边界|ADR-0013]] 的合并条件。",
        "- Phase 1 结论可作为完整设计的验证样本；PR #1 的最终合并条件由 [[80 系统/60 ADR/ADR-0014-完整设计后合并Bootstrap分支|ADR-0014]] 定义。",
        1,
    )
    text = text.replace(
        "Phase 1 试点已经形成来源—数学—图形学—实验—MOC／路线／Manifest 的闭环，满足 PR #1 最终评审条件。\n\n下一步先执行矩阵、投影和深度约定的逐篇审核，再审核来源定位、知识边界和系统一致性。",
        "Phase 1 试点已经形成来源—数学—图形学—实验—MOC／路线／Manifest 的闭环。该试点继续作为完整设计阶段的验证样本，但不再构成 PR #1 的合并触发条件。\n\n下一步进入 [[80 系统/09 完整设计收敛计划|完整设计收敛计划]] 的 D1 顶层信息角色详细设计。",
        1,
    )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace(
        "- 个人知识库总体设计方案 v3.10；",
        "- 个人知识库总体设计方案 v3.11；",
        1,
    )
    marker = "- ADR-0013：Bootstrap PR 合并边界。"
    if "ADR-0014：完整设计后合并" not in text:
        text = text.replace(
            marker,
            marker + "\n- ADR-0014：完整设计后合并 Bootstrap 分支。\n- 完整设计收敛计划 D1～D10。",
            1,
        )
    changed = "- Phase 1 试点复盘已通过，PR #1 等待最终人工检查。"
    if "PR #1 暂不合并" not in text:
        text = text.replace(
            changed,
            changed + "\n- PR #1 暂不合并，当前阶段切换为完整设计收敛。",
            1,
        )
    write(path, text)


def main() -> None:
    update_design()
    update_roadmap()
    update_phase1_review()
    update_changelog()
    print("Complete design phase activated.")


if __name__ == "__main__":
    main()
