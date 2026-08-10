#!/usr/bin/env python3
"""Validate the D3 end-to-end workflow registry using only stdlib."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "80 系统/30 Manifest/端到端工作流清单.yaml"
DESIGN = ROOT / "80 系统/13 D3 端到端工作流设计.md"
GOVERNANCE = ROOT / "80 系统/10 治理规则/端到端工作流与回流规则.md"
ADR = ROOT / "80 系统/60 ADR/ADR-0017-端到端工作流与回流规则.md"

EXPECTED_IDS = {f"WF-{index:03d}" for index in range(1, 11)}
REQUIRED_FIELDS = {
    "id",
    "title",
    "primary_object",
    "trigger",
    "inputs",
    "states",
    "outputs",
    "exceptions",
    "automation",
    "exit_condition",
    "design_section",
}
SCALAR_RE = re.compile(r"^    ([a-z_]+):\s*(.+?)\s*$")
LIST_KEY_RE = re.compile(r"^    ([a-z_]+):\s*$")
ENTRY_RE = re.compile(r"^  - id:\s*(WF-\d{3})\s*$")
LIST_ITEM_RE = re.compile(r"^      -\s+(.+?)\s*$")


def parse_registry() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    list_key: str | None = None

    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        entry = ENTRY_RE.match(line)
        if entry:
            current = {"id": entry.group(1)}
            entries.append(current)
            list_key = None
            continue
        if current is None:
            continue

        scalar = SCALAR_RE.match(line)
        if scalar:
            key, value = scalar.groups()
            current[key] = value.strip().strip('"')
            list_key = None
            continue

        key_match = LIST_KEY_RE.match(line)
        if key_match:
            list_key = key_match.group(1)
            current[list_key] = []
            continue

        item = LIST_ITEM_RE.match(line)
        if item and list_key:
            value = current.get(list_key)
            if isinstance(value, list):
                value.append(item.group(1).strip().strip('"'))

    return entries


def main() -> int:
    errors: list[str] = []

    for path in (REGISTRY, DESIGN, GOVERNANCE, ADR):
        if not path.exists():
            errors.append(f"缺少 D3 文件：{path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    entries = parse_registry()
    ids = [str(entry.get("id", "")) for entry in entries]

    if len(entries) != 10:
        errors.append(f"工作流数量应为 10，实际为 {len(entries)}")
    if len(ids) != len(set(ids)):
        errors.append("工作流 ID 重复")
    if set(ids) != EXPECTED_IDS:
        missing = sorted(EXPECTED_IDS - set(ids))
        extra = sorted(set(ids) - EXPECTED_IDS)
        errors.append(f"工作流 ID 集合不完整；缺少={missing}，多余={extra}")

    design_text = DESIGN.read_text(encoding="utf-8")
    governance_text = GOVERNANCE.read_text(encoding="utf-8")
    adr_text = ADR.read_text(encoding="utf-8")

    for entry in entries:
        workflow_id = str(entry.get("id", "<unknown>"))
        missing_fields = sorted(REQUIRED_FIELDS - set(entry))
        if missing_fields:
            errors.append(f"{workflow_id} 缺少字段：{', '.join(missing_fields)}")

        for key in ("inputs", "states", "outputs", "exceptions", "automation"):
            value = entry.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"{workflow_id} 的 {key} 必须是非空列表")

        for key in ("title", "primary_object", "trigger", "exit_condition", "design_section"):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{workflow_id} 的 {key} 必须是非空标量")

        if workflow_id not in design_text:
            errors.append(f"D3 设计文档缺少 {workflow_id}")
        if workflow_id not in governance_text:
            errors.append(f"治理规则缺少 {workflow_id}")
        if workflow_id not in adr_text:
            errors.append(f"ADR-0017 缺少 {workflow_id}")

    required_design_terms = [
        "触发条件",
        "输入",
        "执行步骤",
        "状态变化",
        "产物",
        "异常与停止条件",
        "自动化点",
        "退出条件",
    ]
    for term in required_design_terms:
        if term not in design_text:
            errors.append(f"D3 设计文档缺少结构术语：{term}")

    for error in errors:
        print(f"ERROR: {error}")
    print(f"Workflow registry check: {len(errors)} error(s), {len(entries)} workflow(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
