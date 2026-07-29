"""
Script único de migración: convierte contraseñas legacy (texto plano) a bcrypt.

Ejecutar UNA SOLA VEZ después de aplicar TASK-002:
    python scripts/migrate_passwords.py

Los passwords legacy se detectan porque NO empiezan con "$2b$".
Los passwords ya en bcrypt se saltan.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt

from database import get_db_connection


def migrate():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, username, password_hash FROM users")
    users = cursor.fetchall()

    migrated = 0
    skipped = 0

    for user in users:
        pwh = user["password_hash"]
        if pwh and pwh.startswith("$2b$"):
            skipped += 1
            print(f"  [{user['username']}] ya en bcrypt, saltando")
            continue

        if not pwh:
            skipped += 1
            print(f"  [{user['username']}] sin password, saltando")
            continue

        new_hash = bcrypt.hashpw(pwh.encode(), bcrypt.gensalt()).decode()
        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user["id"]))
        migrated += 1
        print(f"  [{user['username']}] migrado: '{pwh[:10]}...' → bcrypt")

    conn.commit()
    conn.close()
    print(f"\n✅ Migración completada: {migrated} migrados, {skipped} ya en bcrypt")


if __name__ == "__main__":
    migrate()
