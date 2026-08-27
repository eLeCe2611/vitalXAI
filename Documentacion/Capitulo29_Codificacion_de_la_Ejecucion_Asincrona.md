# Capítulo 29: Codificación de la ejecución asíncrona

La ejecución asíncrona constituye el soporte del procesamiento en segundo plano de vitalXAI: los diagnósticos, los entrenamientos y las validaciones externas se procesan fuera del ciclo de petición HTTP, de modo que la interfaz permanece operativa durante las tareas de larga duración. Este capítulo describe la codificación de este mecanismo, que se materializa en la cola persistente de trabajos y en el worker de la cola. La implementación se organiza en cinco apartados: la cola de trabajos y su máquina de estados, el bucle del worker, la reclamación y el despacho de los trabajos, la tolerancia a fallos y la recuperación, y la consulta y la cancelación desde la API.

La implementación de la ejecución asíncrona se apoya en la persistencia relacional descrita en el capítulo 28: la cola se materializa en la tabla `job_queue` de MySQL, que conserva los trabajos con su estado, su payload serializable, su resultado y su error, y el worker comparte esa persistencia con los routers, pero no comparte el ciclo de petición. Esta frontera, ya declarada en el diseño del subsistema SD-006, se implementa en el módulo `services/queue_worker.py`, que contiene el bucle del worker y las operaciones de transición de estado, y en el router `routers/queue.py`, que expone la consulta del estado y la cancelación de los trabajos.

## 29.1 La cola de trabajos y su máquina de estados

La cola de trabajos se implementa en la tabla `job_queue`, cuyas filas representan los trabajos asíncronos del sistema. Cada trabajo conserva el usuario propietario, el tipo (`diagnosis`, `training` o `external_validation`), el estado, el payload serializable, el resultado y el mensaje de error, de modo que la tabla materializa la clase `QueueJob` definida en el diseño de clases del capítulo 21 y su máquina de estados, representada en la figura 89. Las transiciones de estado se implementan en el worker mediante operaciones que actualizan la fila del trabajo: la reclamación, la finalización y el fallo. El fragmento siguiente muestra la implementación de estas transiciones.

```python
def _claim_job(job_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'running', started_at = %s WHERE id = %s AND status = 'queued'",
        (datetime.now(), job_id),
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def _finish_job(job_id: int, result: dict | None = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    result_json = json.dumps(result) if result else None
    cursor.execute(
        "UPDATE job_queue SET status = 'completed', finished_at = %s, result = %s WHERE id = %s",
        (datetime.now(), result_json, job_id),
    )
    conn.commit()
    conn.close()

def _fail_job(job_id: int, error: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'failed', finished_at = %s, error_message = %s WHERE id = %s",
        (datetime.now(), error[:500], job_id),
    )
    conn.commit()
    conn.close()
```

*Código 29.1 - Transiciones de estado del trabajo (`services/queue_worker.py`)*

La implementación de las transiciones refleja la máquina de estados de la cola. La reclamación utiliza una actualización condicionada a que el trabajo continúe en `queued`, de modo que solo afecta a una fila si el trabajo seguía pendiente; el resultado de la actualización determina si el worker ha adquirido el trabajo, lo que impide que dos iteraciones procesen el mismo registro. La finalización marca el trabajo como `completed` con el resultado en formato JSON, y el fallo lo marca como `failed` con el mensaje de error limitado a quinientos caracteres, de modo que el estado persistido nunca conserva un error desbordado. La cancelación desde la API se implementa con la misma técnica condicionada, limitada a los trabajos en `queued`, tal y como se describe en el apartado 29.5.

## 29.2 El bucle del worker

El worker se implementa como un bucle asíncrono que selecciona el siguiente trabajo pendiente, lo reclama, procesa el flujo correspondiente y actualiza su estado, apoyado en el modelo de concurrencia asíncrona de Python (Python Software Foundation, 2024). El bucle se crea en el arranque de la aplicación mediante `start_worker()`, que restablece los trabajos en ejecución y lanza la tarea asíncrona del procesamiento. El fragmento siguiente muestra la implementación del bucle del worker.

