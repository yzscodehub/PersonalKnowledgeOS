---
id: GFX-PROJ-003
type: system
domain: graphics
maturity: draft
verification: derived
lifecycle: active
sources:
  - "[[Steven J. Gortler - Foundations of 3D Computer Graphics]]"
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---

# Clip Space、透视除法与 NDC

## 问题与定位

Projection 矩阵的输出不是 NDC，也不是屏幕像素，而是四维齐次裁剪坐标。GPU 先在 Clip Space 中完成视体积裁剪，再执行透视除法得到 NDC，最后通过视口变换得到屏幕坐标。

完整链路：

```text
View Space
  ↓ Projection Matrix
Clip Space (x, y, z, w)
  ↓ Homogeneous Clipping
Clipped Primitives
  ↓ Perspective Divide
NDC
  ↓ Viewport Transform
Screen / Window Space
```

## Clip Space

顶点 Shader 输出：

$$
p_{clip}=(x_c,y_c,z_c,w_c)
$$

它是齐次坐标，不能在裁剪前简单视为三维点。

横纵裁剪条件通常为：

$$
-w_c\le x_c\le w_c
$$

$$
-w_c\le y_c\le w_c
$$

深度条件依赖 API：

### Direct3D 与常见 Vulkan 约定

$$
0\le z_c\le w_c
$$

### 经典 OpenGL 约定

$$
-w_c\le z_c\le w_c
$$

使用关于 $w$ 的线性不等式，可以在透视除法前正确裁剪穿越近面和相机平面的图元。

## 为什么先裁剪再除法

若先除以 $w$：

- $w=0$ 附近会产生无穷大；
- 跨越相机平面的边会发生不连续；
- 线性插值和裁剪不再稳定；
- 无法正确处理部分位于视锥内的三角形。

齐次裁剪会对边与裁剪平面的交点进行插值，生成新的顶点，然后才进入透视除法。

## 透视除法

对裁剪后顶点：

$$
x_{ndc}=\frac{x_c}{w_c}
$$

$$
y_{ndc}=\frac{y_c}{w_c}
$$

$$
z_{ndc}=\frac{z_c}{w_c}
$$

透视投影中通常有 $w_c=-z_v$ 或其约定变体，因此横纵坐标产生 $1/z$ 缩放。

正交投影中通常 $w_c=1$，透视除法不改变坐标。

## NDC

NDC 是与具体视口尺寸无关的标准化三维空间。

常见范围：

- $x,y\in[-1,1]$；
- 深度为 $[0,1]$ 或 $[-1,1]$；
- 屏幕 Y 方向尚未必与最终窗口像素方向相同。

NDC 是投影和光栅化之间的规范接口，不应与 View Space 或 Screen Space 混淆。

## 视口变换

设视口左上或左下基准由 API 约定，宽高为 $W,H$。横向映射通常可写为：

$$
x_s=x_0+\frac{x_{ndc}+1}{2}W
$$

Y 方向根据窗口坐标原点决定是否翻转：

$$
y_s=y_0+\frac{y_{ndc}+1}{2}H
$$

或：

$$
y_s=y_0+\frac{1-y_{ndc}}{2}H
$$

深度还会映射到视口的最小和最大深度范围。

像素中心通常位于半整数或由 API 明确定义的位置。精确覆盖规则属于光栅化阶段，不能只凭 NDC 范围推断。

## $w$ 的符号与相机后方

典型右手透视矩阵中：

$$
w_c=-z_v
$$

相机前方 $z_v<0$，因此 $w_c>0$。相机后方点可能得到负 $w$，其齐次裁剪行为与普通前方点不同。

不要通过对 $w$ 取绝对值来“修复”投影，这会破坏射影几何和裁剪语义。

## 透视正确插值

光栅化在屏幕空间进行，但纹理坐标、世界位置等属性原本定义在投影前空间。直接对属性做屏幕线性插值会产生错误。

GPU 使用与 $1/w$ 相关的插值规则。概念上，对属性 $a$：

$$
a=\frac{\sum_i\lambda_i\frac{a_i}{w_i}}{\sum_i\lambda_i\frac{1}{w_i}}
$$

其中 $\lambda_i$ 是屏幕空间重心权重。

这也是不能提前丢弃裁剪 $w$ 的另一个原因。

## API 差异清单

设计跨 API RHI 时至少记录：

- View Space 前方是 $+Z$ 还是 $-Z$；
- Clip Space 深度条件；
- NDC 深度范围；
- NDC 或视口 Y 方向；
- 窗口坐标原点；
- 像素中心和覆盖规则；
- 深度缓冲是否使用 Reversed-Z；
- Projection 矩阵是否已吸收平台修正。

建议在 RHI 层定义统一内部约定，再在投影或视口边界做显式适配。

## 常见误区

### Clip Space 等于 NDC

Clip Space 是四维齐次空间；NDC 是除以 $w$ 后的三维空间。

### Vertex Shader 输出屏幕坐标

标准位置输出仍需经过裁剪、透视除法、视口变换和光栅化。

### 提前手动除以 $w$ 可以节省硬件工作

这会破坏固定管线语义，通常是错误优化。

### OpenGL 和 Vulkan 只差 Y 翻转

它们还可能在深度范围、纹理坐标、视口和扩展能力上存在差异，必须逐项定义。

## 验证方法

1. 对每个 API 写出六个裁剪不等式；
2. 验证近远平面端点在 Clip 和 NDC 中的值；
3. 构造穿越近面的三角形，确认裁剪后不会产生爆炸坐标；
4. 对同一投影结果执行视口映射，检查四个角和屏幕原点；
5. 运行 [[30 知识/04 图形学与渲染/80 图形学实验与实现/投影矩阵与 NDC 映射实验|投影矩阵与 NDC 映射实验]]。

## 知识关系

### 前置知识

- [[30 知识/01 数学/12 解析、仿射与射影几何/齐次坐标|齐次坐标]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影|正交投影]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]

### 后续知识

- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z|深度缓冲、精度与 Reversed-Z]]

## 来源

- [[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]]，射影坐标、裁剪和图像生成相关章节。
- [[40 来源/10 书籍/图形学/Akenine-Möller 等 - Real-Time Rendering 4th]]，Projection、Clipping、Screen Mapping 和 Rasterization 相关章节。
