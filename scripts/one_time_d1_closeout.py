#!/usr/bin/env python3
"""Close D1 after top-level role design and templates are implemented."""

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


def update_complete_design_plan() -> None:
    path = "80 系统/09 完整设计收敛计划.md"
    text = read(path)
    text = text.replace("version: 1.0", "version: 1.1", 1)

    start = text.index("# 4. D1：顶层信息角色详细设计")
    end = text.index("# 5. D2：知识对象与导航模型")
    block = text[start:end]
    block = block.replace("- [ ]", "- [x]")
    if "## 已形成交付物" not in block:
        insertion = '''## 已形成交付物

- [[80 系统/11 D1 顶层信息角色详细设计|D1 顶层信息角色详细设计]]；
- [[80 系统/10 治理规则/信息归属规则|统一信息归属决策树]]；
- [[80 系统/60 ADR/ADR-0015-顶层信息角色详细职责|ADR-0015：顶层信息角色详细职责]]；
- 收件箱、责任领域、输出、周回顾、月度回顾和档案模板；
- 八个顶层角色的运行说明、边界案例和归档／恢复规则。

## 当前状态

`completed`

下一步：D2 知识对象与导航模型。

'''
        marker = "## 退出条件\n\n任意一条新信息都能在一分钟内判断：放哪里、当前状态是什么、下一步是什么、何时归档。\n\n---\n\n"
        if marker not in block:
            raise RuntimeError("D1 exit marker not found")
        block = block.replace(marker, marker.replace("---\n\n", "") + "\n" + insertion + "---\n\n", 1)
    text = text[:start] + block + text[end:]
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    old = "下一步：D1 顶层信息角色详细设计。"
    new = "D1 顶层信息角色详细设计已完成。下一步：D2 知识对象与导航模型。"
    if old in text:
        text = text.replace(old, new, 1)
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.11", "version: 3.12", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.11", "# 个人知识库总体设计方案 v3.12", 1)
    old = "当前进入 **完整设计收敛阶段**，PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。"
    new = "当前处于 **完整设计收敛阶段**。D1 顶层信息角色详细设计已完成，下一步进入 D2 知识对象与导航模型；PR #1 和 `design/knowledge-base-v3` 分支继续保持 Draft 和未合并状态。"
    if old in text:
        text = text.replace(old, new, 1)
    link_marker = "在 [[80 系统/09 完整设计收敛计划|完整设计收敛计划]] 通过前："
    if "D1 顶层信息角色详细设计" not in text.split(link_marker, 1)[0]:
        text = text.replace(
            link_marker,
            "详细角色边界见 [[80 系统/11 D1 顶层信息角色详细设计|D1 顶层信息角色详细设计]]。\n\n" + link_marker,
            1,
        )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    d1_link = "- [[80 系统/11 D1 顶层信息角色详细设计|D1 顶层信息角色详细设计]]"
    plan_link = "- [[80 系统/09 完整设计收敛计划|完整设计收敛计划]]"
    if d1_link not in text:
        text = text.replace(plan_link, plan_link + "\n" + d1_link, 1)
    adr14 = "- [[80 系统/60 ADR/ADR-0014-完整设计后合并Bootstrap分支|ADR-0014：完整设计后合并]]"
    adr15 = "- [[80 系统/60 ADR/ADR-0015-顶层信息角色详细职责|ADR-0015：顶层信息角色职责]]"
    if adr15 not in text:
        text = text.replace(adr14, adr14 + "\n" + adr15, 1)
    text = text.replace("下一步：**D1 顶层信息角色详细设计**。", "D1 已完成。下一步：**D2 知识对象与导航模型**。", 1)
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    marker = "- 完整设计计划：[[80 系统/09 完整设计收敛计划]]"
    d1 = "- D1 顶层信息角色：[[80 系统/11 D1 顶层信息角色详细设计]]"
    if marker in text and d1 not in text:
        text = text.replace(marker, marker + "\n" + d1, 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    if "D1 顶层信息角色详细设计" not in text:
        marker = "### Added"
        addition = '''### Added

- D1 顶层信息角色详细设计；
- ADR-0015：顶层信息角色详细职责；
- 收件箱、责任领域、输出、周回顾、月度回顾和档案索引模板；
- 顶层角色的一分钟信息归属决策树和边界案例；'''
        if marker not in text:
            raise RuntimeError("CHANGELOG Added marker not found")
        text = text.replace(marker, addition, 1)
    if "D1 已完成" not in text:
        changed = "### Changed"
        addition = '''### Changed

- 八个顶层角色 README 已升级为可执行运行说明；
- 完整设计收敛阶段中 D1 已完成，下一步进入 D2；'''
        if changed in text:
            text = text.replace(changed, addition, 1)
    write(path, text)


def main() -> None:
    update_complete_design_plan()
    update_roadmap()
    update_design()
    update_home()
    update_readme()
    update_changelog()
    print("D1 closeout complete.")


if __name__ == "__main__":
    main()
