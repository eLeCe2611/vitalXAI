# Task Checklist — TASK-002

## Source
- Task: TASK-002
- Plan: `agents/task/TASK-002-plan.md`

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

#### 2.1 Environment & Secrets
- [ ] RED: Write test verifying os.getenv reads GROQ_API_KEY in trainer.py
- [ ] GREEN: Move GROQ_API_KEY from hardcoded constant to os.getenv("GROQ_API_KEY")
- [ ] REFACTOR: Ensure graceful fallback message if key is missing
- [ ] RED: Write test verifying database.py reads credentials from env vars
- [ ] GREEN: Move MySQL credentials to os.getenv with sensible defaults (localhost / root / "" / tfg_pneumonia)
- [ ] REFACTOR: Verify all existing callers still get a valid connection

#### 2.2 Password Hashing (bcrypt via passlib)
- [ ] ADR check: confirm passlib[bcrypt] is approved before implementation
- [ ] RED: Write test that register endpoint stores a bcrypt hash (not plaintext)
- [ ] GREEN: Hash password with passlib before INSERT into users table
- [ ] RED: Write test that login verifies password against stored bcrypt hash
- [ ] GREEN: Update login to use passlib.verify() instead of plaintext comparison
- [ ] RED: Write test that wrong password returns same generic error as non-existent user
- [ ] GREEN: Return uniform "credenciales inválidas" for both cases (user unknown or wrong password)
- [ ] REFACTOR: Extract hashing/verification helpers to a shared module (e.g. services/auth_service.py)
- [ ] RED: Write test documenting that legacy plaintext passwords cannot be migrated
- [ ] GREEN: Add startup warning or migration notice; invalidate old sessions on first deploy

#### 2.3 JWT Session Management (access + refresh tokens)
- [ ] ADR check: confirm python-jose[cryptography] is approved before implementation
- [ ] RED: Write test for JWT access token creation with correct payload and expiry
- [ ] GREEN: Implement create_access_token(user_id) using python-jose
- [ ] RED: Write test for JWT access token verification (valid token returns user_id)
- [ ] GREEN: Implement verify_access_token(token) → user_id or None
- [ ] RED: Write test for refresh token creation stored in refresh_tokens table
- [ ] GREEN: Implement create_refresh_token(user_id) → INSERT into refresh_tokens, return raw token
- [ ] RED: Write test for refresh token rotation (using a token invalidates the previous one)
- [ ] GREEN: Implement rotate_refresh_token(old_token) → invalidate old, create and return new
- [ ] RED: Write test for /api/auth/token/refresh endpoint
- [ ] GREEN: Implement POST /api/auth/token/refresh that accepts refresh token and returns new access + refresh cookies
- [ ] RED: Write test that expired or malformed access token returns 401
- [ ] GREEN: Add JWT middleware that checks token expiry and returns 401 on failure
- [ ] RED: Write test that logout invalidates the refresh token in DB and clears cookies
- [ ] GREEN: Implement logout — revoke refresh token, clear httponly cookies
- [ ] RED: Write test for register flow that sets both JWT cookies (access + refresh)
- [ ] GREEN: Adapt register endpoint to set access + refresh cookies on success
- [ ] RED: Write test for login flow that sets both JWT cookies
- [ ] GREEN: Adapt login endpoint to set access + refresh cookies on success
- [ ] RED: Write test that dashboard and training routes redirect to / when no valid access cookie
- [ ] GREEN: Apply JWT middleware to all protected routes (dashboard, training, predict, history, trainer)
- [ ] RED: Write test for refresh token theft detection (used rotated token → revoke all user tokens)
- [ ] GREEN: Implement theft detection: if a rotated token is reused, revoke all refresh_tokens for that user_id
- [ ] REFACTOR: Consolidate JWT logic in services/auth_service.py; keep routes thin

#### 2.4 CSRF Protection (double-submit cookie)
- [ ] RED: Write test that GET response includes a Set-Cookie for csrf_token (non-httponly)
- [ ] GREEN: Add middleware that generates a CSRF token and sets it as a readable cookie on GET responses
- [ ] RED: Write test that POST request without X-CSRF-Token header returns 403
- [ ] GREEN: CSRF middleware rejects state-changing methods (POST/PUT/DELETE) that lack the header
- [ ] RED: Write test that POST with valid X-CSRF-Token (matching cookie) succeeds
- [ ] GREEN: Middleware compares header value to cookie value; passes on match
- [ ] RED: Write test that GET / HEAD / OPTIONS are exempt from CSRF check
- [ ] GREEN: Exclude safe methods from CSRF validation
- [ ] RED: Write test that CSRF token mismatch returns 403
- [ ] GREEN: Return 403 with descriptive but safe error on mismatch
- [ ] Update frontend JS (inline in dashboard.html, training.html) to read csrf_token cookie and attach X-CSRF-Token header to every state-changing fetch/XHR

