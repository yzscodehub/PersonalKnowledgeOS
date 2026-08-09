# Knowledge Link Rules

## Purpose

Define how Knowledge Nodes form a knowledge graph.

## Relationship Types

### Depends On

Fundamental dependency.

Example:

```
PBR -> BRDF
```

### Implements

Engineering implementation.

Example:

```
PBR Theory -> Material System
```

### Applies To

Application relationship.

Example:

```
BRDF -> Real Time Rendering
```

### Compared With

Alternative solutions.

Example:

```
Forward Rendering -> Deferred Rendering
```

### Used In Project

Practical validation.

Example:

```
RenderGraph -> Mini Renderer
```

## Rules

Use links instead of copying the same knowledge into multiple folders.
