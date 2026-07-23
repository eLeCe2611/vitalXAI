"""
trainer.py (VERSIÓN DEFINITIVA MLOPS - HÍBRIDA CNN/TRANSFORMERS + PDF + XAI)
"""
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import csv
import datetime
import json
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog

from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import FileResponse, JSONResponse
from fpdf import FPDF

# === INTEGRACIÓN GROQ AI (Llama 3) ===
from groq import Groq

# Leer API Key desde variable de entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    print("AVISO: GROQ_API_KEY no configurada. El chatbot no funcionará.")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Eres 'X-Ray Consultant AI', un asistente experto en MLOps e Inteligencia Artificial médica.
Tu objetivo principal es ayudar al usuario a lanzar un entrenamiento de redes neuronales para detectar neumonía en radiografías.

Debes recolectar conversando estos 5 datos:
1. Ruta del dataset (Sugiere al usuario usar el botón 'Explorar Carpeta' debajo del chat si no la sabe).
2. Arquitecturas a entrenar (Modelos CNN: ResNet50, ResNet101, ResNet152, ResNet50V2, EfficientNetB0, EfficientNetB3, EfficientNetB7, EfficientNetV2S, DenseNet121, DenseNet201, MobileNetV2, MobileNetV3Large, VGG16, InceptionV3, Xception, ConvNeXtTiny. Modelos Transformers: deit, swin_base, vit_384).
3. Épocas (por defecto 20).
4. Batch Size (16, 32 o 64, por defecto 32).
5. Learning Rate (ej: 0.01, 0.001, 0.0001, por defecto 0.001).

COMPORTAMIENTO:
- Puedes hablar de CUALQUIER tema que el usuario proponga, pero siempre intenta reconducir sutilmente al entrenamiento.
- Si el usuario te dice que quiere REUTILIZAR una configuración anterior, NO lances el entrenamiento de golpe. Enumérale los parámetros y pregúntale si quiere cambiar algo.
- Sé muy natural, empático y directo. No uses formatos complejos.

REGLA CRÍTICA Y ABSOLUTA DE SISTEMA:
Cuando tengas los 5 datos claros y CONFIRMADOS DEFINITIVAMENTE por el usuario, DEBES responder ÚNICAMENTE con un bloque JSON exacto.
Ese JSON será leído por el sistema para arrancar las máquinas. No escribas texto antes ni después del JSON.

