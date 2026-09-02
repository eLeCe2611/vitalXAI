# vitalXAI

Plataforma web para la detección asistida de neumonía en radiografías de tórax. Incluye inferencia con modelos CNN y Transformer, técnicas de explicabilidad (XAI), generación de informes PDF, historial de consultas y un laboratorio MLOps para entrenar y comparar modelos.

## Mapa del repositorio

### Aplicación web

| Ruta | Contenido |
|---|---|
| `main.py` | Punto de entrada de FastAPI. Inicializa la base de datos, el worker de cola, middleware de seguridad, archivos estáticos y routers. |
| `database.py` | Conexión e inicialización de MySQL. |
| `routers/auth.py` | Registro, inicio de sesión y vistas relacionadas con la cuenta. |
| `routers/admin.py` | Funciones y vistas de administración. |
| `routers/inference.py` | Subida de radiografías, predicción, explicabilidad e informes de diagnóstico. |
| `routers/history.py` | Consulta del historial de predicciones. |
| `routers/queue.py` | Consulta y control del estado de trabajos en cola. |
| `routers/trainer.py` | Interfaz del chatbot y lanzamiento de entrenamientos MLOps. |
| `services/auth_service.py` | Lógica de autenticación, contraseñas y tokens. |
| `services/ml_engine.py` | Carga y ejecución de modelos CNN y Transformer. |
| `services/xai_generator.py` | Generación de Saliency Maps, SmoothGrad, Grad-CAM y mapas de atención. |
| `services/pdf_generator.py` | Informes PDF de predicciones individuales. |
| `services/pdf_generator_mlops.py` | Informes PDF de resultados de entrenamiento y evaluación. |
| `services/trainer_engine.py` | Ejecución del motor de entrenamiento desde la aplicación. |
| `services/mlops_engine.py` | Orquestación de los pipelines y sus resultados. |
| `services/chatbot_service.py` | Comunicación con Groq para configurar entrenamientos. |
| `services/queue_worker.py` | Worker que procesa trabajos de entrenamiento en segundo plano. |
| `services/csrf_middleware.py` | Protección CSRF y cabeceras de seguridad. |
| `services/rate_limiter.py` | Limitación de peticiones. |
| `services/lang.py` | Textos y soporte de idioma de la aplicación. |
| `templates/` | Plantillas HTML de la interfaz, renderizadas con Jinja2. |
| `static/` | CSS, JavaScript e imágenes de la interfaz. |

### Datos y resultados

| Ruta | Contenido |
|---|---|
| `static/uploads/` | Radiografías subidas por los usuarios. |
| `static/results/` | Mapas XAI generados durante la inferencia. |
| `static/reports/` | Informes PDF generados. |
| `training_results/` | Resultados de sesiones MLOps y sus informes. |
| `demo-data/` | Dataset reducido utilizado por la demo Docker. |
| `demo-models/` | Pesos de modelos preparados para la demo Docker. |
| `demo-cache/` | Caché de modelos y recursos descargados para la demo. |
| `sql/` | Scripts SQL auxiliares. |
| `agents/db/` | Esquema, cambios y documentación del modelo de datos del proyecto. |
| `Documentacion/` | Documentación de trabajo; se excluye completa de Git y de las imágenes Docker. |

Los directorios de datos, resultados, caché, logs y credenciales están ignorados mediante `.gitignore`. Los directorios montados como volúmenes en Docker conservan sus datos aunque se recree el contenedor.

### Entrenamiento e investigación

| Ruta | Contenido |
|---|---|
| `pneumoniacnn-main/code/` | Scripts de entrenamiento, evaluación estadística, XAI y validación externa. |
| `pneumoniacnn-main/Images/` | Dataset de entrenamiento. No se versiona. |
| `pneumoniacnn-main/ExternalDataset/` | Dataset de validación externa. No se versiona. |
| `pneumoniacnn-main/results/` | Pesos y resultados del benchmarking. |
| `pneumoniacnn-main/README.rst` | Documentación específica del módulo de benchmarking. |
| `pneumoniacnn-main/LICENSE` | Licencia BSD 3-Clause del código de benchmarking. |

### Configuración, ejecución y calidad

