#!/usr/bin/env python3
"""One-time Gate A migration for public attachments, copyright, and large files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POLICY = '''---
type: governance
status: active
created: 2026-08-04
updated: 2026-08-04
---

# 附件、版权与大文件规则

## 目标

本仓库当前公开。附件和来源材料必须同时满足：有权公开、体积可控、来源可追踪、不会泄露隐私或雇主信息。

## 默认原则

1. 仓库保存知识正文、个人重述、必要短引用和可公开的自制素材；
2. 不提交整本受版权保护的书籍、付费课程、盗版资料或无权再分发的文件；
3. 原始来源文件默认保存在合法的本地或外部存储，仓库只记录书目信息和定位；
4. `_assets` 只保存文章实际使用的图片、图表和小型媒体；
5. 大文件不是因为 Git 能保存就应该进入仓库；
6. 任何附件在提交前都要检查隐私、元数据、许可和体积。

## 可提交内容

- 自己绘制或生成的示意图、流程图和图表；
- 自己编写的代码和实验输出；
- 许可明确允许再分发的素材；
- 公有领域或开放许可资料的必要副本；
- 为评论、教学或分析所必需的短摘录，并附来源定位；
- 经过脱敏、裁剪且有公开权利的截图。

## 禁止内容

- 整本商业书籍、EPUB、MOBI、AZW 或扫描版图书；
- 付费课程视频、课件和题库；
- 未公开的公司代码、设计图、日志、数据、截图和文档；
- 身份、健康、财务、合同、聊天和账户相关附件；
- 密钥、Token、Cookie、环境文件和调试转储中的敏感信息；
- 来源不明或许可不明确的网络图片；
- 含有不必要 EXIF、GPS、用户名、路径或设备信息的媒体。

## 引用与重述

来源笔记以个人理解和重述为主：

- 直接引用只保留完成论证所需的最短片段；
- 记录作者、标题、版本、章节、页码或 URL 定位；
- 不通过拆分文件或多篇笔记规避对大段原文复制的限制；
- 图表需要说明是自制、改绘还是原图引用；
- 改绘仍需标注基础来源。

## `_assets` 规则

附件命名建议：

```text
<article-id>-<purpose>-<sequence>.<ext>
```

例如：

```text
GFX-PROJ-002-frustum-01.svg
GFX-DEPTH-001-precision-chart-01.png
```

提交前确认：

- 正文中确实引用；
- 文件名不含私人信息；
- 图片已去除不必要元数据；
- 分辨率和压缩合理；
- 许可和来源已记录；
- 没有功能等价的文本、SVG 或生成脚本可替代。

## 体积策略

默认阈值：

- 单个普通附件不超过 5 MiB；
- 单个仓库文件不超过 10 MiB；
- 超出阈值时优先压缩、转为生成脚本或使用外部存储；
- Git LFS 只有在确有长期版本管理需求并创建 ADR 后才启用；
- 原始视频、模型、数据集、书籍和大型 Frame Capture 默认不入库。

仓库使用：

```bash
python scripts/check_public_assets.py
```

检查禁止扩展名、超大文件和常见媒体元数据提示。该检查不能替代人工版权判断。

## 来源文件存储

来源笔记可以记录：

```text
合法获取位置
本地相对说明
外部书签或 DOI
版本和哈希
许可信息
```

不得在公开笔记中记录私人云盘令牌、带签名下载地址或本机绝对私人路径。

## 误提交处理

发现误提交后：

1. 立即停止继续传播；
2. 删除工作区副本并评估是否需要历史重写；
3. 凭据立即轮换；
4. 检查 Fork、Actions 日志、Release 和缓存；
5. 必要时联系权利人、平台或相关人员；
6. 记录事故、范围和防复发措施。

仅删除最新文件或把仓库改为私有，不能撤回已经公开的 Git 历史。

## 关联规则

- [[80 系统/10 治理规则/公开仓库与隐私规则|公开仓库与隐私规则]]
- [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]
- [[80 系统/60 ADR/ADR-0011-公开附件版权与大文件策略|ADR-0011：公开附件、版权与大文件策略]]
'''

CHECK_SCRIPT = r'''#!/usr/bin/env python3
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
'''

ADR = '''---
type: adr
status: accepted
decision_date: 2026-08-04
created: 2026-08-04
updated: 2026-08-04
---

# ADR-0011：公开附件、版权与大文件策略

## 背景

公开知识库可能接收书籍、截图、图表、视频、模型和实验输出。缺少规则会带来版权侵权、隐私泄露、仓库膨胀和 Git 历史难以清理等风险。

## 决策

- 仓库保存知识正文、个人重述和必要的小型公开素材；
- 整本商业书籍、付费课程和无权分发的原始资料不得提交；
- `_assets` 仅保存正文实际使用且有公开权利的附件；
- 普通附件默认不超过 5 MiB，任一文件默认不超过 10 MiB；
- 大型原始资料优先使用合法外部存储、生成脚本或压缩形式；
- Git LFS 需在明确长期需求后通过独立 ADR 启用；
- CI 运行 `scripts/check_public_assets.py` 检查明显违规，但人工仍需判断版权和隐私。

## 引用规则

直接引用保持必要最短范围，记录作者、标题、版本、章节和页码。自制、改绘和引用图表需要明确标注来源与权利状态。

## 影响

- 来源模板增加权利、定位和存储说明；
- CI 增加公共附件技术检查；
- 提交前检查增加元数据、许可和文件体积；
- 误提交时可能需要历史重写，不能只删除最新文件。

## 关联文档

- [[80 系统/10 治理规则/附件、版权与大文件规则|附件、版权与大文件规则]]
- [[80 系统/10 治理规则/公开仓库与隐私规则|公开仓库与隐私规则]]
- [[80 系统/03 总体设计评审记录|总体设计评审记录]]
'''

SOURCE_TEMPLATE = '''---
type: source-note
source_type:
status: unread
created: {{date}}
updated: {{date}}
---

# 作者 - 标题

## 书目信息与版本

## 阅读目的

## 可支持的声明类型

例如：数学理论、规范语义、研究算法、实现行为、性能观察、工程经验或历史背景。

## 核心主题

## 章节或内容地图

## 重要结论与定位

记录章节、页码、版本、提交、DOI 或其他可追踪位置。

## 限制、立场与适用范围

## 权利、许可与存储

- 版权或许可：
- 是否允许公开再分发：
- 合法来源位置：
- 原始文件是否入库：否／是（说明理由）

## 待验证问题

## 提炼出的正式知识

## 相关项目与输出

## 阅读进度
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


def update_privacy() -> None:
    path = "80 系统/10 治理规则/公开仓库与隐私规则.md"
    text = read(path)
    marker = "## 关联决策"
    note = "## 附件和版权\n\n公开附件、引用、书籍原始文件和大文件还必须遵守 [[80 系统/10 治理规则/附件、版权与大文件规则|附件、版权与大文件规则]]。\n\n"
    if note.strip() not in text:
        text = text.replace(marker, note + marker, 1)
    write(path, text)


def update_design() -> None:
    path = "80 系统/01 知识库设计说明.md"
    text = read(path)
    text = text.replace("version: 3.7", "version: 3.8", 1)
    text = text.replace("# 个人知识库总体设计方案 v3.7", "# 个人知识库总体设计方案 v3.8", 1)
    marker = "详细规则见 [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]。\n\n---"
    addition = '''详细规则见 [[80 系统/10 治理规则/链接与来源规则|链接与来源规则]]。

## 11.7 公开附件与版权

公开仓库只保存有权公开、正文实际使用且体积合理的素材。整本商业书籍、付费课程和无权再分发的原始资料不入库；来源笔记记录书目信息、定位、许可和合法存储位置。

默认普通附件不超过 5 MiB，任一文件不超过 10 MiB。大型视频、模型、数据集和 Frame Capture 优先使用外部存储或生成脚本。Git LFS 需要独立 ADR。

CI 运行 `python scripts/check_public_assets.py` 检查明显风险，人工仍需判断版权、隐私和许可。详细规则见 [[80 系统/10 治理规则/附件、版权与大文件规则|附件、版权与大文件规则]]。

---'''
    if marker not in text:
        raise RuntimeError("Design evidence ending marker not found")
    text = text.replace(marker, addition, 1)
    write(path, text)


def update_review() -> None:
    path = "80 系统/03 总体设计评审记录.md"
    text = read(path)
    text = text.replace("version: 1.6", "version: 1.7", 1)
    text = text.replace("个人知识库总体设计方案 v3.7", "个人知识库总体设计方案 v3.8", 1)
    pattern = re.compile(r"## F-08：公开仓库需要来源文件、附件和版权策略\n[\s\S]*?\n---\n\n## F-09：")
    replacement = '''## F-08：公开附件、版权与大文件策略已确认

### 决策

公开仓库只保存有权公开、正文实际使用且体积合理的附件；整本商业书籍、付费课程和无权分发的资料不得提交。默认附件阈值、外部存储、Git LFS 决策和误提交处理已经形成治理规则，并加入 CI 技术检查。

### 状态

`accepted`

关联决策：[[80 系统/60 ADR/ADR-0011-公开附件版权与大文件策略|ADR-0011：公开附件、版权与大文件策略]]。

---

## F-09：'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace F-08 block")
    text = text.replace(
        "21. 最小 Frontmatter 和日期自动化策略已冻结。",
        "21. 最小 Frontmatter 和日期自动化策略已冻结；\n22. 公开附件、版权与大文件策略已冻结。",
        1,
    )
    text = text.replace(
        "- [ ] 完善公开附件和版权策略；",
        "- [x] 公开附件、版权与大文件规则已通过 ADR-0011 固化；",
        1,
    )
    write(path, text)


def update_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    adr10 = "- [[80 系统/60 ADR/ADR-0010-最小Frontmatter与日期自动化|ADR-0010：最小元数据模型]]"
    if "ADR-0011-公开附件版权与大文件策略" not in text:
        text = text.replace(
            adr10,
            adr10 + "\n- [[80 系统/60 ADR/ADR-0011-公开附件版权与大文件策略|ADR-0011：公开附件策略]]",
            1,
        )
    marker = "- [x] 最小 Frontmatter 和日期自动化策略已确定；"
    if "公开附件、版权与大文件规则已确定" not in text:
        text = text.replace(marker, marker + "\n- [x] 公开附件、版权与大文件规则已确定；", 1)
    write(path, text)


def update_ci() -> None:
    path = ".github/workflows/validate-knowledge-base.yml"
    text = read(path)
    marker = "      - name: Run math and graphics experiments\n"
    check = "      - name: Check public assets\n        run: python scripts/check_public_assets.py\n\n"
    if check not in text:
        text = text.replace(marker, check + marker, 1)
    write(path, text)


def update_readmes() -> None:
    path = "40 来源/README.md"
    text = read(path)
    if "附件、版权与大文件规则" not in text:
        text += "\n## 原始文件与版权\n\n来源笔记不等于原始文件归档。整本商业书籍和无权再分发的资料不入库；许可、定位和存储方式见 [[80 系统/10 治理规则/附件、版权与大文件规则|附件、版权与大文件规则]]。\n"
    write(path, text)

    path = "README.md"
    text = read(path)
    marker = "- 详细规则见 [[80 系统/10 治理规则/公开仓库与隐私规则]]。"
    replacement = marker + "\n- 附件和来源文件还需遵守 [[80 系统/10 治理规则/附件、版权与大文件规则]]。"
    if "附件、版权与大文件规则" not in text:
        text = text.replace(marker, replacement, 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    text = text.replace("- 个人知识库总体设计方案 v3.7；", "- 个人知识库总体设计方案 v3.8；", 1)
    marker = "- ADR-0010：最小 Frontmatter 与日期自动化。"
    if "ADR-0011：公开附件" not in text:
        text = text.replace(marker, marker + "\n- ADR-0011：公开附件、版权与大文件策略。", 1)
    changed = "- 最小 Frontmatter 和暂存区日期同步策略已落地。"
    if "公共附件和大文件 CI 检查" not in text:
        text = text.replace(changed, changed + "\n- 公共附件和大文件 CI 检查已加入。", 1)
    write(path, text)


def main() -> None:
    write("80 系统/10 治理规则/附件、版权与大文件规则.md", POLICY)
    write("scripts/check_public_assets.py", CHECK_SCRIPT)
    write("80 系统/60 ADR/ADR-0011-公开附件版权与大文件策略.md", ADR)
    write("80 系统/20 模板/来源笔记模板.md", SOURCE_TEMPLATE)
    update_privacy()
    update_design()
    update_review()
    update_home()
    update_ci()
    update_readmes()
    update_changelog()
    print("Public asset policy migration complete.")


if __name__ == "__main__":
    main()
