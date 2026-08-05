#!/usr/bin/env python3
"""Close D4 after all knowledge-domain blueprints are implemented."""

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


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: expected text not found: {old[:100]!r}")
    return text.replace(old, new, 1)


def update_plan() -> None:
    path = "80 系统/09 完整设计收敛计划.md"
    text = read(path)
    text = text.replace("version: 1.3", "version: 1.4", 1)
    pattern = re.compile(r"# 7\. D4：全知识领域蓝图\n[\s\S]*?\n---\n\n# 8\. D5：Obsidian 使用体验设计")
    replacement = '''# 7. D4：全知识领域蓝图

## 要求

13 个知识领域和 `99 跨领域知识地图` 已完成一级模块、关键边界、核心 MOC、来源类型、实践方式和跨领域关系设计；未提前创建空文章和空模块目录。

## 工作项

- [x] 01 数学；
- [x] 02 物理与工程科学；
- [x] 03 计算机科学；
- [x] 04 图形学与渲染；
- [x] 05 人工智能与数据科学；
- [x] 06 软件工程；
- [x] 07 系统与平台；
- [x] 08 游戏引擎与实时应用；
- [x] 09 音视频与多媒体；
- [x] 10 嵌入式、机器人与智能驾驶；
- [x] 11 设计、摄影与内容创作；
- [x] 12 产品、商业与职业发展；
- [x] 13 人文与社会科学；
- [x] 99 跨领域知识地图。

每个领域蓝图已经包含：

```text
领域目标
主归属边界
一级模块
核心基础
典型应用
来源与证据
实验与实践
核心 MOC
跨领域关系
首批建设建议
非目标
```

## 退出条件

未来新增任一常见主题时，不需要修改顶层结构，也能判断主归属、一级模块和跨领域链接方式。

## 已形成交付物

- [[80 系统/14 D4 全知识领域蓝图|D4 全知识领域蓝图]]；
- `80 系统/50 领域蓝图/` 下 14 份正式蓝图；
- [[80 系统/10 治理规则/领域蓝图与模块建设规则|领域蓝图与模块建设规则]]；
- [[80 系统/60 ADR/ADR-0018-全知识领域蓝图与建设顺序|ADR-0018：全知识领域蓝图与建设顺序]]；
- `80 系统/30 Manifest/知识领域蓝图清单.yaml`；
- 稳定模块代码、逻辑模块延迟实例化和建设波次；
- `scripts/check_domain_blueprints.py` 自动校验。

## 当前状态

`completed`

下一步：D5 Obsidian 使用体验设计。

---

# 8. D5：Obsidian 使用体验设计'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("D4 block not found in complete-design plan")
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.14", "version: 3.15", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.14", "# 个人知识库总体设计方案 v3.15", 1)
    text = replace_once(
        text,
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色、D2 知识对象与导航模型和 D3 端到端工作流已经完成，下一步进入 D4 全知识领域蓝图；PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。",
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色、D2 知识对象与导航模型、D3 端到端工作流和 D4 全知识领域蓝图已经完成，下一步进入 D5 Obsidian 使用体验设计；PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。",
        "design current state",
    )
    marker = "端到端流程和回流规则见 [[80 系统/13 D3 端到端工作流设计|D3 端到端工作流设计]]。"
    d4 = "全部知识领域和跨领域模块规划见 [[80 系统/14 D4 全知识领域蓝图|D4 全知识领域蓝图]]。"
    if d4 not in text:
        text = replace_once(text, marker, marker + "\n\n" + d4, "design D4 link")
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("version: 1.5", "version: 1.6", 1)
    text = replace_once(
        text,
        "D1、D2 和 D3 已完成。下一步：D4 全知识领域蓝图。",
        "D1、D2、D3 和 D4 已完成。下一步：D5 Obsidian 使用体验设计。",
        "roadmap current state",
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    d3 = "- [[80 系统/13 D3 端到端工作流设计|D3 端到端工作流设计]]"
    d4 = "- [[80 系统/14 D4 全知识领域蓝图|D4 全知识领域蓝图]]"
    if d4 not in text:
        text = replace_once(text, d3, d3 + "\n" + d4, "home D4 link")
    adr17 = "- [[80 系统/60 ADR/ADR-0017-端到端工作流与回流规则|ADR-0017：端到端工作流]]"
    adr18 = "- [[80 系统/60 ADR/ADR-0018-全知识领域蓝图与建设顺序|ADR-0018：全知识领域蓝图]]"
    if adr18 not in text:
        text = replace_once(text, adr17, adr17 + "\n" + adr18, "home ADR-0018")
    decision = "- [x] 13 个知识领域和 99 跨领域知识地图蓝图；"
    if decision not in text:
        marker = "- [x] 十条端到端工作流、主对象、异常和回流规则；"
        text = replace_once(text, marker, marker + "\n" + decision, "home D4 decision")
    text = replace_once(
        text,
        "D1、D2 和 D3 已完成。下一步：**D4 全知识领域蓝图**。",
        "D1、D2、D3 和 D4 已完成。下一步：**D5 Obsidian 使用体验设计**。",
        "home next step",
    )
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    text = replace_once(
        text,
        "Gate A、Phase 1、D1 顶层信息角色、D2 知识对象与导航模型和 D3 端到端工作流已经通过，但 **PR #1 暂不合并**。当前继续在 `design/knowledge-base-v3` 分支完成 D4～D10，全部完成后再统一评审和合并。",
        "Gate A、Phase 1、D1 顶层信息角色、D2 知识对象与导航模型、D3 端到端工作流和 D4 全知识领域蓝图已经通过，但 **PR #1 暂不合并**。当前继续在 `design/knowledge-base-v3` 分支完成 D5～D10，全部完成后再统一评审和合并。",
        "README current phase",
    )
    text = text.replace("- 全知识领域蓝图；\n", "", 1)
    d3 = "- D3 端到端工作流：[[80 系统/13 D3 端到端工作流设计]]"
    d4 = "- D4 全知识领域蓝图：[[80 系统/14 D4 全知识领域蓝图]]"
    if d4 not in text:
        text = replace_once(text, d3, d3 + "\n" + d4, "README D4 link")
    command = "python scripts/check_domain_blueprints.py"
    if command not in text:
        text = replace_once(
            text,
            "python scripts/check_workflow_registry.py\n",
            "python scripts/check_workflow_registry.py\n" + command + "\n",
            "README domain check",
        )
    text = text.replace(
        "Pull Request 中会自动运行知识库结构、D3 工作流清单、公开附件、Phase 1 一致性和上述实验校验。",
        "Pull Request 中会自动运行知识库结构、D3 工作流、D4 领域蓝图、公开附件、Phase 1 一致性和上述实验校验。",
        1,
    )
    write(path, text)


def update_knowledge_overview() -> None:
    path = "30 知识/00 知识总览.md"
    text = read(path)
    section = '''## 领域蓝图

