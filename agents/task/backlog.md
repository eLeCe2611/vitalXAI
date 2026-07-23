# Backlog

Use this file as the task queue. Keep only one task under `## Current`.

Task format:

```md
- TASK-XXX: Short task title
```

When work starts on a current task, create:
- `agents/task/TASK-XXX-plan.md`
- `agents/task/TASK-XXX-checklist.md`

When the task is complete and the user approves closeout, move the task to `## Done` and move its task files to `agents/task/archive/` in the same step.

## Current


## To do
- TASK-003: Refactorización de código (trainer.py, JS inline, type hints, pooling, deprecations, deps)
- TASK-004: Estructura del proyecto (CI/CD, type checker, design.md, domain.md)

## Done
- TASK-001: Infraestructura de tests y cobertura completa (unitarios e integración)
- TASK-002: Seguridad (hashing, JWT, CSRF, rate limiting, headers, .env)
