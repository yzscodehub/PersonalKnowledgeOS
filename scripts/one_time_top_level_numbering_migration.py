#!/usr/bin/env python3
"""One-time Gate A migration to freeze top-level numbering semantics."""

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

# ADR-0012：顶层编号采用语义分区并保留 70

## 背景

当前顶层目录从 `60 日记与回顾` 跳到 `80 系统`。若不解释该空缺，后续可能为了编号连续而随意创建职责不清的目录。

## 决策

顶层编号表示稳定语义分区，不要求连续：

```text
00        捕捉入口
10～60    行动、知识、来源、输出和时间记录
70        保留扩展位
80        系统治理
90        档案
```

`70` 暂不创建实体目录。只有未来出现无法合理归入现有角色、具有长期稳定职责的新顶层对象，并经过 ADR 评审后，才允许启用。

`experiments`、`scripts` 和 `.github` 是仓库工程支持目录，不参与 Obsidian 信息角色编号。

## 影响

- 不为了补齐编号新增目录；
- `80 系统` 和 `90 档案` 保持语义固定；
- 新知识领域继续放在 `30 知识`，不会占用顶层编号；
- 启用 `70` 或改变现有编号必须创建新的 ADR 和迁移计划。

## 关联文档

- [[80 系统/10 治理规则/命名与目录规范|命名与目录规范]]
- [[80 系统/01 知识库设计说明|总体设计方案]]
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


def update_naming_rules() -> None:
    path = "80 系统/10 治理规则/命名与目录规范.md"
    text = read(path)
    marker = "## 避免使用"
    section = '''## 顶层编号语义

顶层编号是语义分区，不承诺连续：

```text
00        收件与捕捉
10～60    核心信息角色
70        保留扩展位，不创建实体目录
80        系统治理
90        档案
```

规则：

- 不为了填补编号创建新顶层目录；
- 新学科进入 `30 知识`，不占用顶层编号；
- `experiments`、`scripts`、`.github` 是工程支持目录，不参与编号；
- 启用 `70`、重编号或增加顶层角色必须创建 ADR；
- `80 系统` 和 `90 档案` 作为语义固定编号长期保留。

'''
    if section.strip() not in text:
        text = text.replace(marker, section + marker, 1)
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.8", "version: 3.9", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.8", "# 个人知识库总体设计方案 v3.9", 1)
    marker = "## 4.2 文件夹使用原则"
    section = '''## 4.2 顶层编号语义

顶层编号用于稳定语义分区，不要求连续：

```text
00        捕捉入口
10～60    核心信息角色
70        保留扩展位
80        系统治理
90        档案
```

`70` 当前不创建实体目录。未来只有出现无法归入现有角色的新型长期对象，并通过 ADR 后才能启用。`experiments`、`scripts` 和 `.github` 属于仓库工程支持目录，不参与 Obsidian 信息角色编号。

## 4.3 文件夹使用原则'''
    if marker not in text:
        raise RuntimeError("Design folder principle marker not found")
    text = text.replace(marker, section, 1)
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.7", "version: 1.8", 1)
    text = text.replace("个人知识库总体设计方案 v3.8", "个人知识库总体设计方案 v3.9", 1)
    pattern = re.compile(r"## F-09：顶层编号 `70` 的空缺需要说明\n[\s\S]*?\n---\n")
    replacement = '''## F-09：顶层编号语义已确认

### 决策

顶层编号采用语义分区，不要求连续；`70` 作为保留扩展位，不创建实体目录。`80 系统` 与 `90 档案` 保持语义固定，工程支持目录不参与编号。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0012-顶层编号语义与70保留位|ADR-0012：顶层编号语义与 70 保留位]]。

---
'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-09 block")
    text = text.replace(
        "22. 公开附件、版权与大文件策略已冻结。",
        "22. 公开附件、版权与大文件策略已冻结；\n23. 顶层编号语义和 70 保留位已冻结。",
        1,
    )
    text = text.replace(
        "- [ ] 说明顶层编号空缺；",
        "- [x] 顶层编号语义和 `70` 保留位已通过 ADR-0012 固化；",
        1,
    )
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("version: 1.0", "version: 1.1", 1)
    text = text.replace(
        "- [ ] 明确是否保留当前顶层编号和命名；",
        "- [x] 顶层命名和编号语义已通过 ADR-0005、ADR-0012 固化；",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    adr11 = "- [[80 系统/60 ADR/ADR-0011-公开附件版权与大文件策略|ADR-0011：公开附件策略]]"
    if "ADR-0012-顶层编号语义与70保留位" not in text:
        text = text.replace(
            adr11,
            adr11 + "\n- [[80 系统/60 ADR/ADR-0012-顶层编号语义与70保留位|ADR-0012：顶层编号语义]]",
            1,
        )
    text = text.replace(
        "- [ ] 顶层目录职责是否清晰且无明显重叠？",
        "- [x] 顶层目录职责、命名和编号语义已确认；",
        1,
    )
    marker = "- [x] 公开附件、版权与大文件规则已确定；"
    if "70 保留位" not in text:
        text = text.replace(marker, marker + "\n- [x] 顶层编号语义和 70 保留位已确定；", 1)
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    marker = "_assets          图片与附件\n```"
    replacement = "_assets          图片与附件\n```\n\n编号不要求连续：`70` 是保留扩展位，`80` 和 `90` 是系统与档案的固定语义编号；`experiments`、`scripts` 等工程目录不参与编号。"
    if "70` 是保留扩展位" not in text:
        text = text.replace(marker, replacement, 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace("- 个人知识库总体设计方案 v3.8；", "- 个人知识库总体设计方案 v3.9；", 1)
    marker = "- ADR-0011：公开附件、版权与大文件策略。"
    if "ADR-0012：顶层编号" not in text:
        text = text.replace(marker, marker + "\n- ADR-0012：顶层编号语义与 70 保留位。", 1)
    changed = "- 公共附件和大文件 CI 检查已加入。"
    if "顶层编号已明确为语义分区" not in text:
        text = text.replace(changed, changed + "\n- 顶层编号已明确为语义分区，并保留 70 扩展位。", 1)
    write(path, text)


def main() -> None:
    write("80 系统/60 ADR/ADR-0012-顶层编号语义与70保留位.md", ADR)
    update_naming_rules()
    update_design()
    update_review()
    update_roadmap()
    update_home()
    update_readme()
    update_changelog()
    print("Top-level numbering semantics frozen.")


if __name__ == "__main__":
    main()
