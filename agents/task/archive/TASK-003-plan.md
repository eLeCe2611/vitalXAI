# Task Plan

## Status
`closed`

## Task
- ID: TASK-003
- Title: Refactorización de código (trainer.py, JS inline, type hints, pooling, deprecations, deps)
- Backlog source: `agents/task/backlog.md`

## Summary
Refactorizar la calidad del código del proyecto vitalXAI: dividir el monolito `trainer.py` (528 líneas) en módulos más pequeños y cohesionados, extraer el JavaScript inline de las templates HTML a archivos `.js` separados, añadir type hints gradualmente, implementar connection pooling en la base de datos, corregir deprecation warnings acumulados, y limpiar dependencias no usadas.

## Scope
**In:**
1. **División de trainer.py** — Separar en módulos: `services/chatbot_router.py`, `services/mlops_engine.py`, `services/pdf_generator_mlops.py`. `routers/trainer.py` queda como fachada ligera.
2. **Extracción de JS inline** — Mover JS de `dashboard.html` y `training.html` a `static/js/dashboard.js` y `static/js/training.js`. Pasar variables Jinja2 mediante atributos `data-*` en HTML.
3. **Type hints** — Añadir type hints en TODOS los routers (`auth.py`, `history.py`, `inference.py`, `trainer.py`), TODOS los services (`auth_service.py`, `csrf_middleware.py`, `rate_limiter.py`, `ml_engine.py`, `xai_generator.py`, `pdf_generator.py`, `trainer_engine.py`), y `database.py`.
4. **Connection pooling** — Reemplazar conexiones directas en `database.py` con `mysql.connector.pooling.MySQLConnectionPool`.
5. **Deprecation warnings** — Corregir: fpdf2 (`Arial` → `helvetica`, `ln=True` → `new_x`/`new_y`), FastAPI (`@app.on_event` → lifespan handlers), Starlette (`TemplateResponse(name, ...)` → `TemplateResponse(request, name, ...)`).
6. **Limpieza de dependencias** — Eliminar `psycopg2-binary`, `pymongo`, `redis` de requirements.txt.

**Out (explicitly excluded):**
- Cambios de comportamiento en endpoints o lógica de negocio
- Refactorización de templates HTML (estructura visual, diseño)
- Configuración de type checker (mypy/pyright) — diferido a TASK-004
- CI/CD, design.md, domain.md — diferido a TASK-004
- Nuevas funcionalidades o endpoints

## Current Behavior
- `routers/trainer.py` monolítico de 528 líneas con chatbot, motor MLOps, generación de PDF, y 17 endpoints API mezclados
- `templates/dashboard.html` (346 líneas) y `training.html` (667 líneas) con JavaScript inline en múltiples bloques `<script>`
- Sin type hints en toda la base de código (salvo algunos añadidos en TASK-002)
- `database.py` crea una nueva conexión MySQL en cada llamada a `get_db_connection()`, sin pooling
- 15 referencias a `Arial` y 11 usos de `ln=True` en fpdf2 (deprecados desde v2.5.2 y v2.7.8)
- `main.py:21` usa `@app.on_event("startup")` (deprecado desde FastAPI 0.111+)
- 4 llamadas a `TemplateResponse(name, {"request": request})` con firma deprecada
- `psycopg2-binary`, `pymongo`, `redis` en requirements.txt pero sin uso en el código

## Target Behavior
- `trainer.py` dividido en: `services/chatbot_router.py` (chat IA), `services/mlops_engine.py` (subprocess/entrenamiento), `services/pdf_generator_mlops.py` (PDF MLOps), `routers/trainer.py` (solo rutas ligeras)
- JS extraído a `static/js/dashboard.js` y `static/js/training.js`, con importación vía `<script src="...">`
- Type hints añadidos en módulos clave (auth_service, csrf_middleware, auth router, database)
- `database.py` usa `mysql.connector.pooling.MySQLConnectionPool` para reutilizar conexiones
- Sin deprecation warnings de fpdf2, FastAPI, ni Starlette
- requirements.txt limpio de dependencias no utilizadas

