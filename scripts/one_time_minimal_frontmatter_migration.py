#!/usr/bin/env python3
"""One-time Gate A migration for minimal Frontmatter and date automation."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAP_PATHS = [
    "30 知识/00 知识总览.md",
    "30 知识/01 数学/00 数学总览.md",
    "30 知识/01 数学/01 数学学习路线/图形学数学基础学习路线.md",
    "30 知识/01 数学/02 数学知识地图/线性代数与空间变换 MOC.md",
    "30 知识/04 图形学与渲染/00 图形学总览.md",
    "30 知识/04 图形学与渲染/01 图形学学习路线/实时渲染基础学习路线.md",
    "30 知识/04 图形学与渲染/02 图形学知识地图/坐标、相机与投影 MOC.md",
    "30 知识/04 图形学与渲染/02 图形学知识地图/实时光栅化管线 MOC.md",
]

TEMPLATE_PATHS = [
    "80 系统/20 模板/知识文章模板.md",
    "80 系统/20 模板/API文章模板.md",
    "80 系统/20 模板/实验文章模板.md",
    "80 系统/20 模板/故障排查模板.md",
    "80 系统/20 模板/MOC模板.md",
    "80 系统/20 模板/来源笔记模板.md",
    "80 系统/20 模板/项目主页模板.md",
]

FRONTMATTER_RULES = '''# Frontmatter 规范

## 目标

Properties 只保存机器需要查询、校验或自动化的稳定结构和动态状态。知识关系、论证和证据明细保留在正文中。

## 最小字段模型

### 正式知识文章

适用于 `concept`、`theory`、`algorithm`、`system`、`api-reference`、`implementation`、`experiment`、`troubleshooting`、`comparison` 和 `principle`：

```yaml
---
id: GFX-PROJ-002
type: theory
domain: graphics
maturity: draft
lifecycle: active
verification:
  - source-checked
  - derived
sources:
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---
```

必填核心字段：

```text
id
type
domain
maturity
lifecycle
```

### 地图类笔记

```yaml
---
type: map
map_kind: moc
domain: graphics
maturity: draft
lifecycle: active
created: 2026-08-04
updated: 2026-08-04
---
```

`id` 仅在地图被 Manifest 稳定引用时按需填写。

### 来源笔记

```yaml
---
type: source-note
source_type: book
status: reading
created: 2026-08-04
updated: 2026-08-04
---
```

来源必填字段：`type`、`source_type`、`status`。

### 项目笔记

```yaml
---
type: project
status: active
area:
  - "[[职业与技术能力]]"
created: 2026-08-04
updated: 2026-08-04
---
```

项目必填字段：`type`、`status`。

## 条件字段

| 条件 | 要求 |
|---|---|
| 存在验证证据 | `verification` 使用列表 |
| 正式知识达到 `draft` 或更高 | `sources` 至少包含一个来源；纯原创推导或实验可以用对应证据替代 |
| `type: map` | 必须填写合法 `map_kind` |
| 版本敏感 | 按需填写 `platforms`、`apis`、`versions`、`version_sensitive` |
| 从旧库迁移 | 填写 `legacy_id` |
| 已被替代 | 填写 `superseded_by` |

## 字段词表

### `type`

```text
concept
theory
algorithm
system
api-reference
implementation
experiment
troubleshooting
comparison
principle
map
source-note
project
area
output
journal
system-design
```

### `domain`

```text
mathematics
physics-engineering
computer-science
graphics
artificial-intelligence
software-engineering
systems-platforms
game-engine
multimedia
embedded-robotics-autonomous-driving
design-content
product-business-career
humanities-social-sciences
knowledge-system
```

### `maturity`

```text
seed
outline
draft
stable
evergreen
```

### `map_kind`

```text
moc
learning-route
index
dashboard
```

### `verification`

```text
source-checked
derived
experiment-reproduced
production-validated
```

尚无证据时使用 `verification: []` 或省略字段。不得使用标量，也不使用 `unverified`。

### `lifecycle`

```text
active
needs-update
deprecated
archived
```

## 日期策略

`created` 和 `updated` 不作为知识语义字段，也不要求人工在每次编辑时维护。

- 模板在创建笔记时写入 `{{date}}`；
- `created` 首次写入后保持不变；
- 提交前运行 `python scripts/sync_note_dates.py --staged`，自动补充空日期并更新暂存区 Markdown 的 `updated`；
- CI 校验已存在日期的格式，但日期字段本身不作为正式知识必填项；
- 需要精确历史时以 Git 记录为最终依据。

## 按需字段

```text
aliases
module
contexts
prerequisites
platforms
apis
versions
version_sensitive
project
legacy_id
superseded_by
```

## 禁止事项

- 不维护与正文重复的庞大 `related` 列表；
- 不把 A/B/C 写成文章的全局绝对优先级；
- 不用标签重复表达目录和知识领域；
- 不把成熟度、生命周期和验证证据混成一条状态链；
- 不把 `verification` 写成单值；
- 不为每篇笔记强制填写所有可选字段；
- 不为了更新时间而进行无意义提交。
'''

DATE_SCRIPT = r'''#!/usr/bin/env python3
"""Synchronize created/updated fields for Markdown notes.

