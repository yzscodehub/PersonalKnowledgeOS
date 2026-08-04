#!/usr/bin/env python3
"""Close D2 after knowledge object and navigation design is implemented."""

from __future__ import annotations

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
    text = text.replace("version: 1.1", "version: 1.2", 1)

    start = text.index("# 5. D2：知识对象与导航模型")
    end = text.index("# 6. D3：端到端工作流设计")
    block = text[start:end].replace("- [ ]", "- [x]")

    if "## 已形成交付物" not in block:
        marker = (
            "## 退出条件\n\n"
            "同一主题不会因为书籍、项目、平台或学习路线不同而产生多个重复主版本。\n\n"
            "---\n\n"
        )
        replacement = '''## 退出条件

同一主题不会因为书籍、项目、平台或学习路线不同而产生多个重复主版本。

## 已形成交付物

- [[80 系统/12 D2 知识对象与导航模型|D2 知识对象与导航模型]]；
- [[80 系统/60 ADR/ADR-0016-知识对象与导航模型|ADR-0016：知识对象与导航模型]]；
- 九种正式知识类型和文章原型；
- 稳定 ID、别名、重命名和 `legacy_ids` 规则；
- 拆分、合并、唯一主解释、废弃和替代规则；
- MOC、学习路线、索引、仪表盘和 Manifest 协作模型；
- 目录、Properties、标签和正文链接职责规则；
- D2 自动校验规则。

## 当前状态

`completed`

下一步：D3 端到端工作流设计。

---

'''
        if marker not in block:
            raise RuntimeError("D2 exit marker not found")
        block = block.replace(marker, replacement, 1)

    text = text[:start] + block + text[end:]
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.12", "version: 3.13", 1)
    text = text.replace(
        "# 个人知识库总体设计方案 v3.12",
        "# 个人知识库总体设计方案 v3.13",
        1,
    )
    old = (
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色详细设计已完成，"
        "下一步进入 D2 知识对象与导航模型；PR #1 和 `design/knowledge-base-v3` "
        "分支继续保持 Draft 和未合并状态。"
    )
    new = (
        "当前处于 **完整设计收敛阶段**。D1 顶层信息角色和 D2 知识对象与导航模型"
        "已经完成，下一步进入 D3 端到端工作流设计；PR #1 和 "
        "`design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。"
    )
    if old not in text:
        raise RuntimeError("Design current-state marker not found")
    text = text.replace(old, new, 1)

    marker = "在 [[80 系统/09 完整设计收敛计划|完整设计收敛计划]] 通过前："
    d2_line = (
        "知识对象和导航规则见 [[80 系统/12 D2 知识对象与导航模型|"
        "D2 知识对象与导航模型]]。\n\n"
    )
    if d2_line.strip() not in text:
        text = text.replace(marker, d2_line + marker, 1)
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    old = "D1 顶层信息角色详细设计已完成。下一步：D2 知识对象与导航模型。"
    new = "D1 和 D2 已完成。下一步：D3 端到端工作流设计。"
    if old not in text:
        raise RuntimeError("Roadmap D1/D2 marker not found")
    text = text.replace(old, new, 1)
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)

    d1 = "- [[80 系统/11 D1 顶层信息角色详细设计|D1 顶层信息角色详细设计]]"
    d2 = "- [[80 系统/12 D2 知识对象与导航模型|D2 知识对象与导航模型]]"
    if d2 not in text:
        text = text.replace(d1, d1 + "\n" + d2, 1)

    adr15 = "- [[80 系统/60 ADR/ADR-0015-顶层信息角色详细职责|ADR-0015：顶层信息角色职责]]"
    adr16 = "- [[80 系统/60 ADR/ADR-0016-知识对象与导航模型|ADR-0016：知识对象与导航模型]]"
    if adr16 not in text:
        text = text.replace(adr15, adr15 + "\n" + adr16, 1)

    decision_marker = "- [x] map_kind 地图类型；"
    d2_decision = "- [x] 正式知识类型、稳定 ID、拆分合并和导航对象协作模型；"
    if d2_decision not in text:
        text = text.replace(decision_marker, decision_marker + "\n" + d2_decision, 1)

    old = "D1 已完成。下一步：**D2 知识对象与导航模型**。"
    new = "D1 和 D2 已完成。下一步：**D3 端到端工作流设计**。"
    if old not in text:
        raise RuntimeError("Home D1/D2 marker not found")
    text = text.replace(old, new, 1)
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)

    old = (
        "Gate A 和 Phase 1 试点复盘已经通过，但 **PR #1 暂不合并**。"
        "当前继续在 `design/knowledge-base-v3` 分支完成整套详细设计，完成后再统一评审和合并。"
    )
    new = (
        "Gate A、Phase 1、D1 顶层信息角色和 D2 知识对象与导航模型已经通过，"
        "但 **PR #1 暂不合并**。当前继续在 `design/knowledge-base-v3` 分支完成 "
        "D3～D10，全部完成后再统一评审和合并。"
    )
    if old not in text:
        raise RuntimeError("README current phase marker not found")
    text = text.replace(old, new, 1)

    text = text.replace(
        "- 顶层信息角色和端到端工作流；",
        "- 端到端工作流；",
        1,
    )

    d1 = "- D1 顶层信息角色：[[80 系统/11 D1 顶层信息角色详细设计]]"
    d2 = "- D2 知识对象与导航：[[80 系统/12 D2 知识对象与导航模型]]"
    if d2 not in text:
        text = text.replace(d1, d1 + "\n" + d2, 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)

    added_marker = "### Added\n\n"
    additions = '''- D2 知识对象与导航模型；
- ADR-0016：知识对象与导航模型；
- 概念、理论、算法、系统、实现和对比文章模板；
- 文章原型选择指南；
- 知识对象类型、拆分合并、稳定 ID、别名、重命名和标签职责规则；
- D2 正式类型、ID、列表字段、实验和替代关系自动校验；
'''
    if "- D2 知识对象与导航模型；" not in text:
        text = text.replace(added_marker, added_marker + additions, 1)

    changed_marker = "### Changed\n\n"
    changes = '''- Frontmatter 正式知识类型移除 `principle`，冻结为九种文章原型；
- MOC、学习路线、索引、仪表盘和 Manifest 职责完成 D2 收敛；
- 通用知识模板改为类型未确定时的 `seed` 回退模板；
- 完整设计收敛阶段中 D2 已完成，下一步进入 D3；
'''
    if "- 完整设计收敛阶段中 D2 已完成，下一步进入 D3；" not in text:
        text = text.replace(changed_marker, changed_marker + changes, 1)
    write(path, text)


def main() -> None:
    update_plan()
    update_design()
    update_roadmap()
    update_home()
    update_readme()
    update_changelog()
    print("D2 closeout complete.")


if __name__ == "__main__":
    main()
