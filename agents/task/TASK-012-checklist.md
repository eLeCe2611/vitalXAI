# TASK-012 Checklist

## Source
- Task: TASK-012
- Plan: `agents/task/TASK-012-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs.
- [x] Load and apply `agents/skills/test-driven-development/SKILL.md`, with configuration-only exception recorded.
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. TDD Ledger
- [x] Configuration exception: validate Dockerfile and Compose through parser/build/startup checks instead of production-code TDD.
- [x] Behavior 1: application container starts and is reachable from the host.
- [x] Behavior 2: application connects to healthy MySQL and initializes its tables.
- [x] Behavior 3: local demo model and reduced dataset are available at the documented paths.
- [x] Behavior 4: image export/import preserves the runnable demo.

### 3. Scope and Docs
- [x] All validation cycles complete or documented as approved configuration exceptions.
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] No out-of-scope findings required a `agents/docs/debt.md` entry.
- [x] Sync check against `AGENTS.md`, `agents/docs/testing.md`, and ADR-011 completed.
- [x] Durable/task documentation updated as needed.

### 4. Database Change Controls
- [x] No schema change: schema and change-log updates marked not applicable.
- [x] Persisted data compatibility reviewed.
- [x] Backup/recovery expectation documented.
- [x] MySQL healthcheck and initialization validated.

### 5. Validation (still `in_progress`)
- [x] Targeted validation: Dockerfile syntax/build and Compose config.
- [x] Full test suite: `python -m pytest tests/ -v` (190 passed).
- [x] Lint: `ruff check .`.
- [x] Typecheck: `python -m mypy`.
- [x] Build: Docker image build and export/import checks.
- [x] DoD `in_progress` criteria checked.

### 6. Closeout (→ `closed`)
- [ ] Ask user before marking backlog task done.
- [ ] Update the plan status to `closed` before archiving task files.
- [ ] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
- Imagen `linux/amd64` construida y exportada; paquete local regenerado en `vitalXAI-demo-package`.
- Validado: dos modelos CNN, 20 imágenes por clase, caché offline de Keras, MySQL no-root, diagnóstico XAI/PDF, entrenamiento MLOps y carga de imagen exportada.
- Los contenedores se dejaron detenidos y los volúmenes se conservaron.
