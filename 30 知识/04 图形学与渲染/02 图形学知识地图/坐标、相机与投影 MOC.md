---
type: map
domain: graphics
maturity: outline
created: 2026-08-04
updated: 2026-08-04
---

# 坐标、相机与投影 MOC

## 核心问题

三维场景中的局部几何如何被放入共同世界，再转换到相机视角，经过投影、裁剪和视口映射成为屏幕坐标？

## 已建设

- [[30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览|图形学坐标空间总览]]

## 数学前置

- [[30 知识/01 数学/11 线性代数/点与向量|点与向量]]
- [[30 知识/01 数学/11 线性代数/基与坐标|基与坐标]]
- [[30 知识/01 数学/12 解析、仿射与射影几何/标架与坐标系|标架与坐标系]]

## 推荐路径

```text
对象空间
  ↓ Model Transform
世界空间
  ↓ View Transform
观察空间
  ↓ Projection Transform
齐次裁剪空间
  ↓ Clipping + Perspective Divide
NDC
  ↓ Viewport Transform
屏幕空间
```

## 需要保持一致的约定

- 左手或右手坐标系；
- 相机前向轴；
- 行向量或列向量乘法；
- 矩阵组合顺序；
- Clip/NDC 深度范围；
- Framebuffer 和纹理原点；
- Front Face 绕序。

## 尚未建设

Object 到 World、World 到 View、正交投影、透视投影、Clip Space、透视除法、视口变换、深度缓冲和 Reversed-Z。

## 核心来源

- [[40 来源/10 书籍/图形学/Steven J. Gortler - Foundations of 3D Computer Graphics]]
- [[40 来源/10 书籍/图形学/Akenine-Möller 等 - Real-Time Rendering 4th]]