Formato exacto de tu última respuesta:
{
  "ready": true,
  "dataset_path": "ruta/extraida/del/chat",
  "models": "ResNet50,swin_base",
  "epochs": 20,
  "batch_size": 32,
  "learning_rate": 0.001
}
"""

chat_sessions = {}
router = APIRouter()
LOG_FILE = "training_log.txt"
TRANSFORMER_MODELS = ["deit", "swin_base", "vit_384"]

# === RUTAS DEL CHATBOT ===
@router.post("/api/chat")
async def chat_endpoint(session_id: str = Form(...), message: str = Form(...)):
    try:
        if session_id not in chat_sessions:
            chat_sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

        chat_sessions[session_id].append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_sessions[session_id],
            temperature=0.7,
            max_tokens=1024
        )

        bot_reply = response.choices[0].message.content
        chat_sessions[session_id].append({"role": "assistant", "content": bot_reply})

        return JSONResponse(content={"response": bot_reply})

    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Error en la IA: Verifica tu API Key de Groq. Detalle: {str(e)}"})


# === MOTOR CENTRAL MLOPS (FLUJO IRROMPIBLE) ===
def run_training_queue(session_id: str, models: list[str], dataset_path: str, epochs: int, batch_size: int, learning_rate: float):
    # Usamos rutas absolutas para garantizar que siempre encuentre los scripts
    base_path = os.getcwd()
    script_train_cnn = os.path.join(base_path, "pneumoniacnn-main", "code", "1_train_kfold.py")
    script_train_trans = os.path.join(base_path, "pneumoniacnn-main", "code", "2_train_transformer_kfold.py")
    script_img = os.path.join(base_path, "pneumoniacnn-main", "code", "6_xai_qualitative.py")
    script_math = os.path.join(base_path, "pneumoniacnn-main", "code", "7_xai_quantitative.py")

    with open(LOG_FILE, "w", encoding="utf-8", errors="replace") as f:
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] SESIÓN DE ENTRENAMIENTO INICIADA: {session_id}\n")
        f.write(f"Modelos a entrenar: {', '.join(models)}\n")
        f.write("-" * 60 + "\n")

    for model_name in models:
        env_vars = os.environ.copy()
        env_vars.update({
            "TFG_SESSION_ID": session_id,
            "TFG_MODEL_NAME": model_name,
            "TFG_DATASET_DIR": dataset_path,
            "TFG_EPOCHS": str(epochs),
            "TFG_BATCH_SIZE": str(batch_size),
            "TFG_LEARNING_RATE": str(learning_rate)
        })

        is_trans = model_name in TRANSFORMER_MODELS
        script_to_run = script_train_trans if is_trans else script_train_cnn

        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
            tipo_arquitectura = "TRANSFORMER" if is_trans else "CNN"
            log.write(f"\n>>> INICIANDO ENTRENAMIENTO [{tipo_arquitectura}]: {model_name}\n")

            p = subprocess.Popen(["python", script_to_run], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            p.wait()

            # Forzamos la ejecución de la fase XAI independientemente de warnings
            log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [XAI AUTO] Generando mapas visuales para {model_name} (Script 6)...\n")
            p_img = subprocess.Popen(["python", script_img], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            p_img.wait()

            log.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [XAI AUTO] Calculando métricas matemáticas reales para {model_name} (Script 7)...\n")
            p_math = subprocess.Popen(["python", script_math], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            p_math.wait()

            log.write(f"\n✅ [XAI AUTO] Explicabilidad completada para {model_name}.\n")

    # Finalizada la iteración de modelos, ejecutamos estadísticas globales
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
        f.write(f"\n{'='*60}\n[{datetime.datetime.now().strftime('%H:%M:%S')}] ENTRENAMIENTOS COMPLETADOS.\n")
        f.write("Generando Ranking Global y Matriz de Wilcoxon...\n")

    env_vars_comp = os.environ.copy()
    env_vars_comp["TFG_SESSION_ID"] = session_id
    script_comp_path = os.path.join(base_path, "pneumoniacnn-main", "code", "3_evaluate_statistics.py")

    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        process_comp = subprocess.Popen(["python", script_comp_path], stdout=log, stderr=subprocess.STDOUT, env=env_vars_comp, text=True, encoding="utf-8", errors="replace")
        process_comp.wait()
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [SESIÓN COMPLETADA Y COMPARADA]\n")

# === RUTAS DE PLATAFORMA (BROWSE, START, LOGS, MODELS) ===
@router.get("/api/train/browse")
async def browse_folder():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Selecciona la carpeta del Dataset")
        root.destroy()
        return {"path": folder_selected}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "No se pudo abrir el explorador."})

@router.post("/api/train/start")
async def start_training(
    background_tasks: BackgroundTasks,
    model_names: str = Form(...),
    dataset_path: str = Form(...),
    epochs: int = Form(...),
    batch_size: int = Form(...),
    learning_rate: float = Form(...)
):
    models_list = [m.strip() for m in model_names.split(",")]
    if not dataset_path or not os.path.exists(dataset_path): return JSONResponse(status_code=400, content={"status": "error", "message": "La ruta no existe."})
    session_id = f"RUN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_dir = f"training_results/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    with open(os.path.join(session_dir, "dataset_path.txt"), "w", encoding="utf-8") as f: f.write(dataset_path)
    config_data = { "dataset_path": dataset_path, "epochs": epochs, "batch_size": batch_size, "learning_rate": learning_rate, "models": models_list }
    with open(os.path.join(session_dir, "config.json"), "w", encoding="utf-8") as f: json.dump(config_data, f)

    background_tasks.add_task(run_training_queue, session_id, models_list, dataset_path, epochs, batch_size, learning_rate)
    return JSONResponse(content={"status": "success", "message": f"Iniciada sesión {session_id}."})

@router.get("/api/train/logs")
async def get_training_logs():
    if not os.path.exists(LOG_FILE): return JSONResponse(content={"logs": "Esperando..."})
    with open(LOG_FILE, encoding="utf-8", errors="replace") as f: lines = f.readlines()[-60:]
    return JSONResponse(content={"logs": "".join(lines)})

@router.get("/api/train/models")
async def get_trained_sessions():
    base_dir = "training_results"
    sessions = []
    if os.path.exists(base_dir):
        for session_folder in sorted(os.listdir(base_dir), reverse=True):
            session_path = os.path.join(base_dir, session_folder)
            if os.path.isdir(session_path):
                models_in_session = [m for m in os.listdir(session_path) if os.path.exists(os.path.join(session_path, m, "kfold_results.csv"))]
                if models_in_session: sessions.append({"session_id": session_folder, "models": models_in_session})
    return JSONResponse(content={"status": "success", "sessions": sessions})

@router.get("/api/train/results/{session_id}/{model_name}")
async def get_model_results(session_id: str, model_name: str):
    model_dir = f"training_results/{session_id}/{model_name}"
    csv_path = f"{model_dir}/kfold_results.csv"
    if not os.path.exists(csv_path): return JSONResponse(status_code=404, content={"error": "Resultados no encontrados"})
    data = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: data.append(row)
    images = [f"/training_results/{session_id}/{model_name}/{file}" for file in os.listdir(model_dir) if file.endswith(".png")]
    calib_data = {"brier": "-", "ece": "-"}
    calib_path = f"{model_dir}/calibration_metrics.txt"
    if os.path.exists(calib_path):
        with open(calib_path, encoding="utf-8") as f:
            for line in f.readlines():
                if "Brier" in line: calib_data["brier"] = line.split(":")[1].strip()
                if "ECE" in line: calib_data["ece"] = line.split(":")[1].strip()
    xai_metrics = []
    xai_csv_path = f"{model_dir}/xai_metrics_comparison.csv"
    if os.path.exists(xai_csv_path):
        with open(xai_csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader: xai_metrics.append(row)
    return JSONResponse(content={"status": "success", "data": data, "images": images, "calib": calib_data, "xai_metrics": xai_metrics})

@router.post("/api/train/run_eval")
async def run_evaluation_script(session_id: str = Form(...), model_name: str = Form(...), dataset_path: str = Form("")):
    session_dir = f"training_results/{session_id}"
    saved_path_file = os.path.join(session_dir, "dataset_path.txt")

    if not dataset_path and os.path.exists(saved_path_file):
        with open(saved_path_file, encoding="utf-8") as f: dataset_path = f.read().strip()
    if not dataset_path or not os.path.exists(dataset_path):
        return JSONResponse(status_code=400, content={"status": "error", "message": "No se encontró la ruta del dataset original."})

    # === EJECUCIÓN SINCRÓNA (El servidor obliga a la web a esperar) ===
    base_path = os.getcwd()
    env_vars = os.environ.copy()
    env_vars.update({
        "TFG_SESSION_ID": session_id,
        "TFG_MODEL_NAME": model_name,
        "TFG_DATASET_DIR": dataset_path
    })

    script_img = os.path.join(base_path, "pneumoniacnn-main", "code", "6_xai_qualitative.py")
    script_math = os.path.join(base_path, "pneumoniacnn-main", "code", "7_xai_quantitative.py")

    # Usamos "a" (append) para no borrar el registro de entrenamiento original en el log
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [MODO MANUAL] 1/2: Generando Mapas XAI...\n")
        p_img = subprocess.Popen(["python", script_img], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
        p_img.wait()

        log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] [MODO MANUAL] 2/2: Calculando Métricas Cuantitativas...\n")
        p_math = subprocess.Popen(["python", script_math], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
        p_math.wait()

        log.write("\n✅ [PROCESO XAI MANUAL COMPLETADO]\n")

    # Solo devolvemos la respuesta de "success" cuando el wait() de los scripts ha terminado
    return JSONResponse(content={"status": "success", "message": "Generación completada. Recargando..."})

# === RUTAS DE SESIÓN Y COMPARATIVAS ===
@router.delete("/api/train/session/{session_id}")
async def delete_session(session_id: str):
    session_path = os.path.join("training_results", session_id)
    if os.path.exists(session_path):
        shutil.rmtree(session_path)
        return JSONResponse(content={"status": "success", "message": "Sesión eliminada."})
    return JSONResponse(status_code=404, content={"status": "error", "message": "Sesión no encontrada."})

@router.post("/api/train/session/rename")
async def rename_session(old_name: str = Form(...), new_name: str = Form(...)):
    old_path = os.path.join("training_results", old_name)
    safe_new_name = "".join([c for c in new_name if c.isalnum() or c in (' ', '-', '_')]).strip()
    if not safe_new_name: return JSONResponse(status_code=400, content={"status": "error", "message": "El nombre no es válido."})
    new_path = os.path.join("training_results", safe_new_name)
    if os.path.exists(new_path): return JSONResponse(status_code=400, content={"status": "error", "message": "Ya existe."})
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return JSONResponse(content={"status": "success", "new_name": safe_new_name})
    return JSONResponse(status_code=404, content={"status": "error", "message": "Sesión no encontrada."})

@router.post("/api/train/session/compare")
async def compare_session_models(background_tasks: BackgroundTasks, session_id: str = Form(...)):
    def run_comparison():
        base_path = os.getcwd()
        env_vars = os.environ.copy()
        env_vars["TFG_SESSION_ID"] = session_id
        script_path = os.path.join(base_path, "pneumoniacnn-main", "code", "3_evaluate_statistics.py")
        with open(LOG_FILE, "w", encoding="utf-8", errors="replace") as log:
            log.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Recalculando estadísticas de la sesión {session_id}...\n")
            process = subprocess.Popen(["python", script_path], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            process.wait()
            log.write("\n✅ [COMPARACIÓN COMPLETADA]\n")
    background_tasks.add_task(run_comparison)
    return JSONResponse(content={"status": "success", "message": "Recálculo iniciado."})

@router.get("/api/train/session/{session_id}/ranking")
async def get_session_ranking(session_id: str):
    session_dir = f"training_results/{session_id}"
    csv_path = f"{session_dir}/session_ranking.csv"
    heatmap_path = f"/training_results/{session_id}/wilcoxon_heatmap.png"
    if not os.path.exists(csv_path): return JSONResponse(status_code=404, content={"error": "Aún no se ha comparado esta sesión."})
    data = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: data.append(row)
    config_data = {}
    config_path = f"{session_dir}/config.json"
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f: config_data = json.load(f)
    elif os.path.exists(f"{session_dir}/dataset_path.txt"):
        with open(f"{session_dir}/dataset_path.txt", encoding="utf-8") as f: config_data["dataset_path"] = f.read().strip()
    return JSONResponse(content={"status": "success", "ranking": data, "heatmap": heatmap_path, "config": config_data})

# === RUTAS DE VALIDACIÓN EXTERNA ===
@router.post("/api/train/session/external_validation")
async def run_external_validation(background_tasks: BackgroundTasks, session_id: str = Form(...), dataset_path: str = Form(...)):
    if not dataset_path or not os.path.exists(dataset_path): return JSONResponse(status_code=400, content={"status": "error", "message": "La ruta del dataset externo no es válida."})
    def run_validation():
        base_path = os.getcwd()
        env_vars = os.environ.copy()
        env_vars["TFG_SESSION_ID"] = session_id
        env_vars["TFG_EXTERNAL_DATASET_DIR"] = dataset_path
        script_val = os.path.join(base_path, "pneumoniacnn-main", "code", "4_external_validation.py")
        script_delong = os.path.join(base_path, "pneumoniacnn-main", "code", "5_evaluate_delong.py")
        with open(LOG_FILE, "w", encoding="utf-8", errors="replace") as log:
            log.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando Validación Externa para sesión {session_id}...\n")
            process_val = subprocess.Popen(["python", script_val], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            process_val.wait()

            log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Calculando Test Estadístico de DeLong...\n")
            process_delong = subprocess.Popen(["python", script_delong], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace")
            process_delong.wait()
            log.write("\n✅ [VALIDACIÓN EXTERNA COMPLETADA]\n")

    background_tasks.add_task(run_validation)
    return JSONResponse(content={"status": "success", "message": "Validación Externa iniciada."})

@router.get("/api/train/session/{session_id}/external_results")
async def get_external_validation_results(session_id: str):
    session_dir = f"training_results/{session_id}/external_validation"
    csv_path = f"{session_dir}/external_validation_metrics.csv"
    roc_path = f"/training_results/{session_id}/external_validation/roc_external_validation.png"
    delong_path = f"/training_results/{session_id}/external_validation/delong_heatmap.png"
    if not os.path.exists(csv_path): return JSONResponse(status_code=404, content={"error": "Aún no hay resultados de validación externa."})
    data = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: data.append(row)
    return JSONResponse(content={"status": "success", "metrics": data, "roc": roc_path, "delong": delong_path})


# === GENERADOR DE PDF MÉDICO MLOPS ===
class MedicalReport(FPDF):
    def header(self):
        # Fondo del encabezado
        self.set_fill_color(30, 41, 59) # Azul muy oscuro (estilo slate-800)
        self.rect(0, 0, 210, 35, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "X-RAY CONSULTANT AI - MEDICAL REPORT", ln=True, align="L")

        self.set_font("Arial", "", 10)
        self.cell(0, 5, f"Protocolo MLOps: Deep Learning para Detección de Neumonía", ln=True, align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()} | Informe generado automáticamente por X-Ray Consultant Platform", align="C")

    def section_title(self, title):
        self.ln(5)
        self.set_fill_color(241, 245, 249) # Gris muy claro
        self.set_text_color(30, 41, 59)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"  {title}", ln=True, fill=True)
        self.ln(3)

@router.get("/api/train/session/{session_id}/report")
async def generate_pdf_report(session_id: str):
    session_dir = f"training_results/{session_id}"
    if not os.path.exists(session_dir):
        return JSONResponse(status_code=404, content={"message": "Sesión no encontrada"})

    pdf = MedicalReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # --- 1. RESUMEN DE CONFIGURACIÓN ---
    pdf.section_title("1. CONFIGURACIÓN DEL SISTEMA Y PARÁMETROS")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(50, 50, 50)

    config_path = os.path.join(session_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            cfg = json.load(f)
            # Tabla de configuración (2 columnas)
            data = [
                ["ID Sesión", session_id],
                ["Fecha", datetime.datetime.now().strftime('%d/%m/%Y %H:%M')],
                ["Dataset", cfg.get('dataset_path', '-')],
                ["Modelos", ", ".join(cfg.get('models', []))],
                ["Hiperparámetros", f"Epochs: {cfg.get('epochs', '-')} | Batch: {cfg.get('batch_size', '-')} | LR: {cfg.get('learning_rate', '-')}"]
            ]
            for row in data:
                pdf.set_font("Arial", "B", 9)
                pdf.cell(40, 7, f"{row[0]}:", border='B')
                pdf.set_font("Arial", "", 9)
                pdf.cell(0, 7, f" {row[1]}", border='B', ln=True)

    # --- 2. RANKING Y WILCOXON (Compacto) ---
    ranking_csv = os.path.join(session_dir, "session_ranking.csv")
    if os.path.exists(ranking_csv):
        pdf.section_title("2. RENDIMIENTO GLOBAL (K-FOLD CROSS-VALIDATION)")

        # Tabla de métricas
        pdf.set_fill_color(71, 85, 105) # Encabezado tabla (slate-600)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(80, 8, " Arquitectura de Modelo", border=1, fill=True)
        pdf.cell(50, 8, " Media AUC", border=1, fill=True)
        pdf.cell(50, 8, " Desviación Estándar", border=1, fill=True, ln=True)

        pdf.set_text_color(30, 41, 59)
        pdf.set_font("Arial", "", 9)
        with open(ranking_csv, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                fill = (i % 2 == 0) # Filas alternas
                if fill: pdf.set_fill_color(248, 250, 252)
                pdf.cell(80, 8, f" {row['Model']}", border=1, fill=fill)
                pdf.cell(50, 8, f" {row['Mean']}", border=1, fill=fill)
                pdf.cell(50, 8, f" {row['Std']}", border=1, fill=fill, ln=True)

    # Matriz Wilcoxon (Acomodada para no dejar huecos)
    wilcoxon_img = os.path.join(session_dir, "wilcoxon_heatmap.png")
    if os.path.exists(wilcoxon_img):
        pdf.ln(5)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, "Matriz de Significancia Estadística (P-Values):", ln=True)
        pdf.image(wilcoxon_img, x=35, w=140)

    # --- 3. VALIDACIÓN EXTERNA ---
    ext_dir = os.path.join(session_dir, "external_validation")
    if os.path.exists(ext_dir):
        pdf.add_page()
        pdf.section_title("3. VALIDACIÓN EXTERNA (DATASET INDEPENDIENTE)")

        # Métricas externas
        ext_csv = os.path.join(ext_dir, "external_validation_metrics.csv")
        if os.path.exists(ext_csv):
            pdf.set_font("Arial", "B", 9)
            pdf.cell(60, 8, " Modelo", border=1)
            pdf.cell(40, 8, " Accuracy", border=1)
            pdf.cell(40, 8, " F1-Score", border=1)
            pdf.cell(40, 8, " AUC", border=1, ln=True)

            pdf.set_font("Arial", "", 9)
            with open(ext_csv, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pdf.cell(60, 7, row['Model'], border=1)
                    pdf.cell(40, 7, row['Accuracy'], border=1)
                    pdf.cell(40, 7, row['F1-score'], border=1)
                    pdf.cell(40, 7, row['AUC'], border=1, ln=True)

        # ROC y DeLong lado a lado (si caben)
        roc_img = os.path.join(ext_dir, "roc_external_validation.png")
        delong_img = os.path.join(ext_dir, "delong_heatmap.png")
        if os.path.exists(roc_img):
            pdf.ln(5)
            pdf.image(roc_img, x=10, w=90)
            if os.path.exists(delong_img):
                pdf.image(delong_img, x=110, y=pdf.get_y(), w=90)
            pdf.ln(70) # Espacio para las imágenes

    # --- 4. DETALLE TÉCNICO POR MODELO (XAI CUALI/CUANTI) ---
    for model_name in os.listdir(session_dir):
        m_path = os.path.join(session_dir, model_name)
        if os.path.isdir(m_path) and model_name != "external_validation":
            pdf.add_page()
            pdf.section_title(f"DETALLE TÉCNICO: {model_name}")

            # XAI Cuantitativo (Tabla compacta)
            xai_cuanti = os.path.join(m_path, "xai_metrics_comparison.csv")
            if os.path.exists(xai_cuanti):
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 8, "Métricas de Fidelidad XAI (Calculadas sobre 5 muestras):", ln=True)
                pdf.set_font("Arial", "", 8)
                with open(xai_cuanti, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames
                    col_width = 190 / len(headers)
                    for h in headers: pdf.cell(col_width, 7, h, border=1, fill=True)
                    pdf.ln()
                    for row in reader:
                        for h in headers: pdf.cell(col_width, 7, row[h], border=1)
                        pdf.ln()

            # XAI Cualitativo (Mosaico de imágenes)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 8, "Mapas de Calor de Interpretabilidad Visual:", ln=True)

            xai_imgs = sorted([f for f in os.listdir(m_path) if f.startswith("xai_example_") and f.endswith(".png")])

            # Imprimimos en 2 columnas para ahorrar espacio y reducir blanco
            for i in range(0, len(xai_imgs), 2):
                img1 = os.path.join(m_path, xai_imgs[i])
                pdf.image(img1, x=10, w=90)
                if i + 1 < len(xai_imgs):
                    img2 = os.path.join(m_path, xai_imgs[i+1])
                    pdf.image(img2, x=105, y=pdf.get_y(), w=90)
                pdf.ln(35) # Salto de línea ajustado al tamaño de imagen

    # Guardar el archivo final
    pdf_output_path = os.path.join(session_dir, f"Informe_Completo_{session_id}.pdf")
    pdf.output(pdf_output_path)
    return FileResponse(pdf_output_path, filename=f"Reporte_MLOps_{session_id}.pdf")
