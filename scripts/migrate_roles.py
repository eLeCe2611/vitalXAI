"""
Script unico de migracion: normaliza roles legacy a admin/doctor.

Ejecutar UNA SOLA VEZ:
    python scripts/migrate_roles.py

Mapeo:
  - "Radiologo Jefe" -> "admin"
  - cualquier otro valor -> "doctor"
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection


def migrate():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    updated = 0
    for user in users:
        old_role = user["role"]
        if old_role == "admin" or old_role == "doctor":
            continue
        new_role = "admin" if old_role in ("Radiologo Jefe", "Radi\u00f3logo Jefe") else "doctor"
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user["id"]))
        updated += 1
        print(f"  [{user['username']}] '{old_role}' -> '{new_role}'")

    conn.commit()
    conn.close()
    print(f"\nMigracion completada: {updated} usuarios actualizados.")


if __name__ == "__main__":
    migrate()
