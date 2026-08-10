#!/usr/bin/env python3
"""Check public-repository assets for obvious policy violations.

This is a conservative technical check, not a copyright or privacy determination.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".trash"}
FORBIDDEN_EXTENSIONS = {
    ".epub",
    ".mobi",
    ".azw",
    ".azw3",
    ".kfx",
}
MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".tif", ".tiff", ".heic"}
ASSET_LIMIT = 5 * 1024 * 1024
FILE_LIMIT = 10 * 1024 * 1024


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        rel = relative(path)
        suffix = path.suffix.lower()
        size = path.stat().st_size

        if suffix in FORBIDDEN_EXTENSIONS:
            errors.append(f"禁止提交电子书原始文件：{rel}")
        if size > FILE_LIMIT:
            errors.append(f"文件超过 10 MiB：{rel} ({size / 1024 / 1024:.2f} MiB)")
        if rel.startswith("_assets/") and size > ASSET_LIMIT:
            errors.append(f"附件超过 5 MiB：{rel} ({size / 1024 / 1024:.2f} MiB)")
        if suffix in MEDIA_EXTENSIONS:
            try:
                header = path.read_bytes()[:256 * 1024]
            except OSError as exc:
                errors.append(f"无法读取媒体文件：{rel}: {exc}")
                continue
            if b"Exif" in header or b"GPS" in header:
                warnings.append(f"媒体可能包含 EXIF/GPS 元数据，请人工检查：{rel}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    print(f"Public asset check: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
