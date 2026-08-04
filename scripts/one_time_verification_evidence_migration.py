#!/usr/bin/env python3
"""One-time migration from scalar verification state to evidence lists.

The migration is intentionally scoped to the Gate A verification-model decision.
It updates current pilot notes, templates, governance documents, the validator,
Manifest metadata, the system dashboard, and review records.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTICLE_EVIDENCE: dict[str, list[str]] = {
    "30 知识/01 数学/11 线性代数/点与向量.md": ["source-checked"],
    "30 知识/01 数学/11 线性代数/向量空间.md": ["source-checked"],
    "30 知识/01 数学/11 线性代数/基与坐标.md": ["source-checked"],
    "30 知识/01 数学/11 线性代数/矩阵作为线性映射.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/01 数学/12 解析、仿射与射影几何/仿射空间与仿射组合.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系.md": [
        "source-checked"
    ],
    "30 知识/01 数学/12 解析、仿射与射影几何/齐次坐标.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览.md": [
        "source-checked"
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换.md": [
        "source-checked"
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC.md": [
        "source-checked",
        "derived",
    ],
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z.md": [
        "source-checked",
        "derived",
        "experiment-reproduced",
    ],
    "30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验.md": [
        "source-checked",
        "experiment-reproduced",
    ],
    "30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验.md": [
        "source-checked",
        "experiment-reproduced",
    ],
    "30 知识/04 图形学与渲染/80 图形学实验与实现/深度精度与 Reversed-Z 实验.md": [
        "source-checked",
        "experiment-reproduced",
    ],
}

TEMPLATE_PATHS = [
    "80 系统/20 模板/知识文章模板.md",
    "80 系统/20 模板/API文章模板.md",
    "80 系统/20 模板/实验文章模板.md",
    "80 系统/20 模板/故障排查模板.md",
]

VALIDATOR_CONTENT = r'''#!/usr/bin/env python3
"""Validate the Markdown structure of the personal knowledge base.

The script intentionally depends only on the Python standard library so it can run
locally and in GitHub Actions without environment setup.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".trash", ".venv", "__pycache__"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
LIST_ITEM_RE = re.compile(r"^\s+-\s+(.*)$")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

PropertyValue: TypeAlias = str | list[str]

KNOWLEDGE_REQUIRED = {"type", "domain", "maturity", "created", "updated"}
SOURCE_REQUIRED = {"type", "source_type", "status", "created", "updated"}
VALID_MATURITY = {"seed", "outline", "draft", "stable", "evergreen"}
VALID_VERIFICATION = {
    "source-checked",
    "derived",
    "experiment-reproduced",
    "production-validated",
}
VALID_LIFECYCLE = {"active", "needs-update", "deprecated", "archived"}


@dataclass(frozen=True)
class Finding:
    level: str
    path: Path
    message: str


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, PropertyValue], str | None]:
    if not text.startswith("---\n") and text != "---":
        return {}, None

    lines = text.splitlines()
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return {}, "Frontmatter 未闭合"

    data: dict[str, PropertyValue] = {}
    index = 1
    while index < closing:
        line = lines[index]
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            index += 1
            continue

        key = match.group(1)
        raw_value = (match.group(2) or "").strip()
        if raw_value == "[]":
            data[key] = []
            index += 1
            continue
        if raw_value:
            data[key] = unquote(raw_value)
            index += 1
            continue

        items: list[str] = []
        cursor = index + 1
        while cursor < closing:
            item_match = LIST_ITEM_RE.match(lines[cursor])
            if not item_match:
                break
            items.append(unquote(item_match.group(1)))
            cursor += 1
        data[key] = items if items else ""
        index = cursor

    return data, None


def scalar(props: dict[str, PropertyValue], key: str) -> str:
    value = props.get(key, "")
    return value if isinstance(value, str) else ""


def formal_knowledge(path: Path) -> bool:
    rel = relative(path)
    return rel.startswith("30 知识/") and not path.name.startswith("README")


def formal_source(path: Path) -> bool:
    rel = relative(path)
    return rel.startswith("40 来源/") and path.name != "README.md"


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def normalize_link(raw: str) -> str:
    target = raw.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    target = target.split("^", 1)[0].strip()
    target = target.replace("\\", "/")
    if target.endswith(".md"):
        target = target[:-3]
    return target.strip("/")


