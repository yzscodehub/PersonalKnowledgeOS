#!/usr/bin/env python3
"""Close D3 after end-to-end workflow design is implemented."""

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


def update_plan() -> None:
    path = "80 系统/09 完整设计收敛计划.md"
    text = read(path)
    text = text.replace("version: 1.2", "version: 1.3", 1)
    pattern = re.compile(r"# 6\. D3：端到端工作流设计\n[\s\S]*?\n---\n\n# 7\. D4：全知识领域蓝图")
    replacement = '''# 6. D3：端到端工作流设计

## 工作项

- [x] 快速捕捉 → 收件箱处理 → 正式归属；
- [x] 书籍／论文阅读 → 来源笔记 → 正式知识；
- [x] 学习路线 → 练习／实验 → 稳定知识；
- [x] 项目问题 → 调研／实验 → 项目决策 → 知识回流；
- [x] 故障排查 → 根因 → 修复验证 → 故障知识；
- [x] 知识文章 → 输出草稿 → 平台发布 → 反向修订；
- [x] 日记 → 周回顾 → 项目和责任领域更新；
- [x] 过时内容 → needs-update → deprecated／superseded；
- [x] 项目完成 → 复盘 → 输出和知识 → 档案；
- [x] 旧内容 → 分类 → 迁移 → 校验 → 回滚。

每条工作流已经定义：

```text
触发条件
输入
执行步骤
状态变化
产物
异常与停止条件
自动化点
退出条件
```

## 退出条件

十条核心工作流具有明确主对象、角色交接、状态边界、回流规则和可验证退出条件。

## 已形成交付物

- [[80 系统/13 D3 端到端工作流设计|D3 端到端工作流设计]]；
- [[80 系统/10 治理规则/端到端工作流与回流规则|端到端工作流与回流规则]]；
- [[80 系统/60 ADR/ADR-0017-端到端工作流与回流规则|ADR-0017：端到端工作流与回流规则]]；
- `80 系统/30 Manifest/端到端工作流清单.yaml`；
- [[80 系统/20 模板/工作流执行记录模板|工作流执行记录模板]]；
- 项目、来源、输出、每日笔记和故障模板的工作流对齐；
- `scripts/check_workflow_registry.py` 和 CI 校验。

## 当前状态

`completed`

下一步：D4 全知识领域蓝图。

---

# 7. D4：全知识领域蓝图'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("D3 block not found in complete-design plan")
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.13", "version: 3.14", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.13", "# 个人知识库总体设计方案 v3.14", 1)
    text = text.replace(
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色和 D2 知识对象与导航模型已经完成，下一步进入 D3 端到端工作流设计；PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。",
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色、D2 知识对象与导航模型和 D3 端到端工作流已经完成，下一步进入 D4 全知识领域蓝图；PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。",
        1,
    )
    marker = "知识对象和导航规则见 [[80 系统/12 D2 知识对象与导航模型|D2 知识对象与导航模型]]。"
    d3 = "端到端流程和回流规则见 [[80 系统/13 D3 端到端工作流设计|D3 端到端工作流设计]]。"
    if d3 not in text:
        text = text.replace(marker, marker + "\n\n" + d3, 1)
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("version: 1.4", "version: 1.5", 1)
    text = text.replace(
        "D1 和 D2 已完成。下一步：D3 端到端工作流设计。",
        "D1、D2 和 D3 已完成。下一步：D4 全知识领域蓝图。",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    d2 = "- [[80 系统/12 D2 知识对象与导航模型|D2 知识对象与导航模型]]"
    d3 = "- [[80 系统/13 D3 端到端工作流设计|D3 端到端工作流设计]]"
    if d3 not in text:
        text = text.replace(d2, d2 + "\n" + d3, 1)
    adr16 = "- [[80 系统/60 ADR/ADR-0016-知识对象与导航模型|ADR-0016：知识对象与导航模型]]"
    adr17 = "- [[80 系统/60 ADR/ADR-0017-端到端工作流与回流规则|ADR-0017：端到端工作流]]"
    if adr17 not in text:
        text = text.replace(adr16, adr16 + "\n" + adr17, 1)
    decision = "- [x] 十条端到端工作流、主对象、异常和回流规则；"
    if decision not in text:
        marker = "- [x] 正式知识类型、稳定 ID、拆分合并和导航对象协作模型；"
        text = text.replace(marker, marker + "\n" + decision, 1)
    text = text.replace(
        "D1 和 D2 已完成。下一步：**D3 端到端工作流设计**。",
        "D1、D2 和 D3 已完成。下一步：**D4 全知识领域蓝图**。",
        1,
    )
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    text = text.replace(
        "Gate A、Phase 1、D1 顶层信息角色和 D2 知识对象与导航模型已经通过，但 **PR #1 暂不合并**。当前继续在 `design/knowledge-base-v3` 分支完成 D3～D10，全部完成后再统一评审和合并。",
        "Gate A、Phase 1、D1 顶层信息角色、D2 知识对象与导航模型和 D3 端到端工作流已经通过，但 **PR #1 暂不合并**。当前继续在 `design/knowledge-base-v3` 分支完成 D4～D10，全部完成后再统一评审和合并。",
        1,
    )
    text = text.replace("- 端到端工作流；\n", "", 1)
    d2 = "- D2 知识对象与导航：[[80 系统/12 D2 知识对象与导航模型]]"
    d3 = "- D3 端到端工作流：[[80 系统/13 D3 端到端工作流设计]]"
    if d3 not in text:
        text = text.replace(d2, d2 + "\n" + d3, 1)
    command = "python scripts/check_workflow_registry.py"
    if command not in text:
        text = text.replace("python scripts/validate_kb.py\n", "python scripts/validate_kb.py\n" + command + "\n", 1)
    text = text.replace(
        "Pull Request 中会自动运行知识库结构、公开附件、Phase 1 一致性和上述实验校验。",
        "Pull Request 中会自动运行知识库结构、D3 工作流清单、公开附件、Phase 1 一致性和上述实验校验。",
        1,
    )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    added_marker = "### Added\n"
    additions = '''### Added

- D3 端到端工作流设计和十条核心工作流；
- ADR-0017：端到端工作流与回流规则；
- 端到端工作流机器清单和执行记录模板；
- 工作流清单校验脚本及 CI 步骤；'''
    if "D3 端到端工作流设计" not in text:
        text = text.replace(added_marker, additions, 1)
    changed_marker = "### Changed\n"
    changes = '''### Changed

- 项目、来源、输出、每日笔记和故障模板已对齐 D3 工作流；
- 完整设计收敛阶段中 D3 已完成，下一步进入 D4；'''
    if "D3 已完成" not in text:
        text = text.replace(changed_marker, changes, 1)
    write(path, text)


def main() -> None:
    update_plan()
    update_design()
    update_roadmap()
    update_home()
    update_readme()
    update_changelog()
    print("D3 closeout complete.")


if __name__ == "__main__":
    main()
