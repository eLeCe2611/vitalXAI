from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from database import get_db_connection
from services import mlops_engine
from services.auth_service import get_user_id_from_token

router = APIRouter()


def _require_admin(request: Request):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return None, None
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user or user["role"] != "admin":
        return user_id, False
    return user_id, True


@router.get("/api/admin/users")
async def admin_users(request: Request):
    user_id, is_admin = _require_admin(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not is_admin:
        return JSONResponse(status_code=403, content={"error": "Se requieren permisos de administrador"})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id, u.username, u.first_name, u.last_name, u.role,
               COUNT(DISTINCT c.id) AS diagnosis_count
        FROM users u
        LEFT JOIN consultations c ON c.user_id = u.id
        GROUP BY u.id
        ORDER BY u.username
    """)
    users = cursor.fetchall()
    conn.close()

    import json as _json
    import os as _os
    sessions_by_user = {}
    base_dir = "training_results"
    if _os.path.exists(base_dir):
        for folder in _os.listdir(base_dir):
            cfg_path = _os.path.join(base_dir, folder, "config.json")
            if _os.path.exists(cfg_path):
                try:
                    with open(cfg_path, encoding="utf-8") as _f:
                        cfg = _json.load(_f)
                    uid = cfg.get("user_id")
                    if uid is not None:
                        sessions_by_user[uid] = sessions_by_user.get(uid, 0) + 1
                except Exception:
                    pass

    for u in users:
        u["lab_count"] = sessions_by_user.get(u["id"], 0)

    return JSONResponse(content={"status": "success", "users": users})


@router.get("/api/admin/users/{user_id}/consultations")
async def admin_user_consultations(request: Request, user_id: int):
    admin_id, is_admin = _require_admin(request)
    if not admin_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not is_admin:
        return JSONResponse(status_code=403, content={"error": "Se requieren permisos de administrador"})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    target = cursor.fetchone()
    if not target:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Usuario no encontrado"})

    cursor.execute("""
        SELECT id, user_id, timestamp, model_name, original_image_path,
               xai_image_path, prediction_label, confidence_score, patient_name, pdf_path
        FROM consultations
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """, (user_id,))
    consultations = cursor.fetchall()

    conn.close()

    for row in consultations:
        row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M")

    sessions = mlops_engine.get_trained_sessions(user_id=user_id)

    return JSONResponse(content={
        "status": "success",
        "consultations": consultations,
        "training_sessions": sessions
    })


@router.get("/api/admin/consultations/{consultation_id}")
async def admin_get_consultation(request: Request, consultation_id: int):
    admin_id, is_admin = _require_admin(request)
    if not admin_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not is_admin:
        return JSONResponse(status_code=403, content={"error": "Se requieren permisos de administrador"})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, user_id, timestamp, model_name, original_image_path,
               xai_image_path, prediction_label, confidence_score, patient_name, pdf_path
        FROM consultations WHERE id = %s
    """, (consultation_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return JSONResponse(status_code=404, content={"error": "Consulta no encontrada"})
    row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M") if row["timestamp"] else ""
    return JSONResponse(content={"status": "success", "consultation": row})