| Ruta | Contenido |
|---|---|
| `requirements.txt` | Dependencias Python fijadas, incluyendo FastAPI, TensorFlow, Transformers, MySQL, Groq y herramientas de test. |
| `pyproject.toml` | Configuración de pytest, coverage, Ruff y mypy. |
| `.env.example` | Plantilla de variables de entorno para ejecución local. |
| `.env.demo.example` | Plantilla de variables de entorno para la demo Docker. |
| `Dockerfile` | Imagen de producción de la aplicación FastAPI. |
| `compose.yaml` | Servicios Docker Compose de la aplicación y MySQL, con volúmenes persistentes. |
| `.gitignore` | Archivos y datos que no deben entrar en Git. |
| `.dockerignore` | Archivos que no deben copiarse al contexto de construcción Docker. |
| `tests/` | Pruebas unitarias e integración. |
| `scripts/` | Arranque de demo, construcción de paquetes Docker y migraciones auxiliares. |
| `run_tests.sh` / `run_tests.bat` | Atajos para ejecutar la suite de pruebas en Linux/macOS y Windows. |
| `.github/` | Automatizaciones y workflows de GitHub. |
| `.opencode/` | Configuración local de OpenCode para este repositorio. |
| `agents/docs/` | Reglas, decisiones, diseño, pruebas y definición de terminado del proyecto. |
| `agents/task/` | Backlog, planes y checklists de tareas. |
| `agents/skills/` | Skills de apoyo al flujo de trabajo del agente. |
| `LICENSE` | Licencia del proyecto principal. |

## Modelos y XAI

Se soportan CNN como ResNet, EfficientNet, DenseNet, MobileNet, VGG, Inception, Xception y ConvNeXt, además de DeiT, Swin y ViT. Las técnicas XAI disponibles son:

- **Saliency Maps**: sensibilidad de la predicción respecto a los píxeles.
- **SmoothGrad**: promedio de mapas de sensibilidad con ruido.
- **Grad-CAM**: activaciones relevantes de una CNN para una clase.
- **Attention Maps**: atención de los modelos Transformer.

## Requisitos

- Python 3.11 o superior.
- MySQL 8 o compatible. Puede utilizarse XAMPP en local.
- Clave de API de [Groq](https://console.groq.com) para el chatbot de entrenamiento.
- Docker y Docker Compose únicamente para la ejecución contenerizada.

## Ejecución local

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

1. Inicia MySQL y crea la base de datos `tfg_pneumonia`.
2. Copia `.env.example` a `.env` y configura la conexión, `JWT_SECRET_KEY` y `GROQ_API_KEY`.
3. Arranca la aplicación:

```bash
python main.py
```

La aplicación queda disponible en `http://127.0.0.1:8000`.

## Demo Docker

La demo utiliza la aplicación y MySQL en contenedores, junto con datos y pesos reducidos. Configura `.env.demo` a partir de `.env.demo.example` y ejecuta:

```powershell
./scripts/docker_demo_build.ps1
./scripts/docker_demo_up.ps1
./scripts/docker_demo_validate.ps1
```

Para detenerla:

```powershell
./scripts/docker_demo_down.ps1
```

Los scripts `docker_demo_load.ps1` y `docker_demo_package.ps1` sirven para cargar o empaquetar los recursos de la demo. `demo_start.bat` y `demo_start.ps1` ofrecen un arranque alternativo.

## Pipeline MLOps

1. El chatbot de Groq recoge la configuración del entrenamiento.
2. Se ejecuta `1_train_kfold.py` para CNN o `2_train_transformer_kfold.py` para Transformer.
3. Se generan análisis XAI cualitativo y cuantitativo.
4. `3_evaluate_statistics.py` calcula el ranking y las pruebas de Wilcoxon.
5. La validación externa utiliza `4_external_validation.py` y `5_evaluate_delong.py`.
6. Se genera un informe con métricas, curvas ROC, comparaciones estadísticas y mapas XAI.

## Pruebas y herramientas

```bash
pytest
ruff check .
mypy
```

La configuración de coverage exige una cobertura mínima del 70 %. Los comandos equivalentes también están disponibles en `run_tests.sh` y `run_tests.bat`.

## Licencia

El proyecto principal utiliza la licencia indicada en `LICENSE`. El código de benchmarking ubicado en `pneumoniacnn-main/` conserva su licencia BSD 3-Clause.
