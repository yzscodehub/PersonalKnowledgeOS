---
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
z_{ndc}=rac{z+n}{n-f}
$$

端点：

$$
z=-n\Rightarrow0,\qquad z=-f\Rightarrow1
$$

与 `projection_mapping.py` 断言一致。

## 4. 透视投影审核

采用：

$$
P=egin{bmatrix}
rac{s_y}{a}&0&0&0\
0&s_y&0&0\
0&0&rac{f}{n-f}&rac{nf}{n-f}\
0&0&-1&0
\end{bmatrix}
$$

其中：

$$
s_y=rac{1}{	an(	heta_y/2)},\qquad w_{clip}=-z_{view}
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
d(s)=rac{f}{f-n}-rac{nf}{(f-n)s}
$$

反解：

$$
s=rac{nf}{f-d(f-n)}
$$

无限远 Reversed-Z：

$$
d_r(s)=rac{n}{s}
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
