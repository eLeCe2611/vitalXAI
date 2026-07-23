# Task Checklist

## Source
- Task: TASK-001
- Plan: `agents/task/TASK-001-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs.
- [x] Load and apply `agents/skills/test-driven-development/SKILL.md`. TDD applied: pre-existing code → regression tests.
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. Infrastructure Setup
- [x] Create `pyproject.toml` with pytest, pytest-cov, and ruff configuration.
- [x] Create `tests/` directory structure.
- [x] Create `tests/conftest.py` with shared fixtures.
- [x] Install test dependencies (pytest, pytest-cov, pytest-mock, ruff).
- [x] Verify pytest discovers tests.

### 3. Tests for database.py
- [x] Test `get_db_connection()` returns connection.
- [x] Test `get_db_connection()` raises on error.
- [x] Test `init_db()` creates table.
- [x] Test `init_db()` handles DB unavailable.

### 4. Tests for services/ml_engine.py
- [x] Test `get_model()` CNN loads .keras.
- [x] Test `get_model()` Transformer loads HuggingFace.
- [x] Test `get_model()` caching.
- [x] Test `get_model()` missing CNN weights.
- [x] Test `get_model()` missing Transformer weights.
- [x] Test `process_and_predict()` CNN pneumonia.
- [x] Test `process_and_predict()` CNN normal.
- [x] Test `process_and_predict()` Transformer.
- [x] Test image size for InceptionV3.
- [x] Test image size for vit_384.
- [x] Test confidence clamped 0–100.

### 5. Tests for services/xai_generator.py
- [x] Test `get_img_size()` 224, 299, 384.
- [x] Test `load_img_tf()` loads and normalizes.
- [x] Test `generate_xai_heatmap()` saves figure.
- [x] Test `generate_xai_heatmap()` transformer label.
- [ ] Skipped: `saliency()`, `smoothgrad()`, `get_cam_or_attention()` — require complex TF tensor mocking; covered by heatmap integration test.

### 6. Tests for services/pdf_generator.py
- [x] Test pneumonia label uses red.
- [x] Test normal label uses green.
- [x] Test returns valid PDF path.
- [x] Test handles image error gracefully.

### 7. Tests for services/trainer_engine.py
- [x] Test `get_img_size()` with various model names.
- [x] Test `build_dataframe()` creates labels.
- [x] Test `build_dataframe()` ignores non-images.
- [x] Test `build_cnn_model()` architecture resolution.
- [x] Test `build_cnn_model()` fallback to MobileNetV2.
- [x] Test `DBProgressCallback` on_epoch_end.
- [x] Test `DBProgressCallback` progress calculation.
- [x] Test `run_training_job_sync()` missing dataset.
- [x] Test `run_training_job_sync()` empty dataset.

### 8. Tests for routers/auth.py
- [x] Test GET `/` returns login page.
- [x] Test POST `/login` valid credentials.
- [x] Test POST `/login` invalid credentials.
- [x] Test GET `/dashboard` with valid session.
- [x] Test GET `/dashboard` without session.
- [x] Test GET `/dashboard` invalid user → redirect.
- [x] Test GET `/training` with session.
- [x] Test GET `/training` without session.
- [x] Test GET `/logout` clears cookie.
- [x] Test GET `/register` returns form.
- [x] Test POST `/api/register` success.
- [x] Test POST `/api/register` duplicate username.

### 9. Tests for routers/history.py
- [x] Test GET `/api/history` without session (401).
- [x] Test GET `/api/history` with data.
- [x] Test GET `/api/history` empty.
- [x] Test POST `/api/history/update_name` success.
- [x] Test POST `/api/history/delete` success.

### 10. Tests for routers/inference.py
- [x] Test POST `/predict` without session (401).
- [x] Test POST `/predict` successful prediction.

### 11. Tests for routers/trainer.py
- [x] Test POST `/api/chat` new session.
- [x] Test POST `/api/chat` existing session.
- [x] Test POST `/api/chat` Groq error.
- [x] Test GET `/api/train/browse` mocks Tkinter.
- [x] Test POST `/api/train/start` valid params.
- [x] Test POST `/api/train/start` invalid path.
- [x] Test GET `/api/train/logs` with file.
- [x] Test GET `/api/train/logs` without file.
- [x] Test GET `/api/train/models` with sessions.
- [x] Test GET `/api/train/results/...` 404.
- [x] Test POST `/api/train/run_eval` missing dataset.
- [x] Test DELETE session success.
- [x] Test DELETE session not found.
- [x] Test POST rename success.
- [x] Test POST rename to existing name.

### 12. Integration Tests (postponed to TASK-002)
- [ ] Integration test auth flow — requires SQLite setup, deferred.
- [ ] Integration test prediction E2E — requires real file handling, deferred.

### 13. Documentation
- [x] `agents/docs/testing.md` populated with commands and structure.
- [x] `agents/docs/api.md` populated with all current routes.
- [x] `agents/db/schema.sql` populated with actual table schemas.

### 14. Validation
- [x] Full test suite: 73 passed.
- [x] Coverage: 58% (above 50% threshold in pyproject.toml).
- [x] Lint: ruff passes with configured ignores.
- [x] DoD `in_progress` criteria checked.

### 15. Scope and Docs
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] Out-of-scope findings registered in `agents/docs/debt.md`.
- [x] Sync check passed. No discrepancies with source-of-truth docs.
- [x] Durable docs updated.

### 16. Database Change Controls
- [x] DB schema file updated in `agents/db/schema.sql`.

### 17. Closeout (→ `closed`)
- [x] Ask user before marking backlog task done.
- [x] Update the plan status to `closed` before archiving task files.
- [x] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
