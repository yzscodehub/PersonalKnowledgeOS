#!/usr/bin/env python3
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
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){1,3}-\d{3}$")

PropertyValue: TypeAlias = str | list[str]

CANONICAL_KNOWLEDGE_REQUIRED = {"id", "type", "domain", "maturity", "lifecycle"}
MAP_REQUIRED = {"type", "map_kind", "domain", "maturity", "lifecycle"}
SOURCE_REQUIRED = {"type", "source_type", "status"}
CANONICAL_KNOWLEDGE_TYPES = {
    "concept",
    "theory",
    "algorithm",
    "system",
    "implementation",
    "api-reference",
    "experiment",
    "troubleshooting",
    "comparison",
}
VALID_DOMAINS = {
    "mathematics",
    "physics-engineering",
    "computer-science",
    "graphics",
    "artificial-intelligence",
    "software-engineering",
    "systems-platforms",
    "game-engine",
    "multimedia",
    "embedded-robotics-autonomous-driving",
    "design-content",
    "product-business-career",
    "humanities-social-sciences",
    "knowledge-system",
}
VALID_MATURITY = {"seed", "outline", "draft", "stable", "evergreen"}
VALID_VERIFICATION = {
    "source-checked",
    "derived",
    "experiment-reproduced",
    "production-validated",
}
VALID_LIFECYCLE = {"active", "needs-update", "deprecated", "archived"}
VALID_MAP_KIND = {"moc", "learning-route", "index", "dashboard"}
LIST_FIELDS = {
    "aliases",
    "verification",
    "sources",
    "platforms",
    "apis",
    "versions",
    "legacy_ids",
    "superseded_by",
    "prerequisites",
    "contexts",
    "project",
    "area",
}


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


def values(props: dict[str, PropertyValue], key: str) -> list[str]:
    value = props.get(key, [])
    return value if isinstance(value, list) else []


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


def validate_list_fields(
    path: Path,
    props: dict[str, PropertyValue],
    findings: list[Finding],
) -> None:
    for key in sorted(LIST_FIELDS):
        if key not in props:
            continue
        value = props[key]
        if not isinstance(value, list):
            findings.append(Finding("ERROR", path, f"{key} 必须使用 YAML 列表"))
            continue
        if len(value) != len(set(value)):
            findings.append(Finding("ERROR", path, f"{key} 包含重复值"))


def validate_verification(
    path: Path,
    props: dict[str, PropertyValue],
    findings: list[Finding],
) -> None:
    if "verification" not in props:
        return

    verification = props["verification"]
    if not isinstance(verification, list):
        return

    invalid = sorted(set(verification) - VALID_VERIFICATION)
    if invalid:
        findings.append(
            Finding("ERROR", path, f"非法 verification 证据：{', '.join(invalid)}")
        )


def validate_knowledge_object(
    path: Path,
    text: str,
    props: dict[str, PropertyValue],
    findings: list[Finding],
) -> None:
    note_type = scalar(props, "type")
    if note_type == "map":
        return

    if note_type not in CANONICAL_KNOWLEDGE_TYPES:
        findings.append(Finding("ERROR", path, f"非法正式知识 type：{note_type or '<empty>'}"))
        return

    note_id = scalar(props, "id")
    if note_id and not ID_RE.match(note_id):
        findings.append(Finding("ERROR", path, f"非法 id 格式：{note_id}"))

    domain = scalar(props, "domain")
    if domain and domain not in VALID_DOMAINS:
        findings.append(Finding("ERROR", path, f"非法 domain：{domain}"))

    if "legacy_id" in props:
        findings.append(
            Finding("WARNING", path, "legacy_id 为旧字段，请迁移为 legacy_ids 列表")
        )

    lifecycle = scalar(props, "lifecycle")
    if lifecycle == "deprecated" and not values(props, "superseded_by"):
        findings.append(
            Finding(
                "WARNING",
                path,
                "deprecated 文章没有 superseded_by；请确认正文说明了弃用原因和历史适用范围",
            )
        )
    if lifecycle == "archived":
        findings.append(
            Finding(
                "WARNING",
                path,
                "正式知识很少直接使用 archived；请确认是否应移动到 90 档案/30 知识历史",
            )
        )

    if note_type == "api-reference":
        if scalar(props, "version_sensitive").lower() != "true":
            findings.append(
                Finding("ERROR", path, "api-reference 必须设置 version_sensitive: true")
            )

    maturity = scalar(props, "maturity")
    if note_type == "experiment" and maturity in {"stable", "evergreen"}:
        if "experiment-reproduced" not in values(props, "verification"):
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "stable/evergreen experiment 必须具有 experiment-reproduced 证据",
                )
            )

    aliases = values(props, "aliases")
    if aliases and path.stem in aliases:
        findings.append(Finding("WARNING", path, "aliases 不应重复当前文件名／标题"))

    if len(text.strip()) < 180:
        findings.append(Finding("WARNING", path, "正式知识文章内容过短，请确认不是空壳"))


