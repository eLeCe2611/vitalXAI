-- DB change log

[TASK-002] Añadir tabla refresh_tokens para JWT refresh tokens con rotación
Date: 2026-07-23
Forward:
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
Rollback:
DROP TABLE IF EXISTS refresh_tokens;
-- ATENCIÓN: Los passwords existentes se migraron a bcrypt. Rollback de auth requiere restaurar copia de BD anterior.

[TASK-002] Migrar autenticación de texto plano a bcrypt + JWT
Date: 2026-07-23
Forward:
-- No hay cambios de esquema en users. password_hash VARCHAR(255) soporta bcrypt (60 chars).
-- Los usuarios existentes con contraseñas en texto plano deben restablecer su contraseña.
Rollback:
-- No es posible revertir hashes bcrypt a texto plano. Restaurar desde backup.

[TASK-004] Añadir FK y NOT NULL a training_jobs.user_id; completar init_db con todas las tablas
Date: 2026-07-24
Forward:
ALTER TABLE training_jobs MODIFY user_id INT NOT NULL;
ALTER TABLE training_jobs ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
Rollback:
ALTER TABLE training_jobs DROP FOREIGN KEY training_jobs_ibfk_1;
ALTER TABLE training_jobs MODIFY user_id INT NULL;