#### 2.5 Security Headers Middleware
- [ ] RED: Write test that every response includes X-Content-Type-Options: nosniff
- [ ] GREEN: Add Starlette/FastAPI middleware that sets base security headers
- [ ] RED: Write one test per required header:
  - [ ] Content-Security-Policy
  - [ ] Strict-Transport-Security
  - [ ] X-Frame-Options: DENY
  - [ ] X-XSS-Protection: 1; mode=block
  - [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] GREEN: Add all required headers in the security middleware
- [ ] REFACTOR: Define header values as named constants or a dictionary for single-source-of-truth

#### 2.6 Rate Limiting (slowapi in-memory)
- [ ] ADR check: confirm slowapi is approved before implementation
- [ ] RED: Write test that /login endpoint returns 429 after 5 rapid attempts from the same IP
- [ ] GREEN: Configure slowapi limiter: 5/minute on login endpoint
- [ ] RED: Write test that other endpoints allow at least 60 requests per minute
- [ ] GREEN: Apply 60/minute default limiter to remaining endpoints
- [ ] RED: Write test that rate-limit response includes Retry-After header
- [ ] GREEN: slowapi provides Retry-After by default; verify it is present
- [ ] REFACTOR: Centralize limiter configuration in a config module or main.py

#### 2.7 Input Validation
- [ ] RED: Write test that register rejects invalid email format
- [ ] GREEN: Add email validation (email-validator dependency already present) on register endpoint
- [ ] RED: Write test that register rejects empty username / first_name / last_name
- [ ] GREEN: Add Pydantic request models or manual validation for required string fields
- [ ] RED: Write test that /predict rejects files larger than 10 MB
- [ ] GREEN: Add file-size check before saving upload in inference endpoint
- [ ] RED: Write test that /predict rejects non-image file types
- [ ] GREEN: Validate MIME type and/or magic bytes on uploaded files
- [ ] REFACTOR: Consolidate validation schemas in a shared module (e.g. services/schemas.py)

### 3. Scope and Docs
- [ ] All TDD cycles complete or documented as approved exceptions.
- [ ] Changes stayed within approved scope. No unrelated refactors.
- [ ] Out-of-scope findings registered in `agents/docs/debt.md`.
- [ ] Sync check: compare implemented code against affected source-of-truth docs from the plan. Discrepancies → stop and ask user. Resolve before proceeding.
- [ ] Durable docs updated:
  - [ ] `agents/docs/api.md` — update auth conventions to JWT/CSRF/rate-limiting; mark old plain-text notes as superseded
  - [ ] `agents/db/schema.sql` — add refresh_tokens table
  - [ ] `agents/db/changes.sql` — record migration with forward SQL and rollback notes
  - [ ] `agents/docs/decisions.md` — add ADR-005 (passlib), ADR-006 (python-jose), ADR-007 (slowapi), ADR-008 (refresh-token strategy)
  - [ ] `agents/docs/debt.md` — close DBT-001 (passwords) and DBT-002 (API key); move to dismissed or resolved
  - [ ] `.env.example` — create or update with all required environment variables (GROQ_API_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, JWT_SECRET_KEY, JWT_ACCESS_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS)

### 4. Database Change Controls
- [ ] `agents/db/schema.sql` — add refresh_tokens table definition.
- [ ] `agents/db/changes.sql` — record forward migration SQL and rollback notes.
- [ ] Persisted data compatibility reviewed: legacy plaintext passwords are NOT migratable; deployment note required.
- [ ] Backup or recovery expectation documented: take full DB dump before first deploy with bcrypt to allow rollback of user data.
- [ ] Pre-check: `SELECT COUNT(*) FROM users` to know how many accounts are affected.
- [ ] Post-check: `SELECT COUNT(*) FROM refresh_tokens` after first login, `DESCRIBE refresh_tokens` to verify schema.

### 5. Validation (still `in_progress`)
- [ ] Targeted tests: `python -m pytest tests/unit/test_auth_router.py -v`
- [ ] Full unit suite: `python -m pytest tests/unit/ -v`
- [ ] Integration suite: `python -m pytest tests/integration/ -v`
- [ ] Full suite: `python -m pytest tests/ -v`
- [ ] Lint: `ruff check .`
- [ ] Coverage: `python -m pytest tests/unit/ --cov=services --cov=routers --cov=database.py --cov-report=term-missing`
- [ ] Typecheck: `not available` (deferred to TASK-004)
- [ ] Build: `not available`
- [ ] DoD `in_progress` criteria checked against `agents/docs/DoD.md`.

### 6. Closeout (→ `closed`)
- [ ] Ask user before marking backlog task done.
- [ ] Update the plan status to `closed` before archiving task files.
- [ ] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
...
