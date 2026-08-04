#!/usr/bin/env python3
"""Validate Phase 1 Manifest, source backlinks, and experiment paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "80 系统/30 Manifest/试点建设清单.yaml"
SOURCE_ROOT = ROOT / "40 来源"
FIELD_RE = re.compile(r"^    ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
ENTRY_RE = re.compile(r"^  - id:\s*(\S+)\s*$")
LIST_ITEM_RE = re.compile(r"^\s+-\s+(.*)$")
TOP_FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")


def parse_manifest() -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {"articles": [], "experiments": []}
    section: str | None = None
    current: dict[str, Any] | None = None
    current_list_key: str | None = None

    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if raw in {"articles:", "experiments:"}:
            section = raw[:-1]
            current = None
            current_list_key = None
            continue
        entry = ENTRY_RE.match(raw)
        if section and entry:
            current = {"id": entry.group(1)}
            result[section].append(current)
            current_list_key = None
            continue
        if current is None:
            continue
        field = FIELD_RE.match(raw)
        if field:
            key, value = field.groups()
            value = value.strip().strip('"')
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                current[key] = [part.strip() for part in inner.split(",") if part.strip()]
            elif value:
                current[key] = value
            else:
                current[key] = []
                current_list_key = key
            continue
        list_item = LIST_ITEM_RE.match(raw)
        if current_list_key and list_item:
            current[current_list_key].append(list_item.group(1).strip().strip('"'))

    return result


def parse_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        return {}
    data: dict[str, Any] = {}
    index = 1
    while index < closing:
        match = TOP_FIELD_RE.match(lines[index])
        if not match:
            index += 1
            continue
        key, raw = match.groups()
        raw = raw.strip().strip('"')
        if raw == "[]":
            data[key] = []
            index += 1
            continue
        if raw:
            data[key] = raw
            index += 1
            continue
        values: list[str] = []
        cursor = index + 1
        while cursor < closing:
            item = LIST_ITEM_RE.match(lines[cursor])
            if not item:
                break
            values.append(item.group(1).strip().strip('"'))
            cursor += 1
        data[key] = values
        index = cursor
    return data


def source_file(link: str) -> Path | None:
    name = link.strip().removeprefix("[[").removesuffix("]] ").removesuffix("]]" )
    name = name.split("|", 1)[0].split("/", 1)[-1]
    matches = list(SOURCE_ROOT.rglob(f"{name}.md"))
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    data = parse_manifest()
    errors: list[str] = []
    article_ids = {entry["id"] for entry in data["articles"]}

    for article in data["articles"]:
        for prerequisite in article.get("prerequisites", []):
            if prerequisite not in article_ids:
                errors.append(f"{article['id']} 引用了不存在的 prerequisite：{prerequisite}")

        status = article.get("status", "planned")
        if status == "planned":
            if article.get("path"):
                errors.append(f"planned 主题不应提前登记实体路径：{article['id']}")
            continue
        path_value = article.get("path")
        if not path_value:
            errors.append(f"{article['id']} 状态为 {status} 但缺少 path")
            continue
        path = ROOT / str(path_value)
        if not path.exists():
            errors.append(f"Manifest 路径不存在：{path_value}")
            continue
        props = parse_frontmatter(path)
        if props.get("id") != article["id"]:
            errors.append(f"ID 不一致：{article['id']} -> {props.get('id')} ({path_value})")
        if props.get("maturity") != status:
            errors.append(f"状态不一致：{article['id']} Manifest={status} note={props.get('maturity')}")

        verification = props.get("verification", [])
        sources = props.get("sources", [])
        if "source-checked" in verification:
            if not sources:
                errors.append(f"{article['id']} 标记 source-checked 但没有 sources")
            for source_link in sources:
                source = source_file(source_link)
                if source is None:
                    errors.append(f"{article['id']} 来源无法唯一解析：{source_link}")
                    continue
                target = str(path_value)[:-3]
                if target not in source.read_text(encoding="utf-8"):
                    errors.append(f"来源缺少反向链接：{source.relative_to(ROOT)} -> {target}")

    for experiment in data["experiments"]:
        article_path = ROOT / str(experiment.get("article_path", ""))
        code_path = ROOT / str(experiment.get("code_path", ""))
        if not article_path.exists():
            errors.append(f"实验文章不存在：{experiment.get('article_path')}")
            continue
        if not code_path.exists():
            errors.append(f"实验代码不存在：{experiment.get('code_path')}")
        props = parse_frontmatter(article_path)
        if props.get("id") != experiment["id"]:
            errors.append(f"实验 ID 不一致：{experiment['id']} -> {props.get('id')}")
        if props.get("maturity") != experiment.get("status"):
            errors.append(
                f"实验状态不一致：{experiment['id']} Manifest={experiment.get('status')} note={props.get('maturity')}"
            )

    for message in errors:
        print(f"ERROR: {message}")
    print(f"Pilot consistency: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