```python
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
```

*Código 29.2 - Bucle del worker y su arranque (`services/queue_worker.py`)*

La implementación del bucle refleja las decisiones de diseño del procesamiento asíncrono. El worker selecciona el primer trabajo pendiente mediante la consulta de prioridad, que ordena los diagnósticos antes que los entrenamientos; si no hay trabajos, espera un segundo y vuelve a consultar. Cuando hay un trabajo, lo reclama con la actualización condicionada; si la reclamación no afecta a una fila, otro consumidor ya lo tomó y el worker continúa con el siguiente. La ejecución del flujo se delega en el executor de eventos mediante `run_in_executor`, de modo que el procesamiento intensivo no bloquea el bucle de eventos de la aplicación; al terminar, el trabajo se marca como completado con el resultado, y ante cualquier excepción se marca como fallido con el mensaje de error. El arranque del worker se integra en el ciclo de vida de la aplicación descrito en el capítulo 28, y conserva la tarea en el estado de la aplicación.

## 29.3 Reclamación, despacho y procesamiento de los trabajos

El procesamiento de cada trabajo se resuelve mediante el despacho por tipo, que selecciona el flujo correspondiente según el tipo del trabajo. La reclamación condicionada, descrita en el apartado 29.1, garantiza que el despacho solo se ejecuta sobre trabajos que el worker ha adquirido. El fragmento siguiente muestra la implementación del despacho y del procesamiento de un diagnóstico.

```python
def _execute_job(job):
    if job["job_type"] == "diagnosis":
        return _process_diagnosis(job)
    elif job["job_type"] == "training":
        return _process_training(job)
    elif job["job_type"] == "external_validation":
        return _process_external_validation(job)
    else:
        raise ValueError(f"Unknown job type: {job['job_type']}")

def _process_diagnosis(job):
    payload = _get_payload(job)
    label, confidence = process_and_predict(payload["model_name"], payload["image_path"], lang=payload.get("lang", "es"))

    xai_path = os.path.join("static", "results", "xai_" + os.path.basename(payload["image_path"]))
    generate_xai_heatmap(payload["model_name"], payload["image_path"], xai_path, lang=payload.get("lang", "es"))

    pdf_path = generate_medical_report(payload["image_path"], xai_path, label, confidence, payload["model_name"], lang=payload.get("lang", "es"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO consultations (user_id, model_name, original_image_path, xai_image_path, prediction_label, confidence_score, patient_name, pdf_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (job["user_id"], payload["model_name"], payload["image_path"], xai_path, label, confidence, default_patient_name, pdf_path),
    )
    conn.commit()
    conn.close()
    return {"label": label, "confidence": confidence, "original_image": f"/{payload['image_path']}",
            "xai_image": f"/{xai_path}", "pdf_report": f"/{pdf_path}", "model_used": payload["model_name"]}
```

*Código 29.3 - Despacho por tipo y procesamiento de un diagnóstico (`services/queue_worker.py`)*

La implementación del procesamiento de un diagnóstico refleja el flujo asíncrono definido en el diseño del subsistema SD-002. El worker deserializa el payload del trabajo, invoca el motor de predicción, genera el mapa de explicabilidad y construye el informe PDF, y persiste la consulta en la tabla `consultations` con las rutas de los artefactos y el resultado. El procesamiento se ejecuta en el executor, de modo que la predicción y la generación de los artefactos no bloquean la interfaz. Los procesamientos de los entrenamientos y de las validaciones externas siguen el mismo patrón y delegan en el motor del laboratorio MLOps, que se describe en el capítulo 31. El resultado devuelto se conserva en el campo `result` del trabajo completado.

## 29.4 Tolerancia a fallos y recuperación

