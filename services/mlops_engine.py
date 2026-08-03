import csv
import datetime
import json
import os
import shutil
import subprocess
import tkinter as tk
from contextlib import suppress
from tkinter import filedialog

LOG_FILE = "training_log.txt"
TRANSFORMER_MODELS = ["deit", "swin_base", "vit_384"]


def run_training_queue(session_id: str, models: list[str], dataset_path: str, epochs: int, batch_size: int, learning_rate: float):
    base_path = os.getcwd()
    script_train_cnn = os.path.join(base_path, "pneumoniacnn-main", "code", "1_train_kfold.py")
    script_train_trans = os.path.join(base_path, "pneumoniacnn-main", "code", "2_train_transformer_kfold.py")
    script_img = os.path.join(base_path, "pneumoniacnn-main", "code", "6_xai_qualitative.py")
    script_math = os.path.join(base_path, "pneumoniacnn-main", "code", "7_xai_quantitative.py")

    with open(LOG_FILE, "w", encoding="utf-8", errors="replace") as f:
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] SESI\u00d3N DE ENTRENAMIENTO INICIADA: {session_id}\n")
        f.write(f"Modelos a entrenar: {', '.join(models)}\n")
        f.write("-" * 60 + "\n")

    for model_name in models:
        env_vars = os.environ.copy()
        env_vars.update({
            "TFG_SESSION_ID": session_id, "TFG_MODEL_NAME": model_name,
            "TFG_DATASET_DIR": dataset_path, "TFG_EPOCHS": str(epochs),
            "TFG_BATCH_SIZE": str(batch_size), "TFG_LEARNING_RATE": str(learning_rate),
        })
        is_trans = model_name in TRANSFORMER_MODELS
        script_to_run = script_train_trans if is_trans else script_train_cnn
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
            tipo = "TRANSFORMER" if is_trans else "CNN"
            log.write(f"\n>>> INICIANDO ENTRENAMIENTO [{tipo}]: {model_name}\n")
            subprocess.Popen(["python", script_to_run], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
            log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [XAI AUTO] Generando mapas visuales para {model_name} (Script 6)...\n")
            subprocess.Popen(["python", script_img], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
            log.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [XAI AUTO] Calculando m\u00e9tricas matem\u00e1ticas reales para {model_name} (Script 7)...\n")
            subprocess.Popen(["python", script_math], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
            log.write(f"\n\u2705 [XAI AUTO] Explicabilidad completada para {model_name}.\n")

    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
        f.write(f"\n{'='*60}\n[{datetime.datetime.now().strftime('%H:%M:%S')}] ENTRENAMIENTOS COMPLETADOS.\n")
        f.write("Generando Ranking Global y Matriz de Wilcoxon...\n")
    env_vars_comp = os.environ.copy()
    env_vars_comp["TFG_SESSION_ID"] = session_id
    script_comp_path = os.path.join(base_path, "pneumoniacnn-main", "code", "3_evaluate_statistics.py")
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        subprocess.Popen(["python", script_comp_path], stdout=log, stderr=subprocess.STDOUT, env=env_vars_comp, text=True, encoding="utf-8", errors="replace").wait()
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [SESI\u00d3N COMPLETADA Y COMPARADA]\n")


def run_xai_evaluation(session_id: str, model_name: str, dataset_path: str) -> None:
    base_path = os.getcwd()
    env_vars = os.environ.copy()
    env_vars.update({"TFG_SESSION_ID": session_id, "TFG_MODEL_NAME": model_name, "TFG_DATASET_DIR": dataset_path})
    script_img = os.path.join(base_path, "pneumoniacnn-main", "code", "6_xai_qualitative.py")
    script_math = os.path.join(base_path, "pneumoniacnn-main", "code", "7_xai_quantitative.py")
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [MODO MANUAL] 1/2: Generando Mapas XAI...\n")
        subprocess.Popen(["python", script_img], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [MODO MANUAL] 2/2: Calculando M\u00e9tricas Cuantitativas...\n")
        subprocess.Popen(["python", script_math], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        log.write("\n\u2705 [PROCESO XAI MANUAL COMPLETADO]\n")


def run_statistical_comparison(session_id: str) -> None:
    base_path = os.getcwd()
    env_vars = os.environ.copy()
    env_vars["TFG_SESSION_ID"] = session_id
    script_path = os.path.join(base_path, "pneumoniacnn-main", "code", "3_evaluate_statistics.py")
    _clear_recalc_status(session_id)
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Recalculando estad\u00edsticas de la sesi\u00f3n {session_id}...\n")
        subprocess.Popen(["python", script_path], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        log.write("\n\u2705 [COMPARACI\u00d3N COMPLETADA]\n")
    _mark_recalc_completed(session_id)


def _recalc_status_path(session_id: str) -> str:
    return os.path.join("training_results", session_id, "recalc_complete.txt")


def _clear_recalc_status(session_id: str) -> None:
    path = _recalc_status_path(session_id)
    with suppress(OSError):
        os.remove(path)

def _mark_recalc_completed(session_id: str) -> None:
    path = _recalc_status_path(session_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(datetime.datetime.now().isoformat())


def get_recalc_status(session_id: str) -> str:
    return "completed" if os.path.exists(_recalc_status_path(session_id)) else "running"


def run_external_validation(session_id: str, dataset_path: str) -> None:
    base_path = os.getcwd()
    env_vars = os.environ.copy()
    env_vars["TFG_SESSION_ID"] = session_id
    env_vars["TFG_EXTERNAL_DATASET_DIR"] = dataset_path
    script_val = os.path.join(base_path, "pneumoniacnn-main", "code", "4_external_validation.py")
    script_delong = os.path.join(base_path, "pneumoniacnn-main", "code", "5_evaluate_delong.py")
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando Validaci\u00f3n Externa para sesi\u00f3n {session_id}...\n")
        subprocess.Popen(["python", script_val], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Calculando Test Estad\u00edstico de DeLong...\n")
        subprocess.Popen(["python", script_delong], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        log.write("\n\u2705 [VALIDACI\u00d3N EXTERNA COMPLETADA]\n")


def browse_folder():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(title="Selecciona la carpeta del Dataset")
        root.destroy()
        return {"path": folder}
    except Exception:
        return None


def _verify_session_ownership(session_id: str, user_id: int) -> bool:
    config_path = os.path.join("training_results", session_id, "config.json")
    if not os.path.exists(config_path):
        return False
    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        return config.get("user_id") == user_id
    except (json.JSONDecodeError, OSError):
        return False


def create_training_session(model_names: str, dataset_path: str, epochs: int, batch_size: int, learning_rate: float, user_id: int | None = None):
    session_id = f"RUN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_dir = f"training_results/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    with open(os.path.join(session_dir, "dataset_path.txt"), "w", encoding="utf-8") as f:
        f.write(dataset_path)
    config = {"dataset_path": dataset_path, "epochs": epochs, "batch_size": batch_size, "learning_rate": learning_rate, "models": [m.strip() for m in model_names.split(",")]}
    if user_id is not None:
        config["user_id"] = user_id
    with open(os.path.join(session_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f)
    return session_id


def get_model_results_data(session_id: str, model_name: str):
    model_dir = f"training_results/{session_id}/{model_name}"
    csv_path = f"{model_dir}/kfold_results.csv"
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data.append(row)
    images = [f"/training_results/{session_id}/{model_name}/{f}" for f in os.listdir(model_dir) if f.endswith(".png")]
    calib = {"brier": "-", "ece": "-"}
    calib_path = f"{model_dir}/calibration_metrics.txt"
    if os.path.exists(calib_path):
        with open(calib_path, encoding="utf-8") as f:
            for line in f:
                if "Brier" in line: calib["brier"] = line.split(":")[1].strip()
                if "ECE" in line: calib["ece"] = line.split(":")[1].strip()
    xai_metrics = []
    xai_csv = f"{model_dir}/xai_metrics_comparison.csv"
    if os.path.exists(xai_csv):
        with open(xai_csv, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                xai_metrics.append(row)
    return {"data": data, "images": images, "calib": calib, "xai_metrics": xai_metrics}


def get_trained_sessions(user_id: int | None = None):
    base_dir = "training_results"
    if not os.path.exists(base_dir):
        return []
    sessions = []
    for folder in sorted(os.listdir(base_dir), reverse=True):
        path = os.path.join(base_dir, folder)
        if os.path.isdir(path):
            if user_id is not None and not _verify_session_ownership(folder, user_id):
                continue
            models = [m for m in os.listdir(path) if os.path.exists(os.path.join(path, m, "kfold_results.csv"))]
            if models:
                sessions.append({"session_id": folder, "models": models})
    return sessions


def get_session_ranking_data(session_id: str):
    session_dir = f"training_results/{session_id}"
    csv_path = f"{session_dir}/session_ranking.csv"
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data.append(row)
    heatmap = f"/training_results/{session_id}/wilcoxon_heatmap.png"
    config = {}
    config_path = f"{session_dir}/config.json"
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    elif os.path.exists(f"{session_dir}/dataset_path.txt"):
        with open(f"{session_dir}/dataset_path.txt", encoding="utf-8") as f:
            config["dataset_path"] = f.read().strip()
    return {"ranking": data, "heatmap": heatmap, "config": config}


def resolve_dataset_path(session_id: str, dataset_path: str) -> str | None:
    if dataset_path:
        return dataset_path
    saved = f"training_results/{session_id}/dataset_path.txt"
    if os.path.exists(saved):
        with open(saved, encoding="utf-8") as f:
            return f.read().strip()
    return None


def safe_rename(old_name: str, new_name: str) -> tuple[int, dict]:
    safe = "".join(c for c in new_name if c.isalnum() or c in (" ", "-", "_")).strip()
    if not safe:
        return 400, {"status": "error", "message": "El nombre no es v\u00e1lido."}
    new_path = os.path.join("training_results", safe)
    old_path = os.path.join("training_results", old_name)
    if os.path.exists(new_path):
        return 400, {"status": "error", "message": "Ya existe."}
    if not os.path.exists(old_path):
        return 404, {"status": "error", "message": "Sesi\u00f3n no encontrada."}
    os.rename(old_path, new_path)
    return 200, {"status": "success", "new_name": safe}


def delete_session(session_id: str) -> tuple[int, dict]:
    path = os.path.join("training_results", session_id)
    if not os.path.exists(path):
        return 404, {"status": "error", "message": "Sesi\u00f3n no encontrada."}
    shutil.rmtree(path)
    return 200, {"status": "success", "message": "Sesi\u00f3n eliminada."}


def get_external_results_data(session_id: str):
    session_dir = f"training_results/{session_id}/external_validation"
    csv_path = f"{session_dir}/external_validation_metrics.csv"
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data.append(row)
    return {"metrics": data, "roc": f"/training_results/{session_id}/external_validation/roc_external_validation.png", "delong": f"/training_results/{session_id}/external_validation/delong_heatmap.png"}
