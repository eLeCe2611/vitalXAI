# Task Checklist

## Source
- Task: TASK-009
- Plan: `agents/task/TASK-009-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs.
- [x] Load and apply TDD skill — pre-existing code modifications, regression tests not affected (all 182 pass).
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. Queue: add external_validation support
- [x] Modificar `queue_worker.py._next_job()`: ORDER BY ahora da prioridad 0 a diagnosis + external_validation, prioridad 1 a training
- [x] Añadir `_process_external_validation(job)` en `queue_worker.py`
- [x] Añadir `external_validation` al `if/elif` en `_execute_job(job)`

### 3. Router: enqueue instead of background task
- [x] Modificar `routers/trainer.py`: `background_tasks.add_task` reemplazado por `INSERT INTO job_queue` con `job_type='external_validation'`
- [x] Devuelve `{"status": "queued", "job_id": ..., "message": "...encolada como trabajo #N"}`
- [x] Añadida clave `validacion_externa_encolada` en `services/lang.py` para 4 idiomas

### 4. Logs: fix overwrite mode
- [x] `mlops_engine.py.run_external_validation`: cambiado `"w"` a `"a"`
- [x] `mlops_engine.py.run_statistical_comparison`: cambiado `"w"` a `"a"`

### 5. Frontend: simplify launchExternalValidation
- [x] `training.js.launchExternalValidation()`: eliminada terminal, spinner, y polling de logs
- [x] Muestra toast flotante vía `showToast()` con mensaje de encolado
- [x] Añadida función `showToast()` en `i18n.js`
- [x] Añadida clave `queueEnqueuedExt` en i18n.js para 4 idiomas

### 6. Frontend: auto-refresh on completion
- [x] `admin.js.pollQueue()`: detecta jobs `external_validation` completados y si `currentViewingSession` coincide, auto-recarga `viewSessionResults()`
- [x] `queue.py`: añadido soporte para `job_type='external_validation'` (extraer session_id del payload)
- [x] `queue.py`: ORDER BY actualizado para prioridad FIFO correcta
- [x] Añadida clave `queueExtValidation` en i18n.js para 4 idiomas

### 7. Scope and Docs
- [x] All implementation items complete.
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] Out-of-scope findings: none.
- [x] Sync check: implemented code matches plan.

### 8. Database Change Controls
Not applicable — no schema changes needed.

### 9. Validation
- [x] Targeted tests: 178 unit tests passed
- [x] Full test suite: 182 tests passed
- [x] Lint: `ruff check .` — all checks passed
- [x] DoD `in_progress` criteria checked.

### 10. Closeout (→ `closed`)
- [x] Ask user before marking backlog task done.
- [x] Update the plan status to `closed` before archiving task files.
- [x] Move task files to `agents/task/archive/` after user approves.
