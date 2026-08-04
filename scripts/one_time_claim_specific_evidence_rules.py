#!/usr/bin/env python3
"""One-time Gate A migration for claim-specific evidence rules."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LINK_SOURCE_RULES = '''# 链接与来源规则

## 正文关系

成熟知识文章优先在正文中显式维护：

- 前置知识；
- 上层应用；
- 对比与边界；
- 实现与实验；
- 来源与验证证据。

不要求在 Frontmatter 中维护庞大的 `related` 列表。

## 来源与证据的基本原则

1. 来源笔记与正式知识分离；
2. 一本书、论文或规范可以支持多篇正式知识文章；
3. 正式文章记录与结论直接相关的关键来源；
4. 不建立适用于所有问题的单一“来源权威排行榜”；
5. 证据必须与声明类型匹配；
6. 规范语义、实现行为、实验观察和工程经验分别记录；
7. 来源发生冲突时保留差异和适用条件，不强行合并为一个结论。

## 按声明类型选择证据

| 声明类型 | 首选证据 | 补充证据 |
|---|---|---|
| 数学定义、定理和公式 | 推导、证明、权威教材 | 数值检查、反例 |
| API、格式和标准语义 | 标准、规范、官方文档 | 一致性测试、官方示例 |
| 研究方法和新算法 | 原始论文、作者资料 | 独立复现、后续研究 |
| 特定版本实现行为 | 对应版本源码、最小实验、调试捕获 | Issue、Release Notes |
| 性能结论 | 固定环境基准、Counter、对照实验 | 架构文档、生产监控 |
| 工程经验和故障结论 | 稳定复现、生产记录、修复验证 | 源码、日志、工具捕获 |
| 历史和背景性陈述 | 原始资料、可靠历史来源 | 权威二手资料 |

## 规范语义与观察行为

必须区分：

```text
规范要求什么
实现实际做了什么
特定环境观察到了什么
工程上决定如何处理
```

例如驱动缺陷不能改写成 API 规范语义；某个引擎版本的源码行为也不能自动推广到所有版本。

## `source-checked` 的使用条件

只有完成以下操作后，才能在 `verification` 中加入 `source-checked`：

- 已明确文章中的主要声明类型；
- 已选择与声明类型匹配的来源；
- 已确认来源真正支持正文结论；
- 版本敏感内容已记录平台、版本或验证日期；
- 来源冲突和不确定性已在正文中说明。

`source-checked` 不表示“文章引用过资料”，也不表示所有结论都已经通过实验。

## 来源笔记职责

来源笔记应记录：

- 书目信息和版本；
- 阅读目的；
- 可支持的声明类型；
- 章节或内容地图；
- 重要结论及其定位；
- 限制、立场和适用范围；
- 待验证问题；
- 已提炼的正式知识。

## 唯一基础解释

基础理论只维护一个完整主版本；知识领域的应用文章通过链接复用基础理论，不重新复制整段定义与推导。

## 过时内容

过时文章使用 `deprecated` 和 `superseded_by`，保留历史链接、原版本语义和替代关系。
'''

SOURCE_TEMPLATE = '''---
type: source-note
source_type:
status: unread
created:
updated:
---

# 作者 - 标题

## 书目信息与版本

## 阅读目的

## 可支持的声明类型

例如：数学理论、规范语义、研究算法、实现行为、性能观察、工程经验或历史背景。

## 核心主题

## 章节或内容地图

## 重要结论与定位

记录章节、页码、版本、提交或其他可追踪位置。

## 限制、立场与适用范围

## 待验证问题

## 提炼出的正式知识

## 相关项目与输出

## 阅读进度
'''

SOURCE_README = '''# 40 来源

来源是知识的证据入口，不是正式知识正文，也不存在适用于所有问题的统一权威排序。

## 来源类型

- 书籍；
- 论文；
- 官方文档与规范；
- 课程与视频；
- 文章与博客；
- 代码仓库与版本源码；
- 数据集与素材；
- 实验、调试捕获与生产记录；
- 访谈与对话。

## 使用原则

来源的价值取决于它能支持什么声明：

- 数学结论优先看证明、推导和权威教材；
- API 语义优先看标准、规范和官方文档；
- 新算法优先看原始论文和独立复现；
- 具体实现行为看对应版本源码、实验和调试捕获；
- 性能结论依赖明确环境下的测量；
- 工程经验必须记录复现条件和适用边界。

来源笔记记录书目信息、版本、阅读目的、可支持的声明类型、章节地图、限制、待验证问题以及已经提炼出的正式知识。

详细规则见 [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]。
'''

ADR_CONTENT = '''---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0007：按声明类型选择证据

## 背景

原总体设计尝试把推导、实验、官方文档、论文、教材、源码和经验排成一个全局顺序。但不同声明需要不同证据：API 的规范语义、某个驱动的实际行为、数学定理和性能测试不能使用同一套优先级判断。

## 决策

不建立全局来源权威排行榜，改为按声明类型选择证据：

| 声明类型 | 首选证据 |
|---|---|
| 数学定义与定理 | 推导、证明、权威教材 |
| API 与标准语义 | 标准、规范、官方文档 |
| 科研方法与新算法 | 原始论文、作者资料、独立复现 |
| 具体实现行为 | 对应版本源码、最小实验、调试捕获 |
| 性能结论 | 固定环境基准、Counter、对照实验 |
| 工程经验 | 生产记录、复现条件、修复验证 |

## 冲突处理

来源冲突时分别记录：

- 规范语义；
- 版本实现；
- 实验环境和观察；
- 工程决策及适用范围。

不得用实现缺陷覆盖规范语义，也不得把单一环境的观察推广为普遍规律。

## 对 verification 的影响

`source-checked` 只表示文章已使用与主要声明类型匹配的来源完成核对。它不等于实验复现或生产验证，其他证据继续分别记录。

## 影响

- 总体设计的来源章节改为声明—证据匹配模型；
- 来源笔记模板增加“可支持的声明类型”和限制；
- 链接与来源规则明确规范、实现和观察的边界；
- `authority` 不再用于跨类型全局排序。

## 关联文档

- [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]
- [[40 来源/README|来源入口]]
- [[80 系统/03 总体设计评审记录|总体设计评审记录]]
'''

DESIGN_EVIDENCE_SECTION = '''# 11. 来源与证据体系

## 11.1 不使用全局权威排序

来源是否可靠取决于它要支持的声明类型。数学定理、API 规范、版本源码、性能测试和工程经验不能放在同一条固定优先级链上。

本系统采用“声明—证据匹配”模型。

## 11.2 按声明类型选择证据

| 声明类型 | 首选证据 | 补充证据 |
|---|---|---|
| 数学定义、定理和公式 | 推导、证明、权威教材 | 数值检查、反例 |
| API、文件格式和标准语义 | 标准、规范、官方文档 | 一致性测试、官方示例 |
| 科研方法和新算法 | 原始论文、作者资料 | 独立复现、后续研究 |
| 特定版本实现行为 | 对应版本源码、最小实验、调试捕获 | Issue、Release Notes |
| 性能结论 | 固定环境基准、Counter、对照实验 | 架构文档、生产监控 |
| 工程经验和故障结论 | 稳定复现、生产记录、修复验证 | 源码、日志、工具捕获 |
| 历史和背景性陈述 | 原始资料、可靠历史来源 | 权威二手资料 |

## 11.3 规范、实现与观察分离

文章需要明确区分：

```text
规范要求什么
特定版本实现做了什么
实验环境观察到了什么
工程上选择如何处理
```

驱动或引擎缺陷不能改写成 API 规范语义；一个版本的源码行为也不能无条件推广到其他版本。

## 11.4 `source-checked` 的含义

在 `verification` 中加入 `source-checked` 前，需要完成：

- 识别文章的主要声明类型；
- 选择与声明类型匹配的来源；
- 核对来源是否真正支持结论；
- 为版本敏感内容记录平台、版本或验证日期；
- 在正文说明冲突、不确定性和适用范围。

Frontmatter 只记录证据类型，具体来源和定位保留在正文及来源笔记中。

## 11.5 版本敏感内容

以下内容默认视为版本敏感：

- API；
- 引擎源码和工具界面；
- 平台能力；
- 驱动行为；
- 软件安装与配置；
- 法规、价格和当前产品信息。

版本敏感文章需要记录平台、版本、验证日期和与声明匹配的来源。

## 11.6 验证闭环

根据文章类型选择验证方式：

- 理论：推导、反例和数值检查；
- 算法：参考实现、单元测试和复杂度验证；
- 图形算法：图像结果、Golden Image、Frame Capture；
- API：规范核对、最小示例和跨平台一致性检查；
- 性能：测试环境、GPU Counter 和对照实验；
- 故障：稳定复现、根因和修复后验证；
- 系统架构：数据流、生命周期、失败路径和真实项目应用。

详细规则见 [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]。

---
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
    text = text.replace("version: 3.3", "version: 3.4", 1)
    text = text.replace(
        "# 个人知识库总体设计方案 v3.3",
        "# 个人知识库总体设计方案 v3.4",
        1,
    )
    pattern = re.compile(
        r"# 11\. 来源与证据体系\n[\s\S]*?\n---\n\n# 12\. 工作流设计"
    )
    replacement = DESIGN_EVIDENCE_SECTION + "\n# 12. 工作流设计"
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace design evidence section")
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.2", "version: 1.3", 1)
    text = text.replace(
        "个人知识库总体设计方案 v3.2",
        "个人知识库总体设计方案 v3.4",
        1,
    )
    text = text.replace(
        "但在证据规则和领域边界冻结前，不进入 Phase 2。",
        "但在领域边界和剩余治理规则冻结前，不进入 Phase 2。",
        1,
    )
    pattern = re.compile(
        r"# 4\. 待决策阻断项\n\n## F-04：来源权威不能使用单一全局排序"
        r"[\s\S]*?### 状态\n\n`decision-required`\n\n---\n"
    )
    replacement = '''# 4. 新增已解决决策

## F-04：按声明类型选择证据

### 决策

不建立跨所有问题的统一来源权威排序，改为按声明类型选择证据。数学、API 规范、研究算法、版本实现、性能和工程经验分别使用与其性质匹配的首选证据。

规范语义、实现行为和实验观察必须分开记录；来源冲突时保留差异、版本、环境和适用范围。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0007-按声明类型选择证据|ADR-0007：按声明类型选择证据]]。

---
'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-04 review block")
    text = text.replace(
        "17. verification 使用多证据列表。",
        "17. verification 使用多证据列表；\n18. 来源按声明类型选择证据。",
        1,
    )
    text = text.replace(
        "- [ ] 将来源权威规则改为按声明类型选择证据；",
        "- [x] 来源规则已改为按声明类型选择证据，并通过 ADR-0007 固化；",
        1,
    )
    write(path, text)


def update_frontmatter_rules() -> None:
    path = "80 系统/10 治理规则/Frontmatter规范.md"
    text = read(path)
    text = text.replace("authority: authoritative-secondary\n", "", 1)
    marker = "来源状态：`unread`、`reading`、`processed`、`reference`、`abandoned`。"
    addition = marker + "\n\n来源不使用单一 `authority` 字段进行跨类型全局排序。来源能支持哪些声明，应在正文的“可支持的声明类型”中说明。"
    if marker not in text:
        raise RuntimeError("Source status marker missing")
    text = text.replace(marker, addition, 1)
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    adr6 = "- [[80 系统/60 ADR/ADR-0006-verification使用多证据列表|ADR-0006：多证据验证模型]]"
    if "ADR-0007-按声明类型选择证据" not in text:
        text = text.replace(
            adr6,
            adr6 + "\n- [[80 系统/60 ADR/ADR-0007-按声明类型选择证据|ADR-0007：声明—证据匹配]]",
            1,
        )
    checklist = "- [x] verification 已改为多证据列表；"
    if "来源规则已改为按声明类型选择证据" not in text:
        text = text.replace(
            checklist,
            checklist + "\n- [x] 来源规则已改为按声明类型选择证据；",
            1,
        )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace(
        "- 个人知识库总体设计方案 v3.3；",
        "- 个人知识库总体设计方案 v3.4；",
        1,
    )
    added = "- ADR-0006：verification 使用多证据列表。"
    if "ADR-0007：按声明类型选择证据" not in text:
        text = text.replace(
            added,
            added + "\n- ADR-0007：按声明类型选择证据。",
            1,
        )
    changed = "- 验证模型已从单值改为多证据列表，并同步现有试点文章、模板、Manifest 和校验脚本。"
    if "来源规则已从全局权威排序改为声明—证据匹配" not in text:
        text = text.replace(
            changed,
            changed + "\n- 来源规则已从全局权威排序改为声明—证据匹配模型。",
            1,
        )
    write(path, text)


def main() -> None:
    write("80 系统/10 治理规则/链接与来源规则.md", LINK_SOURCE_RULES)
    write("80 系统/20 模板/来源笔记模板.md", SOURCE_TEMPLATE)
    write("40 来源/README.md", SOURCE_README)
    write("80 系统/60 ADR/ADR-0007-按声明类型选择证据.md", ADR_CONTENT)
    update_design()
    update_review()
    update_frontmatter_rules()
    update_home()
    update_changelog()
    print("Claim-specific evidence rules migration complete.")


if __name__ == "__main__":
    main()
