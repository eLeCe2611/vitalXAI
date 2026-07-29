# Task Plan

## Status
`closed`

## Task
- ID: TASK-005
- Title: Aislamiento de historiales por usuario (Diagnóstico Rápido y Laboratorio de Entrenamiento)
- Backlog source: `agents/task/backlog.md`

## Summary
El historial de consultas del Diagnóstico Rápido ya se almacena asociado al usuario (`user_id`), pero los endpoints `update_name` y `delete` no verifican que la consulta pertenezca al usuario autenticado. El Laboratorio de Entrenamiento no tiene ningún tipo de aislamiento: todas las sesiones MLOps se almacenan en el sistema de archivos sin asociación a usuario, y ningún endpoint verifica autenticación ni ownership. Se añadirá control de acceso en ambas pestañas.

## Scope

**In:**
- Diagnóstico Rápido: añadir verificación de `user_id` en `POST /api/history/update_name` y `POST /api/history/delete`
- Laboratorio de Entrenamiento:
  - Añadir verificación JWT (`get_user_id_from_token`) a todos los endpoints de `trainer.py`
  - Modificar `mlops_engine.create_training_session()` para aceptar y almacenar `user_id` en el `config.json` de la sesión
  - Modificar `get_trained_sessions()` para filtrar solo las sesiones del usuario autenticado
  - Modificar el resto de funciones que acceden/modifican sesiones (`delete_session`, `safe_rename`, `get_model_results_data`, `get_session_ranking_data`, `resolve_dataset_path`, `get_external_results_data`, `run_xai_evaluation`, `run_statistical_comparison`, `run_external_validation`) para verificar ownership
- Migración: asignar las 4 sesiones existentes a usuarios concretos añadiendo `user_id` a su `config.json`
- Tests: actualizar tests existentes y añadir nuevos tests que cubran la verificación de ownership

**Out (explicitly excluded):**
- No se crean tablas nuevas en BD — se usa `user_id` en `config.json` (sistema de archivos)
- No se modifican las rutas de archivos estáticos (`/training_results/`) — las URLs de imágenes/PDF son opacas (session_id aleatorio), la seguridad se aplica en la capa de API
- No se modifican los endpoints de auth ni el sistema de usuarios
- No se refactoriza el motor de subprocess del pipeline MLOps

## Current Behavior

### Diagnóstico Rápido
- `GET /api/history` ya filtra por `WHERE user_id = %s` correctamente
- `POST /predict` ya guarda con `user_id` del token correctamente
- `POST /api/history/update_name` actualiza cualquier consulta por `id` sin verificar que pertenezca al usuario
- `POST /api/history/delete` elimina cualquier consulta por `id` sin verificar que pertenezca al usuario

### Laboratorio de Entrenamiento
- Ningún endpoint en `trainer.py` extrae el `user_id` del JWT
- `create_training_session()` en `mlops_engine.py` no recibe ni almacena `user_id`
- `get_trained_sessions()` lista todas las sesiones del sistema de archivos sin filtrar
- `delete_session`, `safe_rename`, y el resto de funciones operan sin verificar propiedad
- Los archivos estáticos de `training_results/` están montados como `StaticFiles` globalmente en `main.py:44`

## Target Behavior

### Diagnóstico Rápido
- `POST /api/history/update_name` verifica que `consultation.user_id == current_user_id` antes de actualizar
- `POST /api/history/delete` verifica que `consultation.user_id == current_user_id` antes de eliminar
- Si no coincide, devuelve 403 Forbidden

### Laboratorio de Entrenamiento
- Todos los endpoints de `trainer.py` requieren JWT válido (devuelven 401 si no)
- `create_training_session()` recibe `user_id` y lo guarda en `config.json`
- `get_trained_sessions()` filtra solo las sesiones del usuario autenticado
- `delete_session`, `safe_rename`, y el resto verifican ownership (devuelven 403 si no coincide)
- Las sesiones MLOps se comportan como datos privados por usuario

## Acceptance Criteria

