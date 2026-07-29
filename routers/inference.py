import datetime
import os
import shutil

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse

from database import get_db_connection
from services.auth_service import get_user_id_from_token

# IMPORTANTE: Estas importaciones asumen que tienes estos archivos en la carpeta services/
from services.ml_engine import process_and_predict
from services.pdf_generator import generate_medical_report
from services.xai_generator import generate_xai_heatmap

_ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/jpg"}
_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter()

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

        # 1. Guardar archivo subido
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"

        # Asegúrate de que static/uploads/ existe
        os.makedirs(os.path.join("static", "uploads"), exist_ok=True)
        upload_path = os.path.join("static", "uploads", filename)

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Inferencia ML
        label, confidence = process_and_predict(model_name, upload_path)

        # 3. Generar Mapa de Calor (XAI)
        os.makedirs(os.path.join("static", "results"), exist_ok=True)
        xai_filename = f"xai_{filename}"
        xai_path = os.path.join("static", "results", xai_filename)
        generate_xai_heatmap(model_name, upload_path, xai_path)

        # 4. Generar Reporte PDF
        pdf_path = generate_medical_report(upload_path, xai_path, label, confidence, model_name)

        # 5. Guardar en Base de Datos
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM consultations WHERE user_id = %s AND model_name = %s", (user_id, model_name))
        count_previous = cursor.fetchone()[0]
        current_number = count_previous + 1

        default_patient_name = f"Paciente sin nombre {model_name} #{current_number}"

        query = """
        INSERT INTO consultations
        (user_id, model_name, original_image_path, xai_image_path, prediction_label, confidence_score, patient_name, pdf_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, model_name, upload_path, xai_path, label, confidence, default_patient_name, pdf_path))
        conn.commit()
        conn.close()

        # 6. Respuesta JSON
        return JSONResponse(content={
            "status": "success",
            "label": label,
            "confidence": confidence,
            "original_image": f"/{upload_path}",
            "xai_image": f"/{xai_path}",
            "pdf_report": f"/{pdf_path}",
            "model_used": model_name
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
