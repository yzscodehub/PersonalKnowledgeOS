---
id: GFX-TRANSFORM-002
type: theory
domain: graphics
maturity: draft
verification:
  - source-checked
  - derived
lifecycle: active
sources:
  - "[[Steven J. Gortler - Foundations of 3D Computer Graphics]]"
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---

# World 到 View 变换

## 问题与定位

世界空间描述场景中的对象，相机需要把这些点重新表示到以相机为原点的观察空间。World 到 View 变换不是“把相机移动到原点”，而是把世界点改写为相机标架下的坐标。

设世界点为 $p_w$：

$$
p_v=M_{vw}p_w
$$

本文使用列向量约定。

## 相机世界位姿

设相机在世界空间中的位置为 $c$，相机局部基轴在世界空间中的表示为：

$$
x_c,\ y_c,\ z_c
$$

将它们作为列构成旋转矩阵：

$$
R_c=\begin{bmatrix}x_c&y_c&z_c\end{bmatrix}
$$

相机从局部空间到世界空间的位姿矩阵为：

$$
M_{wv}^{camera}=\begin{bmatrix}
R_c&c\\
0&1
\end{bmatrix}
$$

这里的矩阵把相机局部坐标映射到世界坐标。

## View 矩阵是相机位姿的逆

World 到 View 变换是上述相机世界位姿的逆：

$$
M_{vw}=\left(M_{wv}^{camera}\right)^{-1}
$$

若 $R_c$ 是正交旋转矩阵：

$$
R_c^{-1}=R_c^T
$$

于是：

$$
M_{vw}=\begin{bmatrix}
R_c^T&-R_c^Tc\\
0&1
\end{bmatrix}
$$

展开后：

$$
M_{vw}=\begin{bmatrix}
x_c^T&-x_c\cdot c\\
y_c^T&-y_c\cdot c\\
z_c^T&-z_c\cdot c\\
0&1
\end{bmatrix}
$$

这说明 View 矩阵的前三行把世界向量投影到相机基轴，最后一列处理相机原点平移。

## 观察空间约定

常见右手观察空间令相机沿局部 $-Z$ 方向观察，前方可见点满足：

$$
z_v<0
$$

也有系统使用左手观察空间并令前方为 $+Z$。关键不是选择哪一个，而是使以下部分一致：

- 相机基构造；
- View 矩阵；
- Projection 矩阵；
- 背面剔除和绕序；
- 深度范围；
- Shader 中的方向约定。

## Look-At 构造

给定相机位置 $c$、目标点 $t$ 和参考上方向 $u_{ref}$，先计算观察方向：

$$
f=\operatorname{normalize}(t-c)
$$

在右手、相机前方为 $-Z$ 的约定下，可以令：

$$
z_c=-f
$$

再构造：

$$
x_c=\operatorname{normalize}(u_{ref}\times z_c)
$$

$$
y_c=z_c\times x_c
$$

叉积顺序必须与手性一致。

### 退化情况

当参考上方向与观察方向平行或近似平行时，叉积长度接近零，基构造不稳定。需要：

- 选择备用上方向；
- 对叉积长度设置阈值；
- 保持上一帧稳定朝向；
- 使用四元数或受约束相机控制器避免瞬时翻转。

## View 方向与相机对象变换

相机向右移动时，View 矩阵使整个世界向左移动；相机旋转时，世界在观察空间中应用反向旋转。

这正是被动换基与主动对象变换互为逆的表现。理解这一点比记忆“View 矩阵要反过来”更可靠。

## 相机相对渲染

大世界中常先从所有世界位置减去相机高精度位置，再使用只含旋转或小平移的 View 变换：

$$
p_{relative}=p_w-c
$$

这样可以提高相机附近单精度计算的有效精度。此时 CPU、GPU、阴影、反射和运动向量必须共享一致的相对原点策略。

## 多视图与历史矩阵

立体渲染、阴影相机、反射探针和多视口系统会同时存在多个 View 矩阵。

时域算法通常还需要：

- 当前 View；
- 上一帧 View；
- 当前 View-Projection；
- 上一帧 View-Projection；
- Jittered 与 Unjittered 矩阵。

应明确每个矩阵的坐标空间、抖动状态和帧索引。

## 常见误区

### 直接把相机世界矩阵作为 View 矩阵

View 矩阵是相机世界位姿的逆。

### 认为转置总能代替求逆

只有相机线性部分是正交旋转且不含缩放和切变时，转置才等于逆。

### Look-At 只需前向和上方向

还需处理手性、叉积顺序、近似平行和基归一化。

### 混淆观察方向与相机 $Z$ 轴

右手相机常沿 $-Z$ 看，局部 $z_c$ 轴与前向 $f$ 方向相反。

## 验证方法

1. 相机世界位置 $c$ 经 View 变换后应得到原点；
2. 相机三个世界基轴经 View 线性部分后应得到标准基；
3. 位于相机前方的点应得到符合约定的 View Space 深度符号；
4. 验证 $M_{vw}M_{wv}^{camera}=I$；
5. 对 Look-At 输入接近平行的上方向，验证退化处理。

## 知识关系

### 前置知识

- [[30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系|标架与坐标系]]
- [[30 知识/01 数学/11 线性代数/矩阵作为线性映射|矩阵作为线性映射]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Object 到 World 变换|Object 到 World 变换]]

### 后续知识

- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影|正交投影]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]

## 来源

- [[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]]，标架、相机和观察变换相关章节。
- [[40 来源/10 书籍/图形学/Akenine-Möller 等 - Real-Time Rendering 4th]]，View Transform 和变换管线相关章节。
