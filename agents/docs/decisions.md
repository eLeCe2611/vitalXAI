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
