# Task Plan

## Status
`closed`

## Task
- ID: TASK-007
- Title: Cola única FIFO global con prioridad para diagnósticos
- Backlog source: `agents/task/backlog.md`

## Summary
Actualmente los diagnósticos rápidos y los entrenamientos se ejecutan inmediatamente sin ningún control de concurrencia. Múltiples diagnósticos y entrenamientos pueden ejecutarse en paralelo, saturando CPU/RAM/GPU. Se introduce una cola global única con un solo worker que procesa un trabajo cada vez, dando prioridad a los diagnósticos sobre los entrenamientos.

## Scope
**In:**
- Nueva tabla `job_queue` en MySQL con: id, user_id, job_type, status, payload (JSON), result (JSON), created_at, started_at, finished_at, error_message
- Worker asíncrono global (`services/queue_worker.py`): bucle que procesa un trabajo cada vez, priorizando diagnósticos sobre entrenamientos
- Modificar `POST /predict` para encolar el diagnóstico en lugar de procesarlo inline (guardar imagen primero, encolar después)
- Modificar `POST /api/train/start` para encolar el entrenamiento en lugar de usar BackgroundTasks
- Nuevo endpoint `GET /api/queue/status` que devuelve los jobs del usuario autenticado con su posición en la cola
- Arrancar el worker en el `lifespan` de FastAPI (recuperación: jobs en running → queued al iniciar)
- Panel de cola en sidebar de dashboard y training: muestra jobs pendientes del usuario y su posición
- Polling cada 5s desde frontend
- Tests unitarios para la cola y el worker

**Out (explicitly excluded):**
- No se cambia el sistema de archivos de training_results
- No se añade cancelación de trabajos (se deja para una tarea futura)
- No se limpian jobs completados de la tabla (se quedan como histórico)

## Current Behavior
- `POST /predict` procesa inferencia + XAI + PDF inline, bloqueando la request hasta terminar
- `POST /api/train/start` lanza `BackgroundTasks` con `run_training_queue`, que ejecuta `subprocess.Popen(...).wait()` secuencialmente para cada modelo
- No hay límite de concurrencia: N diagnósticos y M entrenamientos pueden correr en paralelo
- `training_log.txt` es compartido entre todas las sesiones: si dos entrenamientos corren a la vez, los logs se corrompen
- Si el servidor se reinicia, los BackgroundTasks en ejecución se pierden

## Target Behavior
- Todos los trabajos (diagnóstico y entrenamiento) se encolan en `job_queue` con status `queued`
- Un único worker asíncrono procesa un trabajo cada vez
- El worker, al elegir el siguiente trabajo, prioriza: primero todos los `queued` de tipo `diagnosis`, luego el primer `queued` de tipo `training`
- El frontend polling cada 5s muestra la posición en cola y el estado
- Al reiniciar el servidor: los jobs en estado `running` se resetean a `queued` y el worker reanuda

## Acceptance Criteria
1. `POST /predict` guarda la imagen, crea un job en `job_queue` con status=queued, devuelve `{job_id, position}`
2. `POST /api/train/start` crea un job en `job_queue` con status=queued, devuelve `{job_id, position}`
3. El worker procesa jobs uno a uno en orden: todos los diagnósticos pendientes primero, luego entrenamientos
4. `GET /api/queue/status` devuelve los jobs del usuario con su posición en la cola global
5. Al arrancar, jobs en running se resetean a queued
6. Panel en sidebar visible solo si hay jobs pendientes del usuario
7. Polling cada 5s actualiza el panel
8. Tests unitarios cubren creación de jobs, worker loop, y endpoint de status

## Edge Cases
- Worker ocupado con un entrenamiento largo: los diagnósticos se acumulan en cola y se procesan cuando termine el entrenamiento actual
- Servidor se reinicia con un job en running: se resetea a queued, se reprocesa desde el principio
- Diagnóstico falla (modelo no encontrado, imagen corrupta): job pasa a status=failed con error_message, el worker continúa con el siguiente
- Entrenamiento falla: igual, job a failed, worker continúa
- Cola vacía: worker duerme 1s y vuelve a comprobar

## Assumptions / Risks
- El worker es un `asyncio.Task` que corre en el event loop. Las operaciones bloqueantes (TF, subprocess) se ejecutan en `run_in_executor` para no bloquear el loop
- La imagen del diagnóstico se guarda en disco ANTES de encolar (para no perderla si el servidor se reinicia antes de procesarla)
- El worker necesita acceso a todas las funciones de inferencia/XAI/training. Se importan directamente desde `services/`
- Tests: se mockea el worker y la tabla job_queue para pruebas unitarias

## Database Impact
- **Change summary**: Nueva tabla `job_queue`
- **DB schema file**: `agents/db/schema.sql` (añadir CREATE TABLE)
- **DB change log file**: `agents/db/changes.sql` (añadir migración)
- **Affected structures/data**: Nueva tabla job_queue
- **Forward migration approach**: `CREATE TABLE IF NOT EXISTS job_queue (...)` en `database.py:init_db()`
- **Rollback approach**: `DROP TABLE IF EXISTS job_queue`
- **Persisted data compatibility**: No afecta a tablas existentes
- **Operational risks**: Bajo. Tabla nueva sin dependencias con las existentes
- **Validation plan**: Tests unitarios verifican inserción y lectura de jobs
- **Backup/recovery notes**: Ninguna adicional
- **Required doc updates**: `agents/docs/api.md`

## Open Questions
- *(ninguna — todas las decisiones se tomaron en la conversación previa)*

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `services/ml_engine.py` (inferencia)
- `services/xai_generator.py` (XAI)
- `services/pdf_generator.py` (PDF)
- `services/mlops_engine.py` (training pipeline)
- `routers/inference.py` (diagnóstico actual)
- `routers/trainer.py` (entrenamiento actual)
- `database.py` (init_db)
- `main.py` (lifespan)
- `templates/dashboard.html` (sidebar)
- `templates/training.html` (sidebar)
- `static/js/dashboard.js` (frontend)
- `static/js/training.js` (frontend)

## Decision Records
- ADRs read: ADR-001 (mock DB), ADR-003 (coverage threshold)
- New decisions to record after user approval:
  - Cola global única con worker único
  - Prioridad: diagnosis > training
  - Recuperación ante reinicio: running → queued
