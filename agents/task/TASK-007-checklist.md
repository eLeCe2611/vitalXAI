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
- [ ] Add `job_queue` table to `database.py:init_db()`.
- [ ] Run migration (table creation).

### 3. Worker — services/queue_worker.py
- [ ] Create worker with main loop: pick next job, execute, update status.
- [ ] Implement priority: diagnosis > training.
- [ ] Implement recovery: reset running → queued on startup.
- [ ] Implement process_diagnosis_job().
- [ ] Implement process_training_job().

### 4. Queue router — routers/queue.py
- [ ] RED: Write tests for `GET /api/queue/status` (401, 200 with jobs, position).
- [ ] GREEN: Implement endpoint.
- [ ] VERIFY.

### 5. Modify inference.py
- [ ] RED: Write test that `POST /predict` returns job_id and position.
- [ ] GREEN: Modify to save image then enqueue.
- [ ] VERIFY.

### 6. Modify trainer.py
- [ ] RED: Write test that `POST /api/train/start` returns job_id and position.
- [ ] GREEN: Modify to enqueue instead of BackgroundTasks.
- [ ] VERIFY.

### 7. main.py — register and start
- [ ] Register queue router.
- [ ] Start worker in lifespan.
- [ ] Recovery: reset running → queued on startup.

### 8. Frontend — queue panel
- [ ] Add queue panel HTML to dashboard.html.
- [ ] Add queue panel HTML to training.html.
- [ ] Add polling logic to dashboard.js (every 5s).
- [ ] Add polling logic to training.js (every 5s).
- [ ] Add i18n keys for queue status texts.

### 9. Validation
- [ ] Run full test suite.
- [ ] Run ruff lint.
- [ ] Update `agents/docs/api.md`.

### 10. Closeout
- [ ] Ask user before marking done.
- [ ] Archive task files.
