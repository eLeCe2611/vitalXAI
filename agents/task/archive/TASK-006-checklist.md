# Task Checklist

## Source
- Task: TASK-006
- Plan: `agents/task/TASK-006-plan.md`

## Rules
- ALL checkboxes must start `[ ]` (unchecked).
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Plan status set to `in_progress`.
- [x] No open questions block implementation.

### 2. DB Migration — normalizar roles
- [x] Create `scripts/migrate_roles.py`.
- [x] Run migration against actual DB.

### 3. Backend — router admin.py (TDD)
- [x] RED: Write test for `GET /api/admin/users` (401, 403, 200).
- [x] GREEN: Implement `routers/admin.py` + register in `main.py`.
- [x] VERIFY.
- [x] RED: Write test for `GET /api/admin/users/{id}/consultations` (401, 403, 404, 200).
- [x] GREEN: Implement endpoint.
- [x] VERIFY.
- [x] REFACTOR.

### 4. Frontend — template dashboard.html
- [x] Add conditional "Panel de administración" button (sidebar, above logout).
- [x] Add Modal 1 HTML (users list).
- [x] Add Modal 2 HTML (user consultations).

### 5. Frontend — dashboard.js
- [x] Add i18n keys for admin panel.
- [x] Add `loadAdminUsers()` function.
- [x] Add `loadUserConsultations()` function.
- [x] Wire button → Modal 1, user click → Modal 2.

### 6. Validation
- [x] Run full test suite (150 tests).
- [x] Run ruff lint (clean).
- [x] Run coverage (78%).
- [x] Update `agents/docs/api.md`.

### 7. Closeout
- [x] User approved closeout.
- [x] Plan status set to `closed`.
- [x] Task files archived.