## Acceptance Criteria
- [ ] `trainer.py` dividido en al menos 3 módulos; `routers/trainer.py` < 100 líneas
- [ ] Todos los endpoints actuales de trainer siguen funcionando (tests pasan)
- [ ] JS de dashboard.html y training.html extraído a archivos externos
- [ ] Funcionalidad frontend idéntica tras la extracción (tests de integración pasan)
- [ ] Type hints en auth_service.py, csrf_middleware.py, auth.py, database.py
- [ ] Connection pooling implementado con tamaño de pool configurable
- [ ] Sin deprecation warnings de fpdf2, FastAPI, Starlette en la salida de tests
- [ ] psycopg2-binary, pymongo, redis eliminados de requirements.txt
- [ ] Todos los tests existentes pasan (≥126)
- [ ] Cobertura global ≥ 70%
- [ ] Ruff lint pasa sin errores

## Edge Cases
- **trainer.py split**: Los tests existentes importan funciones de `routers.trainer`. Asegurar compatibilidad backwards o actualizar imports.
- **JS extraction**: El JS inline usa variables de template Jinja2 (`{{ full_name }}`, `{{ role }}`). Estas deben pasarse al JS externo mediante `data-` attributes en HTML o un bloque inline mínimo.
- **Connection pooling**: El pool debe cerrarse gracefulmente al apagar la app. Tamaño de pool por defecto razonable (5-10 conexiones).
- **Deprecation warnings**: Al cambiar `@app.on_event` a lifespan, la función `init_db()` debe ejecutarse en el mismo momento (startup).
- **Type hints**: No romper la compatibilidad con Python 3.11. Usar `from __future__ import annotations` si es necesario.

## Assumptions / Risks
- **trainer.py split**: Alto riesgo de romper tests existentes. Se requiere plan de migración cuidadoso con TDD.
- **JS extraction**: El JS de training.html (667 líneas) es grande y está acoplado al HTML. Puede requerir refactorización adicional.
- **Connection pooling**: MySQL Connector/Python soporta pooling nativamente. Configuración simple.
- **Deprecation fixes**: Cambios mecánicos, bajo riesgo. Verificar cada cambio con tests.
- **Type hints**: Solo añadir tipos, no cambiar lógica. Riesgo bajo pero laborioso.

## Database Impact
- **Change summary**: Connection pooling en `database.py`. No cambia esquema.
- **DB schema file**: `agents/db/schema.sql` — sin cambios
- **DB change log file**: `agents/db/changes.sql` — sin cambios
- **Affected structures/data**: Ninguno
- **Operational risks**: Pool de conexiones puede tener límite superior. Configurar `pool_size` y `pool_name` con valores por defecto seguros.
- **Validation plan**: Tests existentes de database.py deben seguir pasando. Verificar que `get_db_connection()` sigue devolviendo una conexión funcional.

## Execution Order
1. Deprecation warnings (fpdf2, @app.on_event, TemplateResponse)
2. Limpieza de dependencias no usadas
3. Connection pooling en database.py
4. División de trainer.py (con types en los módulos extraídos)
5. Extracción de JS inline a archivos externos
6. Type hints en routers y services restantes (pasada separada al final)

## Open Questions
- (ninguna — todas las decisiones tomadas en la discusión de planificación)

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/decisions.md`
- `agents/docs/api.md`
- `agents/docs/dependency-policy.md`
- `agents/db/schema.sql`
- `agents/db/changes.sql`

## Decision Records
- ADRs read from `agents/docs/decisions.md`:
  - ADR-001: Estrategia de base de datos para tests
  - ADR-002: Estrategia de mock para TensorFlow/Keras
  - ADR-003: Umbral de cobertura de código
  - ADR-004: Herramientas de testing y lint
  - ADR-005 a ADR-008: Decisiones de TASK-002
- New decisions to record after user approval:
  - Pendiente según decisiones de planificación
