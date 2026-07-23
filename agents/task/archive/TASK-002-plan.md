# Task Plan

## Status
`closed`

## Task
- ID: TASK-002
- Title: Seguridad (hashing, JWT, CSRF, rate limiting, headers, .env)
- Backlog source: `agents/task/backlog.md`

## Summary
Refactorizar la seguridad del proyecto vitalXAI para eliminar vulnerabilidades críticas: implementar hashing de contraseñas con bcrypt, mover todas las claves y credenciales a variables de entorno, reemplazar el session_token plano por JWT con access + refresh tokens, añadir protección CSRF, security headers, rate limiting y validación de inputs.

## Scope
**In:**
1. **Password hashing** (DBT-001) — bcrypt via passlib en registro y login
2. **API Key de Groq a .env** (DBT-002) — eliminar hardcode en trainer.py
3. **Credenciales MySQL a .env** — host, user, password, database desde variables de entorno
4. **JWT session management** — access token (15 min) + refresh token (7 días con rotación), almacenados en httponly cookie, middleware de verificación
5. **CSRF protection** — doble submit cookie (token en cookie no-httponly + header X-CSRF-Token), middleware de validación en métodos state-changing (POST, PUT, DELETE)
6. **Security headers middleware** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
7. **Rate limiting** — slowapi in-memory: 5 intentos/min para login, 60 req/min para el resto
8. **Input validation** — email (email-validator ya presente), sanitización de strings, tipo/tamaño de archivos subidos

**Out (explicitly excluded):**
- División de trainer.py en módulos (TASK-003)
- Extracción de JS inline de templates a archivos .js (TASK-003)
- Type hints en toda la base de código (TASK-003)
- Corrección de deprecation warnings (fpdf2, @app.on_event, TemplateResponse) (TASK-003)
- Database connection pooling (TASK-003)
- Limpieza de dependencias no usadas: psycopg2-binary, pymongo, redis (TASK-003)
- Configuración de type checker mypy/pyright (TASK-004)
- Configuración de CI/CD GitHub Actions (TASK-004)
- Completar design.md y domain.md (TASK-004)
- Cambios en la UI, nuevos endpoints de negocio, o funcionalidades nuevas

## Current Behavior
- Contraseñas almacenadas y comparadas en texto plano (`routers/auth.py:19,126`)
- API Key de Groq hardcodeada en el código fuente (`routers/trainer.py:26`)
- Credenciales MySQL hardcodeadas (root, sin contraseña) (`database.py:7-10`)
- Session token = plain user_id en cookie, sin firma ni expiración (`routers/auth.py:26`)
- Sin protección CSRF en ningún endpoint
- Sin rate limiting
- Sin security headers
- Validación de inputs mínima (solo campos requeridos vía Form(...))

## Target Behavior
- Todas las contraseñas se almacenan y verifican con bcrypt (passlib)
- GROQ_API_KEY se lee de variable de entorno via os.getenv
- Credenciales MySQL se leen de variables de entorno con fallbacks para desarrollo local
- Autenticación mediante JWT:
  - Access token (15 min de duración) firmado con HS256
  - Refresh token (7 días, con rotación) almacenado en tabla refresh_tokens (hash)
  - Ambos tokens en httponly cookies
  - Middleware que verifica el token en rutas protegidas y renueva automáticamente si es necesario
- CSRF activo en todos los métodos POST, PUT, DELETE mediante doble submit cookie
- Security headers presentes en todas las respuestas HTTP
- Rate limiting: 5 intentos/min en /login, 60 req/min en el resto (slowapi)
- Inputs validados: email válido, tamaños de archivo razonables, sanitización de strings

## Acceptance Criteria
- [ ] Registro de usuario almacena password_hash con bcrypt (no texto plano)
- [ ] Login verifica contraseña contra hash bcrypt
- [ ] Login fallido con credenciales incorrectas (mismo mensaje de error para usuario inexistente o contraseña incorrecta)
- [ ] GROQ_API_KEY leída de .env, no visible en el código
- [ ] Credenciales MySQL leídas de .env con valores por defecto para localhost
- [ ] JWT access token se almacena en httponly cookie al hacer login/registro
- [ ] JWT refresh token se almacena en cookie separada y persiste en tabla refresh_tokens
- [ ] Refresh token con rotación: al usarlo se invalida el anterior y se emite uno nuevo
- [ ] Rutas protegidas redirigen a `/` sin cookie/token válido
- [ ] Logout invalida refresh token en BD y elimina cookies
- [ ] CSRF token presente en cookie no-httponly al cargar páginas con formularios
- [ ] Peticiones POST/PUT/DELETE sin X-CSRF-Token válido son rechazadas (403)
- [ ] Security headers presentes en todas las respuestas (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy)
- [ ] Rate limiting: más de 5 intentos de login/min desde misma IP recibe 429
- [ ] Subida de archivos rechaza tipo no imagen o tamaño excesivo (>10MB)
- [ ] Tests de auth actualizados con bcrypt y JWT
- [ ] Nuevos tests: CSRF middleware, rate limiting, security headers
- [ ] Todos los tests existentes pasan (con adaptaciones al nuevo flujo de auth)
- [ ] Cobertura global ≥ 70%
- [ ] Ruff lint pasa sin errores

