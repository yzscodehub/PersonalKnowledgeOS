# Knowledge Graph Design

## 设计目标

PersonalKnowledgeOS 不采用纯目录树，也不采用纯图数据库，而采用：

- Domain Tree 负责领域组织
- Knowledge Graph 负责知识关系
- Capability Graph 负责能力成长

## 核心模型

```
Domain
  |
  Module
  |
  Knowledge Node
  |
  Capability
  |
  Project
  |
  Output
```

## 树与图的职责

### Tree

负责：

- 学习路径
- 分类管理
- 文件存储位置

### Graph

负责：

- 依赖关系
- 推导关系
- 应用关系
- 实现关系
- 对比关系

## 示例

PBR 作为一个知识节点：

```
Rendering Equation
        |
        v
      BRDF
        |
        v
       PBR
        |
        v
Material System
        |
        v
Rendering Engine
```

每个节点独立存储，通过链接建立关系。