Usage:
    python scripts/sync_note_dates.py --staged
    python scripts/sync_note_dates.py path/to/note.md another.md

The script preserves an existing created date, fills it only when missing or blank,
and sets updated to today's local date. It does not stage files automatically.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def staged_markdown() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = ROOT / line
        if path.suffix.lower() == ".md" and path.exists():
            paths.append(path)
    return paths


def frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return 0, index
    return None


def set_scalar(lines: list[str], closing: int, key: str, value: str, *, preserve: bool) -> int:
    for index in range(1, closing):
        if lines[index].startswith(f"{key}:"):
            current = lines[index].split(":", 1)[1].strip()
            if preserve and current:
                return closing
            lines[index] = f"{key}: {value}"
            return closing
    lines.insert(closing, f"{key}: {value}")
    return closing + 1


def update(path: Path, today: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    bounds = frontmatter_bounds(lines)
    if bounds is None:
        return False
    _, closing = bounds
    closing = set_scalar(lines, closing, "created", today, preserve=True)
    set_scalar(lines, closing, "updated", today, preserve=False)
    updated = "\n".join(lines) + "\n"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    print(path.relative_to(ROOT).as_posix())
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()

    if args.staged and args.paths:
        parser.error("--staged cannot be combined with explicit paths")
    if not args.staged and not args.paths:
        parser.error("provide --staged or one or more Markdown paths")

    paths = staged_markdown() if args.staged else [ROOT / item for item in args.paths]
    today = date.today().isoformat()
    changed = sum(update(path, today) for path in paths if path.suffix.lower() == ".md")
    print(f"Updated {changed} note(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

ADR_CONTENT = '''---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0010：采用最小 Frontmatter 与日期自动化

## 背景

Frontmatter 过重会增加捕捉和维护成本，而字段过少又无法支持查询、校验和迁移。`created`、`updated` 尤其容易成为高频手工负担。

## 决策

正式知识文章的核心必填字段为：

```text
id
type
domain
maturity
lifecycle
```

地图类笔记使用 `type`、`map_kind`、`domain`、`maturity`、`lifecycle`；来源和项目使用各自最小状态字段。

`verification`、`sources`、平台版本和迁移字段按条件填写。

日期策略：

- 模板创建时写入日期；
- `created` 首次写入后保持不变；
- `updated` 由 `scripts/sync_note_dates.py` 对暂存区笔记自动更新；
- 日期不作为知识正文必填字段，Git 历史是最终依据。

## 校验

- 正式知识类型必须具有核心字段；
- 地图类笔记必须具有 `map_kind` 和 `lifecycle`；
- `draft` 以上文章必须具有来源或推导、实验、生产证据；
- 已填写的日期必须符合 `YYYY-MM-DD`；
- 模板和系统说明不因空占位符触发正式知识校验。

## 影响

- 现有地图笔记补充 `lifecycle: active`；
- 模板统一使用 `{{date}}`；
- 校验脚本改为按笔记类型检查字段；
- 提交流程增加日期同步命令；
- 不再要求人工维护所有可选属性。

## 关联文档

- [[80 系统/10 治理规则/Frontmatter规范|Frontmatter 规范]]
- [[80 系统/70 Obsidian与Git/Git工作流|Git 工作流]]
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


def set_frontmatter_scalar(path: str, key: str, value: str) -> None:
    text = read(path)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise RuntimeError(f"Missing frontmatter: {path}")
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        raise RuntimeError(f"Unclosed frontmatter: {path}")
    index = next((i for i in range(1, closing) if lines[i].startswith(f"{key}:")), None)
    if index is None:
        insert_at = next((i for i in range(1, closing) if lines[i].startswith("created:")), closing)
        lines.insert(insert_at, f"{key}: {value}")
    else:
        lines[index] = f"{key}: {value}"
    write(path, "\n".join(lines) + "\n")


def update_templates() -> None:
    for path in TEMPLATE_PATHS:
        text = read(path)
        text = re.sub(r"(?m)^created:\s*$", "created: {{date}}", text)
        text = re.sub(r"(?m)^updated:\s*$", "updated: {{date}}", text)
        if path.endswith("项目主页模板.md") and "updated:" not in text.split("---", 2)[1]:
            text = text.replace("created: {{date}}", "created: {{date}}\nupdated: {{date}}", 1)
        if path.endswith("知识文章模板.md") and not re.search(r"(?m)^id:", text):
            text = text.replace("---\n", "---\nid:\n", 1)
        write(path, text)


def update_validator() -> None:
    path = "scripts/validate_kb.py"
    text = read(path)
    text = text.replace(
        'KNOWLEDGE_REQUIRED = {"type", "domain", "maturity", "created", "updated"}\nSOURCE_REQUIRED = {"type", "source_type", "status", "created", "updated"}',
        'CANONICAL_KNOWLEDGE_REQUIRED = {"id", "type", "domain", "maturity", "lifecycle"}\nMAP_REQUIRED = {"type", "map_kind", "domain", "maturity", "lifecycle"}\nSOURCE_REQUIRED = {"type", "source_type", "status"}\nCANONICAL_KNOWLEDGE_TYPES = {\n    "concept", "theory", "algorithm", "system", "api-reference",\n    "implementation", "experiment", "troubleshooting", "comparison", "principle",\n}\nDATE_RE = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")',
        1,
    )
    old_required = '''        required: set[str] = set()
        if formal_knowledge(path):
            required = KNOWLEDGE_REQUIRED
        elif formal_source(path):
            required = SOURCE_REQUIRED
'''
    new_required = '''        required: set[str] = set()
        note_type = scalar(props, "type")
        if formal_knowledge(path):
            required = MAP_REQUIRED if note_type == "map" else CANONICAL_KNOWLEDGE_REQUIRED
        elif formal_source(path):
            required = SOURCE_REQUIRED
'''
    if old_required not in text:
        raise RuntimeError("Validator required-fields block not found")
    text = text.replace(old_required, new_required, 1)
    text = text.replace(
        '        note_type = scalar(props, "type")\n        map_kind = scalar(props, "map_kind")',
        '        map_kind = scalar(props, "map_kind")',
        1,
    )
    marker = '''        validate_verification(path, props, findings)

        lifecycle = scalar(props, "lifecycle")
'''
    addition = '''        validate_verification(path, props, findings)

        maturity_rank = {"seed": 0, "outline": 1, "draft": 2, "stable": 3, "evergreen": 4}
        if formal_knowledge(path) and note_type in CANONICAL_KNOWLEDGE_TYPES:
            if maturity_rank.get(maturity, 0) >= maturity_rank["draft"]:
                sources = props.get("sources", [])
                verification = props.get("verification", [])
                has_sources = isinstance(sources, list) and bool(sources)
                evidence = set(verification) if isinstance(verification, list) else set()
                original_evidence = {"derived", "experiment-reproduced", "production-validated"}
                if not has_sources and not evidence.intersection(original_evidence):
                    findings.append(
                        Finding(
                            "ERROR",
                            path,
                            "draft 及以上正式知识需要 sources，或 derived/experiment/production 证据",
                        )
                    )

        for date_key in ("created", "updated"):
            date_value = scalar(props, date_key)
            if date_value and not DATE_RE.match(date_value):
                findings.append(Finding("ERROR", path, f"非法 {date_key} 日期：{date_value}"))

        lifecycle = scalar(props, "lifecycle")
'''
    if marker not in text:
        raise RuntimeError("Validator verification marker not found")
    text = text.replace(marker, addition, 1)
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.6", "version: 3.7", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.6", "# 个人知识库总体设计方案 v3.7", 1)
    pattern = re.compile(r"# 9\. 元数据设计\n[\s\S]*?\n---\n\n# 10\. 链接与知识关系")
    replacement = '''# 9. 元数据设计

## 9.1 最小核心字段

正式知识文章必填：

```text
id
type
domain
maturity
lifecycle
```

地图类笔记必填：

```text
type
map_kind
domain
maturity
lifecycle
```

来源和项目使用各自最小类型与状态字段。

## 9.2 条件字段

- 有证据时填写 `verification` 列表；
- 正式知识达到 `draft` 时填写 `sources`，原创推导或实验可由对应证据替代；
- 版本敏感文章填写平台、API 和版本；
- 迁移文章填写 `legacy_id`；
- 替代旧文章时填写 `superseded_by`。

## 9.3 日期自动化

模板创建笔记时写入 `created` 和 `updated`。提交前运行：

```bash
python scripts/sync_note_dates.py --staged
```

脚本保留已有 `created`，并更新暂存 Markdown 的 `updated`。日期字段不要求人工持续维护，Git 历史是最终依据。

## 9.4 三个独立维度

- `maturity`：内容建设程度，单值；
- `verification`：已具备的证据，多选列表；
- `lifecycle`：当前维护状态，单值。

## 9.5 A/B/C 优先级

A/B/C 属于具体学习路线或建设计划，不是文章的绝对属性，保存在 Manifest 或学习路线中。

详细规则见 [[80 系统/10 治理规则/Frontmatter规范|Frontmatter 规范]]。

---

# 10. 链接与知识关系'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace metadata section")
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.5", "version: 1.6", 1)
    text = text.replace("个人知识库总体设计方案 v3.6", "个人知识库总体设计方案 v3.7", 1)
    pattern = re.compile(r"## F-07：最小 Frontmatter 仍需降低手工维护成本\n[\s\S]*?\n---\n\n## F-08：")
    replacement = '''## F-07：最小 Frontmatter 和日期策略已确认

### 决策

正式知识只强制 `id`、`type`、`domain`、`maturity`、`lifecycle`；地图、来源和项目采用各自最小字段。验证、来源、平台版本和迁移字段按条件填写。

模板写入日期，`scripts/sync_note_dates.py --staged` 自动维护暂存笔记的 `updated`；日期不再作为知识语义必填字段。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0010-最小Frontmatter与日期自动化|ADR-0010：最小 Frontmatter 与日期自动化]]。

---

## F-08：'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-07 block")
    text = text.replace(
        "20. 地图类笔记使用 map_kind 区分职责。",
        "20. 地图类笔记使用 map_kind 区分职责；\n21. 最小 Frontmatter 和日期自动化策略已冻结。",
        1,
    )
    text = text.replace(
        "- [ ] 确定最小 Frontmatter 和日期自动化策略；",
        "- [x] 最小 Frontmatter 和日期自动化策略已通过 ADR-0010 固化；",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    adr9 = "- [[80 系统/60 ADR/ADR-0009-map_kind区分地图类笔记|ADR-0009：地图类笔记职责]]"
    if "ADR-0010-最小Frontmatter与日期自动化" not in text:
        text = text.replace(
            adr9,
            adr9 + "\n- [[80 系统/60 ADR/ADR-0010-最小Frontmatter与日期自动化|ADR-0010：最小元数据模型]]",
            1,
        )
    marker = "- [x] MOC、学习路线、索引和仪表盘已通过 map_kind 区分；"
    if "最小 Frontmatter 和日期自动化" not in text:
        text = text.replace(
            marker,
            marker + "\n- [x] 最小 Frontmatter 和日期自动化策略已确定；",
            1,
        )
    write(path, text)


def update_git_docs() -> None:
    path = "80 系统/70 Obsidian与Git/Git工作流.md"
    text = read(path)
    text = text.replace(
        "```bash\npython scripts/validate_kb.py\n```",
        "```bash\npython scripts/sync_note_dates.py --staged\ngit add .\npython scripts/validate_kb.py\n```",
        1,
    )
    write(path, text)

    path = "CONTRIBUTING.md"
    text = read(path)
    text = text.replace(
        "5. 运行 `python scripts/validate_kb.py`；",
        "5. 暂存后运行 `python scripts/sync_note_dates.py --staged`，重新暂存，再运行 `python scripts/validate_kb.py`；",
        1,
    )
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace("- 个人知识库总体设计方案 v3.6；", "- 个人知识库总体设计方案 v3.7；", 1)
    marker = "- ADR-0009：map_kind 区分地图类笔记。"
    if "ADR-0010：最小 Frontmatter" not in text:
        text = text.replace(marker, marker + "\n- ADR-0010：最小 Frontmatter 与日期自动化。", 1)
    changed = "- 地图类笔记已使用 map_kind 区分 MOC、学习路线、索引和仪表盘。"
    if "最小 Frontmatter 和暂存区日期同步策略" not in text:
        text = text.replace(changed, changed + "\n- 最小 Frontmatter 和暂存区日期同步策略已落地。", 1)
    write(path, text)


def main() -> None:
    for path in MAP_PATHS:
        set_frontmatter_scalar(path, "lifecycle", "active")
    update_templates()
    write("80 系统/10 治理规则/Frontmatter规范.md", FRONTMATTER_RULES)
    write("scripts/sync_note_dates.py", DATE_SCRIPT)
    write("80 系统/60 ADR/ADR-0010-最小Frontmatter与日期自动化.md", ADR_CONTENT)
    update_validator()
    update_design()
    update_review()
    update_home()
    update_git_docs()
    update_changelog()
    print("Minimal Frontmatter migration complete.")


if __name__ == "__main__":
    main()
