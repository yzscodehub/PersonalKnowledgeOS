# Knowledge Node Relationship

## 节点关系类型

Knowledge Node 之间通过双向链接表达关系。

支持以下关系：

## Depends On

表示理论或技术依赖。

示例：

PBR -> BRDF

## Implements

表示工程实现。

示例：

PBR Theory -> Material System

## Applies To

表示应用场景。

示例：

BRDF -> Real Time Rendering

## Compared With

表示对比关系。

示例：

Forward Rendering -> Deferred Rendering

## Related

表示一般关联。

## Project Used

表示项目验证。

示例：

RenderGraph -> Mini Renderer

## 原则

不要为了建立关系复制知识。

一个知识只保留一个主要归属位置，其他关系通过链接表达。