def build_link_indexes(files: list[Path]) -> tuple[set[str], dict[str, list[str]]]:
    exact: set[str] = set()
    by_name: dict[str, list[str]] = defaultdict(list)
    for path in files:
        rel = relative(path)
        without_ext = rel[:-3]
        exact.add(without_ext)
        by_name[path.stem].append(without_ext)
    return exact, by_name


def resolve_link(
    source: Path,
    target: str,
    exact: set[str],
    by_name: dict[str, list[str]],
) -> tuple[bool, str | None]:
    if not target:
        return True, None
    if target in exact:
        return True, None

    source_relative_parent = source.relative_to(ROOT).parent
    local_candidate = (source_relative_parent / target).as_posix()
    if local_candidate in exact:
        return True, None

    name = Path(target).name
    matches = by_name.get(name, [])
    if len(matches) == 1:
        return True, None
    if len(matches) > 1:
        return False, f"链接目标存在歧义：{target} -> {', '.join(matches)}"
    return False, f"失效链接：{target}"


def validate_verification(
    path: Path,
    props: dict[str, PropertyValue],
    findings: list[Finding],
) -> None:
    if "verification" not in props:
        return

    verification = props["verification"]
    if not isinstance(verification, list):
        findings.append(
            Finding(
                "ERROR",
                path,
                "verification 必须使用 YAML 列表；未验证请使用 [] 或省略字段",
            )
        )
        return

    if len(verification) != len(set(verification)):
        findings.append(Finding("ERROR", path, "verification 包含重复证据"))

    invalid = sorted(set(verification) - VALID_VERIFICATION)
    if invalid:
        findings.append(
            Finding("ERROR", path, f"非法 verification 证据：{', '.join(invalid)}")
        )


def validate() -> list[Finding]:
    findings: list[Finding] = []
    files = markdown_files()
    exact, by_name = build_link_indexes(files)
    ids: dict[str, list[Path]] = defaultdict(list)

    for path in files:
        text = path.read_text(encoding="utf-8")
        props, frontmatter_error = parse_frontmatter(text)

        if frontmatter_error:
            findings.append(Finding("ERROR", path, frontmatter_error))
            continue

        required: set[str] = set()
        if formal_knowledge(path):
            required = KNOWLEDGE_REQUIRED
        elif formal_source(path):
            required = SOURCE_REQUIRED

        if required and not props:
            findings.append(Finding("ERROR", path, "正式笔记缺少 Frontmatter"))
        else:
            missing = sorted(key for key in required if not props.get(key))
            if missing:
                findings.append(
                    Finding("ERROR", path, f"缺少必填属性：{', '.join(missing)}")
                )

        note_id = scalar(props, "id")
        if note_id:
            ids[note_id].append(path)

        maturity = scalar(props, "maturity")
        if maturity and maturity not in VALID_MATURITY:
            findings.append(Finding("ERROR", path, f"非法 maturity：{maturity}"))

        validate_verification(path, props, findings)

        lifecycle = scalar(props, "lifecycle")
        if lifecycle and lifecycle not in VALID_LIFECYCLE:
            findings.append(Finding("ERROR", path, f"非法 lifecycle：{lifecycle}"))

        body_without_code = strip_fenced_code(text)
        for raw_link in WIKILINK_RE.findall(body_without_code):
            target = normalize_link(raw_link)
            valid, message = resolve_link(path, target, exact, by_name)
            if not valid and message:
                findings.append(Finding("ERROR", path, message))

        if formal_knowledge(path) and len(text.strip()) < 180:
            findings.append(Finding("WARNING", path, "正式知识文章内容过短，请确认不是空壳"))

    for note_id, paths in ids.items():
        if len(paths) > 1:
            joined = ", ".join(relative(path) for path in paths)
            findings.append(Finding("ERROR", paths[0], f"重复 id {note_id}：{joined}"))

    return findings