1. `POST /api/history/update_name` rechaza con 403 si la consulta no pertenece al usuario autenticado
2. `POST /api/history/delete` rechaza con 403 si la consulta no pertenece al usuario autenticado
3. `GET /api/train/models` solo devuelve sesiones del usuario autenticado
4. `GET /api/train/results/{session_id}/{model_name}` devuelve 403 si la sesión no pertenece al usuario
5. `DELETE /api/train/session/{session_id}` devuelve 403 si la sesión no pertenece al usuario
6. `POST /api/train/session/rename` devuelve 403 si la sesión no pertenece al usuario
7. `POST /api/train/run_eval` devuelve 403 si la sesión no pertenece al usuario
8. `POST /api/train/session/compare` devuelve 403 si la sesión no pertenece al usuario
9. `GET /api/train/session/{session_id}/ranking` devuelve 403 si la sesión no pertenece al usuario
10. `POST /api/train/session/external_validation` devuelve 403 si la sesión no pertenece al usuario
11. `GET /api/train/session/{session_id}/external_results` devuelve 403 si la sesión no pertenece al usuario
12. `GET /api/train/session/{session_id}/report` devuelve 403 si la sesión no pertenece al usuario
13. Todos los endpoints de entrenamiento devuelven 401 si no hay JWT válido
14. Las 4 sesiones existentes están asignadas a usuarios y visibles solo por ellos
15. Tests unitarios existentes siguen pasando
16. Nuevos tests cubren los casos de ownership denegado

## Edge Cases
- **Sesión sin `user_id` en config.json** (migración incompleta): tratarla como "no pertenece a nadie", devolver 404
- **Token expirado o inválido**: devolver 401, no filtrar silenciosamente
- **Grace period de refresh token**: el `get_user_id_from_token` solo verifica access token; si expiró, el frontend debe refrescar antes. Esto ya funciona en el sistema actual.
- **CSRF**: los nuevos endpoints POST/DELETE ya requieren CSRF por el middleware global — no hay cambios necesarios
- **Concurrencia**: `delete` y `update_name` no tienen bloqueo; es aceptable para el ámbito del TFG

## Assumptions / Risks
- El `config.json` de cada sesión es la fuente de verdad para el `user_id`
- La ruta estática `/training_results/` queda accesible globalmente — las URLs contienen el session_id (nombre opaco), pero un usuario podría acceder directamente a imágenes de otra sesión si adivina el nombre. Esto es aceptable para el TFG, pero sería mejor servirlas a través de un endpoint autenticado en producción.
- Los tests existentes que usan mock de DB y mock de TF seguirán funcionando; los nuevos tests añadirán mocks de ownership

## Database Impact
Not applicable — no se modifican tablas. La ownership se almacena en `config.json` en el sistema de archivos.

## Open Questions

Por resolver antes de aprobar:

*(Resueltas — ver sección Decision Records)*

## Source of Truth to Read
- `agents/docs/DoD.md` ✓
- `agents/docs/testing.md` ✓
- `agents/docs/decisions.md` ✓ (ADRs revisados: no hay conflictos)
- `agents/docs/api.md` ✓
- `routers/history.py` ✓
- `routers/trainer.py` ✓
- `services/ml_engine.py` ✓
- `services/mlops_engine.py` ✓
- `database.py` ✓

## Decision Records
- ADRs read from `agents/docs/decisions.md`: ADR-001 (mock DB), ADR-002 (mock TF), ADR-006 (JWT auth), ADR-008 (refresh token rotation)
- New decisions to record after user approval: Ninguna (el enfoque es incremental, no introduce nuevas dependencias ni patrones arquitectónicos duraderos)

## Resolved Open Questions
- **Sesiones existentes:** `soloCNN` → admin, `soloTransformers` → admin, `deTodo` → admin, `RUN_20260724_021631` → jperez (ID 3)
- **Actualizar `api.md`:** Sí, documentar que los endpoints de entrenamiento requieren auth y devuelven 401/403
