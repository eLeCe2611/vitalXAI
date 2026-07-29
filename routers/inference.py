import datetime
import json
import os
import shutil

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse

from database import get_db_connection
from services.auth_service import get_user_id_from_token

_ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/jpg"}
_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter()


def _enqueue_job(user_id: int, job_type: str, payload: dict) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO job_queue (user_id, job_type, payload) VALUES (%s, %s, %s)",
        (user_id, job_type, json.dumps(payload))
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id


def _queue_position(job_id: int, job_type: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) AS pos FROM job_queue
        WHERE status = 'queued'
          AND (
            CASE job_type WHEN 'diagnosis' THEN 0 ELSE 1 END < CASE %s WHEN 'diagnosis' THEN 0 ELSE 1 END
            OR (
              CASE job_type WHEN 'diagnosis' THEN 0 ELSE 1 END = CASE %s WHEN 'diagnosis' THEN 0 ELSE 1 END
              AND id < %s
            )
          )
    """, (job_type, job_type, job_id))
    row = cursor.fetchone()
    conn.close()
    return (row["pos"] if row else 0) + 1


@router.post("/predict")
async def predict(request: Request, file: UploadFile = File(...), model_name: str = Form(...)):  # noqa: B008
    try:
        user_id = get_user_id_from_token(request.cookies.get("access_token"))
        if not user_id:
            return JSONResponse(status_code=401, content={"error": "No autenticado"})

        if file.content_type not in _ALLOWED_MIME_TYPES:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Solo se permiten imágenes (JPEG/PNG)"}
            )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > _MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "La imagen no puede superar los 10 MB"}
            )

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        os.makedirs(os.path.join("static", "uploads"), exist_ok=True)
        upload_path = os.path.join("static", "uploads", filename)

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        job_id = _enqueue_job(user_id, "diagnosis", {
            "model_name": model_name,
            "image_path": upload_path,
        })
        position = _queue_position(job_id, "diagnosis")

        return JSONResponse(content={
            "status": "queued",
            "job_id": job_id,
            "position": position,
            "message": f"Diagnóstico encolado en posición {position}"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
