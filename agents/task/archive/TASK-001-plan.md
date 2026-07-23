# Task Plan

## Status
`closed`

## Task
- ID: TASK-001
- Title: Infraestructura de tests y cobertura completa (unitarios e integración)
- Backlog source: `agents/task/backlog.md`

## Summary
El proyecto tiene 0 tests y va a ser refactorizado (TASK-002). Sin una red de seguridad es imposible refactorizar con garantías siguiendo TDD. Esta tarea crea toda la infraestructura de testing, escribe tests para absolutamente todos los módulos actuales, y documenta los contratos de API actuales antes de modificarlos.

## Scope
**In:**
- Instalar y configurar pytest y plugins necesarios (pytest-cov, pytest-mock, etc.)
- Definir estructura de directorios de tests (`tests/unit/`, `tests/integration/`)
- Configurar base de datos de test (ver pregunta abierta sobre estrategia)
- Escribir tests unitarios para `services/ml_engine.py` (mockeando TensorFlow y OpenCV)
- Escribir tests unitarios para `services/xai_generator.py` (mockeando matplotlib y TF)
- Escribir tests unitarios para `services/pdf_generator.py` (mockeando fpdf2)
- Escribir tests unitarios para `services/trainer_engine.py` (mockeando TF y sklearn)
- Escribir tests unitarios para `routers/auth.py` (mockeando DB y cookies)
- Escribir tests unitarios para `routers/history.py` (mockeando DB)
- Escribir tests unitarios para `routers/inference.py` (mockeando servicios y DB)
- Escribir tests unitarios para `routers/trainer.py` (mockeando Groq, subprocess, Tkinter, DB)
- Escribir tests unitarios para `database.py`
- Escribir tests de integración para rutas API clave con DB real o testcontainer
- Poblar `agents/docs/testing.md` con comandos reales, ubicaciones, y configuración
- Poblar `agents/docs/api.md` con los contratos actuales de las rutas
- Configurar comando de lint (ruff o similar)
- Verificar que todos los tests pasan

**Out (explicitly excluded):**
- Tests E2E con navegador real (serían para otra tarea)
- Tests del submódulo `pneumoniacnn-main/code/` (scripts independientes que se ejecutan por subprocess; se mockean a nivel de subprocess)
- Refactorización del código productivo (es TASK-002)
- Cambios en `AGENTS.md` modo (sigue en skeleton)

## Current Behavior
- Zero tests en todo el proyecto
- No hay test runner configurado
- No hay configuración de lint ni typecheck
- `agents/docs/testing.md` está vacío (solo template)
- `agents/docs/api.md` está vacío (solo template)
- Las dependencias del proyecto (TF, Keras, Groq, Tkinter, subprocess) hacen que tests sin mocks sean inviables en CI

## Target Behavior
- `pytest` funciona con un solo comando y ejecuta todos los tests
- Cada módulo tiene tests unitarios que cubren casos normales, bordes y errores
- Las dependencias externas (TF, Groq, subprocess, MySQL) están mockeadas en tests unitarios
- `agents/docs/testing.md` documenta comandos, estructura, ubicaciones, y configuración
- `agents/docs/api.md` documenta todas las rutas actuales con method, path, request, response
- Cobertura mínima del 80% en módulos productivos (definir threshold exacto durante planificación)
- Lint (ruff) configurado y pasando

## Acceptance Criteria
- [ ] `pytest tests/` ejecuta todos los tests sin errores
- [ ] Cada router y service tiene al menos un test file
- [ ] Los tests unitarios no requieren MySQL, GPU, ni API keys externas
- [ ] `agents/docs/testing.md` tiene comandos funcionales (targeted unit, full unit, lint)
- [ ] `agents/docs/api.md` lista todas las rutas con sus contratos actuales
- [ ] Cobertura mínima del 50% en `services/` y `routers/` (threshold real; 80% es objetivo para TASK-002)
- [ ] Ruff configurado y pasando sin errores

## Edge Cases
- `trainer.py` línea 158-165 usa Tkinter (`filedialog.askdirectory`) que abre UI nativa — debe mockearse a nivel de API
- `trainer.py` línea 30 tiene API key de Groq hardcodeada — el test no debe depender de que la key sea válida
- `ml_engine.py` carga modelos TF reales en caché — los tests unitarios deben evitar la carga real
- Las rutas usan `request.cookies.get("session_token")` — los tests de rutas deben simular cookies
- Algunos routers (`auth.py`) ejecutan SQL directo sin ORM — los tests deben mockear `get_db_connection`

## Assumptions / Risks
- **Riesgo alto**: TensorFlow/Keras son difíciles de mockear limpiamente. Los tests de `ml_engine.py` pueden requerir parches a nivel de `tf.keras.models.load_model` y `cv2`.
- **Riesgo medio**: `trainer_engine.py` entrena modelos reales con `model.fit` — mockear todo el pipeline TF es complejo pero factible con `unittest.mock`.
- **Riesgo medio**: El proyecto usa `mysql-connector-python` sin pool ni ORM — la estrategia de BD de test impacta en cómo se escriben los tests de integración.
- **Asunción**: Usaremos `pytest` como test runner (estándar de facto en Python).
- **Asunción**: Usaremos `ruff` para lint (rápido, moderno, reemplaza flake8/isort).

## Database Impact
- Change summary: No se modifica el esquema de BD. Solo se añade soporte para BD de test (ver pregunta abierta).
- DB schema file: `agents/db/schema.sql` (se poblará con el schema real de `users` y `consultations`)
- DB change log file: `agents/db/changes.sql` (sin cambios)
- Affected structures/data: Ninguna
- Forward migration approach: N/A
- Rollback approach: N/A
- Persisted data compatibility: N/A
- Operational risks: Ninguno
- Validation plan: Tests verifican que mock DB funciona
- Backup/recovery notes: N/A
- Required doc updates: `agents/db/schema.sql` se poblará con las tablas reales

## Open Questions

### ✅ Decisiones tomadas

| Decisión | Opción elegida |
|----------|---------------|
| Estrategia BD | Mock `get_db_connection` en unitarios; SQLite en integración |
| Mock TF/Keras | Mock a nivel de `load_model` y `from_pretrained` con objetos mock |
| Cobertura mínima | **80%** en `services/` y `routers/` |
| Configuración | `pyproject.toml` unificado (pytest, ruff, pytest-cov) |
| Estructura tests | `tests/unit/` + `tests/integration/` |
| Fixtures globales | `tests/conftest.py` con fixtures compartidas |

### 3. Pendiente de implementación
Detalles que se resolverán durante la implementación sin necesidad de pregunta explícita:
- Plugins pytest exactos (pytest-cov, pytest-mock)
- Reglas de ruff a aplicar/ignorar
- Contenido exacto de `conftest.py`

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md` (template vacío)
- `agents/docs/api.md` (template vacío)
- `agents/docs/decisions.md` (sin ADRs todavía)
- `agents/db/schema.sql` (vacío)

## Decision Records
- ADRs read from `agents/docs/decisions.md`: Ninguno (vacío)
- New decisions to record after user approval: Decisión de estrategia de BD de test y tooling
