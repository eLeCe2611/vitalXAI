
import json
import os

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from database import get_db_connection
from services.auth_service import get_user_id_from_token

router = APIRouter()


def _get_queue_position(job_id: int, job_type: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) AS pos FROM job_queue
        WHERE status = 'queued'
          AND (
            CASE job_type WHEN 'training' THEN 1 ELSE 0 END < CASE %s WHEN 'training' THEN 1 ELSE 0 END
            OR (
              CASE job_type WHEN 'training' THEN 1 ELSE 0 END = CASE %s WHEN 'training' THEN 1 ELSE 0 END
              AND id < %s
            )
          )
    """, (job_type, job_type, job_id))
    row = cursor.fetchone()
    conn.close()
    return (row["pos"] if row else 0) + 1


@router.get("/api/queue/status")
async def queue_status(request: Request):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, job_type, status, payload, created_at, started_at, finished_at, error_message
        FROM job_queue
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 20
    """, (user_id,))
    jobs = cursor.fetchall()
    conn.close()

    now_queued = [j for j in jobs if j["status"] == "queued"]
    now_running = [j for j in jobs if j["status"] == "running"]

    for j in jobs:
        for key in ("created_at", "started_at", "finished_at"):
            if j[key]:
                j[key] = j[key].strftime("%H:%M:%S") if hasattr(j[key], "strftime") else str(j[key])
        if j["status"] == "queued":
            j["position"] = _get_queue_position(j["id"], j["job_type"])
        if j["job_type"] == "diagnosis":
            p = j["payload"]
            if isinstance(p, str):
                try:
                    p = json.loads(p)
                except Exception:
                    p = {}
            j["model_name"] = p.get("model_name", "?")
        elif j["job_type"] == "training":
            p = j["payload"]
            if isinstance(p, str):
                try:
                    p = json.loads(p)
                except Exception:
                    p = {}
            j["session_id"] = p.get("session_id", "?")
            models = p.get("models", [])
            j["model_name"] = ", ".join(models) if models else "?"
        elif j["job_type"] == "external_validation":
            p = j["payload"]
            if isinstance(p, str):
                try:
                    p = json.loads(p)
                except Exception:
                    p = {}
            j["session_id"] = p.get("session_id", "?")
            session_models = []
            config_path = os.path.join("training_results", j["session_id"], "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, encoding="utf-8") as f:
                        cfg = json.load(f)
                    session_models = cfg.get("models", [])
                except (json.JSONDecodeError, OSError):
                    session_models = []
            j["model_name"] = ", ".join(session_models) if session_models else "Todos los modelos"
        del j["payload"]

    return JSONResponse(content={
        "status": "success",
        "jobs": jobs,
        "has_pending": len(now_queued) + len(now_running) > 0,
        "queued_count": len(now_queued),
    })


@router.delete("/api/queue/cancel/{job_id}")
async def cancel_job(request: Request, job_id: int):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'cancelled', finished_at = NOW() WHERE id = %s AND user_id = %s AND status = 'queued'",
        (job_id, user_id)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    if affected == 0:
        return JSONResponse(status_code=404, content={"error": "Trabajo no encontrado o ya no est\u00e1 en cola"})
    return JSONResponse(content={"status": "success", "message": "Trabajo cancelado"})
