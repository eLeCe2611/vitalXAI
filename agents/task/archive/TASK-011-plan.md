# TASK-011 — Preparación de despliegue para demostración en vivo

## Status
`closed`

## Task
- ID: TASK-011
- Title: Preparación de despliegue para demostración en vivo
- Backlog source: `agents/task/backlog.md`

## Summary
Preparar la plataforma para una demo en vivo el día de la defensa. La app corre en el PC de casa (MySQL, datasets, pesos de modelos) y se expone a Internet mediante un túnel HTTPS seguro; desde el portátil de la universidad solo se abre la URL en el navegador, sin instalar nada. Se añade un script de arranque de un solo comando (servidor + túnel), un fallback para elegir el dataset sin diálogo Tkinter (rutas preconfiguradas por entorno) y una guía para el día de la defensa.

## Scope
**In:**
- Script de arranque `scripts/demo_start.ps1` + `scripts/demo_start.bat`:
  - Fija el CWD a la raíz del repo (las rutas relativas del proyecto dependen de él).
  - Comprueba `.env` y MySQL (puerto 3306) con avisos claros.
  - Arranca uvicorn sin `reload` en `127.0.0.1:8000`.
  - Arranca el túnel según `TUNNEL_PROVIDER` (`cloudflared` por defecto, `ngrok` opcional) y escribe la URL pública en `demo_url.txt` y en consola. `localhost.run` se documenta en la guía como plan C (cero instalación, vía `ssh` de Windows), sin lógica en el script.
- Fallback de selección de dataset en `services/mlops_engine.py::browse_folder()`:
  - Si `TFG_DEMO_DATASET` está definida, devuelve esa ruta sin abrir el diálogo Tkinter.
  - Para validación externa, si `TFG_DEMO_EXTERNAL_DATASET` está definida, devuelve esa ruta (endpoint con parámetro de disambiguación `for_external`).
  - Sin variables definidas, mantiene el diálogo Tkinter actual (comportamiento intacto).
- Añadir a `.env.example` (opcionales): `TFG_DEMO_DATASET`, `TFG_DEMO_EXTERNAL_DATASET`, `TUNNEL_PROVIDER`.
- Guía del día de la defensa: `Documentacion/Guia_Despliegue_Demo.md`.
- Tests unitarios para el fallback de `browse_folder` (con/sin variable, ambos modos).
- Actualizar `agents/docs/api.md` si el endpoint `/api/train/browse` cambia su contrato.

**Out (explicitly excluded):**
- Cambios en el flujo de diagnóstico rápido (`inference.py`, `ml_engine.py`): subir una imagen desde el portátil ya funciona vía túnel, no se toca.
- Cambios en la carga de modelos ni precarga al arrancar (se mantiene la carga perezosa actual: el primer diagnóstico carga el modelo en memoria; los siguientes son instantáneos).
- Migración a SQLite o despliegue en PaaS (Render/Railway/Fly).
- Cambios en pesos de modelos, datasets o scripts de `pneumoniacnn-main/`.
- Cambios de autenticación, seguridad o API pública (salvo el contrato de `/api/train/browse`).
- Configuración de CI/CD.

## Current Behavior
- La app se ejecuta con `python main.py` (uvicorn `reload=True`) en `127.0.0.1:8000`, solo accesible localmente.
- `browse_folder()` (`mlops_engine.py:119`) siempre abre un diálogo Tkinter en la máquina servidora. En un escenario remoto (PC de casa desatendido) la petición se cuelga esperando la selección.
- No existe script de arranque, soporte de túnel ni guía de despliegue.
- `static/uploads`, `static/results`, `static/reports` y `training_results` se sirven como StaticFiles con rutas relativas al CWD.

## Target Behavior
- Un solo comando arranca servidor + túnel desde la raíz del repo, comprueba requisitos, imprime la URL pública y la guarda en `demo_url.txt`.
- Desde el portátil, "Explorar Carpeta" rellena el chat con la ruta preconfigurada del dataset del PC de casa (y lo mismo para validación externa), permitiendo lanzar entrenamiento sin nadie en casa.
- La guía documenta el proceso completo para el día de la defensa.
- El comportamiento sin variables de demo es idéntico al actual.

