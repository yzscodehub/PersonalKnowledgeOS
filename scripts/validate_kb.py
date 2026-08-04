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

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".trash", ".venv", "__pycache__"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

KNOWLEDGE_REQUIRED = {"type", "domain", "maturity", "created", "updated"}
SOURCE_REQUIRED = {"type", "source_type", "status", "created", "updated"}
VALID_MATURITY = {"seed", "outline", "draft", "stable", "evergreen"}
VALID_VERIFICATION = {
    "unverified",
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


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
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

    data: dict[str, str] = {}
    for line in lines[1:closing]:
        if line.startswith((" ", "\t", "-")):
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if match:
            data[match.group(1)] = (match.group(2) or "").strip().strip('"\'')
    return data, None


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

        note_id = props.get("id")
        if note_id:
            ids[note_id].append(path)

        maturity = props.get("maturity")
        if maturity and maturity not in VALID_MATURITY:
            findings.append(Finding("ERROR", path, f"非法 maturity：{maturity}"))

        verification = props.get("verification")
        if verification and verification not in VALID_VERIFICATION:
            findings.append(Finding("ERROR", path, f"非法 verification：{verification}"))

        lifecycle = props.get("lifecycle")
        if lifecycle and lifecycle not in VALID_LIFECYCLE:
            findings.append(Finding("ERROR", path, f"非法 lifecycle：{lifecycle}"))

        body_without_code = strip_fenced_code(text)
        for raw_link in WIKILINK_RE.findall(body_without_code):
            target = normalize_link(raw_link)
            valid, message = resolve_link(path, target, exact, by_name)
            if not valid and message:
                findings.append(Finding("ERROR", path, message))

        if formal_knowledge(path):
            body = text.strip()
            if len(body) < 180:
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
