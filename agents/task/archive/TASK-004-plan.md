# Task Plan

## Status
`closed`

## Task
- ID: TASK-004
- Title: Estructura del proyecto (CI/CD, type checker, design.md, domain.md)
- Backlog source: `agents/task/backlog.md`

## Summary
Completar la estructura del proyecto vitalXAI: configurar CI/CD con GitHub Actions, configurar type checker (mypy), y rellenar los documentos source-of-truth que quedan como plantillas vacías (design.md, domain.md).

## Scope
**In:**
1. **CI/CD (GitHub Actions)** — Workflow que ejecute lint + tests + coverage en push y PR sobre Windows
2. **Type checker (mypy)** — Configuración en pyproject.toml, stubs básicos, integración con testing.md
3. **`agents/docs/design.md`** — Rellenar con tokens de diseño reales (Tailwind CSS: colores, tipografía, componentes, layout, dark mode)
4. **`agents/db/domain.md`** — Rellenar con el modelo de dominio (User, Consultation, TrainingJob, RefreshToken, relaciones, reglas de negocio, glosario)

**Out (explicitly excluded):**
- Añadir type hints al código (parcialmente hecho en TASK-002/003, el resto se puede hacer en tarea separada)
- Refactorizar código o cambiar comportamiento
- Añadir nuevas funcionalidades
- Configurar despliegue o Docker

## Current Behavior
- Sin CI/CD: no hay GitHub Actions, no hay validación automática en PR
- Sin type checker: testing.md indica `not available`, ADR-004 lo dejó diferido
- `design.md`: plantilla vacía sin tokens de diseño
- `domain.md`: plantilla vacía sin entidades ni reglas de negocio

## Target Behavior
- GitHub Actions workflow en `.github/workflows/ci.yml` con:
  - Trigger en push y PR sobre `main` y `refactorizacion`
  - Runner: `windows-latest`
  - Steps: checkout, setup Python 3.11, cache pip, install deps (requirements.txt), ruff lint, pytest tests/ con coverage
  - Coverage threshold 70%
- mypy configurado en pyproject.toml:
  - `python_version = 3.11`
  - `warn_unused_ignores = true`
  - `ignore_missing_imports = true` (para TF, Keras, etc.)
- `design.md` completado con:
  - Paleta de colores real (slate, blue, red, green de Tailwind)
  - Tipografía (system-ui, sans-serif)
  - Componentes (botones, inputs, cards, modals, sidebar)
  - Layout y responsive
  - Dark mode strategy
- `domain.md` completado con:
  - Entidades: User, Consultation, TrainingJob, RefreshToken
  - Relaciones y FK
  - Reglas de negocio (autenticación, XAI, MLOps)
  - Glosario técnico

## Acceptance Criteria
- [ ] `.github/workflows/ci.yml` existe con workflow funcional
- [ ] Workflow ejecuta ruff lint correctamente
- [ ] Workflow ejecuta pytest tests/ con cobertura
- [ ] `mypy` configurado en pyproject.toml
- [ ] `testing.md` actualizado con comando de typecheck
- [ ] `design.md` completado con tokens reales del proyecto
- [ ] `domain.md` completado con entidades, relaciones y glosario
- [ ] Todos los tests existentes siguen pasando (≥127)
- [ ] Ruff lint pasa sin errores

## Edge Cases
- **CI/CD Windows**: Algunas dependencias (TF, Keras) son grandes. El workflow puede fallar por timeout. Considerar caching de pip.
- **mypy con TF**: TensorFlow no tiene stubs oficiales. Usar `ignore_missing_imports = true`.
- **design.md**: Tailwind vía CDN no permite extraer tokens automáticamente. Los tokens deben documentarse manualmente desde las clases usadas en las templates.

## Assumptions / Risks
- **CI/CD**: Windows runner es más lento y caro que Ubuntu pero necesario por Tkinter. Asumir uso gratuito de GitHub Actions.
- **mypy**: Enfoque estricto gradual. Configuración inicial permisiva (`ignore_missing_imports=true`), se endurecerá progresivamente añadiendo archivos al escrutinio.
- **design.md**: Los tokens se extraen de las templates existentes (dashboard.html, training.html, login.html, register.html). No hay Figma ni design system externo.

## Database Impact
Not applicable — no changes to schema or migrations.

## Open Questions
- (ninguna — todas las decisiones tomadas)

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/decisions.md`
- `agents/docs/api.md`
- `agents/db/schema.sql`
- `pyproject.toml`
- Templates: dashboard.html, training.html, login.html, register.html

## Decision Records
- ADRs read from `agents/docs/decisions.md`:
  - ADR-004: Herramientas de testing y lint (type checking diferido)
  - ADR-001 a ADR-008
- New decisions to record after user approval:
  - ADR-009: mypy para type checking
  - ADR-010: GitHub Actions CI/CD en Windows
