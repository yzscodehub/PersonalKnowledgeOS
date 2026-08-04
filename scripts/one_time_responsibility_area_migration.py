#!/usr/bin/env python3
"""One-time terminology migration from Area=领域 to Area=责任领域.

This script is intentionally narrow. It does not replace generic uses of
"领域" because those may correctly refer to knowledge domains.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json"}
EXCLUDED = {
    Path("80 系统/60 ADR/ADR-0005-责任领域命名.md"),
}


def replace_in_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if rel in EXCLUDED:
        return False

    original = path.read_text(encoding="utf-8")
    updated = original.replace("20 领域", "20 责任领域")

    if rel == Path("80 系统/01 知识库设计说明.md"):
        replacements = {
            "version: 3.1": "version: 3.2",
            "# 个人知识库总体设计方案 v3.1": "# 个人知识库总体设计方案 v3.2",
            "├── 领域\n": "├── 责任领域\n",
            "## 5.2 领域 Area": "## 5.2 责任领域 Area",
            "知识、项目或领域。": "知识、项目或责任领域。",
            "项目 / 领域 / 来源 / 知识 / 输出 / 日记 / 删除":
                "项目 / 责任领域 / 来源 / 知识 / 输出 / 日记 / 删除",
        }
        for old, new in replacements.items():
            updated = updated.replace(old, new)

        marker = "数学和图形学不属于这里，它们属于知识学科。"
        terminology = (
            marker
            + "\n\n统一术语：\n\n"
            + "```text\n"
            + "Area   = 责任领域\n"
            + "Domain = 知识领域\n"
            + "Module = 知识模块\n"
            + "Topic  = 知识主题\n"
            + "```"
        )
        if marker in updated and "Area   = 责任领域" not in updated:
            updated = updated.replace(marker, terminology, 1)

    if rel == Path("80 系统/03 总体设计评审记录.md"):
        pattern = re.compile(
            r"## F-02：.*?\n\n---\n\n## F-03：",
            re.DOTALL,
        )
        replacement = """## F-02：责任领域命名已确认

### 决策

顶层目录已从：

```text
20 领域
```

调整为：

```text
20 责任领域
```

统一术语：

- Area = 责任领域；
- Domain = 知识领域；
- Module = 知识模块；
- Topic = 知识主题。

该调整解决了 PARA 长期责任与数学、图形学、AI 等知识领域之间的中文语义冲突。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0005-责任领域命名|ADR-0005：责任领域命名]]。

---

## F-03："""
        updated, count = pattern.subn(replacement, updated, count=1)
        if count != 1:
            raise RuntimeError(f"Could not replace F-02 block in {rel}")
        updated = updated.replace(
            "- [ ] 确定是否将 `20 责任领域` 改为 `20 责任领域`；",
            "- [x] 顶层目录已改为 `20 责任领域`，并通过 ADR-0005 固化术语；",
        )
        updated = updated.replace(
            "- [ ] 确定是否将 `20 领域` 改为 `20 责任领域`；",
            "- [x] 顶层目录已改为 `20 责任领域`，并通过 ADR-0005 固化术语；",
        )

    if updated == original:
        return False

    path.write_text(updated, encoding="utf-8")
    print(rel.as_posix())
    return True


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        changed += replace_in_file(path)
    print(f"Changed {changed} file(s).")


if __name__ == "__main__":
    main()
