"""
trainer.py (FACHADA LIGERA - Rutas MLOPS)
"""
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from fastapi import APIRouter, BackgroundTasks, Form, Request
from fastapi.responses import JSONResponse

from services import mlops_engine
from services.auth_service import get_user_id_from_token
from services.chatbot_service import chat_endpoint as _chat_endpoint
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


def _require_ownership(session_id: str, user_id: int) -> bool:
    return mlops_engine._verify_session_ownership(session_id, user_id)


@router.post("/api/chat")
async def chat_route(request: Request, session_id: str = Form(...), message: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    return await _chat_endpoint(session_id, message)


@router.get("/api/train/browse")
async def browse_folder(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    result = mlops_engine.browse_folder()
    if result is None:
        return JSONResponse(status_code=500, content={"error": "No se pudo abrir el explorador."})
    return result


@router.post("/api/train/start")
async def start_training(request: Request, background_tasks: BackgroundTasks, model_names: str = Form(...), dataset_path: str = Form(...), epochs: int = Form(...), batch_size: int = Form(...), learning_rate: float = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not dataset_path or not os.path.exists(dataset_path):
        return JSONResponse(status_code=400, content={"status": "error", "message": "La ruta no existe."})
    session_id = mlops_engine.create_training_session(model_names, dataset_path, epochs, batch_size, learning_rate, user_id=user_id)
    background_tasks.add_task(run_training_queue, session_id, [m.strip() for m in model_names.split(",")], dataset_path, epochs, batch_size, learning_rate)
    return JSONResponse(content={"status": "success", "message": f"Iniciada sesi\u00f3n {session_id}."})


@router.get("/api/train/logs")
async def get_training_logs(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"logs": "Esperando..."})
    with open(LOG_FILE, encoding="utf-8", errors="replace") as f:
        return JSONResponse(content={"logs": "".join(f.readlines()[-60:])})


@router.get("/api/train/models")
async def get_trained_sessions(request: Request):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    return JSONResponse(content={"status": "success", "sessions": mlops_engine.get_trained_sessions(user_id=user_id)})


@router.get("/api/train/results/{session_id}/{model_name}")
async def get_model_results(request: Request, session_id: str, model_name: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    result = mlops_engine.get_model_results_data(session_id, model_name)
    if result is None:
        return JSONResponse(status_code=404, content={"error": "Resultados no encontrados"})
    return JSONResponse(content={"status": "success", **result})


@router.post("/api/train/run_eval")
async def run_evaluation_script(request: Request, session_id: str = Form(...), model_name: str = Form(...), dataset_path: str = Form("")):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    resolved = mlops_engine.resolve_dataset_path(session_id, dataset_path)
    if not resolved or not os.path.exists(resolved):
        return JSONResponse(status_code=400, content={"status": "error", "message": "No se encontr\u00f3 la ruta del dataset original."})
    mlops_engine.run_xai_evaluation(session_id, model_name, resolved)
    return JSONResponse(content={"status": "success", "message": "Generaci\u00f3n completada. Recargando..."})


@router.delete("/api/train/session/{session_id}")
async def delete_session(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para eliminar esta sesi\u00f3n"})
    status, content = mlops_engine.delete_session(session_id)
    return JSONResponse(status_code=status, content=content)


@router.post("/api/train/session/rename")
async def rename_session(request: Request, old_name: str = Form(...), new_name: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(old_name, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para renombrar esta sesi\u00f3n"})
    status, content = mlops_engine.safe_rename(old_name, new_name)
    return JSONResponse(status_code=status, content=content)


@router.post("/api/train/session/compare")
async def compare_session_models(request: Request, background_tasks: BackgroundTasks, session_id: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    background_tasks.add_task(mlops_engine.run_statistical_comparison, session_id)
    return JSONResponse(content={"status": "success", "message": "Rec\u00e1lculo iniciado."})


@router.get("/api/train/session/{session_id}/ranking")
async def get_session_ranking(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    result = mlops_engine.get_session_ranking_data(session_id)
    if result is None:
        return JSONResponse(status_code=404, content={"error": "A\u00fan no se ha comparado esta sesi\u00f3n."})
    return JSONResponse(content={"status": "success", **result})


@router.post("/api/train/session/external_validation")
async def run_external_validation(request: Request, background_tasks: BackgroundTasks, session_id: str = Form(...), dataset_path: str = Form(...)):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    if not dataset_path or not os.path.exists(dataset_path):
        return JSONResponse(status_code=400, content={"status": "error", "message": "La ruta del dataset externo no es v\u00e1lida."})
    background_tasks.add_task(mlops_engine.run_external_validation, session_id, dataset_path)
    return JSONResponse(content={"status": "success", "message": "Validaci\u00f3n Externa iniciada."})


@router.get("/api/train/session/{session_id}/external_results")
async def get_external_validation_results(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    result = mlops_engine.get_external_results_data(session_id)
    if result is None:
        return JSONResponse(status_code=404, content={"error": "A\u00fan no hay resultados de validaci\u00f3n externa."})
    return JSONResponse(content={"status": "success", **result})


@router.get("/api/train/session/{session_id}/report")
async def pdf_report_route(request: Request, session_id: str):
    user_id = _require_auth(request)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})
    if not _require_ownership(session_id, user_id):
        return JSONResponse(status_code=403, content={"error": "No tienes permiso para acceder a esta sesi\u00f3n"})
    return await _generate_pdf_report(session_id)
