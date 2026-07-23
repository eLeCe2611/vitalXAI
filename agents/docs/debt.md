# Technical Debt

Registry of bugs, issues, improvements, or incidents the agent finds while working on a task that are outside the current task's scope.

When the agent encounters something relevant but out of scope, it must log it here instead of modifying it without permission. The user periodically reviews the log and decides whether to create a formal task.

## Statuses
- `open`: pending user review.
- `dismissed`: the user decided not to address it.

## Format

```md
## DBT-XXX: Short title
Date: YYYY-MM-DD
Status: open | dismissed
Risk: low | medium | high
Impact: low | medium | high
Suggested priority: low | medium | high | critical
Evidence: Related file(s), line(s), or link.
Description: Explanation of the problem.
Recommendation: What to do to resolve it.
```

## Log

## DBT-001: Contraseñas en texto plano (auth.py)
Date: 2026-07-23
Status: resolved (TASK-002)
Risk: high
Impact: high
Suggested priority: critical
Evidence: `routers/auth.py:19,126`
Description: Las contraseñas se comparaban directamente como strings en la BD.
Recommendation: Implementado bcrypt hashing en TASK-002.

## DBT-002: API Key de Groq hardcodeada (trainer.py)
Date: 2026-07-23
Status: resolved (TASK-002)
Risk: high
Impact: high
Suggested priority: critical
Evidence: `routers/trainer.py:26`
Description: GROQ_API_KEY hardcodeada visible en el código fuente.
Recommendation: Movido a variable de entorno (os.getenv) en TASK-002.

## DBT-003: Cobertura de tests en trainer.py (33%) y xai_generator.py (48%)
Date: 2026-07-23
Status: open
Risk: medium
Impact: medium
Suggested priority: medium
Evidence: Coverage report (58% total, trainer.py 33%, xai_generator.py 48%)
Description: Estas rutas tienen lógica compleja (subprocess, TF, matplotlib) que es difícil de mockear.
Recommendation: Añadir tests de integración con SQLite en TASK-002.

## DBT-004: Integration tests pendientes
Date: 2026-07-23
Status: open
Risk: medium
Impact: low
Suggested priority: low
Evidence: Checklist item 12
Description: Los tests de integración (auth flow, prediction E2E) se pospusieron.
Recommendation: Implementar en TASK-002 con SQLite en memoria.

## DBT-006: Deprecation warnings de librerías
Date: 2026-07-23
Status: open
Risk: low
Impact: low
Suggested priority: low
Evidence: `routers/trainer.py` (fpdf2 deprecated params), `main.py:21` (`@app.on_event`), `auth.py` (`TemplateResponse` deprecated signature)
Description: Múltiples deprecation warnings de fpdf2 (ln=True, font Arial), FastAPI (on_event), y Starlette (TemplateResponse). No bloqueantes pero requerirán migración.
Recommendation: Abordar en TASK-002 como parte de la refactorización.

## DBT-005: Ruff lint warnings no críticos
Date: 2026-07-23
Status: open
Risk: low
Impact: low
Suggested priority: low
Evidence: Ruff output (W293, W291, I001, F401, etc.)
Description: Quedan ~14 lint warnings en código productivo y pneumoniacnn-main/ (trailing whitespace, import order, etc.).
Recommendation: Limpiar en TASK-002 con `ruff check --fix`. Los issues en `pneumoniacnn-main/` requieren coordinación.
