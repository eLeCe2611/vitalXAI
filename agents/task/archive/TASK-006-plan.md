# Task Plan

## Status
`closed`

## Task
- ID: TASK-006
- Title: Panel de administración para rol admin (visión global de consultas)
- Backlog source: `agents/task/backlog.md`

## Summary
Actualmente todos los usuarios ven solo sus propias consultas y tienen el mismo nivel de acceso. Se introducen dos roles normalizados (`admin` y `doctor`). El admin, además de ver su propio historial, puede ver un listado de todos los usuarios con su recuento de consultas y acceder al historial completo de cualquier usuario a través de un panel en el sidebar.

## Scope
**In:**
- Migración de roles en DB: normalizar valores existentes a `admin` (jefes) o `doctor` (resto)
- Nuevo endpoint `GET /api/admin/users`: lista usuarios con `consultation_count` (solo admin)
- Nuevo endpoint `GET /api/admin/users/{user_id}/consultations`: consultas de un usuario específico (solo admin)
- Botón "Panel de administración" en sidebar del dashboard, justo encima de Cerrar Sesión (solo visible si role=admin)
- Modal flotante con listado de usuarios y recuento de consultas
- Segundo modal con historial completo de consultas del usuario seleccionado (incluye patient_name)
- Tests unitarios para nuevos endpoints

**Out (explicitly excluded):**
- No se modifican endpoints existentes (history, inference, trainer)
- No se añaden roles adicionales (solo admin/doctor)
- No hay paginación en el listado de usuarios
- No se modifica el laboratorio de entrenamiento

## Current Behavior
- Todos los usuarios ven solo sus propias consultas en el dashboard
- Roles son strings libres: "Radiólogo Jefe", "Médico Residente", "Neumólogo", etc.
- No hay distinción de permisos entre usuarios
- No hay endpoints para que un admin vea datos de otros usuarios

## Target Behavior
- Roles normalizados a `admin` y `doctor`
- El sidebar del dashboard muestra "Panel de administración" solo si role=admin
- Modal 1: lista de usuarios con nombre, username y número de consultas
- Modal 2: al hacer clic en un usuario, muestra sus consultas con los mismos detalles que el historial propio
- Los doctores no ven el botón ni tienen acceso a los endpoints admin (403)

## Acceptance Criteria
1. `scripts/migrate_roles.py` mapea "Radiólogo Jefe" → "admin", resto → "doctor"
2. `GET /api/admin/users` devuelve `[{"id": N, "username": "...", "first_name": "...", "last_name": "...", "role": "...", "consultation_count": N}]`
3. `GET /api/admin/users` devuelve 401 sin JWT, 403 si no es admin
4. `GET /api/admin/users/{user_id}/consultations` devuelve consultas del usuario
5. `GET /api/admin/users/{user_id}/consultations` devuelve 403 si no es admin, 404 si usuario no existe
6. Botón "Panel de administración" visible en sidebar solo si `role == "admin"`
7. Modal 1 se abre con lista actualizada al hacer clic en el botón
8. Modal 2 se abre con consultas al hacer clic en un usuario del Modal 1
9. Tests unitarios cubren auth, forbidden y éxito en ambos endpoints

## Edge Cases
- Usuario sin consultas: `consultation_count = 0`
- Rol legacy no migrado: tratado como `doctor` (cualquier rol != "admin")
- Usuario eliminado entre apertura de modal 1 y clic en modal 2: 404 manejado
- Multi-idioma: textos del panel admin en los 4 idiomas

## Assumptions / Risks
- La migración de roles es un script único (como `scripts/migrate_passwords.py`)
- La verificación de role=admin se hace en el router (application layer)
- El botón se oculta por SSR (condicional en template Jinja2) + verificación en backend (defense in depth)

## Database Impact
- Change summary: Actualizar valores en columna `role` de la tabla `users`. No cambia el esquema.
- DB schema file: `agents/db/schema.sql` (sin cambios estructurales)
- DB change log file: `agents/db/changes.sql`
- Affected structures/data: columna `users.role`. Los valores pasan de strings libres a "admin"/"doctor"
- Forward migration approach: Script `scripts/migrate_roles.py` (UPDATE directo)
- Rollback approach: Restaurar dump previo de la tabla users
- Persisted data compatibility: Cualquier rol != "admin" se trata como "doctor". Compatible hacia atrás.
- Operational risks: Bajo. UPDATE sin cambios de esquema.
- Validation plan: Verificar que admin ve el botón y doctor no.
- Backup/recovery notes: Hacer dump de users antes de migrar.
- Required doc updates: `agents/docs/api.md`

## Open Questions
- *(ninguna por el momento — todas las decisiones se tomaron en la conversación previa)*

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/api.md`
- `routers/auth.py` (cómo se pasa role al template dashboard)
- `templates/dashboard.html` (estructura del sidebar)
- `static/js/dashboard.js` (i18n y patrón JS existente)
- `database.py` (patrón de conexión)

## Decision Records
- ADRs read: ADR-001 (mock DB), ADR-006 (JWT auth)
- New decisions: Normalización de roles a admin/doctor (se registrará como ADR-011 si se aprueba)
