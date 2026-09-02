# TASK-012: Contenedor Docker reproducible para la defensa

## Status
`in_progress`

## Task
- ID: TASK-012
- Title: Contenedor Docker reproducible para la defensa
- Backlog source: `agents/task/backlog.md`

## Summary
Preparar un paquete Docker portable para ejecutar vitalXAI en el ordenador de la defensa sin reinstalar Python ni descargar las dependencias. El paquete debe permitir diagnósticos rápidos con uno o dos modelos ya entrenados y lanzar entrenamientos sobre un dataset reducido de demostración.

## Scope
**In:**
- Crear un `Dockerfile` para Python 3.11 con las dependencias de `requirements.txt`.
- Crear una configuración Compose con la aplicación FastAPI y MySQL.
- Ejecutar Uvicorn escuchando en `0.0.0.0` dentro del contenedor.
- Mantener secretos fuera de la imagen y proporcionar una plantilla de entorno para la demo.
- Persistir base de datos, uploads, resultados XAI, informes y resultados MLOps.
- Empaquetar uno o dos modelos CNN existentes para diagnóstico local sin descargas.
- Preparar un dataset reducido local para entrenamientos de demostración.
- Añadir scripts de exportación/importación de la imagen y documentación de la defensa.
- Validar construcción, arranque, conexión app-MySQL, diagnóstico y lanzamiento de entrenamiento cuando el entorno Docker esté disponible.

**Out (explicitly excluded):**
- Cambiar el modelo de negocio o la API funcional de la aplicación.
- Ejecutar entrenamiento completo del dataset de investigación como parte de la demo.
- Hacer que Docker proporcione GPU automáticamente en un ordenador desconocido.
- Exponer MySQL públicamente.
- Eliminar o modificar la estrategia existente de túnel de `TASK-011`.

## Current Behavior
- La aplicación arranca con `python main.py` y el bloque principal usa `127.0.0.1` y `reload=True`.
- La conexión MySQL usa `DB_HOST`, que por defecto es `localhost`.
- Los scripts MLOps ejecutan subprocesos desde el directorio de trabajo y usan rutas relativas.
- La selección de datasets puede usar `TFG_DEMO_DATASET` y `TFG_DEMO_EXTERNAL_DATASET` para evitar Tkinter en un servidor desatendido.
- Los pesos de modelos y los datasets están excluidos del control de versiones.
- No existen archivos Docker para esta aplicación.

## Target Behavior
- `docker compose up -d` inicia MySQL y la aplicación en una red interna de Compose.
- La aplicación se conecta a MySQL mediante el nombre de servicio `db`.
- `http://localhost:8000` permite usar la aplicación y sus diagnósticos rápidos.
- Los modelos CNN de demo están disponibles localmente y se cargan de forma perezosa, sin descarga durante la inferencia.
- El entrenamiento puede usar `/app/demo-data` y escribir sus resultados en almacenamiento persistente.
- La imagen puede exportarse con `docker save` y cargarse en otro ordenador con `docker load`.
- La configuración de demo no contiene secretos en el Dockerfile ni en la imagen.

## Acceptance Criteria
- [x] La imagen se construye con la versión de Python y dependencias del proyecto.
- [x] Compose valida correctamente y arranca `db` y `app` con healthcheck de MySQL.
- [x] La aplicación responde desde el host por el puerto 8000.
- [x] La base de datos y los directorios generados usan almacenamiento persistente.
- [x] El paquete excluye `.env`, logs, cachés, datasets de investigación y secretos del contexto salvo los artefactos explícitos de demo.
- [x] Al menos un modelo local permite realizar un diagnóstico rápido dentro del contenedor.
- [x] El dataset reducido contiene las dos clases esperadas y puede ser usado por el entrenamiento configurado.
- [x] La imagen se puede exportar y cargar de nuevo.
- [x] La documentación incluye preparación, arranque, parada, exportación, importación y contingencia local.
- [x] Las pruebas existentes no se rompen y las validaciones Docker realizadas quedan registradas.

## Edge Cases
- Primer arranque con un volumen MySQL vacío.
- Reinicio de `app` conservando resultados y uploads.
- Arranque sin `GROQ_API_KEY`, dejando claro que solo se desactiva el chatbot.
- Ordenador de defensa sin Internet: inferencia CNN local debe seguir disponible; túnel y chatbot no.
- Dataset o modelo ausente en el paquete.
- Ordenador ARM frente a la imagen principal `linux/amd64`.
- Entrenamiento demasiado lento en CPU.

## Assumptions / Risks
- El ordenador de la defensa tendrá Docker Desktop o Docker Engine instalado y, previsiblemente, arquitectura Intel/AMD.
- Se construirá como `linux/amd64` por portabilidad; una máquina ARM requiere una variante adicional o emulación.
- TensorFlow y los modelos hacen que la imagen sea grande y el entrenamiento CPU sea lento.
- Los modelos existentes localmente no están versionados; el paquete de demo debe conservarlos fuera de Git o incluirlos explícitamente en el artefacto de entrega.
- Los scripts de entrenamiento pueden requerir acceso a pesos base de Keras o modelos Hugging Face si se entrena desde cero; la demo debe usar CNN y artefactos/cachés preparados, o documentar la necesidad de Internet.
- El túnel seguirá ejecutándose en el host y es opcional para la defensa.

## Database Impact
No se modifica el esquema ni el comportamiento de persistencia; solo se añade una forma reproducible de ejecutar el MySQL compatible.

- Change summary: Añadir servicio MySQL y persistencia Docker para la demo.
- DB schema file from Source of Truth Map: `sql/tfg_pneumonia.sql` como referencia existente; la inicialización normal se realiza mediante `database.init_db()`.
- DB change log file from Source of Truth Map: `agents/db/changes.sql` no se modifica porque no hay cambio de esquema.
- Affected structures/data: Volumen de datos de MySQL y tablas existentes.
- Forward migration approach: Crear un volumen nuevo y dejar que `init_db()` cree las tablas; importar un dump opcional de demo.
- Rollback approach: Detener Compose y eliminar solo el volumen de demo si se desea empezar de cero.
- Persisted data compatibility: Se conservan las tablas actuales y no se realizan migraciones destructivas.
- Operational risks: `docker compose down -v` elimina los datos del volumen.
- Validation plan: Healthcheck de MySQL, arranque de app, creación de tablas y flujo de autenticación/inferencia.
- Backup/recovery notes: Exportar un dump SQL antes de transportar datos precargados.
- Required doc updates: `README-DEFENSA.md` y documentación local del paquete; no se actualiza el esquema.

## Open Questions
- Ninguna bloqueante. Se usará un dataset reducido y modelos CNN locales, con el entrenamiento completo fuera del flujo principal de la defensa.

## Source of Truth to Read
- `AGENTS.md`
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/decisions.md`
- `agents/skills/test-driven-development/SKILL.md`
- `README.md`
- `.env.example`
- `database.py`
- `main.py`
- `services/ml_engine.py`
- `services/mlops_engine.py`

## Decision Records
- ADRs read from `agents/docs/decisions.md`: ADR-002, ADR-004, ADR-010, ADR-011.
- New decisions to record after user approval: none. This task adds a portable local-container mode, preserves lazy model loading and the existing tunnel strategy, and uses a dedicated non-root MySQL user for the demo.
