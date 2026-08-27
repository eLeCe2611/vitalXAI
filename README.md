# vitalXAI — Plataforma de Diagnóstico Asistido por IA para Rayos X de Tórax

Plataforma web MLOps para detección de neumonía en radiografías de tórax con **explicabilidad (XAI)**, entrenamiento de modelos y comparación estadística. Combina una interfaz clínica (diagnóstico, mapas de calor, informes PDF) con un laboratorio de entrenamiento que ejecuta pipelines CNN y Transformer con validación cruzada, análisis XAI cualitativo/cuantitativo y validación externa.

## Arquitectura

```
vitalXAI/
├── main.py                         # FastAPI entry point
├── database.py                     # Conexión MySQL (XAMPP)
├── requirements.txt
├── routers/
│   ├── auth.py                     # Login, registro, dashboard
│   ├── inference.py                # Predicción + XAI + PDF
│   ├── history.py                  # Historial de consultas
│   └── trainer.py                  # Chatbot Groq + pipeline MLOps
├── services/
│   ├── ml_engine.py                # Carga de modelos CNN/Transformer
│   ├── xai_generator.py            # Saliency, SmoothGrad, Grad-CAM / Attention
│   ├── pdf_generator.py            # Informe PDF de diagnóstico
│   └── trainer_engine.py           # Motor de entrenamiento interno
├── templates/                      # Jinja2 HTML
├── static/
│   ├── uploads/                    # Radiografías subidas por el usuario
│   ├── results/                    # Mapas XAI generados
│   └── reports/                    # PDFs generados
├── training_results/               # Resultados de sesiones MLOps
└── pneumoniacnn-main/              # Benchmarking research submodule
    ├── code/                       # Scripts de entrenamiento, evaluación, XAI
    ├── results/                    # Pesos de modelos y resultados
    ├── Images/                     # Dataset de entrenamiento (ignorado por git)
    └── ExternalDataset/            # Dataset de validación externa (ignorado por git)
```

## Modelos Soportados

| Tipo | Modelos |
|------|---------|
| **CNN** | ResNet50, ResNet101, ResNet152, ResNet50V2, EfficientNetB0/B3/B7, EfficientNetV2S, DenseNet121, DenseNet201, MobileNetV2, MobileNetV3Large, VGG16, InceptionV3, Xception, ConvNeXtTiny |
| **Transformer** | DeiT (facebook/deit-base-distilled-patch16-224), Swin-Base (microsoft/swin-base-patch4-window7-224), ViT-384 (google/vit-base-patch16-384) |

## Técnicas XAI

- **Saliency Maps** — Gradientes de la clase predicha respecto a la imagen
- **SmoothGrad** — Promediado de mapas de sensibilidad con ruido gaussiano
- **Grad-CAM** — Mapas de activación de clase para CNN
- **Attention Maps** — Mapas de atención para modelos Transformer

## Requisitos

- Python ≥ 3.11
- XAMPP (MySQL) o base de datos MySQL compatible
- Clave de API de [Groq](https://console.groq.com) para el chatbot

## Inicio Rápido

```bash
git clone <repo>
cd vitalXAI
pnpm install                # (o python -m venv .venv && pip install -r requirements.txt)
```

1. Inicia MySQL en XAMPP y crea la base de datos `tfg_pneumonia`
2. Copia `.env.example` a `.env` y añade tu `GEMINI_API_KEY` y `GROQ_API_KEY`
3. Ejecuta la aplicación:

```bash
python main.py
# Servidor en http://127.0.0.1:8000
```

## Pipeline MLOps

1. El chatbot de Groq (`openai/gpt-oss-120b`) conversa con el usuario para capturar configuración
2. Se ejecutan los scripts `1_train_kfold.py` o `2_train_transformer_kfold.py` según el modelo
3. Se genera automáticamente XAI cualitativo (script 6) y cuantitativo (script 7)
4. Al finalizar todos los modelos, se ejecuta `3_evaluate_statistics.py` (ranking + Wilcoxon)
5. La validación externa opcional ejecuta `4_external_validation.py` + `5_evaluate_delong.py`
6. Se genera un informe PDF completo con métricas, tablas de ranking, matriz Wilcoxon, curvas ROC y mapas XAI

## Licencia

Parte del código de benchmarking (`pneumoniacnn-main/`) tiene licencia BSD 3-Clause.