La ejecución asíncrona incorpora mecanismos de tolerancia a fallos y de recuperación que garantizan la coherencia del sistema ante errores y reinicios. Ante un fallo del procesamiento, el worker captura la excepción y marca el trabajo como fallido con el mensaje de error, de modo que un fallo del motor, de la imagen o del informe no se transforma en una consulta completada con datos ambiguos. Ante el reinicio de la aplicación, los trabajos que quedaron en estado `running` se restablecen a `queued`, de modo que el procesamiento interrumpido vuelve a la cola y puede ser retomado. El fragmento siguiente muestra la implementación del restablecimiento de los trabajos en ejecución.

```python
def _reset_running_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE job_queue SET status = 'queued', started_at = NULL WHERE status = 'running'")
    conn.commit()
    conn.close()
```

*Código 29.4 - Restablecimiento de los trabajos en ejecución (`services/queue_worker.py`)*

La implementación del restablecimiento refleja la decisión de recuperación del diseño. Al arrancar la aplicación, `start_worker()` ejecuta `_reset_running_jobs()`, que devuelve a la cola los trabajos que quedaron en `running` cuando el proceso anterior se detuvo, con su fecha de inicio restablecida; la reclamación condicionada evita que esos trabajos se procesen dos veces, porque solo un consumidor puede adquirir cada trabajo. Esta técnica, junto con la captura de excepciones del bucle, garantiza que el estado persistido de la cola permanece coherente con la ejecución real, incluso ante fallos del proceso o de los componentes.

## 29.5 La cola desde la API

La consulta del estado y la cancelación de los trabajos se exponen en el router `routers/queue.py`, que materializa los casos de uso CU-034 y CU-035 del análisis. La consulta del estado devuelve los trabajos del usuario con su tipo, su estado, su posición y el nombre del modelo o de la sesión, interpretando el payload según el tipo; la cancelación aplica una actualización condicionada que solo afecta a los trabajos en `queued` pertenecientes al usuario. El fragmento siguiente muestra la implementación de la cancelación.

```python
@router.delete("/api/queue/cancel/{job_id}")
async def cancel_job(request: Request, job_id: int):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE job_queue SET status = 'cancelled', finished_at = NOW() WHERE id = %s AND user_id = %s AND status = 'queued'",
        (job_id, user_id),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    if affected == 0:
        return JSONResponse(status_code=404, content={"error": "Trabajo no encontrado o ya no está en cola"})
    return JSONResponse(content={"status": "success", "message": "Trabajo cancelado"})
```

*Código 29.5 - Cancelación de un trabajo desde la API (`routers/queue.py`)*

La implementación de la cancelación refleja la restricción del diseño: solo un trabajo en estado `queued` y perteneciente al usuario puede cancelarse. La actualización condicionada a esos tres criterios afecta a una fila únicamente cuando el trabajo sigue pendiente; si el worker ya lo reclamó o el trabajo finalizó, la actualización no afecta a ninguna fila y el router responde HTTP 404 informando de que el trabajo no está en cola. De este modo, un trabajo en ejecución no se interrumpe de forma abrupta, en coherencia con la máquina de estados de la cola. La consulta del estado, por su parte, interpreta el payload de cada tipo de trabajo para mostrar el nombre del modelo o de la sesión sin exponer el contenido interno completo del payload.

La ejecución asíncrona de vitalXAI queda así codificada de forma completa: la cola persistente materializa la máquina de estados de los trabajos, el worker reclama y procesa los trabajos fuera del ciclo de petición, el despacho por tipo orquesta los flujos de los subsistemas, los mecanismos de tolerancia a fallos y de recuperación mantienen la coherencia del estado, y la API expone la consulta y la cancelación a los usuarios. La implementación de los motores que el worker invoca —la predicción y la explicabilidad del diagnóstico y el laboratorio MLOps— se describe en los capítulos siguientes.