def main() -> int:
    findings = validate()
    for finding in findings:
        print(f"{finding.level}: {relative(finding.path)}: {finding.message}")

    errors = sum(f.level == "ERROR" for f in findings)
    warnings = sum(f.level == "WARNING" for f in findings)
    print(f"\nValidation complete: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
'''

FRONTMATTER_RULES = '''# Frontmatter 规范

## 目标

Properties 用于表达机器可查询的结构化信息和动态状态，不重复正文中的知识关系。

## 通用字段

| 字段 | 说明 | 规则 |
|---|---|---|
| `type` | 笔记类型 | 正式笔记必填 |
| `created` | 创建日期 | `YYYY-MM-DD` |
| `updated` | 最近重要修改日期 | 内容发生实质变化时更新 |
| `id` | Manifest 主题 ID | 已登记的核心知识文章必填 |
| `aliases` | 常用别名 | 按需使用 |
| `legacy_id` | 旧知识库 ID | 迁移文章按需使用 |

## 知识文章字段

```yaml
---
id: MATH-LA-001
type: theory
domain: mathematics
maturity: draft
verification:
  - source-checked
  - derived
lifecycle: active
sources:
  - "[[Steven J. Gortler - Foundations of 3D Computer Graphics]]"
created: 2026-08-04
updated: 2026-08-04
---
```

### `type`

允许的核心类型：

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
dashboard
system-design
```

### `domain`

当前领域标识：

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

### `verification`

`verification` 是可多选的证据列表，不是单选成熟度，也不存在“最高验证状态”。允许值：

```text
source-checked
 derived
experiment-reproduced
production-validated
```

实际 YAML 不应包含上面代码块中的额外缩进；标准写法：

```yaml
verification:
  - source-checked
  - derived
  - experiment-reproduced
```

尚无证据时使用：

```yaml
verification: []
```

也可以省略该字段。不得把 `unverified` 与其他证据并列，因为“未验证”是空证据状态，不是一种正向证据。

具体来源、推导章节、实验文章或生产记录应在正文的“验证证据”部分链接，不只依赖属性标签。

### `lifecycle`

```text
active
needs-update
deprecated
archived
```

## 项目字段

```yaml
---
type: project
status: active
area:
  - "[[职业与技术能力]]"
created: 2026-08-04
due:
---
```

项目状态：`planned`、`active`、`waiting`、`paused`、`completed`、`cancelled`。

## 来源字段

```yaml
---
type: source-note
source_type: book
status: reading
authority: authoritative-secondary
created: 2026-08-04
updated: 2026-08-04
---
```

来源状态：`unread`、`reading`、`processed`、`reference`、`abandoned`。

## 按需字段

```text
module
contexts
prerequisites
platforms
apis
versions
version_sensitive
project
superseded_by
```

## 禁止事项

- 不维护与正文重复的庞大 `related` 列表；
- 不把 A/B/C 写成文章的全局绝对优先级；
- 不用标签重复表达目录和知识领域；
- 不把成熟度、生命周期和验证证据混成一条状态链；
- 不把 `verification` 写成单值；
- 不为每篇笔记强制填写所有可选字段。
'''

MATURITY_RULES = '''# 成熟度与验证规则

## 内容成熟度

| 状态 | 含义 |
|---|---|
| seed | 只有问题、线索或想法 |
| outline | 已形成文章结构 |
| draft | 已有主体内容，但仍需补全 |
| stable | 结构和结论相对稳定 |
| evergreen | 经长期使用、多次修订和复核 |

## 验证证据

验证是可累积的多证据集合，而不是单选等级。

| 证据 | 含义 |
|---|---|
| source-checked | 已核对与声明类型匹配的可靠来源 |
| derived | 已完成公式、逻辑或机制推导 |
| experiment-reproduced | 已通过可复现实验验证 |
| production-validated | 已在明确版本和环境的实际工程中验证 |

尚无证据时，`verification` 使用空列表或省略：

```yaml
verification: []
```

一篇文章可以同时具有多种证据：

```yaml
maturity: stable
verification:
  - source-checked
  - derived
  - experiment-reproduced
lifecycle: active
```

属性只表达证据种类。正文还应链接具体来源、推导、实验或生产记录。

## 生命周期

| 状态 | 含义 |
|---|---|
| active | 当前有效 |
| needs-update | 内容需要更新 |
| deprecated | 已过时但保留历史链接 |
| archived | 不再参与日常维护 |

## 三个维度的关系

- `maturity`：文章内容建设到了什么程度；
- `verification`：目前具备哪些证据；
- `lifecycle`：文章当前是否仍有效和参与维护。

成熟度和生命周期是单值，验证证据是列表，三者互不替代。
'''

ADR_CONTENT = '''---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0006：verification 使用多证据列表

## 背景

原模型把 `verification` 设计成单值：

```yaml
verification: experiment-reproduced
```

但同一篇文章可以同时核对来源、完成推导、通过实验，并在生产环境中验证。它们是可累积、互不排斥的证据类型，不是一条只能保留最高值的线性状态。

## 决策

`verification` 改为 YAML 列表：

```yaml
verification:
  - source-checked
  - derived
  - experiment-reproduced
```

允许证据：

- `source-checked`；
- `derived`；
- `experiment-reproduced`；
- `production-validated`。

尚无证据时使用 `verification: []` 或省略字段。`unverified` 不再作为证据值。

`maturity` 和 `lifecycle` 继续使用单值。

## 证据明细

Frontmatter 只表达证据种类。具体依据必须在正文中链接：

- 核对的来源；
- 推导所在章节；
- 可执行实验；
- 生产项目、版本和环境记录。

## 影响

- 现有试点文章迁移为证据列表；
- 模板默认使用空列表，不预先声称已经验证；
- 校验脚本拒绝标量 `verification` 和非法证据；
- Manifest 中的实验验证字段同步使用列表；
- 查询“待验证”时检查该属性为空或不存在。

## 关联文档

- [[80 系统/10 治理规则/Frontmatter规范|Frontmatter 规范]]
- [[80 系统/10 治理规则/成熟度与验证规则|成熟度与验证规则]]
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


def verification_lines(values: list[str]) -> list[str]:
    if not values:
        return ["verification: []"]
    return ["verification:", *(f"  - {value}" for value in values)]


def set_frontmatter_verification(path: str, values: list[str]) -> None:
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

    index = next(
        (i for i in range(1, closing) if lines[i].startswith("verification:")),
        None,
    )
    if index is None:
        insert_at = next(
            (i for i in range(1, closing) if lines[i].startswith("lifecycle:")),
            closing,
        )
        lines[insert_at:insert_at] = verification_lines(values)
    else:
        end = index + 1
        while end < closing and re.match(r"^\s+-\s+", lines[end]):
            end += 1
        lines[index:end] = verification_lines(values)

    write(path, "\n".join(lines) + "\n")


def replace_exact(path: str, old: str, new: str, *, count: int | None = None) -> None:
    text = read(path)
    occurrences = text.count(old)
    if occurrences == 0:
        raise RuntimeError(f"Expected text not found in {path}: {old[:80]!r}")
    if count is not None and occurrences != count:
        raise RuntimeError(
            f"Unexpected occurrence count in {path}: expected {count}, got {occurrences}"
        )
    write(path, text.replace(old, new))


def update_manifest() -> None:
    path = "80 系统/30 Manifest/试点建设清单.yaml"
    text = read(path)
    pattern = re.compile(
        r"(?P<prefix>  - id: GFX-EXP-[\s\S]*?    status: stable\n)"
        r"    verification: experiment-reproduced\n"
    )
    updated, count = pattern.subn(
        lambda match: match.group("prefix")
        + "    verification:\n"
        + "      - source-checked\n"
        + "      - experiment-reproduced\n",
        text,
    )
    if count != 3:
        raise RuntimeError(f"Expected three Manifest experiment migrations, got {count}")
    write(path, updated)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    replacements = {
        "version: 3.2": "version: 3.3",
        "# 个人知识库总体设计方案 v3.2": "# 个人知识库总体设计方案 v3.3",
        "verification: derived": "verification:\n  - source-checked\n  - derived",
        "### 验证状态\n\n```text\nunverified\nsource-checked\nderived\nexperiment-reproduced\nproduction-validated\n```": "### 验证证据\n\n```yaml\nverification:\n  - source-checked\n  - derived\n  - experiment-reproduced\n```\n\n验证证据为可多选列表；空列表或缺少字段表示尚无验证证据。",
        "三个维度独立维护。": "成熟度和生命周期为单值；验证证据为可多选列表，三个维度独立维护。",
        "11. 成熟度、验证和生命周期独立；": "11. 成熟度、验证证据和生命周期独立；",
    }
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"Design replacement missing: {old!r}")
        text = text.replace(old, new, 1)
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.1", "version: 1.2", 1)
    text = text.replace(
        "但在验证模型、证据规则和领域边界冻结前，不进入 Phase 2。",
        "但在证据规则和领域边界冻结前，不进入 Phase 2。",
        1,
    )

    pattern = re.compile(
        r"# 3\. 待决策阻断项\n\n## F-03：验证状态不应是单选线性枚举"
        r"[\s\S]*?### 状态\n\n`decision-required`\n\n---\n\n## F-04："
    )
    replacement = '''# 3. 新增已解决决策

## F-03：verification 使用多证据列表

### 决策

`verification` 改为可累积的 YAML 列表：

```yaml
verification:
  - source-checked
  - derived
  - experiment-reproduced
```

尚无证据时使用 `verification: []` 或省略字段。`unverified` 不再作为证据值。成熟度和生命周期继续使用单值。

Frontmatter 只记录证据类型；正文需要链接具体来源、推导、实验或生产记录。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0006-verification使用多证据列表|ADR-0006：verification 使用多证据列表]]。

---

# 4. 待决策阻断项

## F-04：'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-03 review block")

    heading_replacements = {
        "# 4. 重要优化项": "# 5. 重要优化项",
        "# 5. 已通过项": "# 6. 已通过项",
        "# 6. PR 和阶段建议": "# 7. PR 和阶段建议",
        "# 7. Gate A 决策清单": "# 8. Gate A 决策清单",
    }
    for old, new in heading_replacements.items():
        text = text.replace(old, new, 1)

    text = text.replace(
        "16. Area 与 Domain 的术语分离。",
        "16. Area 与 Domain 的术语分离；\n17. verification 使用多证据列表。",
        1,
    )
    text = text.replace(
        "- [ ] 确定 verification 使用列表模型；",
        "- [x] verification 已改为多证据列表，并通过 ADR-0006 固化；",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    text = text.replace(
        "- [ ] verification 是否改为多证据列表？",
        "- [x] verification 已改为多证据列表；",
        1,
    )
    adr_line = "- [[80 系统/60 ADR/ADR-0005-责任领域命名|ADR-0005：责任领域命名]]"
    if "ADR-0006-verification使用多证据列表" not in text:
        text = text.replace(
            adr_line,
            adr_line
            + "\n- [[80 系统/60 ADR/ADR-0006-verification使用多证据列表|ADR-0006：多证据验证模型]]",
            1,
        )
    write(path, text)


def update_dashboard() -> None:
    path = "80 系统/02 导航与仪表盘/系统仪表盘.md"
    replace_exact(
        path,
        "- `verification = unverified`：待验证文章；",
        "- `verification` 为空或不存在：待验证文章；",
        count=1,
    )


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace(
        "- 个人知识库总体设计方案 v3.1；",
        "- 个人知识库总体设计方案 v3.3；",
        1,
    )
    marker = "- Phase 0～8 分阶段实施路线图和阶段门禁。"
    if "ADR-0006" not in text:
        text = text.replace(
            marker,
            marker + "\n- ADR-0006：verification 使用多证据列表。",
            1,
        )
    changed_marker = "- 在设计确认前暂停扩展光栅化、PBR、API 和其他领域。"
    if "验证模型已从单值改为多证据列表" not in text:
        text = text.replace(
            changed_marker,
            changed_marker + "\n- 验证模型已从单值改为多证据列表，并同步现有试点文章、模板、Manifest 和校验脚本。",
            1,
        )
    write(path, text)


def update_readme() -> None:
    replace_exact(
        "README.md",
        "7. 内容成熟度、验证状态和生命周期分别管理。",
        "7. 内容成熟度、验证证据和生命周期分别管理。",
        count=1,
    )


def main() -> None:
    for path, evidence in ARTICLE_EVIDENCE.items():
        set_frontmatter_verification(path, evidence)

    for path in TEMPLATE_PATHS:
        set_frontmatter_verification(path, [])

    update_manifest()
    write("scripts/validate_kb.py", VALIDATOR_CONTENT)
    write("80 系统/10 治理规则/Frontmatter规范.md", FRONTMATTER_RULES)
    write("80 系统/10 治理规则/成熟度与验证规则.md", MATURITY_RULES)
    write(
        "80 系统/60 ADR/ADR-0006-verification使用多证据列表.md",
        ADR_CONTENT,
    )
    update_design()
    update_review()
    update_home()
    update_dashboard()
    update_changelog()
    update_readme()
    print("Verification evidence migration complete.")


if __name__ == "__main__":
    main()
