#!/usr/bin/env python3
"""One-time Gate A migration to distinguish map note roles."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAP_NOTES: dict[str, str] = {
    "30 知识/00 知识总览.md": "index",
    "30 知识/01 数学/00 数学总览.md": "moc",
    "30 知识/01 数学/01 数学学习路线/图形学数学基础学习路线.md": "learning-route",
    "30 知识/01 数学/02 数学知识地图/线性代数与空间变换 MOC.md": "moc",
    "30 知识/04 图形学与渲染/00 图形学总览.md": "moc",
    "30 知识/04 图形学与渲染/01 图形学学习路线/实时渲染基础学习路线.md": "learning-route",
    "30 知识/04 图形学与渲染/02 图形学知识地图/坐标、相机与投影 MOC.md": "moc",
    "30 知识/04 图形学与渲染/02 图形学知识地图/实时光栅化管线 MOC.md": "moc",
    "80 系统/20 模板/MOC模板.md": "moc",
}

MAP_RULES = '''# MOC、学习路线、索引与 Manifest 规范

## 地图类笔记的统一模型

所有用于组织、导航或展示知识结构的页面统一使用：

```yaml
type: map
map_kind: moc
```

`map_kind` 允许值：

| 值 | 职责 | 主要回答 |
|---|---|---|
| `moc` | 组织一个主题的知识网络和当前内容 | 这个主题包含什么、彼此如何关联？ |
| `learning-route` | 面向目标给出有顺序的学习路径 | 为达到某个目标应按什么顺序学习？ |
| `index` | 提供尽量完整、简洁的查找入口 | 某类内容在哪里？ |
| `dashboard` | 展示动态状态、行动入口和检查项 | 现在正在做什么、哪些内容需要处理？ |

## MOC

MOC 面向人理解主题结构，负责：

- 解释主题边界；
- 组织已存在的核心文章；
- 展示前置、应用、对比和实验；
- 为同一批文章提供某个稳定视角；
- 说明尚未建设的主题，但不制造空文件。

MOC 不承担完整学习进度，也不追求收录每一篇文章。

## 学习路线

学习路线围绕明确目标和受众组织有序步骤，负责：

- 定义学习目标和完成标准；
- 给出阶段顺序；
- 链接所需 MOC、知识文章和实验；
- 说明每一阶段应能回答的问题；
- 根据不同目标提供不同路线。

同一篇知识文章可以出现在多条学习路线中。学习路线不复制 MOC 的主题说明。

## 索引

索引提供快速查找入口，负责：

- 按术语、公式、算法、API、实验、故障等维度收录入口；
- 保持条目简洁；
- 尽量覆盖已存在内容；
- 允许脚本生成候选列表后人工确认。

索引不解释学习顺序，也不替代知识正文。

## 仪表盘

仪表盘面向当前行动和状态，负责：

- 活跃项目和近期重点；
- 待验证、待更新、正在阅读等动态视图；
- 每周或阶段检查项；
- 常用系统入口。

仪表盘主要依赖 Properties 和查询结果，不承担稳定知识组织。

## Manifest

Manifest 面向规划和自动化，负责：

- 主题稳定 ID；
- 唯一主归属；
- 文章类型；
- 建设状态；
- 学习路线中的上下文优先级；
- 前置依赖；
- 目标文件路径；
- 来源和验证要求。

尚未开始的主题只登记在 Manifest，不创建空 Markdown 文件。

## 职责边界

```text
文件夹    = 稳定主归属
Properties = 类型和动态状态
MOC       = 主题知识网络
学习路线  = 面向目标的顺序
索引      = 查找入口
仪表盘    = 当前行动和状态
Manifest  = 建设计划与机器状态
```

同一份信息只维护一个主版本，其他页面通过链接或查询复用。

## 建设状态

```text
planned
seed
outline
draft
stable
evergreen
```

Manifest 可以在文件尚未创建时使用 `planned`；文件创建后状态应与文章 `maturity` 对齐。

## 路线优先级

A/B/C 属于具体学习路线或建设批次，而不是文章的全局属性。

```yaml
priority:
  graphics-foundation: A
  interview-review: A
  ai-foundation: C
```

简单试点允许使用单值 `priority: A`，正式扩展时改为上下文化映射。

## 路径变化

移动文章时：

1. 更新 Manifest 的 `path`；
2. 依赖 Obsidian 自动更新内部链接；
3. 运行校验脚本；
4. 保留稳定 `id`；
5. 从旧知识库迁移时保留 `legacy_id`。

## 一致性检查

自动化应逐步检查：

- `type: map` 是否具有合法 `map_kind`；
- Manifest 中 `draft` 及以上主题是否存在文件；
- 已登记文件的 Frontmatter `id` 是否匹配；
- ID 是否重复；
- 依赖 ID 是否存在；
- 文件路径是否唯一；
- MOC、路线和索引是否出现失效链接。
'''

MOC_TEMPLATE = '''---
type: map
map_kind: moc
domain:
maturity: outline
created:
updated:
---

# 主题 MOC

## 主题定位

这个主题解决什么问题？与相邻主题的边界是什么？

## 核心知识网络

只链接已经存在、值得主动回访的正式文章。

## 前置知识

## 上层应用

## 对比与边界

## 实验与实现

## 核心来源

## 尚未建设

未实例化主题只使用普通文本，并链接到对应 Manifest。

> 有序学习阶段应放在独立的 `map_kind: learning-route` 笔记中，不在 MOC 中重复维护。
'''

INDEX_CONTENT = '''---
type: map
map_kind: index
domain: knowledge-system
maturity: outline
lifecycle: active
created: 2026-08-04
updated: 2026-08-04
---

# 索引体系

## MOC、路线与索引的区别

- MOC 解释主题网络和知识关系；
- 学习路线给出面向目标的有序步骤；
- 索引提供快速检索入口，尽量保持简洁；
- 仪表盘展示当前状态和行动；
- Manifest 管理尚未实例化的建设计划。

## 全局索引

计划维护：

```text
术语索引
公式索引
算法索引
API 索引
Shader 索引
实验索引
性能案例索引
故障案例索引
来源索引
```

## 收录原则

- 只收录值得主动回访的稳定入口；
- 不复制文章摘要和正文；
- 一个条目可以出现在多个横向索引；
- 条目标题使用正式文章标题；
- 过时内容明确标记替代文章。

## 生成策略

第一阶段手工维护核心索引。文章数量增长后，再由脚本根据 `type`、`domain`、`id`、`apis`、`platforms` 等 Properties 生成候选列表，人工确认后写入正式索引。
'''

ADR_CONTENT = '''---
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


def set_frontmatter_field(path: str, key: str, value: str) -> None:
    text = read(path)
    if not text.startswith("---\n"):
        raise RuntimeError(f"Missing frontmatter: {path}")
    lines = text.splitlines()
    closing = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
        None,
    )
    if closing is None:
        raise RuntimeError(f"Unclosed frontmatter: {path}")

    field_index = next(
        (index for index in range(1, closing) if lines[index].startswith(f"{key}:")),
        None,
    )
    if field_index is not None:
        lines[field_index] = f"{key}: {value}"
    else:
        type_index = next(
            (index for index in range(1, closing) if lines[index].startswith("type:")),
            None,
        )
        insert_at = type_index + 1 if type_index is not None else 1
        lines.insert(insert_at, f"{key}: {value}")
    write(path, "\n".join(lines) + "\n")


def update_validator() -> None:
    path = "scripts/validate_kb.py"
    text = read(path)
    text = text.replace(
        'VALID_LIFECYCLE = {"active", "needs-update", "deprecated", "archived"}',
        'VALID_LIFECYCLE = {"active", "needs-update", "deprecated", "archived"}\nVALID_MAP_KIND = {"moc", "learning-route", "index", "dashboard"}',
        1,
    )
    marker = '''        lifecycle = scalar(props, "lifecycle")
        if lifecycle and lifecycle not in VALID_LIFECYCLE:
            findings.append(Finding("ERROR", path, f"非法 lifecycle：{lifecycle}"))
'''
    replacement = marker + '''
        note_type = scalar(props, "type")
        map_kind = scalar(props, "map_kind")
        if note_type == "map":
            if not map_kind:
                findings.append(Finding("ERROR", path, "type: map 缺少 map_kind"))
            elif map_kind not in VALID_MAP_KIND:
                findings.append(Finding("ERROR", path, f"非法 map_kind：{map_kind}"))
        elif map_kind:
            findings.append(Finding("ERROR", path, "只有 type: map 可以使用 map_kind"))
'''
    if marker not in text:
        raise RuntimeError("Validator lifecycle marker not found")
    text = text.replace(marker, replacement, 1)
    write(path, text)


def update_frontmatter_rules() -> None:
    path = "80 系统/10 治理规则/Frontmatter规范.md"
    text = read(path)
    text = text.replace("dashboard\n", "", 1)
    marker = '''### `maturity`

```text
seed
outline
draft
stable
evergreen
```
'''
    addition = marker + '''
### `map_kind`

当 `type: map` 时必填：

```text
moc
learning-route
index
dashboard
```

分别表示主题知识网络、目标学习路径、查找索引和动态仪表盘。其他类型不得填写 `map_kind`。
'''
    if marker not in text:
        raise RuntimeError("Frontmatter maturity marker not found")
    text = text.replace(marker, addition, 1)
    write(path, text)


def update_dashboard() -> None:
    path = "80 系统/02 导航与仪表盘/系统仪表盘.md"
    text = read(path)
    text = text.replace("type: dashboard", "type: map\nmap_kind: dashboard", 1)
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.5", "version: 3.6", 1)
    text = text.replace(
        "# 个人知识库总体设计方案 v3.5",
        "# 个人知识库总体设计方案 v3.6",
        1,
    )
    marker = '''## 5.8 MOC

MOC 面向人阅读，表达：

- 主题包含什么；
- 推荐学习顺序；
- 核心文章；
- 前置依赖；
- 应用和实验；
- 尚未建设内容。
'''
    replacement = '''## 5.8 地图类笔记

地图类笔记统一使用 `type: map`，并由 `map_kind` 区分：

- `moc`：主题知识网络；
- `learning-route`：面向目标的有序学习路径；
- `index`：简洁查找入口；
- `dashboard`：当前行动和动态状态。

MOC 不替代学习路线，索引不解释知识正文，仪表盘不承担稳定知识组织。
'''
    if marker not in text:
        raise RuntimeError("Design MOC section marker not found")
    text = text.replace(marker, replacement, 1)
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.4", "version: 1.5", 1)
    text = text.replace(
        "个人知识库总体设计方案 v3.5",
        "个人知识库总体设计方案 v3.6",
        1,
    )
    pattern = re.compile(
        r"## F-06：MOC、学习路线和索引需要进一步区分\n[\s\S]*?\n---\n\n## F-07："
    )
    replacement = '''## F-06：地图类笔记职责已区分

### 决策

地图类页面统一使用 `type: map`，通过 `map_kind` 区分 `moc`、`learning-route`、`index` 和 `dashboard`。

MOC 表达主题网络，学习路线表达目标顺序，索引提供查找入口，仪表盘展示动态状态；Manifest 继续独立管理建设计划。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0009-map_kind区分地图类笔记|ADR-0009：map_kind 区分地图类笔记]]。

---

## F-07：'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-06 block")
    text = text.replace(
        "19. 知识领域边界和主归属规则已冻结。",
        "19. 知识领域边界和主归属规则已冻结；\n20. 地图类笔记使用 map_kind 区分职责。",
        1,
    )
    text = text.replace(
        "- [ ] 增加 `map_kind` 区分 MOC、路线、索引和仪表盘；",
        "- [x] 已使用 `map_kind` 区分 MOC、学习路线、索引和仪表盘，并通过 ADR-0009 固化；",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    adr8 = "- [[80 系统/60 ADR/ADR-0008-知识领域边界与主归属|ADR-0008：知识领域边界]]"
    if "ADR-0009-map_kind区分地图类笔记" not in text:
        text = text.replace(
            adr8,
            adr8 + "\n- [[80 系统/60 ADR/ADR-0009-map_kind区分地图类笔记|ADR-0009：地图类笔记职责]]",
            1,
        )
    marker = "- [x] 来源规则已改为按声明类型选择证据；"
    if "map_kind" not in text.split("## 设计评审检查", 1)[1]:
        text = text.replace(
            marker,
            marker + "\n- [x] MOC、学习路线、索引和仪表盘已通过 map_kind 区分；",
            1,
        )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace(
        "- 个人知识库总体设计方案 v3.5；",
        "- 个人知识库总体设计方案 v3.6；",
        1,
    )
    marker = "- ADR-0008：知识领域边界和主归属规则。"
    if "ADR-0009：map_kind" not in text:
        text = text.replace(
            marker,
            marker + "\n- ADR-0009：map_kind 区分地图类笔记。",
            1,
        )
    changed = "- 知识领域职责表和主归属判定流程已冻结。"
    if "地图类笔记已使用 map_kind" not in text:
        text = text.replace(
            changed,
            changed + "\n- 地图类笔记已使用 map_kind 区分 MOC、学习路线、索引和仪表盘。",
            1,
        )
    write(path, text)


def main() -> None:
    for path, kind in MAP_NOTES.items():
        set_frontmatter_field(path, "map_kind", kind)

    update_dashboard()
    write("80 系统/10 治理规则/MOC与Manifest规范.md", MAP_RULES)
    write("80 系统/20 模板/MOC模板.md", MOC_TEMPLATE)
    write("80 系统/40 索引定义/索引体系.md", INDEX_CONTENT)
    write("80 系统/60 ADR/ADR-0009-map_kind区分地图类笔记.md", ADR_CONTENT)
    update_validator()
    update_frontmatter_rules()
    update_design()
    update_review()
    update_home()
    update_changelog()
    print("Map-kind migration complete.")


if __name__ == "__main__":
    main()
