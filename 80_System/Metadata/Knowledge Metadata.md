# Knowledge Metadata Specification v1.0

## Purpose

Define the minimal metadata schema for Knowledge Nodes.

Design principle:

> Metadata only stores essential machine-readable properties. Relationships are handled by links and MOC.

## Schema

```yaml
---
title:
type:
domain:
status:
---
```

## Fields

### title

Knowledge Node title.

### type

Knowledge classification.

Values:

- concept
- theory
- algorithm
- architecture
- api
- practice
- case
- comparison
- insight

### domain

Belonging knowledge domain.

Examples:

- Mathematics
- Computer Graphics
- Rendering Engine
- Artificial Intelligence

### status

Knowledge maturity.

Values:

- inbox
- learning
- understanding
- mastered
- verified
- archived
