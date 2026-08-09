# Domain Design

## Purpose

Domain defines the stable classification of long-term knowledge areas.

Domain is a navigation structure, not the complete knowledge relationship model.

## Structure

```
Domain
 ├── Module
 │    └── Knowledge Node
```

## Rules

- Domain should remain stable for years.
- Avoid creating domains for temporary interests.
- Cross-domain relationships should use links, not duplicated folders.

Example:

```
Computer Graphics
 ├── Rendering Theory
 │    ├── BRDF.md
 │    └── Rendering Equation.md
 └── Material System
      └── PBR.md
```
