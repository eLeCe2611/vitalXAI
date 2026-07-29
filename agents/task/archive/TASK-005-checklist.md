# Task Checklist

## Source
- Task: TASK-005
- Plan: `agents/task/TASK-005-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [ ] Set plan status to `in_progress` before the first implementation change.
- [ ] Load and apply TDD skill — pre-existing code approach (regression tests first, then modify).
- [ ] Verify no open questions block implementation.

### 2. Phase 1 — Diagnóstico Rápido (history.py)

#### 2a. update_name ownership
- [ ] RED: Write test verifying `update_name` returns 403 when consultation belongs to another user.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add user_id check to `update_name` endpoint.
- [ ] GREEN: Verify test passes.
- [ ] REFACTOR: Clean up if needed.

#### 2b. delete ownership
- [ ] RED: Write test verifying `delete` returns 403 when consultation belongs to another user.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add user_id check to `delete` endpoint.
- [ ] GREEN: Verify test passes.
- [ ] REFACTOR: Clean up if needed.

### 3. Phase 2 — Laboratorio de Entrenamiento (trainer.py + mlops_engine.py)

#### 3a. Add ownership helpers in mlops_engine.py
- [ ] RED: Write test for `_verify_session_ownership(session_id, user_id)` — returns True when owner, False otherwise.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Implement `_verify_session_ownership` that reads `user_id` from `config.json`.
- [ ] GREEN: Verify test passes.
- [ ] RED: Write test for `create_training_session` storing `user_id`.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add `user_id` parameter and persist to `config.json`.
- [ ] GREEN: Verify test passes.
- [ ] REFACTOR: Clean up.

#### 3b. Auth + ownership on all trainer.py endpoints
- [ ] RED: Write test verifying `GET /api/train/models` requires auth (401 without JWT).
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add JWT check to `get_trained_sessions` route.
- [ ] GREEN: Verify test passes.
- [ ] RED: Write test verifying `GET /api/train/models` filters by user.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add user_id filtering to `get_trained_sessions`.
- [ ] GREEN: Verify test passes.
- [ ] RED: Write test verifying `DELETE /api/train/session/{id}` returns 403 for unowned session.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add ownership check to `delete_session`.
- [ ] GREEN: Verify test passes.
- [ ] RED: Write test verifying `POST /api/train/session/rename` returns 403 for unowned session.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add ownership check to `safe_rename`.
- [ ] GREEN: Verify test passes.
- [ ] RED: Write test verifying `POST /api/train/run_eval` requires auth.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add auth + ownership checks.
- [ ] GREEN: Verify test passes (batch).
- [ ] RED: Write test verifying `POST /api/train/session/compare` requires auth.
- [ ] RED: Verify test fails correctly.
- [ ] GREEN: Add auth + ownership checks.
- [ ] GREEN: Verify test passes (batch).
- [ ] RED: Write test verifying remaining read endpoints (`results`, `ranking`, `external_results`, `report`) return 403 for unowned sessions.
- [ ] RED: Verify tests fail correctly.
- [ ] GREEN: Add ownership checks to all remaining endpoints.
- [ ] GREEN: Verify all tests pass.
- [ ] REFACTOR: Extract shared auth/ownership helper if duplication warrants it.

### 4. Phase 3 — Migrate existing sessions
- [ ] Add `"user_id": 1` to `config.json` of `soloCNN`, `soloTransformers`, `deTodo`.
- [ ] Add `"user_id": 3` to `config.json` of `RUN_20260724_021631`.

### 5. Phase 4 — Validation and docs

#### 5a. Tests
- [ ] Run targeted tests for each modified module.
- [ ] Run full test suite.
- [ ] Verify coverage threshold.

#### 5b. Lint & Typecheck
- [ ] Run `ruff check .`.
- [ ] Run `python -m mypy` (if relevant).

#### 5c. Docs
- [ ] Sync check: verify code matches affected source-of-truth docs.
- [ ] Update `agents/docs/api.md` to document auth requirements for training endpoints.

#### 5d. DoD check
- [ ] Verify DoD `in_progress` criteria met.

### 6. Closeout (→ `closed`)
- [x] User approved closeout.
- [x] Plan status set to `closed`.
- [x] Task files archived.

## Resume Notes
...
