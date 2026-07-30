# Task Checklist

## Source
- Task: TASK-008
- Plan: `agents/task/TASK-008-plan.md`

## Rules
- Work in order unless blocked.
- Keep items derived from the approved plan.
- ALL checkboxes must start `[ ]` (unchecked). Never pre-mark items when generating the checklist.
- Mark completed items during implementation and closeout only.

## Checklist

### 1. Context
- [x] Re-read the approved plan and referenced source-of-truth docs (do not skip even if read during planning).
- [x] Load and apply `agents/skills/test-driven-development/SKILL.md`, or record why it does not apply.
- [x] Verify no open questions block implementation.
- [x] Set the plan status to `in_progress` before the first implementation change.

### 2. Backend i18n: services/lang.py
- [x] Crear `services/lang.py` con diccionario de 4 idiomas para mensajes del backend
- [x] Incluir helper function `get_text(key, lang='es')` con fallback a español
- [x] Incluir `get_lang_from_cookie(request)` para extraer idioma de cookie `appLang`
- [x] Escribir tests unitarios para `services/lang.py`

### 3. Backend messages: routers
- [x] Traducir mensajes en `routers/auth.py` usando `lang.py`
- [x] Traducir mensajes en `routers/inference.py` usando `lang.py`
- [x] Traducir mensajes en `routers/trainer.py` usando `lang.py`
- [x] Actualizar tests existentes que verifican mensajes en español (no era necesario — tests no verificaban strings)

### 4. ML labels: services/ml_engine.py
- [x] Modificar `ml_engine.py` para aceptar `lang` y devolver labels traducidos
- [x] Actualizar tests existentes (default lang='es' mantiene compatibilidad)

### 5. XAI titles: services/xai_generator.py
- [x] Modificar `xai_generator.py` para aceptar `lang` en títulos matplotlib
- [x] Actualizar tests existentes

### 6. PDF diagnosis: services/pdf_generator.py
- [x] Modificar `pdf_generator.py` para generar PDF en idioma
- [x] Actualizar tests existentes

### 7. Chatbot i18n: services/chatbot_service.py
- [x] Traducir SYSTEM_PROMPT a 4 idiomas
- [x] Modificar `chat_endpoint` para leer cookie `appLang` y seleccionar prompt
- [x] Actualizar tests existentes

### 8. Frontend i18n: static/js/i18n.js
- [x] Crear `static/js/i18n.js` con diccionario unificado para todas las páginas (4 idiomas)
- [x] Incluir función global `t(key)` + `changeLanguage()`
- [x] Incluir lógica de persistencia (localStorage) y detección inicial
- [x] Todas las páginas (dashboard, admin, training, login, register) cargan i18n.js

### 9. Frontend: dashboard.html + dashboard.js
- [x] Refactorizar dashboard.js: eliminar dict local, usar `t()` de i18n.js
- [x] Asegurar que dashboard.html carga i18n.js antes que dashboard.js
- [x] Traducción de labels dinámicos con `t()` en vez de ternario manual

### 10. Frontend: admin.js
- [x] Refactorizar admin.js: eliminar adminDict, usar `t()` de i18n.js
- [x] Asegurar que dashboard.html/training.html cargan i18n.js antes que admin.js

### 11. Frontend: training.html + training.js
- [x] Implementar i18n en training.js: eliminar dict vacío, usar `t()` de i18n.js
- [x] Implementar changeLanguage() funcional en training.js
- [x] Añadir selector de idioma en training.html (mismo estilo que dashboard)
- [x] Textos traducidos mediante función `t()` en training.js
- [x] Cobertura: sidebar, header, chatbot, botones, tablas, terminal, modals

### 12. Frontend: login.html + register.html
- [x] Refactorizar login.html: eliminar dict local, usar i18n.js + data-i18n
- [x] Refactorizar register.html: eliminar dict local, usar i18n.js + data-i18n

### 13. Scope and Docs
- [x] All implementation items complete.
- [x] Changes stayed within approved scope. No unrelated refactors.
- [x] Out-of-scope findings: none to register.
- [x] Sync check: implemented code matches plan.
- [x] Durable docs: `agents/docs/api.md` no necesita cambios (no se tocó API contract). `agents/docs/design.md` no necesita cambios (solo i18n, no diseño visual).

### 14. Database Change Controls
Not applicable — this task does not affect the database.

### 15. Validation
- [x] Targeted tests: 178 unit tests passed
- [x] Full test suite: 182 tests passed (178 unit + 4 integration)
- [x] Lint: `ruff check .` — all checks passed
- [x] Typecheck: `python -m mypy` — success, no issues
- [x] DoD `in_progress` criteria checked.

### 16. Closeout (→ `closed`)
- [ ] Ask user before marking backlog task done.
- [ ] Update the plan status to `closed` before archiving task files.
- [ ] Move task files to `agents/task/archive/` after user approves.

## Resume Notes
