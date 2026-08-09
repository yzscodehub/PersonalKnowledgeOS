# Knowledge Node Specification

## Definition

Knowledge Node is an independent knowledge entity.

A Markdown file is only the storage format of the node.

## Basic Metadata

```yaml
---
title:
type:
domain:
status:
---
```

## Node Principles

- One node represents one core concept.
- Avoid combining unrelated concepts.
- Prefer linking over duplication.

## Example

PBR is a node:

```
PBR.md
```

Related nodes:

```
BRDF.md
Microfacet Theory.md
Fresnel.md
Material System.md
Shader System.md
```

Relations are expressed through links.
