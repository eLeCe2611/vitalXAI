# Task Checklist

## Source
- Task: TASK-007
- Plan: `agents/task/TASK-007-plan.md`

## Rules
- ALL checkboxes must start `[ ]` (unchecked).
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Plan status set to `in_progress`.
- [x] No open questions block implementation.

### 2. Database
- [x] Add `job_queue` table to `database.py:init_db()`.
- [x] Run migration (table creation).

### 3. Worker — services/queue_worker.py
- [x] Create worker with main loop: pick next job, execute, update status.
- [x] Implement priority: diagnosis > training.
- [x] Implement recovery: reset running → queued on startup.
- [x] Implement process_diagnosis_job().
- [x] Implement process_training_job().

### 4. Queue router — routers/queue.py
- [x] RED: Write tests for `GET /api/queue/status` (401, 200 with jobs, position).
- [x] GREEN: Implement endpoint.
- [x] VERIFY.

### 5. Modify inference.py
- [x] RED: Write test that `POST /predict` returns job_id and position.
- [x] GREEN: Modify to save image then enqueue.
- [x] VERIFY.

### 6. Modify trainer.py
- [x] RED: Write test that `POST /api/train/start` returns job_id and position.
- [x] GREEN: Modify to enqueue instead of BackgroundTasks.
- [x] VERIFY.

### 7. main.py — register and start
- [x] Register queue router.
- [x] Start worker in lifespan.
- [x] Recovery: reset running → queued on startup.

### 8. Frontend — queue panel
- [x] Add queue panel HTML to dashboard.html.
- [x] Add queue panel HTML to training.html.
- [x] Add polling logic (every 5s).
- [x] Add i18n keys for queue status texts.

### 9. Validation
- [x] Run full test suite (166 passed).
- [x] Run ruff lint (clean).
- [x] Update `agents/docs/api.md`.

### 10. Closeout
- [x] User approved closeout.
- [x] Plan status set to `closed`.
- [x] Task files archived.
