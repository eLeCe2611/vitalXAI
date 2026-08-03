# TASK-011 Checklist

## Source
- Task: TASK-011
- Plan: `agents/task/TASK-011-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs (do not skip even if read during planning).
- [x] Load and apply `agents/skills/test-driven-development/SKILL.md`, or record why it does not apply.
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. TDD Ledger
- [x] Behavior 1 — `browse_folder` devuelve `TFG_DEMO_DATASET` sin abrir Tkinter cuando la variable está definida (RED → GREEN → REFACTOR).
- [x] Behavior 2 — `browse_folder(for_external=True)` devuelve `TFG_DEMO_EXTERNAL_DATASET` cuando está definida.
- [x] Behavior 3 — `browse_folder` sin variables de demo conserva el diálogo Tkinter (regresión).
- [x] Behavior 4 — endpoint `GET /api/train/browse` acepta `for_external` y lo propaga a `browse_folder`.
- [x] Behavior 5 — `training.js` envía `for_external=true` desde la llamada de validación externa.

### 3. Scope and Docs
- [x] Scripts `scripts/demo_start.ps1` y `scripts/demo_start.bat` creados (CWD fijo, prechecks `.env`/MySQL, uvicorn sin reload, túnel cloudflared/ngrok, `demo_url.txt`).
- [x] `.env.example` actualizado con `TFG_DEMO_DATASET`, `TFG_DEMO_EXTERNAL_DATASET`, `TUNNEL_PROVIDER` (opcionales).
- [x] `Documentacion/Guia_Despliegue_Demo.md` creada (instalación, configuración, arranque, URL, flujo demo, troubleshooting, plan B, localhost.run como plan C).
- [x] `agents/docs/api.md` actualizada con el parámetro `for_external` de `/api/train/browse`.
- [x] All TDD cycles complete or documented as approved exceptions.
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] Out-of-scope findings registered in `agents/docs/debt.md`. (Sin hallazgos fuera de alcance; nada registrado.)
- [x] Sync check: compare implemented code against affected source-of-truth docs from the plan. Discrepancies → stop and ask user. Resolve before proceeding.
- [x] Durable docs updated (`agents/docs/api.md`, DB files from the Source of Truth Map, `agents/docs/design.md`, etc.) as needed.

### 4. Database Change Controls
`Not applicable` — la tarea no afecta a la base de datos.

### 5. Validation (still `in_progress`)
- [x] Targeted tests: unitarios de `browse_folder` y del endpoint `/api/train/browse`.
- [x] Full test suite: `python -m pytest tests/`.
- [x] Lint: `ruff check .`.
- [x] Typecheck: `python -m mypy` (sin cambios en los módulos escrutinados; registrar si aplica).
- [x] Build: not available (según `agents/docs/testing.md`).
- [x] DoD `in_progress` criteria checked.

### 6. Closeout (→ `closed`)
- [x] Ask user before marking backlog task done.
- [x] Update the plan status to `closed` before archiving task files.
- [x] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
- Implementación completada y validada (190 tests, cobertura 73.72%, ruff/mypy limpios).
- Revisión independiente (subagente) sin bugs pendientes tras el arreglo de `TUNNEL_PROVIDER` desde `.env`.
- Notas de la revisión: la demo expone la app públicamente (inherente al plan); Ctrl+C no limpia procesos (usar Enter, documentado en la guía).
- Pendiente de closeout (solo con aprobación del usuario): ADR-011, marcar backlog como done, archivar task files.
