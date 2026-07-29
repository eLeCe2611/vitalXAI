# Task Checklist — TASK-004

## Source
- Task: TASK-004
- Plan: `agents/task/TASK-004-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs.
- [x] Load and apply `agents/skills/test-driven-development/SKILL.md`, or record why it does not apply.
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. TDD Ledger

#### 2.1 CI/CD — GitHub Actions
- [x] Create `.github/workflows/` directory structure
- [x] Create `ci.yml` with triggers on push/PR to main and refactorizacion
- [x] Configure windows-latest runner
- [x] Add pip cache step (actions/cache)
- [x] Add Python 3.11 setup step
- [x] Add ruff lint step
- [x] Add pytest tests/ step with coverage
- [x] Add coverage threshold check (70%)
- [x] Verify CI file syntax (no actual run needed)

#### 2.2 Type checker — mypy
- [x] Install mypy (add to requirements dev or check availability)
- [x] Add mypy configuration to pyproject.toml (python_version=3.11, ignore_missing_imports)
- [x] Configure strict gradual: start with services/auth_service.py
- [x] Run mypy against configured modules
- [x] Update `agents/docs/testing.md` with mypy command

#### 2.3 design.md
- [x] Extract color palette from templates (Tailwind classes)
- [x] Add UI type, audience, tone, density
- [x] Add dark mode strategy
- [x] Add typography tokens (font stack, sizes)
- [x] Add layout and responsive breakpoints
- [x] Add component catalog (button, input, card, modal, sidebar)
- [x] Add interactive states documentation
- [x] Verify content covers all templates (login, register, dashboard, training)

#### 2.4 domain.md
- [x] Document User entity with fields and constraints
- [x] Document Consultation entity with fields and constraints
- [x] Document TrainingJob entity with fields and constraints
- [x] Document RefreshToken entity with fields and constraints
- [x] Document relationships (FKs, cascade)
- [x] Document business rules (auth, XAI, MLOps)
- [x] Add technical glossary

### 3. Scope and Docs
- [x] All TDD cycles complete or documented as approved exceptions.
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] Out-of-scope findings registered in `agents/docs/debt.md`.
- [x] Sync check: compare implemented code against affected source-of-truth docs from the plan.
- [x] Durable docs updated as needed.

### 4. Database Change Controls
Not applicable — no schema or migration changes.

### 5. Validation (still `in_progress`)
- [x] Full test suite: `python -m pytest tests/ -v`
- [x] Lint: `ruff check .`
- [x] Typecheck: `mypy services/auth_service.py`
- [x] Build: `not available`
- [x] DoD `in_progress` criteria checked:

### 6. Closeout (→ `closed`)
- [x] Ask user before marking backlog task done.
- [x] Update the plan status to `closed` before archiving task files.
- [x] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
...
