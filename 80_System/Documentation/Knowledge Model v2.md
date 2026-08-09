# PersonalKnowledgeOS Knowledge Model v2

## 总体模型

```
Sources
   |
   v
Knowledge Graph
   |
   v
Capability Graph
   |
   v
Projects
   |
   v
Outputs
```

## Knowledge Node

Knowledge Node 是最小知识实体。

规则：

- 一个核心概念一个节点
- 一个节点一个 Markdown 文件
- 节点通过链接形成网络

## 存储方式

```
Domain
 |
 Module
 |
 Knowledge Node.md
```

## 示例

```
Computer Graphics
 |
 05 Lighting and Material
 |
 PBR.md
```

PBR 不包含 BRDF、Fresnel 的副本。

而通过链接：

```
PBR
 |
 +-- BRDF
 +-- Microfacet
 +-- Fresnel
 +-- Material System
```

## 设计原则

分类稳定，关系动态。

目录不表达全部知识关系。
