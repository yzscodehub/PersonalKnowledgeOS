# Project Metadata Specification v1.0

## Purpose

Define metadata for projects.

## Schema

```yaml
---
title:
type: project
status:
---
```

## Fields

### title

Project name.

### type

Fixed as project.

### status

Project lifecycle.

Values:

- planning
- active
- paused
- completed
- archived