def validate() -> list[Finding]:
    findings: list[Finding] = []
    files = markdown_files()
    exact, by_name = build_link_indexes(files)
    ids: dict[str, list[Path]] = defaultdict(list)
    legacy_ids: dict[str, list[Path]] = defaultdict(list)

    for path in files:
        text = path.read_text(encoding="utf-8")
        props, frontmatter_error = parse_frontmatter(text)

        if frontmatter_error:
            findings.append(Finding("ERROR", path, frontmatter_error))
            continue

        required: set[str] = set()
        note_type = scalar(props, "type")
        if formal_knowledge(path):
            required = MAP_REQUIRED if note_type == "map" else CANONICAL_KNOWLEDGE_REQUIRED
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

        validate_list_fields(path, props, findings)

        note_id = scalar(props, "id")
        if note_id:
            ids[note_id].append(path)
        for legacy_id in values(props, "legacy_ids"):
            legacy_ids[legacy_id].append(path)

        maturity = scalar(props, "maturity")
        if maturity and maturity not in VALID_MATURITY:
            findings.append(Finding("ERROR", path, f"非法 maturity：{maturity}"))

        validate_verification(path, props, findings)

        maturity_rank = {"seed": 0, "outline": 1, "draft": 2, "stable": 3, "evergreen": 4}
        if formal_knowledge(path) and note_type in CANONICAL_KNOWLEDGE_TYPES:
            if maturity_rank.get(maturity, 0) >= maturity_rank["draft"]:
                has_sources = bool(values(props, "sources"))
                evidence = set(values(props, "verification"))
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
            if date_value and date_value != "{{date}}" and not DATE_RE.match(date_value):
                findings.append(Finding("ERROR", path, f"非法 {date_key} 日期：{date_value}"))

        lifecycle = scalar(props, "lifecycle")
        if lifecycle and lifecycle not in VALID_LIFECYCLE:
            findings.append(Finding("ERROR", path, f"非法 lifecycle：{lifecycle}"))

        map_kind = scalar(props, "map_kind")
        if note_type == "map":
            if not map_kind:
                findings.append(Finding("ERROR", path, "type: map 缺少 map_kind"))
            elif map_kind not in VALID_MAP_KIND:
                findings.append(Finding("ERROR", path, f"非法 map_kind：{map_kind}"))
        elif map_kind:
            findings.append(Finding("ERROR", path, "只有 type: map 可以使用 map_kind"))

        if formal_knowledge(path):
            validate_knowledge_object(path, text, props, findings)

        body_without_code = strip_fenced_code(text)
        for raw_link in WIKILINK_RE.findall(body_without_code):
            target = normalize_link(raw_link)
            valid, message = resolve_link(path, target, exact, by_name)
            if not valid and message:
                findings.append(Finding("ERROR", path, message))

    for note_id, paths in ids.items():
        if len(paths) > 1:
            joined = ", ".join(relative(path) for path in paths)
            findings.append(Finding("ERROR", paths[0], f"重复 id {note_id}：{joined}"))

    for legacy_id, paths in legacy_ids.items():
        if len(paths) > 1:
            joined = ", ".join(relative(path) for path in paths)
            findings.append(
                Finding("ERROR", paths[0], f"重复 legacy_id {legacy_id}：{joined}")
            )

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
