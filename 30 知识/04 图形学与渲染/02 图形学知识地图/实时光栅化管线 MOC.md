---
type: map
map_kind: moc
domain: graphics
maturity: outline
lifecycle: active
created: 2026-08-04
updated: 2026-08-04
---

# 实时光栅化管线 MOC

## 核心问题

实时渲染系统如何把场景、网格、材质和相机转换为一帧可显示图像，并在 CPU 时间、GPU 时间、带宽和延迟约束内持续运行？

## 前置知识

- [[30 知识/04 图形学与渲染/10 图形学基础与约定/图形学坐标空间总览|图形学坐标空间总览]]
- [[30 知识/04 图形学与渲染/02 图形学知识地图/坐标、相机与投影 MOC|坐标、相机与投影 MOC]]

## 高层流程

```text
场景更新与渲染数据提取
  ↓
可见性、排序、批处理和命令录制
  ↓
GPU 队列执行
  ↓
顶点与图元处理
  ↓
裁剪、光栅化和属性插值
  ↓
像素着色、深度模板和混合
  ↓
后处理与 Present
```

## 学习切面

### 功能切面

每个阶段输入什么、输出什么、保证什么不变量。

### 硬件切面

固定功能单元和可编程阶段如何协同，Quad、Wave、Cache 和带宽如何影响执行。

### API 切面

资源、PSO、Descriptor、Command Buffer、Queue 和同步如何表达管线工作。

### 性能切面

CPU Bound、GPU Bound、Overdraw、带宽、同步和 Frame Pacing 如何诊断。

## 尚未建设

CPU 到 GPU 帧流程、顶点处理与图元装配、裁剪、覆盖规则、透视正确插值、Pixel Shader Quad、Depth/Stencil、Early-Z、Blend 和 Present。

## 核心来源

- [[40 来源/10 书籍/图形学/Akenine-Möller 等 - Real-Time Rendering 4th]]
