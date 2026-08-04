---
type: source-note
source_type: book
author: Tomas Akenine-Möller et al.
status: reading
authority: authoritative-secondary
created: 2026-08-04
updated: 2026-08-04
---

# Akenine-Möller 等 - Real-Time Rendering 4th

## 书目信息

- 版本：Fourth Edition
- 作者：Tomas Akenine-Möller、Eric Haines、Naty Hoffman、Angelo Pesce、Michał Iwanicki、Sébastien Hillaire
- 出版年份：2018

## 阅读目的

作为现代实时渲染体系的综合参考来源，用于补全渲染管线、GPU、纹理、光照、材质、阴影、图像空间效果和性能优化等主题。

## 试点章节地图

### 第 2 章：The Graphics Rendering Pipeline

当前关注：

- 实时渲染管线的高层阶段；
- 几何处理和顶点着色；
- Model、World 和 View Space；
- 投影、裁剪和屏幕映射；
- 光栅化和像素处理的职责边界。

### 变换相关章节

用于补充矩阵、Model/View/Projection、法线变换、相机和投影的工程表达。后续批次继续建立精确到小节的映射。

## 知识映射

- [[30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览|图形学坐标空间总览]]
- [[30 知识/04 图形学与渲染/02 图形学知识地图/实时光栅化管线 MOC|实时光栅化管线 MOC]]
- 待建设：顶点处理、裁剪、光栅化、纹理、BRDF、阴影、图像空间效果和性能。

## 提炼原则

不按书籍章节复制正文。每个章节作为证据，映射到具有稳定主归属、可验证且能连接工程实现的正式知识文章。

## 待验证问题

- 书中的通用管线模型如何分别映射到 DX11、DX12、Vulkan 和 Metal？
- 固定功能描述与现代 Mesh Shader、GPU-Driven 管线之间如何建立演化关系？
- 哪些结论需要通过 Frame Capture 和 GPU Counter 验证？

## 阅读进度

- [x] 建立第 2 章试点映射
- [x] 提炼坐标空间总览
- [ ] 提炼 CPU 到 GPU 帧流程
- [ ] 提炼裁剪、光栅化和插值文章
- [ ] 完成核心实验链接
