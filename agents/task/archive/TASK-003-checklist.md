# Task Checklist — TASK-003

## Source
- Task: TASK-003
- Plan: `agents/task/TASK-003-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [ ] Re-read the approved plan and referenced source-of-truth docs (do not skip even if read during planning).
- [ ] Load and apply `agents/skills/test-driven-development/SKILL.md`, or record why it does not apply.
- [ ] Verify no open questions block implementation.
- [ ] Set the plan status to `in_progress` before the first implementation change.

### 2. TDD Ledger

#### 2.1 Deprecation warnings

##### 2.1.1 fpdf2 — Arial → helvetica
- [ ] RED: Write regression test capturing current fpdf2 behavior (Arial usage)
- [ ] GREEN: Replace all `"Arial"` with `"helvetica"` in trainer.py
- [ ] VERIFY: Confirm no Arial references remain and tests pass

##### 2.1.2 fpdf2 — ln=True → new_x / new_y
- [ ] RED: Write regression test capturing ln=True behavior
- [ ] GREEN: Replace all `ln=True` with `new_x=XPos.LMARGIN, new_y=YPos.NEXT` in trainer.py
- [ ] VERIFY: Confirm no ln=True references remain and tests pass

##### 2.1.3 FastAPI — @app.on_event → lifespan
- [ ] RED: Write test verifying startup event registration
- [ ] GREEN: Migrate `@app.on_event("startup")` to lifespan handler in main.py
- [ ] VERIFY: App still initializes DB on startup

##### 2.1.4 Starlette — TemplateResponse signature
- [ ] RED: Write test capturing TemplateResponse behavior
- [ ] GREEN: Update all `TemplateResponse(name, {request: ...})` to `TemplateResponse(request, name, {...})` in auth.py
- [ ] VERIFY: Pages still render correctly

#### 2.2 Limpieza de dependencias no usadas
- [ ] Verify psycopg2-binary, pymongo, redis have no imports in codebase
- [ ] Remove them from requirements.txt
- [ ] Run tests to confirm nothing breaks

#### 2.3 Connection pooling
- [ ] RED: Write test verifying connection pooling is used
- [ ] GREEN: Implement MySQLConnectionPool in database.py
- [ ] GREEN: Update get_db_connection() to get connection from pool
- [ ] VERIFY: All tests pass with pool

#### 2.4 División de trainer.py

##### 2.4.1 Extraer chatbot_router.py
- [ ] RED: Write test importing chatbot functions separately
- [ ] GREEN: Extract chat endpoint + Groq logic to services/chatbot_router.py
- [ ] REFACTOR: Update trainer.py to import from chatbot_router.py
- [ ] VERIFY: All tests pass

##### 2.4.2 Extraer mlops_engine.py
- [ ] RED: Write test importing MLOps engine functions separately
- [ ] GREEN: Extract run_training_queue + subprocess logic to services/mlops_engine.py
- [ ] REFACTOR: Update trainer.py to import from mlops_engine.py
- [ ] VERIFY: All tests pass

##### 2.4.3 Extraer pdf_generator_mlops.py
- [ ] RED: Write test importing MedicalReport separately
- [ ] GREEN: Extract MedicalReport class + report endpoint logic to services/pdf_generator_mlops.py
- [ ] REFACTOR: Update trainer.py to import from pdf_generator_mlops.py
- [ ] VERIFY: All tests pass

##### 2.4.4 trainer.py as thin facade
- [ ] Verify trainer.py < 100 lines after extraction
- [ ] Update test imports if needed
- [ ] VERIFY: Full test suite passes

#### 2.5 Extracción de JS inline

##### 2.5.1 dashboard.js
- [ ] RED: Write test verifying JS behavior (optional — integration)
- [ ] GREEN: Move JS from dashboard.html to static/js/dashboard.js
- [ ] GREEN: Add data-* attributes in HTML for Jinja2 variables
- [ ] GREEN: Update HTML to reference external JS
- [ ] VERIFY: Dashboard renders and functions correctly

##### 2.5.2 training.js
- [ ] GREEN: Move JS from training.html to static/js/training.js
- [ ] GREEN: Add data-* attributes in HTML for Jinja2 variables
- [ ] GREEN: Update HTML to reference external JS
- [ ] VERIFY: Training page renders and functions correctly

#### 2.6 Type hints (pasada separada)
- [ ] Add type hints to services/auth_service.py
- [ ] Add type hints to services/csrf_middleware.py
- [ ] Add type hints to services/rate_limiter.py
- [ ] Add type hints to services/ml_engine.py
- [ ] Add type hints to services/xai_generator.py
- [ ] Add type hints to services/pdf_generator.py
- [ ] Add type hints to services/trainer_engine.py
- [ ] Add type hints to routers/auth.py
- [ ] Add type hints to routers/history.py
- [ ] Add type hints to routers/inference.py
- [ ] Add type hints to routers/trainer.py
- [ ] Add type hints to database.py
- [ ] VERIFY: Ruff lint passes with type hints

### 3. Scope and Docs
- [ ] All TDD cycles complete or documented as approved exceptions.
- [ ] Changes stayed within approved scope. No unrelated refactors.
- [ ] Out-of-scope findings registered in `agents/docs/debt.md`.
- [ ] Sync check: compare implemented code against affected source-of-truth docs from the plan.
- [ ] Durable docs updated as needed.

### 4. Database Change Controls
Not applicable — schema unchanged, only connection pooling implementation.

### 5. Validation (still `in_progress`)
- [ ] Targeted tests:
- [ ] Full test suite:
- [ ] Lint:
- [ ] Typecheck: `not available`
- [ ] Build: `not available`
- [ ] DoD `in_progress` criteria checked:

### 6. Closeout (→ `closed`)
- [ ] Ask user before marking backlog task done.
- [ ] Update the plan status to `closed` before archiving task files.
- [ ] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
...
