# MOC Design

## Definition

MOC (Map of Content) is a knowledge navigation layer.

It is not a storage location for knowledge. It organizes learning paths and entry points into the Knowledge Graph.

## Responsibilities

- Provide learning roadmap
- Organize important nodes
- Connect cross-domain knowledge
- Provide overview of a topic

## Example

PBR MOC:

```
Mathematics
    ↓
Optics
    ↓
Rendering Equation
    ↓
BRDF
    ↓
Microfacet Theory
    ↓
PBR
    ↓
Material System
    ↓
Engine Implementation
```

## Rules

- MOC should reference nodes, not contain duplicate knowledge.
- Multiple MOCs can reference the same Knowledge Node.
- MOC describes paths, not ownership.