## Acceptance Criteria
- `demo_start.bat` (y `.ps1`) arrancan servidor + túnel desde cualquier directorio invocando y dejan la URL pública en `demo_url.txt` y en consola.
- Con `TFG_DEMO_DATASET` definida, `GET /api/train/browse` devuelve esa ruta sin abrir Tkinter; con `for_external=true` devuelve `TFG_DEMO_EXTERNAL_DATASET`.
- Sin las variables de demo, `GET /api/train/browse` conserva el comportamiento actual (diálogo Tkinter).
- `.env.example` documenta las tres variables nuevas como opcionales.
- `Documentacion/Guia_Despliegue_Demo.md` cubre: instalación, configuración, arranque, compartir URL, flujo de demo, troubleshooting y plan B.
- Los tests unitarios nuevos pasan; `python -m pytest tests/` y `ruff check .` quedan limpios.

## Edge Cases
- Variables de demo no definidas → diálogo Tkinter como hoy.
- `TFG_DEMO_DATASET`/`TFG_DEMO_EXTERNAL_DATASET` apuntando a una ruta inexistente → `browse_folder` devuelve la ruta tal cual; el error real lo valida `/api/train/start` (`os.path.exists`). Se documenta en la guía (verificar rutas antes de la demo).
- Ambas variables definidas y llamada sin `for_external` → se devuelve `TFG_DEMO_DATASET` (default entrenamiento).
- MySQL no disponible → el script avisa; la app arranca igual (comportamiento actual del lifespan). La guía recomienda arrancar XAMPP antes.
- Túnel caído durante la demo → plan B documentado: URL local `127.0.0.1:8000`.
- PC de casa en suspensión → la guía recomienda energía "Nunca".
- Rutas con espacios/acentos → el script usa comillas y `os.getenv` sin manipulación extra.

## Assumptions / Risks
- El PC de casa queda encendido y con conexión a Internet durante toda la defensa.
- `GROQ_API_KEY` operativa: el lanzamiento de entrenamiento pasa por el asistente LLM (`/api/chat`). Si Groq falla, no se puede entrenar en vivo. Mitigación: sesiones precomputadas y frase exacta que inserta "Explorar Carpeta".
- Cloudflare Tunnel sin cuenta genera URL aleatoria en cada arranque; ngrok (con cuenta free) da subdominio fijo.
- Los pesos de modelos y datasets ya existen en el PC de casa en las rutas confirmadas.
- El PC de casa mantiene las rutas de dataset invariables hasta el día de la defensa.

## Database Impact
`Not applicable` — la tarea no modifica esquema, datos ni el change log de la base de datos.

## Open Questions
Ninguna pendiente. Decisiones confirmadas:
- Túnel: `cloudflared` por defecto + `ngrok` opcional en el script; `localhost.run` solo en la guía (plan C).
- Precarga de modelos: no (se mantiene la carga perezosa actual).
- Guía: `Documentacion/Guia_Despliegue_Demo.md`.
- Fallback de dataset: `GET /api/train/browse?for_external=true` → `TFG_DEMO_EXTERNAL_DATASET`; sin parámetro → `TFG_DEMO_DATASET`.

## Source of Truth to Read
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/api.md` (contrato de `/api/train/browse`)
- `agents/docs/decisions.md`
- `.env.example`
- `services/mlops_engine.py`
- `routers/trainer.py`
- `static/js/training.js`

## Decision Records
- ADRs read from `agents/docs/decisions.md`: ADR-001 (mock DB en tests), ADR-002 (mock TensorFlow/Keras), ADR-010 (CI/CD en Windows runner). Ninguna entra en conflicto con esta tarea.
- New decisions to record after user approval:
  - ADR-011 propuesto: estrategia de despliegue para demo en vivo (túnel HTTPS Cloudflare/ngrok + script de arranque de un comando + fallback de dataset por variables de entorno).
