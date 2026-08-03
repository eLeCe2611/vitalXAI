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
- TASK-010: Armonización visual completa — Clinical Clean
  - Migrar paleta de gray a slate (tonos fríos, más clínicos)
  - Refinar tipografía: mejor jerarquía (tracking-tight en títulos, mono en métricas)
  - Unificar componentes: bordes (rounded-xl/rounded-lg), sombras (shadow-sm), padding consistente
  - Botones sólidos sin gradientes llamativos, hover sutiles
  - Tablas limpias: cabecera slate, sin bordes verticales, hover en filas
  - Refactorizar login/register con aspecto de portal médico
  - Dashboard: flujo de diagnóstico más guiado, heatmaps en grid limpio
  - Training: menos púrpura, acento cyan/azul, resultados en tarjetas
  - Actualizar agents/docs/design.md con la nueva paleta y tokens



## Done
- TASK-001: Infraestructura de tests y cobertura completa (unitarios e integración)
- TASK-002: Seguridad (hashing, JWT, CSRF, rate limiting, headers, .env)
- TASK-003: Refactorización de código (trainer.py, JS inline, type hints, pooling, deprecations, deps)
- TASK-004: Estructura del proyecto (CI/CD, type checker, design.md, domain.md)
- TASK-005: Aislamiento de historiales por usuario (Diagnóstico Rápido y Laboratorio de Entrenamiento)
- TASK-006: Panel de administración para rol admin (visión global de consultas)
- TASK-007: Cola única FIFO global con prioridad para diagnósticos
- TASK-008: Sistema de internacionalización unificado
- TASK-009: Flujo de validación externa y corrección de logs
- TASK-011: Preparación de despliegue para demostración en vivo
  - Configurar túnel seguro (ngrok/Cloudflare Tunnel) para acceso externo
  - Script de inicio con un solo comando (servidor + túnel)
  - Guía rápida para el día de la defensa (conexión, URL, pasos)