全部领域的主归属、一级模块、核心 MOC、来源和首批建设建议见：

- [[80 系统/14 D4 全知识领域蓝图|D4 全知识领域蓝图]]

未实例化领域和模块继续保留在蓝图与 Manifest 中，不提前创建空目录。

'''
    marker = "## 正式知识准入"
    if section.strip() not in text:
        text = replace_once(text, marker, section + marker, "knowledge overview D4")
    write(path, text)


def update_domain_overview(path: str, blueprint_link: str) -> None:
    text = read(path)
    marker = "## 导航\n"
    link_line = f"- {blueprint_link}"
    if link_line not in text:
        text = replace_once(text, marker, marker + "\n" + link_line, f"domain overview {path}")
    write(path, text)


def update_boundary_rule() -> None:
    path = "80 系统/10 治理规则/知识领域边界与主归属规则.md"
    text = read(path)
    section = '''
## 领域蓝图和模块代码

各领域的稳定一级模块、模块代码、核心 MOC、来源和建设建议由 [[80 系统/14 D4 全知识领域蓝图|D4 全知识领域蓝图]] 管理。

蓝图中的逻辑模块不自动创建实体目录；目录实例化条件见 [[80 系统/10 治理规则/领域蓝图与模块建设规则|领域蓝图与模块建设规则]]。
'''
    if "## 领域蓝图和模块代码" not in text:
        text = text.rstrip() + "\n" + section
    write(path, text)


def update_contributing() -> None:
    path = "CONTRIBUTING.md"
    text = read(path)
    command = "python scripts/check_domain_blueprints.py"
    if command not in text:
        text = replace_once(
            text,
            "python scripts/check_workflow_registry.py\n",
            "python scripts/check_workflow_registry.py\n" + command + "\n",
            "CONTRIBUTING domain check",
        )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    if "D4 全知识领域蓝图" not in text:
        text = replace_once(
            text,
            "### Added\n",
            "### Added\n\n- D4 全知识领域蓝图和 14 份领域蓝图；\n- ADR-0018：全知识领域蓝图与建设顺序；\n- 领域蓝图机器清单、稳定模块代码和自动校验；\n- 领域蓝图与模块延迟实例化治理规则；",
            "CHANGELOG added",
        )
    if "D4 已完成" not in text:
        text = replace_once(
            text,
            "### Changed\n",
            "### Changed\n\n- 数学、图形学和知识总览已连接正式领域蓝图；\n- 完整设计收敛阶段中 D4 已完成，下一步进入 D5；",
            "CHANGELOG changed",
        )
    write(path, text)


def main() -> None:
    update_plan()
    update_design()
    update_roadmap()
    update_home()
    update_readme()
    update_knowledge_overview()
    update_domain_overview(
        "30 知识/01 数学/00 数学总览.md",
        "[[80 系统/50 领域蓝图/01 数学领域蓝图|数学领域蓝图]]",
    )
    update_domain_overview(
        "30 知识/04 图形学与渲染/00 图形学总览.md",
        "[[80 系统/50 领域蓝图/04 图形学与渲染领域蓝图|图形学与渲染领域蓝图]]",
    )
    update_boundary_rule()
    update_contributing()
    update_changelog()
    print("D4 closeout complete.")


if __name__ == "__main__":
    main()
