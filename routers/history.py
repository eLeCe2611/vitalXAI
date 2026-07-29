from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse

from database import get_db_connection
from services.auth_service import get_user_id_from_token

router = APIRouter()

@router.get("/api/history")
async def get_history(request: Request):
    try:
        user_id = get_user_id_from_token(request.cookies.get("access_token"))
        if not user_id:
            return JSONResponse(status_code=401, content={"error": "No autenticado"})

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, user_id, timestamp, model_name, original_image_path,
               xai_image_path, prediction_label, confidence_score, patient_name, pdf_path
        FROM consultations
        WHERE user_id = %s
        ORDER BY timestamp DESC
        """
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        conn.close()

        for row in records:
            row['timestamp'] = row['timestamp'].strftime("%Y-%m-%d %H:%M")

        return JSONResponse(content={"status": "success", "data": records})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def _check_consultation_ownership(consultation_id: int, user_id: int, allow_admin: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM consultations WHERE id = %s", (consultation_id,))
    consultation = cursor.fetchone()
    if not consultation:
        conn.close()
        return "not_found"
    if allow_admin:
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user and user["role"] == "admin":
            conn.close()
            return "ok"
    conn.close()
    if consultation["user_id"] != user_id:
        return "forbidden"
    return "ok"

@router.post("/api/history/update_name")
async def update_patient_name(request: Request, consultation_id: int = Form(...), new_name: str = Form(...)):
    try:
        user_id = get_user_id_from_token(request.cookies.get("access_token"))
        if not user_id:
            return JSONResponse(status_code=401, content={"error": "No autenticado"})
        ownership = _check_consultation_ownership(consultation_id, user_id, allow_admin=True)
        if ownership == "not_found":
            return JSONResponse(status_code=404, content={"error": "Consulta no encontrada"})
        if ownership == "forbidden":
            return JSONResponse(status_code=403, content={"error": "No tienes permiso para modificar esta consulta"})
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE consultations SET patient_name = %s WHERE id = %s", (new_name, consultation_id))
        conn.commit()
        conn.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.post("/api/history/delete")
async def delete_history_record(request: Request, consultation_id: int = Form(...)):
    try:
        user_id = get_user_id_from_token(request.cookies.get("access_token"))
        if not user_id:
            return JSONResponse(status_code=401, content={"error": "No autenticado"})
        ownership = _check_consultation_ownership(consultation_id, user_id, allow_admin=True)
        if ownership == "not_found":
            return JSONResponse(status_code=404, content={"error": "Consulta no encontrada"})
        if ownership == "forbidden":
            return JSONResponse(status_code=403, content={"error": "No tienes permiso para eliminar esta consulta"})
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultations WHERE id = %s", (consultation_id,))
        conn.commit()
        conn.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
