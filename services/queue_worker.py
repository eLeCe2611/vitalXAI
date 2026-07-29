import asyncio
import json
import os
from datetime import datetime

from database import get_db_connection


def _reset_running_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE job_queue SET status = 'queued', started_at = NULL WHERE status = 'running'")
    conn.commit()
    conn.close()


def _next_job():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, user_id, job_type, payload
        FROM job_queue
        WHERE status = 'queued'
        ORDER BY
            CASE job_type WHEN 'diagnosis' THEN 0 ELSE 1 END,
            id ASC
        LIMIT 1
    """)
    job = cursor.fetchone()
    conn.close()
    return job


def _claim_job(job_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'running', started_at = %s WHERE id = %s AND status = 'queued'",
        (datetime.now(), job_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def _fail_job(job_id: int, error: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'failed', finished_at = %s, error_message = %s WHERE id = %s",
        (datetime.now(), error[:500], job_id)
    )
    conn.commit()
    conn.close()


def _finish_job(job_id: int, result: dict | None = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    result_json = json.dumps(result) if result else None
    cursor.execute(
        "UPDATE job_queue SET status = 'completed', finished_at = %s, result = %s WHERE id = %s",
        (datetime.now(), result_json, job_id)
    )
    conn.commit()
    conn.close()


def _get_payload(job):
    p = job["payload"]
    if isinstance(p, str):
        return json.loads(p)
    return p


def _process_diagnosis(job):
    from services.ml_engine import process_and_predict
    from services.pdf_generator import generate_medical_report
    from services.xai_generator import generate_xai_heatmap

    payload = _get_payload(job)
    model_name = payload["model_name"]
    image_path = payload["image_path"]

    label, confidence = process_and_predict(model_name, image_path)

    xai_dir = os.path.join("static", "results")
    os.makedirs(xai_dir, exist_ok=True)
    xai_filename = "xai_" + os.path.basename(image_path)
    xai_path = os.path.join(xai_dir, xai_filename)
    generate_xai_heatmap(model_name, image_path, xai_path)

    pdf_path = generate_medical_report(image_path, xai_path, label, confidence, model_name)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM consultations WHERE user_id = %s AND model_name = %s",
                   (job["user_id"], model_name))
    count_previous = cursor.fetchone()[0]
    current_number = count_previous + 1
    default_patient_name = f"Paciente sin nombre {model_name} #{current_number}"

    cursor.execute("""
        INSERT INTO consultations
        (user_id, model_name, original_image_path, xai_image_path, prediction_label, confidence_score, patient_name, pdf_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (job["user_id"], model_name, image_path, xai_path, label, confidence, default_patient_name, pdf_path))
    conn.commit()
    conn.close()

    return {"label": label, "confidence": confidence, "original_image": f"/{image_path}",
            "xai_image": f"/{xai_path}", "pdf_report": f"/{pdf_path}", "model_used": model_name}


def _process_training(job):
    from services.mlops_engine import run_training_queue

    payload = _get_payload(job)
    session_id = payload["session_id"]
    models = payload["models"]
    dataset_path = payload["dataset_path"]
    epochs = payload["epochs"]
    batch_size = payload["batch_size"]
    learning_rate = payload["learning_rate"]

    run_training_queue(session_id, models, dataset_path, epochs, batch_size, learning_rate)
    return {"session_id": session_id, "status": "completed"}


def _execute_job(job):
    try:
        if job["job_type"] == "diagnosis":
            return _process_diagnosis(job)
        elif job["job_type"] == "training":
            return _process_training(job)
        else:
            raise ValueError(f"Unknown job type: {job['job_type']}")
    except Exception as e:
        raise e


async def worker_loop():
    loop = asyncio.get_running_loop()
    while True:
        try:
            job = _next_job()
            if job is None:
                await asyncio.sleep(1)
                continue

            claimed = _claim_job(job["id"])
            if not claimed:
                continue

            try:
                result = await loop.run_in_executor(None, _execute_job, job)
                _finish_job(job["id"], result)
            except Exception as e:
                _fail_job(job["id"], str(e))
        except Exception:
            await asyncio.sleep(1)


def start_worker(app):
    _reset_running_jobs()
    task = asyncio.create_task(worker_loop())
    app.state.queue_worker = task
