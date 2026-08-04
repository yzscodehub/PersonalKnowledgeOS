---
id: GFX-EXP-PROJ-001
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

# 投影矩阵与 NDC 映射实验

## 实验问题

验证本文统一约定下的正交和透视投影矩阵是否把观察空间视体积端点正确映射到 NDC。

## 约定

- 列向量；
- 右手观察空间；
- 相机沿 $-Z$ 观察；
- NDC 横纵范围 $[-1,1]$；
- NDC 深度范围 $[0,1]$；
- 透视除法在矩阵乘法之后执行；
- 仅使用 Python 标准库。

## 实验代码

```text
experiments/math_graphics/projection_mapping.py
```

运行：

```bash
python experiments/math_graphics/projection_mapping.py
```

## 透视投影用例

参数：

```text
vertical FOV = 90°
aspect       = 1
near         = 1
far          = 10
```

断言：

- 近平面中心 $(0,0,-1)$ 映射到 $(0,0,0)$；
- 远平面中心 $(0,0,-10)$ 映射到 $(0,0,1)$；
- 近平面右上角 $(1,1,-1)$ 映射到 $(1,1,0)$。

最后一个断言同时验证了 $90^\circ$ FOV 下近平面半宽和半高均为 $1$。

## 正交投影用例

视体积：

```text
left/right   = -2 / 2
bottom/top   = -1 / 1
near/far     = 1 / 11
```

断言：

- $(l,b,-n)$ 映射到 $(-1,-1,0)$；
- $(r,t,-f)$ 映射到 $(1,1,1)$。

## 结果

全部断言通过时输出：

```text
projection mapping: PASS
```

脚本加入 GitHub Actions，防止后续修改矩阵推导、约定或示例时产生静默回归。

## 诊断价值

当实际画面出现翻转、裁剪错误或深度异常时，可以把问题拆为端点测试：

1. View Space 点是否符合前方深度符号；
2. Projection 后的 Clip 坐标是否符合预期；
3. 透视除法后的近远端点是否正确；
4. 视口 Y 翻转是否发生在预期层；
5. API 的深度范围是否与矩阵一致。

## 局限

- 未覆盖经典 OpenGL 的 $[-1,1]$ 深度；
- 未覆盖非对称视锥和 TAA Jitter；
- 未覆盖实际 GPU 裁剪和像素中心规则；
- 未覆盖左手观察空间。

## 验证证据

- 可执行代码：`experiments/math_graphics/projection_mapping.py`；
- CI 断言：正交和透视投影的近远端点及视锥角点。

## 知识关系

- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/正交投影|正交投影]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/Clip Space、透视除法与 NDC|Clip Space、透视除法与 NDC]]
