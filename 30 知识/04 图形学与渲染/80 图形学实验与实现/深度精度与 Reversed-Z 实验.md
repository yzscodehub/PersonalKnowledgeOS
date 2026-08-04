---
id: GFX-EXP-DEPTH-001
type: experiment
domain: graphics
maturity: stable
verification: experiment-reproduced
lifecycle: active
sources:
  - "[[Akenine-Möller 等 - Real-Time Rendering 4th]]"
created: 2026-08-04
updated: 2026-08-04
---

# 深度精度与 Reversed-Z 实验

## 实验问题

比较 `float32` 深度缓冲中标准 Forward-Z 和 Reversed-Z 在远距离处相邻深度值对应的世界空间距离步长。

## 约定与参数

```text
near          = 0.1
far           = 1,000,000
sample        = 10,000
NDC depth     = [0, 1]
depth format  = float32 模拟
```

标准深度：

$$
d(s)=\frac{f}{f-n}-\frac{nf}{(f-n)s}
$$

Reversed-Z：

$$
d_r(s)=1-d(s)
$$

## 实验代码

```text
experiments/math_graphics/depth_precision.py
```

运行：

```bash
python experiments/math_graphics/depth_precision.py
```

脚本使用 `struct` 将 Python 浮点数舍入为 IEEE 754 单精度，并通过位级递增获得下一个可表示的正 `float32` 深度值。

## 测量方法

1. 把样本距离映射到深度；
2. 舍入到 `float32`；
3. 获取相邻的更大深度值；
4. 将两个深度反解回观察距离；
5. 比较二者世界空间距离差。

## 当前结果

在样本参数下，脚本输出近似：

```text
forward-Z world step at 10000: 60.0298
reversed-Z world step at 10000: 0.000909495
depth precision: PASS
```

并断言 Reversed-Z 的世界空间步长至少比 Forward-Z 小三个数量级。

结果说明：对浮点深度缓冲，标准透视映射把远处深度压到接近 $1$ 的区域，而 Reversed-Z 将其放到接近 $0$ 的高密度浮点区域。

## 不能过度推导的结论

- 结果不代表所有距离和所有格式都具有同一倍数；
- 固定点深度缓冲不具备相同的浮点分布优势；
- GPU 内部压缩、Hi-Z 和硬件实现可能影响实际性能，但不改变端点约定；
- Reversed-Z 不能修复共面几何或错误 Bias；
- 近裁剪面仍应设置在业务允许的尽可能远位置。

## 扩展实验

后续可以增加：

- 不同 near 值的误差曲线；
- `D16_UNORM`、`D24_UNORM` 与 `D32_FLOAT` 对比；
- 无限远 Reversed-Z；
- 实际 GPU 深度纹理可视化；
- 相机距离变化下的 Z-Fighting 样例。

## 知识关系

- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/透视投影|透视投影]]
- [[30 知识/04 图形学与渲染/12 相机、投影与可见性/深度缓冲、精度与 Reversed-Z|深度缓冲、精度与 Reversed-Z]]