## Edge Cases
- **Usuarios existentes**: las contraseñas en texto plano actuales no pueden migrarse a bcrypt. Se debe forzar reseteo de contraseña o informar que deberán registrarse de nuevo.
- **Refresh token rotation**: si el usuario usa un refresh token ya rotado (posible robo), se deben invalidar TODOS los refresh tokens de ese usuario.
- **Token expirado en mitad de una operación**: el middleware debe responder con 401 y el frontend redirigir al login.
- **CSRF token expirado**: el token CSRF tiene la misma vida que la sesión; si expira, se refresca al recargar la página.
- **Rate limit superado**: respuesta 429 con Retry-After header.
- **Múltiples pestañas/navegadores**: refresh token rotation puede causar race conditions si dos pestañas rotan simultáneamente. Se mitiga con un margen de gracia (el token rotado se acepta hasta 60s después de su rotación).

## Assumptions / Risks
- **Migración de contraseñas**: no es posible migrar hashes bcrypt desde texto plano. Se asume que los usuarios existentes serán notificados para restablecer su contraseña. Riesgo: pérdida de acceso temporal.
- **slowapi en memoria**: los contadores de rate limit se pierden al reiniciar el servidor. Asumible para un proyecto de TFG sin alta disponibilidad.
- **Race condition en refresh rotation**: el margen de gracia de 60s minimiza el impacto de rotaciones concurrentes.
- **JWT_SECRET_KEY**: debe generarse de forma segura (`openssl rand -hex 32`). Si se expone, todos los tokens son vulnerables.
- **Las dependencias nuevas (passlib, python-jose, slowapi) siguen la dependency-policy** y requieren ADRs antes de implementar.

## Database Impact

- **Change summary**: nueva tabla `refresh_tokens` para persistir refresh tokens con rotación
- **DB schema file from Source of Truth Map**: `agents/db/schema.sql`
- **DB change log file from Source of Truth Map**: `agents/db/changes.sql`
- **Affected structures/data**:
  - Nueva tabla: `refresh_tokens` con columnas id (PK), user_id (FK → users.id), token_hash (VARCHAR(255)), expires_at (DATETIME), revoked (BOOLEAN DEFAULT FALSE), created_at (DATETIME DEFAULT CURRENT_TIMESTAMP)
  - La tabla `users` no se modifica; `password_hash` VARCHAR(255) es suficiente para bcrypt (≈60 chars)
  - Los passwords existentes en texto plano NO son migrables
- **Forward migration approach**:
  ```sql
  CREATE TABLE IF NOT EXISTS refresh_tokens (
      id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT NOT NULL,
      token_hash VARCHAR(255) NOT NULL,
      expires_at DATETIME NOT NULL,
      revoked BOOLEAN DEFAULT FALSE,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
  );
  ```
- **Rollback approach**:
  ```sql
  DROP TABLE IF EXISTS refresh_tokens;
  -- Revertir auth.py al comportamiento anterior (texto plano)
  -- ATENCIÓN: los passwords ya hasheados con bcrypt NO se pueden revertir a texto plano
  ```
- **Persisted data compatibility**: los passwords en texto plano en la BD actual serán ilegibles para bcrypt. Se requiere migración de usuarios (reseteo de contraseña) o script one-time para eliminar usuarios existentes.
- **Operational risks**: rotación de refresh tokens puede causar conflictos en sesiones concurrentes. Mitigación con margen de gracia de 60s.
- **Validation plan**: tests unitarios de registro/login con bcrypt, tests de refresh token creation/rotation/revocation, tests de integración del flujo completo de auth
- **Backup/recovery notes**: hacer backup de la BD antes de aplicar migración por si se necesita restaurar usuarios legacy. La migración es destructiva para passwords existentes.

## Open Questions
- (ninguna por ahora — todas las decisiones se tomaron en la discusión de planificación)

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/decisions.md`
- `agents/docs/api.md`
- `agents/docs/dependency-policy.md`
- `agents/db/schema.sql`
- `agents/db/changes.sql`

## Decision Records
- ADRs read from `agents/docs/decisions.md`:
  - ADR-001: Estrategia de base de datos para tests (mock DB unit, SQLite integración)
  - ADR-002: Estrategia de mock para TensorFlow/Keras
  - ADR-003: Umbral de cobertura de código (70% global)
  - ADR-004: Herramientas de testing y lint (pytest, Ruff)
- New decisions to record after user approval (ADRs):
  - **ADR-005**: `bcrypt` (librería directa) para hashing de contraseñas en lugar de `passlib[bcrypt]` — incompatibilidad entre passlib 1.7.4 y bcrypt 5.0.0
  - **ADR-006**: `python-jose[cryptography]` para JWT
  - **ADR-007**: `slowapi` para rate limiting in-memory
  - **ADR-008**: Estrategia de refresh tokens con tabla en BD y rotación
