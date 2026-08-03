# Task Plan

## Status
`closed`

## Task
- ID: TASK-009
- Title: Flujo de validación externa y corrección de logs
- Backlog source: `agents/task/backlog.md`

## Summary
La validación externa actualmente se ejecuta como `background_tasks.add_task` sin pasar por la cola, abre una vista de terminal con logs en vivo y sobrescribe `training_log.txt` con modo `"w"` (destruyendo logs de otros procesos concurrentes). Se refactorizará para encolarla como un trabajo más (tipo `external_validation`), eliminar la vista de terminal/logs, y mostrar solo un mensaje de "encolado" + estado en la cola. También se corregirá el modo de apertura de logs para no sobrescribir procesos concurrentes.

## Scope
**In:**
- Encolar validación externa en `job_queue` (tipo `external_validation`) igual que entrenamiento y diagnóstico
- Prioridad: `external_validation` y `diagnosis` al mismo nivel (FIFO por orden de llegada), ambos antes que `training`. Se modifica el `ORDER BY` en `_next_job()` para agrupar diagnosis + external_validation como prioridad 0 y training como prioridad 1.
- Añadir `_process_external_validation()` en `queue_worker.py` que llame a `mlops_engine.run_external_validation`
- Modificar `routers/trainer.py`: cambiar `background_tasks.add_task` por `INSERT INTO job_queue`
- Modificar `services/mlops_engine.py`: cambiar `open(LOG_FILE, "w")` por `open(LOG_FILE, "a")` en `run_external_validation` y `run_statistical_comparison`
- Modificar `static/js/training.js`: `launchExternalValidation()` ya no muestra terminal ni hace polling de logs; solo muestra mensaje de "Validación externa encolada" y el frontend detecta finalización vía cola
- Limpiar salida verbose de subprocess en scripts de validación externa, wilcoxon y XAI (redirigir stdout/stderr a nul o suprimirlo)

**Out (explicitamente excluido):**
- UI de progreso en tiempo real para validación externa (solo cola + notificación de finalización)
- No se toca el flujo de diagnóstico ni entrenamiento existente
- No se añaden tests nuevos para este flujo (a menos que surja naturalmente)

## Current Behavior
- `POST /api/train/session/external_validation` ejecuta `background_tasks.add_task(mlops_engine.run_external_validation, ...)` — se ejecuta inmediatamente sin cola, en paralelo con otros procesos
- `run_external_validation` abre `training_log.txt` con `"w"` (sobrescribe), borrando logs de otros entrenamientos en ejecución
- `run_statistical_comparison` también abre con `"w"` (mismo problema)
- `launchExternalValidation()` en training.js: abre selector de carpeta, oculta panel de resultados, muestra terminal con spinner, lanza fetch POST, hace polling cada 2s de logs hasta detectar `[VALIDACIÓN EXTERNA COMPLETADA]`
- Los scripts subprocess (4, 5) escriben todo su stdout/stderr al log, saturándolo con verbose warnings

## Target Behavior
- `POST /api/train/session/external_validation` inserta en `job_queue` con `job_type='external_validation'` y prioridad FIFO (diagnosis > external_validation > training)
- `queue_worker.py` procesa `external_validation` igual que `diagnosis` y `training`
- `_next_job()` en `queue_worker.py`: modificar ORDER BY para que diagnosis y external_validation tengan misma prioridad (0), training prioridad 1
- `run_external_validation` y `run_statistical_comparison` usan `"a"` (append) en lugar de `"w"`
- `launchExternalValidation()` en frontend: abre selector de carpeta, POST para encolar, muestra toast flotante "Validación externa encolada como trabajo #N". No muestra terminal ni hace polling de logs.
- `pollQueue` en admin.js detecta cuando un trabajo `external_validation` pasa a `completed`. Si el usuario está viendo la sesión correspondiente (`currentViewingSession`), auto-recarga `viewSessionResults()`.
- La cola (pollQueue) muestra el estado del trabajo en la sidebar como siempre.
- Los scripts subprocess redirigen stdout/stderr para evitar inundar el log con warnings.

## Acceptance Criteria
- [ ] La validación externa se encola como un trabajo más, visible en la cola de la sidebar
- [ ] No se abre vista de terminal al lanzar validación externa
- [ ] Aparece un mensaje "Validación externa encolada" como notificación
- [ ] Los logs de entrenamiento en ejecución no se sobrescriben al lanzar validación externa
- [ ] `run_statistical_comparison` tampoco sobrescribe logs
- [ ] La validación externa completa se detecta vía cola y los resultados son accesibles desde la sesión
- [ ] Tests existentes siguen pasando

## Edge Cases
- Si se lanza validación externa mientras hay entrenamientos en cola, se procesa antes que entrenamientos. Si hay diagnósticos previos, se respeta FIFO.
- Si se lanza validación externa y diagnosis al mismo tiempo, se procesan por orden de llegada (FIFO)
- Si el dataset externo no existe, se rechaza antes de encolar (como ahora)
- Si la sesión no pertenece al usuario, 403 (como ahora)
- Si el usuario cierra la página mientras la validación está en cola, el trabajo se completa igual en segundo plano

## Assumptions / Risks
- Se modificará el ORDER BY para: `CASE WHEN job_type = 'training' THEN 1 ELSE 0 END`, así diagnosis y external_validation comparten prioridad 0 (FIFO), training prioridad 1
- Riesgo: si hay muchos trabajos previos (diagnosis + external_validation), la validación externa podría tardar. El usuario debe saber que está en cola.

## Database Impact
Not applicable. La tabla `job_queue` ya tiene `job_type VARCHAR(20)` que soporta `'external_validation'`. No se requiere migración.

## Open Questions
(Preguntas resueltas durante la planificación — ver Decisiones Tomadas)

## Decisiones Tomadas
1. **Tipo de trabajo**: `job_type = 'external_validation'` — la tabla ya lo soporta
2. **Prioridad**: Diagnosis y external_validation misma prioridad (FIFO por id), training después. Se modifica ORDER BY en `_next_job()`.
3. **Feedback al usuario**: Toast/notificación flotante "Validación externa encolada como trabajo #N" + estado visible en cola lateral
4. **Finalización**: Auto-refresh — si el usuario está en la página de la sesión al completarse, se recarga la vista automáticamente. Si no, lo ve en la cola y abre manualmente.
4. **Logs**: append (`"a"`) en lugar de overwrite (`"w"`) para no destruir logs concurrentes

## Source of Truth to Read
- `agents/task/backlog.md`
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/api.md`
- `routers/trainer.py` (línea 192 — ruta external_validation actual)
- `services/mlops_engine.py` (línea 81 — run_external_validation)
- `services/queue_worker.py` (líneas 116-165 — _process_training, _execute_job)
- `static/js/training.js` (líneas 266-278 — launchExternalValidation)
- `database.py` (esquema job_queue)

## Decision Records
- ADRs read: ADR-007 (cola FIFO), ADR-010 (CI). Ninguna relevante al cambio.
- New decisions: Ninguna.
