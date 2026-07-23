# Architecture Decision Records

ADR log for durable decisions that should guide future work.

Before planning product work, read relevant accepted ADRs and do not contradict them silently.

Record only decisions with future impact. Keep one-off choices, temporary workarounds, task-local assumptions, and obvious coding details in the task plan/checklist.

Before adding or changing an ADR, ask the user for approval and summarize the title, context, decision, consequences, and future value.

If new work conflicts with an accepted ADR, explain the conflict and ask whether to keep, rewrite, or update it.

## Statuses
- `accepted`: approved by the user and active for future work.
- `rejected`: considered and explicitly declined; keep only when remembering the rejection prevents repeated debate.

## Format

```md
## ADR-000: Short title
Date: YYYY-MM-DD
Status: accepted | rejected
Context: What recurring uncertainty, constraint, or tradeoff forced the decision? What options mattered?
Decision: What rule should future work follow? Be specific enough that another agent can apply it.
Consequences: What benefits, costs, constraints, or follow-up work does this create?
```

## Log

## ADR-001: Estrategia de base de datos para tests
Date: 2026-07-23
Status: accepted
Context: Todos los routers y trainer_engine.py usan `database.get_db_connection()` con MySQL real (XAMPP). Sin ORM. Se necesita una estrategia de tests que no dependa de MySQL en CI.
Decision: Tests unitarios: mockear `get_db_connection` con `unittest.mock.patch` en todos los módulos que lo importan directamente. Tests de integración (futuros): SQLite en memoria con schema replicado. No se requiere Docker ni MySQL en CI.
Consequences: Los tests unitarios son rápidos y deterministas. Los tests de integración requieren asegurar compatibilidad SQL entre MySQL y SQLite (el SQL usado es ANSI básico, riesgo bajo).

## ADR-002: Estrategia de mock para TensorFlow/Keras
Date: 2026-07-23
Status: accepted
Context: `ml_engine.py` y `trainer_engine.py` cargan modelos .keras y .h5 reales y hacen inferencia/entrenamiento. No se puede requerir GPU en CI y los modelos son demasiado grandes para tests unitarios.
Decision: Mock total a nivel de `tf.keras.models.load_model` y `TFAutoModelForImageClassification.from_pretrained`, devolviendo objetos mock con `.predict()`, `.logits`, `.fit()` controlados. Rápido, determinista, sin GPU.
Consequences: No se prueba la integración real con TF. Para eso se necesitarían tests de integración con modelos tiny pre-generados (deferido).

## ADR-003: Umbral de cobertura de código
Date: 2026-07-23
Status: accepted
Context: El plan inicial fijaba 80% de cobertura en services/ y routers/. La realidad es que `trainer.py` (32%) y `xai_generator.py` (47%) tienen código difícil de mockear (subprocess, Tkinter, TF internals) que arrastra la media total al 57%.
Decision: Umbral real: 50% como baseline para TASK-001. El 80% se perseguirá en TASK-002 con tests de integración adicionales y mejora de cobertura en los módulos críticos.
Consequences: El threshold en pyproject.toml está en 50%. La desviación del plan está documentada. La red de seguridad actual cubre auth (97%), inference (95%), history (86%), ml_engine (96%), pdf_generator (82%).

## ADR-004: Herramientas de testing y lint
Date: 2026-07-23
Status: accepted
Context: El proyecto no tenía test runner, linter ni type checker configurados.
Decision: pytest + pytest-cov + pytest-mock para tests. Ruff para lint. Configuración en pyproject.toml unificado. pytest-sugar para output formateado.
Consequences: Estandariza el tooling. pyproject.toml como fuente única de configuración. Queda pendiente type checking (deferido).

## ADR-005: bcrypt para hashing de contraseñas
Date: 2026-07-23
Status: accepted
Context: Las contraseñas se almacenaban en texto plano (DBT-001). Se necesita un algoritmo de hashing probado.
Decision: Usar `bcrypt` (librería directa, no via passlib) por su simplicidad y compatibilidad con Python 3.11+. passlib 1.7.4 no es compatible con bcrypt 5.x.
Consequences: Las contraseñas existentes en texto plano no son migrables. Los usuarios deben restablecer su contraseña.

## ADR-006: python-jose[cryptography] para JWT
Date: 2026-07-23
Status: accepted
Context: Se necesita autenticación stateless con JWT en lugar de session_token plano.
Decision: Usar `python-jose[cryptography]` 3.5.0 para crear y verificar tokens JWT. Access token (15 min) + Refresh token (7 días con rotación) almacenados en httponly cookies.
Consequences: Las rutas protegidas verifican el JWT del cookie. Refresh tokens se almacenan hasheados en tabla `refresh_tokens` para permitir revocación.

## ADR-007: slowapi para rate limiting in-memory
Date: 2026-07-23
Status: accepted
Context: No hay protección contra ataques de fuerza bruta ni abuso de API.
Decision: Usar `slowapi` 0.1.10 con límite de 5 peticiones/min en /login y 60 peticiones/min en el resto de endpoints. Almacenamiento en memoria.
Consequences: Los límites se reinician al reiniciar el servidor. No requiere Redis para el ámbito del TFG.

## ADR-008: Estrategia de refresh tokens con rotación y margen de gracia
Date: 2026-07-23
Status: accepted
Context: Se necesita refresh token rotation para mejorar seguridad (si un token es robado, al usarlo se invalida).
Decision: Los refresh tokens se almacenan hasheados (SHA-256) en tabla `refresh_tokens`. La rotación invalida el token anterior y crea uno nuevo. Margen de gracia de 60s para mitigar race conditions entre pestañas concurrentes.
Consequences: Si un token rotado se reutiliza dentro de los 60s, se acepta (grace period). Pasado ese tiempo, se rechaza y se invalidan todos los tokens del usuario (detección de robo).
