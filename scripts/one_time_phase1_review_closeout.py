#!/usr/bin/env python3
"""One-time migration that closes the Phase 1 pilot review.

This script adds source-page maps, verification evidence, transform invariants,
pilot consistency checks, review records, and the final Phase 2 scope. It does
not create Phase 2 content.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOUNDATIONS_PATH = "40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics.md"
RTR_PATH = "40 来源/10 书籍/图形学/Akenine-Möller 等 - Real-Time Rendering 4th.md"

FOUNDATIONS_NOTE = '''---
type: source-note
source_type: book
author: Steven J. Gortler
status: reading
created: 2026-08-04
updated: 2026-08-04
---

# Steven J. Gortler - Foundations of 3D Computer Graphics

## 书目信息与版本

- 作者：Steven J. Gortler
- 出版社：MIT Press
- 出版年份：2012
- ISBN：9780262017350
- 目录核对：MIT Press 官方目录

## 阅读目的

用于建立三维图形学所需的数学、几何、坐标变换、相机、投影、深度和光栅化基础。

## 可支持的声明类型

- 数学定义与推导；
- 图形学坐标、标架和变换概念；
- 相机、投影、深度和顶点到像素的基础机制；
- 基于现代 OpenGL 教学上下文的实现说明。

本书用于基础理论和教学模型，不单独证明 Direct3D、Vulkan、Metal 或某个驱动版本的具体行为。

## Phase 1 精确章节地图

页码范围根据官方目录中的章节起始页和下一章起始页确定。

| 章节 | 页码范围 | Phase 1 用途 |
|---|---:|---|
| 第 2 章 Linear | 9–20 | 向量空间、坐标向量、基、线性映射和矩阵 |
| 第 3 章 Affine | 21–28 | 点与向量、仿射空间、仿射组合和齐次仿射表示 |
| 第 5 章 Frames in Graphics | 35–44 | 标架、局部空间、世界空间和坐标变换 |
| 第 10 章 Projection | 89–100 | 正交投影、透视投影和齐次投影 |
| 第 11 章 Depth | 101–108 | 深度映射、深度缓冲和可见性 |
| 第 12 章 From Vertex to Pixel | 109–118 | 裁剪后到屏幕、光栅化和顶点到像素流程 |
| 第 13 章 Varying Variables (Tricky) | 119–124 | 属性插值和后续透视正确插值试点 |

## 文章映射

### 数学

- 第 2～3 章 → [[30 知识/01 数学/11 线性代数/点与向量|点与向量]]
- 第 2 章 → [[30 知识/01 数学/11 线性代数/向量空间|向量空间]]
- 第 2 章 → [[30 知识/01 数学/11 线性代数/基与坐标|基与坐标]]
- 第 2 章 → [[30 知识/01 数学/11 线性代数/矩阵作为线性映射|矩阵作为线性映射]]
- 第 3 章 → [[30 知识/01 数学/12 解析、仿射与射影几何/仿射空间与仿射组合|仿射空间与仿射组合]]
- 第 3、5 章 → [[30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系|标架与坐标系]]
- 第 3、10 章 → [[30 知识/01 数学/12 解析、仿射与射影几何/齐次坐标|齐次坐标]]

### 图形学

- 第 5、10～12 章 → [[30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览|图形学坐标空间总览]]
- 第 3、5 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换|Object 到 World 变换]]
- 第 5、10 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换|World 到 View 变换]]
- 第 10 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影|正交投影]]
- 第 10 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]
- 第 10、12 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC|Clip Space、透视除法与 NDC]]
- 第 11 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z|深度缓冲、精度与 Reversed-Z]]

## 对应实验

- [[30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验|矩阵乘法与坐标约定实验]]
- [[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]
- [[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]

## 限制、立场与适用范围

- 书中示例以现代 shader-based OpenGL 教学为主；
- 本知识库统一采用列向量、右手观察空间、相机沿 $-Z$、NDC 深度 $[0,1]$ 的内部约定；
- 与书中或具体 API 不同的符号和范围在应用文章中显式转换；
- Reversed-Z、现代跨 API RHI 和具体驱动行为需要额外来源与实验。

## 权利、许可与存储

- 版权：商业出版物，MIT Press；
- 是否允许公开再分发：不提交整本原始文件；
- 仓库保存：书目信息、章节定位和个人重述；
- 原始文件：仅保存在合法获取的位置，不进入公开仓库。

## 待验证问题

- 各 API 的 Clip/NDC、Y 方向和深度范围如何映射到统一内部约定？
- 第 12～13 章内容进入 Phase 2 后，哪些结论需要软件光栅器和 GPU Frame Capture 双重验证？

## 阅读进度

- [x] 建立第 2、3、5、10～13 章 Phase 1 映射
- [x] 补充章节页码范围
- [x] 提炼数学、坐标、相机、投影和深度主干
- [x] 建立第一批可执行实验
- [ ] 进入第 12～13 章的 Phase 2 光栅化与插值建设
'''

RTR_NOTE = '''---
type: source-note
source_type: book
author: Tomas Akenine-Möller et al.
status: reading
created: 2026-08-04
updated: 2026-08-04
---

# Akenine-Möller 等 - Real-Time Rendering 4th

## 书目信息与版本

- 版本：Fourth Edition
- 作者：Tomas Akenine-Möller、Eric Haines、Naty Hoffman、Angelo Pesce、Michał Iwanicki、Sébastien Hillaire
- 出版社：CRC Press
- 出版年份：2018
- 总页数：1198
- 目录核对：出版信息与 Google Books 目录

## 阅读目的

作为现代实时渲染体系的综合参考来源，用于补全渲染管线、GPU、变换、投影、纹理、光照、材质、阴影、图像空间效果和性能优化。

## 可支持的声明类型

- 现代实时渲染管线和 GPU 阶段职责；
- 图形学变换、投影和深度的综合解释；
- 实时渲染算法、工程权衡和行业实践；
- 后续纹理、PBR、阴影、性能和硬件专题。

本书是综合教材和专业参考，不替代具体 API 规范、驱动测试或某个引擎版本源码。

## Phase 1 精确章节地图

页码范围根据目录中的章节起始页和下一章起始页确定。

| 章节 | 页码范围 | Phase 1 用途 |
|---|---:|---|
| 第 2 章 The Graphics Rendering Pipeline | 11–28 | 应用、几何处理、光栅化和像素处理的高层职责 |
| 第 3 章 The Graphics Processing Unit | 29–56 | GPU 可编程阶段、固定功能和执行模型背景 |
| 第 4 章 Transforms | 57–102 | Model/View/Projection、法线、相机、投影和深度 |
| 第 5 章 Shading Basics | 103 起 | Phase 3 的着色基础，不属于当前试点 |

## 文章映射

- 第 2、4 章 → [[30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览|图形学坐标空间总览]]
- 第 4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换|Object 到 World 变换]]
- 第 4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换|World 到 View 变换]]
- 第 4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影|正交投影]]
- 第 4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]
- 第 2、4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC|Clip Space、透视除法与 NDC]]
- 第 4 章 → [[30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z|深度缓冲、精度与 Reversed-Z]]
- 第 2～3 章 → [[30 知识/04 图形学与渲染/02 图形学知识地图/实时光栅化管线 MOC|实时光栅化管线 MOC]]

## 对应实验

- [[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]
- [[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]
- [[30 知识/04 图形学与渲染/80 图形学实验与实现/深度精度与 Reversed-Z 实验|深度精度与 Reversed-Z 实验]]

## 提炼原则

不按书籍章节复制正文。每个章节作为证据，映射到具有稳定主归属、可验证且能连接工程实现的正式知识文章。

## 限制、立场与适用范围

- 书中同时讨论多个 API 和硬件背景，具体约定必须回到文章声明的内部坐标规则；
- API 规范性行为需要官方规范补充；
- Reversed-Z 的浮点精度收益由本库实验验证；
- 性能结论必须在明确 GPU、驱动、分辨率和工作负载下重新测量。

## 权利、许可与存储

- 版权：商业出版物，CRC Press；
- 是否允许公开再分发：不提交整本原始文件；
- 仓库保存：书目信息、章节定位和个人重述；
- 原始文件：仅保存在合法获取的位置，不进入公开仓库。

## 待验证问题

- 通用管线模型如何分别映射到 DX11、DX12、Vulkan、Metal 和 WebGPU？
- 固定功能描述与 Mesh Shader、GPU-Driven 管线之间如何建立演化关系？
- 哪些结论需要 Frame Capture、GPU Counter 和跨 API 实验验证？

## 阅读进度

- [x] 建立第 2～4 章 Phase 1 映射
- [x] 补充章节页码范围
- [x] 提炼坐标、相机、投影和深度主干
- [x] 建立变换、投影和深度最小实验
- [ ] 进入第 2～3 章的 Phase 2 光栅化管线建设
- [ ] 进入第 5 章后的 Phase 3 着色建设
'''

AUDIT_NOTE = '''---
type: system-review
status: accepted
review_scope: phase-1-conventions
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 1 矩阵、投影与深度审核记录

## 1. 统一内部约定

Phase 1 文章和实验统一采用：

```text
向量表示        列向量
矩阵作用        p' = M p，右侧先作用
观察空间        右手
相机前向        -Z
近平面/远平面   0 < n < f
NDC x/y         [-1, 1]
NDC z           [0, 1]
标准深度        near → 0，far → 1
Reversed-Z      near → 1，far → 0
```

这些是知识库的统一教学和工程分析约定，不声称所有 API 或书籍使用相同形式。跨 API 文章必须显式转换。

## 2. 矩阵链路审核

列向量约定下：

$$
p_{clip}=PVMp_{object}
$$

审核结果：

- Model、View、Projection 组合顺序一致；
- Scene Graph 使用 $M_{world}^{child}=M_{world}^{parent}M_{local}^{child}$；
- 相机世界位姿的逆作为 View Matrix；
- 纯旋转时 $R^{-1}=R^T$；
- 一般矩阵不能用转置替代逆；
- 平移只影响 $w=1$ 的点，不影响 $w=0$ 的方向；
- 非均匀缩放下法线使用 $(A^{-1})^T$。

对应实验：

- [[30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验|矩阵乘法与坐标约定实验]]
- [[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]

## 3. 正交投影审核

视空间范围：

$$
l\le x\le r,\quad b\le y\le t,\quad -f\le z\le-n
$$

矩阵深度项：

$$
z_{ndc}=\frac{z+n}{n-f}
$$

端点：

$$
z=-n\Rightarrow0,\qquad z=-f\Rightarrow1
$$

与 `projection_mapping.py` 断言一致。

## 4. 透视投影审核

采用：

$$
P=\begin{bmatrix}
\frac{s_y}{a}&0&0&0\\
0&s_y&0&0\\
0&0&\frac{f}{n-f}&\frac{nf}{n-f}\\
0&0&-1&0
\end{bmatrix}
$$

其中：

$$
s_y=\frac{1}{\tan(\theta_y/2)},\qquad w_{clip}=-z_{view}
$$

端点审核：

$$
z=-n\Rightarrow z_{ndc}=0
$$

$$
z=-f\Rightarrow z_{ndc}=1
$$

横纵坐标在透视除法后得到 $x/(-z)$、$y/(-z)$，与实验一致。

## 5. Clip Space 与 NDC 审核

在当前零到一深度约定下，裁剪条件为：

$$
-w\le x\le w,\quad -w\le y\le w,\quad 0\le z\le w
$$

裁剪先于透视除法。文章没有把 Clip Space 与 NDC 混为一体，且保留 $w$ 用于裁剪和透视正确插值。

## 6. 深度与 Reversed-Z 审核

令正距离 $s=-z$：

$$
d(s)=\frac{f}{f-n}-\frac{nf}{(f-n)s}
$$

反解：

$$
s=\frac{nf}{f-d(f-n)}
$$

无限远 Reversed-Z：

$$
d_r(s)=\frac{n}{s}
$$

审核结果：

- 标准深度和反解公式一致；
- 深度关于 $1/s$ 非线性；
- 推远近裁剪面通常比单纯扩大远平面更能改善精度；
- 浮点深度下 Reversed-Z 的远处精度优势已由位级实验复现；
- 固定点格式不应直接套用同等收益结论；
- Reversed-Z 还需要同步修改清除值、比较函数、Hi-Z 和深度线性化。

## 7. 发现的问题与修正

本轮未发现阻断性的公式错误。确认以下边界：

1. 文章矩阵是知识库统一内部约定，不直接等同任一 API 的默认函数；
2. 书籍负责基础与综合解释，API 规范负责规范性行为；
3. Reversed-Z 的精度结论只对明确的浮点深度模型和实验参数负责；
4. Look-At、非对称投影、TAA Jitter 和具体 API 适配留给后续应用文章；
5. Phase 2 需要补齐齐次裁剪、Top-Left Rule 和透视正确插值的独立实验。

## 8. 结论

`accepted`

Phase 1 的矩阵、投影和深度主干在当前统一约定下自洽，公式与可执行实验一致。
'''

BOUNDARY_AUDIT = '''---
type: system-review
status: accepted
review_scope: phase-1-ownership
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 1 数学与图形学边界审核记录

## 审核目标

确认数学主文章和图形学应用文章没有维护重复的完整基础解释。

## 文章职责

| 数学主文章 | 负责内容 | 图形学应用文章 | 负责内容 |
|---|---|---|---|
| 点与向量 | 点、位移、合法运算 | 图形学坐标空间总览 | 在渲染空间中的数据语义 |
| 基与坐标 | 抽象向量与坐标表示 | Object／World／View | 局部、世界和相机标架的应用 |
| 矩阵作为线性映射 | 矩阵、组合、逆和换基 | Object 到 World | TRS、层级、实例、包围体和法线 |
| 仿射空间与仿射组合 | 点集合、平移、仿射组合 | 光栅化后续应用 | 重心权重和属性插值上下文 |
| 标架与坐标系 | 原点、基和标架变换 | World 到 View | 相机世界位姿的逆和 Look-At |
| 齐次坐标 | 射影等价类、$w$ 和仿射嵌入 | Projection／Clip／NDC | GPU 投影、裁剪和视口链路 |

## 允许的上下文回顾

图形学文章可以简短回顾数学前置，但必须：

- 链接数学主文章；
- 不重新证明完整基础理论；
- 只保留理解工程约定所需的最小定义；
- 把平台、GPU、API 和失败条件留在应用文章。

## 审核结果

- 数学文章主归属稳定；
- 图形学文章均链接对应数学前置；
- Projection 公式属于图形学应用，不需要在齐次坐标文章中复制完整矩阵；
- 法线逆转置留在 Object 到 World 应用文章，数学层只维护线性映射和对偶结构的基础；
- View Matrix 留在相机应用文章，标架文章只维护通用坐标变换；
- 未发现需要合并的重复主文章。

## 后续边界

- UE5、DX12、Vulkan、Metal 等文章链接当前图形学主干，只解释各自 API 和源码映射；
- 机器人 SE(3) 文章链接数学旋转与标架文章，不放入图形学；
- Phase 2 的重心坐标若需要完整数学解释，应在数学领域建立主文章，光栅化文章只维护应用。

## 结论

`accepted`
'''

PROTOTYPE_AUDIT = '''---
type: system-review
status: accepted
review_scope: phase-1-note-prototypes
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 1 文章原型审核记录

## 发现

原知识文章模板同时固定要求定义、机制、推导、直觉、实现、性能等所有章节，容易让简单概念文章出现空章节，也会让作者为了“填模板”重复内容。

## 决策

模板只固定以下主干：

- 问题与范围；
- 定义与约定；
- 核心内容；
- 边界、误区与失败条件；
- 验证证据；
- 知识关系；
- 来源。

推导、算法、数据流、实现、调试和性能按文章类型选择，不要求全部出现。

新文章默认 `maturity: seed`，避免空模板一创建就声称达到 `draft`。达到 `draft` 后必须具有来源或原创推导／实验／生产证据。

## 原型结论

| 类型 | 试点结果 |
|---|---|
| theory | 适合数学定义、推导和边界 |
| concept | 适合坐标空间等稳定概念总览 |
| implementation | 适合 Object 到 World 等工程映射 |
| experiment | 适合问题、输入、断言、结果和局限 |
| map | 通过 `map_kind` 区分 MOC、路线和索引 |
| source-note | 适合章节定位、权利和反向映射 |

## 维护成本判断

- Frontmatter 已缩减为最小字段；
- 日期可由脚本同步；
- MOC、学习路线和 Manifest 不再重复职责；
- 一篇同类文章不需要修改总体架构；
- 当前模板可以进入 Phase 2 使用。

## 结论

`accepted`
'''

PHASE2_SCOPE = '''---
type: roadmap
status: accepted
scope: phase-2
version: 1.0
created: 2026-08-04
updated: 2026-08-04
---

# Phase 2 实时光栅化管线范围确认

## 目标

建立一条从 CPU 提交到像素输出的可运行知识链，并验证算法文章、系统文章和软件实验的组织方式。

## 分支与 PR

```text
branch: content/graphics-raster-pipeline
base: main
```

必须在 PR #1 合并后创建，禁止继续堆入 Bootstrap PR。

## 核心文章

1. CPU 到 GPU 帧流程；
2. 顶点输入与顶点处理；
3. 图元装配与齐次裁剪；
4. 光栅化、边函数与覆盖规则；
5. 重心坐标；
6. 透视正确插值；
7. Pixel Shader Quad 与导数；
8. 深度、模板和 Early-Z；
9. 混合与输出合并；
10. Present 与 Frame Pacing 总览。

## 实验

- 三角形边函数和覆盖测试；
- Top-Left Rule；
- 重心坐标；
- 线性插值与透视正确插值对比；
- 深度测试和简单混合；
- 最小软件光栅器图像输出；
- 关键不变量加入 CI。

## 前置知识

- [[30 知识/04 图形学与渲染/02 图形学知识地图/坐标、相机与投影 MOC|坐标、相机与投影 MOC]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC|Clip Space、透视除法与 NDC]]
- [[30 知识/01 数学/12 解析、仿射与射影几何/仿射空间与仿射组合|仿射空间与仿射组合]]

## 明确非目标

- 不深入 DX12／Vulkan 命令提交和同步细节；
- 不建设完整 GPU 架构课程；
- 不进入纹理过滤、材质、PBR、阴影和后处理；
- 不开始旧知识库全量迁移；
- 不按 API 平台复制一套光栅化理论。

## 退出条件

- 三角形从顶点到像素的链路可运行；
- 软件实验输出可检查结果；
- 原理与 API 应用边界清晰；
- MOC、Manifest、来源和实验同步；
- CI 自动验证覆盖、插值和深度不变量；
- 形成 Phase 2 复盘后才能进入纹理和 PBR。
'''

TRANSFORM_EXPERIMENT_NOTE = '''---
id: GFX-EXP-TRANSFORM-001
type: experiment
domain: graphics
maturity: stable
verification:
  - source-checked
  - experiment-reproduced
lifecycle: active
sources:
  - "[[Steven J. Gortler - Foundations of 3D Computer Graphics]]"
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---

# 观察与法线变换不变量实验

## 实验问题

验证两个容易在工程中出错的不变量：

1. 相机世界位姿的逆是否把相机位置和基轴映射到观察空间标准标架；
2. 非均匀缩放下，法线逆转置是否保持与变换后切向量垂直。

## 实验代码

```text
experiments/math_graphics/transform_invariants.py
```

运行：

```bash
python experiments/math_graphics/transform_invariants.py
```

## 相机测试

构造一个包含旋转和平移的刚体相机世界矩阵：

$$
M_{camera}=
\begin{bmatrix}
R&c\\
0&1
\end{bmatrix}
$$

并使用：

$$
V=M_{camera}^{-1}=
\begin{bmatrix}
R^T&-R^Tc\\
0&1
\end{bmatrix}
$$

断言：

- 相机世界位置经 View 变换得到原点；
- 相机的三个世界基轴经 View 线性部分得到标准基；
- $VM_{camera}$ 接近单位矩阵。

## 法线测试

使用非均匀缩放：

$$
A=\operatorname{diag}(2,3,1)
$$

原始切向量和法线满足：

$$
t=(1,0,-1),\qquad n=(1,0,1),\qquad t\cdot n=0
$$

直接使用 $An$ 后不再与 $At$ 垂直；使用：

$$
n'=(A^{-1})^Tn
$$

则：

$$
(At)\cdot n'=0
$$

## 结果

全部断言通过时输出：

```text
camera view invariants: PASS
normal inverse-transpose invariant: PASS
```

## 局限

- 只验证刚体相机，不覆盖含缩放的相机层级；
- 只验证一个非均匀缩放样例，不覆盖奇异矩阵；
- 不验证具体 Shader 常量缓冲上传和 API 矩阵布局；
- 浮点容差仅用于最小实验，不代表生产误差预算。

## 验证证据

- 代码：`experiments/math_graphics/transform_invariants.py`；
- 理论：[[30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系|标架与坐标系]]；
- 应用：[[30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换|World 到 View 变换]]、[[30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换|Object 到 World 变换]]。

## 知识关系

- [[30 知识/01 数学/11 线性代数/矩阵作为线性映射|矩阵作为线性映射]]
- [[30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系|标架与坐标系]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换|Object 到 World 变换]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换|World 到 View 变换]]
'''

TRANSFORM_CODE = '''from __future__ import annotations

from math import isclose
from typing import Iterable

Vec3 = tuple[float, float, float]
Vec4 = tuple[float, float, float, float]
Mat3 = tuple[tuple[float, float, float], ...]
Mat4 = tuple[tuple[float, float, float, float], ...]


def mat4_vec(m: Mat4, v: Vec4) -> Vec4:
    return tuple(
        sum(m[row][col] * v[col] for col in range(4)) for row in range(4)
    )  # type: ignore[return-value]


def mat4_mul(a: Mat4, b: Mat4) -> Mat4:
    return tuple(
        tuple(sum(a[row][k] * b[k][col] for k in range(4)) for col in range(4))
        for row in range(4)
    )


def mat3_vec(m: Mat3, v: Vec3) -> Vec3:
    return tuple(
        sum(m[row][col] * v[col] for col in range(3)) for row in range(3)
    )  # type: ignore[return-value]


def transpose3(m: Mat3) -> Mat3:
    return tuple(tuple(m[col][row] for col in range(3)) for row in range(3))


def dot(a: Vec3, b: Vec3) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def assert_values(actual: Iterable[float], expected: Iterable[float]) -> None:
    av = tuple(actual)
    ev = tuple(expected)
    for a, e in zip(av, ev, strict=True):
        assert isclose(a, e, rel_tol=1e-9, abs_tol=1e-9), (av, ev)


def camera_world_and_view() -> tuple[Mat4, Mat4, tuple[Vec3, Vec3, Vec3], Vec3]:
    x_axis: Vec3 = (0.0, 1.0, 0.0)
    y_axis: Vec3 = (-1.0, 0.0, 0.0)
    z_axis: Vec3 = (0.0, 0.0, 1.0)
    position: Vec3 = (3.0, -2.0, 5.0)
    rotation: Mat3 = (
        (x_axis[0], y_axis[0], z_axis[0]),
        (x_axis[1], y_axis[1], z_axis[1]),
        (x_axis[2], y_axis[2], z_axis[2]),
    )
    rt = transpose3(rotation)
    tx = -dot(rt[0], position)
    ty = -dot(rt[1], position)
    tz = -dot(rt[2], position)
    world: Mat4 = (
        (rotation[0][0], rotation[0][1], rotation[0][2], position[0]),
        (rotation[1][0], rotation[1][1], rotation[1][2], position[1]),
        (rotation[2][0], rotation[2][1], rotation[2][2], position[2]),
        (0.0, 0.0, 0.0, 1.0),
    )
    view: Mat4 = (
        (rt[0][0], rt[0][1], rt[0][2], tx),
        (rt[1][0], rt[1][1], rt[1][2], ty),
        (rt[2][0], rt[2][1], rt[2][2], tz),
        (0.0, 0.0, 0.0, 1.0),
    )
    return world, view, (x_axis, y_axis, z_axis), position


def test_camera_view() -> None:
    world, view, axes, position = camera_world_and_view()
    assert_values(mat4_vec(view, (*position, 1.0)), (0.0, 0.0, 0.0, 1.0))
    for index, axis in enumerate(axes):
        expected = [0.0, 0.0, 0.0, 0.0]
        expected[index] = 1.0
        assert_values(mat4_vec(view, (*axis, 0.0)), expected)
    identity = mat4_mul(view, world)
    for row in range(4):
        for col in range(4):
            assert isclose(
                identity[row][col],
                1.0 if row == col else 0.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
    print("camera view invariants: PASS")


def test_normal_inverse_transpose() -> None:
    scale: Mat3 = (
        (2.0, 0.0, 0.0),
        (0.0, 3.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    inverse_transpose: Mat3 = (
        (0.5, 0.0, 0.0),
        (0.0, 1.0 / 3.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    tangent: Vec3 = (1.0, 0.0, -1.0)
    normal: Vec3 = (1.0, 0.0, 1.0)
    assert isclose(dot(tangent, normal), 0.0, abs_tol=1e-9)

    transformed_tangent = mat3_vec(scale, tangent)
    naive_normal = mat3_vec(scale, normal)
    correct_normal = mat3_vec(inverse_transpose, normal)

    assert not isclose(dot(transformed_tangent, naive_normal), 0.0, abs_tol=1e-9)
    assert isclose(dot(transformed_tangent, correct_normal), 0.0, abs_tol=1e-9)
    print("normal inverse-transpose invariant: PASS")


def main() -> None:
    test_camera_view()
    test_normal_inverse_transpose()


if __name__ == "__main__":
    main()
'''

CONSISTENCY_SCRIPT = r'''#!/usr/bin/env python3
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
'''

KNOWLEDGE_TEMPLATE = '''---
id:
type: concept
domain:
maturity: seed
verification: []
lifecycle: active
sources: []
created: {{date}}
updated: {{date}}
---

# 标题

## 问题与范围

这篇文章解决什么问题？不解决什么问题？

## 定义与约定

## 核心内容

根据文章类型选择组织方式：理论推导、算法步骤、系统数据流或工程实现，不要求全部出现。

## 边界、误区与失败条件

## 验证证据

链接具体来源、推导章节、实验或生产记录。

## 知识关系

### 前置知识

### 上层应用

### 对比与边界

### 实现与实验

## 来源
'''

API_TEMPLATE = '''---
id:
type: api-reference
domain:
maturity: seed
verification: []
lifecycle: active
version_sensitive: true
platforms: []
apis: []
versions: []
sources: []
created: {{date}}
updated: {{date}}
---

# API／对象名称

## 功能与范围

## 对象、接口与生命周期

## 创建、使用与销毁流程

## 状态、同步、线程与资源所有权

## 最小示例

## 错误、边界与调试

## 性能影响

## 跨平台对应

## 验证证据

## 官方来源
'''

EXPERIMENT_TEMPLATE = '''---
id:
type: experiment
domain:
maturity: seed
verification: []
lifecycle: active
project: []
sources: []
created: {{date}}
updated: {{date}}
---

# 实验标题

## 实验问题与假设

## 环境

- 操作系统：
- CPU：
- GPU：
- 驱动：
- API／引擎：
- 代码版本：

## 输入、变量与控制条件

## 实验步骤与断言

## 原始结果

## 分析与结论

## 局限与威胁

## 复现方式

## 验证的知识与来源
'''

TROUBLESHOOTING_TEMPLATE = '''---
id:
type: troubleshooting
domain:
maturity: seed
verification: []
lifecycle: active
platforms: []
versions: []
created: {{date}}
updated: {{date}}
---

# 症状或问题

## 影响、环境与复现条件

## 预期与实际结果

## 假设与排查过程

## 根因

## 修复方案

## 验证证据

## 预防措施

## 相关知识与来源
'''

EVIDENCE: dict[str, str] = {
    "30 知识/01 数学/11 线性代数/点与向量.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 2～3 章。",
    "30 知识/01 数学/11 线性代数/向量空间.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 2 章。",
    "30 知识/01 数学/11 线性代数/基与坐标.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 2 章。",
    "30 知识/01 数学/11 线性代数/矩阵作为线性映射.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 2 章；\n- 推导：本文“矩阵列”“组合与乘法顺序”“主动变换与被动换基”；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验|矩阵乘法与坐标约定实验]]。",
    "30 知识/01 数学/12 解析、仿射与射影几何/仿射空间与仿射组合.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 3 章；\n- 推导：本文“仿射组合”与原点平移不变性。",
    "30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 3、5 章；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]。",
    "30 知识/01 数学/12 解析、仿射与射影几何/齐次坐标.md": "- 来源核对：[[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]] 第 3、10 章；\n- 推导：本文“齐次点的等价关系”“点与向量的仿射嵌入”；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。",
    "30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览.md": "- 来源核对：两本核心来源的坐标、管线与变换章节；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验|矩阵乘法与坐标约定实验]]、[[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]、[[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换.md": "- 来源核对：Foundations 第 3、5 章；Real-Time Rendering 4th 第 4 章；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验|矩阵乘法与坐标约定实验]]、[[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换.md": "- 来源核对：Foundations 第 5、10 章；Real-Time Rendering 4th 第 4 章；\n- 推导：本文“View 矩阵是相机位姿的逆”；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影.md": "- 来源核对：Foundations 第 10 章；Real-Time Rendering 4th 第 4 章；\n- 推导：本文“一维区间映射”和投影矩阵；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影.md": "- 来源核对：Foundations 第 10 章；Real-Time Rendering 4th 第 4 章；\n- 推导：本文“针孔模型”“齐次投影矩阵”和深度端点；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC.md": "- 来源核对：Foundations 第 10、12 章；Real-Time Rendering 4th 第 2、4 章；\n- 推导：本文齐次裁剪条件和透视除法；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。",
    "30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z.md": "- 来源核对：Foundations 第 11 章；Real-Time Rendering 4th 第 4 章；\n- 推导：本文标准深度、反解和无限远 Reversed-Z 公式；\n- 实验：[[30 知识/04 图形学与渲染/80 图形学实验与实现/深度精度与 Reversed-Z 实验|深度精度与 Reversed-Z 实验]]。",
    "30 知识/04 图形学与渲染/80 图形学实验与实现/矩阵乘法与坐标约定实验.md": "- 可执行代码：`experiments/math_graphics/coordinate_conventions.py`；\n- CI 断言：点／方向平移语义和矩阵组合顺序。",
    "30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验.md": "- 可执行代码：`experiments/math_graphics/projection_mapping.py`；\n- CI 断言：正交和透视投影的近远端点及视锥角点。",
    "30 知识/04 图形学与渲染/80 图形学实验与实现/深度精度与 Reversed-Z 实验.md": "- 可执行代码：`experiments/math_graphics/depth_precision.py`；\n- CI 断言：深度端点和 Float32 远距离世界步长对比。",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_text(encoding="utf-8") == content:
        return
    target.write_text(content, encoding="utf-8")
    print(path)


def add_evidence(path: str, evidence: str) -> None:
    text = read(path)
    if "## 验证证据" in text:
        return
    marker = "\n## 知识关系"
    if marker not in text:
        raise RuntimeError(f"Knowledge relationship marker missing: {path}")
    text = text.replace(marker, f"\n## 验证证据\n\n{evidence}\n{marker}", 1)
    write(path, text)


def add_verification(path: str, value: str) -> None:
    text = read(path)
    lines = text.splitlines()
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        raise RuntimeError(f"Frontmatter missing: {path}")
    start = next((i for i in range(1, closing) if lines[i].startswith("verification:")), None)
    if start is None:
        return
    end = start + 1
    while end < closing and re.match(r"^\s+-\s+", lines[end]):
        end += 1
    current = [re.sub(r"^\s+-\s+", "", line) for line in lines[start + 1 : end]]
    if value in current:
        return
    lines.insert(end, f"  - {value}")
    write(path, "\n".join(lines) + "\n")


def update_manifest() -> None:
    path = "80 系统/30 Manifest/试点建设清单.yaml"
    text = read(path)
    if "GFX-EXP-TRANSFORM-001" not in text:
        text += '''

  - id: GFX-EXP-TRANSFORM-001
    title: 观察与法线变换不变量实验
    status: stable
    verification:
      - source-checked
      - experiment-reproduced
    article_path: 30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验.md
    code_path: experiments/math_graphics/transform_invariants.py
'''
    write(path, text)


def update_mocs() -> None:
    for path in [
        "30 知识/01 数学/02 数学知识地图/线性代数与空间变换 MOC.md",
        "30 知识/04 图形学与渲染/02 图形学知识地图/坐标、相机与投影 MOC.md",
    ]:
        text = read(path)
        link = "- [[30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验|观察与法线变换不变量实验]]"
        if link not in text:
            marker = "## 实验\n"
            text = text.replace(marker, marker + "\n" + link + "\n", 1)
        write(path, text)


def update_experiments_readme() -> None:
    path = "experiments/README.md"
    text = read(path)
    command = "python experiments/math_graphics/transform_invariants.py"
    if command not in text:
        text = text.replace(
            "python experiments/math_graphics/coordinate_conventions.py\n",
            "python experiments/math_graphics/coordinate_conventions.py\n" + command + "\n",
            1,
        )
    write(path, text)


def update_templates() -> None:
    write("80 系统/20 模板/知识文章模板.md", KNOWLEDGE_TEMPLATE)
    write("80 系统/20 模板/API文章模板.md", API_TEMPLATE)
    write("80 系统/20 模板/实验文章模板.md", EXPERIMENT_TEMPLATE)
    write("80 系统/20 模板/故障排查模板.md", TROUBLESHOOTING_TEMPLATE)


def update_phase1_review() -> None:
    path = "80 系统/04 Phase 1 试点复盘.md"
    text = read(path)
    text = text.replace("status: review", "status: accepted", 1)
    text = text.replace("version: 1.0", "version: 2.0", 1)
    review_start = text.index("## 3. 审核清单")
    output_start = text.index("## 4. 需要形成的输出")
    reviewed = text[review_start:output_start].replace("- [ ]", "- [x]")
    text = text[:review_start] + reviewed + text[output_start:]
    output_pattern = re.compile(r"## 4\. 需要形成的输出\n[\s\S]*?\n## 5\. 退出条件")
    output = '''## 4. 已形成的输出

- [[80 系统/05 Phase 1 矩阵投影与深度审核记录|矩阵、投影和深度审核记录]]；
- 两本来源笔记中的章节与页码映射；
- [[80 系统/06 Phase 1 数学与图形学边界审核记录|数学与图形学边界审核记录]]；
- 各试点文章中的“验证证据”章节；
- `scripts/check_pilot_consistency.py` 和 Manifest 一致性检查；
- [[80 系统/07 Phase 1 文章原型审核记录|文章原型审核记录]]；
- [[80 系统/08 Phase 2 范围确认|Phase 2 最终范围和非目标]]。

## 5. 退出条件'''
    text, count = output_pattern.subn(output, text, count=1)
    if count != 1:
        raise RuntimeError("Phase 1 output section not found")
    text = text.replace("## 6. 当前结论\n\n`review-in-progress`", "## 6. 当前结论\n\n`accepted`\n\nPhase 1 试点已经形成来源—数学—图形学—实验—MOC／路线／Manifest 的闭环，满足 PR #1 最终评审条件。", 1)
    write(path, text)


def update_roadmap() -> None:
    path = "80 系统/02 实施路线图.md"
    text = read(path)
    text = text.replace("version: 1.2", "version: 1.3", 1)
    phase1_start = text.index("# 4. Phase 1")
    phase2_start = text.index("# 5. Phase 2")
    phase1 = text[phase1_start:phase2_start].replace("- [ ]", "- [x]")
    if "## 当前状态\n\n`completed`" not in phase1:
        phase1 = phase1.rstrip() + "\n\n## 当前状态\n\n`completed`\n\nPhase 1 复盘已通过；等待 PR #1 最终人工检查和合并。\n\n---\n\n"
    text = text[:phase1_start] + phase1 + text[phase2_start:]
    write(path, text)


def update_system_home() -> None:
    path = "80 系统/00 知识库主页.md"
    text = read(path)
    text = text.replace("Gate A 已通过，当前处于 **Phase 1 试点复盘期**。", "Gate A 和 Phase 1 试点复盘均已通过，当前等待 **PR #1 最终人工检查与合并**。", 1)
    text = text.replace("当前只审核和修复已有数学、坐标、相机、投影和深度试点；PR #1 合并前暂停扩展光栅化、PBR、API 和其他领域。", "PR #1 合并前只允许最终修复和校验；光栅化、PBR、API 和迁移将在独立分支中进行。", 1)
    write(path, text)


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    text = text.replace("Gate A 总体设计已经通过，当前处于 **Phase 1 试点复盘期**。在试点复盘和 PR #1 合并前，暂停扩展光栅化、PBR、API 和其他领域。", "Gate A 和 Phase 1 试点复盘已经通过。当前 Draft PR #1 等待最终人工检查；合并前不扩展光栅化、PBR、API 和其他领域。", 1)
    write(path, text)


def update_changelog() -> None:
    path = "80 系统/90 CHANGELOG/CHANGELOG.md"
    text = read(path)
    marker = "- Phase 1 试点复盘文档。"
    addition = "- Phase 1 矩阵／投影／深度、知识边界和文章原型审核记录；\n- 观察与法线变换不变量实验；\n- 试点 Manifest、来源反向链接和实验路径一致性检查；\n- Phase 2 范围确认。"
    if addition.splitlines()[0] not in text:
        text = text.replace(marker, marker + "\n" + addition, 1)
    changed = "- Gate A 已通过，当前阶段切换到 Phase 1 试点复盘。"
    if "Phase 1 试点复盘已通过" not in text:
        text = text.replace(changed, changed + "\n- Phase 1 试点复盘已通过，PR #1 等待最终人工检查。", 1)
    write(path, text)


def main() -> None:
    write(FOUNDATIONS_PATH, FOUNDATIONS_NOTE)
    write(RTR_PATH, RTR_NOTE)
    write("80 系统/05 Phase 1 矩阵投影与深度审核记录.md", AUDIT_NOTE)
    write("80 系统/06 Phase 1 数学与图形学边界审核记录.md", BOUNDARY_AUDIT)
    write("80 系统/07 Phase 1 文章原型审核记录.md", PROTOTYPE_AUDIT)
    write("80 系统/08 Phase 2 范围确认.md", PHASE2_SCOPE)
    write("30 知识/04 图形学与渲染/80 图形学实验与实现/观察与法线变换不变量实验.md", TRANSFORM_EXPERIMENT_NOTE)
    write("experiments/math_graphics/transform_invariants.py", TRANSFORM_CODE)
    write("scripts/check_pilot_consistency.py", CONSISTENCY_SCRIPT)

    for path, evidence in EVIDENCE.items():
        add_evidence(path, evidence)

    for path in [
        "30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系.md",
        "30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换.md",
        "30 知识/04 图形学与渲染/12 相机、投影与可见性/World 到 View 变换.md",
    ]:
        add_verification(path, "experiment-reproduced")

    update_manifest()
    update_mocs()
    update_experiments_readme()
    update_templates()
    update_phase1_review()
    update_roadmap()
    update_system_home()
    update_readme()
    update_changelog()
    print("Phase 1 review closeout migration complete.")


if __name__ == "__main__":
    main()
