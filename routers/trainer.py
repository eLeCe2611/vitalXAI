"""
trainer.py (FACHADA LIGERA - Rutas MLOPS)
"""
import json
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from fastapi import APIRouter, BackgroundTasks, Form, Request
from fastapi.responses import JSONResponse

from database import get_db_connection
from services import mlops_engine
from services.auth_service import get_user_id_from_token
from services.chatbot_service import chat_endpoint as _chat_endpoint
from services.lang import get_lang_from_cookie, get_text
from services.pdf_generator_mlops import generate_pdf_report as _generate_pdf_report

# Re-export for backward compatibility with tests
run_training_queue = mlops_engine.run_training_queue

router = APIRouter()
LOG_FILE = mlops_engine.LOG_FILE
TRANSFORMER_MODELS = mlops_engine.TRANSFORMER_MODELS


def _require_auth(request: Request):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return None
    return user_id


def _require_ownership(session_id: str, user_id: int, request: Request | None = None) -> bool:
    if mlops_engine._verify_session_ownership(session_id, user_id):
        return True
    if request is not None:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user and user["role"] == "admin":
            return True
    return False


@router.post("/api/chat")
async def chat_route(request: Request, session_id: str = Form(...), message: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    return await _chat_endpoint(session_id, message, request)


@router.get("/api/train/browse")
async def browse_folder(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    result = mlops_engine.browse_folder()
    if result is None:
        return JSONResponse(status_code=500, content={"error": "No se pudo abrir el explorador."})
    return result


@router.post("/api/train/start")
async def start_training(request: Request, model_names: str = Form(...), dataset_path: str = Form(...), epochs: int = Form(...), batch_size: int = Form(...), learning_rate: float = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not dataset_path or not os.path.exists(dataset_path):
        return JSONResponse(status_code=400, content={"status": "error", "message": get_text("ruta_no_existe")})
    session_id = mlops_engine.create_training_session(model_names, dataset_path, epochs, batch_size, learning_rate, user_id=user_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO job_queue (user_id, job_type, payload) VALUES (%s, %s, %s)",
        (user_id, "training", json.dumps({
            "session_id": session_id,
            "models": [m.strip() for m in model_names.split(",")],
            "dataset_path": dataset_path,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
        }))
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()

    lang = get_lang_from_cookie(request)
    return JSONResponse(content={"status": "queued", "job_id": job_id, "session_id": session_id,
                                  "message": get_text("entrenamiento_encolado").format(job_id=job_id)})


@router.get("/api/train/logs")
async def get_training_logs(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"logs": get_text("esperando_logs")})
    with open(LOG_FILE, encoding="utf-8", errors="replace") as f:
        return JSONResponse(content={"logs": "".join(f.readlines()[-60:])})


@router.get("/api/train/models")
async def get_trained_sessions(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    return JSONResponse(content={"status": "success", "sessions": mlops_engine.get_trained_sessions(user_id=user_id)})


@router.get("/api/train/results/{session_id}/{model_name}")
async def get_model_results(request: Request, session_id: str, model_name: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    result = mlops_engine.get_model_results_data(session_id, model_name)
    if result is None:
        return JSONResponse(status_code=404, content={"error": get_text("resultados_no_encontrados")})
    return JSONResponse(content={"status": "success", **result})


@router.post("/api/train/run_eval")
async def run_evaluation_script(request: Request, session_id: str = Form(...), model_name: str = Form(...), dataset_path: str = Form("")):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    resolved = mlops_engine.resolve_dataset_path(session_id, dataset_path)
    if not resolved or not os.path.exists(resolved):
        return JSONResponse(status_code=400, content={"status": "error", "message": get_text("dataset_no_encontrado")})
    mlops_engine.run_xai_evaluation(session_id, model_name, resolved)
    return JSONResponse(content={"status": "success", "message": "Generaci\u00f3n completada. Recargando..."})


@router.delete("/api/train/session/{session_id}")
async def delete_session(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_eliminar")})
    status, content = mlops_engine.delete_session(session_id)
    return JSONResponse(status_code=status, content=content)


@router.post("/api/train/session/rename")
async def rename_session(request: Request, old_name: str = Form(...), new_name: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(old_name, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_renombrar")})
    status, content = mlops_engine.safe_rename(old_name, new_name)
    return JSONResponse(status_code=status, content=content)


@router.post("/api/train/session/compare")
async def compare_session_models(request: Request, background_tasks: BackgroundTasks, session_id: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    background_tasks.add_task(mlops_engine.run_statistical_comparison, session_id)
    return JSONResponse(content={"status": "success", "message": get_text("recalculo_iniciado")})


@router.get("/api/train/session/{session_id}/ranking")
async def get_session_ranking(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    result = mlops_engine.get_session_ranking_data(session_id)
    if result is None:
        return JSONResponse(status_code=404, content={"error": get_text("sesion_no_comparada")})
    return JSONResponse(content={"status": "success", **result})


@router.post("/api/train/session/external_validation")
async def run_external_validation(request: Request, background_tasks: BackgroundTasks, session_id: str = Form(...), dataset_path: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    if not dataset_path or not os.path.exists(dataset_path):
        return JSONResponse(status_code=400, content={"status": "error", "message": get_text("ruta_externa_invalida")})
    background_tasks.add_task(mlops_engine.run_external_validation, session_id, dataset_path)
    return JSONResponse(content={"status": "success", "message": get_text("validacion_externa_iniciada")})


@router.get("/api/train/session/{session_id}/external_results")
async def get_external_validation_results(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    result = mlops_engine.get_external_results_data(session_id)
    if result is None:
        return JSONResponse(status_code=404, content={"error": get_text("sin_resultados_externos")})
    return JSONResponse(content={"status": "success", **result})


@router.get("/api/train/session/{session_id}/report")
async def pdf_report_route(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})
    if not _require_ownership(session_id, user_id, request):
        return JSONResponse(status_code=403, content={"error": get_text("no_permiso_sesion")})
    return await _generate_pdf_report(session_id)
