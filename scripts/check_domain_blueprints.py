#!/usr/bin/env python3
"""Validate the D4 knowledge-domain blueprint registry and documents.

The validator uses only the Python standard library. It intentionally parses the
small, controlled registry schema instead of depending on a YAML package.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "80 系统/30 Manifest/知识领域蓝图清单.yaml"
BLUEPRINT_DIR = ROOT / "80 系统/50 领域蓝图"

EXPECTED_IDS = {f"{value:02d}" for value in range(1, 14)} | {"99"}
REQUIRED_FIELDS = {"id", "slug", "title", "blueprint_path", "wave", "modules"}
REQUIRED_SECTIONS = [
    "## 1. 领域目标",
    "## 2. 主归属边界",
    "## 3. 一级模块",
    "## 4. 核心基础",
    "## 5. 典型应用",
    "## 6. 来源与证据",
    "## 7. 实验与实践",
    "## 8. 核心 MOC",
    "## 9. 跨领域关系",
    "## 10. 首批建设建议",
    "## 11. 非目标",
]
ENTRY_RE = re.compile(r'^  - id:\s*"?([^"\s]+)"?\s*$')
SCALAR_RE = re.compile(r"^    ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^      -\s+(.+)$")
FM_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
MODULE_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_registry() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    list_key: str | None = None

    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        entry_match = ENTRY_RE.match(line)
        if entry_match:
            current = {"id": entry_match.group(1)}
            entries.append(current)
            list_key = None
            continue
        if current is None:
            continue

        scalar_match = SCALAR_RE.match(line)
        if scalar_match:
            key, raw = scalar_match.groups()
            value = unquote(raw)
            if value:
                current[key] = value
                list_key = None
            else:
                current[key] = []
                list_key = key
            continue

        item_match = LIST_ITEM_RE.match(line)
        if item_match and list_key:
            current[list_key].append(unquote(item_match.group(1)))

    return entries


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        return {}
    result: dict[str, str] = {}
    for line in lines[1:closing]:
        match = FM_RE.match(line)
        if match:
            result[match.group(1)] = unquote(match.group(2))
    return result


def main() -> int:
    errors: list[str] = []

    if not REGISTRY.exists():
        print(f"ERROR: registry not found: {REGISTRY.relative_to(ROOT)}")
        return 1

    entries = parse_registry()
    ids = [entry.get("id", "") for entry in entries]
    id_set = set(ids)

    if id_set != EXPECTED_IDS:
        missing = sorted(EXPECTED_IDS - id_set)
        extra = sorted(id_set - EXPECTED_IDS)
        if missing:
            errors.append(f"缺少领域 ID：{', '.join(missing)}")
        if extra:
            errors.append(f"未知领域 ID：{', '.join(extra)}")
    if len(ids) != len(id_set):
        errors.append("领域 ID 存在重复")

    all_modules: dict[str, str] = {}
    registered_paths: set[Path] = set()

    for entry in entries:
        domain_id = str(entry.get("id", ""))
        missing_fields = sorted(REQUIRED_FIELDS - entry.keys())
        if missing_fields:
            errors.append(f"{domain_id} 缺少字段：{', '.join(missing_fields)}")
            continue

        modules = entry.get("modules")
        if not isinstance(modules, list) or not modules:
            errors.append(f"{domain_id} modules 必须是非空列表")
            continue

        path = ROOT / str(entry["blueprint_path"])
        registered_paths.add(path.resolve())
        if not path.exists():
            errors.append(f"{domain_id} 蓝图文件不存在：{entry['blueprint_path']}")
            continue

        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        expected_frontmatter = {
            "type": "system-design",
            "status": "accepted",
            "scope": "domain-blueprint",
            "domain_id": domain_id,
            "domain": str(entry["slug"]),
        }
        for key, expected in expected_frontmatter.items():
            actual = frontmatter.get(key)
            if actual != expected:
                errors.append(
                    f"{domain_id} Frontmatter {key} 不一致：expected={expected!r}, actual={actual!r}"
                )

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{domain_id} 缺少章节：{section}")

        for module in modules:
            if not MODULE_RE.match(module):
                errors.append(f"{domain_id} 非法模块代码：{module}")
            owner = all_modules.get(module)
            if owner:
                errors.append(f"模块代码重复：{module} 同时属于 {owner} 和 {domain_id}")
            else:
                all_modules[module] = domain_id
            if module not in text:
                errors.append(f"{domain_id} 蓝图正文未声明模块：{module}")

    if BLUEPRINT_DIR.exists():
        actual_paths = {path.resolve() for path in BLUEPRINT_DIR.glob("*.md")}
        unregistered = sorted(actual_paths - registered_paths)
        if unregistered:
            errors.append(
                "存在未登记蓝图："
                + ", ".join(path.relative_to(ROOT).as_posix() for path in unregistered)
            )

    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Domain blueprint validation: {len(entries)} domain(s), "
        f"{len(all_modules)} module code(s), {len(errors)} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
