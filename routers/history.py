from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse

from database import get_db_connection

router = APIRouter()

@router.get("/api/history")
async def get_history(request: Request):
    try:
        user_id = request.cookies.get("session_token")
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

@router.post("/api/history/update_name")
async def update_patient_name(consultation_id: int = Form(...), new_name: str = Form(...)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE consultations SET patient_name = %s WHERE id = %s", (new_name, consultation_id))
        conn.commit()
        conn.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.post("/api/history/delete")
async def delete_history_record(consultation_id: int = Form(...)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultations WHERE id = %s", (consultation_id,))
        conn.commit()
        conn.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
